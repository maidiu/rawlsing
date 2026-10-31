# SOROK O-INDEX R2-IR — independent primary-source, validator and whole-program review

**Return:** `WORKER_RETURNS/SOROK-OINDEX-R2-INDEPENDENT-REVIEW-R1`
**Repository:** `maidiu/rawlsing` private
**Review branch:** `review/sorok-programma-oindex-r2-source-correction-independent-test-20261030`
**Commission head:** `bc8cfb77a8fbae1f37e7b2086839e19c71d07513`
**Immutable subject:** `96af4f15c993c7a4f32da4cc31ef3175903a0d5c`
**Original O-INDEX:** `59b4d607697af8bba668122f42b53868fb2758bf`
**Current PRE-MAIN (refreshed):** `87755f02ec5c37499b09e80db6fbdcc9316a6b15`
**Candidate build PRE-MAIN:** `5fc1d43e3d5412194d1f1eaa30ff448f84635e99`
**Model/host:** OpenCode 1.18.34 / `opencode-go/deepseek-v4.1-flash`, local oldMac, MAX requested
**Final remote SHA:** reported in the terminal push readback; a file cannot contain its own commit SHA.

## Decision

**`REVISE_PRECISE_DEFICIENCIES`**

The primary-source correction is real and exact, and the corrected validator
passes its current 9 tests. The O-INDEX is not yet acceptance-grade as a
source-exact, whole-program navigation substrate. The defects are finite and
listed below; this is not a request for another global recovery campaign.

## Four-column findings

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| Both Program Maps are exact 17/17 S0–S16 primary sources with active exploratory status; all S records match the exact map questions/outputs. | R7’s S0–S16 source-absence conclusion is genuinely superseded. The correction is source-grade, not an adoption. | Keep the correction; do not downgrade it to HOLD. | Sorok HQ / O-INDEX author / independent reviewer |
| Validator passes 9 tests and reports 144/23/4/189/431/40, but a forged A5 source path/blob with real metadata and fabricated consumer also passes; forged timestamp and forged Pyat source pass. | The validator proves internal consistency, not source-object identity. | Bind every row/Pyat record to actual Git object/type/blob and actual metadata; add the missing negative tests. | Validator/O-INDEX author |
| Three S/lineage rows have no source path at the stated commit; five rows have null blobs/tree. | Source-exactness is incomplete despite a passing validator. | Correct the exact paths/blobs or mark typed `SOURCE_IDENTITY_INCOMPLETE`; reject missing/forged source. | O-INDEX author / source owners |
| S5, S7, S11, S13, S14, S15 have exact source questions/outputs but only generic `L1_GOVERNANCE` (and sometimes `L1_PERSON`) links; no specific product, UX, economic, safety or evaluation traversal or owner slot. | The map collapses the specifically requested workstreams into the warned generic placeholder. | Add specific product/consumer/owner mappings or explicitly mark them source-defined-but-unmapped; do not claim whole-product traversal. | O-INDEX author / Sorok HQ |
| The package still says 188 nodes/414 edges, seven tests/six mutations, and `claim_epochs.s0_s16=R7_EXACT_HOLD`; current PRE-MAIN is 87755f02, not 5fc1d43e. | Stale proof text and currentness labels undermine a source-of-truth map. | Update counts, test/mutation counts, epoch and current PRE-MAIN; do not cite old `VALIDATION_RESULTS.json`. | O-INDEX author |
| R6 39/94/133/26/9, R7’s other findings, F1CR missing bytes, ZIP mismatch and four author-tested assets are preserved without pooling. | The recovery history is largely represented correctly. | Keep exact grain; do not combine test counts into native/person acceptance. | R6/R7/asset owners |

## Three courts

### ENGINEERING

**REVISE_PRECISE_DEFICIENCIES.** The candidate validates internally: 144 Sorok
rows, 23 Pyat rows, 4 assets, 189 nodes, 431 edges, 3 traversals, 40 owner slots,
0 priority decisions, 9/9 tests. But source path/blob/timestamp and
source-to-consumer claims are not tied to Git; the eight required adversarial
cases are not all caught. Three source paths are absent, five blobs are null/tree,
and stale counts remain.

### SCIENTIFIC

