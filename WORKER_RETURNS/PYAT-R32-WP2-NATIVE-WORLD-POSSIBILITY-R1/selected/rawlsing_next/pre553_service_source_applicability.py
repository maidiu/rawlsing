#!/usr/bin/env python3
"""HQ205 service-source applicability: ADMISSIBLE SET ONLY.

HQ-ratified authority form:

    ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED

This owner answers exactly one question:

    for this exact service / target / scope and this positively bounded candidate
    class, which candidate source universes are APPLICABLE?

It is deliberately the SMALLEST generic source-free owner consistent with the
ratified derivation. Same-grain bounded succession from the sibling authority
``pre553_structural_admission.py`` (D15 STRUCTURAL_EMPIRICAL_ADMISSION_AUTHORITY),
which is the immediate sibling row in the same D15 ledger.

What this owner is NOT
----------------------
It is not ranking, weighting, scoring, preference or source priority. It is not
source relation, pooling, estimand composition, currentness or target-use
permission. It is not F8 geometry transformation. It is not person-level state.
Those are separate powers and live elsewhere. ``FORBIDDEN_AUTHORIZED_PURPOSES``
makes each refusal explicit and machine-checkable rather than a matter of prose.

APPLICABILITY PREDATES EVIDENCE
-------------------------------
Applicability is decided at source-universe / scope / use grain, BEFORE any internal
evidence is examined. Therefore ``ServiceSourceApplicabilityDecision`` carries NO
internal-evidence-sufficiency field. Adding one would merge this power with
downstream evidence powers, and the two grains are then never interchangeable:

    NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS          (request grain, a SUCCESS)
      != APPLICABLE_SOURCE_WITH_MISSING_EVIDENCE    (source grain APPLICABLE,
                                                     then a downstream evidence state)

The first is a statement about SOURCES. The second is a statement about one
APPLICABLE source whose internal evidence is later found insufficient. This owner
never inspects internal evidence and can never convert one into the other.

Distinct state family
---------------------
``SERVICE_SOURCE_APPLICABILITY_STATE`` is a NEW family and is never aliased to
``SOURCE_UNIVERSE_RELATION_STATE``, ``P07_RELATION_DECISIONS``,
``EMPIRICAL_FACT_STATE`` or ``AUTHORITY_STATE``. ``NOT_APPLICABLE``, ``NONCOMPARABLE``
and ``OUT_OF_SCOPE`` each already appear in more than one existing family; aliasing
would make an applicability refusal indistinguishable from a relation refusal and
destroy the separation in the type system itself. The exact internal decision
vocabulary is preserved and coarsened ONLY through ``PUBLIC_STATE_BY_DECISION``.

Coverage honesty
----------------
``candidate_class_coverage`` is mandatory. ``COMPLETE`` means every candidate in the
positively bounded class received a terminal decision. ``INCOMPLETE`` means at least
one candidate is undecided. An INCOMPLETE coverage result may still carry known
per-source findings, but it is never reported as a complete admissible set, and
``NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS`` is never emitted merely because no known
positive exists.

Canonical ordering
------------------
The admissible set is serialized in a canonical, deterministic order for REPLAY ONLY.
That order grants no rank, priority, preference, weight, tie-break or fallback
meaning, and ``ORDERING_SEMANTICS`` says so in the receipt itself.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    authority_ref,
    canonical_json,
    exact_ref,
    semantic_hash,
)

HQC_CONTRACT_ID = "PRE553_HQ205_SERVICE_SOURCE_APPLICABILITY@1.0.0"
DECISION_FAMILY = "ServiceSourceApplicabilityDecision@1.0.0"
RECEIPT_FAMILY = "CandidateClassApplicabilityReceipt@1.0.0"
STATE_FAMILY = "SERVICE_SOURCE_APPLICABILITY_STATE"
IMPLEMENTATION_ID = "rawlsing_next/pre553_service_source_applicability.py"
AUTHORISED_AUTHORITY = "ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED"

# States already present in other families. Recorded so the non-aliasing court can
# assert this module never reuses another family's decision objects.
MUST_NOT_ALIAS_STATE_FAMILIES = (
    "SOURCE_UNIVERSE_RELATION_STATE",
    "P07_RELATION_DECISIONS",
    "EMPIRICAL_FACT_STATE",
    "AUTHORITY_STATE",
    "STRUCTURAL_ADMISSION_STATE",
)

# Ordered so a failure or refusal at a higher position can never be reported as, or
# silently converted into, a lower-position state. Same discipline as the sibling.
DECISION_PRECEDENCE = (
    "INTEGRITY_FAILURE",
    "MISSING_APPLICABILITY_AUTHORITY",
    "UNKNOWN_OR_CONFLICTING_APPLICABILITY_AUTHORITY",
    "REQUEST_KEY_INCOMPLETE_OR_AMBIGUOUS",
    "SOURCE_OUT_OF_DECLARED_SCOPE",
    "SOURCE_NOT_APPLICABLE_TO_THIS_SERVICE_AND_USE",
    "SOURCE_NONCOMPARABLE_AT_THIS_TARGET",
    "NEGATIVE_AUTHORITY_ONLY",
    "UNDETERMINED_NO_POSITIVE_AUTHORITY",
    "ADMITTED",
)
NONPOSITIVE_DECISIONS = frozenset(DECISION_PRECEDENCE[:-1])
POSITIVE_DECISION = "ADMITTED"

# A decision is TERMINAL when it is a settled finding. UNDETERMINED and the authority
# failures are not terminal, so their presence forces INCOMPLETE coverage.
NONTERMINAL_DECISIONS = frozenset({
    "INTEGRITY_FAILURE",
    "MISSING_APPLICABILITY_AUTHORITY",
    "UNKNOWN_OR_CONFLICTING_APPLICABILITY_AUTHORITY",
    "REQUEST_KEY_INCOMPLETE_OR_AMBIGUOUS",
    "UNDETERMINED_NO_POSITIVE_AUTHORITY",
})

# The public vocabulary is deliberately coarser and MAY NOT BE WIDENED.
PUBLIC_STATE_BY_DECISION = MappingProxyType({
    "ADMITTED": "APPLICABLE",
    "MISSING_APPLICABILITY_AUTHORITY": "MISSING_AUTHORITY",
    "UNKNOWN_OR_CONFLICTING_APPLICABILITY_AUTHORITY": "UNRESOLVED",
    "REQUEST_KEY_INCOMPLETE_OR_AMBIGUOUS": "UNRESOLVED",
    "SOURCE_OUT_OF_DECLARED_SCOPE": "OUT_OF_SCOPE",
    "SOURCE_NOT_APPLICABLE_TO_THIS_SERVICE_AND_USE": "NOT_APPLICABLE",
    "SOURCE_NONCOMPARABLE_AT_THIS_TARGET": "NONCOMPARABLE",
    "NEGATIVE_AUTHORITY_ONLY": "NOT_APPLICABLE",
    "UNDETERMINED_NO_POSITIVE_AUTHORITY": "MISSING_AUTHORITY",
    "INTEGRITY_FAILURE": "INTEGRITY_FAILURE",
})
PUBLIC_STATES = tuple(sorted(set(PUBLIC_STATE_BY_DECISION.values())))
POSITIVE_PUBLIC_STATE = "APPLICABLE"

COVERAGE_COMPLETE = "COMPLETE"
COVERAGE_INCOMPLETE = "INCOMPLETE"
COVERAGE_VALUES = (COVERAGE_COMPLETE, COVERAGE_INCOMPLETE)

# Every flag is False except on ADMITTED. "Eligibility is not conditioning": this
# owner may not condition F8 anywhere, and may not transform geometry anywhere.
DECISION_MATRIX = MappingProxyType({
    state: MappingProxyType({
        "public_typed_state": PUBLIC_STATE_BY_DECISION[state],
        "positive_admission": state == POSITIVE_DECISION,
        "may_enter_source_set": state == POSITIVE_DECISION,
        "may_constrain_downstream_query_scope": state == POSITIVE_DECISION,
        "may_rank_or_select": False,
        "may_pool_respondents": False,
        "may_grant_target_use_permission": False,
        "may_authorise_backfill": False,
        "may_condition_F8": False,
        "may_transform_geometry_or_distribution": False,
        "may_support_individual_inference": False,
    })
    for state in DECISION_PRECEDENCE
})

# Purposes this receipt may never be presented as authority for.
FORBIDDEN_AUTHORIZED_PURPOSES = (
    "POOLING",
    "SOURCE_SELECTION",
    "SOURCE_RANKING",
    "SOURCE_PRIORITY",
    "SOURCE_SEMANTIC_EQUIVALENCE",
    "RESPONDENT_LINKAGE",
    "OVERLAP_OR_NONDUPLICATION_AUTHORITY",
    "ESTIMAND_COMPOSITION",
    "BACKFILL_AUTHORITY",
    "CURRENTNESS_AUTHORITY",
    "TARGET_USE_PERMISSION_GRANT",
    "F8_GEOMETRY_OR_DISTRIBUTION_TRANSFORM",
    "INDIVIDUAL_INFERENCE",
    "ACTOR_OR_PERSON_STATE",
)

# Request-key names that would smuggle a comparative judgement in. Refused outright.
FORBIDDEN_REQUEST_KEY_NAMES = (
    "ranking", "rank", "score", "scores", "weight", "weights", "priority",
    "preference", "preferences", "selection_reason", "selected", "best",
    "preferred_source", "pooling", "pool", "weights_by_source", "linkage",
    "overlap", "backfill", "evidence", "evidence_state", "support",
    "sufficiency", "sample_size", "currentness", "permission_grant",
)

# Key components, all required, none defaultable, none inferable.
REQUEST_KEY_COMPONENTS = (
    "service_id",
    "service_authority_ref",
    "target_use_ref",
    "population_scope_ref",
    "geography_scope_ref",
    "effective_time_or_interval_ref",
    "candidate_class_ref",
    "release_identity_ref",
    "target_use_permission_refs",
    "candidate_source_universe_refs",
)

OUTCOME_ADMISSIBLE_SET = "ADMISSIBLE_SOURCE_INDEXED_SET"
OUTCOME_ADMISSIBLE_SET_INCOMPLETE = "ADMISSIBLE_SOURCE_INDEXED_SET__COVERAGE_INCOMPLETE"
OUTCOME_NO_ADMITTED_SOURCE = "NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS"
OUTCOME_REQUEST_UNDETERMINED = "SERVICE_REQUEST_UNDETERMINED"
OUTCOME_AUTHORITY_UNDETERMINED = "SERVICE_AUTHORITY_UNDETERMINED"
OUTCOME_AUTHORITY_CONFLICT = "APPLICABILITY_AUTHORITY_CONFLICT"
OUTCOME_CANDIDATE_CLASS_UNBOUNDED = "CANDIDATE_CLASS_UNBOUNDED"
POSITIVE_OUTCOMES = (OUTCOME_ADMISSIBLE_SET, OUTCOME_ADMISSIBLE_SET_INCOMPLETE)

ORDERING_SEMANTICS = (
    "REPLAY_ONLY_DETERMINISTIC_SERIALIZATION__ZERO_RANKING_PRIORITY_PREFERENCE_WEIGHT_OR_FALLBACK_SEMANTICS"
)

NON_COLLAPSE_LAWS = (
    "NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS != NO_EVIDENCE_FOUND",
    "APPLICABLE_SOURCE != SOURCE_WITH_EVIDENCE",
    "MISSING_AUTHORITY != NOT_APPLICABLE",
    "OUT_OF_SCOPE != NOT_APPLICABLE",
    "NONCOMPARABLE != NOT_APPLICABLE",
    "ADMITTED_SOURCE_SET != POOLED_SAMPLE",
    "ADMITTED_SOURCE_SET != COMPOSITE_ESTIMAND",
    "SERVICE_SOURCE_APPLICABILITY_STATE != SOURCE_UNIVERSE_RELATION_STATE",
    "SERVICE_SOURCE_APPLICABILITY_STATE != EMPIRICAL_FACT_STATE",
    "SOURCE_SEMANTIC_EQUIVALENCE != RESPONDENT_IDENTITY_LINKAGE != SAMPLE_POOLING_AUTHORITY",
    "ABSENCE_OF_EVIDENCE_OF_APPLICABILITY != EVIDENCE_OF_INAPPLICABILITY",
    "ABSENCE_OF_EVIDENCE_OF_APPLICABILITY != EVIDENCE_OF_APPLICABILITY",
)

# The ten components that make the request key. Enforced exact and complete or the
# function refuses: no partial keys, no best effort, no nearest match.
_MUTABLE_SELECTORS = frozenset({"LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER_FALLBACK"})


class ServiceSourceApplicabilityError(Pre553IntegrityError):
    """The exact applicability contract failed closed."""


class _Refusal(ServiceSourceApplicabilityError):
    """A typed refusal carrying its own decision state."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ServiceSourceApplicabilityError(f"{name} must be a non-empty string")
    return value.strip()


