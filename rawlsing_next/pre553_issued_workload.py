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
    BatchExecutionRunner, BatchManifest, BatchUnitSpec, ExecutionOutcome,
    ExecutorBinding, UnitExecutionReceipt,
)
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor, I03GroupedExecutionScope, RuntimeObjectCatalog,
)
from rawlsing_next.pre553_discovery_exact import COVERAGE_CLAIM, I05_CONTRACT_ID
from rawlsing_next._pre553_query_common import QueryExecutionResult
from types import SimpleNamespace
from rawlsing_next.pre553_empirical_objects import (
    DiscoveryResultReceipt, EmpiricalFact, EmpiricalPredicate,
    EmpiricalQuerySpec, ExactRef, exact_ref, semantic_hash,
)
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
class OriginalWaveIdentity:
    """Canonical roster identity; native aliases require the issuer's own binding."""
    atlas_id: str
    dataset_id: str
    source_family: str
    wave: str

    def __post_init__(self):
        if any(not isinstance(value, str) or not value.strip() for value in (
            self.atlas_id, self.dataset_id, self.source_family, self.wave
        )):
            raise WorkloadAdmissionError("COMPLETE_ORIGINAL_WAVE_IDENTITY_REQUIRED")


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
    original_wave_identity: OriginalWaveIdentity | None = None
    native_universe_refs: tuple[ExactRef, ...] = ()


class CurrentDecisionResolver(Protocol):
    def resolve_current(self, decision_ref: ExactRef) -> IssuedWorkloadRecord:
        """Authenticate issuer, scope, source/host/purpose and revocation externally.

        The read must be repeatable: this module rechecks the same decision at
        the source-read, restore and pre-publication boundaries. A resolver must
        not consume a single-use authorization token on the first read.
        """
        ...


def _require_current_resolver(resolver: Any) -> CurrentDecisionResolver:
    """Refuse an absent or non-independent current-decision resolver."""
    if resolver is None or not callable(getattr(resolver, "resolve_current", None)):
        raise WorkloadAdmissionError("INDEPENDENT_CURRENT_DECISION_RESOLVER_REQUIRED")
    return resolver


@dataclass(frozen=True)
class ExpectedWorkloadBinding:
    original_wave_identity: OriginalWaveIdentity
    decision_ref: ExactRef
    envelope_sha256: str


@dataclass(frozen=True)
class IssuedEstateFrontier:
    """Authenticated scheduling read, composed from separately competent issuers.

    This is a permitted-packet census for the current phase, not an issuer of
    original source rights, administered U, or scientific E_pre. Its custody is
    independent of the submitted workload mapping, just like expected_jobs.
    """
    frontier_ref: ExactRef
    host: str
    purpose: str
    roster_identity: str
    expected_workloads: tuple[ExpectedWorkloadBinding, ...]
    currentness: str
    scope: str


def original35_roster(waves) -> tuple[OriginalWaveIdentity, ...]:
    roster = tuple(sorted((OriginalWaveIdentity(
        w["atlas_id"], w["original_manifest_identity"]["dataset_id"], w["family"], w["wave"]
    ) for w in waves), key=lambda w: w.atlas_id))
    if len(roster) != 35 or len({w.atlas_id for w in roster}) != 35:
        raise WorkloadAdmissionError("INDEPENDENT_ORIGINAL35_ROSTER_REQUIRED")
    return roster


def reconcile_estate_workloads(waves, workloads, frontier: IssuedEstateFrontier):
    """No-drop transport for all independently expected permitted native packets.

    A wave can have multiple country/shard/purpose packets. No source is opened
    and no empirical/scientific candidate is generated during reconciliation.
    """
    roster = original35_roster(waves)
    by_atlas = {w.atlas_id: w for w in roster}
    if semantic_hash(material(roster)) != frontier.roster_identity:
        raise WorkloadAdmissionError("ISSUED_ESTATE_ROSTER_IDENTITY_MISMATCH")
    if not set(workloads) <= set(by_atlas):
        raise WorkloadAdmissionError("UNEXPECTED_WAVE_OUTSIDE_ORIGINAL35")
    expected = []
    for entry in frontier.expected_workloads:
        wave = entry.original_wave_identity
        if by_atlas.get(wave.atlas_id) != wave:
            raise WorkloadAdmissionError("ISSUER_FRONTIER_WAVE_NOT_IN_FROZEN_ROSTER")
        expected.append((wave.atlas_id, entry.decision_ref.key, entry.envelope_sha256))
    if len(expected) != len(set(expected)):
        raise WorkloadAdmissionError("ISSUER_FRONTIER_DUPLICATE_NATIVE_PACKET")
    submitted = []
    prepared = []
    for atlas_id, values in workloads.items():
        packets = (values,) if isinstance(values, NativeWorkload) else tuple(values)
        for packet in packets:
            if not isinstance(packet, NativeWorkload):
                raise WorkloadAdmissionError("EXACT_NATIVE_WORKLOAD_REQUIRED")
            if packet.original_wave_identity != by_atlas[atlas_id]:
                raise WorkloadAdmissionError("ORIGINAL35_ROSTER_TO_NATIVE_PACKET_MISMATCH")
            submitted.append((atlas_id, packet.decision_ref.key, semantic_hash(packet.envelope())))
            prepared.append((by_atlas[atlas_id], packet))
    if Counter(submitted) != Counter(expected):
        raise WorkloadAdmissionError("EXPECTED_NATIVE_PACKET_IDENTITY_MULTISET_MISMATCH")
    return tuple(sorted(prepared, key=lambda pair: (
        pair[0].atlas_id, pair[1].decision_ref.key, semantic_hash(pair[1].envelope())
    )))


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
    original_wave_identity: OriginalWaveIdentity | None = None

    def envelope(self):
        descriptor = json.loads(self.descriptor)
        if set(descriptor) != DESCRIPTOR_FIELDS or canonical(descriptor) != self.descriptor:
            raise WorkloadAdmissionError("CLOSED_CANONICAL_COMPLETE_DESCRIPTOR_REQUIRED")
        if any(v is None or v == "UNBOUND" for v in descriptor.values()):
            raise WorkloadAdmissionError("ISSUED_DESCRIPTOR_HAS_UNBOUND_REQUIRED_FIELD")
        envelope = dict(
            descriptor=descriptor, projection=material(self.projection),
            catalog=material(self.catalog), source_factory_ref=self.source_factory_ref.as_dict(),
            requests=[r.as_dict() for r in self.requests],
            discoveries=[r.as_dict() for r in self.discoveries],
            original_u_root=self.original_u_root, expected_frontier_root=self.expected_frontier_root,
        )
        if self.original_wave_identity is not None:
            envelope["original_wave_identity"] = material(self.original_wave_identity)
        return envelope


