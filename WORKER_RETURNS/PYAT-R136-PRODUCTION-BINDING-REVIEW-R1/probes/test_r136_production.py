"""R136 focused production-binding probes (synthetic harness, TEST_ONLY)."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_issued_workload import (
    IssuedWorkloadRecord, OriginalWaveIdentity,
)
from rawlsing_next.pre553_native_workload_binding import (
    OperationFixture, build_projection_catalog,
)
from rawlsing_next.pre553_production_binding import (
    build_production_query_workload, execute_production_workload,
)
from rawlsing_next.tests.test_pre553_production_binding import (
    HOST, PURPOSE, Resolver, _descriptor, _harness_bundle, _query_authority,
)


def _wrong_query_source(qauth):
    fields = dict(qauth.semantic_fields)
    fields["scope_envelope"] = {
        **dict(fields["scope_envelope"]),
        "source_sha256": "0" * 64,
    }
    return type(qauth)(
        typed_state="ALLOW",
        authority_snapshot_refs=qauth.authority_snapshot_refs,
        dependency_refs=qauth.dependency_refs,
        producer_replay_locator_or_reference_root=(
            qauth.producer_replay_locator_or_reference_root
        ),
        **fields,
    )


def _run(tmp_path, *, qauth_transform=None, descriptor_transform=None):
    bundle, _pkg = _harness_bundle(tmp_path)
    qauth = _query_authority(bundle)
    if qauth_transform is not None:
        qauth = qauth_transform(qauth)
    catalog, request = build_projection_catalog(
        bundle=bundle,
        operation=OperationFixture(
            fixture_id="R136-wrong", target_variable_code="SCORE",
            response_value="0",
        ),
        as_of="2026-10-26", query_authority=qauth,
    )
    descriptor = _descriptor(bundle)
    if descriptor_transform is not None:
        descriptor = descriptor_transform(descriptor)
    wave = OriginalWaveIdentity("SRC135", "R135-HARNESS", "SYNTHETIC", "2026")
    decision = ExactRef(
        "R136_HARNESS_DECISION", "urn:r136:harness:wrong", "d" * 64,
    )
    workload = build_production_query_workload(
        bundle=bundle, catalog=catalog, request=request,
        descriptor=descriptor, decision_ref=decision,
        source_factory_ref=ExactRef(
            "SOURCE_FACTORY", "urn:r136:harness:source", bundle.source_sha256,
        ),
        original_u_root="e" * 64, expected_frontier_root="f" * 64,
        original_wave_identity=wave,
    )
    record = IssuedWorkloadRecord(
        decision_ref=workload.decision_ref,
        source_permission_ref=ExactRef(
            "R136_HARNESS_SOURCE_PERMISSION", "urn:r136:source", "1" * 64,
        ),
        scientific_permission_refs=(ExactRef(
            "R136_HARNESS_SCIENTIFIC_PERMISSION", "urn:r136:science", "2" * 64,
        ),),
        host=HOST, purpose=PURPOSE, source_sha256=bundle.source_sha256,
        envelope_sha256=semantic_hash(workload.envelope()),
        original_u_root=workload.original_u_root,
        expected_frontier_root=workload.expected_frontier_root,
        expected_jobs=(("QUERY", request.query_ref.key, request.predicate_ref.key),),
        currentness="CURRENT_GRANTED", scope="ORIGINAL_SOURCE_GRANTED",
        original_wave_identity=wave,
        native_universe_refs=(bundle.projection.universes[0].ref,),
    )
    return execute_production_workload(
        workload=workload, resolver=Resolver(record),
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE,
    )


def test_R136_wrong_query_authority_source_must_refuse(tmp_path):
    result = _run(tmp_path, qauth_transform=_wrong_query_source)
    assert result.scope != "ORIGINAL_SOURCE_GRANTED", (
        "a PREDICATE_GRAMMAR ALLOW authority with a foreign source sha was "
        "accepted for production query execution"
    )


def test_R136_foreign_descriptor_metadata_must_refuse(tmp_path):
    def foreign_descriptor(descriptor):
        descriptor = dict(descriptor)
        descriptor["source_edition"] = "0" * 64
        descriptor["country_and_population"] = {
            "country": "ZZ", "population": "FOREIGN",
        }
        return descriptor

    result = _run(tmp_path, descriptor_transform=foreign_descriptor)
    assert result.scope != "ORIGINAL_SOURCE_GRANTED", (
        "a descriptor with foreign source/country/population metadata was "
        "accepted for production execution"
    )


def test_R136_actual_positive_value_change_and_restore(tmp_path):
    from rawlsing_next.tests.test_pre553_production_binding import _production

    bundle, workload, record = _production(tmp_path, "0")
    result = execute_production_workload(
        workload=workload, resolver=Resolver(record),
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE,
    )
    assert result.scope == "ORIGINAL_SOURCE_GRANTED"
    assert len(result.output_refs) == 1
    bundle2, workload2, record2 = _production(tmp_path, "1")
    result2 = execute_production_workload(
        workload=workload2, resolver=Resolver(record2),
        source_factory=lambda _ref: bundle2.physical_stream,
        host=HOST, purpose=PURPOSE,
    )
    assert result2.output_refs != result.output_refs
    restored = execute_production_workload(
        workload=workload, resolver=Resolver(record),
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE,
    )
    assert restored.output_refs == result.output_refs
    assert restored.summary == result.summary


def test_R136_foreign_source_authority_snapshot_must_refuse(tmp_path):
    from rawlsing_next.pre553_native_workload_binding import (
        OperationFixture, build_projection_catalog,
    )
    from rawlsing_next.pre553_source_native_preimage_adapter import (
        NativeSourceRule, build_authority_set, materialize_native_preimages,
    )
    from rawlsing_next.tests.test_pre553_production_binding import _harness_authority
    from rawlsing_next.tests.test_universal_source_projection import (
        build_s3, decode_sav, package, repeated_plan, s3_rows, write_rows,
    )

    path = tmp_path / "foreign-authority.sav"
    rows = s3_rows(respondents=6, occasions=2)
    write_rows(path, rows)
    incidence = decode_sav(path)
    pkg = package(path, len(rows), (NativeSourceRule("impl.score", "SCORE"),))
    base = build_authority_set(source=pkg.source, as_of=pkg.as_of)
    tags = ("source", "mapping", "coordinate", "routing", "weight", "replay", "projection")
    harness = tuple(
        _harness_authority(a, tag) for a, tag in zip(base, tags)
    )
    source_auth = harness[0]
    fields = dict(source_auth.semantic_fields)
    fields["scope_envelope"] = {
        **dict(fields["scope_envelope"]), "source_sha256": "0" * 64,
    }
    bad_source_auth = type(source_auth)(
        typed_state="ALLOW",
        authority_snapshot_refs=source_auth.authority_snapshot_refs,
        dependency_refs=source_auth.dependency_refs,
        producer_replay_locator_or_reference_root=(
            source_auth.producer_replay_locator_or_reference_root
        ),
        **fields,
    )
    bundle = materialize_native_preimages(
        package=pkg, incidence=incidence,
        row_occurrence_plan=repeated_plan("SCORE"),
        authorities=(bad_source_auth,) + harness[1:],
    )
    qauth = _query_authority(bundle)
    catalog, request = build_projection_catalog(
        bundle=bundle, operation=OperationFixture(
            "foreign-source-auth", "SCORE", "0",
        ), as_of="2026-10-26", query_authority=qauth,
    )
    wave = OriginalWaveIdentity("SRC135", "R135-HARNESS", "SYNTHETIC", "2026")
    decision = ExactRef("R136_HARNESS_DECISION", "urn:r136:foreign-auth", "d" * 64)
    workload = build_production_query_workload(
        bundle=bundle, catalog=catalog, request=request,
        descriptor=_descriptor(bundle), decision_ref=decision,
        source_factory_ref=ExactRef(
            "SOURCE_FACTORY", "urn:r136:foreign-auth", bundle.source_sha256,
        ), original_u_root="e" * 64, expected_frontier_root="f" * 64,
        original_wave_identity=wave,
    )
    record = IssuedWorkloadRecord(
        decision_ref=workload.decision_ref,
        source_permission_ref=ExactRef("S", "urn:r136:foreign-s", "1" * 64),
        scientific_permission_refs=(ExactRef("Sci", "urn:r136:foreign-sci", "2" * 64),),
        host=HOST, purpose=PURPOSE, source_sha256=bundle.source_sha256,
        envelope_sha256=semantic_hash(workload.envelope()),
        original_u_root=workload.original_u_root,
        expected_frontier_root=workload.expected_frontier_root,
        expected_jobs=(("QUERY", request.query_ref.key, request.predicate_ref.key),),
        currentness="CURRENT_GRANTED", scope="ORIGINAL_SOURCE_GRANTED",
        original_wave_identity=wave,
        native_universe_refs=(bundle.projection.universes[0].ref,),
    )
    result = execute_production_workload(
        workload=workload, resolver=Resolver(record),
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE,
    )
    assert result.scope != "ORIGINAL_SOURCE_GRANTED", (
        "a supplied source authority with a foreign source_sha256 was accepted"
    )


def test_R136_actual_positive_requires_supported_empirical_fact(tmp_path):
    from rawlsing_next.tests.test_pre553_production_binding import _production

    bundle, workload, record = _production(tmp_path, "0")
    result = execute_production_workload(
        workload=workload, resolver=Resolver(record),
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE,
    )
    fact = result.native_outputs[0].facts[0]
    assert fact.typed_state in {"SUPPORTED", "EXACT_SUPPORTED"}, (
        "production positive returned a typed non-positive empirical fact: "
        f"{fact.typed_state}/{fact.semantic_fields.get('p02_failure_state')}"
    )
    assert (fact.semantic_fields.get("raw_denominator_support") or 0) > 0
