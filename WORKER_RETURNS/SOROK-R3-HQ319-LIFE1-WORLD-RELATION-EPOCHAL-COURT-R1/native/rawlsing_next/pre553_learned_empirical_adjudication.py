"""Generic M1 learned-empirical adjudication runtime.

Jurisdiction:
    EXACT_I05_DISCOVERY_EVIDENCE
    + EXPLICIT_EXACT_FAMILY_RULE_BINDING
    -> LearnedEmpiricalDisposition@1.0.0

This module is deliberately source-free and non-substantive.  It verifies exact
PRE553 evidence/authority/replay closure, resolves one exact family validator
binding, dispatches only by immutable identity, conserves upstream typed states,
and emits a deterministic adjudication disposition plus determinant/explanation
receipt.

It does NOT decode sources, execute I03/I05, choose substantive validation
criteria, publish/current-select learned products, admit structure, create Field
Forge relations, grant consumer permission, or affect actor/V3 state.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, Sequence

from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    require_exact_authority_ref,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    CanonicalSemanticObject,
    DiscoveryAuthority,
    DiscoveryResultReceipt,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)


M1_ADJUDICATION_CONTRACT_ID = "PYAT_M1_LEARNED_EMPIRICAL_ADJUDICATION@1.0.0"
M1_DEFAULT_SEMANTIC_CEILING = (
    "LEARNED_EMPIRICAL_DISPOSITION_ONLY__NO_PRODUCT_RELEASE__NO_CURRENTNESS__"
    "NO_STRUCTURAL_ADMISSION__NO_CAUSAL_PROMOTION__"
    "NO_POPULATION_GENERALIZATION_BEYOND_BOUND_SCOPE__NO_PERSON_OR_V3_STATE"
)

M1_OUTCOMES = frozenset({
    "RULE_SATISFIED",
    "RULE_NOT_SATISFIED",
    "ABSTAINED",
    "BLOCKED",
    "UNRESOLVED",
    "INTEGRITY_FAILURE",
})
_SELECTION_PURPOSES = frozenset({"CURRENT_GOVERNED_USE", "EXACT_PINNED_REPLAY"})
_PREREQUISITE_STATES = frozenset({
    "SATISFIED",
    "BLOCKED",
    "UNKNOWN",
    "UNRESOLVED",
    "NONCOMPARABLE",
    "NOT_APPLICABLE",
    "DENIED",
    "MISSING",
    "CONFLICTING",
    "OUT_OF_SCOPE",
    "INTEGRITY_FAILURE",
})
_REQUIRED_INPUT_FAMILIES = (
    "DiscoveryResultReceipt@1.0.0",
    "DiscoveryAuthority@1.0.0",
    "EmpiricalFact@1.0.0",
    "EmpiricalQuerySpec@1.0.0",
    "EmpiricalPredicate@1.0.0",
)
_FORBIDDEN_SELECTOR_TOKENS = frozenset({
    "LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER", "SEMVER_FALLBACK", "*",
})
_FALSE_EFFECTS = MappingProxyType({
    "product_release_effect": False,
    "current_selection_effect": False,
    "structural_admission_effect": False,
    "consumer_permission_effect": False,
    "causal_truth_effect": False,
    "actor_v3_effect": False,
})


class M1AdjudicationError(Pre553IntegrityError):
    """Base failure for exact generic M1 adjudication mechanics."""


class M1IntegrityError(M1AdjudicationError):
    """Exact identity/ref/replay/semantic-projection closure failed."""


class M1BlockedError(M1AdjudicationError):
    """Required rule authority or prerequisite is unavailable/denied/out of scope."""


class M1UnresolvedError(M1AdjudicationError):
    """A governed prerequisite remains unresolved and cannot be defaulted."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise M1IntegrityError(f"{name} must be a non-empty exact string")
    return value.strip()


def _selector_safe(value: str, name: str) -> str:
    value = _text(value, name)
    upper = value.upper()
    if upper in _FORBIDDEN_SELECTOR_TOKENS or upper.startswith(
        ("LATEST:", "DEFAULT:", "FUZZY:", "NEAREST:", "SEMVER:")
    ):
        raise M1BlockedError(f"{name} may not use latest/default/fuzzy selection")
    return value


def _freeze(value: Any) -> Any:
    material = _material(value)
    if isinstance(material, Mapping):
        return MappingProxyType({k: _freeze(material[k]) for k in sorted(material)})
    if isinstance(material, list):
        return tuple(_freeze(item) for item in material)
    return material


def _detach(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: _detach(value[k]) for k in value}
    if isinstance(value, tuple):
        return [_detach(item) for item in value]
    return value


def _material(value: Any) -> Any:
    if isinstance(value, _M1ExactObject):
        return value.ref.as_dict()
    if isinstance(value, TypedAbsence):
        return value.as_dict()
    if isinstance(value, (ExactRef, AuthorityRef, CanonicalSemanticObject)):
        return canonicalize(value)
    if isinstance(value, Mapping):
        if any(not isinstance(k, str) for k in value):
            raise M1IntegrityError("semantic mapping keys must be strings")
        return {k: _material(value[k]) for k in sorted(value)}
    if isinstance(value, (set, frozenset)):
        rows = [_material(item) for item in value]
        return sorted(rows, key=canonical_json)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_material(item) for item in value]
    try:
        return canonicalize(value)
    except Pre553IntegrityError as exc:
        raise M1IntegrityError(str(exc)) from exc


def _ref(value: ExactRef | Mapping[str, Any], name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Pre553IntegrityError as exc:
        raise M1IntegrityError(str(exc)) from exc


def _authority_ref(value: AuthorityRef | Mapping[str, Any], name: str) -> AuthorityRef:
    try:
        return require_exact_authority_ref(value)
    except (Pre553IntegrityError, Pre553AuthorityError) as exc:
        raise M1BlockedError(str(exc)) from exc


def _canonical_refs(
    values: Iterable[ExactRef | Mapping[str, Any]], name: str
) -> tuple[ExactRef, ...]:
    refs = tuple(_ref(value, name) for value in values)
    return tuple(sorted(set(refs), key=lambda item: item.key))


def _canonical_authority_refs(
    values: Iterable[AuthorityRef | Mapping[str, Any]], name: str
) -> tuple[AuthorityRef, ...]:
    refs = tuple(_authority_ref(value, name) for value in values)
    return tuple(sorted(set(refs), key=lambda item: item.key))


def _canonical_strings(values: Iterable[str], name: str) -> tuple[str, ...]:
    rows = tuple(_text(value, name) for value in values)
    return tuple(sorted(set(rows)))


def _verify_public_identity(
    obj: CanonicalSemanticObject,
    expected_type: type[CanonicalSemanticObject],
    label: str,
) -> None:
    if not isinstance(obj, expected_type):
        raise M1IntegrityError(f"{label} contains wrong exact public object family")
    if semantic_hash(obj.semantic_projection()) != obj.content_hash:
        raise M1IntegrityError(f"{label} contains identity-drifted public object")


def _canonical_public_objects(
    objects: Iterable[CanonicalSemanticObject],
    expected_type: type[CanonicalSemanticObject],
    label: str,
) -> tuple[CanonicalSemanticObject, ...]:
    by_ref: dict[str, CanonicalSemanticObject] = {}
    for obj in objects:
        _verify_public_identity(obj, expected_type, label)
        prior = by_ref.get(obj.ref.key)
        if prior is not None and canonical_json(prior.as_dict()) != canonical_json(obj.as_dict()):
            raise M1IntegrityError(f"{label} has conflicting exact preimages")
        by_ref[obj.ref.key] = obj
    return tuple(by_ref[key] for key in sorted(by_ref))


def _canonical_authority_snapshots(
    snapshots: Iterable[AuthoritySnapshot],
) -> tuple[AuthoritySnapshot, ...]:
    by_ref: dict[str, AuthoritySnapshot] = {}
    for snapshot in snapshots:
        _verify_public_identity(snapshot, AuthoritySnapshot, "authority_snapshots")
        key = snapshot.authority_ref.key
        prior = by_ref.get(key)
        if prior is not None and canonical_json(prior.as_dict()) != canonical_json(snapshot.as_dict()):
            raise M1IntegrityError("conflicting exact authority snapshot preimages")
        by_ref[key] = snapshot
    return tuple(by_ref[key] for key in sorted(by_ref))


def _typed_absence(state: str, detail: str) -> TypedAbsence:
    return TypedAbsence(state, detail)


class _M1ExactObject:
    SCHEMA_ID = ""
    SCHEMA_VERSION = "1.0.0"

    def _semantic_fields(self) -> Mapping[str, Any]:
        raise NotImplementedError

    @property
    def family(self) -> str:
        return f"{self.SCHEMA_ID}@{self.SCHEMA_VERSION}"

    def semantic_projection(self) -> Mapping[str, Any]:
        return {
            "schema_id": self.SCHEMA_ID,
            "schema_version": self.SCHEMA_VERSION,
            "semantic_fields": _material(self._semantic_fields()),
        }

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.semantic_projection())

    @property
    def object_id(self) -> str:
        return (
            f"urn:rawlsing:pre553:m1:{self.SCHEMA_ID}:sha256:{self.content_hash}"
        )

    @property
    def ref(self) -> ExactRef:
        return ExactRef(self.family, self.object_id, self.content_hash)

    def as_dict(self) -> Mapping[str, Any]:
        return {
            **self.semantic_projection(),
            "object_id": self.object_id,
            "content_hash": self.content_hash,
        }


