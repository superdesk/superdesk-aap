import {formatDate} from 'superdesk-analytics/client/utils';

MissionReportPreview.$inject = [
    'lodash',
    'gettext',
    'moment',
    'config',
    'metadata',
    'ingestSources',
    'desks',
    '$q',
];

/**
 * @ngdoc directive
 * @module superdesk.aap.mission_report
 * @name sdMissionReportPreview
 * @requires lodash
 * @requires gettext
 * @requires moment
 * @requires config
 * @requires metadata
 * @requires ingestSources
 * @requires desks
 * @requires $q
 * @description Directive that renders the parameters for the saved Mission Report
 */
export function MissionReportPreview(
    _,
    gettext,
    moment,
    config,
    metadata,
    ingestSources,
    desks,
    $q
) {
    return {
        template: require('../views/mission-report-preview.html'),
        link: function(scope) {
            const params = _.get(scope.report, 'params') || {};

            // Retrieve metadata, ingest sources and desk information
            // So that we can convert _id/qcode to their respective names
            $q.all([
                metadata.initialize(),
                ingestSources.initialize(),
                desks.initialize()
            ]).then(() => {
                scope.stages = _.map(
                    _.get(params, 'must_not.stages') || [],
                    (stage_id) => {
                        const stage = _.get(desks.stageLookup, stage_id) || {};
                        const desk = _.get(desks.deskLookup, stage.desk) || {};

                        return (desk.name || '') + '/' + (stage.name || '')}
                ).join(', ');

                scope.ingest = _.map(
                    _.get(params, 'must_not.ingest_providers') || [],
                    (ingest_id) => {
                        const provider = _.get(ingestSources.providersLookup, ingest_id);

                        return provider.name || '';
                    }
                ).join(', ');

                scope.categories = _.map(
                    _.get(params, 'must_not.categories') || [],
                    (qcode) => {
                        const category = _.find(metadata.values.categories, (cat) => cat.qcode === qcode);

                        return category.name || ''
                    }
                ).join(', ');

                scope.genres = _.map(
                    _.get(params, 'must_not.genre') || [],
                    (qcode) => {
                        const genre = _.find(metadata.values.genre, (genre) => genre.qcode === qcode);

                        return genre.name || ''
                    }
                ).join(', ');
            });

            if (params.date_filter === 'yesterday') {
                scope.dates = gettext('Yesterday')
            } else if (params.date_filter === 'day') {
                scope.dates = formatDate(moment, config, params.date);
            }
        },
    };
}
