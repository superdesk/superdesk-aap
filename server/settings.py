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

INSTALLED_APPS = [
    'apps.auth',
    'superdesk.roles',
]

# LDAP settings
LDAP_SERVER = env('LDAP_SERVER', '')  # Ex: ldap://sourcefabric.org
LDAP_SERVER_PORT = env('LDAP_SERVER_PORT', 389)

# Fully Qualified Domain Name. Ex: sourcefabric.org
LDAP_FQDN = env('LDAP_FQDN', '')

# LDAP_BASE_FILTER limit the base filter to the security group. Ex: OU=Superdesk Users,dc=sourcefabric,dc=org
LDAP_BASE_FILTER = env('LDAP_BASE_FILTER', '')

# change the user depending on the LDAP directory structure
LDAP_USER_FILTER = env('LDAP_USER_FILTER', "(&(objectCategory=user)(objectClass=user)(sAMAccountName={}))")

# LDAP User Attributes to fetch. Keys would be LDAP Attribute Name and Value would be Supderdesk Model Attribute Name
LDAP_USER_ATTRIBUTES = json.loads(env('LDAP_USER_ATTRIBUTES',
                                      '{"givenName": "first_name", "sn": "last_name", '
                                      '"displayName": "display_name", "mail": "email"}'))

if LDAP_SERVER:
    INSTALLED_APPS.append('apps.ldap')
else:
    INSTALLED_APPS.append('superdesk.users')
    INSTALLED_APPS.append('apps.auth.db')


INSTALLED_APPS.extend([
    'superdesk.upload',
    'superdesk.download',
    'superdesk.sequences',
    'superdesk.notification',
    'superdesk.data_updates',
    'superdesk.activity',
    'superdesk.vocabularies',
    'superdesk.backend_meta',
    'apps.comments',

    'superdesk.io',
    'superdesk.io.feeding_services',
    'superdesk.io.feed_parsers',
    'superdesk.io.subjectcodes',
    'superdesk.io.iptc',
    'apps.io',
    'apps.io.feeding_services',
    'superdesk.publish',
    'superdesk.commands',
    'superdesk.locators',

    'apps.auth',
    'apps.archive',
    'apps.stages',
    'apps.desks',
    'apps.tasks',
    'apps.preferences',
    'apps.spikes',
    'apps.prepopulate',
    'apps.legal_archive',
    'apps.search',
    'apps.saved_searches',
    'apps.privilege',
    'apps.rules',
    'apps.highlights',
    'apps.products',
    'apps.publish',
    'apps.publish.enqueue',
    'apps.publish.formatters',
    'apps.content_filters',
    'apps.content_types',
    'apps.dictionaries',
    'apps.duplication',
    'apps.spellcheck',
    'apps.templates',
    'apps.archived',
    'apps.validators',
    'apps.validate',
    'apps.workspace',
    'apps.macros',
    'apps.export',
    'apps.archive_broadcast',
    'apps.search_providers',
    'apps.feature_preview',
    'apps.workqueue',

    'aap.commands',
    'aap.data_consistency',
    'aap.macros',
    'aap.publish.formatters',
    'aap_mm',
    'aap.io.feed_parsers',
    'aap.data_consistency',
    'aap.io.iptc_extension',
    'instrumentation',
    'planning'
])

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
DEFAULT_URGENCY_VALUE_FOR_MANUAL_ARTICLES = int(env('DEFAULT_URGENCY_VALUE_FOR_MANUAL_ARTICLES', 3))
DEFAULT_GENRE_VALUE_FOR_MANUAL_ARTICLES = [{'qcode': 'Article', 'name': 'Article (news)'}]
RESET_PRIORITY_VALUE_FOR_UPDATE_ARTICLES = json.loads(env('RESET_PRIORITY_VALUE_FOR_UPDATE_ARTICLES', 'True').lower())

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

# copies the metadata from parent for associated item.
COPY_METADATA_FROM_PARENT = env('COPY_METADATA_FROM_PARENT', True)

#: The number of minutes before published content items are purged (3 days)
PUBLISHED_CONTENT_EXPIRY_MINUTES = int(env('PUBLISHED_CONTENT_EXPIRY_MINUTES', 3 * 24 * 60))

# Enable/Disable Content API Publishing
CONTENTAPI_ENABLED = json.loads(env('CONTENTAPI_ENABLED', 'False').lower())

# Enable/Disable Takes Publishing
NO_TAKES = json.loads(env('NO_TAKES', 'False').lower())

# Make sure legal archive is enabled
LEGAL_ARCHIVE = True
