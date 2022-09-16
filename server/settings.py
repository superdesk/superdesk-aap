#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


import os
import json
from superdesk.default_settings import strtobool, _MAIL_FROM

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def env(variable, fallback_value=None):
    env_value = os.environ.get(variable, '')
    if len(env_value) == 0:
        return fallback_value
    else:
        if env_value == "__EMPTY__":
            return ''
        else:
            return env_value


ABS_PATH = os.path.abspath(os.path.dirname(__file__))
INIT_DATA_PATH = os.path.join(ABS_PATH, 'data')

LOG_CONFIG_FILE = env('LOG_CONFIG_FILE', 'logging_config.yml')

APPLICATION_NAME = env('APP_NAME', 'Superdesk')
server_url = urlparse(env('SUPERDESK_URL', 'http://localhost:5000/api'))
CLIENT_URL = env('SUPERDESK_CLIENT_URL', 'http://localhost:9000')
URL_PROTOCOL = server_url.scheme or None
SERVER_NAME = server_url.netloc or None
URL_PREFIX = server_url.path.lstrip('/') or ''
if SERVER_NAME.endswith(':80'):
    SERVER_NAME = SERVER_NAME[:-3]

DEFAULT_TIMEZONE = env('DEFAULT_TIMEZONE', 'Australia/Sydney')

# LDAP settings
#: Enable the ability for the display name of the user to be overridden with Superdesk user attributes
LDAP_SET_DISPLAY_NAME = strtobool(env('LDAP_SET_DISPLAY_NAME', 'True'))


INSTALLED_APPS = [
    'superdesk.macros.imperial',
    'aap.publish.transmitters',
    'aap.commands',
    'aap.data_consistency',
    'aap.macros',
    'aap.publish.formatters',
    'aap.publish.transmitters',
    'aap_mm',
    'aap.io.feed_parsers',
    'aap.data_consistency',
    'aap.io.iptc_extension',
    'instrumentation',
    'planning',
    'aap.io.feeding_services',
    'aap.agenda',
    'analytics',
    'aap.reports',
    'aap.fuel',
    'aap.traffic_incidents',
    'aap.subscriber_transmit_references',
    'apps.languages',
]

RENDITIONS = {
    'picture': {
        'thumbnail': {'width': 220, 'height': 120},
        'viewImage': {'width': 640, 'height': 640},
        'baseImage': {'width': 1400, 'height': 1400},
    },
    'avatar': {
        'thumbnail': {'width': 60, 'height': 60},
        'viewImage': {'width': 200, 'height': 200},
    }
}

SERVER_DOMAIN = 'localhost'

MACROS_MODULE = env('MACROS_MODULE', 'aap.macros')

WS_HOST = env('WSHOST', '0.0.0.0')
WS_PORT = env('WSPORT', '5100')

REDIS_URL = env('REDIS_URL', 'redis://localhost:6379')
if env('REDIS_PORT'):
    REDIS_URL = env('REDIS_PORT').replace('tcp:', 'redis:')
BROKER_URL = env('CELERY_BROKER_URL', REDIS_URL)

# Determines if the ODBC publishing mechanism will be used, If enabled then pyodbc must be installed along with it's
# dependencies
ODBC_PUBLISH = env('ODBC_PUBLISH', None)
# ODBC test server connection string
ODBC_TEST_CONNECTION_STRING = env('ODBC_TEST_CONNECTION_STRING',
                                  'DRIVER=FreeTDS;DSN=NEWSDB;UID=???;PWD=???;DATABASE=News')

DEFAULT_SOURCE_VALUE_FOR_MANUAL_ARTICLES = 'AAP'
# Defines default value for Priority to be set for manually created articles
DEFAULT_PRIORITY_VALUE_FOR_MANUAL_ARTICLES = int(env('DEFAULT_PRIORITY_VALUE_FOR_MANUAL_ARTICLES', 6))

