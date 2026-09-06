#!/usr/bin/env python3
"""Exact M4 binding extension for accepted M1 evaluation contracts.

The frozen M4 implementation remains the owner of V557/V558 objects and
permissions. This adapter adds only the exact relation-M1 contract binding
required by GT2 while delegating the empirical M1 path unchanged.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence

from rawlsing_next.m1_temporal_v554_admission_dedup import (
    M1_CONTRACT_ID,
    M1Evaluation,
    SCR554_CONTRACT_ID,
    semantic_hash,
)
from rawlsing_next.m1_admitted_field_forge_relation_v554_ingress import (
    RELATION_M1_CONTRACT_ID,
)
from rawlsing_next.m4_v557_v558_publication_repository import (
    M4IntegrityError,
    StructuralObject,
    _hash,
    _text,
    make_structural_object,
    structural_objects_from_m1 as structural_objects_from_empirical_m1,
)

ACCEPTED_M1_EVALUATION_CONTRACT_IDS = frozenset(
    {M1_CONTRACT_ID, RELATION_M1_CONTRACT_ID}
)


_VALIDATED_RELATION_USE_BINDING_SEAL = object()


def _relation_evaluation_binding_hash(evaluation: M1Evaluation) -> str:
    return semantic_hash(
        {
            "contract_id": evaluation.contract_id,
            "decision_state": evaluation.decision_state.value,
            "governed_use_id": evaluation.governed_use_id,
            "required_basis_kind": evaluation.required_basis_kind,
            "canonical_basis_semantic_id": evaluation.canonical_basis_semantic_id,
            "f1": evaluation.f1,
            "direct_v557_handoff": evaluation.direct_v557_handoff,
        }
    )


class ValidatedM1ProducerUseBinding:
    """Opaque capability proving one relation M1 evaluation's producer uses.

    The public shared adapter can consume this token but cannot mint it from raw
    use labels. Governed wrappers issue it only after their own exact
    authority/adoption validation. The token is evaluation-specific and does
    not prescribe CONTEXT or any other use globally.
    """

    __slots__ = (
        "m1_contract_id",
        "producer_allowed_uses",
        "authority_binding_hash",
        "evaluation_binding_hash",
        "_seal",
        "_frozen",
    )

    def __init__(
        self,
        *,
        m1_contract_id: str,
        producer_allowed_uses: tuple[str, ...],
        authority_binding_hash: str,
        evaluation_binding_hash: str,
        _seal: object,
    ) -> None:
        if _seal is not _VALIDATED_RELATION_USE_BINDING_SEAL:
            raise M4IntegrityError(
                "validated M1 producer-use binding may be issued only by a governed authority wrapper"
            )
        object.__setattr__(self, "m1_contract_id", m1_contract_id)
        object.__setattr__(self, "producer_allowed_uses", producer_allowed_uses)
        object.__setattr__(self, "authority_binding_hash", authority_binding_hash)
        object.__setattr__(self, "evaluation_binding_hash", evaluation_binding_hash)
        object.__setattr__(self, "_seal", _seal)
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_frozen", False):
            raise AttributeError("validated M1 producer-use binding is immutable")
        object.__setattr__(self, name, value)


def _issue_validated_relation_producer_use_binding(
    evaluation: M1Evaluation,
    authority_binding: Mapping[str, Any],
) -> ValidatedM1ProducerUseBinding:
    """Issue one evaluation-specific token from an already validated binding.

    This function is deliberately internal. It validates binding integrity and
    exact M1 lineage but does not itself decide semantic permission; that
    decision remains owned by the governed wrapper that produced the binding.
    """
    if not isinstance(evaluation, M1Evaluation):
        raise M4IntegrityError("validated producer-use binding requires exact M1Evaluation")
    if evaluation.contract_id != RELATION_M1_CONTRACT_ID:
        raise M4IntegrityError(
            "validated relation producer-use binding requires exact relation M1 contract"
        )
    if not isinstance(authority_binding, Mapping):
        raise M4IntegrityError("validated producer-use authority binding must be mapping")

    material = dict(authority_binding)
    binding_hash = material.pop("binding_hash", None)
    if not isinstance(binding_hash, str) or semantic_hash(material) != binding_hash:
        raise M4IntegrityError("validated producer-use authority binding hash mismatch")

    raw_uses = authority_binding.get("producer_allowed_uses")
    if isinstance(raw_uses, (str, bytes)) or not isinstance(raw_uses, Sequence):
        raise M4IntegrityError("validated producer-use binding uses malformed")
    uses = tuple(_text(value, "producer_allowed_use") for value in raw_uses)
    if not uses or len(uses) != len(set(uses)):
        raise M4IntegrityError("validated producer-use binding requires exact unique nonempty uses")

    if evaluation.f1 is None or not isinstance(evaluation.f1, Mapping):
        raise M4IntegrityError("relation M1 evaluation lacks exact F1 lineage")
    admission_ref = authority_binding.get("upstream_admission_ref")
    relation_ref = authority_binding.get("field_forge_relation_ref")
    admission_lineage = evaluation.f1.get("originating_relation_admission_exact_refs")
    relation_lineage = evaluation.f1.get("originating_field_forge_relation_exact_refs")
    if (
        not isinstance(admission_ref, Mapping)
        or isinstance(admission_lineage, (str, bytes))
        or not isinstance(admission_lineage, Sequence)
        or dict(admission_ref) not in [
            dict(item) for item in admission_lineage if isinstance(item, Mapping)
        ]
    ):
        raise M4IntegrityError(
            "validated producer-use binding admission ref does not match relation M1 lineage"
        )
    if (
        not isinstance(relation_ref, Mapping)
        or isinstance(relation_lineage, (str, bytes))
        or not isinstance(relation_lineage, Sequence)
        or dict(relation_ref) not in [
            dict(item) for item in relation_lineage if isinstance(item, Mapping)
        ]
    ):
        raise M4IntegrityError(
            "validated producer-use binding relation ref does not match relation M1 lineage"
        )

    return ValidatedM1ProducerUseBinding(
        m1_contract_id=evaluation.contract_id,
        producer_allowed_uses=uses,
        authority_binding_hash=binding_hash,
        evaluation_binding_hash=_relation_evaluation_binding_hash(evaluation),
        _seal=_VALIDATED_RELATION_USE_BINDING_SEAL,
    )


def structural_objects_from_accepted_m1(
    evaluation: M1Evaluation,
    *,
    producer_allowed_uses: Sequence[str] | None = None,
    validated_producer_use_binding: ValidatedM1ProducerUseBinding | None = None,
) -> tuple[StructuralObject, ...]:
    """Bind one exact accepted M1 evaluation into actual M4 V557/V558 objects.

    The existing empirical contract delegates directly to the frozen M4
    adapter. The relation contract receives the same exact F1/F2/B1 and
    V554_TO_V557_DIRECT validation, with no new producer family or permission.
    """
    if not isinstance(evaluation, M1Evaluation):
        raise M4IntegrityError("M1 adapter requires exact M1Evaluation")
    if evaluation.contract_id not in ACCEPTED_M1_EVALUATION_CONTRACT_IDS:
        raise M4IntegrityError(
            "M1 adapter requires exact accepted M1 evaluation contract"
        )

    if evaluation.contract_id == M1_CONTRACT_ID:
        if validated_producer_use_binding is not None:
            raise M4IntegrityError(
                "relation producer-use binding may not alter empirical M1 contract semantics"
            )
        if producer_allowed_uses is None:
            raise M4IntegrityError(
                "empirical M1 adapter requires its existing explicit governed producer uses"
            )
        return structural_objects_from_empirical_m1(
            evaluation,
            producer_allowed_uses=producer_allowed_uses,
        )

    if producer_allowed_uses is not None:
        raise M4IntegrityError(
            "relation M1 producer uses may not be caller-selected at the shared boundary"
        )
    if not isinstance(validated_producer_use_binding, ValidatedM1ProducerUseBinding):
        raise M4IntegrityError(
            "relation M1 requires exact validated producer-use authority binding"
        )
    if validated_producer_use_binding._seal is not _VALIDATED_RELATION_USE_BINDING_SEAL:
        raise M4IntegrityError("validated producer-use binding seal mismatch")
    if validated_producer_use_binding.m1_contract_id != evaluation.contract_id:
        raise M4IntegrityError("validated producer-use binding contract mismatch")
    if (
        validated_producer_use_binding.evaluation_binding_hash
        != _relation_evaluation_binding_hash(evaluation)
    ):
        raise M4IntegrityError(
            "validated producer-use binding is not bound to this exact M1 evaluation"
        )
    producer_allowed_uses = validated_producer_use_binding.producer_allowed_uses

    handoff = evaluation.direct_v557_handoff
    if handoff is None:
        return ()
    if not isinstance(handoff, Mapping) or handoff.get("route") != "V554_TO_V557_DIRECT":
        raise M4IntegrityError(
            "relation M1 direct handoff route is not exact V554->V557"
        )
    refs = handoff.get("object_refs")
    if isinstance(refs, (str, bytes)) or not isinstance(refs, Sequence):
        raise M4IntegrityError("relation M1 direct handoff object_refs malformed")

    payloads: dict[str, tuple[str, Mapping[str, object], str]] = {}
    if evaluation.f1 is not None:
        payloads[evaluation.f1["f1_id"]] = (
            "F1",
            evaluation.f1,
            evaluation.f1.get("state", evaluation.decision_state.value),
        )
    for f2 in evaluation.f2:
        payloads[f2["f2_id"]] = (
            "F2",
            f2,
            f2.get("disposition", evaluation.decision_state.value),
        )
    if evaluation.b1 is not None:
        payloads[evaluation.b1["b1_id"]] = (
            "B1",
            evaluation.b1,
            evaluation.b1.get("decision_state", evaluation.decision_state.value),
        )

    out: list[StructuralObject] = []
    for raw in refs:
        if not isinstance(raw, Mapping) or set(raw) != {
            "family",
            "object_id",
            "content_hash",
        }:
            raise M4IntegrityError(
                "relation M1 publication ref fields are not exact"
            )
        family = _text(raw["family"], "relation_M1.family")
        oid = _text(raw["object_id"], "relation_M1.object_id")
        content_hash = _hash(raw["content_hash"], "relation_M1.content_hash")
        if family not in {"F1", "F2", "B1"}:
            raise M4IntegrityError(
                "relation M1 publication family outside frozen V554 object grammar"
            )
        if oid not in payloads or payloads[oid][0] != family:
            raise M4IntegrityError(
                "relation M1 handoff ref does not resolve to exact V554 object"
            )
        _, payload, state = payloads[oid]
        if semantic_hash(payload) != content_hash:
            raise M4IntegrityError("relation M1 handoff object hash mismatch")
        out.append(
            make_structural_object(
                producer_family="V554",
                semantic_class=family,
                object_id=oid,
                schema_id=SCR554_CONTRACT_ID,
                schema_version="1.0.0",
                typed_state=state,
                producer_allowed_uses=producer_allowed_uses,
                payload=payload,
                source_stage="M1_RELATION_V554_TO_V557",
            )
        )
    return tuple(out)


__all__ = [
    "ACCEPTED_M1_EVALUATION_CONTRACT_IDS",
    "ValidatedM1ProducerUseBinding",
    "structural_objects_from_accepted_m1",
]
