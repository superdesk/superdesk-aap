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
from io import StringIO
from datetime import datetime
from eve.utils import ParsedRequest
from superdesk import get_resource_service
import json
from lxml import html
from superdesk.utils import config
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE


logger = logging.getLogger(__name__)


def am_fronters(item, **kwargs):
    now = datetime.now()
    item['abstract'] = '<p>Main stories in Australia\'s newspapers, published on {}</p>'.format(
        now.strftime('%B %-d, %Y'))
    body = StringIO()
    body.write('<p>(Not for publication, this is a guide only.)<br></p>')

    papers = [{'heading': 'THE AUSTRALIAN', 'name': 'The Australian'},
              {'heading': 'THE FINANCIAL REVIEW', 'name': 'The Financial Review'},
              {'heading': 'SYDNEY MORNING HERALD', 'name': 'The Sydney Morning Herald'},
              {'heading': 'THE DAILY TELEGRAPH', 'name': 'The Daily Telegraph'},
              {'heading': 'THE AGE', 'name': 'The Age'},
              {'heading': 'THE HERALD SUN', 'name': 'The Herald Sun'},
              {'heading': 'THE COURIER-MAIL', 'name': 'The Courier-Mail'},
              {'heading': 'THE ADVERTISER', 'name': 'The Advertiser'},
              {'heading': 'THE MERCURY', 'name': 'The Mercury'},
              {'heading': 'WEST AUSTRALIAN', 'name': 'The West Australian'},
              {'heading': 'CANBERRA TIMES', 'name': 'The Canberra Times'},
              {'heading': 'NT NEWS', 'name': 'The NT News'}]
    for paper in papers:
        try:
            service = get_resource_service('published')
            req = ParsedRequest()
            query = {
                "query": {
                    "filtered": {
                        "query": {
                            "query_string": {
                                "query": "headline:(\"Main+stories+in+{}\")".format(paper.get('name').replace(' ', '+'))
                            }
                        },
                        "filter": {
                            "and": [
                                {
                                    "term": {
                                        "anpa_category.qcode": "v"
                                    }
                                }
                            ]
                        }
                    }
                }
            }
            req.sort = '[("_created", -1)]'
            req.args = {'source': json.dumps(query)}
            req.max_results = 1
            articles = service.get(req=req, lookup=None)
            if articles.count():
                article = articles[0]
                # Check that the article is for today, check day month
                if now.strftime('%B') in article.get('abstract') and now.strftime('%-d') in article.get(
                        'abstract'):
                    body.write('<p>{}</p>'.format(paper.get('heading')))
                    tree = html.fromstring(article.get('body_html'))
                    pars = tree.xpath('./p')
                    for par in pars:
                        if par.text and par.text.startswith('PAGE 1:'):
                            if len(par.text) > len('PAGE 1:') + 20:
                                body.write('<p>{}</p>'.format(par.text))
                            elif par.getnext() is not None:
                                body.write('<p>PAGE 1: {}</p>'.format(par.getnext().text))
                            else:
                                body.write('<p>PAGE 1: {}</p>'.format(par.text.replace('PAGE 1: ', '')))
                            continue
                        if par.text and par.text.startswith('SPORT:'):
                            if len(par.text) > len('SPORT:') + 20:
                                body.write('<p>SPORT: {}</p>'.format(par.text.replace('SPORT: ', '')))
                            elif par.getnext() is not None:
                                body.write('<p>SPORT: {}</p>'.format(par.getnext().text))
                            else:
                                body.write('<p>SPORT: {}</p>'.format(par.text.replace('SPORT: ', '')))
                            continue
                else:
                    print('Todays fronter story for {} was not found'.format(paper))
                    logger.warning('Todays fronter story for {} was not found'.format(paper))
            else:
                print('Fronter story for {} was not found'.format(paper))
                logger.warning('Fronter story for {} was not found'.format(paper))
        except Exception as e:
            logger.warning('Fronter story for {} raised exception: {}'.format(paper, e))
            pass

    item['body_html'] = body.getvalue()
    body.close()

    # If the macro is being executed by a scheduled template then publish the item as well
    if 'desk' in kwargs and 'stage' in kwargs:
        update = {'body_html': item.get('body_html', '')}
        get_resource_service('archive').system_update(item[config.ID_FIELD], update, item)

        get_resource_service('archive_publish').patch(id=item[config.ID_FIELD],
                                                      updates={ITEM_STATE: CONTENT_STATE.PUBLISHED,
                                                      'auto_publish': True})
        return get_resource_service('archive').find_one(req=None, _id=item[config.ID_FIELD])

    return item


name = 'AM Fronters'
label = 'AM Fronters'
callback = am_fronters
access_type = 'frontend'
action_type = 'direct'
group = 'AM Desk'
