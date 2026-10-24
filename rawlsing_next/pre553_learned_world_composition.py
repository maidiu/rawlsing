"""PYAT HQ119 I4 — exact learned-world composition/adaptation runtime.

I4 is a seam, not a semantic stage.  It binds exact objects already owned by
M01, M1, M2 and B5.  It never selects a family rule, product family, current
release, consumer permission, or lifecycle action by inference.

The default lifecycle action is NO_LIFECYCLE_SIDE_EFFECT.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_learned_empirical_adjudication import (
    M1_ADJUDICATION_CONTRACT_ID,
    M1AdjudicationInputBundle,
    M1FamilyRuleBinding,
    M1PrerequisiteChannel,
    M1ValidatorRegistry,
    LearnedEmpiricalDisposition,
    adjudicate_learned_empirical,
    build_m1_adjudication_input_bundle,
    verify_m1_disposition_replay,
)
from rawlsing_next.pre553_learned_product_lifecycle import (
    CurrentSelectionReceipt,
    LearnedProductLifecycleError,
    LearnedProductLifecycleExecutor,
    LearnedProductLifecycleSubject,
    LifecycleReplayReceipt,
)
from rawlsing_next.pre553_learned_product_release import (
    M2Repository,
    M2ReleaseError,
    ClosureObject,
    ProducerSubject,
    ReleaseCore,
    constitute_closure,
    constitute_release,
    register_producer_subject,
)
from rawlsing_next.pre553_route_b_production import RouteBProductionResult
from rawlsing_next.pre553_analytical_composition import (
    AnalyticalCompositionResult,
    native_composition_original,
)
from rawlsing_next.pre553_universal_empirical_extension import (
    EXT_ROUTE_DIRECT_MULTI_CONDITIONER,
    EXT_ROUTE_DIRECT_VIA_ACCEPTED_PROVIDER,
    EXT_ROUTE_DISCOVERY,
    EXT_ROUTE_RECURSIVE,
    EmpiricalPossibilitySliceExtensionResult,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
    PositionedSubjectPossibilityResult,
    PossibilitySliceEvidence,
    evaluate_positioned_subject_possibility,
)


PRODUCT_CONTRACT_SCHEMA = "LearnedWorldProductContractBinding@1.0.0"
COMPOSITION_RECEIPT_SCHEMA = "LearnedWorldCompositionReceipt@1.0.0"
COMPOSITION_RUNTIME_ID = "PYAT_HQ119_I4_LEARNED_WORLD_COMPOSITION@1.0.0"
AUTHORITY_TRANSPORT_SCHEMA = "I4AuthorityTransportRef@1.0.0"

ROUTES = frozenset({"M01_M1_M2_B5", "M1_M2_B5", "DIRECT_PRODUCER"})
LIFECYCLE_ACTIONS = ("REGISTER", "PUBLISH", "SELECT_CURRENT")
NO_LIFECYCLE_SIDE_EFFECT = "NO_LIFECYCLE_SIDE_EFFECT"
CLOSURE_RULE = "M1_EXACT_CLOSURE_PRESERVATION@1.0.0"
LIFECYCLE_POLICY = "EXPLICIT_ACTIONS_ONLY@1.0.0"
SEMANTIC_SUBJECT_RULE = "M1_DISPOSITION_REF_EXACT"
SEMANTIC_PRODUCT_RULE = "M2_SUBJECT_REF_EXACT"
SEMANTIC_PROJECTION_RULE = "EXACT_SUBJECT_CONTENT_HASH"

_FORBIDDEN_SELECTOR_TOKENS = frozenset({
    "LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER", "SEMVER_FALLBACK", "*",
})

_ALWAYS_FALSE_EFFECTS = MappingProxyType({
    "consumer_permission_effect": False,
    "structural_admission_effect": False,
    "causal_truth_effect": False,
    "field_forge_effect": False,
    "actor_v3_effect": False,
    "source_or_carrier_retirement_effect": False,
})


class LearnedWorldCompositionError(ValueError):
    """I4 cannot compose the supplied exact objects lawfully."""


class LearnedWorldCompositionBlocked(LearnedWorldCompositionError):
    """A required exact premise or authorization is absent."""


class LearnedWorldCompositionIntegrityError(LearnedWorldCompositionError):
    """An exact identity, replay, or conservation check failed."""


def _exact(value: ExactRef | Mapping[str, Any] | None, name: str) -> ExactRef:
    if value is None:
        raise LearnedWorldCompositionBlocked(f"{name} is required")
    if isinstance(value, str):
        raise LearnedWorldCompositionBlocked(f"{name} requires an exact ref")
    try:
        ref = exact_ref(value, name)
    except Exception as exc:
        raise LearnedWorldCompositionIntegrityError(
            f"{name} is not an exact ref: {exc}"
        ) from exc
    for text in (ref.kind, ref.object_id):
        upper = text.upper()
        if upper in _FORBIDDEN_SELECTOR_TOKENS or any(
            upper.startswith(f"{token}:") or f":{token}" in upper
            for token in _FORBIDDEN_SELECTOR_TOKENS - {"*"}
        ):
            raise LearnedWorldCompositionBlocked(
                f"{name} may not use latest/default/fuzzy/nearest/semver selection"
            )
    return ref


def _optional_exact(
    value: ExactRef | Mapping[str, Any] | None, name: str
) -> ExactRef | None:
    return None if value is None else _exact(value, name)


def _refs(
    values: Iterable[ExactRef | Mapping[str, Any]], name: str
) -> tuple[ExactRef, ...]:
    refs = {_exact(value, name).key: _exact(value, name) for value in values}
    return tuple(refs[key] for key in sorted(refs))


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    material = canonicalize(dict(value or {}))
    return MappingProxyType(material)


def _derived_ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(
        kind,
        f"urn:rawlsing:pre553:i4:{namespace}:sha256:{digest}",
        digest,
    )


M1_DISPOSITION_PRODUCER_CONTRACT_REF = _derived_ref(
    "M1AdjudicationProducerContract",
    "m1-producer-contract",
    {
        "m1_contract_id": M1_ADJUDICATION_CONTRACT_ID,
        "owned_subject_family": "LearnedEmpiricalDisposition@1.0.0",
        "i4_semantic_reownership": False,
    },
)


def authority_transport_ref(value: AuthorityRef) -> ExactRef:
    """Encode one AuthorityRef losslessly for M2's ExactRef-only closure surface."""
    if not isinstance(value, AuthorityRef):
        raise LearnedWorldCompositionIntegrityError(
            "authority transport requires exact AuthorityRef"
        )
    material = {
        "schema": AUTHORITY_TRANSPORT_SCHEMA,
        "authority_ref": value.as_dict(),
        "semantic_reownership": False,
    }
    return _derived_ref("I4AuthorityTransportRef", "authority-transport", material)


def _authority_from_mapping(value: Mapping[str, Any]) -> AuthorityRef:
    if not isinstance(value, Mapping) or set(value) != {
        "authority_id", "authority_version", "authority_content_hash"
    }:
        raise LearnedWorldCompositionIntegrityError(
            "authority transport preimage is malformed"
        )
    return AuthorityRef(
        str(value["authority_id"]),
        str(value["authority_version"]),
        str(value["authority_content_hash"]),
    )


def _contract_ref_material(value: ExactRef | None) -> Any:
    return None if value is None else value.as_dict()


@dataclass(frozen=True)
class LearnedWorldProductContractBinding:
    """Explicit product/lifecycle facts required by the I4 seam.

    Optional fields stay representable so absence can produce a deterministic
    typed BLOCKED receipt rather than being silently defaulted.
    """

    route: str
    product_family_ref: ExactRef | None
    producer_owner_ref: ExactRef | None
    producer_contract_ref: ExactRef | None
    release_subject_kind: str
    selection_scope_ref: ExactRef | None
    producer_permission_ceiling_ref: ExactRef | None
    consumer_product_purpose_ref: ExactRef | None
    m1_family_rule_binding_ref: ExactRef | None = None

    semantic_subject_rule: str = SEMANTIC_SUBJECT_RULE
    semantic_product_rule: str = SEMANTIC_PRODUCT_RULE
    semantic_projection_rule: str = SEMANTIC_PROJECTION_RULE
    closure_construction_rule: str = CLOSURE_RULE
    lifecycle_policy: str = LIFECYCLE_POLICY

    lifecycle_actions: tuple[str, ...] = ()

    registration_event_authority_ref: ExactRef | None = None
    registration_event_rule_ref: ExactRef | None = None
    registration_evidence_refs: tuple[ExactRef, ...] = ()

    publication_event_authority_ref: ExactRef | None = None
    publication_event_rule_ref: ExactRef | None = None
    publication_evidence_refs: tuple[ExactRef, ...] = ()

    selection_purpose_ref: ExactRef | None = None
    selection_event_authority_ref: ExactRef | None = None
    selection_event_rule_ref: ExactRef | None = None
    selection_attestation_ref: ExactRef | None = None
    selection_evidence_refs: tuple[ExactRef, ...] = ()
    consumer_context_partition_ref: ExactRef | None = None
    expected_previous_selection_receipt_ref: ExactRef | None = None

    direct_producer_route_authority_ref: ExactRef | None = None
    direct_consumer_acceptance_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        route = str(self.route).strip().upper()
        if route not in ROUTES:
            raise LearnedWorldCompositionIntegrityError(f"unknown I4 route {route!r}")
        object.__setattr__(self, "route", route)

        kind = str(self.release_subject_kind).strip().upper()
        if not kind:
            raise LearnedWorldCompositionIntegrityError(
                "release_subject_kind must be explicit"
            )
        object.__setattr__(self, "release_subject_kind", kind)

        for name in (
            "semantic_subject_rule",
            "semantic_product_rule",
            "semantic_projection_rule",
            "closure_construction_rule",
            "lifecycle_policy",
        ):
            text = str(getattr(self, name)).strip()
            if not text:
                raise LearnedWorldCompositionIntegrityError(f"{name} must be explicit")
            object.__setattr__(self, name, text)

        actions = tuple(str(x).strip().upper() for x in self.lifecycle_actions)
        if len(set(actions)) != len(actions):
            raise LearnedWorldCompositionIntegrityError(
                "lifecycle action list contains duplicates"
            )
        if any(action not in LIFECYCLE_ACTIONS for action in actions):
            raise LearnedWorldCompositionIntegrityError(
                "lifecycle action list contains an unknown action"
            )
        expected_prefix = LIFECYCLE_ACTIONS[: len(actions)]
        if actions != expected_prefix:
            raise LearnedWorldCompositionBlocked(
                "lifecycle actions must be an explicit REGISTER -> PUBLISH -> SELECT_CURRENT prefix"
            )
        object.__setattr__(self, "lifecycle_actions", actions)

        exact_field_names = (
            "product_family_ref",
            "producer_owner_ref",
            "producer_contract_ref",
            "selection_scope_ref",
            "producer_permission_ceiling_ref",
            "consumer_product_purpose_ref",
            "m1_family_rule_binding_ref",
            "registration_event_authority_ref",
            "registration_event_rule_ref",
            "publication_event_authority_ref",
            "publication_event_rule_ref",
            "selection_purpose_ref",
            "selection_event_authority_ref",
            "selection_event_rule_ref",
            "selection_attestation_ref",
            "consumer_context_partition_ref",
            "expected_previous_selection_receipt_ref",
            "direct_producer_route_authority_ref",
            "direct_consumer_acceptance_ref",
        )
        for name in exact_field_names:
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, _exact(value, name))

        for name in (
            "registration_evidence_refs",
            "publication_evidence_refs",
            "selection_evidence_refs",
        ):
            object.__setattr__(self, name, _refs(getattr(self, name), name))

    def semantic_projection(self) -> Mapping[str, Any]:
        return {
            "schema": PRODUCT_CONTRACT_SCHEMA,
            "route": self.route,
            "product_family_ref": _contract_ref_material(self.product_family_ref),
            "producer_owner_ref": _contract_ref_material(self.producer_owner_ref),
            "producer_contract_ref": _contract_ref_material(self.producer_contract_ref),
            "release_subject_kind": self.release_subject_kind,
            "selection_scope_ref": _contract_ref_material(self.selection_scope_ref),
            "producer_permission_ceiling_ref": _contract_ref_material(
                self.producer_permission_ceiling_ref
            ),
            "consumer_product_purpose_ref": _contract_ref_material(
                self.consumer_product_purpose_ref
            ),
            "m1_family_rule_binding_ref": _contract_ref_material(
                self.m1_family_rule_binding_ref
            ),
            "semantic_subject_rule": self.semantic_subject_rule,
            "semantic_product_rule": self.semantic_product_rule,
            "semantic_projection_rule": self.semantic_projection_rule,
            "closure_construction_rule": self.closure_construction_rule,
            "lifecycle_policy": self.lifecycle_policy,
            "lifecycle_actions": list(self.lifecycle_actions),
            "registration_event_authority_ref": _contract_ref_material(
                self.registration_event_authority_ref
            ),
            "registration_event_rule_ref": _contract_ref_material(
                self.registration_event_rule_ref
            ),
            "registration_evidence_refs": [
                ref.as_dict() for ref in self.registration_evidence_refs
            ],
            "publication_event_authority_ref": _contract_ref_material(
                self.publication_event_authority_ref
            ),
            "publication_event_rule_ref": _contract_ref_material(
                self.publication_event_rule_ref
            ),
            "publication_evidence_refs": [
                ref.as_dict() for ref in self.publication_evidence_refs
            ],
            "selection_purpose_ref": _contract_ref_material(self.selection_purpose_ref),
            "selection_event_authority_ref": _contract_ref_material(
                self.selection_event_authority_ref
            ),
            "selection_event_rule_ref": _contract_ref_material(
                self.selection_event_rule_ref
            ),
            "selection_attestation_ref": _contract_ref_material(
                self.selection_attestation_ref
            ),
            "selection_evidence_refs": [
                ref.as_dict() for ref in self.selection_evidence_refs
            ],
            "consumer_context_partition_ref": _contract_ref_material(
                self.consumer_context_partition_ref
            ),
            "expected_previous_selection_receipt_ref": _contract_ref_material(
                self.expected_previous_selection_receipt_ref
            ),
            "direct_producer_route_authority_ref": _contract_ref_material(
                self.direct_producer_route_authority_ref
            ),
            "direct_consumer_acceptance_ref": _contract_ref_material(
                self.direct_consumer_acceptance_ref
            ),
        }

    @property
    def ref(self) -> ExactRef:
        return _derived_ref(
            PRODUCT_CONTRACT_SCHEMA,
            "product-contract",
            self.semantic_projection(),
        )

    def as_dict(self) -> Mapping[str, Any]:
        return {
            **self.semantic_projection(),
            "contract_ref": self.ref.as_dict(),
        }


