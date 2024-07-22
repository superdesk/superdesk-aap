# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2018 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


from superdesk.metadata.item import (
    ITEM_STATE,
    CONTENT_STATE,
    ITEM_TYPE,
    CONTENT_TYPE,
    FORMAT,
    FORMATS,
)
from superdesk.macros.internal_destination_auto_publish import (
    internal_destination_auto_publish,
)
from apps.archive.common import BROADCAST_GENRE
from superdesk.text_utils import get_text_word_count, get_text
from aap.publish.formatters.field_mappers.locator_mapper import LocatorMapper
from superdesk.errors import StopDuplication, DocumentError
from superdesk.editor_utils import remove_all_embeds
from superdesk import config
from superdesk import get_resource_service
import logging

logger = logging.getLogger(__name__)


def _get_profile_id(label):
    profile = get_resource_service("content_types").find_one(req=None, label=label)
    if profile:
        return str(profile["_id"])
    return None


BROADCAST_PROFILE = "Broadcast Story"


def broadcast_auto_publish(item, **kwargs):
    """Broadcast auto publish macro.

    :param item:
    :param kwargs:
    :return:
    """
    if item.get(ITEM_TYPE) != CONTENT_TYPE.TEXT or item.get(FORMAT) != FORMATS.HTML:
        return

    if item.get("auto_publish", False):
        return

    genre_list = (
        get_resource_service("vocabularies").find_one(req=None, _id="genre") or {}
    )
    broadcast_genre = [
        {"qcode": genre.get("qcode"), "name": genre.get("name")}
        for genre in genre_list.get("items", [])
        if genre.get("qcode") == BROADCAST_GENRE and genre.get("is_active")
    ]

    for genre in item.get("genre", []):
        if genre.get("qcode", None) == BROADCAST_GENRE:
            return

    remove_all_embeds(item)

    body_text = get_text(item.get("body_html"), lf_on_block=True)
    word_count = get_text_word_count(body_text)
    max_word_count = config.MIN_BROADCAST_TEXT_WORD_COUNT
    item["genre"] = broadcast_genre

    # prefixing the slugline with “legal: ” if required
    if (item.get("flags") or {}).get("marked_for_legal") and "slugline" in item:
        item["slugline"] = "Legal: " + item.get("slugline", "")

    # Locator on the headline (FED:, NSW:, Vic: etc. or AFL for Sport etc.)
    mapper = LocatorMapper()
    if len(item.get("anpa_category", [])):
        # set the headline to text
        item["headline"] = get_text(item.get("headline", ""), content="html")
        item["headline"] = mapper.get_formatted_headline(
            item, item.get("anpa_category")[0].get("qcode", "").upper()
        )

    # Signoff is “RTV” in the story from BOB
    item["sign_off"] = "RTV"
    # Agency content will need to have “RAW RTV” appended to the body.
    # The News Value is 5 from BOB
    item["urgency"] = 5

    # BOB strips the byline
    item.pop("byline", None)

    # BOB strips pic, Some debate that audio should be preserved
    # Any associated audio clips should be kept, any other embedded media should be removed.
    item.pop("associations", None)
    item.pop("refs", None)

    # BOB sets the takekey to location/city e.g. (SYDNEY)
    item["anpa_take_key"] = (
        "("
        + (
            ((item.get("dateline") or {}).get("located") or {}).get("city", "") or ""
        ).upper()
        + ")"
    )

    item["profile"] = _get_profile_id(BROADCAST_PROFILE)

    if item[ITEM_STATE] not in {CONTENT_STATE.KILLED, CONTENT_STATE.RECALLED} and not (
        item.get("flags") or {}
    ).get("marked_for_legal"):
        if word_count > max_word_count and not (item.get("flags") or {}).get(
            "marked_for_legal"
        ):
            lines = body_text.splitlines()
            new_body_html = []
            for line in lines:
                para = line.strip()
                if not para:
                    continue

                new_body_html.append("<p>{}</p>".format(para))
                word_count = get_text_word_count("".join(new_body_html))
                if word_count >= max_word_count:
                    if len(new_body_html):
                        item["body_html"] = "".join(new_body_html)
                        item["word_count"] = word_count
                    break
    elif item[ITEM_STATE] in {CONTENT_STATE.KILLED, CONTENT_STATE.RECALLED}:
        # Kill is not required
        return

    try:
        if ("desk" in kwargs and "stage" in kwargs) or (
            "dest_desk_id" in kwargs and "dest_stage_id" in kwargs
        ):
            internal_destination_auto_publish(item)
    except StopDuplication:
        logger.info("macro done item=%s", item.get("_id"))
    except DocumentError as err:
        logger.error(
            "validation error when creating brief item=%s error=%s",
            item.get("_id"),
            err,
        )
    except Exception as err:
        logger.exception(err)
    return item


name = "broadcast_auto_publish"
label = "Broadcast Auto Publish"
callback = broadcast_auto_publish
access_type = "frontend"
action_type = "direct"
