"""
Enrich parent context with OWID/WDI/V-Dem world_state (historical) and fallback to CIA Factbook.

Runs AFTER the methodical pipeline (generate_parent_identities + WVS driver vecs).
Uses get_world_slice(country, child_birth_year) for year-specific data—critical for
someone born in 1985 (internet ~0%, very different IMR/LE) vs 2024.

Primary: world_state (OWID GDP, WDI internet/unemployment/gini, V-Dem repression, etc.)
Fallback: CIA Factbook only when world_state has no row (current-year snapshot—document limitation).
"""

import random
from typing import Any, Callable, Dict, Optional


def _load_factbook_for_country(country_code: str) -> Dict[str, Any] | None:
    """Lazy-load factbook data. Returns None if factbook_loader unavailable."""
    try:
        from .factbook_loader import load_factbook_for_country
    except ImportError:
        try:
            from factbook_loader import load_factbook_for_country
        except ImportError:
            return None
    return load_factbook_for_country(country_code)


def _extract_numeric_pct(raw_val: Any) -> float | None:
    try:
        from .factbook_loader import extract_numeric_pct
    except ImportError:
        try:
            from factbook_loader import extract_numeric_pct
        except ImportError:
            return None
    return extract_numeric_pct(raw_val)


def _extract_numeric(raw_val: Any) -> float | None:
    try:
        from .factbook_loader import extract_numeric
    except ImportError:
        try:
            from factbook_loader import extract_numeric
        except ImportError:
            return None
    return extract_numeric(raw_val)


