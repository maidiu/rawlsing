"""PYAT HQ280 PV3 A04S - canonical v2 workload contract: semantic operation ↔ owner dispatch mapping.

This is the bounded, nonissuing v2 successor that resolves A04R's exact findings:

A04R FINDINGS RESOLVED:
1. Semantic operation class ↔ Owner dispatch class mapping (was: conflated)
   - UNARY_DISTRIBUTION → I03_UNARY_OR_JOINT_QUERY
   - PAIR_RESPONSE_COTRAVEL → I03_UNARY_OR_JOINT_QUERY  
   - NONSCALAR_TOPOLOGY_PRESERVATION → I03_UNARY_OR_JOINT_QUERY
   - BOUNDED_DISCOVERY → I05_BOUNDED_DISCOVERY

2. RAW vs GOVERNED_WEIGHTED preserved as distinct operations (A05 lacked this)
3. condition_order preserved as ordered conditional predicates (A05 lacked this)
4. Consumer obligations separated from expected-work identity (A04 put consumer in key)
5. Genuinely versioned exact preimages with explicit issuer (matching schema token ≠ proof)
6. Separate pre-run independent custodian record (before execution, not after)

This is a DATA-ONLY candidate. It uses real A04 binder + real A05 oracle.
No scheduler invented, no accepted owners modified, no raw SAV/DTA.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

import rawlsing_next.pre553_original_workload_binder_candidate as a04_binder
import rawlsing_next.tests.test_pre553_route_b_production as a04_fixtures
from rawlsing_next.pre553_batch_runner import BatchManifest
from rawlsing_next.pre553_empirical_objects import ExactRef, canonical_json, semantic_hash
from rawlsing_next.pre553_route_b_production import RouteBProductionResult


# =============================================================================
# V2 CANONICAL CONTRACT
# =============================================================================

V2_CONTRACT_ID = "PYAT_HQ280_A04S_CANONICAL_V2_WORKLOAD_CONTRACT@1.0.0"
V2_SCHEMA_VERSION = "HQ280_PV3_A04S_CANONICAL_V2@1.0.0"

# --------------------------------------------------------------------------
# 1. SEMANTIC OPERATION CLASS → OWNER DISPATCH CLASS MAPPING
# --------------------------------------------------------------------------

# Semantic operation classes (scientific, what the instrument asked)
SEMANTIC_OP_CLASSES = frozenset({
    "UNARY_DISTRIBUTION",              # single target distribution
    "PAIR_RESPONSE_COTRAVEL",          # joint/conditional response co-travel
    "NONSCALAR_TOPOLOGY_PRESERVATION", # multi-select/ranked topology
    "BOUNDED_DISCOVERY",               # I05 exact bounded discovery
})

# Owner dispatch classes (what the accepted owners execute)
DISPATCH_CLASSES = frozenset({
    "I03_UNARY_OR_JOINT_QUERY",        # Route B I03 unary or joint query
    "I05_BOUNDED_DISCOVERY",           # Route B I05 exact bounded discovery
})

# Canonical mapping: semantic → dispatch (many-to-one allowed)
SEMANTIC_TO_DISPATCH: Mapping[str, str] = MappingProxyType({
    "UNARY_DISTRIBUTION": "I03_UNARY_OR_JOINT_QUERY",
    "PAIR_RESPONSE_COTRAVEL": "I03_UNARY_OR_JOINT_QUERY",
    "NONSCALAR_TOPOLOGY_PRESERVATION": "I03_UNARY_OR_JOINT_QUERY",
    "BOUNDED_DISCOVERY": "I05_BOUNDED_DISCOVERY",
})

# Reverse lookup: dispatch → set of semantics it can serve
DISPATCH_TO_SEMANTICS: Mapping[str, frozenset[str]] = MappingProxyType({
    "I03_UNARY_OR_JOINT_QUERY": frozenset({
        "UNARY_DISTRIBUTION",
        "PAIR_RESPONSE_COTRAVEL",
        "NONSCALAR_TOPOLOGY_PRESERVATION",
    }),
    "I05_BOUNDED_DISCOVERY": frozenset({"BOUNDED_DISCOVERY"}),
})

MEASURE_KINDS = frozenset({"RAW", "GOVERNED_WEIGHTED"})

EXPECTED_STATES = frozenset({"RUNNABLE", "HELD", "DENIED", "SOURCE_NONAPPLICABLE"})
NON_RUNNABLE_STATES = frozenset({"HELD", "DENIED", "SOURCE_NONAPPLICABLE"})

# Result classes
MEASURED_RESULT_CLASSES = frozenset({
    "MEASURED_POSITIVE",
    "TOPOLOGY_PRESERVED",
    "MEASURED_ZERO_IN_SUPPORTED_RISK_SET",
})
ADMISSIBLE_NULL_CLASS = "MEASURED_NULL"
FORBIDDEN_NULL_SOURCES = frozenset({
    "AUTHORITY_UNAVAILABLE", "ZERO_DENOMINATOR", "UNEXECUTED", "UNVISITED"
})
NEVER_SUCCESS_CLASSES = frozenset({
    "PARTIAL", "ADAPTIVE_PARTIAL", "UNVISITED", "UNAVAILABLE",
})


# =============================================================================
# 2. V2 ERRORS
# =============================================================================

class V2ContractError(ValueError):
    """The v2 contract candidate cannot lawfully emit the requested artifacts."""


class V2MappingError(V2ContractError):
    """Semantic ↔ dispatch mapping violation."""


class V2ReconciliationError(V2ContractError):
    """Outer reconciliation found an omission, extra, or laundered state."""


# =============================================================================
# 3. CANONICAL IDENTITY KINDS (V2 - separated from A04)
# =============================================================================

def _sha256_of(value: Any) -> str:
    return semantic_hash(value)


def v2_documentary_item_key(
    *,
    source: str,
    wave: str,
    item: str,
    form: str,
    slot: str,
    version: str = V2_SCHEMA_VERSION,
) -> str:
    """Original scientific item identity - what the instrument asked."""
    return semantic_hash({
        "kind": "V2_DOCUMENTARY_ITEM",
        "source": source,
        "wave": wave,
        "item": item,
        "form": form,
        "slot": slot,
        "version": version,
    })


def v2_semantic_operation_key(
    *,
    semantic_op_class: str,
    roles: tuple[str, ...],
    target: str,
    condition_order: tuple[str, ...] = (),
    measure_kind: str = "RAW",
    version: str = V2_SCHEMA_VERSION,
) -> str:
    """Semantic operation identity - what scientific operation is proposed.

    This is the SCIENTIFIC operation class, NOT the owner dispatch class.
    condition_order and measure_kind are part of the identity.
    """
    if semantic_op_class not in SEMANTIC_OP_CLASSES:
        raise V2ContractError(f"unsupported semantic_op_class {semantic_op_class!r}")
    if not roles:
        raise V2ContractError("semantic roles must be nonempty")
    if measure_kind not in MEASURE_KINDS:
        raise V2ContractError(f"unsupported measure_kind {measure_kind!r}")
    return semantic_hash({
        "kind": "V2_SEMANTIC_OPERATION",
        "semantic_op_class": semantic_op_class,
        "roles": list(roles),
        "target": target,
        "condition_order": list(condition_order),
        "measure_kind": measure_kind,
        "version": version,
    })


def v2_dispatch_operation_key(
    *,
    dispatch_class: str,
    roles: tuple[str, ...],
    target: str,
    condition_order: tuple[str, ...] = (),
    measure_kind: str = "RAW",
    version: str = V2_SCHEMA_VERSION,
) -> str:
    """Owner dispatch operation identity - what the executor executes."""
    if dispatch_class not in DISPATCH_CLASSES:
        raise V2ContractError(f"unsupported dispatch_class {dispatch_class!r}")
    if not roles:
        raise V2ContractError("dispatch roles must be nonempty")
    if measure_kind not in MEASURE_KINDS:
        raise V2ContractError(f"unsupported measure_kind {measure_kind!r}")
    return semantic_hash({
        "kind": "V2_DISPATCH_OPERATION",
        "dispatch_class": dispatch_class,
        "roles": list(roles),
        "target": target,
        "condition_order": list(condition_order),
        "measure_kind": measure_kind,
        "version": version,
    })


def v2_expected_work_key(
    *,
    item_key: str,
    semantic_operation_key: str,
    dispatch_operation_key: str,
    source_identity: str,
    authority_ref: str,
    risk_identity: str,
    topology_identity: str,
    version: str = V2_SCHEMA_VERSION,
) -> str:
    """Independently frozen expected work - WITHOUT consumer in the key.

    Consumer is a SEPARATE obligation, not part of the expected-work identity.
    This is the v2 fix: consumer was folded into expected_work_key in A04.
    """
    return semantic_hash({
        "kind": "V2_EXPECTED_WORK",
        "item_key": item_key,
        "semantic_operation_key": semantic_operation_key,
        "dispatch_operation_key": dispatch_operation_key,
        "source_identity": source_identity,
        "authority_ref": authority_ref,
        "risk_identity": risk_identity,
        "topology_identity": topology_identity,
        "version": version,
    })


def v2_execution_attempt_key(*, expected_work_key_value: str, attempt_index: int) -> str:
    if not isinstance(attempt_index, int) or isinstance(attempt_index, bool) or attempt_index < 1:
        raise V2ContractError("attempt_index must be a positive integer")
    return semantic_hash({
        "kind": "V2_EXECUTION_ATTEMPT",
        "expected_work_key": expected_work_key_value,
        "attempt_index": attempt_index,
        "version": V2_SCHEMA_VERSION,
    })


def v2_output_identity(
    *,
    expected_work_key_value: str,
    result_type: str,
    value: Any,
) -> str:
    return semantic_hash({
        "kind": "V2_OUTPUT_IDENTITY",
        "expected_work_key": expected_work_key_value,
        "result_type": result_type,
        "value": value,
        "version": V2_SCHEMA_VERSION,
    })


def v2_consumer_obligation_key(
    *,
    expected_work_key_value: str,
    consumer: str,
    version: str = V2_SCHEMA_VERSION,
) -> str:
    """Consumer obligation identity - SEPARATE from expected_work_key.

    This is the v2 fix: consumer obligation is a distinct identity kind,
    not folded into the expected_work_key.
    """
    return semantic_hash({
        "kind": "V2_CONSUMER_OBLIGATION",
        "expected_work_key": expected_work_key_value,
        "consumer": consumer,
        "version": version,
    })


# =============================================================================
# 4. V2 EXPECTED WORK DECLARATION (with issuer)
# =============================================================================

@dataclass(frozen=True)
class V2IssuerRecord:
    """Independent issuer record - the authority that froze this expectation.

    This is the v2 fix: explicit issuer record, not just a schema version token.
    """
    issuer_id: str
    issuer_authority_ref: str
    issuer_signature: str  # SHA-256 over issuer's declaration preimage
    issuance_timestamp: str  # ISO 8601
    scope_version: str = V2_SCHEMA_VERSION

    def projection(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "issuer_id": self.issuer_id,
            "issuer_authority_ref": self.issuer_authority_ref,
            "issuer_signature": self.issuer_signature,
            "issuance_timestamp": self.issuance_timestamp,
            "scope_version": self.scope_version,
        })


@dataclass(frozen=True)
class V2CustodianRecord:
    """Pre-run independent custodian record - frozen BEFORE execution.

    This is the v2 fix: independent custodian record established BEFORE execution,
    not merely hash-equal afterward.
    """
    custodian_id: str
    frozen_frontier_digest: str
    expectation_preimage_hash: str
    issuer_signature: str
    custodian_timestamp: str
    scope_version: str = V2_SCHEMA_VERSION

    def projection(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "custodian_id": self.custodian_id,
            "frozen_frontier_digest": self.frozen_frontier_digest,
            "expectation_preimage_hash": self.expectation_preimage_hash,
            "issuer_signature": self.issuer_signature,
            "custodian_timestamp": self.custodian_timestamp,
            "scope_version": self.scope_version,
        })


@dataclass(frozen=True)
class V2ExpectedWorkDeclaration:
    """One independently declared expected operation (v2 canonical form)."""

    source: str
    wave: str
    item: str
    form: str
    slot: str
    semantic_op_class: str
    semantic_roles: tuple[str, ...]
    target: str
    condition_order: tuple[str, ...]
    measure_kind: str
    source_identity: str
    authority_ref: str
    risk_identity: str
    topology_identity: str
    required_consumer: str
    state: str = "RUNNABLE"
    hold_reason: str | None = None
    multiplicity: int = 1
    # Owner dispatch bindings (caller-owned, already issued)
    query_ref: ExactRef | None = None
    predicate_ref: ExactRef | None = None
    discovery_authority_ref: ExactRef | None = None
    schema_version: str = V2_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.state not in EXPECTED_STATES:
            raise V2ContractError(f"invalid expected state {self.state!r}")
        if self.semantic_op_class not in SEMANTIC_OP_CLASSES:
            raise V2ContractError(f"unsupported semantic_op_class {self.semantic_op_class!r}")
        if self.measure_kind not in MEASURE_KINDS:
            raise V2ContractError(f"unsupported measure_kind {self.measure_kind!r}")
        if not self.semantic_roles:
            raise V2ContractError("semantic roles must be nonempty")
        if (
            not isinstance(self.multiplicity, int)
            or isinstance(self.multiplicity, bool)
            or self.multiplicity < 1
        ):
            raise V2ContractError("multiplicity must be a positive integer")
        if self.state in NON_RUNNABLE_STATES and not self.hold_reason:
            raise V2ContractError(
                f"{self.state} obligation must carry an exact hold/denial reason"
            )
        if self.state == "RUNNABLE" and self.hold_reason is not None:
            raise V2ContractError("RUNNABLE expected work cannot carry a hold reason")
        if self.state == "RUNNABLE":
            dispatch = SEMANTIC_TO_DISPATCH[self.semantic_op_class]
            if dispatch == "I03_UNARY_OR_JOINT_QUERY":
                if self.query_ref is None or self.predicate_ref is None:
                    raise V2ContractError(
                        "I03 expected work requires exact query_ref and predicate_ref"
                    )
                if self.discovery_authority_ref is not None:
                    raise V2ContractError(
                        "I03 expected work cannot also carry a discovery authority"
                    )
            else:
                if self.discovery_authority_ref is None:
                    raise V2ContractError(
                        "I05 expected work requires exact discovery_authority_ref"
                    )
                if self.query_ref is not None or self.predicate_ref is not None:
                    raise V2ContractError(
                        "I05 expected work cannot also carry I03 refs"
                    )
        else:
            if (
                self.query_ref is not None
                or self.predicate_ref is not None
                or self.discovery_authority_ref is not None
            ):
                raise V2ContractError(
                    "non-RUNNABLE obligations must not carry executable owner refs"
                )

    @property
    def dispatch_class(self) -> str:
        return SEMANTIC_TO_DISPATCH[self.semantic_op_class]

    @property
    def item_key(self) -> str:
        return v2_documentary_item_key(
            source=self.source, wave=self.wave, item=self.item,
            form=self.form, slot=self.slot, version=self.schema_version,
        )

    @property
    def semantic_operation_key(self) -> str:
        return v2_semantic_operation_key(
            semantic_op_class=self.semantic_op_class,
            roles=self.semantic_roles,
            target=self.target,
            condition_order=self.condition_order,
            measure_kind=self.measure_kind,
            version=self.schema_version,
        )

    @property
    def dispatch_operation_key(self) -> str:
        dispatch = self.dispatch_class
        return v2_dispatch_operation_key(
            dispatch_class=dispatch,
            roles=self.semantic_roles,
            target=self.target,
            condition_order=self.condition_order,
            measure_kind=self.measure_kind,
            version=self.schema_version,
        )

    @property
    def expected_work_key(self) -> str:
        return v2_expected_work_key(
            item_key=self.item_key,
            semantic_operation_key=self.semantic_operation_key,
            dispatch_operation_key=self.dispatch_operation_key,
            source_identity=self.source_identity,
            authority_ref=self.authority_ref,
            risk_identity=self.risk_identity,
            topology_identity=self.topology_identity,
            version=self.schema_version,
        )

    @property
    def consumer_obligation_key(self) -> str:
        return v2_consumer_obligation_key(
            expected_work_key_value=self.expected_work_key,
            consumer=self.required_consumer,
            version=self.schema_version,
        )

    @property
    def is_runnable(self) -> bool:
        return self.state == "RUNNABLE"

    def preimage(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "source": self.source,
            "wave": self.wave,
            "item": self.item,
            "form": self.form,
            "slot": self.slot,
            "semantic_op_class": self.semantic_op_class,
            "semantic_roles": list(self.semantic_roles),
            "target": self.target,
            "condition_order": list(self.condition_order),
            "measure_kind": self.measure_kind,
            "source_identity": self.source_identity,
            "authority_ref": self.authority_ref,
            "risk_identity": self.risk_identity,
            "topology_identity": self.topology_identity,
            "required_consumer": self.required_consumer,
            "state": self.state,
            "hold_reason": self.hold_reason,
            "multiplicity": self.multiplicity,
            "schema_version": self.schema_version,
            "item_key": self.item_key,
            "semantic_operation_key": self.semantic_operation_key,
            "dispatch_operation_key": self.dispatch_operation_key,
            "dispatch_class": self.dispatch_class,
            "expected_work_key": self.expected_work_key,
            "consumer_obligation_key": self.consumer_obligation_key,
        })


def v2_expected_frontier_digest(
    declarations: Iterable[V2ExpectedWorkDeclaration],
) -> str:
    """Deterministic frontier digest over the RUNNABLE expectation only."""
    keys = sorted(d.expected_work_key for d in declarations if d.is_runnable)
    return semantic_hash({"frontier": keys, "version": V2_SCHEMA_VERSION})


# =============================================================================
# 5. V2 MAPPING: SEMANTIC → DISPATCH BINDING
# =============================================================================

@dataclass(frozen=True)
class V2DispatchBinding:
    """One expected operation bound to its exact owner dispatch inputs."""

    expected_work_key: str
    dispatch_class: str
    dispatch_job_ref: ExactRef
    dispatch_predicate_ref: ExactRef | None
    dispatch_authority_ref: ExactRef
    declared_source_identity: str
    declared_condition_order: tuple[str, ...]


def _v2_owner_short_order(query: Any) -> tuple[str, ...]:
    """The issued owner's semantic target order as short item names.

    The owner carries full URN object_ids (e.g. ``urn:test:i03:...:m01-X``);
    the v2 declaration uses short item names (``X``). This extracts the short
    name from each component so the two orders can be compared exactly.
    """
    arity = query.target_arity_and_topology
    components = arity.get("components", ())
    return tuple(
        str(component["target_ref"]["object_id"]).split(":")[-1].split("-")[-1]
        for component in components
    )


def v2_bind_semantic_to_dispatch(
    *,
    declarations: Iterable[V2ExpectedWorkDeclaration],
    projection_fields: Mapping[str, Any],
    runtime_catalog: a04_binder.RuntimeObjectCatalog,
) -> tuple[V2DispatchBinding, ...]:
    """Bind v2 semantic declarations to exact owner dispatch inputs.

    Returns the exact dispatch bindings needed to execute through A04's binder.
    This is the v2 semantic → dispatch mapping.
    """
    declared = tuple(declarations)
    if not declared:
        raise V2ContractError("expected-work declaration set must be nonempty")

    runnable = tuple(d for d in declared if d.is_runnable)
    if not runnable:
        raise V2ContractError("no RUNNABLE expected work")

    bindings: dict[str, V2DispatchBinding] = {}
    for d in sorted(runnable, key=lambda x: x.expected_work_key):
        dispatch = d.dispatch_class
        authority_snapshot = a04_binder._resolve_declared_authority(
            runtime_catalog, d.authority_ref, expected_work_key_value=d.expected_work_key
        )
        if dispatch == "I03_UNARY_OR_JOINT_QUERY":
            # Verify condition_order matches the owner's exact semantic target
            # order, expressed as short item names. The v2 declaration uses
            # short names; the owner carries full URNs. Both orders must agree.
            query = runtime_catalog.resolve_query_exact(d.query_ref)
            declared_order = tuple(d.condition_order)
            owner_order = _v2_owner_short_order(query)
            if len(owner_order) > 1 and declared_order != owner_order:
                raise V2MappingError(
                    "declared condition_order does not equal owner's exact target order "
                    f"(expected_work_key={d.expected_work_key})"
                )
            binding = V2DispatchBinding(
                expected_work_key=d.expected_work_key,
                dispatch_class=dispatch,
                dispatch_job_ref=d.query_ref,
                dispatch_predicate_ref=d.predicate_ref,
                dispatch_authority_ref=authority_snapshot.ref,
                declared_source_identity=d.source_identity,
                declared_condition_order=d.condition_order,
            )
        else:
            binding = V2DispatchBinding(
                expected_work_key=d.expected_work_key,
                dispatch_class=dispatch,
                dispatch_job_ref=d.discovery_authority_ref,
                dispatch_predicate_ref=None,
                dispatch_authority_ref=authority_snapshot.ref,
                declared_source_identity=d.source_identity,
                declared_condition_order=d.condition_order,
            )
        if d.expected_work_key in bindings:
            raise V2MappingError(f"duplicate expected_work_key in dispatch bindings")
        bindings[d.expected_work_key] = binding

    return tuple(bindings[ewk] for ewk in sorted(bindings))


# =============================================================================
# 6. V2 EXECUTION THROUGH A04 BINDER (real owners)
# =============================================================================

@dataclass(frozen=True)
class V2ExecutedWorkload:
    """Result of executing through A04's real binder."""
    v2_declarations: tuple[V2ExpectedWorkDeclaration, ...]
    a04_executed: a04_binder.ExecutedWorkload
    dispatch_bindings: tuple[V2DispatchBinding, ...]
    consumer_obligations: tuple[Mapping[str, Any], ...]
    v2_frontier_hash: str


