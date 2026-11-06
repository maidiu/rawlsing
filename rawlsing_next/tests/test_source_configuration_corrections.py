"""Source/hash-bound R157 config corrections for the SRC31 response boundary."""
from __future__ import annotations

import json
from pathlib import Path

from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key
from rawlsing_next.source_configuration.corrections import (
    CORRECTIONS_PATH,
    apply_source_config_corrections,
)
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.source_configuration.provider import GitObjectProvider
from rawlsing_next.source_configuration.schema import SourceConfig

ROOT = Path(__file__).resolve().parents[2]
SRC31_PATH = "rawlsing_next/source_configuration/data/SRC31/source.config.json"


def _base_document() -> dict:
    return json.loads(GitObjectProvider().read_bytes(SRC31_PATH).decode("utf-8"))


def _slot(document: dict, name: str) -> dict:
    return next(s for s in document["response_slots"] if s["slot"]["name"] == name)


def _value(slot: dict, raw: float) -> dict:
    return next(v for v in slot["values"] if v["raw_value"] == raw)


def test_src31_correction_is_source_hash_and_base_hash_bound():
    base = _base_document()
    corrected, applied = apply_source_config_corrections(base)
    assert len(applied) == 31
    assert corrected["response_slots"] != base["response_slots"]
    # A different source SHA or base canonical hash must not inherit the correction.
    wrong_sha = json.loads(json.dumps(base))
    wrong_sha["identity"]["expected_source_sha256"] = "f" * 64
    _, wrong_applied = apply_source_config_corrections(wrong_sha)
    assert wrong_applied == []
    wrong_base = json.loads(json.dumps(base))
    wrong_base["config_revision"] += 1
    _, wrong_base_applied = apply_source_config_corrections(wrong_base)
    assert wrong_base_applied == []


def test_src31_declared_user_missing_codes_are_typed_not_substantive():
    base = _base_document()
    old = SourceConfig(base)
    corrected, _ = apply_source_config_corrections(base)
    fixed = SourceConfig(corrected)
    for name, raw, state in (
        ("c10ai", 98.0, "DK"),
        ("c10ai", 99.0, "NOT_ASKED"),
        ("c12", 8.0, "DK"),
        ("c18a", 0.0, "SOURCE_SPECIFIC_SPECIAL"),
        ("d3", 9.0, "NOT_ASKED"),
        ("d13", 9.0, "NOT_ASKED"),
    ):
        before = _value(_slot(old.document, name), raw)
        after = _value(_slot(fixed.document, name), raw)
        assert before["missing_state"] == "OBSERVED_STORAGE_VALUE"
        assert after["missing_state"] == "FORMAT_USER_MISSING_VALUE"
        assert after["response_state"] == state
        assert after["source_missing_declaration"] is not None
        assert after["canonical_value"] is None
        assert after["source_missing_declaration"] == {"kind": "discrete", "value": raw}
        assert physical_value_binding_key(raw, PhysicalMissingState.FORMAT_USER_MISSING_VALUE, after["source_missing_declaration"]) == physical_value_binding_key(raw, PhysicalMissingState.FORMAT_USER_MISSING_VALUE, {"kind": "discrete", "value": raw})


def test_src31_observed_undeclared_codes_are_typed_unresolved_not_substantive():
    corrected, _ = apply_source_config_corrections(_base_document())
    for name, codes in (("d7", (46.0, 67.0, 80.0, 81.0, 82.0, 83.0, 84.0, 86.0)),
                        ("d12", (7.0, 8.0, 12.0, 16.0, 20.0, 29.0, 89.0, 93.0, 94.0))):
        slot = _slot(corrected, name)
        for raw in codes:
            value = _value(slot, raw)
            assert value["missing_state"] == "OBSERVED_STORAGE_VALUE"
            assert value["response_state"] == "INVALID_UNRESOLVED"
            assert value["canonical_value"] is None


def test_library_exposes_corrections_without_changing_denominators_or_fixture():
    library = SourceConfigLibrary.from_pinned_r157()
    original = library.load_original("SRC31")
    fixture = library.load_fixture_config("SRC31")
    assert len(original.corrections_applied) == 31
    assert fixture.corrections_applied == ()
    assert len(original.document["items"]) == 68
    assert len(original.document["physical_slots"]) == 68
    assert len(original.document["response_slots"]) == 64
    selected = library.select("SRC31")
    assert len(selected["corrections_applied"]) == 31
    validation = library.validate_source("SRC31")
    assert validation["passed"] is True
    assert len(validation["corrections_applied"]) == 31


def test_registry_is_versioned_resource_data_with_pinned_lineage():
    registry = json.loads(CORRECTIONS_PATH.read_text(encoding="utf-8"))
    assert registry["schema"] == "PYAT_R157_SOURCE_CONFIGURATION_CORRECTION@1.0.0"
    entry = registry["entries"][0]
    assert entry["source_id"] == "SRC31"
    assert entry["source_sha256"] == "de7b51f9abf455b072555a84c5592e3ac46bb32c4f9f61bc055160f7d871e571"
    assert entry["base_commit"] == "1924499ef52403a0f331b8aff9b7c7eff99bf1e2"
    assert entry["base_config_path"] == SRC31_PATH
    assert len(entry["base_config_canonical_sha256"]) == 64
    assert entry["config_purpose"] == "SOURCE_PREPARATION"
    assert entry["identity_class"] == "ORIGINAL_SOURCE"
    assert {change["slot"]["name"] for change in entry["response_value_changes"]} == {
        "c10ai", "c12", "c17", "c18a", "c18b", "c18d", "c18e", "d3", "d7", "d12", "d13"}
