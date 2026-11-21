"""Narrow q103 recorded-response operation constructor and reader admission.

This is an isolated candidate.  It consumes a held owner decision and an exact
saved-stream operation descriptor, constructs the existing PRE553 predicate and
query objects, and binds only a scoped read-time recorded-membership routing
projection for the native I03 session.  It never edits the saved estate, asks
eligibility, or mints a permanent authority/permanent ref.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from rawlsing_next.pre553_anvil_stream_native_i03 import (
    VerifiedAnvilStreamEstate,
    _stream_exact_universe,
)
from rawlsing_next.pre553_anvil_stream_issuance import (
    HeldStreamIssuanceDecision,
    issue_and_execute_stream_i03,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalQuerySpec,
    ExactRef,
    RoutingEligibilityFact,
    exact_ref,
    make_empirical_predicate,
    semantic_hash,
)


class RecordedResponseError(ValueError):
    """The held recorded-response operation cannot be lawfully materialized."""


@dataclass(frozen=True)
class HeldRecordedOperation:
    """Exact source decision; no source semantics are inferred from stream rows."""

    owner_decision_sha256: str
    source_id: str
    source_root: str
    release_root: str
    universe_root: str
    replay_root: str
    question_ref: ExactRef
    authorized_operation: str
    allowed_raw_codes: tuple[str, ...]
    interpretation: tuple[tuple[str, str], ...]
    authorities: tuple[AuthoritySnapshot, ...]
    query_authority_ref: AuthorityRef
    routing_authority_ref: AuthorityRef
    source_authority_ref: AuthorityRef
    recorded_risk_ref: ExactRef
    routing_rule_ref: ExactRef
    member_set_replay_ref: ExactRef
    measure_basis_ref: ExactRef
    response_state_semantics_ref: ExactRef
    target_domain_replay_ref: ExactRef
    predicate_replay_root: ExactRef
    query_replay_root: ExactRef
    approved_nonanswer_states: tuple[str, ...] = ()
    physical_missing_state: str = "SEPARATE_NOT_RECORDED"


def _authority(authorities, ref, label):
    for snapshot in authorities:
        if snapshot.authority_ref == ref:
            return snapshot
    raise RecordedResponseError(f"held {label} authority is absent")


def _recorded_raw(event) -> str | None:
    value = getattr(event, "raw_response_value", None)
    if value is None:
        return None
    text = str(value)
    return text


def build_recorded_operation(
    *,
    estate: VerifiedAnvilStreamEstate,
    operation: HeldRecordedOperation,
    question_ref: ExactRef,
) -> tuple[HeldStreamIssuanceDecision, tuple[RoutingEligibilityFact, ...], int]:
    """Construct predicate/query and a scoped recorded routing projection.

    The operation's allowed codes come only from the held decision.  Recorded
    membership is the distinct exact respondent occurrence with one allowed
    event; a respondent with no event is an explicit nonmember and is tallied
    separately as physical missing.  Unknown codes and duplicate events refuse.
    """
    if type(estate) is not VerifiedAnvilStreamEstate:
        raise RecordedResponseError("exact verified stream estate required")
    if type(operation) is not HeldRecordedOperation:
        raise RecordedResponseError("exact held recorded operation required")
    if question_ref != exact_ref(operation.question_ref, "recorded question"):
        raise RecordedResponseError("recorded question differs from held operation")
    universe_ref = _stream_exact_universe(estate.i02.universe)
    if universe_ref != _stream_exact_universe(operation.universe_root):
        raise RecordedResponseError("recorded universe differs from held operation")
    if estate.i02.source != operation.source_root:
        raise RecordedResponseError("recorded source differs from held operation")
    if estate.i02.release != operation.release_root:
        raise RecordedResponseError("recorded release differs from held operation")
    if estate.i02.replay != operation.replay_root:
        raise RecordedResponseError("recorded replay differs from held operation")

    allowed = {str(code) for code in operation.allowed_raw_codes}
    if len(allowed) != len(operation.allowed_raw_codes):
        raise RecordedResponseError("duplicate allowed raw code")
    respondents = tuple(
        sorted(estate.iter_family("RespondentIdentity"), key=lambda x: x.ref.key)
    )
    events = tuple(
        sorted(
            (event for event in estate.iter_family("RespondentEvent")
             if exact_ref(event.native_question_ref) == question_ref),
            key=lambda x: x.ref.key,
        )
    )
    by_respondent: dict[str, list] = {}
    for event in events:
        respondent_ref = exact_ref(event.scoped_respondent_ref, "event respondent")
        by_respondent.setdefault(respondent_ref.key, []).append(event)

    recorded: dict[str, object] = {}
    missing: list[object] = []
    for respondent in respondents:
        occurrences = by_respondent.get(respondent.ref.key, ())
        if len(occurrences) > 1:
            raise RecordedResponseError("duplicate recorded respondent occurrence")
        if not occurrences:
            missing.append(respondent)
            continue
        event = occurrences[0]
        raw = _recorded_raw(event)
        if raw not in allowed:
            raise RecordedResponseError("unknown recorded raw code")
        recorded[respondent.ref.key] = event
    if not recorded:
        raise RecordedResponseError("no recorded respondent membership")

    query_authority = _authority(
        operation.authorities, operation.query_authority_ref, "query"
    )
    routing_authority = _authority(
        operation.authorities, operation.routing_authority_ref, "routing"
    )
    source_authority = _authority(
        operation.authorities, operation.source_authority_ref, "source"
    )

    members = tuple(
        sorted((respondent.ref for respondent in respondents), key=lambda ref: ref.key)
    )
    branch_ast = {
        "op": "LEAF",
        "leaf_type": "DERIVED_BRANCH_COHORT",
        "branch_definition_id": "BRANCH-RECORDED-ALL",
        "resolved_predicate_hash_or_exact_membership_ref": operation.member_set_replay_ref,
        "parent_ancestry_ref": ExactRef(
            "BRANCH_PARENT", operation.member_set_replay_ref.object_id,
            operation.member_set_replay_ref.content_hash,
        ),
        "branch_algorithm_authority_ref": query_authority.authority_ref,
        "branch_membership_replay_ref": operation.member_set_replay_ref,
        "branch_source_scope_ref": universe_ref,
        "exact_member_respondent_refs": members,
    }
    predicate = make_empirical_predicate(
        predicate_ast=branch_ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(query_authority.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=operation.predicate_replay_root,
        grammar_authority_ref=query_authority.authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=(operation.recorded_risk_ref,),
        scope_refs=(universe_ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(
            ExactRef(
                "OPERATOR_SEMANTICS",
                "BOOLEAN-AND-OR-NOT",
                semantic_hash({"operator": "BOOLEAN-AND-OR-NOT"}),
            ),
        ),
    )
    included_states = frozenset({
        "SUBSTANTIVE_RESPONSE", "DK", "REFUSAL", "SOURCE_SPECIFIC_SPECIAL",
    })
    query = EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(query_authority.authority_ref,),
        dependency_refs=(predicate.ref,),
        producer_replay_locator_or_reference_root=operation.query_replay_root,
        target_refs=(question_ref,),
        target_arity_and_topology={
            "arity": 1,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": [{
                "target_ref": question_ref,
                "topology": "SCALAR_SINGULAR",
                "domain": list(operation.allowed_raw_codes),
                "target_domain_replay_ref": operation.target_domain_replay_ref,
                "topology_authority_refs": [source_authority.authority_ref],
                "response_semantic_authority_refs": [source_authority.authority_ref],
                "included_states": sorted(included_states),
            }],
        },
        condition_predicate_ref=predicate.ref,
        risk_set_ref=operation.recorded_risk_ref,
        empirical_universe_refs=(universe_ref,),
        scope_refs=(universe_ref,),
        measure_basis_ref=operation.measure_basis_ref,
        requested_output_grain={
            "source_scope_mode": "SINGLE_UNIVERSE",
            "measure_kind": "RAW",
            "risk_set_type": "CUSTOM_GOVERNED_RISK_SET",
            "response_state_semantics_ref": operation.response_state_semantics_ref,
            "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
        },
        query_authority_refs=(query_authority.authority_ref,),
    )

    recorded_routing = []
    for respondent in respondents:
        event = recorded.get(respondent.ref.key)
        state = "ELIGIBLE_APPLICABLE" if event is not None else "NOT_ELIGIBLE"
        dependency = (event.ref,) if event is not None else ()
        replay_ref = ExactRef(
            "MEMBER_SET_REPLAY",
            "recorded-" + operation.owner_decision_sha256 + "-" + respondent.ref.content_hash,
            semantic_hash({
                "owner_decision_sha256": operation.owner_decision_sha256,
                "respondent": respondent.ref.as_dict(),
                "raw_code": _recorded_raw(event) if event is not None else None,
                "state": state,
            }),
        )
        recorded_routing.append(RoutingEligibilityFact(
            typed_state=state,
            authority_snapshot_refs=(routing_authority.authority_ref,),
            dependency_refs=dependency,
            producer_replay_locator_or_reference_root=operation.routing_rule_ref,
            empirical_universe_ref=universe_ref,
            scoped_respondent_ref=respondent.ref,
            question_or_target_ref=question_ref,
            risk_set_ref=operation.recorded_risk_ref,
            routing_rule_ref=operation.routing_rule_ref,
            applicability_state=state,
            routing_state=state,
            parent_predicate_refs=(),
            member_set_replay_ref=replay_ref,
        ))

    decision = HeldStreamIssuanceDecision(
        source_id=operation.source_id,
        source_root=operation.source_root,
        release_root=operation.release_root,
        universe_root=operation.universe_root,
        replay_root=operation.replay_root,
        question_ref=question_ref,
        authorized_operation=operation.authorized_operation,
        authorities=operation.authorities,
        predicate=predicate,
        query=query,
        approved_denominator_ref=operation.recorded_risk_ref,
        approved_response_semantics_ref=operation.response_state_semantics_ref,
        approved_raw_domain=operation.allowed_raw_codes,
        approved_nonanswer_states=operation.approved_nonanswer_states,
    )
    return decision, tuple(recorded_routing), len(missing)


def execute_recorded_response_i03(
    *,
    estate: VerifiedAnvilStreamEstate,
    operation: HeldRecordedOperation,
    decision_verifier,
):
    """Build operation query and execute the existing native I03 once."""
    decision, recorded_routing, missing = build_recorded_operation(
        estate=estate, operation=operation, question_ref=operation.question_ref,
    )
    result = issue_and_execute_stream_i03(
        estate=estate,
        decision=decision,
        decision_verifier=decision_verifier,
        recorded_routing=recorded_routing,
    )
    return result, missing, decision


__all__ = [
    "HeldRecordedOperation",
    "RecordedResponseError",
    "build_recorded_operation",
    "execute_recorded_response_i03",
]
