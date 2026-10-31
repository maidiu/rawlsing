#!/usr/bin/env python3
"""
Query respondents matching persona demographics from survey microdata.

Supports WVS (implemented); EVS and barometers when loaded with survey_demographic_schema.

Usage: python query_persona_slice.py

Persona: lebanon, urban, lower income, high school, male, over 35, sunni
WVS: LBN, urban=1, income=1 (Q288R low), education=3 (ISCED upper secondary),
     sex=1 (male), age>=35, religion=5 (Muslim; WVS has no Sunni/Shia split)

Schema: v2/data/survey_demographic_schema.yaml
Architecture: v2/PERSONA_SLICE_PIPELINE_ARCHITECTURE.md
"""

import os
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional

# Determinicity order (most → least): urban_rural, income, education, sex, age, religion
# Broadening drops in reverse order: religion, age, sex, education, income, urban_rural

BROADEN_ORDER = ["religion", "age", "sex", "education", "income", "urban_rural"]

_SCHEMA_PATH = Path(__file__).parent / "data" / "survey_demographic_schema.yaml"


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="Rawlsing—WVS",
        user="postgres",
        password=os.getenv("PGPASSWORD", "rocketsauce"),
    )


def get_matching_respondents(
    conn,
    country: str = "LBN",
    urban_rural: Optional[str] = "1",
    income: Optional[str] = "1",
    education: Optional[str] = "3",
    sex: Optional[str] = "1",
    religion: Optional[str] = "5",
    min_age: Optional[int] = 35,
    min_n: int = 20,
) -> tuple[List[Dict[str, Any]], str]:
    """
    Query respondent_ids matching demographics. Broadens if N < min_n.
    Returns (list of dicts with respondent_id + demographics, match_level).
    """
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Base CTE: pivot responses to get demographics per respondent
    base_sql = """
    WITH demo AS (
        SELECT r.respondent_id, r.country_code, r.urban_rural,
               MAX(CASE WHEN rs.var_code = 'Q262' THEN rs.value_raw::numeric END) AS age,
               MAX(CASE WHEN rs.var_code = 'Q260' THEN rs.value_raw::numeric END) AS sex,
               MAX(CASE WHEN rs.var_code = 'Q275' THEN rs.value_raw::numeric END) AS education,
               MAX(CASE WHEN rs.var_code = 'Q288R' THEN rs.value_raw::numeric END) AS income,
               MAX(CASE WHEN rs.var_code = 'Q289' THEN rs.value_raw::numeric END) AS religion
        FROM respondents r
        JOIN responses rs ON r.respondent_id = rs.respondent_id
        WHERE r.country_code = %(country)s
          AND rs.var_code IN ('Q262','Q260','Q275','Q288R','Q289')
        GROUP BY r.respondent_id, r.country_code, r.urban_rural
    )
    """

    # Try exact match first
    where_parts = ["age >= %(min_age)s", "age IS NOT NULL", "age BETWEEN 0 AND 120"]
    params = {"country": country, "min_age": min_age or 0}

    if urban_rural:
        where_parts.append("urban_rural = %(urban_rural)s")
        params["urban_rural"] = urban_rural
    if income is not None:
        where_parts.append("income = %(income)s")
        params["income"] = int(income)
    if education is not None:
        where_parts.append("education = %(education)s")
        params["education"] = int(education)
    if sex is not None:
        where_parts.append("sex = %(sex)s")
        params["sex"] = int(sex)
    if religion is not None:
        where_parts.append("religion = %(religion)s")
        params["religion"] = int(religion)

    cur.execute(
        base_sql
        + " SELECT respondent_id, country_code, urban_rural, age, sex, education, income, religion FROM demo WHERE "
        + " AND ".join(where_parts)
        + " ORDER BY respondent_id",
        params,
    )
    rows = cur.fetchall()
    cur.close()

    if len(rows) >= min_n:
        return [dict(r) for r in rows], "full"

    # Broadening: drop constraints one at a time (religion first, then age, sex, etc.)
    filters = {
        "urban_rural": urban_rural,
        "income": income,
        "education": education,
        "sex": sex,
        "religion": religion,
        "age": min_age,
    }
    dropped = []
    for drop in BROADEN_ORDER:
        filters[drop] = None
        dropped.append(drop)

        where_parts = ["age IS NOT NULL", "age BETWEEN 0 AND 120"]
        params = {"country": country}

        if filters.get("age") is not None:
            where_parts.append("age >= %(min_age)s")
            params["min_age"] = filters["age"]
        if filters.get("urban_rural"):
            where_parts.append("urban_rural = %(urban_rural)s")
            params["urban_rural"] = filters["urban_rural"]
        if filters.get("income") is not None:
            where_parts.append("income = %(income)s")
            params["income"] = filters["income"]
        if filters.get("education") is not None:
            where_parts.append("education = %(education)s")
            params["education"] = filters["education"]
        if filters.get("sex") is not None:
            where_parts.append("sex = %(sex)s")
            params["sex"] = filters["sex"]
        if filters.get("religion") is not None:
            where_parts.append("religion = %(religion)s")
            params["religion"] = filters["religion"]

        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            base_sql
            + " SELECT respondent_id, country_code, urban_rural, age, sex, education, income, religion FROM demo WHERE "
            + " AND ".join(where_parts)
            + " ORDER BY respondent_id",
            params,
        )
        rows = cur.fetchall()
        cur.close()

        if len(rows) >= min_n:
            return [dict(r) for r in rows], "dropped_" + "_".join(dropped)

    return [dict(r) for r in rows], "broadest"


