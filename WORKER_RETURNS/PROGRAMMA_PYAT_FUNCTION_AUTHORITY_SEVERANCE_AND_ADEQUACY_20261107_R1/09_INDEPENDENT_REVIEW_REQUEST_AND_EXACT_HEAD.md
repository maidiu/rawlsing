# 09 — C8 independent rereview request and exact output head

## Status

**C8 rereview not yet performed.** The C7 review returned `REVISE`; the author-HQ correction (C7-001–C7-005) is applied in this lease. The corrected fan-in is **not accepted** until a distinct nonauthor C8 exact-head rereview returns. Stage: `C7_REVISE_RECEIVED__FANIN_AUTHOR_CORRECTION_READY_FOR_INDEPENDENT_REREVIEW__GOAL_FALSE`; `goal_complete=false`.

## Named reviewer

**Reviewer job:** `pyat777-hq-fanin-c8-independent-rereview-r1`.
**Reviewer type:** distinct nonauthor, exact-head, schema/lineage rereviewer. Must be a different session from every C1–C6 author/reviewer, the HQ fan-in author, and the C7 reviewer. Must not have write authority in the fan-in lease. Model/effort must be verified on the actual next turn; no silent harness/host/model/effort switch.
**Review lease:** a separate `C8_HQ_FANIN_REREVIEW/` directory only; no edits to `00`–`11`, `CHECKPOINT.json`, the canonical/alias `03`, C7, C1–C6, production code, tests, HQ, peer or protected state.
**Review scope:** **only C7-001–C7-005 plus the widened current-field/taxonomy claims.** This is a schema/lineage correctness rereview, **not** a second whole-machine source/semantic/native acceptance, not a new severance/equivalence court, and not an S3/native authorization. C8 may reuse C7 proof but must read the exact changed files.

## Exact output head to review

**Corrected content commit:** `5efb9fa33aa26e0cfb6bc7a03270e4c896411843` (the commit containing corrected `00`–`11`, `CHECKPOINT.json`, the canonical `03` and its exact-content alias).
**C8 review head:** the corrected metadata branch head on top of the content commit; verify with `git rev-parse HEAD` and `git ls-remote origin refs/heads/agent/pyat-hq-pre-forge-to-prev3-authority-severance-functional-adequacy-20261107-r1`. The branch head contains the same `00`–`11` content plus exact-head metadata; review the branch head.
**Prepared branch:** `agent/pyat-hq-pre-forge-to-prev3-authority-severance-functional-adequacy-20261107-r1`.
**Prior content head reviewed by C7:** `ad4fe3c9cd67eed5bc79644bb399a7090846a8fe`.
**Prior metadata head:** `483f2a156d2156eeed22f31efc23a05b9335219d`.
**C7 independent review SHA:** `605e1cb67156a09f9ce4c0990e572fa3fda1fdd1`.
**Preparation base observed:** `e2fdd975f618228ecc4e146840cb0eed2091a20f`.
**Protected source observation:** `7a5429ffbc48efd25e28c912da80c822e66bc182`.

## Exact inputs the C8 reviewer must read

### Corrected fan-in artifacts

- `00_EXECUTIVE_REAL_OPERATIONS_AND_VERDICT.md`
- `01_LEGACY_SELECTED_AUTHORITY_USE_AND_INCOMPLETE_CALLEE_COVERAGE.tsv`
- `02_CURRENT_IMPLEMENTATIONS_PRE_FORGE_VS_WHOLE_PREV3.tsv`
- `03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl` — **canonical required path**
- `03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl` — exact-content alias; SHA-256 equality and no-drift rule recorded in `11`/`CHECKPOINT`
- `04_PROVED_EQUIVALENCES_AND_NO_BUILD_DECISIONS.md`
- `05_SEVERED_OR_INCOMPLETE_MINIMAL_OWNER_REPAIRS.tsv`
- `06_REAL_LOCAL_TEST_COMMANDS_OUTPUT_HASHES_AND_MUTATIONS.md`
- `07_SECONDARY_AGENDA_NON_DROP_AND_WORKER_COLLISION.md`
- `08_COVERAGE_DENOMINATORS_COLD_HANDOFF.tsv`
- `09_INDEPENDENT_REVIEW_REQUEST_AND_EXACT_HEAD.md`
- `10_HQ_PRIORITY_AND_NEXT_WORK.md`
- `11_C7_CORRECTION_AND_CLOSURE.md`
- `CHECKPOINT.json`

### C7 review (immutable)

`WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C7_HQ_FANIN_INDEPENDENT_REVIEW/` at `605e1cb67156a09f9ce4c0990e572fa3fda1fdd1`:

