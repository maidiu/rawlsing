"""PYAT HQ280 PV3 A04TU - independent worker-authored V2 mutation hostiles.

Development-only, source-free.  This file is authored INDEPENDENTLY of the
A04T candidate suite: it builds its own raw-field payload (own item labels,
own SOURCE tag), drives the REAL source-free owner chain
(C11 -> Route B/I03/I05 -> Batch) through the A04T join worker in one
process, then mutates payload/manifest/result BETWEEN production and the
SEPARATE verifier subprocess and asserts typed failure codes.

Nothing here copies the candidate suite's frozen rows or assertions.  Where a
commission-mandated scenario necessarily overlaps an existing one (e.g. a
missing J2), the payload is independently authored and the assertion names
the exact recomputed identity, not a copied shape.

Conventions: ``_tu_`` marks worker-owned helpers.  ``H-M00`` is the honest
positive control (six RUNNABLE jobs + all four H/D/NA rows, structural PASS
with standing holds).  ``H-M01``..``H-M17`` are hostiles.  Every hostile that
goes through the chain uses two real OS processes (produce, then verify);
unit-level checks call the stdlib-only verifier directly.

No raw SAV/DTA is read; no accepted owner, A04, A04S or A05 file is modified.
"""

from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

import rawlsing_next.pre553_original_workload_v2_verifier_candidate as V

REPO_ROOT = Path(__file__).resolve().parents[2]
RETURN_DIR = (
    REPO_ROOT / "WORKER_RETURNS"
    / "PYAT-HQ280-PV3-A04T-V2-VERIFIED-INDEPENDENT-JOIN-R1"
)
WORKER = RETURN_DIR / "repro" / "a04t_join_worker.py"

SCHEMA = V.ACCEPTED_EXPECTED_SCHEMA
TU_SOURCE = "SYNTHETIC-SOURCEFREE-A04TU"
TU_WAVE = "W1"
TU_C1 = "C1_ANALYTICAL_COMPOSITION"
TU_FF = "FIELD_FORGE_CONDITIONAL_SUPPORT"
TU_LEARNED = "LEARNED_EMPIRICAL_ADJUDICATION"


# --------------------------------------------------------------------------
# Worker-owned scope and payload authorship (own labels, own SOURCE tag)
# --------------------------------------------------------------------------
def _tu_scope():
    import rawlsing_next.tests.test_pre553_original_workload_contract_v2_candidate as T
    return T._v2_scope()


def _tu_raw(scope, item, sem, roles, target, cond=(), measure="RAW",
            risk="RISK-R-ALL", topo="SCALAR_SINGULAR", consumer=TU_C1,
            state="RUNNABLE", hold=None, mult=1, query_slot=None,
            predicate_slot=None):
    raw = {
        "source": TU_SOURCE, "wave": TU_WAVE, "item": item,
        "form": "F1", "slot": "S1",
        "semantic_op_class": sem, "semantic_roles": list(roles),
        "target": target, "condition_order": list(cond),
        "measure_kind": measure,
        "source_identity": scope["source_sha"],
        "authority_ref": scope["qauth"].authority_ref.key,
        "risk_identity": risk, "topology_identity": topo,
        "required_consumer": consumer, "state": state,
        "hold_reason": hold, "multiplicity": mult,
    }
    if state == "RUNNABLE":
        if sem == "BOUNDED_DISCOVERY":
            raw["discovery_authority_ref"] = scope["discovery_ref"].as_dict()
        else:
            raw["query_ref"] = scope["queries"][query_slot].ref.as_dict()
            if predicate_slot == "query":
                dep = scope["queries"][query_slot].dependency_refs[0]
                raw["predicate_ref"] = dep.as_dict() if hasattr(dep, "as_dict") else dict(dep)
            else:
                raw["predicate_ref"] = scope["all_p"].ref.as_dict()
    if query_slot is not None:
        raw["query_slot"] = query_slot
    if predicate_slot is not None:
        raw["predicate_slot"] = predicate_slot
    return raw


