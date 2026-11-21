"""Sourcefree SRC16 racpres operator and preflight regression tests."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src16_operator import (  # noqa: E402
    HISTORICAL_GRADE,
    OPERATION,
    QUESTION_ID,
    Src16Dependency,
    Src16OperatorError,
    materialize,
    validate_preflight,
)


SOURCE = "SOURCE_ARTIFACT|GSS1972.sav|" + "e" * 64
RELEASE = "C11_STREAM_SOURCEFREE_RELEASE|GSS_1972_SOURCE_ARTIFACT|" + "d" * 64
UNIVERSE = (
    "EmpiricalUniverse@1.0.0|"
    "urn:rawlsing:pre553:EmpiricalUniverse:sha256:" + "8" * 64 + "|" + "8" * 64
)
REPLAY = "f" * 64
QUESTION = (
    "NATIVE_QUESTION|urn:rawlsing:r157:source:SRC16:question_impl.phase0."
    "29b0dec400d8150f5123|96e5d1e48d463ec0bf049a7ba4e12754e0c8942bb3238b1da20a36190177b9b1"
)
HISTORICAL = (
    "AuthoritySnapshot@1.0.0|"
    "urn:rawlsing:pre553:AuthoritySnapshot:sha256:" + "a" * 64 + "|" + "a" * 64
)
ROOTS = {"source": SOURCE, "release": RELEASE, "universe": UNIVERSE, "replay": REPLAY}
SCOPE = {
    "host": "sourcefree-host",
    "scope": "GSS1972_RACPRES_RAW_UNWEIGHTED_RECORDED_RESPONSE_ONLY",
    "question_id": QUESTION_ID,
    "questionnaire_sha256": "c" * 64,
    "denominator": {"asked_risk": "HELD_ROUTING_UNKNOWN", "recorded_raw_codes": [1, 2]},
}


def _owner(*, codes=("1", "2"), interpretation=None, approved_states=None):
    if interpretation is None:
        interpretation = {str(code): ["SUBSTANTIVE_RESPONSE"] for code in codes}
    scope = dict(SCOPE)
    scope["denominator"] = {
        "asked_risk": "HELD_ROUTING_UNKNOWN",
        "recorded_raw_codes": [int(code) if str(code).lstrip("-").isdigit() else code for code in codes],
    }
    return {
        "schema": "ANVIL_Q006_SRC16_OWNER_DECISION@1",
        "source_id": "SRC16",
        "source_binding": {
            "custody_estate_path": "/sourcefree/src16",
            "decision_ref": "USER_SOURCE_DECISION|sourcefree-src16|" + "1" * 64,
            "manifest_sha256": "2" * 64,
            "saved_i02": ROOTS,
            "source_sha256": SOURCE,
        },
        "host": "sourcefree-host",
        "scope": scope,
        "question_id": QUESTION_ID,
        "native_question_ref": QUESTION,
        "questionnaire_sha256": "c" * 64,
        "denominator": {
            "asked_risk": "HELD_ROUTING_UNKNOWN",
            "recorded_raw_codes": list(codes),
        },
        "interpretation": interpretation,
        "authorized_operation": OPERATION,
        "historical_scope_grade": HISTORICAL_GRADE,
        "historical_snapshot_ref": HISTORICAL,
        "approved_nonanswer_states": list(approved_states or ()),
    }


def _r2():
    return {
        "waves": {
            "SRC16": {
                "custody_estate_path": "/sourcefree/src16",
                "decision_ref": "USER_SOURCE_DECISION|sourcefree-src16|" + "1" * 64,
                "manifest_sha256": "2" * 64,
                "saved_i02": ROOTS,
                "source_sha256": SOURCE,
            }
        }
    }


def _write(tmp_path, name, value):
    path = tmp_path / name
    path.write_text(json.dumps(value, sort_keys=True))
    return path


def test_src16_materializer_and_preflight_accept_exact_structured_scope(tmp_path):
    owner_path = _write(tmp_path, "owner.json", _owner())
    r2_path = _write(tmp_path, "r2.json", _r2())
    output = tmp_path / "operation.json"
    materialize(owner_path=owner_path, r2_path=r2_path, output=output)
    operation = json.loads(output.read_text())
    assert operation["source_id"] == "SRC16"
    assert operation["question_ref"]["object_id"] == QUESTION.split("|")[1]
    assert operation["allowed_raw_codes"] == ["1", "2"]
    assert operation["historical_scope_grade"] == HISTORICAL_GRADE

    use = {
        "owner_decision_sha256": sha256(owner_path.read_bytes()).hexdigest(),
        "operation_document_sha256": sha256(output.read_bytes()).hexdigest(),
        "historical_scope_grade": HISTORICAL_GRADE,
        "historical_snapshot_ref": HISTORICAL,
        "scope": SCOPE,
        "operation": OPERATION,
        "recorded_raw_codes": ["1", "2"],
    }
    use_path = _write(tmp_path, "use.json", use)
    closure = [{
        "ref": HISTORICAL, "state": "DEFER", "semantic_scope": HISTORICAL_GRADE,
    }]
    closure_path = _write(tmp_path, "closure.json", closure)
    prepared = validate_preflight(
        owner_bytes=owner_path.read_bytes(),
        r2=_r2(),
        operation_bytes=output.read_bytes(),
        use_bytes=use_path.read_bytes(),
        closure_bytes=closure_path.read_bytes(),
    )
    assert prepared.expected_scope == SCOPE
    assert prepared.codes == ("1", "2")
    assert prepared.historical_scope_grade == HISTORICAL_GRADE


def test_src16_preflight_refuses_stale_and_mismatched_shape(tmp_path):
    owner_path = _write(tmp_path, "owner.json", _owner())
    r2_path = _write(tmp_path, "r2.json", _r2())
    output = tmp_path / "operation.json"
    materialize(owner_path=owner_path, r2_path=r2_path, output=output)
    operation = output.read_text()
    owner_bytes = owner_path.read_bytes()
    base_use = {
        "owner_decision_sha256": sha256(owner_bytes).hexdigest(),
        "operation_document_sha256": sha256(operation.encode()).hexdigest(),
        "historical_scope_grade": HISTORICAL_GRADE,
        "historical_snapshot_ref": HISTORICAL,
        "scope": SCOPE,
        "operation": OPERATION,
        "recorded_raw_codes": ["1", "2"],
    }
    closure = [{"ref": HISTORICAL, "state": "DEFER", "semantic_scope": HISTORICAL_GRADE}]
    cases = [
        ("stale_operation", {**base_use, "operation_document_sha256": "0" * 64}),
        ("wrong_scope_field", {**base_use, "scope": {**SCOPE, "host": "other"}}),
        ("wrong_grade", {**base_use, "historical_scope_grade": "EXACT_SOURCE_CODEBOOK_AND_H48_EVIDENCE_ONLY"}),
        ("wrong_codes", {**base_use, "recorded_raw_codes": ["1"]}),
    ]
    for _label, use in cases:
        with pytest.raises(Src16OperatorError):
            validate_preflight(
                owner_bytes=owner_bytes, r2=_r2(), operation_bytes=operation.encode(),
                use_bytes=json.dumps(use).encode(), closure_bytes=json.dumps(closure).encode(),
            )
    with pytest.raises(Src16OperatorError, match="closure|DEFER|historical"):
        validate_preflight(
            owner_bytes=owner_bytes, r2=_r2(), operation_bytes=operation.encode(),
            use_bytes=json.dumps(base_use).encode(),
            closure_bytes=json.dumps([{"ref": HISTORICAL, "state": "ALLOW"}]).encode(),
        )


def test_src16_state_bearing_stored_codes_are_explicit_and_binned(tmp_path):
    codes = ("1", "2", "-98", "-99", "-100")
    owner = _owner(
        codes=codes,
        interpretation={
            "1": ["SUBSTANTIVE_RESPONSE"],
            "2": ["SUBSTANTIVE_RESPONSE"],
            "-98": ["DK"],
            "-99": ["MISSING"],
            "-100": ["INAPPLICABLE"],
        },
        approved_states=("DK", "MISSING", "INAPPLICABLE"),
    )
    owner_path = _write(tmp_path, "owner.json", owner)
    r2_path = _write(tmp_path, "r2.json", _r2())
    output = tmp_path / "op.json"
    materialize(owner_path=owner_path, r2_path=r2_path, output=output)
    operation = json.loads(output.read_text())
    assert operation["state_bearing_raw_codes"] is True
    assert operation["scope_kind"] == "OBSERVED_STORED_CODE_FREQUENCIES"
    assert operation["asked_eligibility"] == "HELD_NOT_PROVEN"
    assert operation["substantive_vote_denominator"] is False
    assert operation["allowed_raw_codes"] == list(codes)
    assert operation["interpretation"] == [
        ["1", "SUBSTANTIVE_RESPONSE"],
        ["2", "SUBSTANTIVE_RESPONSE"],
        ["-98", "DK"],
        ["-99", "MISSING"],
        ["-100", "INAPPLICABLE"],
    ]


def test_src16_unknown_code_state_is_an_exact_dependency(tmp_path):
    owner = _owner(
        codes=("1", "2", "-98"),
        interpretation={
            "1": ["SUBSTANTIVE_RESPONSE"],
            "2": ["SUBSTANTIVE_RESPONSE"],
            "-98": ["NOT_A_RECORDED_STATE"],
        },
    )
    owner_path = _write(tmp_path, "owner.json", owner)
    r2_path = _write(tmp_path, "r2.json", _r2())
    with pytest.raises(Src16Dependency, match="CODE_STATE_CLASSIFICATION_REQUIRED"):
        materialize(owner_path=owner_path, r2_path=r2_path, output=tmp_path / "op.json")


def test_saved_binary_contrast_shape_is_exact_not_alias():
    from rawlsing_next.pre553_anvil_stream_recorded import (
        RecordedResponseError, _translate_saved_scalar_topology,
    )

    actual = {
        "index": 0,
        "kind": "BINARY_CONTRAST_SINGLE",
        "source_manual_topology": "binary_contrast",
    }
    translated = _translate_saved_scalar_topology(actual)
    assert translated["kind"] == "SCALAR_SINGULAR"
    assert translated["source_manual_topology"] == "binary_contrast"
    for malformed in (
        {**actual, "index": 1},
        {**actual, "source_manual_topology": "other"},
        {**actual, "rank": 1},
    ):
        with pytest.raises(RecordedResponseError):
            _translate_saved_scalar_topology(malformed)
    ordered = {**actual, "kind": "ORDERED_SEQUENCE"}
    assert _translate_saved_scalar_topology(ordered) == ordered
    unknown = {**actual, "kind": "UNKNOWN_TOPOLOGY"}
    assert _translate_saved_scalar_topology(unknown) == unknown
