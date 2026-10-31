"""TEST_ONLY_SOURCEFREE owner-bound PE/SC0 successor.

This module is an explicit-dependency successor to the pinned PE/SC0 overlay. It
never installs a sitecustomize hook, never monkeypatches an upstream module and
never promotes a test fixture into a competent source or N9 issuer. It accepts
an already computed N10E/C1 producer result, an explicitly supplied source-free
world provider, an exact scoped issuer registry and a receiving consumer.

The receipt binds every value-bearing field, both refresh receipts, the issuer
grant, the selected-world owner/revision/digest, the exact C1/N10E geometry and
the first-consumer output into one semantic identity. A refusal carries no
world, no geometry and no consumer output.
"""
from __future__ import annotations

import copy
import re
from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    canonicalize,
    semantic_hash,
)

CONTRACT_ID = "PYAT_PE_SC0_OWNER_BOUND_SOURCEFREE_SUCCESSOR@1.0.0"
REQUEST_SCHEMA = "PYAT_PE_SC0_OWNER_BOUND_REQUEST@1"
RECEIPT_SCHEMA = "PYAT_PE_SC0_OWNER_BOUND_RECEIPT@1"
SERVICE_GRADE = (
    "TEST_ONLY_SOURCEFREE__NOT_OPERATIVE_N9__NOT_SOURCE__"
    "NOT_MODEL_USE__NOT_ADOPTION"
)
WORLD_GRADE = "TEST_ONLY_SOURCEFREE_FIXTURE_WORLD__NOT_OPERATIVE_N9"
N10E_CONTRACT_ID = "N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER@1.0.0"
N10E_EXACT_STATE = "EXACT_SUPPORTED_SLICE_PRODUCED"

ROLE_FORWARD = "FORWARD_SUBJECT_TO_TARGET"
ROLE_REVERSE = "REVERSE_TARGET_VALUE_TO_SUBJECT"
ROLE_DIRECTIONS = frozenset({ROLE_FORWARD, ROLE_REVERSE})

N9_SELECTED_IMMUTABLE = "SELECTED_IMMUTABLE"
N9_INVALIDATED = "INVALIDATED"

ISSUER_TEST_ONLY_SOURCEFREE = "TEST_ONLY_SOURCEFREE"
ISSUER_COMPETENT_SOURCE = "COMPETENT_SOURCE"

REQUIRED_CLOCKS = frozenset(
    {
        "observation_effective",
        "publication_knowledge",
        "actor_event",
        "request_currentness",
    }
)
REQUIRED_WORLD_VALUES = (
    "absolute_horizon",
    "native_strata",
    "nary",
    "f2",
    "public_sanctions",
    "public_categories",
    "contradictory_alternatives",
)
NEGATIVE_STATUS_STATES = frozenset(
    {
        "OBSERVED_ZERO",
        "VALID_EMPTY",
        "MISSING",
        "UNDERPOWERED",
        "NOT_ASKED",
        "NONCOMPARABLE",
        "HELD_AUTHORITY",
        "DENIED_USE",
    }
)

REFUSAL_REQUEST_SHAPE = "REQUEST_SHAPE_REFUSED"
REFUSAL_PRODUCER_MISSING = "PRODUCER_MISSING_REFUSED"
REFUSAL_PRODUCER_FAULT = "PRODUCER_FAULT_REFUSED"
REFUSAL_PRODUCER_CONTRACT = "PRODUCER_CONTRACT_REFUSED"
REFUSAL_PRODUCER_REFUSED = "PRODUCER_TYPED_REFUSAL"
REFUSAL_ISSUER_MISSING = "ISSUER_MISSING_OR_INCOMPETENT_REFUSED"
REFUSAL_ISSUER_STATE = "ISSUER_STATE_REFUSED"
REFUSAL_ISSUER_VERSION = "ISSUER_VERSION_REFUSED"
REFUSAL_ISSUER_OPERATION = "ISSUER_OPERATION_REFUSED"
REFUSAL_ISSUER_TARGET = "ISSUER_TARGET_REFUSED"
REFUSAL_ISSUER_RISK = "ISSUER_RISK_REFUSED"
REFUSAL_ISSUER_WORLD = "ISSUER_WORLD_OWNER_REFUSED"
REFUSAL_ISSUER_TIME = "ISSUER_TIME_SCOPE_REFUSED"
REFUSAL_ISSUER_TEST_PROMOTION = "TEST_AUTHORITY_NOT_COMPETENT_FOR_SOURCE_PROMOTION"
REFUSAL_WORLD_PROVIDER_MISSING = "WORLD_PROVIDER_MISSING_REFUSED"
REFUSAL_WORLD_PROVIDER_FAULT = "WORLD_PROVIDER_FAULT_REFUSED"
REFUSAL_WORLD_VALUES_TAMPERED = "WORLD_VALUES_TAMPERED_REFUSED"
REFUSAL_WORLD_DIGEST_MISMATCH = "WORLD_SELECTION_DIGEST_MISMATCH_REFUSED"
REFUSAL_WORLD_OWNER_MISMATCH = "WORLD_OWNER_MISMATCH_REFUSED"
REFUSAL_WORLD_REVISION_MISMATCH = "WORLD_REVISION_MISMATCH_REFUSED"
REFUSAL_WORLD_RISK_SCOPE = "WORLD_RISK_SCOPE_MISMATCH_REFUSED"
REFUSAL_WORLD_UNIT = "WORLD_NATIVE_UNIT_REFUSED"
REFUSAL_WORLD_CLOCK = "WORLD_CLOCK_INVALID_REFUSED"
REFUSAL_STALE_CURRENT = "STALE_CURRENT_REFUSED"
REFUSAL_INVALIDATED_CURRENT = "INVALIDATED_CURRENT_REFUSED"
REFUSAL_FUTURE_ASOF = "FUTURE_ASOF_REFUSED"
REFUSAL_SOURCE_PROMOTION = "SOURCE_PROMOTION_REFUSED"
REFUSAL_NEGATIVE_STATUS_SCOPE = "NEGATIVE_STATUS_SCOPE_REFUSED"
REFUSAL_REFRESH_AUDIT = "REFRESH_AUDIT_MISSING_REFUSED"
REFUSAL_REFRESH_FAULT = "REFRESH_CHANNEL_FAULT_REFUSED"
REFUSAL_REFRESH_MISMATCH = "REFRESH_RECEIPT_MISMATCH_REFUSED"
REFUSAL_REFRESH_NOT_DISTINCT = "REFRESH_RECEIPTS_NOT_DISTINCT_REFUSED"
REFUSAL_GEOMETRY = "GEOMETRY_REFUSED"
REFUSAL_GEOMETRY_ZERO_DENOMINATOR = "GEOMETRY_ZERO_DENOMINATOR_REFUSED"
REFUSAL_GEOMETRY_SUM = "GEOMETRY_CELL_SUM_MISMATCH_REFUSED"
REFUSAL_GEOMETRY_TARGET = "GEOMETRY_TARGET_CELL_REFUSED"
REFUSAL_REVERSAL_GEOMETRY = "REVERSAL_GEOMETRY_REFUSED"
REFUSAL_ROLE_DIRECTION = "ROLE_DIRECTION_REFUSED"
REFUSAL_CONSUMER_SEVERED = "CONSUMER_SEVERED_REFUSED"
REFUSAL_CONSUMER_OUTPUT = "CONSUMER_OUTPUT_REFUSED"
REFUSAL_UNEXPECTED = "UNEXPECTED_FAULT_REFUSED"
REFUSAL_REPLAY = "REPLAY_MISMATCH"