def admit(workload: NativeWorkload, resolver: CurrentDecisionResolver, *, host: str,
          purpose: str, allow_test_only: bool = False,
          expected_wave: OriginalWaveIdentity | None = None) -> IssuedWorkloadRecord:
    """Refuse copied/rehash descriptors and no-drop violations before source open.

    ``resolver`` is an independent external reader, never the historical
    ``item.record`` supplied with a checkpoint. Every failure here happens
    before this module can open source or restore a retained result.
    """
    resolver = _require_current_resolver(resolver)
    if not isinstance(host, str) or not host.strip():
        raise WorkloadAdmissionError("NONEMPTY_HOST_REQUIRED")
    if not isinstance(purpose, str) or not purpose.strip():
        raise WorkloadAdmissionError("NONEMPTY_PURPOSE_REQUIRED")
    try:
        record = resolver.resolve_current(workload.decision_ref)
    except WorkloadAdmissionError:
        raise
    except Exception as exc:
        raise WorkloadAdmissionError("CURRENT_DECISION_RESOLVER_REFUSED") from exc
    if not isinstance(record, IssuedWorkloadRecord) or record.decision_ref != workload.decision_ref:
        raise WorkloadAdmissionError("CURRENT_AUTHENTICATED_ISSUER_RECORD_REQUIRED")
    scopes = {"ORIGINAL_SOURCE_GRANTED"}
    if allow_test_only:
        scopes.add("TEST_ONLY_SOURCEFREE")
    if record.scope not in scopes or record.currentness != "CURRENT_GRANTED":
        raise WorkloadAdmissionError("CURRENT_COMPETENT_SOURCE_AND_SCIENCE_DECISION_REQUIRED")
    if (record.host, record.purpose) != (host, purpose):
        raise WorkloadAdmissionError("SOURCE_HOST_PURPOSE_MISMATCH")
    if record.scope == "ORIGINAL_SOURCE_GRANTED" or expected_wave is not None:
        identity = workload.original_wave_identity
        if not isinstance(identity, OriginalWaveIdentity) or record.original_wave_identity != identity:
            raise WorkloadAdmissionError("ISSUED_ORIGINAL_WAVE_BINDING_REQUIRED")
        if expected_wave is not None and identity != expected_wave:
            raise WorkloadAdmissionError("ORIGINAL35_ROSTER_TO_NATIVE_PACKET_MISMATCH")
        if (not isinstance(record.native_universe_refs, tuple)
                or any(not isinstance(ref, ExactRef) for ref in record.native_universe_refs)
                or Counter(record.native_universe_refs) != Counter(
                    u.ref for u in workload.projection.universes
                )):
            raise WorkloadAdmissionError("ISSUED_NATIVE_UNIVERSE_TO_ORIGINAL_WAVE_MISMATCH")
    if (not isinstance(record.scientific_permission_refs, tuple)
            or not record.scientific_permission_refs
            or any(not isinstance(ref, ExactRef) for ref in record.scientific_permission_refs)
            or not isinstance(record.source_permission_ref, ExactRef)):
        raise WorkloadAdmissionError("SEPARATE_SOURCE_AND_SCIENTIFIC_PERMISSIONS_REQUIRED")
    if (record.original_u_root, record.expected_frontier_root) != (
        workload.original_u_root, workload.expected_frontier_root
    ):
        raise WorkloadAdmissionError("INDEPENDENT_PROSPECTIVE_U_E_PRE_ROOT_MISMATCH")
    if (not isinstance(record.expected_jobs, tuple) or any(
        not isinstance(job, tuple) or len(job) != 3
        or not all(isinstance(part, str) for part in job)
        for job in record.expected_jobs
    )):
        raise WorkloadAdmissionError("EXPECTED_EXECUTED_OPERATION_IDENTITY_MULTISET_MISMATCH")
    jobs = operation_jobs(workload.requests, workload.discoveries)
    if Counter(jobs) != Counter(record.expected_jobs) or len(jobs) != len(set(jobs)) or not jobs:
        raise WorkloadAdmissionError("EXPECTED_EXECUTED_OPERATION_IDENTITY_MULTISET_MISMATCH")
    if record.source_sha256 != workload.projection.expected_source_sha256:
        raise WorkloadAdmissionError("ISSUED_SOURCE_EDITION_MISMATCH")
    try:
        envelope_sha256 = semantic_hash(workload.envelope())
    except WorkloadAdmissionError:
        raise
    except (TypeError, ValueError) as exc:
        raise WorkloadAdmissionError("CLOSED_CANONICAL_COMPLETE_DESCRIPTOR_REQUIRED") from exc
    if envelope_sha256 != record.envelope_sha256:
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
    original_wave_identity: OriginalWaveIdentity | None = None
    source_sha256: str | None = None
    outputs_by_unit: Mapping[str, Any] | None = None

    def exact_s2e_output_census(self, *, require_complete: bool = True,
                                runtime_catalog: RuntimeObjectCatalog | None = None):
        """Audit full native I03/I05 and Batch first-reader output preimages.

        This read-only S2-E proof surface is intentionally optional and
        cannot mint native/source/scientific authority or a completed Batch
        claim for an intentionally partial execution. No second evaluator.
        """
        from rawlsing_next.pre553_s2e_exact_conservation import (
            S2EOutputConservationError, census_native_batch,
        )

        # The issued first consumer sees native_outputs/output_refs, not just
        # outputs_by_unit. A complete private map cannot certify a public
        # NativeWorkloadResult whose exposed output view lost its preimages.
        output_map = self.outputs_by_unit or {}
        exposed_native = tuple(output_map[key] for key in sorted(output_map))
        if tuple(self.native_outputs) != exposed_native:
            raise S2EOutputConservationError("S2E_NATIVE_OUTPUT_VIEW_LOSS")
        receipt_refs = tuple(ref for receipt in self.receipts for ref in receipt.result_refs)
        if tuple(self.output_refs) != receipt_refs:
            raise S2EOutputConservationError("S2E_NATIVE_RESULT_REF_VIEW_LOSS")

        return census_native_batch(
            self.manifest, self.receipts, output_map,
            require_complete=require_complete, runtime_catalog=runtime_catalog,
        )


