# 09 — Independent review request and exact output head

## Status

**Review not yet performed.** This is a request and acceptance contract, not a review result. No independent hostile whole-record review has been run on the fan-in. The fan-in stage is `HQ_FANIN_DRAFT_COMPLETE_INDEPENDENT_REVIEW_PENDING`; `goal_complete` is false.

## Named reviewer

**Reviewer job:** `pyat777-hq-fanin-independent-hostile-whole-record-review-r1`.
**Reviewer type:** independent nonauthor, hostile whole-record reviewer. Must be a distinct session from every C1–C6 author and every C1–C6 reviewer. Must not be the HQ fan-in author. Must not have write authority in the fan-in lease. Model/effort must be verified on the actual next turn; the commission target is DeepSeek V4.1 Flash MAX or a qualified higher-reasoning reviewer if the user explicitly authorizes a switch. No silent harness/host/model/effort change.
**Review lease:** a separate `C7_HQ_FANIN_INDEPENDENT_REVIEW/` directory only; no edits to `00`–`10`, `CHECKPOINT.json`, C1–C6 returns, production code, tests, HQ, peer or protected state.

## Exact output head to review

**Fan-in content head:** `ad4fe3c9cd67eed5bc79644bb399a7090846a8fe` (the commit containing deliverables 00–10 and CHECKPOINT).
**Branch head:** the metadata-only commit on top of the content head; verify with `git rev-parse HEAD` and `git ls-remote origin refs/heads/agent/pyat-hq-pre-forge-to-prev3-authority-severance-functional-adequacy-20261107-r1`. The content under review is the content head; the branch head changes only `09`/`CHECKPOINT.json` metadata.
**Prepared branch:** `agent/pyat-hq-pre-forge-to-prev3-authority-severance-functional-adequacy-20261107-r1`.
**Preparation base observed at intake:** `e2fdd975f618228ecc4e146840cb0eed2091a20f`.
**Protected source observation:** `7a5429ffbc48efd25e28c912da80c822e66bc182`.
**Fan-in lease:** `WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/` — deliverables `00`–`10` and `CHECKPOINT.json` only.

## Exact inputs the reviewer must read

### Fan-in deliverables

- `00_EXECUTIVE_REAL_OPERATIONS_AND_VERDICT.md`
- `01_LEGACY_SELECTED_AUTHORITY_USE_AND_INCOMPLETE_CALLEE_COVERAGE.tsv`
- `02_CURRENT_IMPLEMENTATIONS_PRE_FORGE_VS_WHOLE_PREV3.tsv`
- `03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl`
- `04_PROVED_EQUIVALENCES_AND_NO_BUILD_DECISIONS.md`
- `05_SEVERED_OR_INCOMPLETE_MINIMAL_OWNER_REPAIRS.tsv`
- `06_REAL_LOCAL_TEST_COMMANDS_OUTPUT_HASHES_AND_MUTATIONS.md`
- `07_SECONDARY_AGENDA_NON_DROP_AND_WORKER_COLLISION.md`
- `08_COVERAGE_DENOMINATORS_COLD_HANDOFF.tsv`
- `09_INDEPENDENT_REVIEW_REQUEST_AND_EXACT_HEAD.md`
- `10_HQ_PRIORITY_AND_NEXT_WORK.md`
- `CHECKPOINT.json`

### C1–C6 author returns and independent reviews