@dataclass(frozen=True)
class M2ProductArtifacts:
    subject: ProducerSubject
    authority_closure: ClosureObject
    dependency_closure: ClosureObject
    determinant_closure: ClosureObject
    replay_closure: ClosureObject
    explanation_closure: ClosureObject
    release: ReleaseCore


@dataclass(frozen=True)
class M2B5LifecycleProtocolView:
    """Thin exact M2->B5 protocol; extra fields exist only for conservation audit."""

    release_ref: ExactRef
    product_ref: ExactRef
    product_family_ref: ExactRef
    producer_owner_ref: ExactRef
    producer_contract_ref: ExactRef
    semantic_projection_hash: str
    authority_snapshot_refs: tuple[AuthorityRef, ...]
    direct_dependency_refs: tuple[ExactRef, ...]
    determinant_refs: tuple[ExactRef, ...]
    determinant_set_hash: str
    replay_root_ref: ExactRef
    selection_scope_ref: ExactRef
    build_or_release_receipt_refs: tuple[ExactRef, ...]
    producer_permission_ceiling_ref: ExactRef

    producer_typed_state: str
    m2_authority_closure_ref: ExactRef
    m2_dependency_closure_ref: ExactRef
    m2_determinant_closure_ref: ExactRef
    m2_replay_closure_ref: ExactRef
    m2_explanation_closure_ref: ExactRef

    def as_dict(self) -> Mapping[str, Any]:
        return {
            "release_ref": self.release_ref.as_dict(),
            "product_ref": self.product_ref.as_dict(),
            "product_family_ref": self.product_family_ref.as_dict(),
            "producer_owner_ref": self.producer_owner_ref.as_dict(),
            "producer_contract_ref": self.producer_contract_ref.as_dict(),
            "semantic_projection_hash": self.semantic_projection_hash,
            "authority_snapshot_refs": [
                ref.as_dict() for ref in self.authority_snapshot_refs
            ],
            "direct_dependency_refs": [
                ref.as_dict() for ref in self.direct_dependency_refs
            ],
            "determinant_refs": [ref.as_dict() for ref in self.determinant_refs],
            "determinant_set_hash": self.determinant_set_hash,
            "replay_root_ref": self.replay_root_ref.as_dict(),
            "selection_scope_ref": self.selection_scope_ref.as_dict(),
            "build_or_release_receipt_refs": [
                ref.as_dict() for ref in self.build_or_release_receipt_refs
            ],
            "producer_permission_ceiling_ref": (
                self.producer_permission_ceiling_ref.as_dict()
            ),
            "producer_typed_state": self.producer_typed_state,
            "m2_authority_closure_ref": self.m2_authority_closure_ref.as_dict(),
            "m2_dependency_closure_ref": self.m2_dependency_closure_ref.as_dict(),
            "m2_determinant_closure_ref": self.m2_determinant_closure_ref.as_dict(),
            "m2_replay_closure_ref": self.m2_replay_closure_ref.as_dict(),
            "m2_explanation_closure_ref": self.m2_explanation_closure_ref.as_dict(),
        }


@dataclass(frozen=True)
class DirectProducerIngress:
    subject_ref: ExactRef
    producer_owner_ref: ExactRef
    producer_contract_ref: ExactRef
    typed_state: str
    determinant_refs: tuple[ExactRef, ...]
    replay_ref: ExactRef
    explanation_ref: ExactRef
    semantic_ceiling: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "subject_ref", _exact(self.subject_ref, "subject_ref"))
        object.__setattr__(
            self, "producer_owner_ref", _exact(self.producer_owner_ref, "producer_owner_ref")
        )
        object.__setattr__(
            self,
            "producer_contract_ref",
            _exact(self.producer_contract_ref, "producer_contract_ref"),
        )
        object.__setattr__(
            self, "determinant_refs", _refs(self.determinant_refs, "determinant_ref")
        )
        object.__setattr__(self, "replay_ref", _exact(self.replay_ref, "replay_ref"))
        object.__setattr__(
            self, "explanation_ref", _exact(self.explanation_ref, "explanation_ref")
        )
        if not str(self.typed_state).strip() or not str(self.semantic_ceiling).strip():
            raise LearnedWorldCompositionIntegrityError(
                "direct producer typed state and semantic ceiling are required"
            )


@dataclass(frozen=True)
class LearnedWorldCompositionReceipt:
    product_contract_ref: ExactRef
    route_taken: str
    terminal_state: str
    reason_code: str

    m01_execution_receipt_ref: ExactRef | None = None
    m01_object_graph_ref: ExactRef | None = None
    m1_input_bundle_ref: ExactRef | None = None
    m1_family_rule_binding_ref: ExactRef | None = None
    m1_disposition_ref: ExactRef | None = None

    m2_subject_ref: ExactRef | None = None
    m2_authority_closure_ref: ExactRef | None = None
    m2_dependency_closure_ref: ExactRef | None = None
    m2_determinant_closure_ref: ExactRef | None = None
    m2_replay_closure_ref: ExactRef | None = None
    m2_explanation_closure_ref: ExactRef | None = None
    m2_release_ref: ExactRef | None = None

    b5_lifecycle_subject_ref: ExactRef | None = None
    b5_event_refs: tuple[ExactRef, ...] = ()
    b5_selection_key_ref: ExactRef | None = None
    b5_selection_receipt_ref: ExactRef | None = None
    b5_replay_receipt_ref: ExactRef | None = None

    determinant_root_ref: ExactRef | None = None
    replay_root_ref: ExactRef | None = None
    explanation_root_ref: ExactRef | None = None

    conserved_state_material: Mapping[str, Any] = field(default_factory=dict)
    semantic_ceiling: str = "I4_COMPOSITION_ONLY"
    side_effects: Mapping[str, bool] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "product_contract_ref", _exact(self.product_contract_ref, "product_contract_ref")
        )
        object.__setattr__(self, "route_taken", str(self.route_taken).strip().upper())
        object.__setattr__(self, "terminal_state", str(self.terminal_state).strip())
        object.__setattr__(self, "reason_code", str(self.reason_code).strip())
        if not self.terminal_state or not self.reason_code:
            raise LearnedWorldCompositionIntegrityError(
                "composition receipt terminal state and reason code are required"
            )
        for name in (
            "m01_execution_receipt_ref",
            "m01_object_graph_ref",
            "m1_input_bundle_ref",
            "m1_family_rule_binding_ref",
            "m1_disposition_ref",
            "m2_subject_ref",
            "m2_authority_closure_ref",
            "m2_dependency_closure_ref",
            "m2_determinant_closure_ref",
            "m2_replay_closure_ref",
            "m2_explanation_closure_ref",
            "m2_release_ref",
            "b5_lifecycle_subject_ref",
            "b5_selection_key_ref",
            "b5_selection_receipt_ref",
            "b5_replay_receipt_ref",
            "determinant_root_ref",
            "replay_root_ref",
            "explanation_root_ref",
        ):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, _exact(value, name))
        object.__setattr__(self, "b5_event_refs", _refs(self.b5_event_refs, "b5_event_ref"))
        object.__setattr__(
            self, "conserved_state_material", _freeze_mapping(self.conserved_state_material)
        )
        effects = dict(self.side_effects)
        required = {
            "b5_registration_effect",
            "b5_publication_effect",
            "b5_current_selection_effect",
            *_ALWAYS_FALSE_EFFECTS.keys(),
        }
        if set(effects) != required or any(not isinstance(v, bool) for v in effects.values()):
            raise LearnedWorldCompositionIntegrityError(
                "composition receipt side-effect vocabulary is incomplete"
            )
        for key, value in _ALWAYS_FALSE_EFFECTS.items():
            if effects[key] is not value:
                raise LearnedWorldCompositionIntegrityError(
                    f"I4 may not assert {key}"
                )
        object.__setattr__(self, "side_effects", MappingProxyType(effects))
        object.__setattr__(self, "semantic_ceiling", str(self.semantic_ceiling).strip())

    def semantic_projection(self) -> Mapping[str, Any]:
        optional_names = (
            "m01_execution_receipt_ref",
            "m01_object_graph_ref",
            "m1_input_bundle_ref",
            "m1_family_rule_binding_ref",
            "m1_disposition_ref",
            "m2_subject_ref",
            "m2_authority_closure_ref",
            "m2_dependency_closure_ref",
            "m2_determinant_closure_ref",
            "m2_replay_closure_ref",
            "m2_explanation_closure_ref",
            "m2_release_ref",
            "b5_lifecycle_subject_ref",
            "b5_selection_key_ref",
            "b5_selection_receipt_ref",
            "b5_replay_receipt_ref",
            "determinant_root_ref",
            "replay_root_ref",
            "explanation_root_ref",
        )
        return {
            "schema": COMPOSITION_RECEIPT_SCHEMA,
            "runtime_id": COMPOSITION_RUNTIME_ID,
            "product_contract_ref": self.product_contract_ref.as_dict(),
            "route_taken": self.route_taken,
            "terminal_state": self.terminal_state,
            "reason_code": self.reason_code,
            **{
                name: _contract_ref_material(getattr(self, name))
                for name in optional_names
            },
            "b5_event_refs": [ref.as_dict() for ref in self.b5_event_refs],
            "conserved_state_material": self.conserved_state_material,
            "semantic_ceiling": self.semantic_ceiling,
            "side_effects": self.side_effects,
        }

    @property
    def ref(self) -> ExactRef:
        return _derived_ref(
            COMPOSITION_RECEIPT_SCHEMA,
            "composition-receipt",
            self.semantic_projection(),
        )

    def as_dict(self) -> Mapping[str, Any]:
        return {**self.semantic_projection(), "receipt_ref": self.ref.as_dict()}


