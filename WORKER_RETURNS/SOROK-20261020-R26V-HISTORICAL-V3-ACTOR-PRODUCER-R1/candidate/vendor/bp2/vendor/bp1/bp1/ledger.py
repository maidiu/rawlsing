"""Per-actor append-only historical ledger and durable actor snapshots.

Each BP1 actor owns its ledger. Only that actor's own performed actions change
its state. A shared objective event is an objective fact recorded identically in
both ledgers; it grants no actor state, perception or psychology. A performed
action is only admitted through the G18 source-issued material/action receipt.

This is a TEST_ONLY sourcefree carrier. It is not native ADP007 actor genesis or
a developmental-rule issuer.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from .canon import digest, seal, valid
from .source import (
    ActorSource,
    BP1_ACTOR_SOURCE_GRADE,
    BP1_NATIVE_GRANT,
    PSYCHOLOGY_KEYS,
    SourceRefusal,
    _has_forbidden_key,
    TEST_ONLY_PREFIX,
    verify_actor_source,
)

BP1_EVENT_SCHEMA = "BP1_ACTOR_LEDGER_EVENT@1"
BP1_SNAPSHOT_SCHEMA = "BP1_ACTOR_SNAPSHOT@1"
BP1_OBJECTIVE_SCHEMA = "BP1_SHARED_OBJECTIVE@1"
EVENT_KINDS = frozenset({
    "PRIOR_HISTORY", "SHARED_OBJECTIVE", "PERFORMED_ACTION", "OTHER_ACTION",
    "RELATION_VIEW", "NO_CHANGE", "DENY",
})
_STATE_FIELDS = ("cash", "free_hours", "completed_units", "material_remaining",
                 "tools_remaining", "skill", "debt_units")


class LedgerRefusal(ValueError):
    pass


def _event_id(body: dict) -> str:
    return TEST_ONLY_PREFIX + "EVT_" + digest(body)


def _future_keys(value: Any) -> str | None:
    forbidden = frozenset({
        "future_child", "future_child_personality", "future_child_outcome",
        "future_child_desired_adversity_tag", "future_child_health_outcome",
        "future_child_education_outcome",
        "any_field_derived_from_future_child",
    })
    return _has_forbidden_key(value, forbidden)


def _assert_no_future(value: Any):
    found = _future_keys(value)
    if found:
        raise LedgerRefusal("FUTURE_CHILD_INFORMATION_LEAK:" + found)


def make_objective_event(material: dict, witness: dict,
                         participants: list[str]) -> dict:
    """Build the shared objective fact body and its content identity."""
    if not isinstance(material, dict) or not isinstance(witness, dict):
        raise LedgerRefusal("SHARED_OBJECTIVE_SOURCE_MISSING")
    if witness.get("status") != "WITNESSED":
        raise LedgerRefusal("SHARED_OBJECTIVE_NOT_WITNESSED")
    if len(set(participants)) != 2:
        raise LedgerRefusal("SHARED_OBJECTIVE_REQUIRES_TWO_ACTORS")
    body = {
        "schema": BP1_OBJECTIVE_SCHEMA,
        "objective_kind": "joint_material_task",
        "task": "coordinated_material_inspection",
        "participants": sorted(participants),
        "material_event_ref": material["event_id"],
        "material_receipt_id": digest(material["source_receipt"]),
        "witness_ref": witness["event_id"],
        "witness_participants": sorted(witness["participants"]),
        "source_grade": BP1_ACTOR_SOURCE_GRADE,
        "native_grant": BP1_NATIVE_GRANT,
    }
    _assert_no_future(body)
    objective_hash = digest(body)
    return dict(
        body=body,
        objective_hash=objective_hash,
        objective_event_id=(TEST_ONLY_PREFIX + "OBJ_" + objective_hash),
        hash=digest(body),
    )


@dataclass(frozen=True)
class LedgerEvent:
    event_id: str
    actor_id: str
    actor_source_ref: str
    actor_source_hash: str
    event_index: int
    kind: str
    payload: dict
    causal_parent_event_ids: tuple[str, ...]
    material_event_ref: str | None
    performed_action_receipt_ref: str | None
    source_grade: str
    native_grant: str
    hash: str

    def as_dict(self) -> dict:
        return {
            "schema": BP1_EVENT_SCHEMA,
            "event_id": self.event_id,
            "actor_id": self.actor_id,
            "actor_source_ref": self.actor_source_ref,
            "actor_source_hash": self.actor_source_hash,
            "event_index": self.event_index,
            "kind": self.kind,
            "payload": self.payload,
            "causal_parent_event_ids": list(self.causal_parent_event_ids),
            "material_event_ref": self.material_event_ref,
            "performed_action_receipt_ref": self.performed_action_receipt_ref,
            "source_grade": self.source_grade,
            "native_grant": self.native_grant,
            "hash": self.hash,
        }


class ActorLedger:
    """One actor's append-only event ledger with own-state conservation."""

    def __init__(self, source: ActorSource, prior_history_events: list[dict] | None = None):
        accepted, reason = verify_actor_source(source)
        if not accepted:
            raise SourceRefusal(reason)
        self.source = source
        self.events: list[LedgerEvent] = []
        self._state: dict[str, Any] = {}
        self._base_state: dict[str, Any] = {}
        self.prior_history_hash: str = ""
        self.last_clock: int = source.birth_clock
        if prior_history_events is not None:
            self._ingest_prior_history(prior_history_events)
        else:
            self._state = {
                "actor_id": source.actor_id,
                "role": source.role,
                "cash": source.initial_cash,
                "free_hours": source.initial_free_hours,
                "completed_units": 0,
                "material_remaining": source.material_units,
                "tools_remaining": 0,
                "skill": 0,
                "debt_units": 0,
                "place": "INST_WORKSHOP_A",
                "availability_status": "available_for_encounter",
                "practices": [],
                "attitudes": [],
                "projects": [],
                "nonmother_relations": [],
                "material_position": "waged_" + source.role,
                "health": "recovered",
            }
            self._base_state = deepcopy(self._state)

    # ------------------------------------------------------------------
    # replay / snapshot
    # ------------------------------------------------------------------
    def _ingest_prior_history(self, history_events: list[dict]):
        from lab_sgi1.history import replay_history
        replay = replay_history(history_events)
        if not replay["valid"]:
            raise LedgerRefusal("PRIOR_HISTORY_NOT_RESOLVED")
        self._base_state = deepcopy(replay["state"])
        self._state = deepcopy(self._base_state)
        self.prior_history_hash = replay["history_hash"]
        self.last_clock = max(
            (int(e.get("effective_index", 0)) for e in history_events), default=0)
        payload = {
            "g18_history_hash": replay["history_hash"],
            "g18_state": deepcopy(replay["state"]),
            "role": self.source.role,
            "material_units": self.source.material_units,
            "history_event_count": len(history_events),
            "history_head": history_events[-1]["event_id"] if history_events else None,
        }
        self._append("PRIOR_HISTORY", payload, [], None, None,
                     allow_state_prior=True)

    @property
    def state(self) -> dict:
        return deepcopy(self._state)

    @property
    def state_hash(self) -> str:
        return digest(self._state)

    @property
    def history_hash(self) -> str:
        return digest([e.hash for e in self.events])

    @property
    def event_ids(self) -> tuple[str, ...]:
        return tuple(e.event_id for e in self.events)

    @property
    def prior_history_event_id(self) -> str | None:
        for event in self.events:
            if event.kind == "PRIOR_HISTORY":
                return event.event_id
        return None

    @property
    def performed_action_events(self) -> list[LedgerEvent]:
        return [e for e in self.events if e.kind == "PERFORMED_ACTION"]

    @property
    def objective_events(self) -> list[LedgerEvent]:
        return [e for e in self.events if e.kind == "SHARED_OBJECTIVE"]

    def snapshot(self) -> dict:
        body = {
            "schema": BP1_SNAPSHOT_SCHEMA,
            "actor_id": self.source.actor_id,
            "source_ref": self.source.source_ref,
            "source_hash": self.source.source_hash,
            "role": self.source.role,
            "state": deepcopy(self._state),
            "state_hash": self.state_hash,
            "history_hash": self.history_hash,
            "prior_history_hash": self.prior_history_hash,
            "event_head": self.events[-1].event_id if self.events else None,
            "event_count": len(self.events),
            "last_clock": self.last_clock,
            "performed_action_refs": [e.event_id for e in self.performed_action_events],
            "objective_refs": [e.event_id for e in self.objective_events],
            "other_actor_id": self.source.other_actor_id,
            "known_unknowns": list(self.source.known_unknowns),
            "source_grade": self.source.source_grade,
            "native_grant": self.source.native_grant,
            "psychology_claim": False,
            "native_actor_claim": False,
        }
        _assert_no_future(body)
        return seal(body)

    # ------------------------------------------------------------------
    # append
    # ------------------------------------------------------------------
    def _append(self, kind: str, payload: dict, parents: tuple[str, ...],
                material_event_ref: str | None,
                performed_action_receipt_ref: str | None,
                allow_state_prior: bool = False) -> LedgerEvent:
        if kind not in EVENT_KINDS:
            raise LedgerRefusal("EVENT_KIND_UNKNOWN")
        if kind != "PRIOR_HISTORY" and kind not in self.source.event_permissions:
            raise LedgerRefusal("ACTOR_PERMISSION_DENIED:" + kind)
        _assert_no_future(payload)
        index = len(self.events)
        known = {e.event_id for e in self.events}
        if any(parent not in known for parent in parents):
            raise LedgerRefusal("MISSING_CAUSAL_PARENT")
        body = {
            "schema": BP1_EVENT_SCHEMA,
            "actor_id": self.source.actor_id,
            "actor_source_ref": self.source.source_ref,
            "actor_source_hash": self.source.source_hash,
            "event_index": index,
            "kind": kind,
            "payload": deepcopy(payload),
            "causal_parent_event_ids": list(parents),
            "material_event_ref": material_event_ref,
            "performed_action_receipt_ref": performed_action_receipt_ref,
            "source_grade": self.source.source_grade,
            "native_grant": self.source.native_grant,
        }
        event_hash = digest(body)
        event = LedgerEvent(
            event_id=_event_id(body), actor_id=self.source.actor_id,
            actor_source_ref=self.source.source_ref,
            actor_source_hash=self.source.source_hash, event_index=index,
            kind=kind, payload=deepcopy(payload),
            causal_parent_event_ids=tuple(parents),
            material_event_ref=material_event_ref,
            performed_action_receipt_ref=performed_action_receipt_ref,
            source_grade=self.source.source_grade,
            native_grant=self.source.native_grant, hash=event_hash)
        self.events.append(event)
        return event

    def append_shared_objective(self, objective: dict,
                                parents: tuple[str, ...] = ()) -> LedgerEvent:
        if objective.get("objective_hash") != digest(objective.get("body", {})):
            raise LedgerRefusal("SHARED_OBJECTIVE_HASH_MISMATCH")
        if self.source.actor_id not in objective["body"]["participants"]:
            raise LedgerRefusal("SHARED_OBJECTIVE_NOT_PARTICIPANT")
        return self._append(
            "SHARED_OBJECTIVE",
            {
                "objective_event_id": objective["objective_event_id"],
                "objective_hash": objective["objective_hash"],
                "objective_body": deepcopy(objective["body"]),
                "objective_ref": objective["objective_event_id"],
            },
            parents,
            objective["body"]["material_event_ref"],
            None,
        )

    def append_performed_action(
        self, action: dict, material: dict, objective_event_id: str,
        *, consume_own_material: bool = False,
        own_material_units: int = 0,
        parents: tuple[str, ...] = (),
    ) -> LedgerEvent:
        from lab_sgi1.joint import (
            verify_material_source, verify_performed_action,
        )
        accepted, reason, material_payload = verify_material_source(material)
        if not accepted:
            raise LedgerRefusal("MATERIAL_SOURCE_NOT_AUTHENTICATED:" + str(reason))
        accepted, reason = verify_performed_action(action, material)
        if not accepted:
            raise LedgerRefusal("PERFORMED_ACTION_NOT_AUTHENTICATED:" + str(reason))
        if action.get("owner_id") != self.source.actor_id:
            raise LedgerRefusal("PERFORMED_ACTION_OWNER_MISMATCH")
        if action.get("status") != "PERFORMED":
            raise LedgerRefusal("PERFORMED_ACTION_NOT_PERFORMED")
        if action.get("before") != self._state:
            raise LedgerRefusal("PERFORMED_ACTION_BEFORE_STATE_MISMATCH")
        if consume_own_material:
            if type(own_material_units) is not int or own_material_units <= 0:
                raise LedgerRefusal("OWN_MATERIAL_UNITS_INVALID")
            if self._state.get("material_remaining", 0) < own_material_units:
                raise LedgerRefusal("OWN_MATERIAL_EXHAUSTED")
        event = self._append(
            "PERFORMED_ACTION",
            {
                "objective_event_id": objective_event_id,
                "performed": True,
                "g18_action": deepcopy(action),
                "material_packet": deepcopy(material),
                "material_event_ref": material["event_id"],
                "material_receipt_id": digest(material["source_receipt"]),
                "material_payload": {
                    "payment_per_actor": material_payload["payment_per_actor"],
                    "task_hours": material_payload["task_hours"],
                    "material_units": material_payload["material_units"],
                },
                "before": deepcopy(action["before"]),
                "after": deepcopy(action["after"]),
                "delta": {
                    key: action["after"][key] - action["before"][key]
                    for key in _STATE_FIELDS
                },
                "consume_own_material": consume_own_material,
                "own_material_units": own_material_units,
            },
            parents,
            material["event_id"],
            digest(action["source_receipt"]),
        )
        self._state = deepcopy(action["after"])
        self.last_clock = max(
            self.last_clock, int(action.get("effective_index", self.last_clock)))
        return event

    def append_other_action(self, action: dict, material: dict,
                            parents: tuple[str, ...] = ()) -> LedgerEvent:
        from lab_sgi1.joint import verify_performed_action
        accepted, reason = verify_performed_action(action, material)
        if not accepted:
            raise LedgerRefusal("OTHER_ACTION_NOT_AUTHENTICATED:" + str(reason))
        if action.get("owner_id") != self.source.other_actor_id:
            raise LedgerRefusal("OTHER_ACTION_OWNER_MISMATCH")
        if action.get("status") != "PERFORMED":
            raise LedgerRefusal("OTHER_ACTION_NOT_PERFORMED")
        event = self._append(
            "OTHER_ACTION",
            {
                "performed": True,
                "other_actor_id": action["owner_id"],
                "g18_action": deepcopy(action),
                "material_packet": deepcopy(material),
                "material_event_ref": material["event_id"],
                "material_receipt_id": digest(material["source_receipt"]),
                "effect_on_own_state": "NONE",
            },
            parents,
            material["event_id"],
            digest(action["source_receipt"]),
        )
        return event

    def append_relation_view(self, target_actor_id: str, perceived_state: str,
                             causal_basis: str,
                             parents: tuple[str, ...] = ()) -> LedgerEvent:
        if perceived_state not in {"UNKNOWN_OR_NONRECIPROCAL", "PARTIAL",
                                   "NOT_PERCEIVED"}:
            raise LedgerRefusal("RELATION_VIEW_NOT_TYPED")
        return self._append(
            "RELATION_VIEW",
            {
                "perceiver": self.source.actor_id,
                "target": target_actor_id,
                "perceived_state": perceived_state,
                "causal_basis": causal_basis,
                "psychology_claim": False,
            },
            parents,
            None,
            None,
        )

    def append_no_change(self, reason: str,
                         parents: tuple[str, ...] = ()) -> LedgerEvent:
        if not isinstance(reason, str) or not reason:
            raise LedgerRefusal("NO_CHANGE_REASON_MISSING")
        return self._append(
            "NO_CHANGE",
            {"reason": reason, "performed": False, "state_changed": False},
            parents, None, None)

    def append_deny(self, reason: str,
                    parents: tuple[str, ...] = ()) -> LedgerEvent:
        if not isinstance(reason, str) or not reason:
            raise LedgerRefusal("DENY_REASON_MISSING")
        return self._append(
            "DENY",
            {"reason": reason, "performed": False, "state_changed": False},
            parents, None, None)

    # ------------------------------------------------------------------
    # replay verification
    # ------------------------------------------------------------------
    def verify(self) -> tuple[bool, list[str]]:
        errors: list[str] = []
        accepted, reason = verify_actor_source(self.source)
        if not accepted:
            errors.append(str(reason))
            return False, errors
        known: set[str] = set()
        state = deepcopy(self._base_state)
        for index, event in enumerate(self.events):
            if event.actor_id != self.source.actor_id:
                errors.append("CROSS_ACTOR_EVENT")
            if event.actor_source_ref != self.source.source_ref:
                errors.append("SOURCE_REF_MISMATCH")
            if event.actor_source_hash != self.source.source_hash:
                errors.append("SOURCE_HASH_MISMATCH")
            if event.event_index != index:
                errors.append("EVENT_INDEX_NOT_MONOTONIC")
            if event.event_id in known:
                errors.append("DUPLICATE_EVENT_ID")
            if any(p not in known for p in event.causal_parent_event_ids):
                errors.append("MISSING_CAUSAL_PARENT")
            if event.hash != digest({k: v for k, v in event.as_dict().items()
                                     if k not in {"hash", "event_id"}}):
                errors.append("EVENT_HASH_INVALID")
            try:
                _assert_no_future(event.payload)
            except LedgerRefusal as exc:
                errors.append(str(exc))
            if event.kind == "PRIOR_HISTORY":
                if event.payload.get("g18_state") != self._base_state:
                    errors.append("PRIOR_HISTORY_STATE_MISMATCH")
            elif event.kind == "PERFORMED_ACTION":
                from lab_sgi1.joint import verify_performed_action
                action = event.payload.get("g18_action", {})
                material = event.payload.get("material_packet")
                accepted, reason = verify_performed_action(action, material)
                if not accepted:
                    errors.append("PERFORMED_ACTION_RECEIPT_INVALID:" + str(reason))
                if action.get("owner_id") != self.source.actor_id:
                    errors.append("PERFORMED_ACTION_OWNER_MISMATCH")
                if action.get("before") != state:
                    errors.append("PERFORMED_ACTION_BEFORE_STATE_MISMATCH")
                state = deepcopy(action.get("after", {}))
            elif event.kind == "OTHER_ACTION":
                from lab_sgi1.joint import verify_performed_action
                action = event.payload.get("g18_action", {})
                material = event.payload.get("material_packet")
                accepted, reason = verify_performed_action(action, material)
                if not accepted:
                    errors.append("OTHER_ACTION_RECEIPT_INVALID:" + str(reason))
                if event.payload.get("other_actor_id") != self.source.other_actor_id:
                    errors.append("OTHER_ACTION_OWNER_MISMATCH")
            elif event.kind in {"NO_CHANGE", "DENY"}:
                if event.payload.get("performed") is not False:
                    errors.append("NON_PERFORMED_EVENT_CLAIMS_ACTION")
            known.add(event.event_id)
        if state != self._state:
            errors.append("REPLAY_STATE_MISMATCH")
        if self.state_hash != digest(self._state):
            errors.append("STATE_HASH_INVALID")
        return not errors, errors


