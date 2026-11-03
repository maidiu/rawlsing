"""Smallest sourcefree reader for the already-admitted JOIN-E occurrence.

The reader never admits the event again and never opens a writable store. It
keeps the E1 actor/event clock and the C12 world/branch clock as distinct source
domains, validates event/root/branch/source/clock, validates A perception and A
action separately, and only then calls the normal S35 response selector.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping

from candidate import (
    TargetRuleRegistry,
    bind_conditioning,
    digest,
    eligible_material,
    evaluate_target,
    lookup_rule,
    make_conditioning_source,
    seal,
    valid,
)
from candidate.response_rules import ResponseRuleRegistry

from . import access
from .access import (
    S35ActorAccessRequest,
    S35Context,
    S35_GRADE_CONTROLLED,
    S35_QUALIFICATION_CONTROLLED,
)
from .join_e_compat import (
    make_rule,
    read_c9_summary,
    source_material_access,
)
from .readback import read_c12

OCCURRENCE_SCHEMA = "S35_SAME_ROOT_ADMITTED_OCCURRENCE@1"
CLOCK_BINDING_SCHEMA = "S35_SAME_ROOT_CLOCK_BINDING@1"
MISSING_CONTRACT_SCHEMA = "S35_MISSING_SOURCE_OWNER_CONTRACT@1"
GRADE = "TEST_ONLY_SOURCEFREE_NOT_NATIVE"
EVENT_DOMAIN = "JOIN_E_E1_ACTOR_EVENT_CLOCK"
BRANCH_DOMAIN = "JOIN_E_C12_WORLD_CLOCK"
EVENT_CLOCK_SOURCE = "JOIN_E_C9_OCCURRENCE_TIME"
BRANCH_CLOCK_SOURCE = "JOIN_E_C12_BRANCH_LAST_CLOCK"


@dataclass(frozen=True)
class OccurrenceRead:
    ok: bool
    checks: Mapping[str, bool]
    occurrence: Mapping[str, Any] | None
    missing_contract: Mapping[str, Any] | None


def _clock_binding(
    event_clock: int,
    branch_clock: int,
    *,
    event_source: str = EVENT_CLOCK_SOURCE,
    branch_source: str = BRANCH_CLOCK_SOURCE,
    substitution: bool = False,
    equality_claimed: bool = False,
) -> dict:
    return seal(
        {
            "schema": CLOCK_BINDING_SCHEMA,
            "grade": GRADE,
            "native": False,
            "event_clock": int(event_clock),
            "event_clock_source": event_source,
            "event_clock_domain": EVENT_DOMAIN,
            "branch_clock": int(branch_clock),
            "branch_clock_source": branch_source,
            "branch_clock_domain": BRANCH_DOMAIN,
            "distinct_sources": event_clock != branch_clock,
            "substitution": bool(substitution),
            "equality_claimed": bool(equality_claimed),
            "clock_substitution_allowed": False,
        }
    )


def make_clock_binding(
    event_clock: int,
    branch_clock: int,
    *,
    event_source: str = EVENT_CLOCK_SOURCE,
    branch_source: str = BRANCH_CLOCK_SOURCE,
    substitution: bool = False,
    equality_claimed: bool = False,
) -> dict:
    return _clock_binding(
        event_clock,
        branch_clock,
        event_source=event_source,
        branch_source=branch_source,
        substitution=substitution,
        equality_claimed=equality_claimed,
    )


def missing_source_owner_contract(
    *,
    event_hash: str = "",
    event_id: str = "",
    event_clock: int = 0,
    branch_clock: int = 0,
    root_id: str = "",
    branch_id: str = "",
    missing_fields: tuple[str, ...] = (),
) -> dict:
    return {
        "schema": MISSING_CONTRACT_SCHEMA,
        "status": "MISSING_SOURCE_OWNER_CONTRACT",
        "grade": GRADE,
        "native": False,
        "missing_fields": list(missing_fields),
        "actual_a_producer": "NONE_VERIFIED",
        "controlled_test_only_available": True,
        "required": [
            {
                "field": "qualified_a_perception_receipt",
                "owner": "A local perception source owner",
                "schema": "S35_A_LOCAL_PERCEPTION_RECEIPT@1",
                "event_hash": event_hash,
                "event_id": event_id,
                "event_clock": event_clock,
                "clock_domain": EVENT_DOMAIN,
                "root_id": root_id,
                "branch_id": branch_id,
                "native": False,
            },
            {
                "field": "qualified_a_action_receipt",
                "owner": "A action occurrence owner",
                "schema": "S35_A_OWNED_ACTION_OCCURRENCE@1",
                "event_hash": event_hash,
                "event_id": event_id,
                "event_clock": event_clock,
                "clock_domain": EVENT_DOMAIN,
                "root_id": root_id,
                "branch_id": branch_id,
                "performed_flag_required": True,
                "native": False,
            },
            {
                "field": "clock_domain_binding",
                "owner": "JOIN-E/C12 clock owner",
                "schema": CLOCK_BINDING_SCHEMA,
                "event_clock": event_clock,
                "branch_clock": branch_clock,
                "requires_distinct_sources": True,
                "requires_no_substitution": True,
                "native": False,
            },
        ],
    }


JOIN_SCHEMA = "SOROK_SAME_PERSON_JOIN@1"
REFUSAL_SCHEMA = "SOROK_SAME_PERSON_REFUSAL@1"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf8"))


def _persisted_provenance(state_root: Path) -> dict:
    state_root = Path(state_root).resolve()
    session_path = state_root / "session.json"
    if not session_path.is_file():
        return {"ok": False, "error": "SESSION_META_MISSING"}
    session = _read_json(session_path)
    schema = session.get("schema")
    if schema == JOIN_SCHEMA:
        c9_path = state_root / "bp2" / "c9.sqlite"
        provenance_path = state_root / "product" / "bp2_join.json"
    elif schema == REFUSAL_SCHEMA:
        c9_path = state_root / "source" / "bp2" / "c9.sqlite"
        provenance_path = state_root / "product" / "refusal.json"
    else:
        return {"ok": False, "error": "UNKNOWN_SESSION_SCHEMA"}
    if not provenance_path.is_file():
        return {"ok": False, "error": "PROVENANCE_MISSING"}
    provenance = _read_json(provenance_path)
    if schema == JOIN_SCHEMA:
        journal_path = Path(provenance["artifacts"]["journal_path"])
        occurrence_id = provenance["persisted"]["c8_occurrence_id"]
        provenance_source = provenance.get("r31j_source")
        c8_digest = provenance.get("persisted", {}).get(
            "c8_state_digest", provenance.get("r31j_c8_state_digest")
        )
        actor_snapshot = provenance.get("r31j_actor_snapshot")
    else:
        c8 = provenance.get("c8") or {}
        journal_path = Path(c8.get("journal_path", ""))
        occurrence_id = c8.get("occurrence_id")
        provenance_source = provenance.get("j_source")
        c8_digest = c8.get("c8_state_digest")
        actor_snapshot = provenance.get("actor_snapshot")
    if not journal_path.is_file():
        return {"ok": False, "error": "C8_JOURNAL_MISSING"}
    journal = _read_json(journal_path)
    entries = (journal.get("state") or {}).get("ledger") or []
    entry = next(
        (row for row in entries if row.get("occurrence_id") == occurrence_id),
        None,
    )
    if entry is None:
        return {"ok": False, "error": "C8_OCCURRENCE_MISSING"}
    payload = (
        ((entry.get("identity_preimage") or {}).get("payload"))
        or entry.get("payload")
        or {}
    )
    return {
        "ok": True,
        "state_root": state_root,
        "session": session,
        "session_schema": schema,
        "c9_path": c9_path.resolve(),
        "c12_path": (state_root / "product" / "c12.sqlite").resolve(),
        "branch_id": session.get("branch_id"),
        "root_branch_id": session.get("root_branch_id", "root"),
        "source_actor_map": session.get("source_actor_map") or {},
        "source": session.get("j_source"),
        "provenance_source": provenance_source,
        "journal_source": payload.get("gm01_pre_c9_source"),
        "journal_clock": entry.get("causal_time"),
        "journal_state_digest": journal.get("state_digest"),
        "journal_content_hash": entry.get("content_hash"),
        "journal_occurrence_id": occurrence_id,
        "journal_actor": payload.get("actor") or {},
        "journal_actor_id": (payload.get("actor") or {}).get("actor_id"),
        "journal_other_actor_id": (payload.get("other_actor") or {}).get(
            "actor_id"
        ),
        "c8_digest": c8_digest,
        "e1_hash": session.get("j_e1_event_hash"),
        "actor_snapshot": actor_snapshot,
        "provenance_path": provenance_path,
        "journal_path": journal_path,
    }


def read_occurrence(
    bundle: Mapping[str, Any],
    *,
    clock_binding_override: Mapping[str, Any] | None = None,
) -> OccurrenceRead:
    state_root = Path(str(bundle.get("state_root", ""))).resolve()
    provenance = _persisted_provenance(state_root)
    if not provenance.get("ok"):
        return OccurrenceRead(
            ok=False,
            checks={str(provenance.get("error", "PROVENANCE_FAILURE")): False},
            occurrence=None,
            missing_contract=missing_source_owner_contract(
                missing_fields=(str(provenance.get("error", "PROVENANCE_FAILURE")),),
            ),
        )
    c9 = read_c9_summary({"c9_path": str(provenance["c9_path"])})
    event_hash = str(provenance["e1_hash"])
    event_pair = next(
        ((key, body) for key, body in c9["occurrences"] if key == event_hash),
        None,
    )
    event_body = event_pair[1] if event_pair else {}
    event = dict(event_body, hash=event_hash) if event_pair else {}
    event_clock = int(event.get("time", bundle.get("event_time", 0)))
    c12 = read_c12(provenance["c12_path"])
    branch_id = str(provenance["branch_id"])
    root_branch = c12["branches"].get("root")
    branch = c12["branches"].get(branch_id)
    root_checkpoints = c12["checkpoints"].get("root") or [{}]
    root_state = root_checkpoints[-1]
    initial_root_state = root_checkpoints[0]
    branch_clock = int(c12["last_clock"].get(branch_id, 0))
    root_actors = ((initial_root_state.get("state") or {}).get("actors") or {})
    actor_block = root_actors.get("A") or {}
    actor_state = actor_block.get("state")
    persisted_actor_snapshot = {
        "state": actor_state,
        "state_hash": digest(actor_state) if isinstance(actor_state, Mapping) else "",
        "hash": actor_block.get("snapshot_hash", ""),
        "last_clock": actor_block.get("last_clock", 0),
        "source_ref": actor_block.get("source_ref", ""),
        "source_hash": actor_block.get("source_hash", ""),
    }
    source = dict(provenance["source"] or {})
    binding = (
        dict(clock_binding_override)
        if clock_binding_override is not None
        else _clock_binding(event_clock, branch_clock)
    )
    bundle_source = (
        dict(bundle.get("source"))
        if isinstance(bundle.get("source"), Mapping)
        else {}
    )
    bundle_actor = (
        dict(bundle.get("actor_snapshot"))
        if isinstance(bundle.get("actor_snapshot"), Mapping)
        else {}
    )
    identity_rows = [
        (event_id, ref) for event_id, ref in c9["event_identity"]
    ]
    checks = {
        "session_meta_present": True,
        "state_root_matches_session": Path(
            str(provenance["session"].get("state_root", ""))
        ).resolve()
        == state_root,
        "product_root_matches_session": Path(
            str(provenance["session"].get("product_root", ""))
        ).resolve()
        == (state_root / "product").resolve(),
        "c9_path_canonical": Path(str(bundle.get("c9_path", ""))).resolve()
        == provenance["c9_path"],
        "c12_path_canonical": Path(str(bundle.get("c12_path", ""))).resolve()
        == provenance["c12_path"],
        "branch_id_matches_session": bundle.get("branch_id") == branch_id,
        "root_branch_id_matches_session": provenance["root_branch_id"] == "root",
        "source_actor_map_matches_session": bundle.get("source_actor_map")
        == provenance["source_actor_map"],
        "bundle_source_matches_session": bundle_source == provenance["source"],
        "bundle_source_matches_journal": bundle_source
        == provenance["journal_source"],
        "session_source_matches_journal": provenance["source"]
        == provenance["journal_source"],
        "sidecar_source_matches_session": provenance["provenance_source"]
        == provenance["source"],
        "journal_source_present": isinstance(
            provenance["journal_source"], Mapping
        ),
        "c8_digest_matches_session": bundle.get("c8_state_digest")
        == provenance["c8_digest"],
        "c8_digest_matches_journal": provenance["c8_digest"]
        == provenance["journal_state_digest"],
        "event_hash_matches_session": event_hash == str(provenance["e1_hash"]),
        "bundle_event_hash_matches": bundle.get("e1_event_hash") == event_hash,
        "event_row_present": bool(event_pair),
        "event_hash_is_c9_key": bool(event_pair)
        and event_pair[0] == event_hash,
        "event_id_matches_identity": any(
            event_id == event.get("event_id") and ref == event_hash
            for event_id, ref in identity_rows
        ),
        "event_time_matches_journal": event_clock
        == int(provenance["journal_clock"] or -1),
        "bundle_event_time_matches": int(bundle.get("event_time", -1))
        == event_clock,
        "bundle_event_id_matches": bundle.get("event_id") == event.get("event_id"),
        "actor_id_matches_session": provenance["source_actor_map"].get(
            "TEST_ONLY_R31J_A"
        )
        == provenance["journal_actor_id"],
        "other_actor_id_matches_session": provenance["source_actor_map"].get(
            "TEST_ONLY_R31J_B"
        )
        == provenance["journal_other_actor_id"],
        "actor_snapshot_present": bool(bundle_actor),
        "actor_snapshot_source_ref_matches_c8": bundle_actor.get("source_ref")
        == provenance["journal_actor"].get("source_ref"),
        "actor_snapshot_source_hash_matches_c8": bundle_actor.get("source_hash")
        == provenance["journal_actor"].get("source_hash"),
        "actor_snapshot_actor_id_matches_c8": (
            (bundle_actor.get("state") or {}).get("actor_id")
            == provenance["journal_actor"].get("actor_id")
        ),
        "actor_snapshot_source_ref_matches_c12": bundle_actor.get("source_ref")
        == actor_block.get("source_ref"),
        "actor_snapshot_source_hash_matches_c12": bundle_actor.get("source_hash")
        == actor_block.get("source_hash"),
        "actor_snapshot_authority_from_persisted_c12": True,
        "bundle_actor_snapshot_ignored_as_authority": True,
        "event_clock_source": binding.get("event_clock_source")
        == EVENT_CLOCK_SOURCE,
        "event_clock_domain": binding.get("event_clock_domain") == EVENT_DOMAIN,
        "branch_clock_source": binding.get("branch_clock_source")
        == BRANCH_CLOCK_SOURCE,
        "branch_clock_domain": binding.get("branch_clock_domain")
        == BRANCH_DOMAIN,
        "root_branch_present": root_branch is not None,
        "branch_present": branch is not None,
        "branch_parent_is_root": branch is not None
        and branch.get("parent_branch_id") == "root",
        "branch_clock_matches_c12": int(binding.get("branch_clock", -1))
        == branch_clock,
        "event_clock_matches_occurrence": int(binding.get("event_clock", -1))
        == event_clock,
        "distinct_clock_sources": (
            event_clock != branch_clock
            and binding.get("distinct_sources") is True
            and binding.get("substitution") is False
            and binding.get("equality_claimed") is False
            and binding.get("clock_substitution_allowed") is False
        ),
        "clock_binding_sealed": valid(dict(binding)),
        "source_event_identity": bool(source.get("b_event_hash")),
        "source_operation": source.get("b_operation")
        in {"SHARE_TOOL", "REFUSE_TOOL"},
        "source_performed_flag": isinstance(source.get("b_performed"), bool),
        "source_clock_present": isinstance(source.get("b_clock"), int),
        "no_duplicate_admission": True,
        "no_new_store_created": True,
    }
    missing = tuple(name for name, ok in checks.items() if not ok)
    if missing:
        return OccurrenceRead(
            ok=False,
            checks=checks,
            occurrence=None,
            missing_contract=missing_source_owner_contract(
                event_hash=event_hash,
                event_id=str(event.get("event_id", bundle.get("event_id", ""))),
                event_clock=event_clock,
                branch_clock=branch_clock,
                root_id="root",
                branch_id=branch_id,
                missing_fields=missing,
            ),
        )
    occurrence = {
        "schema": OCCURRENCE_SCHEMA,
        "grade": GRADE,
        "native": False,
        "event": event,
        "event_hash": event_hash,
        "event_id": event.get("event_id"),
        "event_clock": event_clock,
        "branch_clock": branch_clock,
        "clock_binding": binding,
        "clock_binding_hash": binding["hash"],
        "root_branch": root_branch,
        "root_branch_hash": digest(root_branch),
        "root_state": root_state,
        "root_state_hash": root_state.get("hash"),
        "branch": branch,
        "branch_hash": digest(branch),
        "branch_id": branch_id,
        "branch_parent_id": branch.get("parent_branch_id"),
        "branch_fork_clock": branch.get("fork_clock"),
        "source": source,
        "actor_id": provenance["source_actor_map"]["TEST_ONLY_R31J_A"],
        "actor_snapshot": {
            "state": actor_state,
            "state_hash": digest(actor_state)
            if isinstance(actor_state, Mapping)
            else "",
            "hash": actor_block.get("snapshot_hash", ""),
            "last_clock": provenance["journal_actor"].get("clock", 0),
            "source_ref": actor_block.get("source_ref", ""),
            "source_hash": actor_block.get("source_hash", ""),
        },
        "source_material_access": source_material_access(source),
        "c9": c9,
        "c9_path": str(provenance["c9_path"]),
        "c12_path": str(provenance["c12_path"]),
        "provenance": {
            "session_schema": provenance["session_schema"],
            "branch_id": provenance["branch_id"],
            "root_branch_id": provenance["root_branch_id"],
            "c8_digest": provenance["c8_digest"],
            "journal_state_digest": provenance["journal_state_digest"],
            "journal_occurrence_id": provenance["journal_occurrence_id"],
            "journal_content_hash": provenance["journal_content_hash"],
            "journal_clock": provenance["journal_clock"],
            "provenance_path": str(provenance["provenance_path"]),
            "journal_path": str(provenance["journal_path"]),
        },
        "duplicate_admission": False,
        "new_store_created": False,
        "c9_read_only": True,
    }
    return OccurrenceRead(
        ok=True, checks=checks, occurrence=occurrence, missing_contract=None
    )


def build_context(occurrence: Mapping[str, Any]) -> dict:
    event_clock = int(occurrence["event_clock"])
    actor_snapshot = occurrence["actor_snapshot"]
    source = occurrence["source"]
    actor_id = occurrence["actor_id"]
    conditioning_source = make_conditioning_source(
        source_ref="TEST_ONLY_S35_OCCURRENCE_MATERIAL_A",
        source_class="ResolvedStructuralContext",
        subject=actor_id,
        body={
            "access": (
                "granted" if occurrence["source_material_access"] else "denied"
            ),
            "as_of": event_clock,
            "scene": str(
                (occurrence["event"].get("content") or {}).get("scene", "")
            ),
            "material_remaining": actor_snapshot["state"].get(
                "material_remaining"
            ),
            "material_ref": source.get("b_event_hash"),
            "material_feasible_after": source.get("material_feasible_after"),
            "source_grade": "TEST_ONLY_SOURCEFREE_OCCURRENCE_NOT_NATIVE",
            "native_grant": False,
        },
    )
    conditioning = bind_conditioning(
        subject=actor_id,
        sources=[conditioning_source],
        as_of=event_clock,
    )
    material_ok, material_refs, material_reason = eligible_material(
        conditioning,
        event_scene=str(
            (occurrence["event"].get("content") or {}).get("scene", "")
        ),
        event_time=event_clock,
        as_of=event_clock,
    )
    context = S35Context(
        actor_id=actor_id,
        event_ref=occurrence["event_hash"],
        event_id=str(occurrence["event_id"]),
        event_time=event_clock,
        as_of=event_clock,
        scene=str((occurrence["event"].get("content") or {}).get("scene", "")),
        root_id="root",
        root_branch_hash=occurrence["root_branch_hash"],
        root_state_hash=str(occurrence["root_state_hash"]),
        branch_id=occurrence["branch_id"],
        branch_hash=occurrence["branch_hash"],
        branch_parent_id=str(occurrence["branch_parent_id"]),
        branch_fork_clock=int(occurrence["branch_fork_clock"]),
        clock=event_clock,
        material_eligible=material_ok,
        eligible_material_refs=tuple(material_refs),
    )
    return {
        "context": context,
        "conditioning": conditioning,
        "conditioning_source": conditioning_source,
        "material_eligible": material_ok,
        "material_refs": tuple(material_refs),
        "material_reason": material_reason,
    }


def evaluate_occurrence(
    occurrence: Mapping[str, Any],
    *,
    controlled: bool = False,
    perception_status: str = "ACCESSIBLE",
    action_kind: str = "REQUEST_TOOL",
    action_present: bool = True,
    perception_receipt: Mapping[str, Any] | None = None,
    action_receipt: Mapping[str, Any] | None = None,
    qualified_owner_resolver: Any = None,
) -> dict:
    built = build_context(occurrence)
    context = built["context"]
    rule = make_rule(context.actor_id)
    registry = ResponseRuleRegistry.test_only((rule,))
    lookup = lookup_rule(
        registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=context.actor_id,
    )
    perception = (
        dict(perception_receipt) if perception_receipt is not None else None
    )
    action = dict(action_receipt) if action_receipt is not None else None
    perception_gate = "MISSING"
    action_gate = "MISSING"
    if perception is not None:
        perception_gate = (
            access.validate_a_local_perception(perception, context=context)
            or "OK"
        )
    elif controlled:
        perception = access.make_a_local_perception_receipt(
            context=context,
            source_ref="TEST_ONLY_ADP017_ACCESS_S35_A_LOCAL_PERCEPTION",
            perception_ref="TEST_ONLY_OCCURRENCE_PERCEPTION_" + perception_status,
            access_status=perception_status,
            perceived_at=context.event_time,
            scene=context.scene,
            content={
                "occurrence_clock": occurrence["event_clock"],
                "branch_clock": occurrence["branch_clock"],
                "clock_binding_hash": occurrence["clock_binding_hash"],
            },
            evidence_grade=S35_GRADE_CONTROLLED,
            actual_actor_input=False,
            qualification=S35_QUALIFICATION_CONTROLLED,
        )
        perception_gate = (
            access.validate_a_local_perception(perception, context=context)
            or "OK"
        )
    if action is not None:
        action_gate = (
            access.validate_a_owned_action(
                action, context=context, perceived_at=context.event_time
            )
            or "OK"
        )
    elif controlled and action_present:
        action = access.make_a_owned_action_receipt(
            context=context,
            source_ref="TEST_ONLY_A_ACTION_S35_A_OWNED",
            action_ref="TEST_ONLY_OCCURRENCE_ACTION_" + action_kind,
            action_kind=action_kind,
            performed=True,
            action_time=context.event_time,
            content={
                "occurrence_clock": occurrence["event_clock"],
                "branch_clock": occurrence["branch_clock"],
                "clock_binding_hash": occurrence["clock_binding_hash"],
            },
            evidence_grade=S35_GRADE_CONTROLLED,
            actual_actor_input=False,
            qualification=S35_QUALIFICATION_CONTROLLED,
        )
        action_gate = (
            access.validate_a_owned_action(
                action, context=context, perceived_at=context.event_time
            )
            or "OK"
        )
    request = S35ActorAccessRequest(
        perception_receipt=perception,
        action_receipt=action,
        qualified_owner_resolver=qualified_owner_resolver,
    )
    evaluation = access.evaluate_actor_access_response(
        rule_lookup=lookup,
        event_ref=context.event_ref,
        event_time=context.event_time,
        subject=context.actor_id,
        request=request,
        conditioning_readset=built["conditioning"].readset_refs,
        context=context,
        as_of=context.as_of,
        material_eligible=built["material_eligible"],
        eligible_material_refs=built["material_refs"],
    )
    c9 = occurrence["c9"]
    decision = evaluate_target(
        registry=TargetRuleRegistry.production(),
        proposal=None,
        permission=None,
        actor_id=context.actor_id,
        before_target_hash=c9["target_state_hash"],
        existing_target_ids=frozenset(c9["target_ids"]),
        prior_event_hash=context.event_ref,
        as_of=context.clock,
        enacted_history_refs=(),
        permitted_issuer_refs=frozenset(),
        response_hash=evaluation.response.receipt_hash,
    )
    return {
        "occurrence": occurrence,
        "built": built,
        "perception_gate": perception_gate,
        "action_gate": action_gate,
        "perception_validated_before_response": controlled,
        "action_validated_before_response": controlled and action is not None,
        "evaluation": evaluation,
        "decision": decision,
        "c9": c9,
        "new_store_created": False,
        "duplicate_admission": False,
    }


def summary(result: Mapping[str, Any]) -> dict:
    evaluation = result["evaluation"]
    decision = result["decision"]
    receipt = evaluation.receipt or {}
    occurrence = result["occurrence"]
    return {
        "outcome": evaluation.response.reason,
        "response_status": evaluation.response.status.value,
        "target_proposals": len(evaluation.response.target_proposals),
        "target_branch": decision.branch.value,
        "target_reason": decision.reason.value,
        "target_id": decision.target_id,
        "s35_receipt_hash": receipt.get("hash", ""),
        "evidence_grade": receipt.get("evidence_grade", ""),
        "actual_actor_input": receipt.get("actual_actor_input"),
        "qualification": receipt.get("qualification", ""),
        "hold_reason": receipt.get("hold_reason", ""),
        "event_ref": receipt.get("event_ref", ""),
        "event_id": receipt.get("event_id", ""),
        "event_clock": occurrence["event_clock"],
        "branch_clock": occurrence["branch_clock"],
        "clock_binding_hash": occurrence["clock_binding_hash"],
        "root_branch_hash": occurrence["root_branch_hash"],
        "branch_hash": occurrence["branch_hash"],
        "branch_fork_clock": occurrence["branch_fork_clock"],
        "perception_gate": result["perception_gate"],
        "action_gate": result["action_gate"],
        "perception_validated_before_response": result[
            "perception_validated_before_response"
        ],
        "action_validated_before_response": result[
            "action_validated_before_response"
        ],
        "material_eligible": result["built"]["material_eligible"],
        "material_refs": list(result["built"]["material_refs"]),
        "new_store_created": False,
        "duplicate_admission": False,
    }


__all__ = [
    "BRANCH_DOMAIN",
    "CLOCK_BINDING_SCHEMA",
    "EVENT_CLOCK_SOURCE",
    "EVENT_DOMAIN",
    "OccurrenceRead",
    "OCCURRENCE_SCHEMA",
    "build_context",
    "evaluate_occurrence",
    "make_clock_binding",
    "missing_source_owner_contract",
    "read_occurrence",
    "summary",
]
