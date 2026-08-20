from dataclasses import replace
import hashlib

import pytest

from rawlsing_next.pre553_c11_ingest import SourceReleaseManifest
from rawlsing_next.pre553_c11_integrity import ReplayManifest, authority_snapshot_set_hash
from rawlsing_next.pre553_c11_repository import _make_validated_release
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalUniverse,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.pre553_source_equivalence import (
    BOUND_I03_HEAD,
    CertificationDisposition,
    CertificationExecutionReceipt,
    CertificationRequest,
    DimensionState,
    ReplayEquivalenceEvidence,
    SourceEquivalenceIntegrityError,
    SourceNativeIdentity,
    certification_is_replay_stable,
    certify_source_to_c11,
    make_dimension_evidence,
    make_frontier_replay_evidence,
    sha256_bytes,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _root(tag: str) -> ExactRef:
    return _ref("REPLAY_ROOT", tag)


def _authority(tag: str, kind: str, *, families=("EmpiricalUniverse@1.0.0",)) -> AuthoritySnapshot:
    content_hash = _h(f"authority:{tag}:1.0.0")
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root(f"authority-{tag}"),
        authority_id=f"AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=content_hash,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=(f"OP-{tag}",),
        governed_object_families=families,
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", tag),
    )


def _fixture():
    source_bytes = b"exact-source-release-bytes-v1"
    artifact_id = "urn:test:source:release-a"
    artifact_hash = sha256_bytes(source_bytes)
    retention_ref = ExactRef(
        "SOURCE_SNAPSHOT",
        "urn:test:source-snapshot:release-a",
        artifact_hash,
    )
    source_auth = _authority("source", "SOURCE_SEMANTICS_TOPOLOGY")
    replay_auth = _authority("replay", "REPLAY_PROTOCOL", families=("ReplayReceipt@1.0.0",))

    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root("universe-a"),
        raw_source_identity="RAW-SOURCE-A",
        source_family="SOURCE-A",
        study_product_release="STUDY-A/RELEASE-A",
        instrument_release="INSTRUMENT-A",
        country_geography="US",
        sampling_geography="US-NATIONAL",
        raw_wave="W1",
        canonical_wave_if_governed="W1",
        field_or_reference_time="2026-01",
        target_population_and_sample_frame="ADULTS",
        sampling_design_regime="DESIGN-A",
        respondent_namespace="SOURCE-A/RELEASE-A",
        source_artifact_import_lineage={
            "source_artifact_id": artifact_id,
            "source_artifact_content_hash": artifact_hash,
        },
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    manifest = SourceReleaseManifest(
        source_artifact_id=artifact_id,
        source_artifact_content_hash=artifact_hash,
        source_family_id="SOURCE-A",
        study_product_id="STUDY-A",
        release_id="RELEASE-A",
        instrument_release_id="INSTRUMENT-A",
        ingest_contract_version="PRE553_C11_INGEST@1.0.0",
        declared_universe_refs=(universe.ref,),
        declared_authority_snapshot_refs=(source_auth.authority_ref, replay_auth.authority_ref),
        declared_record_counts_by_logical_family={
            "EmpiricalUniverse": 1,
            "AuthoritySnapshot": 2,
            "ReplayManifest": 1,
        },
        source_snapshot_retention_ref=retention_ref,
    )
    authorities = (source_auth, replay_auth)
    authority_set_hash = authority_snapshot_set_hash(authorities)
    replay_manifest = ReplayManifest(
        frontier_version="D13_C11_M01_M18@1.0.0",
        authority_snapshot_set_hash=authority_set_hash,
        source_substrate_content_refs=(manifest.source_artifact_ref,),
        semantic_projection_id="PRE553_C11_LOGICAL_RELEASE_PROJECTION@1.0.0",
        semantic_projection_hash=_h("release-projection"),
        deterministic_tie_order_rules_ref=_ref("TIE_ORDER_RULE", "v1"),
        replay_protocol_version="D13B-REPLAY-PROOF-CONTRACT-v1",
        replay_protocol_authority_ref=replay_auth.authority_ref,
        closure_refs=tuple(sorted((
            manifest.source_artifact_ref,
            retention_ref,
            universe.ref,
            source_auth.ref,
            replay_auth.ref,
        ), key=lambda ref: ref.key)),
    )
    coverage = {f"M{i:02d}": ("fixture-evidence",) for i in range(1, 19)}
    release = _make_validated_release(
        release_id=manifest.release_id,
        source_artifact_ref=manifest.source_artifact_ref,
        source_release_manifest_hash=manifest.content_hash,
        semantic_release_hash=_h("c11-release-a"),
        replay_manifest=replay_manifest,
        public_objects=tuple(sorted((source_auth, replay_auth, universe), key=lambda obj: obj.ref.key)),
        internal_records=(),
        m01_m18_coverage=coverage,
    )
    source_projection = {
        "source_artifact_ref": manifest.source_artifact_ref.as_dict(),
        "source_family_id": manifest.source_family_id,
        "study_product_id": manifest.study_product_id,
        "release_id": manifest.release_id,
        "instrument_release_id": manifest.instrument_release_id,
        "source_universe_ref": universe.ref.as_dict(),
        "source_snapshot_retention_ref": retention_ref.as_dict(),
        "native_semantics": {
            "topology": "EXACT_SOURCE_NATIVE",
            "routing": "EXACT_SOURCE_NATIVE",
            "weights": "EXACT_OR_TYPED_ABSENCE",
        },
    }
    native = SourceNativeIdentity(
        source_artifact_ref=manifest.source_artifact_ref,
        source_family_id=manifest.source_family_id,
        study_product_id=manifest.study_product_id,
        release_id=manifest.release_id,
        instrument_release_id=manifest.instrument_release_id,
        source_universe_ref=universe.ref,
        source_snapshot_retention_ref=retention_ref,
        semantic_projection_id="SOURCE_NATIVE_RELEASE_PROJECTION@1.0.0",
        semantic_projection_hash=semantic_hash(source_projection),
    )
    dimensions = tuple(
        make_dimension_evidence(
            proof_id=f"P{i:02d}",
            state=DimensionState.PASS,
            source_projection={"proof_id": f"P{i:02d}", "semantic": "same"},
            c11_projection={"proof_id": f"P{i:02d}", "semantic": "same"},
            authority_closure={
                "authority_snapshot_set_hash": authority_set_hash,
                "proof_id": f"P{i:02d}",
            },
            evidence_material={"fixture": f"P{i:02d}", "exact_members": [1, 2, 3]},
            reason="exact source-native and C11 projections agree",
        )
        for i in range(1, 21)
    )
    frontier = tuple(
        make_frontier_replay_evidence(
            test_id=f"T{i:02d}",
            state=DimensionState.PASS,
            query_or_fixture={"test_id": f"T{i:02d}", "frontier": "D12-D13"},
            source_result={"test_id": f"T{i:02d}", "semantic_result": "same"},
            c11_result={"test_id": f"T{i:02d}", "semantic_result": "same"},
            authority_closure={"authority_snapshot_set_hash": authority_set_hash},
            evidence_material={"test_id": f"T{i:02d}", "exact_replay": True},
            reason="mandatory D12/D13 replay fixture matches exactly",
        )
        for i in range(1, 19)
    )
    source_root = _h("source-native-replay-root")
    c11_root = replay_manifest.content_hash
    run = _h("replay-semantic-result")
    replay = ReplayEquivalenceEvidence(
        source_replay_root_hash=source_root,
        c11_replay_root_hash=c11_root,
        source_run_semantic_hashes=(run, run),
        c11_run_semantic_hashes=(run, run),
        replay_authority_hash=replay_auth.authority_content_hash,
        deterministic=True,
    )
    execution = CertificationExecutionReceipt(
        git_head=BOUND_I03_HEAD,
        source_artifact_ref=manifest.source_artifact_ref,
        c11_release_ref=release.release_ref,
        source_universe_ref=universe.ref,
        source_snapshot_retention_ref=retention_ref,
        ingest_authority_hash=_h("ingest-authority"),
        query_authority_hash=_h("query-authority"),
        code_config_hashes={
            "CERTIFIER_RUNTIME": _h("certifier-runtime"),
            "I02_INGEST_RUNTIME": _h("i02-ingest-runtime"),
            "I03_QUERY_RUNTIME": _h("i03-query-runtime"),
            "P05_PROTOCOL": _h("p05-protocol"),
        },
        typed_state_counts={
            "SUBSTANTIVE_RESPONSE": 2,
            "OBSERVED_COORDINATE": 1,
            "NOT_ASKED": 0,
            "WEIGHT_MISSING": 0,
        },
        validation_state=DimensionState.PASS,
        validation_output_hash=_h("validation-output"),
        output_bundle_hash=_h("output-bundle"),
        source_replay_root_hash=source_root,
        c11_replay_root_hash=c11_root,
        clean_worktree_before=True,
        clean_worktree_after=True,
        unauthorized_default_count=0,
        unauthorized_coercion_count=0,
        fuzzy_mapping_count=0,
        unproved_source_pooling_count=0,
        source_snapshot_retained=True,
    )
    request = CertificationRequest(
        source_bytes=source_bytes,
        source_manifest=manifest,
        source_native_identity=native,
        source_semantic_projection=source_projection,
        c11_release=release,
        dimension_evidence=dimensions,
        frontier_replay_evidence=frontier,
        replay_evidence=replay,
        execution_receipt=execution,
        authority_snapshot_set_hash=authority_set_hash,
        source_universe_identity_hash=semantic_hash(universe.ref.as_dict()),
    )
    return request


