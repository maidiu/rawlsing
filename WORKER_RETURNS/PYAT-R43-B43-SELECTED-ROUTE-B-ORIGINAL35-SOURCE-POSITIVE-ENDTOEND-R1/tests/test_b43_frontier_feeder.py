from __future__ import annotations
from fractions import Fraction
from types import SimpleNamespace
import pytest
from b43 import feeder
from b43.admission import B43AdmissionDenied, IssuerBoundAdmission, IssuerDescriptorContract
from b43 import frontier

def _contract():
    doc = {"operations": {"op1": {"release_tag": "R1", "source_edition": "ED1",
                                  "native_item_ids": ["I1", "I2"]}}}
    return IssuerDescriptorContract.from_document(doc, issuer_ref="ISSUER_T")

def _plan(*, edition="ED1", items=("I1", "I2"), tag="R1"):
    spec = SimpleNamespace(op_id="op1", release_tag=tag, source_edition=edition,
                           native_item_ids=tuple(items))
    return SimpleNamespace(op_specs={"op1": spec},
                           releases={tag: SimpleNamespace(source_edition=edition)})

def _grant(**kw):
    base = dict(grant_id="G1", source_id="SRC01", host_ref="H1", purpose_ref="P1",
                operation_ref="OP1", issuer_ref="ISS1", valid_until="2026-12-31T00:00:00-0400",
                source_editions=("ED1",))
    base.update(kw)
    return feeder.SourceGrant(**base)

def test_valid_issuer_bound_plan_admits():
    out = IssuerBoundAdmission(_contract()).admit(_plan())
    assert out["state"] == "B43_ISSUER_BOUND_ADMITTED" and out["checked_count"] == 1

def test_forged_source_edition_denied_early():
    with pytest.raises(B43AdmissionDenied, match="SOURCE_EDITION_MISMATCH"):
        IssuerBoundAdmission(_contract()).admit(_plan(edition="FORGED_CALLER_EDITION"))

def test_forged_native_item_ids_denied_early():
    with pytest.raises(B43AdmissionDenied, match="NATIVE_ITEM_IDS_MISMATCH"):
        IssuerBoundAdmission(_contract()).admit(_plan(items=("I1", "FOREIGN_ITEM")))

def test_forged_release_tag_denied_early_not_keyerror():
    with pytest.raises(B43AdmissionDenied, match="RELEASE_TAG_MISMATCH"):
        IssuerBoundAdmission(_contract()).admit(_plan(tag="FORGED_TAG"))

def test_unregistered_operation_denied():
    p = _plan()
    p.op_specs["opX"] = SimpleNamespace(op_id="opX", release_tag="R1",
                                       source_edition="ED1", native_item_ids=("I1", "I2"))
    with pytest.raises(B43AdmissionDenied, match="UNREGISTERED_OPERATION"):
        IssuerBoundAdmission(_contract()).admit(p)

def test_no_grant_is_pending_not_measured():
    out = feeder.request_source_positive(grant=None, request={"source_id": "SRC01",
        "host_ref": "H1", "purpose_ref": "P1", "operation_ref": "OP1"},
        plan=_plan(), admission=IssuerBoundAdmission(_contract()))
    assert out["state"] == "SOURCE_EXECUTION_PENDING_OWNER"
    assert out["measured_output"] is None and out["raw_source_read"] is False

def test_revoked_and_wrong_purpose_grants_refused():
    req = {"source_id": "SRC01", "host_ref": "H1", "purpose_ref": "P1", "operation_ref": "OP1"}
    for g, code in ((_grant(revoked=True), "GRANT_REVOKED"),
                    (_grant(purpose_ref="P2"), "GRANT_WRONG_PURPOSE")):
        out = feeder.request_source_positive(grant=g, request=req, plan=_plan(),
                                             admission=IssuerBoundAdmission(_contract()))
        assert out["state"] == "SOURCE_EXECUTION_PENDING_OWNER" and code in out["reason"]

def test_raw_source_read_without_grant_refused():
    with pytest.raises(feeder.B43GrantDenied, match="RAW_SOURCE_READ_WITHOUT_GRANT"):
        feeder.guard_raw_source_read("/private/wave1.sav", None)

def test_granted_without_stream_does_not_fabricate():
    out = feeder.request_source_positive(grant=_grant(),
        request={"source_id": "SRC01", "host_ref": "H1", "purpose_ref": "P1",
                 "operation_ref": "OP1", "source_edition": "ED1"},
        plan=_plan(), admission=IssuerBoundAdmission(_contract()))
    assert out["state"] == "SOURCE_STREAM_NOT_SUPPLIED"
    assert out["measured_output"] is None

def test_granted_path_calls_real_selected_b_owner(monkeypatch):
    called = {}
    def fake_owner(**kw):
        called.update(kw)
        return {"receipt_identity": "SYNTHETIC_CONTRACT_TEST"}
    # The owner import is inside the function; patch the module attribute it imports.
    import rawlsing_next.pre553_route_b_production as rbp
    monkeypatch.setattr(rbp, "execute_route_b_production", fake_owner)
    out = feeder.request_source_positive(grant=_grant(),
        request={"source_id": "SRC01", "host_ref": "H1", "purpose_ref": "P1",
                 "operation_ref": "OP1", "source_edition": "ED1"},
        plan=_plan(), admission=IssuerBoundAdmission(_contract()),
        source="SRC", projection="PROJ", runtime_catalog="CAT",
        i03_requests=("Q1",), discovery_authority_ref="DISC")
    assert out["state"] == "EXECUTED_UNDER_GRANT"
    assert called["source"] == "SRC" and called["i03_requests"] == ("Q1",)

def test_owner_call_contract_is_real():
    out = feeder.owner_call_contract()
    assert out["owner"].endswith("execute_route_b_production")

def test_all35_frontier_is_complete_and_unexecuted(fr):
    assert fr["wave_count"] == 35
    assert len(fr["waves"]) == 35
    assert all(w["raw_source_permitted"] is False for w in fr["waves"])
    assert all(w["executed_original_operations"] == 0 for w in fr["waves"])
    assert all(w["expected_original_operations"] is None for w in fr["waves"])
    assert fr["executed_original_operations_total"] == 0
    assert fr["expected_original_operations_total"] is None

def test_fixture_frontier_is_not_original(fr):
    f = fr["fixture_frontier"]
    assert (f["produced"], f["held"], f["inadmissible"]) == (3, 16, 6)
    assert f["counts_toward_original_occupancy"] is False

def test_decision_docket_covers_all_waves(docket):
    assert docket["wave_count"] == 35 and len(docket["rows"]) == 35
    assert all(r["state"] == "PENDING_COMPETENT_OWNER" for r in docket["rows"])
