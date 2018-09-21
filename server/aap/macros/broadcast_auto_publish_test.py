# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from mock import patch
from copy import deepcopy
from unittests import AAPTestCase
from .broadcast_auto_publish import broadcast_auto_publish


class BroadcastAutoPublishTestCase(AAPTestCase):

    article = {
        'guid': 'aapimage-1', '_id': '1', 'type': 'text',
        'keywords': ['Student', 'Crime', 'Police', 'Missing'],
        'body_html': '',
        'format': 'HTML',
        'state': 'published',
        'flags': {
            'marked_for_legal': False
        },
        'genre': [{'qcode': 'foo', 'name': 'bar'}]
    }

    def get_item(self):
        item = deepcopy(self.article)
        body_lines = []
        for count in range(1, 125):
            body_lines.append('<p>line-#{}#</p>'.format(count))
        item['body_html'] = ''.join(body_lines)
        return item

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_copy_state_published(self, internal_dest):
        item = self.get_item()
        broadcast_auto_publish(item)
        self.assertNotIn('line-#121#', item['body_html'])
        self.assertEqual([{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}], item['genre'])
        internal_dest.assert_called_with(item)

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_copy_state_corrected(self, internal_dest):
        item = self.get_item()
        item['state'] = 'corrected'

        broadcast_auto_publish(item)
        self.assertNotIn('line-#121#', item['body_html'])
        self.assertEqual([{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}], item['genre'])
        internal_dest.assert_called_with(item)

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_copy_state_killed(self, internal_dest):
        item = self.get_item()
        item['state'] = 'killed'

        broadcast_auto_publish(item)
        self.assertIn('line-#124#', item['body_html'])
        self.assertEqual([{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}], item['genre'])
        internal_dest.assert_called_with(item)

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_copy_state_recalled(self, internal_dest):
        item = self.get_item()
        item['state'] = 'killed'

        broadcast_auto_publish(item)
        self.assertIn('line-#124#', item['body_html'])
        self.assertEqual([{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}], item['genre'])
        internal_dest.assert_called_with(item)

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_copy_legal(self, internal_dest):
        item = self.get_item()
        item['flags']['marked_for_legal'] = True
        broadcast_auto_publish(item)
        self.assertIn('line-#124#', item['body_html'])
        self.assertEqual([{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}], item['genre'])
        internal_dest.assert_called_with(item)

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_copy_not_text_item(self, internal_dest):
        item = self.get_item()
        item['type'] = 'picture'
        broadcast_auto_publish(item)
        self.assertIn('line-#124#', item['body_html'])
        self.assertEqual([{'qcode': 'foo', 'name': 'bar'}], item['genre'])
        self.assertFalse(internal_dest.called)

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_if_body_html_is_long(self, internal_dest):
        item = self.get_item()
        item['type'] = 'text'
        item['body_html'] = "<p>NSW education ministers past and present have savaged Prime Minister " \
                            "Scott Morrison's private schools funding deal, while the state's teachers " \
                            "union says it's \"corrupt\".</p><p>Education Minister Rob Stokes argues " \
                            "the federal government's $4.6 billion proposal would spell a return to the" \
                            " bad old days of the funding wars.</p><p>\"Quite simply, I won't be signing " \
                            "any deal that doesn't treat every student and every school with fairness,\" the " \
                            "Liberal minister said in a statement.</p><p>\"The Gonski principles provide" \
                            " that school funding should be needs based and sector blind and these are the" \
                            " principles we hold dear.</p><p>\"We don't want a return to the school funding" \
                            " wars of the past that pitted private schools against public schools and urge" \
                            " the federal government to provide equal treatment for all schools, public" \
                            " and private.\"</p><p>Former NSW education minister Adrian Piccoli, is also" \
                            " scathing in his criticism.</p><p>\"This is pathetic. There is nothing fair" \
                            " about it. There is nothing Christian about it. It’s throwing money at the" \
                            " powerful and well connected,\" the ex-Nationals MP tweeted.<br></p><p>Mr Piccoli" \
                            " subsequently tweeted Mr Morrison's press release on the deal and " \
                            "stated: \"So, tell us more about the $1.2b slush fund you are setting up " \
                            "only for Catholic and independent schools.\"</p><p>The federal government" \
                            " plans to&nbsp;give Catholic and independent schools an additional $3.4 " \
                            "billion over 11 years to fund changes to the way parents' wealth is " \
                            "measured based on income tax data.</p><p>A further $1.2 billion will " \
                            "be spent on Catholic and independent schools as the coalition sees" \
                            " fit.</p><p>NSW Teachers Federation president Maurie Mulheron is " \
                            "outraged.</p><p>\"This is probably the most corrupt funding deal we've ever" \
                            " seen an Australian government deliver,\" he told AAP.</p><p>\"It's nothing" \
                            " more than an election slush fund. It's not based on need and public schools " \
                            "right across Australia don't get one single dollar out of it.\"</p><p>Mr Mulheron" \
                            " said the states and territories may now refuse to sign funding " \
                            "deals.<br></p><p>\"We'll fight this right up to the next election. If Mr Morrison" \
                            " thinks there's anything settled he's got another thing coming.\"</p><p>The prime " \
                            "minister on Friday brushed off Mr Stokes' attack.&nbsp;<br></p><p>\"I don't think " \
                            "Rob's yet had the chance to really look at the full details of this,\" Mr Morrison " \
                            "told ABC radio.<br></p><p>\"I'm sure once he sees that he'll see those comments" \
                            " don't weigh up with what we've actually announced.\"</p>"
        broadcast_auto_publish(item)
        self.assertIn(item["body_html"],
                      ''.join(
                          [
                              "<p>NSW education ministers past and present have savaged Prime Minister ",
                              "Scott Morrison's private schools funding deal, while the state's teachers ",
                              "union says it's \"corrupt\".</p><p>Education Minister Rob Stokes argues ",
                              "the federal government's $4.6 billion proposal would spell a return to the",
                              " bad old days of the funding wars.</p><p>\"Quite simply, I won't be signing ",
                              "any deal that doesn't treat every student and every school with fairness,\" the ",
                              "Liberal minister said in a statement.</p><p>\"The Gonski principles provide",
                              " that school funding should be needs based and sector blind and these are the",
                              " principles we hold dear.</p><p>\"We don't want a return to the school funding",
                              " wars of the past that pitted private schools against public schools and urge",
                              " the federal government to provide equal treatment for all schools, public",
                              " and private.\"</p>"
                          ])
                      )
        self.assertEqual([{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}], item['genre'])
        internal_dest.assert_called_with(item)

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_if_body_html_is_short(self, internal_dest):
        item = self.get_item()
        item['type'] = 'text'
        item['body_html'] = "<p> </p><p>The first case of a contaminated strawberry has been found in the " \
                            "Northern Territory.</p><p>Police and health officials are yet to say " \
                            "if the strawberry contained a needle in it, as has been occurring across " \
                            "the country.</p><p>Police are holding a media conference in " \
                            "Darwin at 1pm (CST).</p><p>The original contamination was reported in " \
                            "Queensland, prompting dozens of suspected copycat incidents " \
                            "involving strawberries and other fruits.</p>"
        original = deepcopy(item)
        broadcast_auto_publish(item)
        self.assertIn(item["body_html"], original["body_html"])
        self.assertEqual([{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}], item['genre'])
        internal_dest.assert_called_with(item)