def _replace_dimension(request, proof_id, *, state, source=None, c11=None, reason="hostile"):
    values = []
    state = DimensionState(state)
    for item in request.dimension_evidence:
        if item.proof_id != proof_id:
            values.append(item)
            continue
        if state is DimensionState.PASS:
            source = source if source is not None else {"proof_id": proof_id, "semantic": "same"}
            c11 = c11 if c11 is not None else source
            values.append(
                make_dimension_evidence(
                    proof_id=proof_id,
                    state=state,
                    source_projection=source,
                    c11_projection=c11,
                    authority_closure={"authority": proof_id},
                    evidence_material={"fixture": proof_id},
                    reason=reason,
                )
            )
        elif state is DimensionState.NOT_APPLICABLE:
            values.append(
                make_dimension_evidence(
                    proof_id=proof_id,
                    state=state,
                    source_projection=None,
                    c11_projection=None,
                    authority_closure=None,
                    evidence_material={"fixture": proof_id},
                    reason=reason,
                    applicable=False,
                )
            )
        else:
            values.append(
                make_dimension_evidence(
                    proof_id=proof_id,
                    state=state,
                    source_projection=source,
                    c11_projection=c11,
                    authority_closure={"authority": proof_id} if state is DimensionState.FAIL else None,
                    evidence_material={"fixture": proof_id},
                    reason=reason,
                )
            )
    return replace(request, dimension_evidence=tuple(values))


