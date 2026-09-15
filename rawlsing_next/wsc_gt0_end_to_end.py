"""Integrated WSC002G Golden Thread 0 end-to-end harness."""
from __future__ import annotations

from dataclasses import dataclass

from rawlsing_next.wsc_gt0_protocol import GT0StageReceipt, GT0StageStatus, gt0_content_hash
from rawlsing_next.wsc_gt0_source_preff import bind_gt0_f0, run_gt0_preff
from rawlsing_next.wsc_gt0_field_forge_ingress import run_gt0_field_forge_ingress
from rawlsing_next.wsc_gt0_prev3_bridge import run_gt0_prev3
from rawlsing_next.wsc_gt0_v3_runtime import run_gt0_prev3_v3
from rawlsing_next.wsc_gt0_v2_mediation import run_gt0_v3_v2

TERMINAL = "BLOCKED_POSITIVE_ACTOR_PATH__SEMANTIC_CONSERVATION_PASS"

@dataclass(frozen=True, slots=True)
class GT0EndToEndResult:
    receipts: tuple[GT0StageReceipt, ...]
    full_thread_hash: str
    terminal: str

def _assert_conservation(receipts: tuple[GT0StageReceipt, ...]) -> None:
    if not receipts:
        raise AssertionError("GT0 requires receipts")
    owners = {r.output_envelope.semantic_owner_ref for r in receipts}
    if len(owners) != 1:
        raise AssertionError("semantic ownership changed across GT0")
    baseline_permissions = set(receipts[0].output_envelope.permission_ceiling)
    for receipt in receipts[1:]:
        if not set(receipt.output_envelope.permission_ceiling).issubset(baseline_permissions):
            raise AssertionError("permission widened across GT0")
    if receipts[-1].status is not GT0StageStatus.BLOCKED_NAMED_AUTHORITY_REQUIRED:
        raise AssertionError("GT0 did not terminate at the expected V2 authority frontier")

def run_gt0_end_to_end() -> GT0EndToEndResult:
    bound = bind_gt0_f0()
    preff = run_gt0_preff(bound)
    ff = run_gt0_field_forge_ingress(preff)
    prev3 = run_gt0_prev3(ff, f0_ref=bound.f0_ref)
    v3 = run_gt0_prev3_v3(prev3)
    v2 = run_gt0_v3_v2(v3)

    receipts = (
        bound.receipt,
        preff.receipt,
        ff,
        prev3,
        v3.receipt,
        v2.receipt,
    )
    _assert_conservation(receipts)
    if prev3.status is not GT0StageStatus.UNDEFINED_FOR_OBJECT:
        raise AssertionError("PRE-V3 baseline fabricated or misclassified structural meaning")
    if v3.before != v3.after:
        raise AssertionError("V3 state mutated on GT0 blocked actor path")
    if v2.actor_claim_created or v2.rendered_text is not None or v2.v3_mutated:
        raise AssertionError("V2 fabricated actor claim/render or mutated V3")

    thread_hash = gt0_content_hash({
        "terminal": TERMINAL,
        "receipt_hashes": [receipt.content_hash for receipt in receipts],
    })
    return GT0EndToEndResult(
        receipts=receipts,
        full_thread_hash=thread_hash,
        terminal=TERMINAL,
    )

__all__ = ["TERMINAL", "GT0EndToEndResult", "run_gt0_end_to_end"]
