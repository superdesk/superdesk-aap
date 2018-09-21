MissionReportController.$inject = [
    '$scope',
    'savedReports',
    'notify',
    'lodash',
    '$sce',
    'searchReport',
    'metadata',
    'ingestSources',
    'moment',
    'desks',
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
 * @requires $sce
 * @requires searchReport
 * @requires metadata
 * @requires ingestSources
 * @requires moment
 * @requires desks
 * @requires $q
 * @requires missionReportChart
 * @description Controller for the Mission Analytics report
 */
export function MissionReportController(
    $scope,
    savedReports,
    notify,
    _,
    $sce,
    searchReport,
    metadata,
    ingestSources,
    moment,
    desks,
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

            savedReports.selectReportFromURL();

            $scope.ready = true;
        });
    };

    /**
     * @ngdoc method
     * @name MissionReportController#initDefaultParams
     * @description Sets the default report parameters
     */
    this.initDefaultParams = () => {
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
    };

    $scope.isDirty = () => true;

    $scope.$watch(() => savedReports.currentReport, (newReport) => {
        if (!$scope.ready) {
            return;
        } else if (!_.get(newReport, '_id')) {
            $scope.currentParams = _.cloneDeep($scope.defaultReportParams);
        } else {
            $scope.currentParams = _.cloneDeep(savedReports.currentReport);
            $scope.changePanel('advanced');
        }

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
    });

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