def _tu_honest(scope):
    """Six RUNNABLE jobs (P, Q, QW, QC, QJ, QD) + four H/D/NA rows."""
    return [
        _tu_raw(scope, "P", "UNARY_DISTRIBUTION", ("BASE",), "X",
                query_slot="x"),
        _tu_raw(scope, "Q", "UNARY_DISTRIBUTION", ("BASE",), "Y",
                query_slot="y"),
        _tu_raw(scope, "QW", "UNARY_DISTRIBUTION", ("BASE",), "Y",
                measure="GOVERNED_WEIGHTED", query_slot="y_weighted"),
        _tu_raw(scope, "QC", "UNARY_DISTRIBUTION", ("CONDITIONER", "TARGET"),
                "Y", cond=("X",), risk="RISK-R-COND",
                query_slot="y_given_x1", predicate_slot="query",
                consumer=TU_FF),
        _tu_raw(scope, "QJ", "PAIR_RESPONSE_COTRAVEL",
                ("CONDITIONER", "TARGET"), "J2", cond=("X", "Y"),
                risk="RISK-R-COMMON", topo="SCALAR_2X2_JOINT",
                consumer=TU_FF, query_slot="xy"),
        _tu_raw(scope, "QD", "BOUNDED_DISCOVERY", ("BASE",), "D1",
                topo="SCALAR_2X2", consumer=TU_LEARNED),
        _tu_raw(scope, "H1", "UNARY_DISTRIBUTION", ("BASE",), "H1",
                topo="ORDERED_SEQUENCE", state="HELD",
                hold="ORDERED_SEQUENCE_COLLAPSE_NOT_YET_AUTHORIZED"),
        _tu_raw(scope, "H2", "UNARY_DISTRIBUTION", ("BASE",), "H2",
                topo="REPEATED_EVENT", state="HELD",
                hold="REPEATED_EVENT_JOIN_NOT_YET_AUTHORIZED"),
        _tu_raw(scope, "DN", "UNARY_DISTRIBUTION", ("BASE",), "DN",
                state="DENIED", hold="EXPLICIT_FAIL_CLOSED_SOURCE_GAP"),
        _tu_raw(scope, "NA", "UNARY_DISTRIBUTION", ("BASE",), "NA",
                state="SOURCE_NONAPPLICABLE",
                hold="NO_COADMINISTERED_TARGET_IN_THIS_SLICE"),
    ]


def _tu_payload(raws, custodian=None):
    doc = {"schema": SCHEMA, "declarations": raws}
    if custodian is not None:
        doc["custodian"] = custodian
    return doc


def _tu_key(raw):
    return V.reconstruct_record(dict(raw), SCHEMA)["recomputed"]["expected_work_key"]


# --------------------------------------------------------------------------
# Worker-owned two-process chain drivers
# --------------------------------------------------------------------------
def _tu_produce(tmp_path, payload):
    (tmp_path / "payload.json").write_text(json.dumps(payload, sort_keys=True))
    r = subprocess.run(
        [sys.executable, str(WORKER), str(tmp_path), "produce"],
        capture_output=True, text=True, timeout=300, cwd=str(REPO_ROOT))
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads((tmp_path / "produced.json").read_text())


def _tu_produce_must_refuse(tmp_path, payload, pattern):
    (tmp_path / "payload.json").write_text(json.dumps(payload, sort_keys=True))
    r = subprocess.run(
        [sys.executable, str(WORKER), str(tmp_path), "produce"],
        capture_output=True, text=True, timeout=300, cwd=str(REPO_ROOT))
    assert r.returncode != 0, r.stdout[-2000:]
    assert pattern in (r.stdout + r.stderr), (r.stdout + r.stderr)[-2000:]
    return r


def _tu_verify(tmp_path):
    r = subprocess.run(
        [sys.executable, str(WORKER), str(tmp_path), "verify"],
        capture_output=True, text=True, timeout=300, cwd=str(REPO_ROOT))
    assert r.returncode == 0, r.stderr[-2000:]
    out = json.loads(r.stdout)
    assert out["candidate_import_blocked"] is True
    return json.loads((tmp_path / "verdict.json").read_text())


def _tu_join_against(tmp_path, submitted, expected):
    """Produce from SUBMITTED, then verify against EXPECTED (divergence)."""
    _tu_produce(tmp_path, _tu_payload(submitted))
    (tmp_path / "payload.json").write_text(
        json.dumps(_tu_payload(expected), sort_keys=True))
    return _tu_verify(tmp_path)


