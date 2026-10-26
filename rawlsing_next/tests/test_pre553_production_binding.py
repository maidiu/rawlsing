"""R135 narrow production transport qualification; synthetic harness, not source."""
from __future__ import annotations

import dataclasses
from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot, ExactRef, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_issued_workload import (
    IssuedWorkloadRecord, OriginalWaveIdentity, WorkloadAdmissionError,
)
from rawlsing_next.pre553_native_workload_binding import (
    OperationFixture, build_projection_catalog, native_target_configuration,
    profile_risk_tag,
)
from rawlsing_next.pre553_production_binding import (
    ProductionBindingRefusal, build_production_query_workload,
    build_production_workload, execute_production_workload,
)
from rawlsing_next.pre553_source_native_preimage_adapter import (
    build_authority_set, materialize_native_preimages,
)
from rawlsing_next.tests.test_universal_source_projection import (
    build_s3, decode_sav, package, repeated_plan, s3_rows, write_rows,
)
from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceRule

HOST = "r135-harness-host"
PURPOSE = "R135_HARNESS_TRANSPORT_QUALIFICATION"


def _harness_authority(authority: AuthoritySnapshot, tag: str, grade: str = "TEST_HARNESS_ONLY") -> AuthoritySnapshot:
    fields = dict(authority.semantic_fields)
    fields["authority_id"] = f"R135-HARNESS-{tag}"
    fields["scope_envelope"] = {
        **dict(fields["scope_envelope"]),
        "grade": grade,
    }
    fields["authority_content_hash"] = semantic_hash({
        "tag": tag,
        "source_sha256": fields["scope_envelope"].get("source_sha256"),
    })
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=authority.authority_snapshot_refs,
        dependency_refs=authority.dependency_refs,
        producer_replay_locator_or_reference_root=authority.producer_replay_locator_or_reference_root,
        **fields,
    )


def _harness_bundle(tmp_path):
    path = tmp_path / "r135.sav"
    rows = s3_rows(respondents=6, occasions=2)
    write_rows(path, rows)
    incidence = decode_sav(path)
    pkg = package(path, len(rows), (NativeSourceRule("impl.score", "SCORE"),))
    base = build_authority_set(source=pkg.source, as_of=pkg.as_of)
    tags = ("source", "mapping", "coordinate", "routing", "weight", "replay", "projection")
    harness = tuple(_harness_authority(a, t) for a, t in zip(base, tags))
    return materialize_native_preimages(
        package=pkg, incidence=incidence, row_occurrence_plan=repeated_plan("SCORE"),
        authorities=harness), pkg


def _query_authority(bundle):
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=ExactRef(
            "REPLAY_ROOT", "urn:r135:harness:query-replay", "b" * 64),
        authority_id="R135-HARNESS-QUERY",
        authority_version="1.0.0",
        authority_content_hash=semantic_hash({
            "tag": "query", "source_sha256": bundle.source_sha256,
        }),
        authority_kind="PREDICATE_GRAMMAR",
        decision_state="ALLOW",
        governed_operations=("R135-HARNESS-QUERY",),
        governed_object_families=(
            "EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0",
            "EmpiricalFact@1.0.0",
        ),
        scope_envelope={
            "source_sha256": bundle.source_sha256,
            "source_universe_refs": [u.ref.as_dict() for u in bundle.projection.universes],
            "predicate_or_risk_set_refs": [bundle.risk_set_ref.as_dict()],
            "target_use_refs": "EXPLICIT_UNRESTRICTED",
            "grade": "TEST_HARNESS_ONLY",
        },
        effective_time_or_interval="2026-10-26",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash({"tag": "query"}),
        replay_protocol_ref=ExactRef("REPLAY_PROTOCOL", "urn:r135:harness:query", "c" * 64),
    )


def _descriptor(bundle):
    projection = bundle.projection
    topology, _ = native_target_configuration(
        bundle=bundle, target_ref=bundle.question_refs["SCORE"])
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
            "occurrence": topology,
        },
        "target_conditioner_roles": {
            "target": "SCORE", "conditioner": None, "measure_kind": "RAW",
        },
    }


