# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import aap.io.iptc_extension  # noqa
import aap.io.media_topics_extension  # noqa
from .feeding_services.aap_sports_service import AAPSportsHTTPFeedingService  # noqa
from .feeding_services.intelematics_fuel_service import IntelematicsFuelHTTPFeedingService  # noqa
from .feeding_services.intelematics_incidents_service import IntelematicsIncidentHTTPFeedingService  # noqa
from .feeding_services.ap_media_relay import APMediaRelayFeedingService  # noqa
from .feeding_services.petrol_spy_fuel_service import PetrolSpyFuelHTTPFeedingService  # noqa