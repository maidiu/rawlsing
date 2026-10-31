"""
Minimal test to verify the Rawlsing pipeline works.

This script:
1. Creates a simple identity
2. Runs the simulation
3. Prints results

No barometer data needed - just WVS (or defaults if WVS unavailable).
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

def main():
    print("=" * 80)
    print("RAWLSING PIPELINE - MINIMAL TEST")
    print("=" * 80)
    print()
    
    # Create a simple identity
    print("Creating identity...")
    identity = IdentitySkeleton(
        internal_id="minimal_test_001",
        given_name="Test",
        gender="female",
        birth_year=1990,
        anchor_year=2025,
        age_at_anchor=35,
        country_code="US",  # Use US for likely WVS coverage
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
    print(f"✅ Identity created: {identity.given_name}, born {identity.birth_year}")
    print()
    
    # Try to run simulation
    print("Running simulation...")
    try:
        history = simulate_life_course(
            identity=identity,
            adjusters=CohortAdjusters(),
            constraints=None,
            get_world_slice=get_world_slice,
            get_driver_vec=get_driver_vec,
            get_local_modifiers=get_local_modifiers
        )
        
        print(f"✅ Simulation complete!")
        print(f"   Years simulated: {len(history.yearly_states)}")
        print(f"   Age bands: {len(history.band_summaries)}")
        
        if history.enneagram_profile:
            print(f"   Enneagram: {history.enneagram_profile.primary_type}")
            print(f"   Health: {history.enneagram_profile.health_level:.1f}")
        
        # Show a few key states
        print()
        print("Sample states:")
        if len(history.yearly_states) > 0:
            birth = history.yearly_states[0]
            print(f"   Birth (age 0):")
            print(f"      Needs - Belonging: {birth.needs.belonging_group:.1f}, Safety: {birth.needs.safety:.1f}")
            print(f"      DRTS: {birth.indices.drts:.1f}, RMT: {birth.indices.recursive_madness_threshold:.1f}")
        
        if len(history.yearly_states) > 10:
            age_10 = history.yearly_states[10]
            print(f"   Age 10:")
            print(f"      Needs - Belonging: {age_10.needs.belonging_group:.1f}, Safety: {age_10.needs.safety:.1f}")
            print(f"      DRTS: {age_10.indices.drts:.1f}, RMT: {age_10.indices.recursive_madness_threshold:.1f}")
        
        if len(history.yearly_states) > 20:
            age_20 = history.yearly_states[20]
            print(f"   Age 20:")
            print(f"      Needs - Belonging: {age_20.needs.belonging_group:.1f}, Safety: {age_20.needs.safety:.1f}")
            print(f"      DRTS: {age_20.indices.drts:.1f}, RMT: {age_20.indices.recursive_madness_threshold:.1f}")
        
        # Build persona sheet
        print()
        print("Building persona sheet...")
        persona_sheet = build_persona_sheet(history)
        
        # Save to file
        output_file = "minimal_test_output.json"
        with open(output_file, "w") as f:
            json.dump(persona_sheet, f, indent=2, default=str)
        
        print(f"✅ Persona sheet saved to {output_file}")
        print()
        print("=" * 80)
        print("SUCCESS: Pipeline is working!")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("Troubleshooting:")
        print("1. Check database connection in config/config.yaml")
        print("2. Verify driver_aggregates table exists")
        print("3. Set PGPASSWORD environment variable if needed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