# Defines default value for Urgency to be set for manually created articles
DEFAULT_URGENCY_VALUE_FOR_MANUAL_ARTICLES = int(env('DEFAULT_URGENCY_VALUE_FOR_MANUAL_ARTICLES', 0))
DEFAULT_GENRE_VALUE_FOR_MANUAL_ARTICLES = [{'qcode': 'Article', 'name': 'Article'}]
RESET_PRIORITY_VALUE_FOR_UPDATE_ARTICLES = json.loads(env('RESET_PRIORITY_VALUE_FOR_UPDATE_ARTICLES', 'True').lower())

#: Defines default qcodes (comma separated) for category for ingested and auto published articles
DEFAULT_CATEGORY_QCODES_FOR_AUTO_PUBLISHED_ARTICLES = 'a'

# This value gets injected into NewsML 1.2 and G2 output documents.
NEWSML_PROVIDER_ID = 'aap.com.au'
ORGANIZATION_NAME = 'Australian Associated Press'
ORGANIZATION_NAME_ABBREVIATION = 'AAP'
NITF_INCLUDE_SCHEMA = False
# Set to False for production, True will inject the test value for category into the output
TEST_SMS_OUTPUT = env('TEST_SMS_OUTPUT', True)

AMAZON_CONTAINER_NAME = env('AMAZON_CONTAINER_NAME', '')
AMAZON_ACCESS_KEY_ID = env('AMAZON_ACCESS_KEY_ID', '')
AMAZON_SECRET_ACCESS_KEY = env('AMAZON_SECRET_ACCESS_KEY', '')
AMAZON_REGION = env('AMAZON_REGION', 'us-east-1')
AMAZON_SERVE_DIRECT_LINKS = env('AMAZON_SERVE_DIRECT_LINKS', False)
AMAZON_S3_USE_HTTPS = env('AMAZON_S3_USE_HTTPS', False)

is_testing = os.environ.get('SUPERDESK_TESTING', '').lower() == 'true'
ELASTICSEARCH_FORCE_REFRESH = is_testing
ELASTICSEARCH_AUTO_AGGREGATIONS = False

# This setting is used to overide the desk/stage expiry for items to expire from the spike
SPIKE_EXPIRY_MINUTES = int(env('SPIKE_EXPIRY_MINUTES', 3 * 24 * 60))

#: The number of minutes before content items are purged (3 days)
CONTENT_EXPIRY_MINUTES = int(env('CONTENT_EXPIRY_MINUTES', 3 * 24 * 60))

# list of allowed media types from AAP Multimedia System.
AAP_MM_SEARCH_MEDIA_TYPES = ['image']

# The URL endpoint for the images API
AAP_MM_SEARCH_URL = env('AAP_MM_SEARCH_URL', 'https://photos-api.aap.com.au/api/v3')
# Partial URL for the video preview
AAP_MM_CDN_URL = env('AAP_MM_CDN_URL', 'https://photos-cdn.aap.com.au/Preview.mp4')

# copies the metadata from parent for associated item.
COPY_METADATA_FROM_PARENT = env('COPY_METADATA_FROM_PARENT', True)

#: The number of minutes before published content items are purged (3 days)
PUBLISHED_CONTENT_EXPIRY_MINUTES = int(env('PUBLISHED_CONTENT_EXPIRY_MINUTES', 3 * 24 * 60))

# Enable/Disable Content API Publishing
CONTENTAPI_ENABLED = json.loads(env('CONTENTAPI_ENABLED', 'False').lower())

# Make sure legal archive is enabled
LEGAL_ARCHIVE = True

# The Bot User OAuth Token for access to Slack
SLACK_BOT_TOKEN = env('SLACK_BOT_TOKEN', '')

# The URL for the provision of an external feedback or suggestion site
FEEDBACK_URL = env('FEEDBACK_URL', None)

# Currency API Key
CURRENCY_API_KEY = env('CURRENCY_API_KEY', None)

# Validate auto published content using validators not profile
AUTO_PUBLISH_CONTENT_PROFILE = False

# Expire items 3 days after their scheduled date
PLANNING_EXPIRY_MINUTES = int(env('PLANNING_EXPIRY_MINUTES', 4320))

# Delete spiked events/plannings after their scheduled date
PLANNING_DELETE_SPIKED_MINUTES = int(env('PLANNING_DELETE_SPIKED_MINUTES', 1440))

