"""OBL059 R11 bounded repair: stable composed Mapping semantic preservation.

R11 preserves frozen R10 whenever R10 can already establish its coherent
entry view.  When R10 cannot reduce a lawful composed Mapping to one direct
backing dict, R11 obtains the Mapping's observable semantic view only in
isolated forked child state.  The child requires a bounded pre/post entry-state
signature to remain unchanged and requires repeated Mapping materialization to
produce the same exact built-in view.  The parent accepts only identical
results from repeated isolated snapshots.  If a coherent stable view cannot be
established, R10's deterministic negative handling remains authoritative.

No project-current state or runtime effect is created.
"""
from __future__ import annotations

import gc
import importlib.util
import json
import os
import select
import signal
import struct
from collections.abc import Mapping as ABCMapping
from pathlib import Path
from typing import Any, Dict, Mapping

_R10_PATH = (
    Path(__file__).resolve().parents[1]
    / "OBL059_POSITIVE_APPLICABILITY_R10"
    / "positive_applicability_authority_r10.py"
)
_spec = importlib.util.spec_from_file_location("_obl059_r10_authority_for_r11", _R10_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load frozen OBL059 R10 authority: {_R10_PATH}")
_r10 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r10)

AUTHORITY_ID = _r10.AUTHORITY_ID
RECEIPT_VERSION = _r10.RECEIPT_VERSION
FIRST_CANARY_SUBJECT_ID = _r10.FIRST_CANARY_SUBJECT_ID
SUBJECT_CLASSIFICATION_PREDICATE = _r10.SUBJECT_CLASSIFICATION_PREDICATE
ADP007_OWNER = _r10.ADP007_OWNER
ADP008_OWNER = _r10.ADP008_OWNER
ADP010_CONSUMER = _r10.ADP010_CONSUMER
SYNTHETIC_SCOPE = _r10.SYNTHETIC_SCOPE
POSITIVE_DECISION = _r10.POSITIVE_DECISION
NEGATIVE_DECISION = _r10.NEGATIVE_DECISION
FORBIDDEN_ALIAS_AUTHORITIES = _r10.FORBIDDEN_ALIAS_AUTHORITIES
_REQUIRED_BINDINGS = tuple(_r10._REQUIRED_BINDINGS)
_EVIDENCE_COMPONENT_KEYS = tuple(_r10._EVIDENCE_COMPONENT_KEYS)

R11_CANDIDATE_REVISION = "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R11"
_SNAPSHOT_TIMEOUT_SECONDS = 2.0
_MAX_DEPTH = 128
_MAX_ITEMS = 16384
_MAX_PAYLOAD_BYTES = 4_000_000
_PATH_ORDER = dict(_r10._PATH_ORDER)


class _SnapshotUnavailable(Exception):
    pass


