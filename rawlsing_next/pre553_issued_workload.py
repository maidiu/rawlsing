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
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor, RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact, ExactRef, exact_ref, semantic_hash,
)
from types import SimpleNamespace
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
        """Authenticate issuer, scope, source/host/purpose and revocation externally."""
        ...


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
    if record.scope == "ORIGINAL_SOURCE_GRANTED" or expected_wave is not None:
        identity = workload.original_wave_identity
        if not isinstance(identity, OriginalWaveIdentity) or record.original_wave_identity != identity:
            raise WorkloadAdmissionError("ISSUED_ORIGINAL_WAVE_BINDING_REQUIRED")
        if expected_wave is not None and identity != expected_wave:
            raise WorkloadAdmissionError("ORIGINAL35_ROSTER_TO_NATIVE_PACKET_MISMATCH")
        if Counter(record.native_universe_refs) != Counter(u.ref for u in workload.projection.universes):
            raise WorkloadAdmissionError("ISSUED_NATIVE_UNIVERSE_TO_ORIGINAL_WAVE_MISMATCH")
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
    original_wave_identity: OriginalWaveIdentity | None = None
    source_sha256: str | None = None
    outputs_by_unit: Mapping[str, Any] | None = None


def execute_issued_workload(workload: NativeWorkload, resolver: CurrentDecisionResolver, *,
                            source_factory: Callable[[ExactRef], Any], host: str, purpose: str,
                            allow_test_only: bool = False, prior_receipts=(),
                            prior_outputs=None, max_units=None,
                            expected_wave: OriginalWaveIdentity | None = None):
    """Reuse C11, Route B, I03, I05 and Batch; eligibility comes from external U/E_pre.

    A factory is called only after admission. Source bytes stay inside the native
    owner. The return contains native results/receipts, with no authority promotion.
    Exact receipt persistence and preimages remain the existing Batch/C11 custody
    responsibility; prior receipts must resolve in the rebuilt native repository.
    """
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
    outputs = dict(prior_outputs)
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
        record.envelope_sha256, record.decision_ref, record.scope, runner.summary(),
        record.original_wave_identity, record.source_sha256, dict(outputs))


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
    completed_output_facts: Mapping[str, tuple[Mapping[str, Any], ...]]
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
            "completed_output_facts": {
                key: [material(row) for row in rows]
                for key, rows in self.completed_output_facts.items()
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


def _result_output_facts(result: Any) -> dict[str, tuple[Mapping[str, Any], ...]]:
    if getattr(result, "native_result", None) is not None:
        facts = getattr(result.native_result, "empirical_facts", ())
        unit_hash = result.manifest.units[0].unit_hash
        return {unit_hash: tuple(material(fact) for fact in facts)}
    outputs = getattr(result, "outputs_by_unit", None) or {}
    mapped = {}
    for unit_hash, output in outputs.items():
        facts = getattr(output, "facts", ())
        mapped[unit_hash] = tuple(material(fact) for fact in facts)
    return mapped


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
            "completed_output_facts": _result_output_facts(result),
            "receipt_materials": [material(receipt) for receipt in receipts],
            "output_refs": [ref.as_dict() for ref in output_refs],
        }
        entries.append(WorkloadCustodyEntry(
            decision_ref=result.decision_ref,
            envelope_sha256=result.envelope_sha256,
            source_sha256=(
                getattr(result, "source_sha256", None)
                or (source_sha256_by_decision or {}).get(result.decision_ref.key, "")
            ),
            manifest_hash=manifest.manifest_hash,
            kind=entry_payload["kind"], state=state,
            unit_materials=tuple(entry_payload["unit_materials"]),
            completed_output_facts=entry_payload["completed_output_facts"],
            receipt_materials=tuple(entry_payload["receipt_materials"]),
            output_refs=output_refs,
            entry_hash=semantic_hash(entry_payload),
        ))
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
    material_payload: Mapping[str, Any], *, expected_checkpoint_ref: str | None = None
) -> JoinedWorkloadCheckpoint:
    """Rehydrate a joined checkpoint and require the original external pin."""
    if not isinstance(expected_checkpoint_ref, str) or not expected_checkpoint_ref:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_EXPECTED_PIN_REQUIRED")
    payload = dict(material_payload)
    claimed = payload.get("checkpoint_hash")
    entries_material = payload.get("entries", ())
    computed_payload = {
        "schema": payload.get("schema"),
        "entries": [dict(row) for row in entries_material],
    }
    if claimed != semantic_hash(computed_payload):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_HASH_MISMATCH")
    if claimed != expected_checkpoint_ref:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_PIN_MISMATCH")
    entries = []
    for row in entries_material:
        entry_payload = {
            "decision_ref": row["decision_ref"],
            "envelope_sha256": row["envelope_sha256"],
            "source_sha256": row["source_sha256"],
            "manifest_hash": row["manifest_hash"],
            "kind": row["kind"], "state": row["state"],
            "unit_materials": row["unit_materials"],
            "completed_output_facts": row["completed_output_facts"],
            "receipt_materials": row["receipt_materials"],
            "output_refs": row["output_refs"],
        }
        if row.get("entry_hash") != semantic_hash(entry_payload):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_HASH_MISMATCH")
        restored_units = _restore_manifest(row["unit_materials"])
        if restored_units.manifest_hash != row["manifest_hash"]:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_MANIFEST_MISMATCH")
        entries.append(WorkloadCustodyEntry(
            decision_ref=exact_ref(row["decision_ref"]),
            envelope_sha256=row["envelope_sha256"],
            source_sha256=row["source_sha256"],
            manifest_hash=row["manifest_hash"],
            kind=row["kind"], state=row["state"],
            unit_materials=tuple(dict(item) for item in row["unit_materials"]),
            completed_output_facts={
                key: tuple(dict(item) for item in rows)
                for key, rows in row["completed_output_facts"].items()
            },
            receipt_materials=tuple(dict(item) for item in row["receipt_materials"]),
            output_refs=tuple(exact_ref(ref) for ref in row["output_refs"]),
            entry_hash=row["entry_hash"],
        ))
    return JoinedWorkloadCheckpoint(
        schema=payload["schema"], entries=tuple(entries),
        checkpoint_hash=claimed,
    )