def _ref_list(values: Iterable[Any], name: str) -> tuple[ExactRef, ...]:
    seen: dict[str, ExactRef] = {}
    for raw in values:
        ref = exact_ref(raw, name)
        seen[canonical_json(ref.as_dict())] = ref
    return tuple(seen[k] for k in sorted(seen))


def _sorted_replay_only(refs: Sequence[ExactRef]) -> tuple[str, ...]:
    """Deterministic serialization order for replay only. Grants no rank."""
    return tuple(sorted(canonical_json(r.as_dict()) for r in refs))


@dataclass(frozen=True)
class CandidateClassBinding:
    """A POSITIVELY bounded candidate class.

    The bound is what makes an admissible set an admission decision rather than
    "all sources". Without it the set degenerates to everything, which is exactly
    the silent broadening the derivation forbids.
    """

    candidate_class_ref: ExactRef
    candidate_source_universe_refs: tuple[ExactRef, ...]
    binding_authority_ref: AuthorityRef
    declared_population_scope_ref: ExactRef
    declared_geography_scope_ref: ExactRef

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_class_ref",
                           exact_ref(self.candidate_class_ref, "candidate_class_ref"))
        object.__setattr__(self, "candidate_source_universe_refs",
                           _ref_list(self.candidate_source_universe_refs, "candidate_source_universe_refs"))
        object.__setattr__(self, "binding_authority_ref",
                           authority_ref(self.binding_authority_ref, "binding_authority_ref"))
        object.__setattr__(self, "declared_population_scope_ref",
                           exact_ref(self.declared_population_scope_ref, "declared_population_scope_ref"))
        object.__setattr__(self, "declared_geography_scope_ref",
                           exact_ref(self.declared_geography_scope_ref, "declared_geography_scope_ref"))
        if not self.candidate_source_universe_refs:
            raise _Refusal(OUTCOME_CANDIDATE_CLASS_UNBOUNDED,
                           "candidate class carries no members; an unbounded class is refused")

    def as_dict(self) -> dict[str, Any]:
        return {
            "candidate_class_ref": self.candidate_class_ref.as_dict(),
            "candidate_source_universe_refs": [r.as_dict() for r in self.candidate_source_universe_refs],
            "binding_authority_ref": self.binding_authority_ref.as_dict(),
            "declared_population_scope_ref": self.declared_population_scope_ref.as_dict(),
            "declared_geography_scope_ref": self.declared_geography_scope_ref.as_dict(),
            "member_count_is_not_a_sample_size": True,
        }


