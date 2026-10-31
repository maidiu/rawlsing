"""
Test: Generate parents for child born in 1960 Vietnam, simulate to age 7.

This is a demonstration script. Canonical parent generation lives in:
    identity_generator.generate_parent_identities()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import random
from typing import Dict, Any

from identity_generator import (
    generate_parent_identities,
)
from data_access import get_driver_vec, get_world_slice, get_local_modifiers
from spec import (
    IdentitySkeleton, simulate_life_course,
    PersonaHistory, CohortAdjusters
)


def generate_parent_identity_vietnam_1960() -> Dict[str, Any]:
    """Generate parent identity for child born in 1960 Vietnam."""
    country_code = "VN"
    year = 1960

    print("=" * 80)
    print("GENERATING PARENT IDENTITY FOR CHILD BORN IN 1960 VIETNAM")
    print("=" * 80)

    parent_identity = generate_parent_identities(
        country_code=country_code,
        child_birth_year=year,
        allow_story_reasons=False,
        fixed_parent_genders=("male", "female"),
        enforce_father_older=True,
    )

    location = parent_identity["location"]
    ethnic = parent_identity["ethnicity"]
    rel_lang = parent_identity["religion_language"]
    ses = parent_identity["ses"]
    father = parent_identity["parents"]["father"]
    mother = parent_identity["parents"]["mother"]
    age_meta = parent_identity["age_model"]

    print("\n1. LOCATION...")
    print(
        f"   ✅ Location: {location.get('region', {}).get('admin1_name', 'Unknown')}, "
        f"{location.get('city', {}).get('name', 'Unknown')}"
    )
    print(f"      Urbanicity: {location.get('urbanicity', 'unknown')}")

    print("\n2. ETHNICITY...")
    print(f"   ✅ Ethnicity: {ethnic.get('group_name', 'Unknown')}")
    print(f"      Power Status: {ethnic.get('power_status', 'unknown')}")
    print(f"      Size: {ethnic.get('size', 0):.1%}")

    print("\n3. RELIGION & LANGUAGE...")
    print(f"   ✅ Religion: {rel_lang.get('religion', 'Unknown')}")
    print(f"      Language: {rel_lang.get('primary_language', 'Unknown')}")

    print("\n4. SES...")
    print(f"   ✅ SES: {ses.get('class_label', 'Unknown')} (decile: {ses.get('decile', 'N/A')})")

    print("\n5. PARENT GENDERS...")
    print(f"   ✅ Father: {father.get('gender')}")
    print(f"      Mother: {mother.get('gender')}")

    print("\n6. PARENT AGES (at child's birth in 1960)...")
    print(f"   ✅ Mother: Age {mother['age_at_child_birth']} (born ~{mother['birth_year']})")
    print(f"      Father: Age {father['age_at_child_birth']} (born ~{father['birth_year']})")
    print(
        f"      Gap (father - mother): {age_meta.get('gap_father_minus_mother')} years "
        f"[{age_meta['gap_component']}], resamples={age_meta['resamples']}"
    )

    print("\n✅ PARENT IDENTITY GENERATED")

    # Legacy shape used by the rest of this test script
    return {
        "location": location,
        "ethnicity": ethnic,
        "religion_language": rel_lang,
        "ses": ses,
        "parent1": {
            "gender": father.get("gender"),
            "age": father.get("age_at_child_birth"),
            "birth_year": father.get("birth_year"),
        },
        "parent2": {
            "gender": mother.get("gender"),
            "age": mother.get("age_at_child_birth"),
            "birth_year": mother.get("birth_year"),
        },
        "age_model": age_meta,
    }


def create_persona_identity_from_parents(parent_identity: Dict[str, Any], birth_year: int = 1960) -> IdentitySkeleton:
    """Create persona identity from parent identity."""
    location = parent_identity["location"]
    ethnic = parent_identity["ethnicity"]
    rel_lang = parent_identity["religion_language"]
    ses = parent_identity["ses"]

    persona_gender = random.choice(["male", "female"])

    return IdentitySkeleton(
        internal_id=f"VN_1960_{random.randint(1000, 9999)}",
        given_name="",
        gender=persona_gender,
        birth_year=birth_year,
        anchor_year=1967,
        age_at_anchor=7,
        country_code="VN",
        region=location.get("region", {}).get("admin1_name", "") if location.get("region") else "",
        locality=location.get("city", {}).get("name", "") if location.get("city") else "",
        urbanicity=location.get("urbanicity", "rural"),
        class_origin=ses.get("class_label", "working"),
        current_class=ses.get("class_label", "working"),
        ethnicity_label=ethnic.get("group_name", "Unknown"),
        minority_status="dominant" if ethnic.get("power_status") == "dominant" else "minoritized",
        childhood_religion=rel_lang.get("religion", "Unknown"),
        current_religion=rel_lang.get("religion", "Unknown"),
        primary_language=rel_lang.get("primary_language", "Unknown"),
        secondary_languages=rel_lang.get("secondary_languages", []),
    )


def simulate_to_age_7(identity: IdentitySkeleton) -> PersonaHistory:
    """Simulate persona from birth to age 7."""
    print("\n" + "=" * 80)
    print("SIMULATING PERSONA FROM BIRTH TO AGE 7 (1960-1967)")
    print("=" * 80)

    def get_world_slice_func(country_code: str, year: int):
        return get_world_slice(country_code, year)

    def get_driver_vec_func(country_code: str, year: int, age: int, **kwargs):
        return get_driver_vec(country_code=country_code, year=year, age=age, **kwargs)

    history = simulate_life_course(
        identity=identity,
        adjusters=CohortAdjusters(),
        constraints=None,
        get_world_slice=get_world_slice_func,
        get_driver_vec=get_driver_vec_func,
        get_local_modifiers=get_local_modifiers,
    )

    return history


def main() -> None:
    parent_identity = generate_parent_identity_vietnam_1960()
    identity = create_persona_identity_from_parents(parent_identity, birth_year=1960)

    print("\n👶 PERSONA IDENTITY:")
    print(f"   Gender: {identity.gender}")
    print(f"   Birth Year: {identity.birth_year}")
    print(f"   Location: {identity.locality}, {identity.region}")
    print(f"   Ethnicity: {identity.ethnicity_label}")
    print(f"   Religion: {identity.current_religion}")
    print(f"   Language: {identity.primary_language}")
    print(f"   SES: {identity.class_origin}")

    history = simulate_to_age_7(identity)

    print("\n✅ Simulation complete!")


if __name__ == "__main__":
    main()