- `00_REVIEW.md`
- `01_FINDINGS.jsonl`
- `02_COMMANDS_AND_EVIDENCE.md`
- `03_REVIEW_COMMIT.txt`

### C1–C6 returns/reviews

The C1–C6 author cuts and independent review cuts are unchanged from the prior fan-in:

| Lane | Author/correction cut | Review cut |
|---|---|---|
| C1 | `451f8d1e094800d523589cdd4db5159a338db836` | `753ff5dc95fb218f84ebf1697a91a2d392367f2c` |
| C2 | `0d548b033a0a20c9738fa4a3412ba5acd01217c5` | `638f75e7b661057954f7dbd3b58739b83ec2e8e1` |
| C3 | `3fd285d671d51c8576fd2b962bc34eda1a714ece` | `aa122437b1fe224f4c6ea2ee31ed2f7de6af7323` |
| C4 | `0d548b033a0a20c9738fa4a3412ba5acd01217c5` | `0def1171f8f9d2681b64ebe287adb7d209c896c7` |
| C5 | `451f8d1e094800d523589cdd4db5159a338db836` | `ea9ff9e54e2bc7c9a56a1398d172e87a8f109f03` |
| C6 | `0d548b033a0a20c9738fa4a3412ba5acd01217c5` | `333ade4e4c003595630d7f53eaeece85902d6759` |

## C7 5/5 closure mapping the C8 reviewer must verify

| C7 finding | Required correction | Corrected evidence |
|---|---|---|
| **C7-001** | All 29 C6 A–J field `I` typed current grade; historic A02 status preserved separately; no authority promotion | `03` C6 records: `I = CURRENT_SELECTED_ISSUER_UNPROVED; CURRENT_NATIVE_NOT_RUN; CURRENT_SCIENTIFIC_AUTHORITY_NOT_PROVED; ...`; `historical_a02_status` 29/29; `historical_a02_status_source`; `current_grade` object; 02/04/05/CHECKPOINT synchronized |
| **C7-002** | GF1 frozen taxonomy not `IMPLEMENTATION_NOT_CURRENTLY_ADEQUATE`; retain candidate/unmerged/no-defect | `03` C3-FF-04 `frozen_taxonomy_verdict=NOT_RUN`; `exact_hold=UNPROVED_SELECTION_AND_EQUIVALENCE__TEST_ONLY_UNMERGED_CANDIDATE__NO_SELECTED_NON_TEST_DEMAND__NO_DEFECT_PROVED`; `gf1_status`; 02/04/05/00/CHECKPOINT synchronized |
| **C7-003** | All 19 historical-only labels audited; no five-test retirement pretense; preserve genuine evidence; audit 10 current labels | 19/19 retyped `NOT_RUN`/`DEMAND_UNPROVED`; `historical_evidence_class` for F07/F22/F23/F25; `retirement_proof=NOT_PROVIDED__FIVE_TEST_COURT_NOT_RUN`; 10 current labels: 7 exact current generic refs + 3 `UNPROVED_CURRENT_SELECTION` |
| **C7-004** | 05 C6 owner/ABI is documentary locator, not exact current ABI; 02 C6 current fields separated | 05: `OWNER_FILE_OR_ABI=UNKNOWN_NOT_PROVED`, `DOCUMENTARY_EVIDENCE_LOCATOR` preserved 29/29, `CURRENT_OWNER_FILE_OR_ABI` 7 exact + 22 UNKNOWN, `CURRENT_FIRST_READER` 7 exact + 22 UNKNOWN; 02: `HISTORICAL_READER`/`HISTORICAL_A02_METADATA` separated from `CURRENT_OWNER`/`CURRENT_FIRST_CONSUMER`, field-class columns added |
| **C7-005** | Required 03 filename present or governed alias with SHA-256 equality/no-drift | canonical `03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl`; alias `03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl`; SHA-256 equality `9b36b050eb3688d1b5db1efa79ba24a0241520e0b2e51881050d4d20ccb6f049` at correction; single canonical pointer/no-drift rule |

## Source-vs-execution limits the C8 reviewer must enforce

- **S0/S1 documentary:** historical release metadata, selected version/SHA/locator, A02 status, issuer holds. Not execution.
- **S2 local sourcefree:** synthetic nonrespondent fixtures, sourcefree tests, fixture builds, static source inspection. Not original respondent/native execution, not current native issuer.
- **S3 native/original:** **not run** in C1–C7 or this correction. No original respondent/SAV/DTA/DB read; no original35 issuance; no science/actor authority.
- **No actual historical six-stage invocation** for the 29/58; all 581 R1 rows `RUNTIME_EXECUTED=NO`.
- **No current native issuer** for AR-0033, J, R157/original35, structural or actor cases; A02 recorded decisions are not the original signer.
- **No protected merge**; no production/existing-test/HQ/peer write in this lease.
- **No CI waiver**: FIABC 144 pass/3 fail and R09 provenance remain; #774 Q86 open; GF1 #691 test-only/unmerged.
- **No whole-#777 completion**; 17 secondary gates remain open.

