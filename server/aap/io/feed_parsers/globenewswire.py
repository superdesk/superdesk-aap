# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015, 2016, 2017 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.io.registry import register_feed_parser
import textwrap
from lxml import etree
import lxml.html as lxml_html
from superdesk.errors import AlreadyExistsError
from superdesk.text_utils import get_text
from superdesk.io.feed_parsers import NITFFeedParser
from superdesk.metadata.item import FORMAT


class GlobeNewsWireNITF(NITFFeedParser):
    NAME = 'GlobeNewsWire'

    label = 'Globe Newswire NITF Feed Parser'

    def __init__(self):
        self.MAPPING = {
            "guid": self.set_guid,
            "uri": {"xpath": "head/docdata/doc-id/@id-string", "default": None},
            "firstcreated": {
                "xpath": "head/docdata/date.issue",
                "filter": self.get_norm_datetime,
            },
            "versioncreated": {
                "xpath": "head/docdata/date.issue",
                "filter": self.get_norm_datetime,
            },
            "body_html": self.get_content,
            FORMAT: self.get_format,
            "anpa_take_key": {
                "xpath": "head/meta[@name='issuer-name']/@content"
            },
            "version": {"xpath": "head/meta[@name='article-revision']/@content"},
            "headline": self.get_headline,
            "abstract": self.get_abstract,
            "copyrightholder": {"xpath": "head/docdata/doc.copyright/@holder"},
            "extra": self.get_thumbnail,
        }

        super().__init__()
        self.default_mapping = {}

    def get_abstract(self, xml):
        elements = []
        found_dateline = False
        for elem in xml.find("body/body.content"):
            elem_str = etree.tostring(elem, encoding="unicode")
            if ' (GLOBE NEWSWIRE) --' in elem_str or found_dateline:
                found_dateline = True
                elements.append(elem_str)
        content = "".join(elements)
        if not found_dateline:
            content = etree.tostring(xml.find("body/body.content"), encoding="unicode")

        abstract = get_text(content, content="xml")
        return '<p>' + (abstract if len(abstract) <= 450 else textwrap.wrap(abstract, 447)[0] + "...") + '</p>'

    def get_content(self, xml):
        cleaner = lxml_html.clean.Cleaner(
            scripts=True,
            javascript=True,
            style=True,
            embedded=False,
            comments=True,
            add_nofollow=True,
            kill_tags=["style", "script"],
            safe_attrs=["alt", "src", "rel", "href", "target", "title"],
        )
        elements = []
        for elem in xml.find("body/body.content"):
            elements.append(etree.tostring(elem, encoding="unicode"))
        content = "\r\n".join(elements)

        h2 = ''
        if xml.find("body/body.head/hedline/hl2") is not None:
            h2 = '<p>{}</p>'.format(xml.find("body/body.head/hedline/hl2").text)

        div_start = "<div>"
        div_end = "</div>"
        return h2 + cleaner.clean_html(div_start + content + div_end)[len(div_start):-len(div_end)]

    def set_guid(self, xml):
        return 'globenewswire{}:{}'.format(xml.find("head/docdata/doc-id").attrib['id-string'],
                                           xml.find("head/meta[@name='article-revision']").attrib["content"])

    def get_thumbnail(self, xml):
        if xml.find("body/body.content/p/a/img[@alt='Primary Logo']") is not None:
            img = xml.find("body/body.content/p/a/img[@alt='Primary Logo']")
            return {"multimedia": [
                {
                    "caption": "Primary Logo",
                    "seq": "1",
                    "thumbnailurl": img.attrib["src"],
                    "type": "photo",
                    "url": img.attrib["src"],
                }
            ]}

    def parse(self, xml, provider=None):
        item = super().parse(xml, provider)
        item['anpa_category'] = [{'qcode': 'j'}]
        item['slugline'] = 'GlobeNewswire'
        item['original_source'] = 'Intrado'
        return item


try:
    register_feed_parser(GlobeNewsWireNITF.NAME, GlobeNewsWireNITF())
except AlreadyExistsError:
    pass
