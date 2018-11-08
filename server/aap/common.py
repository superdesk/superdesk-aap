# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2018 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.etree import parse_html, to_string
from lxml import etree


REASON_PREFIX = 'AAP has become aware that the story may potentially expose AAP ' \
                'and those who publish the story to the risk of'
KILL_SUFFIX = 'This kill/takedown is mandatory, and no further use can be made of the story'
TAKEDOWN_SUFFIX = 'This takedown is mandatory, and no further use can be made of the story'


def extract_kill_reason_from_html(html, is_kill):
    """Extract the reason from html for a kill/takedown

    Iterates over the xml nodes and find the node that contains the reason prefix.
    Once the reason prefix has been found add the proceeding nodes to our reason tree,
    until the kill/takedown suffix has been found.

    :param html:
    :param is_kill:
    :return:
    """
    # Create a new tree that we will use to construct the reason nodes
    root = etree.Element('div')

    # A flag to indicate if we're to add the current child node to our reason tree
    adding_nodes = False
    for child in parse_html(html, content='html'):
        # Obtain the text from our child nodes (including sub-child nodes)
        child_text = ''.join(child.itertext())

        if not adding_nodes and REASON_PREFIX in child_text:
            # This child node contains the reason prefix (and we haven't found it already)
            # Therefor set the flag to True indicating that the following child nodes
            # are to be added to our reason tree
            adding_nodes = True
            continue
        elif adding_nodes:
            # If the kill/takedown suffix has been found, then our reason tree is complete
            if is_kill and KILL_SUFFIX in child_text:
                break
            elif not is_kill and TAKEDOWN_SUFFIX in child_text:
                break

            # Otherwise continue adding the child nodes to our reason tree

            # Remove the last sub-child if it only contains a line break
            last_child = child[-1]
            if etree.tostring(last_child) == b'<p><br/></p>':
                child.remove(last_child)

            # Then add this child node to our reason tree
            root.append(child)

    num_children = len(list(root))

    # If the reason tree was not populated, then return the original html provided
    if num_children == 0:
        return html

    # Our reason tree was populated, convert the tree to a string and return it
    return to_string(root, method='html', remove_root_div=num_children == 1)
