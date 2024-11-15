import logging
from typing import List, Dict, Set
from io import StringIO
from datetime import datetime, timedelta
import calendar
from eve.utils import ParsedRequest
from superdesk import get_resource_service
import json
from superdesk.utils import config
from superdesk.utc import utcnow
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE
from superdesk.text_utils import get_text_word_count, get_text, get_word_count
from superdesk.editor_utils import Editor3Content, remove_all_embeds
from aap.macros.broadcast_auto_publish import _get_profile_id, BROADCAST_PROFILE

logger = logging.getLogger(__name__)


def abbreviate_item_body(item: dict):
    lines = get_text(item.get("body_html", "<p></p>"), lf_on_block=True).splitlines()
    new_body_html = []
    for line in lines:
        para = line.strip()
        if not para:
            continue

        new_body_html.append("<p>{}</p>".format(para))
        word_count = get_text_word_count("".join(new_body_html))
        if word_count >= config.MIN_BROADCAST_TEXT_WORD_COUNT:
            if len(new_body_html):
                item["body_html"] = "".join(new_body_html)
                item["word_count"] = word_count
            break


def time_rounder(time: datetime):
    """
    Round the passed datetime to the next hour or half hour
    :param time:
    :return:
    """
    # Get the current time
    current_minute = time.minute
    # Calculate minutes to next half hour or hour
    minutes_to_next = (
        (30 - current_minute % 30) if current_minute < 30 else (60 - current_minute)
    )
    # Calculate the delta time to add
    delta = timedelta(minutes=minutes_to_next)
    # Return the adjusted time
    return time + delta


def write_body(body: StringIO, articles: List[dict]):
    """
    Writes to the body string an entry for each article in the past list of articles
    :param body:
    :param articles:
    :return:
    """
    for article in articles:
        abbreviate_item_body(article)
        body.write("<p><br></p><p><br></p>")
        slugline = article.get("slugline", "")
        if (article.get("flags") or {}).get(
            "marked_for_legal"
        ) and "slugline" in article:
            slugline = "Legal: " + article.get("slugline", "")
        city = article.get("dateline", {}).get("located", {}).get("city", "").upper()
        if city:
            body.write(f"<p>{slugline} ({city})</p>")
        else:
            body.write(f"<p>{slugline}</p>")
        body.write(article.get("body_html", ""))


def get_article_category_codes(article: Dict) -> Set:
    return set([c.get("qcode", "").lower() for c in article.get("anpa_category", [])])


def get_broadcast_story_parent_ids() -> List:
    """
    Get a list of the id's of the stories the broadcast stories have been derived from.
    :return: List of story id's
    """
    query = {
        "query": {
            "bool": {
                "must": [
                    {"terms": {"state": ["published", "corrected"]}},
                    {"match": {"pubstatus": "usable"}},
                    {"match": {"last_published_version": True}},
                    {"match": {"genre.qcode": "Broadcast Script"}},
                    {"exists": {"field": "processed_from"}},
                ]
            }
        }
    }
    service = get_resource_service("published")
    req = ParsedRequest()
    req.sort = '[("versioncreated", -1)]'
    req.args = {"source": json.dumps(query)}
    req.projection = json.dumps({"processed_from": 1})
    req.max_results = 100
    return [bs.get("processed_from") for bs in list(service.get(req=req, lookup=None))]


def get_killed_families() -> Set:
    """
    Return a set of families with a killed member, so we can exclude any stories with a hint of death
    :return:
    """
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"state": "killed"}},
                    {"match": {"pubstatus": "canceled"}},
                ]
            }
        }
    }
    service = get_resource_service("published")
    req = ParsedRequest()
    req.sort = '[("versioncreated", -1)]'
    req.args = {"source": json.dumps(query)}
    req.projection = json.dumps({"family_id": 1})
    req.max_results = 100
    return set(bs.get("family_id") for bs in list(service.get(req=req, lookup=None)))