def _production(tmp_path, value="0", *, scope="ORIGINAL_SOURCE_GRANTED", host=HOST, purpose=PURPOSE):
    bundle, _pkg = _harness_bundle(tmp_path)
    qauth = _query_authority(bundle)
    catalog, request = build_projection_catalog(
        bundle=bundle, operation=OperationFixture(
            fixture_id=f"R135-{value}", target_variable_code="SCORE", response_value=value,
        ), as_of="2026-10-26", query_authority=qauth,
    )
    wave = OriginalWaveIdentity("SRC135", "R135-HARNESS", "SYNTHETIC", "2026")
    decision = ExactRef("R135_HARNESS_DECISION", f"urn:r135:harness:{value}", "d" * 64)
    workload = build_production_query_workload(
        bundle=bundle, catalog=catalog, request=request, descriptor=_descriptor(bundle),
        decision_ref=decision,
        source_factory_ref=ExactRef("SOURCE_FACTORY", "urn:r135:harness:source", bundle.source_sha256),
        original_u_root="e" * 64, expected_frontier_root="f" * 64,
        original_wave_identity=wave,
    )
    record = IssuedWorkloadRecord(
        decision_ref=workload.decision_ref,
        source_permission_ref=ExactRef("R135_HARNESS_SOURCE_PERMISSION", "urn:r135:harness:source-permission", "1" * 64),
        scientific_permission_refs=(ExactRef("R135_HARNESS_SCIENTIFIC_PERMISSION", "urn:r135:harness:science-permission", "2" * 64),),
        host=host, purpose=purpose, source_sha256=bundle.source_sha256,
        envelope_sha256=semantic_hash(workload.envelope()),
        original_u_root=workload.original_u_root, expected_frontier_root=workload.expected_frontier_root,
        expected_jobs=(("QUERY", request.query_ref.key, request.predicate_ref.key),),
        currentness="CURRENT_GRANTED", scope=scope, original_wave_identity=wave,
        native_universe_refs=(bundle.projection.universes[0].ref,),
    )
    return bundle, workload, record


class Resolver:
    def __init__(self, record): self.record = record
    def resolve_current(self, decision_ref):
        if decision_ref != self.record.decision_ref: raise WorkloadAdmissionError("WRONG_DECISION")
        return self.record


def test_production_branch_uses_supplied_authority_and_emits_value_dependent_fact(tmp_path):
    bundle, workload, record = _production(tmp_path, "0")
    result = execute_production_workload(
        workload=workload, resolver=Resolver(record),
        source_factory=lambda _ref: bundle.physical_stream, host=HOST, purpose=PURPOSE,
    )
    assert result.scope == "ORIGINAL_SOURCE_GRANTED"
    assert len(result.receipts) == 1
    assert len(result.output_refs) == 1
    bundle2, workload2, record2 = _production(tmp_path, "1")
    result2 = execute_production_workload(
        workload=workload2, resolver=Resolver(record2),
        source_factory=lambda _ref: bundle2.physical_stream, host=HOST, purpose=PURPOSE,
    )
    assert result2.output_refs != result.output_refs
    again = execute_production_workload(
        workload=workload, resolver=Resolver(record),
        source_factory=lambda _ref: bundle.physical_stream, host=HOST, purpose=PURPOSE,
    )
    assert again.output_refs == result.output_refs


def test_production_actual_positive_is_topology_supported_with_real_support(tmp_path):
    bundle, workload, record = _production(tmp_path, "0")
    result = execute_production_workload(
        workload=workload, resolver=Resolver(record),
        source_factory=lambda _ref: bundle.physical_stream, host=HOST, purpose=PURPOSE,
    )
    fact = result.native_outputs[0].facts[0]
    assert fact.typed_state in {"SUPPORTED", "EXACT_SUPPORTED"}
    assert fact.raw_denominator_support > 0
    assert fact.raw_numerator_support > 0
    assert fact.target_topology["complete_cell_semantic_projection"]
    assert fact.target_topology["complete_cell_semantic_projection"][0]["cell"]
    assert fact.execution_detail == "exact governed target distribution resolved"