EPISTEMIC_CEILING = (
    "TEST_ONLY_SOURCEFREE__NOT_OPERATIVE_N9",
    "SYNTHETIC_FIXTURE_VALUES_ARE_NOT_ORIGINAL_RESPONDENT_EVIDENCE",
    "EMPIRICAL_POSSIBILITY != CAUSAL_EFFECT",
    "WORLD_ROUTE_ELIGIBILITY != N10E_CONDITIONED_NUMERICAL_INFERENCE",
    "NO_SOURCE_PROMOTION__NO_MODEL_USE__NO_ADOPTION",
)

_TIME_RE = re.compile(
    r"^(?P<year>\d{4})(?:-(?P<month>\d{2}))?(?:-(?P<day>\d{2}))?"
    r"(?:[T ](?P<hour>\d{2}):(?P<minute>\d{2})(?::(?P<second>\d{2}))?)?"
    r"(?:Z|[+-]\d{2}:?\d{2})?$"
)


class OwnerBoundError(Exception):
    """Base typed successor error."""


class OwnerBoundRefusal(OwnerBoundError):
    def __init__(self, state: str, reason: str) -> None:
        super().__init__(f"{state}: {reason}")
        self.state = state
        self.reason = reason


class OwnerBoundReplayError(OwnerBoundError):
    """Raised when a replay does not reproduce the exact result identity."""


def _fail(state: str, reason: str) -> None:
    raise OwnerBoundRefusal(state, reason)


def _require(condition: bool, state: str, reason: str) -> None:
    if not condition:
        _fail(state, reason)


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(REFUSAL_REQUEST_SHAPE, f"{name} must be a non-empty string")
    out = value.strip()
    if out.lower() in {"latest", "default", "nearest", "fuzzy", "*"}:
        _fail(REFUSAL_REQUEST_SHAPE, f"{name} may not be mutable or fuzzy")
    return out


def _sha(value: Any, name: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        _fail(REFUSAL_REQUEST_SHAPE, f"{name} must be a lowercase sha256")
    return value


def _exact(value: Any, name: str) -> ExactRef:
    if isinstance(value, ExactRef):
        return value
    if isinstance(value, Mapping):
        try:
            return ExactRef(
                value["kind"], value["object_id"], value["content_hash"]
            )
        except Exception as exc:
            raise OwnerBoundRefusal(
                REFUSAL_REQUEST_SHAPE, f"{name} is not an exact ref: {exc}"
            ) from exc
    _fail(REFUSAL_REQUEST_SHAPE, f"{name} must be an ExactRef or mapping")
    raise AssertionError("unreachable")


def _auth(value: Any, name: str) -> AuthorityRef:
    if isinstance(value, AuthorityRef):
        return value
    if isinstance(value, Mapping):
        try:
            return AuthorityRef(
                value["authority_id"],
                value["authority_version"],
                value["authority_content_hash"],
            )
        except Exception as exc:
            raise OwnerBoundRefusal(
                REFUSAL_REQUEST_SHAPE, f"{name} is not an authority ref: {exc}"
            ) from exc
    _fail(REFUSAL_REQUEST_SHAPE, f"{name} must be an AuthorityRef or mapping")
    raise AssertionError("unreachable")


def _time_key(value: Any) -> tuple[int, int, int, int, int, int]:
    if not isinstance(value, str) or not value.strip():
        _fail(REFUSAL_REQUEST_SHAPE, "time coordinate must be a non-empty string")
    match = _TIME_RE.fullmatch(value.strip())
    if match is None:
        _fail(REFUSAL_REQUEST_SHAPE, f"unsupported time coordinate {value!r}")
    parts = {k: int(v) if v is not None else 0 for k, v in match.groupdict().items()}
    month = parts["month"] or 1
    day = parts["day"] or 1
    if not (1 <= month <= 12 and 1 <= day <= 31):
        _fail(REFUSAL_REQUEST_SHAPE, f"invalid time coordinate {value!r}")
    return (
        parts["year"],
        month,
        day,
        parts["hour"],
        parts["minute"],
        parts["second"],
    )


def _time_before(left: Any, right: Any) -> bool:
    return _time_key(left) < _time_key(right)


def _time_at_or_before(left: Any, right: Any) -> bool:
    return _time_key(left) <= _time_key(right)


def _canonical(value: Any) -> Any:
    return canonicalize(value)


@dataclass(frozen=True)
class OwnerBoundRequest:
    request_id: str
    role_direction: str
    target_ref: ExactRef
    risk_set_ref: ExactRef
    conditioner_coordinate_ref: ExactRef
    declared_target_value: str
    declared_condition_value: str
    selected_world_owner: str
    selected_world_digest: str
    world_revision: int
    n9_snapshot_state: str
    n9_asof_time: str
    request_time: str
    issuer_ref: AuthorityRef
    purpose: str = "EMPIRICAL_POSSIBILITY_ONLY"

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _text(self.request_id, "request_id"))
        direction = _text(self.role_direction, "role_direction")
        if direction not in ROLE_DIRECTIONS:
            _fail(REFUSAL_REQUEST_SHAPE, "unsupported role_direction")
        object.__setattr__(self, "role_direction", direction)
        target = _exact(self.target_ref, "target_ref")
        conditioner = _exact(
            self.conditioner_coordinate_ref, "conditioner_coordinate_ref"
        )
        if target == conditioner:
            _fail(REFUSAL_ROLE_DIRECTION, "target and conditioner coordinate are identical")
        object.__setattr__(self, "target_ref", target)
        object.__setattr__(self, "conditioner_coordinate_ref", conditioner)
        object.__setattr__(self, "risk_set_ref", _exact(self.risk_set_ref, "risk_set_ref"))
        target_value = _text(self.declared_target_value, "declared_target_value")
        condition_value = _text(
            self.declared_condition_value, "declared_condition_value"
        )
        if target_value == condition_value:
            _fail(REFUSAL_ROLE_DIRECTION, "target and condition values are identical")
        object.__setattr__(self, "declared_target_value", target_value)
        object.__setattr__(self, "declared_condition_value", condition_value)
        object.__setattr__(
            self, "selected_world_owner", _text(self.selected_world_owner, "selected_world_owner")
        )
        object.__setattr__(
            self, "selected_world_digest", _sha(self.selected_world_digest, "selected_world_digest")
        )
        if type(self.world_revision) is not int or self.world_revision < 0:
            _fail(REFUSAL_REQUEST_SHAPE, "world_revision must be a nonnegative integer")
        state = _text(self.n9_snapshot_state, "n9_snapshot_state")
        if state not in {N9_SELECTED_IMMUTABLE, N9_INVALIDATED}:
            _fail(REFUSAL_REQUEST_SHAPE, "unsupported n9_snapshot_state")
        object.__setattr__(self, "n9_snapshot_state", state)
        object.__setattr__(self, "n9_asof_time", _text(self.n9_asof_time, "n9_asof_time"))
        object.__setattr__(self, "request_time", _text(self.request_time, "request_time"))
        object.__setattr__(self, "issuer_ref", _auth(self.issuer_ref, "issuer_ref"))
        purpose = _text(self.purpose, "purpose")
        if purpose != "EMPIRICAL_POSSIBILITY_ONLY":
            _fail(REFUSAL_REQUEST_SHAPE, "actor/prediction jurisdiction forbidden")
        object.__setattr__(self, "purpose", purpose)

    def material(self) -> Mapping[str, Any]:
        return {
            "schema": REQUEST_SCHEMA,
            "contract": CONTRACT_ID,
            "request_id": self.request_id,
            "role_direction": self.role_direction,
            "target_ref": self.target_ref.as_dict(),
            "risk_set_ref": self.risk_set_ref.as_dict(),
            "conditioner_coordinate_ref": self.conditioner_coordinate_ref.as_dict(),
            "declared_target_value": self.declared_target_value,
            "declared_condition_value": self.declared_condition_value,
            "selected_world_owner": self.selected_world_owner,
            "selected_world_digest": self.selected_world_digest,
            "world_revision": self.world_revision,
            "n9_snapshot_state": self.n9_snapshot_state,
            "n9_asof_time": self.n9_asof_time,
            "request_time": self.request_time,
            "issuer_ref": self.issuer_ref.as_dict(),
            "purpose": self.purpose,
        }

    @property
    def request_hash(self) -> str:
        return semantic_hash(self.material())

    @property
    def ref(self) -> ExactRef:
        digest = self.request_hash
        return ExactRef(
            REQUEST_SCHEMA,
            f"urn:rawlsing:pyat:pe-sc0:owner-bound-request:sha256:{digest}",
            digest,
        )