def v2_execute_through_a04(
    *,
    declarations: Iterable[V2ExpectedWorkDeclaration],
    projection_fields: Mapping[str, Any],
    runtime_catalog: a04_binder.RuntimeObjectCatalog,
    source: Any,
) -> V2ExecutedWorkload:
    """Execute v2 declarations through A04's real binder (real owners)."""
    declared = tuple(declarations)
    dispatch_bindings = v2_bind_semantic_to_dispatch(
        declarations=declared,
        projection_fields=projection_fields,
        runtime_catalog=runtime_catalog,
    )

    # Build A04 declarations from v2 declarations (both runnable and held).
    # The v2 canonical form uses short item names in condition_order; the A04
    # binder (unmodified) requires the owner's exact full URN target tokens.
    # Translate short names to the owner's exact tokens here.
    a04_decls = []
    for d in declared:
        if d.dispatch_class == "I03_UNARY_OR_JOINT_QUERY":
            owner_tokens = tuple(d.condition_order)
            if d.query_ref is not None and d.is_runnable:
                query = runtime_catalog.resolve_query_exact(d.query_ref)
                full_order = tuple(
                    str(component["target_ref"]["object_id"])
                    for component in query.target_arity_and_topology.get("components", ())
                )
                if len(full_order) > 1:
                    owner_tokens = full_order
            a04_decls.append(a04_binder.ExpectedWorkDeclaration(
                source=d.source, wave=d.wave, item=d.item, form=d.form, slot=d.slot,
                op_class="I03_UNARY_OR_JOINT_QUERY", roles=d.semantic_roles, target=d.target,
                condition_order=owner_tokens, measure_kind=d.measure_kind,
                source_identity=d.source_identity, authority_ref=d.authority_ref,
                risk_identity=d.risk_identity, topology_identity=d.topology_identity,
                required_consumer=d.required_consumer, state=d.state,
                hold_reason=d.hold_reason, multiplicity=d.multiplicity,
                query_ref=d.query_ref, predicate_ref=d.predicate_ref,
                schema_version=d.schema_version,
            ))
        else:
            a04_decls.append(a04_binder.ExpectedWorkDeclaration(
                source=d.source, wave=d.wave, item=d.item, form=d.form, slot=d.slot,
                op_class="I05_BOUNDED_DISCOVERY", roles=d.semantic_roles, target=d.target,
                condition_order=d.condition_order, measure_kind=d.measure_kind,
                source_identity=d.source_identity, authority_ref=d.authority_ref,
                risk_identity=d.risk_identity, topology_identity=d.topology_identity,
                required_consumer=d.required_consumer, state=d.state,
                hold_reason=d.hold_reason, multiplicity=d.multiplicity,
                discovery_authority_ref=d.discovery_authority_ref,
                schema_version=d.schema_version,
            ))

    # Execute through A04's real binder
    a04_executed = a04_binder.execute_bound_workload(
        bound=a04_binder.bind_expected_work(
            declarations=a04_decls,
            projection_fields=projection_fields,
            runtime_catalog=runtime_catalog,
        ),
        source=source,
    )

    # Build consumer obligations (SEPARATE from expected-work identity)
    consumer_obligations = tuple(
        MappingProxyType({
            "expected_work_key": d.expected_work_key,
            "consumer": d.required_consumer,
            "consumer_obligation_key": d.consumer_obligation_key,
            "item": d.item,
        })
        for d in sorted(declared, key=lambda x: x.expected_work_key)
        if d.is_runnable
    )

    # Compute v2 frontier hash BEFORE execution (for anti-laundering check)
    v2_frontier_hash = v2_expected_frontier_digest(declared)

    return V2ExecutedWorkload(
        v2_declarations=declared,
        a04_executed=a04_executed,
        dispatch_bindings=dispatch_bindings,
        consumer_obligations=consumer_obligations,
        v2_frontier_hash=v2_frontier_hash,
    )


