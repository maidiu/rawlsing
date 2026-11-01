# TERMINAL LEDGER PRECHECK — RRIF-F0

## 1. Scope

This is a documentary precheck of the existing 34-lineage terminal candidate ledger. It is not a new historical census, not a new RRIF-C/D reconciliation, and not a terminal acceptance.

- Commissioned ledger branch: `research/pyat-rrif-hq-d1d5-intake-20261031-r1`
- Commissioned exact cut: `d80901e9de78803c031fa9d25146f7d8b6aeba2c`
- Live branch head observed: `75eb695ad27652020f9ffc0363f846a7c85ca758`
- Live head delta: exactly one added document, `PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/HQ_D1_D5_INTAKE_R1/06_E4F_RETURN_AND_FINAL_REVIEW_GATE.md` (21 insertions). The commissioned 34-ledger and 30-intake files are unchanged between `d80901e9` and `75eb695`.
- Original RRIF-C source cut for counts and validator: `b75addf621c3a6c1a3b196bd92a810fad77ae3ae`
- PRE-MAIN canonical: `8e44ca9c751049d65e6def47600b5c073ee04b29`
- The independent E4FR return `7cd2206f` and E6 return `b0f7675b` are outside this HQ ledger cut. They are not ledger acceptance and do not change the terminal decision.

No branch-name recensus was run. The check reads already-existing RRIF-C and HQ ledger/validator artifacts.

## 2. Files read

From `d80901e9`:

- `PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/HQ_D1_D5_INTAKE_R1/03_THIRTY_FOUR_GROUP_TERMINAL_CANDIDATES.jsonl`
- `PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/HQ_D1_D5_INTAKE_R1/01_THIRTY_LINEAGE_HQ_INTAKE.jsonl`

From `b75addf`:

- `WORKER_RETURNS/RRIF-C-POST-GAP-LINEAGE-REDUCTION-20261031-R1/DENOMINATOR_AND_DEDUP_VALIDATION.json`
- `WORKER_RETURNS/RRIF-C-POST-GAP-LINEAGE-REDUCTION-20261031-R1/ACCOUNTED_FOR_CODE_BRANCHES.jsonl`
- `WORKER_RETURNS/RRIF-C-POST-GAP-LINEAGE-REDUCTION-20261031-R1/UNIQUE_IMPLEMENTATION_LINEAGES.jsonl`

## 3. Documentary count checks

Independent read of the exact Git objects (not a census):

| Check | Recorded / observed | Result |
|---|---:|---|
| 34-ledger rows | 34 | PASS |
| 34-ledger unique IDs | 34 | PASS |
| 34-ledger `branch_identity_count` sum | 321 | PASS |
| 34-ledger `code_introducing_branches` sum | 155 | PASS |
| 30-lineage HQ intake rows | 30 | PASS |
| 30-lineage unique IDs | 30 | PASS |
| Intake IDs subset of 34 ledger | true | PASS |
| RRIF-C accounted code branches | 321 | PASS |
| RRIF-C accounted branch names unique | 321 | PASS |
| RRIF-C `CODE_INTRODUCING` rows | 155 | PASS |
| RRIF-C lineage rows | 34 | PASS |
| RRIF-C lineage IDs unique | 34 | PASS |

Original validator counts at its original scope:

| Count | Value | Result |
|---|---:|---|
| `frozen_branch_names` | 845 | PRESERVED |
| `distinct_frozen_tips` | 838 | PRESERVED |
| `code_delta_branches` | 321 | PRESERVED |
| `accounted_code_branches` | 321 | PRESERVED |
| `unique_lineage_rows` | 34 | PRESERVED |
| `code_introducing_branches` | 155 | PRESERVED |
| `original_function_ids` | 3135 | PRESERVED |
| `original_families` | 1885 | PRESERVED |
| `code_exact_present` | 45 | PRESERVED |
| `code_stranded_or_diverged` | 276 | PRESERVED |
| `implementation_lineages` | 33 | PRESERVED |
| `integration_test_lineages` | 1 | PRESERVED |
| `inherited_test_review_or_copy_branches` | 166 | PRESERVED |
| `genuinely_unresolved_lineages` | 30 | PRESERVED |

Original validator checks: all recorded booleans are `true`; all nine mutation tests are `PASS_REJECTED` (drop/duplicate accounted branch, drop lineage, duplicate function ID, mutate one tip, drop/duplicate family, drop/duplicate 845 branch join). The precheck preserves the original 845/838/3135/1885 scope without recomputing it.

## 4. Source, negative, and restart pointers

All 34 ledger rows were checked for:

- schema `PYAT_RRIF_TERMINAL_ACCOUNTING_CANDIDATE@1`;
- `original_RRIF_C_source_cut = b75addf621c3a6c1a3b196bd92a810fad77ae3ae`;
- nonempty `negative_owner_wake`;
- `receiving_cas = NOT_ADOPTED`;
- `authority = NOT_ISSUED_BY_RRIF`;
- `scientific = ORIGINAL_NATIVE_OR_QUALIFIED_SCIENCE_NOT_ISSUED_BY_THIS_LEDGER`;
- `engineering = EVIDENCE_ACCOUNTED__ONLY_SPECIFIC_SOURCEFREE_SCOPES_POSSIBLE`.

