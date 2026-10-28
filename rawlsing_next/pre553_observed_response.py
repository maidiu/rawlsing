"""Authority-bound observed-response and co-observed response execution support.

This module is deliberately separate from ``_risk_membership``.  Eligible-risk
semantics remain unchanged: unresolved routing is still unresolved and may never
be coerced into nonmembership.  An observed-response operation instead declares
an exact external contract that binds:

* the source artifact, C11 release, empirical universe and observed-response
  cohort identity;
* the exact operation authority and its governed operation/object families;
* the response states that count as observed and the states that count as
  missing;
* per-target source-native topology bindings (source-native carrier topology to
  the existing I03 public topology);
* target-observation and condition-observation policies; and
* the denominator/missingness ledger semantics.

The module never creates an authority, never fabricates an operation token and
never promotes fixture-only authority to original scientific use.  A caller
flag alone cannot grant science: an authorized contract must resolve through the
existing immutable ``AuthorityRegistry``.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    require_positive_authority,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)

OBSERVED_RESPONSE_RISK_SET = "OBSERVED_RESPONSE_RISK_SET"
CO_OBSERVED_RESPONSE_RISK_SET = "CO_OBSERVED_RESPONSE_RISK_SET"
OBSERVED_RESPONSE_RISK_SET_TYPES = frozenset({
    OBSERVED_RESPONSE_RISK_SET,
    CO_OBSERVED_RESPONSE_RISK_SET,
})

OBSERVED_RESPONSE_CONTRACT_SCHEMA = "PRE553_OBSERVED_RESPONSE_CONTRACT@1.0.0"
OBSERVED_RESPONSE_CONTRACT_STATES = frozenset({"APPROVAL_PENDING", "AUTHORIZED"})
OBSERVED_RESPONSE_AUTHORITY_GRADES = frozenset({
    "ORIGINAL_SCIENTIFIC",
    "NONRESPONDENT_FIXTURE_ONLY",
})
OBSERVED_RESPONSE_DENOMINATOR_POLICIES = frozenset({
    "PER_TARGET_OBSERVED",
    "CO_OBSERVED_TARGETS",
})
OBSERVED_RESPONSE_CONDITION_POLICIES = frozenset({
    "ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED",
})
I03_TARGET_TOPOLOGIES = frozenset({
    "SCALAR_SINGULAR",
    "UNORDERED_MULTISELECT",
    "UNORDERED_MULTISELECT_SET",
    "MULTISELECT",
    "ORDERED_SEQUENCE",
    "REPEATED_EVENT",
    "REPEATED_MEASUREMENT",
    "RANKED_RESPONSE",
    "ROUTED_RESPONSE",
    "COMPONENTIZED_RESPONSE",
})
ISSUER_FIELDS = (
    "operation_authority_ref",
    "release_ref",
    "source_release_manifest_hash",
    "topology_bindings[].topology_authority_ref",
    "target_use_ref/authority/operation when an EmpiricalFact is consumed",
)


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Pre553IntegrityError(f"{name} must be a non-empty string")
    return value.strip()


def _exact(value: Any, name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Pre553IntegrityError as exc:
        raise Pre553IntegrityError(f"{name} must be exact") from exc


def _authority(value: Any, name: str) -> AuthorityRef:
    try:
        return authority_ref(value, name)
    except Pre553IntegrityError as exc:
        raise Pre553IntegrityError(f"{name} must be exact") from exc


def _optional_exact(value: Any, name: str) -> ExactRef | None:
    return None if value is None else _exact(value, name)


def _optional_authority(value: Any, name: str) -> AuthorityRef | None:
    return None if value is None else _authority(value, name)


def _text_tuple(value: Any, name: str, *, allow_empty: bool = False) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise Pre553IntegrityError(f"{name} must be a sequence")
    items = tuple(_text(item, name) for item in value)
    if not items and not allow_empty:
        raise Pre553IntegrityError(f"{name} may not be empty")
    if len(items) != len(set(items)):
        raise Pre553IntegrityError(f"{name} contains duplicates")
    return tuple(sorted(items))


def _ref_tuple(value: Any, name: str, *, allow_empty: bool = False) -> tuple[ExactRef, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise Pre553IntegrityError(f"{name} must be a sequence")
    items = tuple(_exact(item, name) for item in value)
    if not items and not allow_empty:
        raise Pre553IntegrityError(f"{name} may not be empty")
    if len({item.key for item in items}) != len(items):
        raise Pre553IntegrityError(f"{name} contains duplicate exact refs")
    return tuple(sorted(items, key=lambda item: item.key))


def _authority_tuple(value: Any, name: str) -> tuple[AuthorityRef, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise Pre553IntegrityError(f"{name} must be a sequence")
    items = tuple(_authority(item, name) for item in value)
    if not items:
        raise Pre553IntegrityError(f"{name} may not be empty")
    if len({item.key for item in items}) != len(items):
        raise Pre553IntegrityError(f"{name} contains duplicate authority refs")
    return tuple(sorted(items, key=lambda item: item.key))


def _scope_contains(scope_value: Any, required: Any) -> bool:
    if scope_value is None:
        return False
    if isinstance(scope_value, str):
        return scope_value in {"UNRESTRICTED_BY_THIS_AUTHORITY", "EXPLICIT_UNRESTRICTED"} or \
            canonical_json(scope_value) == canonical_json(required)
    if isinstance(scope_value, Mapping):
        return canonical_json(scope_value) == canonical_json(required)
    if isinstance(scope_value, (set, frozenset)) or (
        isinstance(scope_value, Sequence) and not isinstance(scope_value, (str, bytes, bytearray))
    ):
        needle = canonical_json(required)
        return needle in {canonical_json(item) for item in scope_value}
    return canonical_json(scope_value) == canonical_json(required)


def _require_snapshot_source_binding(snapshot, contract: "ObservedResponseContract") -> None:
    scope = snapshot.scope_envelope
    if not isinstance(scope, Mapping):
        raise Pre553AuthorityError("authority scope_envelope must be exact")
    if "source_universe_refs" in scope:
        if contract.universe_ref is None or not _scope_contains(
            scope.get("source_universe_refs"), contract.universe_ref.as_dict()
        ):
            raise Pre553AuthorityError("authority scope does not bind exact source universe")
        return
    if scope.get("source_id") == contract.source_id and scope.get("source_sha256") == contract.source_sha256:
        return
    if contract.authority_grade == "NONRESPONDENT_FIXTURE_ONLY" and \
            scope.get("source_id") == contract.source_id and \
            scope.get("original_source_sha256") == contract.source_sha256:
        return
    raise Pre553AuthorityError("authority scope does not bind exact source identity")


@dataclass(frozen=True)
class ObservedResponseTopologyBinding:
    """One exact source-native topology to I03 public-topology binding."""

    target_ref: ExactRef
    source_native_topology_ref: ExactRef
    source_native_kind: str
    i03_topology: str
    topology_operation: str
    topology_authority_ref: AuthorityRef | None
    response_semantic_authority_refs: tuple[AuthorityRef, ...]

    def __post_init__(self) -> None:
        _exact(self.target_ref, "topology_binding.target_ref")
        _exact(self.source_native_topology_ref, "topology_binding.source_native_topology_ref")
        _text(self.source_native_kind, "topology_binding.source_native_kind")
        if self.i03_topology not in I03_TARGET_TOPOLOGIES:
            raise Pre553IntegrityError("topology_binding.i03_topology is not an I03 target topology")
        _text(self.topology_operation, "topology_binding.topology_operation")
        if self.topology_authority_ref is not None:
            _authority(self.topology_authority_ref, "topology_binding.topology_authority_ref")
        if not self.response_semantic_authority_refs and self.topology_authority_ref is not None:
            raise Pre553IntegrityError("topology binding requires response semantic authority refs")
        for ref in self.response_semantic_authority_refs:
            _authority(ref, "topology_binding.response_semantic_authority_refs")

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "target_ref": self.target_ref.as_dict(),
            "source_native_topology_ref": self.source_native_topology_ref.as_dict(),
            "source_native_kind": self.source_native_kind,
            "i03_topology": self.i03_topology,
            "topology_operation": self.topology_operation,
            "topology_authority_ref": (
                self.topology_authority_ref.as_dict() if self.topology_authority_ref else None
            ),
            "response_semantic_authority_refs": [
                ref.as_dict() for ref in self.response_semantic_authority_refs
            ],
        }

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "ObservedResponseTopologyBinding":
        return cls(
            target_ref=_exact(raw.get("target_ref"), "topology_binding.target_ref"),
            source_native_topology_ref=_exact(
                raw.get("source_native_topology_ref"),
                "topology_binding.source_native_topology_ref",
            ),
            source_native_kind=_text(
                raw.get("source_native_kind"), "topology_binding.source_native_kind"
            ),
            i03_topology=_text(raw.get("i03_topology"), "topology_binding.i03_topology"),
            topology_operation=_text(
                raw.get("topology_operation"), "topology_binding.topology_operation"
            ),
            topology_authority_ref=_optional_authority(
                raw.get("topology_authority_ref"), "topology_binding.topology_authority_ref"
            ),
            response_semantic_authority_refs=_authority_tuple(
                raw.get("response_semantic_authority_refs"),
                "topology_binding.response_semantic_authority_refs",
            ),
        )


@dataclass(frozen=True)
class ObservedResponseContract:
    """Exact external operation contract for observed/co-observed responses."""

    contract_id: str
    contract_version: str
    contract_state: str
    authority_grade: str
    source_id: str
    source_sha256: str
    source_snapshot_ref: ExactRef
    source_artifact_ref: ExactRef
    source_release_manifest_hash: str | None
    release_ref: ExactRef | None
    universe_ref: ExactRef | None
    operation: str
    operation_authority_ref: AuthorityRef | None
    risk_set_ref: ExactRef
    target_refs: tuple[ExactRef, ...]
    observed_states: tuple[str, ...]
    missing_states: tuple[str, ...]
    denominator_policies: tuple[str, ...]
    condition_observation_policy: str
    topology_bindings: tuple[ObservedResponseTopologyBinding, ...]
    target_use_ref: ExactRef | None = None
    target_use_authority_ref: AuthorityRef | None = None
    target_use_operation: str | None = None
    source_config_ref: ExactRef | None = None
    source_literal_authority_ref: AuthorityRef | None = None
    source_literal_operation: str | None = None
    source_event_authority_refs: tuple[AuthorityRef, ...] = ()

    def __post_init__(self) -> None:
        _text(self.contract_id, "contract_id")
        _text(self.contract_version, "contract_version")
        if self.contract_state not in OBSERVED_RESPONSE_CONTRACT_STATES:
            raise Pre553IntegrityError("observed-response contract_state is invalid")
        if self.authority_grade not in OBSERVED_RESPONSE_AUTHORITY_GRADES:
            raise Pre553IntegrityError("observed-response authority_grade is invalid")
        _text(self.source_id, "source_id")
        if len(self.source_sha256) != 64 or any(
            ch not in "0123456789abcdef" for ch in self.source_sha256
        ):
            raise Pre553IntegrityError("source_sha256 must be lowercase sha256")
        _exact(self.source_snapshot_ref, "source_snapshot_ref")
        _exact(self.source_artifact_ref, "source_artifact_ref")
        if self.source_release_manifest_hash is not None and (
            len(self.source_release_manifest_hash) != 64
            or any(ch not in "0123456789abcdef" for ch in self.source_release_manifest_hash)
        ):
            raise Pre553IntegrityError("source_release_manifest_hash must be lowercase sha256")
        if self.release_ref is not None:
            _exact(self.release_ref, "release_ref")
        if self.universe_ref is not None:
            _exact(self.universe_ref, "universe_ref")
        if self.source_config_ref is not None:
            _exact(self.source_config_ref, "source_config_ref")
        _text(self.operation, "operation")
        if self.operation_authority_ref is not None:
            _authority(self.operation_authority_ref, "operation_authority_ref")
        _exact(self.risk_set_ref, "risk_set_ref")
        if not self.target_refs:
            raise Pre553IntegrityError("observed-response contract requires target_refs")
        for ref in self.target_refs:
            _exact(ref, "target_refs")
        if tuple(sorted(set(self.target_refs), key=lambda item: item.key)) != self.target_refs:
            raise Pre553IntegrityError("target_refs must be canonical exact-ref sorted")
        observed = _text_tuple(self.observed_states, "observed_states")
        missing = _text_tuple(self.missing_states, "missing_states")
        if observed != self.observed_states:
            object.__setattr__(self, "observed_states", observed)
        if missing != self.missing_states:
            object.__setattr__(self, "missing_states", missing)
        if set(observed) & set(missing):
            raise Pre553IntegrityError("observed_states and missing_states must be disjoint")
        if not self.denominator_policies:
            raise Pre553IntegrityError("denominator_policies may not be empty")
        for policy in self.denominator_policies:
            if policy not in OBSERVED_RESPONSE_DENOMINATOR_POLICIES:
                raise Pre553IntegrityError("unknown observed-response denominator policy")
        if tuple(sorted(set(self.denominator_policies))) != self.denominator_policies:
            raise Pre553IntegrityError("denominator_policies must be canonical sorted")
        if self.condition_observation_policy not in OBSERVED_RESPONSE_CONDITION_POLICIES:
            raise Pre553IntegrityError("unknown observed-response condition policy")
        if not self.topology_bindings:
            raise Pre553IntegrityError("observed-response contract requires topology bindings")
        binds = {binding.target_ref.key: binding for binding in self.topology_bindings}
        if len(binds) != len(self.topology_bindings):
            raise Pre553IntegrityError("topology bindings contain duplicate target refs")
        if tuple(sorted(binds, key=lambda key: key)) != tuple(ref.key for ref in self.target_refs):
            raise Pre553IntegrityError("topology bindings must cover every target ref exactly")
        if tuple(sorted(self.topology_bindings, key=lambda item: item.target_ref.key)) != self.topology_bindings:
            raise Pre553IntegrityError("topology bindings must be canonical target-ref sorted")
        use_fields = (self.target_use_ref, self.target_use_authority_ref, self.target_use_operation)
        if any(value is not None for value in use_fields) and not all(
            value is not None for value in use_fields
        ):
            raise Pre553IntegrityError("target-use ref, authority and operation must be bound together")
        if self.target_use_operation is not None:
            _text(self.target_use_operation, "target_use_operation")
        literal_fields = (
            self.source_literal_authority_ref,
            self.source_literal_operation,
            self.source_event_authority_refs,
        )
        any_literal = any(value is not None for value in literal_fields) if not isinstance(literal_fields[2], tuple) else bool(literal_fields[0] or literal_fields[1] or literal_fields[2])
        if any_literal:
            if self.source_literal_authority_ref is None or self.source_literal_operation is None or not self.source_event_authority_refs:
                raise Pre553IntegrityError("source-literal authority, operation and event authority refs must be bound together")
            _authority(self.source_literal_authority_ref, "source_literal_authority_ref")
            _text(self.source_literal_operation, "source_literal_operation")
            for ref in self.source_event_authority_refs:
                _authority(ref, "source_event_authority_refs")
            if tuple(sorted(set(self.source_event_authority_refs), key=lambda ref: ref.key)) != self.source_event_authority_refs:
                raise Pre553IntegrityError("source_event_authority_refs must be canonical sorted")
        if self.contract_state == "AUTHORIZED":
            if self.operation_authority_ref is None:
                raise Pre553IntegrityError("AUTHORIZED observed-response contract requires operation authority")
            if self.release_ref is None or self.universe_ref is None or self.source_release_manifest_hash is None:
                raise Pre553IntegrityError("AUTHORIZED observed-response contract requires exact release/universe identity")
            if any(binding.topology_authority_ref is None for binding in self.topology_bindings):
                raise Pre553IntegrityError("AUTHORIZED observed-response contract requires topology authority per target")

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "schema": OBSERVED_RESPONSE_CONTRACT_SCHEMA,
            "contract_id": self.contract_id,
            "contract_version": self.contract_version,
            "contract_state": self.contract_state,
            "authority_grade": self.authority_grade,
            "source_id": self.source_id,
            "source_sha256": self.source_sha256,
            "source_snapshot_ref": self.source_snapshot_ref.as_dict(),
            "source_artifact_ref": self.source_artifact_ref.as_dict(),
            "source_release_manifest_hash": self.source_release_manifest_hash,
            "release_ref": self.release_ref.as_dict() if self.release_ref else None,
            "universe_ref": self.universe_ref.as_dict() if self.universe_ref else None,
            "source_config_ref": self.source_config_ref.as_dict() if self.source_config_ref else None,
            "operation": self.operation,
            "operation_authority_ref": (
                self.operation_authority_ref.as_dict() if self.operation_authority_ref else None
            ),
            "risk_set_ref": self.risk_set_ref.as_dict(),
            "target_refs": [ref.as_dict() for ref in self.target_refs],
            "observed_states": list(self.observed_states),
            "missing_states": list(self.missing_states),
            "denominator_policies": list(self.denominator_policies),
            "condition_observation_policy": self.condition_observation_policy,
            "topology_bindings": [binding.semantic_projection() for binding in self.topology_bindings],
            "target_use_ref": self.target_use_ref.as_dict() if self.target_use_ref else None,
            "target_use_authority_ref": (
                self.target_use_authority_ref.as_dict() if self.target_use_authority_ref else None
            ),
            "target_use_operation": self.target_use_operation,
            **(
                {
                    "source_literal_authority_ref": self.source_literal_authority_ref.as_dict(),
                    "source_literal_operation": self.source_literal_operation,
                    "source_event_authority_refs": [ref.as_dict() for ref in self.source_event_authority_refs],
                }
                if self.source_literal_authority_ref is not None else {}
            ),
        }

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.semantic_projection())

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            "OBSERVED_RESPONSE_CONTRACT",
            f"urn:rawlsing:pre553:observed-response-contract:sha256:{self.content_hash}",
            self.content_hash,
        )

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "contract_ref": self.ref.as_dict()}

    def with_release_binding(
        self,
        *,
        release_ref: ExactRef,
        source_release_manifest_hash: str,
        universe_ref: ExactRef,
        operation_authority_ref: AuthorityRef,
        topology_authority_refs: Mapping[str, AuthorityRef],
    ) -> "ObservedResponseContract":
        """Bind an approval-ready contract to actual release and authority identities.

        This is deterministic construction, not authority creation.  The supplied
        refs must already resolve to positive snapshots during validation.
        """
        release_ref = _exact(release_ref, "release_ref")
        universe_ref = _exact(universe_ref, "universe_ref")
        operation_authority_ref = _authority(operation_authority_ref, "operation_authority_ref")
        if len(source_release_manifest_hash) != 64:
            raise Pre553IntegrityError("source_release_manifest_hash must be sha256")
        bindings = []
        for binding in self.topology_bindings:
            auth = topology_authority_refs.get(binding.target_ref.key)
            if auth is None:
                raise Pre553IntegrityError("missing exact topology authority for target")
            bindings.append(ObservedResponseTopologyBinding(
                target_ref=binding.target_ref,
                source_native_topology_ref=binding.source_native_topology_ref,
                source_native_kind=binding.source_native_kind,
                i03_topology=binding.i03_topology,
                topology_operation=binding.topology_operation,
                topology_authority_ref=_authority(auth, "topology_authority_ref"),
                response_semantic_authority_refs=binding.response_semantic_authority_refs,
            ))
        return ObservedResponseContract(
            **{
                **self.__dict__,
                "contract_state": "AUTHORIZED",
                "source_release_manifest_hash": source_release_manifest_hash,
                "release_ref": release_ref,
                "universe_ref": universe_ref,
                "operation_authority_ref": operation_authority_ref,
                "topology_bindings": tuple(bindings),
            }
        )

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "ObservedResponseContract":
        if not isinstance(raw, Mapping):
            raise Pre553IntegrityError("observed-response contract must be a mapping")
        expected = set(_CONTRACT_FIELDS) | set(_OPTIONAL_CONTRACT_FIELDS) | {"contract_ref"}
        unknown = set(raw) - expected
        if unknown:
            raise Pre553IntegrityError(f"unknown observed-response contract fields: {sorted(unknown)}")
        missing = set(_CONTRACT_FIELDS) - set(raw)
        if missing:
            raise Pre553IntegrityError(f"missing observed-response contract fields: {sorted(missing)}")
        if raw.get("schema") != OBSERVED_RESPONSE_CONTRACT_SCHEMA:
            raise Pre553IntegrityError("observed-response contract schema mismatch")
        bindings_raw = raw.get("topology_bindings")
        if isinstance(bindings_raw, (str, bytes, bytearray)) or not isinstance(bindings_raw, Sequence):
            raise Pre553IntegrityError("topology_bindings must be a sequence")
        target_refs = _ref_tuple(raw.get("target_refs"), "target_refs")
        observed_states = _text_tuple(raw.get("observed_states"), "observed_states")
        missing_states = _text_tuple(raw.get("missing_states"), "missing_states")
        policies = _text_tuple(raw.get("denominator_policies"), "denominator_policies")
        contract = cls(
            contract_id=_text(raw.get("contract_id"), "contract_id"),
            contract_version=_text(raw.get("contract_version"), "contract_version"),
            contract_state=_text(raw.get("contract_state"), "contract_state"),
            authority_grade=_text(raw.get("authority_grade"), "authority_grade"),
            source_id=_text(raw.get("source_id"), "source_id"),
            source_sha256=_text(raw.get("source_sha256"), "source_sha256"),
            source_snapshot_ref=_exact(raw.get("source_snapshot_ref"), "source_snapshot_ref"),
            source_artifact_ref=_exact(raw.get("source_artifact_ref"), "source_artifact_ref"),
            source_release_manifest_hash=raw.get("source_release_manifest_hash"),
            release_ref=_optional_exact(raw.get("release_ref"), "release_ref"),
            universe_ref=_optional_exact(raw.get("universe_ref"), "universe_ref"),
            operation=_text(raw.get("operation"), "operation"),
            operation_authority_ref=_optional_authority(
                raw.get("operation_authority_ref"), "operation_authority_ref"
            ),
            risk_set_ref=_exact(raw.get("risk_set_ref"), "risk_set_ref"),
            target_refs=target_refs,
            observed_states=observed_states,
            missing_states=missing_states,
            denominator_policies=policies,
            condition_observation_policy=_text(
                raw.get("condition_observation_policy"), "condition_observation_policy"
            ),
            topology_bindings=tuple(
                ObservedResponseTopologyBinding.from_mapping(item)
                for item in bindings_raw
            ),
            target_use_ref=_optional_exact(raw.get("target_use_ref"), "target_use_ref"),
            target_use_authority_ref=_optional_authority(
                raw.get("target_use_authority_ref"), "target_use_authority_ref"
            ),
            target_use_operation=raw.get("target_use_operation"),
            source_config_ref=_optional_exact(raw.get("source_config_ref"), "source_config_ref"),
            source_literal_authority_ref=_optional_authority(
                raw.get("source_literal_authority_ref"), "source_literal_authority_ref"),
            source_literal_operation=raw.get("source_literal_operation"),
            source_event_authority_refs=(
                _authority_tuple(raw.get("source_event_authority_refs"), "source_event_authority_refs")
                if raw.get("source_event_authority_refs") else ()
            ),
        )
        provided_ref = raw.get("contract_ref")
        if provided_ref is not None:
            ref = _exact(provided_ref, "contract_ref")
            if ref != contract.ref:
                raise Pre553IntegrityError("observed-response contract_ref does not match contract content")
        return contract


_OPTIONAL_CONTRACT_FIELDS = (
    "source_literal_authority_ref",
    "source_literal_operation",
    "source_event_authority_refs",
)
_CONTRACT_FIELDS = (
    "schema",
    "contract_id",
    "contract_version",
    "contract_state",
    "authority_grade",
    "source_id",
    "source_sha256",
    "source_snapshot_ref",
    "source_artifact_ref",
    "source_release_manifest_hash",
    "release_ref",
    "universe_ref",
    "source_config_ref",
    "operation",
    "operation_authority_ref",
    "risk_set_ref",
    "target_refs",
    "observed_states",
    "missing_states",
    "denominator_policies",
    "condition_observation_policy",
    "topology_bindings",
    "target_use_ref",
    "target_use_authority_ref",
    "target_use_operation",
)


def validate_contract_authority(
    contract: ObservedResponseContract,
    registry: AuthorityRegistry,
) -> None:
    """Resolve and validate every authority the contract invokes."""
    if not isinstance(contract, ObservedResponseContract):
        raise Pre553AuthorityError("exact observed-response contract required")
    if contract.contract_state != "AUTHORIZED":
        raise Pre553AuthorityError("observed-response contract is not authorized")
    if contract.operation_authority_ref is None:
        raise Pre553AuthorityError("observed-response operation authority missing")
    snapshot = registry.resolve_exact(contract.operation_authority_ref).snapshot
    for family in (
        "EmpiricalPredicate@1.0.0",
        "EmpiricalQuerySpec@1.0.0",
        "EmpiricalFact@1.0.0",
    ):
        require_positive_authority(
            snapshot,
            authority_kind="PREDICATE_GRAMMAR",
            operation=contract.operation,
            object_family=family,
            source_universe_ref=contract.universe_ref.as_dict() if contract.universe_ref else None,
            predicate_or_risk_set_ref=contract.risk_set_ref.as_dict(),
        )
    if contract.authority_grade == "ORIGINAL_SCIENTIFIC":
        scope = snapshot.scope_envelope
        if scope.get("fixture_only") is True or str(scope.get("grade", "")).startswith("NONRESPONDENT"):
            raise Pre553AuthorityError("fixture-only authority cannot authorize original observed-response science")
    elif contract.authority_grade == "NONRESPONDENT_FIXTURE_ONLY":
        scope = snapshot.scope_envelope
        if scope.get("fixture_only") is not True:
            raise Pre553AuthorityError("nonrespondent contract requires explicitly fixture-only authority")
    else:
        raise Pre553AuthorityError("unknown observed-response authority grade")

    for binding in contract.topology_bindings:
        if binding.topology_authority_ref is None:
            raise Pre553AuthorityError("topology authority missing")
        topology = registry.resolve_exact(binding.topology_authority_ref).snapshot
        require_positive_authority(
            topology,
            authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
            operation=binding.topology_operation,
            object_family="RespondentEvent@1.0.0",
        )
        _require_snapshot_source_binding(topology, contract)
        if topology.scope_envelope.get("fixture_only") is True and contract.authority_grade != "NONRESPONDENT_FIXTURE_ONLY":
            raise Pre553AuthorityError("fixture-only topology authority cannot authorize original science")

    if contract.source_literal_authority_ref is not None:
        literal = registry.resolve_exact(contract.source_literal_authority_ref).snapshot
        require_positive_authority(
            literal,
            authority_kind="PHYSICAL_NATIVE_REPRESENTATION_BINDING",
            operation=contract.source_literal_operation,
            object_family="RespondentEvent@1.0.0",
            source_universe_ref=contract.universe_ref.as_dict() if contract.universe_ref else None,
        )
        scope = literal.scope_envelope
        canonical_policy = scope.get("canonical_adoption")
        if canonical_policy == "DENY":
            pass
        elif canonical_policy == "NONRESPONDENT_FIXTURE_ONLY" and contract.authority_grade == "NONRESPONDENT_FIXTURE_ONLY":
            pass
        else:
            raise Pre553AuthorityError(
                "source-literal authority canonical policy is not admissible for this contract grade")
        expected_refs = {ref.key for ref in contract.source_event_authority_refs}
        declared_refs = {
            _authority(item, "source_event_authority_refs").key
            for item in scope.get("historical_event_authority_refs", ())
        }
        if declared_refs != expected_refs:
            raise Pre553AuthorityError("source-literal authority does not bind exact historical event refs")
        if literal.scope_envelope.get("fixture_only") is True and contract.authority_grade != "NONRESPONDENT_FIXTURE_ONLY":
            raise Pre553AuthorityError("fixture-only source-literal authority cannot authorize original science")
    elif contract.source_literal_operation is not None or contract.source_event_authority_refs:
        raise Pre553AuthorityError("source-literal binding is incomplete")

    if contract.target_use_authority_ref is None:
        if contract.target_use_ref is not None or contract.target_use_operation is not None:
            raise Pre553AuthorityError("target-use binding is incomplete")
        return
    use_snapshot = registry.resolve_exact(contract.target_use_authority_ref).snapshot
    require_positive_authority(
        use_snapshot,
        authority_kind="TARGET_USE_PERMISSION",
        operation=contract.target_use_operation,
        object_family="EmpiricalFact@1.0.0",
        source_universe_ref=contract.universe_ref.as_dict() if contract.universe_ref else None,
        target_use_ref=contract.target_use_ref.as_dict() if contract.target_use_ref else None,
    )


@dataclass(frozen=True)
class ObservedPredicateRequirements:
    response_question_refs: tuple[ExactRef, ...]
    coordinate_refs: tuple[ExactRef, ...]
    uses_routing: bool


def predicate_requirements(predicate_ast: Mapping[str, Any]) -> ObservedPredicateRequirements:
    response: list[ExactRef] = []
    coordinates: list[ExactRef] = []
    uses_routing = False

    def walk(node: Any) -> None:
        nonlocal uses_routing
        if not isinstance(node, Mapping):
            raise Pre553IntegrityError("predicate node must be a mapping")
        op = node.get("op")
        if op == "LEAF":
            leaf_type = node.get("leaf_type")
            if leaf_type in {"SURVEY_RESPONSE_EVENT", "TYPED_RESPONSE_STATE"}:
                response.append(_exact(node.get("question_semantic_ref"), "question_semantic_ref"))
            elif leaf_type == "EMPIRICAL_POSITION_COORDINATE":
                coordinates.append(_exact(node.get("coordinate_semantic_ref"), "coordinate_semantic_ref"))
            elif leaf_type == "ROUTING_APPLICABILITY_STATE":
                uses_routing = True
            elif leaf_type == "DERIVED_BRANCH_COHORT":
                pass
            else:
                raise Pre553IntegrityError("unknown predicate leaf type")
            return
        children = node.get("children")
        if isinstance(children, (str, bytes, bytearray)) or not isinstance(children, Sequence):
            raise Pre553IntegrityError("predicate node children must be a sequence")
        for child in children:
            walk(child)

    walk(predicate_ast)
    return ObservedPredicateRequirements(
        response_question_refs=tuple(sorted(set(response), key=lambda ref: ref.key)),
        coordinate_refs=tuple(sorted(set(coordinates), key=lambda ref: ref.key)),
        uses_routing=uses_routing,
    )


def _contract_from_profile(profile: Any) -> ObservedResponseContract:
    ref = getattr(profile, "observed_response_contract_ref", None)
    material = getattr(profile, "observed_response_contract", None)
    if not isinstance(ref, ExactRef) or not isinstance(material, Mapping):
        raise Pre553AuthorityError("observed-response profile requires exact contract ref and material")
    contract = ObservedResponseContract.from_mapping(material)
    if contract.ref != ref:
        raise Pre553AuthorityError("observed-response profile contract ref does not match material")
    return contract


def validate_contract_for_query(
    contract: ObservedResponseContract,
    *,
    profile: Any,
    query: Any,
    plan: Any,
    predicate: Any,
    release: Any,
    universe: Any,
    registry: AuthorityRegistry,
) -> None:
    validate_contract_authority(contract, registry)
    if contract.release_ref != release.release_ref:
        raise Pre553AuthorityError("observed-response contract release identity mismatch")
    if contract.source_artifact_ref != release.source_artifact_ref:
        raise Pre553AuthorityError("observed-response contract source artifact identity mismatch")
    if contract.source_release_manifest_hash != release.source_release_manifest_hash:
        raise Pre553AuthorityError("observed-response contract source release manifest mismatch")
    if contract.universe_ref != universe.ref:
        raise Pre553AuthorityError("observed-response contract universe identity mismatch")
    if contract.risk_set_ref != _exact(query.risk_set_ref, "query.risk_set_ref"):
        raise Pre553AuthorityError("observed-response contract risk-set identity mismatch")
    if profile.source_scope_mode != "SINGLE_UNIVERSE":
        raise Pre553AuthorityError("observed-response operations require one exact source universe")
    if profile.measure_kind != "RAW":
        raise Pre553AuthorityError("observed-response operations are not weighted population estimands")
    grain = query.requested_output_grain
    if not isinstance(grain, Mapping):
        raise Pre553AuthorityError("query requested_output_grain must be exact")
    if grain.get("query_operation") != contract.operation:
        raise Pre553AuthorityError("observed-response query operation does not match contract")
    refs = tuple(_exact(ref, "query.target_refs") for ref in query.target_refs)
    if not set(refs).issubset(set(contract.target_refs)):
        raise Pre553AuthorityError("query target is outside observed-response contract target scope")
    op_auth = contract.operation_authority_ref
    query_auths = tuple(_authority(ref, "query.query_authority_refs") for ref in query.query_authority_refs)
    if op_auth not in query_auths:
        raise Pre553AuthorityError("observed-response operation authority is not an exact query authority")
    grammar = _authority(predicate.grammar_authority_ref, "predicate.grammar_authority_ref")
    if grammar != op_auth:
        raise Pre553AuthorityError("observed-response predicate grammar authority differs from contract authority")
    deps = tuple(_exact(ref, "query.dependency_refs") for ref in query.dependency_refs)
    if contract.ref not in deps:
        raise Pre553AuthorityError("observed-response contract is not in exact query dependency closure")

    bindings = {binding.target_ref.key: binding for binding in contract.topology_bindings}
    for component in plan.components:
        binding = bindings.get(component.target_ref.key)
        if binding is None:
            raise Pre553AuthorityError("observed-response target lacks exact topology binding")
        if component.topology != binding.i03_topology:
            raise Pre553AuthorityError("observed-response target topology mismatch")
        if binding.topology_authority_ref not in component.topology_authority_refs:
            raise Pre553AuthorityError("observed-response topology authority is not bound to target")
        if tuple(sorted(binding.response_semantic_authority_refs, key=lambda ref: ref.key)) != tuple(
            sorted(component.response_semantic_authority_refs, key=lambda ref: ref.key)
        ):
            raise Pre553AuthorityError("observed-response semantic authority is not bound to target")
        if contract.source_literal_authority_ref is not None:
            if tuple(binding.response_semantic_authority_refs) != (contract.source_literal_authority_ref,):
                raise Pre553AuthorityError("source-literal contract requires source-literal response authority")
        if set(component.included_states) != set(contract.observed_states):
            raise Pre553AuthorityError("observed-response included states differ from contract")

    if profile.risk_set_type == OBSERVED_RESPONSE_RISK_SET:
        if len(plan.components) != 1 or "PER_TARGET_OBSERVED" not in contract.denominator_policies:
            raise Pre553AuthorityError("per-target observed-response profile requires one target and policy")
    elif profile.risk_set_type == CO_OBSERVED_RESPONSE_RISK_SET:
        if len(plan.components) < 2 or "CO_OBSERVED_TARGETS" not in contract.denominator_policies:
            raise Pre553AuthorityError("co-observed profile requires multiple targets and common policy")
    else:
        raise Pre553AuthorityError("profile is not an observed-response risk set")

    requirements = predicate_requirements(predicate.predicate_ast)
    if requirements.uses_routing:
        raise Pre553AuthorityError("observed-response condition may not use routing/applicability predicates")
    if (requirements.response_question_refs or requirements.coordinate_refs) and \
            contract.condition_observation_policy != "ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED":
        raise Pre553AuthorityError("observed-response condition observation policy is insufficient")

    use_fields = (contract.target_use_ref, contract.target_use_authority_ref, contract.target_use_operation)
    query_use = (grain.get("target_use_ref"), grain.get("target_use_authority_ref"), grain.get("target_use_operation"))
    if any(value is not None for value in use_fields):
        if tuple(
            canonicalize(value) if value is not None else None for value in query_use
        ) != tuple(
            canonicalize(value) if value is not None else None for value in use_fields
        ):
            raise Pre553AuthorityError("observed-response target-use binding does not match query")


def contract_for_query(
    *,
    profile: Any,
    query: Any,
    plan: Any,
    predicate: Any,
    release: Any,
    universe: Any,
    registry: AuthorityRegistry,
) -> ObservedResponseContract:
    contract = _contract_from_profile(profile)
    validate_contract_for_query(
        contract,
        profile=profile,
        query=query,
        plan=plan,
        predicate=predicate,
        release=release,
        universe=universe,
        registry=registry,
    )
    return contract


def topology_binding_for(
    contract: ObservedResponseContract,
    target_ref: ExactRef,
) -> ObservedResponseTopologyBinding:
    for binding in contract.topology_bindings:
        if binding.target_ref == target_ref:
            return binding
    raise Pre553AuthorityError("observed-response target lacks exact topology binding")


def validate_source_literal_object(
    obj: Any,
    contract: ObservedResponseContract,
) -> AuthorityRef | None:
    """Validate any source object whose historical authority refs are under the
    explicit source-literal grant.  No canonical or semantic ALLOW is inferred."""
    if contract.source_literal_authority_ref is None:
        return None
    allowed = {ref.key for ref in contract.source_event_authority_refs}
    obj_refs = tuple(authority_ref(ref, "object.authority_snapshot_refs")
                     for ref in obj.authority_snapshot_refs)
    unexpected = [ref.key for ref in obj_refs if ref.key not in allowed]
    if unexpected:
        raise Pre553AuthorityError(
            "object authority closure contains a ref outside the source-literal grant")
    return contract.source_literal_authority_ref


def validate_source_literal_event(
    event: Any,
    contract: ObservedResponseContract,
) -> AuthorityRef | None:
    """Validate a source-native event under an explicit source-literal authority.

    The historical event authority refs may be preparation/DEFER refs: the positive
    source-literal snapshot is the operation authority for using their raw values,
    and it explicitly denies canonical adoption.  No canonical ALLOW is inferred.
    """
    if contract.source_literal_authority_ref is None:
        return None
    allowed = {ref.key for ref in contract.source_event_authority_refs}
    event_refs = tuple(authority_ref(ref, "event.authority_snapshot_refs")
                       for ref in event.authority_snapshot_refs)
    unexpected = [ref.key for ref in event_refs if ref.key not in allowed]
    if unexpected:
        raise Pre553AuthorityError(
            "event authority closure contains a ref outside the source-literal grant")
    if (
        getattr(event, "canonical_response_value_if_authorized", None) is not None
        and contract.authority_grade != "NONRESPONDENT_FIXTURE_ONLY"
    ):
        raise Pre553AuthorityError(
            "observed source-literal operation cannot consume a canonical response value")
    return contract.source_literal_authority_ref


__all__ = [
    "OBSERVED_RESPONSE_RISK_SET",
    "CO_OBSERVED_RESPONSE_RISK_SET",
    "OBSERVED_RESPONSE_RISK_SET_TYPES",
    "OBSERVED_RESPONSE_CONTRACT_SCHEMA",
    "OBSERVED_RESPONSE_DENOMINATOR_POLICIES",
    "OBSERVED_RESPONSE_CONDITION_POLICIES",
    "ISSUER_FIELDS",
    "ObservedResponseTopologyBinding",
    "ObservedResponseContract",
    "ObservedPredicateRequirements",
    "predicate_requirements",
    "validate_contract_authority",
    "validate_contract_for_query",
    "contract_for_query",
    "topology_binding_for",
    "validate_source_literal_object",
    "validate_source_literal_event",
]
