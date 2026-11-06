"""TEST_ONLY B1 CAN008/CAN011 fixture driven through the received DevelopmentOwner ABI.

This is a compatibility probe, not native science and not a production writer.
It adapts the frozen B1 ``bfirst.py`` SQLite transaction to the #704
``DevelopmentOwner`` protocol. B1 still owns response evaluation, the separate
CAN011 destination court, the mediator record and the later recruit read.
The adapter adds only root/branch/actor identity, operation custody, and the
``EventProposal``/``RealizedEvent`` mapping.
"""
from __future__ import annotations

import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any, Mapping

_HERE = Path(__file__).resolve()
_ENGINE_DEFAULT = (
    _HERE.parents[3]
    / "WORKER_RETURNS"
    / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
)
_ENGINE = Path(os.environ.get("SOROK_ENGINE_PATH", str(_ENGINE_DEFAULT)))
if _ENGINE.is_dir() and str(_ENGINE) not in sys.path:
    sys.path.insert(0, str(_ENGINE))

from developmental_recursion.contracts import (  # noqa: E402
    EventProposal,
    RealizedEvent,
    RecursionRefusal,
    StateIdentity,
    canonical,
    detached,
    digest,
)

GRADE = "TEST_ONLY_B1_DEVELOPMENT_OWNER_ADAPTER_NOT_NATIVE"
OPERATION = "B1_RESPOND"
B1_BLOB = "94ffc52847e4c8ae760212d1bc8543594ba793fa"
B1_SHA256 = "478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3"
_B1_DEFAULT = _HERE.parent / "vendor" / "B1" / "bfirst.py"
_CIRCUMSTANCES = frozenset(
    {"world_ref", "objective_occurrence", "project", "power_ref", "offers", "interrupted"}
)
_META_DDL = """
CREATE TABLE IF NOT EXISTS b1_owner_meta (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  root TEXT NOT NULL,
  branch TEXT NOT NULL,
  actor TEXT NOT NULL,
  source_ref TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS b1_source (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  body TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS b1_operations (
  id TEXT PRIMARY KEY,
  proposal_hash TEXT NOT NULL,
  before_state TEXT NOT NULL,
  status TEXT NOT NULL,
  result TEXT,
  refusal TEXT
);
"""