def execute_issued_workload(workload: NativeWorkload, resolver: CurrentDecisionResolver, *,
                            source_factory: Callable[[ExactRef], Any], host: str, purpose: str,
                            allow_test_only: bool = False, prior_receipts=(),
                            prior_outputs=None, max_units=None,
                            expected_wave: OriginalWaveIdentity | None = None,
                            group_scope: I03GroupedExecutionScope | None = None):
    """Reuse C11, Route B, I03, I05 and Batch; eligibility comes from external U/E_pre.

    A factory is called only after admission. Source bytes stay inside the native
    owner. The return contains native results/receipts, with no authority promotion.
    Exact receipt persistence and preimages remain the existing Batch/C11 custody
    responsibility; prior receipts must resolve in the rebuilt native repository.

    The external decision is re-read at every boundary where source can be read,
    restored or served. A revoked/replaced decision cannot open source or
    publish a positive result.
    """
    if max_units is not None and (
        not isinstance(max_units, int) or isinstance(max_units, bool) or max_units < 1
    ):
        raise WorkloadAdmissionError("POSITIVE_MAX_UNITS_REQUIRED")
    record = admit(workload, resolver, host=host, purpose=purpose, allow_test_only=allow_test_only,
                   expected_wave=expected_wave)
    # The native Batch owner verifies receipt structure, not external issuance.
    # Do not accept caller-rehashed historical receipts through this new ingress.
    # P4's separately authenticated fact/receipt custody is the proven cold path.
    prior_receipts = tuple(prior_receipts)
    prior_outputs = dict(prior_outputs or {})

    def check_current():
        current = admit(workload, resolver, host=host, purpose=purpose, allow_test_only=allow_test_only,
                        expected_wave=expected_wave)
        if current != record:
            raise WorkloadAdmissionError("ISSUER_SNAPSHOT_CHANGED_DURING_EXECUTION")

    # Admit and recheck immediately before the source-read boundary. If the
    # decision changes in this window the factory is never called.
    check_current()
    source = source_factory(workload.source_factory_ref)
    if source.source_sha256 != record.source_sha256:
        raise WorkloadAdmissionError("SOURCE_FACTORY_RETURNED_WRONG_EDITION")
    check_current()
    # No invented empty DiscoveryAuthority: query-only scopes use actual C11/I03.
    routes_list = []
    if max_units is None:
        for n, ref in enumerate(workload.discoveries):
            check_current()
            routes_list.append(execute_route_b_production(
                source=source, projection=workload.projection, runtime_catalog=workload.catalog,
                i03_requests=workload.requests if n == 0 else (), discovery_authority_ref=ref,
            ))
            check_current()
    routes = tuple(routes_list)
    check_current()
    repo, release = build_source_backed_c11_repository(
        source, workload.projection, current_authorities=workload.catalog.authorities,
    )
    check_current()
    executor = CarrierNeutralResearchExecutor(repo, (release.release_ref,), workload.catalog)
    owned_group_scope = None
    if group_scope is None and len(workload.requests) + len(workload.discoveries) > 1:
        group_scope = I03GroupedExecutionScope()
        owned_group_scope = group_scope
    units = tuple(BatchUnitSpec("QUERY", r.query_ref, (release.release_ref,),
                               (r.predicate_ref, workload.decision_ref)) for r in workload.requests)
    units += tuple(BatchUnitSpec("DISCOVERY", d, (release.release_ref,),
                                (workload.decision_ref,)) for d in workload.discoveries)
    manifest = BatchManifest(units)
    _validate_prior_cache(manifest, prior_receipts, prior_outputs)
    outputs = dict(prior_outputs)
    requests_by_query = {r.query_ref.key: r for r in workload.requests}

    def execute(unit):
        check_current()
        if unit.job_kind == "QUERY":
            result = executor.execute_i03(query_ref=unit.job_ref,
                predicate_ref=requests_by_query[unit.job_ref.key].predicate_ref,
                group_scope=group_scope)
            refs = tuple(f.ref for f in result.facts)
        else:
            result = executor.execute_i05(discovery_authority_ref=unit.job_ref,
                group_scope=group_scope)
            refs = tuple(r.ref for r in result.receipts)
        check_current()
        outputs[unit.unit_hash] = result
        return ExecutionOutcome(refs, (release.replay_manifest.ref, workload.decision_ref))

    def executor_ref(kind):
        h = semantic_hash({"module": __name__, "kind": kind, "envelope": record.envelope_sha256})
        return ExactRef("U43_ISSUED_NATIVE_TRANSPORT", "urn:rawlsing:u43:" + h, h)

    runner = BatchExecutionRunner(manifest=manifest, repository=repo, prior_receipts=prior_receipts)
    try:
        check_current()
        runner.run(executors={k: ExecutorBinding(executor_ref(k), execute) for k in ("QUERY", "DISCOVERY")},
                   max_units=max_units)
        check_current()
        # Every receipt is a native unit receipt. A partial run retains the full manifest.
        if max_units is None and (len(runner.receipts) != len(manifest.units)
                                 or any(r.state != "COMPLETED" for r in runner.receipts)):
            raise NativeWorkloadExecutionError("NATIVE_EXECUTION_INCOMPLETE_SEE_RECEIPTS")
        result = NativeWorkloadResult(routes, tuple(outputs[k] for k in sorted(outputs)), manifest, runner.receipts,
            tuple(ref for r in runner.receipts for ref in r.result_refs),
            record.envelope_sha256, record.decision_ref, record.scope, runner.summary(),
            record.original_wave_identity, record.source_sha256, dict(outputs))
    finally:
        if owned_group_scope is not None:
            owned_group_scope.close()
    return result


JOINED_CUSTODY_SCHEMA = "PRE553_R04_JOINED_WORKLOAD_CUSTODY@2.0.0"


@dataclass(frozen=True)
class WorkloadCustodyEntry:
    decision_ref: ExactRef
    envelope_sha256: str
    source_sha256: str
    manifest_hash: str
    kind: str
    state: str
    unit_materials: tuple[Mapping[str, Any], ...]
    completed_outputs: Mapping[str, Mapping[str, Any]]
    receipt_materials: tuple[Mapping[str, Any], ...]
    output_refs: tuple[ExactRef, ...]
    entry_hash: str

    def material(self) -> dict[str, Any]:
        return {
            "decision_ref": self.decision_ref.as_dict(),
            "envelope_sha256": self.envelope_sha256,
            "source_sha256": self.source_sha256,
            "manifest_hash": self.manifest_hash,
            "kind": self.kind, "state": self.state,
            "unit_materials": [material(row) for row in self.unit_materials],
            "completed_outputs": {
                key: material(row) for key, row in self.completed_outputs.items()
            },
            "receipt_materials": [material(row) for row in self.receipt_materials],
            "output_refs": [ref.as_dict() for ref in self.output_refs],
            "entry_hash": self.entry_hash,
        }


@dataclass(frozen=True)
class JoinedWorkloadCheckpoint:
    schema: str
    entries: tuple[WorkloadCustodyEntry, ...]
    checkpoint_hash: str

    def material(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "entries": [entry.material() for entry in self.entries],
            "checkpoint_hash": self.checkpoint_hash,
        }

    @property
    def completed_decision_refs(self) -> tuple[ExactRef, ...]:
        return tuple(entry.decision_ref for entry in self.entries)


@dataclass(frozen=True)
class JoinedWorkloadResumeResult:
    checkpoint: JoinedWorkloadCheckpoint
    completed_results: tuple[Any, ...]
    resumed_results: tuple[Any, ...]
    output_refs: tuple[ExactRef, ...]
    receipt_materials: tuple[Mapping[str, Any], ...]

    @property
    def all_results(self) -> tuple[Any, ...]:
        return (*self.completed_results, *self.resumed_results)


def _unit_material(unit: BatchUnitSpec) -> dict[str, Any]:
    return {
        "job_kind": unit.job_kind, "job_ref": unit.job_ref.as_dict(),
        "release_refs": [ref.as_dict() for ref in unit.release_refs],
        "semantic_input_refs": [ref.as_dict() for ref in unit.semantic_input_refs],
    }


def _restore_manifest(rows: Sequence[Mapping[str, Any]]) -> BatchManifest:
    return BatchManifest(tuple(
        BatchUnitSpec(
            row["job_kind"], exact_ref(row["job_ref"]),
            tuple(exact_ref(ref) for ref in row["release_refs"]),
            tuple(exact_ref(ref) for ref in row.get("semantic_input_refs", ())),
        ) for row in rows
    ))


def _restore_receipt(row: Mapping[str, Any]) -> UnitExecutionReceipt:
    return UnitExecutionReceipt(
        manifest_hash=row["manifest_hash"], unit_ref=exact_ref(row["unit_ref"]),
        attempt_index=row["attempt_index"], state=row["state"],
        execution_performed=row["execution_performed"],
        executor_ref=None if row["executor_ref"] is None else exact_ref(row["executor_ref"]),
        result_refs=tuple(exact_ref(ref) for ref in row["result_refs"]),
        provenance_refs=tuple(exact_ref(ref) for ref in row["provenance_refs"]),
        failure_code=row["failure_code"], detail_hash=row["detail_hash"],
    )


def _restore_fact(row: Mapping[str, Any]) -> EmpiricalFact:
    semantic = dict(row["semantic_fields"])
    return EmpiricalFact(
        typed_state=row["typed_state"],
        authority_snapshot_refs=tuple(row["authority_snapshot_refs"]),
        dependency_refs=tuple(row["dependency_refs"]),
        producer_replay_locator_or_reference_root=row["producer_replay_locator_or_reference_root"],
        object_id=row["object_id"], content_hash=row["content_hash"],
        schema_id=row["schema_id"], schema_version=row["schema_version"],
        **semantic,
    )


