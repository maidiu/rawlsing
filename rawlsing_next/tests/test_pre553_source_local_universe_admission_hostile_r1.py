from __future__ import annotations

import hashlib

import pytest

from rawlsing_next.pre553_c11_integrity import validate_public_carrier_object
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
    negative_limit_ref,
    population_overlay_basis,
    require_source_local_use,
    validate_source_local_universe,
)
from rawlsing_next.wave2_r5_q69b_conditioner_projection import _accepted_universe


def h(tag: str) -> str:
    return hashlib.sha256(tag.encode()).hexdigest()


def ref(kind: str, tag: str) -> ExactRef:
    digest = h(f"{kind}:{tag}")
    return ExactRef(kind, f"urn:hostile:{kind.lower()}:{tag}:sha256:{digest}", digest)


SOURCE = ref("SOURCE_ARTIFACT", "source")
RESP = ref("RESPONDENT_SCOPE", "respondents")
REPLAY = ref("SCOPED_RESPONDENT_REPLAY", "replay")
DOC = ref("DOCUMENT", "methodology")
PROTOCOL = ref("REPLAY_PROTOCOL", "protocol")


def make_spec(*, target=None, design=None):
    return SourceLocalUniverseSpec(
        raw_source_identity="HOSTILE_SOURCE",
        source_family="SURVEY",
        study_product_release="SURVEY/W1/COUNTRY",
        instrument_release="INSTRUMENT",
        country_geography={"source_native_country": "X"},
        sampling_geography={"source_native_scope": "X-W1"},
        raw_wave="W1",
        canonical_wave_if_governed=None,
        field_or_reference_time={"year": 2020},
        respondent_namespace="SOURCE_SHA_PLUS_ROW",
        source_artifact_import_lineage={"source_sha256": SOURCE.content_hash},
        source_artifact_ref=SOURCE,
        respondent_scope_ref=RESP,
        replay_scope_ref=REPLAY,
        target_population_and_sample_frame=target
        or DocumentaryField.not_population_certified("TARGET_FRAME_UNCERTIFIED"),
        sampling_design_regime=design
        or DocumentaryField.not_population_certified("DESIGN_UNCERTIFIED"),
    )


def make_authority(
    spec,
    *,
    source=SOURCE,
    respondent=RESP,
    replay=REPLAY,
    negatives=REQUIRED_NEGATIVE_LIMIT_REFS,
    state="ALLOW",
    tag="base",
):
    deps = (source, respondent, replay)
    scope = {
        "claim_ceiling": CLAIM_CEILING,
        "population_generalization": "DENIED_UNLESS_SEPARATELY_AUTHORIZED",
        "default_measure_ceiling": "RAW_ONLY",
        "source_artifact_ref": source,
        "respondent_scope_ref": respondent,
        "replay_scope_ref": replay,
    }
    material = {
        "contract": CONTRACT_ID,
        "tag": tag,
        "state": state,
        "scope": scope,
        "deps": [x.as_dict() for x in deps],
        "negative_limits": [x.as_dict() for x in negatives],
    }
    return AuthoritySnapshot(
        typed_state=state,
        authority_snapshot_refs=(),
        dependency_refs=deps,
        producer_replay_locator_or_reference_root=ref("AUTH_REPLAY", tag),
        authority_id=f"HOSTILE-SOURCE-LOCAL-{tag}",
        authority_version="1.0.0",
        authority_content_hash=semantic_hash(material),
        authority_kind=AUTHORITY_KIND,
        decision_state=state,
        governed_operations=(ADMISSION_OPERATION,),
        governed_object_families=("EmpiricalUniverse@1.0.0",),
        scope_envelope=scope,
        effective_time_or_interval="HOSTILE",
        parent_authority_refs=(),
        negative_limit_refs=negatives,
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash(
            {"material": material, "no_population_widening": True}
        ),
        replay_protocol_ref=PROTOCOL,
    )


