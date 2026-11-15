"""Scalable TEST_ONLY sourcefree 13-family fixture for PYAT #1006.

The fixture emits the same typed C11 family objects accepted by S2-C's
SourcefreeDirectI02Sections interface.  It is synthetic and sourcefree; it does
not read or impersonate original respondent data, and it is not a source/body
bridge for #997.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
from types import MappingProxyType
from typing import Any, Iterator, Mapping

from rawlsing_next._pre553_direct_i02_sourcefree import (
    SourcefreeDirectI02Sections,
    direct_sections_from_candidate,
)
from rawlsing_next.pre553_c11_ingest import (
    C11SourceReleaseCandidate,
    INGEST_CONTRACT_VERSION,
    SourceReleaseManifest,
    build_candidate_replay_manifest,
    ingest_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import (
    QuestionVariableBinding,
    RespondentIdentity,
    TypedAbsence,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    RoutingEligibilityFact,
    WeightMeasureFact,
)
from rawlsing_next.tests.test_pre553_empirical_query import _auth, _h, _ref


QUESTIONS = ("A", "B", "C", "D", "MR")
RESPONSE_QUESTIONS = ("A", "B", "C", "D", "MR")
REPEATED_QUESTION = "MR"
SPARSE_QUESTION = "D"
RISK_NAME = "R"


def _ceil_div(value: int, divisor: int) -> int:
    return (value + divisor - 1) // divisor


@dataclass(frozen=True)
class ShapeSpec:
    name: str
    respondents: int
    include_weights: bool = False
    missing_mod: int = 17
    sparse_mod: int = 11
    repeated_mod: int = 13
    skew_events: int = 0
    mutate_respondent: int = -1
    mutate_question: str = ""
    tag: str = "PYAT1006"

    def __post_init__(self) -> None:
        if self.respondents < 1:
            raise ValueError("positive respondent count required")
        if not self.name or not self.tag:
            raise ValueError("name and tag required")

    @property
    def sparse_count(self) -> int:
        return _ceil_div(self.respondents, self.sparse_mod)

    @property
    def repeated_count(self) -> int:
        return _ceil_div(self.respondents, self.repeated_mod)

    @property
    def event_count(self) -> int:
        return (
            3 * self.respondents
            + self.sparse_count
            + 2 * self.repeated_count
            + self.skew_events
        )

    @property
    def routing_count(self) -> int:
        return len(QUESTIONS) * self.respondents

    @property
    def weight_count(self) -> int:
        return self.respondents if self.include_weights else 0

    def family_counts(self) -> dict[str, int]:
        return {
            "EmpiricalUniverse": 1,
            "RespondentIdentity": self.respondents,
            "QuestionVariableBinding": len(QUESTIONS),
            "RespondentEvent": self.event_count,
            "RoutingEligibilityFact": self.routing_count,
            "EmpiricalCoordinateFact": self.respondents,
            "WeightMeasureFact": self.weight_count,
            "AuthoritySnapshot": 5 if self.include_weights else 4,
            "SourceUniverseRelation": 0,
            "EmpiricalPredicateReplayBinding": 0,
            "ComparatorReplayBinding": 0,
            "DiscoveryBranchReplayBinding": 0,
            "StructuralAdmissionReplayBinding": 0,
            "ReplayManifest": 1,
        }


@dataclass(frozen=True)
class FixtureContext:
    shape: ShapeSpec
    universe: EmpiricalUniverse
    authorities: tuple[AuthoritySnapshot, ...]
    source_auth: AuthoritySnapshot
    routing_auth: AuthoritySnapshot
    coord_auth: AuthoritySnapshot
    replay_auth: AuthoritySnapshot
    weight_auth: AuthoritySnapshot | None
    question_bindings: tuple[QuestionVariableBinding, ...]
    qrefs: Mapping[str, ExactRef]
    crefs: Mapping[str, ExactRef]
    risk_ref: ExactRef
    tie_order_ref: ExactRef
    manifest: SourceReleaseManifest

    @property
    def tag(self) -> str:
        return self.shape.tag

    @property
    def source_sha256(self) -> str:
        return self.manifest.source_artifact_content_hash

    def _respondent(self, index: int) -> RespondentIdentity:
        return RespondentIdentity(
            empirical_universe_ref=self.universe.ref,
            respondent_key=f"R{index:08d}",
            source_native_respondent_key_ref_or_typed_absence=_ref(
                "SOURCE_RESPONDENT", f"{self.tag}-{index:08d}"
            ),
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        )

    def iter_universes(self) -> Iterator[EmpiricalUniverse]:
        yield self.universe

    def iter_authorities(self) -> Iterator[AuthoritySnapshot]:
        yield from self.authorities

    def iter_questions(self) -> Iterator[QuestionVariableBinding]:
        yield from self.question_bindings

    def iter_respondents(self) -> Iterator[RespondentIdentity]:
        for index in range(self.shape.respondents):
            yield self._respondent(index)

    def _value(self, question: str, index: int) -> int:
        if question == "A":
            value = index % 2
        elif question == "B":
            value = (index // 3) % 2
        elif question == "C":
            value = (index % 2) ^ ((index // 3) % 2)
        elif question == "D":
            value = (index // 5) % 2
        else:
            raise KeyError(question)
        if index == self.shape.mutate_respondent and question == self.shape.mutate_question:
            value = 1 - value
        return value

    def _event(
        self, respondent: RespondentIdentity, index: int, question: str,
        *, topology: str = "SCALAR_SINGULAR", occurrence: int = 0,
        value: int | None,
    ) -> RespondentEvent:
        state = "SUBSTANTIVE_RESPONSE" if value is not None else "MISSING"
        group = f"GROUP-{self.tag}-{index:08d}-{question}"
        event_id = (
            f"{index:08d}-{question}-{occurrence}"
            if topology == "REPEATED_EVENT"
            else f"{index:08d}-{question}"
        )
        fields = (
            {"kind": "REPEATED_EVENT", "multiplicity_index": occurrence, "rank": occurrence + 1}
            if topology == "REPEATED_EVENT"
            else {"kind": "SCALAR_SINGULAR", "index": 0}
        )
        return RespondentEvent(
            typed_state=state,
            authority_snapshot_refs=(self.source_auth.authority_ref,),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_ref(
                "REPLAY_ROOT", f"event-{self.tag}-{index:08d}-{question}-{occurrence}"
            ),
            empirical_universe_ref=self.universe.ref,
            scoped_respondent_ref=respondent.ref,
            native_question_ref=self.qrefs[question],
            canonical_question_ref_if_authorized=None,
            component_or_subitem_ref=None,
            event_group_id=group,
            response_event_id_or_deterministic_index=event_id,
            raw_response_value=None if value is None else str(value),
            canonical_response_value_if_authorized=None,
            value_transform_authority_ref=None,
            response_topology_ref=_ref("TOPOLOGY", f"{self.tag}-{question}-{topology}"),
            multiplicity_order_rank_fields=fields,
            response_state=state,
        )

    def iter_events(self) -> Iterator[RespondentEvent]:
        for index in range(self.shape.respondents):
            respondent = self._respondent(index)
            for question in ("A", "B", "C"):
                value = self._value(question, index)
                if question == "B" and index % self.shape.missing_mod == 0:
                    value = None
                yield self._event(respondent, index, question, value=value)
            if index % self.shape.sparse_mod == 0:
                yield self._event(
                    respondent, index, SPARSE_QUESTION,
                    value=self._value(SPARSE_QUESTION, index),
                )
            if index % self.shape.repeated_mod == 0:
                for occurrence in range(2):
                    yield self._event(
                        respondent, index, REPEATED_QUESTION,
                        topology="REPEATED_EVENT", occurrence=occurrence,
                        value=(index + occurrence) % 3,
                    )
            if index == 0:
                for occurrence in range(self.shape.skew_events):
                    yield self._event(
                        respondent, index, REPEATED_QUESTION,
                        topology="REPEATED_EVENT",
                        occurrence=2 + occurrence,
                        value=(index + occurrence) % 3,
                    )

    def _routing_state(self, index: int, question: str) -> str:
        if question == SPARSE_QUESTION:
            return (
                "ELIGIBLE_APPLICABLE"
                if index % self.shape.sparse_mod == 0
                else "NOT_ELIGIBLE"
            )
        if question == REPEATED_QUESTION:
            return (
                "ELIGIBLE_APPLICABLE"
                if (index % self.shape.repeated_mod == 0
                    or (index == 0 and self.shape.skew_events))
                else "NOT_ELIGIBLE"
            )
        return "ELIGIBLE_APPLICABLE"

    def iter_routing(self) -> Iterator[RoutingEligibilityFact]:
        for index in range(self.shape.respondents):
            respondent = self._respondent(index)
            for question in QUESTIONS:
                state = self._routing_state(index, question)
                yield RoutingEligibilityFact(
                    typed_state=state,
                    authority_snapshot_refs=(self.routing_auth.authority_ref,),
                    dependency_refs=(),
                    producer_replay_locator_or_reference_root=_ref(
                        "REPLAY_ROOT", f"routing-{self.tag}-{index:08d}-{question}"
                    ),
                    empirical_universe_ref=self.universe.ref,
                    scoped_respondent_ref=respondent.ref,
                    question_or_target_ref=self.qrefs[question],
                    risk_set_ref=self.risk_ref,
                    routing_rule_ref=_ref("ROUTING_RULE", f"{self.tag}-{question}"),
                    applicability_state=state,
                    routing_state=state,
                    parent_predicate_refs=(),
                    member_set_replay_ref=_ref(
                        "MEMBER_SET", f"{self.tag}-{RISK_NAME}-{question}-{state}"
                    ),
                )

    def iter_coordinates(self) -> Iterator[EmpiricalCoordinateFact]:
        for index in range(self.shape.respondents):
            respondent = self._respondent(index)
            value = "A" if index % 3 == 0 else "B"
            yield EmpiricalCoordinateFact(
                typed_state="OBSERVED_COORDINATE",
                authority_snapshot_refs=(self.coord_auth.authority_ref,),
                dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref(
                    "REPLAY_ROOT", f"coord-{self.tag}-{index:08d}-G"
                ),
                empirical_universe_ref=self.universe.ref,
                scoped_respondent_ref=respondent.ref,
                native_coordinate_ref=self.crefs["G"],
                canonical_coordinate_ref_if_authorized=None,
                raw_coordinate_value=value,
                canonical_coordinate_value_if_authorized=None,
                unit_category_taxonomy_ref=_ref("UNIT_TAXONOMY", f"{self.tag}-G"),
                effective_or_reference_time="2026-01",
                coordinate_state="OBSERVED_COORDINATE",
                normalization_crosswalk_authority_ref=None,
                source_semantic_authority_ref=self.coord_auth.authority_ref,
            )

    def iter_weights(self) -> Iterator[WeightMeasureFact]:
        if not self.shape.include_weights:
            return
        if self.weight_auth is None:
            raise ValueError("weight authority missing")
        for index in range(self.shape.respondents):
            respondent = self._respondent(index)
            yield WeightMeasureFact(
                typed_state="WEIGHT_VALID_AUTHORIZED",
                authority_snapshot_refs=(self.weight_auth.authority_ref,),
                dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref(
                    "REPLAY_ROOT", f"weight-{self.tag}-{index:08d}"
                ),
                empirical_universe_ref=self.universe.ref,
                scoped_respondent_ref=respondent.ref,
                weight_basis_id="W",
                exact_weight_value_representation=str(1 + (index % 4)),
                weight_state="WEIGHT_VALID_AUTHORIZED",
                weight_source_ref=_ref("WEIGHT_SOURCE", f"{self.tag}-W"),
                design_authority_ref=self.weight_auth.authority_ref,
                estimand_authority_ref=self.weight_auth.authority_ref,
                normalization_or_recalibration_rule_ref=None,
                effective_scope_ref=_ref("SCOPE", f"{self.tag}-W"),
            )

    def typed_absences(self) -> Mapping[str, TypedAbsence]:
        result: dict[str, TypedAbsence] = {
            "SourceUniverseRelation": TypedAbsence("DISTINCT_BY_DEFAULT"),
            "EmpiricalPredicateReplayBinding": TypedAbsence("NOT_APPLICABLE"),
            "ComparatorReplayBinding": TypedAbsence("DEFERRED"),
            "DiscoveryBranchReplayBinding": TypedAbsence("DEFERRED"),
            "StructuralAdmissionReplayBinding": TypedAbsence("NOT_APPLICABLE"),
        }
        if not self.shape.include_weights:
            result["WeightMeasureFact"] = TypedAbsence("NOT_APPLICABLE")
        return MappingProxyType(result)

    def direct_sections(self) -> SourcefreeDirectI02Sections:
        absent = tuple(self.typed_absences())
        sections = {
            "EmpiricalUniverse": self.iter_universes(),
            "RespondentIdentity": self.iter_respondents(),
            "QuestionVariableBinding": self.iter_questions(),
            "RespondentEvent": self.iter_events(),
            "RoutingEligibilityFact": self.iter_routing(),
            "EmpiricalCoordinateFact": self.iter_coordinates(),
            "WeightMeasureFact": self.iter_weights(),
            "AuthoritySnapshot": self.iter_authorities(),
            "SourceUniverseRelation": iter(()),
            "EmpiricalPredicateReplayBinding": iter(()),
            "ComparatorReplayBinding": iter(()),
            "DiscoveryBranchReplayBinding": iter(()),
            "StructuralAdmissionReplayBinding": iter(()),
        }
        if absent:
            for family in absent:
                sections[family] = iter(())
        return SourcefreeDirectI02Sections(
            manifest=self.manifest,
            sections=MappingProxyType(sections),
            typed_absences=self.typed_absences(),
            replay_protocol_authority_ref=self.replay_auth.authority_ref,
            replay_protocol_version="1.0.0",
            deterministic_tie_order_rules_ref=self.tie_order_ref,
        )

    def materialize(self) -> dict[str, tuple[Any, ...]]:
        return {
            "EmpiricalUniverse": tuple(self.iter_universes()),
            "RespondentIdentity": tuple(self.iter_respondents()),
            "QuestionVariableBinding": tuple(self.iter_questions()),
            "RespondentEvent": tuple(self.iter_events()),
            "RoutingEligibilityFact": tuple(self.iter_routing()),
            "EmpiricalCoordinateFact": tuple(self.iter_coordinates()),
            "WeightMeasureFact": tuple(self.iter_weights()),
            "AuthoritySnapshot": tuple(self.iter_authorities()),
            "SourceUniverseRelation": (),
            "EmpiricalPredicateReplayBinding": (),
            "ComparatorReplayBinding": (),
            "DiscoveryBranchReplayBinding": (),
            "StructuralAdmissionReplayBinding": (),
        }

    def candidate(self) -> C11SourceReleaseCandidate:
        sections = self.materialize()
        candidate = C11SourceReleaseCandidate(
            source_release_manifest=self.manifest,
            empirical_universes=sections["EmpiricalUniverse"],
            respondent_identities=sections["RespondentIdentity"],
            question_variable_bindings=sections["QuestionVariableBinding"],
            respondent_events=sections["RespondentEvent"],
            routing_eligibility_facts_or_exact_rules=sections["RoutingEligibilityFact"],
            empirical_coordinate_facts=sections["EmpiricalCoordinateFact"],
            weight_measure_facts_or_typed_absence=(
                sections["WeightMeasureFact"]
                if self.shape.include_weights
                else TypedAbsence("NOT_APPLICABLE")
            ),
            authority_snapshots=sections["AuthoritySnapshot"],
            source_universe_relations_or_explicit_distinct_default=TypedAbsence(
                "DISTINCT_BY_DEFAULT"
            ),
            predicate_replay_bindings_when_retained_objects_require_them=TypedAbsence(
                "NOT_APPLICABLE"
            ),
            comparator_replay_bindings_or_typed_deferred_state=TypedAbsence("DEFERRED"),
            discovery_branch_replay_bindings_or_typed_deferred_state=TypedAbsence("DEFERRED"),
            structural_admission_replay_bindings_or_typed_not_applicable_state=TypedAbsence(
                "NOT_APPLICABLE"
            ),
            candidate_replay_manifest=None,
        )
        replay = build_candidate_replay_manifest(
            candidate,
            replay_protocol_authority_ref=self.replay_auth.authority_ref,
            deterministic_tie_order_rules_ref=self.tie_order_ref,
            replay_protocol_version="1.0.0",
        )
        return replace(candidate, candidate_replay_manifest=replay)

    def native_oracle(self) -> tuple[Any, ExactRef]:
        candidate = self.candidate()
        repository = C11Repository()
        result = ingest_c11_source_release(candidate, repository)
        if not result.accepted:
            raise AssertionError(result.errors)
        return repository, result.release_ref

    def direct_sections_from_materialized_candidate(self) -> SourcefreeDirectI02Sections:
        candidate = self.candidate()
        replay = candidate.candidate_replay_manifest
        return direct_sections_from_candidate(
            replace(candidate, candidate_replay_manifest=None),
            replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
            replay_protocol_version=replay.replay_protocol_version,
            deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
        )


def build_context(shape: ShapeSpec) -> FixtureContext:
    tag = shape.tag
    source_auth = _auth(
        f"source-{tag}",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
    )
    routing_auth = _auth(
        f"routing-{tag}",
        "ROUTING_RISK_SET",
        families=("RoutingEligibilityFact@1.0.0",),
    )
    coord_auth = _auth(
        f"coord-{tag}",
        "COORDINATE_SEMANTICS",
        families=("EmpiricalCoordinateFact@1.0.0",),
    )
    replay_auth = _auth(
        f"replay-{tag}",
        "REPLAY_PROTOCOL",
        families=("ReplayReceipt@1.0.0",),
    )
    weight_auth = (
        _auth(
            f"weight-{tag}",
            "WEIGHT_DESIGN_ESTIMAND",
            families=("WeightMeasureFact@1.0.0",),
        )
        if shape.include_weights
        else None
    )
    authorities = (source_auth, coord_auth, routing_auth, replay_auth)
    if weight_auth is not None:
        authorities = (*authorities, weight_auth)

    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"universe-{tag}"),
        raw_source_identity=f"RAW-{tag}",
        source_family="SURVEY",
        study_product_release=f"STUDY-{tag}/REL-1",
        instrument_release=f"INST-{tag}",
        country_geography="US",
        sampling_geography="US-NATIONAL",
        raw_wave="W1",
        canonical_wave_if_governed=None,
        field_or_reference_time="2026-01",
        target_population_and_sample_frame="ADULTS",
        sampling_design_regime="DESIGN-PYAT1006",
        respondent_namespace=f"NS-{tag}",
        source_artifact_import_lineage=f"SOURCE-LINEAGE-{tag}",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    qrefs = MappingProxyType({
        question: _ref("QUESTION_NATIVE", f"{tag}-{question}")
        for question in QUESTIONS
    })
    crefs = MappingProxyType({"G": _ref("COORDINATE_NATIVE", f"{tag}-G")})
    question_bindings = tuple(
        QuestionVariableBinding(
            empirical_universe_ref=universe.ref,
            native_question_ref=qrefs[question],
            instrument_question_version="1",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=source_auth.authority_ref,
            topology_authority_ref=source_auth.authority_ref,
        )
        for question in QUESTIONS
    )
    source_hash = _h(
        "source-artifact:"
        + tag
        + f":{shape.mutate_respondent}:{shape.mutate_question}"
    )
    counts = shape.family_counts()
    manifest = SourceReleaseManifest(
        source_artifact_id=f"SOURCE-{tag}",
        source_artifact_content_hash=source_hash,
        source_family_id="SURVEY",
        study_product_id=f"STUDY-{tag}",
        release_id=f"REL-{tag}",
        instrument_release_id=f"INST-{tag}",
        ingest_contract_version=INGEST_CONTRACT_VERSION,
        declared_universe_refs=(universe.ref,),
        declared_authority_snapshot_refs=tuple(a.authority_ref for a in authorities),
        declared_record_counts_by_logical_family=counts,
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:test:i03:source-snapshot:{tag}", source_hash
        ),
    )
    return FixtureContext(
        shape=shape,
        universe=universe,
        authorities=authorities,
        source_auth=source_auth,
        routing_auth=routing_auth,
        coord_auth=coord_auth,
        replay_auth=replay_auth,
        weight_auth=weight_auth,
        question_bindings=question_bindings,
        qrefs=qrefs,
        crefs=crefs,
        risk_ref=_ref("RISK_SET", f"{tag}-R"),
        tie_order_ref=_ref("ORDER_RULE", "CANONICAL-REF-SORT"),
        manifest=manifest,
    )


def source_descriptor(ctx: FixtureContext) -> dict[str, Any]:
    return {
        "universe": ctx.universe,
        "qrefs": ctx.qrefs,
        "crefs": ctx.crefs,
        "risk_refs": {RISK_NAME: ctx.risk_ref},
        "source_auth": ctx.source_auth,
        "coord_auth": ctx.coord_auth,
        "routing_auth": ctx.routing_auth,
        "authorities": ctx.authorities,
        "respondents": {},
    }


__all__ = [
    "FixtureContext",
    "QUESTIONS",
    "REPEATED_QUESTION",
    "RISK_NAME",
    "ShapeSpec",
    "build_context",
    "source_descriptor",
]