@dataclass(frozen=True)
class RetainedDiscoveryResultView:
    contract_id: str
    discovery_authority_ref: ExactRef
    candidate_grammar_ref: ExactRef
    evaluated_frontier_ref: ExactRef
    coverage_claim: str
    candidate_count: int
    covered_candidate_count: int
    receipts: tuple[DiscoveryResultReceipt, ...]
    empirical_fact_refs: tuple[ExactRef, ...]
    empirical_facts: tuple[EmpiricalFact, ...]
    executed_predicate_refs: tuple[ExactRef, ...]
    executed_query_refs: tuple[ExactRef, ...]
    valid_empty: bool
    replay_ref: ExactRef

    def __post_init__(self) -> None:
        if tuple(sorted(self.receipts, key=lambda row: row.ref.key)) != self.receipts:
            raise WorkloadAdmissionError("RETAINED_DISCOVERY_RECEIPT_ORDER_INVALID")
        if tuple(sorted(self.empirical_fact_refs, key=lambda ref: ref.key)) != self.empirical_fact_refs:
            raise WorkloadAdmissionError("RETAINED_DISCOVERY_FACT_REF_ORDER_INVALID")
        if tuple(f.ref for f in self.empirical_facts) != self.empirical_fact_refs:
            raise WorkloadAdmissionError("RETAINED_DISCOVERY_FACT_CLOSURE_INVALID")
        if tuple(sorted(self.executed_predicate_refs, key=lambda ref: ref.key)) != self.executed_predicate_refs:
            raise WorkloadAdmissionError("RETAINED_DISCOVERY_PREDICATE_ORDER_INVALID")
        if tuple(sorted(self.executed_query_refs, key=lambda ref: ref.key)) != self.executed_query_refs:
            raise WorkloadAdmissionError("RETAINED_DISCOVERY_QUERY_ORDER_INVALID")


def _restore_discovery_receipt(row: Mapping[str, Any]) -> DiscoveryResultReceipt:
    semantic = dict(row["semantic_fields"])
    return DiscoveryResultReceipt(
        typed_state=row["typed_state"],
        authority_snapshot_refs=tuple(row["authority_snapshot_refs"]),
        dependency_refs=tuple(row["dependency_refs"]),
        producer_replay_locator_or_reference_root=row["producer_replay_locator_or_reference_root"],
        object_id=row["object_id"], content_hash=row["content_hash"],
        schema_id=row["schema_id"], schema_version=row["schema_version"],
        **semantic,
    )


def _restore_output_material(row: Mapping[str, Any]) -> Any:
    if row["kind"] == "QUERY":
        facts = tuple(sorted(
            (_restore_fact(fact) for fact in row["facts"]),
            key=lambda fact: fact.ref.key,
        ))
        return QueryExecutionResult(
            query_ref=exact_ref(row["query_ref"]), facts=facts,
            source_scope_mode=row["source_scope_mode"],
            release_refs=tuple(sorted(
                (exact_ref(ref) for ref in row["release_refs"]),
                key=lambda ref: ref.key,
            )),
        )
    if row["kind"] == "DISCOVERY":
        facts = tuple(sorted(
            (_restore_fact(fact) for fact in row["empirical_facts"]),
            key=lambda fact: fact.ref.key,
        ))
        receipts = tuple(sorted(
            (_restore_discovery_receipt(receipt) for receipt in row["receipts"]),
            key=lambda receipt: receipt.ref.key,
        ))
        return RetainedDiscoveryResultView(
            contract_id=row["contract_id"],
            discovery_authority_ref=exact_ref(row["discovery_authority_ref"]),
            candidate_grammar_ref=exact_ref(row["candidate_grammar_ref"]),
            evaluated_frontier_ref=exact_ref(row["evaluated_frontier_ref"]),
            coverage_claim=row["coverage_claim"],
            candidate_count=row["candidate_count"],
            covered_candidate_count=row["covered_candidate_count"],
            receipts=receipts,
            empirical_fact_refs=tuple(sorted(
                (exact_ref(ref) for ref in row["empirical_fact_refs"]),
                key=lambda ref: ref.key,
            )),
            empirical_facts=facts,
            executed_predicate_refs=tuple(sorted(
                (exact_ref(ref) for ref in row.get("executed_predicate_refs", ())),
                key=lambda ref: ref.key,
            )),
            executed_query_refs=tuple(sorted(
                (exact_ref(ref) for ref in row.get("executed_query_refs", ())),
                key=lambda ref: ref.key,
            )),
            valid_empty=row["valid_empty"],
            replay_ref=exact_ref(row["replay_ref"]),
        )
    raise WorkloadAdmissionError("UNKNOWN_RETAINED_OUTPUT_KIND")


def _discovery_result_material(result: Any) -> dict[str, Any]:
    return {
        "kind": "DISCOVERY",
        "contract_id": result.contract_id,
        "discovery_authority_ref": result.discovery_authority_ref.as_dict(),
        "candidate_grammar_ref": result.candidate_grammar_ref.as_dict(),
        "evaluated_frontier_ref": result.evaluated_frontier_ref.as_dict(),
        "coverage_claim": result.coverage_claim,
        "candidate_count": result.candidate_count,
        "covered_candidate_count": result.covered_candidate_count,
        "receipts": [receipt.as_dict() for receipt in result.receipts],
        "empirical_fact_refs": [ref.as_dict() for ref in result.empirical_fact_refs],
        "empirical_facts": [fact.as_dict() for fact in result.empirical_facts],
        "executed_predicate_refs": [p.ref.as_dict() for p in result.executed_predicates],
        "executed_query_refs": [q.ref.as_dict() for q in result.executed_queries],
        "valid_empty": result.valid_empty,
        "replay_ref": result.replay_ref.as_dict(),
    }


def _result_output_material(result: Any) -> dict[str, Mapping[str, Any]]:
    if getattr(result, "native_result", None) is not None:
        unit_hash = result.manifest.units[0].unit_hash
        return {unit_hash: _discovery_result_material(result.native_result)}
    outputs = getattr(result, "outputs_by_unit", None) or {}
    mapped = {}
    for unit_hash, output in outputs.items():
        if hasattr(output, "query_ref") and hasattr(output, "facts"):
            mapped[unit_hash] = {
                "kind": "QUERY",
                "query_ref": output.query_ref.as_dict(),
                "facts": [fact.as_dict() for fact in output.facts],
                "source_scope_mode": output.source_scope_mode,
                "release_refs": [ref.as_dict() for ref in output.release_refs],
            }
        elif hasattr(output, "receipts") and hasattr(output, "executed_queries"):
            mapped[unit_hash] = _discovery_result_material(output)
        else:
            raise WorkloadAdmissionError("UNKNOWN_NATIVE_OUTPUT_KIND")
    return mapped


