#!/usr/bin/env python3
"""HQ210 SERVICE_APPLICABILITY_TO_F8_SOURCE_SCOPE_BINDING: a thin same-grain binder.

This module closes exactly one seam proven missing by HQ208:

    there was no binding from a CandidateClassApplicabilityReceipt (and its replay
    identity and per-source admission provenance) to the source scope that F8 is
    allowed to evaluate.

It is a BINDER, not an owner. It holds no authority of its own and grants nothing.
Everything it reports is read out of an already-adopted applicability receipt.

What this binder is NOT
-----------------------
It is not a source selector, ranking owner, preference or priority owner, pooling or
composition owner, currentness authority, target-use permission issuer, temporal
authority, F8 geometry/distribution transformer, conditioning owner, or an
actor/person inference layer. Those powers are refused structurally, by raising, and
are enumerated in ``FORBIDDEN_BINDING_PURPOSES``.

The F8 law is load-bearing and preserved
----------------------------------------
``F8_DOES_NOT_TRANSFORM_POSSIBILITY_GEOMETRY``. F8 is
``EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION``: it selects
an exact pre-materialized evidence slice, or performs a governed strictly-decreasing
same-source/release specificity walkback, or refuses.

This binder therefore passes the caller's ``query``, ``rule`` and ``evidence`` into
``evaluate_positioned_subject_possibility`` BY IDENTITY, UNCHANGED. It never edits,
re-orders, widens, narrows, reweights or re-targets them. Narrowing the ADMITTED set
can change WHICH pre-materialized slice F8 selects; that is output SELECTION, not
output TRANSFORMATION, and the geometry is byte-identical either way.

ELIGIBILITY IS NOT CONDITIONING
-------------------------------
An admitted source may be used as a SOURCE SCOPE for F8. It may not become a
CONDITIONER. ``ConditionerBinding`` construction is not this binder's business, the
query's conditioners are never inspected for applicability, and no conditioner may be
added, dropped, widened or re-pointed here. Conditioning remains governed by the F8
query's own exact authority.

The two positive powers, exactly
--------------------------------
1. ``assert_query_source_admitted`` - validate ONE exact F8 query source against a
   positive admitted entry in an exact applicability receipt.
2. ``expose_unranked_admitted_source_set`` - expose the COMPLETE UNRANKED admitted
   ``source_universe_refs`` set for independent source-indexed F8 evaluation.

**Truthful accounting of the public surface (Repair 2).** The declared public
callables are EIGHT, and FIVE of them return a value. They are NOT two:

* the TWO source-touching positive powers -- ``assert_query_source_admitted`` and
  ``expose_unranked_admitted_source_set``;
* plus a binding CONSTRUCTOR ``bind_service_applicability_to_f8_scope``;
* plus a DELEGATING evaluator ``evaluate_bound_positioned_subject_possibility``;
* plus a REPLAY VERIFIER ``verify_service_f8_scope_binding_replay``;
* plus a COVERAGE GUARD ``assert_complete_coverage_from_binding``, which returns
  nothing and only raises.

``evaluate_bound_positioned_subject_possibility`` is NOT a third power over sources:
it invokes the adopted F8 evaluator UNCHANGED after source-scope validation and
grants no selection, transformation, pooling, currentness, permission or actor
semantics of its own. That is why it is a non-power despite returning a full result.

What remains exactly true: there is no THIRD POWER OVER SOURCES. There is no way to
obtain a first, best, latest, local, preferred, ranked or weighted source from this
object, because no such method exists, and all SEVEN selection/permission-shaped
methods refuse loudly when attempted.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.objective_non_event_currentness_contract import (
    STATES as ADOPTED_CURRENTNESS_STATES,
)
from rawlsing_next.pre553_service_source_applicability import (
    AUTHORISED_AUTHORITY,
    COVERAGE_COMPLETE,
    COVERAGE_VALUES,
    FORBIDDEN_AUTHORIZED_PURPOSES,
    ORDERING_SEMANTICS,
    POSITIVE_DECISION,
    POSITIVE_PUBLIC_STATE,
    CandidateClassApplicabilityReceipt,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    PossibilitySliceEvidence,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
    PositionedSubjectPossibilityResult,
    evaluate_positioned_subject_possibility,
)

BINDING_CONTRACT_ID = "SERVICE_APPLICABILITY_TO_F8_SOURCE_SCOPE_BINDING@1.0.0"
BINDING_IMPLEMENTATION_ID = "HQ210_SERVICE_F8_SOURCE_SCOPE_BINDING@1.0.0"
BINDING_FAMILY = "ServiceApplicabilityF8SourceScopeBinding@1.0.0"
BINDING_REQUEST_FAMILY = "ServiceApplicabilityF8ScopeBindingRequest@1.0.0"

#: The F8 algorithm this binder is written against. If F8 ever gains a smoothing,
#: interpolation, extrapolation, geometry or distribution operation, this constant
#: stops matching and the binder must be re-adjudicated rather than silently reused.
EXPECTED_F8_ALGORITHM_ID = "EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION"
EXPECTED_F8_MODEL_RULE_ID = "POSITIONED_SUBJECT_EXACT_CONDITIONAL_WITH_GOVERNED_WALKBACK@1.0.0"

BINDING_STATEMENT = (
    "BINDING_GRANTS_ELIGIBILITY_SCOPE_ONLY__NO_SELECTION_NO_RANKING_NO_POOLING_NO_"
    "CONDITIONING_NO_GEOMETRY_OR_DISTRIBUTION_TRANSFORM_NO_PERMISSION_GRANT_NO_ACTOR_INFERENCE"
)

#: Purposes this binder refuses, by raising. This is the union of the commission's
#: named prohibitions and the applicability owner's own forbidden-authority list, so
#: the two layers agree rather than drifting.
FORBIDDEN_BINDING_PURPOSES: tuple[str, ...] = tuple(sorted(set(FORBIDDEN_AUTHORIZED_PURPOSES) | {
    "SOURCE_SELECTION",
    "SOURCE_RANKING",
    "SOURCE_PRIORITY",
    "SOURCE_PREFERENCE",
    "FIRST_SOURCE_CHOICE",
    "BEST_SOURCE_CHOICE",
    "LATEST_SOURCE_CHOICE",
    "LOCAL_SOURCE_CHOICE",
    "PREFERRED_SOURCE_CHOICE",
    "POOLING",
    "CROSS_SOURCE_COMPOSITION",
    "ESTIMAND_COMPOSITION",
    "OVERLAP_OR_NONDUPLICATION_AUTHORITY",
    "RESPONDENT_LINKAGE",
    "SOURCE_SEMANTIC_EQUIVALENCE",
    "BACKFILL_AUTHORITY",
    "CURRENTNESS_AUTHORITY",
    "TARGET_USE_PERMISSION_GRANT",
    "F8_CONDITIONING",
    "F8_GEOMETRY_OR_DISTRIBUTION_TRANSFORM",
    "PROBABILITY_OR_DISTRIBUTION_TRANSFORM",
    "TEMPORAL_COMPARABILITY_OR_PRESSURE",
    "INDIVIDUAL_INFERENCE",
    "ACTOR_OR_PERSON_STATE",
    "PREV3_TO_V3_ACTOR_WORK",
}))

NON_COLLAPSE_LAWS: tuple[str, ...] = (
    "ELIGIBILITY != CONDITIONING",
    "ELIGIBILITY_NARROWING != POSSIBILITY_GEOMETRY_TRANSFORMATION",
    "ELIGIBILITY_NARROWING != DISTRIBUTION_TRANSFORMATION",
    "BINDING != SOURCE_SELECTION",
    "BINDING != SOURCE_RANKING",
    "BINDING != SOURCE_PRIORITY",
    "BINDING != SOURCE_EQUIVALENCE",
    "BINDING != POOLING_OR_COMPOSITION",
    "BINDING != CURRENTNESS",
    "BINDING != TARGET_USE_PERMISSION_GRANT",
    "BOUND_PERMISSION_REFS != GRANTED_PERMISSION",
    "APPLICABILITY_NONCOMPARABLE != F8_EVIDENCE_NONCOMPARABLE",
    "ADMITTED_SOURCE_SET != POOLED_SAMPLE",
    "ADMITTED_SET_CARDINALITY != SAMPLE_SIZE",
    "CANONICAL_REPLAY_ORDER != RANK_OR_PRIORITY",
    "SOURCE_INDEXED_ENTRY != CROSS_SOURCE_AGGREGATE",
    "EMPIRICAL_POSSIBILITY != INDIVIDUAL_OR_ACTOR_STATE",
)

#: Modes this binder supports. There is no ranked mode, no "best" mode, and no
#: exhaustive-without-COMPLETE mode.
MODE_SINGLE_SOURCE_VALIDATION = "SINGLE_SOURCE_VALIDATION"
MODE_EXHAUSTIVE_UNRANKED_SET = "EXHAUSTIVE_UNRANKED_SET"
BINDING_MODES: tuple[str, ...] = (MODE_SINGLE_SOURCE_VALIDATION, MODE_EXHAUSTIVE_UNRANKED_SET)

#: Repair 2: the exact public surface, counted truthfully.
#: The TWO source-touching positive powers.
TWO_SOURCE_TOUCHING_POWERS: tuple[str, ...] = (
    "assert_query_source_admitted",
    "expose_unranked_admitted_source_set",
)
#: Public callables that return a value but grant NO power over sources.
NON_POWER_RETURNING_CALLABLES: tuple[str, ...] = (
    "bind_service_applicability_to_f8_scope",
    "evaluate_bound_positioned_subject_possibility",
    "verify_service_f8_scope_binding_replay",
)
#: Public callables that return nothing and only raise on a violation.
GUARD_ONLY_CALLABLES: tuple[str, ...] = (
    "assert_complete_coverage_from_binding",
)
#: Why the delegating evaluator is not a new power.
DELEGATING_EVALUATOR_IS_NOT_A_POWER_BECAUSE = (
    "evaluate_bound_positioned_subject_possibility invokes the adopted F8 evaluator UNCHANGED "
    "after source-scope validation and grants no selection, ranking, transformation, pooling, "
    "currentness, permission or actor semantics of its own"
)
#: The substantive claim that IS exact.
NO_THIRD_POWER_OVER_SOURCES = (
    "there is no THIRD POWER OVER SOURCES: no first/best/latest/local/preferred/ranked/"
    "weighted source is obtainable, because no such method exists and all seven "
    "selection-shaped methods refuse loudly when attempted"
)

CURRENTNESS_UNREQUESTED = "CURRENTNESS_NOT_REQUESTED"

#: Repair 4: the accepted currentness vocabulary is now a CLOSED set, taken from the
#: adopted currentness contract's own STATES rather than left open to any caller
#: string. Of the adopted states, only CURRENT is a currency result this binder will
#: record; the adopted non-currency states are refused exactly as the legacy negative
#: tokens are. This binder records a caller-supplied currentness result and never
#: decides currency -- pinning the vocabulary does not make it a currentness authority.
ACCEPTED_CURRENTNESS_RESULTS: frozenset[str] = frozenset({"CURRENT"})
REFUSED_CURRENTNESS_RESULTS: frozenset[str] = frozenset(
    {"CONFLICTING", "UNKNOWN", "MISSING", "UNRESOLVED"}
) | (set(ADOPTED_CURRENTNESS_STATES) - ACCEPTED_CURRENTNESS_RESULTS)
#: Every accepted result must appear in the adopted contract's states.
ACCEPTED_CURRENTNESS_RESULTS_ARE_ADOPTED = ACCEPTED_CURRENTNESS_RESULTS <= set(
    ADOPTED_CURRENTNESS_STATES
)
if not ACCEPTED_CURRENTNESS_RESULTS_ARE_ADOPTED:  # pragma: no cover - defensive
    raise ServiceF8ScopeBindingError(
        "CURRENTNESS_VOCABULARY_NOT_ADOPTED",
        "the accepted currentness vocabulary must be a subset of the adopted contract states",
    )


class ServiceF8ScopeBindingError(Pre553IntegrityError):
    """Every refusal in this binder is this type and carries an exact reason code."""

    def __init__(self, reason_code: str, message: str) -> None:
        super().__init__(f"{reason_code}: {message}")
        self.reason_code = reason_code


def _refusal(code: str, message: str) -> "ServiceF8ScopeBindingError":
    return ServiceF8ScopeBindingError(code, message)


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _refusal("BINDING_INTEGRITY_FAILURE", f"{name} must be a non-empty string")
    return value


def _mat(value: Any) -> Any:
    from rawlsing_next.pre553_empirical_objects import canonicalize

    return canonicalize(value)


def _ref(value: Any, name: str) -> ExactRef:
    if not isinstance(value, ExactRef):
        raise _refusal("BINDING_INTEGRITY_FAILURE", f"{name} must be an ExactRef")
    return value


def _ref_dict(value: Any, name: str) -> dict[str, Any]:
    return dict(_ref(value, name).as_dict())


@dataclass(frozen=True)
class ServiceApplicabilityF8ScopeBindingRequest:
    """The exact request to bind applicability to an F8 source scope.

    Every field is exact. There is no default, no nearest match, and no partial
    binding: a missing or mismatched component refuses.
    """

    binding_request_id: str
    service_request_set_identity: str
    candidate_class_ref: ExactRef
    service_id: str
    target_use_ref: ExactRef
    release_identity_ref: ExactRef
    bound_target_use_permission_refs: tuple[ExactRef, ...]
    binding_mode: str
    requested_source_universe_ref: ExactRef | None = None
    requested_currentness_claim: str | None = None
    requested_purpose: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "binding_request_id", _text(self.binding_request_id, "binding_request_id"))
        object.__setattr__(self, "service_request_set_identity",
                           _text(self.service_request_set_identity, "service_request_set_identity"))
        object.__setattr__(self, "candidate_class_ref", _ref(self.candidate_class_ref, "candidate_class_ref"))
        object.__setattr__(self, "service_id", _text(self.service_id, "service_id"))
        object.__setattr__(self, "target_use_ref", _ref(self.target_use_ref, "target_use_ref"))
        object.__setattr__(self, "release_identity_ref", _ref(self.release_identity_ref, "release_identity_ref"))
        perms = tuple(self.bound_target_use_permission_refs or ())
        if not perms:
            raise _refusal(
                "TARGET_USE_PERMISSION_BOUND_REFS_REQUIRED",
                "exactly-bound target-use permission refs are required as an INPUT; "
                "absence is a refusal and their presence still grants nothing",
            )
        for p in perms:
            _ref(p, "bound_target_use_permission_refs[]")
        object.__setattr__(self, "bound_target_use_permission_refs", perms)
        if self.binding_mode not in BINDING_MODES:
            raise _refusal(
                "BINDING_MODE_NOT_SUPPORTED",
                f"binding_mode must be one of {BINDING_MODES}; there is no ranked, best, "
                f"preferred, latest or local mode",
            )
        object.__setattr__(self, "binding_mode", self.binding_mode)
        if self.binding_mode == MODE_SINGLE_SOURCE_VALIDATION:
            if self.requested_source_universe_ref is None:
                raise _refusal("BINDING_INTEGRITY_FAILURE",
                               "SINGLE_SOURCE_VALIDATION requires an exact requested_source_universe_ref")
        else:
            if self.requested_source_universe_ref is not None:
                raise _refusal(
                    "BINDING_MODE_NOT_SUPPORTED",
                    "EXHAUSTIVE_UNRANKED_SET takes no single requested source; a single-source "
                    "request under an exhaustive mode would be an implicit selection",
                )
        if self.requested_source_universe_ref is not None:
            _ref(self.requested_source_universe_ref, "requested_source_universe_ref")
        if self.requested_currentness_claim is not None:
            _text(self.requested_currentness_claim, "requested_currentness_claim")
        if self.requested_purpose is not None:
            self._refuse_if_forbidden_purpose(self.requested_purpose)

    @staticmethod
    def _refuse_if_forbidden_purpose(purpose: str) -> None:
        want = _text(purpose, "purpose").upper()
        if want in FORBIDDEN_BINDING_PURPOSES:
            raise _refusal(
                "BINDING_POWER_NONCOLLAPSE_VIOLATION",
                f"this binder carries no authority for {want}; it is a source-scope binder under "
                f"{BINDING_STATEMENT} and the F8 law {EXPECTED_F8_ALGORITHM_ID}",
            )

    def material(self) -> Mapping[str, Any]:
        return {
            "contract": BINDING_REQUEST_FAMILY,
            "binding_request_id": self.binding_request_id,
            "service_request_set_identity": self.service_request_set_identity,
            "candidate_class_ref": self.candidate_class_ref.as_dict(),
            "service_id": self.service_id,
            "target_use_ref": self.target_use_ref.as_dict(),
            "release_identity_ref": self.release_identity_ref.as_dict(),
            "bound_target_use_permission_refs": [p.as_dict() for p in self.bound_target_use_permission_refs],
            "bound_permission_refs_are_inputs_not_grants": True,
            "binding_mode": self.binding_mode,
            "requested_source_universe_ref": (self.requested_source_universe_ref.as_dict()
                                              if self.requested_source_universe_ref else None),
            "requested_currentness_claim": self.requested_currentness_claim,
            "requested_purpose": self.requested_purpose,
            "binder_grants_no_authority": True,
        }

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            BINDING_REQUEST_FAMILY,
            f"urn:rawlsing:service-f8-scope-binding-request:sha256:{semantic_hash(self.material())}",
            semantic_hash(self.material()),
        )


@dataclass(frozen=True)
class ServiceApplicabilityF8SourceScopeBinding:
    """Binding material. Carries eligibility scope and provenance. Grants nothing."""

    binding_ref: ExactRef
    binding_request_ref: ExactRef
    applicability_receipt_id: str
    applicability_receipt_replay_identity: str
    service_request_set_identity: str
    service_id: str
    target_use_ref: ExactRef
    candidate_class_ref: ExactRef
    candidate_class_coverage: str
    release_identity_ref: ExactRef
    bound_target_use_permission_refs: tuple[ExactRef, ...]
    admitted_source_universe_refs: tuple[ExactRef, ...]
    admission_provenance: tuple[Mapping[str, Any], ...]
    non_admitted_source_states: tuple[Mapping[str, Any], ...]
    f8_model_rule_refs: tuple[ExactRef, ...]
    f8_rule_hash: str
    f8_algorithm_id: str
    binding_mode: str
    # Repair 1: the requested source is CARRIED on the binding, not discarded.
    # Without this the single-source refinement was inert at evaluation time.
    requested_source_universe_ref: ExactRef | None
    currentness_result: str
    binding_statement: str = BINDING_STATEMENT

    def _require_single_source_binding(self) -> ExactRef:
        """Repair 1: SINGLE_SOURCE_VALIDATION must be semantically binding.

        The requested source is carried on the binding and enforced on EVERY
        validation and evaluation. A binding made for one exact source cannot be
        used to evaluate a different admitted source.
        """
        if self.binding_mode != MODE_SINGLE_SOURCE_VALIDATION:
            raise ServiceF8ScopeBindingError(
                "BINDING_MODE_MISMATCH",
                "single-source enforcement is only defined for SINGLE_SOURCE_VALIDATION bindings",
            )
        if self.requested_source_universe_ref is None:
            raise ServiceF8ScopeBindingError(
                "SINGLE_SOURCE_BINDING_MISSING_REQUESTED_SOURCE",
                "this SINGLE_SOURCE_VALIDATION binding carries no requested source universe ref",
            )
        return self.requested_source_universe_ref

    # -- the two source-touching positive powers ----------------------------
    def assert_query_source_admitted(
        self,
        query: PositionedSubjectPossibilityQuery,
        *,
        request: "ServiceApplicabilityF8ScopeBindingRequest",
        receipt: CandidateClassApplicabilityReceipt,
        rule: PositionedSubjectPossibilityModelRule,
    ) -> Mapping[str, Any]:
        """Power 1. Validate ONE exact F8 query source as admitted. Never selects.

        HQ217: the authoritative request, receipt and rule are REQUIRED. This power
        reports an eligibility claim, so it must not report eligibility derived from
        caller-controlled binding fields. The admitted set is re-derived from the
        receipt and the assertion is made against the RE-DERIVED binding.
        """
        authenticated = _authenticate_binding_against_authority(
            self, request=request, receipt=receipt, rule=rule)
        _require_f8_query(query)
        src = _ref(query.source_universe_ref, "query.source_universe_ref")
        # Repair 1: in single-source mode the query source MUST be the requested
        # source. Membership in the admitted set is not sufficient.
        if authenticated.binding_mode == MODE_SINGLE_SOURCE_VALIDATION:
            want = authenticated._require_single_source_binding()
            if src.key != want.key:
                raise _refusal(
                    "F8_QUERY_SOURCE_NOT_THE_REQUESTED_SOURCE",
                    f"this binding is SINGLE_SOURCE_VALIDATION for source "
                    f"{want.object_id!r}; F8 query source {src.object_id!r} is a different "
                    f"admitted source and may not be evaluated through this binding",
                )
        if src not in set(authenticated.admitted_source_universe_refs):
            raise _refusal(
                "F8_QUERY_SOURCE_NOT_ADMITTED",
                f"F8 query source {src.object_id!r} is not a positively admitted source universe "
                f"under applicability receipt {authenticated.applicability_receipt_id!r} as "
                f"re-derived from the authoritative receipt; this binder validates admission "
                f"and never chooses a substitute",
            )
        if query.release_ref != authenticated.release_identity_ref:
            raise _refusal(
                "F8_QUERY_RELEASE_GRAIN_MISMATCH",
                f"F8 query release {query.release_ref.object_id!r} does not equal the bound "
                f"applicability release {authenticated.release_identity_ref.object_id!r}; "
                f"admission is decided per release identity and may not be inherited across "
                f"releases",
            )
        prov = authenticated._provenance_for(src)
        return {
            "source_universe_ref": src.as_dict(),
            "release_identity_ref": authenticated.release_identity_ref.as_dict(),
            "admitted": True,
            "admission_re_derived_from_authoritative_receipt": True,
            "applicability_public_typed_state": POSITIVE_PUBLIC_STATE,
            "admission_provenance": prov,
            "f8_query_ref": query.ref.as_dict(),
            "f8_query_source_confidence": "ELIGIBLE_FOR_SOURCE_SCOPE_ONLY",
            "not_conditioning": True,
            "not_a_selection_among_sources": True,
            "no_ranking_or_priority_implied": True,
        }

    def expose_unranked_admitted_source_set(
        self,
        *,
        request: "ServiceApplicabilityF8ScopeBindingRequest",
        receipt: CandidateClassApplicabilityReceipt,
        rule: PositionedSubjectPossibilityModelRule,
    ) -> tuple[ExactRef, ...]:
        """Power 2. The COMPLETE UNRANKED admitted set, for source-indexed F8 use.

        Exposing the SET is itself an exhaustive claim, so this method requires
        COMPLETE applicability coverage in EVERY binding mode, not only in the
        exhaustive mode. An INCOMPLETE class may still validate a single
        known-admitted source (power 1), but it may never be presented as the
        complete admissible set however the binding was created.

        HQ217: the authoritative request, receipt and rule are REQUIRED, and the set
        returned is the RE-DERIVED admitted set. A forged binding's own admitted tuple
        is never returned, because that tuple is caller-controlled.
        """
        authenticated = _authenticate_binding_against_authority(
            self, request=request, receipt=receipt, rule=rule)
        assert_complete_coverage_from_binding(authenticated)
        return tuple(authenticated.admitted_source_universe_refs)

    # -- refusals that are deliberately loud, not silent --------------------
    def first_admitted_source(self) -> "Any":
        raise _refusal(
            "BINDING_REFUSES_SOURCE_CHOICE",
            "this binder exposes an UNRANKED SET and has no first/best/latest/local/preferred "
            "source; choosing one would be source selection, which is not authorized "
            f"({AUTHORISED_AUTHORITY})",
        )

    def ranked_sources(self) -> "Any":
        raise _refusal(
            "BINDING_REFUSES_RANKING",
            "this binder carries no rank, score, weight, priority or preference; the emitted order "
            f"is {ORDERING_SEMANTICS}",
        )

    def pooled_source_set(self) -> "Any":
        raise _refusal(
            "BINDING_REFUSES_POOLING",
            "admitted sources remain separate source-indexed entries; the cardinality of this set is "
            "not a sample size and no pooling or cross-source composition is performed here",
        )

    def conditioned_f8_geometry(self) -> "Any":
        raise _refusal(
            "BINDING_REFUSES_F8_CONDITIONING",
            "eligibility is not conditioning; an admitted source may bound F8's source SCOPE and may "
            "not become a conditioner, and F8 performs no geometry or distribution transformation "
            f"({EXPECTED_F8_ALGORITHM_ID})",
        )

    def grant_target_use_permission(self) -> "Any":
        raise _refusal(
            "BINDING_REFUSES_PERMISSION_GRANT",
            "target-use permission refs are BOUND INPUTS carried from the applicability request; "
            "binding them here neither grants them nor re-issues them",
        )

    def currentness_authority(self) -> "Any":
        raise _refusal(
            "BINDING_REFUSES_CURRENTNESS_AUTHORITY",
            "currency/availability is a separate lifecycle power; this binder carries a currentness "
            "RESULT only when one was explicitly supplied and validated, and is never its authority",
        )

    def infer_individual_state(self) -> "Any":
        raise _refusal(
            "BINDING_REFUSES_ACTOR_INFERENCE",
            "this seam is source-free and actor-free; no individual, person, belief, response or "
            "actor state may be inferred from an admitted source scope",
        )

    def assert_binding_does_not_authorize(self, purpose: str) -> None:
        """Refuse every forbidden purpose by raising. Never returns a grant."""
        ServiceApplicabilityF8ScopeBindingRequest._refuse_if_forbidden_purpose(purpose)

    # -- provenance --------------------------------------------------------
    def _provenance_for(self, src: ExactRef) -> Mapping[str, Any]:
        for row in self.admission_provenance:
            if row["source_universe_ref"] == src.as_dict():
                return row
        raise _refusal(
            "ADMISSION_PROVENANCE_MISSING",
            f"no admission provenance recorded for admitted source {src.object_id!r}; an admitted "
            f"entry without provenance may not be bound",
        )

    def material(self) -> Mapping[str, Any]:
        return {
            "contract": BINDING_CONTRACT_ID,
            "implementation": BINDING_IMPLEMENTATION_ID,
            "family": BINDING_FAMILY,
            "binding_ref": self.binding_ref.as_dict(),
            "binding_request_ref": self.binding_request_ref.as_dict(),
            "applicability_receipt_id": self.applicability_receipt_id,
            "applicability_receipt_replay_identity": self.applicability_receipt_replay_identity,
            "applicability_authorised_authority": AUTHORISED_AUTHORITY,
            "service_request_set_identity": self.service_request_set_identity,
            "service_id": self.service_id,
            "target_use_ref": self.target_use_ref.as_dict(),
            "candidate_class_ref": self.candidate_class_ref.as_dict(),
            "candidate_class_coverage": self.candidate_class_coverage,
            "release_identity_ref": self.release_identity_ref.as_dict(),
            "bound_target_use_permission_refs": [p.as_dict() for p in self.bound_target_use_permission_refs],
            "bound_permission_refs_are_inputs_not_grants": True,
            "admitted_source_universe_refs": [s.as_dict() for s in self.admitted_source_universe_refs],
            "admitted_entries_remain_separate_source_indexed": True,
            "admitted_set_cardinality_is_not_a_sample_size": True,
            "admission_provenance": [dict(p) for p in self.admission_provenance],
            "non_admitted_source_states": [dict(s) for s in self.non_admitted_source_states],
            "f8_model_rule_refs": [r.as_dict() for r in self.f8_model_rule_refs],
            "f8_rule_hash": self.f8_rule_hash,
            "f8_algorithm_id": self.f8_algorithm_id,
            "f8_does_not_transform_possibility_geometry": True,
            "binding_mode": self.binding_mode,
            # Repair 1: the ENFORCED single-source refinement is part of the binding
            # material, so it is part of the replay identity. Without this a
            # single-source binding for A could not be distinguished from one for B.
            "requested_source_universe_ref": (self.requested_source_universe_ref.as_dict()
                                              if self.requested_source_universe_ref else None),
            "single_source_refinement_is_enforced_at_validation": True,
            "currentness_result": self.currentness_result,
            "binding_statement": self.binding_statement,
            "ordering_semantics": ORDERING_SEMANTICS,
            "canonical_order_grants_no_rank_priority_preference_weight_or_fallback": True,
            "non_collapse_laws": list(NON_COLLAPSE_LAWS),
            "forbidden_binding_purposes": list(FORBIDDEN_BINDING_PURPOSES),
            "grants_no_authority": True,
        }

    def replay_identity(self) -> str:
        return semantic_hash(self.material())

    def as_dict(self) -> dict[str, Any]:
        return {**self.material(), "replay_identity": self.replay_identity()}


def _require_f8_query(query: Any) -> PositionedSubjectPossibilityQuery:
    if not isinstance(query, PositionedSubjectPossibilityQuery):
        raise _refusal("BINDING_INTEGRITY_FAILURE", "query must be a PositionedSubjectPossibilityQuery")
    return query


def _require_f8_rule(rule: Any) -> PositionedSubjectPossibilityModelRule:
    if not isinstance(rule, PositionedSubjectPossibilityModelRule):
        raise _refusal("BINDING_INTEGRITY_FAILURE", "rule must be a PositionedSubjectPossibilityModelRule")
    if rule.algorithm_id != EXPECTED_F8_ALGORITHM_ID:
        raise _refusal(
            "F8_ALGORITHM_NOT_EXACT_CONDITIONAL_LOOKUP",
            f"this binder is written against {EXPECTED_F8_ALGORITHM_ID}; F8 now reports "
            f"{rule.algorithm_id!r}, so the F8 law must be re-adjudicated before binding",
        )
    if rule.model_rule_id != EXPECTED_F8_MODEL_RULE_ID:
        raise _refusal("F8_MODEL_RULE_NOT_RECOGNISED", f"unrecognised model rule {rule.model_rule_id!r}")
    return rule


def assert_complete_coverage_from_binding(binding: ServiceApplicabilityF8SourceScopeBinding) -> None:
    """Exhaustive use of the admitted SET requires COMPLETE applicability coverage."""
    if binding.candidate_class_coverage != COVERAGE_COMPLETE:
        raise _refusal(
            "APPLICABILITY_COVERAGE_INCOMPLETE",
            f"exhaustive use of the admitted source set requires COMPLETE applicability coverage, but "
            f"coverage is {binding.candidate_class_coverage}; a partial class may still validate a "
            f"single known-admitted source but may never be presented as the complete admissible set",
        )


def bind_service_applicability_to_f8_scope(
    *,
    request: ServiceApplicabilityF8ScopeBindingRequest,
    receipt: CandidateClassApplicabilityReceipt,
    rule: PositionedSubjectPossibilityModelRule,
    currentness_result: str | None = None,
) -> ServiceApplicabilityF8SourceScopeBinding:
    """Bind one exact applicability receipt to one exact F8 source scope.

    Positive powers, exhaustively:
      1. validate one exact F8 query source as admitted (see assert_query_source_admitted);
      2. expose the complete UNRANKED admitted source set (see expose_unranked_admitted_source_set).

    This function performs no selection, no ranking, no ordering preference, no
    pooling, no permission grant, and passes nothing to F8.
    """
    if not isinstance(request, ServiceApplicabilityF8ScopeBindingRequest):
        raise _refusal("BINDING_INTEGRITY_FAILURE", "request must be a ServiceApplicabilityF8ScopeBindingRequest")
    if not isinstance(receipt, CandidateClassApplicabilityReceipt):
        raise _refusal(
            "BINDING_INTEGRITY_FAILURE",
            "receipt must be an adopted CandidateClassApplicabilityReceipt; this binder reads "
            "applicability and never derives it",
        )
    _require_f8_rule(rule)

    # -- authority label: refuse a receipt that is not the ratified form -----
    if receipt.authorised_authority != AUTHORISED_AUTHORITY:
        raise _refusal(
            "BINDING_AUTHORITY_LABEL_MISMATCH",
            f"receipt authority {receipt.authorised_authority!r} is not the ratified "
            f"{AUTHORISED_AUTHORITY!r}",
        )

    # -- request / receipt grain identity -----------------------------------
    if request.service_request_set_identity != receipt.service_request_set_identity:
        raise _refusal(
            "BINDING_REQUEST_RECEIPT_GRAIN_MISMATCH",
            f"binding request identity {request.service_request_set_identity!r} does not equal the "
            f"receipt's service request set identity {receipt.service_request_set_identity!r}; a "
            f"binding may never span two service requests",
        )
    if request.service_id != receipt.service_id:
        raise _refusal("BINDING_SERVICE_GRAIN_MISMATCH",
                       f"binding service {request.service_id!r} does not equal receipt service {receipt.service_id!r}")
    if request.candidate_class_ref.as_dict() != dict(receipt.candidate_class_ref):
        raise _refusal(
            "BINDING_CANDIDATE_CLASS_MISMATCH",
            "binding candidate class does not equal the receipt's candidate class; a binding may never "
            "widen or substitute the positively bounded candidate class",
        )
    if request.target_use_ref.as_dict() != dict(receipt.request_key.get("target_use_ref", request.target_use_ref.as_dict())):
        raise _refusal("BINDING_TARGET_USE_GRAIN_MISMATCH",
                       "binding target use does not equal the receipt's target use")

    # -- bound target-use permission identity coherence ----------------------
    # HQ254 P01 CANDIDATE. Quarantined correction, NOT adopted security authority.
    #
    # Applicability is decided under the exact target_use_permission_refs carried in
    # the receipt's request key; the receipt itself declares those refs to be "bound
    # input not a grant". A binding that declares a DIFFERENT permission set is
    # therefore describing applicability that was never decided. Before this check the
    # binder copied the divergent set verbatim into the binding's canonical material,
    # where downstream attestation would read it as the admitted one.
    #
    # This is the exact missing sibling of BINDING_TARGET_USE_GRAIN_MISMATCH above:
    # the same fail-closed grain-coherence intent, one field that had no check at all.
    # It grants no permission, widens no source-scope power, demands no F8 producer
    # custody, and adds no model use. It only refuses to emit a binding whose declared
    # permissions disagree with the receipt it claims to consume.
    receipt_permission_refs = receipt.request_key.get("target_use_permission_refs", ())
    declared_permission_refs = tuple(request.bound_target_use_permission_refs or ())
    declared_permission_keys = {permission.key for permission in declared_permission_refs}
    receipt_permission_keys = {
        exact_ref(permission, "target_use_permission_ref").key
        for permission in receipt_permission_refs
    }
    if declared_permission_keys != receipt_permission_keys:
        raise _refusal(
            "BINDING_PERMISSION_IDENTITY_MISMATCH",
            f"binding bound_target_use_permission_refs "
            f"{sorted(permission.as_dict()['object_id'] for permission in declared_permission_refs)!r} "
            f"do not equal the receipt's target_use_permission_refs "
            f"{sorted(permission.get('object_id') for permission in receipt_permission_refs)!r}; a "
            f"binding may never re-describe applicability that was decided under a different "
            f"bound target-use permission set",
        )

    # -- release grain ------------------------------------------------------
    receipt_releases = {d.release_identity_ref["object_id"] for d in receipt.decisions}
    if request.release_identity_ref.object_id not in receipt_releases:
        raise _refusal(
            "BINDING_RELEASE_GRAIN_MISMATCH",
            f"bound release {request.release_identity_ref.object_id!r} is not a release decided in "
            f"receipt {receipt.receipt_id!r} (decided: {sorted(receipt_releases)}); applicability is "
            f"decided per release identity",
        )

    # -- coverage -----------------------------------------------------------
    if receipt.candidate_class_coverage not in COVERAGE_VALUES:
        raise _refusal("BINDING_INTEGRITY_FAILURE", "unknown applicability coverage")
    if request.binding_mode == MODE_EXHAUSTIVE_UNRANKED_SET:
        # Checked directly rather than by translating the adopted owner's private
        # refusal type, so a caller sees ONE typed refusal surface from this binder.
        if receipt.candidate_class_coverage != COVERAGE_COMPLETE:
            raise _refusal(
                "APPLICABILITY_COVERAGE_INCOMPLETE",
                f"SERVICE_APPLICABILITY_TO_F8_SOURCE_SCOPE_BINDING requires exhaustive source "
                f"applicability, but candidate class coverage is {receipt.candidate_class_coverage}; "
                f"the operation remains unresolved and no set is emitted",
            )

    # -- admitted set, per-source provenance --------------------------------
    admitted = tuple(receipt.admissible_source_universe_refs())
    admitted_keys = {s.key for s in admitted}
    provenance: list[Mapping[str, Any]] = []
    non_admitted: list[Mapping[str, Any]] = []
    for d in receipt.decisions:
        src = exact_ref(d.source_universe_ref, "source_universe_ref")
        if d.applicability_decision == POSITIVE_DECISION:
            if src.key not in admitted_keys:
                raise _refusal("BINDING_INTEGRITY_FAILURE",
                               "a positive decision is absent from the admissible set")
            # Repair 3: the off-release positive branch is REMOVED and made
            # FAIL CLOSED. It was dead only because the adopted owner stamps every
            # decision with the request release; if that owner ever became
            # per-decision-release, the old code would have admitted an off-release
            # source into the admitted set. An off-release positive decision now
            # refuses instead of being admitted.
            if d.release_identity_ref.get("object_id") != request.release_identity_ref.object_id:
                raise _refusal(
                    "BINDING_OFF_RELEASE_POSITIVE_DECISION",
                    f"applicability decision for source {src.object_id!r} carries release "
                    f"{d.release_identity_ref.get('object_id')!r} but the binding requests release "
                    f"{request.release_identity_ref.object_id!r}; an off-release positive decision "
                    f"is refused rather than admitted, and the adopted owner is expected to stamp "
                    f"every decision with the request release",
                )
            provenance.append({
                "source_universe_ref": src.as_dict(),
                "release_identity_ref": dict(d.release_identity_ref),
                "admitted": True,
                "bound_to_requested_release": True,
                "admission_authority_ref": (dict(d.admission_authority_ref)
                                            if d.admission_authority_ref else None),
                "admission_provenance_refs": [dict(r) for r in d.admission_provenance_refs],
                "public_typed_state": d.public_typed_state,
            })
        else:
            non_admitted.append({
                "source_universe_ref": src.as_dict(),
                "applicability_decision": d.applicability_decision,
                "public_typed_state": d.public_typed_state,
                "reason_code": d.reason_code,
                "applicability_noncomparable_is_not_f8_evidence_noncomparable": True,
            })

    if not admitted and not receipt.no_applicable_source:
        raise _refusal(
            "BINDING_NO_ADMITTED_SOURCE_AND_NO_TERMINAL_OUTCOME",
            "receipt carries no admitted source but does not carry the first-class "
            "NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS outcome; an empty admitted set may only be bound "
            "when the receipt states that outcome truthfully",
        )

    # -- single-source mode: the requested source must actually be admitted --
    if request.binding_mode == MODE_SINGLE_SOURCE_VALIDATION:
        want = request.requested_source_universe_ref
        assert want is not None
        if want not in set(admitted):
            raise _refusal(
                "REQUESTED_SOURCE_NOT_ADMITTED",
                f"requested source {want.object_id!r} is not a positively admitted source universe; "
                f"a nonpositive applicability result is never treated as an admission",
            )

    # Repair 1: the requested source must also be INSIDE the bound F8 rule's source
    # scope. Previously a single-source binding could name a source the rule does not
    # even span, so the refinement was unrelated to the rule it was bound to.
    if request.binding_mode == MODE_SINGLE_SOURCE_VALIDATION:
        want = request.requested_source_universe_ref
        assert want is not None
        if want not in set(rule.source_universe_refs):
            raise _refusal(
                "REQUESTED_SOURCE_NOT_IN_F8_RULE_SOURCE_SCOPE",
                f"requested source {want.object_id!r} is not among the bound F8 model rule's "
                f"source_universe_refs "
                f"{[s.object_id for s in rule.source_universe_refs]!r}; a single-source binding "
                f"must name a source the bound rule actually spans",
            )

    # -- the F8 rule's source scope must lie inside the admitted set ---------
    outside = [s for s in rule.source_universe_refs if s not in set(admitted)]
    if outside:
        raise _refusal(
            "F8_RULE_SOURCE_OUTSIDE_ADMITTED_SET",
            f"F8 model rule declares source universe(s) {[s.object_id for s in outside]!r} that are not "
            f"positively admitted under applicability; the binder narrows eligibility, it never widens "
            f"the F8 source scope",
        )
    if request.binding_mode == MODE_EXHAUSTIVE_UNRANKED_SET:
        missing = [s for s in admitted if s not in set(rule.source_universe_refs)]
        if missing:
            raise _refusal(
                "F8_RULE_SOURCE_SET_NOT_EXHAUSTIVE",
                f"EXHAUSTIVE_UNRANKED_SET requires the F8 model rule to span every admitted source; "
                f"missing {[s.object_id for s in missing]!r}. The binder never adds a source to the F8 "
                f"rule on the caller's behalf.",
            )

    # -- currentness: carried only when a claim was actually requested ------
    if request.requested_currentness_claim is None:
        currentness = CURRENTNESS_UNREQUESTED
        if currentness_result is not None:
            raise _refusal(
                "CURRENTNESS_RESULT_WITHOUT_CLAIM",
                "a currentness result was supplied but no currentness claim was requested; currentness "
                "is a separate lifecycle power and is never smuggled in unrequested",
            )
    else:
        if currentness_result is None:
            raise _refusal(
                "CURRENTNESS_MISSING_WHEN_CLAIMED",
                f"a currentness claim {request.requested_currentness_claim!r} was requested but no "
                f"currentness result was supplied; missing currentness may not become a positive claim",
            )
        claim = request.requested_currentness_claim.strip().upper()
        observed = currentness_result.strip().upper()
        if claim in REFUSED_CURRENTNESS_RESULTS or observed in REFUSED_CURRENTNESS_RESULTS:
            raise _refusal(
                "CURRENTNESS_MISSING_OR_CONFLICTING",
                f"currentness claim {claim!r} against result {observed!r} is missing or conflicting; "
                f"the binding refuses rather than asserting currency",
            )
        # Repair 4: closed vocabulary. Anything outside the adopted contract's current
        # states is refused rather than recorded.
        if claim not in ADOPTED_CURRENTNESS_STATES or observed not in ACCEPTED_CURRENTNESS_RESULTS:
            raise _refusal(
                "CURRENTNESS_RESULT_OUTSIDE_ADOPTED_VOCABULARY",
                f"currentness claim {claim!r} and result {observed!r} are not both adopted "
                f"currentness states from the currentness compatibility contract; this binder "
                f"records only an accepted adopted vocabulary and never invents one",
            )
        currentness = observed

    material_seed = {
        "request": request.material(),
        "receipt_replay_identity": receipt.replay_identity(),
        "receipt_id": receipt.receipt_id,
        "f8_rule_hash": rule.rule_hash,
        "admitted": [s.as_dict() for s in admitted],
        "currentness_result": currentness,
    }
    binding_hash = semantic_hash(material_seed)
    binding_ref = ExactRef(
        BINDING_FAMILY,
        f"urn:rawlsing:service-f8-scope-binding:sha256:{binding_hash}",
        binding_hash,
    )
    return ServiceApplicabilityF8SourceScopeBinding(
        binding_ref=binding_ref,
        binding_request_ref=request.ref,
        applicability_receipt_id=receipt.receipt_id,
        applicability_receipt_replay_identity=receipt.replay_identity(),
        service_request_set_identity=receipt.service_request_set_identity,
        service_id=receipt.service_id,
        target_use_ref=request.target_use_ref,
        candidate_class_ref=exact_ref(receipt.candidate_class_ref, "candidate_class_ref"),
        candidate_class_coverage=receipt.candidate_class_coverage,
        release_identity_ref=request.release_identity_ref,
        bound_target_use_permission_refs=tuple(request.bound_target_use_permission_refs),
        admitted_source_universe_refs=admitted,
        admission_provenance=tuple(provenance),
        non_admitted_source_states=tuple(non_admitted),
        f8_model_rule_refs=tuple(rule.source_universe_refs),
        f8_rule_hash=rule.rule_hash,
        f8_algorithm_id=rule.algorithm_id,
        binding_mode=request.binding_mode,
        requested_source_universe_ref=request.requested_source_universe_ref,
        currentness_result=currentness,
    )


def evaluate_bound_positioned_subject_possibility(
    *,
    binding: ServiceApplicabilityF8SourceScopeBinding,
    request: ServiceApplicabilityF8ScopeBindingRequest,
    receipt: CandidateClassApplicabilityReceipt,
    query: PositionedSubjectPossibilityQuery,
    rule: PositionedSubjectPossibilityModelRule,
    evidence: Iterable[PossibilitySliceEvidence],
) -> PositionedSubjectPossibilityResult:
    """AUTHENTICATE the binding against the exact authority, then hand query/rule/
    evidence to F8 UNCHANGED.

    HQ217. The authority-consuming path no longer trusts the presented binding.

        ``request`` and ``receipt`` are now REQUIRED. They were optional before, and an
        optional receipt meant the only receipt checks could be skipped entirely.

    The order is the whole point:

      1. AUTHENTICATE. The binding is re-derived from the authoritative request, the
         authoritative applicability receipt and the exact bound F8 rule, and the
         RE-DERIVED binding is what this function uses from here on. A forged binding --
         whether built by direct construction, by ``dataclasses.replace``, or by copying
         a genuine receipt's id and replay identity -- cannot match the re-derivation and
         refuses here. Supplying a genuine receipt does NOT rescue it, because nothing on
         the presented binding is trusted: the admitted set and provenance come from the
         re-derivation.
      2. Rule binding is enforced BY authentication itself: a rule that was not the bound
         rule cannot re-derive the binding, so it refuses at step 1. There is no second
         comparison here, because none can fail.
      3. Confirm the F8 algorithm is still the exact-conditional-lookup law.
      4. Validate this exact query source is admitted AT THIS EXACT RELEASE, against the
         re-derived admitted set.
      5. Call the ADOPTED, UNMODIFIED F8 evaluator with the caller's own objects.

    A ``__post_init__`` shape check or a self-hash would NOT be sufficient here: a caller
    can fabricate a self-consistent binding, so only re-derivation from the authoritative
    receipt can prove an admission.

    It does not edit, reorder, widen, narrow, reweight or retarget anything, and it
    never inspects or alters conditioners. Narrowing eligibility may change WHICH
    pre-materialized slice F8 selects; the geometry is untouched either way.
    """
    # 1. AUTHENTICATE. Everything below reads `authenticated`, never `binding`.
    authenticated = _authenticate_binding_against_authority(
        binding, request=request, receipt=receipt, rule=rule)
    _require_f8_query(query)
    bound_rule = _require_f8_rule(rule)

    # 2. RULE BINDING IS ENFORCED BY AUTHENTICATION, not by a second comparison here.
    #    The old explicit `bound_rule.rule_hash != binding.f8_rule_hash` check became
    #    UNREACHABLE once authentication was added: the authenticated binding derives its
    #    f8_rule_hash from this very rule object, so the comparison can never be false.
    #    Leaving unreachable code with a comment overstating its role is precisely the
    #    dead-branch defect class the HQ211 review raised as F3, so it is removed rather
    #    than retained as decoration. A tampered rule now refuses during authentication,
    #    because re-deriving from it cannot reproduce the binding.
    assert bound_rule.rule_hash == authenticated.f8_rule_hash, (
        "authentication must derive the binding from the presented rule; a mismatch here "
        "would mean the authentication path is broken"
    )

    # 4. this exact query source must be admitted, per the RE-DERIVED authority
    authenticated.assert_query_source_admitted(
        query, request=request, receipt=receipt, rule=rule)

    # 5. delegate to the adopted F8 evaluator, unchanged
    return evaluate_positioned_subject_possibility(query=query, rule=rule, evidence=evidence)


def _authenticate_binding_against_authority(
    binding: "ServiceApplicabilityF8SourceScopeBinding",
    *,
    request: "ServiceApplicabilityF8ScopeBindingRequest",
    receipt: CandidateClassApplicabilityReceipt,
    rule: PositionedSubjectPossibilityModelRule,
) -> "ServiceApplicabilityF8SourceScopeBinding":
    """AUTHENTICATE a binding against the exact authoritative material, or refuse.

    HQ217. Every authority-consuming path in this module calls this FIRST. The binding
    dataclass is a PUBLIC, directly constructible, ``dataclasses.replace``-able value, so
    its fields -- including ``admitted_source_universe_refs``, ``admission_provenance``,
    ``binding_mode``, ``requested_source_universe_ref``, ``f8_rule_hash``,
    ``binding_ref`` and the copied receipt identity fields -- are ATTACKER CONTROLLED.
    A self-consistent hash or a ``__post_init__`` shape check proves nothing, because a
    caller can fabricate a self-consistent binding.

    The only thing that cannot be fabricated is the binding that the AUTHORITATIVE
    receipt and request and rule actually derive. So this function RE-DERIVES the
    binding from those exact inputs and returns the RE-DERIVED object. Callers must use
    the returned object, never the one they were handed: that is what stops forged
    material from reaching F8 or being reported as an admission.

    Returns the authenticated, re-derived binding.
    """
    if not isinstance(binding, ServiceApplicabilityF8SourceScopeBinding):
        raise _refusal("BINDING_INTEGRITY_FAILURE",
                       "binding must be a ServiceApplicabilityF8SourceScopeBinding")
    if not isinstance(request, ServiceApplicabilityF8ScopeBindingRequest):
        raise _refusal(
            "BINDING_AUTHORITY_INPUTS_REQUIRED",
            "the exact binding request is REQUIRED to authenticate a binding; a binding "
            "cannot be authenticated from its own fields, because every field on it is "
            "caller-controlled",
        )
    if not isinstance(receipt, CandidateClassApplicabilityReceipt):
        raise _refusal(
            "BINDING_AUTHORITY_INPUTS_REQUIRED",
            "the authoritative applicability receipt is REQUIRED to authenticate a binding; "
            "the admitted set is re-derived from it and never trusted from the binding",
        )
    bound_rule = _require_f8_rule(rule)

    # The currentness result is part of the binding material, so it must be recovered to
    # re-derive exactly. Recovery is safe: re-derivation re-validates it against the
    # request, so a fabricated currentness result refuses rather than being accepted.
    recovered_currentness = (
        None if binding.currentness_result == CURRENTNESS_UNREQUESTED
        else binding.currentness_result
    )

    authenticated = verify_service_f8_scope_binding_replay(
        binding,
        request=request,
        receipt=receipt,
        rule=bound_rule,
        currentness_result=recovered_currentness,
    )
    if authenticated.material() != binding.material():
        # Defensive: the replay verifier already compares material. Kept as an explicit
        # second gate so a future weakening of the verifier cannot silently reopen this.
        raise _refusal(
            "BINDING_NOT_AUTHENTICATED_AGAINST_AUTHORITY",
            "the presented binding material does not equal the material re-derived from the "
            "authoritative request, applicability receipt and bound F8 rule",
        )
    return authenticated


def verify_service_f8_scope_binding_replay(
    expected: ServiceApplicabilityF8SourceScopeBinding,
    *,
    request: ServiceApplicabilityF8ScopeBindingRequest,
    receipt: CandidateClassApplicabilityReceipt,
    rule: PositionedSubjectPossibilityModelRule,
    currentness_result: str | None = None,
) -> ServiceApplicabilityF8SourceScopeBinding:
    """Re-derive the binding and prove it is identical. Mismatch refuses."""
    replayed = bind_service_applicability_to_f8_scope(
        request=request, receipt=receipt, rule=rule, currentness_result=currentness_result
    )
    if replayed.replay_identity() != expected.replay_identity() or replayed.material() != expected.material():
        raise _refusal(
            "BINDING_REPLAY_MISMATCH",
            "re-derived service-to-F8 scope binding does not match the expected binding; provenance "
            "or replay inputs changed",
        )
    return replayed


__all__ = [
    "BINDING_CONTRACT_ID", "BINDING_IMPLEMENTATION_ID", "BINDING_FAMILY", "BINDING_REQUEST_FAMILY",
    "BINDING_STATEMENT", "EXPECTED_F8_ALGORITHM_ID", "EXPECTED_F8_MODEL_RULE_ID",
    "FORBIDDEN_BINDING_PURPOSES", "NON_COLLAPSE_LAWS", "BINDING_MODES",
    "MODE_SINGLE_SOURCE_VALIDATION", "MODE_EXHAUSTIVE_UNRANKED_SET", "CURRENTNESS_UNREQUESTED",
    "TWO_SOURCE_TOUCHING_POWERS", "NON_POWER_RETURNING_CALLABLES", "GUARD_ONLY_CALLABLES",
    "DELEGATING_EVALUATOR_IS_NOT_A_POWER_BECAUSE", "NO_THIRD_POWER_OVER_SOURCES",
    "ACCEPTED_CURRENTNESS_RESULTS", "REFUSED_CURRENTNESS_RESULTS",
    "ACCEPTED_CURRENTNESS_RESULTS_ARE_ADOPTED",
    "ServiceF8ScopeBindingError", "ServiceApplicabilityF8ScopeBindingRequest",
    "ServiceApplicabilityF8SourceScopeBinding", "bind_service_applicability_to_f8_scope",
    "evaluate_bound_positioned_subject_possibility", "verify_service_f8_scope_binding_replay",
    "assert_complete_coverage_from_binding",
]
