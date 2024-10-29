Feature: SMS Report
    @auth
    Scenario: Generates a Daily SMS data
        Given "archived"
        """
        [{
            "_id": "archive1", "state": "published",
            "flags": {"marked_for_sms": false}, "versioncreated": "2018-06-29T21:00:00+0000"
        }, {
            "_id": "archive2", "state": "published",
            "flags": {"marked_for_sms": false}, "versioncreated": "2018-06-30T21:00:00+0000"
        }, {
            "_id": "archive3", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-06-30T21:00:00+0000"
        }, {
            "_id": "archive4", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-07-01T21:00:00+0000"
        }]
        """
        When we get "/sms_report?params={"histogram": {"interval": "daily"}, "dates": {"filter": "range", "start": "2018-06-29", "end": "2018-07-01"}}"
        Then we get list with 1 items
        """
        {"_items": [{
            "start_epoch": 1530226800000,
            "interval": 86400000,
            "with_sms": [0, 1, 1],
            "without_sms": [1, 1, 0]
        }]}
        """

    @auth
    Scenario: Generate Daily SMS highcharts config
        Given "archived"
        """
        [{
            "_id": "archive1", "state": "published",
            "flags": {"marked_for_sms": false}, "versioncreated": "2018-06-29T21:00:00+0000"
        }, {
            "_id": "archive2", "state": "published",
            "flags": {"marked_for_sms": false}, "versioncreated": "2018-06-30T21:00:00+0000"
        }, {
            "_id": "archive3", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-06-30T21:00:00+0000"
        }, {
            "_id": "archive4", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-07-01T21:00:00+0000"
        }]
        """
        When we get "/sms_report?params={"histogram": {"interval": "daily"}, "dates": {"filter": "range", "start": "2018-06-29", "end": "2018-07-01"}}&return_type=highcharts_config"
        Then we get 1 charts
        """
        [{
            "id": "sms_report",
            "type": "highcharts",
            "chart": {"zoomType": "x"},
            "title": {"text": "Daily SMS Report"},
            "subtitle": {"text": "June 29, 2018 - July 1, 2018"},
            "xAxis": [{
                "allowDecimals": false,
                "type": "datetime",
                "startOfWeek": 0,
                "title": {"text": "SMS"}
            }],
            "yAxis": [{
                "title": {"text": "Published Stories"},
                "allowDecimals": false,
                "stackLabels": {"enabled": false}
            }],
            "series": [{
                "name": "With SMS",
                "type": "column",
                "xAxis": 0,
                "data": [0, 1, 1],
                "pointStart": 1530226800000,
                "pointInterval": 86400000
            }, {
                "name": "Without SMS",
                "type": "column",
                "xAxis": 0,
                "data": [1, 1, 0],
                "pointStart": 1530226800000,
                "pointInterval": 86400000
            }]
        }]
        """

    @auth
    Scenario: Generates an Hourly SMS data
        Given "archived"
        """
        [{
            "_id": "archive1", "state": "published",
            "flags": {"marked_for_sms": false}, "versioncreated": "2018-06-30T04:00:00+0000"
        }, {
            "_id": "archive2", "state": "published",
            "flags": {"marked_for_sms": false}, "versioncreated": "2018-06-30T09:00:00+0000"
        }, {
            "_id": "archive3", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-06-30T09:00:00+0000"
        }, {
            "_id": "archive4", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-06-30T14:00:00+0000"
        }]
        """
        When we get "/sms_report?params={"histogram": {"interval": "hourly"}, "dates": {"filter": "range", "start": "2018-06-30", "end": "2018-06-30"}}"
        Then we get list with 1 items
        """
        {"_items": [{
            "start_epoch": 1530313200000,
            "interval": 3600000,
            "with_sms": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            "without_sms": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }]}
        """

    @auth
    Scenario: Generate Hourly SMS highcharts config
        Given "archived"
        """
        [{
            "_id": "archive1", "state": "published",
            "flags": {"marked_for_sms": false}, "versioncreated": "2018-06-30T04:00:00+0000"
        }, {
            "_id": "archive2", "state": "published",
            "flags": {"marked_for_sms": false}, "versioncreated": "2018-06-30T09:00:00+0000"
        }, {
            "_id": "archive3", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-06-30T09:00:00+0000"
        }, {
            "_id": "archive4", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-06-30T14:00:00+0000"
        }]
        """
        When we get "/sms_report?params={"histogram": {"interval": "hourly"}, "dates": {"filter": "range", "start": "2018-06-30", "end": "2018-06-30"}}&return_type=highcharts_config"
        Then we get 1 charts
        """
        [{
            "id": "sms_report",
            "type": "highcharts",
            "chart": {"zoomType": "x"},
            "title": {"text": "Hourly SMS Report"},
            "subtitle": {"text": "June 30, 2018 - June 30, 2018"},
            "xAxis": [{
                "allowDecimals": false,
                "type": "datetime",
                "startOfWeek": 0,
                "title": {"text": "SMS"}
            }],
            "yAxis": [{
                "title": {"text": "Published Stories"},
                "allowDecimals": false,
                "stackLabels": {"enabled": false}
            }],
            "series": [{
                "name": "With SMS",
                "type": "column",
                "xAxis": 0,
                "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                "pointStart": 1530313200000,
                "pointInterval": 3600000
            }, {
                "name": "Without SMS",
                "type": "column",
                "xAxis": 0,
                "data": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "pointStart": 1530313200000,
                "pointInterval": 3600000
            }]
        }]
        """

    @auth
    Scenario: Generates a Weekly SMS data
        Given "archived"
        """
        [{
            "_id": "archive1", "state": "published",
            "flags": {"marked_for_sms": false}, "versioncreated": "2018-06-23T04:00:00+0000"
        }, {
            "_id": "archive2", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-06-23T04:00:00+0000"
        }, {
            "_id": "archive3", "state": "published",
            "flags": {"marked_for_sms": false}, "versioncreated": "2018-06-27T09:00:00+0000"
        }, {
            "_id": "archive4", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-06-27T09:00:00+0000"
        }, {
            "_id": "archive5", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-06-29T14:00:00+0000"
        }]
        """
        When we get "/sms_report?params={"histogram": {"interval": "weekly"}, "dates": {"filter": "range", "start": "2018-06-23", "end": "2018-06-30"}}"
        Then we get list with 1 items
        """
        {"_items": [{
            "start_epoch": 1529190000000,
            "interval": 604800000,
            "with_sms": [1, 2],
            "without_sms": [1, 1]
        }]}
        """

    @auth
    Scenario: Generate Weekly SMS highcharts config
        Given "archived"
        """
        [{
            "_id": "archive1", "state": "published",
            "flags": {"marked_for_sms": false}, "versioncreated": "2018-06-23T04:00:00+0000"
        }, {
            "_id": "archive2", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-06-23T04:00:00+0000"
        }, {
            "_id": "archive3", "state": "published",
            "flags": {"marked_for_sms": false}, "versioncreated": "2018-06-27T09:00:00+0000"
        }, {
            "_id": "archive4", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-06-27T09:00:00+0000"
        }, {
            "_id": "archive5", "state": "published",
            "flags": {"marked_for_sms": true}, "versioncreated": "2018-06-29T14:00:00+0000"
        }]
        """
        When we get "/sms_report?params={"histogram": {"interval": "weekly"}, "dates": {"filter": "range", "start": "2018-06-23", "end": "2018-06-30"}}&return_type=highcharts_config"
        Then we get 1 charts
        """
        [{
            "id": "sms_report",
            "type": "highcharts",
            "chart": {"zoomType": "x"},
            "title": {"text": "Weekly SMS Report"},
            "subtitle": {"text": "June 23, 2018 - June 30, 2018"},
            "xAxis": [{
                "allowDecimals": false,
                "type": "datetime",
                "startOfWeek": 0,
                "title": {"text": "SMS"}
            }],
            "yAxis": [{
                "title": {"text": "Published Stories"},
                "allowDecimals": false,
                "stackLabels": {"enabled": false}
            }],
            "series": [{
                "name": "With SMS",
                "type": "column",
                "xAxis": 0,
                "data": [1, 2],
                "pointStart": 1529190000000,
                "pointInterval": 604800000
            }, {
                "name": "Without SMS",
                "type": "column",
                "xAxis": 0,
                "data": [1, 1],
                "pointStart": 1529190000000,
                "pointInterval": 604800000
            }]
        }]
        """
