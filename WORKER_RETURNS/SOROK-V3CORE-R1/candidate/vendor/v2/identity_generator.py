"""
Identity Generator for Rawlsing v4.1

Builds comprehensive identity context before querying WVS:
1. Location (country → region → city) from geonames
2. SES decile (probabilistic) from WID/CIA data
3. Ethnic group from EPR/GeoEPR
4. Religion from people_groups
5. Language from people_groups
6. THEN queries WVS with all demographics

This ensures WVS queries are specific to the actual demographic context.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any, Optional, Tuple
import numpy as np
import random
try:
    from .config_loader import get_config_loader
    from .country_reference import code_for_system, normalize_country_ref, require_country_ref
    from .spec import IdentitySkeleton, DriverVector, COUNTRY_DEFAULT_LABELS, _DEFAULT_LABEL_FALLBACK
    from .data_access import get_driver_vec, _get_db_connection
    from . import query_persona_slice as _qp
except ImportError:
    from config_loader import get_config_loader
    from country_reference import code_for_system, normalize_country_ref, require_country_ref
    from spec import IdentitySkeleton, DriverVector, COUNTRY_DEFAULT_LABELS, _DEFAULT_LABEL_FALLBACK
    from data_access import get_driver_vec, _get_db_connection
    import query_persona_slice as _qp


def _slice_country_for_survey(persona_country_code: str) -> str:
    """
    Return 3-letter country code to use for parent slice (education/religion distributions).
    For WVS countries: use persona country. For non-WVS (EVS, barometers): use a WVS proxy
    from survey_routing so we slice from WVS respondent data (supplement-routed).
    """
    code3 = code_for_system(persona_country_code, "iso3")
    if not code3:
        return persona_country_code
    try:
        from . import survey_routing
    except ImportError:
        import survey_routing
    iso2 = code_for_system(code3, "geonames")
    routing = survey_routing.survey_for(iso2)
    if not routing or routing.get("source") == "WVS":
        return code3
    wvs_proxies = survey_routing.wvs_approximation_countries_for(iso2)
    if not wvs_proxies:
        countries = routing.get("countries") or []
        wvs_proxies = [c for c in countries if c in survey_routing.WVS_COUNTRIES][:5]
    if not wvs_proxies:
        return code3
    proxy_iso2 = random.choice(wvs_proxies)
    return code_for_system(proxy_iso2, "iso3")


def _get_country_name_from_code(country_code: str) -> Optional[str]:
    """
    Get country name from country code (for EPR lookup).
    
    Uses GDL data as source of truth for country names, then maps to EPR statenames.
    """
    conn = _get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            SELECT DISTINCT country
            FROM gdl.subnational_hdi
            WHERE isocode3 = %s
            LIMIT 1
        """, (country_code,))
        
        row = cur.fetchone()
        if row and row["country"]:
            gdl_name = str(row["country"])
            
            # Map GDL country names to EPR statenames
            # (EPR uses different names for some countries)
            try:
                from .data_access import _load_gdl_to_epr_mapping as _get_gdl_epr
            except ImportError:
                def _get_gdl_epr() -> dict:
                    try:
                        import yaml
                        from pathlib import Path as _P
                        _p = _P(__file__).resolve().parent / "gdl_to_epr_mapping.yaml"
                        with open(_p, encoding="utf-8") as _f:
                            return yaml.safe_load(_f) or {}
                    except Exception:
                        return {}
            gdl_to_epr_mapping = _get_gdl_epr()
            
            # Return mapped name if exists, otherwise return GDL name
            return gdl_to_epr_mapping.get(gdl_name, gdl_name)
        
        return None
    except Exception:
        return None
    finally:
        cur.close()
        conn.close()


def sample_location(
    country_code: str,
    year: int
) -> Dict[str, Any]:
    """
    Sample location: country → region → city from geonames.
    
    Uses current/present geonames data for all years (geographic structure
    is relatively stable, and we don't have historical geonames for all years).
    
    Returns:
        {
            "country_code": str,
            "region": {"admin1_code": str, "admin1_name": str, ...},
            "city": {"name": str, "population": int, "feature_code": str, ...},
            "urbanicity": "rural" | "town" | "city" | "megacity"
        }
    """
    conn = _get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Map country code for geonames (IDN -> ID, etc.) through the central resolver.
    geo_country_code = code_for_system(country_code, "geonames")
    
    try:
        # Sample region (weighted by population)
        cur.execute("""
            SELECT admin1_code, admin1_name, population
            FROM geo.admin_regions
            WHERE country_code = %s
              AND population IS NOT NULL
            ORDER BY RANDOM() * population DESC
            LIMIT 1
        """, (geo_country_code,))
        
        region_row = cur.fetchone()
        if not region_row:
            # No region data - return basic structure
            return {
                "country_code": country_code,
                "region": None,
                "city": None,
                "urbanicity": "rural",
                "_provenance": {
                    "source_family": "geonames",
                    "geo_country_code_used": geo_country_code,
                    "region_found": False,
                    "city_found": False,
                    "fallback_used": True,
                    "fallback_reason": "no_region_data_for_country",
                },
            }
        
        region = {
            "admin1_code": region_row["admin1_code"],
            "admin1_name": region_row["admin1_name"]
        }
        
        # Sample city within region (weighted by population)
        cur.execute("""
            SELECT name, population, feature_code
            FROM geo.admin_cities
            WHERE country_code = %s 
              AND admin1_code = %s
              AND population IS NOT NULL
            ORDER BY RANDOM() * population DESC
            LIMIT 1
        """, (geo_country_code, region["admin1_code"]))
        
        city_row = cur.fetchone()
        if city_row:
            city = {
                "name": city_row["name"],
                "population": int(city_row["population"]) if city_row["population"] else None,
                "feature_code": city_row["feature_code"]
            }
            # Determine urbanicity
            if city["population"]:
                if city["population"] > 10000000:
                    urbanicity = "megacity"
                elif city["population"] > 1000000:
                    urbanicity = "city"
                elif city["population"] > 100000:
                    urbanicity = "town"
                else:
                    urbanicity = "rural"
            else:
                urbanicity = "rural"
        else:
            city = None
            urbanicity = "rural"
        
        return {
            "country_code": country_code,
            "region": region,
            "city": city,
            "urbanicity": urbanicity,
            "_provenance": {
                "source_family": "geonames",
                "geo_country_code_used": geo_country_code,
                "region_found": True,
                "city_found": city is not None,
                "fallback_used": False,
            },
        }
        
    finally:
        cur.close()
        conn.close()


# SINGLE SOURCE OF TRUTH: Region name translation dictionary
# Maps GeoNames region names to GDL region names
# Stored in region_name_translations.yaml — loaded at module level.
try:
    import yaml as _yaml_ig
    from pathlib import Path as _P_ig
    _RTP = _P_ig(__file__).resolve().parent / "region_name_translations.yaml"
    with open(_RTP, encoding="utf-8") as _f:
        _REGION_NAME_TRANSLATIONS = _yaml_ig.safe_load(_f) or {}
except Exception:
    _REGION_NAME_TRANSLATIONS = {}


def map_region_to_gdlcode(
    country_code: str,
    region_code: Optional[str] = None,
    region_name: Optional[str] = None
) -> Optional[str]:
    """
    Map GeoNames region to GDL gdlcode.
    
    GDL codes follow pattern:
    - National: {country_code}t (e.g., IDNt)
    - Subnational: {country_code}r{number} (e.g., IDNr101)
    
    Args:
        country_code: ISO 3-letter country code
        region_code: GeoNames admin1_code (optional)
        region_name: GeoNames admin1_name (optional)
    
    Returns:
        GDL gdlcode (e.g., "IDNr101") or None if not found
        
    Strategy:
    1. If no region_code/region_name → return national code ({country_code}t)
    2. Try translation using _REGION_NAME_TRANSLATIONS dictionary
    3. Try exact match on region name
    4. Try fuzzy match (contains, starts with)
    5. Try matching with normalized names (remove "Provinsi", "Province", etc.)
    6. Fallback to None
    """
    if not region_code and not region_name:
        # National level
        return f"{country_code}t"
    
    conn = _get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Normalize region name for matching
        normalized_name = None
        if region_name:
            # Remove common prefixes/suffixes (expanded list)
            # IMPORTANT: Order matters - longer prefixes first (e.g., "Estado de" before "Estado")
            normalized_name = region_name
            prefixes_to_remove = [
                "Daerah Khusus Ibukota", "Daerah Khusus", "Daerah Istimewa", "Daerah",
                "Estado de", "Estado", "State of", "State",
                "Provinsi", "Province", "Propinsi", 
                "Changwat", "Tỉnh", "Tinh", "Muḩāfaz̧at",
                "Kepulauan", "Nanggroe", "Darussalam", "Ibukota",
                "Oblast", "Respublika", "Krai", "Okrug", "Autonomous", "Region",
                "Ken", "-ken", "Prefecture", "Governorate", "Muhafazat"
            ]
            # Process in order (longer prefixes first)
            for prefix in prefixes_to_remove:
                if normalized_name.startswith(prefix):
                    normalized_name = normalized_name.replace(prefix, "", 1).strip()
                # Also try if it's anywhere in the name (for cases like "Free and Hanseatic City of Hamburg")
                normalized_name = normalized_name.replace(prefix + " ", "").replace(" " + prefix, "")
            
            # Normalize special characters (e.g., São -> Sao, ã -> a)
            import unicodedata
            normalized_name = unicodedata.normalize('NFD', normalized_name)
            normalized_name = ''.join(c for c in normalized_name if unicodedata.category(c) != 'Mn')
            
            # Remove common suffixes
            suffixes_to_remove = ["Province", "Provinsi", "Propinsi", "Region", "State", "Oblast"]
            for suffix in suffixes_to_remove:
                if normalized_name.endswith(suffix):
                    normalized_name = normalized_name.replace(suffix, "", 1).strip()
            
            # Clean up extra spaces
            normalized_name = " ".join(normalized_name.split())
            
            # Try translation for normalized_name using SINGLE translation dictionary
            if normalized_name in _REGION_NAME_TRANSLATIONS:
                normalized_name = _REGION_NAME_TRANSLATIONS[normalized_name]
            elif region_name in _REGION_NAME_TRANSLATIONS:
                normalized_name = _REGION_NAME_TRANSLATIONS[region_name]
        
        # Get translated name using the SAME translation dictionary
        # Check both original region_name and normalized_name
        translated_name = None
        if region_name:
            translated_name = (
                _REGION_NAME_TRANSLATIONS.get(region_name) or 
                (_REGION_NAME_TRANSLATIONS.get(normalized_name) if normalized_name else None)
            )
        
        # Try multiple matching strategies
        queries = []
        
        if region_name:
            # Strategy 1: Exact match
            queries.append(("""
                SELECT DISTINCT gdlcode, region
                FROM gdl.subnational_hdi
                WHERE isocode3 = %s
                  AND level = 'Subnat'
                  AND region = %s
                LIMIT 1
            """, (country_code, region_name)))
            
            # Strategy 2: Translated name match (if available)
            if translated_name:
                queries.append(("""
                    SELECT DISTINCT gdlcode, region
                    FROM gdl.subnational_hdi
                    WHERE isocode3 = %s
                      AND level = 'Subnat'
                      AND region = %s
                    LIMIT 1
                """, (country_code, translated_name)))
            
            # Strategy 3: Case-insensitive exact match
            queries.append(("""
                SELECT DISTINCT gdlcode, region
                FROM gdl.subnational_hdi
                WHERE isocode3 = %s
                  AND level = 'Subnat'
                  AND region ILIKE %s
                LIMIT 1
            """, (country_code, region_name)))
            
            # Strategy 4: Contains match (both directions)
            # Also normalize GDL region names for comparison
            queries.append(("""
                SELECT DISTINCT gdlcode, region,
                    CASE 
                        WHEN region = %s THEN 1
                        WHEN region ILIKE %s THEN 2
                        WHEN region ILIKE %s THEN 3
                        ELSE 4
                    END as match_priority
                FROM gdl.subnational_hdi
                WHERE isocode3 = %s
                  AND level = 'Subnat'
                  AND (region ILIKE %s OR region ILIKE %s)
                ORDER BY match_priority
                LIMIT 1
            """, (region_name, f"{region_name}%", f"%{region_name}%",
                  country_code, f"%{region_name}%", f"{region_name}%")))
            
            # Strategy 4b: Match with normalized special characters
            if normalized_name and normalized_name != region_name:
                # Also search GDL regions with normalized names
                queries.append(("""
                    SELECT DISTINCT gdlcode, region
                    FROM gdl.subnational_hdi
                    WHERE isocode3 = %s
                      AND level = 'Subnat'
                      AND (
                        region ILIKE %s OR 
                        region ILIKE %s OR
                        TRANSLATE(LOWER(region), 'áàâãäéèêëíìîïóòôõöúùûüñç', 'aaaaaeeeeiiiiooooouuuunc') 
                        ILIKE TRANSLATE(LOWER(%s), 'áàâãäéèêëíìîïóòôõöúùûüñç', 'aaaaaeeeeiiiiooooouuuunc')
                      )
                    LIMIT 1
                """, (country_code, f"%{normalized_name}%", f"{normalized_name}%", normalized_name)))
            
            # Strategy 5: Match sub-regions in parentheses (e.g., "Toukai (Gifu, Shizuoka, Aichi, Mie)")
            # Extract key words from region name and search within parentheses
            key_words = [w.strip() for w in region_name.split() if len(w) > 3]  # Words longer than 3 chars
            if key_words:
                for key_word in key_words[:3]:  # Try first 3 key words
                    queries.append(("""
                        SELECT DISTINCT gdlcode, region
                        FROM gdl.subnational_hdi
                        WHERE isocode3 = %s
                          AND level = 'Subnat'
                          AND region LIKE '%(%' 
                          AND region ILIKE %s
                        LIMIT 1
                    """, (country_code, f"%{key_word}%")))
            
            # Strategy 6: Normalized name match
            if normalized_name and normalized_name != region_name:
                queries.append(("""
                    SELECT DISTINCT gdlcode, region
                    FROM gdl.subnational_hdi
                    WHERE isocode3 = %s
                      AND level = 'Subnat'
                      AND (region ILIKE %s OR region ILIKE %s)
                    LIMIT 1
                """, (country_code, f"%{normalized_name}%", f"{normalized_name}%")))
            
            # Strategy 7: Translated name contains match
            if translated_name:
                queries.append(("""
                    SELECT DISTINCT gdlcode, region
                    FROM gdl.subnational_hdi
                    WHERE isocode3 = %s
                      AND level = 'Subnat'
                      AND (region ILIKE %s OR region ILIKE %s)
                    LIMIT 1
                """, (country_code, f"%{translated_name}%", f"{translated_name}%")))
        
        # Execute queries in order
        for query, params in queries:
            cur.execute(query, params)
            row = cur.fetchone()
            if row and row["gdlcode"]:
                return str(row["gdlcode"])
        
        # No match found
        return None
        
    except Exception:
        return None
    finally:
        cur.close()
        conn.close()