def _load_b1(path: Path | str | None = None):
    path = Path(path or os.environ.get("SOROK_B1_PATH", str(_B1_DEFAULT))).resolve()
    if not path.is_file():
        raise RecursionRefusal("B1_SOURCE_MISSING:" + str(path))
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != B1_SHA256:
        raise RecursionRefusal("B1_PINNED_SOURCE_MISMATCH:" + actual)
    name = "b1_pinned_bfirst"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RecursionRefusal("B1_SOURCE_LOAD_FAILED")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _text(value: Any, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecursionRefusal(code)
    return value


def _state_from_document(value: Any) -> StateIdentity:
    if not isinstance(value, Mapping):
        raise RecursionRefusal("B1_STATE_DOCUMENT_INVALID")
    return StateIdentity(
        value["root"], value["actor"], value["branch"], value["clock"], value["state_hash"]
    )


def _result_from_document(value: Mapping[str, Any]) -> RealizedEvent:
    before = _state_from_document(value["before"])
    after = _state_from_document(value["after"])
    return RealizedEvent(
        operation_id=value["operation_id"],
        proposal_hash=value["proposal_hash"],
        before=before,
        after=after,
        status=value["status"],
        objective=value["objective"],
        accessible=value["accessible"],
        consequences=value["consequences"],
        readset=tuple(value["readset"]),
        receipt_ref=value["receipt_ref"],
    )


class B1Owner:
    """A B1 actor fixture that satisfies ``DevelopmentOwner``.

    ``root`` and ``branch`` are adapter custody labels, not B1-native fields.
    The actor is B1's ``child``. The source reference binds the immutable
    synthetic prehistory and the two B1 TEST_ONLY rule hashes.
    """

    def __init__(
        self,
        db_path: str | os.PathLike[str],
        *,
        root: str,
        branch: str = "main",
        actor: str = "child",
        b1_path: Path | str | None = None,
        journal_only: bool = False,
        initial: Mapping[str, Any] | None = None,
    ) -> None:
        self.b1 = _load_b1(b1_path)
        self.root = _text(root, "B1_ROOT_REQUIRED")
        self.branch = _text(branch, "B1_BRANCH_REQUIRED")
        self.actor = _text(actor, "B1_ACTOR_REQUIRED")
        self.journal_only = bool(journal_only)
        if initial is None:
            initial = self.b1.initialize(self.b1.prehistory())
        initial = detached(initial)
        if initial.get("actor_id") != self.actor:
            raise RecursionRefusal("B1_INITIAL_ACTOR_MISMATCH")

        fixture = {
            "schema": "B1_OWNER_SOURCE@1",
            "initial_state": initial,
            "response_rule_hash": self.b1.RESPONSE_RULE["hash"],
            "update_rule_hash": self.b1.UPDATE_RULE["hash"],
            "registry_hash": self.b1.REGISTRY["hash"],
        }
        self.source_ref = "B1_FIXTURE:" + self.b1.digest(fixture)
        self._fixture = fixture

        path = Path(db_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        new = (not path.exists()) or path.stat().st_size == 0
        self.path = path
        self.store = self.b1.Store(path, initial if new else None)
        self.db = self.store.db
        self.db.executescript(_META_DDL)
        if new:
            self.db.execute(
                "INSERT INTO b1_owner_meta VALUES (1,?,?,?,?)",
                (self.root, self.branch, self.actor, self.source_ref),
            )
            self.db.execute(
                "INSERT INTO b1_source VALUES (1,?)", (canonical(self._fixture),)
            )
            self.db.commit()
        self._verify_source()

    # ------------------------------------------------------------------
    # DevelopmentOwner surface

    def snapshot(self) -> StateIdentity:
        self._verify_source()
        state = self._state()
        return StateIdentity(
            self.root,
            self.actor,
            self.branch,
            self._clock(state),
            self.b1.digest(state),
        )

    def validate_proposal(self, proposal: EventProposal) -> None:
        event = self._check_proposal(proposal)
        current = self.snapshot()
        if proposal.event_time <= current.clock:
            raise RecursionRefusal("B1_EVENT_CLOCK_NOT_FUTURE")
        state = self._state()
        try:
            self.b1.propose(state, self.b1.sealed(self._asdict(event)))
        except self.b1.Refusal as exc:
            raise RecursionRefusal("B1_PROPOSAL_REFUSED:" + str(exc)) from exc

    def realize(
        self, operation_id: str, proposal: EventProposal, expected: StateIdentity
    ) -> RealizedEvent:
        lock_path = Path(str(self.path) + ".b1owner.lock")
        with lock_path.open("a") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            try:
                return self._realize(operation_id, proposal, expected)
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)

    def close(self) -> None:
        self.store.close()

    def __enter__(self) -> "B1Owner":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Source, identity and operation custody

    def _state(self) -> dict:
        try:
            state = self.store.state()
        except Exception as exc:  # noqa: BLE001 - B1 exposes no typed read error
            raise RecursionRefusal("B1_CHECKPOINT_UNAVAILABLE:" + type(exc).__name__) from exc
        if not isinstance(state, dict) or state.get("schema") != self.b1.SCHEMA:
            raise RecursionRefusal("B1_CHECKPOINT_SCHEMA_INVALID")
        return state

    def _verify_source(self) -> None:
        meta = self.db.execute(
            "SELECT root, branch, actor, source_ref FROM b1_owner_meta WHERE id=1"
        ).fetchone()
        if meta != (self.root, self.branch, self.actor, self.source_ref):
            raise RecursionRefusal("B1_OWNER_BINDING_MISMATCH")
        row = self.db.execute("SELECT body FROM b1_source WHERE id=1").fetchone()
        if row is None:
            raise RecursionRefusal("B1_SOURCE_IDENTITY_MISSING")
        try:
            fixture = json.loads(row[0])
        except (TypeError, ValueError) as exc:
            raise RecursionRefusal("B1_SOURCE_IDENTITY_MALFORMED") from exc
        if "B1_FIXTURE:" + self.b1.digest(fixture) != self.source_ref:
            raise RecursionRefusal("B1_SOURCE_IDENTITY_TAMPERED")
        initial = fixture.get("initial_state") or {}
        state = self._state()
        for key in ("schema", "actor_id", "capabilities", "epistemic", "history", "project"):
            if canonical(state.get(key)) != canonical(initial.get(key)):
                raise RecursionRefusal("B1_SOURCE_OR_STATE_TAMPERED:" + key)

    def _clock(self, state: Mapping[str, Any]) -> int:
        values = [0]
        values.extend(int(row["time"]) for row in state.get("history", ()))
        values.extend(
            int(row["effective_from"])
            for row in state.get("middle", ())
            if row.get("effective_from") is not None
        )
        values.extend(int(row["time"]) for row in state.get("responses", ()))
        return max(values)

    def _check_proposal(self, proposal: EventProposal) -> Any:
        if not isinstance(proposal, EventProposal):
            raise RecursionRefusal("B1_PROPOSAL_NOT_EVENT_PROPOSAL")
        if proposal.operation != OPERATION:
            raise RecursionRefusal("B1_OPERATION_NOT_QUALIFIED:" + proposal.operation)
        if proposal.source_refs != (self.source_ref,):
            raise RecursionRefusal("B1_SOURCE_REF_MISMATCH")
        if proposal.interval is not None:
            raise RecursionRefusal("B1_INTERVAL_NOT_SUPPORTED")
        circumstances = proposal.circumstances
        if not isinstance(circumstances, Mapping) or set(circumstances) != {"b1"}:
            raise RecursionRefusal("B1_CIRCUMSTANCES_SCHEMA")
        body = circumstances["b1"]
        if not isinstance(body, Mapping) or set(body) != _CIRCUMSTANCES:
            raise RecursionRefusal("B1_CIRCUMSTANCES_SCHEMA")
        offers = body["offers"]
        if not isinstance(offers, (list, tuple)) or not offers:
            raise RecursionRefusal("B1_OFFERS_SCHEMA")
        normalized = []
        for offer in offers:
            if not isinstance(offer, (list, tuple)) or len(offer) != 3:
                raise RecursionRefusal("B1_OFFERS_SCHEMA")
            counterpart = _text(offer[0], "B1_OFFER_COUNTERPART")
            words = _text(offer[1], "B1_OFFER_WORDS")
            plan = _text(offer[2], "B1_OFFER_PLAN")
            normalized.append((counterpart, words, plan))
        participants = ("child",) + tuple(offer[0] for offer in normalized)
        if proposal.participants != participants:
            raise RecursionRefusal("B1_PARTICIPANTS_MISMATCH")
        if not isinstance(body["interrupted"], bool):
            raise RecursionRefusal("B1_INTERRUPTED_SCHEMA")
        event = self.b1.Event(
            event_id=proposal.event_id,
            actor_id="child",
            time=proposal.event_time,
            world_ref=_text(body["world_ref"], "B1_WORLD_REF"),
            objective_occurrence=_text(body["objective_occurrence"], "B1_OCCURRENCE"),
            project=_text(body["project"], "B1_PROJECT"),
            relation_refs=tuple("relation:child:" + item[0] for item in normalized),
            power_ref=_text(body["power_ref"], "B1_POWER_REF"),
            offers=tuple(normalized),
            interrupted=body["interrupted"],
            admission_grade="ADMITTED_SYNTHETIC_FIXTURE_ONLY",
            provenance="B1_AUTHORED_SOURCEFREE",
        )
        return event

    @staticmethod
    def _asdict(event: Any) -> dict:
        from dataclasses import asdict

        return asdict(event)

    def _realize(
        self, operation_id: str, proposal: EventProposal, expected: StateIdentity
    ) -> RealizedEvent:
        operation_id = _text(operation_id, "B1_OPERATION_ID_REQUIRED")
        self._verify_source()
        proposal_hash = digest(proposal.document())
        expected_document = canonical(expected.document())
        row = self.db.execute(
            "SELECT proposal_hash, before_state, status, result, refusal "
            "FROM b1_operations WHERE id=?",
            (operation_id,),
        ).fetchone()
        if row is not None:
            if row[0] != proposal_hash or row[1] != expected_document:
                raise RecursionRefusal("B1_OPERATION_REUSE_MISMATCH")
            if row[2] == "RESERVED":
                raise RecursionRefusal("B1_AMBIGUOUS_PRIOR_OPERATION_HOLD")
            if row[2] == "REFUSED":
                raise RecursionRefusal("B1_PRIOR_REFUSAL:" + (row[4] or "UNKNOWN"))
            stored = _result_from_document(json.loads(row[3]))
            if self.snapshot() != stored.after:
                raise RecursionRefusal("B1_REPLAY_STATE_MISMATCH")
            return stored

        current = self.snapshot()
        if current != expected:
            raise RecursionRefusal("B1_STALE_ROOT_BRANCH_CLOCK_OR_STATE")
        event = self._check_proposal(proposal)
        if proposal.event_time <= current.clock:
            raise RecursionRefusal("B1_EVENT_CLOCK_NOT_FUTURE")
        self.validate_proposal(proposal)

        self.db.execute(
            "INSERT INTO b1_operations VALUES (?,?,?,'RESERVED',NULL,NULL)",
            (operation_id, proposal_hash, expected_document),
        )
        self.db.commit()

        admitted = self.store.admit_fixture(event)
        before_state = self._state()
        response = self.b1.propose(before_state, admitted)
        permission = self.b1.TestOnlyCAN011Owner.permission(before_state, response)
        owner = self.b1.TestOnlyCAN011Owner([permission["hash"]])
        receipt = self.store.commit(
            admitted, response, owner, permission, journal_only=self.journal_only
        )
        if receipt.get("status") != "COMMITTED":
            reason = str(receipt.get("reason", "UNKNOWN"))
            self.db.execute(
                "UPDATE b1_operations SET status='REFUSED', refusal=? WHERE id=?",
                (reason, operation_id),
            )
            self.db.commit()
            raise RecursionRefusal("B1_TRANSACTION_REFUSED:" + reason)

        after_state = self._state()
        after = StateIdentity(
            self.root,
            self.actor,
            self.branch,
            self._clock(after_state),
            self.b1.digest(after_state),
        )
        if self.journal_only:
            status = "IMMEDIATE_ONLY"
        elif response["target_proposals"] or response["practical_activity"]:
            status = "REALIZED"
        else:
            status = "NO_CHANGE"
        mediator_ids = [row["middle_state_id"] for row in after_state["middle"]]
        mediator_records = [
            row["middle_state_record_hash"] for row in after_state["middle"]
        ]
        result = RealizedEvent(
            operation_id=operation_id,
            proposal_hash=proposal_hash,
            before=expected,
            after=after,
            status=status,
            objective={
                "grade": GRADE,
                "event": admitted,
                "response": response,
                "joint_receipt": receipt,
                "before_state_hash": self.b1.digest(before_state),
                "after_state_hash": self.b1.digest(after_state),
            },
            accessible={
                "schema": "B1_ACTOR_ACCESSIBLE_RESPONSE@1",
                "grade": GRADE,
                "actor": self.actor,
                "status": response["status"],
                "actor_surface": response["actor_surface"],
                "uptake": response["uptake"],
                "memory_formation": "TEST_ONLY_FIXTURE_NOT_NATIVE",
                "native_science": "NOT_ISSUED",
            },
            consequences={
                "grade": GRADE,
                "durable_psychological_transition": "TEST_ONLY_B1_V3MS_MEDIATOR",
                "native_science": "NOT_ISSUED",
                "journal_only": self.journal_only,
                "middle_state_ids": mediator_ids,
                "middle_state_record_hashes": mediator_records,
                "recruited": response["recruited"],
                "practical_activity": response["practical_activity"],
                "target_proposal_count": len(response["target_proposals"]),
                "response_status": response["status"],
                "joint_status": receipt["status"],
                "source_rule_ids": [
                    self.b1.RESPONSE_RULE["authority_id"],
                    self.b1.UPDATE_RULE["authority_id"],
                ],
            },
            readset=tuple(
                [self.source_ref, admitted["hash"]] + list(response["recruited"])
            ),
            receipt_ref="B1_JOINT:" + receipt["hash"],
        )
        self.db.execute(
            "UPDATE b1_operations SET status='COMPLETE', result=? WHERE id=?",
            (canonical(result.document()), operation_id),
        )
        self.db.commit()
        return result

    # ------------------------------------------------------------------
    # Probe helpers

    def state(self) -> dict:
        self._verify_source()
        return self._state()

    def checkpoint(self) -> dict:
        row = self.db.execute("SELECT body FROM checkpoint WHERE id=1").fetchone()
        if row is None:
            raise RecursionRefusal("B1_CHECKPOINT_MISSING")
        return json.loads(row[0])


__all__ = [
    "B1_BLOB",
    "B1_SHA256",
    "B1Owner",
    "GRADE",
    "OPERATION",
]