@dataclass(frozen=True)
class ScopedGrant:
    authority_ref: AuthorityRef
    issuer_id: str
    issuer_version: str
    issuer_grade: str
    state: str
    operations: frozenset[str]
    target_refs: frozenset[str]
    risk_set_refs: frozenset[str]
    world_owners: frozenset[str]
    valid_from: str
    valid_until: str | None
    source_promotion_authority: bool = False

    def __post_init__(self) -> None:
        ref = _auth(self.authority_ref, "authority_ref")
        issuer_id = _text(self.issuer_id, "issuer_id")
        issuer_version = _text(self.issuer_version, "issuer_version")
        if ref.authority_id != issuer_id or ref.authority_version != issuer_version:
            _fail(REFUSAL_ISSUER_VERSION, "grant issuer id/version differs from authority ref")
        grade = _text(self.issuer_grade, "issuer_grade")
        if grade not in {ISSUER_TEST_ONLY_SOURCEFREE, ISSUER_COMPETENT_SOURCE}:
            _fail(REFUSAL_ISSUER_MISSING, "unsupported issuer grade")
        state = _text(self.state, "state")
        if state not in {"ALLOW", "DENY"}:
            _fail(REFUSAL_ISSUER_STATE, "unsupported issuer state")
        operations = frozenset(_text(x, "operation") for x in self.operations)
        if not operations:
            _fail(REFUSAL_ISSUER_OPERATION, "empty issuer operation scope")
        target_refs = frozenset(_text(x, "target_ref") for x in self.target_refs)
        risk_set_refs = frozenset(_text(x, "risk_set_ref") for x in self.risk_set_refs)
        world_owners = frozenset(_text(x, "world_owner") for x in self.world_owners)
        if not target_refs or not risk_set_refs or not world_owners:
            _fail(REFUSAL_ISSUER_MISSING, "grant must carry target, risk and world scopes")
        valid_from = _text(self.valid_from, "valid_from")
        valid_until = None if self.valid_until is None else _text(self.valid_until, "valid_until")
        if valid_until is not None and not _time_before(valid_from, valid_until):
            _fail(REFUSAL_ISSUER_TIME, "valid_until must follow valid_from")
        object.__setattr__(self, "authority_ref", ref)
        object.__setattr__(self, "issuer_id", issuer_id)
        object.__setattr__(self, "issuer_version", issuer_version)
        object.__setattr__(self, "issuer_grade", grade)
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "operations", operations)
        object.__setattr__(self, "target_refs", target_refs)
        object.__setattr__(self, "risk_set_refs", risk_set_refs)
        object.__setattr__(self, "world_owners", world_owners)
        object.__setattr__(self, "valid_from", valid_from)
        object.__setattr__(self, "valid_until", valid_until)
        if type(self.source_promotion_authority) is not bool:
            _fail(REFUSAL_ISSUER_MISSING, "source_promotion_authority must be bool")

    def material(self) -> Mapping[str, Any]:
        return {
            "authority_ref": self.authority_ref.as_dict(),
            "issuer_id": self.issuer_id,
            "issuer_version": self.issuer_version,
            "issuer_grade": self.issuer_grade,
            "state": self.state,
            "operations": sorted(self.operations),
            "target_refs": sorted(self.target_refs),
            "risk_set_refs": sorted(self.risk_set_refs),
            "world_owners": sorted(self.world_owners),
            "valid_from": self.valid_from,
            "valid_until": self.valid_until,
            "source_promotion_authority": self.source_promotion_authority,
        }


class ExactIssuerRegistry:
    """Immutable exact-key issuer registry with no latest/default lookup."""

    def __init__(self, grants: Iterable[ScopedGrant]) -> None:
        by_key: dict[str, ScopedGrant] = {}
        for grant in grants:
            if not isinstance(grant, ScopedGrant):
                raise OwnerBoundRefusal(REFUSAL_ISSUER_MISSING, "grant must be ScopedGrant")
            key = grant.authority_ref.key
            if key in by_key and by_key[key] != grant:
                raise OwnerBoundRefusal(
                    REFUSAL_ISSUER_STATE, "conflicting duplicate exact issuer grant"
                )
            by_key[key] = grant
        self._by_key = MappingProxyType(by_key)

    def require_exact(self, ref: AuthorityRef) -> ScopedGrant:
        exact = _auth(ref, "issuer_ref")
        grant = self._by_key.get(exact.key)
        if grant is None:
            _fail(REFUSAL_ISSUER_MISSING, "exact issuer grant is absent")
        return grant

    def require_source_promotion(self, ref: AuthorityRef) -> ScopedGrant:
        grant = self.require_exact(ref)
        if grant.issuer_grade != ISSUER_COMPETENT_SOURCE or not grant.source_promotion_authority:
            _fail(
                REFUSAL_ISSUER_TEST_PROMOTION,
                "test-only or non-promotion grant cannot authorize source promotion",
            )
        if "SOURCE_PROMOTION" not in grant.operations:
            _fail(REFUSAL_ISSUER_TEST_PROMOTION, "source promotion operation is not scoped")
        return grant


