from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

import install

install.install()

import firstclass
from candidate import ResponseStatus, TargetBranch, TargetReason, seal
from r31j.scenarios import evaluated

from bridge import access
from bridge.readback import cold_verify
from bridge.world import S35World

GRADE = "TEST_ONLY_SOURCEFREE_NOT_NATIVE"


def _summary(run) -> dict:
    receipt = run.receipt or {}
    return {
        "label": run.label,
        "refused": run.refused,
        "committed": run.committed,
        "refusal_reason": run.refusal_reason,
        "response_status": getattr(run.response, "status", None).value
        if run.response is not None
        else "",
        "outcome": run.outcome,
        "target_proposals": len(getattr(run.response, "target_proposals", ())),
        "target_branch": getattr(getattr(run, "decision", None), "branch", None).value
        if getattr(run, "decision", None) is not None
        else "",
        "target_reason": getattr(getattr(run, "decision", None), "reason", None).value
        if getattr(run, "decision", None) is not None
        else "",
        "target_id": getattr(getattr(run, "decision", None), "target_id", ""),
        "target_state_rows": run.target_state_rows,
        "response_row_hash": run.response_row_hash,
        "c9_receipt_hash": run.c9_receipt_hash,
        "s35_receipt_hash": receipt.get("hash", ""),
        "access_source_ref": receipt.get("access_source_ref", ""),
        "access_source_hash": receipt.get("access_source_hash", ""),
        "access_status": receipt.get("access_status", ""),
        "access_time": receipt.get("access_time"),
        "response_source_ref": receipt.get("response_source_ref", ""),
        "response_source_hash": receipt.get("response_source_hash", ""),
        "response_ref": receipt.get("response_ref", ""),
        "response_kind": receipt.get("response_kind", ""),
        "response_time": receipt.get("response_time"),
        "actor_id": receipt.get("actor_id", ""),
        "event_ref": receipt.get("event_ref", ""),
        "event_id": receipt.get("event_id", ""),
        "root_id": receipt.get("root_id", ""),
        "root_branch_hash": receipt.get("root_branch_hash", ""),
        "root_state_hash": receipt.get("root_state_hash", ""),
        "branch_id": receipt.get("branch_id", ""),
        "branch_hash": receipt.get("branch_hash", ""),
        "branch_parent_id": receipt.get("branch_parent_id", ""),
        "branch_fork_clock": receipt.get("branch_fork_clock"),
        "clock": receipt.get("clock"),
        "objective_material_eligible": receipt.get("objective_material_eligible"),
        "objective_material_refs": receipt.get("objective_material_refs", []),
        "objective_material_implies_uptake": receipt.get(
            "objective_material_implies_uptake"
        ),
        "claim_ceiling": receipt.get("claim_ceiling", ""),
        "c9_exists": run.store_path is not None and run.store_path.exists(),
    }


def _assert_positive(run) -> None:
    assert run.committed is True
    assert run.refused is False
    assert run.response.status is ResponseStatus.RESPONSE_COMMITTED
    assert run.response.reason == access.OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
    assert run.response.target_proposals == ()
    assert run.decision.branch is TargetBranch.NO_CHANGE
    assert run.decision.reason is TargetReason.NO_PROPOSAL
    assert run.decision.target_id == ""
    assert run.target_state_rows == 0
    assert run.receipt["target_proposals"] == []


def _assert_valid_empty(run, outcome: str) -> None:
    assert run.committed is True
    assert run.refused is False
    assert run.response.status is ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY
    assert run.response.reason == outcome
    assert run.response.target_proposals == ()
    assert run.decision.branch is TargetBranch.NO_CHANGE
    assert run.decision.reason is TargetReason.NO_PROPOSAL
    assert run.target_state_rows == 0


def _trial(name: str, positive_check, fault_run, restore_check) -> dict:
    try:
        positive_check()
        positive_status = "PASS"
        positive_error = ""
    except AssertionError as error:
        positive_status = "RED"
        positive_error = str(error) or name + ": positive assertion failed"
    try:
        fault_run()
        fault_status = "PASS"
        fault_error = ""
    except AssertionError as error:
        fault_status = "RED"
        fault_error = str(error) or name + ": fault run did not satisfy positive assertion"
    try:
        restore_check()
        restore_status = "PASS"
        restore_error = ""
    except AssertionError as error:
        restore_status = "RED"
        restore_error = str(error) or name + ": restored assertion failed"
    return {
        "claim": name,
        "positive": positive_status,
        "positive_error": positive_error,
        "fault": fault_status,
        "fault_error": fault_error,
        "restored": restore_status,
        "restored_error": restore_error,
    }


def _foreign_access(world, field: str, value) -> dict:
    witness = access.reseal_access_witness(world.make_access(), **{field: value})
    run = world.evaluate(f"foreign-access-{field}", access_witness=witness)
    return {
        "field": field,
        "value": value,
        "refused": run.refused,
        "committed": run.committed,
        "response_status": run.response.status.value,
        "reason": run.refusal_reason,
        "c9_exists": (run.run_dir / "c9.sqlite").exists(),
        "target_state_rows": run.target_state_rows,
        "cold_ok": cold_verify(world.root, f"foreign-access-{field}")["ok"],
    }