@dataclass(frozen=True)
class M1PrerequisiteChannel(_M1ExactObject):
    SCHEMA_ID = "M1PrerequisiteChannel"

    channel_id: str
    channel_kind: str
    state: str
    authority_refs: tuple[AuthorityRef, ...] = ()
    dependency_refs: tuple[ExactRef, ...] = ()
    relation_kinds: tuple[str, ...] = ()
    detail: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "channel_id", _selector_safe(self.channel_id, "channel_id"))
        object.__setattr__(self, "channel_kind", _text(self.channel_kind, "channel_kind"))
        if self.state not in _PREREQUISITE_STATES:
            raise M1IntegrityError(f"unknown prerequisite channel state {self.state!r}")
        object.__setattr__(
            self,
            "authority_refs",
            _canonical_authority_refs(self.authority_refs, "prerequisite authority ref"),
        )
        object.__setattr__(
            self,
            "dependency_refs",
            _canonical_refs(self.dependency_refs, "prerequisite dependency ref"),
        )
        object.__setattr__(
            self,
            "relation_kinds",
            _canonical_strings(self.relation_kinds, "relation kind"),
        )
        if not isinstance(self.detail, Mapping):
            raise M1IntegrityError("prerequisite detail must be exact mapping")
        object.__setattr__(self, "detail", _freeze(self.detail))

    def _semantic_fields(self) -> Mapping[str, Any]:
        return {
            "channel_id": self.channel_id,
            "channel_kind": self.channel_kind,
            "state": self.state,
            "authority_refs": self.authority_refs,
            "dependency_refs": self.dependency_refs,
            "relation_kinds": self.relation_kinds,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class M1FamilyRuleBinding(_M1ExactObject):
    SCHEMA_ID = "M1FamilyRuleBinding"

    claim_family_id: str
    claim_rule_id: str
    validator_authority_ref: AuthorityRef
    selection_purpose: str
    current_selection_authority_ref: AuthorityRef | None
    applicability_scope: Mapping[str, Any]
    allowed_input_object_families_and_states: Mapping[str, Any]
    required_prerequisite_channels: tuple[str, ...]
    required_source_relation_kinds: tuple[str, ...]
    required_measure_weight_estimand_authorities: tuple[AuthorityRef, ...]
    required_coverage_strength: Mapping[str, Any]
    uncertainty_policy_ref: ExactRef
    output_semantic_contract: Mapping[str, Any]
    semantic_ceiling: str
    validator_algorithm_identity_if_required: str
    validator_parameters_ref: ExactRef
    replay_contract_ref: ExactRef
    authority_closure_refs: tuple[AuthorityRef, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "claim_family_id", _selector_safe(self.claim_family_id, "claim_family_id")
        )
        object.__setattr__(
            self, "claim_rule_id", _selector_safe(self.claim_rule_id, "claim_rule_id")
        )
        object.__setattr__(
            self,
            "validator_authority_ref",
            _authority_ref(self.validator_authority_ref, "validator_authority_ref"),
        )
        if self.selection_purpose not in _SELECTION_PURPOSES:
            raise M1IntegrityError("unknown M1 rule-selection purpose")
        if self.selection_purpose == "CURRENT_GOVERNED_USE":
            if self.current_selection_authority_ref is None:
                raise M1IntegrityError(
                    "CURRENT_GOVERNED_USE requires exact current-selection authority"
                )
            current = _authority_ref(
                self.current_selection_authority_ref,
                "current_selection_authority_ref",
            )
            object.__setattr__(self, "current_selection_authority_ref", current)
        else:
            if self.current_selection_authority_ref is not None:
                raise M1IntegrityError(
                    "EXACT_PINNED_REPLAY may not smuggle a currentness claim"
                )
        for name, value in (
            ("applicability_scope", self.applicability_scope),
            (
                "allowed_input_object_families_and_states",
                self.allowed_input_object_families_and_states,
            ),
            ("required_coverage_strength", self.required_coverage_strength),
            ("output_semantic_contract", self.output_semantic_contract),
        ):
            if not isinstance(value, Mapping):
                raise M1IntegrityError(f"{name} must be exact mapping")
        allowed = {
            str(key): tuple(sorted(set(_text(x, f"{key} state") for x in value)))
            for key, value in self.allowed_input_object_families_and_states.items()
        }
        missing = sorted(set(_REQUIRED_INPUT_FAMILIES) - set(allowed))
        if missing:
            raise M1IntegrityError(
                f"rule binding omits required input-family state contract: {missing!r}"
            )
        object.__setattr__(self, "applicability_scope", _freeze(self.applicability_scope))
        object.__setattr__(
            self,
            "allowed_input_object_families_and_states",
            _freeze(allowed),
        )
        object.__setattr__(
            self,
            "required_prerequisite_channels",
            _canonical_strings(
                self.required_prerequisite_channels, "required prerequisite channel"
            ),
        )
        object.__setattr__(
            self,
            "required_source_relation_kinds",
            _canonical_strings(
                self.required_source_relation_kinds, "required source relation kind"
            ),
        )
        object.__setattr__(
            self,
            "required_measure_weight_estimand_authorities",
            _canonical_authority_refs(
                self.required_measure_weight_estimand_authorities,
                "required measure/weight/estimand authority",
            ),
        )
        coverage = dict(_material(self.required_coverage_strength))
        required_coverage_keys = {
            "allowed_coverage_claims",
            "allowed_receipt_states",
            "allowed_coverage_states",
        }
        if set(coverage) != required_coverage_keys:
            raise M1IntegrityError(
                "required_coverage_strength must explicitly declare claims, receipt states, and coverage states"
            )
        for key in required_coverage_keys:
            values = coverage[key]
            if not isinstance(values, Sequence) or isinstance(values, (str, bytes)) or not values:
                raise M1IntegrityError(f"{key} must be a nonempty exact sequence")
            coverage[key] = sorted(set(_text(item, key) for item in values))
        object.__setattr__(self, "required_coverage_strength", _freeze(coverage))
        output_contract = dict(_material(self.output_semantic_contract))
        mode = output_contract.get("truth_bearing_claim_emission")
        if mode not in {"PROHIBITED", "EXPLICITLY_AUTHORIZED"}:
            raise M1IntegrityError(
                "output semantic contract must explicitly govern truth-bearing claim emission"
            )
        object.__setattr__(self, "output_semantic_contract", _freeze(output_contract))
        object.__setattr__(
            self, "semantic_ceiling", _text(self.semantic_ceiling, "semantic_ceiling")
        )
        object.__setattr__(
            self,
            "validator_algorithm_identity_if_required",
            _selector_safe(
                self.validator_algorithm_identity_if_required,
                "validator_algorithm_identity",
            ),
        )
        object.__setattr__(
            self,
            "uncertainty_policy_ref",
            _ref(self.uncertainty_policy_ref, "uncertainty_policy_ref"),
        )
        object.__setattr__(
            self,
            "validator_parameters_ref",
            _ref(self.validator_parameters_ref, "validator_parameters_ref"),
        )
        object.__setattr__(
            self,
            "replay_contract_ref",
            _ref(self.replay_contract_ref, "replay_contract_ref"),
        )
        closure = _canonical_authority_refs(
            self.authority_closure_refs, "rule-binding authority closure"
        )
        required_refs = {self.validator_authority_ref}
        if self.current_selection_authority_ref is not None:
            required_refs.add(self.current_selection_authority_ref)
        if not required_refs.issubset(set(closure)):
            raise M1IntegrityError(
                "rule binding authority closure omits validator/current-selection authority"
            )
        object.__setattr__(self, "authority_closure_refs", closure)

    @property
    def validator_dispatch_key(self) -> tuple[str, str, str, str, str]:
        ref = self.validator_authority_ref
        return (
            self.claim_family_id,
            self.claim_rule_id,
            ref.authority_id,
            ref.authority_version,
            ref.authority_content_hash,
        )

    @property
    def validator_contract_fingerprint(self) -> str:
        return semantic_hash({
            "claim_family_id": self.claim_family_id,
            "claim_rule_id": self.claim_rule_id,
            "validator_authority_ref": self.validator_authority_ref,
            "selection_purpose": self.selection_purpose,
            "current_selection_authority_ref": self.current_selection_authority_ref,
            "applicability_scope": self.applicability_scope,
            "authority_closure_refs": self.authority_closure_refs,
            "allowed_input_object_families_and_states": self.allowed_input_object_families_and_states,
            "required_prerequisite_channels": self.required_prerequisite_channels,
            "required_source_relation_kinds": self.required_source_relation_kinds,
            "required_measure_weight_estimand_authorities": self.required_measure_weight_estimand_authorities,
            "required_coverage_strength": self.required_coverage_strength,
            "uncertainty_policy_ref": self.uncertainty_policy_ref,
            "output_semantic_contract": self.output_semantic_contract,
            "semantic_ceiling": self.semantic_ceiling,
            "validator_algorithm_identity": self.validator_algorithm_identity_if_required,
            "validator_parameters_ref": self.validator_parameters_ref,
            "replay_contract_ref": self.replay_contract_ref,
        })

    def _semantic_fields(self) -> Mapping[str, Any]:
        return {
            "claim_family_id": self.claim_family_id,
            "claim_rule_id": self.claim_rule_id,
            "validator_authority_ref": self.validator_authority_ref,
            "selection_purpose": self.selection_purpose,
            "current_selection_authority_ref": (
                self.current_selection_authority_ref
                if self.current_selection_authority_ref is not None
                else _typed_absence("NOT_APPLICABLE", "exact pinned replay")
            ),
            "applicability_scope": self.applicability_scope,
            "allowed_input_object_families_and_states": self.allowed_input_object_families_and_states,
            "required_prerequisite_channels": self.required_prerequisite_channels,
            "required_source_relation_kinds": self.required_source_relation_kinds,
            "required_measure_weight_estimand_authorities": self.required_measure_weight_estimand_authorities,
            "required_coverage_strength": self.required_coverage_strength,
            "uncertainty_policy_ref": self.uncertainty_policy_ref,
            "output_semantic_contract": self.output_semantic_contract,
            "semantic_ceiling": self.semantic_ceiling,
            "validator_algorithm_identity_if_required": self.validator_algorithm_identity_if_required,
            "validator_parameters_ref": self.validator_parameters_ref,
            "replay_contract_ref": self.replay_contract_ref,
            "authority_closure_refs": self.authority_closure_refs,
            "validator_contract_fingerprint": self.validator_contract_fingerprint,
        }


@dataclass(frozen=True)
class M1AdjudicationInputBundle(_M1ExactObject):
    SCHEMA_ID = "M1AdjudicationInputBundle"

    requested_claim_family_id: str
    requested_claim_rule_id: str
    discovery_receipts: tuple[DiscoveryResultReceipt, ...]
    discovery_authorities: tuple[DiscoveryAuthority, ...]
    empirical_facts: tuple[EmpiricalFact, ...]
    empirical_queries: tuple[EmpiricalQuerySpec, ...]
    empirical_predicates: tuple[EmpiricalPredicate, ...]
    authority_snapshots: tuple[AuthoritySnapshot, ...]
    evaluated_frontier_refs: tuple[ExactRef, ...]
    discovery_replay_refs: tuple[ExactRef, ...]
    requested_scope: Mapping[str, Any]
    prerequisite_channels: tuple[M1PrerequisiteChannel, ...] = ()
    additional_dependency_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "requested_claim_family_id",
            _selector_safe(self.requested_claim_family_id, "requested_claim_family_id"),
        )
        object.__setattr__(
            self,
            "requested_claim_rule_id",
            _selector_safe(self.requested_claim_rule_id, "requested_claim_rule_id"),
        )
        object.__setattr__(
            self,
            "discovery_receipts",
            _canonical_public_objects(
                self.discovery_receipts, DiscoveryResultReceipt, "discovery_receipts"
            ),
        )
        object.__setattr__(
            self,
            "discovery_authorities",
            _canonical_public_objects(
                self.discovery_authorities, DiscoveryAuthority, "discovery_authorities"
            ),
        )
        object.__setattr__(
            self,
            "empirical_facts",
            _canonical_public_objects(self.empirical_facts, EmpiricalFact, "empirical_facts"),
        )
        object.__setattr__(
            self,
            "empirical_queries",
            _canonical_public_objects(
                self.empirical_queries, EmpiricalQuerySpec, "empirical_queries"
            ),
        )
        object.__setattr__(
            self,
            "empirical_predicates",
            _canonical_public_objects(
                self.empirical_predicates, EmpiricalPredicate, "empirical_predicates"
            ),
        )
        object.__setattr__(
            self,
            "authority_snapshots",
            _canonical_authority_snapshots(self.authority_snapshots),
        )
        object.__setattr__(
            self,
            "evaluated_frontier_refs",
            _canonical_refs(self.evaluated_frontier_refs, "evaluated_frontier_ref"),
        )
        object.__setattr__(
            self,
            "discovery_replay_refs",
            _canonical_refs(self.discovery_replay_refs, "discovery_replay_ref"),
        )
        if not self.discovery_receipts:
            raise M1IntegrityError("M1 input bundle requires at least one discovery receipt")
        if not isinstance(self.requested_scope, Mapping):
            raise M1IntegrityError("requested_scope must be exact mapping")
        object.__setattr__(self, "requested_scope", _freeze(self.requested_scope))
        channels: dict[str, M1PrerequisiteChannel] = {}
        for channel in self.prerequisite_channels:
            if not isinstance(channel, M1PrerequisiteChannel):
                raise M1IntegrityError("prerequisite_channels contains wrong type")
            if channel.channel_id in channels and channels[channel.channel_id] != channel:
                raise M1IntegrityError("duplicate prerequisite channel id with conflicting body")
            channels[channel.channel_id] = channel
        object.__setattr__(
            self,
            "prerequisite_channels",
            tuple(channels[key] for key in sorted(channels)),
        )
        object.__setattr__(
            self,
            "additional_dependency_refs",
            _canonical_refs(
                self.additional_dependency_refs, "additional_dependency_ref"
            ),
        )

    def _semantic_fields(self) -> Mapping[str, Any]:
        return {
            "requested_claim_family_id": self.requested_claim_family_id,
            "requested_claim_rule_id": self.requested_claim_rule_id,
            "discovery_receipts": [obj.as_dict() for obj in self.discovery_receipts],
            "discovery_authorities": [obj.as_dict() for obj in self.discovery_authorities],
            "empirical_facts": [obj.as_dict() for obj in self.empirical_facts],
            "empirical_queries": [obj.as_dict() for obj in self.empirical_queries],
            "empirical_predicates": [obj.as_dict() for obj in self.empirical_predicates],
            "authority_snapshots": [obj.as_dict() for obj in self.authority_snapshots],
            "evaluated_frontier_refs": self.evaluated_frontier_refs,
            "discovery_replay_refs": self.discovery_replay_refs,
            "requested_scope": self.requested_scope,
            "prerequisite_channels": [channel.as_dict() for channel in self.prerequisite_channels],
            "additional_dependency_refs": self.additional_dependency_refs,
        }