def rolling_broadcast(item, **kwargs):
    """
    Rolls up the most recently published broadcast articles into a single article.
    :param item:
    :param kwargs:
    :return:
    """
    now = datetime.now()
    # Get the time for the bulletin in general the articles will be generated at quarter to the hour and quarter past
    # the hour for the hour and half hour respectively
    bulletin_time = time_rounder(now)

    # Sort them as follows
    # updated in the last three hours,
    # news value,
    # the difference between the creation and the last update > 6 minutes, WEIRD DONT UNDERSTAND
    # then by update time.
    runtime = utcnow()

    def sort_weight(article):
        updated = 0
        # if article.get("rewrite_created"):
        #     age = runtime - article["rewrite_created"]
        #     if age.seconds < 60 * 60 * 3 and article.get('rewrite_created'):
        #         updated = 1
        age = runtime - article["versioncreated"]
        if age.seconds < 60 * 60 * 3 and article.get("rewrite_sequence"):
            updated = 1

        urgency = article.get("urgency", 10) or 10
        version_created_timestamp = calendar.timegm(
            article.get("versioncreated").timetuple()
        )

        # Calculate the weight as a concatenated string
        weight = str(updated) + str(10 - int(urgency)) + str(version_created_timestamp)
        article["weight"] = weight
        return weight

    # Determine if we should apply a 12Hour time limit on potential stories, default True
    time_limit = False if "NOTIMELIMIT" in item.get("slugline", "").upper() else True
    # Determine if we should verify the existence of an associated Broadcast story, Default True
    id_check = False if "NOIDCHECK" in item.get("slugline", "").upper() else True
    # Determin if we should publish
    publish = False if "NOPUB" in item.get("slugline", "").upper() else True

    updates = {}
    updates[
        "headline"
    ] = f'AAP Rolling News Bulletin {bulletin_time.strftime(" %B %-d, %H%M")}'
    # Fixed slugline to identify the rolling bulletins
    slugline = "Rolling News Bulletin"
    updates["slugline"] = slugline
    updates["anpa_take_key"] = bulletin_time.strftime("%H%M")
    updates["genre"] = [{"name": "Broadcast Script", "qcode": "Broadcast Script"}]
    updates["priority"] = 6
    updates["urgency"] = 5

    updates["profile"] = _get_profile_id(BROADCAST_PROFILE)

    body = StringIO()
    # AAP Rolling News Bulletin for Jun 07 at 1400
    body.write(
        "<p>AAP Rolling News Bulletin for " + bulletin_time.strftime("%B %-d at %H%M")
    )
    body.write("</p>")
    body.write("<p>\u000e</p><p>\u000e</p>")

    try:
        ids = get_broadcast_story_parent_ids()
        service = get_resource_service("published")
        req = ParsedRequest()
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"terms": {"state": ["published", "corrected"]}},
                        {"match": {"pubstatus": "usable"}},
                        {"match": {"last_published_version": True}},
                        {"match": {"type": "text"}},
                    ],
                    "must_not": [
                        {"match": {"slugline": slugline}},
                        {"match": {"genre.qcode": "Broadcast Script"}},
                        {"wildcard": {"genre.qcode": "*FactCheck*"}},
                        {"match": {"keywords": "marketplace"}},
                        {"match": {"auto_publish": "true"}},
                    ],
                }
            }
        }
        if time_limit:
            query["query"]["bool"]["must"].append(
                {"range": {"versioncreated": {"gte": "now-12H"}}}
            )
            logger.warning("Applying 12 Hour limit")
        else:
            logger.warning("NOT Applying 12 Hour limit")
        if id_check:
            query["query"]["bool"]["must"].append({"terms": {"item_id": ids}})
            logger.warning("Applying Broadcast Story ID Check")
        else:
            logger.warning("NOT applying Broadcast Story ID check")

        req.sort = '[("versioncreated", -1),("urgency", 1)]'
        req.args = {"source": json.dumps(query)}
        req.max_results = 100
        articles = list(service.get(req=req, lookup=None))

        articles.sort(key=sort_weight, reverse=True)

        logger.warning(f"Articles Found {len(articles)}")
        # Need 10 stories ordered by News Value (urgency) updated in the last 3 hours
        news_stories = []
        sport_stories = []
        entertainment_stories = []
        finance_stories = []

        # Create a set of item_ids that have been rewritten
        rewritten_ids = {
            article.get("rewritten_by")
            for article in articles
            if "rewritten_by" in article
        }

        killed_families = get_killed_families()

        for article in articles:
            # check if the article is in the list of rewritten ones, if it is then ignore the article
            if article.get("item_id") in rewritten_ids:
                continue
            # ignore those killed and their families
            if (
                article.get("state") == "killed"
                or article.get("family_id") in killed_families
            ):
                continue

            # Sometimes there is an inconsistency in the editor state that kills the function
            try:
                remove_all_embeds(article)
            except Exception as e:
                logger.warning(
                    f"Failed to remove embeds from {article.get('item_id')} Exception {str(e)}"
                )
                continue

            category_codes = get_article_category_codes(article)
            logger.warning(
                f"{article.get('weight')} {article.get('slugline')}:{article.get('headline')}  cat{category_codes}"
            )
            if len(news_stories) < 8 and category_codes & {"a", "i"}:
                news_stories.append(article)
            elif len(sport_stories) < 2 and category_codes & {"s", "t"}:
                sport_stories.append(article)
            elif len(finance_stories) < 2 and category_codes & {"f"}:
                finance_stories.append(article)
            elif len(entertainment_stories) < 2 and category_codes & {"e"}:
                entertainment_stories.append(article)

        updates["body_html"] = "<p></p>"
        write_body(body, news_stories)

        if len(finance_stories):
            body.write("<p><br></p><p><br></p><p>In finance ...</p>")
            write_body(body, finance_stories)
        if len(entertainment_stories):
            body.write("<p><br></p><p><br></p><p>In entertainment ...</p>")
            write_body(body, entertainment_stories)
        if len(sport_stories):
            body.write("<p><br></p><p><br></p><p>In sport ...</p>")
            write_body(body, sport_stories)

        body.write(
            "<p>Ends Bulletin</p><p>Rolling News Desk inquiries : 02 9322 8611</p>"
        )

        updates["body_html"] = body.getvalue()
        updates["word_count"] = get_word_count(updates.get("body_html", ""))
        try:
            ed = Editor3Content(updates, reload=True)
            ed.update_item()
        except Exception as e:
            logger.warning(
                f"Failed to generate editor state for {item[config.ID_FIELD]}, Exception {str(e)}"
            )
            pass

        body.close()

    except Exception as e:
        logger.exception("Retrieving broadcast articles raised exception: {}".format(e))
        pass

    # If the macro is being executed by a scheduled template then publish the item as well
    if "desk" in kwargs and "stage" in kwargs and publish:
        logger.warning(f"Auto publishing {item.get('_id')} {updates.get('headline')}")
        updates["state"] = "submitted"
        get_resource_service("archive").system_update(
            item[config.ID_FIELD], updates, item
        )

        get_resource_service("archive_publish").patch(
            id=item[config.ID_FIELD],
            updates={ITEM_STATE: CONTENT_STATE.PUBLISHED, "auto_publish": True},
        )
        return get_resource_service("archive").find_one(
            req=None, _id=item[config.ID_FIELD]
        )
    else:
        logger.warning(
            f"NOT Auto publishing {item.get('_id')} {updates.get('headline')}"
        )

    item.update(updates)
    return item


name = "Rolling Broadcast Bulletin"
label = "Rolling Broadcast Bulletin"
callback = rolling_broadcast
access_type = "frontend"
action_type = "direct"
