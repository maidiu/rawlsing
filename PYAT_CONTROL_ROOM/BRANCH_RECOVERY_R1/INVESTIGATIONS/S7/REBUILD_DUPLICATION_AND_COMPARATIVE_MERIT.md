# PYAT 845 S7 — REBUILD, DUPLICATION AND COMPARATIVE MERIT

**Inputs:** S6 `2c5cf86b…`, H1 `815edc1b…`, PE/V2K `9647d851…`, S1–S5 corrected `6a658ad3… / 3042fca8… / ebdb51a5… / d93e8c24… / 32dac59b…`, evidence law `f50651a2…`.  
**Current cut:** `87755f02ec5c37499b09e80db6fbdcc9316a6b15`; `rawlsing_next` tree `1d88d3fbb1d18dadfda946d9cd7f309d84afa479`, identical to the S6/H1 cut.  
**Rule:** a row count, a same-name AST, a path absence, or a group ID is not behavioral equivalence. Comparative merit is stated only after custody, current presence, receiver and test evidence are separated.

## 1. What the 3,135 rows actually reduce to

| Quantity | Count | Meaning |
|---|---:|---|
| Original corrected rows | 3,135 | 1,279 S1 + 218 S2 + 398 S3 + 897 S4 + 343 S5 |
| S6 groups | 1,881 | 1,879 row-derived + 2 external zero-member priority cases |
| Groups with >1 historical blob | 328 | Variants, not proven duplicates |
| Groups with >1 distinct AST body | 173 | Behavioral variants remain inside one group |
| Groups with no historical blob | 93 | Link/evidence-only or unresolved |
| Evidence-only groups | 841 | Tests, returns, audits, reviewer material; not production recovery |
| Production/candidate/external groups | 1,040 | 1,038 row groups + 2 external |
| Groups with no real current receiver | 1,824 | `NO_REAL_RECEIVER_YET` |
| Groups with text-reference only | 56 | `TEXT_REFERENCE_ONLY__NOT_EXECUTED` |
| Groups with E03 exact only | 1 | E03 is not the whole P41 service |
| Specific defect rows audited | 30 | S2 1 + S3 5 + S4 11 + S5 13 |

The correct conclusion is **not** “1,881 duplicate families” and **not** “1,881 missing capabilities.” It is:

- A large number of rows are repeated historical carriers of the same path+qualified-symbol family.
- A smaller number are genuine behavioral variants within that family.
- A smaller number are evidence-only material.
- Only a subset are missing current production capabilities with a plausible receiver.

## 2. Do not rebuild what is already current

These are exact current code at `87755f02` and should not be re-added as “recovered” blobs:

| Current path | Blob | Status |
|---|---|---|
| `rawlsing_next/pre553_universal_workload.py` | `8e7fe00a3ed008361d9f3c501e7782b2de3a636e` | exact, candidate library chain |
| `rawlsing_next/pre553_issued_workload.py` | `31e84f49d624f5524906e9e7839d2873106f8249` | exact, candidate library chain |
| `rawlsing_next/pre553_native_workload_binding.py` | `dac73e484f8619088f5c6701b2b6991c07540f3b` | exact, candidate library chain |
| `rawlsing_next/pre553_source_native_preimage_adapter.py` | `a6299c1a6e8b26bd055ced1f49e5b757f20ccd8c` | exact, candidate library chain |
| `rawlsing_next/pre553_physical_decoder.py` | `8732e34d0ea3f4cfffd7d33ee00f258dbc2d65dd` | exact, PR526 `_SourceSnapshot` custody |
| `rawlsing_next/pre553_r5_codec.py` | `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540` | exact, inherited mainline; not in 845 branches |
| `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` | `84d404147547767be8ecd4b6e1541f5fa3a8c8a2` | E03 exact, test-only receiver |
| `rawlsing_next/pre553_source_relations.py` | `5b67e3f98a5faf95a6c82700af2346fef6e306a5` | current resolver, test/string reference only |
| `rawlsing_next/pre553_source_equivalence.py` | `0e7f9f6d77ef6efe2c66b04f0527bb1ab99f4ef8` | test-only alternative |
| `rawlsing_next/pre553_source_local_universe_admission.py` | `b968fa16c6620cd06b191ebdb5da7da86f524393` | test-only alternative |

The S1 150 `CURRENT_PRODUCTION_ACCEPTED_AT_NAMED_SCOPE` rows are also exact AST at this cut. Their problem is row-level E3 evidence, not code absence. The S4 325 renamed rows are exact body at current paths; their problem is that exact body at a renamed path is not behavioral equivalence and they have historical-only adoption. Do not “rebuild” either set.