# =============================================================================
# 7. V2 RECONCILIATION (A05-compatible no-drop)
# =============================================================================

@dataclass(frozen=True)
class V2ReconciliationVerdict:
    ok: bool
    work_reconciled: bool
    failures: tuple[Mapping[str, Any], ...]
    expected_keys: tuple[str, ...]
    job_keys: tuple[str, ...]
    omitted: tuple[str, ...]
    extra: tuple[str, ...]
    visible_non_runnable: tuple[str, ...]
    result_classes: Mapping[str, str]
    consumer_obligations: tuple[Mapping[str, Any], ...]
    unsatisfied_consumers: tuple[Mapping[str, Any], ...]
    frontier_hash: str
    declared_frontier_hash: str

    def failure_codes(self) -> tuple[str, ...]:
        return tuple(sorted({str(f["code"]) for f in self.failures}))


def _v2_fail(code: str, detail: Any) -> Mapping[str, Any]:
    return MappingProxyType({"code": code, "detail": detail})


def v2_reconcile(
    *,
    declarations: Iterable[V2ExpectedWorkDeclaration],
    executed: V2ExecutedWorkload,
    consumer_receipts: Iterable[Mapping[str, Any]] = (),
) -> V2ReconciliationVerdict:
    """V2 reconciliation - A05-compatible no-drop with separated consumer obligations."""
    declared = tuple(declarations)
    by_key = {d.expected_work_key: d for d in declared}
    if len(by_key) != len(declared):
        raise V2ContractError("duplicate expected_work_key in declarations")

    a04_executed = executed.a04_executed
    result = a04_executed.production_result
    bound = a04_executed.bound

    # ---- Build mapping from v2 expected_work_key -> A04 job plan key via dispatch bindings ----
    v2_to_a04_key = {}
    for binding in executed.dispatch_bindings:
        # Find the A04 job plan with matching job_ref
        for plan in a04_executed.bound.job_plans:
            if plan.job_ref == binding.dispatch_job_ref:
                v2_to_a04_key[binding.expected_work_key] = plan.expected_work_key
                break

    # ---- J: constructed jobs via the REAL batch manifest ----
    plan_by_expectation = {plan.expected_work_key: plan for plan in a04_executed.bound.job_plans}
    receipts_by_unit = {r.unit_ref.key: r for r in a04_executed.batch_receipts}
    plan_by_unit = {}
    for unit in a04_executed.batch_manifest.units:
        for plan in a04_executed.bound.job_plans:
            if unit.job_kind == plan.job_kind and unit.job_ref == plan.job_ref:
                plan_by_unit[unit.unit_ref.key] = plan
                break

    produced_by_expectation: dict[str, Any] = {}
    multiplicity_by_expectation: dict[str, int] = {}
    execution_state_by_expectation: dict[str, str | None] = {}

    query_to_expectation: dict[str, str] = {}
    for d in declared:
        if d.is_runnable and d.dispatch_class == "I03_UNARY_OR_JOINT_QUERY":
            query_to_expectation[d.query_ref.key] = d.expected_work_key
    for item in result.i03_results:
        ewk = query_to_expectation.get(item.query_ref.key)
        if ewk is None:
            continue
        if item.facts:
            produced_by_expectation[ewk] = item.facts[0]
            multiplicity_by_expectation[ewk] = len(item.facts)

    discovery_ewk = next(
        (d.expected_work_key for d in declared
         if d.is_runnable and d.dispatch_class == "I05_BOUNDED_DISCOVERY"),
        None,
    )
    if discovery_ewk is not None and result.i05_result.receipts:
        produced_by_expectation[discovery_ewk] = result.i05_result.receipts[0]
        multiplicity_by_expectation[discovery_ewk] = len(result.i05_result.receipts)

    for unit_key, plan in plan_by_unit.items():
        receipt = receipts_by_unit.get(unit_key)
        a04_ewk = plan.expected_work_key
        v2_ewk = None
        for v2_ek, a04_ek in v2_to_a04_key.items():
            if a04_ek == a04_ewk:
                v2_ewk = v2_ek
                break
        if v2_ewk:
            execution_state_by_expectation[v2_ewk] = (
                None if receipt is None else receipt.state
            )

    expected_keys = tuple(sorted(d.expected_work_key for d in declared if d.is_runnable))
    job_keys = tuple(sorted(v2_to_a04_key.values()))
    non_runnable_keys = tuple(
        sorted(d.expected_work_key for d in declared if not d.is_runnable)
    )

    failures: list[Mapping[str, Any]] = []

    # ---- Also build expected A04 keys from the DECLARED universe (for extra detection) ----
    # Must use the SAME URN-token translation as v2_execute_through_a04.
    catalog = executed.a04_executed.bound.runtime_catalog
    declared_to_a04_key = {}
    for d in declared:
        if not d.is_runnable:
            continue
        dispatch = d.dispatch_class
        if dispatch == "I03_UNARY_OR_JOINT_QUERY":
            tokens = tuple(d.condition_order)
            if d.query_ref is not None:
                query = catalog.resolve_query_exact(d.query_ref)
                full = tuple(
                    str(component["target_ref"]["object_id"])
                    for component in query.target_arity_and_topology.get("components", ())
                )
                if len(full) > 1:
                    tokens = full
            a04_decl = a04_binder.ExpectedWorkDeclaration(
                source=d.source, wave=d.wave, item=d.item, form=d.form, slot=d.slot,
                op_class="I03_UNARY_OR_JOINT_QUERY", roles=d.semantic_roles, target=d.target,
                condition_order=tokens, measure_kind=d.measure_kind,
                source_identity=d.source_identity, authority_ref=d.authority_ref,
                risk_identity=d.risk_identity, topology_identity=d.topology_identity,
                required_consumer=d.required_consumer, state=d.state,
                hold_reason=d.hold_reason, multiplicity=d.multiplicity,
                query_ref=d.query_ref, predicate_ref=d.predicate_ref,
                schema_version=d.schema_version,
            )
        else:
            a04_decl = a04_binder.ExpectedWorkDeclaration(
                source=d.source, wave=d.wave, item=d.item, form=d.form, slot=d.slot,
                op_class="I05_BOUNDED_DISCOVERY", roles=d.semantic_roles, target=d.target,
                condition_order=d.condition_order, measure_kind=d.measure_kind,
                source_identity=d.source_identity, authority_ref=d.authority_ref,
                risk_identity=d.risk_identity, topology_identity=d.topology_identity,
                required_consumer=d.required_consumer, state=d.state,
                hold_reason=d.hold_reason, multiplicity=d.multiplicity,
                discovery_authority_ref=d.discovery_authority_ref,
                schema_version=d.schema_version,
            )
        declared_to_a04_key[d.expected_work_key] = a04_decl.expected_work_key

    expected_a04_keys = set(declared_to_a04_key.values())

    # 1. omission (outer join keeps absent mappings visible)
    # Compare in A04 key space: v2 expected -> A04 key mapping
    expected_a04_keys = set(declared_to_a04_key.values())
    omitted_v2 = tuple(sorted(
        ewk for ewk in expected_keys
        if declared_to_a04_key.get(ewk) not in job_keys
    ))
    if omitted_v2:
        failures.append(_fail("EXPECTED_OPERATION_OMITTED", list(omitted_v2)))

    # 2. unauthorized extra
    extra = tuple(sorted(set(job_keys) - expected_a04_keys))
    if extra:
        failures.append(_fail("UNAUTHORIZED_EXTRA_JOB", list(extra)))

    # 3. held/denied/NA never executed, always visible
    for d in declared:
        if d.is_runnable:
            continue
        # Check visibility in A04 bound held_frontier using A04's expected_work_key
        a04_held_key = a04_binder.expected_work_key(
            item_key=a04_binder.documentary_item_key(
                source=d.source, wave=d.wave, item=d.item,
                form=d.form, slot=d.slot, version=d.schema_version,
            ),
            operation_key_value=a04_binder.operation_key(
                op_class=d.dispatch_class,
                roles=d.semantic_roles,
                target=d.target,
                condition_order=d.condition_order,
                measure_kind=d.measure_kind,
                version=d.schema_version,
            ),
            source_identity=d.source_identity,
            authority_ref=d.authority_ref,
            risk_identity=d.risk_identity,
            topology_identity=d.topology_identity,
            consumer=d.required_consumer,
            version=d.schema_version,
        )
        if a04_held_key in set(job_keys):
            failures.append(
                _fail("HELD_OR_DENIED_WORK_EXECUTED", {"item": d.item, "state": d.state})
            )
        visible = {row["expected_work_key"] for row in executed.a04_executed.bound.held_frontier}
        if a04_held_key not in visible:
            failures.append(
                _fail("HELD_OR_DENIED_WORK_NOT_VISIBLE", {"item": d.item, "state": d.state})
            )

    # 4. typed results; no laundering
    result_classes: dict[str, str] = {}
    for ewk in expected_keys:
        d = by_key[ewk]
        receipt_state = execution_state_by_expectation.get(ewk)
        observed = multiplicity_by_expectation.get(ewk, 0)
        klass = a04_binder._classify_result(
            expected_work_key_value=ewk,
            declared_measure_kind=d.measure_kind,
            produced_fact=produced_by_expectation.get(ewk),
            executed=observed > 0,
            batch_state=receipt_state,
            expected_multiplicity=d.multiplicity,
            observed_multiplicity=observed,
        )
        result_classes[ewk] = klass
        if klass == "MISSING_TYPED_RESULT":
            failures.append(_fail("MISSING_TYPED_RESULT", ewk))
        if klass == "UNEXECUTED":
            failures.append(_fail("EXPECTED_OPERATION_OMITTED", ewk))
        if klass == "MULTIPLICITY_MISMATCH":
            failures.append(
                _fail("EXPECTED_MULTIPLICITY_MISMATCH", {
                    "expected_work_key": ewk,
                    "expected": d.multiplicity,
                    "observed": observed,
                })
            )
        if klass in NEVER_SUCCESS_CLASSES:
            failures.append(
                _fail("PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS", {
                    "expected_work_key": ewk, "class": klass,
                })
            )
        if d.measure_kind == "GOVERNED_WEIGHTED":
            fact = produced_by_expectation.get(ewk)
            if fact is not None and getattr(fact, "typed_state", "") == "UNAVAILABLE":
                failures.append(
                    _fail("FALSE_EMPIRICAL_NULL", {
                        "expected_work_key": ewk, "null_source": "AUTHORITY_UNAVAILABLE",
                    })
                )

    # 5. candidate own-_dk / co-topic joint
    for plan in bound.job_plans:
        if plan.job_kind != "QUERY" or len(plan.condition_order) < 2:
            continue
        base = lambda token: token[:-3] if token.endswith("_dk") else token
        first, second = plan.condition_order[0], plan.condition_order[1]
        if base(first) == base(second):
            failures.append(
                _fail("CANDIDATE_OWN_DK_JOINT", {
                    "conditioner": first, "target": second,
                    "basis": "constructed job own exact target order",
                })
            )

    # 6. expectation must not be derived from produced manifest
    rebuilt = v2_expected_frontier_digest(declared)
    # Compare against the v2 frontier hash computed BEFORE execution
    if rebuilt != executed.v2_frontier_hash:
        failures.append(
            _fail("EXPECTED_SET_OUTPUT_DERIVED", {
                "bound_frontier": executed.v2_frontier_hash,
                "recomputed": rebuilt,
            })
        )

    # 7. source identity: every CONSTRUCTED job and every declared
    #         expectation must name the exact source the owners ran against
    owner_source_sha = str(result.source_identity.get("source_sha256", ""))
    for d in declared:
        if not d.is_runnable:
            continue
        if d.source_identity != owner_source_sha:
            failures.append(
                _fail("SOURCE_IDENTITY_MISMATCH", {
                    "expected_work_key": d.expected_work_key,
                    "side": "DECLARED_EXPECTATION",
                    "declared_source_identity": d.source_identity,
                    "owner_source_sha256": owner_source_sha,
                })
            )
    for plan in bound.job_plans:
        if plan.declared_source_identity != owner_source_sha:
            failures.append(
                _fail("SOURCE_IDENTITY_MISMATCH", {
                    "expected_work_key": plan.expected_work_key,
                    "side": "CONSTRUCTED_JOB",
                    "declared_source_identity": plan.declared_source_identity,
                    "owner_source_sha256": owner_source_sha,
                })
            )

    # 8. required consumers (SEPARATE obligation, distinct from expected work)
    obligations = executed.consumer_obligations
    satisfied = {
        (str(receipt.get("expected_work_key")), str(receipt.get("consumer")))
        for receipt in consumer_receipts
    }
    unsatisfied = tuple(
        MappingProxyType(dict(obligation))
        for obligation in obligations
        if (obligation["expected_work_key"], obligation["consumer"]) not in satisfied
    )
    if unsatisfied:
        failures.append(
            _fail("REQUIRED_CONSUMER_OMITTED", [dict(u) for u in unsatisfied])
        )

    work_failures = tuple(
        failure
        for failure in failures
        if failure["code"] != "REQUIRED_CONSUMER_OMITTED"
    )

    return V2ReconciliationVerdict(
        ok=not failures,
        work_reconciled=not work_failures,
        failures=tuple(failures),
        expected_keys=expected_keys,
        job_keys=job_keys,
        omitted=omitted_v2,
        extra=extra,
        visible_non_runnable=non_runnable_keys,
        result_classes=MappingProxyType(result_classes),
        consumer_obligations=obligations,
        unsatisfied_consumers=unsatisfied,
        frontier_hash=executed.a04_executed.bound.expected_frontier_hash,
        declared_frontier_hash=rebuilt,
    )


