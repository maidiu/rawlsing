"""Adapter to the accepted S47 actor/world owner, at its TEST_ONLY scope.

Callers supply the case, source and permitted participants. The shared engine
does not select a workshop, actor or developmental response. P2 has no native
operation-id recovery, so interrupted writes remain ambiguous and fail closed.
"""
from __future__ import annotations

from dataclasses import asdict
import fcntl
import json
from pathlib import Path
import sqlite3
import sys
from typing import Any, Mapping

from .contracts import (
    EventProposal, RealizedEvent, RecursionRefusal, StateIdentity,
    canonical, detached, digest,
)
from .supporting_actor import (
    assert_no_private_leak, record_supporting_participation,
    resolve_participants, verify_supporting_participation,
)

MATERIAL_FACT_READ_SCHEMA = "SOROK_P2_MATERIAL_FACT_READ@1"
MATERIAL_FACT_WRITE_SCHEMA = "SOROK_P2_MATERIAL_FACT_WRITE@1"
MATERIAL_FACT_GRADE = "SOURCEFREE_MATERIAL_FACT"
MATERIAL_FACT_BINDING_FIELDS = frozenset({"root", "branch", "epoch", "source"})
MATERIAL_FACT_SLOTS = frozenset({
    "p6_household", "p6_dwelling", "p6_employment", "p6_historical_period",
})
PSYCH_RECORD_FIELDS = frozenset({
    "record_id", "counterpart", "effective_from", "causal_parents",
    "registry_hash", "rule_id", "rule_version", "rule_hash",
    "permitted_rules", "project", "psyche_before", "psyche_after",
    "response_hash", "receipt_hash",
})
PSYCH_RECORD_KINDS = frozenset({
    "MEDIATOR", "TENSION", "PRACTICE",
    "V3MS_MEDIATOR", "V3MS_TENSION", "V3MS_PRACTICE",
})


def material_fact_source(document: Mapping[str, Any]) -> str:
    """Content address of a bounded material fact, excluding its binding."""
    return digest({key: value for key, value in document.items()
                   if key not in MATERIAL_FACT_BINDING_FIELDS})


def _copied_prefix_equal(store, child: str, parent: str, fork_clock: int,
                         root_counts: Any, root_hash: Any) -> bool:
    """Verify the fork-time copied prefix and its recorded root hash."""
    db = getattr(store, "db", None)
    branch_lookup = getattr(store, "_branch", None)
    if db is None or not callable(branch_lookup):
        return False
    if not isinstance(root_counts, Mapping) or not isinstance(root_hash, str):
        return False
    try:
        if branch_lookup(parent) is None:
            return False
    except Exception:
        return False
    tables = (
        ("episode", "seq,hash", True),
        ("world_event", "seq,hash", True),
        ("perception", "seq,event_id,actor_id", False),
        ("checkpoint", "seq,hash", True),
    )
    copied_hashes = []
    try:
        for table, columns, has_hash in tables:
            count = root_counts.get(table)
            if type(count) is not int or count < 0:
                return False
            parent_rows = [tuple(row) for row in db.execute(
                f"SELECT {columns} FROM {table} WHERE branch_id=? "
                "ORDER BY seq LIMIT ?",
                (parent, count))]
            child_rows = [tuple(row) for row in db.execute(
                f"SELECT {columns} FROM {table} WHERE branch_id=? "
                "ORDER BY seq LIMIT ?",
                (child, count))]
            if parent_rows != child_rows:
                return False
            if has_hash:
                copied_hashes.extend(row[1] for row in child_rows)
    except Exception:
        return False
    expected = digest({"parent": parent, "fork_clock": fork_clock,
                       "hashes": sorted(copied_hashes)})
    return expected == root_hash


