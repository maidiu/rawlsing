"""Controlled TEST_ONLY 600-slot sourcefree geometry extension.

This is a fixture harness, not product code.  It keeps the accepted base
A/B/C/D/MR events, coordinates, weights, authorities and query bundle, and adds
native question bindings plus *substantial populated response items* for the
added slots: deterministic 80% valid / 10% typed MISSING / 10% typed NOT_ASKED.
Added slots have a separate TEST_ONLY source-geometry authority; they do not
claim original eligible QUERY issuance or native source rights.

600 columns is NOT assumed to mean 600 events/respondent; the actual cell
pattern is audited and reported.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Any, Iterator, Mapping

from rawlsing_next._pre553_direct_i02_sourcefree import (
    SourcefreeDirectI02Sections,
)
from rawlsing_next.pre553_c11_integrity import (
    QuestionVariableBinding, TypedAbsence,
)
from rawlsing_next.pre553_empirical_objects import (
    RespondentEvent, RoutingEligibilityFact,
)

from fixture_1006 import (
    RISK_NAME, ShapeSpec, _auth, build_context,
)
from query_1006 import build_query_bundle


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
    audit: Mapping[str, Any]
    geometry_authority_ref: Any

    @property
    def universe(self):
        return self.base.universe

    @property
    def family_counts(self):
        return dict(self.manifest.declared_record_counts_by_logical_family)


def build_width(
    base: Any, question_count: int, *, respondents: int | None = None,
) -> WidthFixture:
    if question_count < 5 or question_count > 1300:
        raise ValueError("question_count must be 5..1300 for bounded geometry")
    if respondents is not None and respondents != base.shape.respondents:
        raise ValueError("respondent count is fixed by the base ShapeSpec")
    bundle = build_query_bundle(base)
    if question_count == 5:
        sections = base.direct_sections()
        audit = {
            "added_questions": 0,
            "extra_cells": 0,
            "extra_valid": 0,
            "extra_missing": 0,
            "extra_not_asked": 0,
            "extra_events": 0,
            "total_events": base.shape.event_count,
            "total_routing": base.shape.routing_count,
            "events_per_respondent_mean": base.shape.event_count / base.shape.respondents,
            "note": "base five-role fixture; no added geometry",
        }
        return WidthFixture(
            base, 5, base.qrefs, sections, base.manifest, bundle, audit, None)

    geometry_auth = _auth(
        f"{base.tag}-source-geometry",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=(
            "RespondentEvent@1.0.0",
            "RoutingEligibilityFact@1.0.0",
        ),
    )
    qrefs = dict(base.qrefs)
    added_names = [f"W{index:04d}" for index in range(question_count - len(base.qrefs))]
    for name in added_names:
        qrefs[name] = _ref("QUESTION_NATIVE", f"{base.tag}-{name}")
    qrefs = MappingProxyType(qrefs)

    bindings = list(base.question_bindings)
    for name in added_names:
        bindings.append(QuestionVariableBinding(
            empirical_universe_ref=base.universe.ref,
            native_question_ref=qrefs[name],
            instrument_question_version="1",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=geometry_auth.authority_ref,
            topology_authority_ref=geometry_auth.authority_ref,
        ))
    if len(bindings) != question_count:
        raise AssertionError("question binding count mismatch")

    extra = len(added_names)
    n = base.shape.respondents
    extra_cells = extra * n
    # 0..7 valid, 8 typed MISSING, 9 NOT_ASKED; contiguous modulo cycle gives
    # exact 80/10/10 aggregate at 5950 extra cells.
    valid = len([0 for i in range(n) for q in range(extra)
                 if (i * extra + q) % 10 < 8])
    missing = len([0 for i in range(n) for q in range(extra)
                   if (i * extra + q) % 10 == 8])
    not_asked = extra_cells - valid - missing
    extra_events = valid + missing
    total_events = base.shape.event_count + extra_events
    total_routing = base.shape.routing_count + extra_cells
    per_respondent = []
    for i in range(n):
        count = 0
        for q in range(extra):
            bucket = (i * extra + q) % 10
            count += 1 if bucket < 9 else 0
        per_respondent.append(count)
    # Add the base event counts for the audited per-respondent total.
    base_per = []
    for i in range(n):
        value = 3
        if i % base.shape.sparse_mod == 0:
            value += 1
        if i % base.shape.repeated_mod == 0:
            value += 2
        if i == 0:
            value += base.shape.skew_events
        base_per.append(value)
    per_total = [base_per[i] + per_respondent[i] for i in range(n)]

    def extra_events_iter() -> Iterator[RespondentEvent]:
        for i in range(n):
            respondent = base._respondent(i)
            for q, name in enumerate(added_names):
                bucket = (i * extra + q) % 10
                if bucket == 9:
                    continue
                state = "SUBSTANTIVE_RESPONSE" if bucket < 8 else "MISSING"
                value = str((i + q) % 2) if bucket < 8 else None
                yield RespondentEvent(
                    typed_state=state,
                    authority_snapshot_refs=(geometry_auth.authority_ref,),
                    dependency_refs=(),
                    producer_replay_locator_or_reference_root=_ref(
                        "REPLAY_ROOT",
                        f"event-{base.tag}-{i:04d}-{name}",
                    ),
                    empirical_universe_ref=base.universe.ref,
                    scoped_respondent_ref=respondent.ref,
                    native_question_ref=qrefs[name],
                    canonical_question_ref_if_authorized=None,
                    component_or_subitem_ref=None,
                    event_group_id=f"G-{base.tag}-{i:04d}-{name}",
                    response_event_id_or_deterministic_index=f"{i:04d}-{name}",
                    raw_response_value=value,
                    canonical_response_value_if_authorized=None,
                    value_transform_authority_ref=None,
                    response_topology_ref=_ref(
                        "TOPOLOGY", f"{base.tag}-{name}-SCALAR_SINGULAR"),
                    multiplicity_order_rank_fields={
                        "kind": "SCALAR_SINGULAR", "index": 0,
                    },
                    response_state=state,
                )

    def extra_routing_iter() -> Iterator[RoutingEligibilityFact]:
        for i in range(n):
            respondent = base._respondent(i)
            for q, name in enumerate(added_names):
                bucket = (i * extra + q) % 10
                state = "NOT_ASKED" if bucket == 9 else "ELIGIBLE_APPLICABLE"
                yield RoutingEligibilityFact(
                    typed_state=state,
                    authority_snapshot_refs=(geometry_auth.authority_ref,),
                    dependency_refs=(),
                    producer_replay_locator_or_reference_root=_ref(
                        "REPLAY_ROOT",
                        f"routing-{base.tag}-{i:04d}-{name}",
                    ),
                    empirical_universe_ref=base.universe.ref,
                    scoped_respondent_ref=respondent.ref,
                    question_or_target_ref=qrefs[name],
                    risk_set_ref=base.risk_ref,
                    routing_rule_ref=_ref("ROUTING_RULE", f"{base.tag}-{name}"),
                    applicability_state=state,
                    routing_state=state,
                    parent_predicate_refs=(),
                    member_set_replay_ref=_ref(
                        "MEMBER_SET", f"{base.tag}-{RISK_NAME}-{name}-{state}"),
                )

    def routing() -> Iterator[RoutingEligibilityFact]:
        yield from base.iter_routing()
        yield from extra_routing_iter()

    def events() -> Iterator[RespondentEvent]:
        yield from base.iter_events()
        yield from extra_events_iter()

    def authorities():
        yield from base.iter_authorities()
        yield geometry_auth

    counts = dict(base.manifest.declared_record_counts_by_logical_family)
    counts["QuestionVariableBinding"] = question_count
    counts["RespondentEvent"] = total_events
    counts["RoutingEligibilityFact"] = total_routing
    counts["AuthoritySnapshot"] = len(base.authorities) + 1
    manifest = replace(
        base.manifest,
        declared_record_counts_by_logical_family=counts,
        declared_authority_snapshot_refs=tuple(
            a.authority_ref for a in (*base.authorities, geometry_auth)),
    )
    sections = SourcefreeDirectI02Sections(
        manifest=manifest,
        sections=MappingProxyType({
            "EmpiricalUniverse": base.iter_universes(),
            "RespondentIdentity": base.iter_respondents(),
            "QuestionVariableBinding": iter(bindings),
            "RespondentEvent": events(),
            "RoutingEligibilityFact": routing(),
            "EmpiricalCoordinateFact": base.iter_coordinates(),
            "WeightMeasureFact": base.iter_weights(),
            "AuthoritySnapshot": authorities(),
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
    audit = {
        "added_questions": extra,
        "extra_cells": extra_cells,
        "extra_valid_substantive": valid,
        "extra_typed_missing": missing,
        "extra_typed_not_asked": not_asked,
        "extra_events": extra_events,
        "base_events": base.shape.event_count,
        "total_events": total_events,
        "total_routing": total_routing,
        "total_weights": base.shape.weight_count,
        "total_question_bindings": question_count,
        "events_per_respondent_min": min(per_total),
        "events_per_respondent_max": max(per_total),
        "events_per_respondent_mean": sum(per_total) / n,
        "base_repeated_mr_occurrences": 2 * len([
            i for i in range(n) if i % base.shape.repeated_mod == 0
        ]),
        "deterministic_pattern": "bucket=(respondent*added_questions+q_index)%10; 0-7 valid, 8 MISSING, 9 NOT_ASKED",
        "dense_assumption": False,
        "extra_authority": "TEST_ONLY_SOURCE_GEOMETRY_NOT_ORIGINAL_QUERY_ISSUANCE",
        "query_surface": "base A/B/C/D/MR five operations; added slots load writer/index but are not all queried",
    }
    for key, expected in (
        ("total_events", total_events),
        ("total_routing", total_routing),
        ("total_question_bindings", question_count),
    ):
        if audit[key] != expected:
            raise AssertionError(f"geometry audit mismatch: {key}")
    return WidthFixture(
        base, question_count, qrefs, sections, manifest, bundle, audit,
        geometry_auth.ref if hasattr(geometry_auth, "ref") else geometry_auth.authority_ref,
    )


def width_contract(fixture: WidthFixture) -> dict[str, Any]:
    return {
        "grade": "SOURCEFREE_TEST_ONLY_GEOMETRY_NOT_ECONOMICS",
        "question_count": fixture.question_count,
        "respondents": fixture.base.shape.respondents,
        "family_counts": fixture.family_counts,
        "audit": dict(fixture.audit),
        "note": "Substantial populated response items, but not a native/original survey, not a dense-columns-are-events assumption, and not real-width economics.",
    }


__all__ = ["WidthFixture", "build_width", "width_contract"]