## C8 acceptance gates

1. **C7 5/5 closure:** every C7 finding has the exact corrected evidence above; no finding is papered over.
2. **51-case integrity:** `02`/`03`/`05` each contain exactly 51 unique case IDs, families 1/2/10/2/7/29, no extra/drop; `02` keeps 26 FF, 16 FF dependencies, 15 post-FF mechanisms, 11 seams, 30 #748 owner rows; `05` 51 rows.
3. **C7-001:** all 29 C6 `I` fields are typed current grades; `historical_a02_status` preserved 29/29; no original signer/current operation inferred; `current_native_distinction` and first-readers preserved.
4. **C7-002:** GF1 is `NOT_RUN`/typed unmerged-candidate hold; candidate exists; PR #691 unmerged; not runtime-selected; no defect proved; taxonomy totals 0 `IMPLEMENTATION_NOT_CURRENTLY_ADEQUATE`.
5. **C7-003:** 19/19 historical-only labels withdrawn to `NOT_RUN`/`DEMAND_UNPROVED`; genuine historical evidence preserved by `historical_evidence_class`; 10 current labels audited (7 exact current generic refs, 3 `UNPROVED_CURRENT_SELECTION`); no retirement or operational-currentness claim.
6. **C7-004:** all 29 C6 `05` rows separate `CURRENT_OWNER_FILE_OR_ABI`/`CURRENT_FIRST_READER` from `DOCUMENTARY_EVIDENCE_LOCATOR`; 7 exact current refs + 22 `UNKNOWN_NOT_PROVED`; `02` separates historical readers/A02 metadata from current owner/first consumer.
7. **C7-005:** canonical `03` and exact-content alias have SHA-256 equality, one canonical pointer and a no-drift rule; no two-study claim.
8. **Taxonomy:** 21 `FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED`, 30 `NOT_RUN`, 0 `HISTORICAL_ONLY_OR_NO_JUSTIFIED_CURRENT_CONSUMER`, 0 `IMPLEMENTATION_NOT_CURRENTLY_ADEQUATE`.
9. **Denominators:** 29/58/228/581/687, 42/16, 15/8/7/10/3, 26/16, 15/11, 58, 27/9, 154/1608 remain separate; no magic sum.
10. **No false green:** no proved severance, no full historical equivalence, no native/S3/science/actor/N11/N12, no CI waiver, no whole-#777 completion; `goal_complete=false`; C8 rereview is not acceptance.
11. **Exact head/independence:** corrected content head exact; metadata branch head verified; C8 reviewer distinct nonauthor; no write outside C8 lease.

## Reviewer commands (read-only)

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq
git fetch origin
git rev-parse HEAD
git ls-remote origin refs/heads/agent/pyat-hq-pre-forge-to-prev3-authority-severance-functional-adequacy-20261107-r1
shasum -a 256 WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl \
              WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl
python3 - <<'PY'
import json
p='WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl'
rows=[json.loads(l) for l in open(p)]
assert len(rows)==51 and len({r['case_id'] for r in rows})==51
for r in rows:
    assert r['frozen_taxonomy_verdict'] in ('FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED','NOT_RUN')
    assert r.get('forward_walk') and r.get('reverse_walk') and r.get('exact_hold')
print('51-case schema OK')
PY
```

For C7, use `git show 605e1cb67156a09f9ce4c0990e572fa3fda1fdd1:.../C7_HQ_FANIN_INDEPENDENT_REVIEW/...`. Do not rely on prose alone.

## Requested C8 verdict format

The C8 reviewer must return, in its own lease:

- `00_REVIEW.md` — exact-head schema/lineage verdict on C7-001–005 plus widened current-field/taxonomy claims; supported/rejected; no whole-machine acceptance.
- `01_FINDINGS.jsonl` — one finding per gate/defect, severity, exact file/record/line, evidence, required correction.
- `02_COMMANDS_AND_EVIDENCE.md` — exact read-only commands, hashes, counts, independent spot checks.
- `03_REVIEW_COMMIT.txt` — review commit and remote readback.
- No edits to the fan-in lease, canonical/alias `03`, C7, C1–C6, production code, tests, HQ, peer or protected state.

**C8 rereview not yet performed. The corrected fan-in is not accepted until C8 returns and its findings are adjudicated. Whole #777 remains incomplete.**
