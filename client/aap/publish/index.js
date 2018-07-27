

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
}

export default angular.module('aap.apps.publish', [])
    .run(runConfig);
