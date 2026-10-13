"""PYAT HQ280 PV3 A04 - source-free authorized workload binder CANDIDATE.

Development-only candidate.  It binds an independently frozen, source-scoped
expected-work preimage into the ALREADY ACCEPTED Rawlsing owners:

  * ``bind_governed_c11_projection``  -> real ``GovernedC11Projection``
  * ``RuntimeObjectCatalog``          -> real authority/predicate/query/I05 catalog
  * ``I03ExecutionRequest``           -> real Route B I03 request list
  * ``execute_route_b_production``    -> real C11 -> I03 -> I05 effects
  * ``BatchUnitSpec``/``BatchManifest`` -> real batch unit identities

It is a BINDER, not an issuer and not a replacement engine.  It creates no
source meaning, no authority, no candidate frontier and no discovery rule; all
of those arrive as already-issued caller-owned inputs.  It performs no
structural, causal, model, publication, currentness or actor work.

Identity law (kept strictly separate, per ACTION_PLAN.md A04):

    documentary_item_key -> original scientific item (what was asked)
    operation_key        -> eligible operation (what is proposed)
    expected_work_key    -> independently frozen expected work
    job_key              -> executable job constructed for a real owner
    result/output id     -> produced result of one execution attempt

``expected_work_key`` is computed from a COMPLETE, VERSIONED canonical preimage
before any owner is invoked, so the expectation cannot be laundered from a
produced manifest.  Reconciliation is an OUTER join so that an expected
operation with no constructed job stays visible as an omission rather than
disappearing from an inner join.

Ceiling: source-free development only.  Nothing here grants original-source
use, all-35 scientific eligibility, new model permission or canonical adoption.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner,
    BatchManifest,
    BatchUnitSpec,
    ExecutionOutcome,
    ExecutorBinding,
)
from rawlsing_next.pre553_carrier_execution import (
    RuntimeObjectCatalog,
    bind_governed_c11_projection,
)
from rawlsing_next.pre553_empirical_objects import (
    ExactRef,
    canonical_json,
    semantic_hash,
)
from rawlsing_next.pre553_route_b_production import (
    I03ExecutionRequest,
    RouteBProductionResult,
    execute_route_b_production,
)
from rawlsing_next.pre553_source_backed_c11_facade import GovernedC11Projection


BINDER_CANDIDATE_CONTRACT_ID = "PYAT_HQ280_A04_SOURCEFREE_WORKLOAD_BINDER_CANDIDATE@1.0.0"
EXPECTED_WORK_SCHEMA_VERSION = "HQ280_PV3_A04_EXPECTED_WORK@1.0.0"

#: Declarative compatibility with the independent A05 oracle's public contract.
#: These are the SAME tokens A05 published at
#: ``9491d0296c95ee2942fe80eadc6aa9f54b07c634``; this module does not import or
#: depend on A05 and does not derive its expected set from A05's fixture.
A05_COMPATIBLE_SCHEMA_VERSION = "HQ280_PV3_A05_EXPECTED_WORK@1.0.0"

EXPECTED_STATES = frozenset({"RUNNABLE", "HELD", "DENIED", "SOURCE_NONAPPLICABLE"})

#: States that may never appear as an executable constructed job.
NON_RUNNABLE_STATES = frozenset({"HELD", "DENIED", "SOURCE_NONAPPLICABLE"})

#: Result classes that are legitimately measured (never a null, never absence).
MEASURED_RESULT_CLASSES = frozenset({
    "MEASURED_POSITIVE",
    "TOPOLOGY_PRESERVED",
    "MEASURED_ZERO_IN_SUPPORTED_RISK_SET",
})

#: The only admissible null.
ADMISSIBLE_NULL_CLASS = "MEASURED_NULL"

#: Sources that may NEVER launder into an admissible empirical null.
FORBIDDEN_NULL_SOURCES = frozenset({
    "AUTHORITY_UNAVAILABLE",
    "ZERO_DENOMINATOR",
    "UNEXECUTED",
    "UNVISITED",
})

#: Never-success result classes.
NEVER_SUCCESS_CLASSES = frozenset({
    "PARTIAL",
    "ADAPTIVE_PARTIAL",
    "UNVISITED",
    "UNAVAILABLE",
})

#: Owner job classes this candidate is allowed to construct.
SUPPORTED_JOB_CLASSES = frozenset({
    "I03_UNARY_OR_JOINT_QUERY",
    "I05_BOUNDED_DISCOVERY",
})

#: Measure kinds the real I03 owner supports.
MEASURE_KINDS = frozenset({"RAW", "GOVERNED_WEIGHTED"})


class BinderCandidateError(ValueError):
    """The binder candidate cannot lawfully emit the requested owner inputs."""


class BinderReconciliationError(BinderCandidateError):
    """Outer reconciliation found an omission, an extra, or a laundered state."""


def _sha256_of(value: Any) -> str:
    return semantic_hash(value)


def _exact(ref: ExactRef, label: str) -> ExactRef:
    if not isinstance(ref, ExactRef):
        raise BinderCandidateError(f"{label} must be an exact ExactRef")
    return ref


def _resolve_declared_authority(
    catalog: RuntimeObjectCatalog,
    authority_identity: str,
    *,
    expected_work_key_value: str,
):
    """Resolve a declared authority identity against the caller-issued catalog.

    The binder never creates authority.  It only proves that the authority the
    caller declared is present, exact and immutable in the issued catalog.
    """
    matches = [
        snapshot
        for snapshot in catalog.authorities
        if snapshot.authority_ref.key == authority_identity
    ]
    if len(matches) != 1:
        raise BinderCandidateError(
            "declared operation authority is not exactly present in the issued "
            f"RuntimeObjectCatalog (expected_work_key={expected_work_key_value})"
        )
    return matches[0]


# --------------------------------------------------------------------------
# 1. Distinct identity kinds
# --------------------------------------------------------------------------
def documentary_item_key(
    *,
    source: str,
    wave: str,
    item: str,
    form: str,
    slot: str,
    version: str = EXPECTED_WORK_SCHEMA_VERSION,
) -> str:
    """Original scientific item identity - what the instrument asked."""
    return _sha256_of({
        "kind": "DOCUMENTARY_ITEM",
        "source": source,
        "wave": wave,
        "item": item,
        "form": form,
        "slot": slot,
        "version": version,
    })


def operation_key(
    *,
    op_class: str,
    roles: tuple[str, ...],
    target: str,
    condition_order: tuple[str, ...] = (),
    measure_kind: str = "RAW",
    version: str = EXPECTED_WORK_SCHEMA_VERSION,
) -> str:
    """Eligible operation identity - what operation is proposed.

    ``condition_order`` is part of the identity: q(C|A) and q(C|A,B) are
    DIFFERENT operations and must never share an operation key.

    ``measure_kind`` is part of the operation finite grammar: RAW and
    GOVERNED_WEIGHTED are distinct operations even on one administered item,
    so they must never collide on one operation key.
    """
    if op_class not in SUPPORTED_JOB_CLASSES:
        raise BinderCandidateError(f"unsupported op_class {op_class!r}")
    if not roles:
        raise BinderCandidateError("operation roles must be nonempty")
    if measure_kind not in MEASURE_KINDS:
        raise BinderCandidateError(f"unsupported measure_kind {measure_kind!r}")
    return _sha256_of({
        "kind": "ELIGIBLE_OPERATION",
        "op_class": op_class,
        "roles": list(roles),
        "target": target,
        "condition_order": list(condition_order),
        "measure_kind": measure_kind,
        "version": version,
    })


def expected_work_key(
    *,
    item_key: str,
    operation_key_value: str,
    source_identity: str,
    authority_ref: str,
    risk_identity: str,
    topology_identity: str,
    consumer: str,
    version: str = EXPECTED_WORK_SCHEMA_VERSION,
) -> str:
    """Independently frozen expected work - computed BEFORE any owner runs."""
    return _sha256_of({
        "kind": "EXPECTED_WORK",
        "item_key": item_key,
        "operation_key": operation_key_value,
        "source_identity": source_identity,
        "authority_ref": authority_ref,
        "risk_identity": risk_identity,
        "topology_identity": topology_identity,
        "consumer": consumer,
        "version": version,
    })


def execution_attempt_key(*, expected_work_key_value: str, attempt_index: int) -> str:
    """One attempt at that work - distinct from the expected work itself."""
    if not isinstance(attempt_index, int) or isinstance(attempt_index, bool) or attempt_index < 1:
        raise BinderCandidateError("attempt_index must be a positive integer")
    return _sha256_of({
        "kind": "EXECUTION_ATTEMPT",
        "expected_work_key": expected_work_key_value,
        "attempt_index": attempt_index,
        "version": EXPECTED_WORK_SCHEMA_VERSION,
    })


def output_identity(
    *,
    expected_work_key_value: str,
    result_type: str,
    value: Any,
) -> str:
    """Produced result identity - distinct from job and expectation."""
    return _sha256_of({
        "kind": "OUTPUT_IDENTITY",
        "expected_work_key": expected_work_key_value,
        "result_type": result_type,
        "value": value,
        "version": EXPECTED_WORK_SCHEMA_VERSION,
    })


# --------------------------------------------------------------------------
# 2. Frozen expected-work declarations (external INPUT, not derived output)
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class ExpectedWorkDeclaration:
    """One independently declared expected operation.

    This is an INPUT.  The binder never creates, widens or silently drops
    these; it only projects declared RUNNABLE work onto real owner inputs and
    reconciles the result back against this declaration.
    """

    source: str
    wave: str
    item: str
    form: str
    slot: str
    op_class: str
    roles: tuple[str, ...]
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
    # The exact pre-existing owner inputs this expected operation binds onto.
    # They are caller-owned, already issued objects - never synthesized here.
    query_ref: ExactRef | None = None
    predicate_ref: ExactRef | None = None
    discovery_authority_ref: ExactRef | None = None
    schema_version: str = EXPECTED_WORK_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.state not in EXPECTED_STATES:
            raise BinderCandidateError(f"invalid expected state {self.state!r}")
        if self.op_class not in SUPPORTED_JOB_CLASSES:
            raise BinderCandidateError(f"unsupported op_class {self.op_class!r}")
        if self.measure_kind not in MEASURE_KINDS:
            raise BinderCandidateError(f"unsupported measure_kind {self.measure_kind!r}")
        if not self.roles:
            raise BinderCandidateError("roles must be nonempty")
        if (
            not isinstance(self.multiplicity, int)
            or isinstance(self.multiplicity, bool)
            or self.multiplicity < 1
        ):
            raise BinderCandidateError("multiplicity must be a positive integer")
        if self.state in NON_RUNNABLE_STATES and not self.hold_reason:
            raise BinderCandidateError(
                f"{self.state} obligation must carry an exact hold/denial reason"
            )
        if self.state == "RUNNABLE" and self.hold_reason is not None:
            raise BinderCandidateError("RUNNABLE expected work cannot carry a hold reason")
        if self.state == "RUNNABLE":
            if self.op_class == "I03_UNARY_OR_JOINT_QUERY":
                if self.query_ref is None or self.predicate_ref is None:
                    raise BinderCandidateError(
                        "I03 expected work requires exact query_ref and predicate_ref"
                    )
                if self.discovery_authority_ref is not None:
                    raise BinderCandidateError(
                        "I03 expected work cannot also carry a discovery authority"
                    )
            else:
                if self.discovery_authority_ref is None:
                    raise BinderCandidateError(
                        "I05 expected work requires exact discovery_authority_ref"
                    )
                if self.query_ref is not None or self.predicate_ref is not None:
                    raise BinderCandidateError(
                        "I05 expected work cannot also carry I03 refs"
                    )
        else:
            if (
                self.query_ref is not None
                or self.predicate_ref is not None
                or self.discovery_authority_ref is not None
            ):
                raise BinderCandidateError(
                    "non-RUNNABLE obligations must not carry executable owner refs"
                )
        for ref, label in (
            (self.query_ref, "query_ref"),
            (self.predicate_ref, "predicate_ref"),
            (self.discovery_authority_ref, "discovery_authority_ref"),
        ):
            if ref is not None:
                _exact(ref, label)

    @property
    def item_key(self) -> str:
        return documentary_item_key(
            source=self.source,
            wave=self.wave,
            item=self.item,
            form=self.form,
            slot=self.slot,
            version=self.schema_version,
        )

    @property
    def operation_key_value(self) -> str:
        return operation_key(
            op_class=self.op_class,
            roles=self.roles,
            target=self.target,
            condition_order=self.condition_order,
            measure_kind=self.measure_kind,
            version=self.schema_version,
        )

    @property
    def expected_work_key(self) -> str:
        return expected_work_key(
            item_key=self.item_key,
            operation_key_value=self.operation_key_value,
            source_identity=self.source_identity,
            authority_ref=self.authority_ref,
            risk_identity=self.risk_identity,
            topology_identity=self.topology_identity,
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
            "op_class": self.op_class,
            "roles": list(self.roles),
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
            "documentary_item_key": self.item_key,
            "operation_key": self.operation_key_value,
            "expected_work_key": self.expected_work_key,
        })


def expected_frontier_digest(
    declarations: Iterable[ExpectedWorkDeclaration],
) -> str:
    """Deterministic frontier digest over the RUNNABLE expectation only."""
    keys = sorted(d.expected_work_key for d in declarations if d.is_runnable)
    return _sha256_of({"frontier": keys, "version": EXPECTED_WORK_SCHEMA_VERSION})


# --------------------------------------------------------------------------
# 3. The binder
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class JobPlan:
    """One declared executable job, before a real C11 release ref is attached."""

    expected_work_key: str
    job_kind: str
    job_ref: ExactRef
    predicate_ref: ExactRef | None
    authority_ref: ExactRef
    declared_source_identity: str
    condition_order: tuple[str, ...] = ()

    def preimage(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "expected_work_key": self.expected_work_key,
            "job_kind": self.job_kind,
            "job_ref": self.job_ref.as_dict(),
            "predicate_ref": None if self.predicate_ref is None else self.predicate_ref.as_dict(),
            "authority_ref": self.authority_ref.as_dict(),
            "declared_source_identity": self.declared_source_identity,
            "condition_order": list(self.condition_order),
        })


@dataclass(frozen=True)
class BoundWorkload:
    """Exact owner inputs produced from an independently frozen expectation."""

    projection: GovernedC11Projection
    runtime_catalog: RuntimeObjectCatalog
    i03_requests: tuple[I03ExecutionRequest, ...]
    discovery_authority_ref: ExactRef
    job_plans: tuple[JobPlan, ...]
    expected_frontier_ref: ExactRef
    expected_frontier_hash: str
    held_frontier: tuple[Mapping[str, Any], ...]
    expectation_preimage_hash: str
    effects: Mapping[str, bool]


def _bind_effects() -> Mapping[str, bool]:
    return MappingProxyType({
        "source_meaning_inference": False,
        "authority_creation": False,
        "candidate_frontier_invention": False,
        "structural_truth_effect": False,
        "causal_truth_effect": False,
        "model_permission_effect": False,
        "learned_product_publication_effect": False,
        "actor_v3_effect": False,
    })


def _owner_target_order(query: Any) -> tuple[str, ...]:
    """The issued owner's own semantic target order, exactly as declared."""
    arity = query.target_arity_and_topology
    components = arity.get("components", ())
    return tuple(
        str(component["target_ref"]["object_id"]) for component in components
    )