def _validate_prior_cache(manifest: BatchManifest, prior_receipts, prior_outputs) -> None:
    """Refuse caller/checkpoint prior outputs that do not match their receipts.

    The native Batch owner verifies receipt structure. This closes the cache
    content boundary: a completed prior unit may be skipped only when the
    supplied native output has exactly the receipt's result refs. A different
    value cannot be injected under a valid receipt.
    """
    unit_by_hash = {unit.unit_hash: unit for unit in manifest.units}
    unit_by_ref = {unit.unit_ref.key: unit for unit in manifest.units}
    if not set(prior_outputs) <= set(unit_by_hash):
        raise WorkloadAdmissionError("PRIOR_OUTPUT_UNKNOWN_UNIT")
    completed_by_unit = {}
    for receipt in prior_receipts:
        unit = unit_by_ref.get(receipt.unit_ref.key)
        if unit is not None and receipt.state == "COMPLETED":
            completed_by_unit[unit.unit_hash] = receipt
    if any(
        unit_hash not in completed_by_unit for unit_hash in prior_outputs
    ):
        raise WorkloadAdmissionError("PRIOR_OUTPUT_WITHOUT_COMPLETED_RECEIPT")
    for receipt in prior_receipts:
        unit = unit_by_ref.get(receipt.unit_ref.key)
        if unit is None:
            raise WorkloadAdmissionError("PRIOR_RECEIPT_UNKNOWN_UNIT")
        if receipt.manifest_hash != manifest.manifest_hash:
            raise WorkloadAdmissionError("PRIOR_RECEIPT_MANIFEST_MISMATCH")
        if receipt.state != "COMPLETED":
            continue
        output = prior_outputs.get(unit.unit_hash)
        if output is None:
            raise WorkloadAdmissionError("PRIOR_OUTPUT_MISSING")
        if unit.job_kind == "QUERY":
            facts = getattr(output, "facts", None)
            if facts is None:
                raise WorkloadAdmissionError("PRIOR_OUTPUT_KIND_MISMATCH")
            expected = tuple(fact.ref for fact in facts)
        elif unit.job_kind == "DISCOVERY":
            receipts = getattr(output, "receipts", None)
            if receipts is None:
                raise WorkloadAdmissionError("PRIOR_OUTPUT_KIND_MISMATCH")
            expected = tuple(item.ref for item in receipts)
        else:
            raise WorkloadAdmissionError("PRIOR_OUTPUT_KIND_MISMATCH")
        if Counter(expected) != Counter(receipt.result_refs):
            raise WorkloadAdmissionError("PRIOR_OUTPUT_RECEIPT_MISMATCH")


def _entry_payload(entry: WorkloadCustodyEntry) -> dict[str, Any]:
    """Exact content-addressed entry preimage (excludes the entry hash itself)."""
    return {
        "decision_ref": entry.decision_ref.as_dict(),
        "envelope_sha256": entry.envelope_sha256,
        "source_sha256": entry.source_sha256,
        "manifest_hash": entry.manifest_hash,
        "kind": entry.kind, "state": entry.state,
        "unit_materials": [material(row) for row in entry.unit_materials],
        "completed_outputs": {
            key: material(row) for key, row in entry.completed_outputs.items()
        },
        "receipt_materials": [material(row) for row in entry.receipt_materials],
        "output_refs": [ref.as_dict() for ref in entry.output_refs],
    }


def _checkpoint_content_hash(checkpoint: JoinedWorkloadCheckpoint) -> str:
    """Content address of the complete checkpoint, independent of the claimed pin."""
    return semantic_hash({
        "schema": checkpoint.schema,
        "entries": [entry.material() for entry in checkpoint.entries],
    })


def _validate_entry_material(entry: WorkloadCustodyEntry) -> None:
    """Refuse a corrupt, orphaned or internally inconsistent checkpoint entry.

    This is a material/structure check only. It deliberately does not
    reconstruct native empirical outputs; ``_validate_entry_outputs`` performs
    that parse only after the caller has established current authority. It
    never treats a stored permission field as current authority.
    """
    if not isinstance(entry, WorkloadCustodyEntry):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_REQUIRED")
    if entry.kind not in {"WORKLOAD", "DISCOVERY"}:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_KIND_INVALID")
    if entry.state not in {"COMPLETED", "PARTIAL"}:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_STATE_INVALID")
    if entry.kind == "DISCOVERY" and entry.state != "COMPLETED":
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_DISCOVERY_STATE_INVALID")
    for value in (entry.envelope_sha256, entry.source_sha256, entry.manifest_hash):
        if (not isinstance(value, str) or len(value) != 64
                or any(char not in "0123456789abcdef" for char in value.lower())):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_HASH_INVALID")
    try:
        if entry.entry_hash != semantic_hash(_entry_payload(entry)):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_HASH_MISMATCH")
        manifest = _restore_manifest(entry.unit_materials)
        receipts = tuple(_restore_receipt(row) for row in entry.receipt_materials)
        if manifest.manifest_hash != entry.manifest_hash:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_MANIFEST_MISMATCH")
        if entry.kind == "DISCOVERY" and any(
            unit.job_kind != "DISCOVERY" for unit in manifest.units
        ):
            raise WorkloadAdmissionError(
                "JOINED_CHECKPOINT_DISCOVERY_MANIFEST_MISMATCH"
            )
        if any(receipt.manifest_hash != manifest.manifest_hash for receipt in receipts):
            raise WorkloadAdmissionError(
                "JOINED_CHECKPOINT_RECEIPT_MANIFEST_MISMATCH"
            )
        unit_keys = {unit.unit_ref.key for unit in manifest.units}
        receipt_keys = [receipt.unit_ref.key for receipt in receipts]
        if len(receipt_keys) != len(set(receipt_keys)) or not set(receipt_keys) <= unit_keys:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_RECEIPT_UNIT_MISMATCH")
        completed_keys = {
            receipt.unit_ref.key for receipt in receipts
            if receipt.state == "COMPLETED"
        }
        expected_outputs = {
            unit.unit_hash for unit in manifest.units
            if unit.unit_ref.key in completed_keys
        }
        if set(entry.completed_outputs) != expected_outputs:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_OUTPUT_CLOSURE_MISMATCH")
        if entry.state == "COMPLETED" and (
            set(receipt_keys) != unit_keys or completed_keys != unit_keys
        ):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_COMPLETED_PREFIX_INCOMPLETE")
        if entry.state == "PARTIAL" and not completed_keys:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_EMPTY_PREFIX")
        expected_refs = tuple(sorted(
            (ref for receipt in receipts for ref in receipt.result_refs),
            key=lambda ref: ref.key,
        ))
        if entry.output_refs != expected_refs:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_OUTPUT_REF_MISMATCH")
    except WorkloadAdmissionError:
        raise
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_MATERIAL_INVALID") from exc


def _canonical_refs(values) -> tuple[ExactRef, ...]:
    refs = [
        value if isinstance(value, ExactRef) else exact_ref(value)
        for value in values
    ]
    return tuple(sorted(refs, key=lambda ref: ref.key))


def _discovery_frontier_replay(output: Any) -> ExactRef:
    """Recompute the I05 frontier replay ref from the retained view fields.

    This mirrors the existing I05 derivation; it is a consistency check, not a
    new receipt issuer or authority root.
    """
    digest = semantic_hash({
        "contract": output.contract_id,
        "frontier_ref": output.evaluated_frontier_ref.as_dict(),
        "receipt_refs": [receipt.ref.as_dict() for receipt in output.receipts],
        "fact_refs": [ref.as_dict() for ref in output.empirical_fact_refs],
        "valid_empty": output.valid_empty,
    })
    return ExactRef(
        "PRE553_I05_FRONTIER_REPLAY",
        "urn:rawlsing:pre553:i05:frontier-replay:sha256:" + digest,
        digest,
    )


