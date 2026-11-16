"""Bounded empirical incompleteness runtime contract (OBL063).

This module sits between source/empirical evidence and downstream driver/vector
consumers. It does not create empirical authority, infer missing values, choose
personality semantics, or mutate V3/V2 state.

Core law:
    FULL_SOURCE_CERTIFICATION != APPLICATION_RUNTIME_ADMISSIBLE

Missing evidence stays typed. It never silently becomes numeric zero and never
causes implicit coefficient renormalization.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum
import hashlib
import json
import re
from typing import Any, Mapping, Sequence

CONTRACT_ID = "BOUNDED_EMPIRICAL_INCOMPLETENESS_RUNTIME_CONTRACT@1.0.0"
CANONICAL_PROFILE = "RAWLSING_OBL063_CANONICAL_JSON_V1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class BoundedEmpiricalRuntimeError(ValueError):
    """Base fail-closed runtime-contract error."""


class PopulationClaimAuthorityError(BoundedEmpiricalRuntimeError):
    """A weaker evidence tier was offered as population evidence."""


class RelationAuthorityRequired(BoundedEmpiricalRuntimeError):
    """A source/geo/time substitution lacked exact positive relation authority."""


class MissingAsZeroError(BoundedEmpiricalRuntimeError):
    """A caller attempted to collapse missing evidence into numerical zero."""


class ImplicitRenormalizationError(BoundedEmpiricalRuntimeError):
    """A caller attempted coefficient reallocation without explicit authority."""


class EvidenceTier(str, Enum):
    POPULATION_CERTIFIED = "POPULATION_CERTIFIED"
    SOURCE_LOCAL_CERTIFIED = "SOURCE_LOCAL_CERTIFIED"
    PARTIAL_AUTHORITY = "PARTIAL_AUTHORITY"
    UNAVAILABLE = "UNAVAILABLE"


class ClaimCeiling(str, Enum):
    POPULATION_STATISTIC = "POPULATION_STATISTIC"
    SOURCE_LOCAL_STATISTIC = "SOURCE_LOCAL_STATISTIC"
    SUPPORTED_COMPONENT_ONLY = "SUPPORTED_COMPONENT_ONLY"


class FallbackKind(str, Enum):
    AUTHORIZED_ALTERNATE_SOURCE = "AUTHORIZED_ALTERNATE_SOURCE"
    AUTHORIZED_BROADER_PRIOR = "AUTHORIZED_BROADER_PRIOR"
    VERSIONED_MODEL_PRIOR = "VERSIONED_MODEL_PRIOR"
    WIDEN_UNCERTAINTY = "WIDEN_UNCERTAINTY"
    OMIT_CONTRIBUTION = "OMIT_CONTRIBUTION"


class ContributionClass(str, Enum):
    EMPIRICAL = "EMPIRICAL"
    MODEL_PRIOR = "MODEL_PRIOR"


class DriverRuntimeState(str, Enum):
    ADMISSIBLE_WITH_NUMERIC_CONTRIBUTIONS = "ADMISSIBLE_WITH_NUMERIC_CONTRIBUTIONS"
    ADMISSIBLE_TYPED_NO_NUMERIC_CONTRIBUTION = "ADMISSIBLE_TYPED_NO_NUMERIC_CONTRIBUTION"
    BLOCKED_TERMINAL_REQUIREMENT = "BLOCKED_TERMINAL_REQUIREMENT"


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BoundedEmpiricalRuntimeError(f"{name} must be non-empty text")
    return value.strip()


def _sha256(value: Any, name: str) -> str:
    value = _text(value, name)
    if not SHA256_RE.fullmatch(value):
        raise BoundedEmpiricalRuntimeError(f"{name} must be lowercase sha256")
    return value


def _decimal(value: Any, name: str) -> Decimal:
    if isinstance(value, bool):
        raise BoundedEmpiricalRuntimeError(f"{name} must be finite decimal")
    try:
        out = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise BoundedEmpiricalRuntimeError(f"{name} must be finite decimal") from exc
    if not out.is_finite():
        raise BoundedEmpiricalRuntimeError(f"{name} must be finite decimal")
    return out


def _decimal_text(value: Decimal) -> str:
    normalized = value.normalize()
    out = format(normalized, "f")
    if "." in out:
        out = out.rstrip("0").rstrip(".")
    return out or "0"


def _canonicalize(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Decimal):
        return _decimal_text(value)
    if hasattr(value, "as_dict"):
        return _canonicalize(value.as_dict())
    if isinstance(value, Mapping):
        if any(not isinstance(k, str) for k in value):
            raise BoundedEmpiricalRuntimeError("canonical mapping keys must be strings")
        return {k: _canonicalize(value[k]) for k in sorted(value)}
    if isinstance(value, (tuple, list)):
        return [_canonicalize(x) for x in value]
    if isinstance(value, (set, frozenset)):
        mats = [_canonicalize(x) for x in value]
        return sorted(mats, key=lambda x: json.dumps(x, sort_keys=True, separators=(",", ":")))
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        raise BoundedEmpiricalRuntimeError("float forbidden in receipt identity; use Decimal/text")
    raise BoundedEmpiricalRuntimeError(f"unsupported canonical type {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(
        _canonicalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def semantic_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True, order=True)
class ExactRef:
    kind: str
    object_id: str
    content_hash: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", _text(self.kind, "ref.kind"))
        object.__setattr__(self, "object_id", _text(self.object_id, "ref.object_id"))
        object.__setattr__(self, "content_hash", _sha256(self.content_hash, "ref.content_hash"))

    def as_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "object_id": self.object_id, "content_hash": self.content_hash}


@dataclass(frozen=True)
class FallbackRule:
    kind: FallbackKind
    fallback_id: str
    value: Decimal | None = None
    uncertainty_widening: Decimal | None = None
    relation_authority_ref: ExactRef | None = None
    model_prior_version: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, FallbackKind):
            object.__setattr__(self, "kind", FallbackKind(self.kind))
        object.__setattr__(self, "fallback_id", _text(self.fallback_id, "fallback_id"))
        if self.value is not None:
            object.__setattr__(self, "value", _decimal(self.value, "fallback.value"))
        if self.uncertainty_widening is not None:
            widening = _decimal(self.uncertainty_widening, "fallback.uncertainty_widening")
            if widening < 0:
                raise BoundedEmpiricalRuntimeError("uncertainty widening may not be negative")
            object.__setattr__(self, "uncertainty_widening", widening)

        relation_required = self.kind in {
            FallbackKind.AUTHORIZED_ALTERNATE_SOURCE,
            FallbackKind.AUTHORIZED_BROADER_PRIOR,
        }
        if relation_required and self.relation_authority_ref is None:
            raise RelationAuthorityRequired(
                f"{self.kind.value} requires exact relation/backfill authority"
            )
        if self.kind is FallbackKind.VERSIONED_MODEL_PRIOR:
            if self.value is None:
                raise BoundedEmpiricalRuntimeError(
                    "VERSIONED_MODEL_PRIOR requires an explicit prior value"
                )
            if self.model_prior_version is None:
                raise BoundedEmpiricalRuntimeError(
                    "VERSIONED_MODEL_PRIOR requires model_prior_version"
                )
            object.__setattr__(
                self,
                "model_prior_version",
                _text(self.model_prior_version, "model_prior_version"),
            )
            if self.relation_authority_ref is not None:
                raise BoundedEmpiricalRuntimeError(
                    "model prior must not masquerade as relation-authorized empirical backfill"
                )
        elif self.model_prior_version is not None:
            raise BoundedEmpiricalRuntimeError(
                "model_prior_version is only valid for VERSIONED_MODEL_PRIOR"
            )

        if self.kind in {
            FallbackKind.WIDEN_UNCERTAINTY,
            FallbackKind.OMIT_CONTRIBUTION,
        } and self.value is not None:
            raise BoundedEmpiricalRuntimeError(
                f"{self.kind.value} may not create a numeric contribution"
            )
        if (
            self.kind is FallbackKind.WIDEN_UNCERTAINTY
            and self.uncertainty_widening is None
        ):
            raise BoundedEmpiricalRuntimeError(
                "WIDEN_UNCERTAINTY requires an explicit widening amount"
            )

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "fallback_id": self.fallback_id,
            "value": self.value,
            "uncertainty_widening": self.uncertainty_widening,
            "relation_authority_ref": self.relation_authority_ref,
            "model_prior_version": self.model_prior_version,
        }


@dataclass(frozen=True)
class EvidenceChannelPolicy:
    channel_id: str
    coefficient: Decimal
    claim_ceiling: ClaimCeiling
    required_for_runtime: bool
    fallback: FallbackRule | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "channel_id", _text(self.channel_id, "channel_id"))
        object.__setattr__(self, "coefficient", _decimal(self.coefficient, "coefficient"))
        if self.coefficient < 0:
            raise BoundedEmpiricalRuntimeError(
                "negative evidence coefficients are not permitted"
            )
        if not isinstance(self.claim_ceiling, ClaimCeiling):
            object.__setattr__(
                self, "claim_ceiling", ClaimCeiling(self.claim_ceiling)
            )

    def as_dict(self) -> dict[str, Any]:
        return {
            "channel_id": self.channel_id,
            "coefficient": self.coefficient,
            "claim_ceiling": self.claim_ceiling,
            "required_for_runtime": self.required_for_runtime,
            "fallback": None if self.fallback is None else self.fallback.as_dict(),
        }


@dataclass(frozen=True)
class DriverPolicy:
    driver_id: str
    channels: tuple[EvidenceChannelPolicy, ...]
    allow_typed_no_numeric_driver: bool = False
    policy_version: str = "1.0.0"

    def __post_init__(self) -> None:
        object.__setattr__(self, "driver_id", _text(self.driver_id, "driver_id"))
        object.__setattr__(
            self, "policy_version", _text(self.policy_version, "policy_version")
        )
        channels = tuple(self.channels)
        if not channels:
            raise BoundedEmpiricalRuntimeError(
                "driver policy requires at least one intended channel"
            )
        if len({x.channel_id for x in channels}) != len(channels):
            raise BoundedEmpiricalRuntimeError(
                "duplicate channel_id in driver policy"
            )
        object.__setattr__(
            self, "channels", tuple(sorted(channels, key=lambda x: x.channel_id))
        )

    @property
    def intended_coefficient_mass(self) -> Decimal:
        return sum((x.coefficient for x in self.channels), Decimal("0"))

    def as_dict(self) -> dict[str, Any]:
        return {
            "driver_id": self.driver_id,
            "policy_version": self.policy_version,
            "allow_typed_no_numeric_driver": self.allow_typed_no_numeric_driver,
            "channels": self.channels,
            "coefficient_reallocation_policy": "NO_COEFFICIENT_REALLOCATION",
        }


@dataclass(frozen=True)
class EvidenceContribution:
    driver_id: str
    channel_id: str
    evidence_tier: EvidenceTier
    claim_ceiling: ClaimCeiling
    value: Decimal | None
    source_ref: ExactRef | None
    population_authority_ref: ExactRef | None = None
    weight_authorized: bool | None = None
    estimand_authorized: bool | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "driver_id", _text(self.driver_id, "driver_id"))
        object.__setattr__(self, "channel_id", _text(self.channel_id, "channel_id"))
        if not isinstance(self.evidence_tier, EvidenceTier):
            object.__setattr__(
                self, "evidence_tier", EvidenceTier(self.evidence_tier)
            )
        if not isinstance(self.claim_ceiling, ClaimCeiling):
            object.__setattr__(
                self, "claim_ceiling", ClaimCeiling(self.claim_ceiling)
            )
        if self.value is not None:
            object.__setattr__(
                self, "value", _decimal(self.value, "contribution.value")
            )
        if self.evidence_tier is EvidenceTier.UNAVAILABLE:
            if self.value is not None:
                raise MissingAsZeroError(
                    "UNAVAILABLE evidence may not carry a numeric value, including zero"
                )
            if self.source_ref is not None or self.population_authority_ref is not None:
                raise BoundedEmpiricalRuntimeError(
                    "UNAVAILABLE contribution may not carry positive source/population refs"
                )
        else:
            if self.value is None:
                raise BoundedEmpiricalRuntimeError(
                    "available empirical contribution requires explicit numeric value"
                )
            if self.source_ref is None:
                raise BoundedEmpiricalRuntimeError(
                    "available empirical contribution requires exact source ref"
                )
        if (
            self.evidence_tier is EvidenceTier.POPULATION_CERTIFIED
            and self.population_authority_ref is None
        ):
            raise PopulationClaimAuthorityError(
                "POPULATION_CERTIFIED requires exact population authority ref"
            )
        if (
            self.evidence_tier is not EvidenceTier.POPULATION_CERTIFIED
            and self.population_authority_ref is not None
        ):
            raise PopulationClaimAuthorityError(
                "weaker evidence tier may not carry population authority ref"
            )

    def as_dict(self) -> dict[str, Any]:
        return {
            "driver_id": self.driver_id,
            "channel_id": self.channel_id,
            "evidence_tier": self.evidence_tier,
            "claim_ceiling": self.claim_ceiling,
            "value": self.value,
            "source_ref": self.source_ref,
            "population_authority_ref": self.population_authority_ref,
            "weight_authorized": self.weight_authorized,
            "estimand_authorized": self.estimand_authorized,
        }


@dataclass(frozen=True)
class EffectiveContribution:
    channel_id: str
    coefficient: Decimal
    contribution_class: ContributionClass
    value: Decimal
    evidence_tier: EvidenceTier | None
    claim_ceiling: ClaimCeiling | None
    source_ref: ExactRef | None
    fallback_id: str | None = None
    model_prior_version: str | None = None
    relation_authority_ref: ExactRef | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "channel_id": self.channel_id,
            "coefficient": self.coefficient,
            "contribution_class": self.contribution_class,
            "value": self.value,
            "evidence_tier": self.evidence_tier,
            "claim_ceiling": self.claim_ceiling,
            "source_ref": self.source_ref,
            "fallback_id": self.fallback_id,
            "model_prior_version": self.model_prior_version,
            "relation_authority_ref": self.relation_authority_ref,
        }


@dataclass(frozen=True)
class ChannelDecision:
    channel_id: str
    intended_coefficient: Decimal
    decision: str
    evidence_tier: EvidenceTier | None
    fallback_kind: FallbackKind | None
    uncertainty_widening: Decimal
    relation_authority_ref: ExactRef | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "channel_id": self.channel_id,
            "intended_coefficient": self.intended_coefficient,
            "decision": self.decision,
            "evidence_tier": self.evidence_tier,
            "fallback_kind": self.fallback_kind,
            "uncertainty_widening": self.uncertainty_widening,
            "relation_authority_ref": self.relation_authority_ref,
        }


@dataclass(frozen=True)
class EmpiricalCoverageReceipt:
    contract_id: str
    driver_id: str
    policy_version: str
    policy_hash: str
    intended_channel_count: int
    empirical_contributing_channel_count: int
    model_prior_channel_count: int
    unavailable_channel_count: int
    intended_coefficient_mass: Decimal
    empirical_coefficient_mass: Decimal
    model_prior_coefficient_mass: Decimal
    coefficient_reallocated: bool
    total_uncertainty_widening: Decimal
    channel_decisions: tuple[ChannelDecision, ...]
    receipt_hash: str

    def as_core(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "canonical_profile": CANONICAL_PROFILE,
            "driver_id": self.driver_id,
            "policy_version": self.policy_version,
            "policy_hash": self.policy_hash,
            "intended_channel_count": self.intended_channel_count,
            "empirical_contributing_channel_count": self.empirical_contributing_channel_count,
            "model_prior_channel_count": self.model_prior_channel_count,
            "unavailable_channel_count": self.unavailable_channel_count,
            "intended_coefficient_mass": self.intended_coefficient_mass,
            "empirical_coefficient_mass": self.empirical_coefficient_mass,
            "model_prior_coefficient_mass": self.model_prior_coefficient_mass,
            "coefficient_reallocated": self.coefficient_reallocated,
            "total_uncertainty_widening": self.total_uncertainty_widening,
            "channel_decisions": self.channel_decisions,
        }

    def as_dict(self) -> dict[str, Any]:
        return {
            **_canonicalize(self.as_core()),
            "receipt_hash": self.receipt_hash,
        }


@dataclass(frozen=True)
class DriverRuntimeEnvelope:
    driver_id: str
    state: DriverRuntimeState
    effective_contributions: tuple[EffectiveContribution, ...]
    channel_decisions: tuple[ChannelDecision, ...]
    total_uncertainty_widening: Decimal
    coverage_receipt: EmpiricalCoverageReceipt
    block_reason: str | None = None

    @property
    def runtime_admissible(self) -> bool:
        return self.state is not DriverRuntimeState.BLOCKED_TERMINAL_REQUIREMENT

    @property
    def has_numeric_contribution(self) -> bool:
        return bool(self.effective_contributions)

    def require_legacy_scalar(self) -> Decimal:
        """Never permit typed absence to collapse to a legacy numeric zero."""
        raise MissingAsZeroError(
            "OBL063 does not authorize coercion of its typed envelope to a legacy scalar; "
            "downstream aggregation must consume effective_contributions explicitly"
        )

    def as_dict(self) -> dict[str, Any]:
        return _canonicalize({
            "driver_id": self.driver_id,
            "state": self.state,
            "effective_contributions": self.effective_contributions,
            "channel_decisions": self.channel_decisions,
            "total_uncertainty_widening": self.total_uncertainty_widening,
            "coverage_receipt": self.coverage_receipt.as_dict(),
            "block_reason": self.block_reason,
        })


def _validate_tier_for_policy(
    policy: EvidenceChannelPolicy,
    item: EvidenceContribution,
) -> None:
    if item.claim_ceiling != policy.claim_ceiling:
        raise PopulationClaimAuthorityError(
            f"channel {policy.channel_id} contribution ceiling "
            f"{item.claim_ceiling.value} does not equal policy ceiling "
            f"{policy.claim_ceiling.value}"
        )
    if policy.claim_ceiling is ClaimCeiling.POPULATION_STATISTIC:
        if item.evidence_tier is not EvidenceTier.POPULATION_CERTIFIED:
            raise PopulationClaimAuthorityError(
                f"channel {policy.channel_id} cannot satisfy population claim "
                f"with {item.evidence_tier.value}"
            )
    elif policy.claim_ceiling is ClaimCeiling.SOURCE_LOCAL_STATISTIC:
        if item.evidence_tier not in {
            EvidenceTier.POPULATION_CERTIFIED,
            EvidenceTier.SOURCE_LOCAL_CERTIFIED,
        }:
            raise PopulationClaimAuthorityError(
                f"channel {policy.channel_id} cannot satisfy source-local statistic "
                f"with {item.evidence_tier.value}"
            )
    elif (
        policy.claim_ceiling is ClaimCeiling.SUPPORTED_COMPONENT_ONLY
        and item.evidence_tier is EvidenceTier.UNAVAILABLE
    ):
        raise PopulationClaimAuthorityError(
            "UNAVAILABLE cannot satisfy supported-component use"
        )


def _fallback_effect(
    policy: EvidenceChannelPolicy,
) -> tuple[EffectiveContribution | None, ChannelDecision, bool]:
    rule = policy.fallback
    if rule is None:
        decision = ChannelDecision(
            policy.channel_id,
            policy.coefficient,
            "NO_FALLBACK_DECLARED",
            None,
            None,
            Decimal("0"),
            None,
        )
        return None, decision, policy.required_for_runtime

    numeric: EffectiveContribution | None = None
    widening = rule.uncertainty_widening or Decimal("0")

    if rule.kind in {
        FallbackKind.AUTHORIZED_ALTERNATE_SOURCE,
        FallbackKind.AUTHORIZED_BROADER_PRIOR,
    }:
        if rule.value is None:
            raise BoundedEmpiricalRuntimeError(
                f"{rule.kind.value} requires explicit fallback numeric value"
            )
        numeric = EffectiveContribution(
            policy.channel_id,
            policy.coefficient,
            ContributionClass.EMPIRICAL,
            rule.value,
            EvidenceTier.SOURCE_LOCAL_CERTIFIED,
            ClaimCeiling.SOURCE_LOCAL_STATISTIC,
            rule.relation_authority_ref,
            fallback_id=rule.fallback_id,
            relation_authority_ref=rule.relation_authority_ref,
        )
        decision_text = rule.kind.value
    elif rule.kind is FallbackKind.VERSIONED_MODEL_PRIOR:
        numeric = EffectiveContribution(
            policy.channel_id,
            policy.coefficient,
            ContributionClass.MODEL_PRIOR,
            rule.value,
            None,
            None,
            None,
            fallback_id=rule.fallback_id,
            model_prior_version=rule.model_prior_version,
        )
        decision_text = "VERSIONED_MODEL_PRIOR__NON_EMPIRICAL"
    elif rule.kind is FallbackKind.WIDEN_UNCERTAINTY:
        decision_text = rule.kind.value
    elif rule.kind is FallbackKind.OMIT_CONTRIBUTION:
        decision_text = rule.kind.value
    else:
        raise BoundedEmpiricalRuntimeError("unknown fallback kind")

    decision = ChannelDecision(
        policy.channel_id,
        policy.coefficient,
        decision_text,
        None,
        rule.kind,
        widening,
        rule.relation_authority_ref,
    )
    return numeric, decision, False


def resolve_driver_runtime(
    policy: DriverPolicy,
    contributions: Sequence[EvidenceContribution],
    *,
    requested_coefficient_reallocation: Mapping[str, Decimal] | None = None,
) -> DriverRuntimeEnvelope:
    """Resolve one driver without inventing missing empirical evidence.

    The function preserves channel coefficients exactly. It never computes a
    final driver scalar; downstream aggregation remains separately governed.
    """
    if requested_coefficient_reallocation:
        raise ImplicitRenormalizationError(
            "coefficient reallocation is not authorized by OBL063 R1; "
            "surviving channels keep declared coefficients"
        )

    by_channel: dict[str, EvidenceContribution] = {}
    for item in contributions:
        if item.driver_id != policy.driver_id:
            raise BoundedEmpiricalRuntimeError(
                "contribution driver_id does not match policy"
            )
        if item.channel_id in by_channel:
            raise BoundedEmpiricalRuntimeError(
                f"duplicate contribution for channel {item.channel_id}"
            )
        by_channel[item.channel_id] = item

    unknown = set(by_channel) - {x.channel_id for x in policy.channels}
    if unknown:
        raise BoundedEmpiricalRuntimeError(
            f"unconfigured evidence channels: {sorted(unknown)}"
        )

    effective: list[EffectiveContribution] = []
    decisions: list[ChannelDecision] = []
    blocking: list[str] = []
    total_widening = Decimal("0")

    for channel in policy.channels:
        item = by_channel.get(channel.channel_id)
        if item is not None and item.evidence_tier is not EvidenceTier.UNAVAILABLE:
            _validate_tier_for_policy(channel, item)
            effective.append(
                EffectiveContribution(
                    channel.channel_id,
                    channel.coefficient,
                    ContributionClass.EMPIRICAL,
                    item.value,
                    item.evidence_tier,
                    item.claim_ceiling,
                    item.source_ref,
                )
            )
            decisions.append(
                ChannelDecision(
                    channel.channel_id,
                    channel.coefficient,
                    "EMPIRICAL_CONTRIBUTION_ACCEPTED",
                    item.evidence_tier,
                    None,
                    Decimal("0"),
                    None,
                )
            )
            continue

        fallback_numeric, decision, is_blocking = _fallback_effect(channel)
        decisions.append(decision)
        total_widening += decision.uncertainty_widening
        if fallback_numeric is not None:
            effective.append(fallback_numeric)
        if is_blocking:
            blocking.append(channel.channel_id)

    if blocking:
        state = DriverRuntimeState.BLOCKED_TERMINAL_REQUIREMENT
        block_reason = (
            "NON_FALLBACKABLE_REQUIRED_CHANNELS_MISSING:"
            + ",".join(sorted(blocking))
        )
    elif effective:
        state = DriverRuntimeState.ADMISSIBLE_WITH_NUMERIC_CONTRIBUTIONS
        block_reason = None
    elif policy.allow_typed_no_numeric_driver:
        state = DriverRuntimeState.ADMISSIBLE_TYPED_NO_NUMERIC_CONTRIBUTION
        block_reason = None
    else:
        state = DriverRuntimeState.BLOCKED_TERMINAL_REQUIREMENT
        block_reason = "NO_NUMERIC_CONTRIBUTION_AND_TYPED_ABSENCE_NOT_PERMITTED"

    empirical = [
        x for x in effective
        if x.contribution_class is ContributionClass.EMPIRICAL
    ]
    priors = [
        x for x in effective
        if x.contribution_class is ContributionClass.MODEL_PRIOR
    ]
    unavailable_count = sum(
        1
        for x in decisions
        if x.decision != "EMPIRICAL_CONTRIBUTION_ACCEPTED"
    )
    policy_hash = semantic_hash({
        "contract_id": CONTRACT_ID,
        "policy": policy,
    })
    core = {
        "contract_id": CONTRACT_ID,
        "driver_id": policy.driver_id,
        "policy_version": policy.policy_version,
        "policy_hash": policy_hash,
        "intended_channel_count": len(policy.channels),
        "empirical_contributing_channel_count": len(empirical),
        "model_prior_channel_count": len(priors),
        "unavailable_channel_count": unavailable_count,
        "intended_coefficient_mass": policy.intended_coefficient_mass,
        "empirical_coefficient_mass": sum(
            (x.coefficient for x in empirical),
            Decimal("0"),
        ),
        "model_prior_coefficient_mass": sum(
            (x.coefficient for x in priors),
            Decimal("0"),
        ),
        "coefficient_reallocated": False,
        "total_uncertainty_widening": total_widening,
        "channel_decisions": tuple(
            sorted(decisions, key=lambda x: x.channel_id)
        ),
    }
    receipt = EmpiricalCoverageReceipt(
        **core,
        receipt_hash=semantic_hash({
            "canonical_profile": CANONICAL_PROFILE,
            **core,
        }),
    )
    return DriverRuntimeEnvelope(
        policy.driver_id,
        state,
        tuple(sorted(effective, key=lambda x: x.channel_id)),
        tuple(sorted(decisions, key=lambda x: x.channel_id)),
        total_widening,
        receipt,
        block_reason,
    )


def assert_no_legacy_missing_zero(
    raw_value: Any,
    *,
    evidence_available: bool,
) -> None:
    """Guard old vector callers that historically used missing-default-zero."""
    if not evidence_available and raw_value is not None:
        try:
            numeric = _decimal(raw_value, "raw_value")
        except BoundedEmpiricalRuntimeError:
            return
        if numeric == 0:
            raise MissingAsZeroError(
                "missing evidence may not be represented by numeric zero"
            )
        raise MissingAsZeroError(
            "missing evidence may not be represented by any numeric value"
        )