@dataclass(frozen=True)
class LearnedWorldCompositionResult:
    receipt: LearnedWorldCompositionReceipt
    m1_input_bundle: M1AdjudicationInputBundle | None = None
    m1_disposition: LearnedEmpiricalDisposition | None = None
    m2_artifacts: M2ProductArtifacts | None = None
    b5_protocol_view: M2B5LifecycleProtocolView | None = None
    b5_subject: LearnedProductLifecycleSubject | None = None
    b5_selection_receipt: CurrentSelectionReceipt | None = None
    b5_replay_receipt: LifecycleReplayReceipt | None = None


def _effects_from_events(event_kinds: Iterable[str]) -> Mapping[str, bool]:
    kinds = set(event_kinds)
    return {
        "b5_registration_effect": "PRODUCT_REGISTERED" in kinds,
        "b5_publication_effect": "PRODUCT_PUBLISHED" in kinds,
        "b5_current_selection_effect": "CURRENT_SELECTED" in kinds,
        **dict(_ALWAYS_FALSE_EFFECTS),
    }


def _no_effects() -> Mapping[str, bool]:
    return _effects_from_events(())


def _validate_contract_for_b5(contract: LearnedWorldProductContractBinding) -> None:
    required = (
        ("product_family_ref", contract.product_family_ref),
        ("producer_owner_ref", contract.producer_owner_ref),
        ("producer_contract_ref", contract.producer_contract_ref),
        ("selection_scope_ref", contract.selection_scope_ref),
        ("producer_permission_ceiling_ref", contract.producer_permission_ceiling_ref),
        ("consumer_product_purpose_ref", contract.consumer_product_purpose_ref),
    )
    missing = [name for name, value in required if value is None]
    if missing:
        raise LearnedWorldCompositionBlocked(
            "missing exact product-contract field(s): " + ", ".join(missing)
        )
    if contract.semantic_subject_rule != SEMANTIC_SUBJECT_RULE:
        raise LearnedWorldCompositionBlocked("semantic subject rule is not the adopted exact rule")
    if contract.semantic_product_rule != SEMANTIC_PRODUCT_RULE:
        raise LearnedWorldCompositionBlocked("semantic product rule is not the adopted exact rule")
    if contract.semantic_projection_rule != SEMANTIC_PROJECTION_RULE:
        raise LearnedWorldCompositionBlocked(
            "semantic projection rule is not the adopted exact rule"
        )
    if contract.closure_construction_rule != CLOSURE_RULE:
        raise LearnedWorldCompositionBlocked(
            "closure construction rule is not the adopted exact rule"
        )
    if contract.lifecycle_policy != LIFECYCLE_POLICY:
        raise LearnedWorldCompositionBlocked(
            "lifecycle policy is not explicit-actions-only"
        )
    if contract.release_subject_kind != "TYPED_DISPOSITION":
        raise LearnedWorldCompositionBlocked(
            "M1 composition requires exact TYPED_DISPOSITION release subject kind"
        )
    if contract.producer_contract_ref != M1_DISPOSITION_PRODUCER_CONTRACT_REF:
        raise LearnedWorldCompositionBlocked(
            "producer contract does not exactly identify the current M1 disposition owner"
        )


def _validate_lifecycle_action_authority(
    contract: LearnedWorldProductContractBinding,
) -> None:
    actions = set(contract.lifecycle_actions)
    if "REGISTER" in actions:
        _exact(contract.registration_event_authority_ref, "registration_event_authority_ref")
        _exact(contract.registration_event_rule_ref, "registration_event_rule_ref")
    if "PUBLISH" in actions:
        _exact(contract.publication_event_authority_ref, "publication_event_authority_ref")
        _exact(contract.publication_event_rule_ref, "publication_event_rule_ref")
    if "SELECT_CURRENT" in actions:
        _exact(contract.selection_purpose_ref, "selection_purpose_ref")
        _exact(contract.selection_event_authority_ref, "selection_event_authority_ref")
        _exact(contract.selection_event_rule_ref, "selection_event_rule_ref")
        _exact(contract.selection_attestation_ref, "selection_attestation_ref")


def _m01_execution_ref(result: RouteBProductionResult) -> ExactRef:
    if not isinstance(result, RouteBProductionResult):
        raise LearnedWorldCompositionIntegrityError(
            "M01 route requires exact RouteBProductionResult"
        )
    identity = result.replay_receipt.get("receipt_identity")
    if not isinstance(identity, str) or len(identity) != 64:
        raise LearnedWorldCompositionIntegrityError(
            "M01 replay receipt identity is unavailable"
        )
    return ExactRef(
        "PYAT_M01_ROUTE_B_EXECUTION_REPLAY_RECEIPT@1.0.0",
        f"urn:rawlsing:pre553:m01:replay-receipt:sha256:{identity}",
        identity,
    )


def _m01_graph_ref(result: RouteBProductionResult) -> ExactRef:
    graph = result.object_graph
    material = {
        "authority_snapshot_refs": [obj.ref.as_dict() for obj in graph.authority_snapshots],
        "executed_predicate_refs": [obj.ref.as_dict() for obj in graph.executed_predicates],
        "executed_query_refs": [obj.ref.as_dict() for obj in graph.executed_queries],
        "empirical_fact_refs": [obj.ref.as_dict() for obj in graph.empirical_facts],
        "discovery_authority_refs": [obj.ref.as_dict() for obj in graph.discovery_authorities],
        "discovery_receipt_refs": [obj.ref.as_dict() for obj in graph.discovery_receipts],
    }
    return _derived_ref("I4M01ExactObjectGraph", "m01-object-graph", material)


def build_m1_bundle_from_m01(
    result: RouteBProductionResult,
    *,
    contract: LearnedWorldProductContractBinding,
    family_rule_binding: M1FamilyRuleBinding | None,
    selected_discovery_receipt_refs: Iterable[ExactRef],
    requested_scope: Mapping[str, Any],
    additional_authority_snapshots: Iterable[Any] = (),
    prerequisite_channels: Iterable[M1PrerequisiteChannel] = (),
    additional_dependency_refs: Iterable[ExactRef] = (),
) -> M1AdjudicationInputBundle:
    """Adapt one exact M01 graph to M1 without choosing a family rule."""
    if contract.route != "M01_M1_M2_B5":
        raise LearnedWorldCompositionBlocked("M01 adapter invoked for the wrong route")
    if family_rule_binding is None:
        raise LearnedWorldCompositionBlocked(
            "M01 evidence cannot self-select an M1 family rule"
        )
    if contract.m1_family_rule_binding_ref is None:
        raise LearnedWorldCompositionBlocked(
            "product contract omits exact M1 family-rule binding ref"
        )
    if family_rule_binding.ref != contract.m1_family_rule_binding_ref:
        raise LearnedWorldCompositionBlocked(
            "supplied M1 family-rule binding differs from exact product contract"
        )
    selected_refs = _refs(
        selected_discovery_receipt_refs, "selected_discovery_receipt_ref"
    )
    if not selected_refs:
        raise LearnedWorldCompositionBlocked(
            "M01->M1 requires explicit selected discovery receipt refs"
        )
    by_ref = {obj.ref.key: obj for obj in result.object_graph.discovery_receipts}
    selected = []
    for ref in selected_refs:
        receipt = by_ref.get(ref.key)
        if receipt is None:
            raise LearnedWorldCompositionIntegrityError(
                "selected discovery receipt is absent from exact M01 graph"
            )
        selected.append(receipt)

    authorities = (
        *result.object_graph.authority_snapshots,
        *tuple(additional_authority_snapshots),
    )
    exact_additional_dependencies = _refs(
        additional_dependency_refs, "additional_dependency_ref"
    )
    return build_m1_adjudication_input_bundle(
        requested_claim_family_id=family_rule_binding.claim_family_id,
        requested_claim_rule_id=family_rule_binding.claim_rule_id,
        selected_discovery_receipts=tuple(selected),
        discovery_authority_catalog=result.object_graph.discovery_authorities,
        empirical_fact_catalog=result.object_graph.empirical_facts,
        empirical_query_catalog=result.object_graph.executed_queries,
        empirical_predicate_catalog=result.object_graph.executed_predicates,
        authority_snapshots=authorities,
        requested_scope=requested_scope,
        prerequisite_channels=tuple(prerequisite_channels),
        additional_dependency_refs=(
            result.c11_release.release_ref,
            *exact_additional_dependencies,
        ),
    )


