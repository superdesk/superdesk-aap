Feature: Mission Report
    Background: Initial Setup:
        Given the "vocabularies"
        """
        [{"_id": "categories", "items": [
            {"name": "National", "qcode": "a", "is_active": true},
            {"name": "Advisories", "qcode": "v", "is_active": true},
            {"name": "Racing (Turf)", "qcode": "r", "is_active": true},
            {"name": "FormGuide", "qcode": "h", "is_active": true}
        ]}, {"_id": "genre", "items": [
            {"name": "Article (news)", "qcode": "Article"},
            {"name": "Results (sport)", "qcode": "Results (sport)"}
        ]}]
        """
        And "desks"
        """
        [{
            "_id": "5b501a501d41c84c0bfced4a",
            "name": "Sports Desk",
            "members": [{"user": "#CONTEXT_USER_ID#"}]
        }]
        """
        And "stages"
        """
        [
            {
                "_id": "5b501a511d41c84c0bfced4b", "desk": "5b501a501d41c84c0bfced4a",
                "name": "stage1", "is_visible": true
            },
            {
                "_id": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a",
                "name": "stage2", "is_visible": true
            }
        ]
        """
        Given empty "archive_statistics"

    @auth
    Scenario: Generate the Mission report
        Given "archive_history"
        """
        [{
            "_id": "his1", "version": 0, "item_id": "archive1", "operation": "publish",
            "update": {"state": "published", "anpa_category": [{"qcode": "a"}], "pubstatus": "usable"}
        },
        {
            "_id": "his2", "version": 0, "item_id": "archive2", "operation": "publish",
            "update": {"state": "published", "anpa_category": [{"qcode": "v"}], "pubstatus": "usable"}
        }]
        """
        When we generate stats from archive history
        When we get "/mission_report?params={"query": {"filtered": {}}}"
        Then we get list with 1 items
        """
        {"_items": [{
            "corrections": [],
            "kills": [],
            "takedowns": [],
            "rewrites": 0,
            "sms_alerts": 0,
            "new_stories": {
                "categories": {
                    "a": 1,
                    "h": 0,
                    "r": 0,
                    "v": 1
                },
                "count": 2
            },
            "total_stories": 2
        }]}
        """

    @auth
    Scenario: Include corrections, kills, takedowns and rewrites
        Given "archive_history"
        """
        [{
            "_id": "his1", "version": 0, "item_id": "archive1", "operation": "publish",
            "update": {
                "state": "published", "anpa_category": [{"qcode": "a"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his2", "version": 0, "item_id": "archive2", "operation": "publish",
            "update": {
                "state": "published", "anpa_category": [{"qcode": "v"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his3", "version": 0, "item_id": "archive3", "operation": "publish",
            "update": {
                "state": "published", "anpa_category": [{"qcode": "v"}], "pubstatus": "usable", "rewrite_of": "archive1",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his4", "version": 0, "item_id": "archive4", "operation": "correct",
            "update": {
                "state": "corrected", "anpa_category": [{"qcode": "v"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his5", "version": 0, "item_id": "archive5", "operation": "kill",
            "update": {
                "state": "killed", "anpa_category": [{"qcode": "v"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his6", "version": 0, "item_id": "archive6", "operation": "takedown",
            "update": {
                "state": "recalled", "anpa_category": [{"qcode": "v"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        }]
        """
        When we generate stats from archive history
        When we get "/mission_report?params={"query": {"filtered": {}}}"
        Then we get list with 1 items
        """
        {"_items": [{
            "corrections": [{
                "_id": "archive4", "source": "AAP",
                "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"},
                "anpa_category": [{"qcode": "v"}], "state": "corrected"
            }],
            "kills": [{
                "_id": "archive5", "source": "AAP",
                "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"},
                "anpa_category": [{"qcode": "v"}], "state": "killed"
            }],
            "takedowns": [{
                "_id": "archive6", "source": "AAP",
                "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"},
                "anpa_category": [{"qcode": "v"}], "state": "recalled"
            }],
            "rewrites": 1,
            "sms_alerts": 0,
            "new_stories": {
                "categories": {
                    "a": 1,
                    "h": 0,
                    "r": 0,
                    "v": 4
                },
                "count": 5
            },
            "total_stories": 9
        }]}
        """

    @auth
    Scenario: Calculates count for results, fields, comment and betting
        Given "archive_history"
        """
        [{
            "_id": "his1", "version": 0, "item_id": "archive1", "operation": "publish",
            "update": {
                "state": "published", "anpa_category": [{"qcode": "a"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his2", "version": 0, "item_id": "archive2", "operation": "publish",
            "update": {
                "state": "published", "anpa_category": [{"qcode": "v"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his3", "version": 0, "item_id": "archive3", "operation": "publish",
            "update": {
                "state": "published", "anpa_category": [{"qcode": "r"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his4", "version": 0, "item_id": "archive4", "operation": "publish",
            "update": {
                "state": "published", "anpa_category": [{"qcode": "r"}], "pubstatus": "usable",
                "source": "AP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his5", "version": 0, "item_id": "archive5", "operation": "publish",
            "update": {
                "state": "published", "anpa_category": [{"qcode": "r"}], "pubstatus": "usable",
                "source": "BRA", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his6", "version": 0, "item_id": "archive6", "operation": "publish",
            "update": {
                "state": "published", "anpa_category": [{"qcode": "r"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"},
                "genre": [{"qcode": "Results (sport)"}]
            }
        }]
        """
        When we generate stats from archive history
        When we get "/mission_report?params={"query": {"filtered": {}}}"
        Then we get list with 1 items
        """
        {"_items": [{
            "corrections": [],
            "kills": [],
            "takedowns": [],
            "rewrites": 0,
            "new_stories": {
                "categories": {
                    "a": 1,
                    "h": 0,
                    "r": 2,
                    "results": 2,
                    "v": 1
                },
                "count": 6
            },
            "total_stories": 6
        }]}
        """

    @auth
    Scenario: Receive results as higharts configs
        Given "archive_history"
        """
        [{
            "_id": "his1", "version": 0, "item_id": "archive1", "operation": "publish",
            "update": {
                "state": "published", "anpa_category": [{"qcode": "a"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his2", "version": 0, "item_id": "archive2", "operation": "publish",
            "update": {
                "state": "published", "anpa_category": [{"qcode": "v"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his3", "version": 0, "item_id": "archive3", "operation": "publish",
            "update": {
                "state": "published", "anpa_category": [{"qcode": "v"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"},
                "rewrite_of": "archive1"
            }
        },
        {
            "_id": "his4", "version": 0, "item_id": "archive4", "operation": "correct",
            "update": {
                "state": "corrected", "anpa_category": [{"qcode": "v"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his5", "version": 0, "item_id": "archive5", "operation": "kill",
            "update": {
                "state": "killed", "anpa_category": [{"qcode": "v"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        },
        {
            "_id": "his6", "version": 0, "item_id": "archive6", "operation": "takedown",
            "update": {
                "state": "recalled", "anpa_category": [{"qcode": "v"}], "pubstatus": "usable",
                "source": "AAP", "task": {"stage": "5b501a6f1d41c84c0bfced4c", "desk": "5b501a501d41c84c0bfced4a"}
            }
        }]
        """
        When we generate stats from archive history
        When we get "/mission_report?params={"query": {"filtered": {}}}&return_type=highcharts_config"
        Then we get 7 charts
        """
        [{
            "id": "mission_report_summary",
            "chart": {
                "height": 300,
                "zoomType": "x"
            },
            "series": [{
                "name": "Summary",
                "data": [9, 5, 0, 1, 1, 1, 1],
                "type": "line",
                "xAxis": 0
            }],
            "title": {"text": "Mission Report Summary"},
            "type": "highcharts",
            "xAxis": [{
                "allowDecimals": false,
                "type": "category",
                "categories": [
                    "Total Stories",
                    "New Stories",
                    "Results/Fields/Comment/Betting",
                    "Updates",
                    "Corrections",
                    "Kills",
                    "Takedowns"
                ]
            }],
            "yAxis": [{
                "title": {"text": "Published Stories"},
                "allowDecimals": false
            }],
            "credits": {"enabled": false},
            "fullHeight": false,
            "time": {"useUTC": true},
            "legend": {"enabled": false},
            "plotOptions": {"series": {"dataLabels": {"enabled": false}}}
        }, {
            "id": "mission_report_categories",
            "chart": {"zoomType": "y"},
            "type": "highcharts",
            "title": {"text": "New Stories By Category"},
            "series": [{
                "name": "CATEGORY",
                "data": [1, 0, 0, 0, 4],
                "type": "bar",
                "xAxis": 0
            }],
            "xAxis": [{
                "allowDecimals": false,
                "type": "category",
                "categories": [
                    "National (A)",
                    "FormGuide (H)",
                    "Racing (Turf) (R)",
                    "Results/Fields/Comment/Betting",
                    "Advisories (V)"
                ],
                "title": {"text": "Published Stories"}
            }],
            "yAxis": [{
                "title": {"text": "Category"},
                "allowDecimals": false
            }],
            "credits": {"enabled": false},
            "fullHeight": true,
            "time": {"useUTC": true},
            "legend": {"enabled": false},
            "plotOptions": {"series": {"dataLabels": {"enabled": true}}}
        }, {
            "type": "table",
            "title": "There were 1 corrections issued",
            "headers": ["Sent", "Slugline", "TakeKey", "Ednote"]
        }, {
            "type": "table",
            "title": "There were 1 kills issued",
            "headers": ["Sent", "Slugline", "Reasons"]
        }, {
            "type": "table",
            "title": "There were 1 takedowns issued",
            "headers": ["Sent", "Slugline", "Reasons"]
        }, {
            "type": "table",
            "title": "There were 0 SMS alerts issued",
            "headers": ["Sent", "Slugline", "TakeKey", "Ednote"]
        }, {
            "type": "table",
            "title": "There were 1 updates issued",
            "headers": ["Sent", "Slugline", "TakeKey", "Ednote"]
        }]
        """
