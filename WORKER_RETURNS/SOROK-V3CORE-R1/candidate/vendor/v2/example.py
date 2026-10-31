"""
Example usage of Rawlsing v4.1 simulation engine

This demonstrates how to use the spec to generate a persona.
"""

from spec import (
    IdentitySkeleton,
    simulate_life_course,
    CohortAdjusters,
    PersonaConstraints,
    build_persona_sheet,
    get_world_slice,
    get_driver_vec,
    get_local_modifiers
)
import json

# Example: Generate a persona
def example_generate_persona():
    # Define identity
    identity = IdentitySkeleton(
        internal_id="example_001",
        given_name="Maria",
        gender="female",
        birth_year=1985,
        anchor_year=2025,
        age_at_anchor=40,
        country_code="MEX",
        region="Jalisco",
        locality="Guadalajara",
        urbanicity="city",
        class_origin="working",
        current_class="lower_middle",
        ethnicity_label="mestizo",
        minority_status="dominant",
        childhood_religion="Catholic",
        current_religion="Catholic",
        religiosity_level=70.0,
        primary_language="Spanish"
    )
    
    # Define adjusters (for birth sampling)
    adjusters = CohortAdjusters(
        global_south_only=False,
        reduce_india_china=0.0,
        minority_only=False
    )
    
    # Define constraints (optional end-state constraints)
    constraints = PersonaConstraints()
    
    # Simulate life course
    # Note: get_world_slice, get_driver_vec, get_local_modifiers need to be implemented
    # For now, these will raise NotImplementedError
    try:
        history = simulate_life_course(
            identity,
            adjusters=adjusters,
            constraints=constraints,
            get_world_slice=get_world_slice,
            get_driver_vec=get_driver_vec,
            get_local_modifiers=get_local_modifiers
        )
        
        print(f"✅ Generated {len(history.yearly_states)} yearly states")
        print(f"✅ Aggregated into {len(history.band_summaries)} age bands")
        
        if history.enneagram_profile:
            print(f"✅ Enneagram type: {history.enneagram_profile.primary_type}")
            print(f"   Health level: {history.enneagram_profile.health_level:.1f}")
        
        # Build persona sheet for LLM
        persona_sheet = build_persona_sheet(history)
        
        # Export to JSON
        with open("persona_sheet_example.json", "w") as f:
            json.dump(persona_sheet, f, indent=2, default=str)
        
        print("✅ Persona sheet exported to persona_sheet_example.json")
        
        return history
        
    except NotImplementedError as e:
        print(f"⚠️  Data access functions not implemented: {e}")
        print("   Implement get_world_slice, get_driver_vec, get_local_modifiers")
        return None


if __name__ == "__main__":
    example_generate_persona()