def _tu_unit_by_claimed(produced, claimed_key):
    for u in produced["units"]:
        if u.get("claimed_expected_work_key") == claimed_key:
            return u
    raise KeyError(claimed_key[:16])


# ==========================================================================
# H-M00: honest positive control - six-job outer join, all four H/D/NA
# ==========================================================================
def test_h_m00_positive_six_job_outer_join_passes_structurally(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    verdict = _tu_join_against(tmp_path, honest, honest)
    assert verdict["candidate_import_blocked"] is True
    assert verdict["verifier_contract"] == V.VERIFIER_CONTRACT_ID
    assert verdict["ok"] is True, verdict["failure_codes"]
    assert verdict["omitted"] == []
    assert verdict["extra"] == []
    assert len(verdict["expected_keys"]) == 6
    assert len(verdict["visible_non_runnable"]) == 4
    assert set(verdict["result_classes"].values()) <= V.MEASURED_RESULT_CLASSES
    assert verdict["unsatisfied_consumers"] == []
    assert "EXTERNAL_CUSTODIAN_ISSUER_HOLD" in verdict["holds"]
    assert "REAL_CONSUMER_MODELLED_NOT_EXECUTED" in verdict["holds"]
    assert verdict["actual_consumer_court"]["verdict"] == "HOLD"


# ==========================================================================
# H-M01: weighted + conditioned + raw Y omitted, P/J2/discovery kept
# ==========================================================================
def test_h_m01_q_family_partial_omission_is_exact(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    submitted = [r for r in honest if r["item"] not in ("Q", "QW", "QC")]
    verdict = _tu_join_against(tmp_path, submitted, honest)
    assert verdict["ok"] is False
    assert verdict["failure_codes"] == ["EXPECTED_OPERATION_OMITTED",
                                        "REQUIRED_CONSUMER_OMITTED"]
    assert set(verdict["omitted"]) == {
        _tu_key(next(r for r in honest if r["item"] == "Q")),
        _tu_key(next(r for r in honest if r["item"] == "QW")),
        _tu_key(next(r for r in honest if r["item"] == "QC")),
    }
    assert verdict["extra"] == []


# ==========================================================================
# H-M02: J2 dropped, everything else intact (commission-mandated shape,
# independently authored payload and exact-key assertion)
# ==========================================================================
def test_h_m02_j2_omission_is_exact_and_rest_verifies(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    submitted = [r for r in honest if r["item"] != "QJ"]
    verdict = _tu_join_against(tmp_path, submitted, honest)
    assert verdict["ok"] is False
    assert "EXPECTED_OPERATION_OMITTED" in verdict["failure_codes"]
    assert verdict["omitted"] == [
        _tu_key(next(r for r in honest if r["item"] == "QJ"))]
    assert verdict["extra"] == []
    # the surviving frontier still joins: 5 jobs matched, discovery intact
    assert len(verdict["job_keys"]) == 5


# ==========================================================================
# H-M03: same-count replacement - QC out, QX (yx query) in
# ==========================================================================
def test_h_m03_same_count_replacement_is_omission_plus_extra(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    qx = _tu_raw(scope, "QX", "UNARY_DISTRIBUTION", ("BASE",), "Y",
                 cond=("Y", "X"), query_slot="yx")
    submitted = [r for r in honest if r["item"] != "QC"] + [qx]
    verdict = _tu_join_against(tmp_path, submitted, honest)
    assert verdict["ok"] is False
    assert "EXPECTED_OPERATION_OMITTED" in verdict["failure_codes"]
    assert "UNAUTHORIZED_EXTRA_JOB" in verdict["failure_codes"]
    assert verdict["omitted"] == [
        _tu_key(next(r for r in honest if r["item"] == "QC"))]
    assert verdict["extra"] == [_tu_key(qx)]
    # manifest-level count is unchanged: the produced manifest still carries
    # 6 jobs, so raw counts prove nothing - only identities do
    produced = json.loads((tmp_path / "produced.json").read_text())
    assert len(produced["units"]) == 6
    assert len(verdict["job_keys"]) == 5


# ==========================================================================
# H-M04: conditioning lie - (X,Y) declared through the X-only query
# ==========================================================================
def test_h_m04_condition_arity_lie_fails_as_omission_plus_extra(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    submitted = [dict(r, condition_order=["X", "Y"]) if r["item"] == "QC" else r
                 for r in honest]
    verdict = _tu_join_against(tmp_path, submitted, honest)
    assert verdict["ok"] is False
    assert "EXPECTED_OPERATION_OMITTED" in verdict["failure_codes"]
    assert "UNAUTHORIZED_EXTRA_JOB" in verdict["failure_codes"]
    assert verdict["omitted"] == [
        _tu_key(next(r for r in honest if r["item"] == "QC"))]
    assert len(verdict["extra"]) == 1
    # the lie changes the semantic identity: the extra key is NOT the QC key
    assert verdict["extra"] != verdict["omitted"]


# ==========================================================================
# H-M05: measure infidelity, both directions
# ==========================================================================
def test_h_m05fwd_weighted_through_raw_query_is_claimed_ref_mismatch(tmp_path):
    """A WEIGHTED expectation executed through the RAW query is caught by
    the claimed-key/owner-ref cross-check, not by key identity: the v2 and
    V2 key grammars bind the owner query ref only through that cross-check."""
    scope = _tu_scope()
    honest = _tu_honest(scope)
    qw_via_y = dict(next(r for r in honest if r["item"] == "QW"),
                    query_slot="y",
                    query_ref=scope["queries"]["y"].ref.as_dict())
    submitted = [r for r in honest if r["item"] not in ("Q", "QW")] + [qw_via_y]
    verdict = _tu_join_against(tmp_path, submitted, honest)
    assert verdict["ok"] is False
    assert "CLAIMED_JOB_REF_MISMATCH" in verdict["failure_codes"]
    assert "EXPECTED_OPERATION_OMITTED" in verdict["failure_codes"]
    # the dropped Y-RAW job is the omission; the misbound job claims a known
    # key, so there is no UNAUTHORIZED_EXTRA_JOB here
    assert verdict["omitted"] == [
        _tu_key(next(r for r in honest if r["item"] == "Q"))]
    assert verdict["extra"] == []


def test_h_m05rev_raw_through_weighted_query_is_omission_plus_extra(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    qwr = dict(next(r for r in honest if r["item"] == "QW"),
               item="QWR", measure_kind="RAW",
               query_ref=scope["queries"]["y_weighted"].ref.as_dict())
    submitted = [r for r in honest if r["item"] != "QW"] + [qwr]
    verdict = _tu_join_against(tmp_path, submitted, honest)
    assert verdict["ok"] is False
    assert "EXPECTED_OPERATION_OMITTED" in verdict["failure_codes"]
    assert "UNAUTHORIZED_EXTRA_JOB" in verdict["failure_codes"]
    assert verdict["omitted"] == [
        _tu_key(next(r for r in honest if r["item"] == "QW"))]


# ==========================================================================
# H-M06: smuggled identity - risk changed, OLD key supplied as authentic
# ==========================================================================
def test_h_m06_forged_old_key_with_changed_identity_is_key_mismatch_only(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    old_q = next(r for r in honest if r["item"] == "Q")
    smuggled = dict(old_q, risk_identity="RISK-R-X",
                    expected_work_key=_tu_key(old_q))
    submitted = [smuggled if r["item"] == "Q" else r for r in honest]
    verdict = _tu_join_against(tmp_path, submitted, submitted)
    assert verdict["ok"] is False
    # the join itself is consistent (producer ignores the forged string and
    # claims the recomputed new key); ONLY the preimage check fires
    assert verdict["failure_codes"] == ["KEY_PREIMAGE_MISMATCH"]
    assert verdict["omitted"] == []
    assert verdict["extra"] == []


# ==========================================================================
# H-M07: one-to-many collision - consumer-only duplicate collapses
# ==========================================================================
def test_h_m07_consumer_only_duplicate_fails_closed_at_bind(tmp_path):
    """Two declarations differing ONLY in required_consumer share one
    semantic identity (consumer is not part of the expected-work key).
    The producer refuses the collapse at bind time.  By contrast the
    positive control proves legitimate dispatch-class reuse (one I03 class
    serving five distinct jobs) binds cleanly."""
    scope = _tu_scope()
    honest = _tu_honest(scope)
    dup = dict(next(r for r in honest if r["item"] == "P"),
               required_consumer=TU_FF)
    _tu_produce_must_refuse(tmp_path, _tu_payload(honest + [dup]),
                            "duplicate expected_work_key")


# ==========================================================================
# H-M08: declared multiplicity 2, owner yields 1
# ==========================================================================
def test_h_m08_multiplicity_overclaim_fails(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    submitted = [dict(r, multiplicity=2) if r["item"] == "P" else r
                 for r in honest]
    verdict = _tu_join_against(tmp_path, submitted, submitted)
    assert verdict["ok"] is False
    assert verdict["failure_codes"] == ["EXPECTED_MULTIPLICITY_MISMATCH"]


# ==========================================================================
# H-M09/M10: post-production result forgery (two-process: produced.json
# rewritten between produce and the separate verify subprocess)
# ==========================================================================
def _tu_forge_unit(tmp_path, submitted, claimed_key, **overrides):
    produced = _tu_produce(tmp_path, _tu_payload(submitted))
    forged = deepcopy(produced)
    unit = _tu_unit_by_claimed(forged, claimed_key)
    unit.update(overrides)
    (tmp_path / "produced.json").write_text(json.dumps(forged, sort_keys=True))
    return _tu_verify(tmp_path)


def test_h_m09a_observed_zero_over_zero_denominator_is_not_typed(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    qkey = _tu_key(next(r for r in honest if r["item"] == "Q"))
    verdict = _tu_forge_unit(tmp_path, honest, qkey,
                             result_typed_states=["OBSERVED_ZERO"],
                             denominators=[0], reported_success=True)
    assert verdict["ok"] is False
    assert verdict["failure_codes"] == ["ZERO_DENOMINATOR_NOT_TYPED"]


def test_h_m09b_measured_null_from_unvisited_is_false_null(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    qkey = _tu_key(next(r for r in honest if r["item"] == "Q"))
    verdict = _tu_forge_unit(tmp_path, honest, qkey,
                             result_typed_states=["MEASURED_NULL"],
                             null_sources=["UNVISITED"],
                             reported_success=False)
    assert verdict["ok"] is False
    assert verdict["failure_codes"] == ["FALSE_EMPIRICAL_NULL"]


def test_h_m10_fabricated_null_for_unexecuted_job_is_false_null(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    qkey = _tu_key(next(r for r in honest if r["item"] == "Q"))
    verdict = _tu_forge_unit(tmp_path, honest, qkey,
                             result_typed_states=["MEASURED_NULL"],
                             null_sources=["UNEXECUTED"],
                             reported_success=False)
    assert verdict["ok"] is False
    assert verdict["failure_codes"] == ["FALSE_EMPIRICAL_NULL"]


# ==========================================================================
# H-M11: held/denied visibility games
# ==========================================================================
def test_h_m11a_held_work_executed_via_synthetic_unit_fails(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    produced = _tu_produce(tmp_path, _tu_payload(honest))
    held_key = _tu_key(next(r for r in honest if r["item"] == "H1"))
    forged = deepcopy(produced)
    donor = dict(forged["units"][0])
    donor["job_ref"] = dict(donor["job_ref"],
                            object_id=donor["job_ref"]["object_id"] + "-held-probe",
                            content_hash="1" * 64)
    donor["claimed_expected_work_key"] = held_key
    forged["units"] = forged["units"] + [donor]
    (tmp_path / "produced.json").write_text(json.dumps(forged, sort_keys=True))
    verdict = _tu_verify(tmp_path)
    assert verdict["ok"] is False
    assert "HELD_OR_DENIED_WORK_EXECUTED" in verdict["failure_codes"]


def test_h_m11b_denied_row_dropped_from_export_is_visible(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    produced = _tu_produce(tmp_path, _tu_payload(honest))
    dn_key = _tu_key(next(r for r in honest if r["item"] == "DN"))
    forged = deepcopy(produced)
    forged["held_export"] = [row for row in forged["held_export"]
                             if row.get("expected_work_key") != dn_key]
    (tmp_path / "produced.json").write_text(json.dumps(forged, sort_keys=True))
    verdict = _tu_verify(tmp_path)
    assert verdict["ok"] is False
    assert verdict["failure_codes"] == ["HELD_OR_DENIED_WORK_NOT_VISIBLE"]
    assert verdict["omitted"] == []
    assert verdict["extra"] == []


# ==========================================================================
# H-M12: I05 frontier states (fresh classes and reporting postures)
# ==========================================================================
def test_h_m12a_unvisited_discovery_unreported_still_fails(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    qdkey = _tu_key(next(r for r in honest if r["item"] == "QD"))
    verdict = _tu_forge_unit(tmp_path, honest, qdkey,
                             result_typed_states=["UNVISITED"],
                             reported_success=False)
    assert verdict["ok"] is False
    assert verdict["failure_codes"] == ["PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS"]


def test_h_m12b_adaptive_partial_unreported_still_fails(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    qdkey = _tu_key(next(r for r in honest if r["item"] == "QD"))
    verdict = _tu_forge_unit(tmp_path, honest, qdkey,
                             result_typed_states=["ADAPTIVE_PARTIAL"],
                             reported_success=False)
    assert verdict["ok"] is False
    assert verdict["failure_codes"] == ["PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS"]


def test_h_m12c_honest_pruned_discovery_is_conserved(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    qdkey = _tu_key(next(r for r in honest if r["item"] == "QD"))
    verdict = _tu_forge_unit(tmp_path, honest, qdkey,
                             result_typed_states=["PRUNED_BY_AUTHORITY"],
                             reported_success=False)
    assert verdict["ok"] is True, verdict["failure_codes"]
    assert "PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS" not in verdict["failure_codes"]


# ==========================================================================
# H-M13: post-result expectation reconstruction (self-certification demo)
# ==========================================================================
def test_h_m13_truncated_expectation_rejected_but_self_consistent(tmp_path):
    """Produce honestly, then rebuild the expectation AFTER the run with two
    jobs deleted.  The join REJECTS the rewrite (extra jobs), while the
    custodian self-consistency check on the rewritten pair ACCEPTS it.
    Both halves are executed here: this is the empirical separation between
    independent verification and self-consistency."""
    scope = _tu_scope()
    honest = _tu_honest(scope)
    _tu_produce(tmp_path, _tu_payload(honest))
    truncated = [r for r in honest if r["item"] not in ("Q", "QW")]
    (tmp_path / "payload.json").write_text(
        json.dumps(_tu_payload(truncated), sort_keys=True))
    verdict = _tu_verify(tmp_path)
    assert verdict["ok"] is False
    assert "UNAUTHORIZED_EXTRA_JOB" in verdict["failure_codes"]
    assert set(verdict["extra"]) == {
        _tu_key(next(r for r in honest if r["item"] == "Q")),
        _tu_key(next(r for r in honest if r["item"] == "QW")),
    }
    assert verdict["omitted"] == []
    # ...yet the rewritten pair is self-consistent: digests match, and the
    # hold is STILL present (consistency never authenticates custody)
    frozen_trunc = V.freeze_payload(_tu_payload(truncated))
    cust = V.custodian_check(
        frozen_trunc,
        {"frozen_frontier_digest": frozen_trunc["frontier_digest"],
         "custodian_timestamp": "2026-10-12T00:00:00Z"})
    assert cust["consistent"] is True
    assert cust["finding"] == "STRUCTURALLY_CONSISTENT__EXTERNALLY_UNPROVEN"
    assert cust["hold"] == "EXTERNAL_CUSTODIAN_ISSUER_HOLD"
    full = V.freeze_payload(_tu_payload(honest))
    assert full["frontier_digest"] != frozen_trunc["frontier_digest"]


# ==========================================================================
# H-M14: consumer receipt laundering
# ==========================================================================
def test_h_m14a_modelled_receipt_relabelled_authenticated_still_holds(tmp_path):
    """Even explicitly 'authenticated' receipts cannot satisfy the actual
    consumer court inside this scope: laundering the label changes nothing."""
    scope = _tu_scope()
    honest = _tu_honest(scope)
    produced = _tu_produce(tmp_path, _tu_payload(honest))
    forged = deepcopy(produced)
    for c in forged["consumer_receipts"]:
        c["authenticated"] = True
        c["signature"] = "FORGED-SIGNATURE"
    (tmp_path / "produced.json").write_text(json.dumps(forged, sort_keys=True))
    verdict = _tu_verify(tmp_path)
    # structural join is unaffected (receipts match on key+consumer pairs)
    assert verdict["ok"] is True, verdict["failure_codes"]
    assert verdict["actual_consumer_court"]["verdict"] == "HOLD"
    # and the separate court holds even when handed 'authenticated' input
    qkey = _tu_key(next(r for r in honest if r["item"] == "Q"))
    court = V.actual_consumer_court(
        None, authenticated_receipts=[{"expected_work_key": qkey,
                                       "consumer": TU_C1,
                                       "authenticated": True}])
    assert court["verdict"] == "HOLD"


def test_h_m14b_renamed_consumer_is_omitted_obligation(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    produced = _tu_produce(tmp_path, _tu_payload(honest))
    qkey = _tu_key(next(r for r in honest if r["item"] == "Q"))
    forged = deepcopy(produced)
    for c in forged["consumer_receipts"]:
        if c["expected_work_key"] == qkey:
            c["consumer"] = "SOME_OTHER_CONSUMER"
    (tmp_path / "produced.json").write_text(json.dumps(forged, sort_keys=True))
    verdict = _tu_verify(tmp_path)
    assert verdict["ok"] is False
    assert verdict["failure_codes"] == ["REQUIRED_CONSUMER_OMITTED"]
    assert len(verdict["unsatisfied_consumers"]) == 1
    assert verdict["unsatisfied_consumers"][0]["expected_work_key"] == qkey


# ==========================================================================
# H-M15: custodian timestamp games (forward-dated, missing)
# ==========================================================================
def test_h_m15a_forward_dated_consistent_custodian_still_holds():
    scope = _tu_scope()
    frozen = V.freeze_payload(_tu_payload(_tu_honest(scope)))
    cust = V.custodian_check(
        frozen,
        {"frozen_frontier_digest": frozen["frontier_digest"],
         "custodian_timestamp": "2099-12-31T23:59:59Z"})
    assert cust["consistent"] is True
    assert cust["finding"] == "STRUCTURALLY_CONSISTENT__EXTERNALLY_UNPROVEN"
    assert cust["hold"] == "EXTERNAL_CUSTODIAN_ISSUER_HOLD"
    assert cust["timestamp_trusted"] is False
    assert cust["timestamp_recorded"] == "2099-12-31T23:59:59Z"


def test_h_m15b_custodian_without_timestamp_still_holds():
    scope = _tu_scope()
    frozen = V.freeze_payload(_tu_payload(_tu_honest(scope)))
    cust = V.custodian_check(
        frozen, {"frozen_frontier_digest": frozen["frontier_digest"]})
    assert cust["consistent"] is True
    assert cust["hold"] == "EXTERNAL_CUSTODIAN_ISSUER_HOLD"
    assert cust["timestamp_trusted"] is False
    assert cust.get("timestamp_recorded") is None


# ==========================================================================
# H-M16: identity-field swaps (form, topology, route) + produced source lie;
# respondent has no V2 raw field (proven inert, not asserted absent)
# ==========================================================================
def test_h_m16a_form_swap_changes_identity(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    submitted = [dict(r, form="F9") if r["item"] == "P" else r
                 for r in honest]
    verdict = _tu_join_against(tmp_path, submitted, honest)
    assert verdict["ok"] is False
    assert "EXPECTED_OPERATION_OMITTED" in verdict["failure_codes"]
    assert "UNAUTHORIZED_EXTRA_JOB" in verdict["failure_codes"]
    assert verdict["omitted"] == [
        _tu_key(next(r for r in honest if r["item"] == "P"))]


def test_h_m16b_topology_swap_changes_identity(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    submitted = [dict(r, topology_identity="SCALAR_2X2") if r["item"] == "P"
                 else r for r in honest]
    verdict = _tu_join_against(tmp_path, submitted, honest)
    assert verdict["ok"] is False
    assert "EXPECTED_OPERATION_OMITTED" in verdict["failure_codes"]
    assert "UNAUTHORIZED_EXTRA_JOB" in verdict["failure_codes"]
    assert verdict["omitted"] == [
        _tu_key(next(r for r in honest if r["item"] == "P"))]


def test_h_m16c_route_swap_reroutes_through_foreign_query(tmp_path):
    """Routing P through the (Y,X) query changes its identity: the honest P
    job is omitted and the rerouted job is an unauthorized extra."""
    scope = _tu_scope()
    honest = _tu_honest(scope)
    rerouted = dict(next(r for r in honest if r["item"] == "P"),
                    condition_order=["Y", "X"],
                    query_slot="yx",
                    query_ref=scope["queries"]["yx"].ref.as_dict())
    submitted = [rerouted if r["item"] == "P" else r for r in honest]
    verdict = _tu_join_against(tmp_path, submitted, honest)
    assert verdict["ok"] is False
    assert "EXPECTED_OPERATION_OMITTED" in verdict["failure_codes"]
    assert "UNAUTHORIZED_EXTRA_JOB" in verdict["failure_codes"]
    assert verdict["omitted"] == [
        _tu_key(next(r for r in honest if r["item"] == "P"))]


def test_h_m16d_forged_executed_source_sha_fails_every_job(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    produced = _tu_produce(tmp_path, _tu_payload(honest))
    forged = deepcopy(produced)
    forged["executed_source_sha"] = "f" * 64
    (tmp_path / "produced.json").write_text(json.dumps(forged, sort_keys=True))
    verdict = _tu_verify(tmp_path)
    assert verdict["ok"] is False
    assert "SOURCE_IDENTITY_MISMATCH" in verdict["failure_codes"]


def test_h_m16e_respondent_field_is_inert_and_collapses(tmp_path):
    """The V2 raw grammar has no respondent-identity field.  A smuggled
    respondent field is silently IGNORED (not hashed into identity), so two
    declarations differing only by respondent collapse onto one key and the
    freeze refuses the pair.  Respondent distinction is therefore
    TYPED_ABSENT from this verifier's identity — proven, not assumed."""
    scope = _tu_scope()
    base = next(r for r in _tu_honest(scope) if r["item"] == "P")
    with_resp = dict(base, respondent_identity="RESPONDENT-1")
    assert _tu_key(base) == _tu_key(with_resp)
    with pytest.raises(V.PayloadError, match="duplicate recomputed"):
        V.freeze_payload(_tu_payload([base, with_resp]))


# ==========================================================================
# H-M17: release forgery on a matched job + source lie on an extra unit
# ==========================================================================
def test_h_m17_forged_release_and_unmatched_source_lie(tmp_path):
    scope = _tu_scope()
    honest = _tu_honest(scope)
    produced = _tu_produce(tmp_path, _tu_payload(honest))
    qkey = _tu_key(next(r for r in honest if r["item"] == "Q"))
    forged = deepcopy(produced)
    unit = _tu_unit_by_claimed(forged, qkey)
    unit["release_refs"] = [{"kind": "C11LogicalRelease",
                             "object_id": "release-FORGED-A04TU",
                             "content_hash": "e" * 64}]
    forged["units"] = forged["units"] + [{
        "job_kind": "QUERY",
        "job_ref": {"kind": "TestQuery", "object_id": "urn:tu:extra",
                    "content_hash": "d" * 64},
        "claimed_expected_work_key": "e" * 64,
        "declared_source_identity": "0" * 64,
        "declared_condition_order": [],
        "predicate_ref": None,
        "release_refs": list(forged["units"][0]["release_refs"]),
        "attempt_index": 1,
        "state": "COMPLETED",
        "result_typed_states": ["SUPPORTED"],
        "denominators": [5],
        "null_sources": [None],
        "reported_success": True,
    }]
    (tmp_path / "produced.json").write_text(json.dumps(forged, sort_keys=True))
    verdict = _tu_verify(tmp_path)
    assert verdict["ok"] is False
    assert "FORGED_RELEASE" in verdict["failure_codes"]
    assert "UNAUTHORIZED_EXTRA_JOB" in verdict["failure_codes"]
    assert "SOURCE_IDENTITY_MISMATCH" in verdict["failure_codes"]