def _replace_frontier(request, test_id, *, state, source=None, c11=None, reason="hostile"):
    values = []
    state = DimensionState(state)
    for item in request.frontier_replay_evidence:
        if item.test_id != test_id:
            values.append(item)
            continue
        source = source if source is not None else ({"test": test_id, "semantic": "same"} if state is DimensionState.PASS else None)
        c11 = c11 if c11 is not None else source
        values.append(
            make_frontier_replay_evidence(
                test_id=test_id,
                state=state,
                query_or_fixture={"test": test_id, "fixture": "exact"},
                source_result=source,
                c11_result=c11,
                authority_closure={"authority": test_id} if state is not DimensionState.BLOCKED else None,
                evidence_material={"test": test_id},
                reason=reason,
            )
        )
    return replace(request, frontier_replay_evidence=tuple(values))


def test_complete_p01_p20_t01_t18_exact_bytes_execution_and_replay_certify():
    result = certify_source_to_c11(_fixture())
    assert result.disposition is CertificationDisposition.CERTIFIED
    assert result.certified is True
    assert len(result.dimension_states) == 20
    assert len(result.frontier_test_states) == 18
    assert result.failed_dimensions == ()
    assert result.blocked_dimensions == ()
    assert result.failed_frontier_tests == ()
    assert result.blocked_frontier_tests == ()
    assert result.source_snapshot_retention_required is True
    assert result.source_retirement_authorized is False
    assert result.source_pooling_authorized is False
    assert result.structural_promotion_authorized is False
    assert result.cutover_authorized is False
    assert result.actor_or_v3_semantics_authorized is False
    assert result.result_ref.kind == "SourceToC11EquivalenceCertification"


def test_source_bytes_mismatch_fails_even_when_every_semantic_test_is_green():
    result = certify_source_to_c11(replace(_fixture(), source_bytes=b"different-source-bytes"))
    assert result.disposition is CertificationDisposition.FAILED
    assert "SOURCE_ARTIFACT_BYTES_HASH_MISMATCH" in result.reasons


