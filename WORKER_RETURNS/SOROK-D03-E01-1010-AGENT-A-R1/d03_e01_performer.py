"""D03/E01 sourcefree P2 event-performance connection (Agent A, #1010).

This is an orchestrating adapter, NOT a new actor chooser or state owner.

* Reconstruct the real C04->C12/P6->D03 chain with immutable J1.
* Pass a minimal actor-accessible, plural-stream context to the existing
  RecursionCycle CallProvider. All provider prospectives must pass the original
  P2Owner validator. The existing BatchEngine/P2Owner actually writes events.
* Read completed E1 events through the ordinary world reader, never by treating
  immediate_uptake.eligible_modes or model prose as an event.
* P3 psychology is NOT updated by the P2-only event path. A sourcefree observed
  P2 event proves performance at this grade, NOT native Rule A/T, volition,
  durable acquisition, historical causation of the selected action, or D04/D05.

Important: the existing RecursionCycle prospective list is an ordered batch
of 3-5 events to be realized, NOT 3-5 competing options. This adapter never
selects a motive or a member of that list.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

from developmental_recursion.contracts import RecursionRefusal, detached, digest
from developmental_recursion.engine import BatchEngine
from developmental_recursion.model_cycle import RecursionCycle
from post_provider_guard import GuardedProvider
from owner_custody import P3CoordinatedP2Owner

SCHEMA = "SOROK_D03_E01_P2_PERFORMANCE@1"
CONTEXT_SCHEMA = "SOROK_D03_E01_ACTOR_ACCESS_CONTEXT@1"
GRADE = "SOURCEFREE_P2_EVENT_ONLY"
HELD = "HELD_NOT_PERCEIVED_NO_D03_EVENT_CAUSAL_CLAIM"


def _refuse(code: str) -> None:
    raise RecursionRefusal(code)


def _mapping(value: Any, code: str) -> dict:
    if not isinstance(value, Mapping):
        _refuse(code)
    return detached(value)


def _identity(owner: Any, base: Any, session: Any, child_id: str) -> dict:
    if not hasattr(owner, "base_owner") or owner.base_owner is not base:
        _refuse("E01_P3_P2_OWNER_MISMATCH")
    if getattr(getattr(base, "fanin", None), "session", None) is not session:
        _refuse("E01_SESSION_NOT_P2_OWNER_SESSION")
    p3 = owner.snapshot()
    p2 = base.snapshot()
    if p3.root != p2.root or p3.actor != p2.actor or p3.branch != p2.branch:
        _refuse("E01_OWNER_IDENTITY_MISMATCH")
    if p3.clock != p2.clock or child_id != p2.actor:
        _refuse("E01_CHILD_OR_CLOCK_MISMATCH")
    if session.read_root().get("root_hash") != p2.root:
        _refuse("E01_WORLD_ROOT_MISMATCH")
    if session.branch_id != p2.branch or session.clock() != p2.clock:
        _refuse("E01_WORLD_BRANCH_OR_CLOCK_MISMATCH")
    return {"p3": p3.document(), "p2": p2.document()}


def _context(joined: Mapping[str, Any], identity: Mapping[str, Any]) -> dict:
    """Use an allowlist. The parent's decision/hidden reason never leaves J1."""
    d03 = _mapping(joined.get("immediate_uptake"), "E01_D03_REQUIRED")
    speech = _mapping(d03.get("speech_scope"), "E01_D03_SPEECH_REQUIRED")
    response = _mapping(d03.get("immediate_response"), "E01_D03_RESPONSE_REQUIRED")
    readset = _mapping(d03.get("readset"), "E01_D03_READSET_REQUIRED")
    if speech.get("status") != "PERCEIVED":
        _refuse("E01_D03_NOT_PERCEIVED")
    if speech.get("child_actor_id") != identity["p3"]["actor"]:
        _refuse("E01_D03_CHILD_CHANGED")
    if d03.get("identity") != identity["p3"]:
        _refuse("E01_D03_IDENTITY_STALE")
    if speech.get("hidden_reason") != "NOT_READ":
        _refuse("E01_D03_PRIVATE_STATE_LEAK")
    if d03.get("durable_formation", {}).get("status") != "MISSING_RULE":
        _refuse("E01_UNISSUED_DURABLE_RULE_PROMOTION")
    if response.get("native_action") != "NOT_ISSUED_BY_D03_RULE":
        _refuse("E01_D03_ACTION_PROMOTION")
    if response.get("status") not in {
        "COMPUTED_TEST_ONLY_IMMEDIATE", "CONTRADICTION",
        "NO_PRIOR_ORGANIZATION", "HELD_NO_ELIGIBLE_ORGANIZATION"
    }:
        _refuse("E01_D03_RESPONSE_UNQUALIFIED")
    if speech.get("event_hash") != readset.get("speech_scope", {}).get("event_hash"):
        _refuse("E01_D03_READSET_SPEECH_MISMATCH")
    if readset.get("identity") != identity["p3"]:
        _refuse("E01_D03_READSET_IDENTITY_MISMATCH")
    streams = response.get("streams")
    contradictions = response.get("contradictions")
    if not isinstance(streams, list) or not isinstance(contradictions, list):
        _refuse("E01_D03_STREAMS_SCHEMA")
    prior = _mapping(d03.get("prior_organization_scope"), "E01_PRIOR_SCOPE")
    body = {
        "schema": CONTEXT_SCHEMA,
        "grade": GRADE,
        "actor": {
            "root": identity["p3"]["root"],
            "actor_id": identity["p3"]["actor"],
            "branch": identity["p3"]["branch"],
            "clock": identity["p3"]["clock"],
            "p3_state_hash": identity["p3"]["state_hash"],
            "p2_state_hash": identity["p2"]["state_hash"],
        },
        "actual_access": {
            "event_id": speech["event_id"],
            "event_hash": speech["event_hash"],
            "speaker_actor_id": speech["speaker_actor_id"],
            "public_text": speech["text"],
            "channel": "C04_C12_P6_PERCEIVED_SPEECH",
        },
        "plural_prior_organization": {
            "project": prior.get("project"),
            "counterpart": prior.get("counterpart"),
            "activation_context_hash": d03.get("activation_context", {}).get("hash"),
            "streams": detached(streams),
            "contradictions": detached(contradictions),
            "withheld_record_hashes": detached(
                response.get("withheld_record_hashes", [])),
            "eligible_record_hashes": detached(
                readset.get("eligible_record_hashes", [])),
            "eligible_modes": detached(response.get("eligible_modes", [])),
            "interpretation_is_not_causal_selection": True,
        },
        "boundaries": {
            "parent_private_reason": "NOT_READ",
            "parent_decision": "NOT_READ",
            "child_private_memory": "NOT_ISSUED",
            "durable_formation": "MISSING_RULE",
            "material_feasibility": "OWNER_VALIDATES_PROPOSAL",
            "provider_retrospection": "NONCANONICAL",
            "event_writer": "EXISTING_P2_OWNER_ONLY",
        },
        "j1_join_hash": joined.get("hash"),
        "d03_source_closure_hash": d03.get("source_closure", {}).get("hash"),
    }
    body["hash"] = digest(body)
    return body


