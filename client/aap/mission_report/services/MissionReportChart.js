MissionReportChart.$inject = ['lodash', 'gettext', 'moment'];

/**
 * @ngdoc service
 * @module superdesk.aap.mission_report
 * @name MissionReportChart
 * @requires lodash
 * @requires gettext
 * @requires moment
 * @description Service to create Highcharts configs based on Mission Report data from the API
 */
export function MissionReportChart(_, gettext, moment) {
    /**
     * @ngdoc method
     * @name MissionReportChart#genSummaryChart
     * @param {Object} data - The data used to generate the summary chart
     * @return {Object} - The Highcharts config
     * @description Generate the line chart to displaying the overall summary of the report
     */
    this.genSummaryChart = (data) => {
        const categories = [
            gettext('Total Stories'),
            gettext('Results/Fields/Comment/Betting'),
            gettext('New Stories'),
            gettext('Updates'),
            gettext('Corrections'),
            gettext('Kills'),
            gettext('Takedowns'),
        ];
        const totalStories = _.get(data, 'total_stories') || 0;
        const subtitle = moment(
            _.get(data, 'first_item.versioncreated') ||
            _.get(data, 'first_item._updated')
        ).format('dddd Do MMMM YYYY');

        const source = [
            totalStories,
            _.get(data, 'new_stories.categories.results') || 0,
            _.get(data, 'new_stories.count') || 0,
            _.get(data, 'rewrites.length') || 0,
            _.get(data, 'corrections.length') || 0,
            _.get(data, 'kills.length') || 0,
            _.get(data, 'takedowns.length') || 0,
        ];

        return {
            id: 'mission_report_summary',
            type: 'line',
            chart: {
                type: 'line',
                height: 300,
            },
            title: {text: `Mission Report: Summary (${totalStories} total stories)`},
            subtitle: {text: subtitle},
            xAxis: {categories: categories},
            yAxis: {
                title: {text: 'STORIES TRANSMITTED'},
                labels: {enabled: false},
            },
            legend: {enabled: false},
            tooltip: {enabled: false},
            plotOptions: {
                series: {
                    dataLabels: {enabled: true},
                },
            },
            series: [{
                data: source
            }],
            fullHeight: false,
        }
    };

    /**
     * @ngdoc method
     * @name MissionReportChart#genCategoryChart
     * @param {Object} data - The data used to generate the category chart
     * @param {Object} metadata - The metadata used to get category names from qcodes
     * @return {Object} - The Highcharts config
     * @description Generate the bar chart to displaying the category report
     */
    this.genCategoryChart = (data, metadata) => {
        const categories = _.keyBy(_.get(metadata, 'categories') || {}, 'qcode');
        categories['results'] = {
            qcode: 'results',
            name: 'Results/Fields/Comment/Betting'
        };

        const series = _.get(data, 'new_stories.categories') || {};
        const xAxisTitles = [];
        const seriesData = [];

        Object.keys(series)
            .sort()
            .forEach((qcode) => {
                seriesData.push(_.get(series, qcode) || 0);

                const category = _.get(categories, qcode) || {};
                let title = category.name;

                if (qcode !== 'results') {
                    title += ` ${qcode.toUpperCase()}`;
                }

                xAxisTitles.push(title);
            });

        return {
            id: 'mission_report_categories',
            type: 'bar',
            chart: {
                type: 'bar',
                zoomType: 'y',
            },
            title: {text: gettext('New Stories By Category')},
            xAxis: {
                title: {text: 'CATEGORY'},
                categories: xAxisTitles,
            },
            yAxis: {
                title: {text: gettext('STORIES TRANSMITTED')},
                labels: {enabled: false},
            },
            legend: {enabled: false},
            tooltip: {enabled: false},
            plotOptions: {
                series: {
                    dataLabels: {enabled: true},
                },
            },
            series: [{
                data: seriesData
            }],
            fullHeight: true,
        };
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
                _.get(kill, 'anpa_take_key') || '',
                _.get(kill, 'ednote') || '',
            ]));

        return {
            id: 'mission_report_kills',
            type: 'table',
            chart: {type: 'column'},
            headers: ['Sent', 'Slugline', 'TakeKey', 'Ednote'],
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
                _.get(takedown, 'anpa_take_key') || '',
                _.get(takedown, 'ednote') || '',
            ]));

        return {
            id: 'mission_report_takedowns',
            type: 'table',
            chart: {type: 'column'},
            headers: ['Sent', 'Slugline', 'TakeKey', 'Ednote'],
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
     * @name MissionReportChart#createChart
     * @param {Object} data - The data used to generate the updates table chart
     * @param {Object} metadata - The metadata used to get category names from qcodes
     * @return {Object} - The report chart configs
     * @description Generate the chart configs for the entire report
     */
    this.createChart = function(data, metadata) {
        if ((_.get(data, 'total_stories') || 0) < 1) {
            return {
                charts: [{
                    id: 'mission_report_empty',
                    type: 'table',
                    title: gettext('There were no stories published'),
                    rows: [],
                }],
            };
        }

        return {
            charts: [
                this.genSummaryChart(data),
                this.genCategoryChart(data, metadata),
                this.genCorrectionsChart(data),
                this.genKillsChart(data),
                this.genTakedownsChart(data),
                this.genUpdatesChart(data),
            ],
            multiChart: false,
            marginBottom: true,
        };
    }
}
