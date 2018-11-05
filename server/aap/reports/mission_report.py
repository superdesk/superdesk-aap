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

from analytics.base_report import BaseReportService
from analytics.chart_config import ChartConfig

from aap.common import extract_kill_reason_from_html

from flask import current_app as app


RESULTS_CATEGORIES = ['r', 'h']


class MissionReportResource(Resource):
    """Mission Report resource"""

    item_methods = ['GET']
    resource_methods = ['GET']
    privileges = {'GET': 'mission_report'}


class MissionReportService(BaseReportService):
    repos = ['published']
    aggregations = {}

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
                exclude_categories = [qcode for qcode in terms['anpa_category.qcode'] or []]
        elif args.get('params'):
            must_not = args.get('params', {})\
                           .get('must_not', {})

            exclude_categories = [
                qcode
                for qcode in must_not.get('categories', [])
            ]

        return {
            category.get('qcode'): category
            for category in cv.get('items') or []
            if category.get('is_active', True) and
            category.get('qcode') not in exclude_categories
        }

    def generate_report(self, docs, args, include_categories=False):
        """Returns the category count

        :param docs: document used for generating the report
        :return dict: report
        """
        items = list(docs)
        total_stories = len(items)

        if total_stories < 1:
            return {
                'total_stories': 0,
                'new_stories': {
                    'categories': {},
                    'count': 0
                },
                'corrections': [],
                'kills': [],
                'takedowns': [],
                'first_item': {},
                'rewrites': [],
            }

        categories = self._get_filtered_categories(args)

        new_stories = {
            'count': 0,
            'categories': {qcode: 0 for qcode in categories.keys()}
        }

        new_stories['categories']['results'] = 0

        corrections = []
        kills = []
        takedowns = []
        rewrites = []
        sms_alerts = []

        total_stories = 0

        first_item = None

        for item in items:
            if first_item is None:
                first_item = item

            total_stories += 1
            item_state = item.get(ITEM_STATE)

            if item_state == CONTENT_STATE.PUBLISHED:
                if self._is_rewrite(item):
                    rewrites.append(item)
                else:
                    new_stories['count'] += 1
                    if self._is_results_field(item):
                        new_stories['categories']['results'] += 1
                    else:
                        for category in item.get('anpa_category') or []:
                            new_stories['categories'][category.get('qcode')] += 1

            elif item_state == CONTENT_STATE.CORRECTED:
                corrections.append(item)

            elif item_state == CONTENT_STATE.KILLED:
                item['_reasons'] = extract_kill_reason_from_html(
                    item.get('body_html') or '',
                    is_kill=True
                )
                kills.append(item)

            elif item_state == CONTENT_STATE.RECALLED:
                item['_reasons'] = extract_kill_reason_from_html(
                    item.get('body_html') or '',
                    is_kill=False
                )
                takedowns.append(item)

            if (item.get('flags') or {}).get('marked_for_sms'):
                sms_alerts.append(item)

        report = {
            'total_stories': total_stories,
            'new_stories': new_stories,
            'corrections': corrections,
            'kills': kills,
            'takedowns': takedowns,
            'first_item': first_item,
            'rewrites': rewrites,
            'sms_alerts': sms_alerts,
        }

        if include_categories:
            report['categories'] = categories

        return report

    def generate_elastic_query(self, args):
        if not args.get('params'):
            args['params'] = {}

        args['include_items'] = 1
        args['params'].setdefault('size', 2000)
        return BaseReportService.generate_elastic_query(self, args)

    def generate_highcharts_config(self, docs, args):
        params = args.get('params') or {}

        def gen_summary_chart():
            source = {
                'total_stories': report['total_stories'],
                'new_stories': report['new_stories']['count'],
                'results': report['new_stories']['categories']['results'],
                'rewrites': len(report['rewrites']),
                'corrections': len(report['corrections']),
                'kills': len(report['kills']),
                'takedowns': len(report['takedowns'])
            }

            def get_sorted_keys(data):
                return [
                    'total_stories',
                    'new_stories',
                    'results',
                    'rewrites',
                    'corrections',
                    'kills',
                    'takedowns'
                ]

            def get_chart():
                return {
                    'type': chart_config.chart_type,
                    'height': 300
                }

            def get_plot_options():
                return {'series': {'dataLabels': {'enabled': True}}}

            def gen_subtitle():
                return chart_config.gen_subtitle_for_dates(params)

            chart_config = ChartConfig('mission_report_summary', 'line')

            chart_config.title = 'Mission Report Summary'
            chart_config.get_subtitle = gen_subtitle

            chart_config.translations = {
                'summary': {
                    'title': 'Summary',
                    'names': {
                        'total_stories': 'Total Stories',
                        'results': 'Results/Fields/Comment/Betting',
                        'new_stories': 'New Stories',
                        'rewrites': 'Updates',
                        'corrections': 'Corrections',
                        'kills': 'Kills',
                        'takedowns': 'Takedowns'
                    }
                }
            }

            chart_config.get_chart = get_chart
            chart_config.get_plot_options = get_plot_options
            chart_config.get_sorted_keys = get_sorted_keys

            chart_config.add_source('summary', source)

            chart_config.gen_config()
            chart_config.config['fullHeight'] = False
            chart_config.config['xAxis'].pop('title', None)

            return chart_config.config

        def gen_category_chart():
            categories = report.get('categories')
            categories['results'] = {
                'qcode': 'results',
                'name': 'Results/Fields/Comment/Betting'
            }

            source = {
                qcode: report['new_stories']['categories'][qcode]
                for qcode, category in categories.items()
            }

            def get_sorted_keys(data):
                return [
                    category for category, count
                    in sorted(
                        source.items(),
                        key=lambda kv: kv[0]
                    )
                ]

            chart_config = ChartConfig('mission_report_categories', 'bar')

            chart_config.translations = {
                'category': {
                    'title': 'CATEGORY',
                    'names': {
                        qcode: category['name'] + (
                            '' if qcode == 'results' else ' ({})'.format(qcode.upper())
                        )
                        for qcode, category in categories.items()
                    }
                }
            }
            chart_config.get_sorted_keys = get_sorted_keys

            chart_config.title = 'New Stories By Category'
            chart_config.add_source('category', source)

            return chart_config.gen_config()

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
                'title': 'There were {} updates issued'.format(len(report.get('rewrites') or [])),
                'rows': []
            }

        def gen_sms_alerts_chart():
            return {
                'id': 'mission_report_sms_alerts',
                'type': 'table',
                'headers': ['Sent', 'Slugline', 'TakeKey', 'Ednote'],
                'title': 'There were {} SMS alerts issued'.format(len(report.get('sms_alerts') or [])),
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