def get_slice_distributions(
    conn,
    respondent_ids: List[int],
    source: str = "WVS",
) -> Dict[str, Any]:
    """
    Extract distributions from a respondent slice for parent weighting.

    Returns:
        - education_by_male: {age_bucket: {education_level: count}} for males
        - education_by_female: same for females
        - religion_dist: {religion_code: count}
        - age_gender_counts: {(age_bucket, sex): count}

    Used to weight probabilistic parent generation: sample education from
    education_by_male/education_by_female for parent age range.
    """
    if not respondent_ids:
        return {
            "education_by_male": {},
            "education_by_female": {},
            "religion_dist": {},
            "age_gender_counts": {},
            "n": 0,
        }

    # WVS var_codes
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        WITH demo AS (
            SELECT r.respondent_id,
                   MAX(CASE WHEN rs.var_code = 'Q262' THEN rs.value_raw::numeric END) AS age,
                   MAX(CASE WHEN rs.var_code = 'Q260' THEN rs.value_raw::numeric END) AS sex,
                   MAX(CASE WHEN rs.var_code = 'Q275' THEN rs.value_raw::numeric END) AS education,
                   MAX(CASE WHEN rs.var_code = 'Q289' THEN rs.value_raw::numeric END) AS religion
            FROM respondents r
            JOIN responses rs ON r.respondent_id = rs.respondent_id
            WHERE r.respondent_id = ANY(%s)
              AND rs.var_code IN ('Q262','Q260','Q275','Q289')
            GROUP BY r.respondent_id
        )
        SELECT age, sex, education, religion
        FROM demo
        WHERE age IS NOT NULL AND age BETWEEN 0 AND 120
        """,
        (respondent_ids,),
    )
    rows = cur.fetchall()
    cur.close()

    def age_bucket(age: float) -> str:
        if age < 25:
            return "18-24"
        if age < 35:
            return "25-34"
        if age < 45:
            return "35-44"
        if age < 55:
            return "45-54"
        return "55+"

    education_by_male: Dict[str, Dict[int, int]] = {}
    education_by_female: Dict[str, Dict[int, int]] = {}
    religion_dist: Dict[int, int] = {}
    age_gender_counts: Dict[tuple, int] = {}

    for r in rows:
        age = float(r["age"]) if r["age"] is not None else None
        sex = int(r["sex"]) if r["sex"] is not None else None
        education = int(r["education"]) if r["education"] is not None and r["education"] >= 0 else None
        religion = int(r["religion"]) if r["religion"] is not None and r["religion"] >= 0 else None

        if age is None:
            continue

        bucket = age_bucket(age)
        key = (bucket, sex)

        age_gender_counts[key] = age_gender_counts.get(key, 0) + 1

        if religion is not None:
            religion_dist[religion] = religion_dist.get(religion, 0) + 1

        if education is not None and sex is not None:
            target = education_by_male if sex == 1 else education_by_female
            if bucket not in target:
                target[bucket] = {}
            target[bucket][education] = target[bucket].get(education, 0) + 1

    return {
        "education_by_male": education_by_male,
        "education_by_female": education_by_female,
        "religion_dist": religion_dist,
        "age_gender_counts": dict(age_gender_counts),
        "n": len(rows),
    }


def load_demographic_schema() -> Optional[Dict]:
    """Load survey_demographic_schema.yaml if present."""
    if not _SCHEMA_PATH.exists():
        return None
    try:
        import yaml
        with open(_SCHEMA_PATH) as f:
            return yaml.safe_load(f)
    except Exception:
        return None


if __name__ == "__main__":
    conn = get_connection()
    try:
        rows, level = get_matching_respondents(
            conn,
            country="LBN",
            urban_rural="1",
            income="1",
            education="3",
            sex="1",
            religion="5",
            min_age=35,
            min_n=20,
        )
        print(f"Match level: {level}")
        print(f"Found {len(rows)} respondents")
        if rows:
            print("\nFirst 10:")
            for r in rows[:10]:
                print(r)
            if len(rows) > 10:
                print(f"... and {len(rows) - 10} more")
            print("\nRespondent IDs:", [r["respondent_id"] for r in rows])

            # Extract distributions for parent weighting
            ids = [r["respondent_id"] for r in rows]
            dist = get_slice_distributions(conn, ids)
            print("\n--- Slice distributions (for parent weighting) ---")
            print("Education by male (age_bucket -> {edu_level: count}):", dist["education_by_male"])
            print("Education by female:", dist["education_by_female"])
            print("Religion dist:", dist["religion_dist"])
            print("Age-gender counts:", dist["age_gender_counts"])
    finally:
        conn.close()
