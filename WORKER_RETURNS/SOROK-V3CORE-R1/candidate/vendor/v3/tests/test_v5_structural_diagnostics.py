from __future__ import annotations

from v3.io import calibration_from_identity
from v3.io.identity_to_backbone import backbone_state_from_identity


def test_empty_strata_stack_is_blocked_and_visible(monkeypatch) -> None:
    def return_empty(*_args, **_kwargs):
        return []

    monkeypatch.setattr(calibration_from_identity, "build_strata_stack", return_empty)

    state = backbone_state_from_identity(
        {
            "country_code": "US",
            "class_origin": "middle",
            "current_class": "middle",
            "minority_status": "dominant",
            "urbanicity": "city",
            "age": 32,
        },
        year=2000,
        age=32,
    )

    assert state.strata_stack == []
    assert state.strata_salience == {}
    assert state.generation_diagnostics
    diag = state.generation_diagnostics[-1]
    assert diag["stage"] == "v5_strata_stack"
    assert diag["status"] == "blocked"
    assert diag["fallback_used"] is True
    assert diag["fallback_reason"] == "strata_stack_missing_or_empty"
    assert "strata_stack" in diag["fields_impacted"]
    assert "strata_salience" in diag["fields_impacted"]
