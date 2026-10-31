"""
Data Access Layer for Rawlsing v4.1

Connects to Postgres database to fetch:
- World slices (country/year conditions)
- Driver vectors (WVS parent cohort values) — from microdata when available, else aggregates
- Local modifiers (EPR, ethnic power, etc.)

World slices and driver vectors prefer microdata (respondents + responses) so the
cultural field is sampled from actual respondents; falls back to driver_aggregates
when microdata is missing or no matching respondents.
"""

import json
import math
import os
import random
from pathlib import Path

# Load .env so DATABASE_URL is set when running from CLI/ETL
try:
    from dotenv import load_dotenv
    _root = Path(__file__).resolve().parent.parent
    load_dotenv(_root / ".env")
except ImportError:
    pass

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None  # type: ignore[assignment]
    RealDictCursor = None  # type: ignore[assignment]
from typing import Dict, Any, Optional, Tuple, List
from functools import lru_cache
import numpy as np
# Questionable proxy rules: degrade driver vector verdict when used
_QUESTIONABLE_PROXY_CODES = frozenset({"KP", "SO", "CU", "CF"})
_PACIFIC_ISLAND_CODES = frozenset({"FJ", "WS", "TO", "VU", "SB", "KI", "MH", "NR", "PW", "TV", "NC", "PF", "WF", "NU", "CK", "TK", "NF", "PN"})


def _deterministic_proxy_choice(countries: list[str], target: str, year: int, source: str) -> str:
    import hashlib
    seed_str = f"{target}|{year}|{source}"
    seed = int(hashlib.sha256(seed_str.encode()).hexdigest()[:8], 16)
    idx = seed % len(countries)
    return countries[idx]
try:
    from .country_reference import code_for_system
    from .config_loader import get_config_loader
    from .csv_loaders import (
        iter_item_content_pairs,
        load_content_to_drivers as load_driver_content_map,
    )
    from .driver_field_map import (
        DRIVER_DB_TO_FIELD,
        apply_driver_map_to_target,
        copy_microdata_to_dict,
    )
    from .spec import WorldSlice, DriverVector, LocalModifiers
    from . import survey_routing
except ImportError:
    from config_loader import get_config_loader
    from csv_loaders import (  # type: ignore
        iter_item_content_pairs,
        load_content_to_drivers as load_driver_content_map,
    )
    from driver_field_map import (  # type: ignore
        DRIVER_DB_TO_FIELD,
        apply_driver_map_to_target,
        copy_microdata_to_dict,
    )
    from spec import WorldSlice, DriverVector, LocalModifiers
    import survey_routing  # type: ignore

try:
    from data.final_codebooks.scale_transform_registry import (
        build_item_transform_index,
        build_item_transform_index_by_prefix,
        normalize_item_value,
        normalize_wvs_response,
    )
except ImportError:
    build_item_transform_index = None  # type: ignore[assignment]
    build_item_transform_index_by_prefix = None  # type: ignore[assignment]
    normalize_item_value = None  # type: ignore[assignment]
    normalize_wvs_response = None  # type: ignore[assignment]


# Cache configuration
_CACHE_SIZE = 1000  # LRU cache size


def _get_db_connection():
    """Get Postgres database connection. Prefer DATABASE_URL from env (e.g. .env), else config + PGPASSWORD."""
    if psycopg2 is None:
        return None
    url = os.environ.get("DATABASE_URL")
    if url:
        return psycopg2.connect(url)
    loader = get_config_loader()
    db_config = loader.get("main", "database", {})
    return psycopg2.connect(
        host=db_config.get("host", "localhost"),
        port=int(db_config.get("port", 5432)),
        database=db_config.get("database", "Rawlsing—WVS"),
        user=db_config.get("user", "postgres"),
        password=os.getenv("PGPASSWORD", db_config.get("password", "") or "rocketsauce"),
    )


def _get_gdelt_for_country_year(cur, iso3: str, year: int) -> Optional[Dict[str, Any]]:
    """Get GDELT aggregates for (iso3, year) with resampling. Returns None if not found."""
    for sql, params in [
        ("SELECT * FROM gdelt_country_year WHERE iso3 = %s AND year = %s", (iso3, year)),
        ("SELECT * FROM gdelt_country_year WHERE iso3 = %s AND year BETWEEN %s AND %s ORDER BY ABS(year - %s) LIMIT 1", (iso3, year - 5, year + 5, year)),
        ("SELECT * FROM gdelt_country_year WHERE iso3 = %s ORDER BY year DESC LIMIT 1", (iso3,)),
    ]:
        cur.execute(sql, params)
        row = cur.fetchone()
        if row:
            return dict(row)
    return None


def _map_age_to_age_group(age: int) -> str:
    """Map numeric age to WVS age group bucket."""
    if age < 16:
        return "<16"
    elif age < 25:
        return "16-24"
    elif age < 35:
        return "25-34"
    elif age < 45:
        return "35-44"
    elif age < 55:
        return "45-54"
    elif age < 65:
        return "55-64"
    else:
        return "65+"


def _get_parent_cohort_age_group(age: int) -> str:
    """
    Get parent cohort age group.
    For a child of age X, parents are typically 25-39 years old.
    """
    # Parent cohort is typically 25-39
    return "25-34"  # Most common parent age range


# ---------------------------------------------------------------------------
# Microdata path: driver vectors from respondent-level data (world slices off microdata)
# ---------------------------------------------------------------------------

_ROOT = Path(__file__).resolve().parent.parent
_WVS_DRIVER_SCHEMA_PATH = _ROOT / "enneagrams" / "cross-data" / "driverSchema.json"
_ETL_MANIFEST_PATH = _ROOT / "etl_run_manifest.json"


def _load_wvs_driver_schema_for_microdata() -> Dict[str, List[Tuple[str, float]]]:
    """
    Load driver_name -> [(var_code, weight), ...] for WVS-only proxy vars.
    Skips non-WVS proxies (hofstede.*, gdp_per_capita, etc.) so we can compute from responses.
    """
    out: Dict[str, List[Tuple[str, float]]] = {}
    if not _WVS_DRIVER_SCHEMA_PATH.exists():
        return out
    try:
        with open(_WVS_DRIVER_SCHEMA_PATH, encoding="utf-8") as f:
            schema = json.load(f)
    except Exception:
        return out
    for driver_name, driver_def in schema.items():
        proxies = driver_def.get("proxies") or []
        wvs_proxies: List[Tuple[str, float]] = []
        for p in proxies:
            if isinstance(p, dict):
                var = p.get("variable", "")
                weight = float(p.get("weight", 1.0))
            else:
                var = str(p)
                weight = 1.0
            if not var.startswith("wvs7."):
                continue
            rest = var.split(".", 1)[1]
            var_code = rest if rest.startswith("Q") else f"Q{rest}"
            wvs_proxies.append((var_code, weight))
        if wvs_proxies:
            out[driver_name] = wvs_proxies
    return out


def _normalize_wvs_score(value: Any, var_code: Optional[str] = None) -> Optional[float]:
    """Normalize WVS response value to 0-100 via question metadata."""
    if normalize_wvs_response is None:
        try:
            val = float(value)
            if val != val or val < 0:
                return None
            if val <= 10:
                return max(0.0, min(100.0, (val - 1) / 9.0 * 100.0))
            if val <= 100:
                return max(0.0, min(100.0, val))
            return max(0.0, min(100.0, val / 10.0))
        except (TypeError, ValueError):
            return None
        return normalize_wvs_response(value, var_code or "Q0")