def built(*, target=None, design=None):
    spec = make_spec(target=target, design=design)
    auth = make_authority(spec)
    registry = AuthorityRegistry((auth,))
    universe = materialize_source_local_universe(
        spec=spec,
        admission_authority=auth,
        authority_registry=registry,
    )
    return spec, auth, registry, universe


def clone(universe: EmpiricalUniverse, **field_updates) -> EmpiricalUniverse:
    wire = universe.as_dict()
    fields = dict(wire["semantic_fields"])
    fields.update(field_updates)
    return EmpiricalUniverse(
        typed_state=wire["typed_state"],
        authority_snapshot_refs=wire["authority_snapshot_refs"],
        dependency_refs=wire["dependency_refs"],
        producer_replay_locator_or_reference_root=wire[
            "producer_replay_locator_or_reference_root"
        ],
        **fields,
    )


def test_h01_materialized_source_local_universe_is_valid_c11_public_carrier():
    _, _, registry, universe = built()
    assert validate_public_carrier_object(universe, registry) is universe
    validate_source_local_universe(universe, registry)


def test_h02_existing_afrobarometer_pipeline_already_uses_source_local_nonpopulation_pattern():
    universe, _ = _accepted_universe()
    assert "NO_POPULATION_GENERALIZATION" in universe.target_population_and_sample_frame
    assert "RAW_UNWEIGHTED" in universe.sampling_design_regime


def test_h03_required_negative_limit_refs_are_deterministic_exact_identities():
    regenerated = tuple(
        sorted(
            (negative_limit_ref(name) for name in (
                "NO_POPULATION_GENERALIZATION",
                "NO_WEIGHTED_POPULATION_ESTIMAND_UNLESS_SEPARATELY_AUTHORIZED",
                "NO_CROSS_UNIVERSE_POOLING_WITHOUT_RELATION_AUTHORITY",
                "NO_NEAREST_COUNTRY_OR_WAVE_BACKFILL",
            )),
            key=lambda r: r.key,
        )
    )
    assert regenerated == REQUIRED_NEGATIVE_LIMIT_REFS


def test_h04_forged_population_claim_ceiling_on_universe_is_rejected():
    _, _, registry, universe = built()
    forged = clone(universe, source_local_claim_ceiling="POPULATION_CERTIFIED")
    with pytest.raises(SourceLocalUniverseAdmissionError):
        validate_source_local_universe(forged, registry)


def test_h05_documentary_field_cannot_forge_population_claim_ceiling():
    _, _, registry, universe = built()
    target = dict(universe.target_population_and_sample_frame)
    target["claim_ceiling"] = "POPULATION_CERTIFIED"
    forged = clone(universe, target_population_and_sample_frame=target)
    with pytest.raises(SourceLocalUniverseAdmissionError):
        validate_source_local_universe(forged, registry)


def test_h06_not_certified_documentary_state_cannot_smuggle_content_after_materialization():
    _, _, registry, universe = built()
    target = dict(universe.target_population_and_sample_frame)
    target["content"] = {"invented": "national population"}
    forged = clone(universe, target_population_and_sample_frame=target)
    with pytest.raises(SourceLocalUniverseAdmissionError):
        validate_source_local_universe(forged, registry)


def test_h07_replay_root_forgery_is_rejected_even_when_exact_ref_shaped():
    _, auth, _, universe = built()
    wire = universe.as_dict()
    fields = dict(wire["semantic_fields"])
    forged = EmpiricalUniverse(
        typed_state=wire["typed_state"],
        authority_snapshot_refs=wire["authority_snapshot_refs"],
        dependency_refs=wire["dependency_refs"],
        producer_replay_locator_or_reference_root=ref("SCOPED_RESPONDENT_REPLAY", "other"),
        **fields,
    )
    registry = AuthorityRegistry((auth,))
    with pytest.raises(SourceLocalUniverseAdmissionError):
        validate_source_local_universe(forged, registry)