def _validate_entry_outputs(
    entry: WorkloadCustodyEntry, *, workload: NativeWorkload | None = None,
) -> None:
    """Reconstruct retained native outputs and bind them to their native units.

    This is the protected-payload parse. Callers invoke it only after current
    authority has been established, so a revoked/replaced decision cannot
    cause a retained empirical output to be reconstructed or served. It binds
    the whole retained output identity, not only the fact/receipt refs:
    query_ref, release refs, source-scope mode, fact query/predicate refs,
    discovery authority/frontier/grammar/release/executed-ref closure and the
    I05 frontier replay ref. A different native value or a different per-unit
    identity cannot ride under a valid unit receipt.
    """
    if not isinstance(entry, WorkloadCustodyEntry):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_REQUIRED")
    try:
        manifest = _restore_manifest(entry.unit_materials)
        receipts = tuple(_restore_receipt(row) for row in entry.receipt_materials)
        if workload is not None:
            expected_queries = {
                request.query_ref.key: request for request in workload.requests
            }
            expected_discoveries = {ref.key for ref in workload.discoveries}
            for unit in manifest.units:
                input_keys = {ref.key for ref in unit.semantic_input_refs}
                if workload.decision_ref.key not in input_keys:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DECISION_MISMATCH"
                    )
                if unit.job_kind == "QUERY":
                    request = expected_queries.get(unit.job_ref.key)
                    if request is None:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_UNIT_MISMATCH"
                        )
                    if request.predicate_ref.key not in input_keys:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_PREDICATE_MISMATCH"
                        )
                elif unit.job_kind == "DISCOVERY":
                    if unit.job_ref.key not in expected_discoveries:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_UNIT_MISMATCH"
                        )
                else:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_KIND_MISMATCH"
                    )
            if entry.state == "COMPLETED" and len(manifest.units) != (
                len(expected_queries) + len(expected_discoveries)
            ):
                raise WorkloadAdmissionError(
                    "JOINED_CHECKPOINT_OUTPUT_UNIT_CLOSURE_MISMATCH"
                )
        unit_by_hash = {unit.unit_hash: unit for unit in manifest.units}
        receipt_by_unit = {receipt.unit_ref.key: receipt for receipt in receipts}
        for unit_hash, row in entry.completed_outputs.items():
            unit = unit_by_hash.get(unit_hash)
            if unit is None:
                raise WorkloadAdmissionError("JOINED_CHECKPOINT_OUTPUT_UNIT_MISMATCH")
            receipt = receipt_by_unit.get(unit.unit_ref.key)
            if receipt is None or receipt.state != "COMPLETED":
                raise WorkloadAdmissionError(
                    "JOINED_CHECKPOINT_OUTPUT_RECEIPT_MISMATCH"
                )
            output = _restore_output_material(row)
            if unit.job_kind == "QUERY":
                if row.get("kind") != "QUERY" or not hasattr(output, "facts"):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_KIND_MISMATCH"
                    )
                if output.query_ref != unit.job_ref:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_QUERY_MISMATCH"
                    )
                if _canonical_refs(output.release_refs) != _canonical_refs(unit.release_refs):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_RELEASE_MISMATCH"
                    )
                if workload is not None:
                    query = workload.catalog.resolve_query_exact(unit.job_ref)
                    grain = query.requested_output_grain
                    expected_mode = (
                        grain.get("source_scope_mode")
                        if isinstance(grain, Mapping) else None
                    )
                    if (expected_mode is not None
                            and output.source_scope_mode != expected_mode):
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_SCOPE_MODE_MISMATCH"
                        )
                request = (
                    expected_queries.get(unit.job_ref.key)
                    if workload is not None else None
                )
                unit_input_keys = {
                    ref.key for ref in unit.semantic_input_refs
                }
                for fact in output.facts:
                    if exact_ref(
                        fact.empirical_query_spec_ref, "empirical_query_spec_ref"
                    ) != unit.job_ref:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_QUERY_MISMATCH"
                        )
                    fact_predicate = exact_ref(
                        fact.condition_predicate_ref, "condition_predicate_ref"
                    )
                    if request is not None:
                        if fact_predicate != request.predicate_ref:
                            raise WorkloadAdmissionError(
                                "JOINED_CHECKPOINT_OUTPUT_PREDICATE_MISMATCH"
                            )
                    elif fact_predicate.key not in unit_input_keys:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_PREDICATE_MISMATCH"
                        )
                refs = tuple(fact.ref for fact in output.facts)
            elif unit.job_kind == "DISCOVERY":
                if row.get("kind") != "DISCOVERY" or not hasattr(output, "receipts"):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_KIND_MISMATCH"
                    )
                if output.discovery_authority_ref != unit.job_ref:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_AUTHORITY_MISMATCH"
                    )
                if (output.contract_id != I05_CONTRACT_ID
                        or output.coverage_claim != COVERAGE_CLAIM):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_CONTRACT_MISMATCH"
                    )
                if (output.candidate_count != output.covered_candidate_count
                        or output.candidate_count != len(output.receipts)):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_COUNT_MISMATCH"
                    )
                if output.valid_empty != (
                    not output.receipts
                    or all(item.typed_state == "VALID_EMPTY"
                           for item in output.receipts)
                ):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_EMPTY_MISMATCH"
                    )
                if output.replay_ref != _discovery_frontier_replay(output):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_REPLAY_MISMATCH"
                    )
                if workload is not None:
                    authority = workload.catalog.resolve_discovery_authority_exact(
                        unit.job_ref
                    )
                    if output.candidate_grammar_ref != exact_ref(
                        authority.candidate_grammar_ref
                    ):
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_GRAMMAR_MISMATCH"
                        )
                fact_union = set()
                query_union = set()
                predicate_union = set()
                for item in output.receipts:
                    if exact_ref(
                        item.discovery_authority_ref, "discovery_authority_ref"
                    ) != unit.job_ref:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_AUTHORITY_MISMATCH"
                        )
                    if exact_ref(
                        item.evaluated_frontier_ref, "evaluated_frontier_ref"
                    ) != output.evaluated_frontier_ref:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_FRONTIER_MISMATCH"
                        )
                    if output.candidate_grammar_ref.key not in {
                        exact_ref(ref).key for ref in item.dependency_refs
                    }:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_GRAMMAR_MISMATCH"
                        )
                    if _canonical_refs(item.source_release_refs) != _canonical_refs(
                        unit.release_refs
                    ):
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_RELEASE_MISMATCH"
                        )
                    fact_union.update(
                        exact_ref(ref).key for ref in item.empirical_fact_refs
                    )
                    for role in item.candidate_identity.get("query_roles", ()):
                        query_union.add(exact_ref(role["query_ref"], "query_ref").key)
                        predicate_union.add(
                            exact_ref(role["predicate_ref"], "predicate_ref").key
                        )
                if fact_union != {ref.key for ref in output.empirical_fact_refs}:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_FACT_MISMATCH"
                    )
                if query_union != {ref.key for ref in output.executed_query_refs}:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_QUERY_MISMATCH"
                    )
                if predicate_union != {
                    ref.key for ref in output.executed_predicate_refs
                }:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_PREDICATE_MISMATCH"
                    )
                refs = tuple(item.ref for item in output.receipts)
            else:
                raise WorkloadAdmissionError(
                    "JOINED_CHECKPOINT_OUTPUT_KIND_MISMATCH"
                )
            if Counter(refs) != Counter(receipt.result_refs):
                raise WorkloadAdmissionError(
                    "JOINED_CHECKPOINT_OUTPUT_RECEIPT_MISMATCH"
                )
    except WorkloadAdmissionError:
        raise
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_MATERIAL_INVALID") from exc


