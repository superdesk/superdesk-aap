import {SDChart} from 'superdesk-analytics/client/charts/SDChart';

MissionReportChart.$inject = [
    'lodash',
    'gettext',
    'moment',
    'chartConfig',
    '$q',
    'metadata',
];

/**
 * @ngdoc service
 * @module superdesk.aap.mission_report
 * @name MissionReportChart
 * @requires lodash
 * @requires gettext
 * @requires moment
 * @requires metadata
 * @description Service to create Highcharts configs based on Mission Report data from the API
 */
export function MissionReportChart(_, gettext, moment, chartConfig, $q, metadata) {
    /**
     * @ngdoc method
     * @name MissionReportChart#genSummaryChart
     * @param {Object} data - The data used to generate the summary chart
     * @param {Object} params - The report parameters
     * @return {Object} - The Highcharts config
     * @description Generate the line chart to displaying the overall summary of the report
     */
    this.genSummaryChart = (data, params) => {
        const chart = new SDChart.Chart({
            id: 'mission_report_summary',
            title: gettext('Mission Report Summary'),
            subtitle: chartConfig.generateSubtitleForDates(params),
            chartType: 'highcharts',
            height: 300,
            dataLabels: false,
            tooltipHeader: '{point.x}: {point.y}',
            tooltipPoint: '',
            defaultConfig: chartConfig.defaultConfig,
        });

        chart.setTranslation('summary', gettext('Summary'), {
            total_stories: gettext('Total Stories'),
            results: gettext('Results/Fields/Comment/Betting'),
            new_stories: gettext('New Stories'),
            rewrites: gettext('Updates'),
            corrections: gettext('Corrections'),
            kills: gettext('Kills'),
            takedowns: gettext('Takedowns'),
        });

        chart.addAxis()
            .setOptions({
                type: 'category',
                defaultChartType: 'line',
                yTitle: gettext('Published Stories'),
                categoryField: 'summary',
                categories: [
                    'total_stories',
                    'new_stories',
                    'results',
                    'rewrites',
                    'corrections',
                    'kills',
                    'takedowns'
                ],
            })
            .addSeries()
            .setOptions({
                field: 'summary',
                data: [
                    _.get(data, 'total_stories') || 0,
                    _.get(data, 'new_stories.count') || 0,
                    _.get(data, 'new_stories.categories.results') || 0,
                    _.get(data, 'rewrites') || 0,
                    _.get(data, 'corrections.length') || 0,
                    _.get(data, 'kills.length') || 0,
                    _.get(data, 'takedowns.length') || 0
                ],
            });

        return chart.genConfig();
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#genCategoryChart
     * @param {Object} data - The data used to generate the category chart
     * @return {Object} - The Highcharts config
     * @description Generate the bar chart to displaying the category report
     */
    this.genCategoryChart = (data) => {
        const chart = new SDChart.Chart({
            id: 'mission_report_categories',
            title: gettext('New Stories By Category'),
            dataLabels: false,
            tooltipHeader: '{point.x}: {point.y}',
            tooltipPoint: '',
            fullHeight: true,
        });

        const categories = _.keyBy(_.get(metadata, 'values.categories') || [], 'qcode');

        if (_.get(data, 'new_stories.categories.results', 0) > 0) {
            categories['results'] = {
                qcode: 'results',
                name: gettext('Results/Fields/Comment/Betting')
            };
        }

        const translations = {};
        const source = {};
        const series = _.get(data, 'new_stories.categories') || {};

        Object.keys(categories).forEach((qcode) => {
            if (!(qcode in series)) {
                return;
            }

            source[qcode] = series[qcode] || 0;
            translations[qcode] = categories[qcode].name + (
                qcode === 'results' ? '' : ` (${qcode.toUpperCase()})`
            );
        });

        chart.setTranslation('category', gettext('Category'), translations);

        chart.addAxis()
            .setOptions({
                type: 'category',
                defaultChartType: 'bar',
                yTitle: gettext('Category'),
                xTitle: gettext('Published Stories'),
                categoryField: 'category',
                categories: _.sortBy(Object.keys(source)),
                stackLabels: true,
            })
            .addSeries()
            .setOptions({
                field: 'category',
                data: _.map(
                    _.sortBy(Object.keys(source)),
                    (qcode) => _.get(source, qcode) || 0
                ),
                stack: 0,
                stackType: 'normal'
            });

        return chart.genConfig();
    };

    this.genTableConfig = ({
        id,
        title,
        items,
        fields,
    }) => {
        const chart = new SDChart.Chart({
            id: id,
            title: title,
            chartType: 'table',
            defaultConfig: chartConfig.defaultConfig,
        });

        const axis = chart.addAxis()
            .setOptions({
                defaultChartType: 'table',
                xTitle: 'Sent',
                includeTotal: false,
                categories: _.map(items, (item) => moment(
                    _.get(item, 'versioncreated') ||
                    _.get(item, '_updated')
                ).format('DD/MM/YYYY HH:mm')),
            });

        fields.forEach((field) => {
            axis.addSeries()
                .setOptions({
                    name: field[0],
                    data: _.map(items, (item) => (
                        _.get(item, field[1]) || ''
                    )),
                });
        });

        return chart.genConfig();
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#genCorrectionsChart
     * @param {Object} data - The data used to generate the corrections table chart
     * @return {Object} - The table config
     * @description Generate the table displaying the corrections
     */
    this.genCorrectionsChart = (data) => {
        const corrections = _.get(data, 'corrections') || [];
        const numCorrections = corrections.length;
        const title = `There were ${numCorrections} corrections issued`;

        return this.genTableConfig({
            id: 'mission_report_corrections',
            title: title,
            items: corrections,
            fields: [['Slugline', 'slugline'], ['TakeKey', 'anpa_take_key'], ['Ednote', 'ednote']]
        });
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#genKillsChart
     * @param {Object} data - The data used to generate the kills table chart
     * @return {Object} - The table config
     * @description Generate the table displaying the kills
     */
    this.genKillsChart = (data) => {
        const kills = _.get(data, 'kills') || [];
        const numKills = kills.length;
        const title = `There were ${numKills} kills issued`;

        return this.genTableConfig({
            id: 'mission_report_kills',
            title: title,
            items: kills,
            fields: [['Slugline', 'slugline'], ['Reasons', '_reasons']]
        });
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#genTakedownsChart
     * @param {Object} data - The data used to generate the takedowns table chart
     * @return {Object} - The table config
     * @description Generate the table displaying the takedowns
     */
    this.genTakedownsChart = (data) => {
        const takedowns = _.get(data, 'takedowns') || [];
        const numTakedowns = takedowns.length;
        const title = `There were ${numTakedowns} takedowns issued`;

        return this.genTableConfig({
            id: 'mission_report_takedowns',
            title: title,
            items: takedowns,
            fields: [['Slugline', 'slugline'], ['Reasons', '_reasons']]
        });
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#genUpdatesChart
     * @param {Object} data - The data used to generate the updates table chart
     * @return {Object} - The table config
     * @description Generate the table displaying the updates
     */
    this.genUpdatesChart = (data) => {
        const numUpdates = _.get(data, 'rewrites') || 0;

        return {
            id: 'mission_report_updates',
            type: 'table',
            chart: {type: 'column'},
            headers: ['Sent', 'Slugline', 'TakeKey', 'Ednote'],
            title: `There were ${numUpdates} updates issued`,
            rows: [],
        }
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#genSMSAlertsChart
     * @param {Object} data - The data used to generate the SMS Alerts chart
     * @description Generate the SMS Alerts chart config
     */
    this.genSMSAlertsChart = (data) => {
        const numSMSAlerts = _.get(data, 'sms_alerts') || 0;

        return {
            id: 'mission_report_sms_alerts',
            type: 'table',
            chart: {type: 'column'},
            headers: ['Send', 'Slugline', 'TakeKey', 'Ednote'],
            title: `There were ${numSMSAlerts} SMS alerts issued`,
            rows: [],
        }
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#createChart
     * @param {Object} data - The data used to generate the MissionReport chart
     * @param {Object} params - The report parameters
     * @description Generate the chart configs for the MissionReport charts
     */
    this.createChart = function(data, params) {
        if ((_.get(data, 'total_stories') || 0) < 1) {
            return $q.when({
                charts: [{
                    id: 'mission_report_empty',
                    type: 'table',
                    title: gettext('There were no stories published'),
                    rows: [],
                }],
            });
        }

        return metadata.initialize()
            .then(() => {
                const reportEnabled = (name) => _.get(params, `reports[${name}]`, true);

                const configs = [];

                if (reportEnabled('summary')) {
                    configs.push(this.genSummaryChart(data, params));
                }

                if (reportEnabled('categories')) {
                    configs.push(this.genCategoryChart(data));
                }

                if (reportEnabled('corrections')) {
                    configs.push(this.genCorrectionsChart(data));
                }

                if (reportEnabled('kills')) {
                    configs.push(this.genKillsChart(data));
                }

                if (reportEnabled('takedowns')) {
                    configs.push(this.genTakedownsChart(data));
                }

                if (reportEnabled('sms_alerts')) {
                    configs.push(this.genSMSAlertsChart(data));
                }

                if (reportEnabled('updates')) {
                    configs.push(this.genUpdatesChart(data));
                }

                return {
                    charts: configs,
                    multiChart: false,
                    marginBottom: true,
                }
            });
    }
}
