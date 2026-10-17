"""SDTF R4 G1+G6 mechanism-rule authority/currentness binding.

This module is a bounded binding adapter over project-current exact-reference
patterns.  It does not create an authority registry, select "latest" authority,
mint concrete mechanism rules, execute rule bodies, write actor facts, choose
numeric values, or close OBL062.

The contract deliberately keeps constitution currentness separate from rule
currentness and requires future concrete R4 rules to carry an auditable
source/evidence/mechanism/ceiling/authority envelope before they can be treated
as current.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_authority import (
    Pre553AuthorityError,
    require_exact_authority_ref,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    semantic_hash,
)

CONTRACT_ID = "SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING_R1@1.0.0"
MECHANISM_RULE_REF_KIND = "SDTF_R4_MECHANISM_RULE"
MECHANISM_CLASS_COMPOSITION_REF_KIND = "SDTF_R4_MECHANISM_CLASS_COMPOSITION"
RULE_AUTHORITY_BINDING_REF_KIND = "SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING"

CURRENT_ACCEPTED = "CURRENT_ACCEPTED"
CANDIDATE_NOT_CURRENT = "CANDIDATE_NOT_CURRENT"
HISTORICAL_NONCURRENT = "HISTORICAL_NONCURRENT"

_FORBIDDEN_EXACT_SELECTOR_TOKENS = frozenset({
    "LATEST",
    "DEFAULT",
    "FUZZY",
    "NEAREST",
    "SEMVER",
    "SEMVER_FALLBACK",
    "*",
})
_FORBIDDEN_VERSION_RANGE_CHARS = frozenset("*<>^~")


class R4MechanismRuleAuthorityBindingError(ValueError):
    """The exact R4 rule-authority/currentness envelope failed closed."""


class RuleNotCurrentError(R4MechanismRuleAuthorityBindingError):
    """A caller attempted current execution/admission without current rule proof."""


class MechanismClass(str, Enum):
    P1_MATERIAL_ACCESS_DEPENDENCY = "P1 MATERIAL_ACCESS_DEPENDENCY"
    P2_DIRECTED_AUTHORITY_OBLIGATION_SANCTION = "P2 DIRECTED_AUTHORITY_OBLIGATION_SANCTION"
    P3_ORGANIZED_ACTIVITY_TIME = "P3 ORGANIZED_ACTIVITY_TIME"
    P4_INSTITUTIONAL_GATE_TREATMENT = "P4 INSTITUTIONAL_GATE_TREATMENT"
    P5_COUNTERPART_CHANNEL_RELATION = "P5 COUNTERPART_CHANNEL_RELATION"


_MECHANISM_CLASS_ORDER = {
    item: index for index, item in enumerate(MechanismClass, start=1)
}


class AuthorityRole(str, Enum):
    RULE_OWNER = "RULE_OWNER"
    MEASUREMENT = "MEASUREMENT"
    ESTIMAND = "ESTIMAND"
    IDENTIFICATION = "IDENTIFICATION"
    CAUSAL_USE = "CAUSAL_USE"
    CALIBRATION = "CALIBRATION"


class AuthorityDisposition(str, Enum):
    BOUND = "BOUND"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class RuleValueMode(str, Enum):
    NONNUMERIC = "NONNUMERIC"
    NUMERIC = "NUMERIC"


class RuleCurrentness(str, Enum):
    CANDIDATE_NOT_CURRENT = CANDIDATE_NOT_CURRENT
    CURRENT_ACCEPTED = CURRENT_ACCEPTED
    HISTORICAL_NONCURRENT = HISTORICAL_NONCURRENT


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise R4MechanismRuleAuthorityBindingError(f"{name} must be non-empty text")
    return value.strip()


def _reject_mutable_selector(value: str, name: str, *, version: bool = False) -> str:
    text = _text(value, name)
    upper = text.upper()
    if upper in _FORBIDDEN_EXACT_SELECTOR_TOKENS:
        raise R4MechanismRuleAuthorityBindingError(
            f"{name} must be an exact immutable identity, not a mutable selector"
        )
    if upper.startswith(("LATEST:", "DEFAULT:", "FUZZY:", "NEAREST:", "SEMVER:")):
        raise R4MechanismRuleAuthorityBindingError(
            f"{name} may not use mutable/fuzzy selector syntax"
        )
    if version and any(ch in text for ch in _FORBIDDEN_VERSION_RANGE_CHARS):
        raise R4MechanismRuleAuthorityBindingError(
            f"{name} may not use a version range or wildcard"
        )
    return text


def _exact_ref(value: Any, name: str) -> ExactRef:
    if not isinstance(value, ExactRef):
        raise R4MechanismRuleAuthorityBindingError(f"{name} must be an exact ExactRef")
    return value


def _exact_ref_tuple(
    values: Iterable[ExactRef],
    name: str,
    *,
    require_nonempty: bool,
) -> tuple[ExactRef, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise R4MechanismRuleAuthorityBindingError(f"{name} must be an iterable of ExactRef")
    refs = tuple(values)
    if require_nonempty and not refs:
        raise R4MechanismRuleAuthorityBindingError(f"{name} must not be empty")
    if any(not isinstance(ref, ExactRef) for ref in refs):
        raise R4MechanismRuleAuthorityBindingError(f"{name} must contain only ExactRef")
    keys = [ref.key for ref in refs]
    if len(keys) != len(set(keys)):
        raise R4MechanismRuleAuthorityBindingError(f"{name} contains duplicate exact refs")
    return tuple(sorted(refs, key=lambda ref: ref.key))


def _exact_authority_ref(value: Any, name: str) -> AuthorityRef:
    if not isinstance(value, AuthorityRef):
        raise R4MechanismRuleAuthorityBindingError(f"{name} must be an exact AuthorityRef")
    try:
        return require_exact_authority_ref(value)
    except Pre553AuthorityError as exc:
        raise R4MechanismRuleAuthorityBindingError(str(exc)) from exc


@dataclass(frozen=True, slots=True)
class MechanismRuleIdentity:
    """Exact external identity of one future concrete rule body.

    The rule body is deliberately not stored here.  The content hash binds it.
    """

    rule_id: str
    rule_version: str
    rule_content_hash: str

    def __post_init__(self) -> None:
        rule_id = _reject_mutable_selector(self.rule_id, "rule_id")
        rule_version = _reject_mutable_selector(
            self.rule_version, "rule_version", version=True
        )
        object.__setattr__(self, "rule_id", rule_id)
        object.__setattr__(self, "rule_version", rule_version)
        try:
            ref = ExactRef(
                MECHANISM_RULE_REF_KIND,
                f"{rule_id}@{rule_version}",
                self.rule_content_hash,
            )
        except ValueError as exc:
            raise R4MechanismRuleAuthorityBindingError(
                "rule_content_hash must be an exact lowercase sha256"
            ) from exc
        object.__setattr__(self, "rule_content_hash", ref.content_hash)

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            MECHANISM_RULE_REF_KIND,
            f"{self.rule_id}@{self.rule_version}",
            self.rule_content_hash,
        )


@dataclass(frozen=True, slots=True)
class AuthorityCeilingBinding:
    """Bind one authority role without creating or resolving that authority.

    BOUND requires one exact AuthorityRef plus explicit current-selection
    evidence.  NOT_APPLICABLE is an explicit typed disposition and requires an
    exact scope/N/A basis ref while carrying no authority tuple.
    """

    role: AuthorityRole
    disposition: AuthorityDisposition
    scope_or_na_ref: ExactRef
    authority_ref: AuthorityRef | None = None
    current_selection_evidence_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        try:
            role = self.role if isinstance(self.role, AuthorityRole) else AuthorityRole(self.role)
            disposition = (
                self.disposition
                if isinstance(self.disposition, AuthorityDisposition)
                else AuthorityDisposition(self.disposition)
            )
        except (TypeError, ValueError) as exc:
            raise R4MechanismRuleAuthorityBindingError(
                "unknown authority role or disposition"
            ) from exc
        object.__setattr__(self, "role", role)
        object.__setattr__(self, "disposition", disposition)
        object.__setattr__(
            self, "scope_or_na_ref", _exact_ref(self.scope_or_na_ref, "scope_or_na_ref")
        )

        refs = _exact_ref_tuple(
            self.current_selection_evidence_refs,
            "current_selection_evidence_refs",
            require_nonempty=False,
        )
        object.__setattr__(self, "current_selection_evidence_refs", refs)

        if disposition is AuthorityDisposition.BOUND:
            if self.authority_ref is None:
                raise R4MechanismRuleAuthorityBindingError(
                    f"{role.value} BOUND requires exact authority_ref"
                )
            object.__setattr__(
                self,
                "authority_ref",
                _exact_authority_ref(self.authority_ref, f"{role.value}.authority_ref"),
            )
            if not refs:
                raise R4MechanismRuleAuthorityBindingError(
                    f"{role.value} BOUND requires explicit authority current-selection evidence"
                )
        else:
            if self.authority_ref is not None:
                raise R4MechanismRuleAuthorityBindingError(
                    f"{role.value} NOT_APPLICABLE may not carry authority_ref"
                )
            if refs:
                raise R4MechanismRuleAuthorityBindingError(
                    f"{role.value} NOT_APPLICABLE may not carry current-selection evidence"
                )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "role": self.role.value,
            "disposition": self.disposition.value,
            "scope_or_na_ref": self.scope_or_na_ref.as_dict(),
            "authority_ref": (
                None if self.authority_ref is None else self.authority_ref.as_dict()
            ),
            "current_selection_evidence_refs": [
                ref.as_dict() for ref in self.current_selection_evidence_refs
            ],
        }


@dataclass(frozen=True, slots=True)
class RuleTraceBinding:
    """Exact source -> mechanism -> rule-shape/ceiling trace for one rule."""

    source_refs: tuple[ExactRef, ...]
    claim_refs: tuple[ExactRef, ...]
    evidence_status_ref: ExactRef
    normalized_mechanism_ref: ExactRef
    permitted_rule_shape_ref: ExactRef
    required_objective_inputs_bindings_ref: ExactRef
    qualification_realization_proof_contract_ref: ExactRef
    temporal_currentness_contract_ref: ExactRef
    portability_ceiling_ref: ExactRef
    currentness_ceiling_ref: ExactRef
    historical_institutional_validity_ref: ExactRef
    negative_ceiling_ref: ExactRef
    v3_stop_boundary_ref: ExactRef

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_refs",
            _exact_ref_tuple(self.source_refs, "source_refs", require_nonempty=True),
        )
        object.__setattr__(
            self,
            "claim_refs",
            _exact_ref_tuple(self.claim_refs, "claim_refs", require_nonempty=True),
        )
        for name in (
            "evidence_status_ref",
            "normalized_mechanism_ref",
            "permitted_rule_shape_ref",
            "required_objective_inputs_bindings_ref",
            "qualification_realization_proof_contract_ref",
            "temporal_currentness_contract_ref",
            "portability_ceiling_ref",
            "currentness_ceiling_ref",
            "historical_institutional_validity_ref",
            "negative_ceiling_ref",
            "v3_stop_boundary_ref",
        ):
            object.__setattr__(self, name, _exact_ref(getattr(self, name), name))

    def as_material(self) -> Mapping[str, Any]:
        return {
            "source_refs": [ref.as_dict() for ref in self.source_refs],
            "claim_refs": [ref.as_dict() for ref in self.claim_refs],
            "evidence_status_ref": self.evidence_status_ref.as_dict(),
            "normalized_mechanism_ref": self.normalized_mechanism_ref.as_dict(),
            "permitted_rule_shape_ref": self.permitted_rule_shape_ref.as_dict(),
            "required_objective_inputs_bindings_ref":
                self.required_objective_inputs_bindings_ref.as_dict(),
            "qualification_realization_proof_contract_ref":
                self.qualification_realization_proof_contract_ref.as_dict(),
            "temporal_currentness_contract_ref":
                self.temporal_currentness_contract_ref.as_dict(),
            "portability_ceiling_ref": self.portability_ceiling_ref.as_dict(),
            "currentness_ceiling_ref": self.currentness_ceiling_ref.as_dict(),
            "historical_institutional_validity_ref":
                self.historical_institutional_validity_ref.as_dict(),
            "negative_ceiling_ref": self.negative_ceiling_ref.as_dict(),
            "v3_stop_boundary_ref": self.v3_stop_boundary_ref.as_dict(),
        }


def _mechanism_classes(
    values: Iterable[MechanismClass | str],
) -> tuple[MechanismClass, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise R4MechanismRuleAuthorityBindingError(
            "mechanism_classes must be an iterable of P1-P5 classes"
        )
    raw = tuple(values)
    if not raw:
        raise R4MechanismRuleAuthorityBindingError(
            "at least one P1-P5 mechanism class is required"
        )
    try:
        classes = tuple(
            value if isinstance(value, MechanismClass) else MechanismClass(value)
            for value in raw
        )
    except (TypeError, ValueError) as exc:
        raise R4MechanismRuleAuthorityBindingError(
            "mechanism class must be one of exact P1-P5; no P6 or other class is permitted"
        ) from exc
    if len(classes) != len(set(classes)):
        raise R4MechanismRuleAuthorityBindingError(
            "mechanism class composition may not contain duplicates"
        )
    return tuple(sorted(classes, key=lambda item: _MECHANISM_CLASS_ORDER[item]))


@dataclass(frozen=True, slots=True)
class MechanismRuleAuthorityBinding:
    """Complete bounded G1+G6 binding envelope for one future R4 rule."""

    rule_identity: MechanismRuleIdentity
    mechanism_classes: tuple[MechanismClass, ...]
    constitution_current_selection_ref: ExactRef
    trace: RuleTraceBinding
    rule_owner: AuthorityCeilingBinding
    measurement_authority: AuthorityCeilingBinding
    estimand_authority: AuthorityCeilingBinding
    identification_authority: AuthorityCeilingBinding
    causal_use_authority: AuthorityCeilingBinding
    calibration_authority: AuthorityCeilingBinding
    value_mode: RuleValueMode
    rule_currentness: RuleCurrentness
    rule_current_selection_evidence_refs: tuple[ExactRef, ...] = ()
    rule_noncurrent_disposition_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.rule_identity, MechanismRuleIdentity):
            raise R4MechanismRuleAuthorityBindingError(
                "rule_identity must be MechanismRuleIdentity"
            )
        object.__setattr__(
            self, "mechanism_classes", _mechanism_classes(self.mechanism_classes)
        )
        object.__setattr__(
            self,
            "constitution_current_selection_ref",
            _exact_ref(
                self.constitution_current_selection_ref,
                "constitution_current_selection_ref",
            ),
        )
        if not isinstance(self.trace, RuleTraceBinding):
            raise R4MechanismRuleAuthorityBindingError(
                "trace must be exact RuleTraceBinding"
            )

        expected_roles = (
            ("rule_owner", self.rule_owner, AuthorityRole.RULE_OWNER),
            ("measurement_authority", self.measurement_authority, AuthorityRole.MEASUREMENT),
            ("estimand_authority", self.estimand_authority, AuthorityRole.ESTIMAND),
            (
                "identification_authority",
                self.identification_authority,
                AuthorityRole.IDENTIFICATION,
            ),
            ("causal_use_authority", self.causal_use_authority, AuthorityRole.CAUSAL_USE),
            ("calibration_authority", self.calibration_authority, AuthorityRole.CALIBRATION),
        )
        for name, binding, role in expected_roles:
            if not isinstance(binding, AuthorityCeilingBinding):
                raise R4MechanismRuleAuthorityBindingError(
                    f"{name} must be AuthorityCeilingBinding"
                )
            if binding.role is not role:
                raise R4MechanismRuleAuthorityBindingError(
                    f"{name} role mismatch: expected {role.value}"
                )

        if self.rule_owner.disposition is not AuthorityDisposition.BOUND:
            raise R4MechanismRuleAuthorityBindingError(
                "exact competent rule owner authority is mandatory"
            )
        if self.causal_use_authority.disposition is not AuthorityDisposition.BOUND:
            raise R4MechanismRuleAuthorityBindingError(
                "exact competent causal-use authority is mandatory"
            )

        try:
            value_mode = (
                self.value_mode
                if isinstance(self.value_mode, RuleValueMode)
                else RuleValueMode(self.value_mode)
            )
            currentness = (
                self.rule_currentness
                if isinstance(self.rule_currentness, RuleCurrentness)
                else RuleCurrentness(self.rule_currentness)
            )
        except (TypeError, ValueError) as exc:
            raise R4MechanismRuleAuthorityBindingError(
                "unknown rule value mode or currentness"
            ) from exc
        object.__setattr__(self, "value_mode", value_mode)
        object.__setattr__(self, "rule_currentness", currentness)

        if value_mode is RuleValueMode.NUMERIC:
            if self.calibration_authority.disposition is not AuthorityDisposition.BOUND:
                raise R4MechanismRuleAuthorityBindingError(
                    "numeric rule shape requires exact current calibration authority"
                )
        else:
            if (
                self.calibration_authority.disposition
                is not AuthorityDisposition.NOT_APPLICABLE
            ):
                raise R4MechanismRuleAuthorityBindingError(
                    "nonnumeric rule shape requires explicit calibration NOT_APPLICABLE"
                )

        current_refs = _exact_ref_tuple(
            self.rule_current_selection_evidence_refs,
            "rule_current_selection_evidence_refs",
            require_nonempty=False,
        )
        noncurrent_refs = _exact_ref_tuple(
            self.rule_noncurrent_disposition_refs,
            "rule_noncurrent_disposition_refs",
            require_nonempty=False,
        )
        object.__setattr__(
            self, "rule_current_selection_evidence_refs", current_refs
        )
        object.__setattr__(
            self, "rule_noncurrent_disposition_refs", noncurrent_refs
        )

        if currentness is RuleCurrentness.CURRENT_ACCEPTED:
            if not current_refs:
                raise R4MechanismRuleAuthorityBindingError(
                    "CURRENT_ACCEPTED rule requires explicit rule current-selection evidence"
                )
            if noncurrent_refs:
                raise R4MechanismRuleAuthorityBindingError(
                    "CURRENT_ACCEPTED rule may not carry noncurrent disposition refs"
                )
        elif currentness is RuleCurrentness.CANDIDATE_NOT_CURRENT:
            if current_refs or noncurrent_refs:
                raise R4MechanismRuleAuthorityBindingError(
                    "CANDIDATE_NOT_CURRENT carries no current or historical disposition proof"
                )
        else:
            if not current_refs or not noncurrent_refs:
                raise R4MechanismRuleAuthorityBindingError(
                    "HISTORICAL_NONCURRENT requires prior current-selection and noncurrent disposition refs"
                )

    @property
    def mechanism_class_composition_ref(self) -> ExactRef:
        values = [item.value for item in self.mechanism_classes]
        material = {
            "contract_id": CONTRACT_ID,
            "mechanism_classes": values,
        }
        return ExactRef(
            MECHANISM_CLASS_COMPOSITION_REF_KIND,
            "+".join(values),
            semantic_hash(material),
        )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": CONTRACT_ID,
            "rule_ref": self.rule_identity.ref.as_dict(),
            "rule_id": self.rule_identity.rule_id,
            "rule_version": self.rule_identity.rule_version,
            "rule_content_hash": self.rule_identity.rule_content_hash,
            "mechanism_classes": [item.value for item in self.mechanism_classes],
            "mechanism_class_composition_ref":
                self.mechanism_class_composition_ref.as_dict(),
            "constitution_current_selection_ref":
                self.constitution_current_selection_ref.as_dict(),
            "trace": self.trace.as_material(),
            "rule_owner": self.rule_owner.as_material(),
            "measurement_authority": self.measurement_authority.as_material(),
            "estimand_authority": self.estimand_authority.as_material(),
            "identification_authority": self.identification_authority.as_material(),
            "causal_use_authority": self.causal_use_authority.as_material(),
            "calibration_authority": self.calibration_authority.as_material(),
            "value_mode": self.value_mode.value,
            "rule_currentness": self.rule_currentness.value,
            "rule_current_selection_evidence_refs": [
                ref.as_dict() for ref in self.rule_current_selection_evidence_refs
            ],
            "rule_noncurrent_disposition_refs": [
                ref.as_dict() for ref in self.rule_noncurrent_disposition_refs
            ],
            "authority_law": {
                "constitution_current_does_not_imply_rule_current": True,
                "source_citation_does_not_imply_causal_use": True,
                "numeric_requires_calibration_authority": True,
                "nonnumeric_requires_explicit_calibration_na": True,
                "no_latest_default_fuzzy_authority_selection": True,
            },
        }

    @property
    def binding_hash(self) -> str:
        return semantic_hash(self.as_material())

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            RULE_AUTHORITY_BINDING_REF_KIND,
            self.rule_identity.ref.object_id,
            self.binding_hash,
        )


def require_current_rule_admission(
    binding: MechanismRuleAuthorityBinding,
) -> MechanismRuleAuthorityBinding:
    """Require a fully bound current rule without inferring from constitution currentness."""
    if not isinstance(binding, MechanismRuleAuthorityBinding):
        raise R4MechanismRuleAuthorityBindingError(
            "MechanismRuleAuthorityBinding required"
        )
    if binding.rule_currentness is not RuleCurrentness.CURRENT_ACCEPTED:
        raise RuleNotCurrentError(
            "constitution currentness does not make this mechanism rule current"
        )
    if not binding.rule_current_selection_evidence_refs:
        # Defensive redundancy: constructor already enforces this.
        raise RuleNotCurrentError("exact rule current-selection evidence is required")
    return binding


__all__ = [
    "CONTRACT_ID",
    "MECHANISM_RULE_REF_KIND",
    "MECHANISM_CLASS_COMPOSITION_REF_KIND",
    "RULE_AUTHORITY_BINDING_REF_KIND",
    "CURRENT_ACCEPTED",
    "CANDIDATE_NOT_CURRENT",
    "HISTORICAL_NONCURRENT",
    "R4MechanismRuleAuthorityBindingError",
    "RuleNotCurrentError",
    "MechanismClass",
    "AuthorityRole",
    "AuthorityDisposition",
    "RuleValueMode",
    "RuleCurrentness",
    "MechanismRuleIdentity",
    "AuthorityCeilingBinding",
    "RuleTraceBinding",
    "MechanismRuleAuthorityBinding",
    "require_current_rule_admission",
]