#: The number of minutes before Publish Queue is purged
PUBLISH_QUEUE_EXPIRY_MINUTES = int(env('PUBLISH_QUEUE_EXPIRY_MINUTES', 3 * 24 * 60))

#: The number of minutes since the last update of the Mongo auth object after which it will be deleted
SESSION_EXPIRY_MINUTES = int(env('SESSION_EXPIRY_MINUTES', 740))

#: The number of minutes before ingest items are purged (3 days)
INGEST_EXPIRY_MINUTES = int(env('INGEST_EXPIRY_MINUTES', 3 * 24 * 60))

#: The number of minutes before audit content is purged
AUDIT_EXPIRY_MINUTES = int(env('AUDIT_EXPIRY_MINUTES', 43200))

#: The number records to be fetched for expiry.
MAX_EXPIRY_QUERY_LIMIT = int(env('MAX_EXPIRY_QUERY_LIMIT', 1000))

#: INGEST_ARTICLES_TTL
DAYS_TO_KEEP = int(env('DAYS_TO_KEEP', '3'))

with open(os.path.join(os.path.dirname(__file__), 'picture-profile.json')) as profile_json:
    picture_profile = json.load(profile_json)

with open(os.path.join(os.path.dirname(__file__), 'composite-profile.json')) as profile_json:
    composite_profile = json.load(profile_json)

EDITOR = {
    "picture": picture_profile['editor'],
    "embeds": False,
    "toolbar": False,
    "paste": {
        "forcePlainText": True,
        "cleanPastedHTML": False
    },
    "composite": composite_profile['editor']
}

SCHEMA = {
    "picture": picture_profile['schema'],
    "composite": composite_profile['schema']
}

VALIDATOR_MEDIA_METADATA = {
    "headline": {
        "required": True,
        "maxlength": 42
    },
    "alt_text": {
        "required": True,
        "maxlength": 70
    },
    "description_text": {
        "required": True,
        "maxlength": 100
    },
    "archive_description": {
        "required": False,
    },
    "byline": {
        "required": False,
    },
}

GOOGLE_LOGIN = strtobool(env('GOOGLE_LOGIN', 'false'))


# max multi day event duration in days
MAX_MULTI_DAY_EVENT_DURATION = int(env('MAX_MULTI_DAY_EVENT_DURATION', 7))

# Highcharts Export Server - default settings
ANALYTICS_ENABLE_SCHEDULED_REPORTS = strtobool(
    env('ANALYTICS_ENABLE_SCHEDULED_REPORTS', 'true')
)
ANALYTICS_ENABLE_ARCHIVE_STATS = strtobool(
    env('ANALYTICS_ENABLE_ARCHIVE_STATS', 'true')
)
HIGHCHARTS_SERVER_HOST = env('HIGHCHARTS_SERVER_HOST', 'localhost')
HIGHCHARTS_SERVER_PORT = env('HIGHCHARTS_SERVER_PORT', '6060')
HIGHCHARTS_SERVER_WORKERS = env('HIGHCHARTS_SERVER_WORKERS', None)
HIGHCHARTS_SERVER_WORK_LIMIT = env('HIGHCHARTS_SERVER_WORK_LIMIT', None)
HIGHCHARTS_SERVER_LOG_LEVEL = env('HIGHCHARTS_SERVER_LOG_LEVEL', None)
HIGHCHARTS_SERVER_QUEUE_SIZE = env('HIGHCHARTS_SERVER_QUEUE_SIZE', None)
HIGHCHARTS_SERVER_RATE_LIMIT = env('HIGHCHARTS_SERVER_RATE_LIMIT', None)

MIN_BROADCAST_TEXT_WORD_COUNT = int(env('MIN_BROADCAST_TEXT_WORD_COUNT', 120))

START_OF_WEEK = int(env('START_OF_WEEK', 0))

WATERMARK_IMAGE = env('WATERMARK_IMAGE', 'templates/watermark.png')

PLANNING_AUTO_ASSIGN_TO_WORKFLOW = strtobool(env('PLANNING_AUTO_ASSIGN_TO_WORKFLOW', 'true'))

LONG_EVENT_DURATION_THRESHOLD = int(env('LONG_EVENT_DURATION_THRESHOLD', 4))