def adapt_m1_disposition_to_m2(
    disposition: LearnedEmpiricalDisposition,
    *,
    contract: LearnedWorldProductContractBinding,
    repository: M2Repository,
) -> M2ProductArtifacts:
    """Losslessly bind one M1 disposition into M2 producer/release objects."""
    _validate_contract_for_b5(contract)
    if not isinstance(disposition, LearnedEmpiricalDisposition):
        raise LearnedWorldCompositionIntegrityError(
            "M1->M2 adapter requires LearnedEmpiricalDisposition"
        )
    verify_m1_disposition_replay(disposition)

    authority_transports = tuple(
        authority_transport_ref(ref) for ref in disposition.authority_closure_refs
    )
    subject = register_producer_subject(
        repository,
        subject_ref=disposition.ref,
        subject_kind=contract.release_subject_kind,
        producer_contract_ref=contract.producer_contract_ref,
        typed_state=disposition.adjudication_outcome,
        semantic_anatomy_ref=disposition.ref,
        required_authority_refs=authority_transports,
        required_dependency_refs=disposition.dependency_refs,
        required_determinant_refs=(disposition.determinant_manifest_ref,),
        required_replay_refs=(disposition.replay_ref,),
        required_explanation_refs=(
            disposition.explanation_ref,
            disposition.determinant_explanation_receipt_ref,
        ),
    )
    if subject.ref != disposition.ref:
        raise LearnedWorldCompositionIntegrityError("M1 disposition ref changed in M2")
    if subject.typed_state != disposition.adjudication_outcome:
        raise LearnedWorldCompositionIntegrityError("M1 typed state changed in M2")

    authority = constitute_closure(
        repository,
        closure_kind="AUTHORITY",
        member_refs=(contract.producer_contract_ref, *authority_transports),
        metadata={
            "transport_schema": AUTHORITY_TRANSPORT_SCHEMA,
            "authority_ref_preimages": [
                ref.as_dict() for ref in disposition.authority_closure_refs
            ],
            "semantic_reownership": False,
        },
    )
    dependency = constitute_closure(
        repository,
        closure_kind="DEPENDENCY",
        member_refs=disposition.dependency_refs,
    )
    determinant = constitute_closure(
        repository,
        closure_kind="DETERMINANT",
        member_refs=(disposition.determinant_manifest_ref,),
    )
    replay = constitute_closure(
        repository,
        closure_kind="REPLAY_RECONSTRUCTION",
        member_refs=(disposition.replay_ref,),
        metadata={
            "replay_grade": "HISTORICAL_EXPLANATION_ONLY",
            "m1_replay_verified": True,
        },
    )
    explanation = constitute_closure(
        repository,
        closure_kind="EXPLANATION_LINEAGE",
        member_refs=(
            disposition.ref,
            contract.producer_contract_ref,
            disposition.explanation_ref,
            disposition.determinant_explanation_receipt_ref,
        ),
    )
    release = constitute_release(
        repository,
        release_subject_ref=subject.ref,
        release_subject_kind=contract.release_subject_kind,
        semantic_producer_contract_ref=contract.producer_contract_ref,
        authority_closure_ref=authority.ref,
        dependency_closure_ref=dependency.ref,
        determinant_closure_ref=determinant.ref,
        replay_reconstruction_ref=replay.ref,
        explanation_lineage_ref=explanation.ref,
    )
    return M2ProductArtifacts(
        subject=subject,
        authority_closure=authority,
        dependency_closure=dependency,
        determinant_closure=determinant,
        replay_closure=replay,
        explanation_closure=explanation,
        release=release,
    )


def _restore_authority_refs(closure: ClosureObject) -> tuple[AuthorityRef, ...]:
    raw = closure.metadata.get("authority_ref_preimages")
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)) or not raw:
        raise LearnedWorldCompositionIntegrityError(
            "M2 authority closure lacks exact authority preimages"
        )
    authorities = tuple(_authority_from_mapping(row) for row in raw)
    transports = tuple(authority_transport_ref(ref) for ref in authorities)
    member_keys = {ref.key for ref in closure.member_refs}
    for transport in transports:
        if transport.key not in member_keys:
            raise LearnedWorldCompositionIntegrityError(
                "M2 authority transport/preimage conservation failure"
            )
    return tuple(sorted(set(authorities), key=lambda ref: ref.key))


def adapt_m2_release_to_b5(
    artifacts: M2ProductArtifacts,
    *,
    contract: LearnedWorldProductContractBinding,
) -> M2B5LifecycleProtocolView:
    """Construct the thinnest exact B5 protocol view from M2 + contract."""
    _validate_contract_for_b5(contract)
    release = artifacts.release
    subject = artifacts.subject
    if release.release_subject_ref != subject.ref:
        raise LearnedWorldCompositionIntegrityError("M2 release subject ref drift")
    if release.release_subject_kind != subject.subject_kind:
        raise LearnedWorldCompositionIntegrityError("M2 release subject kind drift")
    if release.semantic_producer_contract_ref != subject.producer_contract_ref:
        raise LearnedWorldCompositionIntegrityError("M2 producer ownership drift")
    expected_closures = {
        "authority_closure_ref": artifacts.authority_closure.ref,
        "dependency_closure_ref": artifacts.dependency_closure.ref,
        "determinant_closure_ref": artifacts.determinant_closure.ref,
        "replay_reconstruction_ref": artifacts.replay_closure.ref,
        "explanation_lineage_ref": artifacts.explanation_closure.ref,
    }
    for name, expected in expected_closures.items():
        if getattr(release, name) != expected:
            raise LearnedWorldCompositionIntegrityError(
                f"M2 release {name} does not match exact closure preimage"
            )

    authorities = _restore_authority_refs(artifacts.authority_closure)
    determinant_refs = artifacts.determinant_closure.member_refs
    if not determinant_refs:
        raise LearnedWorldCompositionIntegrityError(
            "M2 determinant closure must not be empty"
        )
    replay_members = artifacts.replay_closure.member_refs
    if len(replay_members) != 1:
        raise LearnedWorldCompositionIntegrityError(
            "M1-derived replay closure must carry exactly one replay root"
        )
    determinant_set_hash = semantic_hash(
        [ref.as_dict() for ref in determinant_refs]
    )
    return M2B5LifecycleProtocolView(
        release_ref=release.ref,
        product_ref=subject.ref,
        product_family_ref=_exact(contract.product_family_ref, "product_family_ref"),
        producer_owner_ref=_exact(contract.producer_owner_ref, "producer_owner_ref"),
        producer_contract_ref=subject.producer_contract_ref,
        semantic_projection_hash=subject.semantic_anatomy_ref.content_hash,
        authority_snapshot_refs=authorities,
        direct_dependency_refs=artifacts.dependency_closure.member_refs,
        determinant_refs=determinant_refs,
        determinant_set_hash=determinant_set_hash,
        replay_root_ref=replay_members[0],
        selection_scope_ref=_exact(contract.selection_scope_ref, "selection_scope_ref"),
        build_or_release_receipt_refs=(release.ref,),
        producer_permission_ceiling_ref=_exact(
            contract.producer_permission_ceiling_ref,
            "producer_permission_ceiling_ref",
        ),
        producer_typed_state=subject.typed_state,
        m2_authority_closure_ref=artifacts.authority_closure.ref,
        m2_dependency_closure_ref=artifacts.dependency_closure.ref,
        m2_determinant_closure_ref=artifacts.determinant_closure.ref,
        m2_replay_closure_ref=artifacts.replay_closure.ref,
        m2_explanation_closure_ref=artifacts.explanation_closure.ref,
    )


def _state_material(disposition: LearnedEmpiricalDisposition) -> Mapping[str, Any]:
    return {
        "disposition_class": disposition.disposition_class,
        "adjudication_outcome": disposition.adjudication_outcome,
        "rule_outcome": disposition.rule_outcome,
        "reason_code": disposition.reason_code,
        "semantic_assertion_polarity_or_state": (
            disposition.semantic_assertion_polarity_or_state
        ),
        "conserved_empirical_states": disposition.conserved_empirical_states,
        "conserved_authority_states": disposition.conserved_authority_states,
        "required_prerequisite_channel_states": (
            disposition.required_prerequisite_channel_states
        ),
        "support_uncertainty_state": disposition.support_uncertainty_state,
    }


def _receipt_from_parts(
    *,
    contract: LearnedWorldProductContractBinding,
    terminal_state: str,
    reason_code: str,
    m01_result: RouteBProductionResult | None = None,
    bundle: M1AdjudicationInputBundle | None = None,
    binding: M1FamilyRuleBinding | None = None,
    disposition: LearnedEmpiricalDisposition | None = None,
    artifacts: M2ProductArtifacts | None = None,
    b5_subject: LearnedProductLifecycleSubject | None = None,
    b5_event_refs: Iterable[ExactRef] = (),
    b5_event_kinds: Iterable[str] = (),
    selection_key_ref: ExactRef | None = None,
    selection_receipt: CurrentSelectionReceipt | None = None,
    b5_replay_receipt: LifecycleReplayReceipt | None = None,
) -> LearnedWorldCompositionReceipt:
    return LearnedWorldCompositionReceipt(
        product_contract_ref=contract.ref,
        route_taken=contract.route,
        terminal_state=terminal_state,
        reason_code=reason_code,
        m01_execution_receipt_ref=(
            None if m01_result is None else _m01_execution_ref(m01_result)
        ),
        m01_object_graph_ref=(
            None if m01_result is None else _m01_graph_ref(m01_result)
        ),
        m1_input_bundle_ref=None if bundle is None else bundle.ref,
        m1_family_rule_binding_ref=None if binding is None else binding.ref,
        m1_disposition_ref=None if disposition is None else disposition.ref,
        m2_subject_ref=None if artifacts is None else artifacts.subject.ref,
        m2_authority_closure_ref=(
            None if artifacts is None else artifacts.authority_closure.ref
        ),
        m2_dependency_closure_ref=(
            None if artifacts is None else artifacts.dependency_closure.ref
        ),
        m2_determinant_closure_ref=(
            None if artifacts is None else artifacts.determinant_closure.ref
        ),
        m2_replay_closure_ref=(
            None if artifacts is None else artifacts.replay_closure.ref
        ),
        m2_explanation_closure_ref=(
            None if artifacts is None else artifacts.explanation_closure.ref
        ),
        m2_release_ref=None if artifacts is None else artifacts.release.ref,
        b5_lifecycle_subject_ref=(
            None if b5_subject is None else b5_subject.release_ref
        ),
        b5_event_refs=tuple(b5_event_refs),
        b5_selection_key_ref=selection_key_ref,
        b5_selection_receipt_ref=(
            None if selection_receipt is None else selection_receipt.ref
        ),
        b5_replay_receipt_ref=(
            None if b5_replay_receipt is None else b5_replay_receipt.ref
        ),
        determinant_root_ref=(
            None if disposition is None else disposition.determinant_manifest_ref
        ),
        replay_root_ref=None if disposition is None else disposition.replay_ref,
        explanation_root_ref=(
            None if disposition is None else disposition.explanation_ref
        ),
        conserved_state_material=(
            {} if disposition is None else _state_material(disposition)
        ),
        semantic_ceiling=(
            "I4_COMPOSITION_ONLY"
            if disposition is None
            else disposition.semantic_ceiling
        ),
        side_effects=_effects_from_events(b5_event_kinds),
    )


