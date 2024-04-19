from datetime import datetime
from superdesk.utc import utc
from superdesk.io.feed_parsers.newsml_1_2 import NewsMLOneFeedParser
from superdesk.io.registry import register_feed_parser
from superdesk.errors import ParserError
from apps.archive.common import format_dateline_to_locmmmddsrc
from superdesk.io.iptc import subject_codes
from aap.io.feeding_services.bang import MUSIC_ID, MOVIES_ID, SHOWBIZ_ID
from flask import current_app as app


class BangShowbizParser(NewsMLOneFeedParser):
    NAME = "Bang Showbiz"

    label = "Bang Showbiz Feed Parser"

    CITY = "London"
    COUNTRY_CODE = "GB"
    STATE_CODE = "GB.ENG"

    provider = None

    # Map the field/sources entries to appropriate IPTC codes
    subject_map = {MUSIC_ID: "01011000", MOVIES_ID: "01005001", SHOWBIZ_ID: "01021000"}

    def datetime(self, string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S").replace(tzinfo=utc)

    def parse(self, xml, provider=None):
        self.provider = provider
        items = []
        self.root = xml
        for newsItem in xml.findall("NewsItem"):
            item = {}
            try:
                self.parse_news_identifier(item, newsItem)
                self.parse_newslines(item, newsItem)
                self.parse_news_management(item, newsItem)
                item["subject"] = [
                    {
                        "qcode": self.subject_map[provider.get("current_id")],
                        "name": subject_codes[
                            self.subject_map[provider.get("current_id")]
                        ],
                    }
                ]
                item["body_html"] = (
                    "<p>"
                    + newsItem.find(
                        "NewsComponent/ContentItem/DataContent/body/body.content"
                    ).text.replace("<BR>", "</p><p>")
                    + "</p>"
                ).replace("\n", "")

                items.append(self.populate_fields(item))
            except Exception as ex:
                raise ParserError.newsmlOneParserError(ex, provider)
        return items

    def parse_newslines(self, item, tree):
        parsed_el = self.parse_elements(tree.find("NewsComponent/NewsLines"))
        item["headline"] = parsed_el.get("HeadLine", "").strip()
        item["abstract"] = tree.find(
            "NewsComponent/NewsLines/NewsLine/NewsLineText"
        ).text.strip()

        item.setdefault("dateline", {})
        cities = app.locators.find_cities(
            country_code=self.COUNTRY_CODE, state_code=self.STATE_CODE
        )
        located = [c for c in cities if c["city"] == self.CITY]
        if len(located) > 0:
            item["dateline"]["located"] = located[0]
            item["dateline"]["text"] = format_dateline_to_locmmmddsrc(
                located[0], item["versioncreated"], self.provider.get("source")
            )
        return True

    def parse_news_identifier(self, item, tree):
        parsed_el = self.parse_elements(tree.find("Identification/NewsIdentifier"))
        item["uri"] = item["guid"] = "urn:newsml:{}:{}:{}".format(
            self.provider.get("current_id", ""),
            self.datetime(parsed_el["DateId"]).isoformat(),
            parsed_el["NewsItemId"],
        )
        item["versioncreated"] = self.datetime(parsed_el["DateId"])
        item["firstcreated"] = self.datetime(parsed_el["DateId"])

    def parse_news_management(self, item, tree):
        # It's always entertainment
        item["anpa_category"] = [{"qcode": "e"}]


register_feed_parser(BangShowbizParser.NAME, BangShowbizParser())
