"""SDTF R4 K1/K4 proof and type-specific witness-currentness interface.

This module implements only the adopted proof/currentness seam.  It deliberately
contains no universal witness record, no source authority, and no actor-fact
constructor.  Domain owners adapt their native witness/state records through the
``TypeSpecificWitnessAdapterR1`` protocol and expose only proof-visible checks.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol, runtime_checkable

INTERFACE_ID = "SDTF_R4_K1_K4_WITNESS_CURRENTNESS_INTERFACE_R1@1.0.0"
ACTIVE_UMBRELLA_DESCRIPTOR = "ACTIVE"


class AssertionKind(str, Enum):
    K1_CONSTITUTIVE_POSITIONAL = "K1_CONSTITUTIVE_POSITIONAL"
    K2_QUALIFIED_POSSIBILITY = "K2_QUALIFIED_POSSIBILITY"
    K3_REALIZED_OCCURRENCE = "K3_REALIZED_OCCURRENCE"
    K4_ACTIVE_DURATIVE = "K4_ACTIVE_DURATIVE"


class Polarity(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"


class FactCurrentness(str, Enum):
    CURRENT = "CURRENT"
    HISTORICAL_NONCURRENT = "HISTORICAL_NONCURRENT"


class Modality(str, Enum):
    ACTUAL = "ACTUAL"
    PROJECTED_COUNTERFACTUAL = "PROJECTED_COUNTERFACTUAL"


class ProofAdjudication(str, Enum):
    PROVEN = "PROVEN"
    UNKNOWN_NOT_PROVEN = "UNKNOWN_NOT_PROVEN"


class TriState(str, Enum):
    YES = "YES"
    NO = "NO"
    UNKNOWN = "UNKNOWN"


class CheckState(str, Enum):
    CURRENT = "CURRENT"
    REPLACED = "REPLACED"
    REVOKED = "REVOKED"
    UNKNOWN_NOT_PROVEN = "UNKNOWN_NOT_PROVEN"


class WitnessLifecycle(str, Enum):
    CURRENT = "CURRENT"
    REVOKED = "REVOKED"


class WitnessCurrentness(str, Enum):
    CURRENT = "CURRENT"
    STALE_REQUIRES_REPLAY = "STALE_REQUIRES_REPLAY"
    REVOKED = "REVOKED"
    UNKNOWN_NOT_PROVEN = "UNKNOWN_NOT_PROVEN"


class K4ProofPath(str, Enum):
    PATH_A_DIRECT_INTERVAL = "PATH_A_DIRECT_INTERVAL"
    PATH_B_CONTINUING_STATE = "PATH_B_CONTINUING_STATE"


@dataclass(frozen=True)
class AssertionRequestR1:
    """Orthogonal assertion axes plus exact owner/type binding.

    ``query_context`` is intentionally opaque.  The type-specific owner decides
    how its native actor/context/time interval is represented and interpreted.
    """

    assertion_kind: AssertionKind
    polarity: Polarity
    currentness: FactCurrentness
    modality: Modality
    required_owner_contract_ref: str
    required_witness_type_ref: str
    query_context: Any = None
    operative_descriptor: str | None = None


@dataclass(frozen=True)
class CurrentnessCheckR1:
    """One proof-visible authority/dependency check emitted by a type adapter."""

    role: str
    expected_ref: str
    observed_ref: str | None
    state: CheckState


@dataclass(frozen=True)
class WitnessCurrentnessEvidenceR1:
    """Adapter output for currentness only; not a witness record schema."""

    owner_contract_ref: str
    witness_type_ref: str
    witness_ref: str
    lifecycle: WitnessLifecycle
    authority_checks: tuple[CurrentnessCheckR1, ...]
    invalidating_dependency_checks: tuple[CurrentnessCheckR1, ...] = ()


@dataclass(frozen=True)
class WitnessCurrentnessDecisionR1:
    currentness: WitnessCurrentness
    reason: str
    first_failing_role: str | None = None
    expected_ref: str | None = None
    observed_ref: str | None = None


@dataclass(frozen=True)
class K4PathAEvidenceR1:
    competent_current_interval_witness: TriState
    covers_asserted_interval: TriState
    freshness_or_recurrence_satisfied: TriState


@dataclass(frozen=True)
class K4PathBEvidenceR1:
    owner_declares_continuing_state: TriState
    type_compatible_state_support: TriState
    support_interval_overlaps_asserted_or_query_interval: TriState
    complete_termination_supersession_invalidation_coverage_through_query: TriState
    defeating_closing_fact: TriState


@dataclass(frozen=True)
class AdjudicationResultR1:
    assertion_kind: AssertionKind
    polarity: Polarity
    currentness: FactCurrentness
    modality: Modality
    proof_adjudication: ProofAdjudication
    witness_currentness: WitnessCurrentness
    reason: str
    k4_path: K4ProofPath | None = None
    first_failing_role: str | None = None
    operative_descriptor: str | None = None


@runtime_checkable
class TypeSpecificWitnessAdapterR1(Protocol):
    """Contract for an owner adapter over a native witness/state record.

    The protocol intentionally does not prescribe fields on ``native_witness``.
    Each owner remains responsible for source/type semantics and for deciding
    which replay inputs are invalidating.  Unrelated replay churn therefore need
    not be reported as an invalidating dependency, which preserves K4 Path B.
    """

    owner_contract_ref: str
    witness_type_ref: str

    def currentness_evidence(
        self, native_witness: Any, request: AssertionRequestR1
    ) -> WitnessCurrentnessEvidenceR1: ...

    def positive_proof(
        self, native_witness: Any, request: AssertionRequestR1
    ) -> TriState: ...

    def explicit_negative_proof(
        self, native_witness: Any, request: AssertionRequestR1
    ) -> TriState: ...

    def k4_path(
        self, native_witness: Any, request: AssertionRequestR1
    ) -> K4ProofPath | None: ...

    def k4_path_a_evidence(
        self, native_witness: Any, request: AssertionRequestR1
    ) -> K4PathAEvidenceR1 | None: ...

    def k4_path_b_evidence(
        self, native_witness: Any, request: AssertionRequestR1
    ) -> K4PathBEvidenceR1 | None: ...


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _unknown_result(
    request: AssertionRequestR1,
    *,
    witness_currentness: WitnessCurrentness,
    reason: str,
    k4_path: K4ProofPath | None = None,
    first_failing_role: str | None = None,
) -> AdjudicationResultR1:
    return AdjudicationResultR1(
        request.assertion_kind,
        request.polarity,
        request.currentness,
        request.modality,
        ProofAdjudication.UNKNOWN_NOT_PROVEN,
        witness_currentness,
        reason,
        k4_path,
        first_failing_role,
        request.operative_descriptor,
    )


def _proven_result(
    request: AssertionRequestR1,
    *,
    k4_path: K4ProofPath | None = None,
) -> AdjudicationResultR1:
    return AdjudicationResultR1(
        request.assertion_kind,
        request.polarity,
        request.currentness,
        request.modality,
        ProofAdjudication.PROVEN,
        WitnessCurrentness.CURRENT,
        "proof-contract-satisfied",
        k4_path,
        None,
        request.operative_descriptor,
    )


def evaluate_witness_currentness_r1(
    evidence: WitnessCurrentnessEvidenceR1,
    *,
    required_owner_contract_ref: str,
    required_witness_type_ref: str,
) -> WitnessCurrentnessDecisionR1:
    """Evaluate proof-visible currentness before any witness-bearing truth is used."""

    if not isinstance(evidence, WitnessCurrentnessEvidenceR1):
        return WitnessCurrentnessDecisionR1(
            WitnessCurrentness.UNKNOWN_NOT_PROVEN, "currentness-evidence-malformed"
        )
    if not _nonempty(required_owner_contract_ref) or not _nonempty(required_witness_type_ref):
        return WitnessCurrentnessDecisionR1(
            WitnessCurrentness.UNKNOWN_NOT_PROVEN, "required-owner-or-type-unbound"
        )
    if not all(
        _nonempty(v)
        for v in (evidence.owner_contract_ref, evidence.witness_type_ref, evidence.witness_ref)
    ):
        return WitnessCurrentnessDecisionR1(
            WitnessCurrentness.UNKNOWN_NOT_PROVEN, "adapter-owner-type-or-witness-unbound"
        )
    if evidence.owner_contract_ref != required_owner_contract_ref:
        return WitnessCurrentnessDecisionR1(
            WitnessCurrentness.STALE_REQUIRES_REPLAY,
            "owner-contract-binding-changed",
            "owner_contract",
            required_owner_contract_ref,
            evidence.owner_contract_ref,
        )
    if evidence.witness_type_ref != required_witness_type_ref:
        return WitnessCurrentnessDecisionR1(
            WitnessCurrentness.STALE_REQUIRES_REPLAY,
            "witness-type-binding-changed",
            "witness_type",
            required_witness_type_ref,
            evidence.witness_type_ref,
        )
    if evidence.lifecycle is WitnessLifecycle.REVOKED:
        return WitnessCurrentnessDecisionR1(
            WitnessCurrentness.REVOKED, "witness-explicitly-revoked", "witness_lifecycle"
        )
    if evidence.lifecycle is not WitnessLifecycle.CURRENT:
        return WitnessCurrentnessDecisionR1(
            WitnessCurrentness.UNKNOWN_NOT_PROVEN,
            "witness-lifecycle-unknown",
            "witness_lifecycle",
        )
    if not evidence.authority_checks:
        return WitnessCurrentnessDecisionR1(
            WitnessCurrentness.UNKNOWN_NOT_PROVEN,
            "authority-currentness-not-proved",
            "authority_checks",
        )

    for check in evidence.authority_checks + evidence.invalidating_dependency_checks:
        if not isinstance(check, CurrentnessCheckR1) or not _nonempty(check.role):
            return WitnessCurrentnessDecisionR1(
                WitnessCurrentness.UNKNOWN_NOT_PROVEN, "currentness-check-malformed"
            )
        if check.state is CheckState.CURRENT:
            if not _nonempty(check.expected_ref) or check.observed_ref != check.expected_ref:
                return WitnessCurrentnessDecisionR1(
                    WitnessCurrentness.UNKNOWN_NOT_PROVEN,
                    "current-check-reference-not-proved",
                    check.role,
                    check.expected_ref,
                    check.observed_ref,
                )
            continue
        if check.state is CheckState.REVOKED:
            return WitnessCurrentnessDecisionR1(
                WitnessCurrentness.REVOKED,
                "authority-or-invalidating-dependency-revoked",
                check.role,
                check.expected_ref,
                check.observed_ref,
            )
        if check.state is CheckState.REPLACED:
            return WitnessCurrentnessDecisionR1(
                WitnessCurrentness.STALE_REQUIRES_REPLAY,
                "authority-or-invalidating-dependency-replaced",
                check.role,
                check.expected_ref,
                check.observed_ref,
            )
        return WitnessCurrentnessDecisionR1(
            WitnessCurrentness.UNKNOWN_NOT_PROVEN,
            "authority-or-invalidating-dependency-currentness-unknown",
            check.role,
            check.expected_ref,
            check.observed_ref,
        )

    return WitnessCurrentnessDecisionR1(WitnessCurrentness.CURRENT, "witness-current")


def _all_yes(values: tuple[TriState, ...]) -> bool:
    return all(value is TriState.YES for value in values)


def _has_unknown(values: tuple[TriState, ...]) -> bool:
    return any(value is TriState.UNKNOWN for value in values)


def adjudicate_assertion_r1(
    request: AssertionRequestR1,
    native_witness: Any,
    adapter: TypeSpecificWitnessAdapterR1,
) -> AdjudicationResultR1:
    """Adjudicate proof without constructing an actor fact.

    Every non-current witness state fails closed to ``UNKNOWN_NOT_PROVEN``.
    Revocation/staleness never manufactures a negative proposition.
    """

    if not isinstance(request, AssertionRequestR1):
        raise TypeError("request must be AssertionRequestR1")
    if not all(
        isinstance(value, enum_type)
        for value, enum_type in (
            (request.assertion_kind, AssertionKind),
            (request.polarity, Polarity),
            (request.currentness, FactCurrentness),
            (request.modality, Modality),
        )
    ):
        return _unknown_result(
            request,
            witness_currentness=WitnessCurrentness.UNKNOWN_NOT_PROVEN,
            reason="assertion-axis-malformed",
        )
    if not _nonempty(request.required_owner_contract_ref) or not _nonempty(
        request.required_witness_type_ref
    ):
        return _unknown_result(
            request,
            witness_currentness=WitnessCurrentness.UNKNOWN_NOT_PROVEN,
            reason="required-owner-or-type-unbound",
        )

    adapter_owner = getattr(adapter, "owner_contract_ref", None)
    adapter_type = getattr(adapter, "witness_type_ref", None)
    if adapter_owner != request.required_owner_contract_ref:
        return _unknown_result(
            request,
            witness_currentness=WitnessCurrentness.STALE_REQUIRES_REPLAY,
            reason="adapter-owner-contract-mismatch",
            first_failing_role="owner_contract",
        )
    if adapter_type != request.required_witness_type_ref:
        return _unknown_result(
            request,
            witness_currentness=WitnessCurrentness.STALE_REQUIRES_REPLAY,
            reason="adapter-witness-type-mismatch",
            first_failing_role="witness_type",
        )

    try:
        evidence = adapter.currentness_evidence(native_witness, request)
    except Exception:
        return _unknown_result(
            request,
            witness_currentness=WitnessCurrentness.UNKNOWN_NOT_PROVEN,
            reason="adapter-currentness-unavailable",
        )
    current = evaluate_witness_currentness_r1(
        evidence,
        required_owner_contract_ref=request.required_owner_contract_ref,
        required_witness_type_ref=request.required_witness_type_ref,
    )
    if current.currentness is not WitnessCurrentness.CURRENT:
        return _unknown_result(
            request,
            witness_currentness=current.currentness,
            reason=current.reason,
            first_failing_role=current.first_failing_role,
        )

    # Negative propositions are independent proof obligations.  Positive failure,
    # staleness, expiration, revocation, or termination never become negative truth.
    if request.polarity is Polarity.NEGATIVE:
        try:
            negative = adapter.explicit_negative_proof(native_witness, request)
        except Exception:
            negative = TriState.UNKNOWN
        if negative is TriState.YES:
            return _proven_result(request)
        return _unknown_result(
            request,
            witness_currentness=WitnessCurrentness.CURRENT,
            reason=(
                "explicit-negative-proof-unknown"
                if negative is TriState.UNKNOWN
                else "explicit-negative-proof-absent"
            ),
        )

    if request.assertion_kind is not AssertionKind.K4_ACTIVE_DURATIVE:
        try:
            positive = adapter.positive_proof(native_witness, request)
        except Exception:
            positive = TriState.UNKNOWN
        if positive is TriState.YES:
            return _proven_result(request)
        return _unknown_result(
            request,
            witness_currentness=WitnessCurrentness.CURRENT,
            reason=(
                "positive-proof-unknown"
                if positive is TriState.UNKNOWN
                else "positive-proof-not-established"
            ),
        )

    try:
        path = adapter.k4_path(native_witness, request)
    except Exception:
        path = None
    if path is K4ProofPath.PATH_A_DIRECT_INTERVAL:
        try:
            proof = adapter.k4_path_a_evidence(native_witness, request)
        except Exception:
            proof = None
        if not isinstance(proof, K4PathAEvidenceR1):
            return _unknown_result(
                request,
                witness_currentness=WitnessCurrentness.CURRENT,
                reason="k4-path-a-evidence-unavailable",
                k4_path=path,
            )
        values = (
            proof.competent_current_interval_witness,
            proof.covers_asserted_interval,
            proof.freshness_or_recurrence_satisfied,
        )
        if _all_yes(values):
            return _proven_result(request, k4_path=path)
        return _unknown_result(
            request,
            witness_currentness=WitnessCurrentness.CURRENT,
            reason=("k4-path-a-proof-unknown" if _has_unknown(values) else "k4-path-a-proof-failed"),
            k4_path=path,
        )

    if path is K4ProofPath.PATH_B_CONTINUING_STATE:
        try:
            proof = adapter.k4_path_b_evidence(native_witness, request)
        except Exception:
            proof = None
        if not isinstance(proof, K4PathBEvidenceR1):
            return _unknown_result(
                request,
                witness_currentness=WitnessCurrentness.CURRENT,
                reason="k4-path-b-evidence-unavailable",
                k4_path=path,
            )
        positive_requirements = (
            proof.owner_declares_continuing_state,
            proof.type_compatible_state_support,
            proof.support_interval_overlaps_asserted_or_query_interval,
            proof.complete_termination_supersession_invalidation_coverage_through_query,
        )
        if _all_yes(positive_requirements) and proof.defeating_closing_fact is TriState.NO:
            return _proven_result(request, k4_path=path)
        all_values = positive_requirements + (proof.defeating_closing_fact,)
        return _unknown_result(
            request,
            witness_currentness=WitnessCurrentness.CURRENT,
            reason=("k4-path-b-proof-unknown" if _has_unknown(all_values) else "k4-path-b-proof-failed"),
            k4_path=path,
        )

    return _unknown_result(
        request,
        witness_currentness=WitnessCurrentness.CURRENT,
        reason="k4-proof-path-not-established",
    )
