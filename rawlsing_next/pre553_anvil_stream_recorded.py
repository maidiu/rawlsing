"""Narrow q103 recorded-response operation constructor and reader admission.

This is an isolated candidate.  It consumes a held owner decision and an exact
saved-stream operation descriptor, constructs the existing PRE553 predicate and
query objects, and binds only a scoped read-time recorded-membership routing
projection for the native I03 session.  It never edits the saved estate, asks
eligibility, or mints a permanent authority/permanent ref.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Mapping
import json
import struct

import pyarrow.parquet as pq

from rawlsing_next.pre553_anvil_stream_native_i03 import (
    RecordedRoutingPlan,
    VerifiedAnvilStreamEstate,
    _make_recorded_routing_plan,
    _stream_exact_universe,
)
from rawlsing_next.pre553_anvil_stream_issuance import (
    HeldStreamIssuanceDecision,
    issue_and_execute_stream_i03,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    authority_ref,
    EmpiricalQuerySpec,
    ExactRef,
    RespondentEvent,
    RoutingEligibilityFact,
    canonicalize,
    exact_ref,
    make_empirical_predicate,
    semantic_hash,
)
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec


class RecordedResponseError(ValueError):
    """The held recorded-response operation cannot be lawfully materialized."""

@dataclass(frozen=True)
class RecordedUniverseUse:
    """Operation-scoped historical DEFER use with a backed positive identity."""

    historical_snapshot: AuthoritySnapshot
    positive_snapshot: AuthoritySnapshot
    owner_decision_sha256: str
    operation_document_sha256: str
    source_id: str
    source_root: str
    release_root: str
    universe_root: str
    replay_root: str
    question_ref: ExactRef
    query_ref: ExactRef
    predicate_ref: ExactRef
    operation: str
    risk_ref: ExactRef
    interpretation: tuple[tuple[str, str], ...]
    scope: str | Mapping
    current_verifier: Callable[[], bool]

    def __post_init__(self) -> None:
        if type(self.historical_snapshot) is not AuthoritySnapshot:
            raise RecordedResponseError("historical DEFER snapshot required")
        if type(self.positive_snapshot) is not AuthoritySnapshot:
            raise RecordedResponseError("positive owner use snapshot required")
        if self.historical_snapshot.decision_state != "DEFER":
            raise RecordedResponseError("historical snapshot is not DEFER")
        if self.positive_snapshot.decision_state != "ALLOW":
            raise RecordedResponseError("positive use snapshot is not ALLOW")
        if not callable(self.current_verifier):
            raise RecordedResponseError("mandatory current authority verifier required")
        for value, label in ((self.owner_decision_sha256, "owner decision"), (self.operation_document_sha256, "operation document")):
            if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
                raise RecordedResponseError(f"{label} must be exact sha256")

    def authorize(self, universe, query, predicate) -> tuple[AuthorityRef, AuthorityRef]:
        if self.current_verifier() is not True:
            raise RecordedResponseError("universe use current authority refused")
        exact_universe = exact_ref(universe.ref)
        if exact_universe != _stream_exact_universe(self.universe_root):
            raise RecordedResponseError("universe use is bound to a different universe")
        refs = tuple(authority_ref(ref, "universe authority") for ref in universe.authority_snapshot_refs)
        if self.historical_snapshot.authority_ref not in refs:
            raise RecordedResponseError("historical DEFER identity is absent from universe")
        if self.historical_snapshot.authority_kind != "SOURCE_SEMANTICS_TOPOLOGY":
            raise RecordedResponseError("historical snapshot family mismatch")
        if self.historical_snapshot.scope_envelope.get("semantic_scope") != "EXACT_SOURCE_CODEBOOK_AND_H48_EVIDENCE_ONLY":
            raise RecordedResponseError("historical snapshot scope mismatch")
        scope = self.positive_snapshot.scope_envelope
        if not isinstance(scope, Mapping) or not scope:
            raise RecordedResponseError("positive use scope envelope is mandatory")
        allowed = scope.get("source_universe_refs")
        if allowed is None:
            raise RecordedResponseError("positive use scope has no source_universe_refs")
        if isinstance(allowed, Mapping):
            allowed = (allowed,)
        if not isinstance(allowed, (tuple, list)) or len(allowed) != 1:
            raise RecordedResponseError("positive use scope must name exactly one universe")
        try:
            allowed_ref = exact_ref(allowed[0], "positive use universe ref")
        except Exception as exc:
            raise RecordedResponseError("positive use universe ref is not canonical full ref") from exc
        if allowed_ref != exact_universe:
            raise RecordedResponseError("positive use universe ref differs including hash")
        if isinstance(self.scope, Mapping):
            if canonicalize(scope.get("scope")) != canonicalize(self.scope):
                raise RecordedResponseError("positive use scope differs from held scope")
        elif scope.get("scope") != self.scope:
            raise RecordedResponseError("positive use scope differs from held scope")
        if scope.get("release") not in (None, self.release_root):
            raise RecordedResponseError("positive use release binding mismatch")
        if scope.get("replay_root") not in (None, self.replay_root):
            raise RecordedResponseError("positive use replay binding mismatch")
        if scope.get("source_sha256") not in (None, self.source_root):
            raise RecordedResponseError("positive use source binding mismatch")
        if "recorded_raw_codes" in scope and tuple(str(x) for x in scope["recorded_raw_codes"]) != tuple(str(x) for x, _ in self.interpretation):
            raise RecordedResponseError("positive use code/interpretation mismatch")
        if self.operation not in self.positive_snapshot.governed_operations:
            raise RecordedResponseError("positive use operation mismatch")
        if self.operation not in self.historical_snapshot.governed_operations and self.historical_snapshot.decision_state != "DEFER":
            raise RecordedResponseError("historical operation binding mismatch")
        if query.ref != exact_ref(self.query_ref) or predicate.ref != exact_ref(self.predicate_ref):
            raise RecordedResponseError("universe use query/predicate identity mismatch")
        if exact_ref(query.risk_set_ref) != exact_ref(self.risk_ref):
            raise RecordedResponseError("universe use risk identity mismatch")
        if self.current_verifier() is not True:
            raise RecordedResponseError("universe use current authority revoked")
        return self.historical_snapshot.authority_ref, self.positive_snapshot.authority_ref


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
    transform_ref: ExactRef
    approved_nonanswer_states: tuple[str, ...] = ()
    physical_missing_state: str = "SEPARATE_NOT_RECORDED"


_CODEC = R5TypedValueCodec()


def _unwrap_raw_physical_value(value):
    """Strict typed unwrap of the projected native token wrapper."""
    if isinstance(value, dict) and "$raw_physical_value" in value:
        wrapper = value["$raw_physical_value"]
        if not isinstance(wrapper, dict) or "token" not in wrapper:
            raise RecordedResponseError("invalid raw_physical_value wrapper")
        token = wrapper["token"]
        if not isinstance(token, dict):
            raise RecordedResponseError("invalid raw_physical_value token")
        try:
            decoded = _CODEC.decode(token)
        except Exception as exc:
            raise RecordedResponseError("invalid raw_physical_value token") from exc
        if isinstance(decoded, float) and decoded.is_integer():
            return int(decoded)
        return decoded
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def _authority(authorities, ref, label):
    for snapshot in authorities:
        if snapshot.authority_ref == ref:
            return snapshot
    raise RecordedResponseError(f"held {label} authority is absent")


def _decoded_raw_values(
    estate: VerifiedAnvilStreamEstate, selected_refs: set[str],
) -> dict[str, object]:
    """Decode R5 raw_typed only for exact selected event refs.

    The large event family is never materialized into a raw dictionary; only
    the exact q103-selected refs are decoded from the bounded Parquet batches.
    """
    result: dict[str, object] = {}
    parquet = pq.ParquetFile(estate.directory / "RespondentEvent.parquet")
    try:
        for batch in parquet.iter_batches(
            batch_size=1024, columns=["ref", "raw_typed"],
        ):
            for row in batch.to_pylist():
                if row["ref"] not in selected_refs:
                    continue
                try:
                    encoded = json.loads(row["raw_typed"])
                    result[row["ref"]] = _unwrap_raw_physical_value(
                        _CODEC.decode(encoded)
                    )
                except Exception as exc:
                    raise RecordedResponseError(
                        "stored R5 raw_typed value cannot be decoded exactly"
                    ) from exc
    finally:
        parquet.close()
    return result


def _translate_saved_scalar_topology(fields: Any) -> Any:
    """Translate only the exact, singular saved SCALAR carrier envelope.

    The accepted saved writer records a one-occurrence scalar as SCALAR; the
    q103 target is SCALAR_SINGULAR.  Only the kind and optional zero index may
    be present.  Ordered, repeated, unknown, malformed, and non-singular
    envelopes are returned unchanged so the strict native evaluator refuses
    them; this is not a global topology alias.
    """
    if not isinstance(fields, Mapping) or fields.get("kind") != "SCALAR":
        return fields
    if set(fields) - {"kind", "index"}:
        raise RecordedResponseError(
            "saved scalar topology has unsupported multiplicity/order fields"
        )
    if fields.get("index") not in (None, 0):
        raise RecordedResponseError(
            "saved scalar topology is not the singular zero occurrence"
        )
    translated = dict(fields)
    translated["kind"] = "SCALAR_SINGULAR"
    return translated


def build_recorded_operation(
    *,
    estate: VerifiedAnvilStreamEstate,
    operation: HeldRecordedOperation,
    question_ref: ExactRef,
) -> tuple[HeldStreamIssuanceDecision, RecordedRoutingPlan, dict[str, int]]:
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
    # Resolve the exact operation authority before scanning any saved rows.
    query_authority = _authority(
        operation.authorities, operation.query_authority_ref, "query"
    )
    routing_authority = _authority(
        operation.authorities, operation.routing_authority_ref, "routing"
    )
    source_authority = _authority(
        operation.authorities, operation.source_authority_ref, "source"
    )
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
    selected_event_refs = {event.ref.key for event in events}
    decoded_raw = _decoded_raw_values(estate, selected_event_refs)
    by_respondent: dict[str, list] = {}
    for event in events:
        respondent_ref = exact_ref(event.scoped_respondent_ref, "event respondent")
        by_respondent.setdefault(respondent_ref.key, []).append(event)

    recorded: dict[str, object] = {}
    recorded_raw: dict[str, object] = {}
    system_missing: list[object] = []
    absent: list[object] = []
    for respondent in respondents:
        occurrences = by_respondent.get(respondent.ref.key, ())
        if len(occurrences) > 1:
            raise RecordedResponseError("duplicate recorded respondent occurrence")
        if not occurrences:
            absent.append(respondent)
            continue
        event = occurrences[0]
        if event.ref.key not in decoded_raw:
            raise RecordedResponseError("selected event raw_typed ref is missing")
        raw = decoded_raw[event.ref.key]
        if raw is None:
            system_missing.append(respondent)
            continue
        if type(raw) is bool:
            raise RecordedResponseError("boolean raw code is not a recorded scalar label")
        if str(raw) not in allowed:
            raise RecordedResponseError("unknown recorded raw code")
        recorded[respondent.ref.key] = event
        recorded_raw[respondent.ref.key] = raw
    if not recorded:
        raise RecordedResponseError("no recorded respondent membership")

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
                "domain": [
                    int(code) if code.isdigit() else code
                    for code in operation.allowed_raw_codes
                ],
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
            "recorded_transform_ref": operation.transform_ref,
            "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
        },
        query_authority_refs=(query_authority.authority_ref,),
    )

    event_transforms: dict[str, object] = {}
    for respondent in respondents:
        event = recorded.get(respondent.ref.key)
        if event is None:
            continue
        fields = dict(event.semantic_fields)
        fields.pop("typed_state", None)
        fields["multiplicity_order_rank_fields"] = _translate_saved_scalar_topology(
            fields.get("multiplicity_order_rank_fields")
        )
        fields["raw_response_value"] = recorded_raw[respondent.ref.key]
        fields["response_state"] = "SUBSTANTIVE_RESPONSE"
        fields["canonical_response_value_if_authorized"] = None
        fields["value_transform_authority_ref"] = operation.transform_ref
        transformed = RespondentEvent(
            typed_state="SUBSTANTIVE_RESPONSE",
            authority_snapshot_refs=(operation.source_authority_ref,),
            dependency_refs=(event.ref,),
            producer_replay_locator_or_reference_root=operation.transform_ref,
            **fields,
        )
        event_transforms[event.ref.key] = transformed

    operation_authority_keys = {
        authority.authority_ref.key for authority in operation.authorities
    }
    for transformed in event_transforms.values():
        for ref in transformed.authority_snapshot_refs:
            if authority_ref(ref, "transformed event authority").key not in operation_authority_keys:
                raise RecordedResponseError(
                    "transformed event authority is absent from held operation; "
                    "refuse before index"
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
                "raw_code": recorded_raw.get(respondent.ref.key),
                "state": state,
                "observation": "R5_RAW_TYPED_DECODED",
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
    plan = _make_recorded_routing_plan(
        decision_sha256=operation.owner_decision_sha256,
        source_root=operation.source_root,
        release_root=operation.release_root,
        universe_root=operation.universe_root,
        replay_root=operation.replay_root,
        risk_set_ref=operation.recorded_risk_ref,
        facts_by_key=MappingProxyType({
            (
                fact.scoped_respondent_ref.key if hasattr(fact.scoped_respondent_ref, "key") else exact_ref(fact.scoped_respondent_ref).key,
                exact_ref(fact.question_or_target_ref).key,
                exact_ref(fact.risk_set_ref).key,
            ): (fact,)
            for fact in recorded_routing
        }),
        event_transforms=MappingProxyType(event_transforms),
    )
    missing_counts = {
        "system_missing": len(system_missing),
        "absent": len(absent),
    }
    return decision, plan, missing_counts


def execute_recorded_response_i03(
    *,
    estate: VerifiedAnvilStreamEstate,
    operation: HeldRecordedOperation,
    decision_verifier,
):
    """Build operation query and execute the existing native I03 once."""
    decision, recorded_plan, missing = build_recorded_operation(
        estate=estate, operation=operation, question_ref=operation.question_ref,
    )
    result = issue_and_execute_stream_i03(
        estate=estate,
        decision=decision,
        decision_verifier=decision_verifier,
        recorded_plan=recorded_plan,
    )
    return result, missing, decision


__all__ = [
    "HeldRecordedOperation",
    "RecordedResponseError",
    "build_recorded_operation",
    "execute_recorded_response_i03",
]