def get_regional_income_index(
    country_code: str,
    region_code: Optional[str] = None,
    region_name: Optional[str] = None,
    year: int = 2020
) -> Optional[float]:
    """
    Get regional income index from GDL Subnational HDI.
    
    Args:
        country_code: ISO 3-letter country code (e.g., "IDN", "USA")
        region_code: GeoNames admin1_code (optional, for regional queries)
        region_name: Region name (optional, for matching to GDL region names)
        year: Target year
    
    Returns:
        Income index (0-1 scale) or None if not available
        
    Strategy:
    1. If region_code/region_name provided → try to find subnational region
    2. If None → get national level (gdlcode ends with 't')
    3. Resample year if exact match not found
    4. Return incindex if available, fallback to normalized lgnic
    """
    conn = _get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Map region to GDL code
        gdlcode = map_region_to_gdlcode(country_code, region_code, region_name)
        
        if not gdlcode:
            # No mapping found - return None
            return None
        
        # Determine level based on gdlcode pattern
        if gdlcode.endswith('t'):
            level_filter = "National"
            gdlcode_pattern = gdlcode
        else:
            level_filter = "Subnat"
            gdlcode_pattern = gdlcode
        
        # Resample year (get nearest available year)
        # Use exact gdlcode match (we already have the mapped code)
        cur.execute("""
            SELECT year, ABS(year - %s) as year_diff
            FROM gdl.subnational_hdi
            WHERE isocode3 = %s
              AND gdlcode = %s
              AND level = %s
              AND year <= %s
            ORDER BY year_diff
            LIMIT 1
        """, (year, country_code, gdlcode_pattern, level_filter, year))
        
        year_row = cur.fetchone()
        if not year_row:
            return None  # No data available
        
        resampled_year = int(year_row["year"])
        
        # Query using exact gdlcode (already mapped)
        cur.execute("""
            SELECT incindex, lgnic
            FROM gdl.subnational_hdi
            WHERE isocode3 = %s
              AND gdlcode = %s
              AND level = %s
              AND year = %s
            LIMIT 1
        """, (country_code, gdlcode_pattern, level_filter, resampled_year))
        
        row = cur.fetchone()
        if not row:
            return None
        
        # Prefer incindex (0-1 scale), fallback to lgnic (normalized)
        if row["incindex"] is not None:
            return float(row["incindex"])
        elif row["lgnic"] is not None:
            # Convert lgnic to approximate 0-1 scale
            # lgnic is log GNI, typically ranges from ~6 to ~12
            # Normalize: (lgnic - 6) / 6 gives rough 0-1 scale
            lgnic = float(row["lgnic"])
            normalized = (lgnic - 6.0) / 6.0
            return max(0.0, min(1.0, normalized))
        
        return None
        
    except Exception:
        # Graceful fallback: return None on any error
        return None
    finally:
        cur.close()
        conn.close()


def get_regional_education_level(
    country_code: str,
    region_code: Optional[str] = None,
    region_name: Optional[str] = None,
    year: int = 2020
) -> Optional[float]:
    """
    Get regional education level from GDL Education data.
    
    Args:
        country_code: ISO 3-letter country code
        region_code: GeoNames admin1_code (optional)
        region_name: Region name (optional)
        year: Target year
    
    Returns:
        Mean years of education (edyr25) or None if not available
    """
    conn = _get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Map region to GDL code
        gdlcode = map_region_to_gdlcode(country_code, region_code, region_name)
        
        if not gdlcode:
            return None
        
        # Determine level based on gdlcode pattern
        if gdlcode.endswith('t'):
            level_filter = "National"
        else:
            level_filter = "Subnat"
        
        # Resample year
        cur.execute("""
            SELECT year, ABS(year - %s) as year_diff
            FROM gdl.education_work
            WHERE isocode3 = %s
              AND gdlcode = %s
              AND level = %s
              AND year <= %s
            ORDER BY year_diff
            LIMIT 1
        """, (year, country_code, gdlcode, level_filter, year))
        
        year_row = cur.fetchone()
        if not year_row:
            return None
        
        resampled_year = int(year_row["year"])
        
        # Query for education level using exact gdlcode
        cur.execute("""
            SELECT edyr25
            FROM gdl.education_work
            WHERE isocode3 = %s
              AND gdlcode = %s
              AND level = %s
              AND year = %s
            LIMIT 1
        """, (country_code, gdlcode, level_filter, resampled_year))
        
        row = cur.fetchone()
        if not row or row["edyr25"] is None:
            return None
        
        return float(row["edyr25"])
        
    except Exception:
        return None
    finally:
        cur.close()
        conn.close()


def calculate_regional_ses_adjustment(
    country_code: str,
    region_code: Optional[str] = None,
    region_name: Optional[str] = None,
    year: int = 2020
) -> float:
    """
    Calculate regional SES adjustment based on GDL data.
    
    Compares regional income to national average and converts to decile adjustment.
    
    Args:
        country_code: ISO 3-letter country code
        region_code: GeoNames admin1_code (optional)
        region_name: Region name (optional)
        year: Target year
    
    Returns:
        Adjustment value (-2.0 to +2.0 deciles) or 0.0 if data unavailable
        
    Strategy:
    1. Get regional income index
    2. Get national income index (for comparison)
    3. Calculate difference: regional - national
    4. Convert to decile adjustment (0.1 income diff ≈ 1 decile)
    5. Clamp to reasonable range (-2 to +2 deciles)
    """
    # Get regional income
    regional_income = get_regional_income_index(
        country_code, region_code, region_name, year
    )
    if regional_income is None:
        return 0.0  # No adjustment if no regional data
    
    # Get national income (for comparison)
    national_income = get_regional_income_index(
        country_code, None, None, year
    )
    if national_income is None:
        return 0.0  # Can't compare without national baseline
    
    # Calculate difference
    income_diff = regional_income - national_income
    
    # Convert to decile adjustment
    # Income index 0-1 scale, deciles 1-10 scale
    # Rough conversion: 0.1 income difference ≈ 1 decile
    adjustment = income_diff * 10.0
    
    # Clamp to reasonable range (-2 to +2 deciles)
    adjustment = max(-2.0, min(2.0, adjustment))
    
    return adjustment


def get_urbanicity_adjustment(urbanicity: Optional[str]) -> float:
    """
    Map urbanicity to SES adjustment.
    
    Urban areas tend to have higher SES than rural areas.
    
    Args:
        urbanicity: Urbanicity level ("megacity", "city", "town", "rural") or None
    
    Returns:
        Adjustment value (-1.0 to +1.0 deciles)
    """
    adjustments = {
        "megacity": +1.0,   # Highest SES
        "city": +0.5,        # Higher SES
        "town": 0.0,         # Average SES
        "rural": -0.5        # Lower SES
    }
    return adjustments.get(urbanicity, 0.0) if urbanicity else 0.0


def _apply_country_specific_patterns(country_name: str, ethnicity: str) -> str:
    try:
        from .country_ethnicity_patterns import _apply_country_specific_patterns as _impl
    except ImportError:
        from country_ethnicity_patterns import _apply_country_specific_patterns as _impl
    return _impl(country_name, ethnicity)



def get_epr_power_status(
    country_name: str,
    ethnicity: str,
    year: int,
    groupid: Optional[str] = None
) -> Optional[str]:
    """
    Get EPR power status for ethnic group.
    
    Uses multiple matching strategies:
    1. Name mapping (people_groups → EPR names)
    2. GroupID matching (if groupid provided)
    3. Direct name match (fallback)
    
    Args:
        country_name: Country name (as used in EPR, e.g., "Indonesia")
        ethnicity: Ethnic group name (from people_groups, e.g., "Sunda")
        year: Target year
        groupid: Optional group ID for more reliable matching
    
    Returns:
        Power status (e.g., "DOMINANT", "POWERLESS", "DISCRIMINATED") or None
    """
    # Import mapping (lazy import to avoid circular dependencies)
    try:
        from .ethnicity_mapping import ETHNICITY_NAME_MAPPING, GROUPID_TO_EPR
    except ImportError:
        try:
            from ethnicity_mapping import ETHNICITY_NAME_MAPPING, GROUPID_TO_EPR
        except ImportError:
            # Fallback if mapping file doesn't exist
            ETHNICITY_NAME_MAPPING = {}
            GROUPID_TO_EPR = {}
    
    conn = _get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Strategy 1: Use name mapping (people_groups → EPR)
        mapped_name = ETHNICITY_NAME_MAPPING.get(ethnicity, ethnicity)
        
        # Strategy 1b: If not in mapping, try country-specific pattern matching
        if mapped_name == ethnicity and ethnicity:
            mapped_name = _apply_country_specific_patterns(country_name, ethnicity)
        
        # Strategy 2: Try mapped name first (people_groups → EPR name mapping)
        if mapped_name != ethnicity:
            cur.execute("""
                SELECT status
                FROM eth."EPR-2021"
                WHERE statename = %s
                  AND "group" = %s
                  AND "from" <= %s
                  AND "to" >= %s
                ORDER BY "from" DESC
                LIMIT 1
            """, (country_name, mapped_name, year, year))
            
            row = cur.fetchone()
            if row and row["status"]:
                return str(row["status"]).upper()
        
        # Strategy 3: Try original name (fallback)
        cur.execute("""
            SELECT status
            FROM eth."EPR-2021"
            WHERE statename = %s
              AND "group" = %s
              AND "from" <= %s
              AND "to" >= %s
            ORDER BY "from" DESC
            LIMIT 1
        """, (country_name, ethnicity, year, year))
        
        row = cur.fetchone()
        if row and row["status"]:
            return str(row["status"]).upper()
        
        # Strategy 4: If groupid provided, try direct groupid lookup in EPR (last resort)
        if groupid:
            cur.execute("""
                SELECT status
                FROM eth."EPR-2021"
                WHERE statename = %s
                  AND groupid = %s
                  AND "from" <= %s
                  AND "to" >= %s
                ORDER BY "from" DESC
                LIMIT 1
            """, (country_name, str(groupid), year, year))
            
            row = cur.fetchone()
            if row and row["status"]:
                return str(row["status"]).upper()
        
        return None
        
    except Exception:
        return None
    finally:
        cur.close()
        conn.close()


