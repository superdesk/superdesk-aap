import {getErrorMessage, getUtcOffsetInMinutes} from 'superdesk-analytics/client/utils';
import {DATE_FILTERS} from 'superdesk-analytics/client/search/directives/DateFilters.js';
import {SDChart} from 'superdesk-analytics/client/charts/SDChart';

SMSReportController.$inject = [
    '$scope',
    'savedReports',
    'chartConfig',
    'lodash',
    'searchReport',
    'moment',
    'notify',
    'gettext',
    '$q',
    'config',
    'deployConfig',
];


export function SMSReportController(
    $scope,
    savedReports,
    chartConfig,
    _,
    searchReport,
    moment,
    notify,
    gettext,
    $q,
    config,
    deployConfig
) {
    this.init = () => {
        $scope.currentTab = 'parameters';

        $scope.dateFilters = [
            DATE_FILTERS.YESTERDAY,
            DATE_FILTERS.LAST_WEEK,
            DATE_FILTERS.LAST_MONTH,
            DATE_FILTERS.RANGE,
        ];

        this.initDefaultParams();
        savedReports.selectReportFromURL();

        this.chart = chartConfig.newConfig('chart', _.get($scope, 'currentParams.params.chart.type'));
        $scope.updateChartConfig();
    };

    this.initDefaultParams = () => {
        $scope.item_states = searchReport.filterItemStates(
            ['published', 'killed', 'corrected', 'recalled']
        );

        $scope.chart_types = chartConfig.filterChartTypes(
            ['bar', 'column']
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
            report: 'sms_report',
            params: {
                dates: {
                    filter: 'range',
                    start: moment()
                        .subtract(30, 'days')
                        .format(config.model.dateformat),
                    end: moment().format(config.model.dateformat),
                },
                must: {},
                must_not: {},
                repos: {
                    ingest: false,
                    archive: false,
                    published: true,
                    archived: true,
                },
                chart: {
                    type: _.get($scope, 'chart_types[1].qcode') || 'column',
                    sort_order: 'desc',
                    title: null,
                    subtitle: null,
                },
                histogram: {
                    interval: 'daily',
                },
            },
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

    $scope.$watch(() => savedReports.currentReport._id, (newReportId) => {
        if (newReportId) {
            $scope.currentParams = _.cloneDeep(savedReports.currentReport);
            $scope.changePanel('advanced');
        } else {
            $scope.currentParams = _.cloneDeep($scope.defaultReportParams);
        }
    });

    $scope.onDateFilterChange = () => {
        if ($scope.currentParams.params.dates.filter !== 'range') {
            $scope.currentParams.params.dates.start = null;
            $scope.currentParams.params.dates.end = null;
        }

        $scope.updateChartConfig();
    };

    $scope.runQuery = (params) => searchReport.query(
        'sms_report',
        params,
        true
    );

    $scope.generate = () => {
        $scope.changeContentView('report');

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

    $scope.changeTab = (tabName) => {
        $scope.currentTab = tabName;
    };

    this.createChart = (report) => {
        // Calculate the UTC Offset in minutes for the start date of the results
        // This will cause an issue if a report crosses over the daylight savings change
        // Any data after the daylight savings change will be 1 hour out
        const utcOffset = getUtcOffsetInMinutes(
            report['start'],
            config.defaultTimezone,
            moment
        );

        const chart = new SDChart.Chart({
            id: 'sms_report',
            chartType: 'highcharts',
            title: $scope.generateTitle(),
            subtitle: $scope.generateSubtitle(),
            startOfWeek: deployConfig.getSync('start_of_week', 0),
            timezoneOffset: utcOffset,
            useUTC: false,
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

    $scope.getReportParams = () => (
        $q.when(_.cloneDeep($scope.currentParams))
    );

    this.init();
}
