import hashlib
from dataclasses import replace
from types import SimpleNamespace

import pytest

import rawlsing_next.pre553_c11_ingest as c11_ingest
import rawlsing_next.pre553_empirical_query as empirical_query
from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityConflict,
    Pre553AuthorityError,
    require_exact_authority_ref,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.pre553_c11_integrity import ReplayManifest, authority_snapshot_set_hash
from rawlsing_next.pre553_c11_repository import C11Repository, _make_validated_release
from rawlsing_next.pre553_replay_audit import (
    FORBIDDEN_SELECTOR_PROBES,
    HOSTILE_CLASSES,
    NONPOSITIVE_AUTHORITY_STATES,
    ReplayAuditError,
    assert_all_selector_fallbacks_rejected,
    assert_authority_tuple_mismatch_rejected,
    assert_exact_historical_authorities,
    assert_exact_source_content,
    assert_failure_state_never_positive,
    assert_missing_authority_rejected,
    assert_provenance_not_permission,
    assert_public_semantic_integrity,
    assert_replay_manifest_integrity,
    assert_repository_presence_not_permission,
    assert_selector_fallback_rejected,
    assert_supersession_does_not_reinterpret,
    audit_hostile_class,
)


def _h(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _authority_ref(tag: str, version: str = "1.0.0") -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", version, _h(f"authority:{tag}:{version}"))


def _snapshot(
    tag: str,
    *,
    version: str = "1.0.0",
    state: str = "ALLOW",
    kind: str = "PREDICATE_GRAMMAR",
    operations=("EXECUTE_EXACT_QUERY",),
    families=("EmpiricalQuerySpec@1.0.0",),
    supersession_refs=(),
) -> AuthoritySnapshot:
    ref = _authority_ref(tag, version)
    return AuthoritySnapshot(
        typed_state=state,
        producer_replay_locator_or_reference_root=f"urn:test:replay:{tag}:{version}",
        authority_id=ref.authority_id,
        authority_version=ref.authority_version,
        authority_content_hash=ref.authority_content_hash,
        authority_kind=kind,
        decision_state=state,
        governed_operations=operations,
        governed_object_families=families,
        scope_envelope={
            "source_universe_refs": "EXPLICIT_UNRESTRICTED",
            "target_use_refs": "EXPLICIT_UNRESTRICTED",
            "predicate_or_risk_set_refs": "EXPLICIT_UNRESTRICTED",
        },
        effective_time_or_interval="ALL_TIME_FOR_TEST",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=supersession_refs,
        interpretation_semantics_fingerprint=_h(f"meaning:{tag}:{version}"),
        replay_protocol_ref=_ref("ReplayProtocol", f"{tag}-{version}"),
    )


def _manifest(tag: str = "m") -> ReplayManifest:
    return ReplayManifest(
        frontier_version="D13-M01-M18",
        authority_snapshot_set_hash=_h(f"authority-set:{tag}"),
        source_substrate_content_refs=(_ref("SourceArtifact", tag),),
        semantic_projection_id=f"projection:{tag}",
        semantic_projection_hash=_h(f"projection:{tag}"),
        deterministic_tie_order_rules_ref=_ref("TieOrderRules", tag),
        replay_protocol_version="1.0.0",
        replay_protocol_authority_ref=_authority_ref(f"replay-{tag}"),
        closure_refs=(_ref("Closure", tag),),
    )


def _i02_replay_fixture(tag: str = "i02"):
    replay_authority = _snapshot(
        f"{tag}-replay",
        kind="REPLAY_PROTOCOL",
        operations=("REPLAY_EXACT_C11",),
        families=("ReplayReceipt@1.0.0",),
    )
    source_ref = _ref("SOURCE_ARTIFACT", tag)
    closure_refs = (_ref("Closure", f"{tag}-package"),)
    projection = {"candidate": tag, "semantic": "exact"}
    manifest = ReplayManifest(
        frontier_version=c11_ingest.FRONTIER_VERSION,
        authority_snapshot_set_hash=authority_snapshot_set_hash((replay_authority,)),
        source_substrate_content_refs=(source_ref,),
        semantic_projection_id=c11_ingest.SEMANTIC_PROJECTION_ID,
        semantic_projection_hash=semantic_hash(projection),
        deterministic_tie_order_rules_ref=_ref("TieOrderRules", f"{tag}-canonical"),
        replay_protocol_version="1.0.0",
        replay_protocol_authority_ref=replay_authority.authority_ref,
        closure_refs=closure_refs,
    )
    candidate = SimpleNamespace(
        candidate_replay_manifest=manifest,
        authority_snapshots=(replay_authority,),
        source_release_manifest=SimpleNamespace(source_artifact_ref=source_ref),
    )
    return candidate, replay_authority, projection, closure_refs


def _nonempty_repository() -> C11Repository:
    manifest = _manifest("repository-present")
    release = _make_validated_release(
        release_id="REL-R11-PRESENT",
        source_artifact_ref=_ref("SOURCE_ARTIFACT", "repository-present"),
        source_release_manifest_hash=_h("repository-present-manifest"),
        semantic_release_hash=_h("repository-present-semantic-release"),
        replay_manifest=manifest,
        public_objects=(),
        internal_records=(),
        m01_m18_coverage={},
    )
    return C11Repository((release,))


def test_r11_hostile_registry_is_complete_and_finite():
    assert HOSTILE_CLASSES == (
        "HISTORICAL_AUTHORITY_VERSION_PINNING",
        "AUTHORITY_ID_VERSION_HASH_MISMATCH",
        "MISSING_AUTHORITY",
        "LATEST_DEFAULT_FUZZY_NEAREST_FALLBACK",
        "REPLAY_IDENTITY_TAMPER",
        "SOURCE_CONTENT_TAMPER",
        "SEMANTIC_PROJECTION_TAMPER",
        "SUPERSESSION_REINTERPRETATION",
        "REPOSITORY_PRESENCE_AS_PERMISSION",
        "PROVENANCE_AS_QUERY_DISCOVERY_STRUCTURAL_AUTHORITY",
        "FAILURE_STATE_TO_POSITIVE_AUTHORITY",
    )


def test_historical_authority_version_is_pinned_not_upgraded():
    old = _snapshot("predicate", version="1.0.0")
    new = _snapshot("predicate", version="2.0.0")
    registry = AuthorityRegistry((old, new))
    resolved = assert_exact_historical_authorities(
        registry=registry, historical_refs=(old.authority_ref,)
    )
    assert resolved == (old,)
    assert resolved[0].authority_ref != new.authority_ref


def test_authority_id_version_hash_mismatch_fails_closed():
    snap = _snapshot("predicate")
    registry = AuthorityRegistry((snap,))
    wrong_hash = AuthorityRef(
        snap.authority_id,
        snap.authority_version,
        _h("different-content"),
    )
    assert_authority_tuple_mismatch_rejected(registry=registry, ref=wrong_hash)


def test_registry_rejects_same_id_version_with_conflicting_hashes():
    first = _snapshot("conflict")
    different = AuthoritySnapshot(
        typed_state="ALLOW",
        producer_replay_locator_or_reference_root="urn:test:replay:conflict-2",
        authority_id=first.authority_id,
        authority_version=first.authority_version,
        authority_content_hash=_h("conflicting-authority-content"),
        authority_kind="PREDICATE_GRAMMAR",
        decision_state="ALLOW",
        governed_operations=("EXECUTE_EXACT_QUERY",),
        governed_object_families=("EmpiricalQuerySpec@1.0.0",),
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="ALL_TIME_FOR_TEST",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h("conflicting-meaning"),
        replay_protocol_ref=_ref("ReplayProtocol", "conflict-2"),
    )
    with pytest.raises(Pre553AuthorityConflict):
        AuthorityRegistry((first, different))


def test_missing_authority_has_no_neighbor_fallback():
    existing = _snapshot("existing")
    registry = AuthorityRegistry((existing,))
    assert_missing_authority_rejected(
        registry=registry,
        ref=AuthorityRef("AUTH-MISSING", "9.9.9", _h("missing")),
    )


@pytest.mark.parametrize("selector", FORBIDDEN_SELECTOR_PROBES)
def test_latest_default_fuzzy_nearest_and_semver_fallbacks_rejected_in_authority_id(selector):
    assert_selector_fallback_rejected(selector)


@pytest.mark.parametrize("selector", FORBIDDEN_SELECTOR_PROBES)
def test_latest_default_fuzzy_nearest_and_semver_fallbacks_rejected_in_authority_version(selector):
    probe = AuthorityRef("AUTH-R11-EXACT", selector, _h(f"selector-version:{selector}"))
    with pytest.raises(Pre553AuthorityError):
        require_exact_authority_ref(probe)


def test_all_selector_fallbacks_rejected_as_one_oracle():
    assert_all_selector_fallbacks_rejected()


def test_replay_manifest_tamper_fails_against_pinned_identity():
    manifest = _manifest("historical")
    expected = manifest.ref
    object.__setattr__(manifest, "semantic_projection_hash", _h("tampered-projection"))
    with pytest.raises(ReplayAuditError, match="ReplayManifest semantic identity tamper"):
        assert_replay_manifest_integrity(manifest, expected_ref=expected)


def test_i02_validate_replay_accepts_only_exact_manifest(monkeypatch):
    candidate, replay_authority, projection, closure_refs = _i02_replay_fixture("exact")
    monkeypatch.setattr(c11_ingest, "_candidate_projection_semantic_hash", lambda _: semantic_hash(projection))
    monkeypatch.setattr(c11_ingest, "_all_nonmanifest_refs", lambda _: closure_refs)
    registry = AuthorityRegistry((replay_authority,))
    assert c11_ingest._validate_replay(candidate, registry) is candidate.candidate_replay_manifest


def test_i02_validate_replay_rejects_semantic_projection_tamper(monkeypatch):
    candidate, replay_authority, projection, closure_refs = _i02_replay_fixture("projection-tamper")
    monkeypatch.setattr(c11_ingest, "_candidate_projection_semantic_hash", lambda _: semantic_hash(projection))
    monkeypatch.setattr(c11_ingest, "_all_nonmanifest_refs", lambda _: closure_refs)
    tampered_manifest = replace(
        candidate.candidate_replay_manifest,
        semantic_projection_hash=_h("tampered-candidate-projection"),
    )
    tampered_candidate = SimpleNamespace(
        candidate_replay_manifest=tampered_manifest,
        authority_snapshots=candidate.authority_snapshots,
        source_release_manifest=candidate.source_release_manifest,
    )
    with pytest.raises(c11_ingest.C11IngestValidationError, match="semantic projection differs"):
        c11_ingest._validate_replay(tampered_candidate, AuthorityRegistry((replay_authority,)))


def test_i02_validate_replay_rejects_source_content_tamper(monkeypatch):
    candidate, replay_authority, projection, closure_refs = _i02_replay_fixture("source-tamper")
    monkeypatch.setattr(c11_ingest, "_candidate_projection_semantic_hash", lambda _: semantic_hash(projection))
    monkeypatch.setattr(c11_ingest, "_all_nonmanifest_refs", lambda _: closure_refs)
    source_ref = candidate.source_release_manifest.source_artifact_ref
    tampered_source_ref = ExactRef(source_ref.kind, source_ref.object_id, _h("tampered-source-bytes"))
    tampered_candidate = SimpleNamespace(
        candidate_replay_manifest=candidate.candidate_replay_manifest,
        authority_snapshots=candidate.authority_snapshots,
        source_release_manifest=SimpleNamespace(source_artifact_ref=tampered_source_ref),
    )
    with pytest.raises(c11_ingest.C11IngestValidationError, match="source artifact identity/hash differs"):
        c11_ingest._validate_replay(tampered_candidate, AuthorityRegistry((replay_authority,)))


def test_i02_validate_replay_rejects_authority_set_tamper(monkeypatch):
    candidate, replay_authority, projection, closure_refs = _i02_replay_fixture("authority-set")
    monkeypatch.setattr(c11_ingest, "_candidate_projection_semantic_hash", lambda _: semantic_hash(projection))
    monkeypatch.setattr(c11_ingest, "_all_nonmanifest_refs", lambda _: closure_refs)
    tampered_manifest = replace(
        candidate.candidate_replay_manifest,
        authority_snapshot_set_hash=_h("tampered-authority-set"),
    )
    tampered_candidate = SimpleNamespace(
        candidate_replay_manifest=tampered_manifest,
        authority_snapshots=candidate.authority_snapshots,
        source_release_manifest=candidate.source_release_manifest,
    )
    with pytest.raises(c11_ingest.C11IngestValidationError, match="authority snapshot set differs"):
        c11_ingest._validate_replay(tampered_candidate, AuthorityRegistry((replay_authority,)))


def test_i02_validate_replay_rejects_missing_replay_authority(monkeypatch):
    candidate, _replay_authority, projection, closure_refs = _i02_replay_fixture("missing-replay-auth")
    monkeypatch.setattr(c11_ingest, "_candidate_projection_semantic_hash", lambda _: semantic_hash(projection))
    monkeypatch.setattr(c11_ingest, "_all_nonmanifest_refs", lambda _: closure_refs)
    with pytest.raises(c11_ingest.C11IngestValidationError, match="replay protocol authority unavailable"):
        c11_ingest._validate_replay(candidate, AuthorityRegistry(()))


def test_source_content_tamper_has_zero_path_or_label_fallback():
    expected = (_ref("SourceArtifact", "release-a"),)
    tampered = (
        ExactRef(
            expected[0].kind,
            expected[0].object_id,
            _h("same-label-different-source-bytes"),
        ),
    )
    with pytest.raises(ReplayAuditError, match="source-content exact refs differ"):
        assert_exact_source_content(actual=tampered, expected=expected)


def test_public_semantic_projection_tamper_fails_closed():
    snap = _snapshot("semantic")
    expected = snap.ref
    object.__setattr__(snap, "content_hash", _h("forged-content-hash"))
    with pytest.raises(ReplayAuditError, match="semantic projection tamper"):
        assert_public_semantic_integrity(snap, expected_ref=expected)


def test_i03_replay_empirical_query_pins_exact_expected_fact_refs(monkeypatch):
    actual_ref = _ref("EmpiricalFact", "i03-actual")
    fake_result = SimpleNamespace(facts=(SimpleNamespace(ref=actual_ref),))
    monkeypatch.setattr(empirical_query, "execute_empirical_query", lambda **_: fake_result)
    kwargs = {
        "repository": object(),
        "query": object(),
        "predicate": object(),
        "authority_registry": object(),
        "release_refs": (),
    }
    assert empirical_query.replay_empirical_query(
        **kwargs,
        expected_fact_refs=(actual_ref,),
    ) is fake_result

    tampered_ref = ExactRef(actual_ref.kind, actual_ref.object_id, _h("i03-fact-tamper"))
    with pytest.raises(empirical_query.EmpiricalQueryExecutionError, match="deterministic replay mismatch"):
        empirical_query.replay_empirical_query(
            **kwargs,
            expected_fact_refs=(tampered_ref,),
        )


def test_superseding_authority_does_not_reinterpret_historical_object():
    old = _snapshot("policy", version="1.0.0")
    new = _snapshot(
        "policy",
        version="2.0.0",
        supersession_refs=(old.authority_ref,),
    )
    registry = AuthorityRegistry((old, new))
    assert_supersession_does_not_reinterpret(
        registry=registry,
        historical_ref=old.authority_ref,
        superseding_ref=new.authority_ref,
    )
    assert registry.resolve_exact(old.authority_ref).snapshot is old


def test_nonempty_repository_presence_does_not_supply_missing_semantic_permission():
    repository = _nonempty_repository()
    assert len(repository) == 1
    registry = AuthorityRegistry((_snapshot("unrelated"),))
    missing = AuthorityRef("AUTH-STRUCTURAL", "1.0.0", _h("absent-structural"))
    assert_repository_presence_not_permission(
        repository=repository,
        registry=registry,
        required_ref=missing,
    )


@pytest.mark.parametrize(
    "authority_kind,object_family",
    (
        ("PREDICATE_GRAMMAR", "EmpiricalQuerySpec@1.0.0"),
        ("DISCOVERY_FRONTIER", "DiscoveryAuthority@1.0.0"),
        ("STRUCTURAL_ADMISSION", "StructuralEmpiricalAdmission@1.0.0"),
    ),
)
def test_provenance_cannot_infer_query_discovery_or_structural_authority(
    authority_kind, object_family
):
    unrelated = _snapshot(
        "provenance-only",
        kind="REPLAY_PROTOCOL",
        operations=("REPLAY",),
        families=("ReplayReceipt@1.0.0",),
    )
    registry = AuthorityRegistry((unrelated,))
    assert_provenance_not_permission(
        provenance_refs=(_ref("Provenance", authority_kind),),
        registry=registry,
        required_authority_ref=unrelated.authority_ref,
        authority_kind=authority_kind,
        operation="FORBIDDEN_INFERRED_OPERATION",
        object_family=object_family,
    )


@pytest.mark.parametrize("state", sorted(NONPOSITIVE_AUTHORITY_STATES))
def test_every_failure_state_is_zero_positive_authority(state):
    snap = _snapshot("negative", state=state)
    assert_failure_state_never_positive(snap, operation="EXECUTE_EXACT_QUERY")


def test_wrong_operation_cannot_be_repaired_by_positive_authority_presence():
    snap = _snapshot("predicate")
    with pytest.raises(Pre553AuthorityError):
        from rawlsing_next.pre553_empirical_authority import require_positive_authority
        require_positive_authority(snap, operation="DISCOVER_OR_ADMIT_BY_PROVENANCE")


def test_hostile_finding_wrapper_records_pass_only_when_probe_completes():
    finding = audit_hostile_class("MISSING_AUTHORITY", lambda: None)
    assert finding.passed is True
    assert finding.detail == "zero semantic fallback preserved"

    failed = audit_hostile_class(
        "MISSING_AUTHORITY",
        lambda: (_ for _ in ()).throw(RuntimeError("unexpected")),
    )
    assert failed.passed is False
    assert "unexpected" in failed.detail
