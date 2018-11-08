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
        const totalStories = _.get(data, 'total_stories') || 0;

        chartConfig.translations.summary = {
            title: gettext('Summary'),
            names: {
                total_stories: gettext('Total Stories'),
                results: gettext('Results/Fields/Comment/Betting'),
                new_stories: gettext('New Stories'),
                rewrites: gettext('Updates'),
                corrections: gettext('Corrections'),
                kills: gettext('Kills'),
                takedowns: gettext('Takedowns'),
            },
        };

        const source = {
            total_stories: totalStories,
            new_stories: _.get(data, 'new_stories.count') || 0,
            results: _.get(data, 'new_stories.categories.results') || 0,
            rewrites: _.get(data, 'rewrites.length') || 0,
            corrections: _.get(data, 'corrections.length') || 0,
            kills: _.get(data, 'kills.length') || 0,
            takedowns: _.get(data, 'takedowns.length') || 0,
        };

        const chart = chartConfig.newConfig('mission_report_summary', 'line');

        chart.getChart = () => ({
            type: chart.chartType,
            height: 300,
        });

        chart.getSortedKeys = () => ([
            'total_stories',
            'new_stories',
            'results',
            'rewrites',
            'corrections',
            'kills',
            'takedowns'
        ]);

        chart.getPlotOptions = () => ({
            series: {dataLabels: {enabled: true}},
        });

        chart.title = gettext('Mission Report Summary')

        chart.getSubtitle = () => chartConfig.generateSubtitleForDates(params);

        chart.addSource('summary', source)
        return chart.genConfig()
            .then((config) => {
                config.fullHeight = false;
                delete config.xAxis.title;

                return config;
            });
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#genCategoryChart
     * @param {Object} data - The data used to generate the category chart
     * @return {Object} - The Highcharts config
     * @description Generate the bar chart to displaying the category report
     */
    this.genCategoryChart = (data) => {
        const categories = _.keyBy(_.get(metadata, 'values.categories') || [], 'qcode');

        categories['results'] = {
            qcode: 'results',
            name: gettext('Results/Fields/Comment/Betting')
        };

        const series = _.get(data, 'new_stories.categories') || {};

        const source = {};

        const chart = chartConfig.newConfig('mission_report_categories', 'bar');

        chartConfig.translations.category = {
            title: gettext('CATEGORY'),
            names: {},
        };

        Object.keys(categories).forEach((qcode) => {
            source[qcode] = series[qcode] || 0;
            chartConfig.translations.category.names[qcode] = categories[qcode].name + (
                qcode === 'results' ? '' : ` (${qcode.toUpperCase()})`
            );
        });

        chart.getSortedKeys = (data) => (
            _.sortBy(Object.keys(data))
        );

        chart.getPlotOptions = () => ({
            series: {dataLabels: {enabled: true}},
        });

        chart.title = gettext('New Stories by Category');
        chart.addSource('category', source)

        return chart.genConfig()
            .then((config) => {
                config.fullHeight = true;

                return config;
            });
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#genCorrectionsChart
     * @param {Object} data - The data used to generate the corrections table chart
     * @return {Object} - The table config
     * @description Generate the table displaying the corrections
     */
    this.genCorrectionsChart = (data) => {
        const numCorrections = _.get(data, 'corrections.length') || 0;

        const rows = (_.get(data, 'corrections') || [])
            .map((correction) => ([
                moment(
                    _.get(correction, 'versioncreated') ||
                    _.get(correction, '_updated')
                ).format('DD/MM/YYYY HH:mm'),
                _.get(correction, 'slugline') || '',
                _.get(correction, 'anpa_take_key') || '',
                _.get(correction, 'ednote') || '',
            ]));

        return {
            id: 'mission_report_corrections',
            type: 'table',
            chart: {type: 'column'},
            headers: ['Sent', 'Slugline', 'TakeKey', 'Ednote'],
            title: `There were ${numCorrections} corrections issued`,
            rows: rows,
        }
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#genKillsChart
     * @param {Object} data - The data used to generate the kills table chart
     * @return {Object} - The table config
     * @description Generate the table displaying the kills
     */
    this.genKillsChart = (data) => {
        const numKills = _.get(data, 'kills.length') || 0;

        const rows = (_.get(data, 'kills') || [])
            .map((kill) => ([
                moment(
                    _.get(kill, 'versioncreated') ||
                    _.get(kill, '_updated')
                ).format('DD/MM/YYYY HH:mm'),
                _.get(kill, 'slugline') || '',
                _.get(kill, '_reasons') || '',
            ]));

        return {
            id: 'mission_report_kills',
            type: 'table',
            chart: {type: 'column'},
            headers: ['Sent', 'Slugline', 'Reasons'],
            title: `There were ${numKills} kills issued`,
            rows: rows,
        }
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#genTakedownsChart
     * @param {Object} data - The data used to generate the takedowns table chart
     * @return {Object} - The table config
     * @description Generate the table displaying the takedowns
     */
    this.genTakedownsChart = (data) => {
        const numTakedowns = _.get(data, 'takedowns.length') || 0;

        const rows = (_.get(data, 'takedowns') || [])
            .map((takedown) => ([
                moment(
                    _.get(takedown, 'versioncreated') ||
                    _.get(takedown, '_updated')
                ).format('DD/MM/YYYY HH:mm'),
                _.get(takedown, 'slugline') || '',
                _.get(takedown, '_reasons') || '',
            ]));

        return {
            id: 'mission_report_takedowns',
            type: 'table',
            chart: {type: 'column'},
            headers: ['Sent', 'Slugline', 'Reasons'],
            title: `There were ${numTakedowns} takedowns issued`,
            rows: rows,
        }
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#genUpdatesChart
     * @param {Object} data - The data used to generate the updates table chart
     * @return {Object} - The table config
     * @description Generate the table displaying the updates
     */
    this.genUpdatesChart = (data) => {
        const numUpdates = _.get(data, 'rewrites.length') || 0;

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
        const numSMSAlerts = _.get(data, 'sms_alerts.length') || 0;

        return {
            id: 'mission_report_sms_alerts',
            type: 'table',
            chart: {type: 'column'},
            headers: ['Send', 'Slugline', 'TakeKey', 'Ednote'],
            title: `There were ${numSMSAlerts} SMS alerts issued`,
            rows: [],
        }
    }

    /**
     * @ngdoc method
     * @name MissionReportChart#createChart
     * @param {Object} data - The data used to generate the MissionReport chart
     * @param {Object} params - The report parameters
     * @description Generate the chart configs for the MissionReport charts
     */
    this.createChart = function(data, params) {
        return metadata.initialize()
            .then(() => {
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

                const reportEnabled = (name) => _.get(params, `reports[${name}]`, true);

                const promises = {};

                if (reportEnabled('summary')) {
                    promises.summary = this.genSummaryChart(data, params);
                }

                if (reportEnabled('categories')) {
                    promises.categories = this.genCategoryChart(data);
                }

                return $q.all(promises)
                    .then((charts) => {
                        const configs = [];

                        if (_.get(charts, 'summary')) {
                            configs.push(charts.summary);
                        }

                        if (_.get(charts, 'categories')) {
                            configs.push(charts.categories);
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
            });
    }
}
