import {startApp} from 'superdesk-core/scripts/index';
import planningExtension from 'superdesk-planning/client/planning-extension/dist/extension';
import './aap/index.js';

setTimeout(() => {
    startApp(
        [planningExtension],
        {},
    );
});

export default angular.module('main.superdesk', []);