@dataclass(frozen=True)
class FamilyValidationResult(_M1ExactObject):
    SCHEMA_ID = "FamilyValidationResult"

    claim_family_id: str
    claim_rule_id: str
    family_rule_binding_ref: ExactRef
    validator_authority_ref: AuthorityRef
    validator_algorithm_identity: str
    adjudication_outcome: str
    reason_code: str
    relation_proposition_identity_ref: ExactRef | None
    semantic_claim_identity_ref: ExactRef | None
    semantic_assertion_polarity_or_state: str
    semantic_ceiling: str
    determinant_material: Mapping[str, Any]
    explanation_material: Mapping[str, Any]
    effects: Mapping[str, bool] = field(default_factory=lambda: dict(_FALSE_EFFECTS))

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "claim_family_id", _selector_safe(self.claim_family_id, "claim_family_id")
        )
        object.__setattr__(
            self, "claim_rule_id", _selector_safe(self.claim_rule_id, "claim_rule_id")
        )
        object.__setattr__(
            self,
            "family_rule_binding_ref",
            _ref(self.family_rule_binding_ref, "family_rule_binding_ref"),
        )
        object.__setattr__(
            self,
            "validator_authority_ref",
            _authority_ref(self.validator_authority_ref, "validator_authority_ref"),
        )
        object.__setattr__(
            self,
            "validator_algorithm_identity",
            _selector_safe(
                self.validator_algorithm_identity, "validator_algorithm_identity"
            ),
        )
        if self.adjudication_outcome not in M1_OUTCOMES:
            raise M1IntegrityError("unknown family validation outcome")
        object.__setattr__(self, "reason_code", _text(self.reason_code, "reason_code"))
        if self.relation_proposition_identity_ref is not None:
            object.__setattr__(
                self,
                "relation_proposition_identity_ref",
                _ref(
                    self.relation_proposition_identity_ref,
                    "relation_proposition_identity_ref",
                ),
            )
        if self.semantic_claim_identity_ref is not None:
            object.__setattr__(
                self,
                "semantic_claim_identity_ref",
                _ref(self.semantic_claim_identity_ref, "semantic_claim_identity_ref"),
            )
        polarity = _text(
            self.semantic_assertion_polarity_or_state,
            "semantic_assertion_polarity_or_state",
        )
        if self.semantic_claim_identity_ref is None and polarity != "NONE":
            raise M1IntegrityError(
                "semantic assertion polarity requires exact semantic claim identity"
            )
        if self.semantic_claim_identity_ref is not None:
            if self.relation_proposition_identity_ref is None:
                raise M1IntegrityError(
                    "truth-bearing semantic claim requires relation proposition identity"
                )
            if polarity == "NONE":
                raise M1IntegrityError(
                    "truth-bearing semantic claim requires explicit assertion state"
                )
        object.__setattr__(self, "semantic_assertion_polarity_or_state", polarity)
        object.__setattr__(
            self, "semantic_ceiling", _text(self.semantic_ceiling, "semantic_ceiling")
        )
        if not isinstance(self.determinant_material, Mapping):
            raise M1IntegrityError("determinant_material must be exact mapping")
        if not isinstance(self.explanation_material, Mapping):
            raise M1IntegrityError("explanation_material must be exact mapping")
        object.__setattr__(self, "determinant_material", _freeze(self.determinant_material))
        object.__setattr__(self, "explanation_material", _freeze(self.explanation_material))
        effects = dict(self.effects)
        if set(effects) != set(_FALSE_EFFECTS) or any(
            not isinstance(value, bool) for value in effects.values()
        ):
            raise M1IntegrityError("validator effects must use exact M1 side-effect vocabulary")
        object.__setattr__(self, "effects", MappingProxyType(effects))

    def _semantic_fields(self) -> Mapping[str, Any]:
        return {
            "claim_family_id": self.claim_family_id,
            "claim_rule_id": self.claim_rule_id,
            "family_rule_binding_ref": self.family_rule_binding_ref,
            "validator_authority_ref": self.validator_authority_ref,
            "validator_algorithm_identity": self.validator_algorithm_identity,
            "adjudication_outcome": self.adjudication_outcome,
            "reason_code": self.reason_code,
            "relation_proposition_identity_ref": (
                self.relation_proposition_identity_ref
                if self.relation_proposition_identity_ref is not None
                else _typed_absence("NOT_APPLICABLE", "validator emitted no proposition")
            ),
            "semantic_claim_identity_ref": (
                self.semantic_claim_identity_ref
                if self.semantic_claim_identity_ref is not None
                else _typed_absence("NOT_AUTHORIZED", "validator emitted no truth-bearing claim")
            ),
            "semantic_assertion_polarity_or_state": self.semantic_assertion_polarity_or_state,
            "semantic_ceiling": self.semantic_ceiling,
            "determinant_material": self.determinant_material,
            "explanation_material": self.explanation_material,
            "effects": self.effects,
        }


@dataclass(frozen=True)
class M1DeterminantExplanationReceipt(_M1ExactObject):
    SCHEMA_ID = "M1DeterminantExplanationReceipt"

    input_bundle_ref: ExactRef
    family_rule_binding_ref_or_typed_absence: ExactRef | TypedAbsence
    validator_registration_identity: str
    family_validation_result_ref: ExactRef
    determinant_manifest: Mapping[str, Any]
    explanation: Mapping[str, Any]
    replay_material: Mapping[str, Any]
    semantic_ceiling: str
    effects: Mapping[str, bool] = field(default_factory=lambda: dict(_FALSE_EFFECTS))

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "input_bundle_ref", _ref(self.input_bundle_ref, "input_bundle_ref")
        )
        if not isinstance(self.family_rule_binding_ref_or_typed_absence, TypedAbsence):
            object.__setattr__(
                self,
                "family_rule_binding_ref_or_typed_absence",
                _ref(
                    self.family_rule_binding_ref_or_typed_absence,
                    "family_rule_binding_ref",
                ),
            )
        object.__setattr__(
            self,
            "validator_registration_identity",
            _text(
                self.validator_registration_identity,
                "validator_registration_identity",
            ),
        )
        object.__setattr__(
            self,
            "family_validation_result_ref",
            _ref(
                self.family_validation_result_ref, "family_validation_result_ref"
            ),
        )
        for name, value in (
            ("determinant_manifest", self.determinant_manifest),
            ("explanation", self.explanation),
            ("replay_material", self.replay_material),
        ):
            if not isinstance(value, Mapping):
                raise M1IntegrityError(f"{name} must be exact mapping")
            object.__setattr__(self, name, _freeze(value))
        object.__setattr__(
            self, "semantic_ceiling", _text(self.semantic_ceiling, "semantic_ceiling")
        )
        effects = dict(self.effects)
        if effects != dict(_FALSE_EFFECTS):
            raise M1IntegrityError("M1 determinant receipt cannot carry downstream effects")
        object.__setattr__(self, "effects", MappingProxyType(effects))

    @property
    def determinant_manifest_ref(self) -> ExactRef:
        digest = semantic_hash({
            "schema": "M1_DETERMINANT_MANIFEST@1.0.0",
            "material": self.determinant_manifest,
        })
        return ExactRef(
            "M1DeterminantManifest@1.0.0",
            f"urn:rawlsing:pre553:m1:determinants:sha256:{digest}",
            digest,
        )

    @property
    def explanation_ref(self) -> ExactRef:
        digest = semantic_hash({
            "schema": "M1_EXPLANATION@1.0.0",
            "material": self.explanation,
        })
        return ExactRef(
            "M1Explanation@1.0.0",
            f"urn:rawlsing:pre553:m1:explanation:sha256:{digest}",
            digest,
        )

    @property
    def replay_ref(self) -> ExactRef:
        digest = semantic_hash({
            "schema": "M1_ADJUDICATION_REPLAY@1.0.0",
            "material": self.replay_material,
        })
        return ExactRef(
            "M1AdjudicationReplay@1.0.0",
            f"urn:rawlsing:pre553:m1:replay:sha256:{digest}",
            digest,
        )

    def _semantic_fields(self) -> Mapping[str, Any]:
        return {
            "input_bundle_ref": self.input_bundle_ref,
            "family_rule_binding_ref_or_typed_absence": self.family_rule_binding_ref_or_typed_absence,
            "validator_registration_identity": self.validator_registration_identity,
            "family_validation_result_ref": self.family_validation_result_ref,
            "determinant_manifest": self.determinant_manifest,
            "determinant_manifest_ref": self.determinant_manifest_ref,
            "explanation": self.explanation,
            "explanation_ref": self.explanation_ref,
            "replay_material": self.replay_material,
            "replay_ref": self.replay_ref,
            "semantic_ceiling": self.semantic_ceiling,
            "effects": self.effects,
        }


