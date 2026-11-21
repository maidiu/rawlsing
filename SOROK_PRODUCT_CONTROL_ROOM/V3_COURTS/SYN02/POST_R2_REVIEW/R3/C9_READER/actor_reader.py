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


C12_SOURCE_HASHES = {
    "vendor/j/candidate/vendor/bp4/bp4/store.py":
        "872df999b3e6ffcb4a168317cc2591ec6f79f73f9ce7fffc13b24caead7315d4",
    "vendor/j/candidate/vendor/bp4/bp4/canon.py":
        "31e0ff2022000f0b721b9b0ceb6eb358295de4442bb044b14d3f4b60b79e4276",
    "vendor/j/candidate/vendor/bp4/vendor/bp1/canon.py":
        "3d81b9d78765e24dfbbf80b496945d4768c1b5659f4fb69176e724a7d6f50482",
    "vendor/j/r26e/c12_integrity.py":
        "7d046a5bf9d49cbce1f3e5e85aafee56715be712b576063b98bb78ed378e508d",
}


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


def load_c12_source(root: Path) -> dict:
    """Verify exact C12 bytes, then import under private names without cache trust."""
    import types
    root = Path(root)
    for relative, expected in C12_SOURCE_HASHES.items():
        path = root / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ReaderHeld("C12_SOURCE_CHANGED_BEFORE_IMPORT")
    expected_paths = {name: (root / relative).resolve() for name, relative in {
        "bp4.store": "vendor/j/candidate/vendor/bp4/bp4/store.py",
        "bp4.canon": "vendor/j/candidate/vendor/bp4/bp4/canon.py",
        "bp1.canon": "vendor/j/candidate/vendor/bp4/vendor/bp1/canon.py",
    }.items()}
    for name, expected_path in expected_paths.items():
        cached = sys.modules.get(name)
        if cached is not None:
            actual = Path(getattr(cached, "__file__", "")).resolve()
            if actual != expected_path:
                raise ReaderHeld("C12_FOREIGN_CACHE_HELD:" + name)
    bp1_dir = root / "vendor/j/candidate/vendor/bp4/vendor/bp1"
    bp4_dir = root / "vendor/j/candidate/vendor/bp4/bp4"
    bp1_name = "_c9_bp1_" + uuid.uuid4().hex
    bp4_name = "_c9_bp4_" + uuid.uuid4().hex
    bp1 = types.ModuleType(bp1_name)
    bp1.__path__ = [str(bp1_dir)]
    bp4 = types.ModuleType(bp4_name)
    bp4.__path__ = [str(bp4_dir)]
    sys.modules[bp1_name] = bp1
    sys.modules[bp4_name] = bp4
    alias_names = ("bp1", "bp1.canon", "bp4", "bp4.canon", "bp4.store")
    saved = {name: sys.modules.get(name) for name in alias_names}
    try:
        bp1_canon = _load_module(bp1_name + ".canon", bp1_dir / "canon.py")
        sys.modules["bp1"] = bp1
        sys.modules["bp1.canon"] = bp1_canon
        bp4_canon = _load_module(bp4_name + ".canon", bp4_dir / "canon.py")
        bp4_store = _load_module(bp4_name + ".store", bp4_dir / "store.py")
        sys.modules.update({"bp4": bp4, "bp4.canon": bp4_canon,
                            "bp4.store": bp4_store})
        integrity = _load_module(
            "_c9_c12_integrity_" + uuid.uuid4().hex,
            root / "vendor/j/r26e/c12_integrity.py")
    finally:
        for name, old in saved.items():
            if old is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old
    return {"store": bp4_store, "canon": bp4_canon,
            "qualified": integrity.QualifiedC12Store}


def _perception_rows_hash(rows) -> str:
    return sha([dict(row) for row in rows])


def _c12_branch(reader, branch_id: str):
    try:
        return reader.branch(branch_id)
    except ReaderHeld:
        raise
    except Exception as error:
        if getattr(error, "code", None) == "BRANCH_NOT_FOUND":
            raise ReaderHeld("C12_FORK_BRANCH_MISSING:" + branch_id) from error
        raise