def _load_etl_manifest() -> Dict[str, Any] | None:
    """Load the latest ETL manifest when present."""
    if not _ETL_MANIFEST_PATH.exists():
        return None
    try:
        with open(_ETL_MANIFEST_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _manifest_integrity_for_source(source: str) -> tuple[str, list[str], Dict[str, Any] | None]:
    """
    Derive a lightweight integrity status for a source from etl_run_manifest.json.

    Returns (status, reasons, manifest).
    """
    manifest = _load_etl_manifest()
    if manifest is None:
        return "degraded", ["etl_manifest_missing"], None

    required_steps_by_source = {
        "WVS": ["build_wvs_cube", "aggregate_wvs_drivers_from_cube"],
        "EVS": ["build_evs_aggregates"],
        "Arab Barometer": ["build_arab_barometer_aggregates"],
        "Afrobarometer": ["build_afrobarometer_aggregates"],
        "Latinobarómetro": ["build_latinobarometro_aggregates"],
        "Asian Barometer": ["build_asian_barometer_cube"],
    }
    steps = manifest.get("steps") or []
    step_map: Dict[str, Dict[str, Any]] = {}
    for step in steps:
        if isinstance(step, dict) and step.get("step"):
            step_map[str(step["step"])] = step

    required_steps = required_steps_by_source.get(source, [])
    reasons: list[str] = []
    for step_name in required_steps:
        step = step_map.get(step_name)
        if not step:
            reasons.append(f"missing_step:{step_name}")
            continue
        if str(step.get("status") or "").lower() != "ok":
            reasons.append(f"step_not_ok:{step_name}:{step.get('status')}")

    overall_status = str(manifest.get("overall_status") or "").lower()
    if overall_status and overall_status not in {"ok", "success"}:
        reasons.append(f"manifest_overall:{overall_status}")

    status = "ok" if not reasons else "degraded"
    return status, reasons, manifest


def _resample_survey_year_from_respondents(
    cur, country_code: str, target_year: int, window: int = 5
) -> Optional[int]:
    """Get a survey year from respondents table for this country (exact → nearest → latest)."""
    try:
        cur.execute(
            "SELECT DISTINCT survey_year FROM respondents WHERE country_code = %s AND survey_year = %s LIMIT 1",
            (country_code, target_year),
        )
        r = cur.fetchone()
        if r:
            return int(r[0])
        cur.execute(
            """
            SELECT survey_year FROM (
                SELECT DISTINCT survey_year,
                       ABS(survey_year - %s) AS diff
                FROM respondents
                WHERE country_code = %s AND survey_year IS NOT NULL
                  AND ABS(survey_year - %s) <= %s
            ) sub ORDER BY diff LIMIT 1
            """,
            (target_year, country_code, target_year, window),
        )
        r = cur.fetchone()
        if r:
            return int(r[0])
        cur.execute(
            """
            SELECT survey_year FROM respondents
            WHERE country_code = %s AND survey_year IS NOT NULL
            ORDER BY survey_year DESC LIMIT 1
            """,
            (country_code,),
        )
        r = cur.fetchone()
        if r:
            return int(r[0])
    except Exception:
        pass
    return None


def _get_matching_respondent_ids_simple(
    cur,
    country_code: str,
    survey_year: int,
    age_group: Optional[str] = None,
    gender_code: Optional[str] = None,
    limit: int = 50,
) -> List[int]:
    """
    Simpler version: filter by country, year, optional age_group and sex only.
    respondents table: country_code, survey_year, age, sex.
    """
    params: List[Any] = [country_code, survey_year]
    sql = "SELECT respondent_id FROM respondents WHERE country_code = %s AND survey_year = %s"
    if age_group:
        bounds = _age_group_to_sql_bounds(age_group)
        if bounds:
            sql += " AND age >= %s AND age <= %s"
            params.extend(bounds)
    if gender_code:
        sql += " AND sex = %s"
        params.append(gender_code)
    sql += " ORDER BY RANDOM() LIMIT %s"
    params.append(limit)
    try:
        cur.execute(sql, params)
        return [r[0] for r in cur.fetchall()]
    except Exception:
        return []


# WVS respondents table: country_code, survey_year, sex, age, education_level, income_level, urban_rural, religion_label
BROADEN_ORDER_WVS = ["religion_label", "age", "sex", "education_level", "income_level", "urban_rural"]
_SLICE_SAMPLE_MAX = 200  # max respondents to use when building per-driver distribution (used in walkback default)


def _get_matching_respondent_ids_walkback(
    cur,
    country_code: str,
    survey_year: int,
    min_n: int,
    age_group: Optional[str] = None,
    gender_code: Optional[str] = None,
    education: Optional[Any] = None,
    income: Optional[Any] = None,
    urban_rural: Optional[str] = None,
    religion: Optional[str] = None,
    limit: int = _SLICE_SAMPLE_MAX,
) -> List[int]:
    """
    Get respondent IDs from public.respondents with determinicity walkback.
    Try full slice; if count < min_n, drop lowest-determinicity dimension and retry.
    Returns [] only when country+year has no respondents.
    """
    sex_val = None
    if gender_code:
        sex_val = "M" if str(gender_code) == "1" else "F" if str(gender_code) == "2" else str(gender_code).strip().upper()[:1]
    age_bounds = _age_group_to_sql_bounds(age_group)
    filters: Dict[str, Any] = {}
    if religion is not None and str(religion).strip():
        filters["religion_label"] = str(religion).strip()
    if age_bounds is not None:
        filters["age"] = age_bounds
    if sex_val is not None:
        filters["sex"] = sex_val
    if education is not None:
        try:
            filters["education_level"] = int(float(education))
        except (TypeError, ValueError):
            pass
    if income is not None:
        try:
            filters["income_level"] = int(float(income))
        except (TypeError, ValueError):
            pass
    if urban_rural is not None and str(urban_rural).strip():
        filters["urban_rural"] = str(urban_rural).strip()

    drop_order = [d for d in BROADEN_ORDER_WVS if d in filters]
    for k in range(len(drop_order) + 1):
        dims_dropped = set(drop_order[:k])
        where_parts = ["country_code = %s", "survey_year = %s"]
        params: List[Any] = [country_code, survey_year]
        if "age" in filters and "age" not in dims_dropped:
            lo, hi = filters["age"]
            where_parts.append("age IS NOT NULL AND age >= %s AND age <= %s")
            params.extend([lo, hi])
        if "sex" in filters and "sex" not in dims_dropped:
            where_parts.append("sex = %s")
            params.append(filters["sex"])
        if "education_level" in filters and "education_level" not in dims_dropped:
            where_parts.append("education_level = %s")
            params.append(filters["education_level"])
        if "income_level" in filters and "income_level" not in dims_dropped:
            where_parts.append("income_level = %s")
            params.append(filters["income_level"])
        if "urban_rural" in filters and "urban_rural" not in dims_dropped:
            where_parts.append("urban_rural = %s")
            params.append(filters["urban_rural"])
        if "religion_label" in filters and "religion_label" not in dims_dropped:
            where_parts.append("religion_label = %s")
            params.append(filters["religion_label"])

        try:
            sql = "SELECT respondent_id FROM respondents WHERE " + " AND ".join(where_parts) + " ORDER BY RANDOM() LIMIT %s"
            cur.execute(sql, params + [limit])
            rows = cur.fetchall()
        except Exception:
            continue
        ids = [r[0] for r in rows]
        if len(ids) >= min_n:
            return ids
    # Exhausted: return country+year slice if any
    try:
        cur.execute(
            "SELECT respondent_id FROM respondents WHERE country_code = %s AND survey_year = %s ORDER BY RANDOM() LIMIT %s",
            (country_code, survey_year, limit),
        )
        return [r[0] for r in cur.fetchall()]
    except Exception:
        return []


def _compute_respondent_driver_scores(
    respondent_id: int,
    cur,
    driver_schema: Dict[str, List[Tuple[str, float]]],
) -> Dict[str, float]:
    """For one respondent, fetch responses and compute per-driver mean normalized score (0-100)."""
    var_codes = set()
    for proxies in driver_schema.values():
        for v, _ in proxies:
            var_codes.add(v)
    if not var_codes:
        return {}
    var_list = sorted(var_codes)
    placeholders = ",".join("%s" for _ in var_list)
    cur.execute(
        f"SELECT var_code, value_raw FROM responses WHERE respondent_id = %s AND var_code IN ({placeholders})",
        [respondent_id] + var_list,
    )
    rows = cur.fetchall()
    row_map = {r["var_code"]: r["value_raw"] for r in rows} if rows and hasattr(rows[0], "keys") else {r[0]: r[1] for r in rows}
    out: Dict[str, float] = {}
    for driver_name, proxies in driver_schema.items():
        scores = []
        for var_code, weight in proxies:
            val = row_map.get(var_code)
            norm = _normalize_wvs_score(val, var_code)
            if norm is not None:
                scores.append(norm * weight)
        if scores:
            out[driver_name] = sum(scores) / len(scores)
    return out


# Slice-based sampling (_SLICE_SAMPLE_MAX defined above with BROADEN_ORDER_WVS)
_MIN_STD_FOR_SAMPLING = 5.0  # avoid degenerate when std is 0 or very small

# Determinicity walkback: when slice has too few respondents, drop constraints in this order
# (lowest determinicity first: religion, then age, sex, education, income, urban_rural).
# So we keep most predictive dimensions as long as possible.
BROADEN_ORDER_SURVEY_MICRO = ["religion_label", "age_group", "sex", "education_level", "income_level", "urban_rural"]
MIN_SLICE_RESPONDENTS = 30  # require at least this many in slice before using it


def _age_group_to_sql_bounds(age_group: Optional[str]) -> Optional[Tuple[int, int]]:
    """Return (min_age, max_age) for age_group for SQL BETWEEN; None if no filter."""
    if not age_group:
        return None
    a = (age_group or "").strip()
    if a == "16-24":
        return (16, 24)
    if a == "25-34":
        return (25, 34)
    if a == "35-44":
        return (35, 44)
    if a == "45-54":
        return (45, 54)
    if a == "55-64":
        return (55, 64)
    if a == "65+":
        return (65, 150)
    if a == "<16":
        return (0, 15)
    return None


def _sample_driver_vec_from_slice_distribution(
    per_driver_values: Dict[str, List[float]],
) -> Dict[str, float]:
    """
    From per-driver lists of scores (0–100), sample one value per driver:
    mean and std over the slice, then normal(mean, max(std, MIN_STD)) clipped to [0, 100].
    """
    out: Dict[str, float] = {}
    for driver, vals in per_driver_values.items():
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        if len(vals) == 1:
            out[driver] = max(0.0, min(100.0, mean))
            continue
        variance = sum((x - mean) ** 2 for x in vals) / len(vals)
        std = math.sqrt(variance) if variance > 0 else _MIN_STD_FOR_SAMPLING
        std = max(std, _MIN_STD_FOR_SAMPLING)
        sampled = random.gauss(mean, std)
        out[driver] = max(0.0, min(100.0, sampled))
    return out


def _get_driver_vec_from_wvs_microdata(
    conn,
    cur,
    country_code: str,
    year: int,
    age: int,
    gender_code: Optional[str] = None,
    religion: Optional[str] = None,
    education: Optional[str] = None,
    income: Optional[str] = None,
    urbanicity: Optional[str] = None,
) -> Optional[DriverVector]:
    """
    Build a driver vector from the slice distribution: get matching respondents,
    compute per-driver scores for each, then sample one value per driver from that distribution.
    Returns None if respondents table missing, no matching year, or no matching respondents.
    """
    try:
        cur.execute("SELECT 1 FROM respondents LIMIT 1")
        cur.fetchone()
    except Exception:
        return None
    schema = _load_wvs_driver_schema_for_microdata()
    if not schema:
        return None
    survey_year = _resample_survey_year_from_respondents(cur, country_code, year)
    if survey_year is None:
        return None
    age_group = _map_age_to_age_group(age)
    ids = _get_matching_respondent_ids_walkback(
        cur, country_code, survey_year, MIN_SLICE_RESPONDENTS,
        age_group=age_group, gender_code=gender_code, education=education,
        income=income, urban_rural=urbanicity, religion=religion,
        limit=_SLICE_SAMPLE_MAX,
    )
    if not ids:
        return None
    per_driver_values: Dict[str, List[float]] = {}
    for rid in ids:
        drivers = _compute_respondent_driver_scores(rid, cur, schema)
        for db_name, val in drivers.items():
            per_driver_values.setdefault(db_name, []).append(val)
    drivers = _sample_driver_vec_from_slice_distribution(per_driver_values)
    if not drivers:
        return None
    vec = DriverVector()
    apply_driver_map_to_target(drivers, vec)
    for db_name, val in drivers.items():
        if db_name not in DRIVER_DB_TO_FIELD:
            vec.extra[db_name] = val
    vec.extra["_metadata"] = {
        "source": "WVS",
        "from_microdata": True,
        "slice_based": True,
        "survey_year": survey_year,
        "n_respondents": len(ids),
    }
    return vec


# Survey microdata: source -> item_id prefix for content mapping (wave-specific where applicable)
_SURVEY_MICRODATA_ITEM_PREFIX: Dict[str, str] = {
    "Asian Barometer": "Asian Barometer:W1:",
}


def _get_survey_microdata_prefix(source: str, survey_year: Optional[int] = None) -> Optional[str]:
    """Item prefix for content map; for multi-wave sources use survey_year."""
    if source == "Latinobarómetro":
        return "Latinobarómetro:1995:" if (survey_year and survey_year < 2000) else "Latinobarómetro:2024:"
    if source == "Asian Barometer":
        return "Asian Barometer:W6:" if (survey_year and survey_year >= 2018) else "Asian Barometer:W1:"
    if source == "Arab Barometer":
        return "Arab Barometer:W1:" if (survey_year and survey_year < 2010) else "Arab Barometer:W8:"
    if source == "Afrobarometer":
        return "Afrobarometer:R1:" if (survey_year and survey_year < 2010) else "Afrobarometer:R9:"
    if source == "EVS":
        return "EVS:TREND:"
    return _SURVEY_MICRODATA_ITEM_PREFIX.get(source)


def _load_item_content_for_prefix(prefix: str) -> Dict[str, List[Dict[str, Any]]]:
    """Load var_suffix -> [{content_id, scale_transform_id, review_status, ...}] for items starting with prefix."""
    if build_item_transform_index_by_prefix is None:
        return {}
    return build_item_transform_index_by_prefix(prefix)


def _load_content_to_drivers() -> Dict[str, List[str]]:
    """content_id -> [driver_name] from driver_content_map."""
    return load_driver_content_map(_ROOT / "v2" / "driver_content_map.csv")


def _normalize_survey_val(val: Any, scale_min: float = 1.0, scale_max: float = 4.0) -> Optional[float]:
    """Legacy helper preserved for compatibility; now returns 0-100."""
    try:
        v = float(val)
        if v != v or v < 0 or v >= 90:
            return None
        if scale_min >= scale_max:
            return None
        return max(0.0, min(100.0, ((v - scale_min) / (scale_max - scale_min)) * 100.0))
    except (TypeError, ValueError):
        return None


def _get_survey_year_from_microdata(cur, source: str, country_code: str, year: int) -> Optional[int]:
    """Resample survey_year for (source, country_code): exact → nearest ±5 → latest. None if no rows."""
    try:
        cur.execute(
            "SELECT DISTINCT survey_year FROM survey_microdata_respondents WHERE source = %s AND country_code = %s AND survey_year IS NOT NULL ORDER BY survey_year",
            (source, country_code),
        )
        years = [r["survey_year"] if hasattr(r, "keys") else r[0] for r in cur.fetchall()]
    except Exception:
        return None
    if not years:
        return None
    years = [int(y) for y in years]
    if year in years:
        return year
    nearest = min(years, key=lambda y: abs(y - year))
    if abs(nearest - year) <= 5:
        return nearest
    return max(years)


def _get_survey_microdata_respondent_ids(
    cur, source: str, country_code: str, year: int
) -> Optional[Tuple[int, List[int]]]:
    """Get (survey_year, list of respondent ids) for source/country. Resample year if needed. None if table missing or empty."""
    survey_year = _get_survey_year_from_microdata(cur, source, country_code, year)
    if survey_year is None:
        return None
    try:
        cur.execute(
            "SELECT id FROM survey_microdata_respondents WHERE source = %s AND country_code = %s AND survey_year = %s ORDER BY id",
            (source, country_code, survey_year),
        )
        rows = cur.fetchall()
    except Exception:
        return None
    if not rows:
        return None
    ids = [r["id"] if hasattr(r, "keys") else r[0] for r in rows]
    return (survey_year, ids)


def _get_survey_microdata_respondent_ids_with_walkback(
    cur,
    source: str,
    country_code: str,
    year: int,
    min_n: int,
    gender_code: Optional[str] = None,
    age_group: Optional[str] = None,
    education: Optional[Any] = None,
    income: Optional[Any] = None,
    urban_rural: Optional[str] = None,
    religion: Optional[str] = None,
) -> Optional[Tuple[int, List[int], str]]:
    """
    Get (survey_year, respondent ids, match_level) for source/country with determinicity walkback.
    Try full demographic slice; if count < min_n, drop the lowest-determinicity dimension and retry.
    BROADEN_ORDER: religion_label → age_group → sex → education_level → income_level → urban_rural.
    Returns None only when even country+year has no respondents.
    """
    survey_year = _get_survey_year_from_microdata(cur, source, country_code, year)
    if survey_year is None:
        return None
    # Map to table columns; sex: gender_code "1"=M "2"=F
    sex_val = None
    if gender_code:
        sex_val = "M" if str(gender_code) == "1" else "F" if str(gender_code) == "2" else str(gender_code).strip().upper()[:1]
    age_bounds = _age_group_to_sql_bounds(age_group)
    # Active filters: column -> value (for WHERE)
    filters_active: Dict[str, Any] = {}
    if religion is not None and str(religion).strip():
        filters_active["religion_label"] = str(religion).strip()
    if age_bounds is not None:
        filters_active["age_group"] = age_bounds  # special: age BETWEEN
    if sex_val is not None:
        filters_active["sex"] = sex_val
    if education is not None:
        try:
            filters_active["education_level"] = int(float(education))
        except (TypeError, ValueError):
            pass
    if income is not None:
        try:
            filters_active["income_level"] = int(float(income))
        except (TypeError, ValueError):
            pass
    if urban_rural is not None and str(urban_rural).strip():
        filters_active["urban_rural"] = str(urban_rural).strip()

    # Drop order = lowest determinicity first (only dimensions we have)
    drop_order = [d for d in BROADEN_ORDER_SURVEY_MICRO if d in filters_active]

    for k in range(len(drop_order) + 1):
        dims_dropped = set(drop_order[:k])
        where_parts = ["source = %s", "country_code = %s", "survey_year = %s"]
        params: List[Any] = [source, country_code, survey_year]
        if "age_group" in filters_active and "age_group" not in dims_dropped:
            lo, hi = filters_active["age_group"]
            where_parts.append("age IS NOT NULL AND age >= %s AND age <= %s")
            params.extend([lo, hi])
        if "sex" in filters_active and "sex" not in dims_dropped:
            where_parts.append("sex = %s")
            params.append(filters_active["sex"])
        if "education_level" in filters_active and "education_level" not in dims_dropped:
            where_parts.append("education_level = %s")
            params.append(filters_active["education_level"])
        if "income_level" in filters_active and "income_level" not in dims_dropped:
            where_parts.append("income_level = %s")
            params.append(filters_active["income_level"])
        if "urban_rural" in filters_active and "urban_rural" not in dims_dropped:
            where_parts.append("urban_rural = %s")
            params.append(filters_active["urban_rural"])
        if "religion_label" in filters_active and "religion_label" not in dims_dropped:
            where_parts.append("religion_label = %s")
            params.append(filters_active["religion_label"])

        try:
            sql = "SELECT id FROM survey_microdata_respondents WHERE " + " AND ".join(where_parts)
            cur.execute(sql, params)
            rows = cur.fetchall()
        except Exception:
            continue
        ids = [r["id"] if hasattr(r, "keys") else r[0] for r in rows]
        if len(ids) >= min_n:
            level = "full" if k == 0 else "broadened_" + "_".join(drop_order[:k])
            return (survey_year, ids[: _SLICE_SAMPLE_MAX], level)
    # Exhausted walkback: return country+year slice if any
    try:
        cur.execute(
            "SELECT id FROM survey_microdata_respondents WHERE source = %s AND country_code = %s AND survey_year = %s",
            (source, country_code, survey_year),
        )
        rows = cur.fetchall()
    except Exception:
        return None
    ids = [r["id"] if hasattr(r, "keys") else r[0] for r in rows]
    if not ids:
        return None
    return (survey_year, ids[: _SLICE_SAMPLE_MAX], "country_year_only")


def _compute_driver_scores_from_survey_responses(
    cur, respondent_id: int, item_prefix: str
) -> Dict[str, float]:
    """Compute driver_name -> 0-100 from survey_microdata_responses using item_content_map + driver_content_map."""
    var_to_content = _load_item_content_for_prefix(item_prefix)
    content_to_drivers = _load_content_to_drivers()
    if not var_to_content or not content_to_drivers:
        return {}
    cur.execute(
        "SELECT var_code, value_raw FROM survey_microdata_responses WHERE respondent_id = %s",
        (respondent_id,),
    )
    rows = cur.fetchall()
    row_map = {r["var_code"]: r["value_raw"] for r in rows} if rows and hasattr(rows[0], "keys") else {r[0]: r[1] for r in rows}
    driver_scores: Dict[str, List[float]] = {}
    for var, mappings in var_to_content.items():
        val = row_map.get(var)
        if not isinstance(mappings, list):
            mappings = [mappings]
        for mapping in mappings:
            if not isinstance(mapping, dict):
                continue
            if str(mapping.get("review_status") or "").strip().lower() not in {"reviewed", "verified"}:
                continue
            norm = normalize_item_value(val, mapping)
            if norm is None:
                continue
            content_id = str(mapping.get("content_id") or "").strip()
            for driver in content_to_drivers.get(content_id, []):
                driver_scores.setdefault(driver, []).append(norm)
    out: Dict[str, float] = {}
    for driver, vals in driver_scores.items():
        if vals:
            out[driver] = sum(vals) / len(vals)
    return out


def _get_driver_vec_from_survey_microdata(
    conn,
    cur,
    source: str,
    country_code: str,
    year: int,
    gender_code: Optional[str] = None,
    age_group: Optional[str] = None,
    education: Optional[Any] = None,
    income: Optional[Any] = None,
    urbanicity: Optional[str] = None,
    religion: Optional[str] = None,
) -> Optional[Tuple[Dict[str, float], Dict[str, Any]]]:
    """
    Build (drivers dict, metadata) from survey_microdata_* with determinicity walkback.
    Tries full demographic slice; if too few respondents, drops lowest-determinicity
    dimension and retries until slice has enough or we're at country+year. Returns None
    only when there are no respondents for that source/country.
    """
    res = _get_survey_microdata_respondent_ids_with_walkback(
        cur, source, country_code, year, MIN_SLICE_RESPONDENTS,
        gender_code=gender_code, age_group=age_group, education=education,
        income=income, urban_rural=urbanicity, religion=religion,
    )
    if not res:
        return None
    survey_year, ids, match_level = res
    if not ids:
        return None
    prefix = _get_survey_microdata_prefix(source, survey_year)
    if not prefix:
        return None
    sample_ids = ids if len(ids) <= _SLICE_SAMPLE_MAX else random.sample(ids, _SLICE_SAMPLE_MAX)
    per_driver_values: Dict[str, List[float]] = {}
    for respondent_id in sample_ids:
        one = _compute_driver_scores_from_survey_responses(cur, respondent_id, prefix)
        for driver_name, val in one.items():
            per_driver_values.setdefault(driver_name, []).append(val)
    drivers = _sample_driver_vec_from_slice_distribution(per_driver_values)
    if not drivers:
        return None
    metadata = {
        "source": source,
        "from_microdata": True,
        "slice_based": True,
        "survey_year": survey_year,
        "n_respondents": len(sample_ids),
        "match_level": match_level,
    }
    return (drivers, metadata)


# Source priority when not using survey routing (country not in survey_routing)
DRIVER_SOURCE_PRIORITY = (
    "WVS",
    "EVS",
    "Arab Barometer",
    "Afrobarometer",
    "Latinobarómetro",
    "Asian Barometer",
)

# Item ID prefixes → source name (longest first so "Asian Barometer" before "Asian")
_ITEM_PREFIX_TO_SOURCE = [
    ("Asian Barometer:", "Asian Barometer"),
    ("Arab Barometer:", "Arab Barometer"),
    ("Latinobarómetro:", "Latinobarómetro"),
    ("Afrobarometer:", "Afrobarometer"),
    ("EVS:", "EVS"),
    ("WVS:", "WVS"),
]


def _load_driver_sources_availability() -> Dict[str, set]:
    """driver_name -> set of source names that have at least one item for that driver."""
    content_to_sources: Dict[str, set] = {}
    if build_item_transform_index is not None:
        item_index = build_item_transform_index()
        for item_id, mappings in item_index.items():
            source = None
            for prefix, src in _ITEM_PREFIX_TO_SOURCE:
                if item_id.startswith(prefix):
                    source = src
                    break
            if not source:
                continue
            for mapping in mappings:
                if str(mapping.get("review_status") or "").strip().lower() not in {"reviewed", "verified"}:
                    continue
                content_id = str(mapping.get("content_id") or "").strip()
                if not content_id:
                    continue
                content_to_sources.setdefault(content_id, set()).add(source)
    else:
        for item_id, content_id in iter_item_content_pairs(_ROOT / "data" / "final_codebooks" / "item_content_map.csv"):
            source = None
            for prefix, src in _ITEM_PREFIX_TO_SOURCE:
                if item_id.startswith(prefix):
                    source = src
                    break
            if source:
                if content_id not in content_to_sources:
                    content_to_sources[content_id] = set()
                content_to_sources[content_id].add(source)
    driver_to_sources: Dict[str, set] = {}
    for content_id, drivers in _load_content_to_drivers().items():
        for driver in drivers:
            if driver not in driver_to_sources:
                driver_to_sources[driver] = set()
            driver_to_sources[driver].update(content_to_sources.get(content_id, set()))
    return driver_to_sources


def _resample_survey_year(
    target_year: int,
    country_code: str,
    window: int = 5,
    source: Optional[str] = None,
) -> Optional[int]:
    """
    Resample survey year: exact → nearest neighbor → None.
    If source is given, only consider rows with that source.
    
    Returns:
        Survey year if found, None if no data available
    """
    conn = _get_db_connection()
    cur = conn.cursor()
    try:
        source_clause = " AND source = %s" if source else ""
        source_param = (source,) if source else ()
        base_params = (country_code, str(target_year)) + source_param

        # Try exact year first
        cur.execute(
            """
            SELECT DISTINCT survey_year
            FROM driver_aggregates
            WHERE country_code = %s AND survey_year = %s
            """ + source_clause + """
            LIMIT 1
        """,
            base_params,
        )
        result = cur.fetchone()
        if result:
            return int(result[0])

        # Try nearest neighbor within window
        params = (int(target_year), country_code, int(target_year), window) + source_param
        cur.execute(
            """
            SELECT survey_year
            FROM (
                SELECT DISTINCT survey_year,
                       ABS((survey_year::numeric)::integer - %s) as year_diff
                FROM driver_aggregates
                WHERE country_code = %s
                  AND survey_year IS NOT NULL
                  AND survey_year ~ '^[0-9]+(\.[0-9]+)?$'
                  AND ABS((survey_year::numeric)::integer - %s) <= %s
            """
            + source_clause
            + """
            ) subq
            ORDER BY year_diff
            LIMIT 1
        """,
            params,
        )
        result = cur.fetchone()
        if result:
            return int(float(result[0]))

        # Try any available year for this country
        cur.execute(
            """
            SELECT survey_year
            FROM (
                SELECT DISTINCT survey_year
                FROM driver_aggregates
                WHERE country_code = %s
                  AND survey_year IS NOT NULL
                  AND survey_year ~ '^[0-9]+(\.[0-9]+)?$'
            """
            + source_clause
            + """
            ) subq
            ORDER BY (survey_year::numeric)::integer DESC
            LIMIT 1
        """,
            (country_code,) + source_param,
        )
        result = cur.fetchone()
        if result:
            return int(float(result[0]))
        return None
    finally:
        cur.close()
        conn.close()


def _get_aggregates_for_source_country(
    cur,
    source: str,
    country_code: str,
    year: int,
    filters: Dict[str, Any],
    drop_order: List[str],
    dim_priority: List[str],
) -> Tuple[Dict[str, float], Dict[str, Any]]:
    """Query driver_aggregates for (source, country_code, year) with demo hierarchy. Returns (drivers dict 0-100, metadata)."""
    survey_year = _resample_survey_year(year, country_code, source=source)
    if survey_year is None:
        return {}, {}
    where_clauses = ["country_code = %s", "(survey_year::numeric)::integer = %s", "source = %s"]
    params_base = [country_code, int(survey_year), source]
    queries = []
    seen_levels = set()
    for k in range(len(drop_order) + 1):
        dims_active = set(filters.keys())
        for d in drop_order[:k]:
            dims_active.discard(d)
        if not dims_active:
            continue
        params = list(params_base)
        wc = list(where_clauses)
        for dim in dim_priority:
            if dim in dims_active and filters.get(dim) is not None:
                wc.append(f"{dim} = %s")
                params.append(filters[dim])
        level_key = "country+year+" + "+".join(d for d in dim_priority if d in dims_active)
        if level_key in seen_levels:
            continue
        seen_levels.add(level_key)
        queries.append({
            "sql": (
                "SELECT driver_name, AVG(mean_score) as score, SUM(sample_size) as n, "
                "MIN(mapping_version) as mapping_version, MIN(normalizer_version) as normalizer_version, "
                "MIN(question_metadata_version) as question_metadata_version, MIN(source_path) as source_path "
                "FROM driver_aggregates WHERE " + " AND ".join(wc) + " GROUP BY driver_name"
            ),
            "params": tuple(params),
            "level": level_key,
        })
    queries.append({
        "sql": (
            "SELECT driver_name, AVG(mean_score) as score, SUM(sample_size) as n, "
            "MIN(mapping_version) as mapping_version, MIN(normalizer_version) as normalizer_version, "
            "MIN(question_metadata_version) as question_metadata_version, MIN(source_path) as source_path "
            "FROM driver_aggregates WHERE country_code = %s AND (survey_year::numeric)::integer = %s AND source = %s GROUP BY driver_name"
        ),
        "params": (country_code, int(survey_year), source),
        "level": "country+year",
    })
    queries.append({
        "sql": (
            "SELECT driver_name, AVG(mean_score) as score, SUM(sample_size) as n, "
            "MIN(mapping_version) as mapping_version, MIN(normalizer_version) as normalizer_version, "
            "MIN(question_metadata_version) as question_metadata_version, MIN(source_path) as source_path "
            "FROM driver_aggregates WHERE country_code = %s AND source = %s GROUP BY driver_name"
        ),
        "params": (country_code, source),
        "level": "country",
    })
    for q in queries:
        try:
            cur.execute(q["sql"], q["params"])
            rows = cur.fetchall()
            if rows:
                drivers = {r["driver_name"]: float(r["score"]) for r in rows}
                metadata = {
                    "match_level": q["level"],
                    "survey_year": survey_year,
                    "sample_size": sum(int(r["n"]) for r in rows),
                    "source": source,
                    "mapping_version": rows[0].get("mapping_version") if hasattr(rows[0], "get") else None,
                    "normalizer_version": rows[0].get("normalizer_version") if hasattr(rows[0], "get") else None,
                    "question_metadata_version": rows[0].get("question_metadata_version") if hasattr(rows[0], "get") else None,
                    "source_path": rows[0].get("source_path") if hasattr(rows[0], "get") else None,
                }
                return drivers, metadata
        except Exception:
            continue
    return {}, {}


def list_wvs_countries() -> list:
    """
    Return country_code values that have WVS driver data (source='WVS').
    Use when you need only the WVS survey pool.
    """
    try:
        conn = _get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT DISTINCT country_code
                FROM driver_aggregates
                WHERE source = 'WVS' AND country_code IS NOT NULL AND country_code != ''
                ORDER BY country_code
            """)
            return [row[0] for row in cur.fetchall()]
        finally:
            cur.close()
            conn.close()
    except Exception:
        return []


def list_survey_countries() -> list:
    """
    Return country_code values that have any driver data (WVS, EVS, barometers).
    Use for sampling persona location from the full survey pool.
    """
    try:
        conn = _get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT DISTINCT country_code
                FROM driver_aggregates
                WHERE country_code IS NOT NULL AND country_code != ''
                ORDER BY country_code
            """)
            return [row[0] for row in cur.fetchall()]
        finally:
            cur.close()
            conn.close()
    except Exception:
        return []