@dataclass(frozen=True)
class LearnedEmpiricalDisposition(_M1ExactObject):
    SCHEMA_ID = "LearnedEmpiricalDisposition"

    disposition_class: str
    adjudication_outcome: str
    rule_outcome: str
    reason_code: str
    claim_family_id: str
    claim_rule_id: str
    relation_proposition_identity_ref: ExactRef | TypedAbsence
    semantic_claim_identity_ref: ExactRef | TypedAbsence
    semantic_assertion_polarity_or_state: str
    family_rule_binding_ref: ExactRef | TypedAbsence
    validator_authority_ref: AuthorityRef | TypedAbsence
    rule_selection_authority_ref: AuthorityRef | TypedAbsence
    discovery_result_receipt_refs: tuple[ExactRef, ...]
    discovery_authority_refs: tuple[ExactRef, ...]
    empirical_fact_refs: tuple[ExactRef, ...]
    validation_fact_refs: tuple[ExactRef, ...]
    empirical_query_spec_refs: tuple[ExactRef, ...]
    empirical_predicate_refs: tuple[ExactRef, ...]
    source_universe_refs: tuple[ExactRef, ...]
    risk_set_refs: tuple[ExactRef, ...]
    topology_scope_material: tuple[Any, ...]
    measure_basis_refs: tuple[ExactRef, ...]
    weight_design_estimand_refs: tuple[AuthorityRef, ...]
    comparability_authority_refs: tuple[AuthorityRef, ...]
    composition_authority_refs: tuple[AuthorityRef, ...]
    coverage_claims: tuple[str, ...]
    coverage_states: tuple[Mapping[str, Any], ...]
    conserved_empirical_states: tuple[Mapping[str, Any], ...]
    conserved_authority_states: tuple[Mapping[str, Any], ...]
    support_uncertainty_state: tuple[Any, ...]
    support_uncertainty_refs: tuple[ExactRef, ...]
    blocking_negative_authority_refs: tuple[AuthorityRef, ...]
    required_prerequisite_channel_states: Mapping[str, str]
    semantic_ceiling: str
    authority_closure_refs: tuple[AuthorityRef, ...]
    dependency_refs: tuple[ExactRef, ...]
    validator_algorithm_identity: str
    validator_parameters_ref: ExactRef | TypedAbsence
    determinant_manifest_ref: ExactRef
    explanation_ref: ExactRef
    replay_ref: ExactRef
    determinant_explanation_receipt_ref: ExactRef
    effects: Mapping[str, bool]
    determinant_explanation_receipt: M1DeterminantExplanationReceipt = field(
        compare=False, repr=False
    )

    def __post_init__(self) -> None:
        if self.adjudication_outcome not in M1_OUTCOMES:
            raise M1IntegrityError("unknown disposition adjudication_outcome")
        expected = _outcome_axes(self.adjudication_outcome)
        if (self.disposition_class, self.rule_outcome) != expected:
            raise M1IntegrityError("disposition outcome axes are internally inconsistent")
        if dict(self.effects) != dict(_FALSE_EFFECTS):
            raise M1IntegrityError("M1 disposition cannot carry downstream effects")
        if self.determinant_explanation_receipt.ref != self.determinant_explanation_receipt_ref:
            raise M1IntegrityError("determinant/explanation receipt ref mismatch")
        if self.determinant_explanation_receipt.determinant_manifest_ref != self.determinant_manifest_ref:
            raise M1IntegrityError("determinant manifest ref mismatch")
        if self.determinant_explanation_receipt.explanation_ref != self.explanation_ref:
            raise M1IntegrityError("explanation ref mismatch")
        if self.determinant_explanation_receipt.replay_ref != self.replay_ref:
            raise M1IntegrityError("replay ref mismatch")

    @property
    def status_token(self) -> str:
        return f"{self.adjudication_outcome}__{self.reason_code}"

    def _semantic_fields(self) -> Mapping[str, Any]:
        return {
            "jurisdiction_contract_id": M1_ADJUDICATION_CONTRACT_ID,
            "disposition_class": self.disposition_class,
            "adjudication_outcome": self.adjudication_outcome,
            "rule_outcome": self.rule_outcome,
            "reason_code": self.reason_code,
            "claim_family_id": self.claim_family_id,
            "claim_rule_id": self.claim_rule_id,
            "relation_proposition_identity_ref": self.relation_proposition_identity_ref,
            "semantic_claim_identity_ref": self.semantic_claim_identity_ref,
            "semantic_assertion_polarity_or_state": self.semantic_assertion_polarity_or_state,
            "family_rule_binding_ref": self.family_rule_binding_ref,
            "validator_authority_ref": self.validator_authority_ref,
            "rule_selection_authority_ref": self.rule_selection_authority_ref,
            "discovery_result_receipt_refs": self.discovery_result_receipt_refs,
            "discovery_authority_refs": self.discovery_authority_refs,
            "empirical_fact_refs": self.empirical_fact_refs,
            "validation_fact_refs": self.validation_fact_refs,
            "empirical_query_spec_refs": self.empirical_query_spec_refs,
            "empirical_predicate_refs": self.empirical_predicate_refs,
            "source_universe_refs": self.source_universe_refs,
            "risk_set_refs": self.risk_set_refs,
            "topology_scope_material": self.topology_scope_material,
            "measure_basis_refs": self.measure_basis_refs,
            "weight_design_estimand_refs": self.weight_design_estimand_refs,
            "comparability_authority_refs": self.comparability_authority_refs,
            "composition_authority_refs": self.composition_authority_refs,
            "coverage_claims": self.coverage_claims,
            "coverage_states": self.coverage_states,
            "conserved_empirical_states": self.conserved_empirical_states,
            "conserved_authority_states": self.conserved_authority_states,
            "support_uncertainty_state": self.support_uncertainty_state,
            "support_uncertainty_refs": self.support_uncertainty_refs,
            "blocking_negative_authority_refs": self.blocking_negative_authority_refs,
            "required_prerequisite_channel_states": self.required_prerequisite_channel_states,
            "semantic_ceiling": self.semantic_ceiling,
            "authority_closure_refs": self.authority_closure_refs,
            "dependency_refs": self.dependency_refs,
            "validator_algorithm_identity": self.validator_algorithm_identity,
            "validator_parameters_ref": self.validator_parameters_ref,
            "determinant_manifest_ref": self.determinant_manifest_ref,
            "explanation_ref": self.explanation_ref,
            "replay_ref": self.replay_ref,
            "determinant_explanation_receipt_ref": self.determinant_explanation_receipt_ref,
            "effects": self.effects,
        }


@dataclass(frozen=True)
class FamilyValidatorRegistration:
    claim_family_id: str
    claim_rule_id: str
    validator_authority_ref: AuthorityRef
    validator_algorithm_identity: str
    validator_parameters_ref: ExactRef
    validator_contract_fingerprint: str
    validator: Callable[["M1ValidatorContext"], FamilyValidationResult]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "claim_family_id", _selector_safe(self.claim_family_id, "claim_family_id")
        )
        object.__setattr__(
            self, "claim_rule_id", _selector_safe(self.claim_rule_id, "claim_rule_id")
        )
        object.__setattr__(
            self,
            "validator_authority_ref",
            _authority_ref(self.validator_authority_ref, "validator_authority_ref"),
        )
        object.__setattr__(
            self,
            "validator_algorithm_identity",
            _selector_safe(
                self.validator_algorithm_identity, "validator_algorithm_identity"
            ),
        )
        object.__setattr__(
            self,
            "validator_parameters_ref",
            _ref(self.validator_parameters_ref, "validator_parameters_ref"),
        )
        if not isinstance(self.validator_contract_fingerprint, str) or len(
            self.validator_contract_fingerprint
        ) != 64:
            raise M1IntegrityError("validator contract fingerprint must be sha256")
        if not callable(self.validator):
            raise M1IntegrityError("family validator registration requires callable")

    @classmethod
    def from_binding(
        cls,
        binding: M1FamilyRuleBinding,
        validator: Callable[["M1ValidatorContext"], FamilyValidationResult],
    ) -> "FamilyValidatorRegistration":
        return cls(
            claim_family_id=binding.claim_family_id,
            claim_rule_id=binding.claim_rule_id,
            validator_authority_ref=binding.validator_authority_ref,
            validator_algorithm_identity=binding.validator_algorithm_identity_if_required,
            validator_parameters_ref=binding.validator_parameters_ref,
            validator_contract_fingerprint=binding.validator_contract_fingerprint,
            validator=validator,
        )

    @property
    def dispatch_key(self) -> tuple[str, str, str, str, str]:
        ref = self.validator_authority_ref
        return (
            self.claim_family_id,
            self.claim_rule_id,
            ref.authority_id,
            ref.authority_version,
            ref.authority_content_hash,
        )

    @property
    def registration_identity(self) -> str:
        return semantic_hash({
            "schema": "M1_FAMILY_VALIDATOR_REGISTRATION@1.0.0",
            "claim_family_id": self.claim_family_id,
            "claim_rule_id": self.claim_rule_id,
            "validator_authority_ref": self.validator_authority_ref,
            "validator_algorithm_identity": self.validator_algorithm_identity,
            "validator_parameters_ref": self.validator_parameters_ref,
            "validator_contract_fingerprint": self.validator_contract_fingerprint,
        })


class M1ValidatorRegistry:
    """Exact immutable validator registry; no aliases, latest, defaults or fallback."""

    def __init__(self, registrations: Iterable[FamilyValidatorRegistration] = ()) -> None:
        by_key: dict[tuple[str, str, str, str, str], FamilyValidatorRegistration] = {}
        for registration in registrations:
            if not isinstance(registration, FamilyValidatorRegistration):
                raise M1IntegrityError("validator registry accepts exact registrations only")
            prior = by_key.get(registration.dispatch_key)
            if prior is not None and prior.registration_identity != registration.registration_identity:
                raise M1IntegrityError("conflicting validator registrations share exact dispatch key")
            by_key[registration.dispatch_key] = registration
        self._by_key = MappingProxyType(by_key)

    def resolve_exact(self, binding: M1FamilyRuleBinding) -> FamilyValidatorRegistration:
        registration = self._by_key.get(binding.validator_dispatch_key)
        if registration is None:
            raise M1BlockedError(
                "exact validator registration unavailable; no latest/default/fuzzy fallback"
            )
        if registration.validator_contract_fingerprint != binding.validator_contract_fingerprint:
            raise M1BlockedError(
                "validator registration does not match exact family-rule contract"
            )
        if registration.validator_algorithm_identity != binding.validator_algorithm_identity_if_required:
            raise M1BlockedError("validator algorithm identity does not match exact binding")
        if registration.validator_parameters_ref != binding.validator_parameters_ref:
            raise M1BlockedError("validator parameters do not match exact binding")
        return registration


@dataclass(frozen=True)
class M1ValidatorContext:
    input_bundle: M1AdjudicationInputBundle
    family_rule_binding: M1FamilyRuleBinding
    evidence_context: Mapping[str, Any]


@dataclass(frozen=True)
class _BundleVerification:
    authority_registry: AuthorityRegistry
    discovery_receipts: tuple[DiscoveryResultReceipt, ...]
    discovery_authorities: tuple[DiscoveryAuthority, ...]
    empirical_facts: tuple[EmpiricalFact, ...]
    empirical_queries: tuple[EmpiricalQuerySpec, ...]
    empirical_predicates: tuple[EmpiricalPredicate, ...]
    source_universe_refs: tuple[ExactRef, ...]
    risk_set_refs: tuple[ExactRef, ...]
    measure_basis_refs: tuple[ExactRef, ...]
    topology_scope_material: tuple[Any, ...]
    coverage_claims: tuple[str, ...]
    coverage_states: tuple[Mapping[str, Any], ...]
    empirical_states: tuple[Mapping[str, Any], ...]
    authority_states: tuple[Mapping[str, Any], ...]
    support_uncertainty_state: tuple[Any, ...]
    support_uncertainty_refs: tuple[ExactRef, ...]