def bind_expected_work(
    *,
    declarations: Iterable[ExpectedWorkDeclaration],
    projection_fields: Mapping[str, Any],
    runtime_catalog: RuntimeObjectCatalog,
) -> BoundWorkload:
    """Bind a frozen expected-work preimage onto the real existing owners.

    Uses only already-implemented factories: ``bind_governed_c11_projection``,
    ``RuntimeObjectCatalog`` (caller-issued), ``I03ExecutionRequest``,
    ``BatchUnitSpec`` and ``BatchManifest``.  No replacement scheduler,
    no replacement engine and no invented frontier.
    """
    if not isinstance(runtime_catalog, RuntimeObjectCatalog):
        raise BinderCandidateError("caller-owned exact RuntimeObjectCatalog is required")

    declared = tuple(declarations)
    if not declared:
        raise BinderCandidateError("expected-work declaration set must be nonempty")

    # ---- expectation is frozen and made visible BEFORE any owner call ----
    expectation_preimage = {
        "schema_version": EXPECTED_WORK_SCHEMA_VERSION,
        "declarations": [
            dict(d.preimage())
            for d in sorted(declared, key=lambda x: x.expected_work_key)
        ],
    }
    expectation_preimage_hash = _sha256_of(expectation_preimage)
    expected_frontier_hash = expected_frontier_digest(declared)

    runnable = tuple(d for d in declared if d.is_runnable)
    held = tuple(d for d in declared if not d.is_runnable)

    # ---- held / denied / NA obligations stay visible and never runnable ----
    held_frontier = tuple(
        MappingProxyType({
            "expected_work_key": d.expected_work_key,
            "documentary_item_key": d.item_key,
            "operation_key": d.operation_key_value,
            "item": d.item,
            "state": d.state,
            "reason": d.hold_reason,
            "runnable": False,
        })
        for d in sorted(held, key=lambda x: x.expected_work_key)
    )

    if not runnable:
        raise BinderCandidateError(
            "no RUNNABLE expected work; held obligations are not executable work"
        )

    # ---- real projection via the accepted binding factory ----
    projection = bind_governed_c11_projection(projection_fields)

    # ---- real I03 request list, one per declared I03 expected operation ----
    requests: dict[tuple[str, str], I03ExecutionRequest] = {}
    for d in runnable:
        if d.op_class != "I03_UNARY_OR_JOINT_QUERY":
            continue
        # The declared condition_order MUST agree with the issued owner's own
        # semantic target order.  Otherwise a caller could relabel q(C|A) as
        # q(C|A,B) without changing the executed query.
        query = runtime_catalog.resolve_query_exact(d.query_ref)
        declared_order = tuple(d.condition_order)
        owner_order = _owner_target_order(query)
        if len(owner_order) > 1 and declared_order != owner_order:
            raise BinderCandidateError(
                "declared condition_order does not equal the exact owner query's "
                "semantic target order "
                f"(expected_work_key={d.expected_work_key}, "
                f"declared={list(declared_order)}, owner={list(owner_order)}); "
                "declare the exact owner target order tokens"
            )
        request = I03ExecutionRequest(
            query_ref=_exact(d.query_ref, "query_ref"),
            predicate_ref=_exact(d.predicate_ref, "predicate_ref"),
        )
        pair = (request.query_ref.key, request.predicate_ref.key)
        prior = requests.get(pair)
        if prior is None:
            requests[pair] = request
        elif prior.request_identity != request.request_identity:
            raise BinderCandidateError(
                "two expected operations collide on one exact I03 request identity"
            )

    # every bound ref must actually resolve in the caller-issued catalog
    for d in runnable:
        if d.op_class == "I03_UNARY_OR_JOINT_QUERY":
            runtime_catalog.resolve_query_exact(d.query_ref)
            runtime_catalog.resolve_predicate_exact(d.predicate_ref)

    discovery_decls = tuple(
        d for d in runnable if d.op_class == "I05_BOUNDED_DISCOVERY"
    )
    if not discovery_decls:
        raise BinderCandidateError("expected work requires exactly one I05 discovery operation")
    discovery_refs = {d.discovery_authority_ref.key for d in discovery_decls}
    if len(discovery_refs) != 1:
        raise BinderCandidateError("exactly one discovery authority must back I05 expected work")
    discovery_authority_ref = _exact(discovery_decls[0].discovery_authority_ref, "discovery_authority_ref")
    runtime_catalog.resolve_discovery_authority_exact(discovery_authority_ref)

    # ---- real batch unit plans, one per declared runnable operation ----
    job_plans: list[JobPlan] = []
    seen_units: dict[str, str] = {}
    for d in sorted(runnable, key=lambda x: x.expected_work_key):
        ewk = d.expected_work_key
        authority_snapshot = _resolve_declared_authority(
            runtime_catalog, d.authority_ref, expected_work_key_value=ewk
        )
        if d.op_class == "I03_UNARY_OR_JOINT_QUERY":
            plan = JobPlan(
                expected_work_key=ewk,
                job_kind="QUERY",
                job_ref=_exact(d.query_ref, "query_ref"),
                predicate_ref=_exact(d.predicate_ref, "predicate_ref"),
                authority_ref=authority_snapshot.ref,
                declared_source_identity=d.source_identity,
                condition_order=declared_order,
            )
        else:
            plan = JobPlan(
                expected_work_key=ewk,
                job_kind="DISCOVERY",
                job_ref=_exact(d.discovery_authority_ref, "discovery_authority_ref"),
                predicate_ref=None,
                authority_ref=authority_snapshot.ref,
                declared_source_identity=d.source_identity,
                condition_order=declared_order,
            )
        collision_key = (
            f"{plan.job_kind}|{plan.job_ref.key}|"
            f"{'' if plan.predicate_ref is None else plan.predicate_ref.key}"
        )
        prior = seen_units.get(collision_key)
        if prior is not None:
            if prior != ewk:
                raise BinderCandidateError(
                    "two distinct expected operations collapsed onto one semantic batch job"
                )
            if d.multiplicity != 1:
                raise BinderCandidateError(
                    "duplicate semantic job requires an explicitly justified multiplicity"
                )
            continue
        seen_units[collision_key] = ewk
        job_plans.append(plan)

    return BoundWorkload(
        projection=projection,
        runtime_catalog=runtime_catalog,
        i03_requests=tuple(requests[pair] for pair in sorted(requests)),
        discovery_authority_ref=discovery_authority_ref,
        job_plans=tuple(job_plans),
        expected_frontier_ref=ExactRef(
            "HQ280_A04_EXPECTED_FRONTIER@1.0.0",
            f"urn:rawlsing:hq280:a04:expected-frontier:sha256:{expected_frontier_hash}",
            expected_frontier_hash,
        ),
        expected_frontier_hash=expected_frontier_hash,
        held_frontier=held_frontier,
        expectation_preimage_hash=expectation_preimage_hash,
        effects=_bind_effects(),
    )


