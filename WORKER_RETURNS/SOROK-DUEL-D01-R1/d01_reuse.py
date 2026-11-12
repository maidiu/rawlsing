"""D01 exact-reuse boundary over the existing P3 sourcefree producer.

The selected producer is the current ``p3.P3Owner`` composed over
``p3.state_store.PsycheStore`` and the frozen B1-derived ``p3.test_rules``
formation rule. This module adds no owner, scheduler, rule, store or world
writer. It re-opens the durable owner configuration from disk, validates the
exact code/source/registry identity, and checks that a later P3 realization
consumed the committed sourcefree record through the existing readset path.

Everything here is SOURCEFREE_TEST_ONLY engineering. It does not issue native
CAN/ADP science, actor rights, human validity or production authority.
"""
from __future__ import annotations

import fcntl
import json
import os
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

_ROOT = Path(__file__).resolve().parents[1]
_P3_ROOT = _ROOT / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
_ENGINE_ROOT = _ROOT / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for _path in (_P3_ROOT, _ENGINE_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from developmental_recursion.contracts import (  # noqa: E402
    RecursionRefusal,
    canonical,
    detached,
    digest,
)
from p3 import p3_owner, test_rules  # noqa: E402
from p3.state_store import PsycheStore  # noqa: E402

GRADE = test_rules.GRADE
CONFIG_SCHEMA = p3_owner.CONFIG_SCHEMA
CONFIG_FILE_SCHEMA = "P3_OWNER_CONFIG_FILE@1"
STORE_FILE = p3_owner.STORE_FILE
CONFIG_KEYS = frozenset({
    "schema",
    "source",
    "source_hash",
    "history",
    "plans",
    "catalog",
    "compression_specs",
    "standpoints",
    "code_pins",
})
SELECTED_KIND = "V3MS_MEDIATOR"
SELECTED_RULE = test_rules.rule_descriptors()[0]
CHANGED_KEYS = frozenset({
    "record_id",
    "record_hash",
    "record_hashes",
    "payload",
    "source_hash",
    "registry_hash",
    "causal_parents",
    "rule_id",
    "rule_hash",
})
NATIVE_RULE_ALLOWED = frozenset({"MISSING_RULE", "NOT_ISSUED"})
NATIVE_ACTION_ALLOWED = frozenset({
    "NOT_ISSUED_BY_P3_RULE",
    "NOT_ISSUED",
    "MISSING_RULE",
})


def _refuse(code: str, detail: str = "") -> None:
    raise RecursionRefusal(code if not detail else code + ":" + detail)


def _mapping(value: Any, code: str) -> dict:
    if not isinstance(value, Mapping):
        _refuse(code)
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


def _source_identity(source: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = source.get("identity")
    return nested if isinstance(nested, Mapping) else source


def _verify_completed_config(owner: Any) -> None:
    _verify_completed_config_store(
        owner.store, owner.config_hash,
        code="D01_COLD_CONFIG_PROVENANCE_MISMATCH",
    )


def _verify_completed_config_store(
    store: Any, config_hash: str, *, code: str,
) -> dict | None:
    try:
        return p3_owner.verify_completed_config(store, config_hash)
    except RecursionRefusal as exc:
        if str(exc).startswith("P3_CONFIG_PROVENANCE_MISMATCH"):
            _refuse(code)
        raise


def _fsync_directory(path: Path) -> None:
    try:
        handle = os.open(str(path), os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(handle)
    except OSError:
        pass
    finally:
        os.close(handle)


def _walk_claims(value: Any, path: str = "response") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key == "native_rule" and item not in (None, *NATIVE_RULE_ALLOWED):
                _refuse("D01_NATIVE_RULE_CLAIM", path + "." + str(key))
            if key == "native_action" and item not in (None, *NATIVE_ACTION_ALLOWED):
                _refuse("D01_NATIVE_ACTION_CLAIM", path + "." + str(key))
            if key == "native_science":
                if item not in (None, False, "NOT_ISSUED", "HELD"):
                    _refuse("D01_NATIVE_SCIENCE_CLAIM", path + "." + str(key))
            if key == "production" and item not in (None, False):
                _refuse("D01_PRODUCTION_CLAIM", path + "." + str(key))
            if key == "durable_psychological_transition":
                if item not in (None, "MISSING_RULE", "HELD"):
                    _refuse("D01_DURABLE_TRANSITION_CLAIM", path + "." + str(key))
            if key == "memory_formation" and item not in (None, "MISSING_RULE"):
                _refuse("D01_MEMORY_CLAIM", path + "." + str(key))
            if key == "native_action_performed" and item not in (None, False):
                _refuse("D01_NATIVE_ACTION_CLAIM", path + "." + str(key))
            if key == "first_person_claims" and item not in (None, [], ()):
                _refuse("D01_FIRST_PERSON_CLAIM", path + "." + str(key))
            _walk_claims(item, path + "." + str(key))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _walk_claims(item, path + "[" + str(index) + "]")


def _reject_private_keys(value: Any, path: str = "actor_surface") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key in CHANGED_KEYS or str(key).startswith("_"):
                _refuse("D01_ACTOR_SURFACE_PRIVATE_KEY", path + "." + str(key))
            _reject_private_keys(item, path + "." + str(key))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_private_keys(item, path + "[" + str(index) + "]")


def producer_identity() -> dict:
    """Return the exact selected producer/rule/source identity."""
    guard = test_rules.production_guard()
    if guard.get("status") != "DENY_ZERO_EFFECT" or guard.get("effects") != []:
        _refuse("D01_PRODUCTION_GUARD_NOT_EMPTY")
    if guard.get("native_rule") != "MISSING_RULE":
        _refuse("D01_PRODUCTION_GUARD_NATIVE_CLAIM")
    b1 = Path(test_rules.B1_PATH)
    if not b1.is_file():
        _refuse("D01_B1_SOURCE_MISSING")
    import hashlib
    if hashlib.sha256(b1.read_bytes()).hexdigest() != test_rules.B1_SHA256:
        _refuse("D01_B1_SOURCE_MISMATCH")
    return {
        "schema": "SOROK_D01_PRODUCER_SELECTION@1",
        "grade": GRADE,
        "owner": "p3.p3_owner.P3Owner",
        "store": "p3.state_store.PsycheStore",
        "selected_record_kind": SELECTED_KIND,
        "selected_rule": dict(SELECTED_RULE),
        "response_rule": dict(test_rules.rule_descriptors()[1]),
        "b1_source_sha256": test_rules.B1_SHA256,
        "production_guard": detached(guard),
        "code_pins": detached(p3_owner._code_pins()),
        "native_rule": "MISSING_RULE",
        "native_action": "NOT_ISSUED_BY_P3_RULE",
        "authority": "SOURCEFREE_TEST_ONLY",
    }


def _validate_config_body(config: Any) -> dict:
    config = _mapping(config, "D01_COLD_CONFIG_BODY")
    if set(config) != CONFIG_KEYS:
        _refuse("D01_COLD_CONFIG_KEYS")
    if config.get("schema") != CONFIG_SCHEMA:
        _refuse("D01_COLD_OWNER_SCHEMA")
    if config["code_pins"] != p3_owner._code_pins():
        _refuse("D01_COLD_CODE_IDENTITY")
    source = _mapping(config.get("source"), "D01_COLD_SOURCE")
    if source.get("grade") != GRADE:
        _refuse("D01_COLD_SOURCE_GRADE")
    if config.get("source_hash") != digest(source):
        _refuse("D01_COLD_SOURCE_HASH")
    identity = _source_identity(source)
    for key in ("root", "actor", "branch"):
        _text(identity.get(key), "D01_COLD_SOURCE_" + key.upper())
    if not isinstance(config.get("history"), list):
        _refuse("D01_COLD_HISTORY")
    if not isinstance(config.get("plans"), list):
        _refuse("D01_COLD_PLANS")
    if not isinstance(config.get("catalog"), Mapping):
        _refuse("D01_COLD_CATALOG")
    if not isinstance(config.get("compression_specs"), Mapping):
        _refuse("D01_COLD_COMPRESSION_SPECS")
    if not isinstance(config.get("standpoints"), list):
        _refuse("D01_COLD_STANDPOINTS")
    return config


def load_cold_config(state_root: str | Path) -> dict:
    """Read and validate the durable owner configuration without caller state."""
    root = Path(state_root).expanduser().resolve()
    config_path = root / p3_owner.CONFIG_FILE
    store_path = root / STORE_FILE
    if not config_path.is_file():
        _refuse("D01_COLD_CONFIG_MISSING")
    if not store_path.is_file():
        _refuse("D01_COLD_STORE_MISSING")
    try:
        document = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RecursionRefusal("D01_COLD_CONFIG_UNREADABLE") from exc
    document = _mapping(document, "D01_COLD_CONFIG_SCHEMA")
    if document.get("schema") != CONFIG_FILE_SCHEMA:
        _refuse("D01_COLD_CONFIG_SCHEMA")
    config = _validate_config_body(document.get("config"))
    if document.get("config_hash") != digest(config):
        _refuse("D01_COLD_CONFIG_HASH")
    return config


def recover_missing_config(state_root: str | Path, document: Any) -> dict:
    """Restore an absent owner config only when durable evidence proves it.

    The caller supplies a candidate config document (an exact backup or the
    controller's retained copy).  It is never trusted as such: the last
    completed operation's durable ``result.after.state_hash`` embeds the
    config_hash that actually produced it, so a substituted candidate refuses.
    An empty store (no operations, no records) is recoverable because there is
    no durable computation whose provenance could be reinterpreted.  A pending
    operation with no completed anchor is not recoverable from a config pin.
    """
    root = Path(state_root).expanduser().resolve()
    config_path = root / p3_owner.CONFIG_FILE
    store_path = root / STORE_FILE
    if config_path.exists():
        _refuse("D01_RECOVERY_CONFIG_EXISTS")
    if not store_path.is_file():
        _refuse("D01_RECOVERY_STORE_MISSING")
    document = _mapping(document, "D01_RECOVERY_DOCUMENT")
    if not {"schema", "config", "config_hash"} <= set(document):
        _refuse("D01_RECOVERY_DOCUMENT_KEYS")
    if document.get("schema") != CONFIG_FILE_SCHEMA:
        _refuse("D01_RECOVERY_DOCUMENT_SCHEMA")
    config = _validate_config_body(document.get("config"))
    config_hash = _hash(document.get("config_hash"), "D01_RECOVERY_CONFIG_HASH")
    if config_hash != digest(config):
        _refuse("D01_RECOVERY_CONFIG_HASH")
    identity = _source_identity(config["source"])
    source_hash = config["source_hash"]
    registry_hash = test_rules.make_registry(source_hash)["hash"]
    root.mkdir(parents=True, exist_ok=True)
    lock_path = root / p3_owner.LOCK_FILE
    with lock_path.open("a") as lock_handle:
        fcntl.flock(lock_handle, fcntl.LOCK_EX)
        try:
            if config_path.exists():
                _refuse("D01_RECOVERY_CONFIG_EXISTS")
            if not store_path.is_file():
                _refuse("D01_RECOVERY_STORE_MISSING")
            store = PsycheStore(
                store_path,
                binding={key: identity[key]
                         for key in ("root", "actor", "branch")},
                registry_hash=registry_hash,
                source_hash=source_hash,
            )
            try:
                store.verify()
                pending = store.pending()
                latest = store.latest_completed()
                if latest is not None:
                    provenance = _verify_completed_config_store(
                        store, config_hash,
                        code="D01_RECOVERY_PROVENANCE_MISMATCH",
                    )
                    mode = "VERIFIED_COMPLETED_ANCHOR"
                else:
                    if pending:
                        _refuse("D01_RECOVERY_PENDING_UNVERIFIED")
                    if store.head().get("count") != 0:
                        _refuse(
                            "D01_RECOVERY_RECORDS_WITHOUT_COMPLETION")
                    provenance = None
                    mode = "EMPTY_STORE"
                temporary = root / (p3_owner.CONFIG_FILE + ".tmp")
                try:
                    with temporary.open("w", encoding="utf-8") as handle:
                        handle.write(canonical({
                            "schema": CONFIG_FILE_SCHEMA,
                            "config": config,
                            "config_hash": config_hash,
                        }) + "\n")
                        handle.flush()
                        os.fsync(handle.fileno())
                    os.replace(temporary, config_path)
                except BaseException:
                    if temporary.exists():
                        temporary.unlink()
                    raise
                _fsync_directory(root)
                return {
                    "schema": "SOROK_D01_CONFIG_RECOVERY@1",
                    "state_root": str(root),
                    "config_hash": config_hash,
                    "mode": mode,
                    "pending_operation_ids": [
                        row["operation_id"] for row in pending],
                    "last_completed_operation_id": (
                        provenance["operation_id"]
                        if provenance else None),
                    "store_head": detached(store.head()),
                    "authority": "SOURCEFREE_TEST_ONLY",
                    "native_rule": "MISSING_RULE",
                    "native_action": "NOT_ISSUED_BY_P3_RULE",
                }
            finally:
                store.close()
        finally:
            fcntl.flock(lock_handle, fcntl.LOCK_UN)


def open_cold_owner(base_owner: Any, state_root: str | Path | None = None) -> Any:
    """Open the exact durable P3Owner over a caller-supplied actual base owner."""
    root = state_root
    if root is None:
        session = getattr(getattr(base_owner, "fanin", None), "session", None)
        root = getattr(session, "state_root", None)
    if root is None:
        _refuse("D01_COLD_STATE_ROOT_MISSING")
    snapshot = base_owner.snapshot()
    config = load_cold_config(root)
    identity = _source_identity(config["source"])
    for key in ("root", "actor", "branch"):
        if identity.get(key) != getattr(snapshot, key):
            _refuse("D01_COLD_BASE_IDENTITY:" + key)
    registry_hash = test_rules.make_registry(config["source_hash"])["hash"]
    store = PsycheStore(
        Path(root).expanduser().resolve() / p3_owner.STORE_FILE,
        binding={key: identity[key] for key in ("root", "actor", "branch")},
        registry_hash=registry_hash,
        source_hash=config["source_hash"],
    )
    try:
        if store.pending():
            _refuse("D01_COLD_OPERATION_PENDING")
        store.verify()
        _verify_completed_config_store(
            store, digest(config),
            code="D01_COLD_CONFIG_PROVENANCE_MISMATCH",
        )
    finally:
        store.close()
    owner = p3_owner.P3Owner(
        base_owner,
        source=config["source"],
        history=config["history"],
        plans=config["plans"],
        catalog=config["catalog"],
        compression_specs=config["compression_specs"],
        standpoints=config["standpoints"],
        mode="TEST_ONLY",
    )
    if detached(owner.config) != config:
        owner.close()
        _refuse("D01_COLD_CONFIG_REOPEN_MISMATCH")
    try:
        if owner.store.pending():
            _refuse("D01_COLD_OPERATION_PENDING")
        _verify_completed_config(owner)
    except BaseException:
        owner.close()
        raise
    return owner


EXACT_RESPONSE_KEYS = frozenset({
    "grade", "status", "event_ref", "rule", "streams", "contradictions",
    "native_rule", "native_action", "memory_formation",
    "first_person_claims", "hash",
})
HELD_RESPONSE_KEYS = frozenset({"grade", "status", "reason", "streams"})
EXACT_RULE_KEYS = frozenset({"rule_id", "rule_version", "rule_hash"})
STREAM_KEYS = frozenset({
    "mode", "history_ref", "record_id", "record_hash", "candidate_activity",
    "material_eligible", "native_action_performed",
})


def _exact_stream_keys(stream: Mapping[str, Any]) -> frozenset[str]:
    keys = set(stream)
    if "record_id" in keys or "record_hash" in keys:
        return frozenset({
            "mode", "record_id", "record_hash", "candidate_activity",
            "material_eligible", "native_action_performed",
        })
    if "history_ref" in keys:
        return frozenset({
            "mode", "history_ref", "candidate_activity",
            "material_eligible", "native_action_performed",
        })
    return frozenset({
        "mode", "candidate_activity", "material_eligible",
        "native_action_performed",
    })


def validate_sourcefree_response(response: Any, *, exact: bool = False) -> dict:
    """Reject native/durable/first-person claims in a P3 sourcefree response.

    ``exact`` additionally requires the frozen rule's exact response shape, so
    an affirmative claim cannot ride under an unknown key (for example
    ``can_008``).  The D01 later consumer uses the exact form.
    """
    body = _mapping(response, "D01_RESPONSE_SCHEMA")
    status = _text(body.get("status"), "D01_RESPONSE_STATUS")
    if exact:
        keys = set(body)
        if keys not in (EXACT_RESPONSE_KEYS, HELD_RESPONSE_KEYS):
            _refuse("D01_RESPONSE_SCHEMA_KEYS")
        if body.get("grade") != GRADE:
            _refuse("D01_RESPONSE_GRADE")
        if keys == EXACT_RESPONSE_KEYS:
            if status != "COMPUTED_TEST_ONLY_RESPONSE":
                _refuse("D01_RESPONSE_STATUS")
            rule = _mapping(body.get("rule"), "D01_RESPONSE_RULE")
            if set(rule) != EXACT_RULE_KEYS:
                _refuse("D01_RESPONSE_RULE_KEYS")
            streams = body.get("streams")
            if not isinstance(streams, list):
                _refuse("D01_RESPONSE_STREAMS")
            for stream in streams:
                stream = _mapping(stream, "D01_RESPONSE_STREAM")
                if set(stream) != _exact_stream_keys(stream):
                    _refuse("D01_RESPONSE_STREAM_KEYS")
            if not isinstance(body.get("contradictions"), list):
                _refuse("D01_RESPONSE_CONTRADICTIONS")
            supplied = _hash(body.get("hash"), "D01_RESPONSE_HASH")
            if digest({key: item for key, item in body.items()
                       if key != "hash"}) != supplied:
                _refuse("D01_RESPONSE_HASH_MISMATCH")
        else:
            if status != "HELD":
                _refuse("D01_RESPONSE_STATUS")
            if body.get("streams") != []:
                _refuse("D01_RESPONSE_STREAMS")
    if status.startswith("COMPUTED_TEST_ONLY_RESPONSE"):
        for key in ("native_rule", "native_action", "memory_formation"):
            if key not in body:
                _refuse("D01_RESPONSE_BOUNDARY_MISSING:" + key)
    _walk_claims(body)
    return body


def _validate_record(record: Any, *, owner: Any, as_of: int) -> dict:
    value = _mapping(record, "D01_RECORD_SCHEMA")
    _walk_claims(value, "record")
    supplied = _hash(value.get("hash"), "D01_RECORD_HASH")
    if digest({key: item for key, item in value.items() if key != "hash"}) != supplied:
        _refuse("D01_RECORD_HASH_MISMATCH")
    snapshot = owner.snapshot()
    for key in ("root", "actor", "branch"):
        if value.get(key) != getattr(snapshot, key):
            _refuse("D01_RECORD_IDENTITY:" + key)
    if value.get("source_hash") != owner.source_hash:
        _refuse("D01_RECORD_SOURCE")
    if value.get("registry_hash") != owner.registry["hash"]:
        _refuse("D01_RECORD_REGISTRY")
    if value.get("grade") != GRADE:
        _refuse("D01_RECORD_GRADE")
    if value.get("kind") != SELECTED_KIND:
        _refuse("D01_RECORD_KIND")
    if {key: value.get(key) for key in ("rule_id", "rule_version", "rule_hash")} != {
            key: SELECTED_RULE[key] for key in ("rule_id", "rule_version", "rule_hash")}:
        _refuse("D01_RECORD_RULE")
    effective = value.get("effective_from")
    if isinstance(effective, bool) or not isinstance(effective, int):
        _refuse("D01_RECORD_TIME")
    if effective > as_of:
        _refuse("D01_RECORD_FUTURE")
    parents = value.get("causal_parents")
    if (not isinstance(parents, list) or len(parents) != 2
            or not all(isinstance(parent, str) and parent
                       for parent in parents)):
        _refuse("D01_RECORD_PARENTS")
    event_parent = _hash(parents[0], "D01_RECORD_EVENT_PARENT")
    history_parent = _hash(parents[1], "D01_RECORD_HISTORY_PARENT")
    if parents != [event_parent, history_parent]:
        _refuse("D01_RECORD_PARENTS")
    history = next(
        (row for row in owner.history if row.get("hash") == history_parent),
        None,
    )
    if history is None:
        _refuse("D01_RECORD_HISTORY")
    record_id = _hash(value.get("record_id"), "D01_RECORD_ID")
    expected_id = digest([
        value["root"], value["actor"], value["branch"],
        event_parent, history_parent, SELECTED_RULE["rule_hash"],
    ])
    if record_id != expected_id:
        _refuse("D01_RECORD_ID")
    payload = _mapping(value.get("payload"), "D01_RECORD_PAYLOAD")
    if set(payload) != {
            "mode", "origin_access", "activation_roles", "relation_refs",
            "obligation_refs", "requires_actor_access"}:
        _refuse("D01_RECORD_PAYLOAD_KEYS")
    if payload.get("origin_access") != "NOT_GRANTED_AS_MEMORY":
        _refuse("D01_RECORD_PAYLOAD_ORIGIN")
    if payload.get("requires_actor_access") is not True:
        _refuse("D01_RECORD_PAYLOAD_ACCESS")
    for key in ("activation_roles", "relation_refs", "obligation_refs"):
        items = payload.get(key)
        if not isinstance(items, list) or not all(
                isinstance(item, str) and item for item in items):
            _refuse("D01_RECORD_PAYLOAD_SELECTORS:" + key)
    project = value.get("project")
    counterpart = value.get("counterpart")
    if not isinstance(project, str) or not isinstance(counterpart, str):
        _refuse("D01_RECORD_SCOPE")
    modes = {
        row["hash"]: mode
        for row, mode in test_rules._mode_for(
            owner.history,
            {"project": project, "time": effective},
            counterpart,
        )
    }
    if modes.get(history_parent) != payload.get("mode"):
        _refuse("D01_RECORD_MODE")
    return value


def read_sourcefree_records(
    owner: Any,
    *,
    project: str,
    counterpart: str,
    as_of: int,
) -> dict:
    """Read only the selected rule's exact actor-local records at ``as_of``."""
    test_rules._check_sources(owner.registry, owner.source_hash)
    owner.store.verify()
    records = owner.store.query(
        project=project, counterpart=counterpart, as_of=as_of,
    )
    validated = [
        _validate_record(record, owner=owner, as_of=as_of) for record in records
    ]
    hashes = [record["hash"] for record in validated]
    if len(set(hashes)) != len(hashes):
        _refuse("D01_RECORD_DUPLICATE")
    return {
        "schema": "SOROK_D01_RECORD_READ@1",
        "records": validated,
        "hashes": hashes,
        "head": detached(owner.store.head()),
        "as_of": as_of,
        "authority": "SOURCEFREE_TEST_ONLY",
        "native_rule": "MISSING_RULE",
    }


def later_consumer(
    owner: Any,
    operation_id: str,
    proposal: Any,
    *,
    expected: Any = None,
    require_record_hashes: Sequence[str] | None = None,
) -> dict:
    """Realize one later P3 consumer and prove its exact sourcefree readset."""
    owner.store.verify()
    snapshot = owner.snapshot() if expected is None else expected
    result = owner.realize(operation_id, proposal, snapshot)
    consequences = result.consequences if isinstance(result.consequences, Mapping) else {}
    _walk_claims(consequences, "consequences")
    if consequences.get("durable_psychological_transition") != "MISSING_RULE":
        _refuse("D01_DURABLE_TRANSITION_CLAIM")
    response = validate_sourcefree_response(
        consequences.get("test_only_psychological"), exact=True)
    actor_surface = _mapping(result.accessible, "D01_ACTOR_SURFACE")
    projected = _mapping(consequences.get("test_only_actor_surface"),
                         "D01_PROJECTED_ACTOR_SURFACE")
    if detached(actor_surface) != detached(projected):
        _refuse("D01_ACTOR_SURFACE_MISMATCH")
    _reject_private_keys(actor_surface)
    operation = owner.store.get_operation(operation_id)
    if not isinstance(operation, Mapping) or operation.get("phase") != "COMPLETE":
        _refuse("D01_OPERATION_NOT_COMPLETE")
    receipt = operation.get("effects_receipt")
    if not isinstance(receipt, Mapping):
        _refuse("D01_EFFECTS_RECEIPT_MISSING")
    if receipt.get("authority") != "TEST_ONLY" or receipt.get("grade") != GRADE:
        _refuse("D01_RECEIPT_AUTHORITY")
    if receipt.get("native_science") != "NOT_ISSUED" or receipt.get("production") is not False:
        _refuse("D01_RECEIPT_NATIVE_CLAIM")
    _walk_claims(receipt, "receipt")
    if detached(receipt.get("response")) != response:
        _refuse("D01_RECEIPT_RESPONSE_MISMATCH")
    record_hashes = [
        stream["record_hash"] for stream in response.get("streams", [])
        if isinstance(stream, Mapping) and isinstance(stream.get("record_hash"), str)
    ]
    if require_record_hashes is not None:
        required = {_hash(value, "D01_REQUIRED_RECORD_HASH")
                    for value in require_record_hashes}
        if not required <= set(record_hashes):
            _refuse("D01_LATER_CONSUMER_RECORD_MISSING")
        if not required <= set(result.readset):
            _refuse("D01_LATER_CONSUMER_READSET_MISSING")
    return {
        "schema": "SOROK_D01_LATER_CONSUMER@1",
        "operation_id": operation_id,
        "status": result.status,
        "before": result.before.document(),
        "after": result.after.document(),
        "response": response,
        "response_hash": digest(response),
        "effects_receipt_hash": receipt.get("receipt_hash"),
        "readset": list(result.readset),
        "record_hashes": record_hashes,
        "actor_surface": actor_surface,
        "authority": "SOURCEFREE_TEST_ONLY",
        "native_boundary": {
            "native_rule": response.get("native_rule", "MISSING_RULE"),
            "native_action": response.get("native_action", "NOT_ISSUED_BY_P3_RULE"),
            "durable_psychological_transition": "MISSING_RULE",
            "memory_formation": "MISSING_RULE",
        },
    }


__all__ = [
    "GRADE",
    "SELECTED_KIND",
    "SELECTED_RULE",
    "later_consumer",
    "load_cold_config",
    "open_cold_owner",
    "producer_identity",
    "read_sourcefree_records",
    "recover_missing_config",
    "validate_sourcefree_response",
]