def get_driver_vec(
    country_code: str,
    year: int,
    age: int,
    gender: Optional[str] = None,
    religion: Optional[str] = None,
    education: Optional[str] = None,
    income: Optional[str] = None,
    urbanicity: Optional[str] = None
) -> DriverVector:
    """
    Get driver vector for a country/year/cohort. Source is determined by survey routing:
    the survey that covers this country (WVS, EVS, Afrobarometer, Arab Barometer,
    Asian Barometer, Latinobarómetro) or proxy countries when the country is not in any survey.
    
    - WVS countries: use WVS microdata with determinicity walkback (drop lowest-determinicity
      dimensions until slice has enough respondents); only if walkback exhausted → aggregates.
    - EVS/barometer countries: use survey microdata with same walkback; only if exhausted → aggregates.
    - Proxy countries (e.g. Saudi → Arab Barometer, draw from Kuwait): map to that source’s
      countries, then run walkback on the drawn country; only if still no respondents → aggregates.
    - For drivers that the primary source does not measure (content coverage gap), values
      are filled from WVS using the closest approximable WVS countries (see survey_routing
      WVS_APPROXIMATION_COUNTRIES).
    
    Resampling: exact survey_year → nearest ±5 years → most recent.
    """
    conn = _get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        age_group = _map_age_to_age_group(age)
        gender_code = "1" if gender == "male" else "2" if gender == "female" else None if not gender else None
        drop_order = ["religion", "age_group", "gender", "education", "income", "urbanicity"]
        dim_priority = ["urbanicity", "income", "education", "gender", "age_group", "religion"]
        filters = {
            "urbanicity": urbanicity,
            "income": income,
            "education": education,
            "gender": gender_code,
            "age_group": age_group,
            "religion": religion,
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        drivers: Dict[str, float] = {}
        metadata: Dict[str, Any] = {}
        source_country = country_code

        # 1) Survey routing: use the source that covers this country (or proxy countries)
        routing = survey_routing.survey_for(country_code)
        if routing:
            source = routing["source"]
            countries = routing["countries"]
            draw_country = _deterministic_proxy_choice(countries, country_code, year, source) if countries else country_code
            source_country = draw_country
            # Primary vector from that source (microdata for WVS when available, else aggregates)
            if source == "WVS":
                vec_micro = _get_driver_vec_from_wvs_microdata(
                    conn, cur, draw_country, year, age,
                    gender_code=gender_code,
                    religion=religion,
                    education=education,
                    income=income,
                    urbanicity=urbanicity,
                )
                if vec_micro is not None:
                    # Copy to drivers dict using canonical driver field map
                    drivers.update(copy_microdata_to_dict(vec_micro))
                    for k, v in (vec_micro.extra or {}).items():
                        if k != "_metadata" and isinstance(v, (int, float)):
                            drivers[k] = float(v)
                    metadata = (vec_micro.extra or {}).get("_metadata") or {}
                else:
                    drivers, metadata = _get_aggregates_for_source_country(cur, source, draw_country, year, filters, drop_order, dim_priority)
            else:
                # EVS / barometers: try survey_microdata with determinicity walkback
                micro = _get_driver_vec_from_survey_microdata(
                    conn, cur, source, draw_country, year,
                    gender_code=gender_code, age_group=age_group, education=education,
                    income=income, urbanicity=urbanicity, religion=religion,
                )
                if micro is not None:
                    drivers, metadata = micro
                else:
                    drivers, metadata = _get_aggregates_for_source_country(cur, source, draw_country, year, filters, drop_order, dim_priority)

            # 2) Per-driver WVS fill: for drivers the primary source doesn't have, use WVS (closest approximable countries)
            driver_sources = _load_driver_sources_availability()
            primary_has = set(drivers.keys())
            missing = [d for d in driver_sources if d not in primary_has]
            if missing:
                wvs_fill_countries = survey_routing.wvs_approximation_countries_for(country_code) if source != "WVS" else [draw_country]
                if not wvs_fill_countries:
                    wvs_fill_countries = [draw_country] if source == "WVS" else list(survey_routing.WVS_COUNTRIES)[:5]
                fill_country = _deterministic_proxy_choice(wvs_fill_countries, country_code, year, "WVS") if wvs_fill_countries else None
                if fill_country:
                    wvs_fill, _ = _get_aggregates_for_source_country(cur, "WVS", fill_country, year, filters, drop_order, dim_priority)
                    for d in missing:
                        if d in wvs_fill:
                            drivers[d] = wvs_fill[d]
                    if wvs_fill and metadata.get("source") != "WVS":
                        metadata["wvs_fill_drivers"] = [d for d in missing if d in wvs_fill]
                        metadata["wvs_fill_country"] = fill_country
        else:
            # No survey routing: try sources by priority for this country (legacy)
            for source in DRIVER_SOURCE_PRIORITY:
                drivers, metadata = _get_aggregates_for_source_country(cur, source, country_code, year, filters, drop_order, dim_priority)
                if drivers:
                    break
                # Fallback: try WVS microdata for this country
                if source == "WVS":
                    vec_micro = _get_driver_vec_from_wvs_microdata(
                        conn, cur, country_code, year, age,
                        gender_code=gender_code,
                        religion=religion,
                        education=education,
                        income=income,
                        urbanicity=urbanicity,
                    )
                    if vec_micro is not None:
                        drivers.update(copy_microdata_to_dict(vec_micro))
                        for k, v in (vec_micro.extra or {}).items():
                            if k != "_metadata" and isinstance(v, (int, float)):
                                drivers[k] = float(v)
                        metadata = (vec_micro.extra or {}).get("_metadata") or {}
                    break

        if not drivers:
            driver_vec = DriverVector(is_default_fallback=True)
            driver_vec.extra["_integrity"] = {"status": "degraded", "reasons": ["no_data_available"], "target_country": country_code, "source_country": country_code, "confidence": 0.0}
            return driver_vec

        # Convert DB driver names to DriverVector fields via canonical driver map
        vec = DriverVector()
        apply_driver_map_to_target(drivers, vec)
        for k, v in drivers.items():
            vec.extra[k] = float(v) if isinstance(v, (int, float)) else 0.0
        # Build integrity metadata
        meta = dict(metadata)
        meta["source_country"] = source_country
        meta["survey_year"] = metadata.get("survey_year")
        meta["sample_size"] = metadata.get("sample_size")
        meta["match_level"] = metadata.get("match_level")
        vec.extra["_metadata"] = meta
        integrity_status = "ok"
        integrity_reasons: list[str] = []
        if source_country != country_code:
            integrity_status = "degraded"
            integrity_reasons.append(f"proxy_country:{source_country}")
            vec.is_default_fallback = True
        if meta.get("wvs_fill_country"):
            integrity_status = "degraded"
            integrity_reasons.append("wvs_fill")
        if country_code in _QUESTIONABLE_PROXY_CODES or (
            country_code in _PACIFIC_ISLAND_CODES and source == "WVS"
        ):
            integrity_status = "degraded"
            integrity_reasons.append("questionable_proxy")
            vec.is_default_fallback = True
        vec.extra["_integrity"] = {
            "status": integrity_status,
            "reasons": integrity_reasons,
            "target_country": country_code,
            "source_country": source_country,
            "confidence": 100.0 if integrity_status == "ok" else 60.0,
        }
        return vec
        
    finally:
        cur.close()
        conn.close()


def aggregate_parent_driver_vectors(
    parent1_vec: DriverVector,
    parent2_vec: DriverVector
) -> DriverVector:
    """
    Average two parent driver vectors for household-level cultural field.
    Used when both parents contribute to the child's upbringing context.
    """
    averaged = DriverVector()
    missing_fields: List[str] = []
    for fname in DriverVector.__dataclass_fields__:
        if fname == "extra":
            # Merge extras, average _metadata if present
            extra = dict(parent1_vec.extra or {})
            for k, v in (parent2_vec.extra or {}).items():
                if k == "_metadata":
                    continue
                extra[k] = v
            averaged.extra = extra
            continue
        val1 = getattr(parent1_vec, fname)
        val2 = getattr(parent2_vec, fname)
        if val1 is None or val2 is None:
            missing_fields.append(fname)
        v1 = float(val1) if val1 is not None else 50.0
        v2 = float(val2) if val2 is not None else 50.0
        setattr(averaged, fname, (v1 + v2) / 2.0)
    averaged.extra["_integrity"] = {
        "status": "degraded" if missing_fields else "ok",
        "default_value_used": bool(missing_fields),
        "missing_fields": missing_fields,
        "confidence": 100.0 if not missing_fields else 75.0,
    }
    return averaged


# GDP raw (e.g. USD) → normalized 0-100 for WorldSlice (log scale)
_GDP_LOG_MAX = math.log10(1.0 + 150000.0)  # ~5.18; 150k USD/PPP as upper anchor


def _normalize_gdp_to_0_100(raw_gdp: Optional[float]) -> float:
    """Map raw GDP per capita to 0-100. None/missing → 50."""
    if raw_gdp is None or raw_gdp <= 0:
        return 50.0
    log_gdp = math.log10(1.0 + float(raw_gdp))
    return min(100.0, max(0.0, (log_gdp / _GDP_LOG_MAX) * 100.0))


_ws_cache: dict[tuple[str, int], WorldSlice] = {}
_WS_CACHE_MAX = _CACHE_SIZE


def get_world_slice(country_code: str, year: int) -> WorldSlice:
    cache_key = (str(country_code).strip().upper(), year)
    if cache_key in _ws_cache:
        return _ws_cache[cache_key]
    result = _get_world_slice_inner(country_code, year)
    # Only cache real DB results, not default fallbacks
    if not (result.metadata or {}).get("is_default_fallback"):
        if len(_ws_cache) >= _WS_CACHE_MAX:
            _ws_cache.pop(next(iter(_ws_cache)))
        _ws_cache[cache_key] = result
    return result


def _get_world_slice_inner(country_code: str, year: int) -> WorldSlice:
    iso3 = code_for_system(country_code, "iso3")

    try:
        conn = _get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
    except Exception:
        return _default_world_slice(country_code, year)

    try:
        # 1) Exact year
        cur.execute(
            """
            SELECT *
            FROM world_state
            WHERE iso3 = %s AND year = %s
            LIMIT 1
            """,
            (iso3, year),
        )
        row = cur.fetchone()

        # 2) Nearest neighbor within ±5 years
        if not row:
            cur.execute(
                """
                SELECT *
                FROM world_state
                WHERE iso3 = %s
                  AND year BETWEEN %s AND %s
                ORDER BY ABS(year - %s)
                LIMIT 1
                """,
                (iso3, year - 5, year + 5, year),
            )
            row = cur.fetchone()

        # 3) Era fallback: most recent available year
        if not row:
            cur.execute(
                """
                SELECT *
                FROM world_state
                WHERE iso3 = %s
                ORDER BY year DESC
                LIMIT 1
                """,
                (iso3,),
            )
            row = cur.fetchone()

        if row:
            gdp_raw = float(row["gdp_per_capita"]) if row.get("gdp_per_capita") is not None else None
            gdp_pc = _normalize_gdp_to_0_100(gdp_raw)
            unemployment = float(row["unemployment_rate"]) if row.get("unemployment_rate") is not None else 0.0
            internet = float(row["internet_users_pct"]) if row.get("internet_users_pct") is not None else 0.0
            gini = float(row["gini_index"]) if row.get("gini_index") is not None else 50.0
            repression = float(row["state_repression"]) if row.get("state_repression") is not None else 0.0
            conflict = float(row["conflict_intensity"]) if row.get("conflict_intensity") is not None else 0.0
            welfare = float(row["welfare_support"]) if row.get("welfare_support") is not None else 50.0
            propaganda = float(row["propaganda_saturation"]) if row.get("propaganda_saturation") is not None else 0.0

            # GDELT: blend protest/violence into conflict_intensity + derive political/diplomatic texture
            policy_turb = regime_inst = dip_coop = mil_post = dip_isol = 0.0
            media_val = 50.0  # default neutral
            scrutiny = 0.0
            rhetoric = 0.0
            try:
                gdelt_row = _get_gdelt_for_country_year(cur, iso3, year)
                if gdelt_row:
                    def _g(n): return int(gdelt_row.get(n) or 0)
                    if (_g("n_protest") + _g("n_violence")) > 0:
                        n = _g("n_protest") + _g("n_violence")
                        gdelt_contribution = min(100.0, max(0.0, (math.log1p(n) / math.log1p(10000.0)) * 100.0))
                        conflict = max(conflict, gdelt_contribution)
                    # GDELT-derived 0-100 scales (log1p normalized)
                    scale_100k = math.log1p(100000.0)
                    scale_10k = math.log1p(10000.0)
                    scale_1k = math.log1p(1000.0)
                    policy_turb = min(100.0, (math.log1p(_g("n_demand") + _g("n_reject") + _g("n_threaten") + _g("n_disapprove")) / scale_100k) * 100.0)
                    regime_inst = min(100.0, (math.log1p(_g("n_yield")) / scale_1k) * 100.0)
                    dip_coop = min(100.0, (math.log1p(_g("n_cooperation") + _g("n_agree")) / scale_100k) * 100.0)
                    mil_post = min(100.0, (math.log1p(_g("n_military_posture")) / scale_10k) * 100.0)
                    dip_isol = min(100.0, (math.log1p(_g("n_reduce_relations")) / scale_1k) * 100.0)
                    # media_valence: avg_tone -100..+100 → 0..100 (50=neutral)
                    t = gdelt_row.get("avg_tone")
                    if t is not None:
                        try:
                            tv = float(t)
                            media_val = min(100.0, max(0.0, (tv + 100.0) / 2.0))
                        except (TypeError, ValueError):
                            pass
                    scrutiny = min(100.0, (math.log1p(_g("n_investigate")) / scale_10k) * 100.0)
                    rhetoric = min(100.0, (math.log1p(_g("n_public_statement")) / scale_100k) * 100.0)
            except Exception:
                pass  # Table may not exist; ignore

            return WorldSlice(
                year=year,
                country_code=country_code,
                gdp_per_capita=gdp_pc,
                inequality_index=gini,
                conflict_intensity=conflict,
                unemployment_level=unemployment,
                media_saturation=internet,
                propaganda_saturation=propaganda,
                state_repression=repression,
                welfare_support=welfare,
                policy_turbulence=policy_turb,
                regime_instability=regime_inst,
                diplomatic_cooperation=dip_coop,
                military_posture=mil_post,
                diplomatic_isolation=dip_isol,
                media_valence=media_val,
                scrutiny_level=scrutiny,
                rhetoric_saturation=rhetoric,
                metadata={
                    "resampling_method": "world_state",
                    "source_iso3": iso3,
                    "world_state_year": int(row["year"]),
                    "life_expectancy": float(row["life_expectancy"]) if row.get("life_expectancy") is not None else None,
                    "infant_mortality_per_1000": float(row["infant_mortality_per_1000"]) if row.get("infant_mortality_per_1000") is not None else None,
                    "gender_inequality_index": float(row["gender_inequality_index"]) if row.get("gender_inequality_index") is not None else None,
                    "adult_literacy_pct": float(row["adult_literacy_pct"]) if row.get("adult_literacy_pct") is not None else None,
                    "urban_pct": float(row["urban_pct"]) if row.get("urban_pct") is not None else None,
                    "mean_years_schooling": float(row["mean_years_schooling"]) if row.get("mean_years_schooling") is not None else None,
                    "employment_agriculture_pct": float(row["employment_agriculture_pct"]) if row.get("employment_agriculture_pct") is not None else None,
                },
            )

    except Exception:
        return _default_world_slice(country_code, year)
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

    return _default_world_slice(country_code, year)


def _default_world_slice(country_code: str, year: int) -> WorldSlice:
    """Return default WorldSlice when world_state has no data or DB unavailable."""
    return WorldSlice(
        year=year,
        country_code=country_code,
        gdp_per_capita=50.0,
        inequality_index=50.0,
        conflict_intensity=0.0,
        unemployment_level=0.0,
        media_saturation=0.0,
        propaganda_saturation=0.0,
        state_repression=0.0,
        welfare_support=50.0,
        policy_turbulence=0.0,
        regime_instability=0.0,
        diplomatic_cooperation=0.0,
        military_posture=0.0,
        diplomatic_isolation=0.0,
        media_valence=50.0,
        scrutiny_level=0.0,
        rhetoric_saturation=0.0,
        metadata={
            "resampling_method": "default",
            "note": "No world_state row found or DB unavailable",
            "is_default_fallback": True,
        },
    )


def get_local_modifiers(
    identity: Any,  # IdentitySkeleton
    year: int
) -> LocalModifiers:
    """
    Get local modifiers for identity/year.
    
    Uses EPR-2021 for ethnic power status when identity has ethnicity_label.
    """
    try:
        from .epr_lookup import get_epr_status, epr_status_to_ethnic_power
    except ImportError:
        from epr_lookup import get_epr_status, epr_status_to_ethnic_power

    country = getattr(identity, "country_code", None) or ""
    ethnicity = getattr(identity, "ethnicity_label", None) or ""

    epr_status = None
    ethnic_power = "dominant"
    if country and ethnicity:
        epr_status = get_epr_status(country, year, ethnicity)
        ethnic_power = epr_status_to_ethnic_power(epr_status)
    else:
        ethnic_power = "minoritized" if getattr(identity, "minority_status", None) == "minoritized" else "dominant"

    return LocalModifiers(
        ethnic_power_status=ethnic_power,
        epr_power_status=epr_status,
        religion_status="majority",  # TODO: Lookup from database
        urban_rural="rural" if getattr(identity, "urbanicity", None) == "rural" else
                    ("urban" if getattr(identity, "urbanicity", None) in ["city", "megacity"] else "peri_urban"),
        class_position={
            "underclass": 1,
            "working": 3,
            "lower_middle": 5,
            "middle": 6,
            "upper_middle": 8,
            "elite": 10
        }.get(getattr(identity, "current_class", None), 5)
    )
