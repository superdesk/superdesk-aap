runConfig.$inject = ['adminPublishSettingsService', '$templateCache'];
function runConfig(adminPublishSettingsService, $templateCache) {
    // register new publish service
    $templateCache.put(
        'aap/publish/views/socket-config.html',
        require('./views/socket-config.html')
    );
    adminPublishSettingsService.registerTransmissionService('socket', {
        label: 'Socket',
        templateUrl: 'aap/publish/views/socket-config.html',
    });

    // register new publish service
    $templateCache.put(
        'aap/publish/views/http-push-agenda-config.html',
        require('./views/http-push-agenda-config.html')
    );
    adminPublishSettingsService.registerTransmissionService('http_agenda_push', {
        label: 'HTTP Push to Agenda',
        templateUrl: 'aap/publish/views/http-push-agenda-config.html',

    });
}

export default angular.module('aap.apps.publish', [])
    .run(runConfig);

