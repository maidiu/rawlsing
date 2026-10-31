"""
Country-level ethnicity and religion from CIA Factbook (factbook-out/post/countries2).

Used when EPR/GeoEPR have no data for a country: sample ethnicity/religion by share,
then apply a power heuristic (majority → DOMINANT, second → JUNIOR PARTNER, etc.)
so SES and downstream (LocalModifiers, driver_vec) still get a power proxy.

Data source: factbook-out/post/countries2/{code}.json with persona.ethnicity.top,
persona.religion.top, persona.language. File code = CIA factbook code (e.g. ec for Ecuador).
"""

from __future__ import annotations

import random
from typing import Any, Dict, List, Optional, Tuple

def _country_code_to_factbook_code(country_code: str) -> str:
    """Map ISO3 or ISO2 country code to Factbook file code (lowercase).
    Routed through the central country resolver with no local mapping authority."""
    try:
        from .country_reference import code_for_system
    except ImportError:
        from country_reference import code_for_system
    return (code_for_system(country_code, "factbook") or "").strip().lower()


def _demographics_from_payload(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract demographics dict from full countries2 payload (DB)."""
    persona = data.get("persona") if isinstance(data, dict) else None
    if not persona:
        return None
    eth_top = persona.get("ethnicity", {}).get("top") if isinstance(persona.get("ethnicity"), dict) else None
    rel_top = persona.get("religion", {}).get("top") if isinstance(persona.get("religion"), dict) else None
    lang = persona.get("language") if isinstance(persona.get("language"), dict) else None
    if not eth_top and not rel_top:
        return None
    return {
        "ethnicity": eth_top or [],
        "religion": rel_top or [],
        "language": lang or {},
    }


def load_factbook_demographics_from_db(country_code: str) -> Optional[Dict[str, Any]]:
    """
    Load country-level demographics from Postgres factbook_country (countries2 payload).

    Lookup strategy (in order):
      1. By iso3 column — the DB already stores the ISO3 code; no translation needed.
      2. By iso2 column — for codes that arrive as 2-letter.
      3. By cia_code — last resort, using the hardcoded CIA-file-code translation tables.
         This path exists for backward compatibility but should rarely fire now that
         the DB has iso2/iso3 columns populated for all real countries.

    Returns same shape as load_factbook_demographics, or None if not in DB.
    """
    import logging as _logging
    _logger = _logging.getLogger(__name__)

    cc = (country_code or "").strip().upper()
    if not cc:
        return None
    try:
        from .data_access import _get_db_connection
        conn = _get_db_connection()
        cur = conn.cursor()

        payload = None

        # Path 1: query by iso3 (primary — no translation required)
        if len(cc) == 3:
            cur.execute(
                "SELECT payload FROM factbook_country WHERE iso3 = %s LIMIT 1", (cc,)
            )
            row = cur.fetchone()
            if row:
                payload = row[0]

        # Path 2: query by iso2 (for 2-letter codes)
        if payload is None and len(cc) == 2:
            cur.execute(
                "SELECT payload FROM factbook_country WHERE iso2 = %s LIMIT 1", (cc,)
            )
            row = cur.fetchone()
            if row:
                payload = row[0]

        # Path 3: cia_code fallback (translation via hardcoded tables)
        if payload is None:
            cia_code = _country_code_to_factbook_code(cc)
            if cia_code:
                cur.execute(
                    "SELECT payload FROM factbook_country WHERE cia_code = %s LIMIT 1",
                    (cia_code,),
                )
                row = cur.fetchone()
                if row:
                    payload = row[0]
                    _logger.debug(
                        "load_factbook_demographics_from_db: %r found via cia_code=%r "
                        "(iso3 lookup missed — check iso3 column is populated for this row)",
                        cc, cia_code,
                    )

        cur.close()
        conn.close()

        if payload is None:
            return None
        if isinstance(payload, dict):
            data = payload
        else:
            import json
            data = json.loads(payload) if isinstance(payload, str) else None
        return _demographics_from_payload(data) if data else None
    except Exception:
        return None


def load_factbook_demographics(country_code: str) -> Optional[Dict[str, Any]]:
    """
    Load country-level demographics from Postgres factbook_country only (DB-only; no file fallback).

    Returns:
        Dict with keys: ethnicity (list of [label, share]), religion (list of [label, share]),
        language (primary and mentioned), or None if missing/invalid.
    """
    return load_factbook_demographics_from_db(country_code)


def _sample_by_share(items: List[Tuple[str, float]]) -> Optional[Tuple[str, float, int]]:
    """
    Sample one item from list of (label, share). Share can be 0-1 or 0-100; we normalize.
    Returns (label, share, rank_1based) or None if items empty.
    """
    if not items:
        return None
    total = sum(p for _, p in items)
    if total <= 0:
        return None
    if total > 1.5:  # assume 0-100
        items = [(l, p / 100.0) for l, p in items]
    total = sum(p for _, p in items)
    if total <= 0:
        return None
    # Normalize to sum 1 for sampling
    items = [(l, p / total) for l, p in items]
    r = random.random()
    cum = 0.0
    for i, (label, share) in enumerate(items):
        cum += share
        if r <= cum:
            return (label, share, i + 1)
    return (items[-1][0], items[-1][1], len(items))


def power_heuristic_from_rank(rank_1based: int) -> str:
    """
    Map rank (1 = largest share) to EPR-like power status for get_power_status_adjustment.
    Majority → DOMINANT; second → JUNIOR PARTNER; third → IRRELEVANT; smaller → POWERLESS/DISCRIMINATED.
    """
    if rank_1based <= 1:
        return "DOMINANT"
    if rank_1based == 2:
        return "JUNIOR PARTNER"
    if rank_1based == 3:
        return "IRRELEVANT"
    if rank_1based <= 5:
        return "POWERLESS"
    return "DISCRIMINATED"


def sample_ethnic_from_factbook(country_code: str) -> Optional[Dict[str, Any]]:
    """
    Sample ethnicity from Factbook country-level shares; apply power heuristic by rank.

    Returns same shape as sample_ethnic_group: group_name, power_status (dominant/minoritized/mixed),
    epr_power_status (raw for get_power_status_adjustment), size, groupid (None), epr_group_name.
    """
    dem = load_factbook_demographics(country_code)
    if not dem or not dem.get("ethnicity"):
        return None
    items = dem["ethnicity"]
    # Items may be [label, share] or list of two elements
    pairs: List[Tuple[str, float]] = []
    for it in items:
        if isinstance(it, (list, tuple)) and len(it) >= 2:
            label = str(it[0]).strip() if it[0] is not None else "other"
            try:
                share = float(it[1])
            except (TypeError, ValueError):
                share = 0.0
            if label and label.lower() not in ("unknown", "other"):
                pairs.append((label, share))
        elif isinstance(it, dict) and it.get("label"):
            label = str(it["label"]).strip()
            share = float(it.get("value_pct") or it.get("share") or 0)
            if label:
                pairs.append((label, share))
    if not pairs:
        return None
    sampled = _sample_by_share(pairs)
    if not sampled:
        return None
    label, share, rank = sampled
    epr_status = power_heuristic_from_rank(rank)
    if epr_status in ("MONOPOLY", "DOMINANT", "SENIOR PARTNER"):
        power_status = "dominant"
    elif epr_status in ("POWERLESS", "DISCRIMINATED"):
        power_status = "minoritized"
    else:
        power_status = "mixed"
    return {
        "groupid": None,
        "group_name": label,
        "epr_group_name": label,
        "power_status": power_status,
        "epr_power_status": epr_status,
        "size": share,
        "_provenance": {
            "source_family": "factbook",
            "source_method": "factbook_demographics_fallback",
            "fallback_used": True,
            "fallback_reason": "epr_no_data_or_coverage_gap",
        },
    }


def sample_religion_language_from_factbook(country_code: str) -> Optional[Dict[str, Any]]:
    """
    Sample religion and primary language from Factbook. Same shape as sample_religion_language:
    religion, primary_language, secondary_languages.
    """
    dem = load_factbook_demographics(country_code)
    if not dem:
        return None
    out: Dict[str, Any] = {
        "religion": None,
        "primary_language": None,
        "secondary_languages": [],
    }
    rel_top = dem.get("religion") or []
    if rel_top:
        pairs = []
        for it in rel_top:
            if isinstance(it, (list, tuple)) and len(it) >= 2:
                label = str(it[0]).strip() if it[0] else ""
                try:
                    share = float(it[1])
                except (TypeError, ValueError):
                    share = 0.0
                if label and label.lower() not in ("don't know", "no response", "unspecified", "none", "other"):
                    pairs.append((label, share))
        if pairs:
            sampled = _sample_by_share(pairs)
            if sampled:
                out["religion"] = sampled[0]
    lang = dem.get("language") or {}
    mentioned = lang.get("mentioned") if isinstance(lang.get("mentioned"), list) else None
    if mentioned:
        # First non-noisy entry as primary; rest as secondary
        primary = None
        secondary = []
        for x in mentioned:
            if isinstance(x, str) and x.strip():
                x = x.strip()
                if x.lower() in ("other", "foreign", "indigenous", "other indigenous"):
                    continue
                if primary is None:
                    primary = x
                else:
                    secondary.append(x)
        if primary:
            out["primary_language"] = primary
            out["secondary_languages"] = secondary
    if not out["religion"] and not out["primary_language"]:
        return None
    if not out["religion"]:
        out["religion"] = "Unknown"
    if not out["primary_language"]:
        out["primary_language"] = "Unknown"
    out["_provenance"] = {
        "source_family": "factbook",
        "source_method": "factbook_demographics_fallback",
        "religion_found": bool(out.get("religion") and out.get("religion") != "Unknown"),
        "language_found": bool(out.get("primary_language") and out.get("primary_language") != "Unknown"),
        "fallback_used": True,
        "fallback_reason": "people_groups_missing_or_sparse",
    }
    return out
