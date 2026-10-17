from __future__ import annotations

import hashlib

import pytest

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalUniverse,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.pre553_source_local_universe_admission import (
    ADMISSION_OPERATION,
    AUTHORITY_KIND,
    CLAIM_CEILING,
    CONTRACT_ID,
    DocumentaryField,
    REQUIRED_NEGATIVE_LIMIT_REFS,
    SourceLocalUniverseAdmissionError,
    SourceLocalUniverseSpec,
    SourceLocalUse,
    materialize_source_local_universe,
    population_overlay_basis,
    require_source_local_use,
    validate_source_local_universe,
)


def h(tag: str) -> str:
    return hashlib.sha256(tag.encode()).hexdigest()


def ref(kind: str, tag: str) -> ExactRef:
    digest = h(f"{kind}:{tag}")
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}:sha256:{digest}", digest)


SOURCE = ref("SOURCE_ARTIFACT", "wvs7")
RESPONDENTS = ref("RESPONDENT_SCOPE", "wvs7-country-scope")
REPLAY = ref("SCOPED_RESPONDENT_REPLAY", "wvs7-country-scope")
DOC = ref("DOCUMENT", "country-methodology")
REPLAY_PROTOCOL = ref("REPLAY_PROTOCOL", "source-local-admission-r1")


def spec(
    *,
    source_ref: ExactRef = SOURCE,
    target: DocumentaryField | None = None,
    design: DocumentaryField | None = None,
) -> SourceLocalUniverseSpec:
    return SourceLocalUniverseSpec(
        raw_source_identity="WVS7_TEST_SOURCE",
        source_family="WVS",
        study_product_release="WVS/Wave7/TestCountry",
        instrument_release="WVS7 questionnaire",
        country_geography={"source_native_country": "TEST"},
        sampling_geography={"state": "SOURCE_NATIVE_SCOPE"},
        raw_wave="7",
        canonical_wave_if_governed=None,
        field_or_reference_time={"year": 2020},
        respondent_namespace="SOURCE_SHA256_PLUS_SOURCE_ROW_ORDINAL",
        source_artifact_import_lineage={"source_sha256": SOURCE.content_hash},
        source_artifact_ref=source_ref,
        respondent_scope_ref=RESPONDENTS,
        replay_scope_ref=REPLAY,
        target_population_and_sample_frame=target
        or DocumentaryField.not_population_certified("TARGET_FRAME_NOT_YET_CERTIFIED"),
        sampling_design_regime=design
        or DocumentaryField.not_population_certified("DESIGN_NOT_YET_CERTIFIED"),
    )


def authority(
    s: SourceLocalUniverseSpec,
    *,
    state: str = "ALLOW",
    kind: str = AUTHORITY_KIND,
    operations: tuple[str, ...] = (ADMISSION_OPERATION,),
    families: tuple[str, ...] = ("EmpiricalUniverse@1.0.0",),
    dependencies: tuple[ExactRef, ...] | None = None,
    negatives: tuple[ExactRef, ...] = REQUIRED_NEGATIVE_LIMIT_REFS,
    scope_overrides: dict | None = None,
    tag: str = "base",
) -> AuthoritySnapshot:
    deps = dependencies if dependencies is not None else s.exact_scope_refs
    scope = {
        "claim_ceiling": CLAIM_CEILING,
        "population_generalization": "DENIED_UNLESS_SEPARATELY_AUTHORIZED",
        "default_measure_ceiling": "RAW_ONLY",
        "source_artifact_ref": s.source_artifact_ref,
        "respondent_scope_ref": s.respondent_scope_ref,
        "replay_scope_ref": s.replay_scope_ref,
    }
    if scope_overrides:
        scope.update(scope_overrides)
    material = {
        "contract": CONTRACT_ID,
        "tag": tag,
        "state": state,
        "kind": kind,
        "operations": operations,
        "families": families,
        "scope": scope,
        "dependencies": [x.as_dict() for x in deps],
        "negative_limits": [x.as_dict() for x in negatives],
    }
    return AuthoritySnapshot(
        typed_state=state,
        authority_snapshot_refs=(),
        dependency_refs=deps,
        producer_replay_locator_or_reference_root=ref("AUTHORITY_REPLAY", tag),
        authority_id=f"TEST-SOURCE-LOCAL-{tag}",
        authority_version="1.0.0",
        authority_content_hash=semantic_hash(material),
        authority_kind=kind,
        decision_state=state,
        governed_operations=operations,
        governed_object_families=families,
        scope_envelope=scope,
        effective_time_or_interval="TEST",
        parent_authority_refs=(),
        negative_limit_refs=negatives,
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash(
            {"material": material, "source_local_only": True}
        ),
        replay_protocol_ref=REPLAY_PROTOCOL,
    )