def build_batch_manifest(
    bound: BoundWorkload,
    *,
    release_ref: ExactRef,
) -> BatchManifest:
    """Emit the REAL ``BatchManifest`` for the bound jobs at an exact release.

    ``BatchUnitSpec`` requires at least one exact ``C11LogicalRelease`` ref, so
    the manifest is built once the sealed release is real.  Unit identity is
    still derived only from the bound job plan, never from the outcome.
    """
    if not isinstance(bound, BoundWorkload):
        raise BinderCandidateError("build_batch_manifest requires a BoundWorkload")
    exact_release = _exact(release_ref, "release_ref")
    units = tuple(
        BatchUnitSpec(
            job_kind=plan.job_kind,
            job_ref=plan.job_ref,
            release_refs=(exact_release,),
            semantic_input_refs=(
                (plan.predicate_ref,) if plan.predicate_ref is not None else ()
            ) + (plan.authority_ref,),
        )
        for plan in bound.job_plans
    )
    return BatchManifest(units)


# --------------------------------------------------------------------------
# 4. Real execution through the existing owners
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class ExecutedWorkload:
    bound: BoundWorkload
    production_result: RouteBProductionResult
    batch_manifest: BatchManifest
    batch_receipts: tuple[Any, ...]
    batch_summary: Any


