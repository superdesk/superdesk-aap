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
                kills.append(item)

            elif item_state == CONTENT_STATE.RECALLED:
                takedowns.append(item)

        report = {
            'total_stories': total_stories,
            'new_stories': new_stories,
            'corrections': corrections,
            'kills': kills,
            'takedowns': takedowns,
            'first_item': first_item,
            'rewrites': rewrites,
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
        def gen_summary_chart():
            x_axis_titles = [
                'Total Stories',
                'Results/Fields/Comment/Betting',
                'New Stories',
                'Updates',
                'Corrections',
                'Kills',
                'Takedowns'
            ]

            series_data = [
                report['total_stories'],
                report['new_stories']['categories']['results'],
                report['new_stories']['count'],
                len(report['rewrites']),
                len(report['corrections']),
                len(report['kills']),
                len(report['takedowns'])
            ]

            subtitle = self.get_date_time_string(
                report['first_item']['versioncreated'],
                '%A %d %B %Y'
            )

            return {
                'id': 'mission_report_summary',
                'type': 'line',
                'chart': {
                    'type': 'line',
                    'height': 300,
                },
                'title': {'text': 'Mission Report: Summary({})'.format(report['total_stories'])},
                'subtitle': {'text': subtitle},
                'xAxis': {'categories': x_axis_titles},
                'yAxis': {
                    'title': {'text': 'STORIES TRANSMITTED'},
                    'labels': {'enabled': False},
                },
                'legend': {'enabled': False},
                'tooltip': {'enabled': False},
                'plotOptions': {
                    'series': {
                        'dataLabels': {'enabled': True},
                    },
                },
                'series': [{
                    'data': series_data
                }],
                'fullHeight': False,
            }

        def gen_category_chart():
            categories = report.get('categories') or {}
            categories['results'] = {
                'qcode': 'results',
                'name': 'Results/Fields/Comment/Betting'
            }

            sorted_categories = sorted(
                categories.items(),
                key=lambda x: x[0]
            )

            x_axis_titles = [
                category['name'] + ('' if qcode == 'results' else ' ({})'.format(qcode.upper()))
                for qcode, category in sorted_categories
            ]

            series_data = [
                report['new_stories']['categories'][qcode]
                for qcode, category in sorted_categories
            ]

            return {
                'id': 'mission_report_categories',
                'type': 'bar',
                'chart': {
                    'type': 'bar',
                    'zoomType': 'y'
                },
                'title': {'text': 'New Stories By Category'},
                'xAxis': {
                    'title': {'text': 'CATEGORY'},
                    'categories': x_axis_titles
                },
                'yAxis': {
                    'title': {'text': 'STORIES TRANSMITTED'},
                    'labels': {'enabled': False}
                },
                'legend': {'enbaled': False},
                'tooltip': {'enabled': False},
                'plotOptions': {
                    'series': {
                        'dataLabels': {'enabled': True}
                    }
                },
                'series': [{
                    'data': series_data
                }]
            }

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

            return {
                'id': 'mission_report_kills',
                'type': 'table',
                'headers': ['Sent', 'Slugline', 'TakeKey', 'Ednote'],
                'title': 'There were {} kills issued'.format(len(kills)),
                'rows': gen_table_rows(kills)
            }

        def gen_takedowns_chart():
            takedowns = report.get('takedowns') or []

            return {
                'id': 'mission_report_takedowns',
                'type': 'table',
                'headers': ['Sent', 'Slugline', 'TakeKey', 'Ednote'],
                'title': 'There were {} takedowns issued'.format(len(takedowns)),
                'rows': gen_table_rows(takedowns)
            }

        def gen_updates_chart():
            return {
                'id': 'mission_report_updates',
                'type': 'table',
                'headers': ['Sent', 'Slugline', 'TakeKey', 'Ednote'],
                'title': 'There were {} updates issued'.format(len(report.get('rewrites') or [])),
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
            report['highcharts'] = [
                gen_summary_chart(),
                gen_category_chart(),
                gen_corrections_chart(),
                gen_kills_chart(),
                gen_takedowns_chart(),
                gen_updates_chart()
            ]

        report.pop('categories', None)
        return report

    def generate_csv(self, docs, args):
        report = self.generate_report(docs, args)
        report['highcharts'] = []
        return report

    def _gen_html(self, first_item, total_stories, new_stories, corrections, kills, takedowns, rewrites, results):
        return self._gen_summary_header(first_item, total_stories, new_stories) + \
            self._gen_category_summary(new_stories['categories'], results) + \
            self._gen_corrections_summary(corrections) + \
            self._gen_kills_summary(kills) + \
            self._gen_takedowns_summary(takedowns) + \
            self._gen_rewrites_summary(rewrites)

    @staticmethod
    def _gen_summary_header(first_item, total_stories, new_stories):
        return '''<p>SUMMARY FOR {}
Total number of stories transmitted - {}
Total New Stories - {}</p>'''.format(
            utc_to_local(
                app.config['DEFAULT_TIMEZONE'],
                first_item.get('versioncreated')
            ).strftime('%d%b%y'),
            total_stories,
            new_stories['count']
        ).replace('\n', '<br>')

    @staticmethod
    def _gen_category_summary(categories, results):
        html = '<p>New Stories by Category:<br>'
        for category in sorted(categories):
            html += '{} - {}<br>'.format(
                category.upper(),
                categories[category]
            )

            if category == 'r':
                html += '(Results/Fields/Comment/Betting {})<br>'.format(len(results))

        html += '</p>'
        return html

    def _gen_corrections_summary(self, corrections):
        if len(corrections) < 1:
            return '<p>There were no corrections issued.</p>'

        html = '<p>There were {} corrections issued<br>'.format(len(corrections))
        for correction in corrections:
            html += '{} {} {}<br>'.format(
                correction['slugline'],
                correction.get('anpa_take_key') or '',
                self.get_date_time_string(correction['versioncreated'])
            )
        html += '</p>'
        return html

    def _gen_kills_summary(self, kills):
        if len(kills) < 1:
            return '<p>There were no kills issued.</p>'

        html = '<p>There were {} kills issued<br>'.format(len(kills))
        for kill in kills:
            html += '{} {} {}<br>'.format(
                kill['slugline'],
                kill.get('anpa_take_key') or '',
                self.get_date_time_string(kill['versioncreated'])
            )
        html += '</p>'
        return html

    def _gen_takedowns_summary(self, takedowns):
        if len(takedowns) < 1:
            return '<p>There were no take downs issued.</p>'

        html = '<p>There were {} take downs issued<br>'.format(len(takedowns))
        for takedown in takedowns:
            html += '{} {} {}<br>'.format(
                takedown['slugline'],
                takedown.get('anpa_take_key') or '',
                self.et_date_time_string(takedown['versioncreated'])
            )
        html += '</p>'
        return html

    def _gen_rewrites_summary(self, rewrites):
        if len(rewrites) < 1:
            return '<p>There were no updates issued.</p>'

        return '<p>There were {} updates issued<br>'.format(len(rewrites))
