# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


import superdesk


def get_aap_category_list(category_list):
    """
    Content with the a New Zealand category is replaced with the International category.
    :param category_list:
    :return: category list with N replaced with I
    """
    all_categories = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='categories')
    list = []
    for c in category_list:
        if c.get('qcode').upper() == 'N' and not any(e.get('qcode', None) == 'I' for e in list):
            list.append(next((x for x in all_categories['items'] if x.get('qcode').upper() == 'I'), None))
        else:
            if not any(e.get('qcode', None) == c.get('qcode').upper() for e in list):
                list.append(
                    next((x for x in all_categories['items'] if x.get('qcode').upper() == c.get('qcode').upper()),
                         None))
    return list


def get_nzn_category_list(category_list):
    """
    Get a mapped category list mapped as follows, Categories S,T,F and I are preserved all other
    categories are changed to N
    :param category_list:
    :return category_list:
    """
    all_categories = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='categories')
    list = []
    for c in category_list:
        keep_set = {'S', 'T', 'F', 'I'}
        for k in keep_set:
            if c.get('qcode').upper() == k and not any(e.get('qcode', None) == k for e in list):
                list.append(next((x for x in all_categories['items'] if x.get('qcode').upper() == k), None))

        if c.get('qcode').upper() not in keep_set \
                and not any(e.get('qcode', None) == 'N' for e in list):
            list.append(next((x for x in all_categories['items'] if x.get('qcode').upper() == 'N'), None))
    return list
