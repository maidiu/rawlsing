from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

import install

install.install()

import candidate
import candidate.pipeline as pipeline_module
import firstclass
from candidate import ResponseStatus, TargetBranch, TargetReason, lookup_rule, seal
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
        "perception_ref": receipt.get("perception_ref", ""),
        "perception_hash": receipt.get("perception_hash", ""),
        "perception_source_ref": receipt.get("perception_source_ref", ""),
        "perceived_at": receipt.get("perceived_at"),
        "access_status": receipt.get("access_status", ""),
        "action_ref": receipt.get("action_ref", ""),
        "action_receipt_hash": receipt.get("action_receipt_hash", ""),
        "action_source_ref": receipt.get("action_source_ref", ""),
        "action_kind": receipt.get("action_kind", ""),
        "action_time": receipt.get("action_time"),
        "action_performed": receipt.get("action_performed"),
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
        "evidence_grade": receipt.get("evidence_grade", ""),
        "actual_actor_input": receipt.get("actual_actor_input"),
        "qualification": receipt.get("qualification", ""),
        "hold_reason": receipt.get("hold_reason", ""),
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
    assert run.receipt["evidence_grade"] == access.S35_GRADE_CONTROLLED
    assert run.receipt["actual_actor_input"] is False


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


def _perception(world, *, status="ACCESSIBLE", ref, **kwargs):
    return world.perception_receipt(
        access_status=status, perception_ref=ref, **kwargs
    )


def _action(world, *, kind="REQUEST_TOOL", performed=True, ref, **kwargs):
    return world.action_receipt(
        action_kind=kind, performed=performed, action_ref=ref, **kwargs
    )


def _positive_args(world):
    return {
        "perception_receipt": _perception(
            world, ref="TEST_ONLY_A_PERCEPTION_EVIDENCE"
        ),
        "action_receipt": _action(
            world, ref="TEST_ONLY_A_ACTION_EVIDENCE"
        ),
    }


def _break_source_hash(receipt):
    body = {
        key: value
        for key, value in receipt.items()
        if key not in {"hash", "source_hash"}
    }
    body["source_hash"] = "0" * 64
    return seal(body)


def _foreign_perception(world, field, value, action) -> dict:
    receipt = access.reseal_perception_receipt(
        _perception(world, ref="TEST_ONLY_A_PERCEPTION_FOREIGN"),
        **{field: value},
    )
    run = world.evaluate(
        f"foreign-perception-{field}",
        perception_receipt=receipt,
        action_receipt=action,
    )
    return {
        "field": field,
        "value": value,
        "refused": run.refused,
        "committed": run.committed,
        "response_status": run.response.status.value,
        "reason": run.refusal_reason,
        "c9_exists": (run.run_dir / "c9.sqlite").exists(),
        "target_state_rows": run.target_state_rows,
        "cold_ok": cold_verify(world.root, f"foreign-perception-{field}")["ok"],
    }


def _foreign_action(world, field, value, perception) -> dict:
    receipt = access.reseal_action_receipt(
        _action(world, ref="TEST_ONLY_A_ACTION_FOREIGN"),
        **{field: value},
    )
    run = world.evaluate(
        f"foreign-action-{field}",
        perception_receipt=perception,
        action_receipt=receipt,
    )
    return {
        "field": field,
        "value": value,
        "refused": run.refused,
        "committed": run.committed,
        "response_status": run.response.status.value,
        "reason": run.refusal_reason,
        "c9_exists": (run.run_dir / "c9.sqlite").exists(),
        "target_state_rows": run.target_state_rows,
        "cold_ok": cold_verify(world.root, f"foreign-action-{field}")["ok"],
    }