@dataclass(frozen=True)
class ProducerEvidence:
    provider_contract_id: str
    provider_state: str
    producer_receipt_ref: ExactRef
    producer_query_ref: ExactRef
    producer_fact_ref: ExactRef
    consumer_query_ref: ExactRef
    consumer_result_state: str
    consumer_result_identity_hash: str
    role_direction: str
    target_ref: ExactRef
    risk_set_ref: ExactRef
    conditioner_coordinate_ref: ExactRef
    source_universe_ref: ExactRef
    release_ref: ExactRef
    model_rule_hash: str
    cells: tuple[Mapping[str, Any], ...]
    denominator: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "provider_contract_id", _text(self.provider_contract_id, "provider_contract_id"))
        object.__setattr__(self, "provider_state", _text(self.provider_state, "provider_state"))
        for name in (
            "producer_receipt_ref",
            "producer_query_ref",
            "producer_fact_ref",
            "consumer_query_ref",
            "target_ref",
            "risk_set_ref",
            "conditioner_coordinate_ref",
            "source_universe_ref",
            "release_ref",
        ):
            object.__setattr__(self, name, _exact(getattr(self, name), name))
        object.__setattr__(self, "consumer_result_state", _text(self.consumer_result_state, "consumer_result_state"))
        object.__setattr__(
            self, "consumer_result_identity_hash", _sha(self.consumer_result_identity_hash, "consumer_result_identity_hash")
        )
        direction = _text(self.role_direction, "role_direction")
        if direction not in ROLE_DIRECTIONS:
            _fail(REFUSAL_ROLE_DIRECTION, "unsupported producer role direction")
        object.__setattr__(self, "role_direction", direction)
        object.__setattr__(self, "model_rule_hash", _sha(self.model_rule_hash, "model_rule_hash"))
        cells = tuple(_canonical(cell) for cell in self.cells)
        if not cells:
            _fail(REFUSAL_GEOMETRY, "producer carries no cells")
        object.__setattr__(self, "cells", cells)
        if type(self.denominator) is not int or self.denominator < 0:
            _fail(REFUSAL_GEOMETRY, "denominator must be a nonnegative integer")
        object.__setattr__(self, "denominator", self.denominator)

    def material(self) -> Mapping[str, Any]:
        return {
            "provider_contract_id": self.provider_contract_id,
            "provider_state": self.provider_state,
            "producer_receipt_ref": self.producer_receipt_ref.as_dict(),
            "producer_query_ref": self.producer_query_ref.as_dict(),
            "producer_fact_ref": self.producer_fact_ref.as_dict(),
            "consumer_query_ref": self.consumer_query_ref.as_dict(),
            "consumer_result_state": self.consumer_result_state,
            "consumer_result_identity_hash": self.consumer_result_identity_hash,
            "role_direction": self.role_direction,
            "target_ref": self.target_ref.as_dict(),
            "risk_set_ref": self.risk_set_ref.as_dict(),
            "conditioner_coordinate_ref": self.conditioner_coordinate_ref.as_dict(),
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "model_rule_hash": self.model_rule_hash,
            "cells": [copy.deepcopy(cell) for cell in sorted(self.cells, key=lambda c: c.get("cell", ""))],
            "denominator": self.denominator,
        }

    @property
    def identity_hash(self) -> str:
        return semantic_hash(self.material())


def selection_digest_for(
    *,
    world_owner: str,
    revision: int,
    values: Mapping[str, Any],
    clocks: Mapping[str, Any],
    negative_status_rows: Sequence[Mapping[str, Any]],
    generated_binding_echo: Mapping[str, Any],
    native_sampling_unit: str,
    risk_set_ref: ExactRef,
    routing_ref: ExactRef,
    values_read_receipt: Mapping[str, Any],
) -> str:
    return semantic_hash(
        {
            "world_owner": world_owner,
            "revision": revision,
            "values": values,
            "clocks": clocks,
            "negative_status_rows": list(negative_status_rows),
            "generated_binding_echo": generated_binding_echo,
            "native_sampling_unit": native_sampling_unit,
            "risk_set_ref": _exact(risk_set_ref, "risk_set_ref").as_dict(),
            "routing_ref": _exact(routing_ref, "routing_ref").as_dict(),
            "values_read_receipt": values_read_receipt,
        }
    )


@dataclass(frozen=True)
class WorldSnapshot:
    world_owner: str
    revision: int
    selection_digest: str
    values: Mapping[str, Any]
    clocks: Mapping[str, Any]
    negative_status_rows: tuple[Mapping[str, Any], ...]
    generated_binding_echo: Mapping[str, Any]
    native_sampling_unit: str
    risk_set_ref: ExactRef
    routing_ref: ExactRef
    values_read_receipt: Mapping[str, Any]
    grade: str = WORLD_GRADE

    def __post_init__(self) -> None:
        object.__setattr__(self, "world_owner", _text(self.world_owner, "world_owner"))
        if type(self.revision) is not int or self.revision < 0:
            _fail(REFUSAL_WORLD_REVISION_MISMATCH, "world revision must be nonnegative integer")
        object.__setattr__(self, "selection_digest", _sha(self.selection_digest, "selection_digest"))
        object.__setattr__(self, "values", _canonical(self.values))
        object.__setattr__(self, "clocks", _canonical(self.clocks))
        rows = tuple(_canonical(row) for row in self.negative_status_rows)
        object.__setattr__(self, "negative_status_rows", rows)
        object.__setattr__(self, "generated_binding_echo", _canonical(self.generated_binding_echo))
        object.__setattr__(self, "native_sampling_unit", _text(self.native_sampling_unit, "native_sampling_unit"))
        object.__setattr__(self, "risk_set_ref", _exact(self.risk_set_ref, "risk_set_ref"))
        object.__setattr__(self, "routing_ref", _exact(self.routing_ref, "routing_ref"))
        object.__setattr__(self, "values_read_receipt", _canonical(self.values_read_receipt))
        object.__setattr__(self, "grade", _text(self.grade, "grade"))

    def computed_digest(self) -> str:
        return selection_digest_for(
            world_owner=self.world_owner,
            revision=self.revision,
            values=self.values,
            clocks=self.clocks,
            negative_status_rows=self.negative_status_rows,
            generated_binding_echo=self.generated_binding_echo,
            native_sampling_unit=self.native_sampling_unit,
            risk_set_ref=self.risk_set_ref,
            routing_ref=self.routing_ref,
            values_read_receipt=self.values_read_receipt,
        )

    def material(self) -> Mapping[str, Any]:
        return {
            "world_owner": self.world_owner,
            "revision": self.revision,
            "selection_digest": self.selection_digest,
            "values": copy.deepcopy(self.values),
            "clocks": copy.deepcopy(self.clocks),
            "negative_status_rows": [copy.deepcopy(row) for row in self.negative_status_rows],
            "generated_binding_echo": copy.deepcopy(self.generated_binding_echo),
            "native_sampling_unit": self.native_sampling_unit,
            "risk_set_ref": self.risk_set_ref.as_dict(),
            "routing_ref": self.routing_ref.as_dict(),
            "values_read_receipt": copy.deepcopy(self.values_read_receipt),
            "grade": self.grade,
        }


