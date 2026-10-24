"""Helper: build the author's real multi-unit workload from R03 issued objects."""
from __future__ import annotations


def build_multi(bundle, issued, *, as_of, host, purpose):
    from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
    from rawlsing_next.pre553_issued_workload import (
        IssuedWorkloadRecord, NativeWorkload, operation_jobs,
    )
    from rawlsing_next.pre553_native_workload_binding import (
        OperationFixture, TestOnlyDecisionResolver, TestOnlyIssuedWorkload,
        build_projection_catalog,
    )
    from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash

    first, second = issued[0], issued[1]
    catalogs = []
    for item, variable, value in (
        (first, "SCORE", "0"), (second, "SCORE", "1"),
    ):
        fixture = OperationFixture(
            fixture_id="R04V-R2-" + variable + value,
            target_variable_code=variable, response_value=value)
        catalog, request = build_projection_catalog(
            bundle=bundle, operation=fixture, as_of=as_of)
        catalogs.append((catalog, request))
    authorities = {}
    predicates = {}
    queries = {}
    for catalog, _ in catalogs:
        for obj in catalog.authorities:
            authorities[obj.authority_ref.key] = obj
        for obj in catalog.predicates:
            predicates[obj.ref.key] = obj
        for obj in catalog.queries:
            queries[obj.ref.key] = obj
    runtime_catalog = RuntimeObjectCatalog(
        authorities=tuple(authorities.values()),
        predicates=tuple(predicates.values()),
        queries=tuple(queries.values()),
        discovery_authorities=(),
    )
    requests = tuple(request for _, request in catalogs)
    base = first.workload
    workload = NativeWorkload(
        decision_ref=ExactRef("R91_PARTIAL_DECISION", "urn:test:r04v:r2:partial", "9" * 64),
        source_factory_ref=base.source_factory_ref,
        descriptor=base.descriptor, projection=base.projection,
        catalog=runtime_catalog, requests=requests, discoveries=(),
        original_u_root=base.original_u_root,
        expected_frontier_root=base.expected_frontier_root,
    )
    record = IssuedWorkloadRecord(
        decision_ref=workload.decision_ref,
        source_permission_ref=first.record.source_permission_ref,
        scientific_permission_refs=first.record.scientific_permission_refs,
        host=host, purpose=purpose,
        source_sha256=first.record.source_sha256,
        envelope_sha256=semantic_hash(workload.envelope()),
        original_u_root=workload.original_u_root,
        expected_frontier_root=workload.expected_frontier_root,
        expected_jobs=operation_jobs(requests, ()),
        currentness="CURRENT_GRANTED", scope=first.record.scope,
    )
    multi = TestOnlyIssuedWorkload(
        workload=workload, record=record, descriptor=first.descriptor,
        envelope_sha256=record.envelope_sha256)
    return multi, TestOnlyDecisionResolver(record)