def compose_learned_world(
    contract: LearnedWorldProductContractBinding,
    *,
    m2_repository: M2Repository,
    lifecycle_executor: LearnedProductLifecycleExecutor,
    m01_result: RouteBProductionResult | None = None,
    selected_discovery_receipt_refs: Iterable[ExactRef] = (),
    requested_scope: Mapping[str, Any] | None = None,
    m1_family_rule_binding: M1FamilyRuleBinding | None = None,
    validator_registry: M1ValidatorRegistry | None = None,
    m1_authority_snapshots: Iterable[Any] = (),
    prerequisite_channels: Iterable[M1PrerequisiteChannel] = (),
    additional_dependency_refs: Iterable[ExactRef] = (),
    m1_disposition: LearnedEmpiricalDisposition | None = None,
) -> LearnedWorldCompositionResult:
    """Compose the exact existing owners.  Never changes route on missing input."""
    if not isinstance(contract, LearnedWorldProductContractBinding):
        raise LearnedWorldCompositionIntegrityError(
            "exact LearnedWorldProductContractBinding required"
        )
    if not isinstance(m2_repository, M2Repository):
        raise LearnedWorldCompositionIntegrityError("exact M2Repository required")
    if not isinstance(lifecycle_executor, LearnedProductLifecycleExecutor):
        raise LearnedWorldCompositionIntegrityError(
            "exact LearnedProductLifecycleExecutor required"
        )
    exact_additional_dependencies = _refs(
        additional_dependency_refs, "additional_dependency_ref"
    )
    if contract.route != "M01_M1_M2_B5" and exact_additional_dependencies:
        raise LearnedWorldCompositionBlocked(
            "additional dependency refs may only enter through exact M01->M1 input construction"
        )
    if contract.route == "DIRECT_PRODUCER":
        receipt = _receipt_from_parts(
            contract=contract,
            terminal_state="BLOCKED",
            reason_code="DIRECT_ROUTE_REQUIRES_EXPLICIT_DIRECT_PRODUCER_INGRESS",
        )
        return LearnedWorldCompositionResult(receipt=receipt)

    bundle: M1AdjudicationInputBundle | None = None
    disposition = m1_disposition
    artifacts: M2ProductArtifacts | None = None
    protocol: M2B5LifecycleProtocolView | None = None
    b5_subject: LearnedProductLifecycleSubject | None = None
    selection_receipt: CurrentSelectionReceipt | None = None
    replay_receipt: LifecycleReplayReceipt | None = None
    selection_key_ref: ExactRef | None = None
    initial_event_count = len(lifecycle_executor.events)

    try:
        _validate_contract_for_b5(contract)
        _validate_lifecycle_action_authority(contract)

        if contract.route == "M01_M1_M2_B5":
            if m01_result is None:
                raise LearnedWorldCompositionBlocked(
                    "M01_M1_M2_B5 route requires exact M01 result"
                )
            if validator_registry is None:
                raise LearnedWorldCompositionBlocked(
                    "M01_M1_M2_B5 route requires exact M1 validator registry"
                )
            bundle = build_m1_bundle_from_m01(
                m01_result,
                contract=contract,
                family_rule_binding=m1_family_rule_binding,
                selected_discovery_receipt_refs=selected_discovery_receipt_refs,
                requested_scope=requested_scope or {},
                additional_authority_snapshots=m1_authority_snapshots,
                prerequisite_channels=prerequisite_channels,
                additional_dependency_refs=exact_additional_dependencies,
            )
            disposition = adjudicate_learned_empirical(
                bundle,
                m1_family_rule_binding,
                validator_registry=validator_registry,
            )
        elif contract.route == "M1_M2_B5":
            if disposition is None:
                raise LearnedWorldCompositionBlocked(
                    "M1_M2_B5 route requires exact M1 disposition"
                )
            if m01_result is not None:
                raise LearnedWorldCompositionBlocked(
                    "M1_M2_B5 route may not silently consume M01 evidence"
                )

        if disposition is None:
            raise LearnedWorldCompositionBlocked("exact M1 disposition is unavailable")

        artifacts = adapt_m1_disposition_to_m2(
            disposition,
            contract=contract,
            repository=m2_repository,
        )
        protocol = adapt_m2_release_to_b5(artifacts, contract=contract)
        b5_subject = LearnedProductLifecycleSubject.from_protocol(protocol)

        # No staging, registration, publication, or selection occurs by default.
        if contract.lifecycle_actions:
            lifecycle_executor.stage_release(b5_subject)

        if "REGISTER" in contract.lifecycle_actions:
            lifecycle_executor.register_product(
                b5_subject.release_ref,
                event_authority_ref=_exact(
                    contract.registration_event_authority_ref,
                    "registration_event_authority_ref",
                ),
                event_rule_ref=_exact(
                    contract.registration_event_rule_ref,
                    "registration_event_rule_ref",
                ),
                evidence_refs=contract.registration_evidence_refs,
            )
        if "PUBLISH" in contract.lifecycle_actions:
            lifecycle_executor.publish_product(
                b5_subject.release_ref,
                event_authority_ref=_exact(
                    contract.publication_event_authority_ref,
                    "publication_event_authority_ref",
                ),
                event_rule_ref=_exact(
                    contract.publication_event_rule_ref,
                    "publication_event_rule_ref",
                ),
                evidence_refs=contract.publication_evidence_refs,
            )
        if "SELECT_CURRENT" in contract.lifecycle_actions:
            key = lifecycle_executor.selection_key(
                product_family_ref=_exact(contract.product_family_ref, "product_family_ref"),
                selection_scope_ref=_exact(contract.selection_scope_ref, "selection_scope_ref"),
                selection_purpose_ref=_exact(
                    contract.selection_purpose_ref, "selection_purpose_ref"
                ),
                consumer_context_partition_ref=contract.consumer_context_partition_ref,
            )
            selection_key_ref = key.ref
            selection_receipt = lifecycle_executor.select_current(
                key.ref,
                b5_subject.release_ref,
                expected_previous_receipt_ref=(
                    contract.expected_previous_selection_receipt_ref
                ),
                event_authority_ref=_exact(
                    contract.selection_event_authority_ref,
                    "selection_event_authority_ref",
                ),
                event_rule_ref=_exact(
                    contract.selection_event_rule_ref,
                    "selection_event_rule_ref",
                ),
                selection_attestation_ref=_exact(
                    contract.selection_attestation_ref,
                    "selection_attestation_ref",
                ),
                evidence_refs=contract.selection_evidence_refs,
            )

        new_events = lifecycle_executor.events[initial_event_count:]
        if contract.lifecycle_actions:
            replay_receipt = lifecycle_executor.audit_replay()
        receipt = _receipt_from_parts(
            contract=contract,
            terminal_state=disposition.adjudication_outcome,
            reason_code=disposition.reason_code,
            m01_result=m01_result if contract.route == "M01_M1_M2_B5" else None,
            bundle=bundle,
            binding=m1_family_rule_binding,
            disposition=disposition,
            artifacts=artifacts,
            b5_subject=b5_subject,
            b5_event_refs=(event.ref for event in new_events),
            b5_event_kinds=(event.event_kind for event in new_events),
            selection_key_ref=selection_key_ref,
            selection_receipt=selection_receipt,
            b5_replay_receipt=replay_receipt,
        )
        return LearnedWorldCompositionResult(
            receipt=receipt,
            m1_input_bundle=bundle,
            m1_disposition=disposition,
            m2_artifacts=artifacts,
            b5_protocol_view=protocol,
            b5_subject=b5_subject,
            b5_selection_receipt=selection_receipt,
            b5_replay_receipt=replay_receipt,
        )
    except (
        LearnedWorldCompositionError,
        M2ReleaseError,
        LearnedProductLifecycleError,
    ) as exc:
        new_events = lifecycle_executor.events[initial_event_count:]
        reason = (
            type(exc).__name__.upper()
            if not isinstance(exc, LearnedWorldCompositionBlocked)
            else "I4_REQUIRED_PREMISE_BLOCKED"
        )
        receipt = _receipt_from_parts(
            contract=contract,
            terminal_state="BLOCKED",
            reason_code=reason,
            m01_result=m01_result if contract.route == "M01_M1_M2_B5" else None,
            bundle=bundle,
            binding=m1_family_rule_binding,
            disposition=disposition,
            artifacts=artifacts,
            b5_subject=b5_subject,
            b5_event_refs=(event.ref for event in new_events),
            b5_event_kinds=(event.event_kind for event in new_events),
            selection_key_ref=selection_key_ref,
            selection_receipt=selection_receipt,
            b5_replay_receipt=replay_receipt,
        )
        return LearnedWorldCompositionResult(
            receipt=receipt,
            m1_input_bundle=bundle,
            m1_disposition=disposition,
            m2_artifacts=artifacts,
            b5_protocol_view=protocol,
            b5_subject=b5_subject,
            b5_selection_receipt=selection_receipt,
            b5_replay_receipt=replay_receipt,
        )


def compose_direct_producer(
    contract: LearnedWorldProductContractBinding,
    ingress: DirectProducerIngress,
) -> LearnedWorldCompositionResult:
    """Record an explicitly authorized direct consumer route; never infer it."""
    if contract.route != "DIRECT_PRODUCER":
        receipt = _receipt_from_parts(
            contract=contract,
            terminal_state="BLOCKED",
            reason_code="DIRECT_ROUTE_NOT_EXPLICITLY_SELECTED",
        )
        return LearnedWorldCompositionResult(receipt=receipt)
    try:
        if contract.lifecycle_actions:
            raise LearnedWorldCompositionBlocked(
                "direct-producer route cannot smuggle B5 lifecycle actions"
            )
        _exact(
            contract.direct_producer_route_authority_ref,
            "direct_producer_route_authority_ref",
        )
        _exact(
            contract.direct_consumer_acceptance_ref,
            "direct_consumer_acceptance_ref",
        )
        if contract.producer_owner_ref != ingress.producer_owner_ref:
            raise LearnedWorldCompositionBlocked(
                "direct producer owner differs from exact product contract"
            )
        if contract.producer_contract_ref != ingress.producer_contract_ref:
            raise LearnedWorldCompositionBlocked(
                "direct producer contract differs from exact product contract"
            )
        state_material = {
            "direct_subject_ref": ingress.subject_ref.as_dict(),
            "typed_state": ingress.typed_state,
            "determinant_refs": [ref.as_dict() for ref in ingress.determinant_refs],
            "replay_ref": ingress.replay_ref.as_dict(),
            "explanation_ref": ingress.explanation_ref.as_dict(),
            "direct_route_authority_ref": (
                contract.direct_producer_route_authority_ref.as_dict()
            ),
            "direct_consumer_acceptance_ref": (
                contract.direct_consumer_acceptance_ref.as_dict()
            ),
        }
        receipt = LearnedWorldCompositionReceipt(
            product_contract_ref=contract.ref,
            route_taken=contract.route,
            terminal_state=ingress.typed_state,
            reason_code="DIRECT_PRODUCER_ROUTE_EXACTLY_AUTHORIZED",
            determinant_root_ref=(
                ingress.determinant_refs[0] if len(ingress.determinant_refs) == 1 else
                _derived_ref(
                    "I4DirectDeterminantSet",
                    "direct-determinant-set",
                    [ref.as_dict() for ref in ingress.determinant_refs],
                )
            ),
            replay_root_ref=ingress.replay_ref,
            explanation_root_ref=ingress.explanation_ref,
            conserved_state_material=state_material,
            semantic_ceiling=ingress.semantic_ceiling,
            side_effects=_no_effects(),
        )
        return LearnedWorldCompositionResult(receipt=receipt)
    except LearnedWorldCompositionError:
        receipt = _receipt_from_parts(
            contract=contract,
            terminal_state="BLOCKED",
            reason_code="DIRECT_ROUTE_AUTHORITY_OR_GRAIN_BLOCKED",
        )
        return LearnedWorldCompositionResult(receipt=receipt)