def _actual_readback(session: Any, records: Any, identity: Mapping[str, Any]) -> list[dict]:
    if not isinstance(records, list) or not 3 <= len(records) <= 5:
        _refuse("E01_BATCH_NOT_THREE_TO_FIVE_REALIZED")
    result = []
    previous_clock = identity["p2"]["clock"]
    for row in records:
        doc = _mapping(row, "E01_BATCH_RECORD")
        objective = _mapping(doc.get("objective"), "E01_OWNER_OBJECTIVE")
        event = _mapping(objective.get("event"), "E01_OWNER_EVENT")
        if doc.get("status") != "REALIZED":
            _refuse("E01_OWNER_NOT_REALIZED")
        if any(event.get(k) != identity["p2"][k] for k in ("root", "actor", "branch")
               if k in event):
            _refuse("E01_EVENT_FOREIGN_IDENTITY")
        if event.get("actor_id") != identity["p2"]["actor"]:
            _refuse("E01_EVENT_ACTOR_MISMATCH")
        if event.get("branch_id") != identity["p2"]["branch"]:
            _refuse("E01_EVENT_BRANCH_MISMATCH")
        event_id = event.get("e1_event_id")
        event_hash = event.get("e1_event_hash")
        if not isinstance(event_id, str) or not event_id:
            _refuse("E01_MISSING_ADMITTED_EVENT_ID")
        if not isinstance(event_hash, str) or len(event_hash) != 64:
            _refuse("E01_MISSING_ADMITTED_EVENT_HASH")
        ordinary = session.read_event(event_id)
        if not isinstance(ordinary, Mapping) or ordinary.get("e1_event_hash") != event_hash:
            _refuse("E01_REAL_WORLD_READER_SEVERED")
        if ordinary.get("branch_id") != identity["p2"]["branch"]:
            _refuse("E01_READER_BRANCH_MISMATCH")
        if ordinary.get("actor_id") != identity["p2"]["actor"]:
            _refuse("E01_READER_ACTOR_MISMATCH")
        clock = ordinary.get("event_time")
        if type(clock) is not int or clock <= previous_clock:
            _refuse("E01_READER_CLOCK_NONMONOTONE")
        previous_clock = clock
        if ordinary.get("performed") is not True:
            _refuse("E01_OWNER_EVENT_NOT_PERFORMED")
        result.append({
            "proposal_event_id": doc.get("event_id"),
            "admitted_e1_event_id": event_id,
            "admitted_e1_event_hash": event_hash,
            "event_time": clock,
            "performed": True,
            "world_reader": "session.read_event",
            "actor_access_status": doc.get("accessible", {}).get("status"),
            "readset": detached(doc.get("readset", [])),
        })
    return result


