import {startApp} from 'superdesk-core/scripts/index';
import './aap/index.js';

setTimeout(() => {
    startApp(
        [
            {
                id: 'planning-extension',
                load: () => import('superdesk-planning/client/planning-extension'),
            },
        ],
        {},
    );
});

export default angular.module('main.superdesk', []);