def test_production_refuses_test_only_wrong_host_purpose_and_envelope(tmp_path):
    bundle, workload, record = _production(tmp_path)
    with pytest.raises(WorkloadAdmissionError):
        execute_production_workload(
            workload=workload, resolver=Resolver(replace(record, scope="TEST_ONLY_SOURCEFREE")),
            source_factory=lambda _ref: bundle.physical_stream, host=HOST, purpose=PURPOSE,
        )
    with pytest.raises(WorkloadAdmissionError):
        execute_production_workload(
            workload=workload, resolver=Resolver(record),
            source_factory=lambda _ref: bundle.physical_stream, host=HOST, purpose="WRONG",
        )
    with pytest.raises(WorkloadAdmissionError):
        execute_production_workload(
            workload=workload, resolver=Resolver(replace(record, envelope_sha256="0" * 64)),
            source_factory=lambda _ref: bundle.physical_stream, host=HOST, purpose=PURPOSE,
        )


def test_production_refuses_test_only_authority_and_wrong_source_binding(tmp_path):
    bundle, workload, record = _production(tmp_path)
    qauth = _harness_authority(_query_authority(bundle), "query-test-only", grade="TEST_ONLY_SOURCEFREE")
    catalog, request = build_projection_catalog(
        bundle=bundle, operation=OperationFixture(
            fixture_id="R135-test-only", target_variable_code="SCORE", response_value="0",
        ), as_of="2026-10-26", query_authority=qauth,
    )
    with pytest.raises(ProductionBindingRefusal, match="TEST_ONLY_AUTHORITY"):
        build_production_query_workload(
            bundle=bundle, catalog=catalog, request=request, descriptor=_descriptor(bundle),
            decision_ref=workload.decision_ref,
            source_factory_ref=workload.source_factory_ref,
            original_u_root=workload.original_u_root,
            expected_frontier_root=workload.expected_frontier_root,
            original_wave_identity=workload.original_wave_identity,
        )
    with pytest.raises(WorkloadAdmissionError):
        execute_production_workload(
            workload=workload, resolver=Resolver(replace(record, source_sha256="0" * 64)),
            source_factory=lambda _ref: bundle.physical_stream, host=HOST, purpose=PURPOSE,
        )
    with pytest.raises(WorkloadAdmissionError):
        execute_production_workload(
            workload=workload, resolver=Resolver(replace(record, expected_jobs=())),
            source_factory=lambda _ref: bundle.physical_stream, host=HOST, purpose=PURPOSE,
        )


def test_production_refuses_wrong_roots_universe_and_authority_role(tmp_path):
    bundle, workload, record = _production(tmp_path)
    for wrong in (
        replace(record, original_u_root="0" * 64),
        replace(record, expected_frontier_root="0" * 64),
        replace(record, native_universe_refs=()),
    ):
        with pytest.raises(WorkloadAdmissionError):
            execute_production_workload(
                workload=workload, resolver=Resolver(wrong),
                source_factory=lambda _ref: bundle.physical_stream, host=HOST, purpose=PURPOSE,
            )
    wrong_role = _harness_authority(_query_authority(bundle), "query-wrong-role")
    fields = dict(wrong_role.semantic_fields)
    fields["authority_kind"] = "TARGET_USE_PERMISSION"
    wrong_role = AuthoritySnapshot(
        typed_state="ALLOW", authority_snapshot_refs=wrong_role.authority_snapshot_refs,
        dependency_refs=wrong_role.dependency_refs,
        producer_replay_locator_or_reference_root=wrong_role.producer_replay_locator_or_reference_root,
        **fields,
    )
    from rawlsing_next.pre553_native_workload_binding import WorkloadBindingRefusal
    with pytest.raises(WorkloadBindingRefusal, match="SUPPLIED_QUERY_AUTHORITY_NOT_POSITIVE"):
        build_projection_catalog(
            bundle=bundle, operation=OperationFixture(
                fixture_id="R135-wrong-role", target_variable_code="SCORE", response_value="0",
            ), as_of="2026-10-26", query_authority=wrong_role,
        )


def test_production_refuses_unbound_risk_descriptor(tmp_path):
    bundle, workload, record = _production(tmp_path)
    catalog, request = build_projection_catalog(
        bundle=bundle, operation=OperationFixture(
            fixture_id="R135-unbound-risk", target_variable_code="SCORE", response_value="0",
        ), as_of="2026-10-26", query_authority=_query_authority(bundle),
    )
    bad = _descriptor(bundle)
    bad["routing_and_risk"] = None
    with pytest.raises(ProductionBindingRefusal, match="DESCRIPTOR_HAS_UNBOUND_FIELD"):
        build_production_query_workload(
            bundle=bundle, catalog=catalog, request=request, descriptor=bad,
            decision_ref=workload.decision_ref,
            source_factory_ref=workload.source_factory_ref,
            original_u_root=workload.original_u_root,
            expected_frontier_root=workload.expected_frontier_root,
            original_wave_identity=workload.original_wave_identity,
        )


