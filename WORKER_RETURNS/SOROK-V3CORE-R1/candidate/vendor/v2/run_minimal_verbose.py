"""
Run pipeline with full demographic and parent context for plausibility audit.

Prints: persona identity, parent identity (location, ethnicity, SES, religion,
parent ages, WVS codes), and resulting caregiver warmth/authority/material_support
so you can evaluate whether the pipeline renders plausible outputs.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from spec import (
    IdentitySkeleton,
    simulate_life_course,
    CohortAdjusters,
    build_persona_sheet
)
from data_access import get_world_slice, get_driver_vec, get_local_modifiers
import json


def _pp(obj, indent=2):
    """Pretty-print for JSON-serializable objects."""
    return json.dumps(obj, indent=indent, default=str)


def main():
    print("=" * 80)
    print("RAWLSING PIPELINE - VERBOSE RUN (PLAUSIBILITY AUDIT)")
    print("=" * 80)

    # Same identity as run_minimal
    identity = IdentitySkeleton(
        internal_id="minimal_test_001",
        given_name="Test",
        gender="female",
        birth_year=1990,
        anchor_year=2025,
        age_at_anchor=35,
        country_code="US",
        region="California",
        locality="Los Angeles",
        urbanicity="city",
        class_origin="middle",
        current_class="middle",
        ethnicity_label="white",
        minority_status="dominant",
        childhood_religion="Christian",
        current_religion="Christian",
        religiosity_level=50.0,
        primary_language="English"
    )

    print("\n1. PERSONA IDENTITY (who we're simulating)")
    print("-" * 40)
    print(f"   Country:        {identity.country_code}")
    print(f"   Region:         {identity.region}")
    print(f"   Locality:       {identity.locality}")
    print(f"   Urbanicity:     {identity.urbanicity}")
    print(f"   Birth year:     {identity.birth_year}")
    print(f"   Gender:         {identity.gender}")
    print(f"   Ethnicity:      {identity.ethnicity_label}")
    print(f"   Religion:       {identity.childhood_religion}")
    print(f"   Class origin:   {identity.class_origin}")
    print(f"   Language:       {identity.primary_language}")

    print("\n2. RUNNING SIMULATION...")
    history = simulate_life_course(
        identity=identity,
        adjusters=CohortAdjusters(),
        constraints=None,
        get_world_slice=get_world_slice,
        get_driver_vec=get_driver_vec,
        get_local_modifiers=get_local_modifiers
    )
    print("   Done.")

    parent_identity = history.metadata.get("parent_identity")
    if parent_identity:
        print("\n3. PARENT IDENTITY (household context at child's birth)")
        print("-" * 40)
        loc = parent_identity.get("location", {})
        region = loc.get("region", {})
        city = loc.get("city", {})
        print(f"   Location:       {region.get('admin1_name', '?')}, {city.get('name', '?')}")
        print(f"   Urbanicity:     {loc.get('urbanicity', '?')}")

        ethnic = parent_identity.get("ethnicity", {})
        pwr = ethnic.get("power_status") or ethnic.get("epr_power_status", "?")
        print(f"   Ethnicity:      {ethnic.get('group_name', '?')} (power: {pwr})")

        ses = parent_identity.get("ses", {})
        print(f"   SES:            {ses.get('class_label', '?')} (decile {ses.get('decile', '?')})")

        rel = parent_identity.get("religion_language", {})
        print(f"   Religion:       {rel.get('religion', '?')}")
        print(f"   Language:       {rel.get('primary_language', '?')}")

        father = parent_identity.get("parents", {}).get("father", {})
        mother = parent_identity.get("parents", {}).get("mother", {})
        print(f"\n   Father:  age {father.get('age_at_child_birth')} at birth, WVS edu={father.get('wvs_education')} rel={father.get('wvs_religion')} income={father.get('wvs_income')}")
        print(f"   Mother:  age {mother.get('age_at_child_birth')} at birth, WVS edu={mother.get('wvs_education')} rel={mother.get('wvs_religion')} income={mother.get('wvs_income')}")

        age_meta = parent_identity.get("age_model", {})
        print(f"   Age gap (father - mother): {age_meta.get('gap_father_minus_mother')} yrs [{age_meta.get('gap_component', '?')}]")
    else:
        print("\n3. PARENT IDENTITY: (not available - WVS/parent generation may have failed)")

    # Caregivers from first band (0-3)
    band_0_3 = next((b for b in history.band_summaries if b.band == "0-3"), None)
    if band_0_3 and band_0_3.micrograph and band_0_3.micrograph.caregivers:
        print("\n4. CAREGIVER BEHAVIOR (sampled from WVS → parent behavior mapping)")
        print("-" * 40)
        for c in band_0_3.micrograph.caregivers:
            print(f"   {c.role}:  warmth={c.warmth:.1f}  authority={c.authority:.1f}  material_support={c.material_support:.1f}")
        print("\n   (0–100 scale; warmth=emotional responsiveness, authority=rule enforcement, material_support=provision)")
    else:
        print("\n4. CAREGIVER BEHAVIOR: (no caregivers in band 0-3)")

    # Note persona vs parent alignment (they may differ if persona identity is fixed)
    print("\n   NOTE: Persona identity (section 1) may be fixed; parent identity (section 3)")
    print("   is sampled for (country, birth_year). For full alignment, generate persona from parents.")

    print("\n5. ENNEAGRAM RESULT")
    print("-" * 40)
    if history.enneagram_profile:
        print(f"   Type: {history.enneagram_profile.primary_type}, Health: {history.enneagram_profile.health_level:.1f}")
    else:
        print("   (none)")

    # Save full output including metadata
    persona_sheet = build_persona_sheet(history)
    persona_sheet["_metadata"] = history.metadata
    output_file = "minimal_test_verbose_output.json"
    with open(output_file, "w") as f:
        json.dump(persona_sheet, f, indent=2, default=str)
    print(f"\n   Full output saved to {output_file}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
