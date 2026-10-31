"""Test the multi-layer SES approach."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from identity_generator import generate_identity_context

def test_multi_layer_ses():
    """Test the complete multi-layer SES pipeline."""
    
    print("Testing Multi-Layer SES Pipeline")
    print("=" * 60)
    
    # Test 1: Indonesia 2010 (has GDL data, EPR data)
    print("\n1. Indonesia 2010 (full data available):")
    try:
        identity, context = generate_identity_context("IDN", 2010, 30, "male")
        ses = context["ses"]
        print(f"   Final SES decile: {ses['decile']}")
        print(f"   Class label: {ses['class_label']}")
        print(f"   Adjustments:")
        adj = ses.get("adjustments", {})
        print(f"     - Base (WID): {adj.get('base', 0):.2f}")
        print(f"     - Regional (GDL): {adj.get('regional', 0):+.2f} deciles")
        print(f"     - Urbanicity: {adj.get('urbanicity', 0):+.2f} deciles")
        print(f"     - Power Status (EPR): {adj.get('power_status', 0):+.2f} deciles")
        print(f"     - Final: {adj.get('final', 0):.2f} → {ses['decile']}")
        print(f"   Location: {context['location'].get('region', {}).get('admin1_name', 'N/A')}, {context['location'].get('urbanicity', 'N/A')}")
        print(f"   Ethnicity: {context['ethnic'].get('group_name', 'N/A')}, Power: {context['ethnic'].get('epr_power_status', 'N/A')}")
    except Exception as e:
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Country without GDL (fallback should work)
    print("\n2. Country without GDL (fallback test):")
    try:
        identity, context = generate_identity_context("XXX", 2010, 30, "male")
        ses = context["ses"]
        print(f"   Final SES decile: {ses['decile']} (should be 5, middle)")
        print(f"   Adjustments:")
        adj = ses.get("adjustments", {})
        print(f"     - Base: {adj.get('base', 0):.2f}")
        print(f"     - Regional: {adj.get('regional', 0):+.2f}")
        print(f"     - Urbanicity: {adj.get('urbanicity', 0):+.2f}")
        print(f"     - Power Status: {adj.get('power_status', 0):+.2f}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Multiple runs to see variation
    print("\n3. Multiple runs (showing variation):")
    for i in range(3):
        try:
            identity, context = generate_identity_context("IDN", 2010, 30)
            ses = context["ses"]
            adj = ses.get("adjustments", {})
            print(f"   Run {i+1}: Decile {ses['decile']} (base={adj.get('base', 0):.1f}, "
                  f"regional={adj.get('regional', 0):+.1f}, "
                  f"urban={adj.get('urbanicity', 0):+.1f}, "
                  f"power={adj.get('power_status', 0):+.1f})")
        except Exception as e:
            print(f"   Run {i+1}: Error - {e}")
    
    print("\n" + "=" * 60)
    print("✅ Tests complete!")

if __name__ == "__main__":
    test_multi_layer_ses()
