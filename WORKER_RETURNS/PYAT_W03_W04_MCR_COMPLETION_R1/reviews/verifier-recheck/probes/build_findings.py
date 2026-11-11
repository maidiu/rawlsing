#!/usr/bin/env python3
"""Build focused CC-F05 verifier recheck findings JSONL."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent

COUNTS = {
    "reviewed_head": "6658b630f114186099177cbdaf00cab854b18b09",
    "prior_review": "07c172683c4a720b8d1c37599c3e09a5357e56d8",
    "author_candidate": "df32985387da3da26f587ddbcd75ad031b837773",
    "integrated_candidate": "09f97a3a4c77ed7666ee95af586cfdfd91493f73",
    "verifier_tests": "4 passed",
    "validator_self_test": "PASS; 32 negative mutations rejected",
    "launch_validate": "PASS; 12 obligations",
    "frozen_original_validate": "RED_INVALID_FOR_DISPATCH (historical; preserved)",
    "original_file_sha256": "ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166",
    "wrapper_block_sha256": "1e7d6a905bb702c289708d636627625759cee38f883851c60a502126f5b47583",
    "contract_blocks_equal": True,
    "scalar_set_matches_tsv_cut": True,
    "composite_branch_preserved": True,
    "cli_positive_external": "READY_FOR_INDEPENDENT_RECEIVING; exit 0",
    "cli_tracked": "RED_INCOMPLETE; exit 2; MCR_C_EVIDENCE_TRACKED_AT_CANDIDATE",
    "cli_path_text_mismatch": "RED_INCOMPLETE; exit 2",
    "api_tracked": "RED_INCOMPLETE; MCR_C_EVIDENCE_TRACKED_AT_CANDIDATE",
    "api_symlink_to_tracked": "RED_INCOMPLETE; MCR_C_EVIDENCE_TRACKED_AT_CANDIDATE",
    "api_missing_id": "RED_INCOMPLETE; MCR_C_MISSING_PROOF_OBL-B",
    "api_extra_id": "RED_INCOMPLETE; MCR_C_UNCONTRACTED_PROOF_OBL-EXTRA",
    "api_bad_grade": "RED_INCOMPLETE; MCR_C_INSUFFICIENT_EVIDENCE_GRADE_OBL-A",
    "api_no_path": "RED_INCOMPLETE; MCR_C_EVIDENCE_EXTERNALITY_UNVERIFIED",
    "api_copy_outside": "READY under documented repository-tracking-only boundary",
    "api_path_text_mismatch": "READY_FOR_INDEPENDENT_RECEIVING (defect)",
    "proof_gate_author_range": "MECHANICAL_PROOF_GATE_PASS; no verifier-test sidecar required",
    "proof_gate_full_range": "RED only on pre-existing bench integration sidecar (CC-F04 queued)",
    "final_12id_or_economic": "NOT_RUN",
    "100k": "NOT_RUN",
}

HASHES = {
    "validator_blob": "1cdd3e70acd65b6056fd5a7a153c1aba33a7d26e",
    "validator_sha256": "c0b8a53a3a0c7b64f3cb071c454cbbe29d5171156f7faff65fe1b2f6b3f5544a",
    "test_blob": "6994a3356d0c62e34fcf9c5c184a299fa97fd185",
    "test_sha256": "5aa78c0aef8eae26516549e99ed7e88a17a5eb4c8ec81db96a5e1c7562bf735d",
    "launch_blob": "b30926e911b9ccdc4b86e23e76ed9a4c08d2a2a2",
    "launch_sha256": "c25dbb96259971a8f623179dd1435bcdc2d684edb2b02a4970565bbb0c5c25e7",
    "frozen_commission_blob": "47faaf3d115c213de2319f8123d4ac17d4d1cf8e",
    "frozen_commission_sha256": "ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166",
    "contract_block_sha256": "1e7d6a905bb702c289708d636627625759cee38f883851c60a502126f5b47583",
}

FINDINGS = [
    {
        "FINDING_ID": "CCF5-R01",
        "SEVERITY": "P2",
        "STATUS": "REPAIR_REQUIRED",
        "SUBJECT": "verify_return API does not bind evidence text to returned_path",
        "FILE_OR_RECORD": "CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py:331-340,716-720; logs/verifier_probe.stdout.json",
        "EVIDENCE": "Synthetic existing-fixture probe: validator.verify_return(commission, valid_evidence_text, candidate, repo, returned_path=external_junk_file) returns READY_FOR_INDEPENDENT_RECEIVING with errors=[]. The path is outside/untracked and the separately supplied text is valid; the API never reads or compares the path text. The CLI is bound: main() reads args.verify_return.read_text() and the same external junk path returns RED_INCOMPLETE (exit 2). The 4 new tests use consistent text/path and do not cover this mismatch. API no-path, tracked, symlink-to-tracked, missing proof ID, extra proof ID and bad grade all reject; CLI tracked rejects.",
        "MINIMUM_EXACT_REPAIR": "In verify_return, read returned_path and require its text to equal returned, or simplify the API to accept returned_path only and derive the text; add MCR_C_EVIDENCE_TEXT_PATH_MISMATCH/equivalent RED and one focused mismatch test. Do not weaken tracked/candidate/forged/digest/no-drop/grade checks, add a new signer, or create a new checker. No wrapper/contract change is needed.",
        "LIMIT": "CLI is not affected; this is the public API path/text binding only.",
    },
    {
        "FINDING_ID": "CCF5-P01",
        "SEVERITY": "INFO",
        "STATUS": "PASS",
        "SUBJECT": "Frozen contract preservation, exact wrapper block, original RED and wrapper PASS",
        "FILE_OR_RECORD": "PYAT_W03_W04_MCR_C_Commission.md; WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md; logs/contract_identity_scalar.log; logs/frozen_contract_red.log; logs/launch_validate.log",
        "EVIDENCE": "Original frozen file SHA-256 ddc6273...; git diff intake..HEAD for it is empty. Extracted original MCR block and wrapper MCR block are byte-identical, SHA-256 1e7d6a90...; 1 scope/12 obligations/1 receiving. Original literal command remains RED_INVALID_FOR_DISPATCH (historical, not relabeled); wrapper validates PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH with 12 obligations and the same contract hash. Runtime addendum selects the existing OpenCode Go DeepSeek V4.1 Flash MAX; no new obligation, source, grade, no-drop rule, receiving requirement, signer or approval gate.",
        "MINIMUM_EXACT_REPAIR": "None.",
        "LIMIT": "Wrapper validation is structural; not whole-MCR execution.",
    },
    {
        "FINDING_ID": "CCF5-P02",
        "SEVERITY": "INFO",
        "STATUS": "PASS_WITH_CCF5_R01_API_EXCEPTION",
        "SUBJECT": "CLI/negative checks and scalar/composite identity correction",
        "FILE_OR_RECORD": "CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py; CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py; logs/verifier_probe.stdout.json; logs/composite_scalar_branch.log",
        "EVIDENCE": "CLI positive external evidence READY (exit 0); CLI tracked evidence RED (exit 2); CLI external junk path RED (exit 2) proving CLI text/path binding. API tracked and symlink-to-tracked RED; API missing/extra proof IDs and bad grade RED; no-path RED. New tests 4 passed; existing self-test PASS with 32 negative mutations. Actual frozen TSV enumerator: _expected_id_set returns 12 raw IDs exactly matching cut -f1 (no JSON brackets). Composite len>1 branch remains old canonical JSON: synthetic two-column source returns [\"A1\",\"B1\"]/[\"A2\",\"B2\"]. Old checker negatives remain green.",
        "MINIMUM_EXACT_REPAIR": "None beyond CCF5-R01 API mismatch.",
        "LIMIT": "No full MCR/economic acceptance.",
    },
    {
        "FINDING_ID": "CCF5-L01",
        "SEVERITY": "INFO",
        "STATUS": "QUALIFIED_RESIDUAL",
        "SUBJECT": "Repository tracking exclusion is not wall-clock/PR provenance",
        "FILE_OR_RECORD": "WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/mcr/VERIFIER_R1/03_EXTERNAL_EVIDENCE_BOUNDARY.md; logs/verifier_probe.stdout.json",
        "EVIDENCE": "Author explicitly labels evidence_externality_scope REPOSITORY_TRACKING_ONLY__NO_TIMESTAMP_OR_STRONGER_PROVENANCE. A copy outside the candidate root is accepted as external under this rule (api_copy_outside READY); a symlink resolving to tracked candidate evidence is rejected. The author does not claim wall-clock postcommit or PR origin; this is a documented consequential residual. No new signer/approval gate was invented.",
        "MINIMUM_EXACT_REPAIR": "None for this scope; final receiving must still treat external provenance as repository-tracking-only.",
        "LIMIT": "Copy of tracked evidence outside the candidate would pass tracking exclusion; provenance/time remains unproven.",
    },
    {
        "FINDING_ID": "CCF5-L02",
        "SEVERITY": "INFO",
        "STATUS": "QUEUED_OUTSIDE_SCOPE",
        "SUBJECT": "Existing bench proof sidecar remains CC-F04 queued",
        "FILE_OR_RECORD": "logs/proof_gate_lint_verifier.log; logs/proof_gate_changed_verifier_author.log; logs/proof_gate_changed_verifier.log",
        "EVIDENCE": "New verifier test AST lint passes; changed proof gate over the author repair range passes MECHANICAL_PROOF_GATE_PASS with 0 witness contracts, so no verifier-test sidecar is required/waived. A full 26f70635e..6658b630f changed run remains RED only on pre-existing rawlsing_next/tests/test_bench_w03_w04_physical.py missing its .proof.json; that is CC-F04 queued to the bench owner, not a verifier-test waiver.",
        "MINIMUM_EXACT_REPAIR": "Bench owner must add the CC-F04 sidecar; not part of this review.",
        "LIMIT": "No proof gate full-range PASS is claimed.",
    },
    {
        "FINDING_ID": "CCF5-L03",
        "SEVERITY": "INFO",
        "STATUS": "BOUNDARY",
        "SUBJECT": "No final 12-ID/economic/source/native acceptance",
        "FILE_OR_RECORD": "CC-F05 scope",
        "EVIDENCE": "No final RECEIVING_EVIDENCE.md, delivered_ids, 12 same-head PASS package, postcommit block, whole 12-ID or economic/100k, original35/SAV/DTA/DB/source bytes, native/S3/science/actor effect, install, protected merge, CI waiver, new engine/worker or model/provider/account/effort change. Prior W04 F01/F02/F03 and CC-F01 remain accepted and are not reopened. CC-F02 economic-method, CC-F03/F04 bench/workflow proof and final same-SHA both-receiver code/economic receiving remain pending.",
        "MINIMUM_EXACT_REPAIR": "Final both receivers must share the final immutable code/economic SHA with full 12-ID/external MCR proof.",
        "LIMIT": "REVISE at CC-F05 scope is not whole W03/W04 acceptance.",
    },
]


def main() -> int:
    records = [{"RECORD_TYPE": "FINDING", **f, "COUNTS": COUNTS, "HASHES": HASHES} for f in FINDINGS]
    records.append({
        "RECORD_TYPE": "VERIFICATION",
        "VERDICT": "REVISE",
        "STATUS": "CCF5_R01_API_BINDING_REQUIRED",
        "REVIEWED_HEAD": COUNTS["reviewed_head"],
        "AUTHOR_CANDIDATE": COUNTS["author_candidate"],
        "INTEGRATED_CANDIDATE": COUNTS["integrated_candidate"],
        "COUNTS": COUNTS,
        "HASHES": HASHES,
        "REPAIR_FINDINGS": ["CCF5-R01"],
        "PASS_SCOPE": ["frozen contract preservation", "exact wrapper block", "original RED historical", "wrapper 12-ID structural PASS", "CLI evidence binding", "tracking negatives", "scalar/composite identity", "4 tests/32 self-test mutations"],
        "OUTSIDE_SCOPE": ["CC-F02", "CC-F03", "CC-F04", "whole 12-ID", "economic/100k", "final receiving"],
        "BOUNDARY": "Focused CC-F05 verifier/artifact review only; no final 12-ID/economic/source/native/protected acceptance.",
    })
    text = "\n".join(json.dumps(record, sort_keys=True) for record in records) + "\n"
    (OUT / "FINDINGS.jsonl").write_text(text, encoding="utf-8")
    print(f"wrote {len(records)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