def _validate_c12_fork(c12: dict, branch, parent, source_cut: str) -> None:
    connection = c12["connection"]
    reader = c12["reader"]
    actor_id = branch["actor_id"]
    child_id = branch["c12_branch_id"]
    parent_id = parent["c12_branch_id"]
    if not child_id or not parent_id:
        raise ReaderHeld("C12_BRANCH_ID_MISSING")
    if branch["fork_c12_branch_id"] != child_id:
        raise ReaderHeld("C12_FORK_BRANCH_BINDING_MISMATCH")
    if branch["fork_source_cut_hash"] != source_cut or branch["source_cut_hash"] != source_cut:
        raise ReaderHeld("C12_FORK_SOURCE_CUT_MISMATCH")
    child = _c12_branch(reader, child_id)
    actual_parent = _c12_branch(reader, parent_id)
    if child["parent_branch_id"] != parent_id:
        raise ReaderHeld("C12_FORK_PARENT_MISMATCH")
    if branch["fork_c12_root_hash"] != child["root_hash"]:
        raise ReaderHeld("C12_FORK_ROOT_MISMATCH")
    if branch["fork_c12_watermark"] != child["fork_clock"]:
        raise ReaderHeld("C12_FORK_WATERMARK_MISMATCH")
    if actor_id not in child["actor_ids"] or actor_id not in actual_parent["actor_ids"]:
        raise ReaderHeld("C12_ACTOR_MISMATCH")
    verified = reader.verify(child_id)
    if not verified["ok"]:
        raise ReaderHeld("C12_FORK_INTEGRITY_HELD")
    inherited = int((child.get("root_counts") or {}).get("perception", 0))
    child_rows = connection.execute(
        "SELECT seq,actor_id,event_id,clock,channel FROM perception "
        "WHERE branch_id=? ORDER BY seq LIMIT ?", (child_id, inherited)).fetchall()
    parent_rows = connection.execute(
        "SELECT seq,actor_id,event_id,clock,channel FROM perception "
        "WHERE branch_id=? ORDER BY seq LIMIT ?", (parent_id, inherited)).fetchall()
    if [dict(row) for row in child_rows] != [dict(row) for row in parent_rows]:
        raise ReaderHeld("C12_INHERITED_PERCEPTION_PREFIX_MISMATCH")
    if _perception_rows_hash(child_rows) != branch["fork_c12_perception_hash"]:
        raise ReaderHeld("C12_INHERITED_PERCEPTION_HASH_MISMATCH")


