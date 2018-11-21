# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2018 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.resource import Resource
from superdesk.errors import SuperdeskApiError

from analytics.base_report import BaseReportService
from analytics.chart_config import SDChart, ChartConfig
from analytics.common import get_utc_offset_in_minutes

from flask import current_app as app
from datetime import datetime


class SMSReportResource(Resource):
    """SMS Report schema"""

    item_methods = ['GET']
    resource_methods = ['GET']
    privileges = {'GET': 'sms_report'}


class SMSReportService(BaseReportService):
    repos = ['published', 'archived']
    aggregations = {
        'sms': {
            'terms': {
                'field': 'flags.marked_for_sms',
                'min_doc_count': 0
            }
        }
    }

    def _get_request_or_lookup(self, req, **lookup):
        args = super()._get_request_or_lookup(req, **lookup)

        lt, gte, time_zone = self._es_get_date_filters(args.get('params') or {})

        if lt is None and gte is None:
            raise SuperdeskApiError.badRequestError('Must provide date filters')

        return args

    def generate_report(self, docs, args):
        agg_buckets = self.get_aggregation_buckets(getattr(docs, 'hits'), ['dates'])
        date_buckets = agg_buckets.get('dates') or {}

        if len(date_buckets) < 1:
            return {}

        report = {
            'start': date_buckets[0].get('key_as_string'),
            'start_epoch': date_buckets[0].get('key'),
            'interval': self.get_histogram_interval_ms(args),
            'with_sms': [],
            'without_sms': []
        }

        for bucket in agg_buckets.get('dates') or []:
            sms_buckets = (bucket.get('sms') or {}).get('buckets') or []

            with_sms = 0
            without_sms = 0

            for sms in sms_buckets:
                key = sms.get('key_as_string') or sms.get('key')
                if key == 'true' or key == 'T':
                    with_sms = sms.get('doc_count')
                else:
                    without_sms = sms.get('doc_count')

            report['with_sms'].append(with_sms)
            report['without_sms'].append(without_sms)

        return report

    def generate_highcharts_config(self, docs, args):
        params = args.get('params') or {}
        report = self.generate_report(docs, args)

        if (params.get('chart') or {}).get('title'):
            title = params['chart']['title']
        else:
            interval = (params.get('histogram') or {}).get('interval') or 'daily'
            if interval == 'hourly':
                title = 'Hourly SMS Report'
            elif interval == 'weekly':
                title = 'Weekly SMS Report'
            else:
                title = 'Daily SMS Report'

        if (params.get('chart') or {}).get('subtitle'):
            subtitle = params['chart']['subtitle']
        else:
            subtitle = ChartConfig.gen_subtitle_for_dates(params)

        # Calculate the UTC Offset in minutes for the start date of the results
        # This will cause an issue if a report crosses over the daylight savings change
        # Any data after the daylight savings change will be 1 hour out
        timezone_offset = get_utc_offset_in_minutes(
            datetime.utcfromtimestamp(int(report['start_epoch'] / 1000))
        )

        chart = SDChart.Chart(
            'sms_report',
            title=title,
            subtitle=subtitle,
            chart_type='highcharts',
            start_of_week=app.config.get('START_OF_WEEK') or 0,
            timezone_offset=timezone_offset,
            use_utc=False
        )

        chart.set_translation('sms', 'SMS', {
            'with_sms': 'With SMS',
            'without_sms': 'Without SMS'
        })

        axis = chart.add_axis().set_options(
            y_title='Published Stories',
            x_title=chart.get_translation_title('sms'),
            type='datetime',
            default_chart_type=(params.get('chart') or {}).get('type') or 'column',
            point_start=report.get('start_epoch'),
            point_interval=report.get('interval'),
            stack_labels=False
        )

        axis.add_series().set_options(
            field='sms',
            name='with_sms',
            data=report.get('with_sms')
        )

        axis.add_series().set_options(
            field='sms',
            name='without_sms',
            data=report.get('without_sms')
        )

        report['highcharts'] = [chart.gen_config()]

        return report