@dataclass(frozen=True)
class OwnerBoundReceipt:
    receipt_id: str
    request_ref: ExactRef
    request_hash: str
    producer_evidence: Mapping[str, Any]
    issuer_grant: Mapping[str, Any]
    world: Mapping[str, Any]
    refresh_receipts: Mapping[str, Any]
    geometry: Mapping[str, Any]
    consumer_output: Mapping[str, Any]
    provenance: Mapping[str, Any]
    epistemic_ceiling: tuple[str, ...]

    def material(self) -> Mapping[str, Any]:
        return {
            "schema": RECEIPT_SCHEMA,
            "contract": CONTRACT_ID,
            "service_grade": SERVICE_GRADE,
            "receipt_id": self.receipt_id,
            "request_ref": self.request_ref.as_dict(),
            "request_hash": self.request_hash,
            "producer_evidence": copy.deepcopy(self.producer_evidence),
            "issuer_grant": copy.deepcopy(self.issuer_grant),
            "world": copy.deepcopy(self.world),
            "refresh_receipts": copy.deepcopy(self.refresh_receipts),
            "geometry": copy.deepcopy(self.geometry),
            "consumer_output": copy.deepcopy(self.consumer_output),
            "provenance": copy.deepcopy(self.provenance),
            "epistemic_ceiling": list(self.epistemic_ceiling),
        }

    @property
    def receipt_hash(self) -> str:
        return semantic_hash(self.material())

    @property
    def ref(self) -> ExactRef:
        digest = self.receipt_hash
        return ExactRef(
            RECEIPT_SCHEMA,
            f"urn:rawlsing:pyat:pe-sc0:owner-bound-receipt:sha256:{digest}",
            digest,
        )


@dataclass(frozen=True)
class OwnerBoundResult:
    request_ref: ExactRef
    receipt: OwnerBoundReceipt | None
    result_state: str
    refusal_state: str | None = None
    refusal_reason: str | None = None

    def material(self) -> Mapping[str, Any]:
        receipt = self.receipt
        return {
            "schema": "PYAT_PE_SC0_OWNER_BOUND_RESULT@1",
            "contract": CONTRACT_ID,
            "request_ref": self.request_ref.as_dict(),
            "result_state": self.result_state,
            "receipt_ref": None if receipt is None else receipt.ref.as_dict(),
            "receipt_hash": None if receipt is None else receipt.receipt_hash,
            "refusal_state": self.refusal_state,
            "refusal_reason": self.refusal_reason,
        }

    @property
    def result_hash(self) -> str:
        return semantic_hash(self.material())


def _refusal(request: OwnerBoundRequest, state: str, reason: str) -> OwnerBoundResult:
    return OwnerBoundResult(
        request_ref=request.ref,
        receipt=None,
        result_state="TYPED_REFUSAL",
        refusal_state=state,
        refusal_reason=reason,
    )


def _validate_grant(grant: ScopedGrant, request: OwnerBoundRequest) -> None:
    if grant.state != "ALLOW":
        _fail(REFUSAL_ISSUER_STATE, "issuer grant is not ALLOW")
    if grant.issuer_id != request.issuer_ref.authority_id:
        _fail(REFUSAL_ISSUER_MISSING, "issuer id does not match exact grant")
    if grant.issuer_version != request.issuer_ref.authority_version:
        _fail(REFUSAL_ISSUER_VERSION, "issuer version does not match exact grant")
    if request.role_direction not in grant.operations:
        _fail(REFUSAL_ISSUER_OPERATION, "role direction is not scoped by issuer")
    if request.target_ref.key not in grant.target_refs:
        _fail(REFUSAL_ISSUER_TARGET, "target is not within exact issuer scope")
    if request.risk_set_ref.key not in grant.risk_set_refs:
        _fail(REFUSAL_ISSUER_RISK, "risk set is not within exact issuer scope")
    if request.selected_world_owner not in grant.world_owners:
        _fail(REFUSAL_ISSUER_WORLD, "world owner is not within exact issuer scope")
    if _time_before(request.request_time, grant.valid_from):
        _fail(REFUSAL_ISSUER_TIME, "request time precedes issuer validity")
    if grant.valid_until is not None and not _time_before(request.request_time, grant.valid_until):
        _fail(REFUSAL_ISSUER_TIME, "request time is outside issuer validity")


def _validate_request_time(request: OwnerBoundRequest) -> None:
    if request.n9_snapshot_state != N9_SELECTED_IMMUTABLE:
        _fail(REFUSAL_INVALIDATED_CURRENT, "invalidated N9 current cannot serve")
    if not _time_before(request.n9_asof_time, request.request_time):
        _fail(REFUSAL_FUTURE_ASOF, "as-of is not before request time")


def _invoke_producer(producer: Any) -> ProducerEvidence:
    if producer is None:
        _fail(REFUSAL_PRODUCER_MISSING, "no empirical producer was supplied")
    try:
        evidence = producer.produce()
    except Exception as exc:
        _fail(REFUSAL_PRODUCER_FAULT, f"producer raised {type(exc).__name__}: {exc}")
    if not isinstance(evidence, ProducerEvidence):
        _fail(REFUSAL_PRODUCER_CONTRACT, "producer did not return ProducerEvidence")
    if evidence.provider_contract_id != N10E_CONTRACT_ID:
        _fail(REFUSAL_PRODUCER_CONTRACT, "producer contract is not the pinned N10E contract")
    if evidence.provider_state != N10E_EXACT_STATE:
        _fail(REFUSAL_PRODUCER_REFUSED, "producer did not produce an exact slice")
    if evidence.consumer_result_state != "EXACT_SUPPORTED":
        _fail(REFUSAL_PRODUCER_REFUSED, "producer consumer result is not EXACT_SUPPORTED")
    return evidence


def _validate_evidence(evidence: ProducerEvidence, request: OwnerBoundRequest) -> None:
    if evidence.role_direction != request.role_direction:
        _fail(REFUSAL_ROLE_DIRECTION, "producer role direction differs from request")
    if evidence.target_ref != request.target_ref:
        _fail(REFUSAL_ROLE_DIRECTION, "producer target differs from request target")
    if evidence.conditioner_coordinate_ref != request.conditioner_coordinate_ref:
        _fail(REFUSAL_ROLE_DIRECTION, "producer conditioner differs from request conditioner")
    if evidence.risk_set_ref != request.risk_set_ref:
        _fail(REFUSAL_PRODUCER_CONTRACT, "producer risk set differs from request risk set")


def _get_world(world_provider: Any) -> WorldSnapshot:
    if world_provider is None:
        _fail(REFUSAL_WORLD_PROVIDER_MISSING, "no world provider was supplied")
    try:
        snapshot = world_provider.snapshot()
    except Exception as exc:
        _fail(REFUSAL_WORLD_PROVIDER_FAULT, f"world provider raised {type(exc).__name__}: {exc}")
    if not isinstance(snapshot, WorldSnapshot):
        _fail(REFUSAL_WORLD_PROVIDER_FAULT, "world provider did not return WorldSnapshot")
    return snapshot


