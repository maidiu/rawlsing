"""R135 narrow production transport qualification; synthetic harness, not source."""
from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot, ExactRef, semantic_hash,
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