def _bad_scope(authority, **changes):
    fields = dict(authority.semantic_fields)
    fields["scope_envelope"] = {**dict(fields["scope_envelope"]), **changes}
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=authority.authority_snapshot_refs,
        dependency_refs=authority.dependency_refs,
        producer_replay_locator_or_reference_root=(
            authority.producer_replay_locator_or_reference_root
        ),
        **fields,
    )


def test_production_refuses_foreign_query_authority_scope(tmp_path):
    from rawlsing_next.pre553_native_workload_binding import WorkloadBindingRefusal

    bundle, workload, record = _production(tmp_path)
    for changed in (
        {"source_sha256": "0" * 64},
        {"source_universe_refs": []},
        {"predicate_or_risk_set_refs": []},
    ):
        with pytest.raises(WorkloadBindingRefusal):
            build_projection_catalog(
                bundle=bundle,
                operation=OperationFixture("R137-foreign", "SCORE", "0"),
                as_of="2026-10-26",
                query_authority=_bad_scope(_query_authority(bundle), **changed),
            )


def test_production_refuses_foreign_source_authority_before_materialization(tmp_path):
    from rawlsing_next.pre553_source_native_preimage_adapter import NativePreimageRefusal

    bundle, _ = _harness_bundle(tmp_path)
    bad = _bad_scope(bundle.projection.authority_snapshots[0], source_sha256="0" * 64)
    incidence = decode_sav(tmp_path / "r135.sav")
    pkg = package(tmp_path / "r135.sav", len(s3_rows(respondents=6, occasions=2)),
                  (NativeSourceRule("impl.score", "SCORE"),))
    with pytest.raises(NativePreimageRefusal, match="SUPPLIED_AUTHORITY_SOURCE_MISMATCH"):
        materialize_native_preimages(
            package=pkg, incidence=incidence, row_occurrence_plan=repeated_plan("SCORE"),
            authorities=(bad,) + bundle.projection.authority_snapshots[1:],
        )


def test_production_refuses_foreign_descriptor_metadata(tmp_path):
    bundle, workload, record = _production(tmp_path)
    catalog, request = build_projection_catalog(
        bundle=bundle, operation=OperationFixture("R137-descriptor", "SCORE", "0"),
        as_of="2026-10-26", query_authority=_query_authority(bundle),
    )
    bad = _descriptor(bundle)
    bad["source_edition"] = "0" * 64
    bad["country_and_population"] = {"country": "ZZ", "population": "FOREIGN"}
    with pytest.raises(ProductionBindingRefusal, match="DESCRIPTOR_NOT_BOUND_TO_SOURCE"):
        build_production_query_workload(
            bundle=bundle, catalog=catalog, request=request, descriptor=bad,
            decision_ref=workload.decision_ref,
            source_factory_ref=workload.source_factory_ref,
            original_u_root=workload.original_u_root,
            expected_frontier_root=workload.expected_frontier_root,
            original_wave_identity=workload.original_wave_identity,
        )


def test_production_refuses_unbanked_discovery_ingress(tmp_path):
    bundle, workload, _ = _production(tmp_path)
    with pytest.raises(ProductionBindingRefusal, match="PRODUCTION_DISCOVERY_ISSUANCE_CONTRACT_MISSING"):
        build_production_workload(
            bundle=bundle, catalog=workload.catalog, discoveries=(workload.decision_ref,),
            descriptor=_descriptor(bundle), decision_ref=workload.decision_ref,
            source_factory_ref=workload.source_factory_ref,
            original_u_root=workload.original_u_root,
            expected_frontier_root=workload.expected_frontier_root,
            original_wave_identity=workload.original_wave_identity,
        )


