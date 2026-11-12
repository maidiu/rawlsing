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

import json
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
    detached,
    digest,
)
from p3 import p3_owner, test_rules  # noqa: E402

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
    config = _mapping(document.get("config"), "D01_COLD_CONFIG_BODY")
    if set(config) != CONFIG_KEYS:
        _refuse("D01_COLD_CONFIG_KEYS")
    if document.get("config_hash") != digest(config):
        _refuse("D01_COLD_CONFIG_HASH")
    if config["schema"] != CONFIG_SCHEMA:
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
    return owner


def validate_sourcefree_response(response: Any) -> dict:
    """Reject native/durable/first-person claims in a P3 sourcefree response."""
    body = _mapping(response, "D01_RESPONSE_SCHEMA")
    status = _text(body.get("status"), "D01_RESPONSE_STATUS")
    if status.startswith("COMPUTED_TEST_ONLY_RESPONSE"):
        for key in ("native_rule", "native_action", "memory_formation"):
            if key not in body:
                _refuse("D01_RESPONSE_BOUNDARY_MISSING:" + key)
    _walk_claims(body)
    return body


def _validate_record(record: Any, *, owner: Any, as_of: int) -> dict:
    value = _mapping(record, "D01_RECORD_SCHEMA")
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
    if not isinstance(parents, list) or not parents or not all(
            isinstance(parent, str) and parent for parent in parents):
        _refuse("D01_RECORD_PARENTS")
    if not isinstance(value.get("payload"), Mapping):
        _refuse("D01_RECORD_PAYLOAD")
    return value


def read_sourcefree_records(
    owner: Any,
    *,
    project: str,
    counterpart: str,
    as_of: int,
) -> dict:
    """Read only the selected rule's exact actor-local records at ``as_of``."""
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
    snapshot = owner.snapshot() if expected is None else expected
    result = owner.realize(operation_id, proposal, snapshot)
    consequences = result.consequences if isinstance(result.consequences, Mapping) else {}
    if consequences.get("durable_psychological_transition") != "MISSING_RULE":
        _refuse("D01_DURABLE_TRANSITION_CLAIM")
    response = validate_sourcefree_response(consequences.get("test_only_psychological"))
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
    "validate_sourcefree_response",
]
