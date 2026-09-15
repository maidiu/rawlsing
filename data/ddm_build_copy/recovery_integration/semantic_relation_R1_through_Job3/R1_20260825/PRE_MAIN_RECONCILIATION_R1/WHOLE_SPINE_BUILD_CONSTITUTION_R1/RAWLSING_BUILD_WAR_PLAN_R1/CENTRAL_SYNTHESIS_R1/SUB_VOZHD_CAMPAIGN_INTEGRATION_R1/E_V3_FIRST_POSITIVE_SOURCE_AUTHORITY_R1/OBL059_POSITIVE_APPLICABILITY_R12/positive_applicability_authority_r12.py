"""OBL059 R12 semantic-view redesign: observable Mapping semantics only.

R12 replaces private-state/backing-dict admissibility for custom Mapping
carriers with one reusable observable semantic-view rule.

Custom consumed Mapping nodes are never traversed in parent state.  Each
semantic observation runs in an isolated child fork.  The child repeats the
same bounded observation so harmless cache warming, memoization, lazy indexes
or equivalent private changes are tolerated when the normalized observable
key/value view stays equal.  The parent then requires a second fresh child
observation to agree.  Every consumed path is observed from the same untouched
parent entry state, so one carrier's traversal cannot rewrite a later consumed
semantic view.

Mapping entry order is normalized and is not semantic authority.  Observable
view disagreement, protocol failure, cycles that cannot be materialized, size
or depth limits, timeouts, or inability to obtain one stable view fail closed
through the inherited deterministic negative semantics.

No project-current state or runtime effect is created.
"""
from __future__ import annotations

import importlib.util
import json
import os
import select
import signal
import struct
import threading
from collections.abc import Mapping as ABCMapping
from pathlib import Path
from typing import Any, Dict, Mapping

_R11_PATH = (
    Path(__file__).resolve().parents[1]
    / "OBL059_POSITIVE_APPLICABILITY_R11"
    / "positive_applicability_authority_r11.py"
)
_spec = importlib.util.spec_from_file_location("_obl059_r11_authority_for_r12", _R11_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load frozen OBL059 R11 authority: {_R11_PATH}")
_r11 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r11)

AUTHORITY_ID = _r11.AUTHORITY_ID
RECEIPT_VERSION = _r11.RECEIPT_VERSION
FIRST_CANARY_SUBJECT_ID = _r11.FIRST_CANARY_SUBJECT_ID
SUBJECT_CLASSIFICATION_PREDICATE = _r11.SUBJECT_CLASSIFICATION_PREDICATE
ADP007_OWNER = _r11.ADP007_OWNER
ADP008_OWNER = _r11.ADP008_OWNER
ADP010_CONSUMER = _r11.ADP010_CONSUMER
SYNTHETIC_SCOPE = _r11.SYNTHETIC_SCOPE
POSITIVE_DECISION = _r11.POSITIVE_DECISION
NEGATIVE_DECISION = _r11.NEGATIVE_DECISION
FORBIDDEN_ALIAS_AUTHORITIES = _r11.FORBIDDEN_ALIAS_AUTHORITIES
_REQUIRED_BINDINGS = tuple(_r11._REQUIRED_BINDINGS)
_EVIDENCE_COMPONENT_KEYS = tuple(_r11._EVIDENCE_COMPONENT_KEYS)

R12_CANDIDATE_REVISION = "OBL059_POSITIVE_APPLICABILITY_SEMANTIC_VIEW_REDESIGN_R12"

_OBSERVATION_TIMEOUT_SECONDS = 2.0
_MAX_DEPTH = 128
_MAX_ITEMS = 16384
_MAX_PAYLOAD_BYTES = 4_000_000
_FORK_LOCK = threading.RLock()

_MISSING = object()
_PLACEHOLDER = object()


class _ObservableViewUnavailable(Exception):
    pass


