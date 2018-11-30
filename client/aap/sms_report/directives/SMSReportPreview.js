SMSReportPreview.$inject = [];

/**
 * @ngdoc directive
 * @module superdesk.aap.sms_report
 * @name sdSMSReportPreview
 * @description Directive that renders the parameters for the saved SMS Report
 */
export function SMSReportPreview() {
    return {template: require('../views/sms-report-preview.html')};
}