def branch_is_ancestor(session, branch: Any, epoch: Any = None) -> bool:
    """Return true when branch is the current branch or a verified C12 ancestor.

    A C12 fork copies checkpoint rows up to its fork clock. A material fact
    written on an ancestor is therefore valid provenance on a descendant only
    when its epoch is not later than every copied fork edge leading here.
    """
    current = session.branch_id
    if branch == current:
        return True
    if not isinstance(branch, str) or not branch:
        return False
    if (isinstance(epoch, bool) or not isinstance(epoch, int)
            or epoch < 0):
        return False
    product = getattr(session, "product", None)
    store = getattr(product, "store", None)
    if store is None or not hasattr(store, "branch"):
        return False
    validator = getattr(session, "_lineage_result", None)
    if callable(validator):
        try:
            lineage = validator()
        except Exception:
            return False
        if not isinstance(lineage, Mapping) or not lineage.get("ok"):
            return False
    prefix_check = getattr(store, "inherits_verified_prefix", None)
    if callable(prefix_check):
        try:
            if not prefix_check(current, branch):
                return False
        except Exception:
            return False
    seen = set()
    while current not in seen:
        seen.add(current)
        try:
            row = store.branch(current)
        except Exception:
            return False
        if not isinstance(row, Mapping):
            return False
        if current == branch:
            return True
        fork_clock = row.get("fork_clock")
        if (isinstance(fork_clock, bool) or not isinstance(fork_clock, int)
                or fork_clock < epoch):
            return False
        parent = row.get("parent_branch_id")
        if not isinstance(parent, str) or not parent or parent == "root":
            return False
        if not _copied_prefix_equal(store, current, parent, fork_clock,
                                     row.get("root_counts"),
                                     row.get("root_hash")):
            return False
        current = parent
    return False


def validate_material_fact(document: Any, *, root: str, branch: str,
                           world_clock: int) -> dict:
    """Validate the bounded world-material envelope, never a psyche record."""
    if not isinstance(document, Mapping):
        raise RecursionRefusal("P2_MATERIAL_FACT_SCHEMA")
    fact = detached(document)
    if (set(fact) & PSYCH_RECORD_FIELDS) or fact.get("kind") in PSYCH_RECORD_KINDS:
        raise RecursionRefusal("P2_MATERIAL_FACT_PSYCH_RECORD_REFUSED")
    if not isinstance(fact.get("schema"), str) or not fact["schema"].strip():
        raise RecursionRefusal("P2_MATERIAL_FACT_SCHEMA")
    if not isinstance(fact.get("grade"), str) or not fact["grade"].strip():
        raise RecursionRefusal("P2_MATERIAL_FACT_GRADE")
    if fact.get("root") != root or fact.get("branch") != branch:
        raise RecursionRefusal("P2_MATERIAL_FACT_ROOT_OR_BRANCH_MISMATCH")
    epoch = fact.get("epoch")
    if (isinstance(epoch, bool) or not isinstance(epoch, int)
            or epoch < 0 or epoch > world_clock):
        raise RecursionRefusal("P2_MATERIAL_FACT_EPOCH_INVALID")
    source = fact.get("source")
    if not isinstance(source, str) or len(source) != 64:
        raise RecursionRefusal("P2_MATERIAL_FACT_SOURCE_INVALID")
    try:
        int(source, 16)
    except ValueError as exc:
        raise RecursionRefusal("P2_MATERIAL_FACT_SOURCE_INVALID") from exc
    if material_fact_source(fact) != source:
        raise RecursionRefusal("P2_MATERIAL_FACT_SOURCE_MISMATCH")
    return fact


def write_material_fact(session, *, slot: str, document: Mapping[str, Any]) -> dict:
    """Write one bounded material fact through the actual S47/P2 checkpoint."""
    if slot not in MATERIAL_FACT_SLOTS:
        raise RecursionRefusal("P2_MATERIAL_FACT_SLOT_INVALID")
    root = session.read_root()["root_hash"]
    world = session.world()
    fact = validate_material_fact(document, root=root, branch=session.branch_id,
                                  world_clock=world.clock)
    status = "UNCHANGED"
    if world.resources.get(slot) != fact:
        world.resources[slot] = fact
        session.product._checkpoint(session.branch_id, world.clock, world)
        status = "WRITTEN"
    return {
        "schema": MATERIAL_FACT_WRITE_SCHEMA,
        "grade": MATERIAL_FACT_GRADE,
        "status": status,
        "slot": slot,
        "root": root,
        "branch": session.branch_id,
        "clock": world.clock,
        "epoch": fact["epoch"],
        "source": fact["source"],
        "world_hash": digest(world.snapshot()),
    }


