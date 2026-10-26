"""Minimal production transport into the existing U43/C11/I03/I05/Batch owners.

This module creates no authority, source semantics, descriptor, workload record,
or source reader. It only transports caller-supplied production objects into the
unchanged native executor.
"""
from __future__ import annotations

import json
from typing import Any, Callable, Mapping

from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_issued_workload import (
    CurrentDecisionResolver,
    NativeWorkload,
    OriginalWaveIdentity,
    WorkloadAdmissionError,
    execute_issued_workload,
)
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


def _assert_production_authorities(bundle: NativePreimageBundle, catalog: RuntimeObjectCatalog) -> None:
    if not isinstance(bundle, NativePreimageBundle):
        raise ProductionBindingRefusal("NATIVE_PREIMAGE_BUNDLE_REQUIRED")
    if not isinstance(catalog, RuntimeObjectCatalog):
        raise ProductionBindingRefusal("RUNTIME_CATALOG_REQUIRED")
    for authority in (*bundle.projection.authority_snapshots, *catalog.authorities):
        if authority.typed_state != "ALLOW" or authority.decision_state != "ALLOW":
            raise ProductionBindingRefusal("PRODUCTION_AUTHORITY_NOT_ALLOW")
        grade = authority.scope_envelope.get("grade") if isinstance(authority.scope_envelope, Mapping) else None
        if isinstance(grade, str) and "TEST_ONLY" in grade.upper():
            raise ProductionBindingRefusal("TEST_ONLY_AUTHORITY_IS_NOT_PRODUCTION")


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
    workload = NativeWorkload(
        decision_ref=exact_ref(decision_ref, "decision_ref"),
        source_factory_ref=exact_ref(source_factory_ref, "source_factory_ref"),
        descriptor=_descriptor_bytes(descriptor),
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
