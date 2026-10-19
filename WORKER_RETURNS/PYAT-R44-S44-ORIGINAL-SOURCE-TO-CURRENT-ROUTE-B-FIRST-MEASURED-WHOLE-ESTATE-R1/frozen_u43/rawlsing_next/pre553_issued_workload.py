"""Issuer-custodied request transport into the existing selected Route B owners.

This module has no issuer, grant writer, statistical compiler, or source reader.
Deployment supplies a competent current-decision resolver and an exact source
factory. Both are trusted infrastructure, outside caller/checkpoint custody.
The resolver must authenticate competence and current source/host/purpose rights;
matching a hash alone does not establish those rights.
"""
from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, fields, is_dataclass
import json
from typing import Any, Callable, Protocol

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec, ExecutionOutcome, ExecutorBinding,
)
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor, RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest, execute_route_b_production
from rawlsing_next.pre553_source_backed_c11_facade import (
    GovernedC11Projection, build_source_backed_c11_repository,
)


class WorkloadAdmissionError(ValueError):
    pass


class NativeWorkloadExecutionError(RuntimeError):
    pass


def material(value: Any) -> Any:
    """Complete dataclass preimages, including fields omitted by count receipts."""
    if hasattr(value, "as_dict"):
        return material(value.as_dict())
    if is_dataclass(value):
        return {f.name: material(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, Mapping):
        return {str(k): material(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [material(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((material(v) for v in value), key=lambda x: json.dumps(x, sort_keys=True))
    return value


def canonical(value: Any) -> bytes:
    return json.dumps(material(value), sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def operation_jobs(requests, discoveries):
    return tuple(sorted(
        [("QUERY", r.query_ref.key, r.predicate_ref.key) for r in requests]
        + [("DISCOVERY", d.key, "") for d in discoveries]
    ))


@dataclass(frozen=True)
class IssuedWorkloadRecord:
    """Read result from external competent custody; never created by this worker."""
    decision_ref: ExactRef
    source_permission_ref: ExactRef
    scientific_permission_refs: tuple[ExactRef, ...]
    host: str
    purpose: str
    source_sha256: str
    envelope_sha256: str
    original_u_root: str
    expected_frontier_root: str
    expected_jobs: tuple[tuple[str, str, str], ...]
    currentness: str
    scope: str


class CurrentDecisionResolver(Protocol):
    def resolve_current(self, decision_ref: ExactRef) -> IssuedWorkloadRecord:
        """Authenticate issuer, scope, source/host/purpose and revocation externally."""
        ...


DESCRIPTOR_FIELDS = frozenset({
    "source_edition", "native_item_ids", "release_tag", "routing_and_risk",
    "carrier", "country_and_population", "weight_design_estimand",
    "missing_and_occurrence_policy", "target_conditioner_roles",
})


@dataclass(frozen=True)
class NativeWorkload:
    decision_ref: ExactRef
    source_factory_ref: ExactRef
    descriptor: bytes
    projection: GovernedC11Projection
    catalog: RuntimeObjectCatalog
    requests: tuple[I03ExecutionRequest, ...]
    discoveries: tuple[ExactRef, ...]
    original_u_root: str
    expected_frontier_root: str

    def envelope(self):
        descriptor = json.loads(self.descriptor)
        if set(descriptor) != DESCRIPTOR_FIELDS or canonical(descriptor) != self.descriptor:
            raise WorkloadAdmissionError("CLOSED_CANONICAL_COMPLETE_DESCRIPTOR_REQUIRED")
        if any(v is None or v == "UNBOUND" for v in descriptor.values()):
            raise WorkloadAdmissionError("ISSUED_DESCRIPTOR_HAS_UNBOUND_REQUIRED_FIELD")
        return dict(
            descriptor=descriptor, projection=material(self.projection),
            catalog=material(self.catalog), source_factory_ref=self.source_factory_ref.as_dict(),
            requests=[r.as_dict() for r in self.requests],
            discoveries=[r.as_dict() for r in self.discoveries],
            original_u_root=self.original_u_root, expected_frontier_root=self.expected_frontier_root,
        )


def admit(workload: NativeWorkload, resolver: CurrentDecisionResolver, *, host: str,
          purpose: str, allow_test_only: bool = False) -> IssuedWorkloadRecord:
    """Refuse copied/rehash descriptors and no-drop violations before source open."""
    record = resolver.resolve_current(workload.decision_ref)
    if not isinstance(record, IssuedWorkloadRecord) or record.decision_ref != workload.decision_ref:
        raise WorkloadAdmissionError("CURRENT_AUTHENTICATED_ISSUER_RECORD_REQUIRED")
    scopes = {"ORIGINAL_SOURCE_GRANTED"}
    if allow_test_only:
        scopes.add("TEST_ONLY_SOURCEFREE")
    if record.scope not in scopes or record.currentness != "CURRENT_GRANTED":
        raise WorkloadAdmissionError("CURRENT_COMPETENT_SOURCE_AND_SCIENCE_DECISION_REQUIRED")
    if (record.host, record.purpose) != (host, purpose):
        raise WorkloadAdmissionError("SOURCE_HOST_PURPOSE_MISMATCH")
    if not record.scientific_permission_refs or not isinstance(record.source_permission_ref, ExactRef):
        raise WorkloadAdmissionError("SEPARATE_SOURCE_AND_SCIENTIFIC_PERMISSIONS_REQUIRED")
    if (record.original_u_root, record.expected_frontier_root) != (
        workload.original_u_root, workload.expected_frontier_root
    ):
        raise WorkloadAdmissionError("INDEPENDENT_PROSPECTIVE_U_E_PRE_ROOT_MISMATCH")
    jobs = operation_jobs(workload.requests, workload.discoveries)
    if Counter(jobs) != Counter(record.expected_jobs) or len(jobs) != len(set(jobs)) or not jobs:
        raise WorkloadAdmissionError("EXPECTED_EXECUTED_OPERATION_IDENTITY_MULTISET_MISMATCH")
    if record.source_sha256 != workload.projection.expected_source_sha256:
        raise WorkloadAdmissionError("ISSUED_SOURCE_EDITION_MISMATCH")
    if semantic_hash(workload.envelope()) != record.envelope_sha256:
        raise WorkloadAdmissionError("ENTIRE_EXECUTION_DESCRIPTOR_NOT_THE_ISSUED_ENVELOPE")
    for r in workload.requests:
        q = workload.catalog.resolve_query_exact(r.query_ref)
        workload.catalog.resolve_predicate_exact(r.predicate_ref)
        if material(q.condition_predicate_ref) != r.predicate_ref.as_dict():
            raise WorkloadAdmissionError("QUERY_TARGET_CONDITION_DIRECTION_MISMATCH")
    for ref in workload.discoveries:
        workload.catalog.resolve_discovery_authority_exact(ref)
    return record


@dataclass(frozen=True)
class NativeWorkloadResult:
    route_results: tuple[Any, ...]
    native_outputs: tuple[Any, ...]
    manifest: BatchManifest
    receipts: tuple[Any, ...]
    output_refs: tuple[ExactRef, ...]
    envelope_sha256: str
    decision_ref: ExactRef
    scope: str
    summary: Any


def execute_issued_workload(workload: NativeWorkload, resolver: CurrentDecisionResolver, *,
                            source_factory: Callable[[ExactRef], Any], host: str, purpose: str,
                            allow_test_only: bool = False, prior_receipts=(), max_units=None):
    """Reuse C11, Route B, I03, I05 and Batch; eligibility comes from external U/E_pre.

    A factory is called only after admission. Source bytes stay inside the native
    owner. The return contains native results/receipts, with no authority promotion.
    Exact receipt persistence and preimages remain the existing Batch/C11 custody
    responsibility; prior receipts must resolve in the rebuilt native repository.
    """
    record = admit(workload, resolver, host=host, purpose=purpose, allow_test_only=allow_test_only)
    # The native Batch owner verifies receipt structure, not external issuance.
    # Do not accept caller-rehashed historical receipts through this new ingress.
    # P4's separately authenticated fact/receipt custody is the proven cold path.
    if prior_receipts:
        raise WorkloadAdmissionError("RESTORE_THROUGH_EXISTING_ISSUED_FACT_RECEIPT_CUSTODY_REQUIRED")

    def check_current():
        current = admit(workload, resolver, host=host, purpose=purpose, allow_test_only=allow_test_only)
        if current != record:
            raise WorkloadAdmissionError("ISSUER_SNAPSHOT_CHANGED_DURING_EXECUTION")

    source = source_factory(workload.source_factory_ref)
    if source.source_sha256 != record.source_sha256:
        raise WorkloadAdmissionError("SOURCE_FACTORY_RETURNED_WRONG_EDITION")
    check_current()
    # No invented empty DiscoveryAuthority: query-only scopes use actual C11/I03.
    routes = tuple(execute_route_b_production(
        source=source, projection=workload.projection, runtime_catalog=workload.catalog,
        i03_requests=workload.requests if n == 0 else (), discovery_authority_ref=ref,
    ) for n, ref in enumerate(workload.discoveries)) if max_units is None else ()
    repo, release = build_source_backed_c11_repository(source, workload.projection)
    executor = CarrierNeutralResearchExecutor(repo, (release.release_ref,), workload.catalog)
    units = tuple(BatchUnitSpec("QUERY", r.query_ref, (release.release_ref,),
                               (r.predicate_ref, workload.decision_ref)) for r in workload.requests)
    units += tuple(BatchUnitSpec("DISCOVERY", d, (release.release_ref,),
                                (workload.decision_ref,)) for d in workload.discoveries)
    manifest = BatchManifest(units)
    outputs = {}
    requests_by_query = {r.query_ref.key: r for r in workload.requests}

    def execute(unit):
        check_current()
        if unit.job_kind == "QUERY":
            result = executor.execute_i03(query_ref=unit.job_ref,
                predicate_ref=requests_by_query[unit.job_ref.key].predicate_ref)
            refs = tuple(f.ref for f in result.facts)
        else:
            result = executor.execute_i05(discovery_authority_ref=unit.job_ref)
            refs = tuple(r.ref for r in result.receipts)
        check_current()
        outputs[unit.unit_hash] = result
        return ExecutionOutcome(refs, (release.replay_manifest.ref, workload.decision_ref))

    def executor_ref(kind):
        h = semantic_hash({"module": __name__, "kind": kind, "envelope": record.envelope_sha256})
        return ExactRef("U43_ISSUED_NATIVE_TRANSPORT", "urn:rawlsing:u43:" + h, h)

    runner = BatchExecutionRunner(manifest=manifest, repository=repo, prior_receipts=prior_receipts)
    runner.run(executors={k: ExecutorBinding(executor_ref(k), execute) for k in ("QUERY", "DISCOVERY")},
               max_units=max_units)
    check_current()
    # Every receipt is a native unit receipt. A partial run retains the full manifest.
    if max_units is None and (len(runner.receipts) != len(manifest.units)
                             or any(r.state != "COMPLETED" for r in runner.receipts)):
        raise NativeWorkloadExecutionError("NATIVE_EXECUTION_INCOMPLETE_SEE_RECEIPTS")
    return NativeWorkloadResult(routes, tuple(outputs[k] for k in sorted(outputs)), manifest, runner.receipts,
        tuple(ref for r in runner.receipts for ref in r.result_refs),
        record.envelope_sha256, record.decision_ref, record.scope, runner.summary())
