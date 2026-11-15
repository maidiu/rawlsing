"""Corrected WSC002D Golden Thread 0 FIELD FORGE -> PRE-V3 bridge.

This module is deliberately narrower than the historical I04/P06 seam.
The GT0 seed is a governed source-structure/current-J-candidacy fact, not an
EmpiricalFact and not a FIELD FORGE structural relation eligible for direct
I04/P06 or M1 admission.  The baseline therefore preserves exact producer
references and returns UNDEFINED_FOR_OBJECT.  A named substantive structural
request is BLOCKED_EXPLICIT_AUTHORITY until a separately governed
FIELD-FORGE-relation -> PRE-V3 admission surface exists.

No object is coerced into EmpiricalFact or StructuralEmpiricalAdmission.
No V554/V555 object is minted and ZERO_V556_OBJECTS is the lawful baseline.
"""
from __future__ import annotations

from typing import Iterable

from rawlsing_next.wsc_gt0_protocol import (
    GT0ConservationEnvelope,
    GT0ExactRef,
    GT0IntegrityError,
    GT0StageReceipt,
    GT0StageStatus,
    assert_permission_narrowing,
    validate_exact_upstream_ref,
)

CONTRACT_ID = "WSC002D_GT0_FIELD_FORGE_PREV3_BRIDGE@2.0.0"
STAGE_ID = "GT0_FIELD_FORGE_TO_PREV3"
GT0_F0_SOURCE_STRUCTURE_ID = "cssu.r1.afrobarometer.r1.005b474d6eb4253cb166"
GT0_BASELINE_TARGET_USE = "GT0_BASELINE_PREV3_STRUCTURAL_REQUEST"
INFORMATION_LOSS = "NONE__REFERENCE_PRESERVING"
ZERO_V556_MARKER = "ZERO_V556_OBJECTS"

WSC001C_CORRECTION_REF = GT0ExactRef(
    kind="GIT_COMMIT",
    value="3f9017ae3de22d8d9d5ab538096ce2f951c1681c",
    content_hash="3f9017ae3de22d8d9d5ab538096ce2f951c1681c",
)
WSC002_COMMISSION_REF = GT0ExactRef(
    kind="GIT_COMMIT",
    value="dceacb137e1ab111dc4b389d9bf45bea15971d3b",
    content_hash="dceacb137e1ab111dc4b389d9bf45bea15971d3b",
)


class GT0Prev3BridgeError(GT0IntegrityError):
    """The PRE-V3 bridge would violate the GT0 authority or identity ceiling."""


def _stage_ref(receipt: GT0StageReceipt) -> GT0ExactRef:
    return GT0ExactRef(
        kind="GT0_STAGE_RECEIPT",
        value=(
            f"urn:rawlsing:wsc002:stage:{receipt.stage_id}:"
            f"sha256:{receipt.content_hash}"
        ),
        content_hash=receipt.content_hash,
    )


def _all_refs(receipt: GT0StageReceipt) -> frozenset[GT0ExactRef]:
    env = receipt.output_envelope
    return frozenset(
        receipt.upstream_refs
        + receipt.authority_refs
        + receipt.replay_refs
        + env.object_refs
        + env.authority_refs
        + env.current_selection_refs
        + env.scope_refs
        + env.relation_query_refs
        + env.dependency_refs
        + env.provenance_refs
        + env.replay_refs
    )


def _require_bound_f0(receipt: GT0StageReceipt, f0_ref: GT0ExactRef) -> GT0ExactRef:
    exact = validate_exact_upstream_ref(f0_ref, "f0_ref")
    if exact.value != GT0_F0_SOURCE_STRUCTURE_ID:
        raise GT0Prev3BridgeError("f0_ref is not the bound GT0 source-structure seed")
    if exact not in _all_refs(receipt):
        raise GT0Prev3BridgeError(
            "upstream FIELD FORGE receipt does not preserve the exact F0 reference"
        )
    return exact


def _status_for(
    upstream: GT0StageStatus,
    requested_structural_meaning: str | None,
) -> tuple[GT0StageStatus, str]:
    if upstream is not GT0StageStatus.PASS:
        return upstream, "UPSTREAM_NONPOSITIVE_PRESERVED__NO_PREV3_PROMOTION"
    if requested_structural_meaning is not None:
        if not isinstance(requested_structural_meaning, str) or not requested_structural_meaning.strip():
            raise GT0Prev3BridgeError("requested_structural_meaning must be non-empty when supplied")
        return (
            GT0StageStatus.BLOCKED_EXPLICIT_AUTHORITY,
            "FF_RELATION_TO_PREV3_ADMISSION_SURFACE_NOT_CURRENTLY_BOUND",
        )
    return (
        GT0StageStatus.UNDEFINED_FOR_OBJECT,
        "F0_SOURCE_STRUCTURE_CANDIDACY_HAS_NO_SUBSTANTIVE_PREV3_STRUCTURAL_SEMANTICS",
    )


