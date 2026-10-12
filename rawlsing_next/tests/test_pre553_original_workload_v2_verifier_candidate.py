"""PYAT HQ280 PV3 A04T - independent V2 no-drop verifier join tests.

Development-only, source-free.  The verifier under test
(``pre553_original_workload_v2_verifier_candidate``) is stdlib-only: it
imports nothing from ``rawlsing_next`` and operates purely on plain data.

The harness side MAY import the v2 candidate and the real owners — that is
the producer.  The verifier side NEVER does: the subprocess join installs a
candidate-import blocker and proves it held.  No raw SAV/DTA is read; no
accepted owner, A04, A04S or A05 file is modified.
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

SOURCE = "SYNTHETIC-SOURCEFREE-A04T"
WAVE = "W1"
C_C1 = "C1_ANALYTICAL_COMPOSITION"
C_FF = "FIELD_FORGE_CONDITIONAL_SUPPORT"
C_LEARNED = "LEARNED_EMPIRICAL_ADJUDICATION"


# --------------------------------------------------------------------------
# Fixture: real scope once per session; RAW payload authored as plain dicts
# --------------------------------------------------------------------------
def _scope():
    import rawlsing_next.tests.test_pre553_original_workload_contract_v2_candidate as T
    return T._v2_scope()


def _raw(scope, item, form, slot, sem, roles, target, cond=(),
         measure="RAW", risk="RISK-R-ALL", topo="SCALAR_SINGULAR",
         consumer=C_C1, state="RUNNABLE", hold=None, mult=1,
         query_slot=None, predicate_slot=None):
    raw = {
        "source": SOURCE, "wave": WAVE, "item": item,
        "form": form, "slot": slot,
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


def _frozen_raws(scope):
    return [
        _raw(scope, "A", "F1", "S1", "UNARY_DISTRIBUTION", ("BASE",), "X",
             query_slot="x"),
        _raw(scope, "B", "F1", "S1", "UNARY_DISTRIBUTION", ("BASE",), "Y",
             query_slot="y"),
        _raw(scope, "B", "F1", "S1", "UNARY_DISTRIBUTION", ("BASE",), "Y",
             measure="GOVERNED_WEIGHTED", query_slot="y_weighted"),
        _raw(scope, "B", "F1", "S1", "UNARY_DISTRIBUTION",
             ("CONDITIONER", "TARGET"), "Y", cond=("X",), risk="RISK-R-COND",
             query_slot="y_given_x1", predicate_slot="query"),
        _raw(scope, "B", "F1", "S2", "PAIR_RESPONSE_COTRAVEL",
             ("CONDITIONER", "TARGET"), "J2", cond=("X", "Y"),
             risk="RISK-R-COMMON", topo="SCALAR_2X2_JOINT",
             consumer=C_FF, query_slot="xy"),
        _raw(scope, "B", "F1", "S2", "BOUNDED_DISCOVERY", ("BASE",), "D1",
             topo="SCALAR_2X2", consumer=C_LEARNED),
        _raw(scope, "O", "F1", "S1", "UNARY_DISTRIBUTION", ("BASE",), "O",
             topo="ORDERED_SEQUENCE", state="HELD",
             hold="ORDERED_SEQUENCE_COLLAPSE_NOT_YET_AUTHORIZED"),
        _raw(scope, "R", "F1", "S1", "UNARY_DISTRIBUTION", ("BASE",), "R",
             topo="REPEATED_EVENT", state="HELD",
             hold="REPEATED_EVENT_JOIN_NOT_YET_AUTHORIZED"),
        _raw(scope, "V", "F2", "S1", "UNARY_DISTRIBUTION", ("BASE",), "V",
             state="DENIED", hold="EXPLICIT_FAIL_CLOSED_SOURCE_GAP"),
        _raw(scope, "U", "F2", "S1", "UNARY_DISTRIBUTION", ("BASE",), "U",
             state="SOURCE_NONAPPLICABLE",
             hold="NO_COADMINISTERED_TARGET_IN_THIS_SLICE"),
    ]


def _payload(raws, custodian=None):
    doc = {"schema": V.ACCEPTED_EXPECTED_SCHEMA, "declarations": raws}
    if custodian is not None:
        doc["custodian"] = custodian
    return doc


# --------------------------------------------------------------------------
# Harness: real chain in one process, verification in a BLOCKED subprocess
# --------------------------------------------------------------------------
def _produce(tmp_path, raw_payload):
    (tmp_path / "payload.json").write_text(json.dumps(raw_payload, sort_keys=True))
    r = subprocess.run(
        [sys.executable, str(WORKER), str(tmp_path), "produce"],
        capture_output=True, text=True, timeout=300, cwd=str(REPO_ROOT))
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def _verify(tmp_path):
    r = subprocess.run(
        [sys.executable, str(WORKER), str(tmp_path), "verify"],
        capture_output=True, text=True, timeout=300, cwd=str(REPO_ROOT))
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["candidate_import_blocked"] is True
    return json.loads((tmp_path / "verdict.json").read_text())


def _join(tmp_path, raw_payload):
    _produce(tmp_path, raw_payload)
    return _verify(tmp_path)


def _produce_must_refuse(tmp_path, raw_payload, pattern):
    """For submissions the producer itself must fail closed on."""
    (tmp_path / "payload.json").write_text(json.dumps(raw_payload, sort_keys=True))
    r = subprocess.run(
        [sys.executable, str(WORKER), str(tmp_path), "produce"],
        capture_output=True, text=True, timeout=300, cwd=str(REPO_ROOT))
    assert r.returncode != 0, r.stdout
    assert pattern in (r.stdout + r.stderr), (r.stdout + r.stderr)[-2000:]
    return r


def _key_of(verdict_records, item, target=None, measure=None):
    for rec in verdict_records:
        raw = rec["raw"] if "raw" in rec else rec
        if raw.get("item") == item and (target is None or raw.get("target") == target) \
                and (measure is None or raw.get("measure_kind") == measure):
            return rec["recomputed"]["expected_work_key"]
    raise KeyError((item, target, measure))


# ==========================================================================
# POSITIVE: real chain + independent subprocess verification
# ==========================================================================
def test_positive_join_through_blocked_verifier_subprocess(tmp_path):
    scope = _scope()
    verdict = _join(tmp_path, _payload(_frozen_raws(scope)))
    assert verdict["candidate_import_blocked"] is True
    assert verdict["verifier_contract"] == V.VERIFIER_CONTRACT_ID
    assert verdict["ok"] is True, verdict["failure_codes"]
    assert verdict["omitted"] == []
    assert verdict["extra"] == []
    assert len(verdict["expected_keys"]) == 6
    assert len(verdict["visible_non_runnable"]) == 4
    assert set(verdict["result_classes"].values()) <= V.MEASURED_RESULT_CLASSES
    assert verdict["unsatisfied_consumers"] == []
    # standing holds are ALWAYS present, even on a structural pass
    assert "EXTERNAL_CUSTODIAN_ISSUER_HOLD" in verdict["holds"]
    assert "REAL_CONSUMER_MODELLED_NOT_EXECUTED" in verdict["holds"]
    # custodian structurally consistent (payload carries none -> absent, held)
    assert verdict["custodian"]["hold"] == "EXTERNAL_CUSTODIAN_ISSUER_HOLD"
    # actual-consumer court holds despite the structural consumer join passing
    assert verdict["actual_consumer_court"]["verdict"] == "HOLD"


def test_verifier_recomputation_agrees_with_candidate_on_honest_input():
    """Cross-check, not trust: two independent implementations, same digest."""
    import rawlsing_next.pre553_original_workload_contract_v2_candidate as v2c
    scope = _scope()
    for raw in _frozen_raws(scope):
        if raw["state"] != "RUNNABLE":
            continue
        mine = V.reconstruct_record(dict(raw), V.ACCEPTED_EXPECTED_SCHEMA)
        kwargs = dict(
            source=raw["source"], wave=raw["wave"], item=raw["item"],
            form=raw["form"], slot=raw["slot"],
            semantic_op_class=raw["semantic_op_class"],
            semantic_roles=tuple(raw["semantic_roles"]), target=raw["target"],
            condition_order=tuple(raw["condition_order"]),
            measure_kind=raw["measure_kind"],
            source_identity=raw["source_identity"],
            authority_ref=raw["authority_ref"],
            risk_identity=raw["risk_identity"],
            topology_identity=raw["topology_identity"],
            required_consumer=raw["required_consumer"])
        if raw["semantic_op_class"] == "BOUNDED_DISCOVERY":
            kwargs["discovery_authority_ref"] = scope["discovery_ref"]
        else:
            kwargs["query_ref"] = scope["queries"][raw["query_slot"]].ref
            if raw.get("predicate_slot") == "query":
                kwargs["predicate_ref"] = scope["queries"][
                    raw["query_slot"]].dependency_refs[0]
            else:
                kwargs["predicate_ref"] = scope["all_p"].ref
        theirs = v2c.V2ExpectedWorkDeclaration(**kwargs)
        assert mine["recomputed"]["expected_work_key"] == theirs.expected_work_key
        assert mine["recomputed"]["consumer_obligation_key"] == \
            theirs.consumer_obligation_key


def test_verifier_imports_nothing_from_the_repository():
    import subprocess as _sp
    r = _sp.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, %r);"
         "import rawlsing_next.pre553_original_workload_v2_verifier_candidate as V;"
         "mods=[m for m in sys.modules if m.startswith('rawlsing_next.')];"
         "print(mods)" % str(REPO_ROOT)],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert r.returncode == 0, r.stderr
    # Only the verifier module itself (plus its namespace package) may
    # appear; no sibling repository module may be pulled in.
    mods = eval(r.stdout.strip())
    assert "rawlsing_next.pre553_original_workload_v2_verifier_candidate" in mods
    siblings = [m for m in mods if m.startswith("rawlsing_next.")
                and m != "rawlsing_next.pre553_original_workload_v2_verifier_candidate"]
    assert siblings == [], siblings


# ==========================================================================
# VERIFIER UNIT HOSTILES (no owner run needed)
# ==========================================================================
def test_supplied_key_forgery_is_detected_not_trusted():
    scope = _scope()
    raws = _frozen_raws(scope)
    frozen = V.freeze_payload(_payload(raws))
    forged = deepcopy(raws)
    forged[0] = dict(forged[0], expected_work_key="0" * 64)
    frozen_forged = V.freeze_payload(_payload(forged))
    rec = next(r for r in frozen_forged["records"]
               if r["raw"]["item"] == "A")
    assert rec["key_mismatches"]["expected_work_key"]["supplied"] == "0" * 64
    assert rec["key_mismatches"]["expected_work_key"]["recomputed"] == \
        next(r for r in frozen["records"]
             if r["raw"]["item"] == "A")["recomputed"]["expected_work_key"]


def test_forged_supplied_key_fails_the_join(tmp_path):
    scope = _scope()
    raws = _frozen_raws(scope)
    _produce(tmp_path, _payload(raws))
    produced = json.loads((tmp_path / "produced.json").read_text())
    forged = deepcopy(raws)
    forged[0] = dict(forged[0], expected_work_key="0" * 64)
    verdict = V.verify(V.freeze_payload(_payload(forged)), produced)
    assert not verdict.ok
    assert "KEY_PREIMAGE_MISMATCH" in verdict.failure_codes()


def test_duplicate_declarations_fail_closed_at_freeze():
    scope = _scope()
    raws = _frozen_raws(scope)
    with pytest.raises(V.PayloadError, match="duplicate recomputed"):
        V.freeze_payload(_payload(raws + [deepcopy(raws[0])]))


def test_wrong_schema_is_refused_not_coerced():
    scope = _scope()
    with pytest.raises(V.PayloadError, match="not the accepted v2 schema"):
        V.freeze_payload(_payload(_frozen_raws(scope)) | {"schema": "A05_SCHEMA"})
    with pytest.raises(V.PayloadError, match="nonempty list"):
        V.freeze_payload({"schema": V.ACCEPTED_EXPECTED_SCHEMA, "declarations": []})


def test_held_without_reason_and_runnable_with_refs_refused():
    scope = _scope()
    bad = deepcopy(_frozen_raws(scope)[6])
    bad = {k: v for k, v in bad.items() if k != "hold_reason"}
    with pytest.raises(V.PayloadError, match="must carry a hold reason"):
        V.freeze_payload(_payload([bad]))
    bad2 = dict(_frozen_raws(scope)[0], hold_reason="X")
    with pytest.raises(V.PayloadError, match="cannot carry a hold reason"):
        V.freeze_payload(_payload([bad2]))


# ==========================================================================
# REAL-RUN HOSTILES (modified raw payload -> real chain -> full payload check)
# ==========================================================================
def _hostile_run(tmp_path, scope, mutate):
    full = _frozen_raws(scope)
    submitted = mutate([dict(r) for r in full])
    _produce(tmp_path, _payload(submitted))
    produced = json.loads((tmp_path / "produced.json").read_text())
    return V.verify(V.freeze_payload(_payload(full)), produced)


def test_a_only_while_a_and_b_expected(tmp_path):
    scope = _scope()
    v = _hostile_run(tmp_path, scope,
                     lambda rs: [r for r in rs
                                 if r["item"] != "B" or r.get("semantic_op_class") == "BOUNDED_DISCOVERY"])
    assert not v.ok
    assert "EXPECTED_OPERATION_OMITTED" in v.failure_codes()
    assert len(v.omitted) == 4


def test_missing_j2(tmp_path):
    scope = _scope()
    v = _hostile_run(tmp_path, scope,
                     lambda rs: [r for r in rs if r["target"] != "J2"])
    assert not v.ok
    assert "EXPECTED_OPERATION_OMITTED" in v.failure_codes()
    assert len(v.omitted) == 1


def test_same_count_different_keys(tmp_path):
    scope = _scope()

    def mutate(rs):
        out = []
        for r in rs:
            if r["item"] == "A" and r["state"] == "RUNNABLE":
                r = dict(r, item="A-PRIME")
            out.append(r)
        return out

    v = _hostile_run(tmp_path, scope, mutate)
    assert not v.ok
    assert "EXPECTED_OPERATION_OMITTED" in v.failure_codes()
    assert "UNAUTHORIZED_EXTRA_JOB" in v.failure_codes()
    # Same manifest-level count (6 produced jobs), different identities:
    # exactly one omission and exactly one extra.
    assert len(v.omitted) == 1
    assert len(v.extra) == 1


def test_raw_weighted_collision(tmp_path):
    """Collapsing WEIGHTED onto RAW is refused at bind time, fail-closed.

    Two declarations with identical semantic identity cannot both bind: the
    producer raises duplicate expected_work_key instead of silently merging
    two distinct measure operations into one job.
    """
    scope = _scope()

    def mutate(rs):
        out = []
        for r in rs:
            if r.get("measure_kind") == "GOVERNED_WEIGHTED":
                r = dict(r, measure_kind="RAW")
            out.append(r)
        return out

    full = _frozen_raws(scope)
    submitted = mutate([dict(r) for r in full])
    _produce_must_refuse(tmp_path, _payload(submitted), "duplicate expected_work_key")
    # ...and the verifier independently refuses the same collapse at freeze
    with pytest.raises(V.PayloadError, match="duplicate recomputed"):
        V.freeze_payload(_payload(submitted))


def test_condition_order_substitution(tmp_path):
    scope = _scope()

    def mutate(rs):
        out = []
        for r in rs:
            if r["target"] == "J2":
                r = dict(r, condition_order=["Y", "X"],
                         query_slot="yx")
            out.append(r)
        return out

    v = _hostile_run(tmp_path, scope, mutate)
    assert not v.ok
    assert "EXPECTED_OPERATION_OMITTED" in v.failure_codes()
    assert "UNAUTHORIZED_EXTRA_JOB" in v.failure_codes()


def test_form_swap_changes_item_identity(tmp_path):
    scope = _scope()
    v = _hostile_run(
        tmp_path, scope,
        lambda rs: [dict(r, form="F2") if (r["item"] == "A" and r["state"] == "RUNNABLE") else r
                    for r in rs])
    assert not v.ok
    assert "EXPECTED_OPERATION_OMITTED" in v.failure_codes()


def test_risk_person_swap_changes_identity(tmp_path):
    scope = _scope()
    v = _hostile_run(
        tmp_path, scope,
        lambda rs: [dict(r, risk_identity="RISK-R-OTHER")
                    if (r["item"] == "A" and r["state"] == "RUNNABLE") else r
                    for r in rs])
    assert not v.ok
    assert "EXPECTED_OPERATION_OMITTED" in v.failure_codes()


def test_source_swap_fails(tmp_path):
    scope = _scope()
    v = _hostile_run(
        tmp_path, scope,
        lambda rs: [dict(r, source_identity="0" * 64)
                    if (r["item"] == "A" and r["state"] == "RUNNABLE") else r
                    for r in rs])
    assert not v.ok
    assert "SOURCE_IDENTITY_MISMATCH" in v.failure_codes()


def test_weight_measure_swap_fails(tmp_path):
    """A WEIGHTED op pointed at the RAW query collapses onto Y-RAW's job.

    The producer fail-closes at bind time ("collapsed onto one semantic
    batch job") instead of silently executing a weighted operation through
    a raw query.
    """
    scope = _scope()

    def mutate(rs):
        out = []
        for r in rs:
            if r.get("measure_kind") == "GOVERNED_WEIGHTED":
                r = dict(r, query_slot="y")
            out.append(r)
        return out

    full = _frozen_raws(scope)
    submitted = mutate([dict(r) for r in full])
    _produce_must_refuse(tmp_path, _payload(submitted), "collapsed onto one semantic")


def test_own_dk_cotopic_fake_joint_rejected(tmp_path):
    scope = _scope()
    full = _frozen_raws(scope)
    xy = next(r for r in full if r["target"] == "J2")
    fake = dict(xy, target="J2_DK", condition_order=["X", "X"],
                query_slot="x_dk",
                query_ref=scope["queries"]["x_dk"].ref.as_dict())
    submitted = [fake if r is xy else r for r in full]
    _produce(tmp_path, _payload(submitted))
    produced = json.loads((tmp_path / "produced.json").read_text())
    v = V.verify(V.freeze_payload(_payload(full)), produced)
    assert not v.ok
    assert "CANDIDATE_OWN_DK_JOINT" in v.failure_codes()


# ==========================================================================
# PRODUCED-DATA HOSTILES (forged manifest, outcomes, consumers)
# ==========================================================================
def _produced_for(scope, tmp_path, submitted=None):
    full = _frozen_raws(scope)
    _produce(tmp_path, _payload(full if submitted is None else submitted))
    return full, json.loads((tmp_path / "produced.json").read_text())


def test_forged_release_refused(tmp_path):
    scope = _scope()
    full, produced = _produced_for(scope, tmp_path)
    forged = deepcopy(produced)
    forged["executed_release_ref"] = {
        "kind": "C11LogicalRelease", "object_id": "release-FORGED",
        "content_hash": "f" * 64}
    v = V.verify(V.freeze_payload(_payload(full)), forged)
    assert not v.ok
    assert "FORGED_RELEASE" in v.failure_codes()


def test_predicate_substitution_fails(tmp_path):
    scope = _scope()
    full, produced = _produced_for(scope, tmp_path)
    forged = deepcopy(produced)
    forged["units"][0]["predicate_ref"] = dict(forged["units"][0]["predicate_ref"],
                                              content_hash="0" * 64)
    v = V.verify(V.freeze_payload(_payload(full)), forged)
    assert not v.ok
    # The claim names a known expectation but points at foreign owner inputs:
    # the claimed-path cross-check fires first and most precisely.
    assert "CLAIMED_JOB_REF_MISMATCH" in v.failure_codes()


def test_predicate_substitution_without_claim_fails(tmp_path):
    """Owner-ref path: a claimless unit with a foreign predicate is refused."""
    scope = _scope()
    full, produced = _produced_for(scope, tmp_path)
    forged = deepcopy(produced)
    del forged["units"][0]["claimed_expected_work_key"]
    forged["units"][0]["predicate_ref"] = dict(forged["units"][0]["predicate_ref"],
                                              content_hash="0" * 64)
    v = V.verify(V.freeze_payload(_payload(full)), forged)
    assert not v.ok
    assert "PREDICATE_SUBSTITUTION" in v.failure_codes()


def test_false_empirical_null_fails(tmp_path):
    scope = _scope()
    full, produced = _produced_for(scope, tmp_path)
    forged = deepcopy(produced)
    forged["units"][0]["result_typed_states"] = ["MEASURED_NULL"]
    forged["units"][0]["null_sources"] = ["AUTHORITY_UNAVAILABLE"]
    forged["units"][0]["reported_success"] = True
    v = V.verify(V.freeze_payload(_payload(full)), forged)
    assert not v.ok
    assert "FALSE_EMPIRICAL_NULL" in v.failure_codes()


def test_unvisited_discovery_fails(tmp_path):
    scope = _scope()
    full, produced = _produced_for(scope, tmp_path)
    forged = deepcopy(produced)
    disc = next(u for u in forged["units"] if u["job_kind"] == "DISCOVERY")
    disc["result_typed_states"] = ["UNVISITED"]
    disc["reported_success"] = True
    v = V.verify(V.freeze_payload(_payload(full)), forged)
    assert not v.ok
    assert "PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS" in v.failure_codes()


def test_coverage_limited_mispromoted_fails(tmp_path):
    scope = _scope()
    full, produced = _produced_for(scope, tmp_path)
    forged = deepcopy(produced)
    disc = next(u for u in forged["units"] if u["job_kind"] == "DISCOVERY")
    disc["result_typed_states"] = ["COVERAGE_LIMITED"]
    disc["reported_success"] = True
    v = V.verify(V.freeze_payload(_payload(full)), forged)
    assert not v.ok
    assert "PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS" in v.failure_codes()


def test_coverage_limited_honestly_reported_is_conserved(tmp_path):
    scope = _scope()
    full, produced = _produced_for(scope, tmp_path)
    honest = deepcopy(produced)
    disc = next(u for u in honest["units"] if u["job_kind"] == "DISCOVERY")
    disc["result_typed_states"] = ["COVERAGE_LIMITED"]
    disc["reported_success"] = False
    v = V.verify(V.freeze_payload(_payload(full)), honest)
    assert v.ok
    assert "PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS" not in v.failure_codes()


def test_duplicate_constructed_jobs_fail(tmp_path):
    scope = _scope()
    full, produced = _produced_for(scope, tmp_path)
    forged = deepcopy(produced)
    forged["units"] = forged["units"] + [deepcopy(forged["units"][0])]
    v = V.verify(V.freeze_payload(_payload(full)), forged)
    assert not v.ok
    assert "DUPLICATE_CONSTRUCTED_JOB" in v.failure_codes()


def test_missing_typed_result_fails(tmp_path):
    scope = _scope()
    full, produced = _produced_for(scope, tmp_path)
    forged = deepcopy(produced)
    forged["units"][0]["result_typed_states"] = []
    v = V.verify(V.freeze_payload(_payload(full)), forged)
    assert not v.ok
    assert "MISSING_TYPED_RESULT" in v.failure_codes()


def test_zero_denominator_untyped_fails(tmp_path):
    scope = _scope()
    full, produced = _produced_for(scope, tmp_path)
    forged = deepcopy(produced)
    forged["units"][0]["denominators"] = [0]
    forged["units"][0]["result_typed_states"] = ["SUPPORTED"]
    v = V.verify(V.freeze_payload(_payload(full)), forged)
    assert not v.ok
    assert "ZERO_DENOMINATOR_NOT_TYPED" in v.failure_codes()


def test_consumer_omission_fails_with_all_jobs_present(tmp_path):
    scope = _scope()
    full, produced = _produced_for(scope, tmp_path)
    forged = deepcopy(produced)
    forged["consumer_receipts"] = forged["consumer_receipts"][:-1]
    v = V.verify(V.freeze_payload(_payload(full)), forged)
    assert not v.ok
    assert "REQUIRED_CONSUMER_OMITTED" in v.failure_codes()
    assert len(v.unsatisfied_consumers) == 1


def test_held_invisible_fails(tmp_path):
    scope = _scope()
    full, produced = _produced_for(scope, tmp_path)
    forged = deepcopy(produced)
    forged["held_export"] = []
    v = V.verify(V.freeze_payload(_payload(full)), forged)
    assert not v.ok
    assert "HELD_OR_DENIED_WORK_NOT_VISIBLE" in v.failure_codes()


def test_unknown_owner_state_never_promoted():
    assert V.classify_result("SOMETHING_NEW") == "OWNER_TYPED_SOMETHING_NEW"
    assert V.classify_result("SOMETHING_NEW") not in V.MEASURED_RESULT_CLASSES
    assert V.classify_result(None) == "MISSING_TYPED_RESULT"


# ==========================================================================
# CUSTODIAN / PROVENANCE HOSTILES
# ==========================================================================
def test_absent_custodian_holds(tmp_path):
    scope = _scope()
    verdict = _join(tmp_path, _payload(_frozen_raws(scope)))
    assert verdict["custodian"]["finding"] in (
        "CUSTODIAN_ABSENT", "STRUCTURALLY_CONSISTENT__EXTERNALLY_UNPROVEN")
    assert verdict["custodian"]["hold"] == "EXTERNAL_CUSTODIAN_ISSUER_HOLD"
    assert verdict["custodian"]["timestamp_trusted"] is False
    assert verdict["custodian"]["signature_trusted"] is False


def test_forged_custodian_digest_mismatch_fails():
    scope = _scope()
    frozen = V.freeze_payload(_payload(_frozen_raws(scope)))
    cust = {"frozen_frontier_digest": "0" * 64,
            "custodian_timestamp": "2026-10-11T00:00:00Z"}
    out = V.custodian_check(frozen, cust)
    assert out["consistent"] is False
    assert out["finding"] == "CUSTODIAN_MISMATCH"
    assert out["hold"] == "EXTERNAL_CUSTODIAN_ISSUER_HOLD"


def test_consistent_forged_custodian_still_holds_on_external_auth():
    """Self-consistent forgery: digests match, external custody unproven."""
    scope = _scope()
    frozen = V.freeze_payload(_payload(_frozen_raws(scope)))
    cust = {"frozen_frontier_digest": frozen["frontier_digest"],
            "custodian_timestamp": "1999-01-01T00:00:00Z"}  # backdated
    out = V.custodian_check(frozen, cust)
    assert out["consistent"] is True
    assert out["finding"] == "STRUCTURALLY_CONSISTENT__EXTERNALLY_UNPROVEN"
    assert out["hold"] == "EXTERNAL_CUSTODIAN_ISSUER_HOLD"
    assert out["timestamp_trusted"] is False
    assert out["timestamp_recorded"] == "1999-01-01T00:00:00Z"


def test_rewritten_frontier_plus_matching_custodian_still_holds():
    """A fully consistent rewrite is self-consistent — and still unproven."""
    scope = _scope()
    truncated = [r for r in _frozen_raws(scope)
                 if not (r["item"] == "B" and r["state"] == "RUNNABLE"
                         and r["semantic_op_class"] != "BOUNDED_DISCOVERY")]
    frozen_trunc = V.freeze_payload(_payload(truncated))
    cust = {"frozen_frontier_digest": frozen_trunc["frontier_digest"],
            "custodian_timestamp": "2026-10-11T00:00:00Z"}
    out = V.custodian_check(frozen_trunc, cust)
    assert out["consistent"] is True
    assert out["hold"] == "EXTERNAL_CUSTODIAN_ISSUER_HOLD"
    # ...while the FULL payload exposes the rewrite as an omission elsewhere
    full = V.freeze_payload(_payload(_frozen_raws(scope)))
    assert full["frontier_digest"] != frozen_trunc["frontier_digest"]


# ==========================================================================
# MIGRATION AUDIT: injective where true, NONREPRESENTABLE where not
# ==========================================================================
def test_migration_audit_declares_nonrepresentable_honestly():
    scope = _scope()
    frozen = V.freeze_payload(_payload(_frozen_raws(scope)))
    audit = V.audit_a05_migration(frozen["records"])
    by_item = {}
    for rec in audit["per_record"]:
        by_item.setdefault(rec["item"], []).append(rec)
    # RAW unary with empty conditions: triple-mappable, key never equal
    a_rec = next(r for r in audit["per_record"] if r["item"] == "A")
    assert a_rec["triple_mappable_to_a05"] is True
    assert a_rec["full_key_verdict"] == "NONREPRESENTABLE"
    # GOVERNED_WEIGHTED: no A05 distinction -> NONREPRESENTABLE
    w_rec = next(r for r in audit["per_record"]
                 if r.get("triple", {}).get("target") == "Y"
                 and any("measure" in reason for reason in r["triple_reasons"])
                 or False)
    assert w_rec["triple_mappable_to_a05"] is False
    # joint with condition_order: NONREPRESENTABLE triple
    j_rec = next(r for r in audit["per_record"] if r["triple"]["target"] == "J2")
    assert j_rec["triple_mappable_to_a05"] is False
    # discovery: no A05 counterpart at all
    d_rec = next(r for r in audit["per_record"]
                 if r["triple"]["op_class"] == "BOUNDED_DISCOVERY")
    assert d_rec["triple_mappable_to_a05"] is False
    # set-level: Y-RAW and Y-WEIGHTED share one A05 triple -> non-injective
    assert audit["set_level_triple_mapping_injective"] is False
    assert audit["set_verdict"] == "NONREPRESENTABLE__SHARED_A05_TRIPLE_WOULD_COLLIDE"
    assert "cannot satisfy that check" in audit["note"]


def test_no_v2_key_is_ever_claimed_a05_equal():
    scope = _scope()
    frozen = V.freeze_payload(_payload(_frozen_raws(scope)))
    audit = V.audit_a05_migration(frozen["records"])
    assert all(r["full_key_verdict"] == "NONREPRESENTABLE"
               for r in audit["per_record"])
    assert all(r["full_key_equal_to_a05"] is False
               for r in audit["per_record"])


# ==========================================================================
# CONSUMER COURT: modelled join passes structurally, execution unclaimed
# ==========================================================================
def test_actual_consumer_court_holds_despite_structural_join(tmp_path):
    scope = _scope()
    verdict = _join(tmp_path, _payload(_frozen_raws(scope)))
    assert verdict["ok"] is True
    assert verdict["unsatisfied_consumers"] == []
    assert verdict["actual_consumer_court"]["verdict"] == "HOLD"
    assert verdict["actual_consumer_court"]["code"] == \
        "REAL_CONSUMER_MODELLED_NOT_EXECUTED"
    # even "authenticated" input cannot satisfy it in this scope
    court = V.actual_consumer_court(None, authenticated_receipts=[{"x": 1}])
    assert court["verdict"] == "HOLD"


# ==========================================================================
# INHERITED SUITES (rerun, not rewritten)
# ==========================================================================
def test_a04s_26_suite_still_passes_here():
    import subprocess as _sp
    r = _sp.run(
        [sys.executable, "-m", "pytest",
         "rawlsing_next/tests/test_pre553_original_workload_contract_v2_candidate.py",
         "-q"],
        capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=600)
    assert r.returncode == 0, r.stdout[-2000:]
    assert "26 passed" in r.stdout


def test_a04_41_suite_still_passes_in_its_worktree():
    import subprocess as _sp
    other = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a04")
    if not (other / "rawlsing_next" / "tests" /
            "test_pre553_original_workload_binder_candidate.py").exists():
        pytest.skip("A04 worktree not present on this machine")
    r = _sp.run(
        [sys.executable, "-m", "pytest",
         "rawlsing_next/tests/test_pre553_original_workload_binder_candidate.py",
         "-q"],
        capture_output=True, text=True, cwd=str(other), timeout=600)
    assert r.returncode == 0, r.stdout[-2000:]
    assert "41 passed" in r.stdout


def test_a05_18_suite_still_passes_in_its_worktree():
    import subprocess as _sp
    hostiles = (Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a05")
                / "WORKER_RETURNS"
                / "PYAT-HQ280-PV3-A05-INDEPENDENT-NODROP-ORACLE-R1"
                / "repro" / "a05_hostiles.py")
    if not hostiles.exists():
        pytest.skip("A05 worktree not present on this machine")
    r = _sp.run([sys.executable, str(hostiles)],
                capture_output=True, text=True, cwd=str(hostiles.parent),
                timeout=300)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    assert json.loads(r.stdout).get("all_expectations_met") is True


def test_owner_spot_suites_still_pass_here():
    import subprocess as _sp
    r = _sp.run(
        [sys.executable, "-m", "pytest",
         "rawlsing_next/tests/test_pre553_route_b_production.py",
         "rawlsing_next/tests/test_pre553_batch_runner.py",
         "rawlsing_next/tests/test_pre553_discovery_exact.py",
         "rawlsing_next/tests/test_pre553_empirical_query.py",
         "rawlsing_next/tests/test_pre553_carrier_execution.py",
         "-q"],
        capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=900)
    assert r.returncode == 0, r.stdout[-2000:]


def test_no_raw_sav_dta_reads():
    for rel in ("rawlsing_next/pre553_original_workload_v2_verifier_candidate.py",
                "WORKER_RETURNS/PYAT-HQ280-PV3-A04T-V2-VERIFIED-INDEPENDENT-JOIN-R1/repro/a04t_join_worker.py"):
        source = (REPO_ROOT / rel).read_text()
        for forbidden in (".sav", ".dta", "pyreadstat"):
            assert forbidden not in source


def test_accepted_owners_a04_a04s_a05_untouched():
    """Owner-specific integrity (A04TU correction of a self-defeating check).

    The previous form of this test asserted zero ``git diff`` output anywhere
    under ``rawlsing_next/`` relative to sealed base ``b68de0dd``.  That scope
    necessarily contains A04T's own two explicitly permitted NEW files, so the
    assertion could never pass on the committed branch (independent A04TR
    review: 43 passed / 1 failed, owners exonerated by the diff output
    itself).  This corrected form checks three separate properties instead:

    (A) every ``rawlsing_next/`` path changed since the sealed base is inside
        an explicit permitted-change allow-list (the V2 candidate, its test,
        and the A04TU hostile test); any other changed or added path fails;
    (B) every protected accepted-owner file is byte-identical to its pinned
        Git blob (A04 owner, A04S owner, C11, Route B, Batch);
    (C) no TRACKED file under ``rawlsing_next/`` carries uncommitted
        worktree modifications (untracked files cannot conceal an edit to a
        tracked owner, so ``??`` entries are reported but do not fail);
    (D) the external A05 oracle blob is checked independently on its own
        branch (it does not exist on this branch, so it is never asserted
        as a local path).
    """
    import subprocess as _sp
    sealed = "b68de0dd35a9885efcb46bcd8ec9cbe41dabf500"
    # (B) protected accepted owners pinned at the sealed base.  Blobs verified
    # against A04T's own return and HQ intake; A04 binder 7d8b3902, A04S
    # contract 08bb75c4, route_b 2385cd32 match those records.
    protected_blobs = {
        "rawlsing_next/pre553_original_workload_binder_candidate.py":
            "7d8b3902c3f8f257637b7c07ad9feb5e096d48e5",
        "rawlsing_next/tests/test_pre553_original_workload_binder_candidate.py":
            "6c06a5b013d3713af7d7ba9bf143c3ef7a6245a2",
        "rawlsing_next/pre553_original_workload_contract_v2_candidate.py":
            "08bb75c431d3352cb0d17e9a65f7d855b4d35e59",
        "rawlsing_next/tests/test_pre553_original_workload_contract_v2_candidate.py":
            "0b9f1addf2b28f2a8e489fe44f1567a137a166f2",
        "rawlsing_next/pre553_c11_repository.py":
            "67c6eb6494522cd11aab1b93d0e73f9cef6036f3",
        "rawlsing_next/pre553_c11_integrity.py":
            "7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd",
        "rawlsing_next/pre553_route_b_production.py":
            "2385cd327dced3c5b887b59085aa0d21b04d78c3",
        "rawlsing_next/pre553_batch_runner.py":
            "2d291600b9a10c56d9c6f6de7f7d619f6c52e829",
    }
    # (A) exact diff allow-list: the only rawlsing_next/ paths that may
    # differ from the sealed base.  No accepted owner is whitelisted here.
    permitted_changed = frozenset({
        "rawlsing_next/pre553_original_workload_v2_verifier_candidate.py",
        "rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py",
        "rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py",
    })
    r = _sp.run(
        ["git", "diff", "--name-only", sealed, "HEAD", "--", "rawlsing_next/"],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert r.returncode == 0, r.stderr
    changed = [p for p in r.stdout.split() if p]
    unexpected = [p for p in changed if p not in permitted_changed]
    assert unexpected == [], (
        "paths changed outside the permitted V2-candidate allow-list: "
        + ", ".join(unexpected))
    for path, blob in sorted(protected_blobs.items()):
        q = _sp.run(["git", "rev-parse", f"HEAD:{path}"],
                    capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert q.returncode == 0, f"protected owner missing at HEAD: {path}"
        assert q.stdout.strip() == blob, (
            f"protected accepted owner mutated: {path} "
            f"(HEAD {q.stdout.strip()[:12]} != pinned {blob[:12]})")
    # (C) tracked worktree dirt must not conceal an owner edit.  Untracked
    # (??) entries are listed for the record but cannot modify a tracked
    # owner, so they do not fail this check.
    s = _sp.run(["git", "status", "--porcelain", "--", "rawlsing_next/"],
                capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert s.returncode == 0, s.stderr
    dirty_tracked = [ln for ln in s.stdout.splitlines()
                     if not ln.startswith("??")]
    assert dirty_tracked == [], (
        "uncommitted modifications to tracked rawlsing_next/ files: "
        + "; ".join(dirty_tracked))
    # (D) external A05 oracle: independent blob check on its own branch.
    # The oracle does not exist on this branch, so it is never asserted here
    # as a local path.  Absence of the A05 worktree is a HOLD, not a pass.
    a05_root = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a05")
    a05_rel = ("WORKER_RETURNS/PYAT-HQ280-PV3-A05-INDEPENDENT-NODROP-ORACLE-R1"
               "/repro/a05_oracle.py")
    if not (a05_root / ".git").exists():
        pytest.skip("A05 worktree not present on this machine: "
                    "external A05 oracle blob UNCHECKED (HOLD)")
    h = _sp.run(["git", "-C", str(a05_root), "rev-parse", "HEAD"],
                capture_output=True, text=True)
    assert h.returncode == 0, h.stderr
    assert h.stdout.strip() == "9491d0296c95ee2942fe80eadc6aa9f54b07c634", (
        "A05 worktree is not at the accepted oracle commit; "
        f"found {h.stdout.strip()[:12]}")
    b = _sp.run(["git", "-C", str(a05_root), "rev-parse", f"HEAD:{a05_rel}"],
                capture_output=True, text=True)
    assert b.returncode == 0, b.stderr
    assert b.stdout.strip() == "00a4cc84d321c3fbace0f4aa09be62dbb31994fc", (
        "external A05 oracle blob drifted from its accepted identity")