def run_d03_e01_first_batch(
    owner: Any, session: Any, *,
    child_id: str, speech_event_id: str, utterance_receipt: Any,
    plan: Any, provider: Any, journal_path: str | Path, cycle_path: str | Path,
    expected_source_closure: Any = None,
) -> dict:
    """Run existing P2 owner, NOT D03 mode selection or native psychogenesis.

    A successful SOURCEFREE_P2_EVENT proves a real ordinary P2 E1 world event,
    with actual owner receipts and world-reader readback. It does NOT establish
    that the provider's proposal was psychologically caused by P3 organizations.
    That stronger claim needs independent context-dependence falsification.
    """
    import j1_join  # read-only inherited J1 source
    initial = _identity(owner, owner.base_owner, session, child_id)
    if provider is None or not callable(getattr(provider, "call", None)):
        _refuse("E01_REAL_PROVIDER_REQUIRED")
    if Path(journal_path).resolve() == Path(cycle_path).resolve():
        _refuse("E01_JOURNAL_AND_CYCLE_COLLIDE")
    joined = j1_join.compose_j1(
        owner, session, child_id=child_id, speech_event_id=speech_event_id,
        utterance_receipt=utterance_receipt, plan=plan,
        expected=initial["p3"], expected_source_closure=expected_source_closure,
    )
    if joined.get("status") == "HELD_NOT_PERCEIVED":
        return {
            "schema": SCHEMA, "grade": GRADE, "status": HELD,
            "world_events_written": 0, "provider_called": False,
            "d03_status": "HELD_NOT_PERCEIVED",
            "native_rule": "MISSING_RULE",
            "durable_formation": "MISSING_RULE",
        }
    if joined.get("status") != j1_join.UPSTREAM_PROVEN:
        _refuse("E01_J1_UPSTREAM_NOT_PROVEN")
    context = _context(joined, initial)
    if _identity(owner, owner.base_owner, session, child_id) != initial:
        _refuse("E01_PREPROVIDER_WORLD_MOVED")
    # RecursionCycle rejects pre-existing cycle stores: no blind retry or
    # duplicate side-effect. Its BatchEngine records owner operation IDs.
    # Recheck the read-only actor/source state after provider.call but BEFORE
    # RecursionCycle forwards the proposals to the P2 world writer. A's prior
    # post-batch head check could detect a stale P3 state only after a write.
    def precommit_custody() -> None:
        if owner.store.pending():
            _refuse("E01_POSTPROVIDER_P3_PENDING_OPERATION")
        if owner.store.head() != joined["immediate_uptake"]["store_head"]["after"]:
            _refuse("E01_POSTPROVIDER_P3_HEAD_CHANGED")
        if _identity(owner, owner.base_owner, session, child_id) != initial:
            _refuse("E01_POSTPROVIDER_OWNER_IDENTITY_CHANGED")
        if j1_join.source_closure()["hash"] != joined["source_closure"]["hash"]:
            _refuse("E01_POSTPROVIDER_J1_SOURCE_CHANGED")

    # The B proxy checks at provider return, but cannot protect the gap
    # between that check and each of BatchEngine's individual owner writes.
    # P3Owner.realize itself takes _root_lock before P2Owner.realize; preserve
    # the same order, while rechecking custody for EVERY admitted P2 event.
    def event_write_custody() -> None:
        if owner.store.pending():
            _refuse("E01_EVENT_WRITE_P3_PENDING_OPERATION")
        if owner.store.head() != joined["immediate_uptake"]["store_head"]["after"]:
            _refuse("E01_EVENT_WRITE_P3_HEAD_CHANGED")
        current = _identity(owner, owner.base_owner, session, child_id)
        for key in ("root", "actor", "branch"):
            if current["p2"][key] != initial["p2"][key]:
                _refuse("E01_EVENT_WRITE_OWNER_IDENTITY_CHANGED")
        if j1_join.source_closure()["hash"] != joined["source_closure"]["hash"]:
            _refuse("E01_EVENT_WRITE_J1_SOURCE_CHANGED")

    original_p2_write_owner = P3CoordinatedP2Owner(
        owner, owner.base_owner, event_write_custody,
    )
    engine = BatchEngine(original_p2_write_owner, journal_path)
    try:
        batch = RecursionCycle(
            engine, GuardedProvider(provider, precommit_custody), cycle_path
        ).bootstrap(context)
        rows = _actual_readback(session, batch.get("records"), initial)
        status = ("SOURCEFREE_P2_EVENT_ACTOR_OBSERVED"
                  if all(row["actor_access_status"] == "OBSERVED" for row in rows)
                  else "SOURCEFREE_P2_EVENT_ACTOR_ACCESS_PARTIAL")
        report = {
            "schema": SCHEMA, "grade": GRADE, "status": status,
            "actor_id": child_id,
            "j1_hash": joined["hash"],
            "context_hash": context["hash"],
            "batch_id": batch["batch_id"],
            "history_hash": batch["history_hash"],
            "world_events_written": len(rows),
            "world_readbacks": rows,
            "p3_head_unchanged": (
                owner.store.head() == joined["immediate_uptake"]["store_head"]["after"]),
            "native_rule": "MISSING_RULE",
            "durable_formation": "MISSING_RULE",
            "motive_selection": "NOT_ASSERTED",
            "psychological_causation_by_d03": "NOT_ESTABLISHED",
            "post_provider_precommit_custody": "P3_P2_J1_SOURCE_AND_PENDING_CHECKED",
            "per_event_custody": "P3_ROOT_LOCK_PER_P2_REALIZE_ORIGINAL_ORDER",
            "cross_owner_atomicity": "NOT_CLAIMED",
            "p3_pending_operations": "REJECTED_BEFORE_EACH_P2_WRITE",
            "ordinary_unrelated_activity": "NOT_ESTABLISHED_BY_P2_CASE",
            "g2_historical_child_performance": "HELD_NOT_ESTABLISHED",
            "performed_event_owner_scope": "P2_PREBOUND_CASE_NOT_P3_PLAN",
            "distinct_later_actor_performance_reader": "NOT_ESTABLISHED",
            "source_closure": joined["source_closure"]["hash"],
            "adapter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        }
        if not report["p3_head_unchanged"]:
            _refuse("E01_P3_STORE_CHANGED_OUTSIDE_OWNER")
        report["hash"] = digest(report)
        return detached(report)
    finally:
        engine.close()


__all__ = ["run_d03_e01_first_batch", "SCHEMA", "CONTEXT_SCHEMA", "GRADE"]
