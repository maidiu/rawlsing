"""HQ280 F8D: C1-native M2/B5 development binding, NOT an issued service.

This candidate is limited to the HQ260/HQ280 four-case source-free XOR
q(C|A=1) / q(C|A=1,B=0) court. It derives exact identity from an
already-produced current C1 result. It does not confer scientific source
authority, cryptographic producer identity, operative EE14 G0b, B5 publication
or CURRENT selection, or an authenticated G1 service.

The content-addressed candidate producer contract below identifies *this
development proposal*, not an issued external semantic credential. Successful
M2 validation proves closure consistency, not the authenticity of a caller-
supplied C1 result. Independent producer custody and HQ adoption remain gates.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from rawlsing_next.pre553_analytical_composition import (
    AnalyticalCompositionResult, EVIDENCE_CONTRACT_ID, EVIDENCE_PREIMAGE_SCHEMA,
)
from rawlsing_next.pre553_analytical_replay_dependency import (
    AnalyticalDependencyRegistry, AnalyticalProductRegistration,
    AnalyticalReplayClaim, MECHANISM_HISTORICAL_NARRATION,
    REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, ExactRef, canonicalize, semantic_hash,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    PositionedSubjectPossibilityModelRule, PossibilitySliceEvidence,
)
from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next import pre553_learned_product_lifecycle as B5

CONTRACT_ID = "C1_HQ280_F8D_SOURCE_FREE_RELEASE_CANDIDATE@1"
DEVELOPMENT_GRADE = "SOURCE_FREE_CANDIDATE_ONLY__NONAUTHORIZING__G0B_HELD"
GOVERNING_DECISION = "HQD-2026-10-10-280"
C1_ACCEPTED_BLOB = "604c8d591d4cc2b646e9b149cdb233fc9d69cf6b"
M2_REPLAY_GRADE = "HISTORICAL_EXPLANATION_ONLY"
# B5 may stage/register this product; publication needs independently
# qualified replay and producer permission. There is no selectable CURRENT.
B5_REPLAY_STATE = "REPLAY_BLOCKED_MISSING_AUTHORITY"
_ALLOWED_CELLS = {"q1": (1, 2), "q2": (2, 1)}


class C1ImmutableReleaseHold(ValueError):
    """Typed scientific, provenance, contract or replay refusal."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"{code}: {message}")


def _require(ok: bool, code: str, explanation: str) -> None:
    if not ok:
        raise C1ImmutableReleaseHold(code, explanation)


