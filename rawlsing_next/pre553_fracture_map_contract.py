"""Authority-37 fracture-map controller policy and ref-only receipt contracts.

This module implements only the controller-policy / continuation-decision /
aggregate-receipt contract surface. It does not execute discovery traversal,
modify I05 candidate evaluation, enumerate co-signatures, or perform V3 work.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    CanonicalSemanticObject,
    ExactRef,
    Pre553IntegrityError,
    Pre553SemanticCollapseError,
    STATE_FAMILIES,
    authority_ref,
    canonicalize,
    exact_ref,
    semantic_hash,
)

POLICY_CONTRACT_ID = "PRE553_FRACTURE_MAP_CONTROLLER_POLICY@1.0.0"
POLICY_REF_KIND = "PRE553_FRACTURE_MAP_CONTROLLER_POLICY"
AUTHORITY37_POLICY_ID = "AUTHORITY37_CONSERVATIVE_PARITY_V1"
AUTHORITY37_POLICY_VERSION = "1.0.0"

AUTHORITY37_MINIMUM_SPLIT_RAW_N = 50
AUTHORITY37_MINIMUM_REPORT_RAW_N = 25
AUTHORITY37_MAXIMUM_DEPTH = 4

CONTINUATION_DECISION_CONTRACT_ID = "PRE553_FRACTURE_MAP_CONTINUATION_DECISION@1.0.0"
CONTINUATION_DECISION_REF_KIND = "PRE553_FRACTURE_MAP_CONTINUATION_DECISION"

RETENTION_DISPOSITIONS = frozenset({
    "RETAIN_EXACT_BRANCH",
    "RETAIN_ALL_SUPPORTED_CONFIGURATIONS",
    "RETAIN_TYPED_RESULT",
    "RETAIN_RESULT_WITH_LIMITATION",
    "RETAIN_LOW_SUPPORT_STATE",
    "RETAIN_FIRST_CLASS_BRANCH",
    "RETAIN_EXACT_ZERO_EVIDENCE",
    "RETAIN_WITH_STABILITY_QUALIFICATION",
    "RETAIN_CURRENT_EMPIRICAL_RESULT",
})

CONTINUATION_DISPOSITIONS = frozenset({
    "RETAIN_AND_CONTINUE_ELIGIBLE",
    "RETAIN_REPORT_ONLY_STOP",
    "RETAIN_TERMINAL_STOP",
    "RETAIN_TYPED_NONPOSITIVE_STOP",
    "FAIL_CLOSED_UNLESS_SEPARATELY_AUTHORIZED",
})

TERMINAL_STOP_REASONS = frozenset({
    "LOW_N_OR_INSUFFICIENT_SUPPORT",
    "VALID_EMPTY",
    "LOW_SUPPORT_OR_CONTROLLER_POLICY_ABSENT",
    "MISSING_OR_UNAVAILABLE",
    "UNRESOLVED_OR_MISSING_AUTHORITY",
    "NONCOMPARABLE",
    "ZERO_SUPPORT",
    "ZERO_OVERLAP",
    "MAX_DEPTH",
    "NO_MEANINGFUL_SPLIT_OR_NO_GAIN",
    "UNSTABLE_BRANCH",
    "NO_REMAINING_ELIGIBLE_PREDICTORS",
    "NO_REMAINING_ELIGIBLE_QUESTIONS",
})

V1_FAIL_CLOSED_CLASSIFIER_STOP_REASONS = frozenset({
    "NO_MEANINGFUL_SPLIT_OR_NO_GAIN",
    "UNSTABLE_BRANCH",
})

PRODUCER_TYPED_STATES = frozenset().union(
    STATE_FAMILIES["EMPIRICAL_FACT_STATE"],
    STATE_FAMILIES["DISCOVERY_RESULT_STATE"],
    STATE_FAMILIES["QUERY_STATE"],
    STATE_FAMILIES["PREDICATE_STATE"],
    STATE_FAMILIES["DISCOVERY_AUTHORITY_STATE"],
    STATE_FAMILIES["AUTHORITY_STATE"],
)

MAP_RECEIPT_FAMILY = "EmpiricalFractureMapReceipt@1.0.0"
MAP_RECEIPT_STATES = frozenset({
    "FRACTURE_MAP_CLOSURE_COMPLETE",
    "FRACTURE_MAP_CLOSURE_PARTIAL",
    "FRACTURE_MAP_CLOSURE_BLOCKED",
})


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Pre553IntegrityError(f"{name} must be a non-empty string")
    return value.strip()


def _exact_nonnegative_int(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise Pre553IntegrityError(f"{name} must be an exact nonnegative integer")
    return value


def _canonical_exact_refs(values: Iterable[ExactRef | Mapping[str, Any]], name: str) -> tuple[ExactRef, ...]:
    refs = tuple(exact_ref(value, name) for value in values)
    return tuple(sorted(set(refs), key=lambda ref: ref.key))


def _canonical_producer_bindings(
    values: Iterable[tuple[ExactRef | Mapping[str, Any], str]],
) -> tuple[tuple[ExactRef, str], ...]:
    material: dict[str, tuple[ExactRef, str]] = {}
    for ref_value, typed_state in values:
        ref = exact_ref(ref_value, "producer_result_ref")
        state = _text(typed_state, "producer_typed_state")
        if state not in PRODUCER_TYPED_STATES:
            raise Pre553IntegrityError(f"unsupported producer typed state {state!r}")
        prior = material.get(ref.key)
        if prior is not None and prior[1] != state:
            raise Pre553IntegrityError("one producer result ref cannot bind conflicting typed states")
        material[ref.key] = (ref, state)
    if not material:
        raise Pre553IntegrityError("one or more producer typed-state bindings are required")
    return tuple(material[key] for key in sorted(material))


@dataclass(frozen=True)
class FractureMapControllerPolicy:
    """Versioned Authority-37 controller policy identity.

    This is a contract object, not an additional public learned-world family.
    Its ExactRef is included by EmpiricalFractureMapReceipt.
    """

    policy_authority_ref: AuthorityRef | Mapping[str, Any]
    policy_id: str = AUTHORITY37_POLICY_ID
    policy_version: str = AUTHORITY37_POLICY_VERSION
    minimum_split_raw_n: int = AUTHORITY37_MINIMUM_SPLIT_RAW_N
    minimum_report_raw_n: int = AUTHORITY37_MINIMUM_REPORT_RAW_N
    maximum_depth: int = AUTHORITY37_MAXIMUM_DEPTH

    def __post_init__(self) -> None:
        auth = authority_ref(self.policy_authority_ref, "policy_authority_ref")
        policy_id = _text(self.policy_id, "policy_id")
        version = _text(self.policy_version, "policy_version")
        split_n = _exact_nonnegative_int(self.minimum_split_raw_n, "minimum_split_raw_n")
        report_n = _exact_nonnegative_int(self.minimum_report_raw_n, "minimum_report_raw_n")
        depth = _exact_nonnegative_int(self.maximum_depth, "maximum_depth")
        if report_n > split_n:
            raise Pre553IntegrityError("minimum_report_raw_n cannot exceed minimum_split_raw_n")
        if policy_id == AUTHORITY37_POLICY_ID and version == AUTHORITY37_POLICY_VERSION:
            expected = (
                AUTHORITY37_MINIMUM_SPLIT_RAW_N,
                AUTHORITY37_MINIMUM_REPORT_RAW_N,
                AUTHORITY37_MAXIMUM_DEPTH,
            )
            if (split_n, report_n, depth) != expected:
                raise Pre553IntegrityError(
                    "Authority-37 V1 policy values require a new policy version before tuning"
                )
        object.__setattr__(self, "policy_authority_ref", auth)
        object.__setattr__(self, "policy_id", policy_id)
        object.__setattr__(self, "policy_version", version)
        object.__setattr__(self, "minimum_split_raw_n", split_n)
        object.__setattr__(self, "minimum_report_raw_n", report_n)
        object.__setattr__(self, "maximum_depth", depth)

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": POLICY_CONTRACT_ID,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "policy_authority_ref": self.policy_authority_ref.as_dict(),
            "minimum_split_raw_n": self.minimum_split_raw_n,
            "minimum_report_raw_n": self.minimum_report_raw_n,
            "maximum_depth": self.maximum_depth,
            "modal_support_ordering": "GOVERNED_WEIGHTED_IF_AUTHORIZED_ELSE_RAW",
            "maximal_tie_policy": "RETAIN_ALL_MAXIMAL_PATTERNS__NO_FORCED_UNIQUE_MODAL",
            "candidate_reachability_policy": (
                "EXHAUSTIVE_GOVERNED_CANDIDATES__NO_SCORE_TOPK_PREVALENCE_PRUNING"
            ),
            "branch_retention_policy": "STOP_RECURSION_NEVER_DELETES_RETAINED_BRANCH",
            "no_meaningful_split_classifier_authorized": False,
            "unstable_branch_classifier_authorized": False,
            "continuation_dispositions": tuple(sorted(CONTINUATION_DISPOSITIONS)),
            "terminal_stop_reasons": tuple(sorted(TERMINAL_STOP_REASONS)),
            "pre_v3_actor_independent": True,
            "requires_separate_semantic_transformation_authority": True,
            "requires_separate_structural_admission_authority": True,
            "requires_separate_actor_binding_authority": True,
            "requires_explicit_v3_metabolism_authority": True,
            "actor_state_effect": False,
            "v3_state_effect": False,
            "v2_state_effect": False,
            "persona_effect": False,
            "belief_effect": False,
            "response_effect": False,
        }

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.semantic_projection())

    @property
    def ref(self) -> ExactRef:
        digest = self.content_hash
        return ExactRef(
            POLICY_REF_KIND,
            f"urn:rawlsing:pre553:fracture-map-controller-policy:sha256:{digest}",
            digest,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            **canonicalize(self.semantic_projection()),
            "object_id": self.ref.object_id,
            "content_hash": self.ref.content_hash,
            "exact_ref": self.ref.as_dict(),
        }


@dataclass(frozen=True)
class FractureMapContinuationDecision:
    """Ref-only controller decision preserving producer states and retention."""

    controller_policy_ref: ExactRef | Mapping[str, Any]
    controller_policy_authority_ref: AuthorityRef | Mapping[str, Any]
    branch_predicate_ref: ExactRef | Mapping[str, Any]
    producer_state_bindings: Iterable[tuple[ExactRef | Mapping[str, Any], str]]
    retention_disposition: str
    continuation_disposition: str
    stop_reason: str
    depth: int

    def __post_init__(self) -> None:
        policy_ref = exact_ref(self.controller_policy_ref, "controller_policy_ref")
        policy_auth = authority_ref(
            self.controller_policy_authority_ref, "controller_policy_authority_ref"
        )
        branch_ref = exact_ref(self.branch_predicate_ref, "branch_predicate_ref")
        bindings = _canonical_producer_bindings(self.producer_state_bindings)
        retention = _text(self.retention_disposition, "retention_disposition")
        continuation = _text(self.continuation_disposition, "continuation_disposition")
        stop = _text(self.stop_reason, "stop_reason")
        depth = _exact_nonnegative_int(self.depth, "depth")
        if retention not in RETENTION_DISPOSITIONS:
            raise Pre553IntegrityError(f"unknown retention disposition {retention!r}")
        if continuation not in CONTINUATION_DISPOSITIONS:
            raise Pre553IntegrityError(f"unknown continuation disposition {continuation!r}")
        if continuation == "RETAIN_AND_CONTINUE_ELIGIBLE":
            if stop != "NONE":
                raise Pre553IntegrityError("continue-eligible decision must have stop_reason NONE")
        elif stop not in TERMINAL_STOP_REASONS:
            raise Pre553IntegrityError("stopped decision requires an exact Authority-37/D03 stop reason")
        object.__setattr__(self, "controller_policy_ref", policy_ref)
        object.__setattr__(self, "controller_policy_authority_ref", policy_auth)
        object.__setattr__(self, "branch_predicate_ref", branch_ref)
        object.__setattr__(self, "producer_state_bindings", bindings)
        object.__setattr__(self, "retention_disposition", retention)
        object.__setattr__(self, "continuation_disposition", continuation)
        object.__setattr__(self, "stop_reason", stop)
        object.__setattr__(self, "depth", depth)

    @property
    def retains_branch_or_typed_result(self) -> bool:
        return True

    @property
    def may_recurse(self) -> bool:
        return self.continuation_disposition == "RETAIN_AND_CONTINUE_ELIGIBLE"

    @property
    def producer_typed_states(self) -> tuple[str, ...]:
        return tuple(state for _, state in self.producer_state_bindings)

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": CONTINUATION_DECISION_CONTRACT_ID,
            "controller_policy_ref": self.controller_policy_ref.as_dict(),
            "controller_policy_authority_ref": self.controller_policy_authority_ref.as_dict(),
            "branch_predicate_ref": self.branch_predicate_ref.as_dict(),
            "producer_state_bindings": [
                {
                    "producer_result_ref": ref.as_dict(),
                    "producer_typed_state": state,
                }
                for ref, state in self.producer_state_bindings
            ],
            "retention_disposition": self.retention_disposition,
            "continuation_disposition": self.continuation_disposition,
            "stop_reason": self.stop_reason,
            "depth": self.depth,
            "pre_v3_actor_independent": True,
            "actor_state_effect": False,
            "v3_state_effect": False,
            "v2_state_effect": False,
            "persona_effect": False,
            "belief_effect": False,
            "response_effect": False,
        }

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.semantic_projection())

    @property
    def ref(self) -> ExactRef:
        digest = self.content_hash
        return ExactRef(
            CONTINUATION_DECISION_REF_KIND,
            f"urn:rawlsing:pre553:fracture-map-continuation-decision:sha256:{digest}",
            digest,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            **canonicalize(self.semantic_projection()),
            "object_id": self.ref.object_id,
            "content_hash": self.ref.content_hash,
            "exact_ref": self.ref.as_dict(),
        }


class EmpiricalFractureMapReceipt(CanonicalSemanticObject):
    """Ref-only aggregate closure/replay receipt authorized by Authority 37."""

    FAMILY = MAP_RECEIPT_FAMILY
    STATE_FAMILY = "FRACTURE_MAP_RECEIPT_STATE"
    REQUIRED_FIELDS = frozenset({
        "root_query_ref",
        "source_release_refs",
        "controller_policy_ref",
        "controller_policy_authority_ref",
        "branch_predicate_refs",
        "branch_ancestry_refs",
        "generation_frontier_refs",
        "empirical_fact_refs",
        "discovery_result_receipt_refs",
        "branch_cosignature_topology_closure_refs",
        "continuation_decision_refs",
        "final_replay_ref",
        "closure_state",
        "copied_empirical_payload",
        "pre_v3_actor_independent",
        "requires_separate_semantic_transformation_authority",
        "requires_separate_structural_admission_authority",
        "requires_separate_actor_binding_authority",
        "requires_explicit_v3_metabolism_authority",
        "actor_state_effect",
        "v3_state_effect",
        "v2_state_effect",
        "persona_effect",
        "belief_effect",
        "response_effect",
    })
    SET_LIKE_FIELDS = frozenset({
        "source_release_refs",
        "branch_predicate_refs",
        "branch_ancestry_refs",
        "empirical_fact_refs",
        "discovery_result_receipt_refs",
        "branch_cosignature_topology_closure_refs",
        "continuation_decision_refs",
    })

    def _validate_family(self) -> None:
        if set(self.semantic_fields) != self.REQUIRED_FIELDS:
            extras = sorted(set(self.semantic_fields) - self.REQUIRED_FIELDS)
            raise Pre553IntegrityError(
                f"EmpiricalFractureMapReceipt permits ref-only contract fields only; extras={extras!r}"
            )
        if self.typed_state not in MAP_RECEIPT_STATES:
            raise Pre553IntegrityError("invalid fracture-map closure state")
        if self.closure_state != self.typed_state:
            raise Pre553IntegrityError("closure_state must equal typed_state")

        root_query = exact_ref(self.root_query_ref, "root_query_ref")
        source_releases = _canonical_exact_refs(self.source_release_refs, "source_release_ref")
        policy_ref = exact_ref(self.controller_policy_ref, "controller_policy_ref")
        policy_auth = authority_ref(
            self.controller_policy_authority_ref, "controller_policy_authority_ref"
        )
        branch_predicates = _canonical_exact_refs(
            self.branch_predicate_refs, "branch_predicate_ref"
        )
        branch_ancestry = _canonical_exact_refs(
            self.branch_ancestry_refs, "branch_ancestry_ref"
        )
        frontiers = tuple(
            exact_ref(value, "generation_frontier_ref")
            for value in self.generation_frontier_refs
        )
        if not frontiers:
            raise Pre553IntegrityError("one or more sealed generation frontier refs are required")
        facts = _canonical_exact_refs(self.empirical_fact_refs, "empirical_fact_ref")
        discovery = _canonical_exact_refs(
            self.discovery_result_receipt_refs, "discovery_result_receipt_ref"
        )
        topology = _canonical_exact_refs(
            self.branch_cosignature_topology_closure_refs,
            "branch_cosignature_topology_closure_ref",
        )
        decisions = _canonical_exact_refs(
            self.continuation_decision_refs, "continuation_decision_ref"
        )
        replay = exact_ref(self.final_replay_ref, "final_replay_ref")

        if not source_releases:
            raise Pre553IntegrityError("one or more exact source release refs are required")
        if policy_auth not in set(self.authority_snapshot_refs):
            raise Pre553IntegrityError(
                "controller policy authority must be present in authority_snapshot_refs"
            )

        required_dependencies = {
            root_query,
            *source_releases,
            policy_ref,
            *branch_predicates,
            *branch_ancestry,
            *frontiers,
            *facts,
            *discovery,
            *topology,
            *decisions,
            replay,
        }
        if not required_dependencies <= set(self.dependency_refs):
            missing = sorted(
                (ref.key for ref in required_dependencies - set(self.dependency_refs))
            )
            raise Pre553IntegrityError(
                f"fracture-map receipt dependency closure missing exact refs: {missing!r}"
            )
        if canonicalize(self.producer_replay_locator_or_reference_root) != replay.as_dict():
            raise Pre553IntegrityError("producer replay root must equal final_replay_ref")

        if self.copied_empirical_payload is not False:
            raise Pre553SemanticCollapseError(
                "EmpiricalFractureMapReceipt is ref-only and may not copy empirical payload"
            )
        if self.pre_v3_actor_independent is not True:
            raise Pre553SemanticCollapseError("fracture-map receipt must remain PRE-V3 actor-independent")
        for field in (
            "requires_separate_semantic_transformation_authority",
            "requires_separate_structural_admission_authority",
            "requires_separate_actor_binding_authority",
            "requires_explicit_v3_metabolism_authority",
        ):
            if getattr(self, field) is not True:
                raise Pre553SemanticCollapseError(f"{field} must remain an explicit firewall gate")
        for field in (
            "actor_state_effect",
            "v3_state_effect",
            "v2_state_effect",
            "persona_effect",
            "belief_effect",
            "response_effect",
        ):
            if getattr(self, field) not in (False, 0):
                raise Pre553SemanticCollapseError(
                    f"EmpiricalFractureMapReceipt cannot carry positive {field}"
                )


__all__ = [
    "POLICY_CONTRACT_ID",
    "POLICY_REF_KIND",
    "AUTHORITY37_POLICY_ID",
    "AUTHORITY37_POLICY_VERSION",
    "AUTHORITY37_MINIMUM_SPLIT_RAW_N",
    "AUTHORITY37_MINIMUM_REPORT_RAW_N",
    "AUTHORITY37_MAXIMUM_DEPTH",
    "CONTINUATION_DECISION_CONTRACT_ID",
    "CONTINUATION_DECISION_REF_KIND",
    "RETENTION_DISPOSITIONS",
    "CONTINUATION_DISPOSITIONS",
    "TERMINAL_STOP_REASONS",
    "V1_FAIL_CLOSED_CLASSIFIER_STOP_REASONS",
    "PRODUCER_TYPED_STATES",
    "MAP_RECEIPT_FAMILY",
    "MAP_RECEIPT_STATES",
    "FractureMapControllerPolicy",
    "FractureMapContinuationDecision",
    "EmpiricalFractureMapReceipt",
]