__all__ = [
    "PRODUCT_CONTRACT_SCHEMA",
    "COMPOSITION_RECEIPT_SCHEMA",
    "COMPOSITION_RUNTIME_ID",
    "NO_LIFECYCLE_SIDE_EFFECT",
    "M1_DISPOSITION_PRODUCER_CONTRACT_REF",
    "LearnedWorldCompositionError",
    "LearnedWorldCompositionBlocked",
    "LearnedWorldCompositionIntegrityError",
    "LearnedWorldProductContractBinding",
    "M2ProductArtifacts",
    "M2B5LifecycleProtocolView",
    "DirectProducerIngress",
    "LearnedWorldCompositionReceipt",
    "LearnedWorldCompositionResult",
    "authority_transport_ref",
    "build_m1_bundle_from_m01",
    "adapt_m1_disposition_to_m2",
    "adapt_m2_release_to_b5",
    "compose_learned_world",
    "compose_direct_producer",
    "LEARNED_CONSUMER_CONTRACT_ID",
    "LEARNED_CONSUMER_SCHEMA",
    "LearnedWorldConsumerError",
    "LearnedWorldConsumerResult",
    "NativeProductGraph",
    "evaluate_learned_world_consumer",
]


LEARNED_CONSUMER_CONTRACT_ID = "R91_LEARNED_WORLD_POSSIBILITY_CONSUMER@1.0.0"
LEARNED_CONSUMER_SCHEMA = "R91_LEARNED_WORLD_CONSUMER_RESULT@1"


class LearnedWorldConsumerError(LearnedWorldCompositionError):
    """Typed learned-product consumer refusal; no new geometry is invented."""


@dataclass(frozen=True)
class NativeProductGraph:
    """Actual native product/components consumed by the learned consumer."""

    compositions: tuple[AnalyticalCompositionResult, ...]
    extension_result: Any | None = None

    def __post_init__(self) -> None:
        comps = tuple(self.compositions)
        if not comps:
            raise LearnedWorldConsumerError("native product graph requires a composition")
        if any(not isinstance(item, AnalyticalCompositionResult) for item in comps):
            raise LearnedWorldConsumerError("native product graph components must be compositions")
        object.__setattr__(self, "compositions", comps)


@dataclass(frozen=True)
class LearnedWorldConsumerResult:
    contract_id: str
    state: str
    reason_code: str
    learned_receipt_ref: ExactRef
    product_contract_ref: ExactRef
    m1_disposition_ref: ExactRef | None
    m2_release_ref: ExactRef | None
    b5_selection_receipt_ref: ExactRef | None
    evidence_ref: ExactRef | None
    producer_query_ref: ExactRef | None
    producer_predicate_ref: ExactRef | None
    consumer_query_ref: ExactRef | None
    consumer_result: PositionedSubjectPossibilityResult | None
    consumer_values_read: Mapping[str, Any] | None
    eligibility_state: str = "UNKNOWN"
    execution_state: str = "NOT_STARTED"
    result_state: str = "UNKNOWN"
    denominator: int | None = None
    cells: tuple[Mapping[str, Any], ...] = ()
    producer_route: str | None = None
    joint_component_count: int | None = None
    joint_order_semantics: str | None = None
    discovery_receipt_refs: tuple[ExactRef, ...] = ()
    discovery_frontier_ref: ExactRef | None = None
    recursive_handoff_refs: tuple[ExactRef, ...] = ()
    recursive_lineage_refs: tuple[ExactRef, ...] = ()
    z_unresolved: bool = False

    def material(self) -> Mapping[str, Any]:
        return {
            "schema": LEARNED_CONSUMER_SCHEMA,
            "contract_id": self.contract_id,
            "state": self.state,
            "reason_code": self.reason_code,
            "learned_receipt_ref": self.learned_receipt_ref.as_dict(),
            "product_contract_ref": self.product_contract_ref.as_dict(),
            "m1_disposition_ref": None
            if self.m1_disposition_ref is None
            else self.m1_disposition_ref.as_dict(),
            "m2_release_ref": None
            if self.m2_release_ref is None
            else self.m2_release_ref.as_dict(),
            "b5_selection_receipt_ref": None
            if self.b5_selection_receipt_ref is None
            else self.b5_selection_receipt_ref.as_dict(),
            "evidence_ref": None
            if self.evidence_ref is None
            else self.evidence_ref.as_dict(),
            "producer_query_ref": None
            if self.producer_query_ref is None
            else self.producer_query_ref.as_dict(),
            "producer_predicate_ref": None
            if self.producer_predicate_ref is None
            else self.producer_predicate_ref.as_dict(),
            "consumer_query_ref": None
            if self.consumer_query_ref is None
            else self.consumer_query_ref.as_dict(),
            "consumer_result_state": None
            if self.consumer_result is None
            else self.consumer_result.result_state,
            "consumer_result_hash": None
            if self.consumer_result is None
            else self.consumer_result.result_hash,
            "consumer_values_read": self.consumer_values_read,
            "eligibility_state": self.eligibility_state,
            "execution_state": self.execution_state,
            "result_state": self.result_state,
            "denominator": self.denominator,
            "cells": [canonicalize(cell) for cell in self.cells],
            "producer_route": self.producer_route,
            "joint_component_count": self.joint_component_count,
            "joint_order_semantics": self.joint_order_semantics,
            "discovery_receipt_refs": [x.as_dict() for x in self.discovery_receipt_refs],
            "discovery_frontier_ref": None if self.discovery_frontier_ref is None else self.discovery_frontier_ref.as_dict(),
            "recursive_handoff_refs": [x.as_dict() for x in self.recursive_handoff_refs],
            "recursive_lineage_refs": [x.as_dict() for x in self.recursive_lineage_refs],
            "z_unresolved": self.z_unresolved,
        }

    @property
    def result_hash(self) -> str:
        return semantic_hash(self.material())


def _learned_refusal(
    *,
    learned: LearnedWorldCompositionResult,
    reason: str,
    disposition: LearnedEmpiricalDisposition | None = None,
    evidence: PossibilitySliceEvidence | None = None,
    producer_query_ref: ExactRef | None = None,
    producer_predicate_ref: ExactRef | None = None,
) -> LearnedWorldConsumerResult:
    return LearnedWorldConsumerResult(
        contract_id=LEARNED_CONSUMER_CONTRACT_ID,
        state="REFUSED",
        reason_code=reason,
        learned_receipt_ref=learned.receipt.ref,
        product_contract_ref=learned.receipt.product_contract_ref,
        m1_disposition_ref=None if disposition is None else disposition.ref,
        m2_release_ref=None
        if learned.m2_artifacts is None
        else learned.m2_artifacts.release.ref,
        b5_selection_receipt_ref=None
        if learned.b5_selection_receipt is None
        else learned.b5_selection_receipt.ref,
        evidence_ref=None if evidence is None else evidence.evidence_ref,
        producer_query_ref=producer_query_ref,
        producer_predicate_ref=producer_predicate_ref,
        consumer_query_ref=None,
        consumer_result=None,
        consumer_values_read=None,
    )




@dataclass(frozen=True)
class NativeGraphSlot:
    slot_id: str
    source_universe_ref: ExactRef
    release_ref: ExactRef
    producer_query_ref: ExactRef
    producer_predicate_ref: ExactRef
    consumer_query_ref: ExactRef
    model_rule_hash: str
    producer_route: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "slot_id", str(self.slot_id).strip())
        if not self.slot_id:
            raise LearnedWorldConsumerError("graph slot id is required")
        for name in (
            "source_universe_ref", "release_ref", "producer_query_ref",
            "producer_predicate_ref", "consumer_query_ref",
        ):
            object.__setattr__(self, name, _exact(getattr(self, name), name))
        if len(str(self.model_rule_hash)) != 64:
            raise LearnedWorldConsumerError("slot model_rule_hash must be sha256")
        if not str(self.producer_route).strip():
            raise LearnedWorldConsumerError("slot producer route is required")


@dataclass(frozen=True)
class NativeGraphExecutionRequest:
    slots: tuple[NativeGraphSlot, ...]

    def __post_init__(self) -> None:
        slots = tuple(self.slots)
        if not slots:
            raise LearnedWorldConsumerError("graph request requires admitted slots")
        if len({slot.slot_id for slot in slots}) != len(slots):
            raise LearnedWorldConsumerError("graph slot ids must be unique")
        object.__setattr__(self, "slots", slots)


@dataclass(frozen=True)
class BoundNativeProductGraph:
    original_ref: ExactRef
    view: NativeProductGraph
    projection_hash: str


class TrustedNativeGraphCoordinator:
    """Local trusted coordinator holding actual executed originals separately."""

    def __init__(
        self,
        executors: Mapping[str, Callable[[NativeGraphSlot], AnalyticalCompositionResult]],
    ) -> None:
        self._executors = dict(executors)
        self._originals: dict[str, tuple[Mapping[str, Any], tuple[AnalyticalCompositionResult, ...]]] = {}

    def execute(self, request: NativeGraphExecutionRequest) -> BoundNativeProductGraph:
        components = []
        for slot in request.slots:
            executor = self._executors.get(slot.slot_id)
            if executor is None:
                raise LearnedWorldConsumerError(f"no trusted executor for slot {slot.slot_id!r}")
            component = executor(slot)
            if not isinstance(component, AnalyticalCompositionResult):
                raise LearnedWorldConsumerError("trusted executor did not return a native composition")
            if (
                component.producer_query_ref != slot.producer_query_ref
                or component.producer_predicate_ref != slot.producer_predicate_ref
                or component.consumer_query_ref != slot.consumer_query_ref
                or component.consumer_model_rule_hash != slot.model_rule_hash
                or component.producer_route != slot.producer_route
                or slot.source_universe_ref not in set(component.source_universe_refs)
                or slot.release_ref not in set(component.release_refs)
            ):
                raise LearnedWorldConsumerError("executed slot does not match admitted determinants")
            if native_composition_original(component) is None:
                raise LearnedWorldConsumerError("executed slot lacks retained native original")
            components.append(component)
        material = {
            "schema": "R91_BOUND_NATIVE_GRAPH_ORIGINAL@1",
            "slots": [
                {
                    "slot_id": slot.slot_id,
                    "source_universe_ref": slot.source_universe_ref.as_dict(),
                    "release_ref": slot.release_ref.as_dict(),
                    "producer_query_ref": slot.producer_query_ref.as_dict(),
                    "producer_predicate_ref": slot.producer_predicate_ref.as_dict(),
                    "consumer_query_ref": slot.consumer_query_ref.as_dict(),
                    "model_rule_hash": slot.model_rule_hash,
                    "producer_route": slot.producer_route,
                    "composition": canonicalize(component.identity_material()),
                    "composition_hash": component.composed_result_identity_hash,
                }
                for slot, component in zip(request.slots, components)
            ],
        }
        digest = semantic_hash(material)
        ref = ExactRef(
            "R91_BOUND_NATIVE_GRAPH_ORIGINAL@1",
            f"urn:rawlsing:r91:bound-native-graph:sha256:{digest}",
            digest,
        )
        self._originals[digest] = (canonicalize(material), tuple(components))
        return BoundNativeProductGraph(
            original_ref=ref,
            view=NativeProductGraph(tuple(components)),
            projection_hash=digest,
        )

    def resolve_original(self, ref: ExactRef) -> Mapping[str, Any] | None:
        entry = self._originals.get(ref.content_hash)
        return None if entry is None else entry[0]

    def original_components(self, ref: ExactRef) -> tuple[AnalyticalCompositionResult, ...] | None:
        entry = self._originals.get(ref.content_hash)
        return None if entry is None else entry[1]


