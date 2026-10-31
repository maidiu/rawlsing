# SINGLE SOURCE OF TRUTH — no other file may contain a driver field mapping.
# This replaces the 4 duplicated copies previously in data_access.py and
# the inline driver_map dict at the end of get_driver_vec.
from __future__ import annotations

from typing import Any

# DB column name → (DriverVector field name, is_inverse)
# is_inverse=True means a high DB value maps to a low DriverVector value (100.0 - v)
DRIVER_DB_TO_FIELD: dict[str, tuple[str, bool]] = {
    "trustEcology": ("trust_vs_distrust", False),
    "trustEcologyExtended": ("trust_vs_distrust", False),
    "ritualDensity": ("ritual_centrality", False),
    "secularization": ("religiosity", True),
    "hierarchy": ("authoritarian_vs_egalitarian", False),
    "authorityStyle": ("authoritarian_vs_egalitarian", False),
    "collectivism": ("individualism_vs_collectivism", True),
    "fatalism": ("fatalism_vs_agency", True),
    "existentialLocus": ("fatalism_vs_agency", True),
}


def apply_driver_map_to_target(db_values: dict[str, Any], target: Any) -> None:
    """
    Apply db_values to target object's DriverVector fields using the canonical map.
    Sets target.field_name = (100.0 - value) if is_inverse else value for each
    db_name in DRIVER_DB_TO_FIELD that exists in db_values, clamped to [0, 100].
    """
    for db_name, (field_name, is_inverse) in DRIVER_DB_TO_FIELD.items():
        if db_name in db_values:
            v = float(db_values[db_name])
            if is_inverse:
                v = 100.0 - v
            setattr(target, field_name, max(0.0, min(100.0, v)))


def driver_db_names() -> list[str]:
    """Return the list of DB column names that the map covers."""
    return list(DRIVER_DB_TO_FIELD.keys())


def copy_microdata_to_dict(vec_micro: Any) -> dict[str, float]:
    """
    Read DriverVector field values from vec_micro and write them to a dict
    keyed by DB column name. Used in the WVS microdata path where we need to
    store intermediate values in a drivers dict before later applying the map.
    This is the inverse direction of apply_driver_map_to_target.
    """
    out: dict[str, float] = {}
    for db_name, (field_name, is_inverse) in DRIVER_DB_TO_FIELD.items():
        if hasattr(vec_micro, field_name):
            v = getattr(vec_micro, field_name)
            out[db_name] = (100.0 - v) if is_inverse else v
    return out