@dataclass(frozen=True)
class ServiceApplicabilityRequest:
    """The exact service request key. EXACT and COMPLETE, or the function refuses."""

    service_id: str
    service_authority_ref: AuthorityRef
    target_use_ref: ExactRef
    population_scope_ref: ExactRef
    geography_scope_ref: ExactRef
    effective_time_or_interval_ref: ExactRef
    candidate_class_ref: ExactRef
    release_identity_ref: ExactRef
    target_use_permission_refs: tuple[ExactRef, ...]
    candidate_source_universe_refs: tuple[ExactRef, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "service_id", _text(self.service_id, "service_id"))
        object.__setattr__(self, "service_authority_ref",
                           authority_ref(self.service_authority_ref, "service_authority_ref"))
        for name in ("target_use_ref", "population_scope_ref", "geography_scope_ref",
                     "effective_time_or_interval_ref", "candidate_class_ref", "release_identity_ref"):
            object.__setattr__(self, name, exact_ref(getattr(self, name), name))
        object.__setattr__(self, "target_use_permission_refs",
                           _ref_list(self.target_use_permission_refs, "target_use_permission_refs"))
        object.__setattr__(self, "candidate_source_universe_refs",
                           _ref_list(self.candidate_source_universe_refs, "candidate_source_universe_refs"))
        for name in REQUEST_KEY_COMPONENTS:
            value = getattr(self, name)
            if value is None or (isinstance(value, (tuple, list, str)) and len(value) == 0):
                raise _Refusal(OUTCOME_REQUEST_UNDETERMINED,
                               f"request key component {name} is absent; partial keys are refused")
        if self.service_authority_ref.authority_version.upper() in _MUTABLE_SELECTORS:
            raise _Refusal(OUTCOME_REQUEST_UNDETERMINED,
                           "mutable/fuzzy authority selection is forbidden")

    @classmethod
    def build(cls, **kwargs: Any) -> "ServiceApplicabilityRequest":
        """Construct a request, refusing any smuggled comparative or evidence field."""
        for name in kwargs:
            if name.lower() in FORBIDDEN_REQUEST_KEY_NAMES:
                raise _Refusal(
                    "REQUEST_KEY_INCOMPLETE_OR_AMBIGUOUS",
                    f"request key field {name!r} is not part of this authority; "
                    "ranking, weighting, preference, pooling, linkage, backfill, currentness, "
                    "permission-grant and internal-evidence fields are refused",
                )
        unknown = [k for k in kwargs if k not in REQUEST_KEY_COMPONENTS]
        if unknown:
            raise _Refusal("REQUEST_KEY_INCOMPLETE_OR_AMBIGUOUS",
                           f"unknown request key components refused: {sorted(unknown)}")
        # Fail closed with the TYPED refusal rather than a constructor TypeError:
        # an incomplete key must never surface as an incidental Python error.
        absent = [name for name in REQUEST_KEY_COMPONENTS if kwargs.get(name) is None]
        if absent:
            raise _Refusal(OUTCOME_REQUEST_UNDETERMINED,
                           f"request key components absent: {sorted(absent)}; "
                           "the key is EXACT and COMPLETE or the function refuses")
        return cls(**kwargs)

    def candidate_set_identity(self) -> str:
        """Stable identity for this exact request. Replay-only, non-semantic."""
        return semantic_hash({
            "service_id": self.service_id,
            "service_authority_ref": self.service_authority_ref.as_dict(),
            "target_use_ref": self.target_use_ref.as_dict(),
            "population_scope_ref": self.population_scope_ref.as_dict(),
            "geography_scope_ref": self.geography_scope_ref.as_dict(),
            "effective_time_or_interval_ref": self.effective_time_or_interval_ref.as_dict(),
            "candidate_class_ref": self.candidate_class_ref.as_dict(),
            "release_identity_ref": self.release_identity_ref.as_dict(),
            "target_use_permission_refs": [r.as_dict() for r in self.target_use_permission_refs],
            "candidate_source_universe_refs": [r.as_dict() for r in self.candidate_source_universe_refs],
        })

    def as_dict(self) -> dict[str, Any]:
        return {
            "service_id": self.service_id,
            "service_authority_ref": self.service_authority_ref.as_dict(),
            "target_use_ref": self.target_use_ref.as_dict(),
            "population_scope_ref": self.population_scope_ref.as_dict(),
            "geography_scope_ref": self.geography_scope_ref.as_dict(),
            "effective_time_or_interval_ref": self.effective_time_or_interval_ref.as_dict(),
            "candidate_class_ref": self.candidate_class_ref.as_dict(),
            "release_identity_ref": self.release_identity_ref.as_dict(),
            "target_use_permission_refs": [r.as_dict() for r in self.target_use_permission_refs],
            "candidate_source_universe_refs": [r.as_dict() for r in self.candidate_source_universe_refs],
            "target_use_permission_refs_are_bound_input_not_a_grant": True,
            "carries_no_ordering_ranking_or_preference_key": True,
            "carries_no_internal_evidence_field": True,
            "request_set_identity": self.candidate_set_identity(),
        }


