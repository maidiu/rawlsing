"""
Driver Age Introduction Schema

Defines which drivers are active at which ages, allowing gradual introduction
of drivers as the persona develops from birth to adulthood.
"""

from typing import List, Set, Optional, Dict, Any
import yaml
import os

# Load schema
_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "config", "driver_age_schema.yaml")

def _field_to_drivers_map() -> Dict[str, List[str]]:
    """Build reverse map: field_name -> list of driver names that map to it."""
    schema = _load_schema()
    drivers_config = schema.get("drivers", {})
    result: Dict[str, List[str]] = {}
    for driver_name, config in drivers_config.items():
        maps_to = config.get("maps_to")
        if maps_to:
            if maps_to not in result:
                result[maps_to] = []
            result[maps_to].append(driver_name)
    return result


def _load_schema() -> Dict:
    """Load the driver age schema from YAML"""
    with open(_SCHEMA_PATH, 'r') as f:
        return yaml.safe_load(f)


def get_active_drivers(age: int) -> Set[str]:
    """
    Get the set of driver names that are active at a given age.
    
    Args:
        age: Persona's age
        
    Returns:
        Set of driver names that are active at this age
    """
    schema = _load_schema()
    drivers_config = schema.get("drivers", {})
    
    active = set()
    for driver_name, config in drivers_config.items():
        active_from = config.get("active_from", 0)
        if age >= active_from:
            active.add(driver_name)
    
    return active


def get_drivers_by_stage(stage: str) -> List[str]:
    """
    Get all drivers for a given developmental stage.
    
    Args:
        stage: One of "birth", "early_childhood", "school_age", "adolescence", "young_adult", "adulthood"
        
    Returns:
        List of driver names for that stage
    """
    schema = _load_schema()
    stages = schema.get("stages", {})
    
    if stage not in stages:
        return []
    
    return stages[stage].get("drivers", [])


def get_all_drivers_for_age(age: int) -> List[str]:
    """
    Get all drivers that are active at a given age (cumulative).
    
    This includes all drivers from birth up to the current age.
    
    Args:
        age: Persona's age
        
    Returns:
        List of all driver names active at this age (sorted)
    """
    active = get_active_drivers(age)
    return sorted(list(active))


def get_driver_mapping(driver_name: str) -> Optional[Dict]:
    """
    Get the mapping configuration for a driver.
    
    Args:
        driver_name: Name of the driver (e.g., "collectiveAffectTone")
        
    Returns:
        Dict with mapping info: {"maps_to": "field_name", "inverse": bool, "description": str}
        or None if driver not found
    """
    schema = _load_schema()
    drivers_config = schema.get("drivers", {})
    
    if driver_name not in drivers_config:
        return None
    
    config = drivers_config[driver_name]
    return {
        "maps_to": config.get("maps_to"),
        "inverse": config.get("inverse", False),
        "description": config.get("description", ""),
        "active_from": config.get("active_from", 0)
    }


def filter_driver_vector_by_age(driver_vec, age: int):
    """
    Filter a DriverVector to only include drivers active at the given age.
    
    This creates a filtered view where only age-appropriate drivers are used.
    Note: This doesn't modify the original DriverVector, but returns a dict
    of active driver values.
    
    Args:
        driver_vec: DriverVector object
        age: Persona's age
        
    Returns:
        Dict of {driver_name: value} for active drivers only
    """
    active_drivers = get_active_drivers(age)
    active_values = {}
    
    # Get mapped drivers (from DriverVector fields)
    schema = _load_schema()
    drivers_config = schema.get("drivers", {})
    
    for driver_name in active_drivers:
        config = drivers_config.get(driver_name, {})
        maps_to = config.get("maps_to")
        
        if maps_to:
            # Get value from DriverVector field
            if hasattr(driver_vec, maps_to):
                value = getattr(driver_vec, maps_to)
                if value is not None:
                    active_values[driver_name] = value
        
        # Also check extra dict for unmapped drivers
        if driver_name in getattr(driver_vec, "extra", {}):
            active_values[driver_name] = driver_vec.extra[driver_name]
    
    return active_values


def get_field_values_for_age(driver_vec: Any, age: int) -> Dict[str, Any]:
    """
    Return dict of DriverVector field values with inactive fields set to 50.
    Caller constructs the filtered DriverVector.
    """
    active = get_active_drivers(age)
    field_to_drivers = _field_to_drivers_map()
    result = {}
    for attr in ["trust_vs_distrust", "religiosity", "ritual_centrality",
                 "authoritarian_vs_egalitarian", "individualism_vs_collectivism",
                 "fatalism_vs_agency", "meritocracy_belief", "family_importance", "extra"]:
        if attr == "extra":
            result[attr] = getattr(driver_vec, "extra", {}) or {}
            continue
        val = getattr(driver_vec, attr, 50.0)
        drivers_for_field = field_to_drivers.get(attr, [])
        if not drivers_for_field:
            result[attr] = val
            continue
        any_active = any(d in active for d in drivers_for_field)
        result[attr] = (val if val is not None else 50.0) if any_active else 50.0
    return result


def get_stage_for_age(age: int) -> str:
    """
    Get the developmental stage for a given age.
    
    Args:
        age: Persona's age
        
    Returns:
        Stage name: "birth", "early_childhood", "school_age", "adolescence", "young_adult", "adulthood"
    """
    if age == 0:
        return "birth"
    elif age < 7:
        return "early_childhood"
    elif age < 12:
        return "school_age"
    elif age < 18:
        return "adolescence"
    elif age < 30:
        return "young_adult"
    else:
        return "adulthood"


def get_driver_introduction_summary() -> Dict:
    """
    Get a summary of when each driver is introduced.
    
    Returns:
        Dict mapping age -> list of drivers introduced at that age
    """
    schema = _load_schema()
    drivers_config = schema.get("drivers", {})
    
    summary = {}
    for driver_name, config in drivers_config.items():
        age = config.get("active_from", 0)
        if age not in summary:
            summary[age] = []
        summary[age].append(driver_name)
    
    # Sort by age
    return {age: sorted(drivers) for age, drivers in sorted(summary.items())}


if __name__ == "__main__":
    # Test the schema
    print("=" * 80)
    print("DRIVER AGE INTRODUCTION SCHEMA TEST")
    print("=" * 80)
    
    print("\n1. Drivers by age:")
    for age in [0, 3, 7, 10, 15, 20, 35]:
        active = get_all_drivers_for_age(age)
        print(f"   Age {age}: {len(active)} drivers")
    
    print("\n2. Active drivers at age 0 (birth):")
    birth_drivers = get_all_drivers_for_age(0)
    for driver in birth_drivers[:10]:
        print(f"   - {driver}")
    if len(birth_drivers) > 10:
        print(f"   ... and {len(birth_drivers) - 10} more")
    
    print("\n3. Active drivers at age 7 (end of early childhood):")
    age7_drivers = get_all_drivers_for_age(7)
    print(f"   Total: {len(age7_drivers)} drivers")
    
    print("\n4. Active drivers at age 30 (adulthood):")
    adult_drivers = get_all_drivers_for_age(30)
    print(f"   Total: {len(adult_drivers)} drivers")
    
    print("\n5. Driver introduction summary:")
    summary = get_driver_introduction_summary()
    for age, drivers in list(summary.items())[:5]:
        print(f"   Age {age}: {len(drivers)} drivers introduced")
        for driver in drivers[:3]:
            print(f"      - {driver}")
        if len(drivers) > 3:
            print(f"      ... and {len(drivers) - 3} more")

