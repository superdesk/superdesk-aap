# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2018 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE, ITEM_TYPE, CONTENT_TYPE, FORMAT, FORMATS
from superdesk.macros.internal_destination_auto_publish import internal_destination_auto_publish
from superdesk.text_utils import get_text_word_count
from aap.publish.formatters.aap_bulletinbuilder_formatter import AAPBulletinBuilderFormatter
from superdesk import config


def broadcast_auto_publish(item, **kwargs):
    """Broadcast auto publish macro.

    :param item:
    :param kwargs:
    :return:
    """
    if item.get(ITEM_TYPE) != CONTENT_TYPE.TEXT or item.get(FORMAT) != FORMATS.HTML:
        return

    formatter = AAPBulletinBuilderFormatter()
    body_text = formatter.get_text_content(formatter.append_body_footer(item))
    word_count = get_text_word_count(body_text)
    max_word_count = config.MIN_BROADCAST_TEXT_WORD_COUNT
    item['genre'] = [{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}]
    if item[ITEM_STATE] not in {CONTENT_STATE.KILLED, CONTENT_STATE.RECALLED} and \
            not (item.get('flags') or {}).get('marked_for_legal'):
        if word_count > max_word_count and \
                not (item.get('flags') or {}).get('marked_for_legal'):
            lines = body_text.splitlines()
            new_body_html = []
            for line in lines:
                para = line.strip()
                if not para:
                    continue

                new_body_html.append('<p>{}</p>'.format(para))
                word_count = get_text_word_count(''.join(new_body_html))
                if word_count > max_word_count:
                    if len(new_body_html):
                        item['body_html'] = ''.join(new_body_html)
                        item['word_count'] = word_count
                    break
    elif item[ITEM_STATE] in {CONTENT_STATE.KILLED, CONTENT_STATE.RECALLED}:
        lines = body_text.splitlines()
        lines = ['<p>{}</p>'.format(line.strip()) for line in lines if line.strip()]
        # remove the first line/paragraph of kill message
        lines = lines[1:]
        item['body_html'] = ''.join(lines)
        fields_to_remove = ['embargo', 'dateline', 'slugline', 'genre']
        for field in fields_to_remove:
            item.pop(field, None)

    internal_destination_auto_publish(item, **kwargs)


name = 'broadcast_auto_publish'
label = 'Broadcast Auto Publish'
callback = broadcast_auto_publish
access_type = 'backend'
action_type = 'direct'