def test_source_semantic_projection_hash_is_recomputed_not_trusted():
    request = replace(_fixture(), source_semantic_projection={"tampered": True})
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.FAILED
    assert "SOURCE_NATIVE_SEMANTIC_PROJECTION_HASH_MISMATCH" in result.reasons


@pytest.mark.parametrize("proof_id", [f"P{i:02d}" for i in range(1, 21)])
def test_every_p01_p20_observed_mismatch_fails(proof_id):
    request = _replace_dimension(
        _fixture(),
        proof_id,
        state=DimensionState.FAIL,
        source={"side": "source", "proof": proof_id},
        c11={"side": "c11", "proof": proof_id},
        reason="observed semantic mismatch",
    )
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.FAILED
    assert proof_id in result.failed_dimensions


def test_mandatory_dimension_not_applicable_is_blocked_not_certified():
    request = _fixture()
    for proof_id in [f"P{i:02d}" for i in range(1, 21)]:
        request = _replace_dimension(
            request,
            proof_id,
            state=DimensionState.NOT_APPLICABLE,
            reason="hostile attempt to erase full-frontier burden",
        )
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.BLOCKED
    assert result.certified is False
    assert result.blocked_dimensions == tuple(f"P{i:02d}" for i in range(1, 21))


def test_blocked_dimension_blocks_without_guessing():
    request = _replace_dimension(
        _fixture(),
        "P09",
        state=DimensionState.BLOCKED,
        source=None,
        c11=None,
        reason="weight design/estimand authority unavailable",
    )
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.BLOCKED
    assert result.blocked_dimensions == ("P09",)


def test_observed_failure_outranks_blocked_dimension():
    request = _replace_dimension(_fixture(), "P03", state=DimensionState.BLOCKED, reason="topology unresolved")
    request = _replace_dimension(
        request,
        "P01",
        state=DimensionState.FAIL,
        source={"ids": ["a"]},
        c11={"ids": ["b"]},
        reason="respondent incidence mismatch",
    )
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.FAILED
    assert result.failed_dimensions == ("P01",)
    assert result.blocked_dimensions == ("P03",)


def test_pass_cannot_hide_different_source_and_c11_projection():
    with pytest.raises(SourceEquivalenceIntegrityError):
        make_dimension_evidence(
            proof_id="P03",
            state=DimensionState.PASS,
            source_projection={"topology": "MULTISELECT"},
            c11_projection={"topology": "SCALAR"},
            authority_closure={"authority": "topology"},
            evidence_material={"fixture": "mismatch"},
            reason="illegal green claim",
        )


@pytest.mark.parametrize("test_id", [f"T{i:02d}" for i in range(1, 19)])
def test_every_t01_t18_observed_mismatch_fails(test_id):
    request = _replace_frontier(
        _fixture(),
        test_id,
        state=DimensionState.FAIL,
        source={"side": "source", "test": test_id},
        c11={"side": "c11", "test": test_id},
        reason="frontier replay mismatch",
    )
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.FAILED
    assert test_id in result.failed_frontier_tests


def test_blocked_frontier_fixture_blocks_certification():
    request = _replace_frontier(
        _fixture(), "T15", state=DimensionState.BLOCKED, reason="source-native fixture unresolved"
    )
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.BLOCKED
    assert result.blocked_frontier_tests == ("T15",)


def test_missing_one_t01_t18_fixture_is_integrity_error():
    request = _fixture()
    request = replace(request, frontier_replay_evidence=request.frontier_replay_evidence[:-1])
    with pytest.raises(SourceEquivalenceIntegrityError):
        certify_source_to_c11(request)


def test_frontier_pass_cannot_hide_different_semantic_results():
    with pytest.raises(SourceEquivalenceIntegrityError):
        make_frontier_replay_evidence(
            test_id="T06",
            state=DimensionState.PASS,
            query_or_fixture={"query": "XOR"},
            source_result={"xor": True},
            c11_result={"xor": False},
            authority_closure={"authority": "exact-query"},
            evidence_material={"fixture": "xor"},
            reason="illegal green frontier claim",
        )