def _merged_refs(*groups: Iterable[GT0ExactRef]) -> tuple[GT0ExactRef, ...]:
    by_key: dict[str, GT0ExactRef] = {}
    for group in groups:
        for ref in group:
            exact = validate_exact_upstream_ref(ref)
            by_key[exact.key] = exact
    return tuple(by_key[key] for key in sorted(by_key))


def run_gt0_prev3(
    upstream_receipt: GT0StageReceipt,
    *,
    f0_ref: GT0ExactRef,
    requested_structural_meaning: str | None = None,
    consumer_permissions: Iterable[str] | None = None,
) -> GT0StageReceipt:
    """Execute the lawful GT0 FIELD FORGE -> PRE-V3 baseline.

    The function never calls or imitates ``pre553_structural_admission`` and
    never feeds a FIELD FORGE receipt into M1.  Those APIs are typed for a
    different current semantic grain.  This bridge proves conservation at the
    present authority frontier and blocks rather than fabricates structure.
    """

    if not isinstance(upstream_receipt, GT0StageReceipt):
        raise GT0Prev3BridgeError("upstream_receipt must be an exact GT0StageReceipt")

    f0 = _require_bound_f0(upstream_receipt, f0_ref)
    source_env = upstream_receipt.output_envelope
    status, detail = _status_for(
        upstream_receipt.status,
        requested_structural_meaning,
    )

    permissions = (
        source_env.permission_ceiling
        if consumer_permissions is None
        else assert_permission_narrowing(
            source_env.permission_ceiling,
            consumer_permissions,
        )
    )

    upstream_stage_ref = _stage_ref(upstream_receipt)

    # Preserve producer-owned identity and all existing exact closures.  The
    # only new semantic fact here is the typed PRE-V3 disposition itself.
    output_env = GT0ConservationEnvelope(
        semantic_owner_ref=source_env.semantic_owner_ref,
        object_refs=source_env.object_refs,
        authority_refs=source_env.authority_refs,
        current_selection_refs=source_env.current_selection_refs,
        scope_refs=source_env.scope_refs,
        relation_query_refs=source_env.relation_query_refs,
        permission_ceiling=permissions,
        status=status,
        dependency_refs=_merged_refs(source_env.dependency_refs, (upstream_stage_ref,)),
        provenance_refs=_merged_refs(
            source_env.provenance_refs,
            (upstream_stage_ref, f0, WSC001C_CORRECTION_REF, WSC002_COMMISSION_REF),
        ),
        replay_refs=_merged_refs(source_env.replay_refs, (upstream_stage_ref,)),
        information_loss=source_env.information_loss,
    )

    if output_env.information_loss != INFORMATION_LOSS:
        raise GT0Prev3BridgeError(
            "GT0 baseline must remain reference-preserving through PRE-V3"
        )

    detail_code = (
        f"{detail}__NO_I04_COERCION__NO_M1_DIRECT_BASIS__"
        f"NO_V555_ROUTE__{ZERO_V556_MARKER}"
    )

    return GT0StageReceipt(
        stage_id=STAGE_ID,
        status=status,
        input_envelope_hashes=(source_env.content_hash,),
        output_envelope=output_env,
        upstream_refs=_merged_refs(upstream_receipt.upstream_refs, (upstream_stage_ref, f0)),
        authority_refs=_merged_refs(upstream_receipt.authority_refs, source_env.authority_refs),
        replay_refs=_merged_refs(
            upstream_receipt.replay_refs,
            source_env.replay_refs,
            (upstream_stage_ref,),
        ),
        detail_code=detail_code,
    )


__all__ = [
    "CONTRACT_ID",
    "STAGE_ID",
    "GT0_F0_SOURCE_STRUCTURE_ID",
    "GT0_BASELINE_TARGET_USE",
    "INFORMATION_LOSS",
    "ZERO_V556_MARKER",
    "WSC001C_CORRECTION_REF",
    "WSC002_COMMISSION_REF",
    "GT0Prev3BridgeError",
    "run_gt0_prev3",
]