def _ref(kind: str, slug: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(
        kind, f"urn:rawlsing:pre553:c1-f8d:{slug}:sha256:{digest}", digest
    )


CONTRACT_MATERIAL = {
    "contract_id": CONTRACT_ID,
    "decision": GOVERNING_DECISION,
    "accepted_c1_owner_blob": C1_ACCEPTED_BLOB,
    "scientific_purpose": "EMPIRICAL_POSSIBILITY_ONLY",
    "fixture": "HQ260_XOR_FOUR_RESPONDENT_Q1_Q2_ONLY",
    "grant": None,
    "external_issuer": None,
    "status": DEVELOPMENT_GRADE,
    "current_selection": False,
}
# A proposal identifier, explicitly NOT an operative producer issuer credential.
CANDIDATE_CONTRACT_REF = _ref(
    "C1DevelopmentContractCandidate", "nonissued-contract", CONTRACT_MATERIAL
)
CANDIDATE_OWNER_REF = _ref(
    "C1DevelopmentOwnerCandidate", "nonissued-owner",
    {"contract_ref": CANDIDATE_CONTRACT_REF.as_dict(), "authority": None},
)
CANDIDATE_FAMILY_REF = _ref(
    "C1DevelopmentProductFamily", "family",
    {"contract_ref": CANDIDATE_CONTRACT_REF.as_dict(), "product": "C1_IMMUTABLE_SLICE"},
)
PERMISSION_CEILING_REF = _ref(
    "C1DevelopmentPermissionCeiling", "no-usage-grant",
    {"contract_ref": CANDIDATE_CONTRACT_REF.as_dict(), "model_use": False,
     "production": False, "selected_service": False},
)


def _set(*groups: Any) -> tuple[ExactRef, ...]:
    return tuple(sorted(
        {ref for group in groups for ref in group}, key=lambda ref: ref.key
    ))


def _verify(
    *, cell: str, composition: AnalyticalCompositionResult,
    model_rule: PositionedSubjectPossibilityModelRule,
    source_release_ref: ExactRef, requested_replay_grade: str,
) -> PossibilitySliceEvidence:
    _require(cell in _ALLOWED_CELLS, "CELL_OUT_OF_SCOPE", "only q1/q2 source-free XOR")
    _require(type(composition) is AnalyticalCompositionResult,
             "NOT_C1_OWNER_RESULT", "requires an actual typed C1 result")
    _require(type(model_rule) is PositionedSubjectPossibilityModelRule,
             "MODEL_RULE_MISMATCH", "requires the typed accepted F8 rule")
    _require(type(source_release_ref) is ExactRef, "RELEASE_NOT_EXACT",
             "an exact source-C11 release is required")
    _require(requested_replay_grade == M2_REPLAY_GRADE,
             "REPLAY_GRADE_OVERCLAIM", "only historical explanation is supported")
    _require(composition.analytical_state == "SUPPORTED"
             and composition.producer_fact_state == "SUPPORTED",
             "C1_NATIVE_NONPOSITIVE", "no C1 geometry may be generated from a negative")
    _require(composition.composed_result_identity_hash
             == semantic_hash(composition.identity_material()),
             "C1_IDENTITY_DRIFT", "C1 composed hash not derived from actual content")
    ev = composition.possibility_slice_evidence_or_null
    _require(type(ev) is PossibilitySliceEvidence and ev.evidence_state == "SUPPORTED",
             "C1_NATIVE_NONPOSITIVE", "the supported producer evidence is required")
    _require(composition.consumer_result_or_null is not None,
             "NO_ACTUAL_CONSUMER_RESULT", "C1 must have invoked its exact consumer")
    _require(composition.consumer_model_rule_hash == model_rule.rule_hash,
             "MODEL_RULE_MISMATCH", "computed model rule differs from supplied exact rule")
    _require(composition.release_refs == (source_release_ref,)
             and ev.release_ref == source_release_ref,
             "SOURCE_RELEASE_MISMATCH", "source-C11 release does not match C1")
    _require(composition.source_universe_refs == (ev.source_universe_ref,)
             and ev.source_universe_ref in model_rule.source_universe_refs,
             "SOURCE_UNIVERSE_MISMATCH", "no cross-source/implicit pooling")
    _require(len(composition.ordered_target_refs) == 1
             and composition.ordered_target_refs[0] == ev.target_ref,
             "TARGET_TOPOLOGY_MISMATCH", "single exact C target only")
    count, denom = _ALLOWED_CELLS[cell]
    _require(len(ev.retained_conditioner_ids) == count
             and composition.raw_denominator_support == denom
             and ev.raw_support == denom,
             "RISK_CONDITION_MISMATCH", "q1/q2 conditioned denominator/arity drift")
    _require(len(composition.denominator_member_refs) == denom
             and len(set(composition.denominator_member_refs)) == denom,
             "SAME_RESPONDENT_RISK_MISMATCH", "no guessed or duplicated denominator")
    _require(bool(composition.risk_set_member_refs)
             and bool(composition.provenance_refs) and bool(composition.authority_refs)
             and bool(ev.provenance_refs) and bool(ev.authority_refs),
             "MISSING_PROVENANCE_OR_AUTHORITY", "no empty authority/risk/provenance")
    geom = canonicalize(ev.geometry)
    _require(geom["denominator"]["raw_denominator_support"] == denom
             and geom["denominator"]["risk_set_ref"] == composition.risk_set_ref.as_dict()
             and geom["denominator"]["denominator_member_refs"]
             == [r.as_dict() for r in composition.denominator_member_refs]
             and geom["cells"] == canonicalize(composition.complete_cell_geometry),
             "C1_GEOMETRY_MISMATCH", "geometry or risk was substituted")
    # The full C1 evidence preimage is rehashed independently, not merely its label.
    preimage = {
        "schema": EVIDENCE_PREIMAGE_SCHEMA,
        "contract_id": EVIDENCE_CONTRACT_ID,
        "source_universe_ref": ev.source_universe_ref.as_dict(),
        "release_ref": ev.release_ref.as_dict(),
        "target_ref": ev.target_ref.as_dict(),
        "retained_conditioner_ids": list(ev.retained_conditioner_ids),
        "evidence_state": ev.evidence_state, "geometry": ev.geometry,
        "raw_support": ev.raw_support, "uncertainty_state": ev.uncertainty_state,
        "provenance_refs": [x.as_dict() for x in ev.provenance_refs],
        "authority_refs": [x.as_dict() for x in ev.authority_refs],
    }
    _require(ev.evidence_ref.content_hash == semantic_hash(preimage),
             "EVIDENCE_PREIMAGE_MISMATCH", "actual C1 evidence content hash drift")
    _require(ev.target_ref == composition.ordered_target_refs[0]
             and composition.condition_binding_witness_ref_or_hash in ev.provenance_refs
             and composition.producer_query_ref in ev.provenance_refs
             and composition.producer_predicate_ref in ev.provenance_refs
             and composition.producer_fact_ref in ev.provenance_refs,
             "PROVENANCE_MISMATCH", "producer/conditioner ancestry missing")
    # A self-consistent caller object remains a development object, never an
    # authenticated external producer. G1 origin custody is a separate boundary.
    return ev


@dataclass(frozen=True)
class C1CandidateReleaseView:
    """M2 object identities and B5 STAGEABLE, not CURRENT, lifecycle subject."""

    cell: str
    composition: AnalyticalCompositionResult
    evidence: PossibilitySliceEvidence
    repository: M2.M2Repository
    subject: M2.ProducerSubject
    release: M2.ReleaseCore
    closures: dict[str, M2.ClosureObject]
    lifecycle_subject: B5.LearnedProductLifecycleSubject
    analytical_registration: AnalyticalProductRegistration
    analytical_registry: AnalyticalDependencyRegistry
    replay_claim: AnalyticalReplayClaim
    grade: str = DEVELOPMENT_GRADE
    authorizing: bool = False


def build_source_free_c1_release(
    *, cell: str, composition: AnalyticalCompositionResult,
    model_rule: PositionedSubjectPossibilityModelRule,
    source_release_ref: ExactRef,
    requested_replay_grade: str = M2_REPLAY_GRADE,
) -> C1CandidateReleaseView:
    """Wrap actual C1 product into existing M2 and stageable B5 protocol.

    Does not mutate a B5 executor, issue an AuthoritySnapshot, publish, or
    select current. Development-only refs are always derived internally.
    """
    ev = _verify(
        cell=cell, composition=composition, model_rule=model_rule,
        source_release_ref=source_release_ref,
        requested_replay_grade=requested_replay_grade,
    )
    anatomy = _ref(
        "C1ImmutableSemanticAnatomy", "anatomy",
        {"c1": composition.identity_material(), "evidence": ev.evidence_ref.as_dict(),
         "rule_hash": model_rule.rule_hash},
    )
    subject_ref = _ref(
        "C1ImmutableDevelopmentProduct", "product",
        {"anatomy": anatomy.as_dict(), "contract": CANDIDATE_CONTRACT_REF.as_dict(),
         "cell": cell, "source_release": source_release_ref.as_dict()},
    )
    source_scope_ref = _ref(
        "C1SourceFreeSelectionScopeCandidate", "scope",
        {"source": source_release_ref.as_dict(), "universe": ev.source_universe_ref.as_dict(),
         "target": ev.target_ref.as_dict(), "contract": CANDIDATE_CONTRACT_REF.as_dict()},
    )
    model_rule_ref = _ref("C1ModelRuleIdentity", "rule-hash",
                          {"model_rule_hash": model_rule.rule_hash})
    auths = tuple(sorted(set(composition.authority_refs + ev.authority_refs),
                         key=lambda a: a.key))
    transports = _set(tuple(
        _ref("C1AuthorityTransport", "authority",
             {"authority_ref": authority.as_dict()}) for authority in auths
    ))
    dependencies = _set(
        composition.dependency_refs, composition.provenance_refs, ev.provenance_refs,
        (composition.producer_fact_ref, ev.evidence_ref, source_release_ref)
    )
    determinants = _set(
        dependencies, composition.replay_refs,
        (composition.producer_query_ref, composition.producer_predicate_ref,
         composition.consumer_query_ref, composition.risk_set_ref,
         composition.measure_basis_ref, composition.condition_binding_witness_ref_or_hash,
         ev.source_universe_ref, ev.target_ref, model_rule_ref),
        composition.risk_set_member_refs, composition.denominator_member_refs,
        composition.subject_condition_preimage_refs,
        composition.producer_predicate_leaf_refs, composition.pairing_ground_truth_refs,
        composition.discovery_receipt_refs, composition.recursive_handoff_refs,
        composition.recursive_lineage_refs,
    )
    _require(bool(composition.replay_refs), "MISSING_REPLAY_ROOT",
             "actual C1 replay root must exist")
    root = composition.replay_refs[0]
    claim = AnalyticalReplayClaim(
        claim_id=f"{CONTRACT_ID}:{cell}:{subject_ref.content_hash}",
        replayed_product_ref=subject_ref,
        retained_determinant_refs=determinants,
        producer_route=composition.producer_route,
        producer_path="rawlsing_next.pre553_analytical_composition.compose_positioned_subject_possibility",
        authority_refs=auths,
        expected_output_identity_hash=composition.composed_result_identity_hash,
        actual_replay_mechanism=MECHANISM_HISTORICAL_NARRATION,
        replay_grade=REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY,
        limitations=("NO_FRESH_PROCESS_RECOMPUTATION",
                     "NO_INDEPENDENT_PRODUCER_ISSUER", "NO_B5_CURRENT", "NO_G0B"),
        replay_protocol_ref=root,
        deterministic_order_or_tie_rule_refs=(),
        replay_state="REPLAY_UNRESOLVED",
    )
    claim_ref = _ref("C103RHistoricalReplayClaim", "replay-claim", claim.material())
    explanation = _set(
        (subject_ref, CANDIDATE_CONTRACT_REF, ev.evidence_ref, anatomy, claim_ref),
        composition.provenance_refs, ev.provenance_refs,
    )
    registry = AnalyticalDependencyRegistry()
    registration = AnalyticalProductRegistration(
        product_ref=subject_ref,
        product_identity_hash=anatomy.content_hash,
        determinant_authority_refs=auths,
        determinant_exact_refs=determinants,
        dependency_edges_from=dependencies,
    )
    registry.register(registration)
    # Existing C1-03R graph constructor. It does not confer currentness.
    registry.build_graph()

    repo = M2.M2Repository()
    subject = M2.register_producer_subject(
        repo, subject_ref=subject_ref,
        subject_kind="IMMUTABLE_LEARNED_PRODUCT",
        producer_contract_ref=CANDIDATE_CONTRACT_REF,
        typed_state=composition.analytical_state, semantic_anatomy_ref=anatomy,
        required_authority_refs=transports,
        required_dependency_refs=dependencies,
        required_determinant_refs=determinants,
        required_replay_refs=(root, claim_ref),
        required_explanation_refs=_set((ev.evidence_ref, anatomy, claim_ref),
                                       composition.provenance_refs, ev.provenance_refs),
    )
    closures = {
        "AUTHORITY": M2.constitute_closure(
            repo, closure_kind="AUTHORITY",
            member_refs=_set((CANDIDATE_CONTRACT_REF,), transports),
            metadata={"authority_ref_preimages": [a.as_dict() for a in auths],
                      "issuer": None, "non_authorizing": True}),
        "DEPENDENCY": M2.constitute_closure(
            repo, closure_kind="DEPENDENCY", member_refs=dependencies),
        "DETERMINANT": M2.constitute_closure(
            repo, closure_kind="DETERMINANT", member_refs=determinants),
        "REPLAY_RECONSTRUCTION": M2.constitute_closure(
            repo, closure_kind="REPLAY_RECONSTRUCTION", member_refs=(root, claim_ref),
            metadata={"replay_grade": M2_REPLAY_GRADE,
                      "c1_03r_replay_grade": claim.replay_grade,
                      "actual_mechanism": claim.actual_replay_mechanism,
                      "fresh_process_proved": False, "authorizing": False}),
        "EXPLANATION_LINEAGE": M2.constitute_closure(
            repo, closure_kind="EXPLANATION_LINEAGE", member_refs=explanation),
    }
    release = M2.constitute_release(
        repo, release_subject_ref=subject.ref,
        release_subject_kind=subject.subject_kind,
        semantic_producer_contract_ref=CANDIDATE_CONTRACT_REF,
        authority_closure_ref=closures["AUTHORITY"].ref,
        dependency_closure_ref=closures["DEPENDENCY"].ref,
        determinant_closure_ref=closures["DETERMINANT"].ref,
        replay_reconstruction_ref=closures["REPLAY_RECONSTRUCTION"].ref,
        explanation_lineage_ref=closures["EXPLANATION_LINEAGE"].ref,
    )
    lifecycle_subject = B5.LearnedProductLifecycleSubject(
        release_ref=release.ref, product_ref=subject.ref,
        product_family_ref=CANDIDATE_FAMILY_REF,
        producer_owner_ref=CANDIDATE_OWNER_REF,
        producer_contract_ref=CANDIDATE_CONTRACT_REF,
        semantic_projection_hash=anatomy.content_hash,
        authority_snapshot_refs=auths,
        direct_dependency_refs=dependencies,
        determinant_refs=determinants,
        determinant_set_hash=semantic_hash([x.as_dict() for x in determinants]),
        replay_root_ref=root, selection_scope_ref=source_scope_ref,
        build_or_release_receipt_refs=(release.ref,),
        producer_permission_ceiling_ref=PERMISSION_CEILING_REF,
        replay_state=B5_REPLAY_STATE,
        rebuild_state="REBUILD_BLOCKED",
        materialization_class="MANDATORY_RETAINED_CAPITAL",
    )
    _require(release.release_subject_ref == lifecycle_subject.product_ref
             and release.ref == lifecycle_subject.release_ref
             and release.semantic_producer_contract_ref == lifecycle_subject.producer_contract_ref,
             "RELEASE_PROTOCOL_MISMATCH", "M2/B5 subject or producer diverged")
    return C1CandidateReleaseView(
        cell=cell, composition=composition, evidence=ev, repository=repo,
        subject=subject, release=release, closures=closures,
        lifecycle_subject=lifecycle_subject, analytical_registration=registration,
        analytical_registry=registry, replay_claim=claim,
    )


__all__ = [
    "CONTRACT_ID", "DEVELOPMENT_GRADE", "CANDIDATE_CONTRACT_REF",
    "CANDIDATE_OWNER_REF", "CANDIDATE_FAMILY_REF", "PERMISSION_CEILING_REF",
    "C1ImmutableReleaseHold", "C1CandidateReleaseView", "build_source_free_c1_release",
]
