/**
 * This file is part of Superdesk.
 *
 * Copyright 2018 Sourcefabric z.u. and contributors.
 *
 * For the full copyright and license information, please see the
 * AUTHORS and LICENSE files distributed with this source code, or
 * at https://www.sourcefabric.org/superdesk/license
 */

import * as ctrl from './controllers';
import * as directives from './directives';

function cacheIncludedTemplates($templateCache) {
    $templateCache.put(
        'sms-report-panel.html',
        require('./views/sms-report-panel.html')
    );
    $templateCache.put(
        'sms-report-parameters.html',
        require('./views/sms-report-parameters.html')
    );
}
cacheIncludedTemplates.$inject = ['$templateCache'];

/**
 * @ngdoc module
 * @module superdesk.analytics.sms-report
 * @name superdesk.analytics.sms-report
 * @packageName analytics.sms-report
 * @description Superdesk analytics generate report of SMS statistics.
 */
angular.module('aap.apps.sms-report', [])
    .controller('SMSReportController', ctrl.SMSReportController)

    .directive('sdaSmsReportPreview', directives.SMSReportPreview)

    .run(cacheIncludedTemplates)

    .config(['reportsProvider', 'gettext', function(reportsProvider, gettext) {
        reportsProvider.addReport({
            id: 'sms_report',
            label: gettext('SMS'),
            sidePanelTemplate: 'sms-report-panel.html',
            priority: 600,
            privileges: {sms_report: 1},
            allowScheduling: true,
        });
    }]);
