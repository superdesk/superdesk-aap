# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2018 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk import get_resource_service
from superdesk.resource import Resource
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE
from superdesk.utc import utc_to_local

from analytics.chart_config import ChartConfig, SDChart
from analytics.stats.stats_report_service import StatsReportService

from flask import current_app as app
from copy import deepcopy
from collections import namedtuple


RESULTS_CATEGORIES = ['r', 'h']

report_types = [
    'summary',
    'categories',
    'corrections',
    'kills',
    'takedowns',
    'sms_alerts',
    'updates'
]

REPORT_TYPES = namedtuple('REPORT_TYPES', [
    'SUMMARY',
    'CATEGORIES',
    'CORRECTIONS',
    'KILLS',
    'TAKEDOWNS',
    'SMS_ALERTS',
    'UPDATES'
])(*report_types)


class MissionReportResource(Resource):
    """Mission Report resource"""

    item_methods = ['GET']
    resource_methods = ['GET']
    privileges = {'GET': 'mission_report'}


class MissionReportService(StatsReportService):
    aggregations = {}

    def get_request_aggregations(self, params, args):
        return None

    @staticmethod
    def get_date_time_string(datetime_utc, str_format='%X %d%b%y'):
        return utc_to_local(
            app.config['DEFAULT_TIMEZONE'],
            datetime_utc
        ).strftime(str_format)

    @staticmethod
    def _is_rewrite(item):
        return 'rewrite_of' in item

    def _is_results_field(self, item):
        if self._contains_qcodes(item.get('anpa_category') or [], RESULTS_CATEGORIES):
            if self._contains_qcodes(item.get('genre') or [], ['Results (sport)']):
                return True

            if (item.get('source') or '') == 'BRA':
                return True

        return False

    @staticmethod
    def _contains_qcodes(field, qcodes):
        for value in field:
            if value.get('qcode') in qcodes:
                return True

        return False

    @staticmethod
    def _get_filtered_categories(args):
        cv = get_resource_service('vocabularies').find_one(req=None, _id='categories')

        exclude_categories = []

        if args.get('source'):
            must_not = args.get('source', {})\
                           .get('query', {})\
                           .get('filtered', {})\
                           .get('filter', {})\
                           .get('bool', {})\
                           .get('must_not', [])

            for query in must_not:
                terms = query.get('terms') or {}
                if not terms.get('anpa_category.qcode'):
                    continue

                exclude_categories = [
                    qcode
                    for qcode in terms.get('anpa_category.qcode') or []
                ]
        elif args.get('params'):
            must_not = (args.get('params') or {}).get('must_not') or {}

            exclude_categories = [
                qcode
                for qcode in must_not.get('categories') or []
            ]

        return {
            category.get('qcode'): category
            for category in cv.get('items') or []
            if category.get('is_active', True) and
            category.get('qcode') not in exclude_categories
        }

    def add_query_clause(self, params, query):
        if query.get('must'):
            params['source']['query']['filtered']['filter']['bool']['must'].extend(query['must'])

        if query.get('must_not'):
            params['source']['query']['filtered']['filter']['bool']['must_not'].extend(query['must_not'])

        if query.get('should'):
            params['source']['query']['filtered']['filter']['bool']['should'] = query['should']

        if query.get('minimum_should_match'):
            params['source']['query']['filtered']['filter']['bool']['minimum_should_match'] = \
                query['minimum_should_match']

        if query.get('aggs'):
            params['source']['aggs'] = query['aggs']

        if query.get('size'):
            params['source']['size'] = query['size']

        if query.get('_source'):
            params['source']['_source'] = query['_source']

        return params

    def _es_set_size(self, query, params):
        pass

    def run_query(self, params, args):
        reports = (args.get('params') or {}).get('reports') or {
            REPORT_TYPES.SUMMARY: True,
            REPORT_TYPES.CATEGORIES: True,
            REPORT_TYPES.CORRECTIONS: True,
            REPORT_TYPES.KILLS: True,
            REPORT_TYPES.TAKEDOWNS: True,
            REPORT_TYPES.SMS_ALERTS: True,
            REPORT_TYPES.UPDATES: True
        }
        docs = {}

        # Get New Story Counts (excluding results/fields/comment/betting)
        if reports.get(REPORT_TYPES.SUMMARY, True) or reports.get(REPORT_TYPES.CATEGORIES, True):
            es_query = {
                'must': [
                    {
                        'terms': {
                            'state': [
                                'published',
                                'corrected',
                                'killed',
                                'recalled'
                            ]
                        }
                    }
                ],
                'must_not': [
                    {'exists': {'field': 'rewrite_of'}},
                    {
                        'bool': {
                            'must': [
                                {'terms': {'anpa_category.qcode': ['r', 'h']}},
                                {'term': {'source': 'BRA'}}
                            ]
                        }
                    }, {
                        'bool': {
                            'must': [
                                {'terms': {'anpa_category.qcode': ['r', 'h']}},
                                {'term': {'genre.qcode': 'Results (sport)'}}
                            ]
                        }
                    }
                ],
                'size': 0
            }

            if reports.get(REPORT_TYPES.CATEGORIES, True):
                es_query['aggs'] = {
                    'categories': {
                        'terms': {
                            'field': 'anpa_category.qcode',
                            'size': 0
                        }
                    }
                }

            query = self.add_query_clause(deepcopy(params), es_query)
            docs['new'] = StatsReportService.run_query(self, query, args)

            # Get Results/Fields/Comment/Betting counts
            query = self.add_query_clause(deepcopy(params), {
                'must': [{
                    'terms': {
                        'state': [
                            'published',
                            'corrected',
                            'killed',
                            'recalled'
                        ]
                    }
                }, {
                    'terms': {
                        'anpa_category.qcode': ['r', 'h']
                    }
                }],
                'must_not': [{
                    'exists': {'field': 'rewrite_of'}
                }],
                'should': [{
                    'term': {'source': 'BRA'}
                }, {
                    'term': {
                        'genre.qcode': 'Results (sport)'
                    }
                }],
                'minimum_should_match': 1,
                'size': 0
            })
            docs['sports'] = StatsReportService.run_query(self, query, args)

        # Get Corrections/Kills/Takedowns
        if reports.get(REPORT_TYPES.SUMMARY, True) or \
                reports.get(REPORT_TYPES.CORRECTIONS, True) or \
                reports.get(REPORT_TYPES.KILLS, True) or \
                reports.get(REPORT_TYPES.TAKEDOWNS, True):
            query = self.add_query_clause(deepcopy(params), {
                '_source': {
                    'include': [
                        '_id',
                        'slugline',
                        'anpa_take_key',
                        'ednote',
                        'extra',
                        'versioncreated',
                        'state'
                    ]
                },
                'must': [{
                    'terms': {
                        'state': {
                            'corrected',
                            'killed',
                            'recalled'
                        }
                    }
                }],
                "size": 500
            })
            docs[REPORT_TYPES.KILLS] = StatsReportService.run_query(self, query, args)

        # Get Update Counts
        if reports.get(REPORT_TYPES.SUMMARY, True) or reports.get(REPORT_TYPES.UPDATES, True):
            query = self.add_query_clause(deepcopy(params), {
                'must': [{
                    'terms': {
                        'state': {
                            'published',
                            'corrected',
                            'killed',
                            'recalled'
                        }
                    }
                }, {
                    'exists': {'field': 'rewrite_of'}
                }],
                'size': 0
            })
            docs[REPORT_TYPES.UPDATES] = StatsReportService.run_query(self, query, args)

        # Get SMS Counts
        if reports.get(REPORT_TYPES.SMS_ALERTS, True):
            query = self.add_query_clause(deepcopy(params), {
                'must': [{
                    'terms': {
                        'state': [
                            'published',
                            'corrected',
                            'killed',
                            'recalled'
                        ]
                    }
                }, {
                    'term': {'flags.marked_for_sms': 'true'}
                }],
                'aggs': {
                    'timeline': {
                        'nested': {'path': 'stats.timeline'},
                        'aggs': {
                            'operations': {
                                'terms': {
                                    'field': 'stats.timeline.operation',
                                    'size': 0,
                                    'include': [
                                        'publish',
                                        'correct',
                                        'kill',
                                        'correct'
                                    ]
                                }
                            }
                        }
                    }
                },
                'size': 0
            })
            docs[REPORT_TYPES.SMS_ALERTS] = StatsReportService.run_query(self, query, args)

        return docs

    def _get_total_hits(self, doc):
        return (doc.hits.get('hits') or {}).get('total') or 0

    def _get_aggs(self, doc, name):
        return ((doc.hits.get('aggregations') or {}).get(name) or {}).get('buckets') or []

    def generate_report(self, docs, args, include_categories=False):
        """Returns the category count

        :param docs: document used for generating the report
        :return dict: report
        """
        report = {
            'total_stories': 0,
            'new_stories': {
                'count': 0,
                'categories': {}
            },
            'rewrites': 0,
            'sms_alerts': 0,
            'kills': [],
            'takedowns': [],
            'corrections': []
        }

        # Add new story stats
        if docs.get('new'):
            categories = self._get_filtered_categories(args)

            if include_categories:
                report['categories'] = categories

            agg_categories = {
                cat['key']: cat['doc_count']
                for cat in self._get_aggs(docs['new'], 'categories')
            }
            report['new_stories']['count'] = self._get_total_hits(docs['new'])
            report['new_stories']['categories'] = {
                qcode: agg_categories.get(qcode) or 0
                for qcode in categories.keys()
            }
            report['total_stories'] += report['new_stories']['count']

        # Add stats for Results/Fields/Comment/Betting
        if docs.get('sports'):
            sports_count = self._get_total_hits(docs['sports'])
            if sports_count > 0:
                report['new_stories']['categories']['results'] = sports_count
                report['new_stories']['count'] += sports_count
                report['total_stories'] += sports_count
            else:
                report['new_stories']['categories']['results'] = 0
        else:
            report['new_stories']['categories']['results'] = 0

        # Add update stats
        if docs.get(REPORT_TYPES.UPDATES):
            report['rewrites'] = self._get_total_hits(docs[REPORT_TYPES.UPDATES])
            report['total_stories'] += report['rewrites']

        # Add sms stats
        if docs.get(REPORT_TYPES.SMS_ALERTS):
            timeline_aggs = (docs[REPORT_TYPES.SMS_ALERTS].hits.get('aggregations') or {}).get('timeline') or {}
            report[REPORT_TYPES.SMS_ALERTS] = sum([
                sms.get('doc_count') or 0
                for sms in (timeline_aggs.get('operations') or {}).get('buckets') or []
            ])

            if list(docs.keys()) == [REPORT_TYPES.SMS_ALERTS]:
                report['total_stories'] = report[REPORT_TYPES.SMS_ALERTS]

        if docs.get(REPORT_TYPES.KILLS):
            for item in docs[REPORT_TYPES.KILLS]:
                if item[ITEM_STATE] == CONTENT_STATE.KILLED:
                    item['_reasons'] = ((item.get('extra') or {}).get('mission') or {}).get('reasons') or ''
                    report[REPORT_TYPES.KILLS].append(item)
                elif item[ITEM_STATE] == CONTENT_STATE.RECALLED:
                    item['_reasons'] = ((item.get('extra') or {}).get('mission') or {}).get('reasons') or ''
                    report[REPORT_TYPES.TAKEDOWNS].append(item)
                elif item[ITEM_STATE] == CONTENT_STATE.CORRECTED:
                    report[REPORT_TYPES.CORRECTIONS].append(item)

            report['total_stories'] += len(report[REPORT_TYPES.KILLS])
            report['total_stories'] += len(report[REPORT_TYPES.TAKEDOWNS])
            report['total_stories'] += len(report[REPORT_TYPES.CORRECTIONS])

        return report

    def generate_highcharts_config(self, docs, args):
        params = args.get('params') or {}

        def gen_summary_chart():
            chart = SDChart.Chart(
                'mission_report_summary',
                title='Mission Report Summary',
                subtitle=ChartConfig.gen_subtitle_for_dates(params),
                chart_type='highcharts',
                height=300,
                data_labels=False,
                tooltip_header='{point.x}: {point.y}',
                tooltip_point='',
                default_config=ChartConfig.defaultConfig
            )

            chart.set_translation('summary', 'Summary', {
                'total_stories': 'Total Stories',
                'results': 'Results/Fields/Comment/Betting',
                'new_stories': 'New Stories',
                'rewrites': 'Updates',
                'corrections': 'Corrections',
                'kills': 'Kills',
                'takedowns': 'Takedowns'
            })

            axis = chart.add_axis().set_options(
                type='category',
                default_chart_type='line',
                y_title='Published Stories',
                category_field='summary',
                categories=[
                    'total_stories',
                    'new_stories',
                    'results',
                    'rewrites',
                    'corrections',
                    'kills',
                    'takedowns'
                ]
            )

            axis.add_series().set_options(
                field='summary',
                data=[
                    report['total_stories'],
                    report['new_stories']['count'],
                    report['new_stories']['categories']['results'],
                    report['rewrites'],
                    len(report['corrections']),
                    len(report['kills']),
                    len(report['takedowns'])
                ]
            )

            return chart.gen_config()

        def gen_category_chart():
            chart = SDChart.Chart(
                'mission_report_categories',
                title='New Stories By Category',
                data_labels=True,
                tooltip_header='{point.x}: {point.y}',
                tooltip_point='',
                full_height=True,
                default_config=ChartConfig.defaultConfig
            )

            categories = report.get('categories')
            categories['results'] = {
                'qcode': 'results',
                'name': 'Results/Fields/Comment/Betting'
            }

            chart.set_translation('category', 'CATEGORY', {
                qcode: category['name'] + (
                    '' if qcode == 'results' else ' ({})'.format(qcode.upper())
                )
                for qcode, category in categories.items()
            })

            source = {
                qcode: report['new_stories']['categories'][qcode]
                for qcode, category in categories.items()
            }

            sorted_categories = [
                category for category, count
                in sorted(
                    source.items(),
                    key=lambda kv: kv[0]
                )
            ]

            axis = chart.add_axis().set_options(
                type='category',
                default_chart_type='bar',
                y_title='Category',
                x_title='Published Stories',
                category_field='category',
                categories=sorted_categories
            )

            axis.add_series().set_options(
                field='category',
                data=[
                    source.get(qcode) or 0
                    for qcode in sorted_categories
                ]
            )

            return chart.gen_config()

        def gen_table_rows(source):
            return [
                [
                    self.get_date_time_string(
                        row['versioncreated'],
                        '%d/%m/%Y %H:%M'
                    ),
                    row.get('slugline') or '',
                    row.get('anpa_take_key') or '',
                    row.get('ednote') or ''
                ]
                for row in source
            ]

        def gen_corrections_chart():
            corrections = report.get('corrections') or []

            return {
                'id': 'mission_report_corrections',
                'type': 'table',
                'headers': ['Sent', 'Slugline', 'TakeKey', 'Ednote'],
                'title': 'There were {} corrections issued'.format(len(corrections)),
                'rows': gen_table_rows(corrections)
            }

        def gen_kills_chart():
            kills = report.get('kills') or []
            rows = []

            for item in kills:
                rows.append([
                    self.get_date_time_string(item['versioncreated'], '%d/%m/%Y %H:%M'),
                    item.get('slugline') or '',
                    item.get('_reasons') or '',
                ])

            return {
                'id': 'mission_report_kills',
                'type': 'table',
                'headers': ['Sent', 'Slugline', 'Reasons'],
                'title': 'There were {} kills issued'.format(len(kills)),
                'rows': rows
            }

        def gen_takedowns_chart():
            takedowns = report.get('takedowns') or []
            rows = []

            for item in takedowns:
                rows.append([
                    self.get_date_time_string(item['versioncreated'], '%d/%m/%Y %H:%M'),
                    item.get('slugline') or '',
                    item.get('_reasons') or '',
                ])

            return {
                'id': 'mission_report_takedowns',
                'type': 'table',
                'headers': ['Sent', 'Slugline', 'Reasons'],
                'title': 'There were {} takedowns issued'.format(len(takedowns)),
                'rows': rows
            }

        def gen_updates_chart():
            return {
                'id': 'mission_report_updates',
                'type': 'table',
                'headers': ['Sent', 'Slugline', 'TakeKey', 'Ednote'],
                'title': 'There were {} updates issued'.format(report.get('rewrites') or 0),
                'rows': []
            }

        def gen_sms_alerts_chart():
            return {
                'id': 'mission_report_sms_alerts',
                'type': 'table',
                'headers': ['Sent', 'Slugline', 'TakeKey', 'Ednote'],
                'title': 'There were {} SMS alerts issued'.format(report.get('sms_alerts') or 0),
                'rows': []
            }

        report = self.generate_report(docs, args, True)

        if (report.get('total_stories') or 0) < 1:
            report['highcharts'] = [{
                'id': 'mission_report_emtpy',
                'type': 'table',
                'title': 'There were no stories published',
                'rows': []
            }]
        else:
            charts = []

            reports_enabled = params.get('reports') or {}

            if reports_enabled.get('summary', True):
                charts.append(gen_summary_chart())

            if reports_enabled.get('categories', True):
                charts.append(gen_category_chart())

            if reports_enabled.get('corrections', True):
                charts.append(gen_corrections_chart())

            if reports_enabled.get('kills', True):
                charts.append(gen_kills_chart())

            if reports_enabled.get('takedowns', True):
                charts.append(gen_takedowns_chart())

            if reports_enabled.get('sms_alerts', True):
                charts.append(gen_sms_alerts_chart())

            if reports_enabled.get('updates', True):
                charts.append(gen_updates_chart())

            report['highcharts'] = charts

        report.pop('categories', None)
        return report

    def generate_csv(self, docs, args):
        report = self.generate_report(docs, args)
        report['highcharts'] = []
        return report
