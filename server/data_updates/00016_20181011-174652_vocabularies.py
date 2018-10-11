# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author : superdesk
# Creation: 2018-10-11 17:46

from superdesk.commands.data_updates import DataUpdate


class DataUpdate(DataUpdate):

    resource = 'vocabularies'

    def forwards(self, mongodb_collection, mongodb_database):
        mongodb_collection.insert(
            [
                {
                    "_id": "regions",
                    "helper_text": "The administrative state or region of an address",
                    "schema": {
                        "name": {

                        },
                        "qcode": {

                        }
                    },
                    "type": "manageable",
                    "display_name": "State / Region",
                    "unique_field": "qcode",
                    "items": [
                        {
                            "qcode": "NSW",
                            "name": "NSW",
                            "is_active": True
                        },
                        {
                            "qcode": "VIC",
                            "name": "VIC",
                            "is_active": True
                        },
                        {
                            "qcode": "TAS",
                            "name": "TAS",
                            "is_active": True
                        },
                        {
                            "qcode": "WA",
                            "name": "WA",
                            "is_active": True
                        },
                        {
                            "qcode": "QLD",
                            "name": "QLD",
                            "is_active": True
                        },
                        {
                            "qcode": "NT",
                            "name": "NT",
                            "is_active": True
                        },
                        {
                            "qcode": "ACT",
                            "name": "ACT",
                            "is_active": True
                        }
                    ]
                },
                {
                    "_id": "countries",
                    "schema": {
                        "name": {

                        },
                        "qcode": {

                        }
                    },
                    "type": "manageable",
                    "display_name": "Countries",
                    "unique_field": "qcode",
                    "items": [
                        {
                            "qcode": "AFG",
                            "name": "Afghanistan",
                            "is_active": True
                        },
                        {
                            "qcode": "ALA",
                            "name": "Aland Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "ALB",
                            "name": "Albania",
                            "is_active": True
                        },
                        {
                            "qcode": "DZA",
                            "name": "Algeria",
                            "is_active": True
                        },
                        {
                            "qcode": "ASM",
                            "name": "American Samoa",
                            "is_active": True
                        },
                        {
                            "qcode": "AND",
                            "name": "Andorra",
                            "is_active": True
                        },
                        {
                            "qcode": "AGO",
                            "name": "Angola",
                            "is_active": True
                        },
                        {
                            "qcode": "AIA",
                            "name": "Anguilla",
                            "is_active": True
                        },
                        {
                            "qcode": "ATA",
                            "name": "Antarctica",
                            "is_active": True
                        },
                        {
                            "qcode": "ATG",
                            "name": "Antigua and Barbuda",
                            "is_active": True
                        },
                        {
                            "qcode": "ARG",
                            "name": "Argentina",
                            "is_active": True
                        },
                        {
                            "qcode": "ARM",
                            "name": "Armenia",
                            "is_active": True
                        },
                        {
                            "qcode": "ABW",
                            "name": "Aruba",
                            "is_active": True
                        },
                        {
                            "qcode": "AUS",
                            "name": "Australia",
                            "is_active": True
                        },
                        {
                            "qcode": "AUT",
                            "name": "Austria",
                            "is_active": True
                        },
                        {
                            "qcode": "AZE",
                            "name": "Azerbaijan",
                            "is_active": True
                        },
                        {
                            "qcode": "BHS",
                            "name": "Bahamas",
                            "is_active": True
                        },
                        {
                            "qcode": "BHR",
                            "name": "Bahrain",
                            "is_active": True
                        },
                        {
                            "qcode": "BGD",
                            "name": "Bangladesh",
                            "is_active": True
                        },
                        {
                            "qcode": "BRB",
                            "name": "Barbados",
                            "is_active": True
                        },
                        {
                            "qcode": "BLR",
                            "name": "Belarus",
                            "is_active": True
                        },
                        {
                            "qcode": "BEL",
                            "name": "Belgium",
                            "is_active": True
                        },
                        {
                            "qcode": "BLZ",
                            "name": "Belize",
                            "is_active": True
                        },
                        {
                            "qcode": "BEN",
                            "name": "Benin",
                            "is_active": True
                        },
                        {
                            "qcode": "BMU",
                            "name": "Bermuda",
                            "is_active": True
                        },
                        {
                            "qcode": "BTN",
                            "name": "Bhutan",
                            "is_active": True
                        },
                        {
                            "qcode": "BOL",
                            "name": "Bolivia",
                            "is_active": True
                        },
                        {
                            "qcode": "BIH",
                            "name": "Bosnia and Herzegovina",
                            "is_active": True
                        },
                        {
                            "qcode": "BWA",
                            "name": "Botswana",
                            "is_active": True
                        },
                        {
                            "qcode": "BVT",
                            "name": "Bouvet Island",
                            "is_active": True
                        },
                        {
                            "qcode": "BRA",
                            "name": "Brazil",
                            "is_active": True
                        },
                        {
                            "qcode": "VGB",
                            "name": "British Virgin Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "IOT",
                            "name": "British Indian Ocean Territory",
                            "is_active": True
                        },
                        {
                            "qcode": "BRN",
                            "name": "Brunei Darussalam",
                            "is_active": True
                        },
                        {
                            "qcode": "BGR",
                            "name": "Bulgaria",
                            "is_active": True
                        },
                        {
                            "qcode": "BFA",
                            "name": "Burkina Faso",
                            "is_active": True
                        },
                        {
                            "qcode": "BDI",
                            "name": "Burundi",
                            "is_active": True
                        },
                        {
                            "qcode": "KHM",
                            "name": "Cambodia",
                            "is_active": True
                        },
                        {
                            "qcode": "CMR",
                            "name": "Cameroon",
                            "is_active": True
                        },
                        {
                            "qcode": "CAN",
                            "name": "Canada",
                            "is_active": True
                        },
                        {
                            "qcode": "CPV",
                            "name": "Cape Verde",
                            "is_active": True
                        },
                        {
                            "qcode": "CYM",
                            "name": "Cayman Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "CAF",
                            "name": "Central African Republic",
                            "is_active": True
                        },
                        {
                            "qcode": "TCD",
                            "name": "Chad",
                            "is_active": True
                        },
                        {
                            "qcode": "CHL",
                            "name": "Chile",
                            "is_active": True
                        },
                        {
                            "qcode": "CHN",
                            "name": "China",
                            "is_active": True
                        },
                        {
                            "qcode": "HKG",
                            "name": "Hong Kong, SAR China",
                            "is_active": True
                        },
                        {
                            "qcode": "MAC",
                            "name": "Macao, SAR China",
                            "is_active": True
                        },
                        {
                            "qcode": "CXR",
                            "name": "Christmas Island",
                            "is_active": True
                        },
                        {
                            "qcode": "CCK",
                            "name": "Cocos (Keeling) Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "COL",
                            "name": "Colombia",
                            "is_active": True
                        },
                        {
                            "qcode": "COM",
                            "name": "Comoros",
                            "is_active": True
                        },
                        {
                            "qcode": "COG",
                            "name": "Congo (Brazzaville)",
                            "is_active": True
                        },
                        {
                            "qcode": "COD",
                            "name": "Congo, (Kinshasa)",
                            "is_active": True
                        },
                        {
                            "qcode": "COK",
                            "name": "Cook Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "CRI",
                            "name": "Costa Rica",
                            "is_active": True
                        },
                        {
                            "qcode": "CIV",
                            "name": "Côte d'Ivoire",
                            "is_active": True
                        },
                        {
                            "qcode": "HRV",
                            "name": "Croatia",
                            "is_active": True
                        },
                        {
                            "qcode": "CUB",
                            "name": "Cuba",
                            "is_active": True
                        },
                        {
                            "qcode": "CYP",
                            "name": "Cyprus",
                            "is_active": True
                        },
                        {
                            "qcode": "CZE",
                            "name": "Czech Republic",
                            "is_active": True
                        },
                        {
                            "qcode": "DNK",
                            "name": "Denmark",
                            "is_active": True
                        },
                        {
                            "qcode": "DJI",
                            "name": "Djibouti",
                            "is_active": True
                        },
                        {
                            "qcode": "DMA",
                            "name": "Dominica",
                            "is_active": True
                        },
                        {
                            "qcode": "DOM",
                            "name": "Dominican Republic",
                            "is_active": True
                        },
                        {
                            "qcode": "ECU",
                            "name": "Ecuador",
                            "is_active": True
                        },
                        {
                            "qcode": "EGY",
                            "name": "Egypt",
                            "is_active": True
                        },
                        {
                            "qcode": "SLV",
                            "name": "El Salvador",
                            "is_active": True
                        },
                        {
                            "qcode": "GNQ",
                            "name": "Equatorial Guinea",
                            "is_active": True
                        },
                        {
                            "qcode": "ERI",
                            "name": "Eritrea",
                            "is_active": True
                        },
                        {
                            "qcode": "EST",
                            "name": "Estonia",
                            "is_active": True
                        },
                        {
                            "qcode": "ETH",
                            "name": "Ethiopia",
                            "is_active": True
                        },
                        {
                            "qcode": "FLK",
                            "name": "Falkland Islands (Malvinas)",
                            "is_active": True
                        },
                        {
                            "qcode": "FRO",
                            "name": "Faroe Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "FJI",
                            "name": "Fiji",
                            "is_active": True
                        },
                        {
                            "qcode": "FIN",
                            "name": "Finland",
                            "is_active": True
                        },
                        {
                            "qcode": "FRA",
                            "name": "France",
                            "is_active": True
                        },
                        {
                            "qcode": "GUF",
                            "name": "French Guiana",
                            "is_active": True
                        },
                        {
                            "qcode": "PYF",
                            "name": "French Polynesia",
                            "is_active": True
                        },
                        {
                            "qcode": "ATF",
                            "name": "French Southern Territories",
                            "is_active": True
                        },
                        {
                            "qcode": "GAB",
                            "name": "Gabon",
                            "is_active": True
                        },
                        {
                            "qcode": "GMB",
                            "name": "Gambia",
                            "is_active": True
                        },
                        {
                            "qcode": "GEO",
                            "name": "Georgia",
                            "is_active": True
                        },
                        {
                            "qcode": "DEU",
                            "name": "Germany",
                            "is_active": True
                        },
                        {
                            "qcode": "GHA",
                            "name": "Ghana",
                            "is_active": True
                        },
                        {
                            "qcode": "GIB",
                            "name": "Gibraltar",
                            "is_active": True
                        },
                        {
                            "qcode": "GRC",
                            "name": "Greece",
                            "is_active": True
                        },
                        {
                            "qcode": "GRL",
                            "name": "Greenland",
                            "is_active": True
                        },
                        {
                            "qcode": "GRD",
                            "name": "Grenada",
                            "is_active": True
                        },
                        {
                            "qcode": "GLP",
                            "name": "Guadeloupe",
                            "is_active": True
                        },
                        {
                            "qcode": "GUM",
                            "name": "Guam",
                            "is_active": True
                        },
                        {
                            "qcode": "GTM",
                            "name": "Guatemala",
                            "is_active": True
                        },
                        {
                            "qcode": "GGY",
                            "name": "Guernsey",
                            "is_active": True
                        },
                        {
                            "qcode": "GIN",
                            "name": "Guinea",
                            "is_active": True
                        },
                        {
                            "qcode": "GNB",
                            "name": "Guinea-Bissau",
                            "is_active": True
                        },
                        {
                            "qcode": "GUY",
                            "name": "Guyana",
                            "is_active": True
                        },
                        {
                            "qcode": "HTI",
                            "name": "Haiti",
                            "is_active": True
                        },
                        {
                            "qcode": "HMD",
                            "name": "Heard and Mcdonald Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "VAT",
                            "name": "Holy See (Vatican City State)",
                            "is_active": True
                        },
                        {
                            "qcode": "HND",
                            "name": "Honduras",
                            "is_active": True
                        },
                        {
                            "qcode": "HUN",
                            "name": "Hungary",
                            "is_active": True
                        },
                        {
                            "qcode": "ISL",
                            "name": "Iceland",
                            "is_active": True
                        },
                        {
                            "qcode": "IND",
                            "name": "India",
                            "is_active": True
                        },
                        {
                            "qcode": "IDN",
                            "name": "Indonesia",
                            "is_active": True
                        },
                        {
                            "qcode": "IRN",
                            "name": "Iran, Islamic Republic of",
                            "is_active": True
                        },
                        {
                            "qcode": "IRQ",
                            "name": "Iraq",
                            "is_active": True
                        },
                        {
                            "qcode": "IRL",
                            "name": "Ireland",
                            "is_active": True
                        },
                        {
                            "qcode": "IMN",
                            "name": "Isle of Man",
                            "is_active": True
                        },
                        {
                            "qcode": "ISR",
                            "name": "Israel",
                            "is_active": True
                        },
                        {
                            "qcode": "ITA",
                            "name": "Italy",
                            "is_active": True
                        },
                        {
                            "qcode": "JAM",
                            "name": "Jamaica",
                            "is_active": True
                        },
                        {
                            "qcode": "JPN",
                            "name": "Japan",
                            "is_active": True
                        },
                        {
                            "qcode": "JEY",
                            "name": "Jersey",
                            "is_active": True
                        },
                        {
                            "qcode": "JOR",
                            "name": "Jordan",
                            "is_active": True
                        },
                        {
                            "qcode": "KAZ",
                            "name": "Kazakhstan",
                            "is_active": True
                        },
                        {
                            "qcode": "KEN",
                            "name": "Kenya",
                            "is_active": True
                        },
                        {
                            "qcode": "KIR",
                            "name": "Kiribati",
                            "is_active": True
                        },
                        {
                            "qcode": "PRK",
                            "name": "Korea (North)",
                            "is_active": True
                        },
                        {
                            "qcode": "KOR",
                            "name": "Korea (South)",
                            "is_active": True
                        },
                        {
                            "qcode": "KWT",
                            "name": "Kuwait",
                            "is_active": True
                        },
                        {
                            "qcode": "KGZ",
                            "name": "Kyrgyzstan",
                            "is_active": True
                        },
                        {
                            "qcode": "LAO",
                            "name": "Lao PDR",
                            "is_active": True
                        },
                        {
                            "qcode": "LVA",
                            "name": "Latvia",
                            "is_active": True
                        },
                        {
                            "qcode": "LBN",
                            "name": "Lebanon",
                            "is_active": True
                        },
                        {
                            "qcode": "LSO",
                            "name": "Lesotho",
                            "is_active": True
                        },
                        {
                            "qcode": "LBR",
                            "name": "Liberia",
                            "is_active": True
                        },
                        {
                            "qcode": "LBY",
                            "name": "Libya",
                            "is_active": True
                        },
                        {
                            "qcode": "LIE",
                            "name": "Liechtenstein",
                            "is_active": True
                        },
                        {
                            "qcode": "LTU",
                            "name": "Lithuania",
                            "is_active": True
                        },
                        {
                            "qcode": "LUX",
                            "name": "Luxembourg",
                            "is_active": True
                        },
                        {
                            "qcode": "MKD",
                            "name": "Macedonia, Republic of",
                            "is_active": True
                        },
                        {
                            "qcode": "MDG",
                            "name": "Madagascar",
                            "is_active": True
                        },
                        {
                            "qcode": "MWI",
                            "name": "Malawi",
                            "is_active": True
                        },
                        {
                            "qcode": "MYS",
                            "name": "Malaysia",
                            "is_active": True
                        },
                        {
                            "qcode": "MDV",
                            "name": "Maldives",
                            "is_active": True
                        },
                        {
                            "qcode": "MLI",
                            "name": "Mali",
                            "is_active": True
                        },
                        {
                            "qcode": "MLT",
                            "name": "Malta",
                            "is_active": True
                        },
                        {
                            "qcode": "MHL",
                            "name": "Marshall Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "MTQ",
                            "name": "Martinique",
                            "is_active": True
                        },
                        {
                            "qcode": "MRT",
                            "name": "Mauritania",
                            "is_active": True
                        },
                        {
                            "qcode": "MUS",
                            "name": "Mauritius",
                            "is_active": True
                        },
                        {
                            "qcode": "MYT",
                            "name": "Mayotte",
                            "is_active": True
                        },
                        {
                            "qcode": "MEX",
                            "name": "Mexico",
                            "is_active": True
                        },
                        {
                            "qcode": "FSM",
                            "name": "Micronesia, Federated States of",
                            "is_active": True
                        },
                        {
                            "qcode": "MDA",
                            "name": "Moldova",
                            "is_active": True
                        },
                        {
                            "qcode": "MCO",
                            "name": "Monaco",
                            "is_active": True
                        },
                        {
                            "qcode": "MNG",
                            "name": "Mongolia",
                            "is_active": True
                        },
                        {
                            "qcode": "MNE",
                            "name": "Montenegro",
                            "is_active": True
                        },
                        {
                            "qcode": "MSR",
                            "name": "Montserrat",
                            "is_active": True
                        },
                        {
                            "qcode": "MAR",
                            "name": "Morocco",
                            "is_active": True
                        },
                        {
                            "qcode": "MOZ",
                            "name": "Mozambique",
                            "is_active": True
                        },
                        {
                            "qcode": "MMR",
                            "name": "Myanmar",
                            "is_active": True
                        },
                        {
                            "qcode": "NAM",
                            "name": "Namibia",
                            "is_active": True
                        },
                        {
                            "qcode": "NRU",
                            "name": "Nauru",
                            "is_active": True
                        },
                        {
                            "qcode": "NPL",
                            "name": "Nepal",
                            "is_active": True
                        },
                        {
                            "qcode": "NLD",
                            "name": "Netherlands",
                            "is_active": True
                        },
                        {
                            "qcode": "ANT",
                            "name": "Netherlands Antilles",
                            "is_active": True
                        },
                        {
                            "qcode": "NCL",
                            "name": "New Caledonia",
                            "is_active": True
                        },
                        {
                            "qcode": "NZL",
                            "name": "New Zealand",
                            "is_active": True
                        },
                        {
                            "qcode": "NIC",
                            "name": "Nicaragua",
                            "is_active": True
                        },
                        {
                            "qcode": "NER",
                            "name": "Niger",
                            "is_active": True
                        },
                        {
                            "qcode": "NGA",
                            "name": "Nigeria",
                            "is_active": True
                        },
                        {
                            "qcode": "NIU",
                            "name": "Niue",
                            "is_active": True
                        },
                        {
                            "qcode": "NFK",
                            "name": "Norfolk Island",
                            "is_active": True
                        },
                        {
                            "qcode": "MNP",
                            "name": "Northern Mariana Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "NOR",
                            "name": "Norway",
                            "is_active": True
                        },
                        {
                            "qcode": "OMN",
                            "name": "Oman",
                            "is_active": True
                        },
                        {
                            "qcode": "PAK",
                            "name": "Pakistan",
                            "is_active": True
                        },
                        {
                            "qcode": "PLW",
                            "name": "Palau",
                            "is_active": True
                        },
                        {
                            "qcode": "PSE",
                            "name": "Palestinian Territory",
                            "is_active": True
                        },
                        {
                            "qcode": "PAN",
                            "name": "Panama",
                            "is_active": True
                        },
                        {
                            "qcode": "PNG",
                            "name": "Papua New Guinea",
                            "is_active": True
                        },
                        {
                            "qcode": "PRY",
                            "name": "Paraguay",
                            "is_active": True
                        },
                        {
                            "qcode": "PER",
                            "name": "Peru",
                            "is_active": True
                        },
                        {
                            "qcode": "PHL",
                            "name": "Philippines",
                            "is_active": True
                        },
                        {
                            "qcode": "PCN",
                            "name": "Pitcairn",
                            "is_active": True
                        },
                        {
                            "qcode": "POL",
                            "name": "Poland",
                            "is_active": True
                        },
                        {
                            "qcode": "PRT",
                            "name": "Portugal",
                            "is_active": True
                        },
                        {
                            "qcode": "PRI",
                            "name": "Puerto Rico",
                            "is_active": True
                        },
                        {
                            "qcode": "QAT",
                            "name": "Qatar",
                            "is_active": True
                        },
                        {
                            "qcode": "REU",
                            "name": "Réunion",
                            "is_active": True
                        },
                        {
                            "qcode": "ROU",
                            "name": "Romania",
                            "is_active": True
                        },
                        {
                            "qcode": "RUS",
                            "name": "Russian Federation",
                            "is_active": True
                        },
                        {
                            "qcode": "RWA",
                            "name": "Rwanda",
                            "is_active": True
                        },
                        {
                            "qcode": "BLM",
                            "name": "Saint-Barthélemy",
                            "is_active": True
                        },
                        {
                            "qcode": "SHN",
                            "name": "Saint Helena",
                            "is_active": True
                        },
                        {
                            "qcode": "KNA",
                            "name": "Saint Kitts and Nevis",
                            "is_active": True
                        },
                        {
                            "qcode": "LCA",
                            "name": "Saint Lucia",
                            "is_active": True
                        },
                        {
                            "qcode": "MAF",
                            "name": "Saint-Martin (French part)",
                            "is_active": True
                        },
                        {
                            "qcode": "SPM",
                            "name": "Saint Pierre and Miquelon",
                            "is_active": True
                        },
                        {
                            "qcode": "VCT",
                            "name": "Saint Vincent and Grenadines",
                            "is_active": True
                        },
                        {
                            "qcode": "WSM",
                            "name": "Samoa",
                            "is_active": True
                        },
                        {
                            "qcode": "SMR",
                            "name": "San Marino",
                            "is_active": True
                        },
                        {
                            "qcode": "STP",
                            "name": "Sao Tome and Principe",
                            "is_active": True
                        },
                        {
                            "qcode": "SAU",
                            "name": "Saudi Arabia",
                            "is_active": True
                        },
                        {
                            "qcode": "SEN",
                            "name": "Senegal",
                            "is_active": True
                        },
                        {
                            "qcode": "SRB",
                            "name": "Serbia",
                            "is_active": True
                        },
                        {
                            "qcode": "SYC",
                            "name": "Seychelles",
                            "is_active": True
                        },
                        {
                            "qcode": "SLE",
                            "name": "Sierra Leone",
                            "is_active": True
                        },
                        {
                            "qcode": "SGP",
                            "name": "Singapore",
                            "is_active": True
                        },
                        {
                            "qcode": "SVK",
                            "name": "Slovakia",
                            "is_active": True
                        },
                        {
                            "qcode": "SVN",
                            "name": "Slovenia",
                            "is_active": True
                        },
                        {
                            "qcode": "SLB",
                            "name": "Solomon Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "SOM",
                            "name": "Somalia",
                            "is_active": True
                        },
                        {
                            "qcode": "ZAF",
                            "name": "South Africa",
                            "is_active": True
                        },
                        {
                            "qcode": "SGS",
                            "name": "South Georgia and the South Sandwich Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "SSD",
                            "name": "South Sudan",
                            "is_active": True
                        },
                        {
                            "qcode": "ESP",
                            "name": "Spain",
                            "is_active": True
                        },
                        {
                            "qcode": "LKA",
                            "name": "Sri Lanka",
                            "is_active": True
                        },
                        {
                            "qcode": "SDN",
                            "name": "Sudan",
                            "is_active": True
                        },
                        {
                            "qcode": "SUR",
                            "name": "Suriname",
                            "is_active": True
                        },
                        {
                            "qcode": "SJM",
                            "name": "Svalbard and Jan Mayen Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "SWZ",
                            "name": "Swaziland",
                            "is_active": True
                        },
                        {
                            "qcode": "SWE",
                            "name": "Sweden",
                            "is_active": True
                        },
                        {
                            "qcode": "CHE",
                            "name": "Switzerland",
                            "is_active": True
                        },
                        {
                            "qcode": "SYR",
                            "name": "Syrian Arab Republic (Syria)",
                            "is_active": True
                        },
                        {
                            "qcode": "TWN",
                            "name": "Taiwan, Republic of China",
                            "is_active": True
                        },
                        {
                            "qcode": "TJK",
                            "name": "Tajikistan",
                            "is_active": True
                        },
                        {
                            "qcode": "TZA",
                            "name": "Tanzania, United Republic of",
                            "is_active": True
                        },
                        {
                            "qcode": "THA",
                            "name": "Thailand",
                            "is_active": True
                        },
                        {
                            "qcode": "TLS",
                            "name": "Timor-Leste",
                            "is_active": True
                        },
                        {
                            "qcode": "TGO",
                            "name": "Togo",
                            "is_active": True
                        },
                        {
                            "qcode": "TKL",
                            "name": "Tokelau",
                            "is_active": True
                        },
                        {
                            "qcode": "TON",
                            "name": "Tonga",
                            "is_active": True
                        },
                        {
                            "qcode": "TTO",
                            "name": "Trinidad and Tobago",
                            "is_active": True
                        },
                        {
                            "qcode": "TUN",
                            "name": "Tunisia",
                            "is_active": True
                        },
                        {
                            "qcode": "TUR",
                            "name": "Turkey",
                            "is_active": True
                        },
                        {
                            "qcode": "TKM",
                            "name": "Turkmenistan",
                            "is_active": True
                        },
                        {
                            "qcode": "TCA",
                            "name": "Turks and Caicos Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "TUV",
                            "name": "Tuvalu",
                            "is_active": True
                        },
                        {
                            "qcode": "UGA",
                            "name": "Uganda",
                            "is_active": True
                        },
                        {
                            "qcode": "UKR",
                            "name": "Ukraine",
                            "is_active": True
                        },
                        {
                            "qcode": "ARE",
                            "name": "United Arab Emirates",
                            "is_active": True
                        },
                        {
                            "qcode": "GBR",
                            "name": "United Kingdom",
                            "is_active": True
                        },
                        {
                            "qcode": "USA",
                            "name": "United States of America",
                            "is_active": True
                        },
                        {
                            "qcode": "UMI",
                            "name": "US Minor Outlying Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "URY",
                            "name": "Uruguay",
                            "is_active": True
                        },
                        {
                            "qcode": "UZB",
                            "name": "Uzbekistan",
                            "is_active": True
                        },
                        {
                            "qcode": "VUT",
                            "name": "Vanuatu",
                            "is_active": True
                        },
                        {
                            "qcode": "VEN",
                            "name": "Venezuela (Bolivarian Republic)",
                            "is_active": True
                        },
                        {
                            "qcode": "VNM",
                            "name": "Viet Nam",
                            "is_active": True
                        },
                        {
                            "qcode": "VIR",
                            "name": "Virgin Islands, US",
                            "is_active": True
                        },
                        {
                            "qcode": "WLF",
                            "name": "Wallis and Futuna Islands",
                            "is_active": True
                        },
                        {
                            "qcode": "ESH",
                            "name": "Western Sahara",
                            "is_active": True
                        },
                        {
                            "qcode": "YEM",
                            "name": "Yemen",
                            "is_active": True
                        },
                        {
                            "qcode": "ZMB",
                            "name": "Zambia",
                            "is_active": True
                        },
                        {
                            "qcode": "ZWE",
                            "name": "Zimbabwe",
                            "is_active": True
                        }
                    ]
                }
            ]
        )
        mongodb_collection.remove("contact_states")

    def backwards(self, mongodb_collection, mongodb_database):
        mongodb_collection.remove("regions")
        mongodb_collection.remove("countries")
        mongodb_collection.insert(
            [
                {
                    "_id": "contact_states",
                    "helper_text": "The administrative state or region of an address",
                    "schema": {
                        "name": {

                        },
                        "qcode": {

                        }
                    },
                    "type": "manageable",
                    "display_name": "State / Region",
                    "unique_field": "qcode",
                    "items": [
                        {
                            "qcode": "NSW",
                            "name": "NSW",
                            "is_active": True
                        },
                        {
                            "qcode": "VIC",
                            "name": "VIC",
                            "is_active": True
                        },
                        {
                            "qcode": "TAS",
                            "name": "TAS",
                            "is_active": True
                        },
                        {
                            "qcode": "WA",
                            "name": "WA",
                            "is_active": True
                        },
                        {
                            "qcode": "QLD",
                            "name": "QLD",
                            "is_active": True
                        },
                        {
                            "qcode": "NT",
                            "name": "NT",
                            "is_active": True
                        },
                        {
                            "qcode": "ACT",
                            "name": "ACT",
                            "is_active": True
                        }
                    ]
                }
            ]
        )