def _discovery_fixture(tmp_path):
    from dataclasses import replace as _replace

    from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot
    from rawlsing_next.pre553_native_workload_binding import (
        build_frontier_native_catalog,
    )
    from rawlsing_next.universal_grammar.native_map import lower_frontier
    from rawlsing_next.tests.test_universal_grammar import (
        _frontier, _inventory, _occurrence, _policy,
    )

    path = tmp_path / "r140-scalar.sav"
    values = [(0, 0, 1), (1, 0, 0), (0, 1, 1), (1, 1, 0), (0, 0, 1), (1, 1, 0)]
    rows = [{"ROWID": float(i + 1), "X": float(x), "Y": float(y), "Z": float(z)}
            for i, (x, y, z) in enumerate(values)]
    write_rows(path, rows)
    pkg = package(path, len(rows), (
        NativeSourceRule("impl.x", "X"), NativeSourceRule("impl.y", "Y"),
        NativeSourceRule("impl.z", "Z")), coordinate="ROWID")
    base = build_authority_set(source=pkg.source, as_of=pkg.as_of)
    tags = ("source", "mapping", "coordinate", "routing", "weight", "replay", "projection")
    harness = tuple(_harness_authority(a, tag) for a, tag in zip(base, tags))
    bundle = materialize_native_preimages(package=pkg, incidence=decode_sav(path),
                                          authorities=harness)
    inventory = _replace(
        _inventory((_occurrence("X"), _occurrence("Y"), _occurrence("Z"))),
        source_sha256=bundle.source_sha256, source_id="R140-SCALAR",
        wave="W1", edition="E1", scope="W1",
    )
    policy = _policy()
    frontier = _frontier(inventory, policy)
    query_authority = _query_authority(bundle)
    catalog, _qa, _baseline, _projection_auth = build_frontier_native_catalog(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of="2026-10-26", query_authority=query_authority,
    )
    pending = set(frontier.pending_operation_ids)
    active = _replace(frontier, operations=tuple(
        op for op in frontier.operations if op.op_id not in pending))
    plan = lower_frontier(inventory, policy, active, catalog)
    grammar = plan.native_grammar()
    fields = dict(query_authority.semantic_fields)
    fields.update(
        authority_id="R140-HARNESS-DISCOVERY",
        authority_kind="DISCOVERY_FRONTIER",
        governed_operations=(str(grammar["discovery_operation"]),),
        governed_object_families=(
            "DiscoveryAuthority@1.0.0", "DiscoveryResultReceipt@1.0.0",
            "EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0",
            "EmpiricalFact@1.0.0",
        ),
        scope_envelope={
            **dict(fields["scope_envelope"]),
            "grade": "TEST_HARNESS_ONLY",
        },
        authority_content_hash=semantic_hash({
            "tag": "discovery", "source": bundle.source_sha256,
        }),
    )
    discovery_snapshot = AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=query_authority.authority_snapshot_refs,
        dependency_refs=query_authority.dependency_refs,
        producer_replay_locator_or_reference_root=(
            query_authority.producer_replay_locator_or_reference_root),
        **fields,
    )
    return bundle, inventory, policy, frontier, query_authority, discovery_snapshot


def _discovery_descriptor(bundle, frontier):
    from rawlsing_next.pre553_production_binding import _base_descriptor
    descriptor = _base_descriptor(bundle)
    descriptor["missing_and_occurrence_policy"] = {
        "missing": "EXPLICIT_TYPED_STATES",
        "occurrence": "FRONTIER_DECLARED_TOPOLOGY",
    }
    descriptor["target_conditioner_roles"] = {
        "targets": sorted({target.item_id for op in frontier.operations
                           for target in op.targets}),
        "conditions": sorted({key.item_id for op in frontier.operations
                              for key, _ in op.conditions}),
        "measures": sorted({"RAW" if op.measure_kind == "SAMPLE"
                            else "GOVERNED_WEIGHTED"
                            for op in frontier.operations}),
    }
    return descriptor


