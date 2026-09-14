from __future__ import annotations

from dataclasses import dataclass

from rawlsing_next.m4_v557_v558_publication_repository import AuthorityRef, ExactRef, semantic_hash

CONTRACT_ID = "PREV3_D05_NON_EVENT_CURRENTNESS_COMPATIBILITY@1.0.0"
CONTRACT_HASH = "80d361179530d84e08b48094a6cc68d0864365dc396d8740e4dffd20d80bb6c0"
CONTRACT_REF = ExactRef(
    "PREV3_D05_NON_EVENT_CURRENTNESS_COMPATIBILITY_CONTRACT",
    f"D05CURCOMPAT:{CONTRACT_HASH}",
    CONTRACT_HASH,
)
RECEIPT_SCHEMA = "PREV3_OBJECTIVE_NON_EVENT_CURRENTNESS_RECEIPT@1.0.0"
RECEIPT_KIND = "PREV3_OBJECTIVE_NON_EVENT_CURRENTNESS_RECEIPT"
STATES = frozenset({"CURRENT", "STALE", "REFRESH_REQUIRED", "INVALID"})


@dataclass(frozen=True)
class ObjectiveNonEventCurrentnessReceipt:
    receipt_id: str
    receipt_hash: str
    schema: str
    compatibility_contract_ref: ExactRef
    state: str
    authority_ref: AuthorityRef
    structural_currentness_basis_ref: ExactRef
    decision_effective_time_ref: ExactRef
    non_event_resolution_receipt_ref: ExactRef
    selection_record_ref: ExactRef
    producer_object_ref: ExactRef
    world_or_release_root_ref: ExactRef

    @property
    def ref(self) -> ExactRef:
        return ExactRef(RECEIPT_KIND, self.receipt_id, self.receipt_hash)


def receipt_material(receipt: ObjectiveNonEventCurrentnessReceipt):
    return {
        "schema": RECEIPT_SCHEMA,
        "compatibility_contract_ref": receipt.compatibility_contract_ref.as_dict(),
        "state": receipt.state,
        "authority_ref": receipt.authority_ref.as_dict(),
        "structural_currentness_basis_ref": receipt.structural_currentness_basis_ref.as_dict(),
        "decision_effective_time_ref": receipt.decision_effective_time_ref.as_dict(),
        "non_event_resolution_receipt_ref": receipt.non_event_resolution_receipt_ref.as_dict(),
        "selection_record_ref": receipt.selection_record_ref.as_dict(),
        "producer_object_ref": receipt.producer_object_ref.as_dict(),
        "world_or_release_root_ref": receipt.world_or_release_root_ref.as_dict(),
    }


def seal_receipt(draft: ObjectiveNonEventCurrentnessReceipt):
    h = semantic_hash(receipt_material(draft))
    return ObjectiveNonEventCurrentnessReceipt(
        f"D05CUR:{h}", h, draft.schema, draft.compatibility_contract_ref, draft.state,
        draft.authority_ref, draft.structural_currentness_basis_ref,
        draft.decision_effective_time_ref, draft.non_event_resolution_receipt_ref,
        draft.selection_record_ref, draft.producer_object_ref, draft.world_or_release_root_ref,
    )
