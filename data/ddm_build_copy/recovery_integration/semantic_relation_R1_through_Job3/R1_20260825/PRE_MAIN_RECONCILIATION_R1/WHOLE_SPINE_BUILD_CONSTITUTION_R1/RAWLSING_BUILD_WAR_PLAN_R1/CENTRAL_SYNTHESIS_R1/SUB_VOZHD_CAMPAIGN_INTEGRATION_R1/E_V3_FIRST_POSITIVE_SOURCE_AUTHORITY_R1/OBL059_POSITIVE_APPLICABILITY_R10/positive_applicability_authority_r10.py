"""OBL059 R10 bounded repair: coherent entry-state views for consumed custom Mapping carriers.

R10 preserves frozen R9 applicability semantics and its stable oversized-integer
receipt handling.  It changes only preparation of custom Mapping carriers.

Before any Mapping method is invoked, R10 captures an exact built-in view of the
outer packet and every consumed Mapping from backing state that can be read
without invoking Mapping protocol methods.  Each unique custom Mapping is then
validated exactly once in an isolated forked child created from the same untouched
parent entry state.  Child-local traversal changes cannot alter another carrier or
the parent entry view.  If an entry view cannot be established or a carrier's
one-shot Mapping traversal does not match that entry view, R10 uses the existing
deterministic negative outcome for the corresponding field.

No project-current state or runtime effect is created.
"""
from __future__ import annotations

import gc
import hashlib
import importlib.util
import json
import os
import select
import signal
import struct
from collections.abc import Mapping as ABCMapping
from pathlib import Path
from typing import Any, Dict, Mapping

_R9_PATH = (
    Path(__file__).resolve().parents[1]
    / "OBL059_POSITIVE_APPLICABILITY_R9"
    / "positive_applicability_authority_r9.py"
)
_spec = importlib.util.spec_from_file_location("_obl059_r9_authority_for_r10", _R9_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load frozen OBL059 R9 authority: {_R9_PATH}")
_r9 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r9)

AUTHORITY_ID = _r9.AUTHORITY_ID
RECEIPT_VERSION = _r9.RECEIPT_VERSION
FIRST_CANARY_SUBJECT_ID = _r9.FIRST_CANARY_SUBJECT_ID
SUBJECT_CLASSIFICATION_PREDICATE = _r9.SUBJECT_CLASSIFICATION_PREDICATE
ADP007_OWNER = _r9.ADP007_OWNER
ADP008_OWNER = _r9.ADP008_OWNER
ADP010_CONSUMER = _r9.ADP010_CONSUMER
SYNTHETIC_SCOPE = _r9.SYNTHETIC_SCOPE
POSITIVE_DECISION = _r9.POSITIVE_DECISION
NEGATIVE_DECISION = _r9.NEGATIVE_DECISION
FORBIDDEN_ALIAS_AUTHORITIES = _r9.FORBIDDEN_ALIAS_AUTHORITIES
_REQUIRED_BINDINGS = tuple(_r9._REQUIRED_BINDINGS)
_EVIDENCE_COMPONENT_KEYS = tuple(_r9._EVIDENCE_COMPONENT_KEYS)

R10_CANDIDATE_REVISION = "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R10"
_VALIDATION_TIMEOUT_SECONDS = 2.0
_SIGNATURE_MAX_DEPTH = 128
_SIGNATURE_MAX_ITEMS = 16384

_PATH_ORDER = {
    "outer": 0,
    "opportunity": 1,
    "evidence": 2,
    "subject_classification": 3,
    "actor_activation": 4,
    "developmental_phase": 5,
}

_NODE_REASONS = {
    "opportunity": "OPPORTUNITY_BINDING_MISSING_OR_MALFORMED",
    "evidence": "EVIDENCE_MISSING_OR_MALFORMED",
    "subject_classification": "STRUCTURAL_CLASSIFICATION_EVIDENCE_MISSING",
    "actor_activation": "ACTOR_ACTIVATION_EVIDENCE_MISSING",
    "developmental_phase": "DEVELOPMENTAL_PHASE_EVIDENCE_MISSING",
}