def test_production_bounded_discovery_full_frontier_native_values_and_accounting(tmp_path):
    from rawlsing_next.pre553_issued_workload import OriginalWaveIdentity
    from rawlsing_next.pre553_production_binding import prepare_production_discovery
    from rawlsing_next.universal_grammar.native_map import native_receipt_anti_join

    bundle, inventory, policy, frontier, qa, ds = _discovery_fixture(tmp_path)
    wave = OriginalWaveIdentity("SRC140", "R140", "SYNTHETIC", "W1")
    prep = prepare_production_discovery(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of="2026-10-26", host="r140-harness-host", purpose="R140_DISCOVERY",
        query_authority=qa, discovery_authority_snapshot=ds,
        descriptor=_discovery_descriptor(bundle, frontier),
        decision_ref=ExactRef("R140_DECISION", "urn:r140:discovery", "d" * 64),
        source_factory_ref=ExactRef("SOURCE_FACTORY", "urn:r140:source", bundle.source_sha256),
        original_u_root="e" * 64, expected_frontier_root="f" * 64,
        original_wave_identity=wave,
    )
    record = IssuedWorkloadRecord(
        decision_ref=prep.workload.decision_ref,
        source_permission_ref=ExactRef("R140_SOURCE_PERMISSION", "urn:r140:s", "1" * 64),
        scientific_permission_refs=(ExactRef(
            "R140_SCIENTIFIC_PERMISSION", "urn:r140:sci", "2" * 64),),
        host="r140-harness-host", purpose="R140_DISCOVERY",
        source_sha256=bundle.source_sha256,
        envelope_sha256=semantic_hash(prep.workload.envelope()),
        original_u_root=prep.workload.original_u_root,
        expected_frontier_root=prep.workload.expected_frontier_root,
        expected_jobs=(("DISCOVERY", prep.discovery_ref.key, ""),),
        currentness="CURRENT_GRANTED", scope="ORIGINAL_SOURCE_GRANTED",
        original_wave_identity=wave,
        native_universe_refs=(bundle.projection.universes[0].ref,),
    )
    result = execute_production_workload(
        workload=prep.workload, resolver=Resolver(record),
        source_factory=lambda _ref: bundle.physical_stream,
        host="r140-harness-host", purpose="R140_DISCOVERY",
    )
    native = result.native_outputs[0]
    assert prep.compilation.runtime_catalog.queries
    assert prep.compilation.expected_operation_ids
    assert native.candidate_count == native.covered_candidate_count == len(
        prep.expected_candidate_ids)
    assert len(native.receipts) == native.candidate_count
    assert {receipt.typed_state for receipt in native.receipts} >= {
        "DISCOVERED_RESULT_SUPPORTED", "VALID_EMPTY"}
    assert all(receipt.coverage_state.startswith("EVALUATED_")
               for receipt in native.receipts)
    facts = {fact.ref.key: fact for fact in native.empirical_facts}
    assert len(facts) == len(native.empirical_facts)
    assert {ref.key for ref in native.empirical_fact_refs} == set(facts)
    receipt_fact_refs = {exact_ref(ref).key for receipt in native.receipts
                         for ref in receipt.empirical_fact_refs}
    assert receipt_fact_refs <= set(facts)
    supported = [fact for fact in native.empirical_facts
                 if fact.typed_state in {"SUPPORTED", "EXACT_SUPPORTED"}]
    assert supported
    assert any(fact.raw_denominator_support > 0 and fact.raw_numerator_support > 0
               for fact in supported)
    anti = native_receipt_anti_join(prep.compilation.plan, native.receipts)
    assert anti["no_drop_ok"] is True
    assert anti["missing_candidate_ids"] == anti["unexpected_candidate_ids"] == ()
    restored = execute_production_workload(
        workload=prep.workload, resolver=Resolver(record),
        source_factory=lambda _ref: bundle.physical_stream,
        host="r140-harness-host", purpose="R140_DISCOVERY",
    )
    assert restored.native_outputs[0].receipts == native.receipts
    assert restored.native_outputs[0].empirical_facts == native.empirical_facts
    assert restored.native_outputs[0].evaluated_frontier_ref == native.evaluated_frontier_ref


def _clone_authority(authority, **changes):
    fields = dict(authority.semantic_fields)
    fields.update(changes)
    return AuthoritySnapshot(
        typed_state=fields.pop("typed_state", authority.typed_state),
        authority_snapshot_refs=authority.authority_snapshot_refs,
        dependency_refs=authority.dependency_refs,
        producer_replay_locator_or_reference_root=(
            authority.producer_replay_locator_or_reference_root),
        **fields,
    )


