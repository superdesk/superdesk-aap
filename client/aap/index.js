import './publish';
import './mission_report';
import './sms_report';

import {startApp} from 'superdesk-core/scripts/index';
import planningExtension from 'superdesk-planning/client/planning-extension/dist/src/extension';

setTimeout(() => {
    startApp(
        [planningExtension],
        {},
    );
});

export default angular.module('aap.apps', [
    'aap.apps.publish',
    'aap.apps.mission-report',
    'aap.apps.sms-report',
]);
