"""PYAT HQ119 I4 — exact learned-world composition/adaptation runtime.

I4 is a seam, not a semantic stage.  It binds exact objects already owned by
M01, M1, M2 and B5.  It never selects a family rule, product family, current
release, consumer permission, or lifecycle action by inference.

The default lifecycle action is NO_LIFECYCLE_SIDE_EFFECT.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

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
]
