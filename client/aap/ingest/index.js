

runPlanning.$inject = ['ingestSources', '$templateCache'];
function runPlanning(ingestSources, $templateCache) {
    // register new ingest feeding service and custom settings template
    $templateCache.put(
        'aap/ingest/views/aapSportsHttp.html',
        require('./views/aapSportsHttp.html')
    );
    ingestSources.registerFeedingService('aap_sports_http', {
        label: 'AAP Sports Results Feed',
        templateUrl: 'aap/ingest/views/aapSportsHttp.html'
    });
}

export default angular.module('aap.apps.ingest', [])
    .run(runPlanning)