def _validate_world(snapshot: WorldSnapshot, request: OwnerBoundRequest) -> None:
    if snapshot.world_owner != request.selected_world_owner:
        _fail(REFUSAL_WORLD_OWNER_MISMATCH, "world owner differs from request owner")
    if snapshot.revision != request.world_revision:
        _fail(REFUSAL_WORLD_REVISION_MISMATCH, "world revision differs from requested revision")
    if snapshot.selection_digest != request.selected_world_digest:
        _fail(REFUSAL_WORLD_DIGEST_MISMATCH, "world digest differs from requested digest")
    if snapshot.computed_digest() != snapshot.selection_digest:
        _fail(REFUSAL_WORLD_VALUES_TAMPERED, "world values do not recompute the reported selection digest")
    if snapshot.risk_set_ref != request.risk_set_ref:
        _fail(REFUSAL_WORLD_RISK_SCOPE, "world risk scope differs from request risk set")
    if snapshot.native_sampling_unit != "RESPONDENT":
        _fail(REFUSAL_WORLD_UNIT, "world native sampling unit is not RESPONDENT")
    for name in REQUIRED_WORLD_VALUES:
        if name not in snapshot.values or snapshot.values[name] is None:
            _fail(REFUSAL_WORLD_PROVIDER_FAULT, f"world value is absent: {name}")
    if set(snapshot.clocks) != REQUIRED_CLOCKS:
        _fail(REFUSAL_WORLD_CLOCK, "world clocks are not the exact four clock axes")
    for clock_name in ("observation_effective", "publication_knowledge"):
        clock_value = snapshot.clocks.get(clock_name)
        if not isinstance(clock_value, str) or not clock_value.strip():
            _fail(REFUSAL_WORLD_CLOCK, f"{clock_name} clock is absent")
    if snapshot.clocks.get("request_currentness") != request.request_time:
        _fail(REFUSAL_STALE_CURRENT, "request currentness clock differs from request time")
    if not _time_before(snapshot.clocks.get("publication_knowledge"), request.request_time):
        _fail(REFUSAL_STALE_CURRENT, "publication knowledge is not before request time")
    if not _time_at_or_before(
        snapshot.clocks.get("observation_effective"),
        snapshot.clocks.get("publication_knowledge"),
    ):
        _fail(REFUSAL_WORLD_CLOCK, "observation clock follows publication clock")
    if not snapshot.negative_status_rows:
        _fail(REFUSAL_NEGATIVE_STATUS_SCOPE, "negative status algebra is absent")
    for row in snapshot.negative_status_rows:
        if not isinstance(row, Mapping):
            _fail(REFUSAL_NEGATIVE_STATUS_SCOPE, "negative status row is not a mapping")
        state = row.get("state")
        if state not in NEGATIVE_STATUS_STATES:
            _fail(REFUSAL_NEGATIVE_STATUS_SCOPE, f"unsupported negative status {state!r}")
        if not isinstance(row.get("scope"), str) or not row.get("scope").strip():
            _fail(REFUSAL_NEGATIVE_STATUS_SCOPE, f"status {state} lacks source/risk scope")
        try:
            row_risk = _exact(row.get("risk_set_ref"), "risk_set_ref")
        except OwnerBoundRefusal:
            _fail(REFUSAL_NEGATIVE_STATUS_SCOPE, f"status {state} lacks exact risk scope")
        if row_risk != request.risk_set_ref:
            _fail(REFUSAL_NEGATIVE_STATUS_SCOPE, f"status {state} risk scope differs from request")
    echo = snapshot.generated_binding_echo
    if echo.get("tag") != "GENERATED_RUNTIME_FACT_REF":
        _fail(REFUSAL_SOURCE_PROMOTION, "generated binding echo tag is not the runtime-fact tag")
    if echo.get("upstream_authorship") is not False:
        _fail(REFUSAL_SOURCE_PROMOTION, "generated binding claims upstream source authorship")
    if echo.get("may_use_as_source_observation") is not False:
        _fail(REFUSAL_SOURCE_PROMOTION, "generated binding claims source-observation promotion")
    values_read = snapshot.values_read_receipt
    if not isinstance(values_read, Mapping):
        _fail(REFUSAL_WORLD_PROVIDER_FAULT, "values-read receipt is absent")
    keys = values_read.get("keys")
    if not isinstance(keys, (list, tuple)) or not keys:
        _fail(REFUSAL_WORLD_PROVIDER_FAULT, "values-read receipt carries no value keys")
    if not isinstance(values_read.get("digest"), str) or not re.fullmatch(
        r"[0-9a-f]{64}", values_read.get("digest", "")
    ):
        _fail(REFUSAL_WORLD_PROVIDER_FAULT, "values-read receipt digest is not sha256")


def _validate_geometry(
    evidence: ProducerEvidence, request: OwnerBoundRequest
) -> tuple[str, Mapping[str, Any]]:
    denominator = evidence.denominator
    if type(denominator) is not int:
        _fail(REFUSAL_GEOMETRY, "denominator is not an exact integer")
    if denominator <= 0:
        _fail(REFUSAL_GEOMETRY_ZERO_DENOMINATOR, "denominator must be positive")
    seen: set[str] = set()
    total = 0
    target_cell: Mapping[str, Any] | None = None
    for cell in evidence.cells:
        if not isinstance(cell, Mapping):
            _fail(REFUSAL_GEOMETRY, "cell is not a mapping")
        name = cell.get("cell")
        if not isinstance(name, str) or not name.strip() or name in seen:
            _fail(REFUSAL_GEOMETRY, "cell name is empty or duplicated")
        seen.add(name)
        numerator = cell.get("raw_numerator_support")
        if type(numerator) is not int or numerator < 0:
            _fail(REFUSAL_GEOMETRY, "cell numerator is not a nonnegative exact integer")
        fraction = cell.get("raw_probability_exact_fraction")
        if not isinstance(fraction, Mapping):
            _fail(REFUSAL_GEOMETRY, "cell exact fraction is absent")
        parts = fraction.get("$exact_fraction")
        if not isinstance(parts, (list, tuple)) or len(parts) != 2:
            _fail(REFUSAL_GEOMETRY, "cell exact fraction is not [numerator, denominator]")
        numerator_part, denominator_part = parts
        if type(numerator_part) is not int or type(denominator_part) is not int:
            _fail(REFUSAL_GEOMETRY, "cell exact fraction is not integer")
        if denominator_part <= 0 or numerator_part < 0:
            _fail(REFUSAL_GEOMETRY, "cell exact fraction has invalid sign or zero denominator")
        if Fraction(numerator_part, denominator_part) != Fraction(numerator, denominator):
            _fail(REFUSAL_GEOMETRY, "cell exact fraction does not match cell numerator/denominator")
        total += numerator
        if name == request.declared_target_value:
            target_cell = cell
    if total != denominator:
        _fail(REFUSAL_GEOMETRY_SUM, f"cell sum {total} differs from denominator {denominator}")
    if target_cell is None:
        _fail(REFUSAL_GEOMETRY_TARGET, "declared target value is not a geometry cell")
    if request.declared_condition_value in seen:
        _fail(REFUSAL_ROLE_DIRECTION, "declared condition value appears as a target cell")
    if request.role_direction == ROLE_REVERSE and len(seen) < 2:
        _fail(REFUSAL_REVERSAL_GEOMETRY, "reverse geometry requires its own target domain")
    return request.declared_target_value, target_cell


