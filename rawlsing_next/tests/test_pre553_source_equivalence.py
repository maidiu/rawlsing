from dataclasses import replace
import hashlib

import pytest

from rawlsing_next.pre553_c11_ingest import SourceReleaseManifest
from rawlsing_next.pre553_c11_integrity import ReplayManifest
from rawlsing_next.pre553_c11_repository import _make_validated_release
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next.pre553_source_equivalence import (
    CertificationDisposition,
    CertificationRequest,
    DimensionState,
    ReplayEquivalenceEvidence,
    SourceEquivalenceIntegrityError,
    SourceNativeIdentity,
    certification_is_replay_stable,
    certify_source_to_c11,
    make_dimension_evidence,
    sha256_bytes,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", "1.0.0", _h(f"authority:{tag}"))


def _fixture():
    source_bytes = b"exact-source-release-bytes-v1"
    artifact_id = "urn:test:source:release-a"
    artifact_hash = sha256_bytes(source_bytes)
    universe_ref = _ref("EmpiricalUniverse", "u1")
    retention_ref = _ref("SOURCE_SNAPSHOT_RETENTION", "release-a")
    auth = _auth("source")
    manifest = SourceReleaseManifest(
        source_artifact_id=artifact_id,
        source_artifact_content_hash=artifact_hash,
        source_family_id="SOURCE-A",
        study_product_id="STUDY-A",
        release_id="RELEASE-A",
        instrument_release_id="INSTRUMENT-A",
        ingest_contract_version="PRE553_C11_INGEST@1.0.0",
        declared_universe_refs=(universe_ref,),
        declared_authority_snapshot_refs=(auth,),
        declared_record_counts_by_logical_family={},
        source_snapshot_retention_ref=retention_ref,
    )
    authority_set_hash = _h("authority-set")
    replay_manifest = ReplayManifest(
        frontier_version="D13_C11_M01_M18@1.0.0",
        authority_snapshot_set_hash=authority_set_hash,
        source_substrate_content_refs=(manifest.source_artifact_ref,),
        semantic_projection_id="PRE553_C11_LOGICAL_RELEASE_PROJECTION@1.0.0",
        semantic_projection_hash=_h("release-projection"),
        deterministic_tie_order_rules_ref=_ref("TIE_ORDER_RULE", "v1"),
        replay_protocol_version="D13B-REPLAY-PROOF-CONTRACT-v1",
        replay_protocol_authority_ref=_auth("replay"),
        closure_refs=(manifest.source_artifact_ref, retention_ref, universe_ref),
    )
    coverage = {f"M{i:02d}": ("fixture-evidence",) for i in range(1, 19)}
    release = _make_validated_release(
        release_id="C11-RELEASE-A",
        source_artifact_ref=manifest.source_artifact_ref,
        source_release_manifest_hash=manifest.content_hash,
        semantic_release_hash=_h("c11-release-a"),
        replay_manifest=replay_manifest,
        public_objects=(),
        internal_records=(),
        m01_m18_coverage=coverage,
    )
    native = SourceNativeIdentity(
        source_artifact_ref=manifest.source_artifact_ref,
        source_family_id=manifest.source_family_id,
        study_product_id=manifest.study_product_id,
        release_id=manifest.release_id,
        instrument_release_id=manifest.instrument_release_id,
        source_universe_ref=universe_ref,
        source_snapshot_retention_ref=retention_ref,
        semantic_projection_id="SOURCE_NATIVE_RELEASE_PROJECTION@1.0.0",
        semantic_projection_hash=_h("source-native-projection"),
    )
    dimensions = tuple(
        make_dimension_evidence(
            proof_id=f"P{i:02d}",
            state=DimensionState.PASS,
            source_projection={"proof_id": f"P{i:02d}", "semantic": "same"},
            c11_projection={"proof_id": f"P{i:02d}", "semantic": "same"},
            authority_closure={"authority": f"P{i:02d}"},
            evidence_material={"fixture": f"P{i:02d}", "rows": [1, 2, 3]},
            reason="exact source-native and C11 projections agree",
        )
        for i in range(1, 21)
    )
    root = _h("replay-root")
    run = _h("replay-result")
    replay = ReplayEquivalenceEvidence(
        source_replay_root_hash=root,
        c11_replay_root_hash=root,
        repeated_run_semantic_hashes=(run, run),
        replay_authority_hash=_h("replay-authority"),
        deterministic=True,
    )
    request = CertificationRequest(
        source_bytes=source_bytes,
        source_manifest=manifest,
        source_native_identity=native,
        c11_release=release,
        dimension_evidence=dimensions,
        replay_evidence=replay,
        authority_snapshot_set_hash=authority_set_hash,
        source_universe_identity_hash=semantic_hash(universe_ref.as_dict()),
    )
    return request


def _replace_dimension(request, proof_id, *, state, source=None, c11=None, reason="hostile"):
    values = []
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


def test_all_twenty_dimensions_exact_bytes_and_replay_certify():
    request = _fixture()
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.CERTIFIED
    assert result.certified is True
    assert len(result.dimension_states) == 20
    assert result.failed_dimensions == ()
    assert result.blocked_dimensions == ()
    assert result.source_snapshot_retention_required is True
    assert result.source_retirement_authorized is False
    assert result.source_pooling_authorized is False
    assert result.structural_promotion_authorized is False
    assert result.cutover_authorized is False
    assert result.actor_or_v3_semantics_authorized is False
    assert result.result_ref.kind == "SourceToC11EquivalenceCertification"


def test_source_bytes_mismatch_fails_even_if_schema_counts_and_dimensions_look_green():
    request = replace(_fixture(), source_bytes=b"different-source-bytes")
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.FAILED
    assert "SOURCE_ARTIFACT_BYTES_HASH_MISMATCH" in result.reasons


@pytest.mark.parametrize(
    "proof_id",
    ["P01", "P02", "P03", "P04", "P05", "P06", "P08", "P09", "P10", "P15", "P16", "P18", "P19", "P20"],
)
def test_hostile_mandatory_dimension_mismatch_fails(proof_id):
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
    assert result.certified is False
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


@pytest.mark.parametrize(
    "shortcut",
    [
        "SCHEMA_PARITY_ONLY",
        "ROW_COUNT_PARITY_ONLY",
        "RESPONDENT_COUNT_PARITY_ONLY",
        "AGGREGATE_PARITY_ONLY",
        "SELECTED_QUERY_PARITY_ONLY",
        "SPOT_CHECK_ONLY",
        "MARGINAL_SUMMARY_PARITY_ONLY",
        "SERIALIZED_FILE_HASH_ONLY",
        "SCHEMA_HASH_ONLY",
        "CANONICAL_LABEL_EQUALITY_ONLY",
    ],
)
def test_non_certifying_shortcuts_are_rejected_at_request_boundary(shortcut):
    with pytest.raises(SourceEquivalenceIntegrityError):
        replace(_fixture(), requested_claim_basis=(shortcut,))


@pytest.mark.parametrize(
    "authorization",
    [
        "SOURCE_RETIREMENT",
        "SOURCE_POOLING",
        "STRUCTURAL_PROMOTION",
        "CUTOVER",
        "ACTOR_SEMANTICS",
        "V3_SEMANTICS",
    ],
)
def test_certification_api_cannot_grant_forbidden_downstream_authority(authorization):
    with pytest.raises(SourceEquivalenceIntegrityError):
        replace(_fixture(), requested_authorizations=(authorization,))


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
    result = certify_source_to_c11(replace(request, c11_release=bad_release))
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
    result = certify_source_to_c11(replace(request, c11_release=bad_release))
    assert result.disposition is CertificationDisposition.FAILED
    assert "C11_SOURCE_RELEASE_MANIFEST_HASH_MISMATCH" in result.reasons


def test_source_universe_identity_mismatch_fails():
    request = replace(_fixture(), source_universe_identity_hash=_h("wrong-universe"))
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.FAILED
    assert "SOURCE_UNIVERSE_IDENTITY_HASH_MISMATCH" in result.reasons


def test_authority_snapshot_set_mismatch_fails():
    request = replace(_fixture(), authority_snapshot_set_hash=_h("wrong-authority-set"))
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.FAILED
    assert "AUTHORITY_SNAPSHOT_SET_HASH_MISMATCH" in result.reasons


def test_nondeterministic_replay_fails():
    request = _fixture()
    replay = ReplayEquivalenceEvidence(
        source_replay_root_hash=_h("source-root"),
        c11_replay_root_hash=_h("c11-root"),
        repeated_run_semantic_hashes=(_h("run-a"), _h("run-b")),
        replay_authority_hash=_h("replay-authority"),
        deterministic=False,
    )
    result = certify_source_to_c11(replace(request, replay_evidence=replay))
    assert result.disposition is CertificationDisposition.FAILED
    assert "REPLAY_ROOT_MISMATCH" in result.reasons
    assert "REPLAY_NONDETERMINISTIC" in result.reasons


def test_matching_counts_do_not_rescue_respondent_identity_failure():
    request = _replace_dimension(
        _fixture(),
        "P01",
        state=DimensionState.FAIL,
        source={"respondent_count": 2, "ids": ["a", "b"]},
        c11={"respondent_count": 2, "ids": ["c", "d"]},
        reason="same count, different exact scoped respondent set",
    )
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.FAILED


def test_matching_marginals_do_not_rescue_joint_topology_failure():
    request = _replace_dimension(
        _fixture(),
        "P15",
        state=DimensionState.FAIL,
        source={"marginals": [5, 5], "joint": [[5, 0], [0, 5]]},
        c11={"marginals": [5, 5], "joint": [[0, 5], [5, 0]]},
        reason="same marginals, different same-respondent joint incidence",
    )
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.FAILED


def test_missing_weight_is_blocked_not_defaulted_to_one():
    request = _replace_dimension(
        _fixture(),
        "P09",
        state=DimensionState.BLOCKED,
        source={"weight_state": "WEIGHT_BASIS_UNRESOLVED"},
        c11={"weight_state": "WEIGHT_BASIS_UNRESOLVED"},
        reason="missing exact design/estimand authority; no 1.0 repair",
    )
    result = certify_source_to_c11(request)
    assert result.disposition is CertificationDisposition.BLOCKED


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


def test_physical_dimension_evidence_order_is_semantically_stable():
    request = _fixture()
    first = certify_source_to_c11(request)
    second = certify_source_to_c11(
        replace(request, dimension_evidence=tuple(reversed(request.dimension_evidence)))
    )
    assert certification_is_replay_stable(first, second)