def execute_bound_workload(
    bound: BoundWorkload,
    *,
    source: Any,
) -> ExecutedWorkload:
    """Execute through the REAL Route B compositor and the REAL batch runner."""
    if not isinstance(bound, BoundWorkload):
        raise BinderCandidateError("execute requires a BoundWorkload")

    production = execute_route_b_production(
        source=source,
        projection=bound.projection,
        runtime_catalog=bound.runtime_catalog,
        i03_requests=bound.i03_requests,
        discovery_authority_ref=bound.discovery_authority_ref,
    )

    executor = production.repository_binding.executor
    manifest = build_batch_manifest(
        bound, release_ref=production.c11_release.release_ref
    )
    repository = executor.repository

    def _query_execute(unit: BatchUnitSpec) -> ExecutionOutcome:
        # BatchUnitSpec canonicalizes semantic_input_refs by exact ref key, so
        # the predicate is selected by exact family, never by position.
        predicates = [
            ref for ref in unit.semantic_input_refs
            if ref.kind == "EmpiricalPredicate@1.0.0"
        ]
        if len(predicates) != 1:
            raise BinderCandidateError(
                "batch unit must carry exactly one exact I03 predicate ref"
            )
        outcome = executor.execute_i03(
            query_ref=unit.job_ref,
            predicate_ref=predicates[0],
        )
        return ExecutionOutcome(
            result_refs=tuple(fact.ref for fact in outcome.facts),
            provenance_refs=(unit.job_ref, *unit.semantic_input_refs),
        )

    def _discovery_execute(unit: BatchUnitSpec) -> ExecutionOutcome:
        outcome = executor.execute_i05(discovery_authority_ref=unit.job_ref)
        return ExecutionOutcome(
            result_refs=tuple(receipt.ref for receipt in outcome.receipts),
            provenance_refs=(unit.job_ref, *unit.semantic_input_refs),
        )

    runner = BatchExecutionRunner(manifest=manifest, repository=repository)
    receipts = runner.run(
        executors={
            "QUERY": ExecutorBinding(
                ExactRef(
                    "PRE553_EXECUTOR_BINDING@1.0.0",
                    "urn:rawlsing:hq280:a04:executor:i03",
                    _sha256_of({"executor": "I03", "binder": BINDER_CANDIDATE_CONTRACT_ID}),
                ),
                _query_execute,
            ),
            "DISCOVERY": ExecutorBinding(
                ExactRef(
                    "PRE553_EXECUTOR_BINDING@1.0.0",
                    "urn:rawlsing:hq280:a04:executor:i05",
                    _sha256_of({"executor": "I05", "binder": BINDER_CANDIDATE_CONTRACT_ID}),
                ),
                _discovery_execute,
            ),
        }
    )

    return ExecutedWorkload(
        bound=bound,
        production_result=production,
        batch_manifest=manifest,
        batch_receipts=receipts,
        batch_summary=runner.summary(),
    )