Every lineage therefore retains a source cut, a negative condition, a restart/owner wake, and a non-adoption posture. This does not claim any lineage is current, approved, or scientifically issued.

## 5. R157 scope check

Row: `LIN-R157_SOURCE_CONFIGURATION`

- `terminal_candidate_status = HISTORICAL_RECOVERABLE_NOT_CURRENT__NO_AUTO_REIMPORT`
- `branch_identity_count = 23`; `code_introducing_branches = 5`
- `scope_correction` retains all four distinct grains: 119 historical `source_configuration`/`read_admission` Git blob paths with zero same-path PREMAIN; 19 unique code paths, all absent; 34 final-review comparative rows; 32 five-introducer blob occurrences. It explicitly rejects inventing a 34→32→19 equivalence.
- `negative_owner_wake` retains `reopen from d81bc2c67` and says to recompare all 19 paths only if a future real source-configuration consumer is authorized; otherwise do not fan in R157 or its 13 lanes.
- `first_consumer` remains `ENTRYPOINT_ONLY` at `rawlsing_next/source_configuration/cli.py`, with no external current consumer found.

Result: PASS at the ledger's declared scope. R157 is historical recoverable configuration, not current implementation and not a scientific/U-E_pre source grant.

## 6. C5 scope check

Row: `LIN-C5_N5_STRUCTURAL_CONTEXT`

- `terminal_candidate_status = ONE_GT2_CASE_RECONSTITUTED__WRAPPER_API_NOT_PROVED`
- `branch_identity_count = 3`; `code_introducing_branches = 2`
- `scope_correction` retains the exact one-case evidence: `19,210` GT2 context and `19,211` refusal, not general zero-argument service API supersession or a real receiver.
- `negative_owner_wake` retains `Do not re-import the wrapper`; if a current consumer appears, call the owner-level path directly or re-propose the zero-argument service with a named receiver and fresh tests.
- `first_consumer = null`.

Result: PASS. C5 does not claim full accepted-wrapper API supersession, a current consumer, or authority.

## 7. Pending code-gate rows

The ledger records the two code gates as pending and not adopted:

- `LIN-C3_PHYSICAL_DECODER_R5_G01`
  - `terminal_candidate_status = E1_PATCH_COMPLETE__E4_DISTINCT_REVIEW_PENDING`
  - `scope_correction` records E1 `ffd03934` selected regressions 194 pass/1 skip and the two G01 pre-existing REDs.
  - This row predates E4's hostile RED, E4F's corrected return, the E4FR return, and this preflight. It is stale as a current gate pointer. Exact review/CAS must update it; nobody may infer E4F acceptance from the row.
- `LIN-LEARNED_WORLD_PRODUCT`
  - `terminal_candidate_status = E5_PATCH_COMPLETE__E6_DISTINCT_REVIEW_PENDING`
  - `scope_correction` records E5 `96e6d49` local B5/M2 repair with `179 pass/14 fail`, the 12 historical defect-presence assertions, and the 2 unchanged accepted M2 foreign-release fixture clashes. It explicitly says not green/not adopted and requires independent review of the exact blobs.
  - The E6 return is HOLD and the M2 owner fixture-amendment decision is absent; the row remains not adopted.

Both rows retain their negative owner wake and `receiving_cas = NOT_ADOPTED`.

## 8. Reproducible command and receipt

```sh
cd /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/pyat-rrif-f0-receiving-20261101-r1
PYTHONDONTWRITEBYTECODE=1 /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/f0-venv/bin/python \
  WORKER_RETURNS/PYAT_RRIF_F0_RECEIVING_PREFLIGHT_20261101_R1/ledger_precheck.py \
  --repo /Users/matthewsmith/Desktop/Rawlsing \
  --ledger-ref d80901e9de78803c031fa9d25146f7d8b6aeba2c \
  --rrifc-ref b75addf621c3a6c1a3b196bd92a810fad77ae3ae
```

Observed: exit `0`, `documentary_checks_pass: true`, `terminal_decision: PENDING_REVIEW_CAS`, one warning that the C3 row predates E4/E4F. Counts observed: 34 ledger rows / 34 unique; 321 membership sum; 155 introducing sum; 30 intake rows / 30 unique; 321 accounted rows / 321 unique names; 34 lineage rows / 34 unique.

Receipt log sha256: `539adc231d108f69b2516b4afb269489277402b05d497732f5be284189d5ee16`.

## 9. Terminal decision

`PENDING_REVIEW_CAS`

The ledger is documentary-consistent at its commissioned cut, but terminal RRIF completion is not accepted:

- E4F has an independent positive review, but no protected CAS or merge has occurred.
- E5 is held by E6 and lacks the owner-authorized versioned M2 fixture amendment; the resulting SHA would need a fresh full court and a distinct review.
- The C3 row needs an exact review/CAS update, not textual acceptance by this preflight.
- The 34-lineage terminal decision remains pending review and CAS evidence.

No historical branch census, source-native execution, or new authority was performed.