**REVISE_PRECISE_DEFICIENCIES.** The source obligations are exact for all 17 S
workstreams, and the 102 inherited definitions remain clearly source/requirement/
decision/edge typed. However S5 flourishing, S7 player praxis, S11 UX, S13
monetization, S14 safety/privacy and S15 alpha/evaluation are not traversable as
specific product/science obligations. Their exact source questions survive, but
the product map cannot yet support HQ's substantive synthesis of them. No native
science issuance is expected or claimed.

### AUTHORITY

**HOLD.** No native source, CAN/ADP/SCI05, C9/C12, N11/N12, Pyat C0 or A5 human
acceptance is issued. No owner adoption, PRE-MAIN mutation, PR change or
self-review occurred. The four assets remain author-tested candidates at their
declared sourcefree scope.

## What is verified

- Current Program Map `865b5b01…`, blob `2a0a3a42…`, 17/17 exact.
- Earlier Program Map `3c423a0f…`, blob `6271bb66…`, 17/17 exact.
- All 17 S registry records carry the exact current commit/path/blob, and their
  questions/outputs match both maps; active exploratory status is preserved.
- Current PRE-MAIN `87755f02…` is three Pyat S6/H1/PE intake files ahead of the
  candidate’s `5fc1d43e…` build cut; no rebase was performed.
- Intact candidate validator: `PASS`, 189 nodes / 431 edges / 66 typed cycles.
- Intact test file: 9 passed; `unittest` 9/9.
- R6 39 rows/94 files/9 material families/R41 133/26; four assets candidate-only
  with separate author counts.

## Defects preventing acceptance

1. **Source validation gap:** forged non-S source path/blob and fabricated
   `first_consumer` pass; forged metadata timestamp and forged Pyat source pass.
2. **Source identity gaps:** `B3A`, `B3AS`, `S39_S52` paths absent; `B1`, `B2`,
   `B3`, `BP2P4J` blobs null; `R15_V2` is a tree, not a file blob.
3. **S5/S7/S11/S13/S14/S15:** exact source rows, generic graph mapping only;
   S13/S14 have no non-governance target; no specific traversals or owner slots.
4. **Stale proof text:** 188/414, seven tests/six mutations, old
   `VALIDATION_RESULTS.json`, and `s0_s16=R7_EXACT_HOLD` remain beside corrected
   counts and `POST_SOURCE_CORRECTION`.
5. **Stale currentness:** candidate launch PRE-MAIN `5fc1d43e` vs refreshed
   `87755f02` (3 Pyat files; S0–S16 map unchanged).

## DONE

- Independently retrieved and compared both exact Program Maps.
- Verified all 17 S headings, questions, outputs, commits, paths and blobs.
- Ran corrected validator and tests in isolated S2: `PASS`, 9/9.
- Executed eight required and additional adversarial mutations; documented the
  exact false-pass defects.
- Audited all 144 Sorok and 23 Pyat source references against Git.
- Reviewed all three traversals, S5/S7/S11/S13/S14/S15, R6/R7 and four assets.
- Preserved no-native/no-priority/no-adoption boundaries.

## REMAINING

- Correct source-object binding and adversarial coverage in the validator.
- Correct three paths, five null/tree blobs, and the aggregate `S0_S16_SOURCE`
  owner-slot limitation.
- Add specific S5/S7/S11/S13/S14/S15 product/consumer/owner traversal or mark
  them explicitly unmapped.
- Update stale counts, proof epoch and current PRE-MAIN labels.
- Independent re-review and owner adoption; none performed here.

## CRITICAL_BLOCKERS

- Validator `PASS` cannot yet be used as source-exactness proof.
- S5/S7/S11/S13/S14/S15 cannot yet be traversed to their actual product
  obligations through the graph.
- No native source/science/actor/A5 authority is present or implied.

## LARGEST_PRODUCTIVE_MOVE

Fix the validator’s Git-object binding and the six S product-workstream mappings;
that is a bounded correction to this candidate, not another recovery campaign or
Programma priority decision.

## FLIGHT

Local S2 sourcefree Git/Python/pytest only. No original survey, provider/model
call, native actor/world, production import, PRE-MAIN mutation, branch rewrite,
PR edit or candidate code execution.

## DELTA

The primary S0–S16 correction is independently verified and the candidate
validator/tests are freshly executed; the remaining defects are now precise
source-binding, product-mapping and stale-proof issues rather than an unknown
historical-source estate.
