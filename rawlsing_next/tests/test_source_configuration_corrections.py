"""Source/hash-bound corrections for accepted response and SRC15 coordinate gaps."""
from __future__ import annotations

import json
from pathlib import Path

from rawlsing_next.source_configuration.corrections import (
    CORRECTIONS_PATH,
    SourceCorrectionError,
    apply_source_config_corrections,
)
from rawlsing_next.source_configuration.factory import build_coordinate_slot_rules
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.source_configuration.provider import GitObjectProvider
from rawlsing_next.source_configuration.schema import SourceConfig

R157_COMMIT = "1924499ef52403a0f331b8aff9b7c7eff99bf1e2"
SRC31_PATH = "rawlsing_next/source_configuration/data/SRC31/source.config.json"


def _registry() -> dict:
    return json.loads(CORRECTIONS_PATH.read_text(encoding="utf-8"))


def test_src15_coordinate_missing_range_and_observed_age_codes_are_bound():
    library = SourceConfigLibrary.from_pinned_r157()
    config = library.load_original("SRC15")
    assert len(config.corrections_applied) == 11
    slot = next(s for s in config.document["coordinate_slots"] if s["slot"]["name"] == "age_r2")
    values = {v["raw_value"]: v for v in slot["values"]}
    for raw in (-10.0, -9.0, -8.0, -5.0, -4.0, -3.0, -2.0, -1.0):
        assert values[raw]["missing_state"] == "FORMAT_USER_MISSING_RANGE"
        assert values[raw]["source_missing_declaration"] == {"kind": "range", "lo": -10.0, "hi": -1.0}
    for raw in (1.0, 2.0, 3.0):
        assert values[raw]["missing_state"] == "OBSERVED_STORAGE_VALUE"
        assert values[raw]["coordinate_state"] == "UNKNOWN"
        assert values[raw]["canonical_value"] is None
    assert len(slot["values"]) == 11
    assert len(config.document["items"]) == 474
    assert len(config.document["physical_slots"]) == 474
    assert len(config.document["response_slots"]) == 337
    validation = library.validate_source("SRC15")
    assert validation["passed"] is True
    assert len(validation["corrections_applied"]) == 11


def test_src31_accepted_correction_and_provenance_are_unchanged():
    library = SourceConfigLibrary.from_pinned_r157()
    config = library.load_original("SRC31")
    assert len(config.corrections_applied) == 31
    base = json.loads(GitObjectProvider().read_bytes(SRC31_PATH).decode("utf-8"))
    _, unproven = apply_source_config_corrections(base)
    assert unproven == []
    for bad_commit, bad_path in (("f" * 40, SRC31_PATH), (R157_COMMIT, "wrong/SRC31.config.json")):
        try:
            apply_source_config_corrections(base, base_commit=bad_commit, base_config_path=bad_path)
        except SourceCorrectionError as error:
            assert "CORRECTION_BASE_PROVENANCE_MISMATCH" in str(error)
        else:
            raise AssertionError("mismatched base provenance was not refused")
    _, restored = apply_source_config_corrections(
        base, base_commit=R157_COMMIT, base_config_path=SRC31_PATH)
    assert len(restored) == 31


def test_composite_labels_remain_conservative_and_no_substantive_additions():
    registry = _registry()
    composite = {
        ("SRC16", "dk, na, iap"), ("SRC24", "No answer/Refused"),
        ("SRC25", "DK/NA"), ("SRC25", "Don't know / Don't answer"),
        ("SRC25", "Don't know/No answer"), ("SRC25", "Don't know/No asnwer"),
        ("SRC25", "No answer/Don't know"), ("SRC25", "No answer/Refused"),
        ("SRC26", "Don't know / No answer"), ("SRC26", "Don't know/Don't remember"),
    }
    matched = 0
    for entry in registry["entries"]:
        for change in entry["response_value_changes"]:
            if (entry["source_id"], change.get("source_label")) in composite:
                matched += 1
                assert change["response_state"] == "SOURCE_SPECIFIC_SPECIAL"
    assert matched == 362
    assert not any(
        change.get("response_state") == "SUBSTANTIVE_RESPONSE"
        for entry in registry["entries"] for change in entry["response_value_changes"])


def test_95_substantive_to_missing_transitions_remain_warranted():
    registry = _registry()
    provider = GitObjectProvider()
    transitions = []
    for entry in registry["entries"]:
        if entry["source_id"] == "SRC31":
            continue
        base = SourceConfig(json.loads(provider.read_bytes(entry["base_config_path"]).decode("utf-8")))
        slots = {(s["slot"]["ordinal"], s["slot"]["name"]): s for s in base.document["response_slots"]}
        for change in entry["response_value_changes"]:
            slot = slots[(change["slot"]["ordinal"], change["slot"]["name"])]
            old = next((v for v in slot["values"]
                        if type(v["raw_value"]) is type(change["raw_value"])
                        and v["raw_value"] == change["raw_value"]), None)
            if old and old.get("response_state") == "SUBSTANTIVE_RESPONSE" and change["response_state"] != "SUBSTANTIVE_RESPONSE":
                transitions.append(change)
    assert len(transitions) == 95
    for change in transitions:
        assert change["missing_state"] != "OBSERVED_STORAGE_VALUE"
        assert change.get("source_missing_declaration") is not None
        assert change["response_state"] != "SUBSTANTIVE_RESPONSE"


def test_src15_coordinate_rules_are_exposed_to_current_owner():
    config = SourceConfigLibrary.from_pinned_r157().load_original("SRC15")
    rules = build_coordinate_slot_rules(config)
    age = next(rule for rule in rules if rule.slot.name == "age_r2")
    keys = {rule.physical_key for rule in age.values}
    assert len(keys) == 11
    assert all(rule.coordinate_state in {"UNKNOWN", "MISSING", "NOT_LAWFULLY_CONDITIONABLE"} for rule in age.values)
    # The missing range is bound by exact declaration; observed age codes remain typed unknown.
    missing = [rule for rule in age.values if rule.coordinate_state == "MISSING"]
    assert len(missing) >= 1
