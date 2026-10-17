"""Generic PRE-V3 progressive world/empirical possibility court (TEST_ONLY).

NOT AN ADOPTED N10W OWNER. This candidate deliberately composes *actual*
N10E provider objects (or C1-composed results, after competent qualification)
without recalculating probabilities, inventing joints, or assigning actors.

World predicates choose which already-qualified conditional QUESTION is
currently applicable. They NEVER modify the empirical denominator/geometry
or turn objective eligibility into an individual's response prediction.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_analytical_composition import AnalyticalCompositionResult
from rawlsing_next.pre553_empirical_possibility_provider import (
    EmpiricalPossibilitySliceProviderResult,
    PROVIDER_STATE_EXACT,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    PositionedSubjectPossibilityQuery,
)

CONTRACT = "PE_GENERIC_PROGRESSIVE_WORLD_SITUATED_POSSIBILITY_TEST_ONLY@1"
GRADE = "TEST_ONLY_COMPOSITION__NOT_N9_CURRENT__NOT_EE14_MODEL_ISSUED"
STATES = {"SELECTED", "UNRESOLVED", "WORLD_BLOCKED", "AMBIGUOUS", "REFUSED"}
FORBIDDEN_KINDS = {
    "GENERATED_PARENT", "CONCEPTION", "PARTNER_IDENTITY", "RELATIONSHIP",
    "HOUSEHOLD_PERSONA", "DESIRE", "LOVE", "MEMORY", "WOUND", "ENNEAGRAM",
    "ACTOR_PSYCHE", "V3_ACTOR", "V2_VOICE",
}


class GenericPossibilityRefusal(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise GenericPossibilityRefusal(code)


def _ref(ref: ExactRef) -> Mapping[str, Any]:
    _require(isinstance(ref, ExactRef), "EXACT_REF_REQUIRED")
    return ref.as_dict()


@dataclass(frozen=True)
class WorldFact:
    fact_ref: ExactRef
    predicate_ref: ExactRef
    value_ref: ExactRef
    effective_from: int
    effective_through: int
    authorized_use: str = "TEST_ONLY_CONTEXT"
    def material(self) -> Mapping[str, Any]:
        return {
            "fact_ref": _ref(self.fact_ref), "predicate_ref": _ref(self.predicate_ref),
            "value_ref": _ref(self.value_ref), "effective_from": self.effective_from,
            "effective_through": self.effective_through, "authorized_use": self.authorized_use
        }


@dataclass(frozen=True)
class WorldSnapshot:
    snapshot_ref: ExactRef
    subject_ref: ExactRef
    geography_ref: ExactRef
    as_of_year: int
    publication_year: int
    selection_year: int
    currentness_state: str
    facts: tuple[WorldFact, ...]
    grade: str = GRADE
    def material(self) -> Mapping[str, Any]:
        return {
            "snapshot_ref": _ref(self.snapshot_ref), "subject_ref": _ref(self.subject_ref),
            "geography_ref": _ref(self.geography_ref),
            "as_of_year": self.as_of_year,
            "publication_year": self.publication_year,
            "selection_year": self.selection_year,
            "currentness_state": self.currentness_state,
            "grade": self.grade,
            "facts": [f.material() for f in self.facts]
        }


@dataclass(frozen=True)
class WorldCondition:
    condition_id: str
    predicate_ref: ExactRef
    expected_value_ref: ExactRef
    expected_world_fact_ref: ExactRef
    def material(self) -> Mapping[str, Any]:
        return {
            "condition_id": self.condition_id,
            "predicate_ref": _ref(self.predicate_ref),
            "expected_value_ref": _ref(self.expected_value_ref),
            "expected_world_fact_ref": _ref(self.expected_world_fact_ref),
        }


@dataclass(frozen=True)
class EmpiricalOption:
    option_id: str
    consumer_query: PositionedSubjectPossibilityQuery
    computed_provider: EmpiricalPossibilitySliceProviderResult | None
    world_conditions: tuple[WorldCondition, ...]
    generated_binding_echo_ref: ExactRef | None = None
    computed_c1: AnalyticalCompositionResult | None = None

    def __post_init__(self) -> None:
        _require(bool(self.option_id), "OPTION_ID_REQUIRED")
        _require(bool(self.world_conditions), "WORLD_CONDITION_REQUIRED")
        _require(len({c.condition_id for c in self.world_conditions}) ==
                 len(self.world_conditions), "DUPLICATE_WORLD_CONDITION")
        _require((self.computed_provider is None) != (self.computed_c1 is None),
                 "ONE_COMPUTED_OWNER_PATH_REQUIRED")


@dataclass(frozen=True)
class GenericRequest:
    request_id: str
    consumer_id: str
    subject_ref: ExactRef
    world: WorldSnapshot
    options: tuple[EmpiricalOption, ...]
    expected_as_of_year: int
    requested_kind: str = "EMPIRICAL_POSSIBILITY_ONLY"
    claim_current_n9: bool = False


def _checked_material(
    *,
    option: EmpiricalOption,
    evidence: Any,
    result: Any,
    producer_fact_ref: ExactRef,
    receipt_ref: ExactRef | None,
    producer_route: str,
) -> Mapping[str, Any]:
    query = option.consumer_query
    _require(evidence is not None and result is not None,
             "ONLY_PRODUCER_GENERATED_EVIDENCE_ALLOWED")
    _require(result.result_state == "EXACT_SUPPORTED" and
             result.exact_geometry is not None,
             "NO_EXACT_SUPPORTED_CONDITIONAL")
    _require(evidence.evidence_ref == result.exact_evidence_ref,
             "EVIDENCE_CONSUMER_RESULT_IDENTITY_MISMATCH")
    _require(evidence.target_ref == query.target_ref and
             evidence.source_universe_ref == query.source_universe_ref and
             evidence.release_ref == query.release_ref,
             "SOURCE_TARGET_RELEASE_MISMATCH")
    _require(evidence.retained_conditioner_ids == query.conditioner_ids,
             "CONDITIONER_GRAIN_MISMATCH")
    _require(evidence.raw_support is not None and evidence.raw_support > 0,
             "NO_POSITIVE_SOURCE_SUPPORT")
    return {
        "query_ref": query.ref.as_dict(),
        "producer_route": producer_route,
        "provider_receipt_ref": None if receipt_ref is None else receipt_ref.as_dict(),
        "producer_fact_ref": producer_fact_ref.as_dict(),
        "evidence_ref": evidence.evidence_ref.as_dict(),
        "source_universe_ref": query.source_universe_ref.as_dict(),
        "release_ref": query.release_ref.as_dict(),
        "target_ref": query.target_ref.as_dict(),
        "conditioner_ids": list(query.conditioner_ids),
        "raw_support": evidence.raw_support,
        "uncertainty_state": evidence.uncertainty_state,
        "geometry": result.exact_geometry,
        "result_hash": result.result_hash,
        "epistemic_ceiling": "SOURCE_FREE_FIXTURE_ONLY__NOT_PERSONAL_PREDICTION",
    }


def _check_producer(option: EmpiricalOption) -> Mapping[str, Any]:
    """Reuse existing N10E single-binding or C1 exact multi-binding producer.

    Never infer C1 authorization from a schema: in an operative successor the
    competent source/operation issuer must supply exact C1 target/risk/weight,
    same-respondent/joint and model-use authority. This probe is TEST_ONLY.
    """
    query = option.consumer_query
    if option.computed_c1 is not None:
        c = option.computed_c1
        _require(isinstance(c, AnalyticalCompositionResult),
                 "ONLY_REAL_C1_COMPOSITION_RESULT_ACCEPTED")
        _require(c.analytical_state == "SUPPORTED" and
                 c.producer_fact_state == "SUPPORTED",
                 "C1_FACT_NOT_SUPPORTED")
        _require(c.consumer_query_ref == query.ref,
                 "QUERY_C1_IDENTITY_MISMATCH")
        _require(query.release_ref in c.release_refs and
                 query.source_universe_ref in c.source_universe_refs,
                 "C1_RELEASE_UNIVERSE_MISMATCH")
        evidence = c.possibility_slice_evidence_or_null
        _require(evidence is not None and
                 c.raw_denominator_support == evidence.raw_support,
                 "C1_DENOMINATOR_IDENTITY_MISMATCH")
        return _checked_material(
            option=option, evidence=evidence,
            result=c.consumer_result_or_null,
            producer_fact_ref=c.producer_fact_ref,
            receipt_ref=None,
            producer_route=c.producer_route,
        )

    p = option.computed_provider
    _require(isinstance(p, EmpiricalPossibilitySliceProviderResult),
             "ONLY_REAL_N10E_PROVIDER_RESULT_ACCEPTED")
    _require(p.provider_state == PROVIDER_STATE_EXACT and
             p.generated_evidence_or_null is not None and
             p.consumer_result_or_null is not None,
             "NO_COMPUTED_SUPPORTED_EVIDENCE")
    _require(p.provider_receipt.generated_evidence_identity_is_producer_derived,
             "HANDWRITTEN_EVIDENCE_FORBIDDEN")
    _require(p.provider_receipt.consumer_query_ref == query.ref,
             "QUERY_PROVIDER_IDENTITY_MISMATCH")
    _require(p.provider_receipt.generated_evidence_ref ==
             p.generated_evidence_or_null.evidence_ref,
             "EVIDENCE_PROVIDER_IDENTITY_MISMATCH")
    _require(p.provider_receipt.consumer_result_identity_hash ==
             p.consumer_result_or_null.result_hash,
             "CONSUMER_PROVIDER_IDENTITY_MISMATCH")
    return _checked_material(
        option=option, evidence=p.generated_evidence_or_null,
        result=p.consumer_result_or_null,
        producer_fact_ref=p.provider_receipt.producer_fact_ref,
        receipt_ref=p.receipt_ref, producer_route=p.provider_receipt.provider_route,
    )


def _world_facts(world: WorldSnapshot) -> Mapping[str, WorldFact]:
    ids = [f.predicate_ref.key for f in world.facts]
    _require(len(ids) == len(set(ids)), "DUPLICATE_WORLD_PREDICATE")
    return {f.predicate_ref.key: f for f in world.facts}


def _check_world(request: GenericRequest) -> None:
    w = request.world
    _require(request.requested_kind == "EMPIRICAL_POSSIBILITY_ONLY" and
             request.requested_kind not in FORBIDDEN_KINDS,
             "ACTOR_OR_FOREIGN_ONTOLOGY_FORBIDDEN")
    _require(not request.claim_current_n9, "UNISSUED_N9_CURRENT")
    _require(w.grade == GRADE, "REAL_WORLD_PROMOTION_FORBIDDEN")
    _require(w.currentness_state == "CURRENT_AT_SELECTED_AS_OF",
             "WORLD_CURRENTNESS_NOT_CURRENT")
    _require(w.subject_ref == request.subject_ref,
             "SUBJECT_SCOPE_MISMATCH")
    _require(w.as_of_year == request.expected_as_of_year,
             "WORLD_AS_OF_MISMATCH")
    _require(w.publication_year <= w.selection_year and
             w.as_of_year <= w.selection_year,
             "FOUR_CLOCKS_PUBLICATION_AS_OF_SELECTION_CONFLICT")
    _require(bool(request.options), "NO_EMPIRICAL_OPTIONS")
    _require(len({o.option_id for o in request.options}) == len(request.options),
             "DUPLICATE_OPTION")


def _matches(world: WorldSnapshot, condition: WorldCondition,
             facts: Mapping[str, WorldFact]) -> tuple[bool, str]:
    fact = facts.get(condition.predicate_ref.key)
    if fact is None:
        return False, "WORLD_PREDICATE_UNAVAILABLE"
    if not (fact.effective_from <= world.as_of_year <= fact.effective_through):
        return False, "WORLD_FACT_OUTSIDE_EFFECTIVE_TIME"
    if fact.authorized_use != "TEST_ONLY_CONTEXT":
        return False, "WORLD_FACT_USE_UNAUTHORIZED"
    if fact.fact_ref != condition.expected_world_fact_ref:
        return False, "WORLD_FACT_IDENTITY_MISMATCH"
    if fact.value_ref != condition.expected_value_ref:
        return False, "WORLD_FACT_VALUE_MISMATCH"
    return True, "EXACT_TEST_ONLY_WORLD_CONDITION_MATCH"


def evaluate_generic_progressive(request: GenericRequest) -> Mapping[str, Any]:
    """Proof of generic composition; not a newly authorized source or world owner.

    Each stage narrows the applicable option set. A world change can change the
    selected *computed empirical* slice, but never change that slice's numbers.
    World ineligibility does not destroy minority/alternative empirical cells.
    """
    _check_world(request)
    facts = _world_facts(request.world)
    steps: list[dict[str, Any]] = []
    candidate_ids = {o.option_id for o in request.options}
    option_map = {o.option_id: o for o in request.options}
    all_evidence = {o.option_id: _check_producer(o) for o in request.options}
    # Different competing queries may have different target or condition roles,
    # but source-universe/release crossjoins are NEVER implicit. Separate
    # candidate products from distinct releases require their own EE authority.
    exact_source_releases = {
        (o.consumer_query.source_universe_ref.key,
         o.consumer_query.release_ref.key)
        for o in request.options
    }
    _require(len(exact_source_releases) == 1,
             "CROSS_SOURCE_OR_RELEASE_OPTION_POOL_FORBIDDEN")
    # The consumer supplies its *own* actor-owned criterion as an echo if needed;
    # this service does not create it or infer that a person's survey answer exists.
    for o in request.options:
        if o.generated_binding_echo_ref is not None:
            _ref(o.generated_binding_echo_ref)
    max_depth = max(len(o.world_conditions) for o in request.options)
    steps.append({
        "stage": 0, "kind": "UNCONDITIONED_CANDIDATE_SET",
        "possible_option_ids": sorted(candidate_ids),
        "world_fact_refs_consulted": [],
    })
    for i in range(max_depth):
        stage_outcomes: dict[str, Any] = {}
        retained: set[str] = set()
        for oid in sorted(candidate_ids):
            o = option_map[oid]
            if i >= len(o.world_conditions):
                retained.add(oid)
                stage_outcomes[oid] = "NO_FURTHER_CONDITION"
                continue
            c = o.world_conditions[i]
            ok, reason = _matches(request.world, c, facts)
            stage_outcomes[oid] = reason
            if ok:
                retained.add(oid)
        candidate_ids = retained
        steps.append({
            "stage": i + 1, "kind": "ORDERED_WORLD_CONDITION",
            "possible_option_ids": sorted(candidate_ids),
            "condition_outcomes": stage_outcomes,
            "world_fact_refs_consulted": sorted({
                c.expected_world_fact_ref.key
                for o in request.options
                if i < len(o.world_conditions)
                for c in (o.world_conditions[i],)
            }),
        })
    state = ("WORLD_BLOCKED" if not candidate_ids else
             "AMBIGUOUS" if len(candidate_ids) > 1 else "SELECTED")
    selected = next(iter(candidate_ids)) if state == "SELECTED" else None
    selected_evidence = all_evidence[selected] if selected is not None else None
    # Preserve ALL computed minority/counterpattern cells, even from options
    # rendered inapplicable by the world. Do not multiply probabilities by gates.
    material = {
        "contract": CONTRACT, "grade": GRADE,
        "request_id": request.request_id, "consumer_id": request.consumer_id,
        "subject_ref": request.subject_ref.as_dict(),
        "world_snapshot_ref": request.world.snapshot_ref.as_dict(),
        "world_snapshot_hash": semantic_hash(request.world.material()),
        "world_as_of_year": request.world.as_of_year,
        "world_publication_year": request.world.publication_year,
        "world_selection_year": request.world.selection_year,
        "world_effective_bounds": [
            [f.effective_from, f.effective_through] for f in request.world.facts
        ],
        "status": state, "selected_option_id": selected,
        "progressive_steps": steps,
        "selected_computed_empirical_evidence": selected_evidence,
        "all_computed_empirical_evidence": all_evidence,
        "generated_binding_echo_refs": [
            o.generated_binding_echo_ref.as_dict()
            for o in request.options if o.generated_binding_echo_ref is not None
        ],
        "world_to_empirical_semantics": (
            "WORLD_SELECTS_EXACT_ALREADY_COMPUTED_QUERY"
            "__NO_NEW_DENOMINATOR_OR_PROBABILITY_ARITHMETIC"
        ),
        "joint_or_multi_conditioner_measurement": (
            "ONLY_WHERE_EXISTING_C1_EXACT_PRODUCER_GRANTED"
        ),
        "actor_generations": 0, "model_calls": 0,
        "real_world_promotion": False,
    }
    return {**material, "receipt_hash": semantic_hash(material)}


def verify_generic_replay(expected: Mapping[str, Any],
                          request: GenericRequest) -> Mapping[str, Any]:
    actual = evaluate_generic_progressive(request)
    _require(actual == expected, "PROGRESSIVE_REPLAY_MISMATCH")
    return actual