def test_production_discovery_refuses_foreign_authority_descriptor_and_currentness(tmp_path):
    from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot
    from rawlsing_next.pre553_native_workload_binding import (
        WorkloadBindingRefusal, build_discovery_authority,
    )
    from rawlsing_next.pre553_production_binding import prepare_production_discovery

    bundle, inventory, policy, frontier, qa, ds = _discovery_fixture(tmp_path)
    with pytest.raises(WorkloadBindingRefusal, match="SUPPLIED_QUERY_AUTHORITY_SOURCE_MISMATCH"):
        prepare_production_discovery(
            bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
            as_of="2026-10-26", host="r140-harness-host", purpose="R140_DISCOVERY",
            query_authority=_bad_scope(qa, source_sha256="0" * 64),
            discovery_authority_snapshot=ds,
            descriptor=_discovery_descriptor(bundle, frontier),
            decision_ref=ExactRef("R140_DECISION", "urn:r140:bad", "d" * 64),
            source_factory_ref=ExactRef("SOURCE_FACTORY", "urn:r140:bad", bundle.source_sha256),
            original_u_root="e" * 64, expected_frontier_root="f" * 64,
        )
    with pytest.raises(WorkloadBindingRefusal, match="SUPPLIED_DISCOVERY_AUTHORITY_SOURCE_MISMATCH"):
        prepare_production_discovery(
            bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
            as_of="2026-10-26", host="r140-harness-host", purpose="R140_DISCOVERY",
            query_authority=qa,
            discovery_authority_snapshot=_bad_scope(ds, source_sha256="0" * 64),
            descriptor=_discovery_descriptor(bundle, frontier),
            decision_ref=ExactRef("R140_DECISION", "urn:r140:bad2", "d" * 64),
            source_factory_ref=ExactRef("SOURCE_FACTORY", "urn:r140:bad2", bundle.source_sha256),
            original_u_root="e" * 64, expected_frontier_root="f" * 64,
        )
    with pytest.raises(WorkloadBindingRefusal, match="SUPPLIED_DISCOVERY_AUTHORITY_RISK_MISMATCH"):
        prepare_production_discovery(
            bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
            as_of="2026-10-26", host="r140-harness-host", purpose="R140_DISCOVERY",
            query_authority=qa,
            discovery_authority_snapshot=_bad_scope(ds, predicate_or_risk_set_refs=[]),
            descriptor=_discovery_descriptor(bundle, frontier),
            decision_ref=ExactRef("R140_DECISION", "urn:r140:bad-risk", "d" * 64),
            source_factory_ref=ExactRef("SOURCE_FACTORY", "urn:r140:bad-risk", bundle.source_sha256),
            original_u_root="e" * 64, expected_frontier_root="f" * 64,
        )
    from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
    wrong_operation = _clone_authority(ds, governed_operations=("R140-WRONG-OPERATION",))
    with pytest.raises(Pre553AuthorityError):
        prepare_production_discovery(
            bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
            as_of="2026-10-26", host="r140-harness-host", purpose="R140_DISCOVERY",
            query_authority=qa, discovery_authority_snapshot=wrong_operation,
            descriptor=_discovery_descriptor(bundle, frontier),
            decision_ref=ExactRef("R140_DECISION", "urn:r140:bad-op", "d" * 64),
            source_factory_ref=ExactRef("SOURCE_FACTORY", "urn:r140:bad-op", bundle.source_sha256),
            original_u_root="e" * 64, expected_frontier_root="f" * 64,
        )
    with pytest.raises(WorkloadBindingRefusal, match="FRONTIER_POLICY_HASH_MISMATCH"):
        prepare_production_discovery(
            bundle=bundle, inventory=inventory, policy=policy,
            frontier=dataclasses.replace(frontier, policy_hash="0" * 64),
            as_of="2026-10-26", host="r140-harness-host", purpose="R140_DISCOVERY",
            query_authority=qa, discovery_authority_snapshot=ds,
            descriptor=_discovery_descriptor(bundle, frontier),
            decision_ref=ExactRef("R140_DECISION", "urn:r140:bad-frontier", "d" * 64),
            source_factory_ref=ExactRef("SOURCE_FACTORY", "urn:r140:bad-frontier", bundle.source_sha256),
            original_u_root="e" * 64, expected_frontier_root="f" * 64,
        )
    bad = _discovery_descriptor(bundle, frontier)
    bad["target_conditioner_roles"]["measures"] = ["WEIGHTED_FOREIGN"]
    with pytest.raises(ProductionBindingRefusal, match="DISCOVERY_DESCRIPTOR_NOT_BOUND_TO_FRONTIER"):
        prepare_production_discovery(
            bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
            as_of="2026-10-26", host="r140-harness-host", purpose="R140_DISCOVERY",
            query_authority=qa, discovery_authority_snapshot=ds, descriptor=bad,
            decision_ref=ExactRef("R140_DECISION", "urn:r140:bad-measure", "d" * 64),
            source_factory_ref=ExactRef("SOURCE_FACTORY", "urn:r140:bad-measure", bundle.source_sha256),
            original_u_root="e" * 64, expected_frontier_root="f" * 64,
        )
    bad = _discovery_descriptor(bundle, frontier)
    bad["carrier"] = {"source_format": "DTA", "source_artifact_id": "foreign"}
    with pytest.raises(ProductionBindingRefusal, match="DISCOVERY_DESCRIPTOR_NOT_BOUND_TO_FRONTIER"):
        prepare_production_discovery(
            bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
            as_of="2026-10-26", host="r140-harness-host", purpose="R140_DISCOVERY",
            query_authority=qa, discovery_authority_snapshot=ds,
            descriptor=bad,
            decision_ref=ExactRef("R140_DECISION", "urn:r140:bad3", "d" * 64),
            source_factory_ref=ExactRef("SOURCE_FACTORY", "urn:r140:bad3", bundle.source_sha256),
            original_u_root="e" * 64, expected_frontier_root="f" * 64,
        )