@dataclass(frozen=True)
class ApplicabilityAuthorityRecord:
    """One candidate source universe's exact applicability authority.

    ``decision`` is one of DECISION_PRECEDENCE. A positive ADMITTED record MUST
    carry the exact positive admission authority; that is the admission provenance
    substitute for a selection reason, which does not exist because no selection
    occurs.
    """

    source_universe_ref: ExactRef
    decision: str
    admission_authority_ref: AuthorityRef | None = None
    basis_refs: tuple[ExactRef, ...] = ()
    negative_limit_refs: tuple[ExactRef, ...] = ()
    reason_code: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_universe_ref",
                           exact_ref(self.source_universe_ref, "source_universe_ref"))
        if self.decision not in DECISION_PRECEDENCE:
            raise _Refusal("INTEGRITY_FAILURE",
                           f"decision {self.decision!r} is not in the exact applicability vocabulary")
        object.__setattr__(self, "basis_refs", _ref_list(self.basis_refs, "basis_refs"))
        object.__setattr__(self, "negative_limit_refs",
                           _ref_list(self.negative_limit_refs, "negative_limit_refs"))
        if self.decision == POSITIVE_DECISION:
            if self.admission_authority_ref is None:
                raise _Refusal("INTEGRITY_FAILURE",
                               "an ADMITTED applicability result requires exact admission provenance")
            object.__setattr__(self, "admission_authority_ref",
                               authority_ref(self.admission_authority_ref, "admission_authority_ref"))
            if self.admission_authority_ref.authority_version.upper() in _MUTABLE_SELECTORS:
                raise _Refusal("INTEGRITY_FAILURE",
                               "mutable/fuzzy admission authority selection is forbidden")
        elif self.admission_authority_ref is not None:
            raise _Refusal("INTEGRITY_FAILURE",
                           "a non-positive applicability result must not carry admission provenance")
        if self.decision in ("SOURCE_NOT_APPLICABLE_TO_THIS_SERVICE_AND_USE",
                             "SOURCE_NONCOMPARABLE_AT_THIS_TARGET",
                             "SOURCE_OUT_OF_DECLARED_SCOPE",
                             "NEGATIVE_AUTHORITY_ONLY") and not self.basis_refs:
            raise _Refusal("INTEGRITY_FAILURE",
                           "a negative applicability finding requires its exact basis ref; "
                           "silence is never a verdict")

    @property
    def public_state(self) -> str:
        return PUBLIC_STATE_BY_DECISION[self.decision]

    @property
    def is_terminal(self) -> bool:
        return self.decision not in NONTERMINAL_DECISIONS

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "applicability_decision": self.decision,
            "public_typed_state": self.public_state,
            "admission_authority_ref": (self.admission_authority_ref.as_dict()
                                        if self.admission_authority_ref else None),
            "basis_refs": [r.as_dict() for r in self.basis_refs],
            "negative_limit_refs": [r.as_dict() for r in self.negative_limit_refs],
            "reason_code": self.reason_code,
            "terminal": self.is_terminal,
            "no_selection_reason_record_exists": True,
        }