@pytest.mark.parametrize(
    "shortcut",
    [
        "schema parity only",
        "ROW_COUNT_PARITY_ONLY",
        "respondent count parity only",
        "aggregate parity only",
        "selected query parity only",
        "spot check only",
        "marginal summary parity only",
        "serialized file hash only",
        "schema hash only",
        "canonical label equality only",
    ],
)
def test_non_certifying_shortcuts_are_rejected_at_request_boundary(shortcut):
    with pytest.raises(SourceEquivalenceIntegrityError):
        replace(_fixture(), requested_claim_basis=(shortcut,))


@pytest.mark.parametrize(
    "authorization",
    [
        "source retirement",
        "SOURCE_POOLING",
        "structural promotion",
        "cutover",
        "actor semantics",
        "v3 semantics",
    ],
)
def test_certification_api_cannot_grant_forbidden_downstream_authority(authorization):
    with pytest.raises(SourceEquivalenceIntegrityError):
        replace(_fixture(), requested_authorizations=(authorization,))


def test_result_type_itself_cannot_be_mutated_into_pooling_authority():
    result = certify_source_to_c11(_fixture())
    with pytest.raises(SourceEquivalenceIntegrityError):
        replace(result, source_pooling_authorized=True)


def test_missing_one_p01_p20_dimension_is_integrity_error_not_certification():
    request = _fixture()
    request = replace(request, dimension_evidence=request.dimension_evidence[:-1])
    with pytest.raises(SourceEquivalenceIntegrityError):
        certify_source_to_c11(request)


def test_duplicate_dimension_is_integrity_error():
    request = _fixture()
    request = replace(request, dimension_evidence=request.dimension_evidence + (request.dimension_evidence[0],))
    with pytest.raises(SourceEquivalenceIntegrityError):
        certify_source_to_c11(request)


def test_missing_c11_m01_m18_information_closure_fails():
    request = _fixture()
    coverage = dict(request.c11_release.m01_m18_coverage)
    coverage["M12"] = ()
    bad_release = _make_validated_release(
        release_id=request.c11_release.release_id,
        source_artifact_ref=request.c11_release.source_artifact_ref,
        source_release_manifest_hash=request.c11_release.source_release_manifest_hash,
        semantic_release_hash=request.c11_release.semantic_release_hash,
        replay_manifest=request.c11_release.replay_manifest,
        public_objects=request.c11_release.public_objects,
        internal_records=request.c11_release.internal_records,
        m01_m18_coverage=coverage,
    )
    bad_execution = replace(request.execution_receipt, c11_release_ref=bad_release.release_ref)
    result = certify_source_to_c11(replace(request, c11_release=bad_release, execution_receipt=bad_execution))
    assert result.disposition is CertificationDisposition.FAILED
    assert "C11_M12_INFORMATION_CLOSURE_MISSING" in result.reasons


def test_source_release_manifest_binding_mismatch_fails():
    request = _fixture()
    bad_release = _make_validated_release(
        release_id=request.c11_release.release_id,
        source_artifact_ref=request.c11_release.source_artifact_ref,
        source_release_manifest_hash=_h("different-manifest"),
        semantic_release_hash=request.c11_release.semantic_release_hash,
        replay_manifest=request.c11_release.replay_manifest,
        public_objects=request.c11_release.public_objects,
        internal_records=request.c11_release.internal_records,
        m01_m18_coverage=request.c11_release.m01_m18_coverage,
    )
    bad_execution = replace(request.execution_receipt, c11_release_ref=bad_release.release_ref)
    result = certify_source_to_c11(replace(request, c11_release=bad_release, execution_receipt=bad_execution))
    assert result.disposition is CertificationDisposition.FAILED
    assert "C11_SOURCE_RELEASE_MANIFEST_HASH_MISMATCH" in result.reasons


def test_source_universe_must_be_declared_and_present_in_actual_c11_release():
    request = _fixture()
    public_without_universe = tuple(
        obj for obj in request.c11_release.public_objects if not isinstance(obj, EmpiricalUniverse)
    )
    bad_release = _make_validated_release(
        release_id=request.c11_release.release_id,
        source_artifact_ref=request.c11_release.source_artifact_ref,
        source_release_manifest_hash=request.c11_release.source_release_manifest_hash,
        semantic_release_hash=request.c11_release.semantic_release_hash,
        replay_manifest=request.c11_release.replay_manifest,
        public_objects=public_without_universe,
        internal_records=request.c11_release.internal_records,
        m01_m18_coverage=request.c11_release.m01_m18_coverage,
    )
    bad_execution = replace(request.execution_receipt, c11_release_ref=bad_release.release_ref)
    result = certify_source_to_c11(replace(request, c11_release=bad_release, execution_receipt=bad_execution))
    assert result.disposition is CertificationDisposition.FAILED
    assert "SOURCE_UNIVERSE_NOT_PRESENT_IN_C11_RELEASE" in result.reasons