def load_p2():
    repo = Path(__file__).resolve().parents[3]
    package = repo / "WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1"
    if not (package / "p2_product_fanin/integration.py").is_file():
        raise RecursionRefusal("P2_SOURCE_MISSING")
    if str(package) not in sys.path:
        sys.path.insert(0, str(package))
    from p2_product_fanin.integration import P2ProductFanin
    return P2ProductFanin


class P2Owner:
    grade = "TEST_ONLY_S47_OWNER_NOT_NATIVE_DEVELOPMENTAL_SCIENCE"

    def __init__(self, fanin, *, case: Mapping, source: Mapping,
                 participants: tuple[str, ...]):
        self.fanin = fanin
        self.case = detached(case)
        self.source = detached(source)
        self.participants = tuple(participants)
        self.source_ref = "P2_INPUT:" + digest({"case": self.case, "source": self.source})
        root = fanin.session.read_root()
        root_ids = tuple(root["actor_ids"])
        resolve_participants(fanin.session, self.participants)
        if root_ids[0] not in self.participants:
            raise RecursionRefusal("P2_FOCAL_PARTICIPANT_REQUIRED")
        self.actor = root_ids[0]
        self.db = sqlite3.connect(Path(fanin.session.state_root) / "recursion_owner.sqlite")
        self.db.execute("CREATE TABLE IF NOT EXISTS operations "
                        "(id TEXT PRIMARY KEY, proposal TEXT NOT NULL, "
                        "before_state TEXT NOT NULL, result TEXT)")
        self.db.execute("CREATE TABLE IF NOT EXISTS binding (id INTEGER PRIMARY KEY, value TEXT)")
        # The binding is the original root/branch/source invariant over the
        # root actor IDs. Declared owner participants are validated live at
        # construction and per proposal; they are not a second invariant that
        # can lock an ordinary P2/P3 owner out after a supporting actor enters.
        current = {
            "root": fanin.root_hash, "branch": fanin.session.branch_id,
            "source": self.source_ref, "root_participants": root_ids,
        }
        binding = canonical(current)
        row = self.db.execute("SELECT value FROM binding WHERE id=1").fetchone()
        if row is None:
            self.db.execute("INSERT INTO binding VALUES (1,?)", (binding,))
        elif row[0] != binding:
            try:
                stored = json.loads(row[0])
            except (TypeError, ValueError):
                stored = {}
            identity_matches = (
                stored.get("root") == current["root"]
                and stored.get("branch") == current["branch"]
                and stored.get("source") == current["source"]
            )
            stored_root = stored.get("root_participants")
            if stored_root is not None:
                root_matches = tuple(stored_root) == root_ids
            else:
                # Legacy row from the baseline or the first C01 cut: it bound a
                # declared participant tuple. Migrate it to the root invariant
                # when it still names this root's focal actor.
                legacy = stored.get("participants")
                root_matches = (
                    isinstance(legacy, (list, tuple))
                    and bool(legacy)
                    and all(isinstance(value, str) for value in legacy)
                    and root_ids[0] in legacy
                )
            if not (identity_matches and root_matches):
                self.db.close()
                raise RecursionRefusal("P2_OWNER_BINDING_MISMATCH")
            self.db.execute("UPDATE binding SET value=? WHERE id=1", (binding,))
        self.db.commit()

    def snapshot(self) -> StateIdentity:
        if self.source_ref != "P2_INPUT:" + digest({"case": self.case, "source": self.source}):
            raise RecursionRefusal("P2_INPUT_SOURCE_MUTATED")
        s = self.fanin.session
        verified = s.verify()
        if not verified.get("ok"):
            raise RecursionRefusal("P2_SOURCE_OR_STATE_VERIFICATION_FAILED")
        material = {
            "world": vars(s.world()),
            "events": s.read_events(),
            "intervals": s.read_interval_states(),
            "encounters": s.read_encounters(),
        }
        return StateIdentity(self.fanin.root_hash, self.actor, s.branch_id,
                             s.clock(), digest(material))

    def material_fact(self, slot: str) -> dict:
        """Read one bounded world-material fact held by this composite snapshot.

        The caller's own reader remains responsible for the fact's schema.
        This accessor refuses psyche-store records and binds the read to the
        verified root, current branch, clock and world state of this owner.
        A C12 fork may carry a fact established on a verified ancestor; the
        optional state_scope records when unrelated S46 state was not forked.
        """
        if self.source_ref != "P2_INPUT:" + digest({"case": self.case, "source": self.source}):
            raise RecursionRefusal("P2_INPUT_SOURCE_MUTATED")
        s = self.fanin.session
        if slot not in MATERIAL_FACT_SLOTS:
            raise RecursionRefusal("P2_MATERIAL_FACT_SLOT_INVALID")
        world = s.world()
        if slot not in world.resources:
            raise RecursionRefusal("P2_MATERIAL_FACT_ABSENT:" + str(slot))
        stored = world.resources[slot]
        if not isinstance(stored, Mapping):
            raise RecursionRefusal("P2_MATERIAL_FACT_SCHEMA")
        stored_branch = stored.get("branch")
        stored_epoch = stored.get("epoch")
        root = s.read_root()["root_hash"]
        if stored_branch == s.branch_id:
            verified = s.verify()
            if not verified.get("ok"):
                raise RecursionRefusal("P2_SOURCE_OR_STATE_VERIFICATION_FAILED")
        elif branch_is_ancestor(s, stored_branch, stored_epoch):
            # A C12 fork copies the checkpoint preimages but deliberately does
            # not copy unrelated S46/S47 period state. Verify the branch that
            # actually owns this world fact, not an unrelated period owner.
            verifier = getattr(s.product, "c12_verify", None)
            if not callable(verifier):
                raise RecursionRefusal("P2_SOURCE_OR_STATE_VERIFICATION_FAILED")
            verified = verifier(s.branch_id)
            if not verified.get("ok"):
                raise RecursionRefusal("P2_SOURCE_OR_STATE_VERIFICATION_FAILED")
        else:
            raise RecursionRefusal("P2_MATERIAL_FACT_ROOT_OR_BRANCH_MISMATCH")
        fact = validate_material_fact(stored, root=root,
                                      branch=stored_branch, world_clock=world.clock)
        if stored_branch == s.branch_id:
            state_hash = self.snapshot().state_hash
            state_scope = None
        else:
            # The fork copied the world/event/encounter preimages but no S46
            # interval state, so do not pretend a full composite hash exists.
            material = {
                "world": vars(s.world()),
                "events": s.read_events(),
                "intervals": "NOT_FORKED_ON_C12_BRANCH",
                "encounters": s.read_encounters(),
            }
            state_hash = digest(material)
            state_scope = "C12_FORK_WITHOUT_S46_INTERVAL_STATE"
        result = {
            "schema": MATERIAL_FACT_READ_SCHEMA,
            "grade": self.grade,
            "slot": slot,
            "root": root,
            "branch": s.branch_id,
            "clock": world.clock,
            "epoch": fact["epoch"],
            "source": fact["source"],
            "state_hash": state_hash,
            "world_hash": digest(world.snapshot()),
            "document": fact,
        }
        if state_scope is not None:
            result["state_scope"] = state_scope
        return result

    def validate_proposal(self, proposal: EventProposal) -> None:
        if proposal.operation != "ADMIT_EVENT":
            raise RecursionRefusal("P2_OPERATION_NOT_QUALIFIED:" + proposal.operation)
        if proposal.source_refs != (self.source_ref,):
            raise RecursionRefusal("P2_ABSENT_OR_WRONG_SOURCE")
        resolution = resolve_participants(self.fanin.session, proposal.participants)
        if resolution["focal_actor_id"] not in proposal.participants:
            raise RecursionRefusal("P2_FOCAL_PARTICIPANT_REQUIRED")
        world = self.fanin.session.world()
        focal_position = world.positions.get(resolution["focal_alias"])
        if not isinstance(focal_position, str) or not focal_position.strip():
            raise RecursionRefusal("P2_FOCAL_POSITION_UNAVAILABLE")
        for participant in resolution["participants"]:
            if participant["kind"] == "SUPPORTING_ACTOR":
                if (world.positions.get(participant["alias"])
                        != focal_position):
                    raise RecursionRefusal("P2_SUPPORTING_PARTICIPANT_NOT_COPRESENT")
        assert_no_private_leak(
            self.fanin.session, proposal.document(), proposal.participants)
        if set(proposal.circumstances) - {"history_refs", "language_context"}:
            raise RecursionRefusal("P2_UNSUPPORTED_EVENT_CIRCUMSTANCES")
        if proposal.circumstances.get("language_context") is not None:
            context = proposal.circumstances["language_context"]
            if (not isinstance(context, Mapping)
                    or not isinstance(context.get("milieu_id"), str)
                    or not context["milieu_id"].strip()):
                raise RecursionRefusal("P2_LANGUAGE_CONTEXT_SCHEMA")
            from s43.registry import registry_document
            contexts = {unit["milieu_id"] for unit in
                        registry_document()["unit_library"].values()}
            if context["milieu_id"] not in contexts:
                raise RecursionRefusal("P2_LANGUAGE_CONTEXT_UNSUPPORTED")
        if isinstance(proposal.event_time, bool) or not isinstance(proposal.event_time, int):
            raise RecursionRefusal("P2_INVALID_EVENT_CLOCK")
        refs = proposal.circumstances.get("history_refs", ())
        if not isinstance(refs, (list, tuple)) or any(
                not isinstance(ref, str) or not ref.strip() for ref in refs):
            raise RecursionRefusal("P2_HISTORY_REFS_SCHEMA")
        # Mirror the existing native reader's identity/order prerequisites
        # before any ACTUAL interval can commit. Resolve only native IDs/hashes.
        history = self.fanin.session.read_events() if refs else []
        seen = set()
        last_ordinal, last_time = -1, -1
        for ref in refs:
            prior = next((row for row in history if ref in
                          (row["e1_event_id"], row["e1_event_hash"])), None)
            if prior is None:
                raise RecursionRefusal("P2_HISTORY_REF_MISSING:" + ref)
            if prior["e1_event_id"] in seen:
                raise RecursionRefusal("P2_HISTORY_REF_DUPLICATE")
            if (prior["branch_id"] != self.fanin.session.branch_id
                    or prior["actor_id"] != self.actor):
                raise RecursionRefusal("P2_HISTORY_IDENTITY_MISMATCH")
            ordinal, clock = int(prior["event_ordinal"]), int(prior["event_time"])
            if (ordinal <= last_ordinal or clock <= last_time
                    or clock >= proposal.event_time):
                raise RecursionRefusal("P2_HISTORY_REF_ORDER_INVALID")
            seen.add(prior["e1_event_id"])
            last_ordinal, last_time = ordinal, clock
        now = self.snapshot().clock
        if proposal.event_time <= now:
            raise RecursionRefusal("P2_EVENT_CLOCK_NOT_FUTURE")
        if proposal.interval is not None:
            if set(proposal.interval) != {"mode", "span"}:
                raise RecursionRefusal("P2_INTERVAL_SCHEMA")
            span = proposal.interval["span"]
            if isinstance(span, bool) or not isinstance(span, int) or span < 1:
                raise RecursionRefusal("P2_INVALID_INTERVAL_SPAN")
            if proposal.interval["mode"] not in {"ACTUAL", "SCHEDULED_ONLY"}:
                raise RecursionRefusal("P2_UNQUALIFIED_INTERVAL_MODE")
            if now + span >= proposal.event_time:
                raise RecursionRefusal("P2_INTERVAL_CROSSES_EVENT_CLOCK")

    def realize(self, operation_id: str, proposal: EventProposal,
                expected: StateIdentity) -> RealizedEvent:
        lock = Path(self.fanin.session.state_root) / "recursion_owner.lock"
        with lock.open("a") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            return self._realize(operation_id, proposal, expected)

    def actor_experience(self, event: Mapping, *, after_clock: int) -> dict:
        """Compile actual actor perceptions, never the portal user's view.

        The accepted E1 binding identifies the generated actor and its actual
        BP4 action. That action supplies the store's actor alias; no alias is
        guessed from an actor name. Perception rows govern event inclusion.
        This is an experience input, not an issued psychological memory.
        """
        result = {"schema": "SOROK_ACTOR_EXPERIENCE@1", "grade": self.grade,
                  "actor_ref": self.actor, "status": "HELD", "events": [],
                  "memory_formation": "MISSING_RULE"}
        s = self.fanin.session
        if event.get("actor_id") != self.actor:
            result["reason"] = "P2_EVENT_ACTOR_MISMATCH"
            return result
        action = s.event(event.get("action_event_id") or "")
        if (not action or not event.get("action_event_hash")
                or action.get("hash") != event["action_event_hash"]):
            result["reason"] = "P2_ACTOR_ACTION_BINDING_UNAVAILABLE"
            return result
        alias = action.get("actor_id")
        if not alias or alias == s.meta.get("user_actor"):
            result["reason"] = "P2_DEVELOPING_ACTOR_ALIAS_UNAVAILABLE"
            return result
        receipts = s.product.store.perceptions(s.branch_id, actor_id=alias)
        receipts = [row for row in receipts if row["actor_id"] == alias
                    and after_clock < row["clock"] <= action["clock"]]
        if not any(row["event_id"] == action["event_id"] for row in receipts):
            result["reason"] = "P2_ACTOR_PERCEPTION_UNAVAILABLE"
            return result
        # Reuse the accepted observable-content projection, but remove its
        # user-specific assertion. Access here comes from this actor's receipts.
        from s45_projection.projection import project_event
        for receipt in receipts:
            observed = s.event(receipt["event_id"])
            if not observed or observed["clock"] > receipt["clock"]:
                result["reason"] = "P2_ACTOR_PERCEPTION_EVENT_UNAVAILABLE"
                result["events"] = []
                return result
            projected = project_event(observed)
            projected.pop("perceived_by_user")
            projected["perception"] = {"clock": receipt["clock"],
                                       "channel": receipt["channel"]}
            result["events"].append(projected)
        result.update(status="OBSERVED", actor_alias=alias)
        return result

    def _realize(self, operation_id: str, proposal: EventProposal,
                 expected: StateIdentity) -> RealizedEvent:
        proposal_hash = digest(proposal.document())
        # BEGIN IMMEDIATE serializes adapter calls, including native owner writes.
        self.db.execute("BEGIN IMMEDIATE")
        row = self.db.execute("SELECT proposal, before_state, result FROM operations "
                              "WHERE id=?", (operation_id,)).fetchone()
        if row is not None:
            self.db.rollback()
            if row[:2] != (proposal_hash, canonical(expected.document())):
                raise RecursionRefusal("P2_OPERATION_REUSE_MISMATCH")
            if row[2] is None:
                raise RecursionRefusal("P2_AMBIGUOUS_PRIOR_OPERATION_HOLD")
            body = json.loads(row[2])
            body["before"] = StateIdentity(**body["before"])
            body["after"] = StateIdentity(**body["after"])
            body["readset"] = tuple(body["readset"])
            result = RealizedEvent(**body)
            if self.snapshot() != result.after:
                raise RecursionRefusal("P2_REPLAY_STATE_MISMATCH")
            supporting = (result.consequences.get("supporting_participants") or [])
            if supporting:
                verify_supporting_participation(
                    self.fanin.session,
                    event_id=supporting[0]["event_id"], participants=supporting,
                )
            return result
        try:
            if self.snapshot() != expected:
                raise RecursionRefusal("P2_STALE_ROOT_BRANCH_CLOCK_OR_STATE")
            self.validate_proposal(proposal)
            self.db.execute("INSERT INTO operations VALUES (?,?,?,NULL)",
                            (operation_id, proposal_hash, canonical(expected.document())))
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise
        # The reservation survives errors/crashes. Native P2 operations are never
        # reissued blindly. A pending result requires owner-level reconciliation.
        s = self.fanin.session
        material_before = detached(s.world().actor_state)
        interval_result = None
        if proposal.interval is not None:
            deps = self.fanin.deps
            start = s.clock()
            domain = deps["make_domain"](mode=proposal.interval["mode"], start=start,
                                         end=start + proposal.interval["span"])
            interval_result = s.produce_interval(domain)
        refs = tuple(proposal.circumstances.get("history_refs") or ())
        if not refs:
            refs = tuple(x["e1_event_id"] for x in s.read_events())
        kwargs = {}
        if "language_context" in proposal.circumstances:
            kwargs["language_context"] = detached(proposal.circumstances["language_context"])
        admitted = s.admit_event(case=self.case, source=self.source,
                                 history_event_refs=refs, event_time=proposal.event_time,
                                 **kwargs)
        event = admitted.get("event") or {}
        event_ref = event.get("e1_event_id")
        if not event_ref:
            raise RecursionRefusal("P2_NATIVE_EVENT_NOT_REALIZED")
        read = s.read_event(event_ref)
        language = s.read_s43_event(event_ref)
        conditioning = s.read_c9_conditioning(event_ref)
        from p2_continuation.continuation import _s43_summary, _c9_summary
        observation = {
            "event_ref": event_ref,
            "event_hash": read["e1_event_hash"],
            "status": admitted.get("status"),
            "event_ordinal": event.get("event_ordinal"),
            "performed": event.get("performed"),
            "s43": _s43_summary(language),
            "c9": _c9_summary(conditioning),
        }
        root_ids = tuple(s.read_root()["actor_ids"])
        supporting_ids = tuple(participant for participant in proposal.participants
                               if participant not in root_ids)
        supporting, participation_status = [], "NONE"
        if supporting_ids:
            action_event_id = read.get("action_event_id") or ""
            action_event = s.event(action_event_id) if action_event_id else None
            if action_event:
                supporting = record_supporting_participation(
                    s, event=action_event, participants=supporting_ids,
                )
                participation_status = "RECORDED"
            else:
                participation_status = "HELD_NO_PERFORMED_EVENT"
        after = self.snapshot()
        consequence = {
            "grade": self.grade,
            "focal_actor": self.actor,
            "owner_state_changed": expected.state_hash != after.state_hash,
            "material_state_changed": material_before != detached(s.world().actor_state),
            "interval": detached(interval_result),
            "immediate_response": observation["c9"],
            "durable_psychological_transition": "MISSING_RULE",
            "independent_B": "CONTROLLED_SOURCEFREE_PARTICIPANT_ONLY",
            "supporting_participation": participation_status,
            "supporting_participants": supporting,
        }
        if supporting:
            verify_supporting_participation(
                s, event_id=supporting[0]["event_id"], participants=supporting,
            )
        result = RealizedEvent(
            operation_id, proposal_hash, expected, after, "REALIZED",
            {"event": detached(read), "interval": detached(interval_result)},
            self.actor_experience(read, after_clock=expected.clock), consequence,
            (self.source_ref, read["e1_event_hash"]), "P2_EVENT:" + read["e1_event_hash"],
        )
        self.db.execute("UPDATE operations SET result=? WHERE id=?",
                        (canonical(asdict(result)), operation_id))
        self.db.commit()
        return result

    def close(self) -> None:
        self.db.close()
        self.fanin.close()
