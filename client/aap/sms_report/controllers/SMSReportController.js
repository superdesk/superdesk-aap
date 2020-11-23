import {getErrorMessage, getUtcOffsetInMinutes} from 'superdesk-analytics/client/utils';
import {DATE_FILTERS} from 'superdesk-analytics/client/search/common';
import {CHART_FIELDS, CHART_TYPES} from 'superdesk-analytics/client/charts/directives/ChartOptions';
import {SDChart} from 'superdesk-analytics/client/charts/SDChart';
import {searchReportService} from 'superdesk-analytics/client/search/services/SearchReport';
import {appConfig} from 'superdesk-core/scripts/appConfig';

SMSReportController.$inject = [
    '$scope',
    'savedReports',
    'chartConfig',
    'lodash',
    'moment',
    'notify',
    'gettext',
    '$q',
    'reportConfigs',
];


export function SMSReportController(
    $scope,
    savedReports,
    chartConfig,
    _,
    moment,
    notify,
    gettext,
    $q,
    reportConfigs
) {
    const reportName = 'sms_report';

    this.init = () => {
        $scope.form = {
            datesError: null,
            submitted: false,
            showErrors: false,
        };
        $scope.config = reportConfigs.getConfig(reportName);

        $scope.chartFields = [
            CHART_FIELDS.TITLE,
            CHART_FIELDS.SUBTITLE,
            CHART_FIELDS.TYPE,
        ];

        this.initDefaultParams();
        savedReports.selectReportFromURL();

        this.chart = chartConfig.newConfig('chart', _.get($scope, 'currentParams.params.chart.type'));
        $scope.updateChartConfig();
    };

    this.initDefaultParams = () => {
        $scope.item_states = searchReportService.filterItemStates(
            ['published', 'killed', 'corrected', 'recalled']
        );

        $scope.intervals = [{
            qcode: 'hourly',
            name: gettext('Hourly'),
        }, {
            qcode: 'daily',
            name: gettext('Daily'),
        }, {
            qcode: 'weekly',
            name: gettext('Weekly'),
        }];

        $scope.currentParams = {
            report: reportName,
            params: $scope.config.defaultParams({
                dates: {
                    filter: DATE_FILTERS.RANGE,
                    start: moment()
                        .subtract(30, 'days')
                        .format(appConfig.model.dateformat),
                    end: moment().format(appConfig.model.dateformat),
                },
                must: {},
                must_not: {},
                chart: {
                    type: CHART_TYPES.COLUMN,
                    sort_order: 'desc',
                    title: null,
                    subtitle: null,
                },
                histogram: {
                    interval: 'daily',
                },
            }),
        };

        $scope.defaultReportParams = _.cloneDeep($scope.currentParams);
    };

    $scope.updateChartConfig = () => {
        this.chart.chartType = _.get($scope, 'currentParams.params.chart.type');
        this.chart.sortOrder = _.get($scope, 'currentParams.params.chart.sort_order');
        this.chart.title = _.get($scope, 'currentParams.params.chart.title');
        this.chart.subtitle = _.get($scope, 'currentParams.params.chart.subtitle');
    };

    this.getIntervalName = () => {
        const interval = _.get($scope, 'currentParams.params.histogram.interval') || 'daily';

        switch (interval) {
        case 'hourly':
            return gettext('Hourly');
        case 'weekly':
            return gettext('Weekly');
        case 'daily':
        default:
            return gettext('Daily');
        }
    };

    $scope.generateTitle = () => {
        if (_.get($scope, 'currentParams.params.chart.title')) {
            return $scope.currentParams.params.chart.title;
        }

        return this.getIntervalName() + ' ' + gettext('SMS Report');
    };

    $scope.generateSubtitle = () => {
        if (_.get($scope, 'currentParams.params.chart.subtitle')) {
            return $scope.currentParams.params.chart.subtitle;
        }

        return chartConfig.generateSubtitleForDates(
            _.get($scope, 'currentParams.params') || {}
        );
    };

    $scope.isDirty = () => true;

    $scope.$watch(() => savedReports.currentReport, (newReport) => {
        if (_.get(newReport, '_id')) {
            $scope.currentParams = _.cloneDeep(savedReports.currentReport);
        } else {
            $scope.currentParams = _.cloneDeep($scope.defaultReportParams);
        }
    }, true);

    $scope.onDateFilterChange = () => {
        if ($scope.currentParams.params.dates.filter !== 'range') {
            $scope.currentParams.params.dates.start = null;
            $scope.currentParams.params.dates.end = null;
        }

        $scope.updateChartConfig();
    };

    $scope.generate = () => {
        $scope.changeContentView('report');
        $scope.form.submitted = true;

        if ($scope.form.datesError) {
            $scope.form.showErrors = true;
            return;
        }

        $scope.form.showErrors = false;
        $scope.beforeGenerateChart();

        const params = _.cloneDeep($scope.currentParams.params);

        $scope.runQuery(params)
            .then((data) => {
                this.createChart(
                    Object.assign(
                        {},
                        $scope.currentParams.params,
                        data
                    )
                )
                    .then((chartConfig) => {
                        $scope.changeReportParams(chartConfig);
                        $scope.form.submitted = false;
                    });
            }, (error) => {
                notify.error(
                    getErrorMessage(
                        error,
                        gettext('Error. The SMS Report could not be generated!')
                    )
                );
            })
    };

    this.createChart = (report) => {
        return _.get($scope, 'currentParams.params.chart.type') === 'table' ?
            this.genTableConfig(report) :
            this.genChartConfig(report);
    };

    this.genChartConfig = (report) => {
        // Calculate the UTC Offset in minutes for the start date of the results
        // This will cause an issue if a report crosses over the daylight savings change
        // Any data after the daylight savings change will be 1 hour out
        const utcOffset = getUtcOffsetInMinutes(
            report['start'],
            appConfig.defaultTimezone
        );

        const chart = new SDChart.Chart({
            id: reportName,
            chartType: 'highcharts',
            title: $scope.generateTitle(),
            subtitle: $scope.generateSubtitle(),
            startOfWeek: appConfig.start_of_week || appConfig.startingDay || 0,
            timezoneOffset: utcOffset,
            useUTC: false,
            fullHeight: true,
        });

        chart.setTranslation('sms', gettext('SMS'), {
            with_sms: gettext('With SMS'),
            without_sms: gettext('Without SMS'),
        });

        const axis = chart.addAxis()
            .setOptions({
                type: 'datetime',
                defaultChartType: _.get($scope, 'currentParams.params.chart.type'),
                pointStart: Date.parse(_.get(report, 'start')),
                pointInterval: _.get(report, 'interval'),
                stackLabels: false,
                yTitle: gettext('Published Stories'),
                xTitle: chart.getTranslationTitle('sms'),
            });

        axis.addSeries()
            .setOptions({
                field: 'sms',
                name: 'with_sms',
                data: _.get(report, 'with_sms'),
            });

        axis.addSeries()
            .setOptions({
                field: 'sms',
                name: 'without_sms',
                data: _.get(report, 'without_sms'),
            });

        return $q.when({
            charts: [chart.genConfig()],
            wrapCharts: report.chart.type === 'table',
            height500: false,
            fullWidth: true,
            multiChart: false,
        })
    };

    this.genTableConfig = (report) => {
        let dateHeader;

        switch ($scope.currentParams.params.histogram.interval) {
        case 'hourly':
            dateHeader = gettext('Date/Time');
            break;
        case 'weekly':
            dateHeader = gettext('Week Starting');
            break;
        case 'daily':
        default:
            dateHeader = gettext('Date');
            break;
        }

        const headers = [
            dateHeader,
            gettext('With SMS'),
            gettext('Without SMS'),
        ];

        const rows = [];
        const totals = [0, 0];
        const startEpoch = _.get(report, 'start_epoch');
        const interval = _.get(report, 'interval') / 1000;
        const withSms = _.get(report, 'with_sms', []);
        const withoutSms = _.get(report, 'without_sms', []);
        let dateFormat;

        switch ($scope.currentParams.params.histogram.interval) {
        case 'hourly':
            dateFormat = 'MMM Do HH:mm';
            break;
        case 'daily':
        case 'weekly':
        default:
            dateFormat = 'MMM Do';
            break;
        }

        withSms.forEach((_, index) => {
            totals[0] += withSms[index];
            totals[1] += withoutSms[index];

            rows.push([
                moment(startEpoch).add(index * interval, 'seconds').format(dateFormat),
                withSms[index],
                withoutSms[index],
            ]);
        });

        rows.push([
            gettext('Total'),
            totals[0],
            totals[1],
        ]);

        return $q.when({
            charts: [{
                id: reportName,
                type: 'table',
                chart: {type: 'column'},
                headers: headers,
                title: $scope.generateTitle(),
                subtitle: $scope.generateSubtitle(),
                rows: rows,
            }],
            wrapCharts: true,
            height500: false,
            fullWidth: true,
            multiChart: false,
        });
    };

    $scope.getReportParams = () => (
        $q.when(_.cloneDeep($scope.currentParams))
    );

    this.init();
}