# --------------------------------------------------------------------------
# 5. Outer reconciliation - the no-drop court inside the producer
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class ReconciliationVerdict:
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


def _fail(code: str, detail: Any) -> Mapping[str, Any]:
    return MappingProxyType({"code": code, "detail": detail})


def _classify_result(
    *,
    expected_work_key_value: str,
    declared_measure_kind: str,
    produced_fact: Any | None,
    executed: bool,
    batch_state: str | None,
    expected_multiplicity: int,
    observed_multiplicity: int,
) -> str:
    """Map a REAL owner outcome onto a typed result class.

    Absence of execution is NEVER an admissible null and NEVER success.  The
    mapping is one-way and total over the owners' own state vocabularies; an
    unrecognized owner state is surfaced as ``OWNER_TYPED_<state>`` and never
    promoted to a measured class.
    """
    if not executed:
        return "UNEXECUTED"
    if observed_multiplicity != expected_multiplicity:
        return "MULTIPLICITY_MISMATCH"
    if produced_fact is None:
        return "MISSING_TYPED_RESULT"
    typed_state = str(getattr(produced_fact, "typed_state", "UNKNOWN"))

    # EmpiricalFact (I03) states
    i03_classes = {
        "SUPPORTED": "MEASURED_POSITIVE",
        "OBSERVED_ZERO": "MEASURED_ZERO_IN_SUPPORTED_RISK_SET",
        "VALID_EMPTY": "TOPOLOGY_PRESERVED",
    }
    # DiscoveryResultReceipt (I05) states
    i05_classes = {
        "DISCOVERED_RESULT_SUPPORTED": "MEASURED_POSITIVE",
        "VALID_EMPTY": "TOPOLOGY_PRESERVED",
        "COVERAGE_LIMITED": "COVERAGE_LIMITED",
        "PRUNED_BY_AUTHORITY": "PRUNED_BY_AUTHORITY",
    }
    if typed_state in i03_classes:
        return i03_classes[typed_state]
    if typed_state in i05_classes:
        return i05_classes[typed_state]
    if typed_state in (
        "ZERO_SUPPORT", "NOT_APPLICABLE", "NOT_ELIGIBLE", "ZERO_OVERLAP",
        "INSUFFICIENT_SUPPORT", "NONCOMPARABLE", "INSUFFICIENT_EVIDENCE",
        "UNRESOLVED", "NOT_ASKED", "INAPPLICABLE",
    ):
        return typed_state
    return f"OWNER_TYPED_{typed_state}"


