#!/usr/bin/env python3
"""Exact M4 binding extension for accepted M1 evaluation contracts.

The frozen M4 implementation remains the owner of V557/V558 objects and
permissions. This adapter adds only the exact relation-M1 contract binding
required by GT2 while delegating the empirical M1 path unchanged.
"""
from __future__ import annotations

from typing import Mapping, Sequence

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


def structural_objects_from_accepted_m1(
    evaluation: M1Evaluation,
    *,
    producer_allowed_uses: Sequence[str],
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
        return structural_objects_from_empirical_m1(
            evaluation,
            producer_allowed_uses=producer_allowed_uses,
        )

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
