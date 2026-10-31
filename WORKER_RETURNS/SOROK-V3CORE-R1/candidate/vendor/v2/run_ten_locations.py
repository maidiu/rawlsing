"""
Run pipeline for 10 separate locations and compare results.

Each run: different country/region. Parent identity is sampled for that context.
Output: compact summary for plausibility comparison.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from spec import (
    IdentitySkeleton,
    simulate_life_course,
    CohortAdjusters,
)
from data_access import get_world_slice, get_driver_vec, get_local_modifiers

# 10 diverse locations (country, region, locality, urbanicity, birth_year)
LOCATIONS = [
    ("US", "California", "Los Angeles", "city", 1990),
    ("US", "Texas", "Houston", "city", 1985),
    ("GB", "England", "London", "city", 1988),
    ("DE", "Bavaria", "Munich", "city", 1992),
    ("VN", "Ho Chi Minh City", "Ho Chi Minh City", "megacity", 1980),
    ("JP", "Kanto", "Tokyo", "megacity", 1987),
    ("MX", "Mexico City", "Mexico City", "megacity", 1990),
    ("BR", "São Paulo", "São Paulo", "megacity", 1985),
    ("ZA", "Gauteng", "Johannesburg", "city", 1988),
    ("IN", "Maharashtra", "Mumbai", "megacity", 1990),
]


def run_one(i: int, country: str, region: str, locality: str, urbanicity: str, birth_year: int):
    """Run pipeline for one location; return summary dict."""
    identity = IdentitySkeleton(
        internal_id=f"run_ten_{i:02d}",
        given_name="",
        gender="female",
        birth_year=birth_year,
        anchor_year=2025,
        age_at_anchor=2025 - birth_year,
        country_code=country,
        region=region,
        locality=locality,
        urbanicity=urbanicity,
        class_origin="middle",
        current_class="middle",
        ethnicity_label="",
        minority_status="",
        childhood_religion="",
        current_religion="",
        religiosity_level=50.0,
        primary_language="",
    )
    try:
        history = simulate_life_course(
            identity=identity,
            adjusters=CohortAdjusters(),
            constraints=None,
            get_world_slice=get_world_slice,
            get_driver_vec=get_driver_vec,
            get_local_modifiers=get_local_modifiers,
        )
    except Exception as e:
        return {"location": f"{country} {region}", "error": str(e)}

    parent = history.metadata.get("parent_identity") or {}
    loc = parent.get("location", {})
    reg = loc.get("region", {})
    city = loc.get("city", {})
    ethnic = parent.get("ethnicity", {})
    ses = parent.get("ses", {})
    rel = parent.get("religion_language", {})
    father = parent.get("parents", {}).get("father", {})
    mother = parent.get("parents", {}).get("mother", {})

    band = next((b for b in history.band_summaries if b.band == "0-3"), None)
    caregivers = band.micrograph.caregivers if (band and band.micrograph) else []
    f_c = next((c for c in caregivers if c.role == "father"), None)
    m_c = next((c for c in caregivers if c.role == "mother"), None)

    return {
        "location": f"{country} {region}",
        "parent_loc": f"{reg.get('admin1_name', '?')}, {city.get('name', '?')}",
        "urbanicity": loc.get("urbanicity", "?"),
        "ethnicity": ethnic.get("group_name", "?"),
        "ses": ses.get("class_label", "?"),
        "religion": rel.get("religion", "?"),
        "father_age": father.get("age_at_child_birth"),
        "mother_age": mother.get("age_at_child_birth"),
        "gap": parent.get("age_model", {}).get("gap_father_minus_mother"),
        "father_warmth": round(f_c.warmth, 1) if f_c else None,
        "father_authority": round(f_c.authority, 1) if f_c else None,
        "father_material": round(f_c.material_support, 1) if f_c else None,
        "mother_warmth": round(m_c.warmth, 1) if m_c else None,
        "mother_authority": round(m_c.authority, 1) if m_c else None,
        "mother_material": round(m_c.material_support, 1) if m_c else None,
        "enneagram": history.enneagram_profile.primary_type if history.enneagram_profile else None,
        "health": round(history.enneagram_profile.health_level, 1) if history.enneagram_profile else None,
    }


def main():
    print("=" * 100)
    print("RAWLSING - 10 LOCATIONS RUN")
    print("=" * 100)

    results = []
    for i, (country, region, locality, urbanicity, birth_year) in enumerate(LOCATIONS, 1):
        print(f"  [{i}/10] {country} {region}...", end=" ", flush=True)
        r = run_one(i, country, region, locality, urbanicity, birth_year)
        results.append(r)
        if "error" in r:
            print(f"ERROR: {r['error']}")
        else:
            print("ok")

    print("\n" + "=" * 100)
    print("RESULTS")
    print("=" * 100)

    for r in results:
        if "error" in r:
            print(f"\n{r['location']}: ERROR - {r['error']}")
            continue
        print(f"\n--- {r['location']} ---")
        print(f"  Parents: {r['parent_loc']} ({r['urbanicity']})")
        print(f"  Ethnicity: {r['ethnicity']}  |  SES: {r['ses']}  |  Religion: {r['religion']}")
        print(f"  Ages: father {r['father_age']}, mother {r['mother_age']} (gap {r['gap']} yrs)")
        print(f"  Father:  warmth={r['father_warmth']}  authority={r['father_authority']}  material={r['father_material']}")
        print(f"  Mother:  warmth={r['mother_warmth']}  authority={r['mother_authority']}  material={r['mother_material']}")
        print(f"  Enneagram: {r['enneagram']}  Health: {r['health']}")

    print("\n" + "=" * 100)


if __name__ == "__main__":
    main()
