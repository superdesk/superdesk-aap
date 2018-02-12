# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from ..field_mappers import FieldMapper
from ..aap_formatter_common import set_subject


class LocatorMapper(FieldMapper):

    iptc_locators = {
        '01020000': 'ARTS',
        '01010000': 'BOOKS',
        '08003002': 'CELEB',
        '01007000': 'FASH',
        '01005000': 'FILM',
        '07000000': 'HLTH',
        '10014000': 'MOTOR',
        '01011000': 'MUSIC',
        '01014000': 'RADIO',
        '13000000': 'SCI',
        '13010000': 'TECH',
        '10006000': 'TRAV',
        '01016000': 'TV',
        '01028000': 'HIST',
        '13003002': 'HIST'
    }

    iptc_sports_locators = {
        '15084000': 'AFL',
        '15005000': 'ATHS',
        '15004000': 'ARC',
        '15006000': 'BAD',
        '15007000': 'BASE',
        '15008000': 'BASK',
        '15013000': 'BOWLS',
        '15014000': 'BOX',
        '15067001': 'BVO',
        '15017000': 'CRIK',
        '15019000': 'CYCLE',
        '15100000': 'DAR',
        '15021000': 'DIVE',
        '15022000': 'EQN',
        '15023000': 'FENCE',
        '15073005': 'GAMES',
        '15027000': 'GOLF',
        '15028000': 'GYM',
        '15029000': 'HBL',
        '15024000': 'HOCK',
        '15076000': 'HOCK',  # Bandy
        '15087000': 'HOCK',  # hornuss
        '15031000': 'ICE',
        '15066000': 'TRI',  # and IRON
        '15033000': 'JUDO',
        '15015000': 'KAYAK',  # and CANOE
        '15039000': 'MOTOR',  # motor racing
        '15040000': 'MOTOR',  # motor rallying
        '15041000': 'MOTOR',  # motor cycling
        '15042000': 'NET',
        '15003001': 'NFL',
        '15073001': 'OLY',
        '15073002': 'OLY',
        '15073047': 'PARA',
        '15038000': 'PENT',
        '15045000': 'POLO',
        '15030000': 'RACE',
        '15048000': 'RL',
        '15047000': 'ROW',
        '15049000': 'RU',
        '15050000': 'SAIL',
        '15051000': 'SHOOT',
        '15002000': 'SKI',  # alpine skiing
        '15011000': 'SKI',  # bobsleigh
        '15026000': 'SKI',  # Freestyle Skiing
        '15052000': 'SKI',  # ski jumping
        '15053000': 'SKI',  # snow boarding
        '15043000': 'SKI',  # nordic skiing
        '15090000': 'SKI',  # grass ski
        '15091000': 'SKI',  # snowbiking
        '15083000': 'SKI',  # skeleton
        '15036000': 'SKI',  # luge
        '15010000': 'SNOOK',
        '15000000': 'SPO',
        '15054000': 'SOC',
        '15055000': 'SOFT',
        '15059000': 'SQSH',
        '15062025': 'SSWIM',
        '15062026': 'SSWIM',
        '15061000': 'SURF',
        '15062000': 'SWIM',
        '15064000': 'TAE',
        '15065000': 'TEN',
        '15063000': 'TTEN',
        '15067000': 'VOL',
        '15070000': 'WGHT',
        '15068000': 'WPOL',
        '15072000': 'WRES',  # wrestling
        '15060000': 'WRES',  # sumo wrestling
        '15034000': 'WRES',  # karate
        '15069000': 'WSKI',
        '15089000': 'SPO',  # inline skating
        '15025000': 'SPO',  # figure Skating
        '15056000': 'SPO'  # speed skating
    }

    sport_categories = {'S', 'T', 'R'}

    def map(self, article, category):
        """
        Based on the category and subject code it returns the locator
        :param dict article: original article
        :param str category: category of the article
        :return: if found then the locator as string else None
        """
        # if the category is one of sports categories or
        # if X category and contains sports topic then sports locators.
        if category in self.sport_categories or self._is_special_sport_event(article, category):
            mapped_value = self._map_locator_code(article, category, self.iptc_sports_locators)
        else:
            mapped_value = self._map_locator_code(article, category, self.iptc_locators)

        # If no mapping is found then use the first place value
        if not mapped_value:
            for place in (article.get('place') or []):
                return place.get('qcode')

        return mapped_value

    def _map_locator_code(self, article, category, locators):
        """
        Based on the category and subject code it returns the locator
        :param dict article: original article
        :param str category: category of the article
        :param dict locators: subject code locator mapping dictionary
        :return: if found then the locator as string else None
        """
        subjects = article.get('subject') or []

        # for sports category
        if category in self.sport_categories or self._is_special_sport_event(article, category):
            subject = set_subject({'qcode': category}, article) or ''
            feature = locators.get('{}000'.format(subject[:5])) or locators.get(subject)
            if feature:
                return feature

        # for now restricting to features category.
        if category != 'C':
            return None

        for subject in subjects:
            qcode = subject.get('qcode', '')
            feature = locators.get(qcode)
            if feature:
                if qcode == '10006000':
                    place = article.get('place')[0] if article.get('place', None) else None
                    suffix = 'D'
                    if not place or place.get('country') != 'Australia':
                        suffix = 'I'
                    return '{}{}'.format(feature, suffix)
                else:
                    return feature

        return None

    def _is_special_sport_event(self, article, category):
        """# if X category and contains sports topic then it is special sports event."""
        return category == 'X' and \
            [s for s in article.get('subject') if (s.get('qcode') or '').startswith('15')]

    def get_formatted_headline(self, article, category):
        """
        Based on the category and subject code it prefix the headline with locator.
        If headline contains ':' in first six characters (legacy auto publish)
        then no need for locator mapping.
        :param dict article: original article
        :param str category: category of the article
        :return: Headline with locator prefix
        """
        headline = article.get('headline') or ''

        if article.get('auto_publish', False):
            return headline

        headline_prefix = LocatorMapper().map(article, category)
        if headline_prefix:
            headline = '{}:{}'.format(headline_prefix, headline)

        return headline