def _fail(code: str, detail: Any) -> Mapping[str, Any]:
    return MappingProxyType({"code": code, "detail": detail})


def v2_fail_on_reconciliation(verdict: V2ReconciliationVerdict) -> None:
    if not verdict.ok:
        codes = ", ".join(verdict.failure_codes())
        raise V2ReconciliationError(f"v2 expected-work reconciliation failed: {codes}")


# =============================================================================
# 8. V2 COMPATIBILITY LAYER (for A05 oracle interop)
# =============================================================================

def v2_to_a05_universe(
    declarations: Iterable[V2ExpectedWorkDeclaration],
    issuer: V2IssuerRecord | None = None,
) -> Mapping[str, Any]:
    """Translate v2 declarations to A05 oracle format for interop testing.

    This is a TRANSLATION, not derivation - the v2 universe is independently
    declared; this is only for interop verification against A05's oracle.
    """
    declared = tuple(declarations)
    E, H, D, NA = [], [], [], []

    for d in declared:
        if not d.is_runnable:
            base = {
                "expected_work_key": d.expected_work_key,
                "documentary_item_key": d.item_key,
                "operation_key": d.semantic_operation_key,
                "item": d.item,
                "state": d.state,
                "reason": d.hold_reason,
                "runnable": False,
            }
            if d.state == "HELD":
                H.append(base)
            elif d.state == "DENIED":
                D.append(base)
            else:
                NA.append(base)
            continue

        E.append({
            "expected_work_key": d.expected_work_key,
            "documentary_item_key": d.item_key,
            "operation_key": d.semantic_operation_key,
            "op_class": d.semantic_op_class,
            "roles": list(d.semantic_roles),
            "target": d.target,
            "topology": d.topology_identity,
            "required_consumer": d.required_consumer,
            "authority": d.authority_ref,
            "risk": d.risk_identity,
            "item": d.item,
            "form": d.form,
            "slot": d.slot,
            "source": d.source,
            "wave": d.wave,
        })

    schema = V2_SCHEMA_VERSION
    if issuer:
        schema = issuer.scope_version

    return {
        "schema": schema,
        "E": E, "H": H, "D": D, "NA": NA,
        "frontier_digest": semantic_hash([e["expected_work_key"] for e in sorted(E, key=lambda x: x["expected_work_key"])]),
    }