def reconcile(
    *,
    declarations: Iterable[ExpectedWorkDeclaration],
    executed: ExecutedWorkload,
    consumer_receipts: Iterable[Mapping[str, Any]] = (),
) -> ReconciliationVerdict:
    """OUTER-join reconciliation of expectation against constructed work.

    An expected operation with no constructed job stays visible as an
    OMISSION.  A constructed job with no expected operation is an
    UNAUTHORIZED EXTRA.  Equal counts with different keys fail.
    """
    declared = tuple(declarations)
    by_key = {d.expected_work_key: d for d in declared}
    if len(by_key) != len(declared):
        raise BinderCandidateError("duplicate expected_work_key in declarations")

    result = executed.production_result
    bound = executed.bound

    # ---- J: constructed jobs, identified by the REAL batch manifest ----
    plan_by_expectation = {plan.expected_work_key: plan for plan in bound.job_plans}
    receipts_by_unit = {r.unit_ref.key: r for r in executed.batch_receipts}
    plan_by_unit = {}
    for unit in executed.batch_manifest.units:
        for plan in bound.job_plans:
            if (
                unit.job_kind == plan.job_kind
                and unit.job_ref == plan.job_ref
            ):
                plan_by_unit[unit.unit_ref.key] = plan
                break

    produced_by_expectation: dict[str, Any] = {}
    multiplicity_by_expectation: dict[str, int] = {}
    execution_state_by_expectation: dict[str, str | None] = {}

    # map I03 results back through the real request/query identities
    query_to_expectation: dict[str, str] = {}
    for d in declared:
        if d.is_runnable and d.op_class == "I03_UNARY_OR_JOINT_QUERY":
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
         if d.is_runnable and d.op_class == "I05_BOUNDED_DISCOVERY"),
        None,
    )
    if discovery_ewk is not None and result.i05_result.receipts:
        produced_by_expectation[discovery_ewk] = result.i05_result.receipts[0]
        multiplicity_by_expectation[discovery_ewk] = len(result.i05_result.receipts)

    for unit_key, plan in plan_by_unit.items():
        receipt = receipts_by_unit.get(unit_key)
        execution_state_by_expectation[plan.expected_work_key] = (
            None if receipt is None else receipt.state
        )

    expected_keys = tuple(sorted(d.expected_work_key for d in declared if d.is_runnable))
    job_keys = tuple(sorted(plan_by_expectation))
    non_runnable_keys = tuple(
        sorted(d.expected_work_key for d in declared if not d.is_runnable)
    )

    failures: list[Mapping[str, Any]] = []

    # ---- 1. omission (outer join keeps absent mappings visible) ----
    omitted = tuple(sorted(set(expected_keys) - set(job_keys)))
    if omitted:
        failures.append(_fail("EXPECTED_OPERATION_OMITTED", list(omitted)))

    # ---- 2. unauthorized extra ----
    extra = tuple(sorted(set(job_keys) - set(expected_keys)))
    if extra:
        failures.append(_fail("UNAUTHORIZED_EXTRA_JOB", list(extra)))

    # ---- 3. held/denied/NA never executed, always visible ----
    for d in declared:
        if d.is_runnable:
            continue
        if d.expected_work_key in set(job_keys):
            failures.append(
                _fail("HELD_OR_DENIED_WORK_EXECUTED", {"item": d.item, "state": d.state})
            )
        visible = {row["expected_work_key"] for row in bound.held_frontier}
        if d.expected_work_key not in visible:
            failures.append(
                _fail("HELD_OR_DENIED_WORK_NOT_VISIBLE", {"item": d.item, "state": d.state})
            )

    # ---- 4. typed results; no laundering ----
    result_classes: dict[str, str] = {}
    for ewk in expected_keys:
        d = by_key[ewk]
        receipt_state = execution_state_by_expectation.get(ewk)
        observed = multiplicity_by_expectation.get(ewk, 0)
        klass = _classify_result(
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
                    "expected_work_key": ewk,
                    "class": klass,
                })
            )
        if d.measure_kind == "GOVERNED_WEIGHTED":
            fact = produced_by_expectation.get(ewk)
            if fact is not None and getattr(fact, "typed_state", "") == "UNAVAILABLE":
                failures.append(
                    _fail("FALSE_EMPIRICAL_NULL", {
                        "expected_work_key": ewk,
                        "null_source": "AUTHORITY_UNAVAILABLE",
                    })
                )

    # ---- 5. candidate own-_dk / co-topic used as a joint warrant ----
    # Checked on the CONSTRUCTED JOB's own exact owner target refs, not on a
    # caller-supplied label: a shared topic is never a joint warrant.
    for plan in bound.job_plans:
        if plan.job_kind != "QUERY" or len(plan.condition_order) < 2:
            continue
        base = lambda token: token[:-3] if token.endswith("_dk") else token
        first, second = plan.condition_order[0], plan.condition_order[1]
        if base(first) == base(second):
            failures.append(
                _fail("CANDIDATE_OWN_DK_JOINT", {
                    "expected_work_key": plan.expected_work_key,
                    "conditioner": first,
                    "target": second,
                    "basis": "constructed job own exact target order",
                })
            )

    # ---- 6. expectation must not be derived from the produced manifest ----
    rebuilt = expected_frontier_digest(declared)
    if rebuilt != bound.expected_frontier_hash:
        failures.append(
            _fail("EXPECTED_SET_OUTPUT_DERIVED", {
                "bound_frontier": bound.expected_frontier_hash,
                "recomputed": rebuilt,
            })
        )

    # ---- 7. source identity: every CONSTRUCTED job and every declared
    #         expectation must name the exact source the owners ran against ----
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

    # ---- 8. required consumers, distinct from produced results ----
    obligations = tuple(
        MappingProxyType({
            "expected_work_key": d.expected_work_key,
            "consumer": d.required_consumer,
            "item": d.item,
        })
        for d in sorted(declared, key=lambda x: x.expected_work_key)
        if d.is_runnable
    )
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
    return ReconciliationVerdict(
        ok=not failures,
        work_reconciled=not work_failures,
        failures=tuple(failures),
        expected_keys=expected_keys,
        job_keys=job_keys,
        omitted=omitted,
        extra=extra,
        visible_non_runnable=non_runnable_keys,
        result_classes=MappingProxyType(result_classes),
        consumer_obligations=obligations,
        unsatisfied_consumers=unsatisfied,
        frontier_hash=bound.expected_frontier_hash,
        declared_frontier_hash=rebuilt,
    )


