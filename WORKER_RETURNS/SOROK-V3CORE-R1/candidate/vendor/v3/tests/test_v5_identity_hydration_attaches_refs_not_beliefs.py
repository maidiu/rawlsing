from __future__ import annotations

from v3.io.identity_to_backbone import backbone_state_from_identity
from v3.io.json_codec import state_to_dict


def test_v5_identity_hydration_attaches_refs_not_beliefs() -> None:
    identity = {
        "given_name": "Amina",
        "family_name": "Qadir",
        "country_code": "US",
        "region": "Midwest",
        "class_origin": "working",
        "current_class": "middle",
        "urbanicity": "city",
        "minority_status": "dominant",
        "religiosity_level": 42,
        "gender": "female",
        "primary_language": "English",
        "secondary_languages": ["Spanish"],
    }

    baseline = backbone_state_from_identity(identity, year=2024, age=18)
    bridged = backbone_state_from_identity(
        identity,
        year=2024,
        age=18,
        v5_runtime_input_bundle={
            "status": "attached",
            "source": "driver_bundle",
            "payload": {"bundle": "identity-hydration"},
            "provenance": {"owner": "v5"},
        },
        v5_runtime_input_refs=["bundle://v5/hydration"],
        v5_bridge_status="attached",
        v5_runtime_input_notes=["refs-not-beliefs"],
    )

    baseline_dict = state_to_dict(baseline)
    bridged_dict = state_to_dict(bridged)

    for key, value in baseline_dict.items():
        if key in {"v5_runtime_input_bundle", "v5_runtime_input_refs", "v5_bridge_status"}:
            continue
        assert bridged_dict[key] == value, key

    assert bridged.v5_bridge_status == "attached"
    assert bridged.v5_runtime_input_refs == ["bundle://v5/hydration"]
    assert bridged.v5_runtime_input_bundle["status"] == "attached"
    assert bridged.v5_runtime_input_bundle["source"] == "driver_bundle"
    assert bridged.v5_runtime_input_bundle["payload"] == {"bundle": "identity-hydration"}
    assert bridged.v5_runtime_input_bundle["provenance"] == {"owner": "v5"}
    assert bridged.initial_state_provenance == baseline.initial_state_provenance