def test_production_discovery_refuses_noncurrent_record_before_native_execution(tmp_path):
    from rawlsing_next.pre553_issued_workload import OriginalWaveIdentity
    from rawlsing_next.pre553_production_binding import prepare_production_discovery

    bundle, inventory, policy, frontier, qa, ds = _discovery_fixture(tmp_path)
    wave = OriginalWaveIdentity("SRC140", "R140", "SYNTHETIC", "W1")
    prep = prepare_production_discovery(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of="2026-10-26", host="r140-harness-host", purpose="R140_DISCOVERY",
        query_authority=qa, discovery_authority_snapshot=ds,
        descriptor=_discovery_descriptor(bundle, frontier),
        decision_ref=ExactRef("R140_DECISION", "urn:r140:stale", "d" * 64),
        source_factory_ref=ExactRef("SOURCE_FACTORY", "urn:r140:stale", bundle.source_sha256),
        original_u_root="e" * 64, expected_frontier_root="f" * 64,
        original_wave_identity=wave,
    )
    stale = IssuedWorkloadRecord(
        decision_ref=prep.workload.decision_ref,
        source_permission_ref=ExactRef("R140_SOURCE_PERMISSION", "urn:r140:s", "1" * 64),
        scientific_permission_refs=(ExactRef(
            "R140_SCIENTIFIC_PERMISSION", "urn:r140:sci", "2" * 64),),
        host="r140-harness-host", purpose="R140_DISCOVERY",
        source_sha256=bundle.source_sha256,
        envelope_sha256=semantic_hash(prep.workload.envelope()),
        original_u_root=prep.workload.original_u_root,
        expected_frontier_root=prep.workload.expected_frontier_root,
        expected_jobs=(("DISCOVERY", prep.discovery_ref.key, ""),),
        currentness="REVOKED", scope="ORIGINAL_SOURCE_GRANTED",
        original_wave_identity=wave,
        native_universe_refs=(bundle.projection.universes[0].ref,),
    )
    with pytest.raises(WorkloadAdmissionError):
        execute_production_workload(
            workload=prep.workload, resolver=Resolver(stale),
            source_factory=lambda _ref: (_ for _ in ()).throw(
                AssertionError("source factory called")),
            host="r140-harness-host", purpose="R140_DISCOVERY",
        )


def test_R141_query_authority_scope_successor_replays_R138_foreign_fields(tmp_path):
    """Versioned successor for the preserved RED R138 scope witness."""
    from rawlsing_next.pre553_native_workload_binding import WorkloadBindingRefusal

    bundle, _workload, _record = _production(tmp_path)
    for changes in (
        {"target_use_refs": []},
        {"target_use_refs": "FOREIGN_TARGET_USE"},
        {"measure": "GOVERNED_WEIGHTED"},
        {"as_of": "1999-01-01"},
        {"grammar": "FOREIGN_GRAMMAR"},
        {"frontier": "FOREIGN_FRONTIER"},
    ):
        with pytest.raises(WorkloadBindingRefusal):
            build_projection_catalog(
                bundle=bundle,
                operation=OperationFixture("R141-successor", "SCORE", "0"),
                as_of="2026-10-26",
                query_authority=_bad_scope(_query_authority(bundle), **changes),
            )