def build(s: SourceLocalUniverseSpec | None = None, a: AuthoritySnapshot | None = None):
    s = s or spec()
    a = a or authority(s)
    registry = AuthorityRegistry((a,))
    return materialize_source_local_universe(
        spec=s,
        admission_authority=a,
        authority_registry=registry,
    ), registry


def reload_universe(universe: EmpiricalUniverse) -> EmpiricalUniverse:
    value = universe.as_dict()
    fields = dict(value["semantic_fields"])
    return EmpiricalUniverse(
        typed_state=value["typed_state"],
        authority_snapshot_refs=value["authority_snapshot_refs"],
        dependency_refs=value["dependency_refs"],
        producer_replay_locator_or_reference_root=value[
            "producer_replay_locator_or_reference_root"
        ],
        object_id=value["object_id"],
        content_hash=value["content_hash"],
        schema_id=value["schema_id"],
        schema_version=value["schema_version"],
        **fields,
    )


def test_01_source_local_universe_materializes_without_population_documentation():
    universe, registry = build()
    assert universe.typed_state == "UNIVERSE_IDENTIFIED"
    assert universe.source_local_claim_ceiling == CLAIM_CEILING
    assert universe.target_population_and_sample_frame["state"] == "NOT_POPULATION_CERTIFIED"
    assert universe.sampling_design_regime["state"] == "NOT_POPULATION_CERTIFIED"
    validate_source_local_universe(universe, registry)


def test_02_preserved_documentary_content_does_not_grant_population_permission():
    target = DocumentaryField.preserve(
        {"target": "adults 18+", "frame": "named address frame"},
        (DOC,),
    )
    design = DocumentaryField.preserve(
        {"design": "multistage probability sample"},
        (DOC,),
    )
    universe, _ = build(spec(target=target, design=design))
    assert universe.target_population_and_sample_frame["content"]["target"] == "adults 18+"
    assert (
        universe.target_population_and_sample_frame["claim_ceiling"]
        == CLAIM_CEILING
    )
    basis = population_overlay_basis(universe)
    assert basis["population_permission_granted"] is False
    assert basis["source_local_universe_ref"] == universe.ref.as_dict()


@pytest.mark.parametrize("missing", ["source", "respondent", "replay"])
def test_03_05_exact_scope_dependencies_are_mandatory(missing):
    s = spec()
    deps = {
        "source": (RESPONDENTS, REPLAY),
        "respondent": (SOURCE, REPLAY),
        "replay": (SOURCE, RESPONDENTS),
    }[missing]
    a = authority(s, dependencies=deps, tag=f"missing-{missing}")
    with pytest.raises(SourceLocalUniverseAdmissionError):
        materialize_source_local_universe(
            spec=s,
            admission_authority=a,
            authority_registry=AuthorityRegistry((a,)),
        )


def test_06_all_required_negative_limits_are_mandatory():
    s = spec()
    a = authority(
        s,
        negatives=REQUIRED_NEGATIVE_LIMIT_REFS[:-1],
        tag="missing-negative",
    )
    with pytest.raises(SourceLocalUniverseAdmissionError):
        materialize_source_local_universe(
            spec=s,
            admission_authority=a,
            authority_registry=AuthorityRegistry((a,)),
        )


def test_07_nonpositive_authority_is_rejected():
    s = spec()
    a = authority(s, state="DENY", tag="deny")
    with pytest.raises(SourceLocalUniverseAdmissionError):
        materialize_source_local_universe(
            spec=s,
            admission_authority=a,
            authority_registry=AuthorityRegistry((a,)),
        )


def test_08_wrong_authority_kind_is_rejected():
    s = spec()
    a = authority(s, kind="REPLAY_PROTOCOL", tag="wrong-kind")
    with pytest.raises(SourceLocalUniverseAdmissionError):
        materialize_source_local_universe(
            spec=s,
            admission_authority=a,
            authority_registry=AuthorityRegistry((a,)),
        )