def capture_joined_checkpoint(
    results: Sequence[Any], *,
    source_sha256_by_decision: Mapping[str, str] | None = None,
) -> JoinedWorkloadCheckpoint:
    """Capture completed or real partial prefix with native output facts retained."""
    entries = []
    for result in results:
        is_discovery = getattr(result, "native_result", None) is not None
        manifest = getattr(result, "manifest", None)
        receipts = tuple(getattr(result, "receipts", ()))
        if manifest is None or not receipts:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_NATIVE_RESULT_REQUIRED")
        by_unit = {}
        for receipt in receipts:
            if receipt.unit_ref.key in by_unit:
                raise WorkloadAdmissionError("JOINED_CHECKPOINT_DUPLICATE_UNIT")
            by_unit[receipt.unit_ref.key] = receipt
        completed = {unit.unit_ref.key: by_unit.get(unit.unit_ref.key)
                     for unit in manifest.units}
        if is_discovery:
            state = "COMPLETED"
        else:
            if not completed or not any(receipt is not None for receipt in completed.values()):
                raise WorkloadAdmissionError("JOINED_CHECKPOINT_EMPTY_PREFIX")
            state = ("COMPLETED" if all(
                receipt is not None and receipt.state == "COMPLETED"
                for receipt in completed.values()) else "PARTIAL")
        output_refs = tuple(sorted(
            (ref for receipt in receipts for ref in receipt.result_refs),
            key=lambda ref: ref.key,
        ))
        entry_payload = {
            "decision_ref": result.decision_ref.as_dict(),
            "envelope_sha256": result.envelope_sha256,
            "source_sha256": (
                getattr(result, "source_sha256", None)
                or (source_sha256_by_decision or {}).get(result.decision_ref.key, "")
            ),
            "manifest_hash": manifest.manifest_hash,
            "kind": "DISCOVERY" if is_discovery else "WORKLOAD",
            "state": state,
            "unit_materials": [_unit_material(unit) for unit in manifest.units],
            "completed_outputs": _result_output_material(result),
            "receipt_materials": [material(receipt) for receipt in receipts],
            "output_refs": [ref.as_dict() for ref in output_refs],
        }
        entry = WorkloadCustodyEntry(
            decision_ref=result.decision_ref,
            envelope_sha256=result.envelope_sha256,
            source_sha256=(
                getattr(result, "source_sha256", None)
                or (source_sha256_by_decision or {}).get(result.decision_ref.key, "")
            ),
            manifest_hash=manifest.manifest_hash,
            kind=entry_payload["kind"], state=state,
            unit_materials=tuple(entry_payload["unit_materials"]),
            completed_outputs=entry_payload["completed_outputs"],
            receipt_materials=tuple(entry_payload["receipt_materials"]),
            output_refs=output_refs,
            entry_hash=semantic_hash(entry_payload),
        )
        _validate_entry_material(entry)
        _validate_entry_outputs(entry)
        entries.append(entry)
    ordered = tuple(sorted(entries, key=lambda entry: entry.decision_ref.key))
    if len({entry.decision_ref.key for entry in ordered}) != len(ordered):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_DUPLICATE_DECISION")
    payload = {"schema": JOINED_CUSTODY_SCHEMA,
               "entries": [entry.material() for entry in ordered]}
    return JoinedWorkloadCheckpoint(
        schema=JOINED_CUSTODY_SCHEMA, entries=ordered,
        checkpoint_hash=semantic_hash(payload),
    )


