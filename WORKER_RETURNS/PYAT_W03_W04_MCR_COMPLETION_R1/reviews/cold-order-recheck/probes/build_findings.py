#!/usr/bin/env python3
"""Build the focused CC-F01 recheck findings JSONL."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent

COUNTS = {
    "reviewed_head": "bcc176d7719e57d1e88b7f395f0280f72b0a74c5",
    "prior_review": "07c172683c4a720b8d1c37599c3e09a5357e56d8",
    "repair_intake": "26f70635e8493c7759fa087b17da269104bd8922",
    "author_production_test_commit": "f9aedf8e2b570174881cef627dc6a24b78031ed7",
    "author_return_commit": "8f36fceb8fc518a8be03dfef6c32b4124f1d8867",
    "integration_commit": "0dc8ee923dddf75716c0e5ac227d90ca8cd1ab89",
    "focused_new_test_cases": "3 passed",
    "focused_cold_file": "18 passed",
    "author_73_receipt": "73 passed (read, not independently rerun in full)",
    "current_parity_event_sequence": True,
    "current_parity_selector_yield": True,
    "current_parity_selector_differences": 0,
    "current_parity_consumer_material": True,
    "severance_test": "3 failed by assertion under temporary unsorted source mutation",
    "severance_parity_event_sequence": False,
    "severance_parity_selector_yield": False,
    "severance_parity_selector_differences": 3,
    "source_restored": True,
    "proof_gate_lint": "PASS",
    "proof_gate_changed": "MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION",
    "sidecar_required_for_new_test": False,
    "100k_benchmark": "NOT_RUN",
    "final_12id_or_economic": "NOT_RUN",
}

HASHES = {
    "production_blob": "06eefd8fe8c1839854a783c78045b170627806f2",
    "production_sha256": "bb0093fa0ad8f19e324f2ecd01cc1faad4e690f2152f6cb7316ee91b5a033e93",
    "test_blob": "75314ade650f87c3e5aec0e17c9e31b9fe22b07c",
    "test_sha256": "675ad4d5e014e81ab3db19ab45b30d62adfc4e2b4c356630cdb8883ebe88aeaa",
    "prior_accepted_production_blob": "986f327aa18053edc61bd837cdded02bbf8388d9",
    "prior_accepted_test_blob": "8e8effa58579af0c3326ecd4af7e159947abe4ec",
    "contract_source_blob": "b17c63cea9706f50a0d9c0f0ce064e967da4c8eb",
}

FINDINGS = [
    {
        "FINDING_ID": "CCF1-R01",
        "SEVERITY": "INFO",
        "STATUS": "ACCEPT_AT_CC_F01_SCOPE",
        "SUBJECT": "Exact cold respondent-order repair verified",
        "FILE_OR_RECORD": "rawlsing_next/_pre553_w03_cold_compact.py:132-142; rawlsing_next/tests/test_pre553_w03_w04_cold.py:149-196; probes/cold_parity_probe.py",
        "EVIDENCE": "Production now sorts each respondent group's integer rows by self.event_keys[row], the frozen exact event ref key. The change only reorders _RespondentEvents rows; selectors, bodies, entries, non_events, event_states, release/replay/coverage are untouched. Current parity probe: event_sequence_parity=true, selector_yield_parity=true, selector_yield_differences=0, consumer_material_parity=true; release/replay/public-object material equal for routed-ordered-repeated, missing-optional-weight and valid-empty. New three-case test: 3 passed; full cold file: 18 passed. New test compares real _ReleaseIndex events_by_respondent ref sequences, actual _select_respondent_events yields for every native-question target, and full typed I03/I05 consumer material via CarrierNeutralResearchExecutor.",
        "MINIMUM_EXACT_REPAIR": "None. The previous review's exact requested sort is implemented and independently verified.",
        "LIMIT": "Scope is CC-F01 only; no whole W03/W04/12-ID/economic acceptance.",
    },
    {
        "FINDING_ID": "CCF1-R02",
        "SEVERITY": "INFO",
        "STATUS": "SEVERANCE_VERIFIED",
        "SUBJECT": "New parity test is assertion-meaningful; temporary source was restored",
        "FILE_OR_RECORD": "logs/severance_mutation.txt; logs/severance_new_test.log; logs/severance_parity_probe.stdout.json; logs/source_identity_after_restore.log",
        "EVIDENCE": "Temporary source mutation in this review checkout only replaced the candidate sorted expression with the exact pre-repair tuple(rows). New three-case test then failed by assertion (3 failed); parity probe then showed event_sequence_parity=false, selector_yield_parity=false, selector_yield_differences=3, consumer_material_parity=true. Restored with git checkout; production blob returned to 06eefd8f...; source status clean. Post-restore new test 3 passed; full cold file 18 passed; post-restore parity probe true/true/0/true.",
        "MINIMUM_EXACT_REPAIR": "None; no test was weakened and no source mutation remains.",
        "LIMIT": "The mutation was temporary and never committed.",
    },
    {
        "FINDING_ID": "CCF1-R03",
        "SEVERITY": "INFO",
        "STATUS": "PROOF_GATE_PASS",
        "SUBJECT": "New test satisfies existing proof-integrity gate; no sidecar required",
        "FILE_OR_RECORD": "CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py; logs/proof_gate_lint_cold.log; logs/proof_gate_changed_cold.log",
        "EVIDENCE": "Lint returns AST_LINT_PASS for test_pre553_w03_w04_cold.py. changed --base 26f70635e... --head bcc176d77... examines only the new cold test and returns MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION with zero witness contracts. The new test is not an integration-claim test requiring a .proof.json sidecar under the existing gate; no residual was quietly waived.",
        "MINIMUM_EXACT_REPAIR": "None for this test. Existing CC-F04 benchmark sidecar remains queued outside this lease.",
        "LIMIT": "Proof-gate PASS is mechanical, not scientific or whole-MCR adoption.",
    },
    {
        "FINDING_ID": "CCF1-R04",
        "SEVERITY": "INFO",
        "STATUS": "RECEIPTS_READ",
        "SUBJECT": "Author RED/GREEN and 73-test receipts read; proportionate independent focus",
        "FILE_OR_RECORD": "WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/cold/ORDER_R3",
        "EVIDENCE": "Author RED receipt: event_sequence_parity=false, selector_yield_parity=false, selector_yield_differences=3, consumer_material_parity=true. Author GREEN receipt: true/true/0/true. Author 73-test receipt: 73 passed in 15.97s; read but not independently rerun in full. Independent focused work: current parity probe GREEN for all three fixtures; new three-case test 3 passed; cold file 18 passed. No full 73 suite/matrix was rerun because the one-line repair and focused selector+yield+consumer test are proportionate.",
        "MINIMUM_EXACT_REPAIR": "None.",
        "LIMIT": "Author receipt is not independent proof; the independent focused results are recorded separately.",
    },
    {
        "FINDING_ID": "CCF1-L01",
        "SEVERITY": "INFO",
        "STATUS": "BOUNDARY",
        "SUBJECT": "No reopening of W04/CC-F02/F05 bypass/economic/final acceptance",
        "FILE_OR_RECORD": "CC-F01 review scope; frozen contract and TSV read",
        "EVIDENCE": "This recheck addresses CC-F01 only. W04 F01/F02/F03, the known cold/governed cache coupling bypass and caller path, CC-F02 economic-method work, CC-F03/F04 workflow/bench proof, and CC-F05 validator work were not reopened. No 100k benchmark, no final 12-ID/economic receiving, no original35/SAV/DTA/DB/source bytes, no native/S3/science/actor effect, no install, no protected merge, no CI waiver, no new engine/worker, no model/provider/account/effort change. Final same-SHA code/economic receiving with all 12 proof records remains pending.",
        "MINIMUM_EXACT_REPAIR": "Continue the separately owned CC-F02/CC-F05 and queued CC-F03/F04 work; final same-SHA receiving remains mandatory.",
        "LIMIT": "ACCEPT_AT_CC_F01_SCOPE is not whole W03/W04 or 12-ID acceptance.",
    },
]


def main() -> int:
    records = [{"RECORD_TYPE": "FINDING", **f, "COUNTS": COUNTS, "HASHES": HASHES} for f in FINDINGS]
    records.append({
        "RECORD_TYPE": "VERIFICATION",
        "VERDICT": "ACCEPT_AT_CC_F01_SCOPE",
        "REVIEWED_HEAD": COUNTS["reviewed_head"],
        "REPAIR_INTAKE": COUNTS["repair_intake"],
        "AUTHOR_PRODUCTION_TEST_COMMIT": COUNTS["author_production_test_commit"],
        "AUTHOR_RETURN_COMMIT": COUNTS["author_return_commit"],
        "INTEGRATION_COMMIT": COUNTS["integration_commit"],
        "COUNTS": COUNTS,
        "HASHES": HASHES,
        "ACCEPTED_SCOPE": ["CC-F01 exact cold respondent order", "real selector/yield parity", "full typed I03/I05 consumer material parity", "assertion-level severance/restoration"],
        "OPEN_OUTSIDE_SCOPE": ["CC-F02", "CC-F03", "CC-F04", "CC-F05", "whole 12-ID", "economic/final receiving", "100k matrix"],
        "BOUNDARY": "Focused CC-F01 only; no whole W03/W04/12-ID/economic/native/source/protected acceptance.",
    })
    text = "\n".join(json.dumps(record, sort_keys=True) for record in records) + "\n"
    (OUT / "FINDINGS.jsonl").write_text(text, encoding="utf-8")
    print(f"wrote {len(records)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
