#!/usr/bin/env python3
"""Golden Thread 0 end-to-end acceptance harness.

This module is deliberately sibling-blind. It defines the integration contract
for WSC002 A-F without importing those worker branches at module import time.
Central integration may use load_integrated_stage_api() once the real stage
modules are present; this independent branch uses injected test doubles.

The harness proves semantic conservation along the currently lawful blocked
baseline. It does not create semantic authority and does not turn a blocked
positive actor path into failure.
"""
from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
import hashlib
import importlib
import json
from typing import Any, Callable, Mapping, Sequence


GT0_SEED_ID = "cssu.r1.afrobarometer.r1.005b474d6eb4253cb166"
GT0_J01A_REF = "ba23b0fc1d22bb35abb8a6e8f9ab6100df8f7564"
GT0_SEED_TYPE = "MATRIX_GRID"
GT0_SEED_LABEL = "Current-versus-past freedoms and equality"
GT0_SEED_MEMBERS = (
    "pfesol",
    "pfrsay",
    "pfrass",
    "pfrvot",
    "pfreql",
    "pfpsaf",
)
GT0_AUTHORITY_CEILING = "CURRENT_J_CANDIDATE != EXECUTABLE_J"

EXPECTED_STAGE_SEQUENCE = (
    "F0_BIND",
    "PRE_FF",
    "FIELD_FORGE_INGRESS",
    "PRE_V3",
    "PRE_V3_TO_V3",
    "V3_TO_V2",
)

GT0_FINAL_TERMINAL = "BLOCKED_POSITIVE_ACTOR_PATH__SEMANTIC_CONSERVATION_PASS"

_ALLOWED_PREV3_TERMINALS = frozenset(
    {"UNDEFINED_FOR_OBJECT", "BLOCKED_EXPLICIT_AUTHORITY"}
)
_ALLOWED_V3_TERMINALS = frozenset(
    {
        "BLOCKED_COMPARATOR_ANCESTRY",
        "BLOCKED_POSITIVE_TRANSITION_AUTHORITY",
        "OBSERVED_ZERO",
        "VALID_EMPTY",
    }
)
_ALLOWED_V2_TERMINALS = frozenset(
    {
        "BLOCKED_NAMED_AUTHORITY_REQUIRED",
        "DENIED",
        "VALID_EMPTY",
    }
)


class GT0HarnessContractError(AssertionError):
    """The candidate stage API violated the GT0 integration contract."""


@dataclass(frozen=True)
class GT0SeedBinding:
    """Nonsemantic harness configuration for the exact governed F0 seed."""

    object_id: str = GT0_SEED_ID
    producer_authority_ref: str = GT0_J01A_REF
    object_type: str = GT0_SEED_TYPE
    label: str = GT0_SEED_LABEL
    members: tuple[str, ...] = GT0_SEED_MEMBERS
    authority_ceiling: str = GT0_AUTHORITY_CEILING


@dataclass(frozen=True)
class GT0StageAPI:
    """Dependency-injected WSC002 A-F candidate API."""

    bind_gt0_f0: Callable[[GT0SeedBinding], Any]
    run_gt0_preff: Callable[[Any], Any]
    run_gt0_field_forge_ingress: Callable[[Any], Any]
    run_gt0_prev3: Callable[[Any], Any]
    run_gt0_prev3_v3: Callable[[Any], Any]
    run_gt0_v3_v2: Callable[[Any], Any]


@dataclass(frozen=True)
class GT0EndToEndResult:
    seed_id: str
    seed_authority_ref: str
    authority_ceiling: str
    stage_statuses: tuple[tuple[str, str], ...]
    stage_receipt_hashes: tuple[str, ...]
    semantic_owner: str
    permission_ceiling: tuple[str, ...]
    v3_fingerprint_before: str
    v3_fingerprint_after: str
    final_terminal: str
    full_thread_hash: str


_MISSING = object()


def _status_text(value: Any) -> str:
    if isinstance(value, Enum):
        return str(value.value)
    if hasattr(value, "value") and isinstance(getattr(value, "value"), str):
        return str(value.value)
    return str(value)


def _get(obj: Any, *names: str, default: Any = _MISSING) -> Any:
    if isinstance(obj, Mapping):
        for name in names:
            if name in obj:
                return obj[name]
    else:
        for name in names:
            if hasattr(obj, name):
                return getattr(obj, name)
    if default is not _MISSING:
        return default
    raise GT0HarnessContractError(
        f"missing required integration field; expected one of {names!r}"
    )