def enrich_family_context(
    parent_identity: Dict[str, Any],
    country_code: str,
    child_birth_year: int,
    get_world_slice: Optional[Callable[[str, int], Any]] = None,
    rng: Optional[random.Random] = None,
) -> Dict[str, Any]:
    """
    Enrich family context with HISTORICAL data for child_birth_year.
    
    Primary: get_world_slice(country_code, child_birth_year) → OWID/WDI/V-Dem.
    This gives year-specific: internet_users_pct, unemployment, gdp_per_capita, gini,
    conflict_intensity, welfare_support. For a 40yo (born 1985), internet is ~0%.
    
    Fallback: CIA Factbook when world_state empty—but Factbook is current (2023–24),
    so IMR/LE may be wrong for historical births. Used only when no world_state row.
    
    Returns:
        { "world_slice": {...}, "household": {...}, "birth_context": {...} }
    """
    rng = rng or random.Random()
    result: Dict[str, Any] = {"world_slice": {}, "household": {}, "birth_context": {}}
    internet_pct = 0.0
    
    # 1. Primary: historical world_state (OWID/WDI/V-Dem) – year-specific
    world_row = None
    if get_world_slice:
        try:
            ws = get_world_slice(country_code, child_birth_year)
            # data_access: media_saturation = internet_users_pct from world_state
            has_real_data = getattr(ws, "metadata", {}) and ws.metadata.get("resampling_method") != "default"
            meta = getattr(ws, "metadata", None) or {}
            world_row = {
                "internet_users_pct": getattr(ws, "media_saturation", 0) or 0,
                "gdp_per_capita": getattr(ws, "gdp_per_capita", 50),
                "unemployment_rate": getattr(ws, "unemployment_level", 0) or 0,
                "gini_index": getattr(ws, "inequality_index", 50),
                "conflict_intensity": getattr(ws, "conflict_intensity", 0),
                "welfare_support": getattr(ws, "welfare_support", 50),
                "adult_literacy_pct": meta.get("adult_literacy_pct"),
                "gender_inequality_index": meta.get("gender_inequality_index"),
                "urban_pct": meta.get("urban_pct"),
                "mean_years_schooling": meta.get("mean_years_schooling"),
                "employment_agriculture_pct": meta.get("employment_agriculture_pct"),
                "_historical": has_real_data,
            }
        except Exception:
            pass
    
    if world_row:
        result["world_slice"] = world_row
        internet_pct = world_row.get("internet_users_pct") or 0
        # Birth context from world_state when available (life_expectancy, infant_mortality in metadata)
        try:
            meta = getattr(ws, "metadata", None) or {}
            le = meta.get("life_expectancy")
            imr = meta.get("infant_mortality_per_1000")
            if le is not None or imr is not None:
                result["birth_context"] = {
                    "country_life_expectancy": float(le) if le is not None else None,
                    "infant_mortality_per_1000": float(imr) if imr is not None else None,
                }
        except Exception:
            pass
        # Country literacy in metadata → will be used below for household adult_literacy_context
    else:
        # 2. Fallback: CIA Factbook (optional — fine if unavailable)
        factbook = None
        try:
            factbook = _load_factbook_for_country(country_code)
        except Exception:
            pass
        if factbook:
            # When from DB, values are already numeric; else parse from text (e.g. "77% (2024 est.)")
            from_db = factbook.get("_from_db") is True
            v = factbook.get("internet_users_pct")
            internet_pct = float(v) if (from_db and isinstance(v, (int, float))) else (_extract_numeric_pct(v) or 0.0)
            u = factbook.get("unemployment")
            if from_db and isinstance(u, (int, float)):
                unemp_rate = (u * 100.0) if u <= 1 else u  # loader gives 0–100; if raw decimal use *100
            else:
                unemp_rate = _extract_numeric_pct(u) or 0
            gdp = factbook.get("gdp_per_capita") if from_db else None
            gdp_val = float(gdp) if isinstance(gdp, (int, float)) else 50.0
            result["world_slice"] = {
                "internet_users_pct": internet_pct,
                "gdp_per_capita": gdp_val if from_db else 50,
                "unemployment_rate": unemp_rate,
                "gini_index": 50,
                "conflict_intensity": 0,
                "welfare_support": 50,
                "_source": "factbook_current",
                "_note": "CIA Factbook is current (2023–24); for historical births use get_world_slice",
            }
            imr_raw = factbook.get("imr_total")
            le_raw = factbook.get("le_total")
            imr = float(imr_raw) if (from_db and isinstance(imr_raw, (int, float))) else _extract_numeric(imr_raw)
            le = float(le_raw) if (from_db and isinstance(le_raw, (int, float))) else _extract_numeric(le_raw)
            result["birth_context"] = {
                "infant_mortality_per_1000": imr,
                "country_life_expectancy": le,
            }
        else:
            result["world_slice"] = {"internet_users_pct": 0, "gdp_per_capita": 50, "unemployment_rate": 0, "gini_index": 50}
            result["birth_context"] = {"infant_mortality_per_1000": None, "country_life_expectancy": None}
    
    # 3. Probabilistic household (SES + urbanicity modulate historical internet; literacy from world_state when available)
    ses = parent_identity.get("ses") or {}
    decile = ses.get("decile", 5)
    location = parent_identity.get("location") or {}
    urbanicity = (location.get("urbanicity") or "").lower()
    
    ses_factor = 0.5 + (decile / 10.0) * 0.5
    urb_factor = 1.2 if any(k in urbanicity for k in ("city", "mega", "town")) else 0.9
    hh_internet = (internet_pct or 0) * ses_factor * (urb_factor if urbanicity else 1.0)
    # Country-year adult literacy from world_slice when available (from world_state); else proxy 50 * ses_factor
    country_literacy = result.get("world_slice", {}).get("adult_literacy_pct") if result.get("world_slice") else None
    hh_literacy = (float(country_literacy) if country_literacy is not None else 50.0) * ses_factor
    
    result["household"] = {
        "internet_access_pct": min(100.0, max(0.0, hh_internet + rng.uniform(-3, 3))),
        "adult_literacy_context": min(100.0, hh_literacy),
        "urbanicity": urbanicity,
        "ses_decile": decile,
    }
    
    if not result.get("birth_context") and world_row:
        result["birth_context"] = {
            "infant_mortality_per_1000": None,
            "country_life_expectancy": None,
        }
    
    return result
