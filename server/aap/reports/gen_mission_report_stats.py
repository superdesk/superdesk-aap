# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
#  Copyright 2013-2019 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from analytics.stats.common import OPERATION
from analytics.stats.gen_archive_statistics import connect_stats_signals

from aap.common import extract_kill_reason_from_html


def on_generate_stats(sender, entry, update):
    if entry.get('operation') not in [OPERATION.KILL, OPERATION.TAKEDOWN]:
        return

    update.update({
        'mission': {
            'body_html': (entry.get('update') or {}).get('body_html') or ''
        }
    })


def on_process_stats(sender, entry, new_timeline, updates, update, stats):
    if entry.get('operation') not in [OPERATION.KILL, OPERATION.TAKEDOWN]:
        return

    if not updates.get('extra'):
        updates['extra'] = {}

    updates['extra']['mission'] = {
        'reasons': extract_kill_reason_from_html(
            update.get('body_html') or '',
            is_kill=entry.get('operation') == OPERATION.KILL
        )
    }


connect_stats_signals(
    on_generate=on_generate_stats,
    on_process=on_process_stats,
)
