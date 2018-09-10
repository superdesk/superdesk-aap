import {getErrorMessage} from 'superdesk-analytics/client/utils';

MissionReportController.$inject = [
    '$scope',
    '$rootScope',
    '$location',
    'config',
    'savedReports',
    'gettext',
    'notify',
    'lodash',
    '$sce',
    'searchReport',
    'metadata',
    'ingestSources',
    'moment',
    'desks',
    '$q',
    'session',
    'missionReportChart',
];

/**
 * @ngdoc controller
 * @module superdesk.aap.mission_report
 * @name MissionReportController
 * @requires $scope
 * @requires $rootScope
 * @requires $location
 * @requires config
 * @requires savedReports
 * @requires gettext
 * @requires notify
 * @requires lodash
 * @requires $sce
 * @requires searchReport
 * @requires metadata
 * @requires ingestSources
 * @requires moment
 * @requires desks
 * @requires $q
 * @requires session
 * @requires missionReportChart
 * @description Controller for the Mission Analytics report
 */
export function MissionReportController(
    $scope,
    $rootScope,
    $location,
    config,
    savedReports,
    gettext,
    notify,
    _,
    $sce,
    searchReport,
    metadata,
    ingestSources,
    moment,
    desks,
    $q,
    session,
    missionReportChart
) {
    /**
     * @ngdoc method
     * @name MissionReportController#init
     * @description Initializes the scope parameters for use with the form and charts
     */
    this.init = () => {
        $scope.currentPanel = 'advanced';

        $q.all([
            metadata.initialize(),
            ingestSources.initialize(),
            desks.initialize()
        ]).then(() => {
            $scope.metadata = metadata.values;
            $scope.ingest_providers = ingestSources.providers;

            $scope.form_metadata = {
                categories: [],
                genre: [],
                ingest_providers: [],
                stages: []
            };

            const desk_stages = [];

            _.forEach((desks.deskStages), (stages, desk_id) => {
                const desk_name = _.get(desks.deskLookup, `[${desk_id}].name`) || '';

                desk_stages.push(
                    ...stages.map((stage) => ({
                        _id: stage._id,
                        name: desk_name + "/" + stage.name
                    }))
                );
            });

            $scope.desk_stages = desk_stages;

            this.initDefaultParams();
        });

        this.deregisterReportsUpdate = $rootScope.$on(
            'savedreports:update',
            angular.bind(this, this.onSavedReportUpdated)
        );
        $scope.$on('$destroy', angular.bind(this, this.onDestroy));
    };

    /**
     * @ngdoc method
     * @name MissionReportController#initDefaultParams
     * @description Sets the default report parameters
     */
    this.initDefaultParams = () => {
        $scope.currentTemplate = {};
        $scope.currentParams = {
            params: {
                date_filter: 'yesterday',
                size: 2000,
                repos: {published: true},
                must_not: {
                    categories: [],
                    genre: [],
                    ingest_providers: [],
                    stages: [],
                },
            },
            report: 'mission_report',
        };

        $scope.defaultReportParams = _.cloneDeep($scope.currentParams);

        // If a savedReport (template) is in the url, then load and apply its values
        if ($location.search().template) {
            savedReports.fetchById($location.search().template)
                .then((savedReport) => {
                    $scope.selectReport(savedReport);
                }, (error) => {
                    if (_.get(error, 'status') === 404) {
                        notify.error(gettext('Saved report not found!'));
                    } else {
                        notify.error(
                            getErrorMessage(error, gettext('Failed to load the saved report!'))
                        );
                    }
                });
        }
    };

    $scope.isDirty = () => true;

    /**
     * @ngdoc method
     * @name MissionReportController#clearFilters
     * @description Sets the current report parameters to the default values, and clears the currently
     * selected saved report/template
     */
    $scope.clearFilters = () => {
        $scope.currentParams = _.cloneDeep($scope.defaultReportParams);
        $scope.currentTemplate = {};
        $location.search('template', null);
    };

    /**
     * @ngdoc method
     * @name MissionReportController#selectReport
     * @param {object} selectedReport - The saved report/template to select
     * @description Selects the provided saved report/template and sets the form values
     */
    $scope.selectReport = (selectedReport) => {
        $scope.currentTemplate = _.cloneDeep(selectedReport);
        $scope.currentParams = _.cloneDeep(selectedReport);
        $scope.changePanel('advanced');
        $location.search('template', _.get(selectedReport, '_id'));

        const mustNot = _.get($scope, 'currentParams.params.must_not') || {};
        const categories = _.keyBy($scope.metadata.categories, 'qcode');
        const genres = _.keyBy($scope.metadata.genre, 'qcode');
        const providers = _.keyBy($scope.ingest_providers, '_id');
        const desk_stages = _.keyBy($scope.desk_stages, '_id');

        $scope.form_metadata.genre = (_.get(mustNot, 'genre') || {}).map(
            (qcode) => _.get(genres, qcode) || {}
        );

        $scope.form_metadata.categories = (_.get(mustNot, 'categories') || {}).map(
            (qcode) => _.get(categories, qcode) || {}
        );

        $scope.form_metadata.ingest_providers = (_.get(mustNot, 'ingest_providers') || {}).map(
            (ingest_id) => _.get(providers, ingest_id) || {}
        );

        $scope.form_metadata.stages = (_.get(mustNot, 'stages') || {}).map(
            (stage_id) => _.get(desk_stages, stage_id) || {}
        );
    };

    /**
     * @ngdoc method
     * @name MissionReportController#onReportSaved
     * @param {Promise<object>} response - Promise with the API save response
     * @description If the save is successful, select that report and notify the user, otherwise notify the
     * user if the save fails
     */
    $scope.onReportSaved = (response) => (
        response.then((savedReport) => {
            $scope.selectReport(savedReport);
            notify.success(gettext('Report saved!'));
        }, (error) => {
            notify.error(
                getErrorMessage(error, gettext('Failed to delete the saved report!'))
            );
        })
    );

    /**
     * @ngdoc method
     * @name MissionReportController#onReportDeleted
     * @param {Promise<object>} response - Promise with the API remove response
     * @description Notify the user of the result when deleting a saved report
     */
    $scope.onReportDeleted = (response) => (
        response.then(() => {
            notify.success(gettext('Report deleted!'));
        }, (error) => {
            notify.error(
                getErrorMessage(error, gettext('Failed to delete the saved report!'))
            );
        })
    );

    /**
     * @ngdoc method
     * @name MissionReportController#onDestroy
     * @description Make sure to reset the defaultReportParams to empty object on controller destruction
     */
    this.onDestroy = () => {
        $scope.defaultReportParams = {};
        this.deregisterReportsUpdate();
    };

    /**
     * @ngdoc method
     * @name MissionReportController#onSavedReportUpdated
     * @param {object} event - The websocket event object
     * @param {object} data - The websocket data (saved report details)
     * @description Respond when a saved report is created/updated/deleted
     * (from a websocket notification from the server)
     */
    this.onSavedReportUpdated = (event, data) => {
        const reportType = _.get(data, 'report_type');
        const operation = _.get(data, 'operation');
        const reportId = _.get(data, 'report_id');
        const userId = _.get(data, 'user_id');
        const sessionId = _.get(data, 'session_id');

        const currentUserId = _.get(session, 'identity._id');
        const currentSessionId = _.get(session, 'sessionId');

        // Disregard if this update is not the same type as this report
        if (reportType !== 'mission_report') {
            return;
        }

        // Disregard if this update is not for the currently used template
        if (reportId !== _.get($scope.currentTemplate, '_id')) {
            return;
        }

        if (operation === 'delete') {
            // If the saved report was deleted, then unset the currentTemplate
            $scope.$applyAsync(() => {
                $scope.currentTemplate = {};

                // Remove the saved report ID from the url parameters
                $location.search('template', null);

                if (sessionId !== currentSessionId) {
                    notify.warning(gettext('The Saved Report you are using was deleted!'));
                }
            });
        } else if (operation === 'update' && userId !== currentUserId) {
            // Otherwise if this report was updated in a different session,
            // then notify the current user
            $scope.$applyAsync(() => {
                notify.warning(gettext('The Saved Report you are using was updated!'));
            });
        }
    };

    /**
     * @ngdoc method
     * @name MissionReportController#changePanel
     * @param {String} panelName - The name of the panel to change to
     * @description Changes the current outter tab (panel) to use in the side panel
     */
    $scope.changePanel = (panelName) => {
        $scope.currentPanel = panelName;
    };

    /**
     * @ngdoc method
     * @name MissionReportController#onMultiSelectChange
     * @param {Object} item - The updated values
     * @param {String} field - The name of the field that changed
     * @description onChange callback for input fields that accept multiple values. Converts the value
     * to/from cv qcode/name
     */
    $scope.onMultiSelectChange = (item, field) => {
        if (field === 'genre') {
            $scope.currentParams.params.must_not.genre = $scope.form_metadata.genre.map(
                (genre) => genre.qcode
            );
        } else if (field === 'categories') {
            $scope.currentParams.params.must_not.categories = $scope.form_metadata.categories.map(
                (category) => category.qcode
            );
        } else if (field === 'ingest_providers') {
            $scope.currentParams.params.must_not.ingest_providers = $scope.form_metadata.ingest_providers.map(
                (ingest) => ingest._id
            );
        } else if (field === 'stages') {
            $scope.currentParams.params.must_not.stages = $scope.form_metadata.stages.map(
                (stage) => stage._id
            );
        }
    };

    /**
     * @ngdoc method
     * @name MissionReportController#runQuery
     * @returns {Promise<Object>} - Search API query response
     * @description Sends the current form parameters to the search API
     */
    this.runQuery = () => searchReport.query(
        'mission_report',
        $scope.currentParams.params
    );

    /**
     * @ngdoc method
     * @name MissionReportController#generate
     * @description Using the current form parameters, query the Search API and update the chart configs
     */
    $scope.generate = () => {
        this.runQuery().then((data) => {
            $scope.changeReportParams(
                missionReportChart.createChart(data, $scope.metadata)
            );
        }).catch((error) => {
            notify.error(error);
        });
    };

    this.init();
}