def test_source_universe_identity_hash_mismatch_fails():
    result = certify_source_to_c11(replace(_fixture(), source_universe_identity_hash=_h("wrong-universe")))
    assert result.disposition is CertificationDisposition.FAILED
    assert "SOURCE_UNIVERSE_IDENTITY_HASH_MISMATCH" in result.reasons


def test_authority_set_is_recomputed_from_actual_c11_objects_not_request_claim():
    request = _fixture()
    public_without_replay_authority = tuple(
        obj for obj in request.c11_release.public_objects
        if not (isinstance(obj, AuthoritySnapshot) and obj.authority_kind == "REPLAY_PROTOCOL")
    )
    bad_release = _make_validated_release(
        release_id=request.c11_release.release_id,
        source_artifact_ref=request.c11_release.source_artifact_ref,
        source_release_manifest_hash=request.c11_release.source_release_manifest_hash,
        semantic_release_hash=request.c11_release.semantic_release_hash,
        replay_manifest=request.c11_release.replay_manifest,
        public_objects=public_without_replay_authority,
        internal_records=request.c11_release.internal_records,
        m01_m18_coverage=request.c11_release.m01_m18_coverage,
    )
    bad_execution = replace(request.execution_receipt, c11_release_ref=bad_release.release_ref)
    result = certify_source_to_c11(replace(request, c11_release=bad_release, execution_receipt=bad_execution))
    assert result.disposition is CertificationDisposition.FAILED
    assert "AUTHORITY_SNAPSHOT_SET_HASH_MISMATCH" in result.reasons
    assert "SOURCE_MANIFEST_C11_AUTHORITY_SET_MISMATCH" in result.reasons


def test_replay_authority_hash_must_bind_sealed_c11_replay_authority():
    request = _fixture()
    replay = replace(request.replay_evidence, replay_authority_hash=_h("wrong-replay-authority"))
    result = certify_source_to_c11(replace(request, replay_evidence=replay))
    assert result.disposition is CertificationDisposition.FAILED
    assert "REPLAY_AUTHORITY_HASH_MISMATCH" in result.reasons


def test_c11_replay_root_must_be_actual_sealed_replay_manifest_identity():
    request = _fixture()
    wrong_root = _h("wrong-c11-root")
    replay = replace(request.replay_evidence, c11_replay_root_hash=wrong_root)
    execution = replace(request.execution_receipt, c11_replay_root_hash=wrong_root)
    result = certify_source_to_c11(replace(request, replay_evidence=replay, execution_receipt=execution))
    assert result.disposition is CertificationDisposition.FAILED
    assert "C11_REPLAY_ROOT_NOT_BOUND_TO_SEALED_REPLAY_MANIFEST" in result.reasons


def test_nondeterministic_or_semantically_divergent_replay_fails():
    request = _fixture()
    replay = ReplayEquivalenceEvidence(
        source_replay_root_hash=request.replay_evidence.source_replay_root_hash,
        c11_replay_root_hash=request.replay_evidence.c11_replay_root_hash,
        source_run_semantic_hashes=(_h("source-run-a"), _h("source-run-b")),
        c11_run_semantic_hashes=(_h("c11-run"), _h("c11-run")),
        replay_authority_hash=request.replay_evidence.replay_authority_hash,
        deterministic=False,
    )
    result = certify_source_to_c11(replace(request, replay_evidence=replay))
    assert result.disposition is CertificationDisposition.FAILED
    assert "REPLAY_NONDETERMINISTIC" in result.reasons
    assert "SOURCE_REPEATED_REPLAY_SEMANTIC_HASH_MISMATCH" in result.reasons
    assert "SOURCE_C11_REPLAY_SEMANTIC_RESULT_MISMATCH" in result.reasons


