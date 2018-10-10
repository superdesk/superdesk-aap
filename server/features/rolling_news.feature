Feature: Rolling news
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
        When we post to "/desks" with "ROLLING_NEWS_DESK" and success
        """
        [{"name": "Rolling News", "content_expiry": 60}]
        """
        And we post to "/internal_destinations"
        """
        [
            {
                "name" : "Rolling News",
                "stage" : "#desks.incoming_stage#",
                "desk" : "#desks._id#",
                "is_active" : true,
                "macro" : "broadcast_auto_publish"
            }
        ]
        """
        Then we get OK response

    @auth
    @vocabularies @
    Scenario: Auto Publish Rolling news
        When we get "/archive"
        Then we get list with 1 items
        """
        {
            "_items": [
                {"_id": "123", "state":"fetched"}
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
                    "task": {"desk": "#ROLLING_NEWS_DESK#"},
                    "genre": [{"qcode": "Broadcast Script", "name": "Broadcast Script"}],
                    "processed_from": "123",
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
        Then we get list with 0 items
        When we publish "123" with "correct" type and "corrected" state
        """
        {"slugline": "corrected", "genre": [{"qcode": "Results", "name": "Results"}]}
        """
        Then we get OK response
        When we get "/published"
        Then we get list with 4 items
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
                    "state": "corrected",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "slugline": "corrected",
                    "genre": [{"qcode": "Results", "name": "Results"}]
                },
                {
                    "state": "published",
                    "task": {"desk": "#ROLLING_NEWS_DESK#"},
                    "genre": [{"qcode": "Broadcast Script", "name": "Broadcast Script"}],
                    "processed_from": "123",
                    "original_id" : "123",
                    "slugline": "test 123",
                    "priority": 2, "urgency": 2,
                    "headline": "test",
                    "flags": {
                        "marked_for_sms": false
                    }
                },
                {
                    "state": "corrected",
                    "task": {"desk": "#ROLLING_NEWS_DESK#"},
                    "genre": [{"qcode": "Broadcast Script", "name": "Broadcast Script"}],
                    "processed_from": "123",
                    "original_id" : "123",
                    "slugline": "corrected",
                    "priority": 2, "urgency": 2,
                    "headline": "test",
                    "flags": {
                        "marked_for_sms": false
                    }
                }
            ]
        }
        """
        When we publish "123" with "kill" type and "killed" state
        Then we get OK response
        When we get "/published"
        Then we get list with 6 items
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
                    "state": "corrected",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "slugline": "corrected",
                    "genre": [{"qcode": "Results", "name": "Results"}]
                },
                {
                    "state": "killed",
                    "task": {"desk": "#SPORTS_DESK#"},
                    "slugline": "corrected"
                },
                {
                    "state": "published",
                    "task": {"desk": "#ROLLING_NEWS_DESK#"},
                    "genre": [{"qcode": "Broadcast Script", "name": "Broadcast Script"}],
                    "processed_from": "123",
                    "original_id" : "123",
                    "slugline": "test 123",
                    "priority": 2, "urgency": 2,
                    "headline": "test",
                    "flags": {
                        "marked_for_sms": false
                    }
                },
                {
                    "state": "corrected",
                    "task": {"desk": "#ROLLING_NEWS_DESK#"},
                    "genre": [{"qcode": "Broadcast Script", "name": "Broadcast Script"}],
                    "processed_from": "123",
                    "original_id" : "123",
                    "slugline": "corrected",
                    "priority": 2, "urgency": 2,
                    "headline": "test",
                    "flags": {
                        "marked_for_sms": false
                    }
                },
                {
                    "state": "killed",
                    "task": {"desk": "#ROLLING_NEWS_DESK#"},
                    "genre": [{"qcode": "Broadcast Script", "name": "Broadcast Script"}],
                    "processed_from": "123",
                    "original_id" : "123",
                    "priority": 2, "urgency": 2,
                    "flags": {
                        "marked_for_sms": false
                    }
                }
            ]
        }
        """
