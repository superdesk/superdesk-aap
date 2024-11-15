import datetime
from unittests import AAPTestCase
from .rolling_broadcast import rolling_broadcast
from superdesk.utc import utcnow
from copy import deepcopy


class TestRollingBroadcast(AAPTestCase):
    published = [
        {
            "_id": "1111",
            "item_id": "urn:newsml:aap.com.au:2024-05-27T12:05:39.890501:b4ba91e7-1272-4d9d-887a-9c43df5934d9",
            "family_id": "urn:newsml:aap.com.au:2024-05-27T12:05:39.890501:b4ba91e7-1272-4d9d-887a-9c43df5934d9",
            "state": "published",
            "type": "text",
            "last_published_version": True,
            "genre": {"code": "Article"},
            "slugline": "Markets Aust",
            "anpa_category": [{"qcode": "f"}],
            "urgency": None,
            "pubstatus": "usable",
            "firstcreated": utcnow() - datetime.timedelta(hours=1),
            "headline": "Australian shares rebound from losses at midday",
            "versioncreated": utcnow() - datetime.timedelta(hours=1),
            "body_html": "<p>Finance Story one hour old</p>"
            + "<p>1</p><p>1</p><p>1</p><p>1</p><p>1</p><p>1</p><p>1</p><p>1</p><p>1</p><p>1</p><p>1</p>"
            * 200,
        },
        {
            "_id": "2222",
            "item_id": "urn:newsml:aap.com.au:2024-05-27T10:01:41.293453:410954b3-3612-49a5-b11f-40b81c2e4a82",
            "rewrite_of": "urn:newsml:aap.com.au:2024-07-09T08:21:22.215191:ca76857b-199b-41c8-9b91-6b6e210e40d7",
            "rewrite_sequence": 1,
            "state": "published",
            "type": "text",
            "last_published_version": True,
            "genre": {"code": "Article"},
            "slugline": "Oly24 Row Aust",
            "keywords": ["OLY", "Women"],
            "anpa_category": [{"qcode": "s"}, {"qcode": "a"}],
            "urgency": 2,
            "pubstatus": "usable",
            "firstcreated": utcnow() - datetime.timedelta(hours=1),
            "headline": "Aussie rowers bag four World Cup silver medals",
            "versioncreated": utcnow() - datetime.timedelta(hours=1),
            "body_html": "<p>Sport and News Story one hour old and has been rewritten adds weight</p>"
            + "<p>2</p><p>2</p><p>2</p><p>2</p><p>2</p><p>2</p><p>2</p><p>2</p><p>2</p><p>2</p><p>2</p>"
            * 200,
        },
        {
            "_id": "3333",
            "item_id": "urn:newsml:aap.com.au:2024-05-27T11:26:51.232837:72fda625-011d-41bd-9336-c7e05ac7934e",
            "state": "published",
            "last_published_version": True,
            "type": "text",
            "genre": {"code": "Article"},
            "slugline": "PNG Aust",
            "anpa_category": [{"qcode": "a"}],
            "urgency": 1,
            "pubstatus": "usable",
            "firstcreated": utcnow() - datetime.timedelta(hours=1),
            "headline": "Time 'not on side' for people trapped in PNG landslide",
            "versioncreated": utcnow() - datetime.timedelta(hours=1),
            "body_html": "<p>News one hour old</p>"
            + "<p>3</p><p>3</p><p>3</p><p>3</p><p>3</p><p>3</p><p>3</p><p>3</p><p>3</p><p>3</p><p>3</p>"
            * 200,
        },
        {
            "_id": "4444",
            "item_id": "urn:newsml:aap.com.au:2024-05-27T11:08:09.739087:6cdefd94-e4ac-4ede-8f21-bc6b1703c96c",
            "state": "published",
            "type": "text",
            "genre": {"code": "Article"},
            "slugline": "Palestine Aust",
            "last_published_version": True,
            "anpa_category": [{"qcode": "a"}],
            "urgency": 1,
            "pubstatus": "usable",
            "firstcreated": utcnow() - datetime.timedelta(hours=4),
            "headline": "Cops arrive at Gaza protest as students refuse to budge",
            "versioncreated": utcnow() - datetime.timedelta(hours=4),
            "body_html": "<p>Finance Story four hours old</p>"
            + "<p>4</p><p>4</p><p>4</p><p>4</p><p>4</p><p>4</p><p>4</p><p>4</p><p>4</p><p>4</p><p>4</p>"
            * 200,
        },
        {
            "_id": "5555",
            "item_id": "urn:newsml:aap.com.au:2024-07-09T08:21:22.215191:ca76857b-199b-41c8-9b91-6b6e210e40d7",
            "rewritten_by": "urn:newsml:aap.com.au:2024-05-27T10:01:41.293453:410954b3-3612-49a5-b11f-40b81c2e4a82",
            "state": "published",
            "type": "text",
            "genre": {"code": "Article"},
            "slugline": "Palestine Aust",
            "last_published_version": True,
            "anpa_category": [{"qcode": "a"}],
            "urgency": 1,
            "pubstatus": "usable",
            "firstcreated": utcnow() - datetime.timedelta(hours=2),
            "headline": "Cops arrive at Gaza protest as students refuse to budge",
            "versioncreated": utcnow() - datetime.timedelta(hours=2),
            "body_html": "<p>Updated Story 2 hours old</p>"
            + "<p>4</p><p>4</p><p>4</p><p>4</p><p>4</p><p>4</p><p>4</p><p>4</p><p>4</p><p>4</p><p>4</p>"
            * 200,
        },
        {
            "processed_from": "urn:newsml:aap.com.au:2024-05-27T12:05:39.890501:b4ba91e7-1272-4d9d-887a-9c43df5934d9",
            "state": "published",
            "type": "text",
            "pubstatus": "usable",
            "last_published_version": True,
            "genre": {"qcode": "Broadcast Script"},
            "versioncreated": utcnow() - datetime.timedelta(hours=1),
        },
        {
            "processed_from": "urn:newsml:aap.com.au:2024-05-27T10:01:41.293453:410954b3-3612-49a5-b11f-40b81c2e4a82",
            "state": "published",
            "type": "text",
            "pubstatus": "usable",
            "last_published_version": True,
            "genre": {"qcode": "Broadcast Script"},
            "versioncreated": utcnow() - datetime.timedelta(hours=1),
        },
        {
            "processed_from": "urn:newsml:aap.com.au:2024-05-27T11:26:51.232837:72fda625-011d-41bd-9336-c7e05ac7934e",
            "state": "published",
            "type": "text",
            "pubstatus": "usable",
            "last_published_version": True,
            "genre": {"qcode": "Broadcast Script"},
            "versioncreated": utcnow() - datetime.timedelta(hours=1),
        },
        {
            "processed_from": "urn:newsml:aap.com.au:2024-05-27T11:08:09.739087:6cdefd94-e4ac-4ede-8f21-bc6b1703c96c",
            "state": "published",
            "type": "text",
            "pubstatus": "usable",
            "last_published_version": True,
            "genre": {"qcode": "Broadcast Script"},
            "versioncreated": utcnow() - datetime.timedelta(hours=1),
        },
        {
            "processed_from": "urn:newsml:aap.com.au:2024-07-09T08:21:22.215191:ca76857b-199b-41c8-9b91-6b6e210e40d7",
            "state": "published",
            "type": "text",
            "pubstatus": "usable",
            "last_published_version": True,
            "genre": {"qcode": "Broadcast Script"},
            "versioncreated": utcnow() - datetime.timedelta(hours=1),
        },
    ]

    def test_sort_boost(self):
        self.app.data.insert("published", self.published)
        item = rolling_broadcast({"slugline": "fish"})
        self.assertEquals(item.get("slugline"), "Rolling News Bulletin")
        first = item.get("body_html").find("Oly24 Row Aust")
        second = item.get("body_html").find("PNG Aust")
        third = item.get("body_html").find("Palestine Aust")
        fourth = item.get("body_html").find("Markets Aust")
        order = [first, second, third, fourth]
        self.assertTrue(all(order[i] < order[i + 1] for i in range(len(order) - 1)))
        self.assertNotIn("Old Story", item.get("body_html"))

    def test_remove_time_limits(self):
        with_old_item = deepcopy(self.published)
        with_old_item.append(
            {
                "_id": "6666",
                "item_id": "urn:newsml:aap.com.au:2024-07-09T08:21:22.215191:ca76857b-199b-41c8-9b91-6b6e210e40d8",
                "state": "published",
                "type": "text",
                "genre": {"code": "Article"},
                "slugline": "Old Story",
                "last_published_version": True,
                "anpa_category": [{"qcode": "a"}],
                "urgency": 1,
                "pubstatus": "usable",
                "firstcreated": utcnow() - datetime.timedelta(hours=13),
                "headline": "Somthing from Some time ago",
                "versioncreated": utcnow() - datetime.timedelta(hours=13),
                "body_html": "<p>Somthing from Some time ago</p>"
                + "<p>6</p><p>6</p><p>6</p><p>6</p><p>6</p><p>6</p><p>6</p><p>6</p><p>6</p><p>6</p><p>6</p>"
                * 200,
            }
        )
        self.app.data.insert("published", with_old_item)
        item = rolling_broadcast({"slugline": "NOIDCHECK NOTIMELIMIT"})
        self.assertIn("Old Story", item.get("body_html"))
        item = rolling_broadcast({"slugline": "NOTIMELIMIT"})
        self.assertNotIn("Old Story", item.get("body_html"))

    def test_id_check(self):
        with_old_item = deepcopy(self.published)
        with_old_item.append(
            {
                "_id": "6666",
                "item_id": "urn:newsml:aap.com.au:2024-07-09T08:21:22.215191:ca76857b-199b-41c8-9b91-6b6e210e40d8",
                "state": "published",
                "type": "text",
                "genre": {"code": "Article"},
                "slugline": "Story",
                "last_published_version": True,
                "anpa_category": [{"qcode": "a"}],
                "urgency": 1,
                "pubstatus": "usable",
                "firstcreated": utcnow() - datetime.timedelta(hours=1),
                "headline": "Recent story with no Broadcast version",
                "versioncreated": utcnow() - datetime.timedelta(hours=1),
                "body_html": "<p>Recent story with no Broadcast version</p>"
                + "<p>6</p><p>6</p><p>6</p><p>6</p><p>6</p><p>6</p><p>6</p><p>6</p><p>6</p><p>6</p><p>6</p>"
                * 200,
            }
        )
        self.app.data.insert("published", with_old_item)
        item = rolling_broadcast({"slugline": "test"})
        self.assertNotIn(
            "Recent story with no Broadcast version", item.get("body_html")
        )

        item = rolling_broadcast({"slugline": "NOIDCHECK"})
        self.assertIn("Recent story with no Broadcast version", item.get("body_html"))

    def test_remove_killed_family(self):
        with_old_item = deepcopy(self.published)
        with_old_item.append(
            {
                "_id": "6666",
                "item_id": "urn:newsml:aap.com.au:2024-07-09T08:21:22.215191:ca76857b-199b-41c8-9b91-6b6e210e40d8",
                "family_id": "urn:newsml:aap.com.au:2024-05-27T12:05:39.890501:b4ba91e7-1272-4d9d-887a-9c43df5934d9",
                "state": "killed",
                "type": "text",
                "genre": {"code": "Article"},
                "slugline": "Old Story",
                "last_published_version": True,
                "anpa_category": [{"qcode": "a"}],
                "urgency": 1,
                "pubstatus": "canceled",
                "firstcreated": utcnow() - datetime.timedelta(hours=13),
                "headline": "Somthing from Some time ago",
                "versioncreated": utcnow() - datetime.timedelta(hours=13),
                "body_html": "Killed",
            }
        )
        self.app.data.insert("published", with_old_item)
        item = rolling_broadcast({})
        self.assertNotIn("Finance Story one hour old", item.get("body_html"))

    def test_bad_state(self):
        update = {
            "fields_meta": {
                "body_html": {
                    "draftjsState": [
                        {
                            "blocks": [
                                {
                                    "key": "nqk8",
                                    "text": " ",
                                    "type": "unstyled",
                                    "depth": 0,
                                    "inlineStyleRanges": [],
                                    "entityRanges": [],
                                    "data": {"MULTIPLE_HIGHLIGHTS": {}},
                                },
                                {
                                    "key": "169iu",
                                    "text": " ",
                                    "type": "atomic",
                                    "depth": 0,
                                    "inlineStyleRanges": [],
                                    "entityRanges": [
                                        {"offset": 0, "length": 1, "key": 0}
                                    ],
                                    "data": {},
                                },
                                {
                                    "key": "2l5j1",
                                    "text": "",
                                    "type": "unstyled",
                                    "depth": 0,
                                    "inlineStyleRanges": [],
                                    "entityRanges": [],
                                    "data": {},
                                },
                            ],
                            "entityMap": {},
                        }
                    ]
                }
            }
        }
        self.app.data.insert("published", self.published)
        self.app.data.update(
            "published", self.published[2]["_id"], update, self.published[2]
        )
        item = rolling_broadcast({"_id": "123"})
        self.assertTrue("body_html" in item)