## 3. Genuinely missing or genuinely different valuable functions

The following are the highest-value non-duplicates. “Merit” is engineering/scientific potential, not adoption.

| Rank | Family | What is actually missing | Current receiver / UNKNOWN | Exact integration requirement | Comparative merit / reason |
|---:|---|---|---|---|---|
| 1 | **R61-R08 evidence binder** | 118 KB `pre553_universal_evidence_binding.py` candidate, module blob `3ca860e4…`, introduced at `80bb8c18…` (2026-10-23). 22 groups / 164 rows. | PATH_ABSENT; no receiver. Candidate branch `be113339…`; review tip `2937966b…`. | ABI/schema/descriptor diff vs current provider/C1/J42/P41; sourcefree positive + fault-negative; independent owner review. | Highest evidence-admission value. It is a reviewed, scoped-local binder, not a duplicate of current provider/C1. It is also the largest single merge-risk because no current ABI exists. |
| 2 | **C3 G01/D01/D02 + R5 carrier** | Current decoder `8732e34d…` and R5 `72f8f3c0…` lack C3 G01/D01/D02; C3 decoder candidate `d3d828c1…` introduced `901e3e77…`. G01 path absent. | Static decoder/r5 imports exist; executed consumer NOT_RUN. | Port into current decoder/r5 while preserving PR526 read-only/stable/TOCTOU snapshot custody; rerun 55-test C3 court on current receiver. | Highest direct decode/representation value. Neither current PR526 nor C3 is a proven superset; a port is more valuable than replacing either. |
| 3 | **R9 broker/session/execution binding** | `pre553_source_access_broker.py`, `pre553_source_session.py`, `pre553_execution_binding.py`; final blobs `090d978b…`, `ac1390b8…`, `0e11af22…`; integration `dfdf5659…` (2026-10-04). | PATH_ABSENT; no receiver. | Integrate as sourcefree modules; reconcile decoder route with PR526 custody; run 20 broker / 15 session / 34 binding / R7 tests. | Highest source-access value. The R9 branch decoder lacks PR526 custody, so a wholesale replacement would regress current custody. |
| 4 | **P41/E04L generic progressive service** | `p41_service.py` blob `7d428106…` introduced `24f80eeb…` (2026-10-19); 5 groups / 4 rows + external service. | E03 exact `84d40414…` is test-only; P41 service absent. | Port P41 service onto current E03/C1/N10E/M4/M5; run 19 tests + 3 severance witnesses; keep N9/N10W/N11 holds. | E03 is byte-identical evidence of a component, not the service. This is the only path to a real progressive N10W service without relabeling E03. |
| 5 | **F7 temporal comparability + P07 repair** | `pre553_temporal_comparability.py` absent; sealed P07 owner blobs `d9fb2c48…`, `8053d30d…` are defective; current resolver present but test-only. | Temporal absent; current resolver `5b67e3f9…` has no production import. | Repair/replace P07 owner custody and F7 TCB; rerun HQ232/HQ236 negatives and F7 49/159; no sealed-owner promotion. | High scientific/engineering value but the highest known defect concentration: 11 S4 and 13 S5 defect rows include RR-04F/G, writable custody cell, TCB alias, malformed native Stage A/B. |
| 6 | **Selected-world contract and seam** | `pre553_selected_world_progressive_contract.py` and `r3_s02_seam_witness.py`; seam tip `ed34944e…`; contract origin `c98e8881…`. | PATH_ABSENT; E03 exact only. | Fix seam `KeyError`; rerun 27 tests with zero failures; then current P41/C1/N9 consumer. | Blocks selected-world/N10W integration. The seam failure is a genuine negative; the 24 selected-world passes and 18 E03 passes do not erase it. |
| 7 | **PE whole contract and repaired `_auth`** | Original PE blob `58484f4c…` at `e61a26ce…` has 9 strict failures; repaired candidate at `9647d851…` fixes the reversed-issuer case. | No current static receiver; candidate branch-local. | Owner decision on 8 remaining SC0 value-bearing/schema gaps; independent I3 rerun of repaired 5/8; do not merge the candidate as production. | The `_auth` repair is real at candidate scope (S7 ran 2/2), but the whole contract is still RED/HOLD. |
| 8 | **V2K historical lineage** | `pre553_original_identity_v2k_successor_candidate.py` exists at `694fb450…`; exact dependency `pre553_original_workload_contract_v2_candidate.py` absent there and absent at current. | No current consumer; exact branch cannot collect. | Decide historical dependency preservation vs new current-ABI adapter. Make any replay self-contained; do not claim 111/111 or 63/63 from an external tree. | Historical/science value only. Current `pre553_issued_workload.py` is a distinct native API, not a V2K successor. |
| 9 | **R157 source-configuration preparation** | `source_configuration` factory absent; alternatives `pre553_source_equivalence.py` and `pre553_source_local_universe_admission.py` are test-only. | PATH_ABSENT; no production receiver. | Map 35 configurations to current source owners; verify item/slot identity; actual U/E_pre execution only under separate grant. | High preparation value, but a factory restoration would duplicate/revert mature current source-local-universe logic. Map, do not revert. |
| 10 | **R61-R09 parent-owned capture** | No current capture owner. D1 forged child observation, D4 child-reported loaded bytes, D7 malformed expectation crash. | No current receiver. | Parent-owned observation and loaded-byte channel; rerun D1/D4/D7 + real C11 positive; host/platform boundary. | Critical custody primitive. It is not a function family in the 3,135 rows; it is an external negative that must not be lost. |