def _refresh_token(
    request: OwnerBoundRequest, *, channel: str, world_owner: str, revision: int
) -> str:
    return semantic_hash(
        {
            "request_ref": request.ref.as_dict(),
            "channel": channel,
            "world_owner": world_owner,
            "base_revision": revision,
            "selection_digest": request.selected_world_digest,
        }
    )


def _expected_successor(
    *, channel: str, world_owner: str, revision: int, world_result_ref: str, token: str
) -> str:
    return semantic_hash(
        {
            "channel": channel,
            "world_owner": world_owner,
            "base_revision": revision,
            "world_result_ref": world_result_ref,
            "invocation_token": token,
        }
    )


def _refresh_counts(world_provider: Any) -> dict[str, int]:
    getter = getattr(world_provider, "refresh_invocation_counts", None)
    if not callable(getter):
        _fail(REFUSAL_REFRESH_AUDIT, "world provider has no refresh invocation audit")
    counts = getter()
    if not isinstance(counts, Mapping):
        _fail(REFUSAL_REFRESH_AUDIT, "refresh invocation audit is not a mapping")
    return {str(k): int(v) for k, v in counts.items()}


def _validate_refresh_receipt(
    receipt: Any,
    *,
    channel: str,
    request: OwnerBoundRequest,
    token: str,
    world: WorldSnapshot,
) -> Mapping[str, Any]:
    if not isinstance(receipt, Mapping):
        _fail(REFUSAL_REFRESH_MISMATCH, f"{channel} refresh receipt is not a mapping")
    if receipt.get("channel") != channel:
        _fail(REFUSAL_REFRESH_MISMATCH, f"{channel} refresh channel is wrong")
    if receipt.get("executed") is not True:
        _fail(REFUSAL_REFRESH_MISMATCH, f"{channel} refresh was not executed")
    if receipt.get("world_owner") != request.selected_world_owner:
        _fail(REFUSAL_REFRESH_MISMATCH, f"{channel} refresh owner mismatch")
    if receipt.get("base_revision") != request.world_revision:
        _fail(REFUSAL_REFRESH_MISMATCH, f"{channel} refresh base revision mismatch")
    if receipt.get("world_result_ref") != request.selected_world_digest:
        _fail(REFUSAL_REFRESH_MISMATCH, f"{channel} refresh world result ref mismatch")
    if receipt.get("invocation_token") != token:
        _fail(REFUSAL_REFRESH_MISMATCH, f"{channel} refresh invocation token mismatch")
    generation = receipt.get("generation")
    if type(generation) is not int or generation != request.world_revision + 1:
        _fail(REFUSAL_REFRESH_MISMATCH, f"{channel} refresh generation is not the next revision")
    expected = _expected_successor(
        channel=channel,
        world_owner=request.selected_world_owner,
        revision=request.world_revision,
        world_result_ref=request.selected_world_digest,
        token=token,
    )
    if receipt.get("successor_digest") != expected:
        _fail(REFUSAL_REFRESH_MISMATCH, f"{channel} refresh successor digest mismatch")
    return _canonical(receipt)


def _invoke_refresh(world_provider: Any, request: OwnerBoundRequest, world: WorldSnapshot) -> Mapping[str, Any]:
    before = _refresh_counts(world_provider)
    publication_token = _refresh_token(
        request,
        channel="H2_PUBLICATION_BOUNDARY_REFRESH",
        world_owner=world.world_owner,
        revision=world.revision,
    )
    try:
        publication = world_provider.refresh_publication(invocation_token=publication_token)
    except Exception as exc:
        _fail(REFUSAL_REFRESH_FAULT, f"publication refresh raised {type(exc).__name__}: {exc}")
    after_publication = _refresh_counts(world_provider)
    if after_publication.get("publication", 0) != before.get("publication", 0) + 1:
        _fail(REFUSAL_REFRESH_AUDIT, "publication refresh invocation was not audited")
    publication_material = _validate_refresh_receipt(
        publication,
        channel="H2_PUBLICATION_BOUNDARY_REFRESH",
        request=request,
        token=publication_token,
        world=world,
    )
    binding_token = _refresh_token(
        request,
        channel="H2_GENERATED_BINDING_REFRESH",
        world_owner=world.world_owner,
        revision=world.revision,
    )
    try:
        binding = world_provider.refresh_binding(invocation_token=binding_token)
    except Exception as exc:
        _fail(REFUSAL_REFRESH_FAULT, f"binding refresh raised {type(exc).__name__}: {exc}")
    after_binding = _refresh_counts(world_provider)
    if after_binding.get("binding", 0) != after_publication.get("binding", 0) + 1:
        _fail(REFUSAL_REFRESH_AUDIT, "binding refresh invocation was not audited")
    binding_material = _validate_refresh_receipt(
        binding,
        channel="H2_GENERATED_BINDING_REFRESH",
        request=request,
        token=binding_token,
        world=world,
    )
    if semantic_hash(publication_material) == semantic_hash(binding_material):
        _fail(REFUSAL_REFRESH_NOT_DISTINCT, "publication and binding refresh receipts are not distinct")
    return {
        "publication": publication_material,
        "binding": binding_material,
    }


def _invoke_consumer(
    consumer: Any,
    *,
    request: OwnerBoundRequest,
    world: WorldSnapshot,
    target_cell: str,
    target_entry: Mapping[str, Any],
) -> Mapping[str, Any]:
    if consumer is None:
        _fail(REFUSAL_CONSUMER_SEVERED, "no receiving consumer was supplied")
    try:
        output = consumer.consume(
            request=request,
            world=world.material(),
            target_cell=target_cell,
            target_fraction=copy.deepcopy(target_entry.get("raw_probability_exact_fraction")),
        )
    except Exception as exc:
        _fail(REFUSAL_CONSUMER_SEVERED, f"consumer raised {type(exc).__name__}: {exc}")
    if not isinstance(output, Mapping):
        _fail(REFUSAL_CONSUMER_OUTPUT, "consumer output is not a mapping")
    if output.get("no_person_generation") is not True:
        _fail(REFUSAL_CONSUMER_OUTPUT, "consumer did not assert no person generation")
    if output.get("no_actor_state") is not True:
        _fail(REFUSAL_CONSUMER_OUTPUT, "consumer did not assert no actor state")
    if output.get("world_owner") != request.selected_world_owner:
        _fail(REFUSAL_CONSUMER_OUTPUT, "consumer output is bound to another world owner")
    if output.get("world_revision") != request.world_revision:
        _fail(REFUSAL_CONSUMER_OUTPUT, "consumer output is bound to another world revision")
    if output.get("target_cell") != target_cell:
        _fail(REFUSAL_CONSUMER_OUTPUT, "consumer output target cell differs")
    if not output.get("route_constraints"):
        _fail(REFUSAL_CONSUMER_OUTPUT, "consumer output carries no route constraint")
    grade = output.get("consumer_grade")
    if not isinstance(grade, str) or "TEST_ONLY_SOURCEFREE" not in grade:
        _fail(REFUSAL_CONSUMER_OUTPUT, "consumer is not declared TEST_ONLY_SOURCEFREE")
    return _canonical(output)