def _foreign_response(world, field: str, value) -> dict:
    witness = access.reseal_response_witness(world.make_response(), **{field: value})
    run = world.evaluate(f"foreign-response-{field}", response_witness=witness)
    return {
        "field": field,
        "value": value,
        "refused": run.refused,
        "committed": run.committed,
        "response_status": run.response.status.value,
        "reason": run.refusal_reason,
        "c9_exists": (run.run_dir / "c9.sqlite").exists(),
        "target_state_rows": run.target_state_rows,
        "cold_ok": cold_verify(world.root, f"foreign-response-{field}")["ok"],
    }


def _file_hashes() -> dict:
    rows = {}
    for path in sorted(RETURN.rglob("*")):
        if not path.is_file():
            continue
        if path.name.endswith(".pyc") or "__pycache__" in path.parts:
            continue
        if path.is_relative_to(RETURN / "evidence") and path.name == "s35_evidence.json":
            continue
        rows[str(path.relative_to(RETURN))] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
    return rows


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-s35-evidence-"))
    share_case = evaluated(share=True, e2=False)["case"]
    share = S35World.build(root / "share", case=share_case)
    vectors = []
    same_world = {}
    try:
        baseline = share.evaluate("p1")
        _assert_positive(baseline)
        vectors.append(_summary(baseline))

        access_fault = share.evaluate("access-fault", access_witness=None)
        _assert_valid_empty(access_fault, access.UNKNOWN_RECEIVABILITY)
        vectors.append(_summary(access_fault))
        access_restored = share.evaluate("access-restored")
        _assert_positive(access_restored)
        vectors.append(_summary(access_restored))

        request_fault = share.evaluate("request-fault", response_witness=None)
        _assert_valid_empty(request_fault, access.RECEIVABLE_NO_OBSERVED_UPTAKE)
        vectors.append(_summary(request_fault))
        request_restored = share.evaluate("request-restored")
        _assert_positive(request_restored)
        vectors.append(_summary(request_restored))

        contradictory = share.evaluate(
            "contradictory",
            response_witness=None,
            contradictory_context=True,
            contradictory_refs=("TEST_ONLY_S35_CONTRADICTION_A",),
        )
        _assert_valid_empty(contradictory, access.AMBIGUOUS_CONTRADICTORY)
        vectors.append(_summary(contradictory))
        unbound = share.evaluate(
            "contradictory-unbound",
            response_witness=None,
            contradictory_context=True,
        )
        assert unbound.refused is True
        vectors.append(_summary(unbound))

        history = share.evaluate(
            "history-refs",
            enacted_history_refs=(
                "TEST_ONLY_HISTORY_ACT_ONE",
                "TEST_ONLY_HISTORY_ACT_TWO",
            ),
        )
        _assert_positive(history)
        vectors.append(_summary(history))
        assert history.receipt["hash"] == baseline.receipt["hash"]

        share_explicit = share.evaluate(
            "share-explicit-refusal",
            response_witness=share.make_response(response_kind="EXPLICIT_REFUSAL"),
        )
        assert share_explicit.response.reason == access.OBSERVED_CURRENT_REFUSAL
        assert share_explicit.receipt["hash"] != baseline.receipt["hash"]
        vectors.append(_summary(share_explicit))

        for run in (
            baseline,
            access_fault,
            access_restored,
            request_fault,
            request_restored,
            contradictory,
            history,
            share_explicit,
        ):
            receipt = run.receipt
            same_world[run.label] = {
                "event_ref": receipt.get("event_ref"),
                "event_id": receipt.get("event_id"),
                "root_id": receipt.get("root_id"),
                "root_branch_hash": receipt.get("root_branch_hash"),
                "root_state_hash": receipt.get("root_state_hash"),
                "branch_id": receipt.get("branch_id"),
                "branch_hash": receipt.get("branch_hash"),
                "branch_fork_clock": receipt.get("branch_fork_clock"),
                "clock": receipt.get("clock"),
            }

        access_mutations = [
            ("root_id", "TEST_ONLY_FOREIGN_ROOT"),
            ("root_branch_hash", "f" * 64),
            ("root_state_hash", "e" * 64),
            ("branch_id", "TEST_ONLY_FOREIGN_BRANCH"),
            ("branch_hash", "d" * 64),
            ("branch_parent_id", "TEST_ONLY_FOREIGN_PARENT"),
            ("branch_fork_clock", -1),
            ("clock", 999999),
            ("actor_id", "TEST_ONLY_FOREIGN_ACTOR"),
            ("event_ref", "0" * 64),
            ("event_id", "TEST_ONLY_FOREIGN_EVENT"),
            ("source_ref", "NOT_TEST_ONLY_ACCESS"),
            ("revoked", True),
        ]
        response_mutations = [
            ("root_id", "TEST_ONLY_FOREIGN_ROOT"),
            ("root_branch_hash", "f" * 64),
            ("branch_id", "TEST_ONLY_FOREIGN_BRANCH"),
            ("branch_hash", "d" * 64),
            ("clock", 999999),
            ("actor_id", "TEST_ONLY_FOREIGN_ACTOR"),
            ("event_ref", "0" * 64),
            ("event_id", "TEST_ONLY_FOREIGN_EVENT"),
            ("response_kind", "UNKNOWN_KIND"),
            ("performed", False),
            ("revoked", True),
        ]
        access_refusals = [
            _foreign_access(share, field, value) for field, value in access_mutations
        ]
        response_refusals = [
            _foreign_response(share, field, value)
            for field, value in response_mutations
        ]
        cold = {
            label: cold_verify(share.root, label)
            for label in (
                "p1",
                "access-fault",
                "access-restored",
                "request-fault",
                "request-restored",
                "contradictory",
                "contradictory-unbound",
                "history-refs",
                "share-explicit-refusal",
            )
        }
    finally:
        share.close()

    refuse_case = evaluated(share=False, e2=False)["case"]
    refuse = S35World.build(root / "refuse", case=refuse_case)
    try:
        refuse_run = refuse.evaluate("refuse")
        assert refuse_run.response.reason == access.OBSERVED_CURRENT_REFUSAL
        assert refuse_run.receipt["objective_material_eligible"] is False
        vectors.append(_summary(refuse_run))
        refuse_cold = cold_verify(refuse.root, "refuse")
    finally:
        refuse.close()

    label_case = deepcopy(share_case)
    label_case["social_role"] = "TEST_ONLY_ALTERED_ROLE"
    label_case["demographic_label"] = "TEST_ONLY_ALTERED_LABEL"
    label_preimage_equal = firstclass.case_preimage(label_case) == (
        firstclass.case_preimage(share_case)
    )
    label_source_equal = firstclass.source_from_case(label_case) == (
        firstclass.source_from_case(share_case)
    )
    label_world = S35World.build(root / "label-world", case=label_case)
    try:
        label_run = label_world.evaluate("label-altered")
        label_positive = (
            label_run.response.reason == access.OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
            and label_run.response.target_proposals == ()
            and label_run.target_state_rows == 0
        )
        label_cold = cold_verify(label_world.root, "label-altered")
    finally:
        label_world.close()

    fault_trials = [
        _trial(
            "access witness gate",
            lambda: _assert_positive(baseline),
            lambda: _assert_positive(access_fault),
            lambda: _assert_positive(access_restored),
        ),
        _trial(
            "response witness gate",
            lambda: _assert_positive(baseline),
            lambda: _assert_positive(request_fault),
            lambda: _assert_positive(request_restored),
        ),
    ]

    mismatched_hash = {
        key: value
        for key, value in share.make_access().items()
        if key not in {"hash", "source_hash"}
    }
    mismatched_hash["source_hash"] = "0" * 64
    mismatched_hash = seal(mismatched_hash)
    hash_run = None
    share_for_hash = S35World.build(root / "hash-world", case=share_case)
    try:
        hash_run = share_for_hash.evaluate(
            "source-hash-mismatch", access_witness=mismatched_hash
        )
        hash_cold = cold_verify(share_for_hash.root, "source-hash-mismatch")
    finally:
        share_for_hash.close()

    evidence = {
        "schema": "SOROK_S35_C9R_ACCESS_EVIDENCE@1",
        "grade": GRADE,
        "native": False,
        "base": install.CUTS["m35"],
        "cuts": dict(install.CUTS),
        "source_manifest": install.source_manifest(),
        "file_hashes": _file_hashes(),
        "vectors": vectors,
        "same_world": same_world,
        "fault_trials": fault_trials,
        "foreign_refusals": {
            "access": access_refusals,
            "response": response_refusals,
        },
        "source_hash_mismatch": {
            "refused": hash_run.refused,
            "committed": hash_run.committed,
            "reason": hash_run.refusal_reason,
            "c9_exists": (hash_run.run_dir / "c9.sqlite").exists(),
            "cold_ok": hash_cold["ok"],
        }
        if hash_run is not None
        else {},
        "cold_readback": {
            "share": cold,
            "refuse": refuse_cold,
            "label_altered": label_cold,
        },
        "label_invariance": {
            "case_preimage_equal": label_preimage_equal,
            "source_equal": label_source_equal,
            "outcome": label_run.response.reason,
            "target_proposals": len(label_run.response.target_proposals),
            "target_state_rows": label_run.target_state_rows,
        },
        "not_run": [
            "native CAN008/CAN011 issuance",
            "ADP017/ADP019 owner receipt",
            "C8 native custody",
            "C11/C12 native consumer",
            "Pyat N11/N12",
            "human A5",
            "H1 acquired practice",
            "external provider/browser call",
        ],
    }
    evidence_dir = RETURN / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "s35_evidence.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf8",
    )
    summary = {
        "vectors": len(vectors),
        "foreign_access_refusals": len(access_refusals),
        "foreign_response_refusals": len(response_refusals),
        "cold_all_ok": all(
            item["ok"] for item in cold.values()
        )
        and refuse_cold["ok"]
        and label_cold["ok"],
        "fault_trials": fault_trials,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