| Lane | Worktree / branch / cut | Author return | Independent review |
|---|---|---|---|
| C1 | `pyat777-source-consumer` / `agent/pyat777-source-consumer-20261107-r1` @ `451f8d1e094800d523589cdd4db5159a338db836` | `C1_SOURCE_CONSUMER/00_RETURN.md`, `01_CASES.jsonl`, `02_CASES.tsv`, `03_TEST_RECEIPTS.md`, `04_MINIMAL_OWNER_ACTIONS.tsv`, `05_REGISTER_ANTIJOIN.tsv`, `06_REPORTING_CORRECTIONS.md` | `753ff5dc95fb218f84ebf1697a91a2d392367f2c` — `C1_INDEPENDENT_REVIEW/00_REVIEW.md`, `01_FINDINGS.jsonl`, `02_COMMANDS_AND_EVIDENCE.md` |
| C2 | `pyat777-joint-consumer` / `agent/pyat777-joint-consumer-20261107-r1` @ `0d548b033a0a20c9738fa4a3412ba5acd01217c5` | `C2_JOINT_CONSUMER/00_RETURN.md`, `01_CASES.jsonl`, `02_CASES.tsv`, `03_TEST_RECEIPTS.md`, `04_MINIMAL_OWNER_ACTIONS.tsv`, `05_REGISTER_ANTIJOIN.tsv`, `06_REPORTING_CORRECTIONS.md` | `638f75e7b661057954f7dbd3b58739b83ec2e8e1` — `C2_INDEPENDENT_REVIEW/00_REVIEW.md`, `01_FINDINGS.jsonl`, `02_COMMANDS_AND_EVIDENCE.md`, `03_PROBE_REPLAY.json` … `09_PROBE_DIFF.txt` |
| C3 | `pyat777-ff-postff-consumer` / `agent/pyat777-ff-postff-consumer-20261107-r1` @ `3fd285d671d51c8576fd2b962bc34eda1a714ece` | `C3_FF_POSTFF_CONSUMER/00_RETURN.md`, `01_CASES.jsonl`, `02_CASES.tsv`, `03_TEST_RECEIPTS.md`, `03a/03b` logs, `04_MINIMAL_OWNER_ACTIONS.tsv`, `05_REGISTER_ANTIJOIN.tsv`, `06_HASH_AND_SOURCE_MANIFEST.tsv`, `07_REPORTING_CORRECTIONS.md` | `aa122437b1fe224f4c6ea2ee31ed2f7de6af7323` — `C3_INDEPENDENT_REVIEW/00_REVIEW.md`, `01_FINDINGS.jsonl`, `02_COMMANDS_AND_EVIDENCE.md`, logs/probes |
| C4 | `pyat777-joint-consumer` / `agent/pyat777-joint-consumer-20261107-r1` @ `0d548b033a0a20c9738fa4a3412ba5acd01217c5` | `C4_J_ROLE_FIRST_CONSUMER/00_RETURN.md`, `01_CASES.jsonl`, `02_CASES.tsv`, `03_TEST_RECEIPTS.md`, `04_MINIMAL_OWNER_ACTIONS.tsv`, `05_REGISTER_ANTIJOIN.tsv`, `06_REPORTING_CORRECTIONS.md` | `0def1171f8f9d2681b64ebe287adb7d209c896c7` — `C4_INDEPENDENT_REVIEW/00_REVIEW.md`, `01_FINDINGS.jsonl`, `02_COMMANDS_AND_EVIDENCE.md`, `03_CALLER_AND_REGISTRATION_SEARCH.txt`, `04_SOURCE_PINS.txt`, `05_M1_REGISTRATION_AND_CALLTHROUGH.txt` |
| C5 | `pyat777-source-consumer` / `agent/pyat777-source-consumer-20261107-r1` @ `451f8d1e094800d523589cdd4db5159a338db836` | `C5_SOURCE_ESTATE_PRODUCER_CONSUMER/00_RETURN.md`, `01_CASES.jsonl`, `02_CASES.tsv`, `03_TEST_RECEIPTS.md`, `04_MINIMAL_OWNER_ACTIONS.tsv`, `05_REGISTER_ANTIJOIN.tsv`, `06_ALL35_SOURCE_DISPOSITIONS.tsv`, `07_REPORTING_CORRECTIONS.md` | `ea9ff9e54e2bc7c9a56a1398d172e87a8f109f03` — `C5_INDEPENDENT_REVIEW/00_REVIEW.md`, `01_FINDINGS.jsonl`, `02_COMMANDS_AND_EVIDENCE.md`, logs/probes |
| C6 | `pyat777-joint-consumer` / `agent/pyat777-joint-consumer-20261107-r1` @ `0d548b033a0a20c9738fa4a3412ba5acd01217c5` | `C6_HISTORICAL_SELECTED_USE/00_RETURN.md`, `01_HISTORICAL_SELECTED_USE_CASES.jsonl`, `02_LEGACY_AUTHORITY_CALLSITE_COVERAGE.tsv`, `03_AUTHORITY_RELEASE_USAGE.tsv`, `04_UNPROVED_SELECTIONS_AND_MINIMUM_EVIDENCE.tsv`, `05_COMMANDS_AND_RETENTION_CHECKS.md`, `06_REPORTING_CORRECTIONS.md` | `333ade4e4c003595630d7f53eaeece85902d6759` — `C6_INDEPENDENT_REVIEW/00_REVIEW.md`, `01_FINDINGS.jsonl`, `02_COMMANDS_AND_EVIDENCE.md`, logs/scripts |

### HQ inputs

- `GOAL.md`, `STANDING_DISCIPLINES.md`, `SECONDARY_AGENDA_FROZEN.jsonl`, `CHECKPOINT.json`, `FLIGHT_BOARD.json`.
- `P0_INPUT_REGISTER_INDEX.json`, `P0_FRONTIER.json`, `P0_EXISTING_WORKTREES.json`, `P0_CANDIDATE_REFS.json`, `P0_HQ_DISPATCH_RECEIPT.json`.
- `P1_SOURCE_REGISTER_ROWS.jsonl` (154 rows), `P1_HISTORICAL_ESTATE_AND_CALLSITE_ROWS.jsonl` (1608 rows), `P1_REGISTER_GRAPH.json`, `P1_UNMATCHED_CASE_ANTIJOIN.tsv`, `P1_HISTORICAL_ESTATE_INDEX.json`, `P1_IMPORT_AND_GRAPH_CHECKS.json`, `P1_SOURCE_RETENTION_AND_UNMATCHED_NOTE.md`.
- `C1_RETURN_INTAKE.json`, `C1_REVIEW_INTAKE.json`, `C1_CORRECTION_INTAKE.json`, `C2_RETURN_INTAKE.json`, `C2_REVIEW_INTAKE.json`, `C2_CORRECTION_INTAKE.json`, `C3_RETURN_INTAKE.json`, `C3_REVIEW_INTAKE.json`, `C4_RETURN_INTAKE.json`, `C4_REVIEW_INTAKE.json`, `C4_CORRECTION_INTAKE.json`, `C5_INTAKE.json`, `C6_INTAKE.json`.