def _history_records(connection, actor_id: str, branch, source_cut: str,
                     stop_hash: str | None, c12: dict | None,
                     seen: frozenset) -> tuple[list, dict, bool]:
    key = (branch["actor_id"], branch["branch_id"], branch["branch_epoch"])
    if key in seen:
        raise ReaderHeld("C9_FORK_ANCESTRY_CYCLE")
    seen = seen | {key}
    versions = list(connection.execute(
        "SELECT * FROM actor_version WHERE actor_id=? AND branch_id=? AND branch_epoch=? ORDER BY version_no",
        (branch["actor_id"], branch["branch_id"], branch["branch_epoch"])))
    if not versions or versions[0]["version_no"] != 0:
        raise ReaderHeld("VERSION_KIND_HELD")
    cutoff = len(versions)
    if stop_hash is not None:
        positions = [index for index, version in enumerate(versions)
                     if version["version_hash"] == stop_hash]
        if not positions:
            raise ReaderHeld("C9_FORK_FRONTIER_MISSING")
        cutoff = positions[0] + 1
    records = []
    previous = None
    pending = False
    for version in versions[:cutoff]:
        if version["source_cut_hash"] != source_cut:
            raise ReaderHeld("HISTORY_SOURCE_CUT_MISMATCH")
        kind = version["version_kind"]
        if kind == "GENESIS_VALID_EMPTY":
            if branch["parent_actor_id"] is not None:
                raise ReaderHeld("GENESIS_ANCESTRY_MISMATCH")
            expected = sha({"schema": "C9_ACTOR_VERSION_R3@1", "actor": actor_id,
                            "branch": branch["branch_id"], "epoch": branch["branch_epoch"],
                            "version": 0, "kind": "GENESIS_VALID_EMPTY",
                            "parent": None, "semantic": sha({}), "state": {}})
            if (previous is not None or version["version_no"] != 0
                    or version["version_hash"] != expected
                    or version["semantic_hash"] != sha({})
                    or version["canonical_state_json"] != "{}"):
                raise ReaderHeld("GENESIS_BINDING_MISMATCH")
            previous = dict(version)
            continue
        if kind == "FORK_INHERITED":
            if branch["parent_actor_id"] is None:
                raise ReaderHeld("FORK_INHERITED_WITHOUT_PARENT")
            if previous is not None or version["version_no"] != 0:
                raise ReaderHeld("VERSION_KIND_HELD")
            parent_branch = connection.execute(
                "SELECT * FROM actor_branch WHERE actor_id=? AND branch_id=?",
                (branch["parent_actor_id"], branch["parent_branch_id"])).fetchone()
            if parent_branch is None:
                raise ReaderHeld("C9_FORK_PARENT_MISSING")
            if (branch["parent_actor_id"] != actor_id
                    or branch["parent_branch_id"] == branch["branch_id"]
                    or branch["parent_branch_epoch"] != parent_branch["branch_epoch"]):
                raise ReaderHeld("C9_FORK_PARENT_MISMATCH")
            if branch["fork_source_cut_hash"] != source_cut:
                raise ReaderHeld("C9_FORK_SOURCE_CUT_MISMATCH")
            if c12 is None:
                raise ReaderHeld("FORK_HELD_ORIGINAL_C12_NOT_QUALIFIED")
            _validate_c12_fork(c12, branch, parent_branch, source_cut)
            parent_records, frontier, parent_pending = _history_records(
                connection, actor_id, parent_branch,
                parent_branch["source_cut_hash"],
                branch["fork_base_version_hash"], c12, seen)
            if branch["fork_base_version_hash"] != frontier["version_hash"]:
                raise ReaderHeld("C9_FORK_FRONTIER_MISMATCH")
            expected = sha({"schema": "C9_ACTOR_VERSION_R3@1", "actor": actor_id,
                            "branch": branch["branch_id"], "epoch": branch["branch_epoch"],
                            "version": 0, "kind": "FORK_INHERITED",
                            "parent": frontier["version_hash"],
                            "semantic": frontier["semantic_hash"]})
            if (version["parent_version_hash"] != frontier["version_hash"]
                    or version["semantic_hash"] != frontier["semantic_hash"]
                    or version["canonical_state_json"] != frontier["canonical_state_json"]
                    or version["version_hash"] != expected):
                raise ReaderHeld("C9_FORK_INHERITED_BINDING_MISMATCH")
            records.extend(parent_records)
            pending = pending or parent_pending
            previous = dict(version)
            continue
        if previous is None or kind not in {"SEMANTIC_CHANGE", "ADMINISTRATIVE_NOCHANGE"}:
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
                actor_id, branch["branch_id"], branch["branch_epoch"], version["version_hash"], version["semantic_hash"]):
            raise ReaderHeld("VERSION_RECEIPT_BINDING_MISMATCH")
        expected_version = sha({"schema": "C9_ACTOR_VERSION_R3@1", "actor": actor_id,
                                "branch": branch["branch_id"], "epoch": branch["branch_epoch"],
                                "seq": body["commit_seq"], "parent": previous["version_hash"],
                                "semantic": version["semantic_hash"], "kind": body["decision_kind"]})
        if (expected_version != version["version_hash"] or body["before_version_hash"] != previous["version_hash"]
                or body["before_semantic_hash"] != previous["semantic_hash"]):
            raise ReaderHeld("VERSION_HASH_MISMATCH")
        if kind == "ADMINISTRATIVE_NOCHANGE":
            if (body["decision_kind"] != "TRUE_NO_CHANGE_EVALUATED"
                    or version["semantic_hash"] != previous["semantic_hash"]
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
        semantic = sha({"actor": actor_id, "branch": branch["branch_id"],
                        "epoch": branch["branch_epoch"], "event": state["event_key"],
                        "payload": state["payload"]})
        if semantic != version["semantic_hash"] or state["semantic"] != semantic or state["event_key"] != body["event_key"]:
            raise ReaderHeld("SEMANTIC_PAYLOAD_MISMATCH")
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
    if previous is None:
        raise ReaderHeld("HEAD_HISTORY_BINDING_MISMATCH")
    branch_pending = connection.execute(
        "SELECT count(*) FROM projection_outbox WHERE actor_id=? AND branch_id=? "
        "AND branch_epoch=? AND projection_state<>'ACKED'",
        (branch["actor_id"], branch["branch_id"], branch["branch_epoch"])).fetchone()[0]
    return records, previous, bool(pending or branch_pending)


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
    visible_records: tuple[SurfaceRecord, ...] | None
    grade: str = "SOURCEFREE_CANDIDATE_NOT_OWNER_FROZEN"


def read_actor_snapshot(source: Path, database: Path, *, actor_id: str,
                        branch_id: str, branch_epoch: str, source_cut: str,
                        c12_source: Path | None = None,
                        c12_database: Path | None = None) -> ActorSnapshotReadV1:
    candidate = load_candidate(source)
    c12 = None
    c12_connection = None
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
            if c12_source is None or c12_database is None:
                raise ReaderHeld("FORK_HELD_ORIGINAL_C12_NOT_QUALIFIED")
            modules = load_c12_source(Path(c12_source))
            c12_connection = sqlite3.connect(
                Path(c12_database).resolve().as_uri() + "?mode=ro",
                uri=True, isolation_level=None)
            c12_connection.row_factory = sqlite3.Row
            c12_connection.execute("PRAGMA query_only=ON")
            c12_connection.execute("BEGIN")
            c12_reader = object.__new__(modules["qualified"])
            c12_reader.path = Path(c12_database)
            c12_reader.db = c12_connection
            c12 = {"connection": c12_connection, "reader": c12_reader}
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
        records, previous, pending = _history_records(
            connection, actor_id, branch, source_cut, None, c12, frozenset())
        if previous["version_hash"] != raw["version_hash"]:
            raise ReaderHeld("HEAD_HISTORY_BINDING_MISMATCH")
        # ACK alone cannot prove original C12 source/mirror integrity.
        delivery = "SYNC_HELD" if pending else "C12_SOURCE_QUALIFICATION_HELD"
        return ActorSnapshotReadV1(actor_id, branch_id, branch_epoch, raw["version_hash"], raw["semantic_hash"],
                                   canon(raw["state"]), source_cut, delivery, tuple(records))
    except (sqlite3.Error, json.JSONDecodeError, KeyError, TypeError) as error:
        raise ReaderHeld("C9_READ_HELD") from error
    finally:
        if c12_connection is not None:
            if c12_connection.in_transaction:
                c12_connection.rollback()
            c12_connection.close()
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


@dataclass(frozen=True)
class DerivedViewRequestV1:
    view_id: str
    actor_id: str
    source_cut: str


@dataclass(frozen=True)
class DerivedViewValueV1:
    view_id: str
    value: SurfacePacketV1 | None
    source_fact_ids: tuple[str, ...]
    status: str
    warnings: tuple[str, ...]
    source_version_ref: str | None = None


def compute_view(snapshot: ActorSnapshotReadV1, request: DerivedViewRequestV1) -> DerivedViewValueV1:
    """Pure F1 view used by F2. No store, globals, legacy defaults or arithmetic law.

    Only the implemented received-surface view is registered. The version frontier
    is a technical reference; canonical fact IDs await an owner-frozen contract.
    """
    from copy import deepcopy
    from dataclasses import asdict
    def held(reason):
        return DerivedViewValueV1(request.view_id, None, (), "HELD", (reason,))
    if request.actor_id != snapshot.actor_id:
        return held("ACTOR_SCOPE_MISMATCH")
    if request.source_cut != snapshot.source_cut:
        return held("SOURCE_CUT_MISMATCH")
    if request.view_id != "ACTOR_RECEIVED_SURFACE_TESTONLY@1":
        return held("UNKNOWN_VIEW")
    if snapshot.visible_records is None:
        return DerivedViewValueV1(request.view_id, None, (), "UNKNOWN", ("ACTOR_ACCESS_UNAVAILABLE",))
    work = deepcopy(snapshot)
    before = asdict(work)
    value = build_surface_packet(work)
    after = asdict(work)
    if before != after:
        changed = tuple(key for key in before if before[key] != after.get(key))
        raise ReaderHeld("DERIVED_VIEW_MUTATION:" + ",".join(changed))
    return DerivedViewValueV1(request.view_id, value, (), "OK",
                              ("SOURCEFREE_NOT_OWNER_FROZEN",), snapshot.version_hash)


def read_surface(snapshot: ActorSnapshotReadV1) -> ActorVisibleSurfaceV1:
    """F1.compute_view -> SurfacePacketV1 -> ActorVisibleSurfaceV1; no writer."""
    result = compute_view(snapshot, DerivedViewRequestV1("ACTOR_RECEIVED_SURFACE_TESTONLY@1", snapshot.actor_id, snapshot.source_cut))
    if result.status != "OK":
        raise ReaderHeld("DERIVED_VIEW_" + result.status)
    return actor_visible_surface(result.value)


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
    parser.add_argument("--c12-source", type=Path)
    parser.add_argument("--c12-database", type=Path)
    options = parser.parse_args()
    try:
        snapshot = read_actor_snapshot(options.source, options.database, actor_id=options.actor,
                                       branch_id=options.branch, branch_epoch=options.epoch,
                                       source_cut=options.source_cut,
                                       c12_source=options.c12_source,
                                       c12_database=options.c12_database)
        print(read_surface(snapshot).to_json())
    except (ReaderHeld, OSError, sqlite3.Error):
        print("ACTOR_SURFACE_HELD", file=sys.stderr)
        raise SystemExit(2)
