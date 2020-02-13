# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2016 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.metadata.item import FORMATS, FORMAT, CONTENT_STATE, ITEM_STATE, ITEM_TYPE, CONTENT_TYPE
import logging
from superdesk.etree import parse_html
from superdesk.utc import utcnow, get_date
from copy import deepcopy
from datetime import datetime
from aap.utils import set_dateline
import re
from titlecase import titlecase
from superdesk import get_resource_service
from collections import OrderedDict

logger = logging.getLogger(__name__)


def process_victorian_harness_racing(item, **kwargs):

    number_words_map = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
                        6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
                        11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen',
                        15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen',
                        19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty',
                        50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty',
                        90: 'Ninety', 0: 'Zero'}

    substitution_map = OrderedDict({"second": "2nd", "third": "3rd", "fourth": "4th", "fifth": "5th", "sixth": "6th",
                                    "seventh": "7th", "eighth": "8th", "ninth": "9th", "2nd row": "second row",
                                    "2nd up": "second up", "2nd line": "second line", "2nd run": "second run",
                                    "2nd pick": "second pick", "January": "Jan", "February": "Feb", "August": "Aug",
                                    "September": "Sept", "October": "Oct", "November": "Nov", "December": "Dec",
                                    "Harold Park": "HP", "Moonee Valley": "MV"})

    def race_number_to_words(race):
        n = int(race.replace('Race', '').replace(':', ''))
        try:
            return titlecase(number_words_map[n])
        except KeyError:
            try:
                return titlecase(number_words_map[n - n % 10] + number_words_map[n % 10].lower())
            except KeyError:
                return str(n)

    content = item.get('body_html', '')
    comment_item = {
        "anpa_category": [
            {
                "qcode": "r",
                "name": "Racing (Turf)",
                "subject": "15030001"
            }
        ],
        "subject": [
            {
                "parent": "15000000",
                "name": "horse racing, harness racing",
                "qcode": "15030000"
            }
        ],
        "place": [
            {
                "state": "Victoria",
                "name": "VIC",
                "group": "Australia",
                "country": "Australia",
                "qcode": "VIC",
                "world_region": "Oceania"
            }
        ],
        FORMAT: FORMATS.HTML,
        ITEM_TYPE: CONTENT_TYPE.TEXT
    }
    selections_item = deepcopy(comment_item)
    # copy the genre of the item that we are oprerting on
    if 'genre' in item:
        selections_item['genre'] = deepcopy(item['genre'])

    parsed = parse_html(content, content='html')

    for tag in parsed.xpath('/html/div/child::*'):
        if tag.tag == 'p':
            if tag.text.startswith('VENUE: '):
                venue = tag.text.replace('VENUE: ', '')
            elif tag.text.startswith('DATE: '):
                try:
                    meeting_date = datetime.strptime(tag.text.replace('DATE: ', '').replace(' ', ''), '%d/%m/%y')
                except Exception:
                    logger.warning('Date format exception for {}'.format(tag.text.replace('DATE: ', '')))
                    try:
                        meeting_date = datetime.strptime(tag.text.replace('DATE: ', '').replace(' ', ''), '%d/%m/%Y')
                    except Exception:
                        logger.warning('Date format exception 2 for {}'.format(tag.text.replace('DATE: ', '')))
                        try:
                            meeting_date = get_date(tag.text.replace('DATE: ', '').replace(' ', ''))
                        except Exception:
                            logger.warning('Date format exception 3 for {}'.format(tag.text.replace('DATE: ', '')))
                            meeting_date = utcnow()

                comment_item['slugline'] = venue + ' Comment'
                comment_item['anpa_take_key'] = meeting_date.strftime('%A')
                comment_item['headline'] = venue + ' Trot Comment ' + meeting_date.strftime('%A')
                comment_item['firstcreated'] = utcnow()
                set_dateline(comment_item, 'Melbourne', 'AAP')

                selections_item['slugline'] = venue + ' Selections'
                selections_item['anpa_take_key'] = meeting_date.strftime('%A')
                selections_item['headline'] = venue + ' Trot Selections ' + meeting_date.strftime('%A')
                selections_item['firstcreated'] = utcnow()
                set_dateline(selections_item, 'Melbourne', 'AAP')
                selections_item['body_html'] = '<p>{} Selections for {}\'s {} trots.-</p>'.format(
                    selections_item.get('dateline').get('text'),
                    meeting_date.strftime('%A'), venue)
                selections_item['firstcreated'] = utcnow()
                break

    regex = r"Race ([1-9][0-9]|[1-9]):"
    for tag in parsed.xpath('/html/div/child::*'):
        if tag.tag == 'p':
            m = re.match(regex, tag.text)
            if m:
                selections_item['body_html'] += '<p>{} '.format(tag.text)
            if tag.text.startswith('SELECTIONS: '):
                sels = titlecase(tag.text.replace('SELECTIONS: ', ''))
                # In some cases there is no comma between the selections, apparently there should be!
                sels = sels.replace(') ', '), ')
                sels = re.sub(r'\s\(.*?\)', '', sels)
                # get rid of the trailing one
                sels = re.sub(r'(, $|,$)', ' ', sels)
                selections_item['body_html'] += '{}</p>'.format(sels)
    selections_item['body_html'] += '<p>AAP SELECTIONS</p>'

    comment_item['body_html'] = ''
    overview = ''
    regex = r"Race ([1-9][0-9]|[1-9]):"
    for tag in parsed.xpath('/html/div/child::*'):
        if tag.tag == 'p':
            m = re.match(regex, tag.text)
            if m:
                comment_item['body_html'] += '<p>Race {}:</p>'.format(race_number_to_words(tag.text))
            if tag.text.startswith('EARLY SPEED: '):
                comment_item['body_html'] += '<p>{}</p>'.format(overview.rstrip())
                overview = ''
                comment_item['body_html'] += '<p>{}</p>'.format(tag.text.rstrip())
            if tag.text.startswith('OVERVIEW: '):
                overview = tag.text
            elif overview:
                overview += tag.text

    for i, j in substitution_map.items():
        comment_item['body_html'] = comment_item['body_html'].replace(i, j)
    comment_item['body_html'] += '<p>AAP COMMENT</p>'

    service = get_resource_service('archive')
    selections_item['task'] = item.get('task')
    selections_item['profile'] = item.get('profile')
    selections_item[ITEM_STATE] = CONTENT_STATE.PROGRESS
    service.post([selections_item])

    item.update(comment_item)

    return item


name = 'process victorian harness racing'
label = 'Process Harness Racing Doc'
callback = process_victorian_harness_racing
access_type = 'frontend'
action_type = 'direct'
group = 'Copytakers'