def test_09_wrong_operation_is_rejected():
    s = spec()
    a = authority(s, operations=("SOME_OTHER_OPERATION",), tag="wrong-operation")
    with pytest.raises(SourceLocalUniverseAdmissionError):
        materialize_source_local_universe(
            spec=s,
            admission_authority=a,
            authority_registry=AuthorityRegistry((a,)),
        )


def test_10_wrong_governed_family_is_rejected():
    s = spec()
    a = authority(s, families=("RespondentEvent@1.0.0",), tag="wrong-family")
    with pytest.raises(SourceLocalUniverseAdmissionError):
        materialize_source_local_universe(
            spec=s,
            admission_authority=a,
            authority_registry=AuthorityRegistry((a,)),
        )


@pytest.mark.parametrize(
    "use",
    [
        SourceLocalUse.POPULATION_GENERALIZATION,
        SourceLocalUse.GOVERNED_WEIGHTED_POPULATION_ESTIMAND,
        SourceLocalUse.AUTHORIZED_COMPOSITE_POOLING,
        SourceLocalUse.SOURCE_BACKFILL,
        SourceLocalUse.HARMONIZATION,
    ],
)
def test_11_15_stronger_uses_are_rejected_without_separate_authority(use):
    universe, registry = build()
    with pytest.raises(SourceLocalUniverseAdmissionError):
        require_source_local_use(universe, registry, use)


@pytest.mark.parametrize(
    "use",
    [
        SourceLocalUse.RAW_SINGLE_UNIVERSE,
        SourceLocalUse.RAW_SOURCE_INDEXED_MULTI_UNIVERSE,
    ],
)
def test_16_17_raw_source_local_uses_are_allowed(use):
    universe, registry = build()
    require_source_local_use(universe, registry, use)


def test_18_not_certified_state_cannot_smuggle_documentary_content():
    with pytest.raises(SourceLocalUniverseAdmissionError):
        DocumentaryField(
            "NOT_POPULATION_CERTIFIED",
            {"invented": "population frame"},
            (),
        )


def test_19_preserved_documentary_content_requires_exact_provenance():
    with pytest.raises(SourceLocalUniverseAdmissionError):
        DocumentaryField.preserve({"target": "adults"}, ())


def test_20_source_identity_mutation_changes_universe_identity():
    first, _ = build()
    changed_source = ref("SOURCE_ARTIFACT", "wvs7-mutated")
    second_spec = spec(source_ref=changed_source)
    second_auth = authority(second_spec, tag="source-mutated")
    second, _ = build(second_spec, second_auth)
    assert first.ref != second.ref
    assert first.content_hash != second.content_hash


def test_21_authority_negative_limit_mutation_changes_universe_identity():
    s = spec()
    base = authority(s, tag="negative-base")
    extra = ref("NEGATIVE_LIMIT", "extra-source-local-limit")
    changed = authority(
        s,
        negatives=tuple((*REQUIRED_NEGATIVE_LIMIT_REFS, extra)),
        tag="negative-extra",
    )
    first, _ = build(s, base)
    second, _ = build(s, changed)
    assert first.ref != second.ref


def test_22_exact_reload_preserves_source_local_identity_and_validation():
    universe, registry = build()
    reloaded = reload_universe(universe)
    assert reloaded == universe
    assert reloaded.ref == universe.ref
    validate_source_local_universe(reloaded, registry)


def test_23_authority_scope_source_mismatch_is_rejected():
    s = spec()
    other = ref("SOURCE_ARTIFACT", "other")
    a = authority(
        s,
        scope_overrides={"source_artifact_ref": other},
        tag="scope-source-mismatch",
    )
    with pytest.raises(SourceLocalUniverseAdmissionError):
        materialize_source_local_universe(
            spec=s,
            admission_authority=a,
            authority_registry=AuthorityRegistry((a,)),
        )


def test_24_population_overlay_basis_is_deterministic_and_source_bound():
    universe, _ = build()
    left = population_overlay_basis(universe)
    right = population_overlay_basis(reload_universe(universe))
    assert dict(left) == dict(right)
    assert left["overlay_basis_hash"] == right["overlay_basis_hash"]