@dataclass(frozen=True)
class ServiceSourceApplicabilityDecision:
    """One source universe's applicability decision.

    REQUIRED_FIELDS is EXACT and contains NO internal-evidence-sufficiency field.
    That omission is the structural enforcement of APPLICABILITY_PREDATES_EVIDENCE.
    """

    FAMILY = DECISION_FAMILY
    STATE_FAMILY = STATE_FAMILY
    REQUIRED_FIELDS = frozenset({
        "applicability_decision_id",
        "service_request_set_identity",
        "service_id",
        "target_use_ref",
        "candidate_class_ref",
        "candidate_class_coverage",
        "source_universe_ref",
        "release_identity_ref",
        "admission_authority_ref",
        "admission_provenance_refs",
        "applicability_decision",
        "public_typed_state",
        "basis_refs",
        "negative_limit_refs",
        "reason_code",
        "authorised_authority",
    })
    FORBIDDEN_FIELDS = frozenset({
        "evidence", "evidence_state", "support", "support_count", "sufficiency",
        "sample_size", "denominator", "numerator", "n_rows", "zero_support",
        "observed_zero", "low_support", "uncertainty", "unavailable",
    })

    applicability_decision_id: str
    service_request_set_identity: str
    service_id: str
    target_use_ref: Mapping[str, Any]
    candidate_class_ref: Mapping[str, Any]
    candidate_class_coverage: str
    source_universe_ref: Mapping[str, Any]
    release_identity_ref: Mapping[str, Any]
    admission_authority_ref: Mapping[str, Any] | None
    admission_provenance_refs: tuple[Mapping[str, Any], ...]
    applicability_decision: str
    public_typed_state: str
    basis_refs: tuple[Mapping[str, Any], ...]
    negative_limit_refs: tuple[Mapping[str, Any], ...]
    reason_code: str | None
    authorised_authority: str = AUTHORISED_AUTHORITY

    def __post_init__(self) -> None:
        if self.candidate_class_coverage not in COVERAGE_VALUES:
            raise _Refusal("INTEGRITY_FAILURE", "candidate_class_coverage must be COMPLETE or INCOMPLETE")
        if self.applicability_decision not in DECISION_PRECEDENCE:
            raise _Refusal("INTEGRITY_FAILURE", "unknown applicability decision")
        if self.public_typed_state != PUBLIC_STATE_BY_DECISION[self.applicability_decision]:
            raise _Refusal("INTEGRITY_FAILURE",
                           "public_typed_state must equal PUBLIC_STATE_BY_DECISION for its decision")
        if self.authorised_authority != AUTHORISED_AUTHORITY:
            raise _Refusal("INTEGRITY_FAILURE", "receipt must carry the exact ratified authority label")
        if self.applicability_decision == POSITIVE_DECISION and self.admission_authority_ref is None:
            raise _Refusal("INTEGRITY_FAILURE", "a positive applicability result requires admission provenance")

    def as_dict(self) -> dict[str, Any]:
        return {
            "applicability_decision_id": self.applicability_decision_id,
            "service_request_set_identity": self.service_request_set_identity,
            "service_id": self.service_id,
            "target_use_ref": dict(self.target_use_ref),
            "candidate_class_ref": dict(self.candidate_class_ref),
            "candidate_class_coverage": self.candidate_class_coverage,
            "source_universe_ref": dict(self.source_universe_ref),
            "release_identity_ref": dict(self.release_identity_ref),
            "admission_authority_ref": (dict(self.admission_authority_ref)
                                        if self.admission_authority_ref else None),
            "admission_provenance_refs": [dict(r) for r in self.admission_provenance_refs],
            "applicability_decision": self.applicability_decision,
            "public_typed_state": self.public_typed_state,
            "state_family": STATE_FAMILY,
            "basis_refs": [dict(r) for r in self.basis_refs],
            "negative_limit_refs": [dict(r) for r in self.negative_limit_refs],
            "reason_code": self.reason_code,
            "authorised_authority": self.authorised_authority,
            "applicability_predates_evidence": True,
            "carries_no_internal_evidence_field": True,
            "no_selection_reason_record_exists": True,
            "power_flags": dict(DECISION_MATRIX[self.applicability_decision]),
        }


