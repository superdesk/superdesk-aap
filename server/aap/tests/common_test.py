# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2018 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.tests import TestCase

from aap.common import extract_kill_reason_from_html


class CommonTestCase(TestCase):
    def test_extract_kill_reason_from_html(self):
        # Test kill with unmodified template
        html = '<p>Please kill story slugged kill test headlined kill test ex  at 02 Nov 2018 ' \
               '11:15 AEDT.</p><p>Pursuant to your Information Supply Agreement with Australian ' \
               'Associated Press (AAP)  , AAP requests that you remove the above story from any ' \
               'media you publish and access to the story be immediately disabled including but ' \
               'not limited to those websites in either your direct or indirect possession, ' \
               'custody, or control. AAP has become aware that the story may potentially expose ' \
               'AAP and those who publish the story to the risk of:</p>' \
               '<div style="color:red">' \
               '<p><strong>[insert relevant option/s from below]</strong></p>' \
               '<p>- a claim in defamation.<br></p>' \
               '<p>    - a possible prosecution for contempt.</p>' \
               '<p>    - a contempt prosecution arising out of breach of an order of the ' \
               'Family/Supreme/District/Federal Court.</p>' \
               '<p>    - a breach of a law prohibiting publication.</p>' \
               '<p>    - a breach of an order prohibiting publication that has retrospective ' \
               'effect.</p>' \
               '<p>    - a breach of any State or Commonwealth privacy laws.</p>' \
               '<p>    - a claim for damages.</p>' \
               '<p>    - publishing extremely erroneous material.</p>' \
               '<p><br></p>' \
               '</div>' \
               '<p>    This kill/takedown is mandatory, and no ' \
               'further use can be made of the story.</p><p>    A replacement story will be ' \
               'issued shortly/will not be issued.</p><p>    AAP will not be liable for any ' \
               'losses, costs and expenses, damages and other costs (including without ' \
               'limitation reasonable legal costs), indirect, consequential special or punitive' \
               ' loss or damage, arising out of the story and this Notice suffered or incurred' \
               ' by you after receipt of this Notice.</p>'
        self.assertEqual(
            extract_kill_reason_from_html(html, is_kill=True),
            '<div style="color:red">'
            '<p><strong>[insert relevant option/s from below]</strong></p>'
            '<p>- a claim in defamation.<br></p><p>    - a possible prosecution for contempt.</p>'
            '<p>    - a contempt prosecution arising out of breach of an order of the '
            'Family/Supreme/District/Federal Court.</p>'
            '<p>    - a breach of a law prohibiting publication.</p>'
            '<p>    - a breach of an order prohibiting publication that has retrospective effect.'
            '</p>'
            '<p>    - a breach of any State or Commonwealth privacy laws.</p>'
            '<p>    - a claim for damages.</p>'
            '<p>    - publishing extremely erroneous material.</p>'
            '</div>'
        )

        # Test kill with reason delete from above
        html = '<p>Please kill story slugged Test2 headlined Test2 ex Sydney at 02 Nov 2018 ' \
               '11:21 AEDT.</p><p>Pursuant to your Information Supply Agreement with Australian ' \
               'Associated Press (AAP)  , AAP requests that you remove the above story from any ' \
               'media you publish and access to the story be immediately disabled including but ' \
               'not limited to those websites in either your direct or indirect possession, ' \
               'custody, or control. AAP has become aware that the story may potentially expose ' \
               'AAP and those who publish the story to the risk of:</p>' \
               '<div style="color:red">' \
               '<p>- a claim in defamation.<br></p>' \
               '<p>- a contempt prosecution arising out of breach of an order of the ' \
               'Family/Supreme/District/Federal Court.<br></p>' \
               '<p>    - publishing extremely erroneous material.</p>' \
               '<p><br></p>' \
               '</div>' \
               '<p>    This kill/takedown is mandatory, and no ' \
               'further use can be made of the story.</p><p>    A replacement story will be ' \
               'issued shortly/will not be issued.</p><p>    AAP will not be liable for any ' \
               'losses, costs and expenses, damages and other costs (including without ' \
               'limitation reasonable legal costs), indirect, consequential special or punitive' \
               ' loss or damage, arising out of the story and this Notice suffered or incurred' \
               ' by you after receipt of this Notice.</p>'
        self.assertEqual(
            extract_kill_reason_from_html(html, is_kill=True),
            '<div style="color:red">'
            '<p>- a claim in defamation.<br></p>'
            '<p>- a contempt prosecution arising out of breach of an order of the '
            'Family/Supreme/District/Federal Court.<br></p>'
            '<p>    - publishing extremely erroneous material.</p>'
            '</div>'
        )

        # Test kill with few reasons
        html = '<p>Please kill story slugged Test3 headlined Test3 ex Sydney at 02 Nov 2018 ' \
               '11:25 AEDT.</p><p>Pursuant to your Information Supply Agreement with Australian ' \
               'Associated Press (AAP)  , AAP requests that you remove the above story from any ' \
               'media you publish and access to the story be immediately disabled including but ' \
               'not limited to those websites in either your direct or indirect possession, ' \
               'custody, or control. AAP has become aware that the story may potentially expose ' \
               'AAP and those who publish the story to the risk of:</p>' \
               '<div style="color:red">' \
               '<p>    - a claim for damages.</p>' \
               '<p>    - publishing extremely erroneous material.</p>' \
               '<p><br></p>' \
               '</div>' \
               '<p>    This kill/takedown is mandatory, and no ' \
               'further use can be made of the story.</p><p>    A replacement story will be ' \
               'issued shortly/will not be issued.</p><p>    AAP will not be liable for any ' \
               'losses, costs and expenses, damages and other costs (including without ' \
               'limitation reasonable legal costs), indirect, consequential special or punitive' \
               ' loss or damage, arising out of the story and this Notice suffered or incurred' \
               ' by you after receipt of this Notice.</p>'
        self.assertEqual(
            extract_kill_reason_from_html(html, is_kill=True),
            '<div style="color:red">'
            '<p>    - a claim for damages.</p>'
            '<p>    - publishing extremely erroneous material.</p>'
            '</div>'
        )

        # Test kill
        html = '<p>Please kill story slugged Test4 headlined Test4 ex Sydney at 02 Nov 2018 ' \
               '11:28 AEDT.</p><p>Pursuant to your Information Supply Agreement with Australian ' \
               'Associated Press (AAP)  , AAP requests that you remove the above story from any ' \
               'media you publish and access to the story be immediately disabled including but ' \
               'not limited to those websites in either your direct or indirect possession, ' \
               'custody, or control. AAP has become aware that the story may potentially expose ' \
               'AAP and those who publish the story to the risk of:</p>' \
               '<div style="color:red">' \
               '<p>- a claim in defamation.<br></p>' \
               '<p>    - a possible prosecution for contempt.</p>' \
               '</div>' \
               '<p>    This kill/takedown is mandatory, and no ' \
               'further use can be made of the story.</p><p>    A replacement story will be ' \
               'issued shortly/will not be issued.</p><p>    AAP will not be liable for any ' \
               'losses, costs and expenses, damages and other costs (including without ' \
               'limitation reasonable legal costs), indirect, consequential special or punitive' \
               ' loss or damage, arising out of the story and this Notice suffered or incurred' \
               ' by you after receipt of this Notice.</p>'
        self.assertEqual(
            extract_kill_reason_from_html(html, is_kill=True),
            '<div style="color:red">'
            '<p>- a claim in defamation.<br></p>'
            '<p>    - a possible prosecution for contempt.</p>'
            '</div>'
        )

    def test_extract_takedown_reason_from_html(self):
        # Test takedown with unmodified template
        html = '<p>Pursuant to your Information Supply Agreement with Australian Associated ' \
               'Press (AAP)  , AAP requests that you remove the above story from any media you ' \
               'publish and access to the story be immediately disabled including but not ' \
               'limited to those websites in either your direct or indirect possession, ' \
               'custody, or control. AAP has become aware that the story may potentially expose ' \
               'AAP and those who publish the story to the risk of:</p>' \
               '<div style=\"color:red\">' \
               '<p><strong>[insert relevant option/s from below]</strong></p>' \
               '<p>   - a breach of an enforceable embargo</p>' \
               '<p>- a possible prosecution for contempt.<br></p>' \
               '<p><br></p>' \
               '</div>' \
               '<p>    This takedown is mandatory, and no further use can be made of the ' \
               'story.</p><p>    A replacement story will be issued shortly/will not be ' \
               'issued.</p><p>    AAP will not be liable for any losses, costs and expenses, ' \
               'damages and other costs (including without limitation reasonable legal costs), ' \
               'indirect, consequential special or punitive loss or damage, arising out of the ' \
               'story and this Notice suffered or incurred by you after receipt of this Notice.</p>'
        self.assertEqual(
            extract_kill_reason_from_html(html, is_kill=False),
            '<div style="color:red">'
            '<p><strong>[insert relevant option/s from below]</strong></p>'
            '<p>   - a breach of an enforceable embargo</p>'
            '<p>- a possible prosecution for contempt.<br></p>'
            '</div>'
        )

        # Test takedown with a single reason
        html = '<p>Please takedown story slugged Test5 headlined Test5 ex Sydney at 02 Nov ' \
               '2018 11:30 AEDT.</p><p>Pursuant to your Information Supply Agreement with ' \
               'Australian Associated Press (AAP)  , AAP requests that you remove the above ' \
               'story from any media you publish and access to the story be immediately ' \
               'disabled including but not limited to those websites in either your direct or ' \
               'indirect possession, custody, or control. AAP has become aware that the story ' \
               'may potentially expose AAP and those who publish the story to the risk of:</p>' \
               '<div style="color:red">' \
               '<p>- a possible prosecution for contempt.</p>' \
               '</div>' \
               '<p>    This takedown is mandatory, and no further use can be made of the ' \
               'story.</p><p>    A replacement story will be issued shortly/will not be ' \
               'issued.</p><p>    AAP will not be liable for any losses, costs and expenses, ' \
               'damages and other costs (including without limitation reasonable legal costs), ' \
               'indirect, consequential special or punitive loss or damage, arising out of the ' \
               'story and this Notice suffered or incurred by you after receipt of this Notice.</p>'
        self.assertEqual(
            extract_kill_reason_from_html(html, is_kill=False),
            '<div style="color:red">'
            '<p>- a possible prosecution for contempt.</p>'
            '</div>'
        )
