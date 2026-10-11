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
    AuthorityRef, ExactRef, authority_ref, canonicalize, semantic_hash,
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
# F8E H01/H02 repair: owner-pinned cell identity.
#
# Arity and denominator alone do not identify a conditioned cell. Source-free
# q1 is q(C|A=1) and q2 is q(C|A=1,B=0) over target C. A caller may build a
# genuinely computed C1 composition with the same arity and the same
# denominator (for example q(C|A=0), or the reversed-numerator q(C|A=1,B=1)),
# and the original shape check would have accepted it.
#
# The condition tuple is therefore pinned as a source-visible scientific
# precondition here, and the frozen four-respondent oracle fixes the exact
# ordered C=0 / C=1 numerators so a reversed alien distribution cannot be
# hidden by sorting. This is a stated development precondition, NOT an issued
# authority: it records the native instrument semantics the candidate is scoped
# to and does not grant any operation, model-use or source permission.
_CELL_PRECONDITIONS = {
    "q1": (("RESPONSE", "A", 1),),
    "q2": (("RESPONSE", "A", 1), ("RESPONSE", "B", 0)),
}
_CELL_TARGET = "C"
# Exact owner identities recorded from the accepted C1/query owner path.
_PINNED_CELL_IDENTITY = {
    "q1": {
        "conditions": _CELL_PRECONDITIONS["q1"],
        "target_question": _CELL_TARGET,
        "predicate": "9bdff5e3d9b93b43480b14397dda1e79de89876a5cfd39a0c4807c47440d4289",
        "condition_witness": "7dab39293f831dd8a0bcd04ad9f3d7660838102e21943428d9e518a730b29a4a",
        "target": "454c46970031c7256bd66f76c14afd35b0bb285c958af83d62ffb3755dd4e1e2",
        "target_domain_identity": "72854a7389f125037019b7ec3302c528e4383f7cc82c9ec7e16092545d79a3b3",
        "risk_set": "080132c4e80a767f0eb45a69855c295311bf57741c84decc34349f8d4e82b3b2",
    },
    "q2": {
        "conditions": _CELL_PRECONDITIONS["q2"],
        "target_question": _CELL_TARGET,
        "predicate": "a8b05e75b088822782bb670ef909b0394b740a3e2b8a7ba226b4c5a6e21753c7",
        "condition_witness": "2a3cb5b950c4f88c38e133ad4227ba64dd652527b6860fc1447d29b006beb459",
        "target": "454c46970031c7256bd66f76c14afd35b0bb285c958af83d62ffb3755dd4e1e2",
        "target_domain_identity": "72854a7389f125037019b7ec3302c528e4383f7cc82c9ec7e16092545d79a3b3",
        "risk_set": "080132c4e80a767f0eb45a69855c295311bf57741c84decc34349f8d4e82b3b2",
    },
}
# Frozen HQ260/HQ280 four-respondent XOR oracle, ordered by C value.
_FROZEN_CELL_NUMERATORS = {"q1": (1, 1), "q2": (0, 1)}
_FROZEN_CELL_DENOMINATOR = {"q1": 2, "q2": 1}


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
    # --- F8E H01: owner-pinned condition/target identity, not shape alone ---
    # Pinned from the accepted C1/query owner path over the HQ260/HQ280 XOR
    # fixture. These are recorded native identities for this development scope,
    # NOT an issued authority and NOT a new scientific claim.
    pinned = _PINNED_CELL_IDENTITY[cell]
    _require(composition.producer_predicate_ref.content_hash == pinned["predicate"],
             "CELL_PREDICATE_IDENTITY_MISMATCH",
             f"cell {cell} is pinned to predicate {pinned['predicate']}; a correctly "
             "shaped wrong-condition composition is not the admitted cell")
    _require(composition.condition_binding_witness_ref_or_hash.content_hash
             == pinned["condition_witness"],
             "CELL_CONDITION_WITNESS_MISMATCH",
             "condition binding witness does not match the pinned native condition")
    _require(composition.ordered_target_refs[0].content_hash == pinned["target"],
             "CELL_TARGET_IDENTITY_MISMATCH",
             "target must be the pinned native target C for this candidate")
    _require(composition.target_domain_identity == pinned["target_domain_identity"],
             "CELL_TARGET_DOMAIN_MISMATCH",
             "target domain identity does not match the pinned native target")
    # --- F8E H02: fixed-value numerator oracle (order-sensitive) ---
    observed = tuple(
        cell["raw_numerator_support"]
        for cell in sorted(
            ev.geometry["cells"],
            key=lambda c: (0, int(c["cell"][0])) if str(c["cell"][0]).isdigit()
            else (1, str(c["cell"][0])),
        )
    )
    _require(observed == _FROZEN_CELL_NUMERATORS[cell],
             "CELL_NUMERATOR_VALUE_MISMATCH",
             f"cell {cell} numerator profile {observed} does not equal the frozen "
             f"native oracle {_FROZEN_CELL_NUMERATORS[cell]}; identical denominator "
             "and support labels are not sufficient")
    _require(composition.raw_denominator_support == _FROZEN_CELL_DENOMINATOR[cell],
             "CELL_DENOMINATOR_VALUE_MISMATCH",
             "denominator does not equal the frozen native oracle")
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
    # --- F8E H03: risk member cross-preimage ---
    # The risk-set member identity must agree across the native evidence
    # geometry and the composition, not merely by risk-set id and by
    # denominator length. A rehashed composition can otherwise carry substituted
    # or missing respondent members behind an unchanged risk-set reference.
    _require(geom["denominator"].get("risk_set_member_refs")
             == [r.as_dict() for r in composition.risk_set_member_refs],
             "RISK_MEMBER_PREIMAGE_MISMATCH",
             "evidence geometry and composition disagree on risk-set member identity")
    _require(bool(composition.risk_set_member_refs)
             and len(composition.risk_set_member_refs) >= denom,
             "RISK_MEMBER_SET_INCOMPLETE",
             "risk-set member identity does not cover the admitted denominator")
    # --- F8E H03 (continued): pinned risk-set identity per admitted cell ---
    # The fixture's risk set is shared by both admitted cells, so a swapped
    # ``risk_set_ref`` is a no-op and cannot be detected by rehashing alone.
    # The admitted cell's risk-set identity is therefore pinned explicitly.
    _require(composition.risk_set_ref.content_hash == _PINNED_CELL_IDENTITY[cell]["risk_set"],
             "RISK_SET_IDENTITY_MISMATCH",
             f"cell {cell} is pinned to risk set "
             f"{_PINNED_CELL_IDENTITY[cell]['risk_set']}")
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
    analytical_graph: Any
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
    # --- F8E H04: consumed model/walkback authorities are closure members ---
    # The consumed PositionedSubjectPossibilityModelRule carries mandatory
    # model and walkback authorities. Representing them only through the
    # model-rule hash leaves them absent from the AUTHORITY closure and from
    # any authority edge. They are retained here as exact, separate authority
    # identities so revocation/changed-authority affected-set semantics apply.
    model_authority = model_rule.model_authority_ref
    walkback_authority = model_rule.walkback_authority_ref
    _require(model_authority is not None and walkback_authority is not None,
             "MISSING_CONSUMED_MODEL_AUTHORITY",
             "the consumed model rule must expose exact model and walkback authorities")
    auths = tuple(sorted(
        {authority_ref(a, "authority_ref")
         for a in tuple(composition.authority_refs) + tuple(ev.authority_refs)}
        | {authority_ref(model_authority, "model_authority_ref"),
           authority_ref(walkback_authority, "walkback_authority_ref")},
        key=lambda a: a.key,
    ))
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
    # --- F8E H05: every determinant identity becomes a real dependency edge ---
    # The accepted registry only emits edges from ``dependency_edges_from``; it
    # does not traverse ``determinant_exact_refs``. Declaring the full
    # determinant set as the edge source is what actually makes replay and
    # changed-authority affected-set propagation include the model-rule ref
    # and the other non-dependency determinant ancestors.
    _require(set(determinants) >= set(dependencies),
             "DETERMINANT_EDGE_SET_INVALID",
             "determinant closure must contain its dependency closure")
    registration = AnalyticalProductRegistration(
        product_ref=subject_ref,
        product_identity_hash=anatomy.content_hash,
        determinant_authority_refs=auths,
        determinant_exact_refs=determinants,
        dependency_edges_from=determinants,
    )
    registry.register(registration)
    # Existing C1-03R graph constructor. It does not confer currentness.
    c103r_graph = registry.build_graph()
    # (kept: the C1-03R graph is the accepted owner graph, not a substitute)
    _require(len(c103r_graph.dependency_edges) == len(determinants),
             "C103R_GRAPH_EDGE_INCOMPLETE",
             "C1-03R graph did not emit an edge for every retained determinant")
    _require(subject_ref in c103r_graph.affected(auths),
             "C103R_AFFECTED_SET_INCOMPLETE",
             "authority change must propagate to the registered product")

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
        analytical_registry=registry, analytical_graph=c103r_graph,
        replay_claim=claim,
    )


__all__ = [
    "CONTRACT_ID", "DEVELOPMENT_GRADE", "CANDIDATE_CONTRACT_REF",
    "CANDIDATE_OWNER_REF", "CANDIDATE_FAMILY_REF", "PERMISSION_CEILING_REF",
    "C1ImmutableReleaseHold", "C1CandidateReleaseView", "build_source_free_c1_release",
]
