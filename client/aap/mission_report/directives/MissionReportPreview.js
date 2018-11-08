MissionReportPreview.$inject = [];

/**
 * @ngdoc directive
 * @module superdesk.aap.mission_report
 * @name sdMissionReportPreview
 * @description Directive that renders the parameters for the saved Mission Report
 */
export function MissionReportPreview() {
    return {template: require('../views/mission-report-preview.html')};
}
