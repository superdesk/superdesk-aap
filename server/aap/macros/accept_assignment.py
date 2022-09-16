# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
import logging
import re
import superdesk


logger = logging.getLogger(__name__)


def accept_assignment(item, **kwargs):
    """
    Look for evidence that the item is an assignment acceptance and try to extract an assignment id and assignee id
    Mark the assignment as accepted.

    :param item:
    :param kwargs:
    :return:
    """
    regex = r"Assignment ([a-f0-9]{24}) has been accepted by (.*) ([a-f0-9]{24})."

    found = re.search(regex, item.get('body_html'))
    if found and len(found.groups()) == 3:
        assignment = found.group(1)
        assignee = found.group(3)

        assignment_service = superdesk.get_resource_service('assignments')
        assignment_service.accept_assignment(assignment, assignee)

    return item


name = 'accept assignment'
label = 'Accept Assignment'
callback = accept_assignment
access_type = 'backend'
action_type = 'direct'