PLANNING_CHECK_FOR_ASSIGNMENT_ON_PUBLISH = strtobool(env('PLANNING_CHECK_FOR_ASSIGNMENT_ON_PUBLISH', 'true'))
PLANNING_CHECK_FOR_ASSIGNMENT_ON_SEND = strtobool(env('PLANNING_CHECK_FOR_ASSIGNMENT_ON_SEND', 'true'))

PLANNING_LINK_UPDATES_TO_COVERAGES = strtobool(env('PLANNING_LINK_UPDATES_TO_COVERAGES', 'true'))

PLANNING_FULFIL_ON_PUBLISH_FOR_DESKS = env(
    'PLANNING_FULFIL_ON_PUBLISH_FOR_DESKS',
    '54e68fcd1024542de76d6643,'  # News
    '54e691ca1024542de640fef1,'  # Finance
    '54e6928d1024542de640fef5,'  # Sport
    '5768dd55a5398f5efb985e19,'  # World News
    '5768ddc2a5398f5efa2cda65,'  # News Extra
    '57b0f07ea5398f41862b951e'  # Court Production
)

PLANNING_EVENT_TEMPLATES_ENABLED = strtobool(env('PLANNING_EVENT_TEMPLATES_ENABLED', 'false'))

WORLDVIEW_TARGET_SUBSCRIBERS = env(
    'WORLDVIEW_TARGET_SUBSCRIBERS',
    '5c08aff98e64b91845e0dcdb,'  # System - Newsroom - AAPX Content (Production)
    '5becd97b66f3e17e4e3ae4cc'  # System - Marketplace Test (UAT)
)

PLANNING_ALLOW_SCHEDULED_UPDATES = strtobool(env('PLANNING_ALLOW_SCHEDULED_UPDATES', 'true'))
PLANNING_USE_XMP_FOR_PIC_ASSIGNMENTS = strtobool(env('PLANNING_USE_XMP_FOR_PIC_ASSIGNMENTS', 'true'))
PLANNING_XMP_ASSIGNMENT_MAPPING = {
    'xpath': '//x:xmpmeta/rdf:RDF/rdf:Description',
    'namespaces': {
        'x': 'adobe:ns:meta/',
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'photoshop': 'http://ns.adobe.com/photoshop/1.0/'
    },
    'atribute_key': '{http://ns.adobe.com/photoshop/1.0/}TransmissionReference'
}

PLANNING_USE_XMP_FOR_PIC_SLUGLINE = strtobool(env('PLANNING_USE_XMP_FOR_PIC_SLUGLINE', 'true'))
PLANNING_XMP_SLUGLINE_MAPPING = {
    'xpath': '//x:xmpmeta/rdf:RDF/rdf:Description/dc:title/rdf:Alt/rdf:li',
    'namespaces': {
        'x': 'adobe:ns:meta/',
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'photoshop': 'http://ns.adobe.com/photoshop/1.0/',
        'dc': 'http://purl.org/dc/elements/1.1/',
    }
}

# If true planning a notification will be sent to a user who creates and assignment assigned to themselves
PLANNING_SEND_NOTIFICATION_FOR_SELF_ASSIGNMENT = strtobool(
    env('PLANNING_SEND_NOTIFICATION_FOR_SELF_ASSIGNMENT', 'true'))

# Enable or disable the fulfill assignments task
ENABLE_FULFILL_ASSIGNMENTS = strtobool(env('ENABLE_FULFILL_ASSIGNMENTS', 'true'))

# DC credentials used by fulfill assignments task to determine the user that completed the assignment.
DC_URL = env('DC_URL', '')
DC_USERNAME = env('DC_USERNAME', '')
DC_PASSWORD = env('DC_PASSWORD', '')
DC_SEARCH_FIELD = env('DC_SEARCH_FIELD', 'ORIGINALTRANSMISSIONREFERENCE')
PLANNING_ACCEPT_ASSIGNMENT_EMAIL = env('PLANNING_ACCEPT_ASSIGNMENT_EMAIL', _MAIL_FROM)

try:
    from aap_settings import *  # noqa
except Exception:
    pass
