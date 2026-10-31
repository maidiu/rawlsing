from __future__ import annotations

from v3.core.state import BackboneState
from v3.io.calibration_from_identity import apply_calibration_to_state
from v3.systems.relational_field import build_relational_field_projection


def test_v5_relational_field_does_not_add_tenth_stratum() -> None:
    state = BackboneState(year=2026, age=29)
    identity = {
        "country_code": "US",
        "region": "Northeast",
        "class_origin": "working",
        "current_class": "middle",
        "urbanicity": "city",
        "minority_status": "dominant",
    }
    relational_field = {
        "status": "ok",
        "source": "validated_9_plus_absolute",
        "projection": {
            "channels": ["formal_legibility", "boundary_pressure"],
            "notes": ["9-strata only"],
        },
        "absolute_horizon": {
            "status": "internal_only",
            "surface_export_allowed": False,
            "surface_label_allowed": False,
        },
        "notes": ["no tenth stratum"],
    }

    apply_calibration_to_state(state, identity, relational_field=relational_field)
    projection = build_relational_field_projection(state.strata_stack)

    assert len(state.strata_stack) == 9
    assert [s.level for s in state.strata_stack] == list(range(9))
    assert state.strata_stack[-1].name == "self"
    assert state.strata_salience["absolute_horizon"]["surface_export_allowed"] is False
    assert state.strata_salience["relational_field"]["status"] == "ok"
    assert state.yearly_integrity["relational_field"]["status"] == "ok"
    assert state.yearly_integrity["relational_field"]["strata_count"] == 9
    assert projection["strata_count"] == 9
    assert len(projection["relations"]) == 8
    assert projection["absolute_horizon"]["surface_export_allowed"] is False
