"""WG0P7 — the exact 14 WG0O frozen authority-API controls, JUnit grade.

Uses the WG0O's frozen oracle and its UNCHANGED adapter; this file only asserts
the admission law and the repair's typed outcomes.  It is an author regression,
not independent acceptance.
"""
import json
import pathlib
import sys

import pytest

RET = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RET / "repro"))

import phase_b_support_v1 as S  # noqa: E402
import authority_seam_adapter_v1 as A  # noqa: E402

CASES = json.loads((RET / "repro" / "01_FROZEN_ACTUAL_AUTHORITY_API_CASES.json").read_text())["controls"]
_COURT = {}


def court():
    if "c" not in _COURT:
        _COURT["c"] = A.AuthoritySeamCourt()
    return _COURT["c"]


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["case"])
def test_frozen_control(case):
    out = court().execute_case(case["group"], case["case"])
    if case["kind"] == "NEGATIVE_REFUSAL":
        assert out["served_supported_original_fact"] is False, out
        assert out["supported_fact_cells_served"] == 0, out
        assert out["new_I03_calls"] == 0, out
        assert out["typed_refusal"] is not None, out
        assert out["exception_type"] in (
            "IdentityError", "FrontierError", "RevocationError", "ColdRestartError",
            "NativeDataError", "BatchIntegrityError",
            "Pre553IntegrityError", "Pre553AuthorityError", "Pre553AuthorityConflict",
            "Pre553SemanticCollapseError", "AuthorityCurrentnessHold"), out
    else:
        assert out["exception_type"] is None, out
        assert out["served_supported_original_fact"] is True, out
        assert out["supported_fact_cells_served"] == 42, out
        assert out["consumer"], out


def test_three_reds_are_closed_typed_before_i03():
    """A2 HELD; A3/A4 REFUSED; none served; none reached native I03."""
    by = {}
    for name in ("A2_stale_issuer_epoch_same_identity",
                 "A3_same_hash_foreign_signed_body",
                 "A4_foreign_governed_operations_same_hash"):
        case = next(c for c in CASES if c["case"] == name)
        by[name] = court().execute_case(case["group"], case["case"])
    assert by["A2_stale_issuer_epoch_same_identity"]["typed_refusal"] == "HELD"
    assert by["A3_same_hash_foreign_signed_body"]["typed_refusal"] == "REFUSED"
    assert by["A4_foreign_governed_operations_same_hash"]["typed_refusal"] == "REFUSED"
    for out in by.values():
        assert out["supported_fact_cells_served"] == 0
        assert out["new_I03_calls"] == 0