def build_m1_adjudication_input_bundle(
    *,
    requested_claim_family_id: str,
    requested_claim_rule_id: str,
    selected_discovery_receipts: Iterable[DiscoveryResultReceipt],
    discovery_authority_catalog: Iterable[DiscoveryAuthority],
    empirical_fact_catalog: Iterable[EmpiricalFact],
    empirical_query_catalog: Iterable[EmpiricalQuerySpec],
    empirical_predicate_catalog: Iterable[EmpiricalPredicate],
    authority_snapshots: Iterable[AuthoritySnapshot],
    requested_scope: Mapping[str, Any],
    prerequisite_channels: Iterable[M1PrerequisiteChannel] = (),
    additional_dependency_refs: Iterable[ExactRef] = (),
) -> M1AdjudicationInputBundle:
    """Build one exact M1 bundle from a broad exact graph without importing M01.

    Selection is purely ref-driven from the caller-selected I05 receipts.  This
    helper does not execute I03/I05 or infer claim meaning.
    """
    receipts = _canonical_public_objects(
        selected_discovery_receipts,
        DiscoveryResultReceipt,
        "selected_discovery_receipts",
    )
    if not receipts:
        raise M1IntegrityError("one or more selected discovery receipts are required")

    discovery_by = {
        obj.ref.key: obj
        for obj in _canonical_public_objects(
            discovery_authority_catalog,
            DiscoveryAuthority,
            "discovery_authority_catalog",
        )
    }
    fact_by = {
        obj.ref.key: obj
        for obj in _canonical_public_objects(
            empirical_fact_catalog, EmpiricalFact, "empirical_fact_catalog"
        )
    }
    query_by = {
        obj.ref.key: obj
        for obj in _canonical_public_objects(
            empirical_query_catalog, EmpiricalQuerySpec, "empirical_query_catalog"
        )
    }
    predicate_by = {
        obj.ref.key: obj
        for obj in _canonical_public_objects(
            empirical_predicate_catalog,
            EmpiricalPredicate,
            "empirical_predicate_catalog",
        )
    }

    discoveries: dict[str, DiscoveryAuthority] = {}
    facts: dict[str, EmpiricalFact] = {}
    queries: dict[str, EmpiricalQuerySpec] = {}
    predicates: dict[str, EmpiricalPredicate] = {}

    for receipt in receipts:
        discovery_ref = _ref(receipt.discovery_authority_ref, "receipt discovery authority")
        discovery = discovery_by.get(discovery_ref.key)
        if discovery is None:
            raise M1IntegrityError("selected receipt discovery authority preimage unavailable")
        discoveries[discovery.ref.key] = discovery

        for raw_ref in (*receipt.empirical_fact_refs, *receipt.validation_fact_refs):
            fact_ref = _ref(raw_ref, "receipt empirical fact ref")
            fact = fact_by.get(fact_ref.key)
            if fact is None:
                raise M1IntegrityError("selected receipt empirical fact preimage unavailable")
            facts[fact.ref.key] = fact

        winning = _ref(receipt.winning_predicate_ref, "winning predicate ref")
        predicate = predicate_by.get(winning.key)
        if predicate is None:
            raise M1IntegrityError("selected receipt winning predicate preimage unavailable")
        predicates[predicate.ref.key] = predicate

        identity = receipt.candidate_identity
        roles = identity.get("query_roles") if isinstance(identity, Mapping) else None
        if not isinstance(roles, Sequence) or isinstance(roles, (str, bytes)):
            raise M1IntegrityError("selected receipt query-role closure malformed")
        for role in roles:
            if not isinstance(role, Mapping):
                raise M1IntegrityError("selected receipt query role malformed")
            predicate_ref = _ref(role.get("predicate_ref"), "role predicate_ref")
            query_ref = _ref(role.get("query_ref"), "role query_ref")
            if predicate_ref.key not in predicate_by or query_ref.key not in query_by:
                raise M1IntegrityError("selected receipt role preimage unavailable")
            predicates[predicate_ref.key] = predicate_by[predicate_ref.key]
            queries[query_ref.key] = query_by[query_ref.key]

    for fact in tuple(facts.values()):
        query_ref = _ref(fact.empirical_query_spec_ref, "fact query ref")
        predicate_ref = _ref(fact.condition_predicate_ref, "fact predicate ref")
        if query_ref.key not in query_by or predicate_ref.key not in predicate_by:
            raise M1IntegrityError("fact constitutive query/predicate preimage unavailable")
        queries[query_ref.key] = query_by[query_ref.key]
        predicates[predicate_ref.key] = predicate_by[predicate_ref.key]

    return M1AdjudicationInputBundle(
        requested_claim_family_id=requested_claim_family_id,
        requested_claim_rule_id=requested_claim_rule_id,
        discovery_receipts=receipts,
        discovery_authorities=tuple(discoveries.values()),
        empirical_facts=tuple(facts.values()),
        empirical_queries=tuple(queries.values()),
        empirical_predicates=tuple(predicates.values()),
        authority_snapshots=tuple(authority_snapshots),
        evaluated_frontier_refs=tuple(
            _ref(receipt.evaluated_frontier_ref, "receipt frontier ref")
            for receipt in receipts
        ),
        discovery_replay_refs=tuple(
            _ref(receipt.replay_ref, "receipt replay ref") for receipt in receipts
        ),
        requested_scope=requested_scope,
        prerequisite_channels=tuple(prerequisite_channels),
        additional_dependency_refs=tuple(additional_dependency_refs),
    )


def _verify_bundle(bundle: M1AdjudicationInputBundle) -> _BundleVerification:
    if not isinstance(bundle, M1AdjudicationInputBundle):
        raise M1IntegrityError("exact M1AdjudicationInputBundle@1.0.0 required")

    try:
        authority_registry = AuthorityRegistry(bundle.authority_snapshots)
    except (Pre553AuthorityError, Pre553IntegrityError) as exc:
        raise M1BlockedError(f"authority registry cannot close: {exc}") from exc

    for obj in (
        *bundle.discovery_authorities,
        *bundle.empirical_facts,
        *bundle.empirical_queries,
        *bundle.empirical_predicates,
        *bundle.discovery_receipts,
    ):
        try:
            validate_object_authority_closure(obj, authority_registry)
        except Pre553AuthorityError as exc:
            raise M1BlockedError(f"missing authority closure for {obj.ref.key}: {exc}") from exc

    discovery_by = {obj.ref.key: obj for obj in bundle.discovery_authorities}
    fact_by = {obj.ref.key: obj for obj in bundle.empirical_facts}
    query_by = {obj.ref.key: obj for obj in bundle.empirical_queries}
    predicate_by = {obj.ref.key: obj for obj in bundle.empirical_predicates}

    observed_frontiers: list[ExactRef] = []
    observed_replays: list[ExactRef] = []
    referenced_fact_keys: set[str] = set()
    referenced_query_keys: set[str] = set()
    referenced_predicate_keys: set[str] = set()

    for receipt in bundle.discovery_receipts:
        discovery_ref = _ref(receipt.discovery_authority_ref, "receipt discovery authority")
        discovery = discovery_by.get(discovery_ref.key)
        if discovery is None:
            raise M1IntegrityError("receipt discovery authority ref substitution detected")
        observed_frontiers.append(
            _ref(receipt.evaluated_frontier_ref, "receipt evaluated frontier")
        )
        observed_replays.append(_ref(receipt.replay_ref, "receipt replay ref"))

        for raw_ref in (*receipt.empirical_fact_refs, *receipt.validation_fact_refs):
            fact_ref = _ref(raw_ref, "receipt fact ref")
            if fact_ref.key not in fact_by:
                raise M1IntegrityError("receipt empirical/validation fact ref substitution detected")
            referenced_fact_keys.add(fact_ref.key)

        winning_ref = _ref(receipt.winning_predicate_ref, "winning predicate ref")
        if winning_ref.key not in predicate_by:
            raise M1IntegrityError("winning predicate ref substitution detected")
        referenced_predicate_keys.add(winning_ref.key)

        identity = receipt.candidate_identity
        roles = identity.get("query_roles") if isinstance(identity, Mapping) else None
        if not isinstance(roles, Sequence) or isinstance(roles, (str, bytes)):
            raise M1IntegrityError("receipt candidate query-role closure malformed")
        for role in roles:
            if not isinstance(role, Mapping):
                raise M1IntegrityError("receipt candidate query role malformed")
            predicate_ref = _ref(role.get("predicate_ref"), "candidate role predicate")
            query_ref = _ref(role.get("query_ref"), "candidate role query")
            predicate = predicate_by.get(predicate_ref.key)
            query = query_by.get(query_ref.key)
            if predicate is None or query is None:
                raise M1IntegrityError("receipt query/predicate role substitution detected")
            if _ref(query.condition_predicate_ref, "query condition predicate") != predicate_ref:
                raise M1IntegrityError("receipt role query/predicate exact binding mismatch")
            referenced_predicate_keys.add(predicate_ref.key)
            referenced_query_keys.add(query_ref.key)

        required_dependencies = {
            discovery_ref.key,
            _ref(receipt.evaluated_frontier_ref, "receipt frontier").key,
            winning_ref.key,
            *(_ref(ref, "receipt fact dependency").key for ref in receipt.empirical_fact_refs),
        }
        actual_dependencies = {
            _ref(ref, "receipt dependency_ref").key for ref in receipt.dependency_refs
        }
        if not required_dependencies.issubset(actual_dependencies):
            raise M1IntegrityError("receipt dependency closure omits constitutive exact refs")

        grammar_ref = _ref(discovery.candidate_grammar_ref, "candidate grammar ref")
        if grammar_ref.key not in actual_dependencies:
            raise M1IntegrityError("receipt dependency closure omits exact candidate grammar")

    if _canonical_refs(observed_frontiers, "observed frontier") != bundle.evaluated_frontier_refs:
        raise M1IntegrityError("evaluated-frontier declaration/root substitution detected")
    if _canonical_refs(observed_replays, "observed replay") != bundle.discovery_replay_refs:
        raise M1IntegrityError("discovery replay/root substitution detected")

    for fact in bundle.empirical_facts:
        query_ref = _ref(fact.empirical_query_spec_ref, "fact query ref")
        predicate_ref = _ref(fact.condition_predicate_ref, "fact predicate ref")
        query = query_by.get(query_ref.key)
        predicate = predicate_by.get(predicate_ref.key)
        if query is None or predicate is None:
            raise M1IntegrityError("fact query/predicate preimage substitution detected")
        if _ref(query.condition_predicate_ref, "query condition predicate") != predicate_ref:
            raise M1IntegrityError("fact/query/predicate constitutive closure mismatch")
        referenced_query_keys.add(query_ref.key)
        referenced_predicate_keys.add(predicate_ref.key)

    if not referenced_fact_keys.issubset(fact_by):
        raise M1IntegrityError("fact closure cannot be satisfied")
    if not referenced_query_keys.issubset(query_by):
        raise M1IntegrityError("query closure cannot be satisfied")
    if not referenced_predicate_keys.issubset(predicate_by):
        raise M1IntegrityError("predicate closure cannot be satisfied")

    source_refs: list[ExactRef] = []
    risk_refs: list[ExactRef] = []
    measure_refs: list[ExactRef] = []
    topology_material: list[Any] = []
    for fact in bundle.empirical_facts:
        source_refs.extend(
            _ref(ref, "fact source universe ref") for ref in fact.empirical_universe_refs
        )
        risk_refs.append(_ref(fact.risk_set_ref, "fact risk set ref"))
        measure_refs.append(_ref(fact.measure_basis_ref, "fact measure basis ref"))
        topology_material.append(_material(fact.target_topology))
    for query in bundle.empirical_queries:
        source_refs.extend(
            _ref(ref, "query source universe ref") for ref in query.empirical_universe_refs
        )
        risk_refs.append(_ref(query.risk_set_ref, "query risk set ref"))
        measure_refs.append(_ref(query.measure_basis_ref, "query measure basis ref"))
        topology_material.append(_material(query.target_arity_and_topology))

    topology_by = {canonical_json(item): item for item in topology_material}
    topology_tuple = tuple(topology_by[key] for key in sorted(topology_by))

    coverage_claims = tuple(sorted({
        _text(authority.coverage_claim, "coverage claim")
        for authority in bundle.discovery_authorities
    }))
    coverage_states = tuple(sorted(
        (
            {
                "receipt_ref": receipt.ref.as_dict(),
                "receipt_state": receipt.typed_state,
                "coverage_state": _text(receipt.coverage_state, "coverage_state"),
            }
            for receipt in bundle.discovery_receipts
        ),
        key=canonical_json,
    ))
    empirical_states = tuple(sorted(
        (
            {
                "family": obj.family,
                "object_ref": obj.ref.as_dict(),
                "state": obj.typed_state,
            }
            for obj in (*bundle.empirical_facts, *bundle.discovery_receipts)
        ),
        key=canonical_json,
    ))
    authority_states = tuple(sorted(
        (
            {
                "authority_ref": snapshot.authority_ref.as_dict(),
                "state": snapshot.typed_state,
                "authority_kind": snapshot.authority_kind,
            }
            for snapshot in bundle.authority_snapshots
        ),
        key=canonical_json,
    ))
    uncertainty = tuple(sorted(
        (
            _material(receipt.support_uncertainty_state)
            for receipt in bundle.discovery_receipts
        ),
        key=canonical_json,
    ))
    uncertainty_refs: list[ExactRef] = []
    for channel in bundle.prerequisite_channels:
        if channel.channel_kind == "UNCERTAINTY":
            uncertainty_refs.extend(channel.dependency_refs)

    return _BundleVerification(
        authority_registry=authority_registry,
        discovery_receipts=bundle.discovery_receipts,
        discovery_authorities=bundle.discovery_authorities,
        empirical_facts=bundle.empirical_facts,
        empirical_queries=bundle.empirical_queries,
        empirical_predicates=bundle.empirical_predicates,
        source_universe_refs=_canonical_refs(source_refs, "source universe ref"),
        risk_set_refs=_canonical_refs(risk_refs, "risk set ref"),
        measure_basis_refs=_canonical_refs(measure_refs, "measure basis ref"),
        topology_scope_material=topology_tuple,
        coverage_claims=coverage_claims,
        coverage_states=coverage_states,
        empirical_states=empirical_states,
        authority_states=authority_states,
        support_uncertainty_state=uncertainty,
        support_uncertainty_refs=_canonical_refs(
            uncertainty_refs, "support uncertainty ref"
        ),
    )