def _consumer_probe(world, perception, action) -> dict:
    lookup = lookup_rule(
        world.response_registry,
        authority_id=world.rule.authority_id,
        rule_version=world.rule.rule_version,
        rule_content_hash=world.rule.rule_content_hash,
        subject=world.context.actor_id,
    )
    evaluation = access.evaluate_actor_access_response(
        rule_lookup=lookup,
        event_ref=world.context.event_ref,
        event_time=world.context.event_time,
        subject=world.context.actor_id,
        request=access.S35ActorAccessRequest(
            perception_receipt=perception,
            action_receipt=action,
        ),
        conditioning_readset=world.conditioning.readset_refs,
        context=world.context,
        as_of=world.context.as_of,
        material_eligible=world.material_eligible,
        eligible_material_refs=world.eligible_material_refs,
    )
    expected = {
        "event_time": world.context.event_time,
        "conditioning_readset": world.conditioning.readset_refs,
        "material_eligible": world.material_eligible,
        "eligible_material_refs": world.eligible_material_refs,
        "actor_history_refs": (),
        "other_person_offer_ref": "",
        "material_opportunity_ref": "",
        "prior_response_count": 0,
        "rule_lookup": lookup,
    }
    current = {
        "context": world.context,
        "evaluation": evaluation,
        "expected": expected,
    }
    kwargs = {
        "rule_lookup": lookup,
        "event_ref": world.context.event_ref,
        "event_time": world.context.event_time,
        "subject": world.context.actor_id,
        "conditioning_readset": world.conditioning.readset_refs,
        "actor_history_refs": (),
        "other_person_offer_ref": "",
        "material_opportunity_ref": "",
        "prior_response_count": 0,
        "material_eligible": world.material_eligible,
        "eligible_material_refs": world.eligible_material_refs,
    }
    token = access.set_current_context(current)
    try:
        accepted = access.pipeline_selector(**kwargs) is evaluation.response
    finally:
        access.reset_current_context(token)
    mutations = (
        ("rule_lookup", replace(lookup, rule_content_hash="0" * 64)),
        ("event_time", world.context.event_time + 1),
        (
            "conditioning_readset",
            world.conditioning.readset_refs + ("TEST_ONLY_EXTRA",),
        ),
        ("material_eligible", not world.material_eligible),
        (
            "eligible_material_refs",
            ("TEST_ONLY_OTHER_MATERIAL",),
        ),
        ("actor_history_refs", ("TEST_ONLY_HISTORY_EXTRA",)),
        ("other_person_offer_ref", "TEST_ONLY_OTHER_OFFER"),
        ("material_opportunity_ref", "TEST_ONLY_OTHER_OPPORTUNITY"),
        ("prior_response_count", 1),
    )
    rejected = []
    for field, value in mutations:
        changed = dict(kwargs)
        changed[field] = value
        token = access.set_current_context(current)
        try:
            access.pipeline_selector(**changed)
            error = ""
        except RuntimeError as exc:
            error = str(exc)
        finally:
            access.reset_current_context(token)
        rejected.append(
            {
                "field": field,
                "error": error,
                "rejected": error == "S35_CONSUMER_INPUT_MISMATCH:" + field,
            }
        )
    legacy = candidate.evaluate_response(**kwargs)
    delegated = pipeline_module.evaluate_response(**kwargs)
    return {
        "matching_accepted": accepted,
        "mutations": rejected,
        "legacy_delegation": {
            "status": delegated.status.value,
            "reason": delegated.reason,
            "target_proposals": len(delegated.target_proposals),
            "receipt_hash": delegated.receipt_hash,
            "same_status": delegated.status == legacy.status,
            "same_reason": delegated.reason == legacy.reason,
            "same_target_proposals": delegated.target_proposals
            == legacy.target_proposals,
            "same_receipt_hash": delegated.receipt_hash == legacy.receipt_hash,
            "same_candidate_route": delegated.candidate_route
            == legacy.candidate_route,
        },
    }