def _primitive_token(value: Any) -> Any:
    value_type = type(value)
    if value is None:
        return ["none"]
    if value_type is bool:
        return ["bool", value]
    if value_type is int:
        magnitude = value if value >= 0 else -value
        bits = int.bit_length(magnitude)
        raw = int.to_bytes(magnitude, max(1, (bits + 7) // 8), "big", signed=False)
        return ["int", -1 if value < 0 else 1, bits, raw.hex()]
    if value_type is float:
        return ["float", struct.pack("!d", value).hex()]
    if value_type is str:
        return ["str", value]
    if value_type is bytes:
        return ["bytes", value.hex()]
    raise _SnapshotUnavailable("not an exact primitive")


def _state_token(value: Any, active: set[int] | None = None, depth: int = 0) -> Any:
    """Bounded raw-state signature without invoking Mapping protocol methods."""
    if active is None:
        active = set()
    if depth > _MAX_DEPTH:
        raise _SnapshotUnavailable("state depth exceeded")

    value_type = type(value)
    if value is None or value_type in (str, bool, int, float, bytes):
        return _primitive_token(value)

    marker = id(value)
    if marker in active:
        return ["cycle", value_type.__module__, value_type.__qualname__, marker]

    if value_type is dict:
        active.add(marker)
        try:
            pairs = []
            for index, (key, item) in enumerate(dict.items(value)):
                if index >= _MAX_ITEMS:
                    raise _SnapshotUnavailable("state breadth exceeded")
                kt = _state_token(key, active, depth + 1)
                vt = _state_token(item, active, depth + 1)
                pairs.append([kt, vt])
            pairs.sort(key=lambda pair: json.dumps(pair[0], sort_keys=True, separators=(",", ":")))
            return ["dict", pairs]
        finally:
            active.remove(marker)

    if value_type in (list, tuple):
        active.add(marker)
        try:
            iterator = list.__iter__(value) if value_type is list else tuple.__iter__(value)
            items = []
            for index, item in enumerate(iterator):
                if index >= _MAX_ITEMS:
                    raise _SnapshotUnavailable("state breadth exceeded")
                items.append(_state_token(item, active, depth + 1))
            return [value_type.__name__, items]
        finally:
            active.remove(marker)

    if value_type in (set, frozenset):
        active.add(marker)
        try:
            iterator = set.__iter__(value) if value_type is set else frozenset.__iter__(value)
            items = []
            for index, item in enumerate(iterator):
                if index >= _MAX_ITEMS:
                    raise _SnapshotUnavailable("state breadth exceeded")
                items.append(_state_token(item, active, depth + 1))
            items.sort(key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
            return [value_type.__name__, items]
        finally:
            active.remove(marker)

    active.add(marker)
    try:
        state = None
        try:
            candidate = object.__getattribute__(value, "__dict__")
            if type(candidate) is dict:
                state = candidate
        except BaseException:
            state = None

        refs = []
        try:
            for ref in gc.get_referents(value):
                if ref is state:
                    continue
                if type(ref) in (dict, list, tuple, set, frozenset):
                    refs.append(_state_token(ref, active, depth + 1))
        except BaseException:
            raise _SnapshotUnavailable("raw referents unavailable")

        if state is None and not refs:
            raise _SnapshotUnavailable("opaque custom state")
        refs.sort(key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
        return [
            "object",
            value_type.__module__,
            value_type.__qualname__,
            _state_token(state, active, depth + 1) if state is not None else None,
            refs,
        ]
    finally:
        active.remove(marker)


def _materialize(value: Any, active: set[int] | None = None, depth: int = 0) -> Any:
    """Materialize lawful observable Mapping semantics to exact built-ins."""
    if active is None:
        active = set()
    if depth > _MAX_DEPTH:
        raise _SnapshotUnavailable("semantic depth exceeded")

    value_type = type(value)
    if value is None or value_type in (str, bool, int, float, bytes):
        return value

    marker = id(value)
    if marker in active:
        raise _SnapshotUnavailable("semantic cycle")

    if value_type is dict:
        active.add(marker)
        try:
            out = {}
            for index, (key, item) in enumerate(dict.items(value)):
                if index >= _MAX_ITEMS:
                    raise _SnapshotUnavailable("semantic breadth exceeded")
                out[_materialize(key, active, depth + 1)] = _materialize(item, active, depth + 1)
            return out
        finally:
            active.remove(marker)

    if value_type is list:
        active.add(marker)
        try:
            return [_materialize(item, active, depth + 1) for item in list.__iter__(value)]
        finally:
            active.remove(marker)

    if value_type is tuple:
        active.add(marker)
        try:
            return tuple(_materialize(item, active, depth + 1) for item in tuple.__iter__(value))
        finally:
            active.remove(marker)

    if value_type is set:
        active.add(marker)
        try:
            return set(_materialize(item, active, depth + 1) for item in set.__iter__(value))
        finally:
            active.remove(marker)

    if value_type is frozenset:
        active.add(marker)
        try:
            return frozenset(_materialize(item, active, depth + 1) for item in frozenset.__iter__(value))
        finally:
            active.remove(marker)

    if isinstance(value, ABCMapping):
        active.add(marker)
        try:
            observed = dict(value)
            return _materialize(observed, active, depth + 1)
        finally:
            active.remove(marker)

    raise _SnapshotUnavailable("unsupported custom semantic value")


def _wire_encode(value: Any) -> Any:
    value_type = type(value)
    if value is None:
        return ["N"]
    if value_type is bool:
        return ["Q", value]
    if value_type is str:
        return ["S", value]
    if value_type is int:
        magnitude = value if value >= 0 else -value
        bits = int.bit_length(magnitude)
        raw = int.to_bytes(magnitude, max(1, (bits + 7) // 8), "big", signed=False)
        return ["I", -1 if value < 0 else 1, raw.hex()]
    if value_type is float:
        return ["F", struct.pack("!d", value).hex()]
    if value_type is bytes:
        return ["B", value.hex()]
    if value_type is dict:
        return ["D", [[_wire_encode(k), _wire_encode(v)] for k, v in dict.items(value)]]
    if value_type is list:
        return ["L", [_wire_encode(v) for v in list.__iter__(value)]]
    if value_type is tuple:
        return ["T", [_wire_encode(v) for v in tuple.__iter__(value)]]
    if value_type is set:
        items = [_wire_encode(v) for v in set.__iter__(value)]
        items.sort(key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
        return ["E", items]
    if value_type is frozenset:
        items = [_wire_encode(v) for v in frozenset.__iter__(value)]
        items.sort(key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
        return ["R", items]
    raise _SnapshotUnavailable("wire value unsupported")


def _wire_decode(token: Any) -> Any:
    tag = token[0]
    if tag == "N":
        return None
    if tag == "Q":
        return bool(token[1])
    if tag == "S":
        return token[1]
    if tag == "I":
        magnitude = int.from_bytes(bytes.fromhex(token[2]), "big", signed=False)
        return -magnitude if token[1] < 0 else magnitude
    if tag == "F":
        return struct.unpack("!d", bytes.fromhex(token[1]))[0]
    if tag == "B":
        return bytes.fromhex(token[1])
    if tag == "D":
        return {_wire_decode(k): _wire_decode(v) for k, v in token[1]}
    if tag == "L":
        return [_wire_decode(v) for v in token[1]]
    if tag == "T":
        return tuple(_wire_decode(v) for v in token[1])
    if tag == "E":
        return set(_wire_decode(v) for v in token[1])
    if tag == "R":
        return frozenset(_wire_decode(v) for v in token[1])
    raise _SnapshotUnavailable("unknown wire tag")


def _child_payload(root: Any, target: ABCMapping) -> bytes:
    try:
        before = _state_token(root)
        first = _materialize(target)
        middle = _state_token(root)
        second = _materialize(target)
        after = _state_token(root)
        first_wire = _wire_encode(first)
        second_wire = _wire_encode(second)
        if before != middle or middle != after or first_wire != second_wire:
            return b'{"ok":false}'
        payload = json.dumps({"ok": True, "view": first_wire}, sort_keys=True, separators=(",", ":")).encode("utf-8")
        if len(payload) > _MAX_PAYLOAD_BYTES:
            return b'{"ok":false}'
        return payload
    except BaseException:
        return b'{"ok":false}'


def _fork_once(root: Any, target: ABCMapping) -> bytes | None:
    if not hasattr(os, "fork"):
        return None
    read_fd, write_fd = os.pipe()
    pid = os.fork()
    if pid == 0:
        try:
            os.close(read_fd)
            payload = _child_payload(root, target)
            with os.fdopen(write_fd, "wb", buffering=0) as handle:
                handle.write(payload)
        finally:
            os._exit(0)

    os.close(write_fd)
    try:
        ready, _, _ = select.select([read_fd], [], [], _SNAPSHOT_TIMEOUT_SECONDS)
        if not ready:
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass
            os.waitpid(pid, 0)
            return None
        chunks = []
        total = 0
        while True:
            chunk = os.read(read_fd, 65536)
            if not chunk:
                break
            total += len(chunk)
            if total > _MAX_PAYLOAD_BYTES:
                try:
                    os.kill(pid, signal.SIGKILL)
                except OSError:
                    pass
                os.waitpid(pid, 0)
                return None
            chunks.append(chunk)
        _, status = os.waitpid(pid, 0)
        if status != 0:
            return None
        payload = b"".join(chunks)
        result = json.loads(payload.decode("utf-8"))
        if not result.get("ok"):
            return None
        return payload
    except BaseException:
        return None
    finally:
        try:
            os.close(read_fd)
        except OSError:
            pass


def _stable_isolated_view(root: Any, target: ABCMapping) -> dict[Any, Any] | None:
    first = _fork_once(root, target)
    if first is None:
        return None
    second = _fork_once(root, target)
    if second is None or second != first:
        return None
    try:
        decoded = json.loads(first.decode("utf-8"))
        view = _wire_decode(decoded["view"])
    except BaseException:
        return None
    return view if type(view) is dict else None


def _entry_source(packet: Mapping[str, Any], path: str) -> Any:
    if path == "outer":
        return packet

    if type(packet) is dict:
        outer = packet
    elif isinstance(packet, ABCMapping):
        outer = _r10._raw_mapping_backing(packet)
    else:
        return None
    if type(outer) is not dict:
        return None

    if path == "opportunity":
        return dict.get(outer, "opportunity")
    evidence = dict.get(outer, "evidence")
    if path == "evidence":
        return evidence

    if type(evidence) is dict:
        evidence_backing = evidence
    elif isinstance(evidence, ABCMapping):
        evidence_backing = _r10._raw_mapping_backing(evidence)
    else:
        return None
    if type(evidence_backing) is not dict:
        return None
    return dict.get(evidence_backing, path)


def _install_view(working: dict[str, Any] | None, path: str, view: dict[Any, Any]) -> dict[str, Any] | None:
    if path == "outer":
        return view
    if working is None:
        return None
    out = _r10._clone_exact(working)
    if path in ("opportunity", "evidence"):
        dict.__setitem__(out, path, view)
        return out
    evidence = dict.get(out, "evidence")
    if type(evidence) is not dict:
        return None
    evidence = _r10._clone_exact(evidence)
    dict.__setitem__(evidence, path, view)
    dict.__setitem__(out, "evidence", evidence)
    return out


def _r10_captures_valid(captures: dict[int, dict[str, Any]]) -> bool:
    ordered = sorted(
        captures.values(),
        key=lambda item: min(_PATH_ORDER.get(path, 999) for path in item["paths"]),
    )
    for item in ordered:
        if not _r10._validate_in_entry_fork(item["carrier"], item["signature"]):
            return False
    return True


def evaluate_direct_positive_applicability(packet: Mapping[str, Any]) -> Dict[str, Any]:
    """Preserve R10, adding only stable composed-Mapping semantic fallback."""
    if type(packet) is not dict and not isinstance(packet, ABCMapping):
        return _r10.evaluate_direct_positive_applicability(packet)

    working, captures, failures = _r10._prepare_entry_view(packet)
    if not failures:
        return _r10.evaluate_direct_positive_applicability(packet)

    if not _r10_captures_valid(captures):
        return _r10.evaluate_direct_positive_applicability(packet)

    installed: dict[int, dict[Any, Any]] = {}
    for path in sorted(set(failures), key=lambda item: _PATH_ORDER.get(item, 999)):
        target = _entry_source(packet, path)
        if not isinstance(target, ABCMapping):
            return _r10.evaluate_direct_positive_applicability(packet)
        marker = id(target)
        view = installed.get(marker)
        if view is None:
            view = _stable_isolated_view(packet, target)
            if view is None:
                return _r10.evaluate_direct_positive_applicability(packet)
            installed[marker] = view
        working = _install_view(working, path, view)
        if working is None:
            return _r10.evaluate_direct_positive_applicability(packet)

    return _r10._r9._evaluate_prepared(working)
