"""P3 sourcefree psychological owner composed over the unchanged P2 owner.

The P2 owner remains the sole actor/world writer. This class adds only a
normalized psychological sidecar and the frozen PREPARED -> WORLD_COMMITTED ->
PSYCH_COMMITTED -> COMPLETE protocol. The normalized store implementation is
an external dependency and is imported lazily; absence is an explicit blocked
condition, never a fallback owner or store.
"""
from __future__ import annotations

import fcntl
import hashlib
import os
from pathlib import Path
from typing import Any, Mapping

from developmental_recursion.contracts import (
    EventProposal,
    RealizedEvent,
    RecursionRefusal,
    StateIdentity,
    canonical,
    detached,
    digest,
)
from . import compression as compression_module
from . import projections
from . import test_rules

GRADE = "SOURCEFREE_TEST_ONLY"
CONFIG_SCHEMA = "P3_OWNER_CONFIG@1"
CONFIG_FILE = "p3_owner_config.json"
STORE_FILE = "p3_psyche.sqlite3"
LOCK_FILE = "p3_owner.lock"
STORE_MISSING = "DEPENDENT_EXECUTION_NOT_RUN_MISSING_RETURNED_STATE_STORE"


def _refuse(code: str, detail: str = "") -> None:
    raise RecursionRefusal(code if not detail else code + ":" + detail)


def _mapping(value: Any, code: str) -> dict:
    if not isinstance(value, Mapping):
        _refuse(code + ":SCHEMA")
    return detached(value)


