"""Authority-governed PRE553 predicate composition successor."""
from __future__ import annotations

from typing import Any, Sequence

from rawlsing_next.pre553_empirical_objects import (
    EmpiricalPredicate,
    canonical_json,
    exact_ref,
    make_empirical_predicate,
)
from rawlsing_next.pre553_runtime_authority import Pre553RuntimeAuthoritySet
from rawlsing_next.pre553_discovery_exact import (
    ExactBoundedDiscoveryError,
    _canonical_auths,
    _canonical_refs,
    _derived_ref,
)


def compose_predicates_runtime(
    predicates: Sequence[EmpiricalPredicate],
    *,
    op: str,
    tag_material: Any,
    runtime_authorities: Pre553RuntimeAuthoritySet | None = None,
) -> EmpiricalPredicate:
    if not predicates:
        raise ExactBoundedDiscoveryError("cannot compose empty predicate set")

    grammar_refs = {canonical_json(p.grammar_authority_ref) for p in predicates}
    bindings = {p.same_respondent_binding_semantics for p in predicates}
    if len(grammar_refs) == 1 and len(bindings) == 1:
        if op not in {"AND", "OR"}:
            raise ExactBoundedDiscoveryError("unsupported predicate composition op")
        ast = {"op": op, "children": [p.predicate_ast for p in predicates]}
        return make_empirical_predicate(
            predicate_ast=ast,
            typed_state="PREDICATE_RESOLVED_AUTHORIZED",
            authority_snapshot_refs=_canonical_auths(
                ref for p in predicates for ref in p.authority_snapshot_refs
            ),
            dependency_refs=_canonical_refs(p.ref for p in predicates),
            producer_replay_locator_or_reference_root=_derived_ref(
                "PRE553_I05_PREDICATE_REPLAY_ROOT", "predicate-replay", tag_material
            ),
            grammar_authority_ref=predicates[0].grammar_authority_ref,
            coordinate_question_value_refs=_canonical_refs(
                exact_ref(ref, "coordinate_question_value_ref")
                for p in predicates for ref in p.coordinate_question_value_refs
            ),
            risk_set_refs=_canonical_refs(
                exact_ref(ref, "risk_set_ref") for p in predicates for ref in p.risk_set_refs
            ),
            scope_refs=_canonical_refs(
                exact_ref(ref, "scope_ref") for p in predicates for ref in p.scope_refs
            ),
            same_respondent_binding_semantics=predicates[0].same_respondent_binding_semantics,
            operator_semantics_refs=_canonical_refs(
                exact_ref(ref, "operator_semantics_ref")
                for p in predicates for ref in p.operator_semantics_refs
            ),
        )

    if runtime_authorities is None:
        raise ExactBoundedDiscoveryError(
            "mixed predicates require exact adopted runtime composition authority"
        )
    if op != "AND":
        raise ExactBoundedDiscoveryError(
            "mixed predicate OR/NOT is not granted by exact adopted composition authority"
        )
    try:
        resolution = runtime_authorities.authorize_mixed_predicate_composition(
            predicates, operation=op, tag_material=tag_material
        )
    except Exception as exc:
        raise ExactBoundedDiscoveryError(str(exc)) from exc

    ast = {"op": "AND", "children": [p.predicate_ast for p in predicates]}
    replay_ref = _derived_ref(
        "PRE553_I05_PREDICATE_REPLAY_ROOT",
        "mixed-predicate-replay",
        resolution.replay_material,
    )
    return make_empirical_predicate(
        predicate_ast=ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=_canonical_auths([
            *(ref for p in predicates for ref in p.authority_snapshot_refs),
            resolution.authority_snapshot_ref,
        ]),
        dependency_refs=_canonical_refs(p.ref for p in predicates),
        producer_replay_locator_or_reference_root=replay_ref,
        grammar_authority_ref=resolution.grammar_authority_ref,
        coordinate_question_value_refs=_canonical_refs(
            exact_ref(ref, "coordinate_question_value_ref")
            for p in predicates for ref in p.coordinate_question_value_refs
        ),
        risk_set_refs=_canonical_refs(
            exact_ref(ref, "risk_set_ref") for p in predicates for ref in p.risk_set_refs
        ),
        scope_refs=_canonical_refs(
            exact_ref(ref, "scope_ref") for p in predicates for ref in p.scope_refs
        ),
        same_respondent_binding_semantics=resolution.respondent_binding_semantics,
        operator_semantics_refs=_canonical_refs(
            exact_ref(ref, "operator_semantics_ref")
            for p in predicates for ref in p.operator_semantics_refs
        ),
    )


__all__ = ["compose_predicates_runtime"]