def _scope_allows(scope_value: Any, required: Any) -> bool:
    material = _material(scope_value)
    required_material = _material(required)
    if isinstance(material, str):
        if material == "EXPLICIT_UNRESTRICTED":
            return True
        if material.upper() in _FORBIDDEN_SELECTOR_TOKENS:
            raise M1BlockedError("rule applicability scope uses forbidden selector")
        return canonical_json(material) == canonical_json(required_material)
    if isinstance(material, Sequence) and not isinstance(material, (str, bytes)):
        allowed = {canonical_json(item) for item in material}
        return canonical_json(required_material) in allowed
    return canonical_json(material) == canonical_json(required_material)


def _verify_binding(
    *,
    bundle: M1AdjudicationInputBundle,
    verified: _BundleVerification,
    binding: M1FamilyRuleBinding,
) -> Mapping[str, M1PrerequisiteChannel]:
    if not isinstance(binding, M1FamilyRuleBinding):
        raise M1BlockedError("exact M1FamilyRuleBinding@1.0.0 required")
    if (
        binding.claim_family_id != bundle.requested_claim_family_id
        or binding.claim_rule_id != bundle.requested_claim_rule_id
    ):
        raise M1BlockedError("rule binding claim-family/rule identity mismatch")

    for ref in binding.authority_closure_refs:
        try:
            snapshot = verified.authority_registry.resolve_exact(ref).snapshot
        except Pre553AuthorityError as exc:
            raise M1BlockedError("rule binding authority closure is incomplete") from exc
        if snapshot.typed_state != "ALLOW":
            raise M1BlockedError(
                f"rule binding authority is not positive: {snapshot.typed_state}"
            )

    validator_snapshot = verified.authority_registry.resolve_exact(
        binding.validator_authority_ref
    ).snapshot
    if validator_snapshot.typed_state != "ALLOW":
        raise M1BlockedError("validator authority is not positive")

    if binding.selection_purpose == "CURRENT_GOVERNED_USE":
        assert binding.current_selection_authority_ref is not None
        selection_snapshot = verified.authority_registry.resolve_exact(
            binding.current_selection_authority_ref
        ).snapshot
        if selection_snapshot.typed_state != "ALLOW":
            raise M1BlockedError("current rule-selection authority is not positive")

    scope = binding.applicability_scope
    required_dimensions = {
        "source_universe_refs": verified.source_universe_refs,
        "risk_set_refs": verified.risk_set_refs,
        "measure_basis_refs": verified.measure_basis_refs,
        "topology_scope_material": verified.topology_scope_material,
    }
    for dimension, values in required_dimensions.items():
        if dimension not in scope:
            raise M1BlockedError(f"rule applicability scope omits {dimension}")
        for value in values:
            if not _scope_allows(scope[dimension], value):
                raise M1BlockedError(f"rule applicability scope mismatch for {dimension}")
    if "requested_scope" not in scope:
        raise M1BlockedError("rule applicability scope omits requested_scope")
    bound_requested = scope["requested_scope"]
    if not isinstance(bound_requested, Mapping):
        if bound_requested != "EXPLICIT_UNRESTRICTED":
            raise M1BlockedError("requested_scope applicability contract malformed")
    else:
        for key, value in bundle.requested_scope.items():
            if key not in bound_requested or not _scope_allows(bound_requested[key], value):
                raise M1BlockedError(f"requested scope mismatch for {key}")

    family_objects = {
        "DiscoveryResultReceipt@1.0.0": bundle.discovery_receipts,
        "DiscoveryAuthority@1.0.0": bundle.discovery_authorities,
        "EmpiricalFact@1.0.0": bundle.empirical_facts,
        "EmpiricalQuerySpec@1.0.0": bundle.empirical_queries,
        "EmpiricalPredicate@1.0.0": bundle.empirical_predicates,
    }
    for family, objects in family_objects.items():
        allowed = set(binding.allowed_input_object_families_and_states[family])
        for obj in objects:
            if obj.typed_state not in allowed:
                raise M1BlockedError(
                    f"input state {obj.typed_state!r} is outside exact rule contract for {family}"
                )

    coverage = binding.required_coverage_strength
    allowed_claims = set(coverage["allowed_coverage_claims"])
    allowed_receipt_states = set(coverage["allowed_receipt_states"])
    allowed_coverage_states = set(coverage["allowed_coverage_states"])
    if not set(verified.coverage_claims).issubset(allowed_claims):
        raise M1BlockedError("coverage claim exceeds exact family-rule allowance")
    for row in verified.coverage_states:
        if row["receipt_state"] not in allowed_receipt_states:
            raise M1BlockedError("receipt state exceeds exact family-rule coverage allowance")
        if row["coverage_state"] not in allowed_coverage_states:
            raise M1BlockedError("coverage state exceeds exact family-rule allowance")

    channels = {channel.channel_id: channel for channel in bundle.prerequisite_channels}
    for channel_id in binding.required_prerequisite_channels:
        channel = channels.get(channel_id)
        if channel is None:
            raise M1BlockedError(
                f"missing required prerequisite channel {channel_id}"
            )
        if channel.state == "INTEGRITY_FAILURE":
            exc = M1IntegrityError(
                f"required prerequisite channel {channel_id} has integrity failure"
            )
            if channel.detail.get("terminal_reason_code") is not None:
                setattr(
                    exc,
                    "reason_code",
                    _text(channel.detail["terminal_reason_code"], "terminal_reason_code"),
                )
            raise exc
        if channel.state in {"UNKNOWN", "UNRESOLVED"}:
            exc = M1UnresolvedError(
                f"required prerequisite channel {channel_id} is {channel.state}"
            )
            if channel.detail.get("terminal_reason_code") is not None:
                setattr(
                    exc,
                    "reason_code",
                    _text(channel.detail["terminal_reason_code"], "terminal_reason_code"),
                )
            raise exc
        if channel.state != "SATISFIED":
            exc = M1BlockedError(
                f"required prerequisite channel {channel_id} is {channel.state}"
            )
            if channel.detail.get("terminal_reason_code") is not None:
                setattr(
                    exc,
                    "reason_code",
                    _text(channel.detail["terminal_reason_code"], "terminal_reason_code"),
                )
            raise exc

    relation_kinds = {
        kind for channel in channels.values() for kind in channel.relation_kinds
    }
    if not set(binding.required_source_relation_kinds).issubset(relation_kinds):
        raise M1BlockedError("required source-relation premise is absent")

    premise_authorities = {
        ref for channel in channels.values() for ref in channel.authority_refs
    }
    if not set(binding.required_measure_weight_estimand_authorities).issubset(
        premise_authorities
    ):
        raise M1BlockedError(
            "required measure/weight/estimand authority premise is absent"
        )
    for ref in binding.required_measure_weight_estimand_authorities:
        try:
            snapshot = verified.authority_registry.resolve_exact(ref).snapshot
        except Pre553AuthorityError as exc:
            raise M1BlockedError(
                "required measure/weight/estimand authority is unavailable"
            ) from exc
        if snapshot.typed_state != "ALLOW":
            raise M1BlockedError(
                "required measure/weight/estimand authority is not positive"
            )

    if any(
        row["state"] == "INTEGRITY_FAILURE" for row in verified.empirical_states
    ):
        raise M1IntegrityError("upstream empirical evidence carries INTEGRITY_FAILURE")

    return channels


def _validate_family_result(
    result: FamilyValidationResult,
    *,
    binding: M1FamilyRuleBinding,
    registration: FamilyValidatorRegistration,
) -> None:
    if not isinstance(result, FamilyValidationResult):
        raise M1IntegrityError("family validator returned wrong result object")
    if (
        result.claim_family_id != binding.claim_family_id
        or result.claim_rule_id != binding.claim_rule_id
        or result.family_rule_binding_ref != binding.ref
        or result.validator_authority_ref != binding.validator_authority_ref
        or result.validator_algorithm_identity
        != binding.validator_algorithm_identity_if_required
    ):
        raise M1IntegrityError("family validator result does not match exact binding")
    if result.semantic_ceiling != binding.semantic_ceiling:
        raise M1IntegrityError("family validator attempted semantic-ceiling drift")
    if dict(result.effects) != dict(_FALSE_EFFECTS):
        raise M1IntegrityError("family validator requested forbidden downstream side effect")
    emission = binding.output_semantic_contract["truth_bearing_claim_emission"]
    if result.semantic_claim_identity_ref is not None and emission != "EXPLICITLY_AUTHORIZED":
        raise M1IntegrityError(
            "family validator emitted truth-bearing claim without exact output authority"
        )


def _outcome_axes(outcome: str) -> tuple[str, str]:
    return {
        "RULE_SATISFIED": ("SUBSTANTIVE", "RULE_SATISFIED"),
        "RULE_NOT_SATISFIED": ("SUBSTANTIVE", "RULE_NOT_SATISFIED"),
        "ABSTAINED": ("ABSTENTION", "NOT_EVALUATED"),
        "BLOCKED": ("BLOCKED", "NOT_EVALUATED"),
        "UNRESOLVED": ("UNRESOLVED", "UNRESOLVED"),
        "INTEGRITY_FAILURE": ("INTEGRITY_FAILURE", "UNRESOLVED"),
    }[outcome]


def _channel_refs(
    channels: Iterable[M1PrerequisiteChannel], kind: str
) -> tuple[AuthorityRef, ...]:
    return _canonical_authority_refs(
        (
            ref
            for channel in channels
            if channel.channel_kind == kind
            for ref in channel.authority_refs
        ),
        f"{kind} authority ref",
    )