def _consumer_status_axes(state: str) -> tuple[str, str, str]:
    if state == "SUPPORTED":
        return ("ELIGIBLE", "COMPLETED", "SUPPORTED")
    if state == "ZERO_SUPPORT":
        return ("ELIGIBLE", "COMPLETED", "ZERO_SUPPORT")
    if state == "VALID_EMPTY":
        return ("ELIGIBLE", "COMPLETED", "VALID_EMPTY")
    if state in {"UNRESOLVED", "UNKNOWN"}:
        return ("ELIGIBLE", "COMPLETED", "UNKNOWN")
    if state in {"UNAVAILABLE", "HELD"}:
        return ("HELD", "COMPLETED", "UNSUPPORTED")
    if state in {"NOT_APPLICABLE", "INAPPLICABLE"}:
        return ("INAPPLICABLE_PROVED", "COMPLETED", "UNSUPPORTED")
    return ("ELIGIBLE", "UNSUPPORTED_RUNTIME", "UNSUPPORTED")


def _fallback_graph(compositions: Sequence[AnalyticalCompositionResult]) -> Mapping[str, Any]:
    counts = []
    routes = set()
    for component in compositions:
        topology = canonicalize(component.target_arity_and_topology)
        arity = topology.get("arity")
        counts.append(arity if type(arity) is int and arity > 0 else 1)
        route = component.producer_route
        routes.add(route if isinstance(route, str) else "UNKNOWN_ROUTE")
    return {
        "component_count": len(compositions),
        "producer_routes": tuple(sorted(routes)),
        "producer_route": tuple(sorted(routes))[0] if len(routes) == 1 else "MULTI_ROUTE",
        "joint_component_count": sum(counts),
        "joint_order_semantics": "SEMANTIC_ORDERED",
        "discovery_receipt_refs": (),
        "discovery_frontier_ref": None,
        "recursive_handoff_refs": (),
        "recursive_lineage_refs": (),
        "component_result_hashes": tuple(
            component.composed_result_identity_hash for component in compositions
        ),
    }


def _authoritative_graph(
    compositions: Sequence[AnalyticalCompositionResult],
) -> tuple[Mapping[str, Any], str | None]:
    discovery: list[ExactRef] = []
    recursive: list[ExactRef] = []
    lineage: list[ExactRef] = []
    frontiers: list[ExactRef] = []
    routes: set[str] = set()
    joint_counts: list[int] = []
    orders: list[str] = []
    hashes: list[str] = []
    valid_routes = {
        "DIRECT_I03_TO_POSITIONED_SUBJECT",
        "I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT",
        "MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT",
    }
    for component in compositions:
        original = native_composition_original(component)
        if (
            original is None
            or canonicalize(original) != canonicalize(component.identity_material())
        ):
            return (_fallback_graph(compositions), "COMPONENT_NOT_RETAINED_NATIVE_ORIGINAL")
        topology = canonicalize(component.target_arity_and_topology)
        arity = topology.get("arity")
        components = topology.get("components", ())
        if (
            type(arity) is not int
            or arity < 1
            or len(components) != arity
            or component.joint_component_count != arity
            or component.joint_order_semantics != topology.get("joint_order_semantics")
        ):
            return (_fallback_graph(compositions), "JOINT_COMPONENT_COUNT_OR_ORDER_MISMATCH")
        route = component.producer_route
        if route not in valid_routes:
            return (_fallback_graph(compositions), "UNKNOWN_NATIVE_PRODUCER_ROUTE")
        if route == "DIRECT_I03_TO_POSITIONED_SUBJECT":
            if (
                component.discovery_receipt_refs
                or component.discovery_frontier_ref is not None
                or component.recursive_handoff_refs
                or component.recursive_lineage_refs
            ):
                return (_fallback_graph(compositions), "DIRECT_ROUTE_CARRIES_DISCOVERY_OR_RECURSIVE_LABELS")
        elif route == "I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT":
            if not component.discovery_receipt_refs or component.discovery_frontier_ref is None:
                return (_fallback_graph(compositions), "DISCOVERY_ROUTE_MISSING_RECEIPT_OR_FRONTIER")
            if component.recursive_handoff_refs or component.recursive_lineage_refs:
                return (_fallback_graph(compositions), "DISCOVERY_ROUTE_CARRIES_RECURSIVE_LABELS")
            discovery.extend(component.discovery_receipt_refs)
            frontiers.append(component.discovery_frontier_ref)
        else:
            if not component.recursive_handoff_refs or not component.recursive_lineage_refs:
                return (_fallback_graph(compositions), "RECURSIVE_ROUTE_MISSING_HANDOFF_OR_LINEAGE")
            recursive.extend(component.recursive_handoff_refs)
            lineage.extend(component.recursive_lineage_refs)
        routes.add(route)
        joint_counts.append(arity)
        orders.append(topology.get("joint_order_semantics", "SEMANTIC_ORDERED"))
        hashes.append(component.composed_result_identity_hash)
    if len(set(hashes)) != len(hashes):
        return (_fallback_graph(compositions), "DUPLICATE_GRAPH_COMPONENT")
    graph = {
        "component_count": len(compositions),
        "producer_routes": tuple(sorted(routes)),
        "producer_route": tuple(sorted(routes))[0] if len(routes) == 1 else "MULTI_ROUTE",
        "joint_component_count": sum(joint_counts),
        "joint_order_semantics": orders[0] if len(set(orders)) == 1 else "MIXED",
        "discovery_receipt_refs": tuple(discovery),
        "discovery_frontier_ref": frontiers[0] if frontiers else None,
        "recursive_handoff_refs": tuple(recursive),
        "recursive_lineage_refs": tuple(lineage),
        "component_result_hashes": tuple(hashes),
    }
    return (graph, None)


def _graph_refs(compositions: Sequence[AnalyticalCompositionResult]) -> Mapping[str, Any]:
    graph, problem = _authoritative_graph(compositions)
    if problem is not None:
        raise LearnedWorldConsumerError(problem)
    return graph


def _graph_value(value: Any) -> Any:
    if isinstance(value, ExactRef):
        return value.as_dict()
    if isinstance(value, tuple):
        return [_graph_value(item) for item in value]
    return value


def _typed_graph_result(
    *,
    learned: LearnedWorldCompositionResult,
    disposition: LearnedEmpiricalDisposition,
    composition: AnalyticalCompositionResult,
    compositions: Sequence[AnalyticalCompositionResult],
    graph: Mapping[str, Any],
    consumer_query: PositionedSubjectPossibilityQuery,
    producer_query_ref: ExactRef,
    producer_predicate_ref: ExactRef,
    reason_code: str,
) -> LearnedWorldConsumerResult:
    state = composition.producer_fact_state
    if state == "SUPPORTED":
        state = composition.analytical_state if composition.analytical_state != "SUPPORTED" else "UNKNOWN"
    eligibility, execution, result_state = _consumer_status_axes(state)
    denominator = composition.raw_denominator_support
    cells = tuple(canonicalize(cell) for cell in composition.complete_cell_geometry)
    values = {
        "schema": "R91_LEARNED_WORLD_CONSUMER_VALUES@2",
        "learned_receipt_ref": learned.receipt.ref.as_dict(),
        "product_contract_ref": learned.receipt.product_contract_ref.as_dict(),
        "m1_disposition_ref": disposition.ref.as_dict(),
        "m2_release_ref": learned.m2_artifacts.release.ref.as_dict(),
        "b5_selection_receipt_ref": None
        if learned.b5_selection_receipt is None
        else learned.b5_selection_receipt.ref.as_dict(),
        "consumer_query_ref": consumer_query.ref.as_dict(),
        "producer_query_ref": producer_query_ref.as_dict(),
        "producer_predicate_ref": producer_predicate_ref.as_dict(),
        "eligibility_state": eligibility,
        "execution_state": execution,
        "result_state": result_state,
        "denominator": denominator,
        "cells": [canonicalize(cell) for cell in cells],
        "z_unresolved": result_state == "UNKNOWN" and denominator == 16,
        **{key: _graph_value(value) for key, value in graph.items()},
    }
    return LearnedWorldConsumerResult(
        contract_id=LEARNED_CONSUMER_CONTRACT_ID,
        state=f"LEARNED_CONSUMER_{result_state}",
        reason_code=reason_code,
        learned_receipt_ref=learned.receipt.ref,
        product_contract_ref=learned.receipt.product_contract_ref,
        m1_disposition_ref=disposition.ref,
        m2_release_ref=learned.m2_artifacts.release.ref,
        b5_selection_receipt_ref=None
        if learned.b5_selection_receipt is None
        else learned.b5_selection_receipt.ref,
        evidence_ref=None,
        producer_query_ref=producer_query_ref,
        producer_predicate_ref=producer_predicate_ref,
        consumer_query_ref=consumer_query.ref,
        consumer_result=None,
        consumer_values_read=values,
        eligibility_state=eligibility,
        execution_state=execution,
        result_state=result_state,
        denominator=denominator,
        cells=cells,
        producer_route=graph["producer_route"],
        joint_component_count=graph["joint_component_count"],
        joint_order_semantics=graph["joint_order_semantics"],
        discovery_receipt_refs=graph["discovery_receipt_refs"],
        discovery_frontier_ref=graph["discovery_frontier_ref"],
        recursive_handoff_refs=graph["recursive_handoff_refs"],
        recursive_lineage_refs=graph["recursive_lineage_refs"],
        z_unresolved=result_state == "UNKNOWN" and denominator == 16,
    )


