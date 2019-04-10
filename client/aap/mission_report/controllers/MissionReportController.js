import {DATE_FILTERS} from 'superdesk-analytics/client/search/common';

MissionReportController.$inject = [
    '$scope',
    'savedReports',
    'notify',
    'lodash',
    'searchReport',
    '$q',
    'missionReportChart',
    'reportConfigs',
];

/**
 * @ngdoc controller
 * @module superdesk.aap.mission_report
 * @name MissionReportController
 * @requires $scope
 * @requires savedReports
 * @requires notify
 * @requires lodash
 * @requires searchReport
 * @requires $q
 * @requires missionReportChart
 * @requires reportConfigs
 * @description Controller for the Mission Analytics report
 */
export function MissionReportController(
    $scope,
    savedReports,
    notify,
    _,
    searchReport,
    $q,
    missionReportChart,
    reportConfigs
) {
    const reportName = 'mission_report';
    /**
     * @ngdoc method
     * @name MissionReportController#init
     * @description Initializes the scope parameters for use with the form and charts
     */
    this.init = () => {
        $scope.form = {
            datesError: null,
            submitted: false,
            showErrors: false,
        };
        $scope.config = reportConfigs.getConfig(reportName);
        $scope.ready = false;

        this.initDefaultParams();

        savedReports.selectReportFromURL();

        $scope.ready = true;
    };

    /**
     * @ngdoc method
     * @name MissionReportController#initDefaultParams
     * @description Sets the default report parameters
     */
    this.initDefaultParams = () => {
        $scope.currentParams = {
            report: reportName,
            params: $scope.config.defaultParams({
                dates: {
                    filter: DATE_FILTERS.YESTERDAY,
                },
                size: 2000,
                repos: {published: true},
                must_not: {
                    categories: [],
                    genre: [],
                    ingest_providers: [],
                    stages: [],
                },
                reports: {
                    summary: true,
                    categories: true,
                    corrections: true,
                    kills: true,
                    takedowns: true,
                    updates: true,
                    sms_alerts: true,
                },
            }),
        };

        $scope.defaultReportParams = _.cloneDeep($scope.currentParams);
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

    /**
     * @ngdoc method
     * @name MissionReportController#generate
     * @description Using the current form parameters, query the Search API and update the chart configs
     */
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

        $scope.runQuery(params).then((data) => {
            missionReportChart.createChart(data, params)
                .then((config) => {
                    $scope.changeReportParams(config);
                    $scope.form.submitted = false;
                });
        }).catch((error) => {
            notify.error(error);
        });
    };

    $scope.getReportParams = () => (
        $q.when(_.cloneDeep($scope.currentParams))
    );

    this.init();
}