def fail_on_reconciliation(verdict: ReconciliationVerdict) -> None:
    """Fail closed with the exact typed failure codes."""
    if not verdict.ok:
        codes = ", ".join(verdict.failure_codes())
        raise BinderReconciliationError(
            f"expected-work reconciliation failed: {codes}"
        )


def canonical_preimage_json(value: Any) -> str:
    return canonical_json(value)


__all__ = [
    "BINDER_CANDIDATE_CONTRACT_ID",
    "EXPECTED_WORK_SCHEMA_VERSION",
    "A05_COMPATIBLE_SCHEMA_VERSION",
    "EXPECTED_STATES",
    "NON_RUNNABLE_STATES",
    "MEASURED_RESULT_CLASSES",
    "ADMISSIBLE_NULL_CLASS",
    "FORBIDDEN_NULL_SOURCES",
    "NEVER_SUCCESS_CLASSES",
    "SUPPORTED_JOB_CLASSES",
    "BinderCandidateError",
    "BinderReconciliationError",
    "documentary_item_key",
    "operation_key",
    "expected_work_key",
    "execution_attempt_key",
    "output_identity",
    "ExpectedWorkDeclaration",
    "expected_frontier_digest",
    "JobPlan",
    "BoundWorkload",
    "bind_expected_work",
    "build_batch_manifest",
    "ExecutedWorkload",
    "execute_bound_workload",
    "ReconciliationVerdict",
    "reconcile",
    "fail_on_reconciliation",
    "canonical_preimage_json",
]