# =============================================================================
# 9. EXPORTS
# =============================================================================

__all__ = [
    "V2_CONTRACT_ID",
    "V2_SCHEMA_VERSION",
    "SEMANTIC_OP_CLASSES",
    "DISPATCH_CLASSES",
    "SEMANTIC_TO_DISPATCH",
    "DISPATCH_TO_SEMANTICS",
    "MEASURE_KINDS",
    "EXPECTED_STATES",
    "NON_RUNNABLE_STATES",
    "MEASURED_RESULT_CLASSES",
    "ADMISSIBLE_NULL_CLASS",
    "FORBIDDEN_NULL_SOURCES",
    "NEVER_SUCCESS_CLASSES",
    "V2ContractError",
    "V2MappingError",
    "V2ReconciliationError",
    "v2_documentary_item_key",
    "v2_semantic_operation_key",
    "v2_dispatch_operation_key",
    "v2_expected_work_key",
    "v2_execution_attempt_key",
    "v2_output_identity",
    "v2_consumer_obligation_key",
    "V2IssuerRecord",
    "V2CustodianRecord",
    "V2ExpectedWorkDeclaration",
    "v2_expected_frontier_digest",
    "V2DispatchBinding",
    "v2_bind_semantic_to_dispatch",
    "V2ExecutedWorkload",
    "v2_execute_through_a04",
    "V2ReconciliationVerdict",
    "v2_reconcile",
    "v2_fail_on_reconciliation",
    "v2_to_a05_universe",
]