@dataclass(frozen=True)
class CandidateClassApplicabilityReceipt:
    """The candidate-class receipt: an admissible SET plus truthful coverage."""

    receipt_id: str
    service_request_set_identity: str
    service_id: str
    candidate_class_ref: Mapping[str, Any]
    candidate_class_coverage: str
    decisions: tuple[ServiceSourceApplicabilityDecision, ...]
    outcome: str
    no_applicable_source: bool
    candidate_class_binding: Mapping[str, Any]
    request_key: Mapping[str, Any]
    canonical_replay_only_order: tuple[str, ...] = ()
    authorised_authority: str = AUTHORISED_AUTHORITY

    def __post_init__(self) -> None:
        if self.candidate_class_coverage not in COVERAGE_VALUES:
            raise _Refusal("INTEGRITY_FAILURE", "candidate_class_coverage must be COMPLETE or INCOMPLETE")
        if self.authorised_authority != AUTHORISED_AUTHORITY:
            raise _Refusal("INTEGRITY_FAILURE", "receipt must carry the exact ratified authority label")
        # NO_ADMITTED_SOURCE is a COMPLETE-coverage outcome ONLY. An incomplete class
        # may not be laundered into "there are no applicable sources".
        if self.no_applicable_source and self.candidate_class_coverage != COVERAGE_COMPLETE:
            raise _Refusal(
                POST_COVERAGE_LAW,
                "NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS requires COMPLETE coverage; "
                "an INCOMPLETE class must not masquerade as a decided empty set",
            )
        if self.outcome == OUTCOME_NO_ADMITTED_SOURCE and self.candidate_class_coverage != COVERAGE_COMPLETE:
            raise _Refusal(POST_COVERAGE_LAW,
                           "NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS is a COMPLETE-coverage outcome only")

    # -- set-like accessors, never aggregations -----------------------------
    def admissible_source_universe_refs(self) -> tuple[ExactRef, ...]:
        """Set-like output of the positively admitted sources. Never a sample."""
        return tuple(exact_ref(d.source_universe_ref)
                     for d in self.decisions if d.applicability_decision == POSITIVE_DECISION)

    def admissible_source_universe_refs_as_set(self) -> tuple[dict[str, Any], ...]:
        return tuple(r.as_dict() for r in self.admissible_source_universe_refs())

    def per_source_states(self) -> tuple[dict[str, Any], ...]:
        return tuple({
            "source_universe_ref": dict(d.source_universe_ref),
            "public_typed_state": d.public_typed_state,
            "applicability_decision": d.applicability_decision,
            "reason_code": d.reason_code,
        } for d in self.decisions)

    def is_complete_admissible_set(self) -> bool:
        return self.candidate_class_coverage == COVERAGE_COMPLETE

    def _material(self) -> dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "service_request_set_identity": self.service_request_set_identity,
            "service_id": self.service_id,
            "candidate_class_ref": dict(self.candidate_class_ref),
            "candidate_class_coverage": self.candidate_class_coverage,
            "outcome": self.outcome,
            "no_applicable_source": self.no_applicable_source,
            "candidate_class_binding": dict(self.candidate_class_binding),
            "request_key": dict(self.request_key),
            "decisions": [d.as_dict() for d in self.decisions],
            "authorised_authority": self.authorised_authority,
        }

    def replay_identity(self) -> str:
        """Replay-only stable identity. Carries no ranking semantics."""
        return semantic_hash(self._material())

    def as_dict(self) -> dict[str, Any]:
        return {
            **self._material(),
            "receipt_family": RECEIPT_FAMILY,
            "state_family": STATE_FAMILY,
            "admissible_source_universe_refs": list(self.admissible_source_universe_refs_as_set()),
            "admissible_set_is_a_set_of_separate_source_indexed_entries": True,
            "cardinality_is_not_a_sample_size": True,
            "canonical_replay_only_order": list(self.canonical_replay_only_order),
            "ordering_semantics": ORDERING_SEMANTICS,
            "canonical_order_grants_no_rank_priority_preference_weight_or_fallback": True,
            "per_source_states": list(self.per_source_states()),
            "is_complete_admissible_set": self.is_complete_admissible_set(),
            "applicability_predates_evidence": True,
            "no_internal_evidence_field": True,
            "no_selection_reason_record_exists": True,
            "admission_provenance_is_the_lawful_substitute": True,
            "geography_and_population_are_inclusion_filters_only": True,
            "locality_assigns_no_priority": True,
            "replay_identity": self.replay_identity(),
            "non_collapse_laws": list(NON_COLLAPSE_LAWS),
            "forbidden_authorised_purposes": list(FORBIDDEN_AUTHORIZED_PURPOSES),
            "may_not_alias_state_families": list(MUST_NOT_ALIAS_STATE_FAMILIES),
        }