def verify_snapshot(snapshot: dict, expected_hash: str | None = None) -> tuple[bool, str | None]:
    """Verify a durable actor snapshot's internal identity and source grade."""
    if not isinstance(snapshot, dict):
        return False, "SNAPSHOT_NOT_OBJECT"
    if not valid(snapshot):
        return False, "SNAPSHOT_HASH_INVALID"
    if expected_hash is not None and snapshot.get("hash") != expected_hash:
        return False, "SNAPSHOT_NOT_THE_EXPECTED_SOURCE"
    if snapshot.get("schema") != BP1_SNAPSHOT_SCHEMA:
        return False, "SNAPSHOT_SCHEMA_UNKNOWN"
    if snapshot.get("source_grade") != BP1_ACTOR_SOURCE_GRADE:
        return False, "SNAPSHOT_SOURCE_GRADE_NOT_DECLARED"
    if snapshot.get("native_grant") != BP1_NATIVE_GRANT:
        return False, "SNAPSHOT_CANNOT_CARRY_NATIVE_GRANT"
    if not snapshot.get("actor_id", "").startswith(TEST_ONLY_PREFIX):
        return False, "SNAPSHOT_ACTOR_NOT_TEST_ONLY_BP1"
    if not snapshot.get("source_ref", "").startswith(TEST_ONLY_PREFIX):
        return False, "SNAPSHOT_SOURCE_REF_NOT_TEST_ONLY_BP1"
    if snapshot.get("state_hash") != digest(snapshot.get("state", {})):
        return False, "SNAPSHOT_STATE_HASH_INVALID"
    if not isinstance(snapshot.get("history_hash"), str) or not snapshot["history_hash"]:
        return False, "SNAPSHOT_HISTORY_HASH_MISSING"
    forbidden = _has_forbidden_key(snapshot, PSYCHOLOGY_KEYS)
    if forbidden:
        return False, "SNAPSHOT_PSYCHOLOGY_CLAIM:" + forbidden
    _assert_no_future(snapshot)
    return True, None