def _canonical(value: Any) -> Any:
    if isinstance(value, Enum):
        return _canonical(value.value)
    if is_dataclass(value):
        return {field.name: _canonical(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Mapping):
        return {
            str(key): _canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    if isinstance(value, (set, frozenset)):
        normalized = [_canonical(item) for item in value]
        return sorted(
            normalized,
            key=lambda item: json.dumps(
                item, sort_keys=True, separators=(",", ":"), ensure_ascii=False
            ),
        )
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        raise GT0HarnessContractError(
            "floating-point material is not permitted in the deterministic GT0 harness hash"
        )
    if hasattr(value, "as_dict") and callable(value.as_dict):
        return _canonical(value.as_dict())
    raise GT0HarnessContractError(
        f"unsupported receipt material for deterministic hash: {type(value).__name__}"
    )


def deterministic_content_hash(value: Any) -> str:
    payload = json.dumps(
        _canonical(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _stage_name(receipt: Any) -> str:
    return str(_get(receipt, "stage", "stage_id", "stage_name"))


def _stage_status(receipt: Any) -> str:
    return _status_text(_get(receipt, "status", "stage_status", "typed_status"))


def _envelope(receipt: Any) -> Any:
    return _get(
        receipt,
        "envelope",
        "conservation_envelope",
        "output_envelope",
    )


def _metadata(receipt: Any) -> Mapping[str, Any]:
    metadata = _get(receipt, "metadata", "details", "evidence", default={})
    if metadata is None:
        return {}
    if not isinstance(metadata, Mapping):
        raise GT0HarnessContractError("receipt metadata/details must be mapping-like")
    return metadata


def _lookup(receipt: Any, *names: str, default: Any = _MISSING) -> Any:
    for carrier in (receipt, _metadata(receipt), _envelope(receipt)):
        try:
            return _get(carrier, *names)
        except GT0HarnessContractError:
            pass
    if default is not _MISSING:
        return default
    raise GT0HarnessContractError(
        f"missing required receipt/envelope field; expected one of {names!r}"
    )


def _permission_tokens(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Mapping):
        return tuple(
            sorted(str(key) for key, enabled in value.items() if bool(enabled))
        )
    if isinstance(value, (tuple, list, set, frozenset)):
        return tuple(sorted(str(item) for item in value))
    raise GT0HarnessContractError(
        f"unsupported consumer-permission representation: {type(value).__name__}"
    )


def _semantic_owner(receipt: Any) -> str:
    return str(
        _lookup(
            receipt,
            "semantic_owner",
            "producer_owner",
            "source_semantic_owner",
        )
    )


def _permission(receipt: Any) -> tuple[str, ...]:
    return _permission_tokens(
        _lookup(
            receipt,
            "consumer_permission",
            "consumer_permissions",
            "permission_ceiling",
        )
    )


def _assert_upstream_link(current: Any, upstream: Any) -> None:
    current_refs = _lookup(
        current,
        "upstream_refs",
        "upstream_references",
        "source_receipt_refs",
        default=(),
    )
    if not current_refs:
        return
    if isinstance(current_refs, str):
        current_refs = (current_refs,)
    expected = deterministic_content_hash(upstream)
    normalized = {str(item) for item in current_refs}
    if expected not in normalized:
        raise GT0HarnessContractError(
            f"{_stage_name(current)} does not exact-reference the upstream receipt hash"
        )


def _assert_exact_seed(f0: Any, seed: GT0SeedBinding) -> tuple[str, tuple[str, ...]]:
    if _stage_name(f0) != EXPECTED_STAGE_SEQUENCE[0]:
        raise GT0HarnessContractError("first receipt is not F0_BIND")
    if _stage_status(f0) != "PASS":
        raise GT0HarnessContractError("F0 binding must PASS exact identity verification")
    env = _envelope(f0)
    object_id = str(_get(env, "object_id", "source_object_id"))
    if object_id != seed.object_id:
        raise GT0HarnessContractError("F0 source-structure identity changed")
    authority_ref = str(
        _get(
            env,
            "producer_authority",
            "producer_authority_ref",
            "authority_ref",
        )
    )
    if authority_ref != seed.producer_authority_ref:
        raise GT0HarnessContractError("F0 J01-A authority reference changed")
    ceiling = str(_get(env, "authority_ceiling", "semantic_ceiling"))
    if ceiling != seed.authority_ceiling:
        raise GT0HarnessContractError("F0 authority ceiling widened or changed")
    object_type = str(_get(env, "object_type", "source_object_type"))
    if object_type != seed.object_type:
        raise GT0HarnessContractError("F0 source-structure type changed")
    members = tuple(_get(env, "members", "member_ids", default=()))
    if members and members != seed.members:
        raise GT0HarnessContractError("F0 member identity/order changed")
    return _semantic_owner(f0), _permission(f0)


def _assert_owner_and_permission_conservation(
    receipts: Sequence[Any],
    source_owner: str,
    source_permission: tuple[str, ...],
) -> tuple[str, tuple[str, ...]]:
    previous_permission = source_permission
    for receipt in receipts:
        owner = _semantic_owner(receipt)
        if owner != source_owner:
            raise GT0HarnessContractError(
                f"{_stage_name(receipt)} changed producer semantic ownership"
            )
        permission = _permission(receipt)
        if not set(permission).issubset(set(previous_permission)):
            raise GT0HarnessContractError(
                f"{_stage_name(receipt)} widened consumer permission"
            )
        previous_permission = permission
    return source_owner, previous_permission


def _assert_prev3_abstains(prev3: Any) -> None:
    status = _stage_status(prev3)
    if status not in _ALLOWED_PREV3_TERMINALS:
        raise GT0HarnessContractError(
            f"PRE_V3 must abstain/block for F0, got {status}"
        )
    for name in (
        "positive_structural_object_count",
        "v555_route_count",
        "v556_object_count",
    ):
        value = _lookup(prev3, name, default=0)
        if value != 0:
            raise GT0HarnessContractError(
                f"PRE_V3 manufactured positive structure via {name}={value!r}"
            )
    refs = _lookup(
        prev3,
        "positive_structural_object_refs",
        "v555_route_refs",
        "v556_object_refs",
        default=(),
    )
    if refs:
        raise GT0HarnessContractError("PRE_V3 emitted substantive structural refs for F0")


def _required_equal_pair(
    receipt: Any,
    before_names: tuple[str, ...],
    after_names: tuple[str, ...],
) -> tuple[str, str]:
    before = str(_lookup(receipt, *before_names))
    after = str(_lookup(receipt, *after_names))
    if before != after:
        raise GT0HarnessContractError(
            f"{_stage_name(receipt)} zero-effect invariant failed: {before_names[0]} changed"
        )
    return before, after


def _assert_v3_zero_effect(v3: Any) -> tuple[str, str]:
    status = _stage_status(v3)
    if status not in _ALLOWED_V3_TERMINALS:
        raise GT0HarnessContractError(
            f"PRE_V3_TO_V3 must be typed nonpositive for baseline F0, got {status}"
        )
    fingerprint_before, fingerprint_after = _required_equal_pair(
        v3,
        ("v3_fingerprint_before", "runtime_fingerprint_before"),
        ("v3_fingerprint_after", "runtime_fingerprint_after"),
    )
    _required_equal_pair(
        v3,
        ("ledger_hash_before", "causal_ledger_hash_before"),
        ("ledger_hash_after", "causal_ledger_hash_after"),
    )
    _required_equal_pair(
        v3,
        ("rng_state_hash_before", "rng_hash_before"),
        ("rng_state_hash_after", "rng_hash_after"),
    )
    _required_equal_pair(
        v3,
        ("scheduler_state_hash_before", "scheduler_hash_before"),
        ("scheduler_state_hash_after", "scheduler_hash_after"),
    )
    mutation_count = int(
        _lookup(v3, "v3_causal_mutation_count", "causal_mutation_count", default=0)
    )
    if mutation_count != 0:
        raise GT0HarnessContractError("V3 recorded causal mutation on denied GT0 proposal")
    return fingerprint_before, fingerprint_after


def _assert_v2_blocks(v2: Any) -> None:
    status = _stage_status(v2)
    if status not in _ALLOWED_V2_TERMINALS:
        raise GT0HarnessContractError(
            f"V3_TO_V2 must block/deny/empty for baseline F0, got {status}"
        )
    actor_claim_count = int(
        _lookup(v2, "actor_claim_count", "positive_actor_claim_count", default=0)
    )
    render_count = int(
        _lookup(v2, "positive_render_count", "rendered_expression_count", default=0)
    )
    model_called = bool(_lookup(v2, "model_called", default=False))
    if actor_claim_count != 0:
        raise GT0HarnessContractError("V2 derived an actor claim from F0")
    if render_count != 0:
        raise GT0HarnessContractError("V2 produced a positive render from F0")
    if model_called:
        raise GT0HarnessContractError("V2 called a model on the blocked GT0 path")


def _assert_stage_sequence(receipts: Sequence[Any]) -> None:
    actual = tuple(_stage_name(receipt) for receipt in receipts)
    if actual != EXPECTED_STAGE_SEQUENCE:
        raise GT0HarnessContractError(
            f"unexpected GT0 stage sequence: {actual!r}"
        )


def _full_thread_hash(
    seed: GT0SeedBinding,
    receipts: Sequence[Any],
    terminal: str,
) -> tuple[tuple[str, ...], str]:
    receipt_hashes = tuple(deterministic_content_hash(receipt) for receipt in receipts)
    material = {
        "seed": seed,
        "expected_stage_sequence": EXPECTED_STAGE_SEQUENCE,
        "receipt_hashes": receipt_hashes,
        "terminal": terminal,
    }
    return receipt_hashes, deterministic_content_hash(material)


def load_integrated_stage_api() -> GT0StageAPI:
    """Load the exact WSC002 A-F integration surfaces lazily.

    This function is intentionally unused by the independent G-lane tests.
    It becomes executable only after central integration installs A-F.
    """

    bindings = (
        ("rawlsing_next.wsc_gt0_source_preff", "bind_gt0_f0"),
        ("rawlsing_next.wsc_gt0_source_preff", "run_gt0_preff"),
        ("rawlsing_next.wsc_gt0_field_forge_ingress", "run_gt0_field_forge_ingress"),
        ("rawlsing_next.wsc_gt0_prev3_bridge", "run_gt0_prev3"),
        ("rawlsing_next.wsc_gt0_v3_runtime", "run_gt0_prev3_v3"),
        ("rawlsing_next.wsc_gt0_v2_mediation", "run_gt0_v3_v2"),
    )
    callables: list[Callable[..., Any]] = []
    for module_name, function_name in bindings:
        module = importlib.import_module(module_name)
        function = getattr(module, function_name, None)
        if not callable(function):
            raise GT0HarnessContractError(
                f"integrated stage surface missing: {module_name}.{function_name}"
            )
        callables.append(function)
    return GT0StageAPI(*callables)


def run_gt0_end_to_end(
    stage_api: GT0StageAPI | None = None,
    *,
    seed: GT0SeedBinding = GT0SeedBinding(),
) -> GT0EndToEndResult:
    """Execute and validate the full blocked-path Golden Thread 0.

    On the independent WSC002G branch callers inject stage_api test doubles.
    After fan-in, omitting stage_api loads the real A-F module surfaces.
    """

    api = stage_api if stage_api is not None else load_integrated_stage_api()

    f0 = api.bind_gt0_f0(seed)
    preff = api.run_gt0_preff(f0)
    field_forge = api.run_gt0_field_forge_ingress(preff)
    prev3 = api.run_gt0_prev3(field_forge)
    v3 = api.run_gt0_prev3_v3(prev3)
    v2 = api.run_gt0_v3_v2(v3)

    receipts = (f0, preff, field_forge, prev3, v3, v2)
    _assert_stage_sequence(receipts)

    source_owner, source_permission = _assert_exact_seed(f0, seed)
    for current, upstream in zip(receipts[1:], receipts[:-1]):
        _assert_upstream_link(current, upstream)

    owner, final_permission = _assert_owner_and_permission_conservation(
        receipts[1:],
        source_owner,
        source_permission,
    )
    _assert_prev3_abstains(prev3)
    fingerprint_before, fingerprint_after = _assert_v3_zero_effect(v3)
    _assert_v2_blocks(v2)

    receipt_hashes, thread_hash = _full_thread_hash(
        seed, receipts, GT0_FINAL_TERMINAL
    )

    return GT0EndToEndResult(
        seed_id=seed.object_id,
        seed_authority_ref=seed.producer_authority_ref,
        authority_ceiling=seed.authority_ceiling,
        stage_statuses=tuple(
            (_stage_name(receipt), _stage_status(receipt)) for receipt in receipts
        ),
        stage_receipt_hashes=receipt_hashes,
        semantic_owner=owner,
        permission_ceiling=final_permission,
        v3_fingerprint_before=fingerprint_before,
        v3_fingerprint_after=fingerprint_after,
        final_terminal=GT0_FINAL_TERMINAL,
        full_thread_hash=thread_hash,
    )