POST_COVERAGE_LAW = "COVERAGE_INCOMPLETE_MAY_NOT_MASQUERADE_AS_COMPLETE"


def assert_complete_coverage(receipt: CandidateClassApplicabilityReceipt, operation: str) -> None:
    """Downstream operations needing EXHAUSTIVE applicability fail closed unless COMPLETE."""
    _text(operation, "operation")
    if receipt.candidate_class_coverage != COVERAGE_COMPLETE:
        raise _Refusal(
            "APPLICABILITY_COVERAGE_INCOMPLETE",
            f"{operation} requires exhaustive source applicability, but candidate class coverage is "
            f"{receipt.candidate_class_coverage}; the operation remains unresolved and no set is emitted",
        )


def assert_receipt_does_not_authorize(receipt: CandidateClassApplicabilityReceipt, purpose: str) -> None:
    """This receipt may never be presented as authority for a separate power."""
    want = _text(purpose, "purpose").upper()
    if want in FORBIDDEN_AUTHORIZED_PURPOSES:
        raise _Refusal(
            "POWER_NONCOLLAPSE_VIOLATION",
            f"a service-source applicability receipt carries no authority for {want}; "
            f"the implemented authority is {AUTHORISED_AUTHORITY}",
        )


def resolve_service_source_applicability(
    request: ServiceApplicabilityRequest,
    candidate_class: CandidateClassBinding,
    authority_records: Sequence[ApplicabilityAuthorityRecord],
) -> CandidateClassApplicabilityReceipt:
    """Resolve which candidate source universes are APPLICABLE. Nothing more.

    Emits an admissible SET or a first-class refusal. Performs no ranking, no
    selection, no combination, and never inspects internal evidence.
    """
    if not isinstance(request, ServiceApplicabilityRequest):
        raise _Refusal(OUTCOME_REQUEST_UNDETERMINED, "request must be a ServiceApplicabilityRequest")
    if not isinstance(candidate_class, CandidateClassBinding):
        raise _Refusal(OUTCOME_CANDIDATE_CLASS_UNBOUNDED,
                       "candidate_class must be a positively bounded CandidateClassBinding")
    if request.candidate_class_ref.as_dict() != candidate_class.candidate_class_ref.as_dict():
        raise _Refusal(OUTCOME_CANDIDATE_CLASS_UNBOUNDED,
                       "request candidate_class_ref does not match the bounded candidate class")

    members = candidate_class.candidate_source_universe_refs
    member_keys = {canonical_json(r.as_dict()): r for r in members}
    supplied = {canonical_json(r.as_dict()): r for r in request.candidate_source_universe_refs}

    # No silent broadening AND no silent narrowing: the key's candidate refs must be
    # exactly the positively bounded class members.
    if set(supplied) != set(member_keys):
        raise _Refusal(
            "CANDIDATE_CLASS_BROADENING_OR_NARROWING_REFUSED",
            "request candidate_source_universe_refs must equal the bounded candidate class exactly; "
            "a broader or narrower class may not be substituted",
        )

    records: dict[str, ApplicabilityAuthorityRecord] = {}
    for record in authority_records:
        if not isinstance(record, ApplicabilityAuthorityRecord):
            raise _Refusal("INTEGRITY_FAILURE", "authority records must be ApplicabilityAuthorityRecord")
        key = canonical_json(record.source_universe_ref.as_dict())
        if key in records:
            raise _Refusal("INTEGRITY_FAILURE",
                           f"duplicate applicability authority for {key}; one exact authority per source")
        if key not in member_keys:
            raise _Refusal(
                "CANDIDATE_CLASS_BROADENING_REFUSED",
                "an applicability authority names a source outside the bounded candidate class",
            )
        records[key] = record

    decisions: list[ServiceSourceApplicabilityDecision] = []
    for key in sorted(member_keys):
        source_ref = member_keys[key]
        record = records.get(key)
        if record is None:
            # Absence of an applicability authority is MISSING_AUTHORITY, never
            # NOT_APPLICABLE. Absence of evidence is never evidence either way.
            decision = "MISSING_APPLICABILITY_AUTHORITY"
            adm_auth = None
            basis: tuple[ExactRef, ...] = ()
            limits: tuple[ExactRef, ...] = ()
            reason = "NO_APPLICABILITY_AUTHORITY_BOUND_FOR_THIS_SOURCE"
        else:
            decision = record.decision
            adm_auth = (record.admission_authority_ref.as_dict()
                        if record.admission_authority_ref else None)
            basis = tuple(r.as_dict() for r in record.basis_refs)
            limits = tuple(r.as_dict() for r in record.negative_limit_refs)
            reason = record.reason_code

        provenance: tuple[Mapping[str, Any], ...] = ()
        if decision == POSITIVE_DECISION:
            provenance = ({"admission_authority_ref": adm_auth,
                           "candidate_class_ref": candidate_class.candidate_class_ref.as_dict(),
                           "candidate_class_binding_authority_ref":
                               candidate_class.binding_authority_ref.as_dict()},)

        decisions.append(ServiceSourceApplicabilityDecision(
            applicability_decision_id=semantic_hash({
                "request": request.candidate_set_identity(),
                "source": source_ref.as_dict(),
                "decision": decision,
            }),
            service_request_set_identity=request.candidate_set_identity(),
            service_id=request.service_id,
            target_use_ref=request.target_use_ref.as_dict(),
            candidate_class_ref=candidate_class.candidate_class_ref.as_dict(),
            candidate_class_coverage=COVERAGE_COMPLETE,  # provisional; set below
            source_universe_ref=source_ref.as_dict(),
            release_identity_ref=request.release_identity_ref.as_dict(),
            admission_authority_ref=adm_auth,
            admission_provenance_refs=provenance,
            applicability_decision=decision,
            public_typed_state=PUBLIC_STATE_BY_DECISION[decision],
            basis_refs=basis,
            negative_limit_refs=limits,
            reason_code=reason,
        ))

    # COMPLETE means EVERY candidate received a terminal decision.
    coverage = (COVERAGE_COMPLETE if all(d.applicability_decision not in NONTERMINAL_DECISIONS
                                         for d in decisions) else COVERAGE_INCOMPLETE)
    decisions = [replace_coverage(d, coverage) for d in decisions]

    admitted = [d for d in decisions if d.applicability_decision == POSITIVE_DECISION]
    if coverage == COVERAGE_COMPLETE:
        outcome = OUTCOME_ADMISSIBLE_SET if admitted else OUTCOME_NO_ADMITTED_SOURCE
    else:
        outcome = OUTCOME_ADMISSIBLE_SET_INCOMPLETE

    receipt = CandidateClassApplicabilityReceipt(
        receipt_id=semantic_hash({"request": request.candidate_set_identity(),
                                  "class": candidate_class.candidate_class_ref.as_dict()}),
        service_request_set_identity=request.candidate_set_identity(),
        service_id=request.service_id,
        candidate_class_ref=candidate_class.candidate_class_ref.as_dict(),
        candidate_class_coverage=coverage,
        decisions=tuple(decisions),
        outcome=outcome,
        no_applicable_source=(coverage == COVERAGE_COMPLETE and not admitted),
        candidate_class_binding=candidate_class.as_dict(),
        request_key=request.as_dict(),
    )
    object.__setattr__(receipt, "canonical_replay_only_order",
                       _sorted_replay_only(receipt.admissible_source_universe_refs()))
    return receipt