def evaluate_learned_world_consumer(
    learned: LearnedWorldCompositionResult,
    *,
    composition: AnalyticalCompositionResult,
    consumer_query: PositionedSubjectPossibilityQuery,
    model_rule: PositionedSubjectPossibilityModelRule,
    producer_query_ref: ExactRef,
    producer_predicate_ref: ExactRef,
    require_current_selection: bool = False,
    product_graph: NativeProductGraph | None = None,
    trusted_graph_reader: TrustedNativeGraphCoordinator | None = None,
) -> LearnedWorldConsumerResult:
    """Serve unchanged N10E consumer values over the actual native product graph.

    The learned product gates/provenance-binds the result; all geometry and
    component results come from actual C1/E41/D03/I05 owners. Multiple
    compositions must share the same consumer query/model and are evaluated
    independently by the unchanged N10E evaluator. No aggregation is invented.
    """
    if not isinstance(learned, LearnedWorldCompositionResult):
        raise LearnedWorldConsumerError("exact LearnedWorldCompositionResult required")
    if not isinstance(composition, AnalyticalCompositionResult):
        raise LearnedWorldConsumerError("exact AnalyticalCompositionResult required")
    if trusted_graph_reader is not None:
        if not isinstance(trusted_graph_reader, TrustedNativeGraphCoordinator):
            raise LearnedWorldConsumerError("trusted_graph_reader is not a configured coordinator")
        if not isinstance(product_graph, BoundNativeProductGraph):
            return _learned_refusal(
                learned=learned,
                reason="UNTRUSTED_GRAPH_VIEW",
                disposition=learned.m1_disposition,
                evidence=composition.possibility_slice_evidence_or_null,
                producer_query_ref=producer_query_ref,
                producer_predicate_ref=producer_predicate_ref,
            )
        original = trusted_graph_reader.resolve_original(product_graph.original_ref)
        original_components = trusted_graph_reader.original_components(
            product_graph.original_ref
        )
        if (
            original is None
            or original_components is None
            or product_graph.projection_hash != product_graph.original_ref.content_hash
            or len(product_graph.view.compositions) != len(original["slots"])
            or [
                canonicalize(component.identity_material())
                for component in product_graph.view.compositions
            ]
            != [slot["composition"] for slot in original["slots"]]
        ):
            return _learned_refusal(
                learned=learned,
                reason="GRAPH_VIEW_DOES_NOT_MATCH_RETAINED_ORIGINAL",
                disposition=learned.m1_disposition,
                evidence=composition.possibility_slice_evidence_or_null,
                producer_query_ref=producer_query_ref,
                producer_predicate_ref=producer_predicate_ref,
            )
        graph_model = NativeProductGraph(tuple(original_components))
        composition = original_components[0]
        compositions = graph_model.compositions
    else:
        graph_model = NativeProductGraph((composition,)) if product_graph is None else product_graph
        if not isinstance(graph_model, NativeProductGraph):
            raise LearnedWorldConsumerError("product_graph must be NativeProductGraph")
        compositions = graph_model.compositions
        if composition not in compositions:
            raise LearnedWorldConsumerError("primary composition is not in the product graph")
    disposition = learned.m1_disposition
    if learned.receipt.terminal_state != "RULE_SATISFIED" or disposition is None:
        return _learned_refusal(
            learned=learned,
            reason="LEARNED_PRODUCT_NOT_PRODUCTIVE",
            disposition=disposition,
            evidence=composition.possibility_slice_evidence_or_null,
            producer_query_ref=producer_query_ref,
            producer_predicate_ref=producer_predicate_ref,
        )
    if learned.m2_artifacts is None or learned.b5_protocol_view is None:
        return _learned_refusal(
            learned=learned,
            reason="LEARNED_PRODUCT_RELEASE_OR_PROTOCOL_ABSENT",
            disposition=disposition,
            evidence=composition.possibility_slice_evidence_or_null,
            producer_query_ref=producer_query_ref,
            producer_predicate_ref=producer_predicate_ref,
        )
    if require_current_selection and learned.b5_selection_receipt is None:
        return _learned_refusal(
            learned=learned,
            reason="LEARNED_CURRENT_SELECTION_ABSENT",
            disposition=disposition,
            evidence=composition.possibility_slice_evidence_or_null,
            producer_query_ref=producer_query_ref,
            producer_predicate_ref=producer_predicate_ref,
        )
    graph, graph_problem = _authoritative_graph(compositions)
    if graph_problem is not None:
        return _typed_graph_result(
            learned=learned,
            disposition=disposition,
            composition=composition,
            compositions=compositions,
            graph=graph,
            consumer_query=consumer_query,
            producer_query_ref=producer_query_ref,
            producer_predicate_ref=producer_predicate_ref,
            reason_code=graph_problem,
        )
    if graph_model.extension_result is not None:
        extension = graph_model.extension_result
        allowed_routes = {
            EXT_ROUTE_DIRECT_VIA_ACCEPTED_PROVIDER,
            EXT_ROUTE_DIRECT_MULTI_CONDITIONER,
            EXT_ROUTE_DISCOVERY,
            EXT_ROUTE_RECURSIVE,
        }
        ext_comp = getattr(extension, "composition_result", None)
        ext_route = getattr(extension, "producer_route", None)
        ext_consumer = getattr(extension, "consumer_result_or_null", None)
        if (
            not isinstance(extension, EmpiricalPossibilitySliceExtensionResult)
            or ext_comp is None
            or ext_route not in allowed_routes
            or not any(
                ext_comp.composed_result_identity_hash
                == component.composed_result_identity_hash
                for component in compositions
            )
            or ext_consumer is None
            or composition.consumer_result_or_null is None
            or ext_consumer.result_hash != composition.consumer_result_or_null.result_hash
            or ext_route != extension.extension_receipt.producer_route
            or extension.extension_receipt.composed_result_identity_hash
            != composition.composed_result_identity_hash
        ):
            return _learned_refusal(
                learned=learned,
                reason="E41_EXTENSION_GRAPH_MISMATCH",
                disposition=disposition,
                evidence=composition.possibility_slice_evidence_or_null,
                producer_query_ref=producer_query_ref,
                producer_predicate_ref=producer_predicate_ref,
            )
        graph = {**graph, "extension_route": ext_route}
    if (
        composition.producer_query_ref != producer_query_ref
        or composition.producer_predicate_ref != producer_predicate_ref
    ):
        return _learned_refusal(
            learned=learned,
            reason="EMPIRICAL_COMPOSITION_DETERMINANT_MISMATCH",
            disposition=disposition,
            evidence=composition.possibility_slice_evidence_or_null,
            producer_query_ref=producer_query_ref,
            producer_predicate_ref=producer_predicate_ref,
        )
    for component in compositions:
        if (
            component.consumer_query_ref != consumer_query.ref
            or component.consumer_model_rule_hash != model_rule.rule_hash
        ):
            return _learned_refusal(
                learned=learned,
                reason="PRODUCT_GRAPH_CONSUMER_IDENTITY_MISMATCH",
                disposition=disposition,
                evidence=composition.possibility_slice_evidence_or_null,
                producer_query_ref=producer_query_ref,
                producer_predicate_ref=producer_predicate_ref,
            )
        if producer_predicate_ref not in set(disposition.empirical_predicate_refs):
            return _learned_refusal(
                learned=learned,
                reason="LEARNED_EMPIRICAL_PREDICATE_MISMATCH",
                disposition=disposition,
                evidence=composition.possibility_slice_evidence_or_null,
                producer_query_ref=producer_query_ref,
                producer_predicate_ref=producer_predicate_ref,
            )
        if component.source_universe_refs and not set(component.source_universe_refs) & set(disposition.source_universe_refs):
            return _learned_refusal(
                learned=learned,
                reason="LEARNED_SOURCE_UNIVERSE_MISMATCH",
                disposition=disposition,
                evidence=composition.possibility_slice_evidence_or_null,
                producer_query_ref=producer_query_ref,
                producer_predicate_ref=producer_predicate_ref,
            )
    if (
        composition.producer_fact_state != "SUPPORTED"
        or composition.analytical_state != "SUPPORTED"
        or composition.possibility_slice_evidence_or_null is None
        or composition.raw_denominator_support
        != composition.possibility_slice_evidence_or_null.raw_support
    ):
        return _typed_graph_result(
            learned=learned,
            disposition=disposition,
            composition=composition,
            compositions=compositions,
            graph=graph,
            consumer_query=consumer_query,
            producer_query_ref=producer_query_ref,
            producer_predicate_ref=producer_predicate_ref,
            reason_code=f"TYPED_{composition.producer_fact_state}_PRODUCT",
        )
    component_results = []
    for component in compositions:
        evidence = component.possibility_slice_evidence_or_null
        if evidence is None:
            return _typed_graph_result(
                learned=learned,
                disposition=disposition,
                composition=composition,
                compositions=compositions,
                graph=graph,
                consumer_query=consumer_query,
                producer_query_ref=producer_query_ref,
                producer_predicate_ref=producer_predicate_ref,
                reason_code="PRODUCT_GRAPH_MISSING_COMPONENT_EVIDENCE",
            )
        if (
            evidence.source_universe_ref not in set(disposition.source_universe_refs)
        ):
            return _learned_refusal(
                learned=learned,
                reason="LEARNED_SOURCE_UNIVERSE_MISMATCH",
                disposition=disposition,
                evidence=evidence,
                producer_query_ref=producer_query_ref,
                producer_predicate_ref=producer_predicate_ref,
            )
        component_results.append(
            evaluate_positioned_subject_possibility(
                query=consumer_query,
                rule=model_rule,
                evidence=(evidence,),
            )
        )
    if any(item.result_state != "EXACT_SUPPORTED" for item in component_results):
        return _typed_graph_result(
            learned=learned,
            disposition=disposition,
            composition=composition,
            compositions=compositions,
            graph=graph,
            consumer_query=consumer_query,
            producer_query_ref=producer_query_ref,
            producer_predicate_ref=producer_predicate_ref,
            reason_code="PRODUCT_GRAPH_COMPONENT_NOT_EXACT_SUPPORTED",
        )
    producer_result = component_results[0]
    evidence = composition.possibility_slice_evidence_or_null
    values = {
        "schema": "R91_LEARNED_WORLD_CONSUMER_VALUES@2",
        "learned_receipt_ref": learned.receipt.ref.as_dict(),
        "product_contract_ref": learned.receipt.product_contract_ref.as_dict(),
        "m1_disposition_ref": disposition.ref.as_dict(),
        "m2_release_ref": learned.m2_artifacts.release.ref.as_dict(),
        "b5_selection_receipt_ref": None
        if learned.b5_selection_receipt is None
        else learned.b5_selection_receipt.ref.as_dict(),
        "evidence_ref": evidence.evidence_ref.as_dict(),
        "producer_query_ref": producer_query_ref.as_dict(),
        "producer_predicate_ref": producer_predicate_ref.as_dict(),
        "consumer_query_ref": consumer_query.ref.as_dict(),
        "consumer_result_state": producer_result.result_state,
        "consumer_result_hash": producer_result.result_hash,
        "consumer_values_read": canonicalize(producer_result.material()),
        "eligibility_state": "ELIGIBLE",
        "execution_state": "COMPLETED",
        "result_state": "SUPPORTED",
        "denominator": composition.raw_denominator_support,
        "cells": [canonicalize(cell) for cell in composition.complete_cell_geometry],
        "z_unresolved": False,
        "component_consumer_result_hashes": [
            item.result_hash for item in component_results
        ],
        **{key: _graph_value(value) for key, value in graph.items()},
    }
    return LearnedWorldConsumerResult(
        contract_id=LEARNED_CONSUMER_CONTRACT_ID,
        state="LEARNED_CONSUMER_EXACT_SUPPORTED",
        reason_code="PRODUCTIVE_LEARNED_PRODUCT_WITH_ACTUAL_EMPIRICAL_EVIDENCE",
        learned_receipt_ref=learned.receipt.ref,
        product_contract_ref=learned.receipt.product_contract_ref,
        m1_disposition_ref=disposition.ref,
        m2_release_ref=learned.m2_artifacts.release.ref,
        b5_selection_receipt_ref=None
        if learned.b5_selection_receipt is None
        else learned.b5_selection_receipt.ref,
        evidence_ref=evidence.evidence_ref,
        producer_query_ref=producer_query_ref,
        producer_predicate_ref=producer_predicate_ref,
        consumer_query_ref=consumer_query.ref,
        consumer_result=producer_result,
        consumer_values_read=values,
        eligibility_state="ELIGIBLE",
        execution_state="COMPLETED",
        result_state="SUPPORTED",
        denominator=composition.raw_denominator_support,
        cells=tuple(canonicalize(cell) for cell in composition.complete_cell_geometry),
        producer_route=graph["producer_route"],
        joint_component_count=graph["joint_component_count"],
        joint_order_semantics=graph["joint_order_semantics"],
        discovery_receipt_refs=graph["discovery_receipt_refs"],
        discovery_frontier_ref=graph["discovery_frontier_ref"],
        recursive_handoff_refs=graph["recursive_handoff_refs"],
        recursive_lineage_refs=graph["recursive_lineage_refs"],
        z_unresolved=False,
    )
