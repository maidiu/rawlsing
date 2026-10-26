"""Minimal production transport into the existing U43/C11/I03/I05/Batch owners.

This module creates no authority, source semantics, descriptor, workload record,
or source reader. It only transports caller-supplied production objects into the
unchanged native executor.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable, Mapping

from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_native_workload_binding import (
    profile_risk_tag, native_target_configuration,
)
from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec, ExecutionOutcome, ExecutorBinding,
)
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
from rawlsing_next.pre553_issued_workload import (
    CurrentDecisionResolver,
    NativeWorkload,
    NativeWorkloadResult,
    OriginalWaveIdentity,
    WorkloadAdmissionError,
    admit,
    execute_issued_workload,
)
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_source_native_preimage_adapter import NativePreimageBundle


class ProductionBindingRefusal(ValueError):
    def __init__(self, code: str, detail: str = ""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def _descriptor_bytes(descriptor: Mapping[str, Any]) -> bytes:
    if not isinstance(descriptor, Mapping):
        raise ProductionBindingRefusal("DESCRIPTOR_MAPPING_REQUIRED")
    material = dict(descriptor)
    if any(value is None or value == "UNBOUND" for value in material.values()):
        raise ProductionBindingRefusal("DESCRIPTOR_HAS_UNBOUND_FIELD")
    return json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _exact_descriptor(
    *, bundle: NativePreimageBundle, catalog: RuntimeObjectCatalog,
    requests: tuple[I03ExecutionRequest, ...], descriptor: Mapping[str, Any],
) -> bytes:
    projection = bundle.projection
    if len(requests) != 1:
        raise ProductionBindingRefusal("DESCRIPTOR_REQUIRES_ONE_EXACT_QUERY")
    request = requests[0]
    query = catalog.resolve_query_exact(request.query_ref)
    target_refs = tuple(exact_ref(ref, "descriptor.target_ref") for ref in query.target_refs)
    if len(target_refs) != 1:
        raise ProductionBindingRefusal("DESCRIPTOR_TARGET_ARITY_UNSUPPORTED")
    target_ref = target_refs[0]
    target_codes = [code for code, ref in bundle.question_refs.items() if ref == target_ref]
    if len(target_codes) != 1:
        raise ProductionBindingRefusal("DESCRIPTOR_TARGET_NOT_EXACT")
    topology, _ = native_target_configuration(bundle=bundle, target_ref=target_ref)
    grain = query.requested_output_grain
    if not isinstance(grain, Mapping):
        raise ProductionBindingRefusal("DESCRIPTOR_QUERY_GRAIN_REQUIRED")
    weight_basis = (projection.weight_slots[0].weight_basis_id
                    if projection.weight_slots else "NO_WEIGHT_DECLARED")
    estimand = (projection.weight_slots[0].estimand_authority_ref.as_dict()
                if projection.weight_slots
                else projection.universes[0].sampling_design_regime)
    expected = {
        "source_edition": bundle.source_sha256,
        "native_item_ids": list(sorted(bundle.administered_ids)),
        "release_tag": projection.instrument_release_id,
        "routing_and_risk": {
            "routing_facts": len(projection.routing),
            "risk_tag": profile_risk_tag(projection),
        },
        "carrier": {
            "source_format": bundle.source_format,
            "source_artifact_id": projection.source_artifact_id,
        },
        "country_and_population": {
            "country": projection.universes[0].country_geography,
            "population": projection.universes[0].target_population_and_sample_frame,
        },
        "weight_design_estimand": {
            "weight_basis": weight_basis,
            "estimand": estimand,
        },
        "missing_and_occurrence_policy": {
            "missing": "EXPLICIT_TYPED_STATES",
            "occurrence": topology,
        },
        "target_conditioner_roles": {
            "target": target_codes[0],
            "conditioner": None,
            "measure_kind": grain.get("measure_kind"),
        },
    }
    try:
        supplied = _descriptor_bytes(descriptor)
        supplied_material = json.loads(supplied)
    except ProductionBindingRefusal:
        raise
    except (TypeError, ValueError) as exc:
        raise ProductionBindingRefusal("DESCRIPTOR_CANONICAL_REQUIRED") from exc
    if supplied_material != expected:
        foreign = sorted(
            key for key in set(supplied_material) | set(expected)
            if supplied_material.get(key) != expected.get(key)
        )
        raise ProductionBindingRefusal("DESCRIPTOR_NOT_BOUND_TO_SOURCE", repr(foreign))
    return supplied


def _assert_production_authorities(bundle: NativePreimageBundle, catalog: RuntimeObjectCatalog) -> None:
    if not isinstance(bundle, NativePreimageBundle):
        raise ProductionBindingRefusal("NATIVE_PREIMAGE_BUNDLE_REQUIRED")
    if not isinstance(catalog, RuntimeObjectCatalog):
        raise ProductionBindingRefusal("RUNTIME_CATALOG_REQUIRED")
    universe_refs = tuple(universe.ref for universe in bundle.projection.universes)
    for authority in (*bundle.projection.authority_snapshots, *catalog.authorities):
        if authority.typed_state != "ALLOW" or authority.decision_state != "ALLOW":
            raise ProductionBindingRefusal("PRODUCTION_AUTHORITY_NOT_ALLOW")
        scope = authority.scope_envelope
        if not isinstance(scope, Mapping):
            raise ProductionBindingRefusal("PRODUCTION_AUTHORITY_SCOPE_REQUIRED")
        if scope.get("source_sha256") != bundle.source_sha256:
            raise ProductionBindingRefusal("PRODUCTION_AUTHORITY_SOURCE_MISMATCH")
        grade = scope.get("grade")
        if isinstance(grade, str) and "TEST_ONLY" in grade.upper():
            raise ProductionBindingRefusal("TEST_ONLY_AUTHORITY_IS_NOT_PRODUCTION")
        universe_scope = scope.get("source_universe_refs")
        if universe_scope not in ("EXPLICIT_UNRESTRICTED", "UNRESTRICTED_BY_THIS_AUTHORITY"):
            if isinstance(universe_scope, (str, bytes)) or not hasattr(universe_scope, "__iter__"):
                raise ProductionBindingRefusal("PRODUCTION_AUTHORITY_UNIVERSE_SCOPE_REQUIRED")
            try:
                declared = {exact_ref(value, "authority.scope.source_universe_refs").key
                            for value in universe_scope}
            except Exception as exc:
                raise ProductionBindingRefusal("PRODUCTION_AUTHORITY_UNIVERSE_SCOPE_REQUIRED") from exc
            if not set(ref.key for ref in universe_refs) <= declared:
                raise ProductionBindingRefusal("PRODUCTION_AUTHORITY_FOREIGN_UNIVERSE")


def _base_descriptor(bundle: NativePreimageBundle) -> dict[str, Any]:
    projection = bundle.projection
    return {
        "source_edition": bundle.source_sha256,
        "native_item_ids": list(sorted(bundle.administered_ids)),
        "release_tag": projection.instrument_release_id,
        "routing_and_risk": {
            "routing_facts": len(projection.routing),
            "risk_tag": profile_risk_tag(projection),
        },
        "carrier": {
            "source_format": bundle.source_format,
            "source_artifact_id": projection.source_artifact_id,
        },
        "country_and_population": {
            "country": projection.universes[0].country_geography,
            "population": projection.universes[0].target_population_and_sample_frame,
        },
        "weight_design_estimand": {
            "weight_basis": (projection.weight_slots[0].weight_basis_id
                             if projection.weight_slots else "NO_WEIGHT_DECLARED"),
            "estimand": (projection.weight_slots[0].estimand_authority_ref.as_dict()
                         if projection.weight_slots
                         else projection.universes[0].sampling_design_regime),
        },
        "missing_and_occurrence_policy": {
            "missing": "EXPLICIT_TYPED_STATES",
            "occurrence": "FRONTIER_DECLARED_TOPOLOGY",
        },
    }


def _exact_discovery_descriptor(
    *, bundle: NativePreimageBundle, frontier: Any, descriptor: Mapping[str, Any],
) -> bytes:
    expected = _base_descriptor(bundle)
    expected["target_conditioner_roles"] = {
        "targets": sorted({target.item_id for operation in frontier.operations
                           for target in operation.targets}),
        "conditions": sorted({key.item_id for operation in frontier.operations
                              for key, _ in operation.conditions}),
        "measures": sorted({
            "RAW" if operation.measure_kind == "SAMPLE" else "GOVERNED_WEIGHTED"
            for operation in frontier.operations
        }),
    }
    try:
        supplied = _descriptor_bytes(descriptor)
        supplied_material = json.loads(supplied)
    except ProductionBindingRefusal:
        raise
    except (TypeError, ValueError) as exc:
        raise ProductionBindingRefusal("DESCRIPTOR_CANONICAL_REQUIRED") from exc
    if supplied_material != expected:
        foreign = sorted(
            key for key in set(supplied_material) | set(expected)
            if supplied_material.get(key) != expected.get(key)
        )
        raise ProductionBindingRefusal("DISCOVERY_DESCRIPTOR_NOT_BOUND_TO_FRONTIER", repr(foreign))
    return supplied


@dataclass(frozen=True)
class ProductionDiscoveryPreparation:
    workload: NativeWorkload
    compilation: Any
    descriptor: Mapping[str, Any]
    expected_candidate_ids: tuple[str, ...]
    discovery_ref: ExactRef


def prepare_production_discovery(
    *,
    bundle: NativePreimageBundle,
    inventory: Any,
    policy: Any,
    frontier: Any,
    as_of: str,
    host: str,
    purpose: str,
    query_authority: Any,
    discovery_authority_snapshot: Any,
    descriptor: Mapping[str, Any],
    decision_ref: ExactRef | Mapping[str, Any],
    source_factory_ref: ExactRef | Mapping[str, Any],
    original_u_root: str,
    expected_frontier_root: str,
    original_wave_identity: OriginalWaveIdentity | None = None,
) -> ProductionDiscoveryPreparation:
    from rawlsing_next.pre553_universal_workload import compile_governed_frontier

    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=as_of, host=host, purpose=purpose,
        query_authority=query_authority,
        discovery_authority_snapshot=discovery_authority_snapshot,
    )
    catalog = compilation.runtime_catalog
    _assert_production_authorities(bundle, catalog)
    if len(catalog.discovery_authorities) != 1:
        raise ProductionBindingRefusal("EXACT_DISCOVERY_AUTHORITY_REQUIRED")
    descriptor_bytes = _exact_discovery_descriptor(
        bundle=bundle, frontier=frontier, descriptor=descriptor)
    discovery_ref = catalog.discovery_authorities[0].ref
    if not isinstance(original_u_root, str) or len(original_u_root) != 64:
        raise ProductionBindingRefusal("EXACT_U_ROOT_REQUIRED")
    if not isinstance(expected_frontier_root, str) or len(expected_frontier_root) != 64:
        raise ProductionBindingRefusal("EXACT_EPRE_FRONTIER_ROOT_REQUIRED")
    workload = NativeWorkload(
        decision_ref=exact_ref(decision_ref, "decision_ref"),
        source_factory_ref=exact_ref(source_factory_ref, "source_factory_ref"),
        descriptor=descriptor_bytes,
        projection=bundle.projection,
        catalog=catalog,
        requests=(),
        discoveries=(discovery_ref,),
        original_u_root=original_u_root,
        expected_frontier_root=expected_frontier_root,
        original_wave_identity=original_wave_identity,
    )
    workload.envelope()
    return ProductionDiscoveryPreparation(
        workload=workload, compilation=compilation, descriptor=dict(descriptor),
        expected_candidate_ids=compilation.expected_candidate_ids,
        discovery_ref=discovery_ref,
    )


def _execute_production_discovery(
    *, workload: NativeWorkload, resolver: CurrentDecisionResolver,
    source_factory: Callable[[ExactRef], Any], host: str, purpose: str,
) -> NativeWorkloadResult:
    record = admit(workload, resolver, host=host, purpose=purpose, allow_test_only=False)

    def check_current() -> None:
        current = admit(workload, resolver, host=host, purpose=purpose, allow_test_only=False)
        if current != record:
            raise ProductionBindingRefusal("ISSUER_SNAPSHOT_CHANGED_DURING_EXECUTION")

    source = source_factory(workload.source_factory_ref)
    if getattr(source, "source_sha256", None) != record.source_sha256:
        raise ProductionBindingRefusal("SOURCE_FACTORY_RETURNED_WRONG_EDITION")
    check_current()
    repository, release = build_source_backed_c11_repository(source, workload.projection)
    executor = CarrierNeutralResearchExecutor(
        repository, (release.release_ref,), workload.catalog)
    manifest = BatchManifest(tuple(
        BatchUnitSpec("DISCOVERY", ref, (release.release_ref,), (workload.decision_ref,))
        for ref in workload.discoveries
    ))
    outputs: dict[str, Any] = {}

    def execute(unit: BatchUnitSpec) -> ExecutionOutcome:
        check_current()
        result = executor.execute_i05(discovery_authority_ref=unit.job_ref)
        outputs[unit.unit_hash] = result
        return ExecutionOutcome(
            tuple(receipt.ref for receipt in result.receipts),
            (release.replay_manifest.ref, workload.decision_ref),
        )

    executor_ref = exact_ref(ExactRef(
        "U43_ISSUED_NATIVE_TRANSPORT",
        "urn:rawlsing:u43:r140-discovery:" + record.envelope_sha256,
        record.envelope_sha256,
    ), "executor_ref")
    runner = BatchExecutionRunner(manifest=manifest, repository=repository)
    runner.run(executors={
        "DISCOVERY": ExecutorBinding(executor_ref, execute),
    })
    check_current()
    if len(runner.receipts) != len(manifest.units) or any(
            receipt.state != "COMPLETED" for receipt in runner.receipts):
        raise ProductionBindingRefusal("NATIVE_DISCOVERY_EXECUTION_INCOMPLETE")
    return NativeWorkloadResult(
        (), tuple(outputs[key] for key in sorted(outputs)), manifest,
        runner.receipts,
        tuple(ref for receipt in runner.receipts for ref in receipt.result_refs),
        record.envelope_sha256, record.decision_ref, record.scope, runner.summary(),
        record.original_wave_identity, record.source_sha256, dict(outputs),
    )


def build_production_workload(
    *,
    bundle: NativePreimageBundle,
    catalog: RuntimeObjectCatalog,
    requests: tuple[I03ExecutionRequest, ...] = (),
    discoveries: tuple[ExactRef, ...] = (),
    descriptor: Mapping[str, Any],
    decision_ref: ExactRef | Mapping[str, Any],
    source_factory_ref: ExactRef | Mapping[str, Any],
    original_u_root: str,
    expected_frontier_root: str,
    original_wave_identity: OriginalWaveIdentity | None = None,
) -> NativeWorkload:
    """Prepare one unsigned exact native workload; the record remains external."""
    _assert_production_authorities(bundle, catalog)
    requests = tuple(requests)
    discoveries = tuple(exact_ref(ref, "discovery_ref") for ref in discoveries)
    if discoveries:
        raise ProductionBindingRefusal("PRODUCTION_DISCOVERY_ISSUANCE_CONTRACT_MISSING")
    if any(not isinstance(request, I03ExecutionRequest) for request in requests):
        raise ProductionBindingRefusal("EXACT_I03_REQUEST_REQUIRED")
    if not requests and not discoveries:
        raise ProductionBindingRefusal("NATIVE_OPERATION_REQUIRED")
    if not isinstance(original_u_root, str) or len(original_u_root) != 64:
        raise ProductionBindingRefusal("EXACT_U_ROOT_REQUIRED")
    if not isinstance(expected_frontier_root, str) or len(expected_frontier_root) != 64:
        raise ProductionBindingRefusal("EXACT_EPRE_FRONTIER_ROOT_REQUIRED")
    if original_wave_identity is not None and not isinstance(original_wave_identity, OriginalWaveIdentity):
        raise ProductionBindingRefusal("ORIGINAL_WAVE_IDENTITY_INVALID")
    descriptor_bytes = (_exact_descriptor(
        bundle=bundle, catalog=catalog, requests=requests, descriptor=descriptor)
        if requests else _descriptor_bytes(descriptor))
    workload = NativeWorkload(
        decision_ref=exact_ref(decision_ref, "decision_ref"),
        source_factory_ref=exact_ref(source_factory_ref, "source_factory_ref"),
        descriptor=descriptor_bytes,
        projection=bundle.projection,
        catalog=catalog,
        requests=requests,
        discoveries=discoveries,
        original_u_root=original_u_root,
        expected_frontier_root=expected_frontier_root,
        original_wave_identity=original_wave_identity,
    )
    workload.envelope()
    return workload


def build_production_query_workload(
    *,
    bundle: NativePreimageBundle,
    catalog: RuntimeObjectCatalog,
    request: I03ExecutionRequest,
    descriptor: Mapping[str, Any],
    decision_ref: ExactRef | Mapping[str, Any],
    source_factory_ref: ExactRef | Mapping[str, Any],
    original_u_root: str,
    expected_frontier_root: str,
    original_wave_identity: OriginalWaveIdentity | None = None,
) -> NativeWorkload:
    return build_production_workload(
        bundle=bundle, catalog=catalog, requests=(request,), discoveries=(),
        descriptor=descriptor, decision_ref=decision_ref,
        source_factory_ref=source_factory_ref, original_u_root=original_u_root,
        expected_frontier_root=expected_frontier_root,
        original_wave_identity=original_wave_identity,
    )


def execute_production_workload(
    *,
    workload: NativeWorkload,
    resolver: CurrentDecisionResolver,
    source_factory: Callable[[ExactRef], Any],
    host: str,
    purpose: str,
    prior_receipts=(),
    max_units=None,
    expected_wave: OriginalWaveIdentity | None = None,
):
    """Execute only after the externally supplied current record is admitted."""
    if not isinstance(workload, NativeWorkload):
        raise ProductionBindingRefusal("EXACT_NATIVE_WORKLOAD_REQUIRED")
    if workload.discoveries and not workload.requests:
        return _execute_production_discovery(
            workload=workload, resolver=resolver, source_factory=source_factory,
            host=host, purpose=purpose,
        )
    if workload.discoveries:
        raise ProductionBindingRefusal("PRODUCTION_COMBINED_QUERY_DISCOVERY_TRANSPORT_UNSUPPORTED")
    try:
        return execute_issued_workload(
            workload,
            resolver,
            source_factory=source_factory,
            host=host,
            purpose=purpose,
            allow_test_only=False,
            prior_receipts=prior_receipts,
            max_units=max_units,
            expected_wave=expected_wave,
        )
    except WorkloadAdmissionError:
        raise