class _ViewUnavailable(Exception):
    pass


def _raw_mapping_backing(value: ABCMapping) -> Mapping[str, Any] | None:
    """Return Mapping backing state without invoking Mapping protocol methods."""
    if isinstance(value, dict):
        return value

    state = None
    try:
        state = object.__getattribute__(value, "__dict__")
    except Exception:
        state = None

    preferred = []
    candidates = []
    if type(state) is dict:
        for name, item in dict.items(state):
            if type(item) is dict:
                candidates.append(item)
                if name in {"_data", "data", "_mapping", "mapping", "_store", "store"}:
                    preferred.append(item)

    try:
        for item in gc.get_referents(value):
            if type(item) is dict and item is not state:
                candidates.append(item)
    except Exception:
        return None

    def unique(items):
        out = []
        seen = set()
        for item in items:
            marker = id(item)
            if marker not in seen:
                seen.add(marker)
                out.append(item)
        return out

    preferred = unique(preferred)
    candidates = unique(candidates)
    if len(preferred) == 1:
        return preferred[0]
    if len(candidates) == 1:
        return candidates[0]
    return None


def _clone_exact(value: Any, memo: dict[int, Any] | None = None, depth: int = 0) -> Any:
    """Copy exact built-in mutable containers without invoking custom methods."""
    if memo is None:
        memo = {}
    if depth > _SIGNATURE_MAX_DEPTH:
        raise _ViewUnavailable("entry view depth exceeded")

    value_type = type(value)
    if value_type in (type(None), str, bool, int, float, bytes):
        return value

    marker = id(value)
    if marker in memo:
        return memo[marker]

    if value_type is dict:
        out: dict[Any, Any] = {}
        memo[marker] = out
        count = 0
        for key, item in dict.items(value):
            count += 1
            if count > _SIGNATURE_MAX_ITEMS:
                raise _ViewUnavailable("entry view breadth exceeded")
            out[_clone_exact(key, memo, depth + 1)] = _clone_exact(item, memo, depth + 1)
        return out

    if value_type is list:
        out_list: list[Any] = []
        memo[marker] = out_list
        for index, item in enumerate(list.__iter__(value)):
            if index >= _SIGNATURE_MAX_ITEMS:
                raise _ViewUnavailable("entry view breadth exceeded")
            out_list.append(_clone_exact(item, memo, depth + 1))
        return out_list

    if value_type is tuple:
        items = []
        for index, item in enumerate(tuple.__iter__(value)):
            if index >= _SIGNATURE_MAX_ITEMS:
                raise _ViewUnavailable("entry view breadth exceeded")
            items.append(_clone_exact(item, memo, depth + 1))
        out_tuple = tuple(items)
        memo[marker] = out_tuple
        return out_tuple

    # set/frozenset and arbitrary objects remain referenced. Mapping traversal
    # validation happens in isolated children and cannot mutate parent memory.
    return value