def _text(value: Any, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _refuse(code)
    return value


def _hash(value: Any, code: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        _refuse(code)
    try:
        int(value, 16)
    except ValueError:
        _refuse(code)
    return value.lower()


def _whole_hash(value: Mapping[str, Any], code: str) -> str:
    supplied = _hash(value.get("hash"), code + ":HASH")
    if digest({key: item for key, item in value.items() if key != "hash"}) != supplied:
        _refuse(code + ":HASH_MISMATCH")
    return supplied


def _identity(value: Any, code: str = "IDENTITY") -> dict:
    doc = _mapping(value, code)
    for key in ("root", "actor", "branch"):
        _text(doc.get(key), code + ":" + key)
    if isinstance(doc.get("clock"), bool) or not isinstance(doc.get("clock"), int):
        _refuse(code + ":CLOCK")
    _hash(doc.get("state_hash"), code + ":STATE_HASH")
    return doc


def _code_pins() -> dict:
    files = []
    candidates = [
        __file__,
        getattr(projections, "__file__", None),
        getattr(test_rules, "__file__", None),
        getattr(compression_module, "__file__", None),
        str(Path(__file__).with_name("state_store.py")),
        str(Path(__file__).resolve().parents[2] /
            "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1" /
            "developmental_recursion" / "contracts.py"),
        str(Path(__file__).resolve().parents[2] /
            "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1" /
            "developmental_recursion" / "p2_owner.py"),
    ]
    for value in candidates:
        if value:
            path = Path(value).resolve()
            if path.is_file():
                files.append({"path": str(path), "sha256": hashlib.sha256(
                    path.read_bytes()).hexdigest()})
    return {"files": sorted(files, key=lambda row: row["path"])}


def _store_class():
    try:
        from .state_store import PsycheStore  # type: ignore
    except ImportError as exc:
        raise RecursionRefusal(STORE_MISSING) from exc
    return PsycheStore


class P3Owner:
    """Compose the unchanged P2 owner with a frozen TEST_ONLY psychology sidecar."""

    def __init__(
        self,
        base_owner: Any,
        *,
        source: Any,
        history: Any,
        plans: Any,
        catalog: Any = None,
        compression_specs: Any = None,
        standpoints: Any = None,
        mode: str = "TEST_ONLY",
    ) -> None:
        if mode != "TEST_ONLY":
            _refuse("P3_MODE_REFUSED_BEFORE_WRITES")
        for name in ("snapshot", "validate_proposal", "realize", "actor_experience",
                     "fanin"):
            if not hasattr(base_owner, name):
                _refuse("P3_BASE_OWNER_PROTOCOL_MISSING:" + name)
        self.base_owner = base_owner
        self.mode = mode
        self._store_class = _store_class()
        base = self._base_snapshot()
        self._initial_base = base.document()
        self.source = _mapping(source, "P3_SOURCE")
        if self.source.get("grade") != GRADE:
            _refuse("P3_SOURCE_GRADE")
        source_identity = self.source.get("identity")
        if not isinstance(source_identity, Mapping):
            source_identity = self.source
        for key in ("root", "actor", "branch"):
            if source_identity.get(key) != base.document()[key]:
                _refuse("P3_SOURCE_IDENTITY:" + key)
        self.source_ref = self.source.get("source_ref") or self.source.get("base_source_ref")
        _text(self.source_ref, "P3_SOURCE_REF")
        self.source_hash = digest(self.source)
        self.registry = test_rules.make_registry(self.source_hash)
        self.history = test_rules.validate_history(
            list(history), identity=base.document(), source_hash=self.source_hash
        )
        self.catalog = _mapping(catalog or {}, "P3_CATALOG")
        self.compression_specs = _mapping(compression_specs or {}, "P3_COMPRESSION_SPECS")
        self.standpoints = self._normalize_standpoints(standpoints)
        self.plans = self._normalize_plans(plans, base)
        self._plans_by_event = {plan["event_id"]: plan for plan in self.plans}
        self.code_pins = _code_pins()
        self.config = {
            "schema": CONFIG_SCHEMA,
            "source": self.source,
            "source_hash": self.source_hash,
            "history": self.history,
            "plans": self.plans,
            "catalog": self.catalog,
            "compression_specs": self.compression_specs,
            "standpoints": self.standpoints,
            "code_pins": self.code_pins,
        }
        self.config_hash = digest(self.config)
        self._state_root = Path(base_owner.fanin.session.state_root).resolve()
        self._config_path = self._state_root / CONFIG_FILE
        self._lock_path = self._state_root / LOCK_FILE
        with self._root_lock():
            self._check_or_write_config()
        self.store = self._store_class()(
            self._state_root / STORE_FILE,
            binding={"root": base.root, "actor": base.actor, "branch": base.branch},
            registry_hash=self.registry["hash"],
            source_hash=self.source_hash,
        )

    # ------------------------------------------------------------------
    # Identity/config helpers

    def _base_snapshot(self) -> StateIdentity:
        value = self.base_owner.snapshot()
        if not isinstance(value, StateIdentity):
            _refuse("P3_BASE_SNAPSHOT_INVALID")
        return value

    @staticmethod
    def _base_doc(value: Any) -> dict:
        if isinstance(value, StateIdentity):
            return value.document()
        return _identity(value, "P3_BASE_STATE")

    def _head_hash(self) -> str:
        if not hasattr(self, "store"):
            _refuse("P3_STORE_NOT_INITIALIZED")
        head = self.store.head()
        if not isinstance(head, Mapping) or not isinstance(head.get("hash"), str):
            _refuse("P3_STORE_HEAD_INVALID")
        return _hash(head["hash"], "P3_STORE_HEAD_HASH")

    def _p3_identity(self, base: StateIdentity) -> StateIdentity:
        return StateIdentity(
            base.root, base.actor, base.branch, base.clock,
            digest({"base_state_hash": base.state_hash,
                    "psychology_head": self._head_hash(),
                    "config_hash": self.config_hash}),
        )

    def snapshot(self) -> StateIdentity:
        self._check_config()
        base = self._base_snapshot()
        if base.root != self._initial_base["root"] or base.actor != self._initial_base["actor"]:
            _refuse("P3_BASE_IDENTITY_CHANGED")
        if base.branch != self._initial_base["branch"]:
            _refuse("P3_BASE_BRANCH_CHANGED")
        return self._p3_identity(base)

    def _check_config(self) -> None:
        if not self._config_path.is_file():
            _refuse("P3_CONFIG_FILE_MISSING")
        document = _mapping(canonical_load(self._config_path), "P3_CONFIG_FILE")
        if document.get("config_hash") != self.config_hash:
            _refuse("P3_CONFIG_CHANGED")
        if document.get("config") != self.config:
            _refuse("P3_CONFIG_FILE_MISMATCH")

    def _check_or_write_config(self) -> None:
        document = {"schema": "P3_OWNER_CONFIG_FILE@1",
                    "config": self.config, "config_hash": self.config_hash}
        if self._config_path.exists():
            self._check_config()
            return
        temporary = self._state_root / (CONFIG_FILE + ".tmp")
        temporary.write_text(canonical(document) + "\n", encoding="utf-8")
        os.replace(temporary, self._config_path)

    def _root_lock(self):
        self._state_root.mkdir(parents=True, exist_ok=True)
        handle = self._lock_path.open("a")
        fcntl.flock(handle, fcntl.LOCK_EX)
        class _Lock:
            def __enter__(inner):
                return handle
            def __exit__(inner, exc_type, exc, tb):
                fcntl.flock(handle, fcntl.LOCK_UN)
                handle.close()
        return _Lock()

    def _normalize_standpoints(self, value: Any) -> list[dict]:
        if value is None:
            return []
        if isinstance(value, Mapping):
            if "permissions" in value:
                raw = [value]
            else:
                raw = list(value.values())
        elif isinstance(value, (list, tuple)):
            raw = list(value)
        else:
            _refuse("P3_STANDPOINTS_SCHEMA")
        result = []
        for item in raw:
            doc = _mapping(item, "P3_STANDPOINT")
            for key in ("root", "actor", "branch", "clock", "interlocutor_ref",
                        "role", "permissions", "source_refs", "grade", "hash"):
                if key not in doc:
                    _refuse("P3_STANDPOINT_MISSING:" + key)
            _whole_hash(doc, "P3_STANDPOINT")
            result.append(doc)
        return result

    def _normalize_plans(self, value: Any, base: StateIdentity) -> list[dict]:
        if isinstance(value, Mapping):
            if "event_id" in value and "proposal_hash" in value:
                raw = [value]
            else:
                raw = list(value.values())
        elif isinstance(value, (list, tuple)):
            raw = list(value)
        else:
            _refuse("P3_PLANS_SCHEMA")
        result = []
        seen = set()
        for item in raw:
            plan = _mapping(item, "P3_PLAN")
            for key in ("event_id", "proposal_hash", "permitted_rules",
                        "phase", "project", "counterpart", "activation_roles",
                        "relation_refs", "obligation_refs", "grade", "source_hash",
                        "registry_hash", "root", "actor", "branch", "hash"):
                if key not in plan:
                    _refuse("P3_PLAN_MISSING:" + key)
            _text(plan["event_id"], "P3_PLAN_EVENT_ID")
            _hash(plan["proposal_hash"], "P3_PLAN_PROPOSAL_HASH")
            _whole_hash(plan, "P3_PLAN")
            if plan["grade"] != GRADE:
                _refuse("P3_PLAN_GRADE")
            if (plan["source_hash"], plan["registry_hash"]) != (
                    self.source_hash, self.registry["hash"]):
                _refuse("P3_PLAN_SOURCE")
            if (plan["root"], plan["actor"], plan["branch"]) != (
                    base.root, base.actor, base.branch):
                _refuse("P3_PLAN_IDENTITY")
            if plan["permitted_rules"] != test_rules.rule_descriptors():
                _refuse("P3_PLAN_RULE_VERSION")
            if plan["phase"] not in ("FORMATION", "RECRUIT", "STABILITY"):
                _refuse("P3_PLAN_PHASE")
            if plan["event_id"] in seen:
                _refuse("P3_PLAN_DUPLICATE")
            seen.add(plan["event_id"])
            result.append(plan)
        return sorted(result, key=lambda row: row["event_id"])

    def _plan(self, proposal: EventProposal) -> dict:
        plan = self._plans_by_event.get(proposal.event_id)
        if plan is None:
            _refuse("P3_PLAN_MISSING:" + proposal.event_id)
        return plan

    def _validate_plan(self, plan: dict, proposal: EventProposal,
                       base: StateIdentity) -> dict:
        return test_rules.validate_plan(
            plan, identity=base.document(), proposal=proposal.document(),
            source_hash=self.source_hash, registry=self.registry,
        )

    def _preflight_compression(self, proposal: EventProposal,
                               base: StateIdentity) -> dict | None:
        spec = self.compression_specs.get(proposal.event_id)
        if spec is None:
            return None
        return compression_module.preflight(
            spec, identity=base.document(), proposal=proposal.document(),
            catalog=self.catalog,
        )

    def validate_proposal(self, proposal: EventProposal) -> None:
        self._check_config()
        base = self._base_snapshot()
        plan = self._plan(proposal)
        self.base_owner.validate_proposal(proposal)
        test_rules.validate_history(
            self.history, identity=base.document(), source_hash=self.source_hash
        )
        self._validate_plan(plan, proposal, base)
        self._preflight_compression(proposal, base)

    # ------------------------------------------------------------------
    # Realization and recovery

    def _operation(self, operation_id: str) -> dict | None:
        value = self.store.get_operation(operation_id)
        if value is None:
            return None
        if not isinstance(value, Mapping):
            _refuse("P3_OPERATION_RECORD_INVALID")
        return detached(value)

    def _base_operation_id(self, operation_id: str, base: StateIdentity) -> str:
        return "p3base:" + digest({
            "operation_id": operation_id,
            "root": base.root,
            "actor": base.actor,
            "branch": base.branch,
        })

    def _check_existing(self, existing: Mapping, proposal: EventProposal,
                        plan: Mapping, expected: StateIdentity) -> StateIdentity:
        if existing.get("proposal_hash") != digest(proposal.document()):
            _refuse("P3_OPERATION_PROPOSAL_MISMATCH")
        if existing.get("plan_hash") != plan["hash"]:
            _refuse("P3_OPERATION_PLAN_MISMATCH")
        stored = _identity(existing.get("expected"), "P3_OPERATION_EXPECTED")
        stored_identity = StateIdentity(**stored)
        supplied = expected.document()
        if supplied != stored:
            current = self._p3_identity(self._base_snapshot()).document()
            if supplied != current:
                # A COMPLETE operation may be replayed with #704's current after
                # identity. A non-complete operation may be recovered only when
                # the caller supplies either its original expected state or the
                # exact current combined snapshot; an arbitrary state refuses.
                if existing.get("phase") == "COMPLETE" and existing.get("result"):
                    result_after = detached(existing["result"]).get("after")
                    if result_after != supplied:
                        _refuse("P3_OPERATION_EXPECTED_MISMATCH")
                else:
                    _refuse("P3_OPERATION_EXPECTED_MISMATCH")
        return stored_identity

    def _stored_base(self, existing: Mapping) -> StateIdentity:
        if existing.get("base_before") is None:
            _refuse("P3_OPERATION_BASE_BEFORE_MISSING")
        doc = _identity(existing["base_before"], "P3_OPERATION_BASE_BEFORE")
        return StateIdentity(**doc)

    def _existing_effect(self, existing: Mapping) -> dict:
        receipt = existing.get("effects_receipt")
        if not isinstance(receipt, Mapping):
            _refuse("P3_EFFECT_RECEIPT_MISSING")
        response = receipt.get("response")
        if not isinstance(response, Mapping):
            response = receipt.get("psychological_response")
        if not isinstance(response, Mapping):
            _refuse("P3_EFFECT_RECEIPT_RESPONSE_MISSING")
        readset = receipt.get("readset")
        if not isinstance(readset, (list, tuple)):
            readset = response.get("readset", [])
        return {"records": detached(receipt.get("records", [])),
                "response": detached(response), "readset": list(readset)}

    def _psych_result(self, operation_id: str, proposal: EventProposal,
                      expected: StateIdentity, base_result: RealizedEvent,
                      effect: Mapping) -> RealizedEvent:
        projection = self._project(base_result)
        return self._result(operation_id, proposal, expected, base_result,
                            effect, projection)

    def _base_result(self, value: Any) -> RealizedEvent:
        if isinstance(value, RealizedEvent):
            return value
        doc = _mapping(value, "P3_BASE_RESULT")
        if set(doc) != {"operation_id", "proposal_hash", "before", "after",
                        "status", "objective", "accessible", "consequences",
                        "readset", "receipt_ref"}:
            _refuse("P3_BASE_RESULT_SCHEMA")
        return RealizedEvent(
            operation_id=doc["operation_id"],
            proposal_hash=doc["proposal_hash"],
            before=StateIdentity(**_identity(doc["before"], "P3_BASE_BEFORE")),
            after=StateIdentity(**_identity(doc["after"], "P3_BASE_AFTER")),
            status=doc["status"],
            objective=detached(doc["objective"]),
            accessible=detached(doc["accessible"]),
            consequences=detached(doc["consequences"]),
            readset=tuple(doc["readset"]),
            receipt_ref=doc["receipt_ref"],
        )

    def _run_base(self, operation_id: str, proposal: EventProposal,
                  base: StateIdentity) -> RealizedEvent:
        base_operation_id = self._base_operation_id(operation_id, base)
        try:
            result = self.base_owner.realize(base_operation_id, proposal, base)
        except RecursionRefusal as exc:
            if "AMBIGUOUS" in str(exc) or "PENDING" in str(exc):
                raise RecursionRefusal("P3_AMBIGUOUS_PRIOR_BASE_OPERATION_HOLD") from exc
            raise
        if result.before.root != base.root or result.before.actor != base.actor:
            _refuse("P3_BASE_RESULT_IDENTITY")
        if result.before.branch != base.branch or result.before.clock != base.clock:
            _refuse("P3_BASE_RESULT_IDENTITY")
        self.store.save_world(operation_id, result.document())
        return result

    def _context(self, plan: Mapping, base_result: RealizedEvent) -> dict:
        base = base_result.after
        access = base_result.accessible if isinstance(base_result.accessible, Mapping) else {}
        observed = access.get("status") == "OBSERVED" and access.get("actor_ref") == base.actor
        relation_refs = list(plan.get("relation_refs") or [])
        relation_ref = plan.get("relation_ref")
        if relation_ref is None and len(relation_refs) == 1:
            relation_ref = relation_refs[0]
        material = None
        consequences = base_result.consequences if isinstance(base_result.consequences, Mapping) else {}
        immediate = consequences.get("immediate_response")
        if isinstance(immediate, Mapping) and immediate.get("objective_material_eligible") in (True, False, None):
            material = immediate.get("objective_material_eligible")
        body = {
            "root": base.root, "actor": base.actor, "branch": base.branch,
            "clock": base.clock, "project": plan["project"],
            "counterpart": plan["counterpart"],
            "interlocutor_role": plan.get("interlocutor_role"),
            "relation_ref": relation_ref,
            "obligation_refs": list(plan.get("obligation_refs") or []),
            "actor_observed": bool(observed), "material_eligible": material,
            "source_refs": [self.source_hash], "grade": GRADE,
        }
        body["hash"] = digest(body)
        return body

    def _standpoint(self, base: StateIdentity) -> dict:
        for item in self.standpoints:
            if (item.get("root"), item.get("actor"), item.get("branch")) != (
                    base.root, base.actor, base.branch):
                continue
            body = detached(item)
            if body.get("clock") != base.clock:
                body["clock"] = base.clock
                body["hash"] = digest({k: v for k, v in body.items() if k != "hash"})
            return body
        body = {
            "root": base.root, "actor": base.actor, "branch": base.branch,
            "clock": base.clock, "interlocutor_ref": "UNCONFIGURED",
            "role": "UNCONFIGURED", "permissions": [],
            "source_refs": [self.source_hash], "grade": GRADE,
        }
        body["hash"] = digest(body)
        return body

    def _project(self, base_result: RealizedEvent) -> dict:
        base = base_result.after
        experience = base_result.accessible
        public = self.base_owner.fanin.view()
        if not isinstance(experience, Mapping) or not isinstance(public, Mapping):
            _refuse("P3_PROJECTION_INPUT")
        standpoint = self._standpoint(base)
        return projections.project_views(
            identity=base.document(),
            actor_experience=experience,
            experience_binding={
                "root": base.root, "actor": base.actor, "branch": base.branch,
                "clock": base.clock, "experience_hash": digest(experience),
            },
            public_view=public,
            public_binding={
                "root": base.root, "actor": base.actor, "branch": base.branch,
                "clock": base.clock, "view_hash": digest(public),
            },
            standpoint=standpoint,
        )

    def _effect(self, operation_id: str, proposal: EventProposal, plan: dict,
                base_result: RealizedEvent) -> tuple[dict, dict, dict]:
        records = self.store.query(
            project=plan["project"], counterpart=plan["counterpart"],
            as_of=base_result.after.clock,
        )
        context = self._context(plan, base_result)
        activated = projections.activate(
            records, identity=base_result.after.document(), context=context,
            registry=self.registry,
        )
        effect = test_rules.evaluate_event(
            identity=base_result.after.document(), proposal=proposal.document(),
            realized=base_result.document(), history=self.history,
            records=records, plan=plan, source_hash=self.source_hash,
            registry=self.registry, activation=activated,
        )
        event = (base_result.objective.get("event") or {}) if isinstance(
            base_result.objective, Mapping) else {}
        event_binding = {
            "root": base_result.after.root, "actor": base_result.after.actor,
            "branch": base_result.after.branch, "clock": base_result.after.clock,
            "event_id": event.get("e1_event_id", ""),
            "event_hash": event.get("e1_event_hash", ""),
            "e1_event_id": event.get("e1_event_id", ""),
            "e1_event_hash": event.get("e1_event_hash", ""),
            "action_event_id": event.get("action_event_id", ""),
            "action_event_hash": event.get("action_event_hash", ""),
            "access_status": base_result.accessible.get("status", ""),
            "access_hash": digest(base_result.accessible),
            "base_receipt_ref": base_result.receipt_ref,
        }
        self.store.commit_effects(
            operation_id, records=effect["records"], response=effect["response"],
            event_binding=event_binding,
        )
        if proposal.event_id in self.compression_specs:
            # Optional evidence only. The compression worker's current return
            # is REVISE; no positive compression claim is made here.
            effect["compression"] = compression_module.bind(
                self.compression_specs[proposal.event_id],
                identity=base_result.before.document(),
                proposal=proposal.document(), catalog=self.catalog,
                realized=base_result.document(),
            )
        return effect, activated, event_binding

    def _result(self, operation_id: str, proposal: EventProposal,
                expected: StateIdentity, base_result: RealizedEvent,
                effect: Mapping, projection: Mapping) -> RealizedEvent:
        base = self._base_snapshot()
        if (base.root, base.actor, base.branch, base.clock) != (
                base_result.after.root, base_result.after.actor,
                base_result.after.branch, base_result.after.clock):
            _refuse("P3_BASE_STATE_CHANGED_AFTER_EFFECT")
        after = self._p3_identity(base)
        consequences = detached(base_result.consequences)
        consequences.update({
            "durable_psychological_transition": "MISSING_RULE",
            "test_only_psychological": detached(effect["response"]),
            "test_only_user_surface": detached(projection["user"]),
            "test_only_actor_surface": detached(projection["actor"]),
            "native_action": "NOT_ISSUED_BY_P3_RULE",
        })
        if "compression" in effect:
            consequences["test_only_compression_evidence"] = detached(
                effect["compression"])
        readset = list(dict.fromkeys(
            list(base_result.readset) + list(effect.get("readset", []))
        ))
        return RealizedEvent(
            operation_id=operation_id, proposal_hash=digest(proposal.document()),
            before=expected, after=after, status=base_result.status,
            objective=detached(base_result.objective),
            accessible=detached(projection["actor"]),
            consequences=consequences, readset=tuple(readset),
            receipt_ref="P3_PSYCH:" + str(effect["response"].get("hash", operation_id)),
        )

    def _complete(self, operation_id: str, result: RealizedEvent) -> RealizedEvent:
        self.store.finish(operation_id, result.document())
        return result

    def _existing_result(self, existing: Mapping) -> RealizedEvent:
        value = existing.get("result")
        if value is None:
            _refuse("P3_COMPLETE_RESULT_MISSING")
        return self._base_result(value)

    def realize(self, operation_id: str, proposal: EventProposal,
                expected: StateIdentity) -> RealizedEvent:
        _text(operation_id, "P3_OPERATION_ID")
        self._check_config()
        with self._root_lock():
            existing = self._operation(operation_id)
            if existing is None:
                base = self._base_snapshot()
                expected_doc = _identity(expected.document(), "P3_EXPECTED")
                if (expected_doc["root"], expected_doc["actor"], expected_doc["branch"],
                        expected_doc["clock"]) != (base.root, base.actor, base.branch, base.clock):
                    _refuse("P3_EXPECTED_IDENTITY_MISMATCH")
                if expected_doc["state_hash"] != self._p3_identity(base).state_hash:
                    _refuse("P3_EXPECTED_STATE_MISMATCH")
                plan = self._plan(proposal)
                self.base_owner.validate_proposal(proposal)
                test_rules.validate_history(
                    self.history, identity=base.document(), source_hash=self.source_hash
                )
                self._validate_plan(plan, proposal, base)
                self._preflight_compression(proposal, base)
                pending = self.store.pending()
                if pending:
                    _refuse("P3_OWNER_HAS_PENDING_OPERATION")
                self.store.reserve(
                    operation_id, proposal_hash=digest(proposal.document()),
                    expected=expected.document(), plan_hash=plan["hash"],
                    base_before=base.document(), psyche_before=self.store.head(),
                    plan=plan,
                )
                base_result = self._run_base(operation_id, proposal, base)
                effect, _activated, _binding = self._effect(
                    operation_id, proposal, plan, base_result
                )
                result = self._psych_result(operation_id, proposal, expected,
                                            base_result, effect)
                return self._complete(operation_id, result)

            plan = self._plan(proposal)
            stored_expected = self._check_existing(existing, proposal, plan, expected)
            stored_base = self._stored_base(existing)
            test_rules.validate_history(
                self.history, identity=stored_base.document(),
                source_hash=self.source_hash,
            )
            self._validate_plan(plan, proposal, stored_base)
            phase = existing.get("phase")
            if phase == "COMPLETE":
                result = self._existing_result(existing)
                if self.snapshot().document() != result.after.document():
                    _refuse("P3_REPLAY_STATE_MISMATCH")
                return result
            if phase == "PSYCH_COMMITTED":
                if existing.get("result"):
                    result = self._existing_result(existing)
                    self.store.finish(operation_id, result.document())
                    return result
                base_result = self._base_result(existing.get("base_result"))
                result = self._psych_result(
                    operation_id, proposal, stored_expected, base_result,
                    self._existing_effect(existing),
                )
                return self._complete(operation_id, result)
            if phase == "WORLD_COMMITTED":
                base_result = self._base_result(existing.get("base_result"))
                effect, _activated, _binding = self._effect(
                    operation_id, proposal, plan, base_result
                )
                result = self._psych_result(
                    operation_id, proposal, stored_expected, base_result, effect
                )
                return self._complete(operation_id, result)
            if phase == "PREPARED":
                # The saved base_before is authoritative for a completed base
                # reservation. P2.realize replays that exact base receipt; it
                # never receives the later state as a new expected state.
                base_result = self._run_base(operation_id, proposal, stored_base)
                effect, _activated, _binding = self._effect(
                    operation_id, proposal, plan, base_result
                )
                result = self._psych_result(
                    operation_id, proposal, stored_expected, base_result, effect
                )
                return self._complete(operation_id, result)
            _refuse("P3_OPERATION_PHASE_UNKNOWN")

    def close(self) -> None:
        if hasattr(self, "store"):
            self.store.close()
        self.base_owner.close()


def canonical_load(path: Path) -> Any:
    """Read a canonical JSON file without introducing a second state owner."""
    import json
    return json.loads(path.read_text(encoding="utf-8"))


__all__ = ["CONFIG_FILE", "CONFIG_SCHEMA", "P3Owner", "STORE_FILE", "STORE_MISSING"]