def _blocking_authority_refs(
    channels: Iterable[M1PrerequisiteChannel],
) -> tuple[AuthorityRef, ...]:
    return _canonical_authority_refs(
        (
            ref
            for channel in channels
            if channel.state != "SATISFIED"
            for ref in channel.authority_refs
        ),
        "blocking negative authority ref",
    )


def _safe_verified_or_summary(
    bundle: M1AdjudicationInputBundle,
) -> _BundleVerification:
    try:
        return _verify_bundle(bundle)
    except M1AdjudicationError:
        source_refs: list[ExactRef] = []
        risk_refs: list[ExactRef] = []
        measure_refs: list[ExactRef] = []
        topology: list[Any] = []
        for fact in bundle.empirical_facts:
            try:
                source_refs.extend(_ref(x, "source") for x in fact.empirical_universe_refs)
                risk_refs.append(_ref(fact.risk_set_ref, "risk"))
                measure_refs.append(_ref(fact.measure_basis_ref, "measure"))
                topology.append(_material(fact.target_topology))
            except Exception:
                pass
        authority_states = tuple(sorted(
            ({
                "authority_ref": snapshot.authority_ref.as_dict(),
                "state": snapshot.typed_state,
                "authority_kind": snapshot.authority_kind,
            } for snapshot in bundle.authority_snapshots),
            key=canonical_json,
        ))
        empirical_states = tuple(sorted(
            ({
                "family": obj.family,
                "object_ref": obj.ref.as_dict(),
                "state": obj.typed_state,
            } for obj in (*bundle.empirical_facts, *bundle.discovery_receipts)),
            key=canonical_json,
        ))
        coverage_states = tuple(sorted(
            ({
                "receipt_ref": receipt.ref.as_dict(),
                "receipt_state": receipt.typed_state,
                "coverage_state": str(receipt.coverage_state),
            } for receipt in bundle.discovery_receipts),
            key=canonical_json,
        ))
        try:
            registry = AuthorityRegistry(bundle.authority_snapshots)
        except Exception:
            registry = AuthorityRegistry(())
        return _BundleVerification(
            authority_registry=registry,
            discovery_receipts=bundle.discovery_receipts,
            discovery_authorities=bundle.discovery_authorities,
            empirical_facts=bundle.empirical_facts,
            empirical_queries=bundle.empirical_queries,
            empirical_predicates=bundle.empirical_predicates,
            source_universe_refs=_canonical_refs(source_refs, "source"),
            risk_set_refs=_canonical_refs(risk_refs, "risk"),
            measure_basis_refs=_canonical_refs(measure_refs, "measure"),
            topology_scope_material=tuple(
                {canonical_json(x): x for x in topology}[k]
                for k in sorted({canonical_json(x): x for x in topology})
            ),
            coverage_claims=tuple(sorted({
                str(x.coverage_claim) for x in bundle.discovery_authorities
            })),
            coverage_states=coverage_states,
            empirical_states=empirical_states,
            authority_states=authority_states,
            support_uncertainty_state=(),
            support_uncertainty_refs=(),
        )


def _make_terminal_result(
    *,
    bundle: M1AdjudicationInputBundle,
    binding: M1FamilyRuleBinding | None,
    outcome: str,
    reason_code: str,
    detail: str,
) -> FamilyValidationResult:
    binding_ref = (
        binding.ref
        if binding is not None
        else ExactRef(
            "M1FamilyRuleBinding@1.0.0",
            "urn:rawlsing:pre553:m1:missing-family-rule-binding",
            semantic_hash({
                "missing_binding": True,
                "claim_family_id": bundle.requested_claim_family_id,
                "claim_rule_id": bundle.requested_claim_rule_id,
            }),
        )
    )
    validator_authority = (
        binding.validator_authority_ref
        if binding is not None
        else AuthorityRef(
            "MISSING_FAMILY_VALIDATION_RULE_AUTHORITY",
            "0",
            semantic_hash({
                "missing_validator_authority": True,
                "claim_family_id": bundle.requested_claim_family_id,
                "claim_rule_id": bundle.requested_claim_rule_id,
            }),
        )
    )
    algorithm = (
        binding.validator_algorithm_identity_if_required
        if binding is not None
        else "NOT_EVALUATED__MISSING_FAMILY_RULE_BINDING"
    )
    ceiling = (
        binding.semantic_ceiling if binding is not None else M1_DEFAULT_SEMANTIC_CEILING
    )
    return FamilyValidationResult(
        claim_family_id=bundle.requested_claim_family_id,
        claim_rule_id=bundle.requested_claim_rule_id,
        family_rule_binding_ref=binding_ref,
        validator_authority_ref=validator_authority,
        validator_algorithm_identity=algorithm,
        adjudication_outcome=outcome,
        reason_code=reason_code,
        relation_proposition_identity_ref=None,
        semantic_claim_identity_ref=None,
        semantic_assertion_polarity_or_state="NONE",
        semantic_ceiling=ceiling,
        determinant_material={"terminal_detail": detail},
        explanation_material={
            "reason_code": reason_code,
            "detail": detail,
            "substantive_validator_executed": False,
        },
    )


def _build_disposition(
    *,
    bundle: M1AdjudicationInputBundle,
    verified: _BundleVerification,
    binding: M1FamilyRuleBinding | None,
    validation_result: FamilyValidationResult,
    registration_identity: str,
) -> LearnedEmpiricalDisposition:
    channels = bundle.prerequisite_channels
    binding_ref_material: ExactRef | TypedAbsence = (
        binding.ref
        if binding is not None
        else _typed_absence("MISSING", "no exact M1 family rule binding")
    )
    validator_ref_material: AuthorityRef | TypedAbsence = (
        binding.validator_authority_ref
        if binding is not None
        else _typed_absence("MISSING", "no exact validator authority")
    )
    selection_ref_material: AuthorityRef | TypedAbsence = (
        binding.current_selection_authority_ref
        if binding is not None and binding.current_selection_authority_ref is not None
        else _typed_absence(
            "NOT_APPLICABLE",
            "exact pinned replay or adjudication blocked before current selection",
        )
    )
    params_ref_material: ExactRef | TypedAbsence = (
        binding.validator_parameters_ref
        if binding is not None
        else _typed_absence("MISSING", "validator parameters unavailable without binding")
    )
    relation_ref_material: ExactRef | TypedAbsence = (
        validation_result.relation_proposition_identity_ref
        if validation_result.relation_proposition_identity_ref is not None
        else _typed_absence("NOT_APPLICABLE", "no proposition emitted")
    )
    claim_ref_material: ExactRef | TypedAbsence = (
        validation_result.semantic_claim_identity_ref
        if validation_result.semantic_claim_identity_ref is not None
        else _typed_absence("NOT_AUTHORIZED", "no truth-bearing claim emitted")
    )

    empirical_fact_refs = tuple(obj.ref for obj in verified.empirical_facts)
    validation_fact_refs = _canonical_refs(
        (
            ref
            for receipt in verified.discovery_receipts
            for ref in receipt.validation_fact_refs
        ),
        "validation fact ref",
    )
    discovery_receipt_refs = tuple(obj.ref for obj in verified.discovery_receipts)
    discovery_authority_refs = tuple(obj.ref for obj in verified.discovery_authorities)
    query_refs = tuple(obj.ref for obj in verified.empirical_queries)
    predicate_refs = tuple(obj.ref for obj in verified.empirical_predicates)

    authority_closure = _canonical_authority_refs(
        (
            *(snapshot.authority_ref for snapshot in bundle.authority_snapshots),
            *((binding.authority_closure_refs) if binding is not None else ()),
        ),
        "disposition authority closure",
    )
    dependency_refs = _canonical_refs(
        (
            *discovery_receipt_refs,
            *discovery_authority_refs,
            *empirical_fact_refs,
            *query_refs,
            *predicate_refs,
            *bundle.evaluated_frontier_refs,
            *bundle.discovery_replay_refs,
            *bundle.additional_dependency_refs,
            *(channel.ref for channel in channels),
            *((binding.ref,) if binding is not None else ()),
            validation_result.ref,
        ),
        "disposition dependency ref",
    )

    prerequisite_states = MappingProxyType({
        channel.channel_id: channel.state for channel in channels
    })
    determinant_manifest = {
        "jurisdiction_contract_id": M1_ADJUDICATION_CONTRACT_ID,
        "claim_family_id": bundle.requested_claim_family_id,
        "claim_rule_id": bundle.requested_claim_rule_id,
        "input_bundle_ref": bundle.ref.as_dict(),
        "input_bundle_preimage": bundle.as_dict(),
        "family_rule_binding_ref_or_typed_absence": _material(binding_ref_material),
        "family_rule_binding_preimage": binding.as_dict() if binding is not None else None,
        "validator_registration_identity": registration_identity,
        "family_validation_result_ref": validation_result.ref.as_dict(),
        "family_validation_result_preimage": validation_result.as_dict(),
        "discovery_result_receipt_refs": [ref.as_dict() for ref in discovery_receipt_refs],
        "discovery_authority_refs": [ref.as_dict() for ref in discovery_authority_refs],
        "empirical_fact_refs": [ref.as_dict() for ref in empirical_fact_refs],
        "validation_fact_refs": [ref.as_dict() for ref in validation_fact_refs],
        "empirical_query_spec_refs": [ref.as_dict() for ref in query_refs],
        "empirical_predicate_refs": [ref.as_dict() for ref in predicate_refs],
        "evaluated_frontier_refs": [ref.as_dict() for ref in bundle.evaluated_frontier_refs],
        "discovery_replay_refs": [ref.as_dict() for ref in bundle.discovery_replay_refs],
        "coverage_claims": verified.coverage_claims,
        "coverage_states": verified.coverage_states,
        "conserved_empirical_states": verified.empirical_states,
        "conserved_authority_states": verified.authority_states,
        "required_prerequisite_channel_states": prerequisite_states,
        "validator_determinants": validation_result.determinant_material,
        "effects": _FALSE_EFFECTS,
    }
    explanation = {
        "what_was_adjudicated": {
            "claim_family_id": bundle.requested_claim_family_id,
            "claim_rule_id": bundle.requested_claim_rule_id,
            "requested_scope": bundle.requested_scope,
        },
        "governing_rule": {
            "family_rule_binding_ref_or_typed_absence": _material(binding_ref_material),
            "validator_authority_ref_or_typed_absence": _material(validator_ref_material),
            "rule_selection_authority_ref_or_typed_absence": _material(selection_ref_material),
            "validator_algorithm_identity": validation_result.validator_algorithm_identity,
        },
        "evidence_and_scope": {
            "empirical_fact_refs": [ref.as_dict() for ref in empirical_fact_refs],
            "validation_fact_refs": [ref.as_dict() for ref in validation_fact_refs],
            "source_universe_refs": [
                ref.as_dict() for ref in verified.source_universe_refs
            ],
            "risk_set_refs": [ref.as_dict() for ref in verified.risk_set_refs],
            "measure_basis_refs": [ref.as_dict() for ref in verified.measure_basis_refs],
            "coverage_states": verified.coverage_states,
            "conserved_empirical_states": verified.empirical_states,
        },
        "prerequisites": prerequisite_states,
        "result": {
            "adjudication_outcome": validation_result.adjudication_outcome,
            "reason_code": validation_result.reason_code,
            "validator_explanation": validation_result.explanation_material,
        },
        "semantic_ceiling": validation_result.semantic_ceiling,
        "does_not_authorize": tuple(sorted(
            key for key, value in _FALSE_EFFECTS.items() if value is False
        )),
    }
    replay_material = {
        "contract": M1_ADJUDICATION_CONTRACT_ID,
        "input_bundle_ref": bundle.ref.as_dict(),
        "family_rule_binding_ref_or_typed_absence": _material(binding_ref_material),
        "validator_registration_identity": registration_identity,
        "family_validation_result_ref": validation_result.ref.as_dict(),
        "authority_closure_refs": [ref.as_dict() for ref in authority_closure],
        "dependency_refs": [ref.as_dict() for ref in dependency_refs],
        "determinant_manifest_hash": semantic_hash(determinant_manifest),
        "semantic_ceiling": validation_result.semantic_ceiling,
        "effects": _FALSE_EFFECTS,
    }
    receipt = M1DeterminantExplanationReceipt(
        input_bundle_ref=bundle.ref,
        family_rule_binding_ref_or_typed_absence=binding_ref_material,
        validator_registration_identity=registration_identity,
        family_validation_result_ref=validation_result.ref,
        determinant_manifest=determinant_manifest,
        explanation=explanation,
        replay_material=replay_material,
        semantic_ceiling=validation_result.semantic_ceiling,
    )

    disposition_class, rule_outcome = _outcome_axes(
        validation_result.adjudication_outcome
    )
    return LearnedEmpiricalDisposition(
        disposition_class=disposition_class,
        adjudication_outcome=validation_result.adjudication_outcome,
        rule_outcome=rule_outcome,
        reason_code=validation_result.reason_code,
        claim_family_id=bundle.requested_claim_family_id,
        claim_rule_id=bundle.requested_claim_rule_id,
        relation_proposition_identity_ref=relation_ref_material,
        semantic_claim_identity_ref=claim_ref_material,
        semantic_assertion_polarity_or_state=validation_result.semantic_assertion_polarity_or_state,
        family_rule_binding_ref=binding_ref_material,
        validator_authority_ref=validator_ref_material,
        rule_selection_authority_ref=selection_ref_material,
        discovery_result_receipt_refs=discovery_receipt_refs,
        discovery_authority_refs=discovery_authority_refs,
        empirical_fact_refs=empirical_fact_refs,
        validation_fact_refs=validation_fact_refs,
        empirical_query_spec_refs=query_refs,
        empirical_predicate_refs=predicate_refs,
        source_universe_refs=verified.source_universe_refs,
        risk_set_refs=verified.risk_set_refs,
        topology_scope_material=verified.topology_scope_material,
        measure_basis_refs=verified.measure_basis_refs,
        weight_design_estimand_refs=(
            binding.required_measure_weight_estimand_authorities
            if binding is not None
            else ()
        ),
        comparability_authority_refs=_channel_refs(channels, "COMPARABILITY"),
        composition_authority_refs=_channel_refs(channels, "COMPOSITION"),
        coverage_claims=verified.coverage_claims,
        coverage_states=verified.coverage_states,
        conserved_empirical_states=verified.empirical_states,
        conserved_authority_states=verified.authority_states,
        support_uncertainty_state=verified.support_uncertainty_state,
        support_uncertainty_refs=verified.support_uncertainty_refs,
        blocking_negative_authority_refs=_blocking_authority_refs(channels),
        required_prerequisite_channel_states=prerequisite_states,
        semantic_ceiling=validation_result.semantic_ceiling,
        authority_closure_refs=authority_closure,
        dependency_refs=dependency_refs,
        validator_algorithm_identity=validation_result.validator_algorithm_identity,
        validator_parameters_ref=params_ref_material,
        determinant_manifest_ref=receipt.determinant_manifest_ref,
        explanation_ref=receipt.explanation_ref,
        replay_ref=receipt.replay_ref,
        determinant_explanation_receipt_ref=receipt.ref,
        effects=_FALSE_EFFECTS,
        determinant_explanation_receipt=receipt,
    )