def _int_token(value: int) -> list[Any]:
    magnitude = value if value >= 0 else -value
    bits = int.bit_length(magnitude)
    payload = int.to_bytes(magnitude, max(1, (bits + 7) // 8), "big", signed=False)
    return ["int", -1 if value < 0 else 1, bits, hashlib.sha256(payload).hexdigest()]


def _signature(value: Any, active: set[int] | None = None, depth: int = 0) -> Any:
    """JSON-safe structural signature using exact built-in operations only."""
    if active is None:
        active = set()
    if depth > _SIGNATURE_MAX_DEPTH:
        raise _ViewUnavailable("signature depth exceeded")

    value_type = type(value)
    if value is None:
        return ["none"]
    if value_type is bool:
        return ["bool", value]
    if value_type is int:
        return _int_token(value)
    if value_type is float:
        return ["float", struct.pack("!d", value).hex()]
    if value_type is str:
        return ["str", value]
    if value_type is bytes:
        return ["bytes", len(value), hashlib.sha256(value).hexdigest()]

    marker = id(value)
    if marker in active:
        return ["cycle", value_type.__module__, value_type.__qualname__]

    if value_type is dict or isinstance(value, dict):
        active.add(marker)
        try:
            pairs = []
            for index, (key, item) in enumerate(dict.items(value)):
                if index >= _SIGNATURE_MAX_ITEMS:
                    raise _ViewUnavailable("signature breadth exceeded")
                pairs.append([
                    _signature(key, active, depth + 1),
                    _signature(item, active, depth + 1),
                ])
            pairs.sort(key=lambda pair: json.dumps(pair[0], sort_keys=True, separators=(",", ":")))
            return ["dict", pairs]
        finally:
            active.remove(marker)

    if value_type is list:
        active.add(marker)
        try:
            items = []
            for index, item in enumerate(list.__iter__(value)):
                if index >= _SIGNATURE_MAX_ITEMS:
                    raise _ViewUnavailable("signature breadth exceeded")
                items.append(_signature(item, active, depth + 1))
            return ["list", items]
        finally:
            active.remove(marker)

    if value_type is tuple:
        active.add(marker)
        try:
            items = []
            for index, item in enumerate(tuple.__iter__(value)):
                if index >= _SIGNATURE_MAX_ITEMS:
                    raise _ViewUnavailable("signature breadth exceeded")
                items.append(_signature(item, active, depth + 1))
            return ["tuple", items]
        finally:
            active.remove(marker)

    if value_type in (set, frozenset):
        active.add(marker)
        try:
            iterator = set.__iter__(value) if value_type is set else frozenset.__iter__(value)
            items = []
            for index, item in enumerate(iterator):
                if index >= _SIGNATURE_MAX_ITEMS:
                    raise _ViewUnavailable("signature breadth exceeded")
                items.append(_signature(item, active, depth + 1))
            items.sort(key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
            return [value_type.__name__, items]
        finally:
            active.remove(marker)

    return ["object", value_type.__module__, value_type.__qualname__, marker]


def _capture_custom(
    path: str,
    value: Any,
    captures: dict[int, dict[str, Any]],
    failures: list[str],
) -> Any:
    if type(value) is dict:
        try:
            return _clone_exact(value)
        except Exception:
            failures.append(path)
            return None
    if not isinstance(value, ABCMapping):
        return value

    marker = id(value)
    existing = captures.get(marker)
    if existing is not None:
        existing["paths"].append(path)
        try:
            return _clone_exact(existing["backing"])
        except Exception:
            failures.append(path)
            return None

    backing = _raw_mapping_backing(value)
    if backing is None:
        failures.append(path)
        return None
    try:
        raw_signature = _signature(backing)
        exact_view = _clone_exact(backing)
    except Exception:
        failures.append(path)
        return None

    captures[marker] = {
        "carrier": value,
        "backing": backing,
        "signature": raw_signature,
        "paths": [path],
    }
    return exact_view


def _prepare_entry_view(packet: Mapping[str, Any]) -> tuple[dict[str, Any] | None, dict[int, dict[str, Any]], list[str]]:
    captures: dict[int, dict[str, Any]] = {}
    failures: list[str] = []

    if type(packet) is dict:
        try:
            outer = _clone_exact(packet)
        except Exception:
            return None, captures, ["outer"]
    else:
        outer = _capture_custom("outer", packet, captures, failures)
        if type(outer) is not dict:
            return None, captures, failures or ["outer"]

    opportunity_source = dict.get(outer, "opportunity")
    evidence_source = dict.get(outer, "evidence")

    safe_opportunity = _capture_custom(
        "opportunity", opportunity_source, captures, failures
    )
    safe_evidence = _capture_custom("evidence", evidence_source, captures, failures)

    if type(safe_evidence) is dict:
        evidence_working = _clone_exact(safe_evidence)
        for key in _EVIDENCE_COMPONENT_KEYS:
            component = dict.get(safe_evidence, key)
            safe_component = _capture_custom(key, component, captures, failures)
            dict.__setitem__(evidence_working, key, safe_component)
        safe_evidence = evidence_working

    working = _clone_exact(outer)
    dict.__setitem__(working, "opportunity", safe_opportunity)
    dict.__setitem__(working, "evidence", safe_evidence)
    return working, captures, failures


def _child_validation_payload(carrier: ABCMapping) -> bytes:
    try:
        snapshot = dict(carrier)
        sig = _signature(snapshot)
        return json.dumps({"ok": True, "signature": sig}, sort_keys=True, separators=(",", ":")).encode("utf-8")
    except BaseException:
        return b'{"ok":false}'


def _validate_in_entry_fork(carrier: ABCMapping, expected_signature: Any) -> bool:
    """Validate one carrier in child memory forked from the untouched parent view."""
    if not hasattr(os, "fork"):
        return False

    read_fd, write_fd = os.pipe()
    pid = os.fork()
    if pid == 0:
        try:
            os.close(read_fd)
            payload = _child_validation_payload(carrier)
            with os.fdopen(write_fd, "wb", buffering=0) as handle:
                handle.write(payload)
        finally:
            os._exit(0)

    os.close(write_fd)
    try:
        ready, _, _ = select.select([read_fd], [], [], _VALIDATION_TIMEOUT_SECONDS)
        if not ready:
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass
            os.waitpid(pid, 0)
            return False

        chunks = []
        while True:
            chunk = os.read(read_fd, 65536)
            if not chunk:
                break
            chunks.append(chunk)
            if sum(len(piece) for piece in chunks) > 4_000_000:
                try:
                    os.kill(pid, signal.SIGKILL)
                except OSError:
                    pass
                os.waitpid(pid, 0)
                return False
        _, status = os.waitpid(pid, 0)
        if status != 0:
            return False
        try:
            result = json.loads(b"".join(chunks).decode("utf-8"))
        except Exception:
            return False
        return bool(result.get("ok")) and result.get("signature") == expected_signature
    finally:
        try:
            os.close(read_fd)
        except OSError:
            pass


def _first_failure_path(paths: list[str]) -> str:
    return min(paths, key=lambda path: _PATH_ORDER.get(path, 999))


def _invalidate_path(working: dict[str, Any], path: str) -> dict[str, Any] | None:
    if path == "outer":
        return None
    out = _clone_exact(working)
    if path == "opportunity":
        dict.__setitem__(out, "opportunity", None)
        return out
    if path == "evidence":
        dict.__setitem__(out, "evidence", None)
        return out
    evidence = dict.get(out, "evidence")
    if type(evidence) is not dict:
        return out
    evidence = _clone_exact(evidence)
    dict.__setitem__(evidence, path, None)
    dict.__setitem__(out, "evidence", evidence)
    return out


def _packet_malformed_receipt() -> Dict[str, Any]:
    return _r9._r7._existing_packet_malformed_receipt()


def evaluate_direct_positive_applicability(packet: Mapping[str, Any]) -> Dict[str, Any]:
    """Evaluate frozen R9 semantics from one coherent pre-traversal Mapping view."""
    if type(packet) is not dict and not isinstance(packet, ABCMapping):
        return _r9.evaluate_direct_positive_applicability(packet)

    working, captures, capture_failures = _prepare_entry_view(packet)
    if working is None:
        return _packet_malformed_receipt()

    if capture_failures:
        path = _first_failure_path(capture_failures)
        invalid = _invalidate_path(working, path)
        if invalid is None:
            return _packet_malformed_receipt()
        return _r9._evaluate_prepared(invalid)

    validation_failures: list[str] = []
    ordered = sorted(
        captures.values(),
        key=lambda item: min(_PATH_ORDER.get(path, 999) for path in item["paths"]),
    )
    for item in ordered:
        if not _validate_in_entry_fork(item["carrier"], item["signature"]):
            validation_failures.extend(item["paths"])

    if validation_failures:
        path = _first_failure_path(validation_failures)
        invalid = _invalidate_path(working, path)
        if invalid is None:
            return _packet_malformed_receipt()
        return _r9._evaluate_prepared(invalid)

    # All custom Mapping semantics were validated from independent forks of the
    # same parent entry state. Evaluation now uses only the captured exact view.
    return _r9._evaluate_prepared(working)