def _token_key(token: Any) -> str:
    return json.dumps(token, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _wire(value: Any, active: set[int] | None = None, depth: int = 0) -> Any:
    """Normalize exact/Mapping observable values without decimal-rendering ints."""
    if active is None:
        active = set()
    if depth > _MAX_DEPTH:
        raise _ObservableViewUnavailable("semantic depth exceeded")

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

    marker = id(value)
    if marker in active:
        raise _ObservableViewUnavailable("semantic cycle")

    if value_type is dict:
        active.add(marker)
        try:
            entries = []
            for index, (key, item) in enumerate(dict.items(value)):
                if index >= _MAX_ITEMS:
                    raise _ObservableViewUnavailable("semantic breadth exceeded")
                kt = _wire(key, active, depth + 1)
                vt = _wire(item, active, depth + 1)
                entries.append([kt, vt])
            entries.sort(key=lambda pair: _token_key(pair[0]))
            return ["D", entries]
        finally:
            active.remove(marker)

    if value_type is list:
        active.add(marker)
        try:
            out = []
            for index, item in enumerate(list.__iter__(value)):
                if index >= _MAX_ITEMS:
                    raise _ObservableViewUnavailable("semantic breadth exceeded")
                out.append(_wire(item, active, depth + 1))
            return ["L", out]
        finally:
            active.remove(marker)

    if value_type is tuple:
        active.add(marker)
        try:
            out = []
            for index, item in enumerate(tuple.__iter__(value)):
                if index >= _MAX_ITEMS:
                    raise _ObservableViewUnavailable("semantic breadth exceeded")
                out.append(_wire(item, active, depth + 1))
            return ["T", out]
        finally:
            active.remove(marker)

    if value_type in (set, frozenset):
        active.add(marker)
        try:
            iterator = set.__iter__(value) if value_type is set else frozenset.__iter__(value)
            out = []
            for index, item in enumerate(iterator):
                if index >= _MAX_ITEMS:
                    raise _ObservableViewUnavailable("semantic breadth exceeded")
                out.append(_wire(item, active, depth + 1))
            out.sort(key=_token_key)
            return ["E" if value_type is set else "R", out]
        finally:
            active.remove(marker)

    if isinstance(value, ABCMapping):
        active.add(marker)
        try:
            observed = dict(value)
            entries = []
            for index, (key, item) in enumerate(dict.items(observed)):
                if index >= _MAX_ITEMS:
                    raise _ObservableViewUnavailable("semantic breadth exceeded")
                kt = _wire(key, active, depth + 1)
                vt = _wire(item, active, depth + 1)
                entries.append([kt, vt])
            entries.sort(key=lambda pair: _token_key(pair[0]))
            return ["D", entries]
        finally:
            active.remove(marker)

    raise _ObservableViewUnavailable("unsupported semantic value")


def _unwire(token: Any) -> Any:
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
        return {_unwire(key): _unwire(value) for key, value in token[1]}
    if tag == "L":
        return [_unwire(value) for value in token[1]]
    if tag == "T":
        return tuple(_unwire(value) for value in token[1])
    if tag == "E":
        return set(_unwire(value) for value in token[1])
    if tag == "R":
        return frozenset(_unwire(value) for value in token[1])
    raise _ObservableViewUnavailable("unknown semantic wire tag")


def _mapping_entries(value: Any) -> list[tuple[Any, Any]]:
    if type(value) is dict:
        return list(dict.items(value))
    if isinstance(value, ABCMapping):
        return list(dict.items(dict(value)))
    raise _ObservableViewUnavailable("target is not a Mapping")


def _resolve_path(root: Any, path: tuple[str, ...]) -> Any:
    current = root
    for key in path:
        if type(current) is dict:
            if not dict.__contains__(current, key):
                return _MISSING
            current = dict.__getitem__(current, key)
            continue
        if isinstance(current, ABCMapping):
            try:
                current = current[key]
            except KeyError:
                return _MISSING
            continue
        return _MISSING
    return current


def _shallow_token(value: Any, placeholder_keys: frozenset[str]) -> Any:
    if not isinstance(value, ABCMapping):
        return ["V", _wire(value)]

    entries = []
    for index, (key, item) in enumerate(_mapping_entries(value)):
        if index >= _MAX_ITEMS:
            raise _ObservableViewUnavailable("semantic breadth exceeded")
        kt = _wire(key)
        if type(key) is str and key in placeholder_keys and isinstance(item, ABCMapping):
            vt = ["P"]
        else:
            vt = ["V", _wire(item)]
        entries.append([kt, vt])
    entries.sort(key=lambda pair: _token_key(pair[0]))
    return ["M", entries]


def _observation_token(
    root: Any,
    path: tuple[str, ...],
    placeholder_keys: frozenset[str] | None,
) -> Any:
    target = _resolve_path(root, path)
    if target is _MISSING:
        return ["Z"]
    if placeholder_keys is None:
        return ["V", _wire(target)]
    return _shallow_token(target, placeholder_keys)


def _child_payload(
    root: Any,
    path: tuple[str, ...],
    placeholder_keys: frozenset[str] | None,
) -> bytes:
    try:
        first = _observation_token(root, path, placeholder_keys)
        second = _observation_token(root, path, placeholder_keys)
        if first != second:
            return b'{"ok":false}'
        payload = json.dumps(
            {"ok": True, "token": first},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
        if len(payload) > _MAX_PAYLOAD_BYTES:
            return b'{"ok":false}'
        return payload
    except BaseException:
        return b'{"ok":false}'


def _fork_once(
    root: Any,
    path: tuple[str, ...],
    placeholder_keys: frozenset[str] | None,
) -> bytes | None:
    if not hasattr(os, "fork"):
        return None

    read_fd, write_fd = os.pipe()
    pid = os.fork()
    if pid == 0:
        try:
            os.close(read_fd)
            payload = _child_payload(root, path, placeholder_keys)
            with os.fdopen(write_fd, "wb", buffering=0) as handle:
                handle.write(payload)
        finally:
            os._exit(0)

    os.close(write_fd)
    try:
        ready, _, _ = select.select([read_fd], [], [], _OBSERVATION_TIMEOUT_SECONDS)
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
        decoded = json.loads(payload.decode("utf-8"))
        if not decoded.get("ok"):
            return None
        return payload
    except BaseException:
        return None
    finally:
        try:
            os.close(read_fd)
        except OSError:
            pass


def _stable_observation(
    root: Any,
    path: tuple[str, ...] = (),
    placeholder_keys: frozenset[str] | None = None,
) -> Any | None:
    """Return one agreed normalized observation token from two fresh children."""
    with _FORK_LOCK:
        first = _fork_once(root, path, placeholder_keys)
        if first is None:
            return None
        second = _fork_once(root, path, placeholder_keys)
        if second is None or second != first:
            return None
    try:
        decoded = json.loads(first.decode("utf-8"))
        return decoded["token"]
    except BaseException:
        return None


def _decode_token(token: Any) -> tuple[str, Any, set[str]]:
    tag = token[0]
    if tag == "Z":
        return "missing", None, set()
    if tag == "V":
        return "value", _unwire(token[1]), set()
    if tag != "M":
        raise _ObservableViewUnavailable("invalid observation token")

    out: dict[Any, Any] = {}
    placeholders: set[str] = set()
    for key_token, value_token in token[1]:
        key = _unwire(key_token)
        if value_token[0] == "P":
            out[key] = _PLACEHOLDER
            if type(key) is str:
                placeholders.add(key)
        elif value_token[0] == "V":
            out[key] = _unwire(value_token[1])
        else:
            raise _ObservableViewUnavailable("invalid shallow value token")
    return "mapping", out, placeholders


def _observe_decoded(
    root: Any,
    path: tuple[str, ...] = (),
    placeholder_keys: frozenset[str] | None = None,
) -> tuple[bool, str, Any, set[str]]:
    token = _stable_observation(root, path, placeholder_keys)
    if token is None:
        return False, "failed", None, set()
    try:
        kind, value, placeholders = _decode_token(token)
    except BaseException:
        return False, "failed", None, set()
    return True, kind, value, placeholders


def _has_custom_consumed_mapping(packet: Any) -> bool:
    if type(packet) is not dict:
        return isinstance(packet, ABCMapping)

    opportunity = dict.get(packet, "opportunity")
    if isinstance(opportunity, ABCMapping) and type(opportunity) is not dict:
        return True

    evidence = dict.get(packet, "evidence")
    if isinstance(evidence, ABCMapping) and type(evidence) is not dict:
        return True
    if type(evidence) is dict:
        for key in _EVIDENCE_COMPONENT_KEYS:
            component = dict.get(evidence, key)
            if isinstance(component, ABCMapping) and type(component) is not dict:
                return True
    return False


def _set_failure(working: dict[str, Any], path: str) -> None:
    if path == "opportunity":
        dict.__setitem__(working, "opportunity", None)
        return
    if path == "evidence":
        dict.__setitem__(working, "evidence", None)
        return
    evidence = dict.get(working, "evidence")
    if type(evidence) is dict:
        evidence_copy = _r11._r10._clone_exact(evidence)
        dict.__setitem__(evidence_copy, path, None)
        dict.__setitem__(working, "evidence", evidence_copy)


def _prepare_exact_outer(packet: dict[str, Any]) -> dict[str, Any]:
    """Observe only custom consumed nodes; exact parent slots use built-in reads."""
    working = _r11._r10._clone_exact(packet)

    opportunity_source = dict.get(packet, "opportunity")
    if isinstance(opportunity_source, ABCMapping) and type(opportunity_source) is not dict:
        ok, kind, value, _ = _observe_decoded(opportunity_source)
        if not ok or kind != "value" or type(value) is not dict:
            _set_failure(working, "opportunity")
        else:
            dict.__setitem__(working, "opportunity", value)

    evidence_source = dict.get(packet, "evidence")
    if isinstance(evidence_source, ABCMapping) and type(evidence_source) is not dict:
        ok, kind, evidence_view, placeholders = _observe_decoded(
            evidence_source,
            (),
            frozenset(_EVIDENCE_COMPONENT_KEYS),
        )
        if not ok or kind != "mapping" or type(evidence_view) is not dict:
            _set_failure(working, "evidence")
            return working

        for key in _EVIDENCE_COMPONENT_KEYS:
            if key not in placeholders:
                continue
            ok, component_kind, component_view, _ = _observe_decoded(
                evidence_source,
                (key,),
                None,
            )
            if not ok or component_kind != "value" or type(component_view) is not dict:
                dict.__setitem__(evidence_view, key, None)
            else:
                dict.__setitem__(evidence_view, key, component_view)
        dict.__setitem__(working, "evidence", evidence_view)
        return working

    if type(evidence_source) is dict:
        evidence_working = _r11._r10._clone_exact(evidence_source)
        for key in _EVIDENCE_COMPONENT_KEYS:
            component = dict.get(evidence_source, key)
            if isinstance(component, ABCMapping) and type(component) is not dict:
                ok, kind, component_view, _ = _observe_decoded(component)
                if not ok or kind != "value" or type(component_view) is not dict:
                    dict.__setitem__(evidence_working, key, None)
                else:
                    dict.__setitem__(evidence_working, key, component_view)
        dict.__setitem__(working, "evidence", evidence_working)

    return working


def _prepare_custom_outer(packet: ABCMapping) -> dict[str, Any] | None:
    """Build the consumed packet from path observations rooted at one entry state."""
    ok, kind, outer_view, outer_placeholders = _observe_decoded(
        packet,
        (),
        frozenset(("opportunity", "evidence")),
    )
    if not ok or kind != "mapping" or type(outer_view) is not dict:
        return None

    if "opportunity" in outer_placeholders:
        ok, opp_kind, opportunity_view, _ = _observe_decoded(packet, ("opportunity",), None)
        if not ok or opp_kind != "value" or type(opportunity_view) is not dict:
            dict.__setitem__(outer_view, "opportunity", None)
        else:
            dict.__setitem__(outer_view, "opportunity", opportunity_view)

    if "evidence" in outer_placeholders:
        ok, ev_kind, evidence_view, evidence_placeholders = _observe_decoded(
            packet,
            ("evidence",),
            frozenset(_EVIDENCE_COMPONENT_KEYS),
        )
        if not ok or ev_kind != "mapping" or type(evidence_view) is not dict:
            dict.__setitem__(outer_view, "evidence", None)
        else:
            for key in _EVIDENCE_COMPONENT_KEYS:
                if key not in evidence_placeholders:
                    continue
                ok, comp_kind, component_view, _ = _observe_decoded(
                    packet,
                    ("evidence", key),
                    None,
                )
                if not ok or comp_kind != "value" or type(component_view) is not dict:
                    dict.__setitem__(evidence_view, key, None)
                else:
                    dict.__setitem__(evidence_view, key, component_view)
            dict.__setitem__(outer_view, "evidence", evidence_view)

    # No internal placeholder is allowed to reach semantic evaluation.
    for value in dict.values(outer_view):
        if value is _PLACEHOLDER:
            return None
    evidence = dict.get(outer_view, "evidence")
    if type(evidence) is dict:
        for value in dict.values(evidence):
            if value is _PLACEHOLDER:
                return None
    return outer_view


def evaluate_direct_positive_applicability(packet: Mapping[str, Any]) -> Dict[str, Any]:
    """Evaluate from bounded observable semantic views for every custom carrier."""
    if not isinstance(packet, ABCMapping):
        return _r11.evaluate_direct_positive_applicability(packet)

    # Preserve the fully exact-dict path without introducing process machinery.
    if not _has_custom_consumed_mapping(packet):
        return _r11.evaluate_direct_positive_applicability(packet)

    if type(packet) is dict:
        prepared = _prepare_exact_outer(packet)
    else:
        prepared = _prepare_custom_outer(packet)
        if prepared is None:
            return _r11._r10._r9._r7._existing_packet_malformed_receipt()

    return _r11._r10._r9._evaluate_prepared(prepared)
