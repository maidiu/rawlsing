"""
EPR (Ethnic Power Relations) lookup for get_local_modifiers.

Looks up ethnic group power status from EPR-2021 by country and year.
Used to compute exposure/valence for conflict, repression, etc.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from functools import lru_cache

from .country_reference import code_for_system

ROOT = Path(__file__).resolve().parent.parent
EPR_JSON = ROOT / "data" / "EPR-2021.json"

# EPR statename (from EPR-2021) -> ISO3. Covers EPR countries.
# Built from EPR statenames; extend as needed.
STATENAME_TO_ISO3: Dict[str, str] = {
    "Afghanistan": "AFG",
    "Albania": "ALB",
    "Algeria": "DZA",
    "Angola": "AGO",
    "Argentina": "ARG",
    "Armenia": "ARM",
    "Australia": "AUS",
    "Austria": "AUT",
    "Azerbaijan": "AZE",
    "Bahamas": "BHS",
    "Bahrain": "BHR",
    "Bangladesh": "BGD",
    "Barbados": "BRB",
    "Belarus (Byelorussia)": "BLR",
    "Belgium": "BEL",
    "Belize": "BLZ",
    "Benin": "BEN",
    "Bhutan": "BTN",
    "Bolivia": "BOL",
    "Bosnia-Herzegovina": "BIH",
    "Botswana": "BWA",
    "Brazil": "BRA",
    "Brunei": "BRN",
    "Bulgaria": "BGR",
    "Burkina Faso (Upper Volta)": "BFA",
    "Burundi": "BDI",
    "Cambodia (Kampuchea)": "KHM",
    "Cameroon": "CMR",
    "Canada": "CAN",
    "Cape Verde": "CPV",
    "Central African Republic": "CAF",
    "Chad": "TCD",
    "Chile": "CHL",
    "China": "CHN",
    "Colombia": "COL",
    "Comoros": "COM",
    "Congo": "COG",
    "Congo, Democratic Republic of (Zaire)": "COD",
    "Costa Rica": "CRI",
    "Cote D'Ivoire": "CIV",
    "Croatia": "HRV",
    "Cuba": "CUB",
    "Cyprus": "CYP",
    "Denmark": "DNK",
    "Dominican Republic": "DOM",
    "Ecuador": "ECU",
    "Egypt": "EGY",
    "El Salvador": "SLV",
    "Eritrea": "ERI",
    "Estonia": "EST",
    "Ethiopia": "ETH",
    "Fiji": "FJI",
    "Finland": "FIN",
    "France": "FRA",
    "Gabon": "GAB",
    "Gambia": "GMB",
    "Georgia": "GEO",
    "German Federal Republic": "DEU",
    "Ghana": "GHA",
    "Greece": "GRC",
    "Guatemala": "GTM",
    "Guinea": "GIN",
    "Guinea-Bissau": "GNB",
    "Guyana": "GUY",
    "Haiti": "HTI",
    "Honduras": "HND",
    "Hungary": "HUN",
    "India": "IND",
    "Indonesia": "IDN",
    "Iran (Persia)": "IRN",
    "Iraq": "IRQ",
    "Ireland": "IRL",
    "Israel": "ISR",
    "Italy": "ITA",
    "Italy/Sardinia": "ITA",
    "Jamaica": "JAM",
    "Japan": "JPN",
    "Jordan": "JOR",
    "Kazakhstan": "KAZ",
    "Kenya": "KEN",
    "Korea, Republic of": "KOR",
    "Korea, South": "KOR",
    "Kuwait": "KWT",
    "Kyrgyz Republic": "KGZ",
    "Kyrgyzstan": "KGZ",
    "Laos": "LAO",
    "Latvia": "LVA",
    "Lebanon": "LBN",
    "Lesotho": "LSO",
    "Liberia": "LBR",
    "Libya": "LBY",
    "Lithuania": "LTU",
    "Luxembourg": "LUX",
    "Macedonia": "MKD",
    "Madagascar": "MDG",
    "Malawi": "MWI",
    "Malaysia": "MYS",
    "Mali": "MLI",
    "Mauritania": "MRT",
    "Mauritius": "MUS",
    "Mexico": "MEX",
    "Moldova": "MDA",
    "Mongolia": "MNG",
    "Morocco": "MAR",
    "Mozambique": "MOZ",
    "Myanmar (Burma)": "MMR",
    "Namibia": "NAM",
    "Nepal": "NPL",
    "Netherlands": "NLD",
    "Nicaragua": "NIC",
    "Niger": "NER",
    "Nigeria": "NGA",
    "North Yemen": "YEM",
    "Norway": "NOR",
    "Oman": "OMN",
    "Pakistan": "PAK",
    "Panama": "PAN",
    "Papua New Guinea": "PNG",
    "Paraguay": "PRY",
    "Peru": "PER",
    "Philippines": "PHL",
    "Poland": "POL",
    "Portugal": "PRT",
    "Qatar": "QAT",
    "Romania": "ROU",
    "Rumania": "ROU",
    "Russia (Soviet Union)": "RUS",
    "Rwanda": "RWA",
    "Saudi Arabia": "SAU",
    "Senegal": "SEN",
    "Serbia": "SRB",
    "Sierra Leone": "SLE",
    "Singapore": "SGP",
    "Slovakia": "SVK",
    "Slovak Republic": "SVK",
    "Slovenia": "SVN",
    "Somalia": "SOM",
    "South Africa": "ZAF",
    "South Sudan": "SSD",
    "South Yemen": "YEM",
    "Spain": "ESP",
    "Sri Lanka": "LKA",
    "Sudan": "SDN",
    "Surinam": "SUR",
    "Suriname": "SUR",
    "Swaziland": "SWZ",
    "Sweden": "SWE",
    "Switzerland": "CHE",
    "Syria": "SYR",
    "Taiwan": "TWN",
    "Tajikistan": "TJK",
    "Tanzania": "TZA",
    "Thailand": "THA",
    "Togo": "TGO",
    "Trinidad and Tobago": "TTO",
    "Trinidad & Tobago": "TTO",
    "Tunisia": "TUN",
    "Turkey (Ottoman Empire)": "TUR",
    "Turkey": "TUR",
    "Turkmenistan": "TKM",
    "Uganda": "UGA",
    "Ukraine": "UKR",
    "United Arab Emirates": "ARE",
    "United Kingdom": "GBR",
    "United States of America": "USA",
    "Uruguay": "URY",
    "Uzbekistan": "UZB",
    "Venezuela": "VEN",
    "Vietnam": "VNM",
    "Vietnam, Democratic Republic of": "VNM",
    "Yemen": "YEM",
    "Zambia": "ZMB",
    "Zimbabwe": "ZWE",
    "Zimbabwe (Rhodesia)": "ZWE",
    "Czech Republic": "CZE",
    "Czechoslovakia": "CZE",
    "Djibouti": "DJI",
    "East Timor": "TLS",
    "Equatorial Guinea": "GNQ",
    "German Democratic Republic": "DEU",
    "Iceland": "ISL",
    "Korea, People's Republic of": "PRK",
    "Kosovo": "XKX",
    "Macedonia (FYROM/North Macedonia)": "MKD",
    "Madagascar (Malagasy)": "MDG",
    "Maldives": "MDV",
    "Malta": "MLT",
    "Montenegro": "MNE",
    "New Zealand": "NZL",
    "Solomon Islands": "SLB",
    "Sri Lanka (Ceylon)": "LKA",
    "Swaziland (Eswatini)": "SWZ",
    "Tanzania (Tanganyika)": "TZA",
    "Tibet": "CHN",
    "Vietnam, Republic of": "VNM",
    "Yemen (Arab Republic of Yemen)": "YEM",
    "Yemen, People's Republic of": "YEM",
    "Yugoslavia": "SRB",
    "Zanzibar": "TZA",
}

# Reverse: ISO3 -> EPR statename (first match)
ISO3_TO_STATENAME: Dict[str, str] = {}
for sname, iso in STATENAME_TO_ISO3.items():
    if iso not in ISO3_TO_STATENAME:
        ISO3_TO_STATENAME[iso] = sname


def _normalize_group(s: str) -> str:
    """Normalize group name for matching."""
    if not s:
        return ""
    return " ".join(s.strip().lower().split())


def _group_matches(epr_group: str, identity_ethnicity: str) -> bool:
    """Check if identity ethnicity matches EPR group (fuzzy)."""
    if not identity_ethnicity:
        return False
    epr_n = _normalize_group(epr_group)
    id_n = _normalize_group(identity_ethnicity)
    if epr_n == id_n:
        return True
    # Plural/singular: "African Americans" vs "African American"
    if epr_n.rstrip("s") == id_n or epr_n == id_n.rstrip("s"):
        return True
    # Substring: "African Americans" contains "African American"
    if id_n in epr_n or epr_n in id_n:
        return True
    return False


def _load_epr() -> List[Dict]:
    """Load EPR data from JSON."""
    if not EPR_JSON.exists():
        return []
    with EPR_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("data", [])


@lru_cache(maxsize=1)
def _get_epr_index() -> List[Tuple[str, int, int, str, str]]:
    """Index: (statename, from, to, group, status)."""
    records = _load_epr()
    out = []
    for r in records:
        statename = (r.get("statename") or "").strip()
        from_y = int(r.get("from", 0))
        to_y = int(r.get("to", 0))
        group = (r.get("group") or "").strip()
        status = (r.get("status") or "").strip()
        if statename and group and status:
            out.append((statename, from_y, to_y, group, status))
    return out


def get_epr_status(
    country_code: str,
    year: int,
    ethnicity_label: str,
) -> Optional[str]:
    """
    Get EPR power status for a group in a country/year.

    Args:
        country_code: ISO2 or ISO3 (e.g. "US", "USA")
        year: Target year
        ethnicity_label: Identity's ethnicity (e.g. "African Americans", "Whites")

    Returns:
        EPR status: MONOPOLY, DOMINANT, SENIOR PARTNER, JUNIOR PARTNER,
                   POWERLESS, DISCRIMINATED, IRRELEVANT, SELF-EXCLUSION, or None
    """
    code = (country_code or "").strip().upper()
    if len(code) == 2:
        code = code_for_system(code, "iso3")
    statename = ISO3_TO_STATENAME.get(code)
    if not statename:
        return None

    index = _get_epr_index()
    for sname, from_y, to_y, group, status in index:
        if sname != statename:
            continue
        if not (from_y <= year <= to_y):
            continue
        if _group_matches(group, ethnicity_label):
            return status
    return None


def epr_status_to_ethnic_power(status: Optional[str]) -> str:
    """
    Map EPR status to LocalModifiers.ethnic_power_status.

    - MONOPOLY, DOMINANT, SENIOR PARTNER, JUNIOR PARTNER -> dominant
    - POWERLESS, DISCRIMINATED, SELF-EXCLUSION -> minoritized
    - IRRELEVANT -> unclear (ethnically homogenous)
    """
    if not status:
        return "unclear"
    status = status.upper()
    if status in ("MONOPOLY", "DOMINANT", "SENIOR PARTNER", "JUNIOR PARTNER"):
        return "dominant"
    if status in ("POWERLESS", "DISCRIMINATED", "SELF-EXCLUSION"):
        return "minoritized"
    if status == "IRRELEVANT":
        return "unclear"
    return "unclear"