def _completed_entry_view(entry: WorkloadCustodyEntry, scope: str) -> Any:
    manifest = _restore_manifest(entry.unit_materials)
    receipts = tuple(_restore_receipt(row) for row in entry.receipt_materials)
    if entry.kind == "DISCOVERY":
        facts = tuple(
            _restore_fact(row)
            for rows in entry.completed_output_facts.values() for row in rows
        )
        return SimpleNamespace(
            native_result=SimpleNamespace(empirical_facts=facts, receipts=receipts),
            manifest=manifest, receipts=receipts,
            envelope_sha256=entry.envelope_sha256,
            decision_ref=entry.decision_ref, scope=scope,
            source_sha256=entry.source_sha256,
        )
    outputs = {
        unit_hash: SimpleNamespace(facts=tuple(_restore_fact(row) for row in rows))
        for unit_hash, rows in entry.completed_output_facts.items()
    }
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
    source_factory: Callable[[ExactRef], Any],
    host: str,
    purpose: str,
    checkpoint: JoinedWorkloadCheckpoint,
    expected_checkpoint_ref: str | None = None,
    allow_test_only: bool = True,
) -> JoinedWorkloadResumeResult:
    """Resume actual R03-issued workloads, partial native prefixes included."""
    if not isinstance(checkpoint, JoinedWorkloadCheckpoint):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_REQUIRED")
    if expected_checkpoint_ref is None or checkpoint.checkpoint_hash != expected_checkpoint_ref:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_PIN_MISMATCH")
    by_decision = {item.record.decision_ref.key: item for item in workloads}
    if len(by_decision) != len(workloads):
        raise WorkloadAdmissionError("JOINED_WORKLOAD_DUPLICATE_DECISION")
    completed_entries = {entry.decision_ref.key: entry for entry in checkpoint.entries}
    if not set(completed_entries) <= set(by_decision):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_UNKNOWN_WORKLOAD")
    completed_results: list[Any] = []
    resumed_results: list[Any] = []
    for item in workloads:
        key = item.record.decision_ref.key
        entry = completed_entries.get(key)
        if entry is not None:
            if (entry.envelope_sha256 != semantic_hash(item.workload.envelope())
                    or entry.source_sha256 != item.record.source_sha256
                    or entry.decision_ref != item.record.decision_ref):
                raise WorkloadAdmissionError("JOINED_CHECKPOINT_WORKLOAD_IDENTITY_MISMATCH")
            if entry.state == "COMPLETED":
                completed_results.append(_completed_entry_view(entry, item.record.scope))
                continue
            prior_receipts = tuple(_restore_receipt(row) for row in entry.receipt_materials)
            prior_outputs = {
                unit_hash: SimpleNamespace(facts=tuple(_restore_fact(row) for row in rows))
                for unit_hash, rows in entry.completed_output_facts.items()
            }
            resumed_results.append(execute_issued_workload(
                item.workload, _resolver_for(item), source_factory=source_factory,
                host=host, purpose=purpose, allow_test_only=allow_test_only,
                prior_receipts=prior_receipts, prior_outputs=prior_outputs,
            ))
            continue
        resumed_results.append(execute_issued_workload(
            item.workload, _resolver_for(item), source_factory=source_factory,
            host=host, purpose=purpose, allow_test_only=allow_test_only,
        ))
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


def _resolver_for(item: Any) -> CurrentDecisionResolver:
    record = item.record
    class _Resolver:
        def resolve_current(self, decision_ref: ExactRef) -> IssuedWorkloadRecord:
            if decision_ref != record.decision_ref:
                raise WorkloadAdmissionError("UNKNOWN_DECISION_REF")
            return record
    return _Resolver()
