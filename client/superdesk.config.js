module.exports = function() {
    return {
        defaultRoute: '/workspace',

        workspace: {
            ingest: 1,
            content: 1,
            tasks: 0
        },

        editor: {
            toolbar: false,
            embeds: false,
            paste: {
                forcePlainText: true,
                cleanPastedHTML: false
            }
        },

        view: {
            timeformat: 'HH:mm',
            dateformat: 'DD/MM/YYYY'
        },

        previewFormats: [{
            name: 'AAPIpNewsFormatter',
            outputType: 'json',
            outputField: 'article_text'
        }],

        defaultTimezone: 'Australia/Sydney',
        shortDateFormat: 'DD/MM',
        ArchivedDateFormat: 'D/MM/YYYY',

        list: {
            'priority': [
                'priority',
                'urgency'
            ],
            'firstLine': [
                'wordcount',
                'slugline',
                'highlights',
                'headline',
                'versioncreated'
            ],
            'secondLine': [
                'profile',
                'state',
                'embargo',
                'takekey',
                'takepackage',
                'signal',
                'broadcast',
                'flags',
                'updated',
                'category',
                'provider',
                'expiry',
                'desk'
            ]
        },

        langOverride: {
            'en': {
                "URGENCY": "NEWS VALUE",
                "Urgency": "News Value",
                "urgency": "news value",
                "Urgency stats": "News Value stats",
                "SERVICE": "CATEGORY",
                "SERVICES": "CATEGORIES",
                "Services": "Categories",
                "Service": "Category",
                "Mar": "March",
                "Apr": "April",
                "Jun": "June",
                "Jul": "July",
                "Sep": "Sept"        
            },

            'en_GB': {
                "URGENCY": "NEWS VALUE",
                "Urgency": "News Value",
                "urgency": "news value",
                "Urgency stats": "News Value stats",
                "SERVICE": "CATEGORY",
                "SERVICES": "CATEGORIES",
                "Services": "Categories",
                "Service": "Category",
                "Mar": "March",
                "Apr": "April",
                "Jun": "June",
                "Jul": "July",
                "Sep": "Sept"
            },

            'en_US': {
                "URGENCY": "NEWS VALUE",
                "Urgency": "News Value",
                "urgency": "news value",
                "Urgency stats": "News Value stats",
                "SERVICE": "CATEGORY",
                "SERVICES": "CATEGORIES",
                "Services": "Categories",
                "Service": "Category",
                "Mar": "March",
                "Apr": "April",
                "Jun": "June",
                "Jul": "July",
                "Sep": "Sept"
            },

            'en_AU': {
                "URGENCY": "NEWS VALUE",
                "Urgency": "News Value",
                "urgency": "news value",
                "Urgency stats": "News Value stats",
                "SERVICE": "CATEGORY",
                "SERVICES": "CATEGORIES",
                "Services": "Categories",
                "Service": "Category",
                "Mar": "March",
                "Apr": "April",
                "Jun": "June",
                "Jul": "July",
                "Sep": "Sept"
            }
        }
    };
};
