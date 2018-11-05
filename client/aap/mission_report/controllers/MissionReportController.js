import {DATE_FILTERS} from 'superdesk-analytics/client/search/directives/DateFilters.js';

MissionReportController.$inject = [
    '$scope',
    'savedReports',
    'notify',
    'lodash',
    'searchReport',
    '$q',
    'missionReportChart',
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
 * @description Controller for the Mission Analytics report
 */
export function MissionReportController(
    $scope,
    savedReports,
    notify,
    _,
    searchReport,
    $q,
    missionReportChart
) {
    /**
     * @ngdoc method
     * @name MissionReportController#init
     * @description Initializes the scope parameters for use with the form and charts
     */
    this.init = () => {
        $scope.ready = false;
        $scope.currentTab = 'parameters';
        $scope.dateFilters = [
            DATE_FILTERS.YESTERDAY,
            DATE_FILTERS.RELATIVE,
        ];

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
            params: {
                dates: {
                    filter: 'yesterday',
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
            },
            report: 'mission_report',
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
     * @name MissionReportController#runQuery
     * @returns {Promise<Object>} - Search API query response
     * @description Sends the current form parameters to the search API
     */
    this.runQuery = (params) => searchReport.query(
        'mission_report',
        params,
        true
    );

    /**
     * @ngdoc method
     * @name MissionReportController#generate
     * @description Using the current form parameters, query the Search API and update the chart configs
     */
    $scope.generate = () => {
        $scope.changeContentView('report');

        const params = _.cloneDeep($scope.currentParams.params);

        this.runQuery(params).then((data) => {
            missionReportChart.createChart(data, params)
                .then((config) => {
                    $scope.changeReportParams(config)
                });
        }).catch((error) => {
            notify.error(error);
        });
    };

    $scope.getReportParams = () => (
        $q.when(_.cloneDeep($scope.currentParams))
    );

    /**
     * @ngdoc method
     * @name MissionReportController#changeTab
     * @param {String} tabName - The name of the tab to change to
     * @description Change the current tab in the filters panel
     */
    $scope.changeTab = (tabName) => {
        $scope.currentTab = tabName;
    };

    this.init();
}