def restore_joined_checkpoint(
    material_payload: Mapping[str, Any], *, expected_checkpoint_ref: str | None = None,
    current_guard: Callable[[tuple[ExactRef, ...]], None] | None = None,
) -> JoinedWorkloadCheckpoint:
    """Rehydrate a joined checkpoint and require the original external pin.

    This helper restores custody material, not native empirical outputs when
    no current guard is supplied: ``_validate_entry_material`` validates
    hashes/manifest/receipt structure but deliberately does not call
    ``_restore_output_material``. The protected payload parse then happens in
    ``resume_joined_workloads`` only after it has admitted the current decision.
    ``current_guard`` remains an optional early-refusal hook for callers that
    own an independent resolver; it runs after the pin/hash checks and before
    any entry material is parsed. When it is supplied and succeeds, the helper
    also performs the full output/receipt binding check. It is not a permission
    cache, and omitting it cannot cause a protected output restore because this
    function does not perform one without it.
    """
    if not isinstance(expected_checkpoint_ref, str) or not expected_checkpoint_ref:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_EXPECTED_PIN_REQUIRED")
    if not isinstance(material_payload, Mapping):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_MATERIAL_REQUIRED")
    payload = dict(material_payload)
    if payload.get("schema") != JOINED_CUSTODY_SCHEMA:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_SCHEMA_MISMATCH")
    claimed = payload.get("checkpoint_hash")
    entries_material = payload.get("entries", ())
    if not isinstance(entries_material, (list, tuple)):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRIES_INVALID")
    if any(not isinstance(row, Mapping) for row in entries_material):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRIES_INVALID")
    computed_payload = {
        "schema": payload.get("schema"),
        "entries": [dict(row) for row in entries_material],
    }
    if claimed != semantic_hash(computed_payload):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_HASH_MISMATCH")
    if claimed != expected_checkpoint_ref:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_PIN_MISMATCH")
    if current_guard is not None:
        if not callable(current_guard):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_CURRENT_GUARD_INVALID")
        try:
            decision_refs = tuple(
                exact_ref(row["decision_ref"]) for row in entries_material
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_MATERIAL_INVALID") from exc
        try:
            current_guard(decision_refs)
        except WorkloadAdmissionError:
            raise
        except Exception as exc:
            raise WorkloadAdmissionError(
                "JOINED_CHECKPOINT_CURRENT_GUARD_REFUSED"
            ) from exc
    entries = []
    try:
        for row in entries_material:
            entry_payload = {
                "decision_ref": row["decision_ref"],
                "envelope_sha256": row["envelope_sha256"],
                "source_sha256": row["source_sha256"],
                "manifest_hash": row["manifest_hash"],
                "kind": row["kind"], "state": row["state"],
                "unit_materials": row["unit_materials"],
                "completed_outputs": row["completed_outputs"],
                "receipt_materials": row["receipt_materials"],
                "output_refs": row["output_refs"],
            }
            if row.get("entry_hash") != semantic_hash(entry_payload):
                raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_HASH_MISMATCH")
            restored_units = _restore_manifest(row["unit_materials"])
            if restored_units.manifest_hash != row["manifest_hash"]:
                raise WorkloadAdmissionError("JOINED_CHECKPOINT_MANIFEST_MISMATCH")
            entry = WorkloadCustodyEntry(
                decision_ref=exact_ref(row["decision_ref"]),
                envelope_sha256=row["envelope_sha256"],
                source_sha256=row["source_sha256"],
                manifest_hash=row["manifest_hash"],
                kind=row["kind"], state=row["state"],
                unit_materials=tuple(dict(item) for item in row["unit_materials"]),
                completed_outputs={
                    key: dict(item) for key, item in row["completed_outputs"].items()
                },
                receipt_materials=tuple(dict(item) for item in row["receipt_materials"]),
                output_refs=tuple(exact_ref(ref) for ref in row["output_refs"]),
                entry_hash=row["entry_hash"],
            )
            _validate_entry_material(entry)
            if current_guard is not None:
                # The guard has already established current authority above;
                # only now may a guarded cold restore parse protected output.
                _validate_entry_outputs(entry)
            entries.append(entry)
    except WorkloadAdmissionError:
        raise
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_MATERIAL_INVALID") from exc
    return JoinedWorkloadCheckpoint(
        schema=payload["schema"], entries=tuple(entries),
        checkpoint_hash=claimed,
    )


def _completed_entry_view(entry: WorkloadCustodyEntry, scope: str) -> Any:
    manifest = _restore_manifest(entry.unit_materials)
    receipts = tuple(_restore_receipt(row) for row in entry.receipt_materials)
    outputs = {
        unit_hash: _restore_output_material(row)
        for unit_hash, row in entry.completed_outputs.items()
    }
    if entry.kind == "DISCOVERY":
        if len(outputs) != 1:
            raise WorkloadAdmissionError("RETAINED_DISCOVERY_OUTPUT_COUNT_INVALID")
        native_result = next(iter(outputs.values()))
        return SimpleNamespace(
            native_result=native_result, manifest=manifest, receipts=receipts,
            envelope_sha256=entry.envelope_sha256,
            decision_ref=entry.decision_ref, scope=scope,
            source_sha256=entry.source_sha256,
        )
    return NativeWorkloadResult(
        route_results=(), native_outputs=tuple(outputs[key] for key in sorted(outputs)),
        manifest=manifest, receipts=receipts, output_refs=entry.output_refs,
        envelope_sha256=entry.envelope_sha256, decision_ref=entry.decision_ref,
        scope=scope, summary=None, source_sha256=entry.source_sha256,
        outputs_by_unit=outputs,
    )


def resume_joined_workloads(
    *,
    workloads: Sequence[Any],
    resolver: CurrentDecisionResolver,
    source_factory: Callable[[ExactRef], Any],
    host: str,
    purpose: str,
    checkpoint: JoinedWorkloadCheckpoint,
    expected_checkpoint_ref: str | None = None,
    allow_test_only: bool = False,
) -> JoinedWorkloadResumeResult:
    """Resume actual R03-issued workloads under one independent current issuer.

    The resolver is required for every fate. No historical ``item.record``,
    checkpoint field or retained permission is used as current authority. The
    first admission happens before entry branching, protected result
    restoration, ``source_factory`` or native execution. Completed results are
    rechecked twice: before restore and immediately before serve.
    """
    resolver = _require_current_resolver(resolver)
    if not isinstance(checkpoint, JoinedWorkloadCheckpoint):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_REQUIRED")
    if checkpoint.schema != JOINED_CUSTODY_SCHEMA:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_SCHEMA_MISMATCH")
    if not isinstance(checkpoint.entries, tuple) or any(
        not isinstance(entry, WorkloadCustodyEntry) for entry in checkpoint.entries
    ):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_REQUIRED")
    # Recompute the content address from the entries before trusting the
    # claimed hash or the caller-supplied pin. A mutated in-memory checkpoint
    # that retained its old hash is refused before any resolver/source read.
    try:
        computed_checkpoint_hash = _checkpoint_content_hash(checkpoint)
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_MATERIAL_INVALID") from exc
    if computed_checkpoint_hash != checkpoint.checkpoint_hash:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_HASH_MISMATCH")
    if expected_checkpoint_ref is None or checkpoint.checkpoint_hash != expected_checkpoint_ref:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_PIN_MISMATCH")
    items = tuple(workloads)
    by_decision: dict[str, Any] = {}
    for item in items:
        workload = getattr(item, "workload", None)
        historical = getattr(item, "record", None)
        if not isinstance(workload, NativeWorkload):
            raise WorkloadAdmissionError("EXACT_NATIVE_WORKLOAD_REQUIRED")
        if not isinstance(historical, IssuedWorkloadRecord):
            raise WorkloadAdmissionError("HISTORICAL_ISSUED_RECORD_REQUIRED")
        if historical.decision_ref != workload.decision_ref:
            raise WorkloadAdmissionError("JOINED_WORKLOAD_RECORD_DECISION_MISMATCH")
        if historical.envelope_sha256 != semantic_hash(workload.envelope()):
            raise WorkloadAdmissionError("JOINED_WORKLOAD_HISTORICAL_ENVELOPE_MISMATCH")
        if historical.source_sha256 != workload.projection.expected_source_sha256:
            raise WorkloadAdmissionError("JOINED_WORKLOAD_HISTORICAL_SOURCE_MISMATCH")
        key = workload.decision_ref.key
        if key in by_decision:
            raise WorkloadAdmissionError("JOINED_WORKLOAD_DUPLICATE_DECISION")
        by_decision[key] = item
    completed_entries = {entry.decision_ref.key: entry for entry in checkpoint.entries}
    if len(completed_entries) != len(checkpoint.entries):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_DUPLICATE_DECISION")
    if not set(completed_entries) <= set(by_decision):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_UNKNOWN_WORKLOAD")
    # Metadata-only shape check before the first external read. Full native
    # material validation happens after current admission, so a revoked
    # decision cannot cause a protected payload restore.
    for entry in checkpoint.entries:
        if not isinstance(entry, WorkloadCustodyEntry):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_REQUIRED")
        if entry.kind not in {"WORKLOAD", "DISCOVERY"}:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_KIND_INVALID")
        if entry.state not in {"COMPLETED", "PARTIAL"}:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_STATE_INVALID")

    def current_for(item: Any) -> IssuedWorkloadRecord:
        return admit(
            item.workload, resolver, host=host, purpose=purpose,
            allow_test_only=allow_test_only,
            expected_wave=item.workload.original_wave_identity,
        )

    def require_unchanged(item: Any, expected: IssuedWorkloadRecord, code: str) -> None:
        if current_for(item) != expected:
            raise WorkloadAdmissionError(code)

    completed_results: list[Any] = []
    resumed_results: list[Any] = []
    current_by_key: dict[str, IssuedWorkloadRecord] = {}
    for item in items:
        workload = item.workload
        # Required for every fate, including COMPLETED and ABSENT, before any
        # checkpoint material is restored or a source factory can be called.
        current_record = current_for(item)
        key = workload.decision_ref.key
        current_by_key[key] = current_record
        entry = completed_entries.get(key)
        if entry is None:
            resumed_results.append(execute_issued_workload(
                workload, resolver, source_factory=source_factory,
                host=host, purpose=purpose, allow_test_only=allow_test_only,
                expected_wave=workload.original_wave_identity,
            ))
            continue
        if (entry.envelope_sha256 != current_record.envelope_sha256
                or entry.source_sha256 != current_record.source_sha256
                or entry.decision_ref != current_record.decision_ref):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_WORKLOAD_IDENTITY_MISMATCH")
        if entry.state == "COMPLETED":
            require_unchanged(
                item, current_record, "ISSUER_SNAPSHOT_CHANGED_BEFORE_RESTORE"
            )
            # Current authority is established immediately above. Only now may
            # the checkpoint's native material be parsed and validated.
            _validate_entry_material(entry)
            _validate_entry_outputs(entry, workload=workload)
            view = _completed_entry_view(entry, current_record.scope)
            require_unchanged(
                item, current_record, "ISSUER_SNAPSHOT_CHANGED_BEFORE_SERVE"
            )
            completed_results.append(view)
            continue
        if entry.state != "PARTIAL":
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_STATE_INVALID")
        require_unchanged(
            item, current_record, "ISSUER_SNAPSHOT_CHANGED_BEFORE_RESTORE"
        )
        _validate_entry_material(entry)
        _validate_entry_outputs(entry, workload=workload)
        prior_receipts = tuple(_restore_receipt(row) for row in entry.receipt_materials)
        prior_outputs = {
            unit_hash: _restore_output_material(row)
            for unit_hash, row in entry.completed_outputs.items()
        }
        resumed_results.append(execute_issued_workload(
            workload, resolver, source_factory=source_factory,
            host=host, purpose=purpose, allow_test_only=allow_test_only,
            prior_receipts=prior_receipts, prior_outputs=prior_outputs,
            expected_wave=workload.original_wave_identity,
        ))
    # One final read for every item, after all native work and immediately
    # before publication. A change affecting an earlier completed result
    # still aborts the whole return.
    for item in items:
        require_unchanged(
            item, current_by_key[item.workload.decision_ref.key],
            "ISSUER_SNAPSHOT_CHANGED_BEFORE_PUBLICATION",
        )
    all_results = tuple(completed_results + resumed_results)
    output_refs = tuple(sorted(
        {ref for result in all_results for receipt in result.receipts
         for ref in receipt.result_refs},
        key=lambda ref: ref.key,
    ))
    receipt_materials = tuple(
        material(receipt) for result in all_results for receipt in result.receipts
    )
    return JoinedWorkloadResumeResult(
        checkpoint=checkpoint, completed_results=tuple(completed_results),
        resumed_results=tuple(resumed_results), output_refs=output_refs,
        receipt_materials=receipt_materials,
    )