def get_power_status_adjustment(power_status: Optional[str]) -> float:
    """
    Map EPR power status to SES adjustment.
    
    Power status correlates with economic power and SES.
    
    Args:
        power_status: EPR power status (e.g., "DOMINANT", "POWERLESS") or None
    
    Returns:
        Adjustment value (-2.0 to +2.0 deciles)
    """
    adjustments = {
        "MONOPOLY": +2.0,           # Highest SES
        "DOMINANT": +1.5,            # High SES
        "SENIOR PARTNER": +1.0,      # Above average SES
        "JUNIOR PARTNER": +0.5,      # Slightly above average
        "IRRELEVANT": 0.0,           # Average (homogeneous country)
        "POWERLESS": -1.0,           # Below average SES
        "DISCRIMINATED": -1.5,       # Low SES
        "SELF-EXCLUSION": -0.5       # Slightly below average
    }
    if not power_status:
        return 0.0
    return adjustments.get(power_status.upper(), 0.0)


def sample_ses_decile(
    country_code: str,
    year: int,
    region_code: Optional[str] = None,
    region_name: Optional[str] = None,
    urbanicity: Optional[str] = None,
    ethnicity: Optional[str] = None,
    country_name: Optional[str] = None,
    power_status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Sample SES decile using multi-layer proxy approach.
    
    Layers:
    1. Base SES from WID (country-level) - ALWAYS works
    2. Regional adjustment (GDL Subnational HDI) - OPTIONAL
    3. Urbanicity adjustment (from location) - ALWAYS works
    4. EPR power status adjustment (from ethnicity) - OPTIONAL
    
    Args:
        country_code: ISO 3-letter country code
        year: Target year
        region_code: GeoNames admin1_code (optional)
        region_name: Region name (optional, for GDL matching)
        urbanicity: Urbanicity level ("megacity", "city", "town", "rural")
        ethnicity: Ethnic group name (optional, for EPR lookup)
        country_name: Country name (optional, for EPR lookup)
        power_status: EPR power status (optional, if already known)
    
    Returns:
        {
            "decile": int (1-10),
            "avg_income_year": float,
            "ses01": float (0-1),
            "class_label": str,
            "adjustments": {
                "base": float,
                "regional": float,
                "urbanicity": float,
                "power_status": float,
                "final": float
            }
        }
    """
    conn = _get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Layer 1: Base SES from WID (country-level)
        # Try to get WID decile data for this country/year
        cur.execute("""
            SELECT year
            FROM (
                SELECT DISTINCT year
                FROM public.wid_income_deciles
                WHERE country_code = %s
                  AND year <= %s
            ) subq
            ORDER BY ABS(year - %s)
            LIMIT 1
        """, (country_code, year, year))
        
        year_row = cur.fetchone()
        if not year_row:
            # No WID data - calculate adjustments anyway and apply to default base
            base_ses = 5.0
            
            # Calculate all adjustments even without WID data
            regional_adjustment = calculate_regional_ses_adjustment(
                country_code, region_code, region_name, year
            )
            
            urbanicity_adjustments = {
                "megacity": +1.0,
                "city": +0.5,
                "town": 0.0,
                "rural": -0.5
            }
            urbanicity_adjustment = urbanicity_adjustments.get(urbanicity, 0.0) if urbanicity else 0.0
            
            if power_status is None and ethnicity and country_name:
                power_status = get_epr_power_status(country_name, ethnicity, year, groupid=None)
            power_adjustment = get_power_status_adjustment(power_status)
            
            # Apply adjustments
            final_ses = base_ses + (
                regional_adjustment * 0.3 +
                urbanicity_adjustment * 0.2 +
                power_adjustment * 0.4
            )
            final_decile = max(1, min(10, round(final_ses)))
            
            class_map = {
                1: "underclass", 2: "underclass", 3: "working", 4: "working",
                5: "lower_middle", 6: "middle", 7: "middle",
                8: "upper_middle", 9: "upper_middle", 10: "elite"
            }
            
            return {
                "decile": final_decile,
                "avg_income_year": None,
                "ses01": (final_decile - 1) / 9.0,
                "class_label": class_map.get(final_decile, "middle"),
                "adjustments": {
                    "base": base_ses,
                    "regional": regional_adjustment,
                    "urbanicity": urbanicity_adjustment,
                    "power_status": power_adjustment,
                    "final": final_ses
                }
            }
        
        resampled_year = int(year_row["year"])
        
        # Get decile data from wid_income_deciles table
        cur.execute("""
            SELECT decile, avg_income_year
            FROM public.wid_income_deciles
            WHERE country_code = %s
              AND year = %s
            ORDER BY decile
        """, (country_code, resampled_year))
        
        decile_rows = cur.fetchall()
        if not decile_rows or len(decile_rows) < 10:
            # Not enough decile data - calculate adjustments anyway
            base_ses = 5.0
            
            regional_adjustment = calculate_regional_ses_adjustment(
                country_code, region_code, region_name, year
            )
            
            urbanicity_adjustments = {
                "megacity": +1.0,
                "city": +0.5,
                "town": 0.0,
                "rural": -0.5
            }
            urbanicity_adjustment = urbanicity_adjustments.get(urbanicity, 0.0) if urbanicity else 0.0
            
            if power_status is None and ethnicity and country_name:
                power_status = get_epr_power_status(country_name, ethnicity, year, groupid=None)
            power_adjustment = get_power_status_adjustment(power_status)
            
            final_ses = base_ses + (
                regional_adjustment * 0.3 +
                urbanicity_adjustment * 0.2 +
                power_adjustment * 0.4
            )
            final_decile = max(1, min(10, round(final_ses)))
            
            class_map = {
                1: "underclass", 2: "underclass", 3: "working", 4: "working",
                5: "lower_middle", 6: "middle", 7: "middle",
                8: "upper_middle", 9: "upper_middle", 10: "elite"
            }
            
            return {
                "decile": final_decile,
                "avg_income_year": None,
                "ses01": (final_decile - 1) / 9.0,
                "class_label": class_map.get(final_decile, "middle"),
                "adjustments": {
                    "base": base_ses,
                    "regional": regional_adjustment,
                    "urbanicity": urbanicity_adjustment,
                    "power_status": power_adjustment,
                    "final": final_ses
                }
            }
        
        # Convert to list
        deciles = [
            {
                "decile": int(row["decile"]),
                "avg_income_year": float(row["avg_income_year"]) if row["avg_income_year"] else None
            }
            for row in decile_rows
        ]
        
        # Sample probabilistically (uniform for now, could weight by population)
        sampled_decile = random.choice(deciles)
        base_ses = float(sampled_decile["decile"])
        
        # Layer 2: Regional adjustment (GDL)
        regional_adjustment = calculate_regional_ses_adjustment(
            country_code, region_code, region_name, year
        )
        
        # Layer 3: Urbanicity adjustment
        urbanicity_adjustments = {
            "megacity": +1.0,
            "city": +0.5,
            "town": 0.0,
            "rural": -0.5
        }
        urbanicity_adjustment = urbanicity_adjustments.get(urbanicity, 0.0) if urbanicity else 0.0
        
        # Layer 4: EPR power status adjustment
        # Get power status if not provided but we have ethnicity
        if power_status is None and ethnicity and country_name:
            power_status = get_epr_power_status(country_name, ethnicity, year, groupid=None)
        
        power_adjustment = get_power_status_adjustment(power_status)
        
        # Combine all adjustments with weights
        final_ses = base_ses + (
            regional_adjustment * 0.3 +      # 30% weight
            urbanicity_adjustment * 0.2 +    # 20% weight
            power_adjustment * 0.4           # 40% weight
        )
        
        # Clamp to valid range (1-10)
        final_decile = max(1, min(10, round(final_ses)))
        
        # Get avg_income_year for final decile (for consistency)
        avg_income = None
        for d in deciles:
            if d["decile"] == final_decile:
                avg_income = d["avg_income_year"]
                break
        
        # Map to class label
        class_map = {
            1: "underclass",
            2: "underclass",
            3: "working",
            4: "working",
            5: "lower_middle",
            6: "middle",
            7: "middle",
            8: "upper_middle",
            9: "upper_middle",
            10: "elite"
        }
        
        return {
            "decile": final_decile,
            "avg_income_year": avg_income,
            "ses01": (final_decile - 1) / 9.0,
            "class_label": class_map.get(final_decile, "middle"),
            "adjustments": {
                "base": base_ses,
                "regional": regional_adjustment,
                "urbanicity": urbanicity_adjustment,
                "power_status": power_adjustment,
                "final": final_ses
            }
        }
        
    finally:
        cur.close()
        conn.close()


def sample_ethnic_group(
    country_code: str,
    region_code: Optional[str] = None,
    year: int = 2020
) -> Dict[str, Any]:
    """
    Sample ethnic group using EPR → JP mapping approach.
    
    For India: Use EPR → JP mapping (sample EPR group, then sample JP group from that EPR group)
    For other countries: Sample from JP, then map JP → EPR for power status
    
    Returns:
        {
            "groupid": str (JP people_id3, used as ID),
            "group_name": str (JP group name - granular),
            "epr_group_name": str (EPR group name - for power status lookup),
            "power_status": "dominant" | "minoritized" | "mixed",
            "epr_power_status": str (original EPR status),
            "size": float (0-1, population share from EPR if available, else 0.5)
        }
    """
    conn = _get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Get country name for EPR lookup
        country_name = _get_country_name_from_code(country_code)
        
        # Clean up country name (remove "urban", "rural", etc. suffixes)
        if country_name:
            country_name = country_name.replace(" urban", "").replace(" rural", "").strip()
        
        # If no mapping found, try code→EPR fallback then EPR statename search
        if not country_name:
            code_to_epr = {
                "US": "United States of America", "USA": "United States of America",
                "GB": "United Kingdom", "GBR": "United Kingdom",
                "IN": "India", "IND": "India",  # IN/IND → India (not Indonesia)
                "ID": "Indonesia", "IDN": "Indonesia",  # ID/IDN → Indonesia
            }
            country_name = code_to_epr.get((country_code or "").upper())
            if not country_name:
                cur.execute("""
                    SELECT DISTINCT statename
                    FROM eth."EPR-2021"
                    WHERE statename ILIKE %s
                       OR statename ILIKE %s
                    LIMIT 1
                """, (f"%{country_code}%", country_code))
                result = cur.fetchone()
                if result:
                    country_name = result['statename']
                else:
                    country_name = country_code
        
        # Strategy: EPR-first approach for all countries
        # 1. Sample EPR group (weighted by size)
        # 2. Get JP groups that map to that EPR group
        # 3. Sample JP group from those (weighted by population)
        # 4. Return JP group with EPR power status
        
        # Special handling for countries with EPR → JP mappings
        if country_name == "India":
            result = _sample_ethnic_group_india(country_code, year, cur)
            result["_provenance"] = {
                "source_family": "epr_to_jp_mapping",
                "source_method": "india_epr_weighted_jp_sample",
                "fallback_used": False,
            }
            return result
        # Settler/majority-dominant countries: restrict to groups ≥5% to avoid tiny diasporas (Greeks, Punu, etc.)
        if country_name in ("United States of America", "United States", "USA"):
            result = _sample_ethnic_group_dominant_bias(country_code, "United States of America", year, cur, min_size=0.05)
            result["_provenance"] = {
                "source_family": "epr_dominant_bias",
                "source_method": "us_dominant_min_size_005",
                "fallback_used": False,
            }
            return result
        if country_name in ("United Kingdom", "UK", "Great Britain"):
            result = _sample_ethnic_group_dominant_bias(country_code, "United Kingdom", year, cur, min_size=0.03)
            result["_provenance"] = {
                "source_family": "epr_dominant_bias",
                "source_method": "uk_dominant_min_size_003",
                "fallback_used": False,
            }
            return result
        
        # Check if we have a mapping for this country
        country_mappings = {
            "Indonesia": "INDONESIA",
            "Pakistan": "PAKISTAN",
            "Brazil": "BRAZIL",
            "Mexico": "MEXICO",
            "Ethiopia": "ETHIOPIA",
            "Thailand": "THAILAND",
            "Kenya": "KENYA",
            "Malaysia": "MALAYSIA",
            "Nepal": "NEPAL",
            "Ghana": "GHANA",
            "Uganda": "UGANDA",
            "Cameroon": "CAMEROON",
            "Colombia": "COLOMBIA",
            "Peru": "PERU",
            "Argentina": "ARGENTINA",
            "Argentine": "ARGENTINA"  # Alternative name
        }
        
        if country_name in country_mappings:
            result = _sample_ethnic_group_with_mapping(country_code, country_name, year, cur, country_mappings[country_name])
            result["_provenance"] = {
                "source_family": "epr_to_jp_mapping",
                "source_method": f"country_specific_{country_mappings[country_name]}",
                "fallback_used": False,
            }
            return result
        
        # For other countries: Try EPR-first, then Factbook demographics if EPR has no data
        result = _sample_ethnic_group_epr_first(country_code, country_name, year, cur)
        if result.get("group_name") == "Unknown" and result.get("groupid") is None:
            try:
                from .factbook_demographics import sample_ethnic_from_factbook
                fb = sample_ethnic_from_factbook(country_code)
                if fb:
                    fb["_provenance"] = {
                        "source_family": "factbook",
                        "source_method": "factbook_demographics_fallback",
                        "fallback_used": True,
                        "fallback_reason": "epr_first_returned_unknown",
                    }
                    return fb
            except Exception:
                pass
        result["_provenance"] = {
            "source_family": "epr_first",
            "source_method": "epr_weighted_sample_jp_lookup",
            "fallback_used": False,
        }
        return result
    
    finally:
        cur.close()
        conn.close()


def _sample_ethnic_group_dominant_bias(
    country_code: str,
    epr_statename: str,
    year: int,
    cur: Any,  # Cursor
    min_size: float = 0.05
) -> Dict[str, Any]:
    """
    EPR-first with size floor: only sample from groups ≥ min_size to avoid tiny diasporas
    (e.g. US Greeks, UK Punu). Uses same JP matching as _sample_ethnic_group_epr_first.
    """
    cur.execute("""
        SELECT "group", "size", status, groupid
        FROM eth."EPR-2021"
        WHERE statename = %s
          AND "from" <= %s AND "to" >= %s
          AND "size" IS NOT NULL
        ORDER BY "size" DESC
    """, (epr_statename, year, year))
    all_epr = cur.fetchall()
    if not all_epr:
        result = _sample_ethnic_group_jp_first(country_code, epr_statename, year, cur)
        result["_provenance"] = {
            "source_family": "epr_dominant_bias",
            "source_method": "jp_first_fallback",
            "fallback_used": True,
            "fallback_reason": "no_epr_rows_for_dominant_bias",
        }
        return result
    # Restrict to groups ≥ min_size; fallback to 0.03 then all if none qualify
    filtered = [r for r in all_epr if float(r["size"]) >= min_size]
    if not filtered:
        filtered = [r for r in all_epr if float(r["size"]) >= 0.03]
    if not filtered:
        filtered = all_epr
    total_size = sum(float(r["size"]) for r in filtered)
    rand_val = random.random() * total_size
    cumsum = 0
    epr_row = None
    for row in filtered:
        cumsum += float(row["size"])
        if rand_val <= cumsum:
            epr_row = row
            break
    if not epr_row:
        epr_row = filtered[-1]
    epr_group = epr_row["group"]
    epr_power_status = epr_row["status"]
    epr_size = float(epr_row["size"])
    pg_country_code = code_for_system(country_code, "joshua_project")
    mapped_epr_name = _apply_country_specific_patterns(epr_statename, epr_group)
    cur.execute("""
        SELECT people_id3, people_name, population_pgac
        FROM jp.people_groups
        WHERE country_code = %s
          AND population_pgac IS NOT NULL
          AND population_pgac > 0
          AND (
            people_name = %s OR
            people_name ILIKE %s OR
            people_name ILIKE %s
          )
        ORDER BY RANDOM() * population_pgac DESC
        LIMIT 10
    """, (pg_country_code, epr_group, f"%{epr_group}%", f"%{mapped_epr_name}%"))
    matching_jp = cur.fetchall()
    if matching_jp:
        total_pop = sum(float(jp.get("population_pgac", 0) or 0) for jp in matching_jp)
        if total_pop > 0:
            rand_val = random.random() * total_pop
            cumsum = 0
            selected_jp = None
            for jp in matching_jp:
                pop = float(jp.get("population_pgac", 0) or 0)
                cumsum += pop
                if cumsum >= rand_val:
                    selected_jp = jp
                    break
            if not selected_jp:
                selected_jp = matching_jp[-1]
        else:
            selected_jp = random.choice(matching_jp)
        if epr_power_status in ["MONOPOLY", "DOMINANT", "SENIOR PARTNER"]:
            status_label = "dominant"
        elif epr_power_status in ["POWERLESS", "DISCRIMINATED"]:
            status_label = "minoritized"
        else:
            status_label = "mixed"
        return {
            "groupid": str(selected_jp["people_id3"]),
            "group_name": selected_jp["people_name"],
            "epr_group_name": epr_group,
            "power_status": status_label,
            "epr_power_status": epr_power_status,
            "size": epr_size
        }
    if epr_power_status in ["MONOPOLY", "DOMINANT", "SENIOR PARTNER"]:
        status_label = "dominant"
    elif epr_power_status in ["POWERLESS", "DISCRIMINATED"]:
        status_label = "minoritized"
    else:
        status_label = "mixed"
    return {
        "groupid": str(epr_row.get("groupid", "") or ""),
        "group_name": epr_group,
        "epr_group_name": epr_group,
        "power_status": status_label,
        "epr_power_status": epr_power_status,
        "size": epr_size
    }


def _sample_ethnic_group_india(
    country_code: str,
    year: int,
    cur: Any  # Cursor
) -> Dict[str, Any]:
    """
    Sample ethnic group for India using EPR → JP mapping.
    
    Strategy:
    1. Sample EPR group (weighted by size)
    2. Get all JP groups that map to that EPR group
    3. Sample JP group from those (weighted by population)
    4. Return JP group with EPR power status
    """
    try:
        from .epr_to_jp_mapping import build_india_epr_to_jp_mapping, get_jp_groups_for_epr
    except ImportError:
        try:
            from epr_to_jp_mapping import build_india_epr_to_jp_mapping, get_jp_groups_for_epr
        except ImportError:
            # Fallback to old method if mapping module not available
            return _sample_ethnic_group_fallback_india(country_code, year, cur)
    
    # Step 1: Get all EPR groups for India and sample using cumulative distribution
    cur.execute("""
        SELECT "group", "size", status
        FROM eth."EPR-2021"
        WHERE statename = 'India'
          AND "from" <= %s AND "to" >= %s
          AND "size" IS NOT NULL
        ORDER BY "size" DESC
    """, (year, year))
    
    all_epr = cur.fetchall()
    if not all_epr:
        return _sample_ethnic_group_fallback_india(country_code, year, cur)
    
    # Cumulative distribution sampling (correct weighted random)
    import random
    total_size = sum(float(row["size"]) for row in all_epr)
    rand_val = random.random() * total_size
    
    cumsum = 0
    epr_row = None
    for row in all_epr:
        cumsum += float(row["size"])
        if rand_val <= cumsum:
            epr_row = row
            break
    
    if not epr_row:
        epr_row = all_epr[-1]  # Fallback to last group
    
    epr_group = epr_row["group"]
    epr_power_status = epr_row["status"]
    epr_size = float(epr_row["size"])
    
    # Step 2: Get all JP groups for India
    pg_country_code = code_for_system(country_code, "joshua_project")
    cur.execute("""
        SELECT people_id3, people_name, population_pgac
        FROM jp.people_groups
        WHERE country_code = %s
          AND population_pgac IS NOT NULL
          AND population_pgac > 0
    """, (pg_country_code,))
    
    all_jp_groups = [dict(row) for row in cur.fetchall()]
    
    # Step 3: Get JP groups that map to this EPR group
    matching_jp = get_jp_groups_for_epr(epr_group, all_jp_groups)
    # Exclude JP groups that are clearly Indonesian/Malaysian/East Timorese (wrong country in JP data)
    INDIA_JP_EXCLUDE = (
        "javanese", "sundanese", "balinese", "batak", "acehnese", "madurese",
        "minangkabau", "dayak", "makassar", "bugis", "papuan", "ambonese", "minahasa",
        "timorese", "east timor", "ambonese", "ternate", "gorontalo"
    )
    def _is_excluded(jp: dict) -> bool:
        name = (jp.get("people_name") or "").lower()
        return any(ex in name for ex in INDIA_JP_EXCLUDE)
    matching_jp = [jp for jp in matching_jp if not _is_excluded(jp)]
    if not matching_jp:
        # No JP groups match - use EPR group name directly
        if epr_power_status in ["MONOPOLY", "DOMINANT", "SENIOR PARTNER"]:
            status_label = "dominant"
        elif epr_power_status in ["POWERLESS", "DISCRIMINATED"]:
            status_label = "minoritized"
        else:
            status_label = "mixed"
        
        return {
            "groupid": epr_group,  # Use EPR name as ID
            "group_name": epr_group,  # EPR name (less granular)
            "epr_group_name": epr_group,
            "power_status": status_label,
            "epr_power_status": epr_power_status,
            "size": epr_size,
            "_provenance": {
                "source_family": "epr_to_jp_mapping",
                "source_method": "india_epr_group_fallback",
                "fallback_used": True,
                "fallback_reason": "no_matching_jp_group_for_india_epr_group",
            },
        }
    
    # Step 4: Sample JP group from matching groups (weighted by population)
    import random
    from decimal import Decimal
    
    # Convert Decimal to float for calculations
    total_pop = sum(float(jp.get("population_pgac", 0) or 0) for jp in matching_jp)
    if total_pop > 0:
        rand_val = random.random() * total_pop
        cumsum = 0
        selected_jp = None
        for jp in matching_jp:
            pop = float(jp.get("population_pgac", 0) or 0)
            cumsum += pop
            if cumsum >= rand_val:
                selected_jp = jp
                break
        if not selected_jp:
            selected_jp = matching_jp[-1]  # Fallback to last
    else:
        selected_jp = random.choice(matching_jp)
    
    # Map EPR status to simplified status
    if epr_power_status in ["MONOPOLY", "DOMINANT", "SENIOR PARTNER"]:
        status_label = "dominant"
    elif epr_power_status in ["POWERLESS", "DISCRIMINATED"]:
        status_label = "minoritized"
    else:
        status_label = "mixed"
    
    return {
        "groupid": str(selected_jp["people_id3"]),
        "group_name": selected_jp["people_name"],  # Granular JP name
        "epr_group_name": epr_group,  # EPR group it maps to
        "power_status": status_label,
        "epr_power_status": epr_power_status,
        "size": epr_size,
        "_provenance": {
            "source_family": "epr_to_jp_mapping",
            "source_method": "india_epr_weighted_jp_sample",
            "fallback_used": False,
        },
    }


def _sample_ethnic_group_with_mapping(
    country_code: str,
    country_name: str,
    year: int,
    cur: Any,  # Cursor
    mapping_name: str  # e.g., "INDONESIA", "PAKISTAN", etc.
) -> Dict[str, Any]:
    """
    Sample ethnic group using country-specific EPR → JP mapping.
    
    Similar to India but for other countries with mappings.
    """
    try:
        from .epr_to_jp_mapping import (
            INDONESIA_EPR_TO_JP_MAPPING, PAKISTAN_EPR_TO_JP_MAPPING,
            BRAZIL_EPR_TO_JP_MAPPING, MEXICO_EPR_TO_JP_MAPPING,
            ETHIOPIA_EPR_TO_JP_MAPPING, THAILAND_EPR_TO_JP_MAPPING,
            KENYA_EPR_TO_JP_MAPPING, MALAYSIA_EPR_TO_JP_MAPPING,
            NEPAL_EPR_TO_JP_MAPPING, GHANA_EPR_TO_JP_MAPPING,
            UGANDA_EPR_TO_JP_MAPPING, CAMEROON_EPR_TO_JP_MAPPING,
            COLOMBIA_EPR_TO_JP_MAPPING, PERU_EPR_TO_JP_MAPPING,
            ARGENTINA_EPR_TO_JP_MAPPING,
            SOUTH_AFRICA_EPR_TO_JP_MAPPING, AFGHANISTAN_EPR_TO_JP_MAPPING,
            LAOS_EPR_TO_JP_MAPPING, ANGOLA_EPR_TO_JP_MAPPING,
            MOZAMBIQUE_EPR_TO_JP_MAPPING, MALI_EPR_TO_JP_MAPPING,
            GUATEMALA_EPR_TO_JP_MAPPING, ECUADOR_EPR_TO_JP_MAPPING,
            FRANCE_EPR_TO_JP_MAPPING, LIBYA_EPR_TO_JP_MAPPING,
            SLOVENIA_EPR_TO_JP_MAPPING, TURKMENISTAN_EPR_TO_JP_MAPPING,
            NEW_ZEALAND_EPR_TO_JP_MAPPING, GREECE_EPR_TO_JP_MAPPING,
            IRAN_EPR_TO_JP_MAPPING, NIGERIA_EPR_TO_JP_MAPPING,
            ITALY_EPR_TO_JP_MAPPING, CANADA_EPR_TO_JP_MAPPING,
            EGYPT_EPR_TO_JP_MAPPING,
            CHINA_EPR_TO_JP_MAPPING, RUSSIA_EPR_TO_JP_MAPPING,
            CONGO_DRC_EPR_TO_JP_MAPPING, CHAD_EPR_TO_JP_MAPPING,
            VIETNAM_EPR_TO_JP_MAPPING, AUSTRALIA_EPR_TO_JP_MAPPING,
            BANGLADESH_EPR_TO_JP_MAPPING, BOTSWANA_EPR_TO_JP_MAPPING,
            VENEZUELA_EPR_TO_JP_MAPPING,             AZERBAIJAN_EPR_TO_JP_MAPPING,
            ALGERIA_EPR_TO_JP_MAPPING, FIJI_EPR_TO_JP_MAPPING,
            LIBERIA_EPR_TO_JP_MAPPING, ERITREA_EPR_TO_JP_MAPPING,
            BULGARIA_EPR_TO_JP_MAPPING,
            SAUDI_ARABIA_EPR_TO_JP_MAPPING, SYRIA_EPR_TO_JP_MAPPING,
            FINLAND_EPR_TO_JP_MAPPING, CUBA_EPR_TO_JP_MAPPING,
            CAPE_VERDE_EPR_TO_JP_MAPPING, JAMAICA_EPR_TO_JP_MAPPING,
            SUDAN_EPR_TO_JP_MAPPING, ISRAEL_EPR_TO_JP_MAPPING,
            JAPAN_EPR_TO_JP_MAPPING, SPAIN_EPR_TO_JP_MAPPING,
            MOROCCO_EPR_TO_JP_MAPPING, TOGO_EPR_TO_JP_MAPPING,
            TURKEY_EPR_TO_JP_MAPPING, ZIMBABWE_EPR_TO_JP_MAPPING,
            PARAGUAY_EPR_TO_JP_MAPPING, POLAND_EPR_TO_JP_MAPPING,
            CROATIA_EPR_TO_JP_MAPPING, HONDURAS_EPR_TO_JP_MAPPING,
            UZBEKISTAN_EPR_TO_JP_MAPPING, PORTUGAL_EPR_TO_JP_MAPPING,
            SOMALIA_EPR_TO_JP_MAPPING, SWEDEN_EPR_TO_JP_MAPPING,
            CYPRUS_EPR_TO_JP_MAPPING, HUNGARY_EPR_TO_JP_MAPPING,
            NETHERLANDS_EPR_TO_JP_MAPPING, NORWAY_EPR_TO_JP_MAPPING,
            DOMINICAN_REPUBLIC_EPR_TO_JP_MAPPING,
            UNITED_ARAB_EMIRATES_EPR_TO_JP_MAPPING,
            DENMARK_EPR_TO_JP_MAPPING,
            build_country_epr_to_jp_mapping
        )
    except ImportError:
        try:
            from epr_to_jp_mapping import (
                INDONESIA_EPR_TO_JP_MAPPING, PAKISTAN_EPR_TO_JP_MAPPING,
                BRAZIL_EPR_TO_JP_MAPPING, MEXICO_EPR_TO_JP_MAPPING,
                ETHIOPIA_EPR_TO_JP_MAPPING, THAILAND_EPR_TO_JP_MAPPING,
                KENYA_EPR_TO_JP_MAPPING, MALAYSIA_EPR_TO_JP_MAPPING,
                NEPAL_EPR_TO_JP_MAPPING, GHANA_EPR_TO_JP_MAPPING,
                UGANDA_EPR_TO_JP_MAPPING, CAMEROON_EPR_TO_JP_MAPPING,
                COLOMBIA_EPR_TO_JP_MAPPING, PERU_EPR_TO_JP_MAPPING,
                ARGENTINA_EPR_TO_JP_MAPPING,
                SOUTH_AFRICA_EPR_TO_JP_MAPPING, AFGHANISTAN_EPR_TO_JP_MAPPING,
                LAOS_EPR_TO_JP_MAPPING, ANGOLA_EPR_TO_JP_MAPPING,
                MOZAMBIQUE_EPR_TO_JP_MAPPING, MALI_EPR_TO_JP_MAPPING,
                GUATEMALA_EPR_TO_JP_MAPPING, ECUADOR_EPR_TO_JP_MAPPING,
                FRANCE_EPR_TO_JP_MAPPING, LIBYA_EPR_TO_JP_MAPPING,
                SLOVENIA_EPR_TO_JP_MAPPING, TURKMENISTAN_EPR_TO_JP_MAPPING,
                NEW_ZEALAND_EPR_TO_JP_MAPPING, GREECE_EPR_TO_JP_MAPPING,
                IRAN_EPR_TO_JP_MAPPING, NIGERIA_EPR_TO_JP_MAPPING,
                ITALY_EPR_TO_JP_MAPPING, CANADA_EPR_TO_JP_MAPPING,
                EGYPT_EPR_TO_JP_MAPPING,
                CHINA_EPR_TO_JP_MAPPING, RUSSIA_EPR_TO_JP_MAPPING,
                CONGO_DRC_EPR_TO_JP_MAPPING, CHAD_EPR_TO_JP_MAPPING,
                VIETNAM_EPR_TO_JP_MAPPING, AUSTRALIA_EPR_TO_JP_MAPPING,
                BANGLADESH_EPR_TO_JP_MAPPING, BOTSWANA_EPR_TO_JP_MAPPING,
                VENEZUELA_EPR_TO_JP_MAPPING, AZERBAIJAN_EPR_TO_JP_MAPPING,
                ALGERIA_EPR_TO_JP_MAPPING, FIJI_EPR_TO_JP_MAPPING,
                LIBERIA_EPR_TO_JP_MAPPING, ERITREA_EPR_TO_JP_MAPPING,
                BULGARIA_EPR_TO_JP_MAPPING,
                SAUDI_ARABIA_EPR_TO_JP_MAPPING, SYRIA_EPR_TO_JP_MAPPING,
                FINLAND_EPR_TO_JP_MAPPING, CUBA_EPR_TO_JP_MAPPING,
                CAPE_VERDE_EPR_TO_JP_MAPPING, JAMAICA_EPR_TO_JP_MAPPING,
                SUDAN_EPR_TO_JP_MAPPING, ISRAEL_EPR_TO_JP_MAPPING,
                JAPAN_EPR_TO_JP_MAPPING, SPAIN_EPR_TO_JP_MAPPING,
                MOROCCO_EPR_TO_JP_MAPPING, TOGO_EPR_TO_JP_MAPPING,
                TURKEY_EPR_TO_JP_MAPPING, ZIMBABWE_EPR_TO_JP_MAPPING,
                PARAGUAY_EPR_TO_JP_MAPPING, POLAND_EPR_TO_JP_MAPPING,
                CROATIA_EPR_TO_JP_MAPPING, HONDURAS_EPR_TO_JP_MAPPING,
                UZBEKISTAN_EPR_TO_JP_MAPPING, PORTUGAL_EPR_TO_JP_MAPPING,
                SOMALIA_EPR_TO_JP_MAPPING, SWEDEN_EPR_TO_JP_MAPPING,
                CYPRUS_EPR_TO_JP_MAPPING, HUNGARY_EPR_TO_JP_MAPPING,
                NETHERLANDS_EPR_TO_JP_MAPPING, NORWAY_EPR_TO_JP_MAPPING,
                DOMINICAN_REPUBLIC_EPR_TO_JP_MAPPING,
                UNITED_ARAB_EMIRATES_EPR_TO_JP_MAPPING,
                DENMARK_EPR_TO_JP_MAPPING,
                build_country_epr_to_jp_mapping
            )
        except ImportError:
            # Fallback to generic EPR-first
            return _sample_ethnic_group_epr_first(country_code, country_name, year, cur)
    
    # Get the right mapping
    mapping_dicts = {
        "INDONESIA": INDONESIA_EPR_TO_JP_MAPPING,
        "PAKISTAN": PAKISTAN_EPR_TO_JP_MAPPING,
        "BRAZIL": BRAZIL_EPR_TO_JP_MAPPING,
        "MEXICO": MEXICO_EPR_TO_JP_MAPPING,
        "ETHIOPIA": ETHIOPIA_EPR_TO_JP_MAPPING,
        "THAILAND": THAILAND_EPR_TO_JP_MAPPING,
        "KENYA": KENYA_EPR_TO_JP_MAPPING,
        "MALAYSIA": MALAYSIA_EPR_TO_JP_MAPPING,
        "NEPAL": NEPAL_EPR_TO_JP_MAPPING,
        "GHANA": GHANA_EPR_TO_JP_MAPPING,
        "UGANDA": UGANDA_EPR_TO_JP_MAPPING,
        "CAMEROON": CAMEROON_EPR_TO_JP_MAPPING,
        "COLOMBIA": COLOMBIA_EPR_TO_JP_MAPPING,
        "PERU": PERU_EPR_TO_JP_MAPPING,
        "ARGENTINA": ARGENTINA_EPR_TO_JP_MAPPING,
        "SOUTH_AFRICA": SOUTH_AFRICA_EPR_TO_JP_MAPPING,
        "AFGHANISTAN": AFGHANISTAN_EPR_TO_JP_MAPPING,
        "LAOS": LAOS_EPR_TO_JP_MAPPING,
        "ANGOLA": ANGOLA_EPR_TO_JP_MAPPING,
        "MOZAMBIQUE": MOZAMBIQUE_EPR_TO_JP_MAPPING,
        "MALI": MALI_EPR_TO_JP_MAPPING,
        "GUATEMALA": GUATEMALA_EPR_TO_JP_MAPPING,
        "ECUADOR": ECUADOR_EPR_TO_JP_MAPPING,
        "FRANCE": FRANCE_EPR_TO_JP_MAPPING,
        "LIBYA": LIBYA_EPR_TO_JP_MAPPING,
        "SLOVENIA": SLOVENIA_EPR_TO_JP_MAPPING,
        "TURKMENISTAN": TURKMENISTAN_EPR_TO_JP_MAPPING,
        "NEW_ZEALAND": NEW_ZEALAND_EPR_TO_JP_MAPPING,
        "GREECE": GREECE_EPR_TO_JP_MAPPING,
        "IRAN": IRAN_EPR_TO_JP_MAPPING,
        "NIGERIA": NIGERIA_EPR_TO_JP_MAPPING,
        "ITALY": ITALY_EPR_TO_JP_MAPPING,
        "CANADA": CANADA_EPR_TO_JP_MAPPING,
        "EGYPT": EGYPT_EPR_TO_JP_MAPPING,
        "CHINA": CHINA_EPR_TO_JP_MAPPING,
        "RUSSIA": RUSSIA_EPR_TO_JP_MAPPING,
        "CONGO_DRC": CONGO_DRC_EPR_TO_JP_MAPPING,
        "CHAD": CHAD_EPR_TO_JP_MAPPING,
        "VIETNAM": VIETNAM_EPR_TO_JP_MAPPING,
        "AUSTRALIA": AUSTRALIA_EPR_TO_JP_MAPPING,
        "BANGLADESH": BANGLADESH_EPR_TO_JP_MAPPING,
        "BOTSWANA": BOTSWANA_EPR_TO_JP_MAPPING,
        "VENEZUELA": VENEZUELA_EPR_TO_JP_MAPPING,
        "AZERBAIJAN": AZERBAIJAN_EPR_TO_JP_MAPPING,
        "ALGERIA": ALGERIA_EPR_TO_JP_MAPPING,
        "FIJI": FIJI_EPR_TO_JP_MAPPING,
        "LIBERIA": LIBERIA_EPR_TO_JP_MAPPING,
        "ERITREA": ERITREA_EPR_TO_JP_MAPPING,
        "BULGARIA": BULGARIA_EPR_TO_JP_MAPPING,
        "SAUDI_ARABIA": SAUDI_ARABIA_EPR_TO_JP_MAPPING,
        "SYRIA": SYRIA_EPR_TO_JP_MAPPING,
        "FINLAND": FINLAND_EPR_TO_JP_MAPPING,
        "CUBA": CUBA_EPR_TO_JP_MAPPING,
        "CAPE_VERDE": CAPE_VERDE_EPR_TO_JP_MAPPING,
        "JAMAICA": JAMAICA_EPR_TO_JP_MAPPING,
        "SUDAN": SUDAN_EPR_TO_JP_MAPPING,
        "ISRAEL": ISRAEL_EPR_TO_JP_MAPPING,
        "JAPAN": JAPAN_EPR_TO_JP_MAPPING,
        "SPAIN": SPAIN_EPR_TO_JP_MAPPING,
        "MOROCCO": MOROCCO_EPR_TO_JP_MAPPING,
        "TOGO": TOGO_EPR_TO_JP_MAPPING,
        "TURKEY": TURKEY_EPR_TO_JP_MAPPING,
        "ZIMBABWE": ZIMBABWE_EPR_TO_JP_MAPPING,
        "PARAGUAY": PARAGUAY_EPR_TO_JP_MAPPING,
        "POLAND": POLAND_EPR_TO_JP_MAPPING,
        "CROATIA": CROATIA_EPR_TO_JP_MAPPING,
        "HONDURAS": HONDURAS_EPR_TO_JP_MAPPING,
        "UZBEKISTAN": UZBEKISTAN_EPR_TO_JP_MAPPING,
        "PORTUGAL": PORTUGAL_EPR_TO_JP_MAPPING,
        "SOMALIA": SOMALIA_EPR_TO_JP_MAPPING,
        "SWEDEN": SWEDEN_EPR_TO_JP_MAPPING,
        "CYPRUS": CYPRUS_EPR_TO_JP_MAPPING,
        "HUNGARY": HUNGARY_EPR_TO_JP_MAPPING,
        "NETHERLANDS": NETHERLANDS_EPR_TO_JP_MAPPING,
        "NORWAY": NORWAY_EPR_TO_JP_MAPPING,
        "DOMINICAN_REPUBLIC": DOMINICAN_REPUBLIC_EPR_TO_JP_MAPPING,
        "UNITED_ARAB_EMIRATES": UNITED_ARAB_EMIRATES_EPR_TO_JP_MAPPING,
        "DENMARK": DENMARK_EPR_TO_JP_MAPPING,
    }
    
    country_mapping = mapping_dicts.get(mapping_name)
    if not country_mapping:
        return _sample_ethnic_group_epr_first(country_code, country_name, year, cur)
    
    # Step 1: Get all EPR groups and sample using cumulative distribution
    cur.execute("""
        SELECT "group", "size", status
        FROM eth."EPR-2021"
        WHERE statename = %s
          AND "from" <= %s AND "to" >= %s
          AND "size" IS NOT NULL
        ORDER BY "size" DESC
    """, (country_name, year, year))
    
    all_epr = cur.fetchall()
    if not all_epr:
        return _sample_ethnic_group_epr_first(country_code, country_name, year, cur)
    
    # Cumulative distribution sampling (correct weighted random)
    import random
    total_size = sum(float(row["size"]) for row in all_epr)
    rand_val = random.random() * total_size
    
    cumsum = 0
    epr_row = None
    for row in all_epr:
        cumsum += float(row["size"])
        if rand_val <= cumsum:
            epr_row = row
            break
    
    if not epr_row:
        epr_row = all_epr[-1]  # Fallback to last group
    
    epr_group = epr_row["group"]
    epr_power_status = epr_row["status"]
    epr_size = float(epr_row["size"])
    
    # Step 2: Get all JP groups for this country
    pg_country_code = code_for_system(country_code, "joshua_project")
    cur.execute("""
        SELECT people_id3, people_name, population_pgac, primary_language
        FROM jp.people_groups
        WHERE country_code = %s
          AND population_pgac IS NOT NULL
          AND population_pgac > 0
    """, (pg_country_code,))
    
    all_jp_groups = [dict(row) for row in cur.fetchall()]
    
    # Step 3: Get JP groups that map to this EPR group
    from epr_to_jp_mapping import get_jp_groups_for_epr_generic
    matching_jp = get_jp_groups_for_epr_generic(epr_group, all_jp_groups, country_mapping)
    
    if not matching_jp:
        # No JP groups match - use EPR group name directly
        if epr_power_status in ["MONOPOLY", "DOMINANT", "SENIOR PARTNER"]:
            status_label = "dominant"
        elif epr_power_status in ["POWERLESS", "DISCRIMINATED"]:
            status_label = "minoritized"
        else:
            status_label = "mixed"
        
        return {
            "groupid": epr_group,
            "group_name": epr_group,
            "epr_group_name": epr_group,
            "power_status": status_label,
            "epr_power_status": epr_power_status,
            "size": epr_size,
            "_provenance": {
                "source_family": "epr_to_jp_mapping",
                "source_method": f"country_specific_{mapping_name}",
                "fallback_used": True,
                "fallback_reason": "no_matching_jp_group_for_country_mapping",
            },
        }
    
    # Step 4: Sample JP group from matching groups (weighted by population)
    import random
    
    total_pop = sum(float(jp.get("population_pgac", 0) or 0) for jp in matching_jp)
    if total_pop > 0:
        rand_val = random.random() * total_pop
        cumsum = 0
        selected_jp = None
        for jp in matching_jp:
            pop = float(jp.get("population_pgac", 0) or 0)
            cumsum += pop
            if cumsum >= rand_val:
                selected_jp = jp
                break
        if not selected_jp:
            selected_jp = matching_jp[-1]
    else:
        selected_jp = random.choice(matching_jp)
    
    # Map EPR status to simplified status
    if epr_power_status in ["MONOPOLY", "DOMINANT", "SENIOR PARTNER"]:
        status_label = "dominant"
    elif epr_power_status in ["POWERLESS", "DISCRIMINATED"]:
        status_label = "minoritized"
    else:
        status_label = "mixed"
    
    return {
        "groupid": str(selected_jp["people_id3"]),
        "group_name": selected_jp["people_name"],
        "epr_group_name": epr_group,
        "power_status": status_label,
        "epr_power_status": epr_power_status,
        "size": epr_size,
        "_provenance": {
            "source_family": "epr_to_jp_mapping",
            "source_method": f"country_specific_{mapping_name}",
            "fallback_used": False,
        },
    }


def _sample_ethnic_group_fallback_india(
    country_code: str,
    year: int,
    cur: Any  # Cursor
) -> Dict[str, Any]:
    """Fallback method for India if mapping module not available."""
    cur.execute("""
        SELECT "group", "size", status
        FROM eth."EPR-2021"
        WHERE statename = 'India'
          AND "from" <= %s AND "to" >= %s
          AND "size" IS NOT NULL
        ORDER BY "size" DESC
    """, (year, year))
    
    all_epr = cur.fetchall()
    if not all_epr:
        return None
    
    # Cumulative distribution sampling (correct weighted random)
    import random
    total_size = sum(float(row["size"]) for row in all_epr)
    rand_val = random.random() * total_size
    
    cumsum = 0
    epr_row = None
    for row in all_epr:
        cumsum += float(row["size"])
        if rand_val <= cumsum:
            epr_row = row
            break
    
    if not epr_row:
        epr_row = all_epr[-1]  # Fallback to last group
    if epr_row:
        power_status = epr_row["status"]
        if power_status in ["MONOPOLY", "DOMINANT", "SENIOR PARTNER"]:
            status_label = "dominant"
        elif power_status in ["POWERLESS", "DISCRIMINATED"]:
            status_label = "minoritized"
        else:
            status_label = "mixed"
        
        return {
            "groupid": epr_row["group"],
            "group_name": epr_row["group"],
            "epr_group_name": epr_row["group"],
            "power_status": status_label,
            "epr_power_status": power_status,
            "size": float(epr_row["size"]),
            "_provenance": {
                "source_family": "epr_to_jp_mapping",
                "source_method": "india_fallback_epr_group",
                "fallback_used": True,
                "fallback_reason": "india_epr_mapping_module_unavailable_or_no_match",
            },
        }
    
    return {
        "groupid": None,
        "group_name": "Unknown",
        "epr_group_name": None,
        "power_status": "dominant",
        "epr_power_status": None,
        "size": 0.5
    }


def _sample_ethnic_group_epr_first(
    country_code: str,
    country_name: str,
    year: int,
    cur: Any  # Cursor
) -> Dict[str, Any]:
    """
    EPR-first approach for non-India countries.
    
    Strategy:
    1. Sample EPR group (weighted by size)
    2. Try to find JP groups that match (using pattern matching)
    3. If found, sample JP group; otherwise use EPR group name
    """
    if not country_name:
        # Fallback to old JP-first method
        return _sample_ethnic_group_jp_first(country_code, country_name, year, cur)
    
    # Step 1: Get all EPR groups and sample using cumulative distribution
    cur.execute("""
        SELECT "group", "size", status
        FROM eth."EPR-2021"
        WHERE statename = %s
          AND "from" <= %s AND "to" >= %s
          AND "size" IS NOT NULL
        ORDER BY "size" DESC
    """, (country_name, year, year))
    
    all_epr = cur.fetchall()
    if not all_epr:
        # No EPR data - fallback to JP-first
        return _sample_ethnic_group_jp_first(country_code, country_name, year, cur)
    
    # Cumulative distribution sampling (correct weighted random)
    import random
    total_size = sum(float(row["size"]) for row in all_epr)
    rand_val = random.random() * total_size
    
    cumsum = 0
    epr_row = None
    for row in all_epr:
        cumsum += float(row["size"])
        if rand_val <= cumsum:
            epr_row = row
            break
    
    if not epr_row:
        epr_row = all_epr[-1]  # Fallback to last group
    
    epr_group = epr_row["group"]
    epr_power_status = epr_row["status"]
    epr_size = float(epr_row["size"])
    
    # Step 2: Try to find JP groups that match this EPR group
    pg_country_code = code_for_system(country_code, "joshua_project")
    
    # Use pattern matching to find JP groups
    mapped_epr_name = _apply_country_specific_patterns(country_name, epr_group)
    
    # Try to find JP groups matching the EPR group name
    cur.execute("""
        SELECT people_id3, people_name, population_pgac
        FROM jp.people_groups
        WHERE country_code = %s
          AND population_pgac IS NOT NULL
          AND population_pgac > 0
          AND (
            people_name = %s OR
            people_name ILIKE %s OR
            people_name ILIKE %s
          )
        ORDER BY RANDOM() * population_pgac DESC
        LIMIT 10
    """, (pg_country_code, epr_group, f"%{epr_group}%", f"%{mapped_epr_name}%"))
    
    matching_jp = cur.fetchall()
    
    if matching_jp:
        # Found JP groups - sample one
        import random
        from decimal import Decimal
        
        total_pop = sum(float(jp.get("population_pgac", 0) or 0) for jp in matching_jp)
        if total_pop > 0:
            rand_val = random.random() * total_pop
            cumsum = 0
            selected_jp = None
            for jp in matching_jp:
                pop = float(jp.get("population_pgac", 0) or 0)
                cumsum += pop
                if cumsum >= rand_val:
                    selected_jp = jp
                    break
            if not selected_jp:
                selected_jp = matching_jp[-1]
        else:
            selected_jp = random.choice(matching_jp)
        
        # Map EPR status
        if epr_power_status in ["MONOPOLY", "DOMINANT", "SENIOR PARTNER"]:
            status_label = "dominant"
        elif epr_power_status in ["POWERLESS", "DISCRIMINATED"]:
            status_label = "minoritized"
        else:
            status_label = "mixed"
        
        return {
            "groupid": str(selected_jp["people_id3"]),
            "group_name": selected_jp["people_name"],  # Granular JP name
            "epr_group_name": epr_group,
            "power_status": status_label,
            "epr_power_status": epr_power_status,
            "size": epr_size,
            "_provenance": {
                "source_family": "epr_to_jp_mapping",
                "source_method": "epr_weighted_sample_jp_lookup",
                "fallback_used": False,
            },
        }
    
    # No JP groups found - use EPR group name directly
    if epr_power_status in ["MONOPOLY", "DOMINANT", "SENIOR PARTNER"]:
        status_label = "dominant"
    elif epr_power_status in ["POWERLESS", "DISCRIMINATED"]:
        status_label = "minoritized"
    else:
        status_label = "mixed"
    
    return {
        "groupid": epr_group,  # Use EPR name as ID
        "group_name": epr_group,  # EPR name (less granular)
        "epr_group_name": epr_group,
        "power_status": status_label,
        "epr_power_status": epr_power_status,
        "size": epr_size,
        "_provenance": {
            "source_family": "epr_first",
            "source_method": "epr_weighted_sample_jp_lookup",
            "fallback_used": False,
        },
    }


def _sample_ethnic_group_jp_first(
    country_code: str,
    country_name: str,
    year: int,
    cur: Any  # Cursor
) -> Dict[str, Any]:
    """Fallback: JP-first approach (old method)."""
    pg_country_code = code_for_system(country_code, "joshua_project")
    
    cur.execute("""
        SELECT people_id3, people_name, population_pgac
        FROM jp.people_groups
        WHERE country_code = %s
          AND population_pgac IS NOT NULL
          AND population_pgac > 0
        ORDER BY RANDOM() * population_pgac DESC
        LIMIT 1
    """, (pg_country_code,))
    
    jp_row = cur.fetchone()
    if jp_row:
        jp_group_name = jp_row["people_name"]
        jp_group_id = str(jp_row["people_id3"])
        
        # Try to get EPR power status
        epr_power_status = None
        epr_group_name = None
        
        if country_name:
            epr_power_status = get_epr_power_status(
                country_name, 
                jp_group_name, 
                year, 
                groupid=jp_group_id
            )
        
        if epr_power_status:
            if epr_power_status in ["MONOPOLY", "DOMINANT", "SENIOR PARTNER"]:
                status_label = "dominant"
            elif epr_power_status in ["POWERLESS", "DISCRIMINATED"]:
                status_label = "minoritized"
            else:
                status_label = "mixed"
        else:
            status_label = "mixed"
        
        return {
            "groupid": jp_group_id,
            "group_name": jp_group_name,
            "epr_group_name": epr_group_name,
            "power_status": status_label,
            "epr_power_status": epr_power_status,
            "size": 0.5,
            "_provenance": {
                "source_family": "epr_dominant_bias",
                "source_method": "jp_first",
                "fallback_used": False,
            },
        }
    
    return {
        "groupid": None,
        "group_name": "Unknown",
        "epr_group_name": None,
        "power_status": "dominant",
        "epr_power_status": None,
        "size": 0.5,
        "_provenance": {
            "source_family": "epr_dominant_bias",
            "source_method": "jp_first_unknown",
            "fallback_used": True,
            "fallback_reason": "no_jp_people_groups_available",
        },
    }


def sample_religion_language(
    country_code: str,
    ethnic_group_id: Optional[str] = None,
    ethnic_group_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Sample religion and language from people_groups.
    
    Args:
        country_code: Country code
        ethnic_group_id: Either people_groups people_id3 (numeric) or EPR group name (string)
        ethnic_group_name: EPR group name (used if ethnic_group_id is an EPR name)
    
    Returns:
        {
            "religion": str,
            "primary_language": str,
            "secondary_languages": List[str]
        }
    """
    conn = _get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Map country code for people_groups
        pg_country_code = code_for_system(country_code, "joshua_project")
        
        if ethnic_group_id:
            # Check if ethnic_group_id is numeric (people_id3) or string (EPR group name)
            try:
                # Try as numeric ID first
                group_id_int = int(ethnic_group_id)
                cur.execute("""
                    SELECT primary_religion, primary_language
                    FROM jp.people_groups
                    WHERE people_id3 = %s
                    LIMIT 1
                """, (group_id_int,))
            except (ValueError, TypeError):
                # Not numeric - treat as EPR group name
                # Try to match by name
                group_name = ethnic_group_name or ethnic_group_id
                cur.execute("""
                    SELECT primary_religion, primary_language
                    FROM jp.people_groups
                    WHERE country_code = %s
                      AND (people_name = %s OR people_name ILIKE %s)
                    LIMIT 1
                """, (pg_country_code, group_name, f"%{group_name}%"))
            
            group_row = cur.fetchone()
            if group_row:
                # Get secondary languages (if table exists and has that data)
                # For now, skip secondary languages - can add later if needed
                secondary = []
                
                secondary = [r["language_name"] for r in cur.fetchall()]
                
                return {
                    "religion": group_row["primary_religion"] or "Unknown",
                    "primary_language": group_row["primary_language"] or "Unknown",
                    "secondary_languages": secondary,
                    "_provenance": {
                        "source_family": "joshua_project",
                        "source_method": "matched_by_id" if isinstance(ethnic_group_id, int) or str(ethnic_group_id).strip().isdigit() else "matched_by_name",
                        "religion_found": bool(group_row.get("primary_religion")),
                        "language_found": bool(group_row.get("primary_language")),
                        "fallback_used": False,
                    },
                }
        
        # Fallback: sample from country (try multiple code variations)
        codes_to_try = [
            country_code,
            code_for_system(country_code, "geonames"),
            pg_country_code
        ]
        codes_to_try = list(dict.fromkeys(codes_to_try))  # Remove duplicates
        
        for code in codes_to_try:
            cur.execute("""
                SELECT primary_religion, primary_language
                FROM jp.people_groups
                WHERE country_code = %s
                ORDER BY RANDOM() * population_pgac DESC
                LIMIT 1
            """, (code,))
            
            country_row = cur.fetchone()
            if country_row:
                return {
                    "religion": country_row["primary_religion"] or "Unknown",
                    "primary_language": country_row["primary_language"] or "Unknown",
                    "secondary_languages": [],
                    "_provenance": {
                        "source_family": "joshua_project",
                        "source_method": "random_country_level_fallback",
                        "religion_found": bool(country_row.get("primary_religion")),
                        "language_found": bool(country_row.get("primary_language")),
                        "fallback_used": True,
                        "fallback_reason": "no_group_level_match_for_" + ("id" if ethnic_group_id else "name"),
                    },
                }
        
        # No people_groups row: try Factbook country-level religion/language shares
        try:
            from .factbook_demographics import sample_religion_language_from_factbook
            fb = sample_religion_language_from_factbook(country_code)
            if fb:
                fb["_provenance"] = {
                    "source_family": "factbook",
                    "source_method": "factbook_demographics_fallback",
                    "religion_found": bool(fb.get("religion") and fb.get("religion") != "Unknown"),
                    "language_found": bool(fb.get("primary_language") and fb.get("primary_language") != "Unknown"),
                    "fallback_used": True,
                    "fallback_reason": "no_joshua_project_data_for_country",
                }
                return fb
        except Exception:
            pass
        return {
            "religion": "Unknown",
            "primary_language": "Unknown",
            "secondary_languages": [],
            "_provenance": {
                "source_family": "none",
                "source_method": "ultimate_fallback_no_data",
                "religion_found": False,
                "language_found": False,
                "fallback_used": True,
                "fallback_reason": "no_data_from_joshua_project_or_factbook",
            },
        }
        
    finally:
        cur.close()
        conn.close()


def _apply_country_defaults_to_identity(
    country_code: str,
    ethnic: Dict[str, Any],
    rel_lang: Dict[str, Any],
) -> None:
    """
    Display-only fallback: when EPR/people_groups return no match, fill labels from
    COUNTRY_DEFAULT_LABELS so prompt/sheet don't show empty or "Unknown". Mutates in place.
    Does NOT replace power/SES: those still come from sample_ethnic_group's return (e.g. when
    no EPR data, power_status stays the hardcoded "dominant"). See IDENTITY_FALLBACK_AND_NO_EPR.md.
    """
    ref = normalize_country_ref(country_code or "")
    code = str(ref.get("iso3") or ref.get("iso2") or (country_code or "")).upper().strip()
    defaults = COUNTRY_DEFAULT_LABELS.get(code) or _DEFAULT_LABEL_FALLBACK
    missing_ethnic = not ethnic.get("group_name") or (ethnic.get("group_name") or "").strip() == "Unknown"
    if missing_ethnic and defaults.get("ethnicity"):
        ethnic["group_name"] = defaults["ethnicity"]
    missing_religion = not rel_lang.get("religion") or (rel_lang.get("religion") or "").strip() == "Unknown"
    if missing_religion and defaults.get("religion"):
        rel_lang["religion"] = defaults["religion"]
    missing_lang = not rel_lang.get("primary_language") or (rel_lang.get("primary_language") or "").strip() == "Unknown"
    if missing_lang and defaults.get("language"):
        rel_lang["primary_language"] = defaults["language"]


def generate_identity_context(
    country_code: str,
    year: int,
    age: int,
    gender: Optional[str] = None
) -> Tuple[IdentitySkeleton, Dict[str, Any]]:
    """
    Generate full identity context before querying WVS.
    
    Pipeline:
    1. Location (country → region → city)
    2. SES decile (from WID)
    3. Ethnic group (from EPR/GeoEPR)
    4. Religion & language (from people_groups)
    5. Build IdentitySkeleton
    6. Return context for WVS querying
    
    Returns:
        (IdentitySkeleton, context_dict)
    """
    # 1. Sample location
    location = sample_location(country_code, year)
    
    # 2. Sample ethnic group (needed for SES adjustment)
    ethnic = sample_ethnic_group(
        country_code,
        location["region"]["admin1_code"] if location["region"] else None,
        year
    )
    
    # 3. Sample SES (with multi-layer adjustments)
    country_name = _get_country_name_from_code(country_code)
    ses = sample_ses_decile(
        country_code=country_code,
        year=year,
        region_code=location["region"]["admin1_code"] if location["region"] else None,
        region_name=location["region"]["admin1_name"] if location["region"] else None,
        urbanicity=location["urbanicity"],
        ethnicity=ethnic.get("group_name"),
        country_name=country_name,
        power_status=ethnic.get("epr_power_status")  # Use EPR status if available
    )
    
    # 4. Sample religion & language
    rel_lang = sample_religion_language(
        country_code,
        ethnic.get("groupid"),
        ethnic.get("group_name")  # Pass group name for EPR group name matching
    )

    # 4b. Country-level fallbacks when EPR/people_groups data is missing or thin
    _apply_country_defaults_to_identity(country_code, ethnic, rel_lang)

    # 5. Build IdentitySkeleton
    identity = IdentitySkeleton(
        internal_id=f"{country_code}_{year}_{random.randint(1000, 9999)}",
        given_name="",  # Would be generated separately
        gender=gender or ("male" if random.random() < 0.5 else "female"),
        birth_year=year - age,
        anchor_year=year,
        age_at_anchor=age,
        country_code=country_code,
        region=location["region"]["admin1_name"] if location["region"] else "",
        locality=location["city"]["name"] if location["city"] else "",
        urbanicity=location["urbanicity"],
        class_origin=ses["class_label"],
        current_class=ses["class_label"],
        ethnicity_label=ethnic["group_name"],
        minority_status=ethnic["power_status"],
        childhood_religion=rel_lang["religion"],
        current_religion=rel_lang["religion"],
        primary_language=rel_lang["primary_language"],
        secondary_languages=rel_lang["secondary_languages"]
    )
    
    # 6. Build context for WVS querying (with all demographic mappings)
    context = {
        "location": location,
        "ses": ses,
        "ethnic": ethnic,
        "religion": rel_lang["religion"],
        "language": rel_lang["primary_language"],
        "_rel_lang_provenance": rel_lang.get("_provenance", {}),
        "gender": identity.gender,
        "age_group": _map_age_to_age_group(age),
        # WVS-specific demographic codes
        "wvs_income": _map_ses_decile_to_wvs_income(ses["decile"]),
        "wvs_education": _map_class_to_wvs_education(identity.current_class, ses["decile"]),
        "wvs_urbanicity": _map_urbanicity_to_wvs(identity.urbanicity),
        "wvs_religion": _map_religion_name_to_wvs_code(rel_lang["religion"], country_code)
    }
    
    return identity, context


def generate_parent_identities(
    *,
    country_code: str,
    child_birth_year: int,
    allow_story_reasons: bool = False,
    fixed_parent_genders: Tuple[str, str] = ("male", "female"),
    enforce_father_older: bool = True,
    father_younger_probability: float = 0.05,
    max_father_younger_gap_years: int = 6,
) -> Dict[str, Any]:
    """
    Canonical entrypoint: generate two parents (typically father+mother) at a child's birth year.

    This is the function we can wire into the broader v2 pipeline. It produces:
    - location, ethnicity, SES, religion/language context (shared household defaults)
    - two parent records with *coupled ages at child's birth* generated via the mixture age-gap model

    Notes:
    - We intentionally do NOT pretend to have country-specific spouse age-gap truth by default.
      The model uses global priors with optional overrides in config/parent_age_model.json.
    - If allow_story_reasons=False, large gaps / life-stage mismatches are rejected/resampled.
    """
    try:
        from .parent_age_model import sample_parent_ages_at_birth
    except ImportError:
        from parent_age_model import sample_parent_ages_at_birth

    year = int(child_birth_year)

    # 1. Shared household context at child's birth year
    location = sample_location(country_code, year)
    ethnic = sample_ethnic_group(
        country_code,
        location["region"]["admin1_code"] if location.get("region") else None,
        year,
    )
    country_name = _get_country_name_from_code(country_code)
    ses = sample_ses_decile(
        country_code=country_code,
        year=year,
        region_code=location["region"]["admin1_code"] if location.get("region") else None,
        region_name=location["region"]["admin1_name"] if location.get("region") else None,
        urbanicity=location.get("urbanicity"),
        ethnicity=ethnic.get("group_name"),
        country_name=country_name,
        power_status=ethnic.get("epr_power_status"),
    )
    rel_lang = sample_religion_language(
        country_code,
        ethnic.get("groupid"),
        ethnic.get("group_name"),
    )

    # Apply country defaults so we never pass "Unknown" to child identity (everyone gets an identity)
    _apply_country_defaults_to_identity(country_code, ethnic, rel_lang)

    # 2. Coupled parent ages at child's birth
    age_sample = sample_parent_ages_at_birth(
        country_code=country_code,
        child_birth_year=year,
        urbanicity=location.get("urbanicity"),
        allow_story_reasons=allow_story_reasons,
    )

    # Convention: Parent A = younger-typical anchor; map to mother by default.
    mother_age = age_sample.parent_a_age_at_birth
    father_age = age_sample.parent_b_age_at_birth

    # If you want the default social pattern “father older than mother”, enforce it here.
    # This is a modeling choice (not a universal truth), so it is configurable.
    #
    # We allow "father younger" *rarely* (default 5%) for modest gaps, because it is real.
    # For large negative gaps, we only allow it if allow_story_reasons=True.
    if enforce_father_older and father_age < mother_age:
        younger_gap = int(mother_age) - int(father_age)  # positive when father younger
        keep_younger = False

        if younger_gap <= max_father_younger_gap_years:
            # Rare-but-allowed case (near peers)
            keep_younger = random.random() < float(father_younger_probability)
        else:
            # Large negative gap: only if we're allowing "story reasons"
            if allow_story_reasons and (random.random() < float(father_younger_probability)):
                keep_younger = True

        if not keep_younger:
            father_age, mother_age = mother_age, father_age

    father_gender, mother_gender = fixed_parent_genders

    gap_father_minus_mother = int(father_age) - int(mother_age)

    # 3. Optionally refine parent WVS demographics (education/religion) from WVS respondent slice
    #    using existing slice query utilities.
    def _map_urbanicity_to_urbrural(urb: Optional[str]) -> Optional[str]:
        if not urb:
            return None
        u = urb.lower()
        if any(k in u for k in ("mega", "city", "town")):
            return "1"  # Urban
        if "rural" in u:
            return "2"
        return None

    father_wvs_education = None
    mother_wvs_education = None
    father_wvs_religion = None
    mother_wvs_religion = None

    try:
        conn = _get_db_connection()
        urbr = _map_urbanicity_to_urbrural(location.get("urbanicity"))
        income_code = _map_ses_decile_to_wvs_income(ses["decile"])
        # For non-WVS countries, slice from WVS proxy (supplement-routed) so we get education/religion distributions
        slice_country = _slice_country_for_survey(country_code)

        # Father slice (male)
        rows_f, _ = _qp.get_matching_respondents(
            conn,
            country=slice_country,
            urban_rural=urbr,
            income=income_code,
            education=None,
            sex="1",
            religion=None,
            min_age=18,
            min_n=20,
        )
        ids_f = [r["respondent_id"] for r in rows_f]
        dist_f = _qp.get_slice_distributions(conn, ids_f)

        # Mother slice (female)
        rows_m, _ = _qp.get_matching_respondents(
            conn,
            country=slice_country,
            urban_rural=urbr,
            income=income_code,
            education=None,
            sex="2",
            religion=None,
            min_age=16,
            min_n=20,
        )
        ids_m = [r["respondent_id"] for r in rows_m]
        dist_m = _qp.get_slice_distributions(conn, ids_m)

        def _age_bucket_for_parent(age: int) -> str:
            if age < 25:
                return "18-24"
            if age < 35:
                return "25-34"
            if age < 45:
                return "35-44"
            if age < 55:
                return "45-54"
            return "55+"

        def _sample_from_counts(counts: Dict[int, int]) -> Optional[str]:
            if not counts:
                return None
            total = sum(counts.values())
            if total <= 0:
                return None
            r = random.random() * total
            acc = 0
            for k, v in counts.items():
                acc += v
                if r <= acc:
                    return str(k)
            return str(next(iter(counts.keys())))

        # Father education / religion
        bucket_f = _age_bucket_for_parent(father_age)
        edu_male = dist_f["education_by_male"].get(bucket_f)
        if not edu_male:
            # fallback: aggregate over all male buckets
            agg: Dict[int, int] = {}
            for b_counts in dist_f["education_by_male"].values():
                for k, v in b_counts.items():
                    agg[k] = agg.get(k, 0) + v
            edu_male = agg
        father_wvs_education = _sample_from_counts(edu_male)
        if dist_f["religion_dist"]:
            father_wvs_religion = _sample_from_counts(dist_f["religion_dist"])

        # Mother education / religion
        bucket_m = _age_bucket_for_parent(mother_age)
        edu_female = dist_m["education_by_female"].get(bucket_m)
        if not edu_female:
            agg_f: Dict[int, int] = {}
            for b_counts in dist_m["education_by_female"].values():
                for k, v in b_counts.items():
                    agg_f[k] = agg_f.get(k, 0) + v
            edu_female = agg_f
        mother_wvs_education = _sample_from_counts(edu_female)
        if dist_m["religion_dist"]:
            mother_wvs_religion = _sample_from_counts(dist_m["religion_dist"])
    except Exception:
        # If anything goes wrong, fall back to SES/religion-name mappings elsewhere.
        pass
    finally:
        try:
            conn.close()
        except Exception:
            pass

    return {
        "child_birth_year": year,
        "location": location,
        "ethnicity": ethnic,
        "ses": ses,
        "religion_language": rel_lang,
        "parents": {
            "father": {
                "gender": father_gender,
                "age_at_child_birth": father_age,
                "birth_year": year - father_age,
                "wvs_income": _map_ses_decile_to_wvs_income(ses["decile"]),
                "wvs_education": father_wvs_education,
                "wvs_religion": father_wvs_religion,
            },
            "mother": {
                "gender": mother_gender,
                "age_at_child_birth": mother_age,
                "birth_year": year - mother_age,
                "wvs_income": _map_ses_decile_to_wvs_income(ses["decile"]),
                "wvs_education": mother_wvs_education,
                "wvs_religion": mother_wvs_religion,
            },
        },
        "age_model": {
            "parent_a_age_at_birth": age_sample.parent_a_age_at_birth,
            "parent_b_age_at_birth": age_sample.parent_b_age_at_birth,
            "gap_b_minus_a": age_sample.gap_b_minus_a,
            "gap_father_minus_mother": gap_father_minus_mother,
            "a_component": age_sample.a_component,
            "gap_component": age_sample.gap_component,
            "resamples": age_sample.resamples,
            "story_reason_required": age_sample.story_reason_required,
            "story_reason_hint": age_sample.story_reason_hint,
        },
    }


def create_persona_identity_from_parents(
    parent_identity: Dict[str, Any],
    birth_year: int,
    anchor_year: int,
    age_at_anchor: int,
    gender: Optional[str] = None,
    country_code: Optional[str] = None,
) -> IdentitySkeleton:
    """
    Derive child IdentitySkeleton from a precomputed parent_identity (from generate_parent_identities).
    Use this when generating parents first and the child from them (parents-first flow).
    """
    location = parent_identity.get("location") or {}
    ethnic = dict(parent_identity.get("ethnicity") or {})
    rel_lang = dict(parent_identity.get("religion_language") or {})
    ses = parent_identity.get("ses") or {}
    country_code = code_for_system(country_code or location.get("country_code") or "", "iso3")
    region = (location.get("region") or {}).get("admin1_name", "")
    city = location.get("city") or {}
    locality = city.get("name", "") if isinstance(city, dict) else ""
    urb = (location.get("urbanicity") or "rural").lower()
    if urb not in ("rural", "town", "city", "megacity"):
        urb = "rural"
    class_label = (ses.get("class_label") or "working").replace(" ", "_").lower()
    if class_label not in ("underclass", "working", "lower_middle", "middle", "upper_middle", "elite"):
        class_label = "working"
    # Ensure child never gets Unknown: apply country defaults if missing (everyone gets an identity)
    _apply_country_defaults_to_identity(country_code, ethnic, rel_lang)
    power = ethnic.get("epr_power_status") or ethnic.get("power_status") or ""
    minority_status = "dominant" if (power and "dominant" in str(power).lower()) else "minoritized"
    religion = rel_lang.get("religion") or ""
    primary_lang = rel_lang.get("primary_language") or ""
    secondary_langs = rel_lang.get("secondary_languages")
    if secondary_langs is None:
        secondary_langs = []
    if gender is None:
        gender = random.choice(["male", "female"])
    return IdentitySkeleton(
        internal_id=f"child_{country_code}_{birth_year}_{random.randint(1000, 9999)}",
        given_name="",
        family_name="",
        gender=gender,
        birth_year=birth_year,
        anchor_year=anchor_year,
        age_at_anchor=age_at_anchor,
        country_code=country_code,
        region=region,
        locality=locality,
        urbanicity=urb,
        class_origin=class_label,
        current_class=class_label,
        ethnicity_label=ethnic.get("group_name", "") or "",
        minority_status=minority_status,
        childhood_religion=religion,
        current_religion=religion,
        primary_language=primary_lang,
        secondary_languages=list(secondary_langs) if secondary_langs else [],
    )


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


def _map_ses_decile_to_wvs_income(decile: int) -> str:
    """
    Map SES decile (1-10) to WVS income groups (1-3).
    
    WVS Q288R:
    - 1 = Low (steps 1-3 of 10-step scale)
    - 2 = Middle (steps 4-7)
    - 3 = High (steps 8-10)
    """
    if decile <= 3:
        return "1"  # Low
    elif decile <= 7:
        return "2"  # Middle
    else:
        return "3"  # High


def _map_class_to_wvs_education(class_label: str, decile: int) -> str:
    """
    Map class label and decile to WVS education level (0-8, ISCED 2011).
    
    WVS Q275 (ISCED 2011):
    - 0 = No education
    - 1 = Primary
    - 2 = Lower secondary
    - 3 = Upper secondary
    - 4 = Post-secondary non-tertiary
    - 5 = Short-cycle tertiary
    - 6 = Bachelor
    - 7 = Master
    - 8 = Doctoral
    
    Probabilistic mapping based on class and decile.
    """
    # Base education by class
    class_education_map = {
        "underclass": (0, 2),  # No education to lower secondary
        "working": (1, 3),      # Primary to upper secondary
        "lower_middle": (2, 4), # Lower secondary to post-secondary
        "middle": (3, 5),       # Upper secondary to short-cycle tertiary
        "upper_middle": (4, 6), # Post-secondary to bachelor
        "elite": (6, 8)         # Bachelor to doctoral
    }
    
    min_edu, max_edu = class_education_map.get(class_label, (2, 4))
    
    # Adjust based on decile within class
    # Higher decile = higher education within class range
    decile_within_class = (decile - 1) % 10  # 0-9
    education_level = min_edu + int((decile_within_class / 9.0) * (max_edu - min_edu))
    
    return str(education_level)


def _map_urbanicity_to_wvs(urbanicity: str) -> Optional[str]:
    """
    Map our urbanicity labels to WVS urbanicity codes.
    
    Note: WVS cube uses values 1-4 for urbanicity (possibly from H_SETTLEMENT or G_TOWNSIZE2).
    Based on data distribution and H_SETTLEMENT codes:
    - 1 = Capital/Regional center (megacity/city)
    - 2 = District center (city)
    - 3 = Town
    - 4 = Village/Rural
    
    Returns WVS code as string, or None if unknown.
    """
    mapping = {
        "rural": "4",
        "town": "3",
        "city": "2",
        "megacity": "1"
    }
    return mapping.get(urbanicity)


def _map_religion_name_to_wvs_code(religion_name: str, country_code: str) -> Optional[str]:
    """
    Map religion name to WVS religion code.
    
    WVS Q289 uses numeric codes (0-9) that vary by country.
    For now, we'll need to query the database to find the most common code
    for a given religion name in a country, or use a default mapping.
    
    Returns WVS religion code as string, or None if unknown.
    """
    # Common mappings (may need to be country-specific)
    # These are rough approximations - ideally we'd query the database
    common_mappings = {
        "Islam": "1",
        "Christianity": "2",
        "Catholic": "2",
        "Protestant": "2",
        "Hinduism": "3",
        "Buddhism": "4",
        "Judaism": "5",
        "Atheist": "0",
        "None": "0"
    }
    
    # Try direct mapping first
    for key, code in common_mappings.items():
        if key.lower() in religion_name.lower():
            return code
    
    # If no match, return None (will fall back to country-level query)
    return None


def get_driver_vec_with_context(
    country_code: str,
    year: int,
    age: int,
    gender: Optional[str] = None
) -> Tuple[DriverVector, IdentitySkeleton, Dict[str, Any]]:
    """
    Full pipeline: Generate identity context → Query WVS with demographics.
    
    This is the main function that does everything:
    1. Builds identity (location, SES, ethnicity, religion, language)
    2. Queries WVS with all those demographics
    3. Returns driver vector + identity + context
    
    Returns:
        (DriverVector, IdentitySkeleton, context_dict)
    """
    # Generate identity context
    identity, context = generate_identity_context(country_code, year, age, gender)
    
    # Query WVS with all demographics (including education, income, urbanicity)
    driver_vec = get_driver_vec(
        country_code=country_code,
        year=year,
        age=age,
        gender=context["gender"],
        religion=context.get("wvs_religion"),  # WVS religion code
        education=context.get("wvs_education"),  # WVS education code (0-8)
        income=context.get("wvs_income"),  # WVS income code (1-3)
        urbanicity=context.get("wvs_urbanicity")  # WVS urbanicity code (1-4)
    )
    
    return driver_vec, identity, context
