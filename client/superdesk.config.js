module.exports = function() {
    return {
        defaultRoute: '/workspace',
        validatorMediaMetadata: {
            headline: {
                required: true
            },
            alt_text: {
                required: true
            },
            description_text: {
                required: true
            },
            byline: {
                required: false
            }
        },
        workspace: {
            ingest: 1,
            content: 1,
            tasks: 0
        },

        item_profile: {
            change_profile: 1
        },

        editor: {
            toolbar: false,
            embeds: false,
            paste: {
                forcePlainText: true,
                cleanPastedHTML: false
            }
        },

        features: {
            elasticHighlight: 1,
            swimlane: {columnsLimit: 4},
            editFeaturedImage: 1,
            confirmMediaOnUpdate: 1,
            hideLiveSuggestions: 1,
            preview: 1,
            previewFormats: 1
        },

        view: {
            timeformat: 'HH:mm',
            dateformat: 'DD/MM/YYYY'
        },

        search: {
            slugline: 1, headline: 1, unique_name: 1, story_text: 1,
            byline: 1, keywords: 1, creator: 1, from_desk: 1,
            to_desk: 1, spike: 1, scheduled: 1, company_codes: 1,
            useDefaultTimezone: 1, ingest_provider: 1, raw_search: 1,
            featuremedia: 1
        },
        
        defaultTimezone: 'Australia/Sydney',
        shortDateFormat: 'DD/MM',
        ArchivedDateFormat: 'D/MM/YYYY',

        list: {
            'priority': [
                'urgency',
                'priority'
            ],
            'firstLine': [
                'wordcount',
                'slugline',
                'highlights',
                'associations',
                'queueError',
                'headline',
                'markedDesks',
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
            ],
            'singleLine': [
                'slugline',
                'highlights',
                'takekey',
                'state',
                'update',
                'takepackage',
                'embargo',
                'flags',
                'updated',
                'headline',
                'markedDesks',
                'wordcount',
                'provider',
                'versioncreator',
                'versioncreated'
            ],
            'narrowView': [
                'slugline',
                'takekey',
                'state',
                'markedDesks',
                'provider',
                'versioncreated'
            ],
            'singleLineView': true 
        },
        langOverride: {
            'en': {
                'Advanced Search': 'Advanced',
                'URGENCY': 'NEWS VALUE',
                'Urgency': 'News Value',
                'urgency': 'news value',
                'Urgency stats': 'News Value stats',
                'SERVICE': 'CATEGORY',
                'SERVICES': 'CATEGORIES',
                'Services': 'Categories',
                'Service': 'Category',
                'Mar': 'March',
                'Apr': 'April',
                'Jun': 'June',
                'Jul': 'July',
                'Sep': 'Sept',
                'ANPA Category': 'Category',
                'ANPA CATEGORY': 'CATEGORY'
            },

            'en_GB': {
                'Advanced Search': 'Advanced',
                'URGENCY': 'NEWS VALUE',
                'Urgency': 'News Value',
                'urgency': 'news value',
                'Urgency stats': 'News Value stats',
                'SERVICE': 'CATEGORY',
                'SERVICES': 'CATEGORIES',
                'Services': 'Categories',
                'Service': 'Category',
                'Mar': 'March',
                'Apr': 'April',
                'Jun': 'June',
                'Jul': 'July',
                'Sep': 'Sept',
                'ANPA Category': 'Category',
                'ANPA CATEGORY': 'CATEGORY'
            },

            'en_US': {
                'Advanced Search': 'Advanced',
                'URGENCY': 'NEWS VALUE',
                'Urgency': 'News Value',
                'urgency': 'news value',
                'Urgency stats': 'News Value stats',
                'SERVICE': 'CATEGORY',
                'SERVICES': 'CATEGORIES',
                'Services': 'Categories',
                'Service': 'Category',
                'Mar': 'March',
                'Apr': 'April',
                'Jun': 'June',
                'Jul': 'July',
                'Sep': 'Sept',
                'ANPA Category': 'Category',
                'ANPA CATEGORY': 'CATEGORY'
            },

            'en_AU': {
                'Advanced Search': 'Advanced',
                'URGENCY': 'NEWS VALUE',
                'Urgency': 'News Value',
                'urgency': 'news value',
                'Urgency stats': 'News Value stats',
                'SERVICE': 'CATEGORY',
                'SERVICES': 'CATEGORIES',
                'Services': 'Categories',
                'Service': 'Category',
                'Mar': 'March',
                'Apr': 'April',
                'Jun': 'June',
                'Jul': 'July',
                'Sep': 'Sept',
                'ANPA Category': 'Category',
                'ANPA CATEGORY': 'CATEGORY'
            }
        }
    };
};
