"""BP3 sourcefree C9 event ingress over a committed C8 receipt.

This reads the ACTUAL OUT9-compatible committed journal through the accepted
C8O read-only consumer. It does not claim ADP019 admission or a performed E2.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDOR = HERE / "vendor"
if str(VENDOR) not in sys.path:
    sys.path.insert(0, str(VENDOR))

from c8_readonly_consumer import C8ReadOnlyConsumer  # noqa: E402

SCHEMA = "C9_SOURCEFREE_EVENT_INGRESS@1"
ADP019_ADMISSION_RECEIPT_ABSENT = "ADP019_ADMISSION_RECEIPT_ABSENT"
E2_PERFORMED = False


class C9IngressRefused(Exception):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def receive_event(journal_path, *, expected_state_digest=None, proof_verifier=None):
    if proof_verifier is None:
        raise C9IngressRefused("PROOF_VERIFIER_REQUIRED")
    proof_verifier()
    consumer = C8ReadOnlyConsumer(journal_path)
    view = consumer.load()
    readset = view.readset.to_json()
    if expected_state_digest is not None and readset["state_digest"] != expected_state_digest:
        raise C9IngressRefused("C8_STATE_DIGEST_MISMATCH")
    return {
        "schema": SCHEMA,
        "state": "TEST_ONLY_EVENT_AVAILABLE",
        "occurrence_ids": list(readset["occurrence_ids"]),
        "occurrence_count": len(readset["occurrence_ids"]),
        "state_digest": readset["state_digest"],
        "version_state_digest": readset["version_state_digest"],
        "ledger_prefix_digest": readset["ledger_prefix_digest"],
        "writer_version": readset["writer_version"],
        "writer_id": readset["writer_id"],
        "commit_receipt_id": readset["commit_receipt_id"],
        "adp019_admission_receipt": ADP019_ADMISSION_RECEIPT_ABSENT,
        "adp019_owner": "V3 External Admission Court",
        "e2_performed": E2_PERFORMED,
        "native_actor_admitted": False,
        "route_probability": None,
        "selection_weight": None,
        "scientific_grade": "SOURCEFREE_TEST_ONLY_EVENT_INGRESS",
    }
