Feature: AM Snaps Test
    Background:
        Given the "validators"
        """
        [
            {
                "schema": {},
                "type": "text",
                "act": "publish",
                "_id": "publish_text"
            },
            {
                "_id": "publish_composite",
                "act": "publish",
                "type": "composite",
                "schema": {}
            }
        ]
        """
        When we post to "/desks" with "SPORTS_DESK" and success
        """
        [{"name": "Sports", "content_expiry": 60}]
        """
        Given "archive"
            """
            [{"guid": "123", "type": "text", "headline": "test", "state": "fetched",
            "task": {"desk": "#desks._id#", "stage": "#desks.incoming_stage#", "user": "#CONTEXT_USER_ID#"},
            "subject":[{"qcode": "17004000", "name": "Statistics"}],
            "genre": [{"qcode": "Article", "name": "Article"}],
            "slugline": "test 123",
            "priority": 2, "urgency": 2,
            "place": [{"qcode": "QLD", "name": "QLD"}],
            "body_html": "Test Document body",
            "sms_message": "This is sms contains & (100 ) < # characters",
            "flags": {"marked_for_sms": true},
            "dateline": {
                "located" : {
                    "country" : "Afghanistan",
                    "tz" : "Asia/Kabul",
                    "city" : "Mazar-e Sharif",
                    "alt_name" : "",
                    "country_code" : "AF",
                    "city_code" : "Mazar-e Sharif",
                    "dateline" : "city",
                    "state" : "Balkh",
                    "state_code" : "AF.30"
                },
                "text" : "MAZAR-E SHARIF, Dec 30  -",
                "source": "AAP"
                }
            },
            {"guid": "456", "type": "text", "headline": "test", "state": "fetched",
            "task": {"desk": "#desks._id#", "stage": "#desks.incoming_stage#", "user": "#CONTEXT_USER_ID#"},
            "subject":[{"qcode": "17004000", "name": "Statistics"}],
            "genre": [{"qcode": "Article", "name": "Article"}],
            "slugline": "test 456",
            "priority": 2, "urgency": 2,
            "body_html": "Test Document body",
            "sms_message": "This is sms contains & (100 ) < # characters",
            "flags": {"marked_for_sms": true},
            "dateline": {
                "located" : {
                    "country" : "Afghanistan",
                    "tz" : "Asia/Kabul",
                    "city" : "Mazar-e Sharif",
                    "alt_name" : "",
                    "country_code" : "AF",
                    "city_code" : "Mazar-e Sharif",
                    "dateline" : "city",
                    "state" : "Balkh",
                    "state_code" : "AF.30"
                },
                "text" : "MAZAR-E SHARIF, Dec 30  -",
                "source": "AAP"
                }
            }]
        """
        When we post to "/desks" with "SNAP_DESK" and success
        """
        [{"name": "Snap Desk", "content_expiry": 60}]
        """
        And we post to "/internal_destinations"
        """
        [
            {
                "name" : "Snaps for Snap Test",
                "stage" : "#desks.incoming_stage#",
                "desk" : "#desks._id#",
                "is_active" : true,
                "macro" : "am_snaps_auto_publish"
            },
            {
                "macro" : "am_service_content",
                "stage" : "#desks.incoming_stage#",
                "desk" : "#desks._id#",
                "name" : "copy snap",
                "is_active" : true
            }
        ]
        """
        Then we get OK response

    @auth
    @vocabularies
    Scenario: Auto Publish snap via Internal Destinations
        When we get "/archive"
        Then we get list with 2 items
        """
        {
            "_items": [
                {"_id": "123", "state":"fetched"},
                {"_id": "456", "state":"fetched"}
            ]
        }
        """
        When we publish "123" with "publish" type and "published" state
        Then we get OK response
        When we get "/published"
        Then we get list with 2 items
        """
        {
            "_items": [
                {
                    "state": "published",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "slugline": "test 123",
                    "genre": [{"qcode": "Article", "name": "Article"}]
                },
                {
                    "state": "published",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 123",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}],
                    "place": [{"qcode": "FED", "name": "FED"}],
                    "anpa_take_key": "snap",
                    "abstract": "This is sms contains & (100 ) < # characters",
                    "body_html": "This is sms contains & (100 ) < # characters",
                    "sms_message": "__no_value__",
                    "original_id" : "123",
                    "priority": 2, "urgency": 2,
                    "headline": "test",
                    "flags": {
                        "marked_for_sms": false
                    }
                }
            ]
        }
        """
        When we get "/archive"
        Then we get list with 2 items
        """
        {
            "_items": [
                {"_id": "456", "state":"fetched", "task": {"desk": "#SPORTS_DESK#"}},
                {
                    "original_id": "123",
                    "state": "routed",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 123",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}]
                }
            ]
        }
        """

    @auth
    @vocabularies
    Scenario: Auto Publish snap with same sms message won't create another snap
        When we get "/archive"
        Then we get list with 2 items
        """
        {
            "_items": [
                {"_id": "123", "state":"fetched"},
                {"_id": "456", "state":"fetched"}
            ]
        }
        """
        When we publish "123" with "publish" type and "published" state
        Then we get OK response
        When we get "/published"
        Then we get list with 2 items
        """
        {
            "_items": [
                {
                    "state": "published",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "slugline": "test 123",
                    "genre": [{"qcode": "Article", "name": "Article"}]
                },
                {
                    "state": "published",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 123",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}],
                    "anpa_take_key": "snap",
                    "abstract": "This is sms contains & (100 ) < # characters",
                    "body_html": "This is sms contains & (100 ) < # characters",
                    "sms_message": "__no_value__",
                    "original_id" : "123",
                    "priority": 2, "urgency": 2,
                    "headline": "test",
                    "flags": {
                        "marked_for_sms": false
                    }
                }
            ]
        }
        """
        When we get "/archive"
        Then we get list with 2 items
        """
        {
            "_items": [
                {"_id": "456", "state":"fetched"},
                {
                    "original_id": "123",
                    "state": "routed",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 123",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}]
                }
            ]
        }
        """
        When we publish "456" with "publish" type and "published" state
        Then we get OK response
        When we get "/published"
        Then we get list with 3 items
        """
        {
            "_items": [
                {
                    "_id": "123",
                    "state": "published",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "slugline": "test 123",
                    "genre": [{"qcode": "Article", "name": "Article"}]
                },
                {
                    "_id": "456",
                    "state": "published",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "slugline": "test 456",
                    "genre": [{"qcode": "Article", "name": "Article"}]
                },
                {
                    "state": "published",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 123",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}],
                    "anpa_take_key": "snap",
                    "abstract": "This is sms contains & (100 ) < # characters",
                    "body_html": "This is sms contains & (100 ) < # characters",
                    "sms_message": "__no_value__",
                    "original_id" : "123",
                    "priority": 2, "urgency": 2,
                    "headline": "test",
                    "flags": {
                        "marked_for_sms": false
                    }
                }
            ]
        }
        """
        When we get "/archive"
        Then we get list with 2 items
        """
        {
            "_items": [
                {
                    "original_id": "123",
                    "state": "routed",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 123",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}]
                },
                {
                    "original_id": "456",
                    "state": "routed",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 456",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}]
                }
            ]
        }
        """
        When we publish "456" with "correct" type and "corrected" state
        """
        {
            "sms_message": "This is sms contains & (100 ) < # characters",
            "flags": {"marked_for_sms": true},
            "slugline": "corrected"
        }
        """
        Then we get OK response
        When we get "/published"
        Then we get list with 4 items
        """
        {
            "_items": [
                {
                    "_id": "123",
                    "state": "published",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "slugline": "test 123",
                    "genre": [{"qcode": "Article", "name": "Article"}]
                },
                {
                    "_id": "456",
                    "state": "published",
                    "slugline": "test 456",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "genre": [{"qcode": "Article", "name": "Article"}]
                },
                {
                    "_id": "456",
                    "state": "corrected",
                    "slugline": "corrected",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "genre": [{"qcode": "Article", "name": "Article"}]
                },
                {
                    "state": "published",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 123",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}],
                    "anpa_take_key": "snap",
                    "abstract": "This is sms contains & (100 ) < # characters",
                    "body_html": "This is sms contains & (100 ) < # characters",
                    "sms_message": "__no_value__",
                    "original_id" : "123",
                    "priority": 2, "urgency": 2,
                    "headline": "test",
                    "flags": {
                        "marked_for_sms": false
                    }
                }
            ]
        }
        """
        When we get "/archive"
        Then we get list with 3 items
        """
        {
            "_items": [
                {
                    "original_id": "123",
                    "state": "routed",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 123",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}]
                },
                {
                    "original_id": "456",
                    "state": "routed",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 456",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}]
                },
                {
                    "original_id": "456",
                    "state": "routed",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM corrected",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}]
                }
            ]
        }
        """
        When we publish "123" with "correct" type and "corrected" state
        """
        {
            "sms_message": "New SMS Message",
            "flags": {"marked_for_sms": true},
            "slugline": "corrected"
        }
        """
        Then we get OK response
        When we get "/published"
        Then we get list with 6 items
        """
        {
            "_items": [
                {
                    "_id": "123",
                    "state": "published",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "slugline": "test 123",
                    "genre": [{"qcode": "Article", "name": "Article"}]
                },
                {
                    "_id": "123",
                    "state": "corrected",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "slugline": "corrected",
                    "genre": [{"qcode": "Article", "name": "Article"}]
                },
                {
                    "_id": "456",
                    "state": "published",
                    "slugline": "test 456",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "genre": [{"qcode": "Article", "name": "Article"}]
                },
                {
                    "_id": "456",
                    "state": "corrected",
                    "slugline": "corrected",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "genre": [{"qcode": "Article", "name": "Article"}]
                },
                {
                    "state": "published",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 123",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}],
                    "anpa_take_key": "snap",
                    "abstract": "This is sms contains & (100 ) < # characters",
                    "body_html": "This is sms contains & (100 ) < # characters",
                    "sms_message": "__no_value__",
                    "original_id" : "123",
                    "priority": 2, "urgency": 2,
                    "headline": "test",
                    "flags": {
                        "marked_for_sms": false
                    }
                },
                {
                    "state": "published",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline" : "AM corrected",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}],
                    "anpa_take_key": "snap",
                    "abstract" : "New SMS Message",
                    "body_html" : "New SMS Message",
                    "sms_message": "__no_value__",
                    "original_id" : "123",
                    "priority": 2, "urgency": 2,
                    "headline": "test",
                    "flags": {
                        "marked_for_sms": false
                    }
                }
            ]
        }
        """
        When we get "/archive"
        Then we get list with 4 items
        """
        {
            "_items": [
                {
                    "original_id": "123",
                    "state": "routed",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 123",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}]
                },
                {
                    "original_id": "123",
                    "state": "routed",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM corrected",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}]
                },
                {
                    "original_id": "456",
                    "state": "routed",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM test 456",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}]
                },
                {
                    "original_id": "456",
                    "state": "routed",
                    "task": {"desk": "#SNAP_DESK#"},
                    "slugline": "AM corrected",
                    "genre": [{"qcode": "AM Service", "name": "AM Service"}]
                }
            ]
        }
        """