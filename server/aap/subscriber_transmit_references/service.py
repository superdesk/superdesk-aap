# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.services import BaseService
from eve.utils import config


class SubscriberTransmitReferenceService(BaseService):
    def get_subscriber_reference(self, item_id, subscriber_id):
        return self.find_one(req=None, item_id=item_id, subscriber_id=subscriber_id)

    def insert_update_reference(self, item_id, subscriber_id, extra, reference_id):
        reference = self.find_one(req=None, reference_id=reference_id)
        if not self.find_one(req=None, reference_id=reference_id):
            self.post(
                [
                    {
                        'item_id': item_id,
                        'reference_id': reference_id,
                        'subscriber_id': subscriber_id,
                        'extra': extra
                    }
                ]
            )
        else:
            self.patch(reference.get(config.ID_FIELD), {'extra': extra})