## Source-vs-execution limits the reviewer must enforce

- **S0/S1 documentary:** historical release metadata, selected version/SHA/locator, row rules, A02 statuses, issuer holds. These are **not** execution.
- **S2 local sourcefree:** synthetic nonrespondent fixtures, sourcefree tests, fixture builds, static source inspection. These are **not** original respondent/native execution and **not** current native issuer.
- **S3 native/original:** **not run** in C1–C6 or this fan-in. No original respondent/SAV/DTA/DB read; no original35 issuance; no science/actor authority.
- **No actual historical six-stage invocation** for the 29 functions/58 releases; all 581 R1 rows `RUNTIME_EXECUTED=NO`.
- **No current native issuer** for AR-0033, J, R157/original35, structural or actor cases; A02 recorded decisions are not the original signer.
- **No protected merge**; no production/existing-test/HQ/peer write in this lease.
- **No CI waiver**: FIABC 144 pass/3 fail and R09 provenance remain; #774 Q86 open; GF1 #691 test-only/unmerged.
- **No whole-#777 completion**; 17 secondary gates remain open.

## Acceptance gates for the independent review

The reviewer must issue a hostile whole-record verdict against all of the following. A failure of any gate is a finding, not a reason to silently repair outside the review lease.

1. **Completeness of attempted functions.** All 51 C1–C6 case records are present and typed; all 29 F1 functions, 30 #748 responsibilities, 26 FF functions, 16 FF dependencies, 15 post-FF mechanisms and 11 post-FF seams are accounted for without silent loss.
2. **No denominator drop or false sum.** 29/58/228/581/687, 42/16, 15/8/7/10/3, 26/16, 15/11, 58, 27/9, 154 and 1608 are preserved separately; overlapping registers are not summed.
3. **Frozen taxonomy.** Every `03` record carries a frozen-taxonomy verdict or a typed hold; no invented verdict; `UNKNOWN`/`UNPROVED`/`NOT_RUN` preserved.
4. **No false green.** No proved severance, no full historical equivalence, no native/S3/science/actor/N11/N12 claim, no CI waiver, no whole-#777 completion.
5. **Forward and reverse walks.** Each case has a forward selected-document/callsite→current-consumer walk and a reverse current-operation→required-authority/owner walk, or an explicit hold.
6. **Exact evidence.** Selected version/SHA/row/negative and current owner/first consumer are exact where claimed; absent evidence is named, not guessed.
7. **No unjustified rebuild.** No Pre-Forge duplication of FF, no generic FF engine, no old J registry/compiler/cache, no `source_configuration` rebuild, no AR-0033 runtime reload, no weight=1 default, no new authority gate.
8. **Repair minimality.** Every `05` repair row distinguishes first missing wiring edge vs missing function vs issuer-only vs intentional no-need, with exact owner/file/ABI and go/no-go.
9. **Agenda preservation.** All 17 frozen gates are present with current status; no closure pretense; collision boundary respected.
10. **Exact head and independence.** The reviewed head is the exact fan-in commit; reviewer is a distinct nonauthor session; no write outside the review lease.

## Reviewer commands (read-only)

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq
git fetch origin
git rev-parse HEAD
git ls-remote origin refs/heads/agent/pyat-hq-pre-forge-to-prev3-authority-severance-functional-adequacy-20261107-r1
sha256sum WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/0*
python3 - <<'PY'
import json
for i,l in enumerate(open('WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl'),1):
    r=json.loads(l)
    assert r['case_id'] and r['frozen_taxonomy_verdict']
print('03 records OK')
PY
```

For the C1–C6 reviews at cuts, use `git -C <worktree> show <review-cut>:<path>`; do not rely on prose alone. The exact review cuts are listed above.

## Requested review verdict format

The reviewer must return, in its own lease:

- `00_REVIEW.md` — hostile whole-record verdict, supported claims, rejected inferences, exact defects, scope limits.
- `01_FINDINGS.jsonl` — one finding per defect/acceptance gate, with severity, exact file/line/record, evidence, required correction.
- `02_COMMANDS_AND_EVIDENCE.md` — exact read-only commands, hashes, counts and any independent spot checks.
- `03_REVIEW_COMMIT.txt` — review commit and remote readback.
- No edits to the fan-in lease, C1–C6 returns, production code, tests, HQ, peer or protected state.

**This review has not been performed. The fan-in is not accepted until the independent hostile whole-record review returns and its findings are adjudicated.**
