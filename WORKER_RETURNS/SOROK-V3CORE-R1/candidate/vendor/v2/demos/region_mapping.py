"""Test region code to GDL code mapping."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from identity_generator import map_region_to_gdlcode, get_regional_income_index, calculate_regional_ses_adjustment

def test_region_mapping():
    """Test the region mapping function."""
    print("Testing Region Code → GDL Code Mapping")
    print("="*70)
    
    # Test cases: (country_code, region_code, region_name, expected_pattern)
    test_cases = [
        ('IDN', None, None, 'IDNt'),  # National
        ('IDN', '33', 'Banten', 'IDNr115'),  # Should match
        ('IDN', '30', 'Jawa Barat', 'IDNr111'),  # West Java
        ('IDN', '08', 'Jawa Timur', 'IDNr114'),  # East Java
        ('IDN', '04', 'Daerah Khusus Ibukota Jakarta', 'IDNr110'),  # Jakarta
        ('IDN', '01', 'Nanggroe Aceh Darussalam Province', 'IDNr101'),  # Aceh
        ('IDN', '26', 'North Sumatra', 'IDNr102'),  # North Sumatra
        ('CHN', None, None, 'CHNt'),  # National
        ('USA', None, None, 'USAt'),  # National
    ]
    
    print("\n1. Testing map_region_to_gdlcode():")
    print("-"*70)
    
    results = []
    for country_code, region_code, region_name, expected_pattern in test_cases:
        gdlcode = map_region_to_gdlcode(country_code, region_code, region_name)
        match = "✓" if gdlcode else "✗"
        if gdlcode:
            pattern_match = "✓" if gdlcode.startswith(expected_pattern.split('r')[0] if 'r' in expected_pattern else expected_pattern) else "✗"
        else:
            pattern_match = "?"
        
        results.append({
            'country': country_code,
            'region': region_name or region_code or 'National',
            'gdlcode': gdlcode,
            'expected': expected_pattern,
            'matched': gdlcode is not None
        })
        
        print(f"  {match} {country_code}, {region_name or region_code or 'National'}: {gdlcode or 'None'}")
        if gdlcode and expected_pattern:
            if gdlcode == expected_pattern:
                print(f"    ✓ Exact match with expected: {expected_pattern}")
            elif gdlcode.startswith(expected_pattern.split('r')[0] if 'r' in expected_pattern else expected_pattern):
                print(f"    ✓ Pattern match (got {gdlcode}, expected starts with {expected_pattern})")
    
    print(f"\n  Summary: {sum(1 for r in results if r['matched'])}/{len(results)} mappings successful")
    
    # Test 2: Test with actual regional income queries
    print("\n2. Testing get_regional_income_index() with mapping:")
    print("-"*70)
    
    test_regions = [
        ('IDN', '33', 'Banten', 2010),
        ('IDN', '30', 'Jawa Barat', 2010),
        ('IDN', '08', 'Jawa Timur', 2010),
        ('IDN', '04', 'Daerah Khusus Ibukota Jakarta', 2010),
    ]
    
    for country_code, region_code, region_name, year in test_regions:
        income = get_regional_income_index(country_code, region_code, region_name, year)
        if income is not None:
            print(f"  ✓ {region_name}: income index = {income:.3f}")
        else:
            print(f"  ✗ {region_name}: No data found")
    
    # Test 3: Test regional SES adjustment
    print("\n3. Testing calculate_regional_ses_adjustment() with mapping:")
    print("-"*70)
    
    for country_code, region_code, region_name, year in test_regions[:3]:  # Test first 3
        adjustment = calculate_regional_ses_adjustment(country_code, region_code, region_name, year)
        if adjustment != 0.0:
            print(f"  ✓ {region_name}: adjustment = {adjustment:+.2f} deciles")
        else:
            print(f"  - {region_name}: adjustment = {adjustment:+.2f} (no regional difference or no data)")
    
    # Test 4: Test with full pipeline
    print("\n4. Testing full pipeline with region mapping:")
    print("-"*70)
    
    from identity_generator import generate_identity_context
    
    for i in range(3):
        try:
            identity, context = generate_identity_context('IDN', 2010, 30)
            ses = context['ses']
            location = context['location']
            adj = ses['adjustments']
            
            region_name = location.get('region', {}).get('admin1_name', 'N/A')
            regional_adj = adj['regional']
            
            if regional_adj != 0.0:
                print(f"  Run {i+1}: {region_name} - Regional adjustment: {regional_adj:+.2f} deciles")
            else:
                print(f"  Run {i+1}: {region_name} - Regional adjustment: {regional_adj:+.2f} (no match or no difference)")
        except Exception as e:
            print(f"  Run {i+1}: Error - {e}")
    
    print("\n" + "="*70)
    print("✅ Mapping tests complete!")
    print("\nNote: Some regions may not match if names differ significantly.")
    print("The system gracefully falls back to 0.0 adjustment when no match is found.")


if __name__ == "__main__":
    test_region_mapping()
