from __future__ import annotations

from v3.core.state import BackboneState, Stratum
from v3.io.calibration_from_identity import build_strata_stack
from v3.io.identity_to_backbone import backbone_state_from_identity


def test_stratum_clamp_preserves_strings_and_clamps_numeric_fields() -> None:
    stratum = Stratum(
        level=2,
        name="nation_state",
        material_relation="exploited",
        hegemonic_story="The nation is inevitable.",
        loyalty_demand="Obey the law.",
        provision_strength=123.4,
        coercion_strength=-5.0,
        contradiction_load=200.0,
        visibility_of_complicity=88.0,
        salience=144.0,
    )

    stratum.clamp_all()

    assert stratum.material_relation == "exploited"
    assert stratum.hegemonic_story == "The nation is inevitable."
    assert stratum.loyalty_demand == "Obey the law."
    assert stratum.provision_strength == 100.0
    assert stratum.coercion_strength == 0.0
    assert stratum.contradiction_load == 100.0
    assert stratum.visibility_of_complicity == 88.0
    assert stratum.salience == 100.0


def test_build_strata_stack_returns_local_nine_strata() -> None:
    strata = build_strata_stack(
        {
            "country_code": "US",
            "class_origin": "middle",
            "current_class": "middle",
            "minority_status": "dominant",
            "urbanicity": "city",
            "age": 32,
        }
    )

    assert isinstance(strata, list)
    assert len(strata) == 9
    assert [s.level for s in strata] == list(range(9))
    assert strata[0].name == "planetary"
    assert strata[-1].name == "self"


def test_backbone_initialization_attaches_nine_strata_stack() -> None:
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

    assert isinstance(state, BackboneState)
    assert len(state.strata_stack) == 9
    assert [s.level for s in state.strata_stack] == list(range(9))
    assert state.strata_salience == {str(i): s.to_salient_dict() for i, s in enumerate(state.strata_stack)}


def test_backbone_initialization_records_visible_diagnostic_when_calibration_fails(monkeypatch) -> None:
    from v3.io import calibration_from_identity as calibration_module

    def boom(*_args, **_kwargs):
        raise RuntimeError("calibration boom")

    monkeypatch.setattr(calibration_module, "build_strata_stack", boom)

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
    assert diag["stage"] == "backbone_init.calibration"
    assert diag["status"] == "degraded"
    assert diag["exception_type"] == "RuntimeError"
    assert diag["fallback_behavior"] == "calibration_skipped"
    assert "strata_salience" in diag["fields_impacted"]
