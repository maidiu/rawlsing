"""Quick test script for GDL query functions."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from identity_generator import (
    get_regional_income_index,
    get_regional_education_level,
    calculate_regional_ses_adjustment
)

def test_gdl_functions():
    """Test GDL functions with known data."""
    
    print("Testing GDL Query Functions...")
    print("=" * 60)
    
    # Test 1: National level (should work for most countries)
    print("\n1. Testing National Level (Indonesia 2010):")
    national_income = get_regional_income_index("IDN", None, None, 2010)
    print(f"   National income index: {national_income}")
    
    # Test 2: Regional level (Indonesia, Java region)
    print("\n2. Testing Regional Level (Indonesia, Java 2010):")
    # Try with region name
    regional_income = get_regional_income_index("IDN", None, "Java", 2010)
    print(f"   Regional income index (Java): {regional_income}")
    
    # Test 3: Regional adjustment calculation
    print("\n3. Testing Regional SES Adjustment (Indonesia, Java 2010):")
    adjustment = calculate_regional_ses_adjustment("IDN", None, "Java", 2010)
    print(f"   Regional adjustment: {adjustment:.2f} deciles")
    
    # Test 4: Education level
    print("\n4. Testing Education Level (Indonesia 2010):")
    education = get_regional_education_level("IDN", None, None, 2010)
    print(f"   Mean years education (national): {education}")
    
    # Test 5: Country without GDL (should return None gracefully)
    print("\n5. Testing Fallback (Country not in GDL):")
    missing_income = get_regional_income_index("XXX", None, None, 2010)
    print(f"   Income index (should be None): {missing_income}")
    missing_adj = calculate_regional_ses_adjustment("XXX", None, None, 2010)
    print(f"   Adjustment (should be 0.0): {missing_adj}")
    
    # Test 6: Year resampling (try year that might not exist)
    print("\n6. Testing Year Resampling (Indonesia 1962):")
    old_income = get_regional_income_index("IDN", None, None, 1962)
    print(f"   Income index (resampled year): {old_income}")
    
    print("\n" + "=" * 60)
    print("✅ Tests complete!")
    print("\nNote: Some tests may return None if data not available.")
    print("This is expected behavior (graceful fallback).")

if __name__ == "__main__":
    test_gdl_functions()