def test_execution_receipt_dirty_worktree_fails():
    request = _fixture()
    execution = replace(request.execution_receipt, clean_worktree_after=False)
    result = certify_source_to_c11(replace(request, execution_receipt=execution))
    assert result.disposition is CertificationDisposition.FAILED
    assert "EXECUTION_WORKTREE_NOT_CLEAN_AFTER" in result.reasons


@pytest.mark.parametrize(
    "field,reason",
    [
        ("unauthorized_default_count", "UNAUTHORIZED_DEFAULT_COUNT_NONZERO"),
        ("unauthorized_coercion_count", "UNAUTHORIZED_COERCION_COUNT_NONZERO"),
        ("fuzzy_mapping_count", "FUZZY_MAPPING_COUNT_NONZERO"),
        ("unproved_source_pooling_count", "UNPROVED_SOURCE_POOLING_COUNT_NONZERO"),
    ],
)
def test_execution_receipt_nonzero_forbidden_transformation_count_fails(field, reason):
    request = _fixture()
    execution = replace(request.execution_receipt, **{field: 1})
    result = certify_source_to_c11(replace(request, execution_receipt=execution))
    assert result.disposition is CertificationDisposition.FAILED
    assert reason in result.reasons


def test_execution_receipt_blocked_validation_blocks_certification():
    request = _fixture()
    execution = replace(request.execution_receipt, validation_state=DimensionState.BLOCKED)
    result = certify_source_to_c11(replace(request, execution_receipt=execution))
    assert result.disposition is CertificationDisposition.BLOCKED
    assert "POPULATED_VALIDATION_BLOCKED" in result.reasons


def test_source_snapshot_must_remain_retained_even_after_positive_equivalence():
    request = _fixture()
    execution = replace(request.execution_receipt, source_snapshot_retained=False)
    result = certify_source_to_c11(replace(request, execution_receipt=execution))
    assert result.disposition is CertificationDisposition.FAILED
    assert "SOURCE_SNAPSHOT_NOT_RETAINED" in result.reasons


def test_matching_counts_do_not_rescue_respondent_identity_failure():
    request = _replace_dimension(
        _fixture(),
        "P01",
        state=DimensionState.FAIL,
        source={"respondent_count": 2, "ids": ["a", "b"]},
        c11={"respondent_count": 2, "ids": ["c", "d"]},
        reason="same count, different exact scoped respondent set",
    )
    assert certify_source_to_c11(request).disposition is CertificationDisposition.FAILED


def test_matching_marginals_do_not_rescue_joint_topology_failure():
    request = _replace_dimension(
        _fixture(),
        "P15",
        state=DimensionState.FAIL,
        source={"marginals": [5, 5], "joint": [[5, 0], [0, 5]]},
        c11={"marginals": [5, 5], "joint": [[0, 5], [5, 0]]},
        reason="same marginals, different same-respondent joint incidence",
    )
    assert certify_source_to_c11(request).disposition is CertificationDisposition.FAILED


def test_missing_weight_is_blocked_not_defaulted_to_one():
    request = _replace_dimension(
        _fixture(),
        "P09",
        state=DimensionState.BLOCKED,
        source={"weight_state": "WEIGHT_BASIS_UNRESOLVED"},
        c11={"weight_state": "WEIGHT_BASIS_UNRESOLVED"},
        reason="missing exact design/estimand authority; no 1.0 repair",
    )
    assert certify_source_to_c11(request).disposition is CertificationDisposition.BLOCKED


def test_order_sensitive_rank_loss_fails_even_when_event_values_match():
    request = _replace_dimension(
        _fixture(),
        "P20",
        state=DimensionState.FAIL,
        source={"values": ["A", "B"], "rank": [1, 2]},
        c11={"values": ["A", "B"], "rank": None},
        reason="semantic rank lost",
    )
    assert certify_source_to_c11(request).disposition is CertificationDisposition.FAILED


def test_exact_same_complete_request_replays_same_certification_identity():
    request = _fixture()
    first = certify_source_to_c11(request)
    second = certify_source_to_c11(request)
    assert first == second
    assert certification_is_replay_stable(first, second)


def test_physical_evidence_order_is_semantically_stable():
    request = _fixture()
    first = certify_source_to_c11(request)
    second = certify_source_to_c11(
        replace(
            request,
            dimension_evidence=tuple(reversed(request.dimension_evidence)),
            frontier_replay_evidence=tuple(reversed(request.frontier_replay_evidence)),
        )
    )
    assert certification_is_replay_stable(first, second)
