"""Read-only SOURCEFREE consumer of exact C9 candidate 1e99681f.

Technical snapshot/delivery data is separate from the actor-visible surface.
This neither freezes the candidate writer nor qualifies an original C12 fork.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import uuid

from check_reader_precondition import HASHES


class ReaderHeld(ValueError):
    pass


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha(value):
    return hashlib.sha256(canon(value).encode()).hexdigest()


def load_candidate(root: Path):
    for name, expected in HASHES.items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ReaderHeld("SOURCE_CHANGED_BEFORE_IMPORT")
    name = "c9_verified_reader_" + uuid.uuid4().hex
    spec = importlib.util.spec_from_file_location(name, root / "c9_actor_r3.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


@dataclass(frozen=True)
class SurfaceRecord:
    text: str
    epistemic_kind: str


@dataclass(frozen=True)
class ActorSnapshotReadV1:
    actor_id: str
    branch_id: str
    branch_epoch: str
    version_hash: str
    semantic_hash: str
    state_json: str
    source_cut: str
    delivery_status: str
    # Filtered records only; no hidden receipt IDs/count/order enter actor JSON.
    visible_records: tuple[SurfaceRecord, ...]
    grade: str = "SOURCEFREE_CANDIDATE_NOT_OWNER_FROZEN"


def read_actor_snapshot(source: Path, database: Path, *, actor_id: str,
                        branch_id: str, branch_epoch: str,
                        source_cut: str) -> ActorSnapshotReadV1:
    candidate = load_candidate(source)
    uri = database.resolve().as_uri() + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True, isolation_level=None)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("PRAGMA query_only=ON")
        connection.execute("BEGIN")
        if connection.execute("PRAGMA application_id").fetchone()[0] != 1129533491:
            raise ReaderHeld("C9_SCHEMA_MISMATCH")
        schema = connection.execute("SELECT value FROM actor_meta WHERE key='schema'").fetchone()
        if schema is None or schema[0] != "C9_ACTOR_AUTHORITY_R3@1":
            raise ReaderHeld("C9_SCHEMA_MISMATCH")
        branch = connection.execute("SELECT * FROM actor_branch WHERE actor_id=? AND branch_id=?",
                                    (actor_id, branch_id)).fetchone()
        if branch is None or branch["branch_epoch"] != branch_epoch:
            raise ReaderHeld("ACTOR_BRANCH_EPOCH_MISMATCH")
        if branch["source_cut_hash"] != source_cut:
            raise ReaderHeld("ACTOR_SOURCE_CUT_MISMATCH")
        if branch["parent_actor_id"] is not None:
            raise ReaderHeld("FORK_HELD_ORIGINAL_C12_NOT_QUALIFIED")
        # Bind existing read-only methods without running the writer constructor/DDL.
        reader = object.__new__(candidate.ActorAuthority)
        reader.conn = connection
        reader.actor_id, reader.branch_id, reader.branch_epoch = actor_id, branch_id, branch_epoch
        verified = reader.verify()
        if not verified["ok"]:
            raise ReaderHeld("ACTOR_INTEGRITY_HELD")
        head = verified["head"]
        if head["branch_epoch"] != branch_epoch:
            raise ReaderHeld("ACTOR_HEAD_EPOCH_MISMATCH")
        raw = reader.read_semantic()
        if raw["source_cut_hash"] != source_cut:
            raise ReaderHeld("ACTOR_VERSION_SOURCE_MISMATCH")
        records = []
        previous = None
        for version in connection.execute(
            "SELECT * FROM actor_version WHERE actor_id=? AND branch_id=? AND branch_epoch=? ORDER BY version_no",
            (actor_id, branch_id, branch_epoch)):
            if version["source_cut_hash"] != source_cut:
                raise ReaderHeld("HISTORY_SOURCE_CUT_MISMATCH")
            if version["version_kind"] == "GENESIS_VALID_EMPTY":
                expected = sha({"schema": "C9_ACTOR_VERSION_R3@1", "actor": actor_id, "branch": branch_id,
                                "epoch": branch_epoch, "version": 0, "kind": "GENESIS_VALID_EMPTY",
                                "parent": None, "semantic": sha({}), "state": {}})
                if previous is not None or version["version_no"] != 0 or version["version_hash"] != expected or version["semantic_hash"] != sha({}) or version["canonical_state_json"] != "{}":
                    raise ReaderHeld("GENESIS_BINDING_MISMATCH")
                previous = dict(version)
                continue
            if previous is None or version["version_kind"] not in {"SEMANTIC_CHANGE", "ADMINISTRATIVE_NOCHANGE"}:
                raise ReaderHeld("VERSION_KIND_HELD")
            if version["version_no"] != previous["version_no"] + 1 or version["parent_version_hash"] != previous["version_hash"]:
                raise ReaderHeld("VERSION_CHAIN_MISMATCH")
            receipt = connection.execute("SELECT * FROM decision_receipt WHERE receipt_hash=?",
                                         (version["decision_receipt_hash"],)).fetchone()
            if receipt is None:
                raise ReaderHeld("VERSION_RECEIPT_MISSING")
            body = json.loads(receipt["canonical_receipt_json"])
            bound = ("actor_id", "branch_id", "branch_epoch", "result_version_hash", "after_semantic_hash",
                     "source_cut_hash", "source_status", "world_occurrence", "actor_reception", "memory_evidence", "sci05_status")
            body_keys = {"actor_id": "actor", "branch_id": "branch", "branch_epoch": "epoch"}
            if sha(body) != receipt["receipt_hash"] or any(receipt[key] != body.get(body_keys.get(key, key)) for key in bound):
                raise ReaderHeld("RECEIPT_BINDING_MISMATCH")
            if (receipt["actor_id"], receipt["branch_id"], receipt["branch_epoch"], receipt["result_version_hash"], receipt["after_semantic_hash"]) != (
                actor_id, branch_id, branch_epoch, version["version_hash"], version["semantic_hash"]):
                raise ReaderHeld("VERSION_RECEIPT_BINDING_MISMATCH")
            expected_version = sha({"schema": "C9_ACTOR_VERSION_R3@1", "actor": actor_id,
                                    "branch": branch_id, "epoch": branch_epoch, "seq": body["commit_seq"],
                                    "parent": previous["version_hash"], "semantic": version["semantic_hash"],
                                    "kind": body["decision_kind"]})
            if (expected_version != version["version_hash"] or body["before_version_hash"] != previous["version_hash"]
                or body["before_semantic_hash"] != previous["semantic_hash"]):
                raise ReaderHeld("VERSION_HASH_MISMATCH")
            if version["version_kind"] == "ADMINISTRATIVE_NOCHANGE":
                if (body["decision_kind"] != "TRUE_NO_CHANGE_EVALUATED" or version["semantic_hash"] != previous["semantic_hash"]
                    or version["canonical_state_json"] != previous["canonical_state_json"]):
                    raise ReaderHeld("NO_CHANGE_STATE_MISMATCH")
                previous = dict(version)
                continue
            if body["decision_kind"] != "COMMITTED_CHANGE":
                raise ReaderHeld("VERSION_DECISION_MISMATCH")
            previous = dict(version)
            state = json.loads(version["canonical_state_json"])
            if not isinstance(state, dict) or set(state) != {"event_key", "semantic", "payload"}:
                raise ReaderHeld("SEMANTIC_STATE_SHAPE_HELD")
            semantic = sha({"actor": actor_id, "branch": branch_id, "epoch": branch_epoch,
                            "event": state["event_key"], "payload": state["payload"]})
            if semantic != version["semantic_hash"] or state["semantic"] != semantic or state["event_key"] != body["event_key"]:
                raise ReaderHeld("SEMANTIC_PAYLOAD_MISMATCH")
            if receipt["source_cut_hash"] != source_cut:
                raise ReaderHeld("HISTORY_SOURCE_CUT_MISMATCH")
            # No inferred observation from objective occurrence or analyst-only material.
            if (receipt["source_status"] != "QUALIFIED" or receipt["world_occurrence"] != "OCCURRED"
                or receipt["actor_reception"] not in {"RECEIVED", "PARTIAL", "TESTIMONY"}
                or receipt["memory_evidence"] not in {"ACTOR_ACCESSIBLE", "PARTIAL_TRACE", "BELIEF_WITH_SOURCE"}
                or receipt["sci05_status"] not in {"ADMITTED", "NOT_APPLICABLE"}):
                continue
            payload = state["payload"]
            surface = payload.get("actor_surface") if isinstance(payload, dict) else None
            if surface is None:
                continue
            if not isinstance(surface, dict) or set(surface) != {"text"} or not isinstance(surface["text"], str):
                raise ReaderHeld("ACTOR_SURFACE_ALLOWLIST_HELD")
            if not surface["text"] or len(surface["text"]) > 4096:
                raise ReaderHeld("ACTOR_SURFACE_TEXT_HELD")
            epistemic = {"ACTOR_ACCESSIBLE": "received_account", "PARTIAL_TRACE": "partial_trace",
                         "BELIEF_WITH_SOURCE": "sourced_belief"}[receipt["memory_evidence"]]
            records.append(SurfaceRecord(surface["text"], epistemic))
        if previous is None or previous["version_hash"] != raw["version_hash"]:
            raise ReaderHeld("HEAD_HISTORY_BINDING_MISMATCH")
        pending = connection.execute(
            "SELECT count(*) FROM projection_outbox WHERE actor_id=? AND branch_id=? AND branch_epoch=? AND projection_state<>'ACKED'",
            (actor_id, branch_id, branch_epoch)).fetchone()[0]
        # ACK alone cannot prove original C12 source/mirror integrity.
        delivery = "SYNC_HELD" if pending else "C12_SOURCE_QUALIFICATION_HELD"
        return ActorSnapshotReadV1(actor_id, branch_id, branch_epoch, raw["version_hash"], raw["semantic_hash"],
                                   canon(raw["state"]), source_cut, delivery, tuple(records))
    except (sqlite3.Error, json.JSONDecodeError, KeyError, TypeError) as error:
        raise ReaderHeld("C9_READ_HELD") from error
    finally:
        if connection.in_transaction:
            connection.rollback()
        connection.close()


@dataclass(frozen=True)
class SurfacePacketV1:
    records: tuple[SurfaceRecord, ...]


@dataclass(frozen=True)
class ActorVisibleSurfaceV1:
    records: tuple[SurfaceRecord, ...]

    def to_json(self) -> str:
        return canon({"schema": "ActorVisibleSurfaceV1", "records": [
            {"text": row.text, "epistemic_kind": row.epistemic_kind} for row in self.records]})


def build_surface_packet(snapshot: ActorSnapshotReadV1) -> SurfacePacketV1:
    for record in snapshot.visible_records:
        if (type(record) is not SurfaceRecord or type(record.text) is not str
            or record.epistemic_kind not in {"received_account", "partial_trace", "sourced_belief"}):
            raise ReaderHeld("SURFACE_RECORD_SHAPE_HELD")
    return SurfacePacketV1(snapshot.visible_records)


def actor_visible_surface(packet: SurfacePacketV1) -> ActorVisibleSurfaceV1:
    return ActorVisibleSurfaceV1(packet.records)


def read_surface(snapshot: ActorSnapshotReadV1) -> ActorVisibleSurfaceV1:
    """SurfaceRecord -> SurfacePacketV1 -> ActorVisibleSurfaceV1; no writer callback."""
    return actor_visible_surface(build_surface_packet(snapshot))


def gate_second_half(first_half_status: str, proposals: tuple) -> tuple[str, ...]:
    """No independence inference from omitted dependency pointers; no world execution."""
    if not 3 <= len(proposals) <= 5:
        raise ReaderHeld("BATCH_PROPOSAL_COUNT_HELD")
    status = "PROPOSED_ONLY" if first_half_status == "ADMITTED" else "HELD_SCI05_FIRST_HALF"
    return tuple(status for _ in proposals)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--epoch", required=True)
    parser.add_argument("--source-cut", required=True)
    options = parser.parse_args()
    try:
        snapshot = read_actor_snapshot(options.source, options.database, actor_id=options.actor,
                                       branch_id=options.branch, branch_epoch=options.epoch,
                                       source_cut=options.source_cut)
        print(read_surface(snapshot).to_json())
    except (ReaderHeld, OSError, sqlite3.Error):
        print("ACTOR_SURFACE_HELD", file=sys.stderr)
        raise SystemExit(2)