def adjudicate_learned_empirical(
    input_bundle: M1AdjudicationInputBundle,
    family_rule_binding: M1FamilyRuleBinding | None,
    *,
    validator_registry: M1ValidatorRegistry,
) -> LearnedEmpiricalDisposition:
    """Verify, exactly dispatch, conserve states, and emit one M1 disposition."""
    if not isinstance(input_bundle, M1AdjudicationInputBundle):
        raise M1IntegrityError("exact M1AdjudicationInputBundle@1.0.0 required")
    if not isinstance(validator_registry, M1ValidatorRegistry):
        raise M1IntegrityError("exact M1ValidatorRegistry required")

    try:
        verified = _verify_bundle(input_bundle)
    except M1IntegrityError as exc:
        summary = _safe_verified_or_summary(input_bundle)
        result = _make_terminal_result(
            bundle=input_bundle,
            binding=family_rule_binding
            if isinstance(family_rule_binding, M1FamilyRuleBinding)
            else None,
            outcome="INTEGRITY_FAILURE",
            reason_code="INPUT_BUNDLE_INTEGRITY_FAILURE",
            detail=str(exc),
        )
        return _build_disposition(
            bundle=input_bundle,
            verified=summary,
            binding=family_rule_binding
            if isinstance(family_rule_binding, M1FamilyRuleBinding)
            else None,
            validation_result=result,
            registration_identity="NOT_DISPATCHED__INPUT_INTEGRITY_FAILURE",
        )
    except M1BlockedError as exc:
        summary = _safe_verified_or_summary(input_bundle)
        result = _make_terminal_result(
            bundle=input_bundle,
            binding=family_rule_binding
            if isinstance(family_rule_binding, M1FamilyRuleBinding)
            else None,
            outcome="BLOCKED",
            reason_code="MISSING_AUTHORITY_CLOSURE",
            detail=str(exc),
        )
        return _build_disposition(
            bundle=input_bundle,
            verified=summary,
            binding=family_rule_binding
            if isinstance(family_rule_binding, M1FamilyRuleBinding)
            else None,
            validation_result=result,
            registration_identity="NOT_DISPATCHED__AUTHORITY_CLOSURE_BLOCKED",
        )

    if family_rule_binding is None:
        result = _make_terminal_result(
            bundle=input_bundle,
            binding=None,
            outcome="BLOCKED",
            reason_code="MISSING_FAMILY_VALIDATION_RULE_AUTHORITY",
            detail=(
                "exact family rule binding is absent; provenance/support/replay do not self-authorize"
            ),
        )
        return _build_disposition(
            bundle=input_bundle,
            verified=verified,
            binding=None,
            validation_result=result,
            registration_identity="NOT_DISPATCHED__MISSING_FAMILY_RULE_BINDING",
        )

    try:
        channels = _verify_binding(
            bundle=input_bundle, verified=verified, binding=family_rule_binding
        )
        registration = validator_registry.resolve_exact(family_rule_binding)
    except M1IntegrityError as exc:
        result = _make_terminal_result(
            bundle=input_bundle,
            binding=family_rule_binding,
            outcome="INTEGRITY_FAILURE",
            reason_code=getattr(
                exc, "reason_code", "M1_BINDING_OR_PREMISE_INTEGRITY_FAILURE"
            ),
            detail=str(exc),
        )
        return _build_disposition(
            bundle=input_bundle,
            verified=verified,
            binding=family_rule_binding,
            validation_result=result,
            registration_identity="NOT_DISPATCHED__M1_INTEGRITY_FAILURE",
        )
    except M1UnresolvedError as exc:
        result = _make_terminal_result(
            bundle=input_bundle,
            binding=family_rule_binding,
            outcome="UNRESOLVED",
            reason_code=getattr(
                exc, "reason_code", "REQUIRED_PREREQUISITE_UNRESOLVED"
            ),
            detail=str(exc),
        )
        return _build_disposition(
            bundle=input_bundle,
            verified=verified,
            binding=family_rule_binding,
            validation_result=result,
            registration_identity="NOT_DISPATCHED__PREREQUISITE_UNRESOLVED",
        )
    except (M1BlockedError, Pre553AuthorityError) as exc:
        result = _make_terminal_result(
            bundle=input_bundle,
            binding=family_rule_binding,
            outcome="BLOCKED",
            reason_code=getattr(
                exc, "reason_code", "RULE_BINDING_OR_PREREQUISITE_BLOCKED"
            ),
            detail=str(exc),
        )
        return _build_disposition(
            bundle=input_bundle,
            verified=verified,
            binding=family_rule_binding,
            validation_result=result,
            registration_identity="NOT_DISPATCHED__RULE_OR_PREMISE_BLOCKED",
        )

    evidence_context = MappingProxyType({
        "source_universe_refs": verified.source_universe_refs,
        "risk_set_refs": verified.risk_set_refs,
        "measure_basis_refs": verified.measure_basis_refs,
        "topology_scope_material": verified.topology_scope_material,
        "coverage_claims": verified.coverage_claims,
        "coverage_states": verified.coverage_states,
        "conserved_empirical_states": verified.empirical_states,
        "conserved_authority_states": verified.authority_states,
        "prerequisite_channels": MappingProxyType(dict(channels)),
    })
    context = M1ValidatorContext(
        input_bundle=input_bundle,
        family_rule_binding=family_rule_binding,
        evidence_context=evidence_context,
    )
    try:
        validation_result = registration.validator(context)
        _validate_family_result(
            validation_result,
            binding=family_rule_binding,
            registration=registration,
        )
    except Exception as exc:
        result = _make_terminal_result(
            bundle=input_bundle,
            binding=family_rule_binding,
            outcome="INTEGRITY_FAILURE",
            reason_code="VALIDATOR_EXECUTION_OR_CONTRACT_FAILURE",
            detail=f"{type(exc).__name__}: {exc}",
        )
        return _build_disposition(
            bundle=input_bundle,
            verified=verified,
            binding=family_rule_binding,
            validation_result=result,
            registration_identity=registration.registration_identity,
        )

    return _build_disposition(
        bundle=input_bundle,
        verified=verified,
        binding=family_rule_binding,
        validation_result=validation_result,
        registration_identity=registration.registration_identity,
    )


def verify_m1_disposition_replay(
    disposition: LearnedEmpiricalDisposition,
) -> str:
    """Verify the deterministic determinant/explanation/replay closure of output."""
    if not isinstance(disposition, LearnedEmpiricalDisposition):
        raise M1IntegrityError("LearnedEmpiricalDisposition@1.0.0 required")
    receipt = disposition.determinant_explanation_receipt
    if receipt.ref != disposition.determinant_explanation_receipt_ref:
        raise M1IntegrityError("determinant/explanation receipt identity drift")
    if receipt.determinant_manifest_ref != disposition.determinant_manifest_ref:
        raise M1IntegrityError("determinant manifest identity drift")
    if receipt.explanation_ref != disposition.explanation_ref:
        raise M1IntegrityError("explanation identity drift")
    if receipt.replay_ref != disposition.replay_ref:
        raise M1IntegrityError("replay identity drift")
    if dict(disposition.effects) != dict(_FALSE_EFFECTS):
        raise M1IntegrityError("M1 replay detected forbidden downstream effect")
    return disposition.replay_ref.content_hash


__all__ = [
    "M1_ADJUDICATION_CONTRACT_ID",
    "M1_DEFAULT_SEMANTIC_CEILING",
    "M1_OUTCOMES",
    "M1AdjudicationError",
    "M1IntegrityError",
    "M1BlockedError",
    "M1UnresolvedError",
    "M1PrerequisiteChannel",
    "M1FamilyRuleBinding",
    "M1AdjudicationInputBundle",
    "FamilyValidationResult",
    "M1DeterminantExplanationReceipt",
    "LearnedEmpiricalDisposition",
    "FamilyValidatorRegistration",
    "M1ValidatorRegistry",
    "M1ValidatorContext",
    "build_m1_adjudication_input_bundle",
    "adjudicate_learned_empirical",
    "verify_m1_disposition_replay",
]
