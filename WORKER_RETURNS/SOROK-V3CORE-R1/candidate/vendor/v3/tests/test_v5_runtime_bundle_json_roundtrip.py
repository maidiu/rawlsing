from __future__ import annotations

from v3.core.state import BackboneState
from v3.io.json_codec import state_from_json, state_to_json
from v3.io.v5_bridge import attach_v5_runtime_input_bundle


def test_v5_runtime_bundle_json_roundtrip() -> None:
    state = BackboneState(year=2026, age=31)
    state.autonomy_drive = 73.25
    state.safety_condition = 61.5

    attach_v5_runtime_input_bundle(
        state,
        {
            "status": "degraded",
            "source": "driver_bundle",
            "payload": {"bridge": "carrier-only", "stage": 1},
            "provenance": {"owner": "v5", "scope": "bridge"},
        },
        refs=["bundle://v5/alpha", "bundle://v5/beta"],
        notes=["carrier-only", "json-roundtrip"],
    )

    encoded = state_to_json(state, indent=2)
    loaded = state_from_json(encoded)

    assert loaded.year == 2026
    assert loaded.age == 31
    assert loaded.autonomy_drive == 73.25
    assert loaded.safety_condition == 61.5
    assert loaded.v5_bridge_status == "degraded"
    assert loaded.v5_runtime_input_refs == ["bundle://v5/alpha", "bundle://v5/beta"]
    assert loaded.v5_runtime_input_bundle["status"] == "degraded"
    assert loaded.v5_runtime_input_bundle["source"] == "driver_bundle"
    assert loaded.v5_runtime_input_bundle["payload"] == {"bridge": "carrier-only", "stage": 1}
    assert loaded.v5_runtime_input_bundle["provenance"] == {"owner": "v5", "scope": "bridge"}
    assert loaded.v5_runtime_input_bundle["refs"] == ["bundle://v5/alpha", "bundle://v5/beta"]
    assert loaded.v5_runtime_input_bundle["notes"] == ["carrier-only", "json-roundtrip"]