def _build_receipt(
    *,
    request: OwnerBoundRequest,
    grant: ScopedGrant,
    evidence: ProducerEvidence,
    world: WorldSnapshot,
    refresh: Mapping[str, Any],
    geometry: Mapping[str, Any],
    consumer_output: Mapping[str, Any],
) -> OwnerBoundReceipt:
    base = {
        "request": request.material(),
        "producer": evidence.material(),
        "issuer": grant.material(),
        "world": world.material(),
        "refresh": refresh,
        "geometry": geometry,
        "consumer": consumer_output,
    }
    receipt_id = f"urn:rawlsing:pyat:pe-sc0:owner-bound-receipt:{semantic_hash(base)[:32]}"
    return OwnerBoundReceipt(
        receipt_id=receipt_id,
        request_ref=request.ref,
        request_hash=request.request_hash,
        producer_evidence=evidence.material(),
        issuer_grant=grant.material(),
        world=world.material(),
        refresh_receipts=refresh,
        geometry=geometry,
        consumer_output=consumer_output,
        provenance={
            "producer": "actual invoked N10E empirical possibility provider",
            "world_provider": "explicit source-free fixture world provider",
            "refresh": "actual invoked provider publication and binding refresh methods",
            "issuer": "exact test-only scoped issuer registry",
            "consumer": "in-candidate TEST_ONLY_SOURCEFREE first consumer",
            "service_grade": SERVICE_GRADE,
            "sitecustomize_used": False,
            "global_monkeypatch_used": False,
        },
        epistemic_ceiling=EPISTEMIC_CEILING,
    )


def serve(
    *,
    producer: Any,
    world_provider: Any,
    issuer_registry: Any,
    consumer: Any,
    request: OwnerBoundRequest,
) -> OwnerBoundResult:
    if not isinstance(request, OwnerBoundRequest):
        raise OwnerBoundRefusal(REFUSAL_REQUEST_SHAPE, "request must be OwnerBoundRequest")
    try:
        _validate_request_time(request)
        if issuer_registry is None:
            _fail(REFUSAL_ISSUER_MISSING, "no issuer registry was supplied")
        try:
            grant = issuer_registry.require_exact(request.issuer_ref)
        except OwnerBoundRefusal:
            raise
        except Exception as exc:
            _fail(REFUSAL_ISSUER_MISSING, f"issuer registry failed: {type(exc).__name__}: {exc}")
        _validate_grant(grant, request)
        evidence = _invoke_producer(producer)
        _validate_evidence(evidence, request)
        world = _get_world(world_provider)
        _validate_world(world, request)
        target_cell, target_entry = _validate_geometry(evidence, request)
        refresh = _invoke_refresh(world_provider, request, world)
        consumer_output = _invoke_consumer(
            consumer,
            request=request,
            world=world,
            target_cell=target_cell,
            target_entry=target_entry,
        )
        geometry = {
            "denominator": evidence.denominator,
            "cells": [copy.deepcopy(cell) for cell in sorted(evidence.cells, key=lambda c: c["cell"])],
            "target_cell": target_cell,
        }
        receipt = _build_receipt(
            request=request,
            grant=grant,
            evidence=evidence,
            world=world,
            refresh=refresh,
            geometry=geometry,
            consumer_output=consumer_output,
        )
        return OwnerBoundResult(
            request_ref=request.ref,
            receipt=receipt,
            result_state="EXACT_SUPPORTED",
        )
    except OwnerBoundRefusal as exc:
        return _refusal(request, exc.state, exc.reason)
    except Exception as exc:
        return _refusal(request, REFUSAL_UNEXPECTED, f"{type(exc).__name__}: {exc}")


def verify_replay(
    expected: OwnerBoundResult,
    *,
    producer: Any,
    world_provider: Any,
    issuer_registry: Any,
    consumer: Any,
    request: OwnerBoundRequest,
) -> OwnerBoundResult:
    replayed = serve(
        producer=producer,
        world_provider=world_provider,
        issuer_registry=issuer_registry,
        consumer=consumer,
        request=request,
    )
    if replayed.result_hash != expected.result_hash:
        raise OwnerBoundReplayError(
            "owner-bound replay did not reproduce the exact result identity"
        )
    if expected.receipt is not None:
        if replayed.receipt is None or replayed.receipt.receipt_hash != expected.receipt.receipt_hash:
            raise OwnerBoundReplayError(
                "owner-bound replay did not reproduce the exact receipt identity"
            )
    return replayed


def verify_receipt_integrity(receipt: OwnerBoundReceipt) -> None:
    if not isinstance(receipt, OwnerBoundReceipt):
        raise OwnerBoundReplayError("receipt is not OwnerBoundReceipt")
    if receipt.ref.content_hash != receipt.receipt_hash:
        raise OwnerBoundReplayError("receipt ref content hash differs from receipt hash")
    if semantic_hash(receipt.material()) != receipt.receipt_hash:
        raise OwnerBoundReplayError("receipt material does not recompute its identity")


def verify_result_integrity(result: OwnerBoundResult) -> None:
    if not isinstance(result, OwnerBoundResult):
        raise OwnerBoundReplayError("result is not OwnerBoundResult")
    if semantic_hash(result.material()) != result.result_hash:
        raise OwnerBoundReplayError("result material does not recompute its identity")
    if result.receipt is not None:
        verify_receipt_integrity(result.receipt)


__all__ = [
    "CONTRACT_ID",
    "REQUEST_SCHEMA",
    "RECEIPT_SCHEMA",
    "SERVICE_GRADE",
    "WORLD_GRADE",
    "N10E_CONTRACT_ID",
    "ROLE_FORWARD",
    "ROLE_REVERSE",
    "ROLE_DIRECTIONS",
    "N9_SELECTED_IMMUTABLE",
    "N9_INVALIDATED",
    "ISSUER_TEST_ONLY_SOURCEFREE",
    "ISSUER_COMPETENT_SOURCE",
    "EPISTEMIC_CEILING",
    "OwnerBoundError",
    "OwnerBoundRefusal",
    "OwnerBoundReplayError",
    "OwnerBoundRequest",
    "ScopedGrant",
    "ExactIssuerRegistry",
    "ProducerEvidence",
    "WorldSnapshot",
    "OwnerBoundReceipt",
    "OwnerBoundResult",
    "selection_digest_for",
    "serve",
    "verify_replay",
    "verify_receipt_integrity",
    "verify_result_integrity",
]
