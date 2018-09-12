/**
 * This file is part of Superdesk.
 *
 * Copyright 2018 Sourcefabric z.u. and contributors.
 *
 * For the full copyright and license information, please see the
 * AUTHORS and LICENSE files distributed with this source code, or
 * at https://www.sourcefabric.org/superdesk/license
 */

import * as svc from './services';
import * as ctrl from './controllers';
import * as directives from './directives';

function cacheIncludedTemplates($templateCache) {
    $templateCache.put(
        'mission-report-panel.html',
        require('./views/mission-report-panel.html')
    );
    $templateCache.put(
        'mission-report-parameters.html',
        require('./views/mission-report-parameters.html')
    );
    $templateCache.put(
        'mission-report-preview.html',
        require('./views/mission-report-preview.html')
    );
}
cacheIncludedTemplates.$inject = ['$templateCache'];

/**
 * @ngdoc module
 * @module aap.apps
 * @name mission-report
 * @packageName mission-report
 * @description AAP analytics generate mission report.
 */
angular.module('aap.apps.mission-report', ['superdesk.analytics'])
    .service('missionReportChart', svc.MissionReportChart)

    .controller('MissionReportController', ctrl.MissionReportController)

    .directive('sdMissionReportPreview', directives.MissionReportPreview)

    .run(cacheIncludedTemplates)

    .config(['reportsProvider', 'gettext', function(reportsProvider, gettext) {
        reportsProvider.addReport({
            id: 'mission_report',
            label: gettext('Mission'),
            sidePanelTemplate: 'mission-report-panel.html',
            priority: 500,
            privileges: {mission_report: 1},
            allowScheduling: true,
        });
    }]);
