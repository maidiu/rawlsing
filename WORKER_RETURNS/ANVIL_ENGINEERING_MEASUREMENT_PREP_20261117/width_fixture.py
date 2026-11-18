"""Bounded 600-slot TEST_ONLY geometry extension of the #1006 fixture.

This is a controlled fixture harness, not a product implementation.  It keeps
the accepted base events/coordinates/weights and adds `question_count` native
QuestionVariableBindings plus one RoutingEligibilityFact per respondent per
question.  Extra slots are deliberately NOT dense events: 600 columns is not
assumed to mean 600 events/respondent.  The base A/B/C/D/MR query bundle remains
the query surface; extra slots test geometry/admission/index behavior.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Any, Iterator, Mapping

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, TypedAbsence
from rawlsing_next.pre553_empirical_objects import RoutingEligibilityFact
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec

from fixture_1006 import (
    RISK_NAME, ShapeSpec, build_context, source_descriptor,
)
from query_1006 import build_query_bundle

_CODEC = R5TypedValueCodec()


def _ref(kind: str, object_id: str):
    from fixture_1006 import _ref as base_ref
    return base_ref(kind, object_id)


@dataclass(frozen=True)
class WidthFixture:
    base: Any
    question_count: int
    qrefs: Mapping[str, Any]
    sections: Any
    manifest: Any
    query_bundle: Any

    @property
    def universe(self):
        return self.base.universe

    @property
    def family_counts(self):
        return dict(self.manifest.declared_record_counts_by_logical_family)


def build_width(base: Any, question_count: int) -> WidthFixture:
    if question_count < 5 or question_count > 1300:
        raise ValueError("question_count must be 5..1300 for bounded geometry")
    if question_count == 5:
        bundle = build_query_bundle(base)
        from rawlsing_next._pre553_direct_i02_sourcefree import SourcefreeDirectI02Sections
        sections = SourcefreeDirectI02Sections(
            manifest=base.manifest,
            sections=base.direct_sections().sections,
            typed_absences=base.direct_sections().typed_absences,
            replay_protocol_authority_ref=base.direct_sections().replay_protocol_authority_ref,
            replay_protocol_version=base.direct_sections().replay_protocol_version,
            deterministic_tie_order_rules_ref=base.direct_sections().deterministic_tie_order_rules_ref,
        )
        return WidthFixture(base, 5, base.qrefs, sections, base.manifest, bundle)

    # Keep the accepted five query roles and add geometry slots.
    qrefs = dict(base.qrefs)
    extra = question_count - len(base.qrefs)
    for index in range(extra):
        qrefs[f"W{index:04d}"] = _ref(
            "QUESTION_NATIVE", f"{base.tag}-W{index:04d}")
    qrefs = MappingProxyType(qrefs)
    bindings = list(base.question_bindings)
    for name, ref in list(qrefs.items()):
        if name in base.qrefs:
            continue
        bindings.append(QuestionVariableBinding(
            empirical_universe_ref=base.universe.ref,
            native_question_ref=ref,
            instrument_question_version="1",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=base.source_auth.authority_ref,
            topology_authority_ref=base.source_auth.authority_ref,
        ))
    if len(bindings) != question_count:
        raise AssertionError("question binding count mismatch")

    def extra_routing() -> Iterator[RoutingEligibilityFact]:
        for index in range(base.shape.respondents):
            respondent = base._respondent(index)
            for name, ref in qrefs.items():
                if name in base.qrefs:
                    continue
                yield RoutingEligibilityFact(
                    typed_state="NOT_ELIGIBLE",
                    authority_snapshot_refs=(base.routing_auth.authority_ref,),
                    dependency_refs=(),
                    producer_replay_locator_or_reference_root=_ref(
                        "REPLAY_ROOT",
                        f"routing-{base.tag}-{index:08d}-{name}",
                    ),
                    empirical_universe_ref=base.universe.ref,
                    scoped_respondent_ref=respondent.ref,
                    question_or_target_ref=ref,
                    risk_set_ref=base.risk_ref,
                    routing_rule_ref=_ref("ROUTING_RULE", f"{base.tag}-{name}"),
                    applicability_state="NOT_ELIGIBLE",
                    routing_state="NOT_ELIGIBLE",
                    parent_predicate_refs=(),
                    member_set_replay_ref=_ref(
                        "MEMBER_SET", f"{base.tag}-{RISK_NAME}-{name}-NOT_ELIGIBLE"),
                )

    def routing() -> Iterator[RoutingEligibilityFact]:
        yield from base.iter_routing()
        yield from extra_routing()

    counts = dict(base.manifest.declared_record_counts_by_logical_family)
    counts["QuestionVariableBinding"] = question_count
    counts["RoutingEligibilityFact"] = (
        base.shape.routing_count + extra * base.shape.respondents
    )
    manifest = replace(
        base.manifest, declared_record_counts_by_logical_family=counts)
    from rawlsing_next._pre553_direct_i02_sourcefree import (
        SourcefreeDirectI02Sections,
    )
    sections = SourcefreeDirectI02Sections(
        manifest=manifest,
        sections=MappingProxyType({
            "EmpiricalUniverse": base.iter_universes(),
            "RespondentIdentity": base.iter_respondents(),
            "QuestionVariableBinding": iter(bindings),
            "RespondentEvent": base.iter_events(),
            "RoutingEligibilityFact": routing(),
            "EmpiricalCoordinateFact": base.iter_coordinates(),
            "WeightMeasureFact": base.iter_weights(),
            "AuthoritySnapshot": base.iter_authorities(),
            "SourceUniverseRelation": iter(()),
            "EmpiricalPredicateReplayBinding": iter(()),
            "ComparatorReplayBinding": iter(()),
            "DiscoveryBranchReplayBinding": iter(()),
            "StructuralAdmissionReplayBinding": iter(()),
        }),
        typed_absences=base.typed_absences(),
        replay_protocol_authority_ref=base.replay_auth.authority_ref,
        replay_protocol_version="1.0.0",
        deterministic_tie_order_rules_ref=base.tie_order_ref,
    )
    bundle = build_query_bundle(base)
    return WidthFixture(base, question_count, qrefs, sections, manifest, bundle)


def width_contract(fixture: WidthFixture) -> dict[str, Any]:
    counts = fixture.family_counts
    return {
        "grade": "SOURCEFREE_TEST_ONLY_GEOMETRY_NOT_ECONOMICS",
        "question_count": fixture.question_count,
        "respondents": fixture.base.shape.respondents,
        "event_count": counts["RespondentEvent"],
        "routing_count": counts["RoutingEligibilityFact"],
        "weight_count": counts["WeightMeasureFact"],
        "question_binding_count": counts["QuestionVariableBinding"],
        "dense_event_assumption": False,
        "note": "Extra question slots have routing-only NOT_ELIGIBLE facts; events remain the accepted sparse base. This is not a dense 600-event/respondent workload.",
    }


__all__ = ["WidthFixture", "build_width", "width_contract"]
