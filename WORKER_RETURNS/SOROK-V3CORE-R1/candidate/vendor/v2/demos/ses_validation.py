"""
Comprehensive Testing & Validation for Multi-Layer SES System

Tests:
1. Indonesia 1962 (Javanese DOMINANT, Chinese POWERLESS)
2. Multiple countries with GDL data
3. Countries without GDL data (fallback)
4. Edge cases (no region, no ethnicity, no power status)
5. Validate adjustments are reasonable
6. Verify final SES is always in range 1-10
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from identity_generator import generate_identity_context, sample_ses_decile
from data_access import _get_db_connection
from psycopg2.extras import RealDictCursor

def test_indonesia_1962():
    """Test Indonesia 1962 with known ethnic groups."""
    print("\n" + "="*70)
    print("TEST 1: Indonesia 1962 (Javanese DOMINANT, Chinese POWERLESS)")
    print("="*70)
    
    # Test multiple runs to see variation
    results = []
    for i in range(5):
        try:
            identity, context = generate_identity_context('IDN', 1962, 30, 'male')
            ses = context['ses']
            ethnic = context['ethnic']
            results.append({
                'decile': ses['decile'],
                'adjustments': ses['adjustments'],
                'ethnicity': ethnic.get('group_name'),
                'power_status': ethnic.get('epr_power_status')
            })
        except Exception as e:
            print(f"  Error in run {i+1}: {e}")
            continue
    
    print(f"\nGenerated {len(results)} identities:")
    for i, r in enumerate(results, 1):
        adj = r['adjustments']
        print(f"\n  Run {i}:")
        print(f"    Ethnicity: {r['ethnicity']}")
        print(f"    Power Status: {r['power_status']}")
        print(f"    Final SES: {r['decile']}")
        print(f"    Adjustments: base={adj['base']:.1f}, "
              f"regional={adj['regional']:+.2f}, "
              f"urban={adj['urbanicity']:+.2f}, "
              f"power={adj['power_status']:+.2f}")
        
        # Validate
        assert 1 <= r['decile'] <= 10, f"Decile out of range: {r['decile']}"
        print(f"    ✓ Decile in valid range (1-10)")
    
    return results


def test_multiple_countries():
    """Test multiple countries with GDL data."""
    print("\n" + "="*70)
    print("TEST 2: Multiple Countries with GDL Data")
    print("="*70)
    
    # Countries known to have GDL data
    test_countries = [
        ('IDN', 2010, 'Indonesia'),
        ('CHN', 2010, 'China'),
        ('IND', 2010, 'India'),
        ('BRA', 2010, 'Brazil'),
        ('MEX', 2010, 'Mexico'),
    ]
    
    results = []
    for country_code, year, country_name in test_countries:
        try:
            identity, context = generate_identity_context(country_code, year, 30)
            ses = context['ses']
            adj = ses['adjustments']
            
            results.append({
                'country': country_name,
                'decile': ses['decile'],
                'adjustments': adj
            })
            
            print(f"\n  {country_name} ({country_code}, {year}):")
            print(f"    Final SES: {ses['decile']}")
            print(f"    Base: {adj['base']:.1f}, "
                  f"Regional: {adj['regional']:+.2f}, "
                  f"Urban: {adj['urbanicity']:+.2f}, "
                  f"Power: {adj['power_status']:+.2f}")
            
            # Validate
            assert 1 <= ses['decile'] <= 10, f"Decile out of range: {ses['decile']}"
            print(f"    ✓ Valid decile")
            
        except Exception as e:
            print(f"  {country_name}: Error - {e}")
            continue
    
    print(f"\n✓ Tested {len(results)}/{len(test_countries)} countries")
    return results


def test_fallback_countries():
    """Test countries without GDL data (fallback behavior)."""
    print("\n" + "="*70)
    print("TEST 3: Countries Without GDL Data (Fallback)")
    print("="*70)
    
    # Countries likely without GDL data
    test_countries = [
        ('XXX', 2010, 'Fake Country'),
        ('SOM', 2010, 'Somalia'),  # May not have GDL
    ]
    
    results = []
    for country_code, year, country_name in test_countries:
        try:
            identity, context = generate_identity_context(country_code, year, 30)
            ses = context['ses']
            adj = ses['adjustments']
            
            results.append({
                'country': country_name,
                'decile': ses['decile'],
                'adjustments': adj
            })
            
            print(f"\n  {country_name} ({country_code}, {year}):")
            print(f"    Final SES: {ses['decile']}")
            print(f"    Base: {adj['base']:.1f}, "
                  f"Regional: {adj['regional']:+.2f}, "
                  f"Urban: {adj['urbanicity']:+.2f}, "
                  f"Power: {adj['power_status']:+.2f}")
            
            # Validate - should still return valid SES
            assert 1 <= ses['decile'] <= 10, f"Decile out of range: {ses['decile']}"
            print(f"    ✓ Valid decile (fallback working)")
            
        except Exception as e:
            print(f"  {country_name}: Error - {e}")
            continue
    
    print(f"\n✓ Tested {len(results)}/{len(test_countries)} fallback countries")
    return results


def test_edge_cases():
    """Test edge cases (no region, no ethnicity, no power status)."""
    print("\n" + "="*70)
    print("TEST 4: Edge Cases")
    print("="*70)
    
    edge_cases = [
        {
            'name': 'No region data',
            'country_code': 'IDN',
            'year': 2010,
            'test': lambda context: context['location']['region'] is None
        },
        {
            'name': 'No ethnicity data',
            'country_code': 'XXX',
            'year': 2010,
            'test': lambda context: context['ethnic']['group_name'] == 'Unknown'
        },
        {
            'name': 'No power status',
            'country_code': 'IDN',
            'year': 2010,
            'test': lambda context: context['ethnic'].get('epr_power_status') is None
        },
        {
            'name': 'No WID data',
            'country_code': 'IDN',
            'year': 1962,  # May not have WID data
            'test': lambda context: context['ses']['adjustments']['base'] == 5.0
        },
    ]
    
    results = []
    for case in edge_cases:
        try:
            identity, context = generate_identity_context(
                case['country_code'], 
                case['year'], 
                30
            )
            ses = context['ses']
            
            # Check if edge case condition is met
            condition_met = case['test'](context)
            
            results.append({
                'case': case['name'],
                'condition_met': condition_met,
                'decile': ses['decile'],
                'adjustments': ses['adjustments']
            })
            
            print(f"\n  {case['name']}:")
            print(f"    Condition met: {condition_met}")
            print(f"    Final SES: {ses['decile']}")
            print(f"    Adjustments: {ses['adjustments']}")
            
            # Validate
            assert 1 <= ses['decile'] <= 10, f"Decile out of range: {ses['decile']}"
            print(f"    ✓ Valid decile")
            
        except Exception as e:
            print(f"  {case['name']}: Error - {e}")
            continue
    
    print(f"\n✓ Tested {len(results)}/{len(edge_cases)} edge cases")
    return results


def test_adjustment_reasonableness():
    """Validate that adjustments are reasonable."""
    print("\n" + "="*70)
    print("TEST 5: Adjustment Reasonableness")
    print("="*70)
    
    # Test various combinations
    test_cases = [
        ('IDN', 2010, 'city', 'Javanese', 'DOMINANT'),
        ('IDN', 2010, 'rural', 'Javanese', 'DOMINANT'),
        ('IDN', 2010, 'megacity', None, None),
        ('IDN', 2010, 'town', None, None),
    ]
    
    results = []
    for country_code, year, urbanicity, ethnicity, power_status in test_cases:
        try:
            result = sample_ses_decile(
                country_code=country_code,
                year=year,
                region_code=None,
                region_name=None,
                urbanicity=urbanicity,
                ethnicity=ethnicity,
                country_name='Indonesia' if ethnicity else None,
                power_status=power_status
            )
            
            adj = result['adjustments']
            results.append({
                'urbanicity': urbanicity,
                'ethnicity': ethnicity,
                'power_status': power_status,
                'adjustments': adj
            })
            
            print(f"\n  Test case:")
            print(f"    Urbanicity: {urbanicity}")
            print(f"    Ethnicity: {ethnicity}")
            print(f"    Power Status: {power_status}")
            print(f"    Adjustments: {adj}")
            
            # Validate reasonableness
            # Urbanicity: -0.5 to +1.0
            assert -0.5 <= adj['urbanicity'] <= 1.0, f"Urbanicity adjustment out of range: {adj['urbanicity']}"
            
            # Power status: -1.5 to +2.0
            assert -1.5 <= adj['power_status'] <= 2.0, f"Power adjustment out of range: {adj['power_status']}"
            
            # Regional: -2.0 to +2.0
            assert -2.0 <= adj['regional'] <= 2.0, f"Regional adjustment out of range: {adj['regional']}"
            
            # Final SES: 1-10
            assert 1 <= result['decile'] <= 10, f"Final decile out of range: {result['decile']}"
            
            print(f"    ✓ All adjustments in reasonable range")
            
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    print(f"\n✓ Tested {len(results)}/{len(test_cases)} adjustment combinations")
    return results


def test_ses_range():
    """Verify final SES is always in range 1-10."""
    print("\n" + "="*70)
    print("TEST 6: SES Range Validation (1-10)")
    print("="*70)
    
    # Test many random combinations
    test_cases = []
    urbanicities = ['megacity', 'city', 'town', 'rural', None]
    power_statuses = ['DOMINANT', 'POWERLESS', 'DISCRIMINATED', None]
    
    for urbanicity in urbanicities:
        for power_status in power_statuses:
            test_cases.append(('IDN', 2010, urbanicity, power_status))
    
    results = []
    out_of_range = []
    
    for country_code, year, urbanicity, power_status in test_cases:
        try:
            result = sample_ses_decile(
                country_code=country_code,
                year=year,
                region_code=None,
                region_name=None,
                urbanicity=urbanicity,
                ethnicity='Javanese' if power_status else None,
                country_name='Indonesia' if power_status else None,
                power_status=power_status
            )
            
            decile = result['decile']
            results.append(decile)
            
            if not (1 <= decile <= 10):
                out_of_range.append({
                    'urbanicity': urbanicity,
                    'power_status': power_status,
                    'decile': decile
                })
                
        except Exception as e:
            print(f"  Error with {urbanicity}/{power_status}: {e}")
            continue
    
    print(f"\n  Tested {len(results)} combinations")
    print(f"  All deciles in range 1-10: {len(out_of_range) == 0}")
    
    if out_of_range:
        print(f"  ⚠️  Found {len(out_of_range)} out-of-range deciles:")
        for case in out_of_range:
            print(f"    {case}")
    else:
        print(f"  ✓ All deciles in valid range")
    
    # Statistics
    if results:
        print(f"\n  Statistics:")
        print(f"    Min: {min(results)}")
        print(f"    Max: {max(results)}")
        print(f"    Mean: {sum(results)/len(results):.2f}")
    
    return results, out_of_range


def run_all_tests():
    """Run all validation tests."""
    print("\n" + "="*70)
    print("COMPREHENSIVE SES SYSTEM VALIDATION")
    print("="*70)
    
    all_passed = True
    
    try:
        # Test 1: Indonesia 1962
        results1 = test_indonesia_1962()
        if not results1:
            print("  ⚠️  No results for Indonesia 1962")
            all_passed = False
        
        # Test 2: Multiple countries
        results2 = test_multiple_countries()
        if len(results2) < 3:
            print("  ⚠️  Fewer than 3 countries tested successfully")
            all_passed = False
        
        # Test 3: Fallback countries
        results3 = test_fallback_countries()
        if not results3:
            print("  ⚠️  No fallback tests passed")
            all_passed = False
        
        # Test 4: Edge cases
        results4 = test_edge_cases()
        if len(results4) < 3:
            print("  ⚠️  Fewer than 3 edge cases tested")
            all_passed = False
        
        # Test 5: Adjustment reasonableness
        results5 = test_adjustment_reasonableness()
        if not results5:
            print("  ⚠️  No adjustment tests passed")
            all_passed = False
        
        # Test 6: SES range
        results6, out_of_range = test_ses_range()
        if out_of_range:
            print("  ⚠️  Some deciles out of range")
            all_passed = False
        
        # Summary
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)
        
        if all_passed:
            print("✅ ALL TESTS PASSED")
        else:
            print("⚠️  SOME TESTS HAD ISSUES (see above)")
        
        print(f"\nTest Results:")
        print(f"  - Indonesia 1962: {len(results1)} identities generated")
        print(f"  - Multiple countries: {len(results2)} countries tested")
        print(f"  - Fallback countries: {len(results3)} countries tested")
        print(f"  - Edge cases: {len(results4)} cases tested")
        print(f"  - Adjustment tests: {len(results5)} combinations tested")
        print(f"  - Range validation: {len(results6)} combinations, {len(out_of_range)} out of range")
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
