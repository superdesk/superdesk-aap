

runPlanning.$inject = ['adminPublishSettingsService', '$templateCache'];
function runPlanning(adminPublishSettingsService, $templateCache) {
    // register new publish service 
    $templateCache.put(
        'aap/publish/views/http-push-agenda-config.html',
        require('./views/http-push-agenda-config.html')
    );
    adminPublishSettingsService.registerTransmissionService('http_agenda_push', {
        label: 'HTTP Push to Agenda',
        templateUrl: 'aap/publish/views/http-push-agenda-config.html'
    });
}

export default angular.module('aap.apps.publish', [])
    .run(runPlanning)