## 4. Comparative merit, not branch census

The comparative ranking above is based on four separated axes:

1. **Missing capability:** the function is not present or not behaviorally equivalent at current scope.
2. **Receiving consumer:** a real current path or a named integration target exists.
3. **Evidence quality:** historical scoped acceptance or a reviewed candidate, never a branch label.
4. **Risk:** known defect density, custody conflict, or authority requirement.

This produces a different order from “largest branch” or “oldest tip”:

- **R61-R08** is first because it is a reviewed, non-duplicate binder with a named current comparison target, even though it has no current ABI.
- **C3/R5** is second because current static receivers already exist and the missing G01/D01/D02 has direct decode value.
- **R9** is third because the modules are sourcefree and complete at binding grain, but the decoder custody conflict is a real regression risk.
- **P41** is fourth because E03 is exact but is not the whole service.
- **F7/P07** is fifth because the defects are real and the owner boundary is unresolved.
- **Selected-world** is sixth because the seam failure blocks the consumer chain.
- **PE/V2K** are seventh/eighth because they are partly repaired but structurally incomplete.
- **R157** is ninth because its preparation is valuable but its current alternatives are already mature.
- **R61-R09** is a cross-cutting custody blocker, not a function to merge.

Branches that contain only evidence, tests, audits, or reviewer returns are **not** lower-merit production candidates. They are evidence-only by role; 841 groups fall here.

## 5. Implementation sequence

1. **Fix S6 boundaries first.** Split the five merged `SourceRelationResolver` groups and join the two `iter_batches.emit` groups. Re-key all downstream dispositions. This is cheap and prevents wrong merit comparisons.
2. **Establish current receiver truth.** For each candidate, name the exact current import/call path and mark executed consumer NOT_RUN until it is actually run. Static imports are not executed consumers.
3. **Run the high-value sourcefree ports in order:** C3/R5 (55 tests), R9 (20/15/34/R7), R61-R08 ABI/fault-negative, P41 (19 + 3 witnesses), F7/P07 (HQ232/HQ236 + 49/159), selected-world (27), PE (13 strict), V2K (self-contained exact or new ABI).
4. **Preserve the negatives.** The seam failure, PE nine failures, V2K collection error, R61-R09 D1/D4/D7, F7/P07 TCB defects, R56 byte custody, and native Stage A/B must remain visible after any repair.
5. **Do not merge on this evidence.** Each integration needs independent I3 review and a separate PRE-MAIN/HQ adoption decision.

## 6. False economies to avoid

- **Counting groups as functions.** 1,881 is a custody grouping, not a capability count. 173 groups contain multiple AST bodies.
- **Counting rows as duplicates.** 3,135 rows include inherited carriers and evidence-only material. They are not 3,135 independent capabilities.
- **Replacing current custody with a branch.** C3 and R9 branches lack PR526 `_SourceSnapshot` custody; P41 is not E03; V2K is not current issued workload.
- **Promoting the sealed P07 owner.** The 11 S4 and 13 S5 defect rows include reproduced RR-04F/G, writable custody and TCB failures.
- **Treating a green module suite as row-level acceptance.** 105 current tests cover four modules, not 150 S1 rows.
- **Treating exact body at a renamed path as behavioral equivalence.** 325/325 S4 bodies are exact, but zero have current consumer/positive/fault-negative receipts.
- **Treating a branch tip date as origin.** S6 left 664 introducing tips null; S7 reconstructed exact blob-introducing commits for the priority families.
- **Treating a green repair-branch candidate as integrated.** PE candidate 2/2 and V2K severance 2/2 claims are branch-local; the V2K test is not even self-contained at the exact 9647 tree.
