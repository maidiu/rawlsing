"""
Test script for config loader and config-driven update functions
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_loader import get_config_loader, ConfigLoader
from spec import (
    IdentitySkeleton, NeedGradients, StrategyPortfolio, CivicSoulConditions,
    WorldSlice, DriverVector, LocalModifiers, RelationalGraph, RelationalNode,
    RelationalRoleType, CognitiveProfile, update_needs, update_strategies,
    compute_civic_soul, clamp
)


def test_config_loader_basic():
    """Test basic config loading"""
    print("=" * 60)
    print("Test 1: Basic Config Loading")
    print("=" * 60)
    
    loader = get_config_loader()
    
    # Test loading needs config
    needs_config = loader.get("needs", "needs", {})
    assert needs_config, "Needs config should be loaded"
    print(f"✅ Loaded {len(needs_config)} needs from config")
    
    # Test loading strategies config
    strategies_config = loader.get("strategies", "strategies", {})
    assert strategies_config, "Strategies config should be loaded"
    print(f"✅ Loaded {len(strategies_config)} strategies from config")
    
    # Test loading civic_soul config
    civic_soul_config = loader.get("civic_soul", "civic_soul", {})
    assert civic_soul_config, "Civic soul config should be loaded"
    print(f"✅ Loaded {len(civic_soul_config)} civic soul conditions from config")
    
    # Test getting specific need config
    safety_config = loader.get_needs_config("safety")
    assert safety_config, "Should get safety config"
    assert "description" in safety_config, "Safety config should have description"
    print(f"✅ Safety config loaded: {safety_config.get('description', '')[:50]}...")
    
    print("✅ All basic config loading tests passed!\n")


def test_path_evaluation():
    """Test path-based evaluation"""
    print("=" * 60)
    print("Test 2: Path-Based Evaluation")
    print("=" * 60)
    
    loader = get_config_loader()
    
    # Create test context
    world_slice = WorldSlice(
        year=2020,
        country_code="MEX",
        conflict_intensity=60.0,
        state_repression=40.0,
        inequality_index=55.0,
        unemployment_level=30.0,
        gdp_per_capita=10000.0,
        welfare_support=50.0,
        media_saturation=70.0,
        propaganda_saturation=50.0
    )
    
    needs = NeedGradients(safety=50.0, warmth_bonding=40.0)
    identity = IdentitySkeleton(
        internal_id="test_001",
        given_name="Test",
        gender="male",
        birth_year=2000,
        country_code="MEX",
        current_class="working"
    )
    
    context = {
        "world_slice": world_slice,
        "needs": needs,
        "identity": identity
    }
    
    # Test evaluating paths
    conflict = loader.evaluate_path("world_slice.conflict_intensity", context)
    assert conflict == 60.0, f"Expected 60.0, got {conflict}"
    print(f"✅ Evaluated world_slice.conflict_intensity = {conflict}")
    
    safety = loader.evaluate_path("needs.safety", context)
    assert safety == 50.0, f"Expected 50.0, got {safety}"
    print(f"✅ Evaluated needs.safety = {safety}")
    
    gender = loader.evaluate_path("identity.gender", context)
    assert gender == "male", f"Expected 'male', got {gender}"
    print(f"✅ Evaluated identity.gender = {gender}")
    
    print("✅ All path evaluation tests passed!\n")


def test_condition_evaluation():
    """Test condition evaluation"""
    print("=" * 60)
    print("Test 3: Condition Evaluation")
    print("=" * 60)
    
    loader = get_config_loader()
    
    world_slice = WorldSlice(
        year=2020,
        country_code="MEX",
        conflict_intensity=60.0,
        state_repression=40.0,
        inequality_index=55.0,
        unemployment_level=30.0,
        gdp_per_capita=10000.0,
        welfare_support=50.0,
        media_saturation=70.0,
        propaganda_saturation=50.0
    )
    
    needs = NeedGradients(safety=30.0, warmth_bonding=40.0, recognition_status=35.0)
    identity = IdentitySkeleton(
        internal_id="test_001",
        given_name="Test",
        gender="male",
        birth_year=2000,
        country_code="MEX",
        current_class="working"
    )
    
    context = {
        "world_slice": world_slice,
        "needs": needs,
        "identity": identity
    }
    
    # Test conditions
    condition1 = "needs.safety < 40"
    result1 = loader.evaluate_condition(condition1, context)
    assert result1 == True, f"Expected True, got {result1}"
    print(f"✅ Condition '{condition1}' = {result1}")
    
    condition2 = "needs.safety > 50"
    result2 = loader.evaluate_condition(condition2, context)
    assert result2 == False, f"Expected False, got {result2}"
    print(f"✅ Condition '{condition2}' = {result2}")
    
    condition3 = "identity.gender == 'male'"
    result3 = loader.evaluate_condition(condition3, context)
    assert result3 == True, f"Expected True, got {result3}"
    print(f"✅ Condition '{condition3}' = {result3}")
    
    condition4 = "world_slice.conflict_intensity > 50"
    result4 = loader.evaluate_condition(condition4, context)
    assert result4 == True, f"Expected True, got {result4}"
    print(f"✅ Condition '{condition4}' = {result4}")
    
    print("✅ All condition evaluation tests passed!\n")


def test_update_needs():
    """Test update_needs with config"""
    print("=" * 60)
    print("Test 4: update_needs() with Config")
    print("=" * 60)
    
    # Create test data
    prev_needs = NeedGradients(
        safety=50.0,
        warmth_bonding=40.0,
        coherence_meaning=50.0,
        bodily_comfort=60.0,
        belonging_group=50.0,
        recognition_status=50.0,
        competence_effectiveness=50.0,
        autonomy_agency=50.0,
        play_pleasure=50.0,
        transcendence_sacred=50.0
    )
    
    civic_soul = CivicSoulConditions(
        rootedness=50.0,
        perceived_justice_order=50.0,
        obligation_symmetry=50.0,
        rehabilitative_punishment_norms=50.0,
        hierarchy_legitimacy=50.0,
        shared_stake_in_common_goods=50.0,
        risk_band=30.0
    )
    
    # Create a simple relational graph with a caregiver
    caregiver = RelationalNode(
        node_id="mother_001",
        role="mother",
        role_type=RelationalRoleType.PRIMARY_CAREGIVER,
        warmth=70.0,
        harshness=20.0,
        reliability=80.0,
        authority=60.0
    )
    relations = RelationalGraph(nodes={"mother_001": caregiver})
    
    strategies = StrategyPortfolio(piety_ideology=60.0)
    
    world_slice = WorldSlice(
        year=2020,
        country_code="MEX",
        conflict_intensity=40.0,  # Moderate conflict
        state_repression=30.0,
        inequality_index=50.0,
        unemployment_level=25.0,
        gdp_per_capita=10000.0,
        welfare_support=50.0,
        media_saturation=60.0,
        propaganda_saturation=40.0
    )
    
    # Update needs
    updated_needs = update_needs(prev_needs, civic_soul, relations, strategies, world_slice)
    
    # Verify all needs are updated and within bounds
    assert updated_needs.safety >= 0 and updated_needs.safety <= 100, "Safety out of bounds"
    assert updated_needs.warmth_bonding >= 0 and updated_needs.warmth_bonding <= 100, "Warmth out of bounds"
    
    print(f"✅ Updated needs:")
    print(f"   Safety: {prev_needs.safety:.1f} → {updated_needs.safety:.1f}")
    print(f"   Warmth bonding: {prev_needs.warmth_bonding:.1f} → {updated_needs.warmth_bonding:.1f}")
    print(f"   Coherence meaning: {prev_needs.coherence_meaning:.1f} → {updated_needs.coherence_meaning:.1f}")
    
    # With moderate conflict and warm caregiver, safety should be reasonable
    assert updated_needs.safety > 30, "Safety should be reasonable with moderate conflict"
    assert updated_needs.warmth_bonding > prev_needs.warmth_bonding, "Warmth should increase with warm caregiver"
    
    print("✅ All update_needs tests passed!\n")


def test_update_strategies():
    """Test update_strategies with config"""
    print("=" * 60)
    print("Test 5: update_strategies() with Config")
    print("=" * 60)
    
    prev_strategies = StrategyPortfolio(
        piety_ideology=30.0,
        aggression_outward=20.0,
        compliance_obedience=40.0
    )
    
    needs = NeedGradients(
        warmth_bonding=30.0,  # Low warmth
        recognition_status=35.0,  # Low recognition
        safety=50.0,
        coherence_meaning=40.0
    )
    
    cognitive = CognitiveProfile()
    identity = IdentitySkeleton(
        internal_id="test_001",
        given_name="Test",
        gender="male",
        birth_year=2000,
        country_code="MEX",
        current_class="working",
        religiosity_level=50.0
    )
    
    world_slice = WorldSlice(
        year=2020,
        country_code="MEX",
        conflict_intensity=65.0,  # High conflict
        state_repression=50.0,
        inequality_index=55.0,
        unemployment_level=30.0,
        gdp_per_capita=10000.0,
        welfare_support=50.0,
        media_saturation=60.0,
        propaganda_saturation=50.0
    )
    
    civic_soul = CivicSoulConditions(
        rootedness=40.0,  # Moderate rootedness (church available)
        perceived_justice_order=50.0,
        obligation_symmetry=50.0,
        rehabilitative_punishment_norms=50.0,
        hierarchy_legitimacy=50.0,
        shared_stake_in_common_goods=50.0,
        risk_band=50.0
    )
    
    # Update strategies
    updated_strategies = update_strategies(
        prev_strategies, needs, cognitive, identity, world_slice, civic_soul
    )
    
    print(f"✅ Updated strategies:")
    print(f"   Piety ideology: {prev_strategies.piety_ideology:.1f} → {updated_strategies.piety_ideology:.1f}")
    print(f"   Aggression outward: {prev_strategies.aggression_outward:.1f} → {updated_strategies.aggression_outward:.1f}")
    assert 0 <= updated_strategies.piety_ideology <= 100, "Piety ideology should stay in range"
    assert 0 <= updated_strategies.aggression_outward <= 100, "Aggression outward should stay in range"
    assert 0 <= updated_strategies.compliance_obedience <= 100, "Compliance obedience should stay in range"
    
    # With low warmth and moderate rootedness, piety should potentially increase
    # With low recognition, male, and high conflict, aggression might increase
    print("✅ All update_strategies tests passed!\n")


def test_compute_civic_soul():
    """Test compute_civic_soul with config"""
    print("=" * 60)
    print("Test 6: compute_civic_soul() with Config")
    print("=" * 60)
    
    world_slice = WorldSlice(
        year=2020,
        country_code="MEX",
        conflict_intensity=50.0,
        state_repression=40.0,
        inequality_index=60.0,
        unemployment_level=30.0,
        gdp_per_capita=10000.0,
        welfare_support=50.0,
        media_saturation=60.0,
        propaganda_saturation=40.0
    )
    
    driver_vec = DriverVector(
        meritocracy_belief=55.0,
        trust_vs_distrust=50.0,
        religiosity=60.0,
        ritual_centrality=50.0
    )
    
    local_modifiers = LocalModifiers(
        ethnic_power_status="dominant",
        religion_status="majority",
        urban_rural="urban",
        class_position=5
    )
    
    # Compute civic soul
    civic_soul = compute_civic_soul(world_slice, driver_vec, local_modifiers)
    
    # Verify all conditions are computed and within bounds
    assert civic_soul.rootedness >= 0 and civic_soul.rootedness <= 100
    assert civic_soul.perceived_justice_order >= 0 and civic_soul.perceived_justice_order <= 100
    assert civic_soul.risk_band >= 0 and civic_soul.risk_band <= 100
    
    print(f"✅ Computed civic soul conditions:")
    print(f"   Rootedness: {civic_soul.rootedness:.1f}")
    print(f"   Perceived justice order: {civic_soul.perceived_justice_order:.1f}")
    print(f"   Obligation symmetry: {civic_soul.obligation_symmetry:.1f}")
    print(f"   Risk band: {civic_soul.risk_band:.1f}")
    
    # With moderate conflict, risk_band should be moderate
    assert civic_soul.risk_band > 20 and civic_soul.risk_band < 80, "Risk band should be moderate"
    
    print("✅ All compute_civic_soul tests passed!\n")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("RAWLSING V4.1 - CONFIG LOADER TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_config_loader_basic()
        test_path_evaluation()
        test_condition_evaluation()
        test_update_needs()
        test_update_strategies()
        test_compute_civic_soul()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