def test_h08_authority_bound_to_other_source_cannot_validate_same_universe_dependencies():
    spec, _, _, universe = built()
    other = ref("SOURCE_ARTIFACT", "other")
    forged_auth = make_authority(spec, source=other, tag="other-source")
    forged = clone(
        universe,
    )
    wire = forged.as_dict()
    fields = dict(wire["semantic_fields"])
    rebound = EmpiricalUniverse(
        typed_state=wire["typed_state"],
        authority_snapshot_refs=(forged_auth.authority_ref,),
        dependency_refs=wire["dependency_refs"],
        producer_replay_locator_or_reference_root=wire[
            "producer_replay_locator_or_reference_root"
        ],
        **fields,
    )
    with pytest.raises(SourceLocalUniverseAdmissionError):
        validate_source_local_universe(rebound, AuthorityRegistry((forged_auth,)))


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
def test_h09_h13_every_stronger_claim_class_fails_closed(use):
    _, _, registry, universe = built()
    with pytest.raises(SourceLocalUniverseAdmissionError):
        require_source_local_use(universe, registry, use)


@pytest.mark.parametrize(
    "use",
    [
        SourceLocalUse.RAW_SINGLE_UNIVERSE,
        SourceLocalUse.RAW_SOURCE_INDEXED_MULTI_UNIVERSE,
    ],
)
def test_h14_h15_only_raw_source_local_classes_are_admitted(use):
    _, _, registry, universe = built()
    require_source_local_use(universe, registry, use)


def test_h16_preserved_positive_documentary_text_still_has_no_population_permission():
    target = DocumentaryField.preserve(
        {"target": "adults 18+", "frame": "address frame"},
        (DOC,),
    )
    design = DocumentaryField.preserve(
        {"design": "probability sample"},
        (DOC,),
    )
    _, _, registry, universe = built(target=target, design=design)
    assert universe.target_population_and_sample_frame["content"]["target"] == "adults 18+"
    with pytest.raises(SourceLocalUniverseAdmissionError):
        require_source_local_use(
            universe,
            registry,
            SourceLocalUse.POPULATION_GENERALIZATION,
        )


def test_h17_population_overlay_basis_preserves_documentary_material_without_granting_permission():
    target = DocumentaryField.preserve({"target": "adults"}, (DOC,))
    _, _, _, universe = built(target=target)
    basis = population_overlay_basis(universe)
    assert basis["population_permission_granted"] is False
    assert basis["target_population_and_sample_frame"]["content"]["target"] == "adults"


def test_h18_documentary_mutation_changes_overlay_identity():
    first = DocumentaryField.preserve({"target": "adults"}, (DOC,))
    second = DocumentaryField.preserve({"target": "adults 18+"}, (DOC,))
    _, _, _, u1 = built(target=first)
    _, _, _, u2 = built(target=second)
    assert population_overlay_basis(u1)["overlay_basis_hash"] != population_overlay_basis(u2)["overlay_basis_hash"]


def test_h19_extra_negative_limit_does_not_remove_required_limits_or_widen_claim_ceiling():
    spec = make_spec()
    extra = ref("NEGATIVE_LIMIT", "extra")
    auth = make_authority(
        spec,
        negatives=tuple((*REQUIRED_NEGATIVE_LIMIT_REFS, extra)),
        tag="extra-negative",
    )
    registry = AuthorityRegistry((auth,))
    universe = materialize_source_local_universe(
        spec=spec,
        admission_authority=auth,
        authority_registry=registry,
    )
    validate_source_local_universe(universe, registry)
    with pytest.raises(SourceLocalUniverseAdmissionError):
        require_source_local_use(
            universe, registry, SourceLocalUse.POPULATION_GENERALIZATION
        )


def test_h20_non_allow_authority_never_materializes_source_local_universe():
    spec = make_spec()
    auth = make_authority(spec, state="DENY", tag="deny")
    with pytest.raises(SourceLocalUniverseAdmissionError):
        materialize_source_local_universe(
            spec=spec,
            admission_authority=auth,
            authority_registry=AuthorityRegistry((auth,)),
        )