def replace_coverage(decision: ServiceSourceApplicabilityDecision, coverage: str) -> ServiceSourceApplicabilityDecision:
    from dataclasses import replace as _replace
    return _replace(decision, candidate_class_coverage=coverage)


__all__ = [
    "HQC_CONTRACT_ID", "IMPLEMENTATION_ID", "DECISION_FAMILY", "RECEIPT_FAMILY",
    "STATE_FAMILY", "AUTHORISED_AUTHORITY", "DECISION_PRECEDENCE", "NONPOSITIVE_DECISIONS",
    "POSITIVE_DECISION", "NONTERMINAL_DECISIONS", "PUBLIC_STATE_BY_DECISION", "PUBLIC_STATES",
    "POSITIVE_PUBLIC_STATE", "COVERAGE_COMPLETE", "COVERAGE_INCOMPLETE", "COVERAGE_VALUES",
    "DECISION_MATRIX", "FORBIDDEN_AUTHORIZED_PURPOSES", "FORBIDDEN_REQUEST_KEY_NAMES",
    "REQUEST_KEY_COMPONENTS", "NON_COLLAPSE_LAWS", "ORDERING_SEMANTICS",
    "MUST_NOT_ALIAS_STATE_FAMILIES",
    "OUTCOME_ADMISSIBLE_SET", "OUTCOME_ADMISSIBLE_SET_INCOMPLETE", "OUTCOME_NO_ADMITTED_SOURCE",
    "OUTCOME_REQUEST_UNDETERMINED", "OUTCOME_AUTHORITY_UNDETERMINED", "OUTCOME_AUTHORITY_CONFLICT",
    "OUTCOME_CANDIDATE_CLASS_UNBOUNDED", "POST_COVERAGE_LAW",
    "ServiceSourceApplicabilityError", "CandidateClassBinding", "ServiceApplicabilityRequest",
    "ApplicabilityAuthorityRecord", "ServiceSourceApplicabilityDecision",
    "CandidateClassApplicabilityReceipt", "assert_complete_coverage",
    "assert_receipt_does_not_authorize", "resolve_service_source_applicability",
]