def _file_hashes() -> dict:
    rows = {}
    for path in sorted(RETURN.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(RETURN)
        parts = relative.parts
        if path.name.endswith(".pyc") or "__pycache__" in parts:
            continue
        if relative.as_posix() == "evidence/s35_evidence.json":
            continue
        included = (
            relative.as_posix() in {
                "install.py",
                ".gitignore",
                "evidence/test_run.txt",
                "evidence/s35_full.xml",
            }
            or (parts and parts[0] in {"bridge", "tests", "tools"})
        )
        if not included:
            continue
        rows[relative.as_posix()] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
    return rows


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-s35-evidence-"))
    share_case = evaluated(share=True, e2=False)["case"]
    share = S35World.build(root / "share", case=share_case)
    vectors = []
    same_world = {}
    public_privacy = {}
    try:
        perception_ok = _perception(
            share, ref="TEST_ONLY_A_PERCEPTION_P1"
        )
        action_ok = _action(share, ref="TEST_ONLY_A_ACTION_P1")
        baseline = share.evaluate(
            "p1",
            perception_receipt=perception_ok,
            action_receipt=action_ok,
        )
        _assert_positive(baseline)
        vectors.append(_summary(baseline))

        hold = share.evaluate("actual-a-hold")
        _assert_valid_empty(hold, access.A_LOCAL_PERCEPTION_HOLD)
        vectors.append(_summary(hold))

        access_fault = share.evaluate(
            "access-fault",
            perception_receipt=_perception(
                share,
                status="NOT_WITNESSED",
                ref="TEST_ONLY_A_PERCEPTION_NOT_WITNESSED",
            ),
            action_receipt=action_ok,
        )
        _assert_valid_empty(access_fault, access.UNKNOWN_RECEIVABILITY)
        vectors.append(_summary(access_fault))
        access_restored = share.evaluate(
            "access-restored",
            perception_receipt=perception_ok,
            action_receipt=action_ok,
        )
        _assert_positive(access_restored)
        vectors.append(_summary(access_restored))

        action_fault = share.evaluate(
            "action-missing",
            perception_receipt=perception_ok,
        )
        _assert_valid_empty(action_fault, access.A_OWNED_ACTION_HOLD)
        vectors.append(_summary(action_fault))
        not_performed = share.evaluate(
            "action-not-performed",
            perception_receipt=perception_ok,
            action_receipt=_action(
                share,
                kind="NO_OBSERVED_ACTION",
                performed=False,
                ref="TEST_ONLY_A_ACTION_NONE",
            ),
        )
        _assert_valid_empty(not_performed, access.RECEIVABLE_NO_OBSERVED_UPTAKE)
        vectors.append(_summary(not_performed))
        action_restored = share.evaluate(
            "action-restored",
            perception_receipt=perception_ok,
            action_receipt=action_ok,
        )
        _assert_positive(action_restored)
        vectors.append(_summary(action_restored))

        contradictory = share.evaluate(
            "contradictory",
            perception_receipt=perception_ok,
            contradictory_context=True,
            contradictory_refs=("TEST_ONLY_S35_CONTRADICTION_A",),
        )
        _assert_valid_empty(contradictory, access.AMBIGUOUS_CONTRADICTORY)
        vectors.append(_summary(contradictory))
        unbound = share.evaluate(
            "contradictory-unbound",
            perception_receipt=perception_ok,
            contradictory_context=True,
        )
        assert unbound.refused is True
        vectors.append(_summary(unbound))

        history = share.evaluate(
            "history-refs",
            perception_receipt=perception_ok,
            action_receipt=action_ok,
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
            perception_receipt=perception_ok,
            action_receipt=_action(
                share,
                kind="EXPLICIT_REFUSAL",
                ref="TEST_ONLY_A_ACTION_SHARE_REFUSAL",
            ),
        )
        assert share_explicit.response.reason == access.OBSERVED_CURRENT_REFUSAL
        vectors.append(_summary(share_explicit))

        for run in (
            baseline,
            hold,
            access_fault,
            access_restored,
            action_fault,
            not_performed,
            action_restored,
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
            public_privacy[run.label] = {
                "receipt": not access.public_privacy_error(receipt),
                "run": not access.public_privacy_error(
                    json.loads((run.run_dir / "run.json").read_text(encoding="utf8"))
                ),
            }

        episodes = share.c12.episodes("s35")
        public_privacy["c12_episodes"] = {
            "ok": not any(
                access.public_privacy_error(episode.get("body") or {})
                for episode in episodes
            )
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
            ("perceived_at", -1),
            ("access_status", "INVALID_STATUS"),
            ("source_ref", "NOT_TEST_ONLY_PERCEPTION"),
            ("owner_ref", "TEST_ONLY_FOREIGN_OWNER"),
            ("revoked", True),
            ("evidence_grade", "UNKNOWN_GRADE"),
            ("actual_actor_input", True),
            ("native", True),
        ]
        action_mutations = [
            ("root_id", "TEST_ONLY_FOREIGN_ROOT"),
            ("branch_id", "TEST_ONLY_FOREIGN_BRANCH"),
            ("branch_hash", "d" * 64),
            ("clock", 999999),
            ("actor_id", "TEST_ONLY_FOREIGN_ACTOR"),
            ("event_ref", "0" * 64),
            ("event_id", "TEST_ONLY_FOREIGN_EVENT"),
            ("action_kind", "UNKNOWN_KIND"),
            ("performed", False),
            ("action_ref", ""),
            ("owner_ref", "TEST_ONLY_FOREIGN_OWNER"),
            ("action_time", -1),
            ("revoked", True),
            ("evidence_grade", "UNKNOWN_GRADE"),
            ("actual_actor_input", True),
            ("native", True),
        ]
        foreign_access = [
            _foreign_perception(share, field, value, action_ok)
            for field, value in access_mutations
        ]
        foreign_action = [
            _foreign_action(share, field, value, perception_ok)
            for field, value in action_mutations
        ]
        source_hash_mismatch = {}
        for kind in ("perception", "action"):
            if kind == "perception":
                receipt = _break_source_hash(
                    _perception(share, ref="TEST_ONLY_A_PERCEPTION_BROKEN_HASH")
                )
                run = share.evaluate(
                    "perception-source-hash",
                    perception_receipt=receipt,
                    action_receipt=action_ok,
                )
            else:
                receipt = _break_source_hash(
                    _action(share, ref="TEST_ONLY_A_ACTION_BROKEN_HASH")
                )
                run = share.evaluate(
                    "action-source-hash",
                    perception_receipt=perception_ok,
                    action_receipt=receipt,
                )
            source_hash_mismatch[kind] = {
                "refused": run.refused,
                "committed": run.committed,
                "reason": run.refusal_reason,
                "c9_exists": (run.run_dir / "c9.sqlite").exists(),
                "cold_ok": cold_verify(share.root, run.label)["ok"],
            }

        qualified_perception = share.perception_receipt(
            access_status="ACCESSIBLE",
            perception_ref="TEST_ONLY_A_PERCEPTION_QUALIFIED",
            evidence_grade=access.S35_GRADE_QUALIFIED,
            actual_actor_input=True,
            qualification=access.S35_QUALIFICATION_QUALIFIED,
        )
        qualified_action = share.action_receipt(
            action_kind="REQUEST_TOOL",
            performed=True,
            action_ref="TEST_ONLY_A_ACTION_QUALIFIED",
            evidence_grade=access.S35_GRADE_QUALIFIED,
            actual_actor_input=True,
            qualification=access.S35_QUALIFICATION_QUALIFIED,
        )
        qualified_hold = share.evaluate(
            "qualified-hold",
            perception_receipt=qualified_perception,
            action_receipt=qualified_action,
        )
        _assert_valid_empty(qualified_hold, access.A_LOCAL_PERCEPTION_HOLD)
        qualified_refused = share.evaluate(
            "qualified-refused",
            perception_receipt=qualified_perception,
            action_receipt=qualified_action,
            qualified_owner_resolver=lambda **kwargs: False,
        )
        assert qualified_refused.refused is True

        consumer = _consumer_probe(share, perception_ok, action_ok)
        cold_labels = (
            "p1",
            "actual-a-hold",
            "access-fault",
            "access-restored",
            "action-missing",
            "action-not-performed",
            "action-restored",
            "contradictory",
            "contradictory-unbound",
            "history-refs",
            "share-explicit-refusal",
            "qualified-hold",
            "qualified-refused",
            "perception-source-hash",
            "action-source-hash",
        )
        cold = {
            label: cold_verify(share.root, label) for label in cold_labels
        }
    finally:
        share.close()

    refuse_case = evaluated(share=False, e2=False)["case"]
    refuse = S35World.build(root / "refuse", case=refuse_case)
    try:
        refuse_run = refuse.evaluate(
            "refuse",
            perception_receipt=_perception(
                refuse, ref="TEST_ONLY_A_PERCEPTION_REFUSE"
            ),
            action_receipt=_action(
                refuse,
                kind="EXPLICIT_REFUSAL",
                ref="TEST_ONLY_A_ACTION_REFUSE",
            ),
        )
        assert refuse_run.response.reason == access.OBSERVED_CURRENT_REFUSAL
        assert refuse_run.receipt["objective_material_eligible"] is False
        vectors.append(_summary(refuse_run))
        refuse_cold = cold_verify(refuse.root, "refuse")
        refuse_privacy = {
            "receipt": not access.public_privacy_error(refuse_run.receipt),
            "run": not access.public_privacy_error(
                json.loads(
                    (refuse_run.run_dir / "run.json").read_text(encoding="utf8")
                )
            ),
        }
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
        label_run = label_world.evaluate(
            "label-altered",
            perception_receipt=_perception(
                label_world, ref="TEST_ONLY_A_PERCEPTION_LABEL"
            ),
            action_receipt=_action(
                label_world, ref="TEST_ONLY_A_ACTION_LABEL"
            ),
        )
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
            "a-local perception gate",
            lambda: _assert_positive(baseline),
            lambda: _assert_positive(access_fault),
            lambda: _assert_positive(access_restored),
        ),
        _trial(
            "a-owned action gate",
            lambda: _assert_positive(baseline),
            lambda: _assert_positive(action_fault),
            lambda: _assert_positive(action_restored),
        ),
    ]

    evidence = {
        "schema": "SOROK_S35_C9R_ACCESS_EVIDENCE@2",
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
            "perception": foreign_access,
            "action": foreign_action,
        },
        "source_hash_mismatch": source_hash_mismatch,
        "qualified_input": {
            "hold_outcome": qualified_hold.response.reason,
            "hold_reason": qualified_hold.receipt.get("hold_reason"),
            "refused_reason": qualified_refused.refusal_reason,
        },
        "consumer_binding": consumer,
        "public_value_privacy": {
            "share": public_privacy,
            "refuse": refuse_privacy,
        },
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
            "actual qualified A-local perception owner receipt",
            "actual qualified A-owned action occurrence/receipt",
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
        "foreign_perception_refusals": len(foreign_access),
        "foreign_action_refusals": len(foreign_action),
        "cold_all_ok": all(item["ok"] for item in cold.values())
        and refuse_cold["ok"]
        and label_cold["ok"],
        "consumer_all_negative": all(
            item["rejected"] for item in consumer["mutations"]
        ),
        "legacy_delegation": consumer["legacy_delegation"],
        "fault_trials": fault_trials,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
