# DDM VOSKRES #1059 — R2 exact-defect correction return

**Candidate branch:** `docs/voskres1059-r2-composed-author-20261115`
**Frozen first R2:** `7ebd363dedc36cdc34b3a6ef53e32603f291c84e` (parent `819dc54c69633dd75b6d13ac0ee8c3bbfd624853`)
**Correction review:** `1b525d00ee55a78e18d78e8f1afcb81bb9682bb8` — `REVISE_EXACT_DEFECT`, 11 reproducible defects
**Original source pin:** `25830fe7462bb9e29bc4087e6ae14f3f84cec377`
**Modern cuts checked:** `3e0ed0794498506520ae62c997a5c852ac672061`; `6a5c12f04323d74001f9632063ec907f4fc4468e`
**Scope:** same author/session, one bounded correction pass; write scope `WORKER_RETURNS/DDM_VOSKRES1059_R2/` only
**Grade:** `DOCUMENTARY_SOURCE_ONLY_CORRECTED_CANDIDATE / G5_ORIGINAL_REVIEW_REMAINS_REVISE / NOT_SELF_ACCEPTED`

## 1. What changed

All 11 review IDs are addressed in `CORRECTION_MATRIX.tsv`. No new A/B survey, general inventory, source read, raw respondent bytes, scientific execution, test, CI, product edit, protected merge, provider/model/VM change or subagent was used. The original R1 A/B/HQ and first-R2 commits are preserved as immutable; this pass modifies only the R2 return files.

### G1 — canonical accounting

`G1_CANONICAL_ACCOUNTING.tsv` now has 11 supersession rows, each with stable machine coordinates:

- `source_file`, `source_commit`, `source_file_sha256`, `source_row_number` (1-based including the header), `source_column`, exact `source_cell_value`;
- the corrected value in `canonical_correction`;
- exact source evidence and snapshot.

Corrections preserved: one primary plus at most k−1 candidate-vs-primary comparisons (not O(k²)); configurable `max_depth` default 3 (not an unconditional cap); complete marker + `question_use_contract` hash resume guard (not existence-only). `G1-11` adds the previously missing `B_R1/COST_CARDINALITY.tsv:9` depth cell. The prose row keys are gone; `A_R1/SOURCE_LEDGER.tsv` rows 5 and 14 are addressed by number and `claim` column, and the duplicate CORR-A-01 text is not used as a target.

### Exact 11-cell verification

Verified against `git show <source_commit>:<source_file>`, file SHA-256, 1-based physical row, header lookup, and exact cell comparison. All 11 match after the two locator corrections.

| Cell | Source coordinate | Exact cell result |
|---|---|---|
| G1-01 | A COST row 8 / `cardinality_symbolic` | PASS — corrected to `k = available indicators <=12; joint mask and joint conditional entropy per non-primary pair with joint n>=50`; the false `per non-primary pair` assertion is quoted, while the row's separate `O(k^2)` preparation label is explicitly distinguished as paraphrase/label |
| G1-02 | A SOURCE_LEDGER row 14 / `claim` | PASS |
| G1-03 | A COST row 9 / `cardinality_symbolic` | PASS |
| G1-04 | A TSM row 11 / `old_function_and_evidence` | PASS |
| G1-05 | B TSM row 4 / `operation` | PASS |
| G1-06 | B SOURCE_LEDGER row 12 / `claim` | PASS |
| G1-07 | A COST row 6 / `lifetime_invalidation` | PASS |
| G1-08 | A TSM row 6 / `old_function_and_evidence` | PASS |
| G1-09 | A TSM row 6 / `stage2_forge_evidence_3e0ed07` | PASS — corrected locator; actual `stage1_successor_fate` is `Batch receipts and immutable unit receipts (pre553_batch_runner.py 386-470)` and is not the false cell |
| G1-10 | A SOURCE_LEDGER row 5 / `claim` | PASS |
| G1-11 | B COST row 9 / `per_operation_cardinality` | PASS |

### G2 — composed graph and V553 inputs

`G2_COMPOSED_GRAPH.tsv` now has 23 edges. `G2_V553_INPUTS.tsv` now has 17 input rows.

- **Canonical V553 inputs** now include `manifest.json`, `packets/v552j_structural_join_index.parquet`, `audits/v552j_join_audit.parquet`, and `manifest/v552j_v553_handoff_manifest.json`, with their exact identity/hash/row-count/equality checks.
- **Legacy V553 inputs are separated** from canonical: `packets/v552j_structural_handoff_packet.json`, dereferenced V551J certified/reviewable frames, and V552 optional pressure tables are real inputs to `ddm_v553_harmonization._load_wave_bundle`, not provenance-only. The canonical adapter still does not dereference V551J; that finding is now explicitly canonical-path-only.
- **V551J candidate bundle** `v551j_joint_packet_candidate_index.parquet` is added to J-07/J-08; it is required for review-row enrichment.
- **V550J respondent membership** `joint_pattern_respondent_membership` is now a named V550J output (J-02), with a distinct V550J→V551J loss row (J-10): aggregate pattern/item membership survives; exact `respondent_id`/`respondent_id_norm`/weight/answered-item grain does not.

### G3 — concrete family and true diamond

`G3_SELECTED_JOINT_PATH.md` now selects the concrete bounded-nine family:

`JCFG-GSS-ABORTION-CONDITIONS` / `gss_abortion_condition_family`, GSS 2010 US, six ordered items `abdefect`, `abhlth`, `abrape`, `abany`, `absingle`, `abnomore`, with exact `question_implementation_id`/`p2_lineage_id` identities, authority release `V550J-BOUNDED-AUTHORITY-2026-08-02-R1`, adjudication `V550JADJ-0005`.

It traces the family through expected V550J prepared substrate, V550J pattern/item/relation/membership, V551 atoms, V551J candidate/certified/review packets, V552 facts, V552J join and V553 output, marking each missing run/manifest/row explicitly. The headline is corrected to the actual diamond:

`(V550 ordinary distributions → V551 atoms) || (V550J patterns) → V551J; V551 atoms → V552 facts; V551J + V552 facts → V552J → V553`.

There is no V550J→V551 atom edge and no V551J→V552 fact edge. `HISTORICAL_EXECUTED = NO`; the C4R1 0/9 positive-load and missing-substrate HOLD is preserved.

### G4 — old→FORGE first readers and J-parity gate

`G4_OLD_TO_FORGE.tsv` corrected:

- `G4-03`/`G4-06`: `NONE_IN_PRODUCTION` first reader; `produce_governed_diagnostics` is the producer, `assert_diagnostic_only_use` is a guard, and only `rawlsing_next/tests/test_pre553_diagnostics.py` consumes the product at the inspected cuts.
- `G4-07`: cut-scoped primary search added at both `3e0ed079` and `6a5c12` (`git grep -n conditional_determinicity -- rawlsing_next` → no match, exit 1); PROGRAMMA G3A row is retained only as a lead; `pre553_legacy_compat.py:112-123` parity denial is cited.
- `G4-08`: `pre553_legacy_compat.py:4-6,112-123` added as the actual modern J-parity gate, disposition `COMPATIBILITY_GATE_DENIES_J_PARITY` — not a carrier, not a conservation proof, and not global absence of joint capability. Independent I03 exact math is preserved.

`G4_CONDITIONAL_INDEX_TRACE.md` is unchanged; its `HELD_LOCAL_UNCONSUMED_AUXILIARY_CAPABILITY_WITH_NO_PROVED_HISTORICAL_PRODUCER_OR_READER` disposition and the local-non-use vs global-loss distinction remain accepted S1.

## 2. Defect→correction map

See `CORRECTION_MATRIX.tsv` for all 11 IDs:

- `G1-D1`, `G1-D2`
- `G2-D1`, `G2-D2`, `G2-D3`, `G2-D4`
- `G3-D1`, `G3-D2`
- `G4-D1`, `G4-D2`, `G4-D3`

No exact defect is knowingly left unresolved. Residual HOLDs are evidence holds, not unfixed review defects:

- historical V550J/V551J/V552J/V553 output rows or positive-load receipt for the selected family;
- a real V551 conditional-index producer invocation/reader;
- external historical invocation of the conditional index remains `NOT_INSPECTED`.

## 3. Evidence and updated manifest

`SOURCE_LEDGER_R2.tsv` now records the exact review-source cuts, blob hashes, line ranges and hashes for:

- G1 raw cells and stable-coordinate sources;
- canonical and legacy V553 inputs;
- V551J candidate bundle;
- V550J respondent membership and D11 §8;
- GSS family registry/authority/crosswalk and CURRENT_STATE;
- diagnostics producer/guard/test consumers;
- cut-scoped primary search and `pre553_legacy_compat.py` J-parity gate;
- expected V550J/V551/V551J/V552/V552J run paths and artifact names.

`MANIFEST.json` is updated for the corrected payload, its file hashes and counts. `00_RETURN.md`, `CORRECTION_MATRIX.tsv` and all corrected payload files are included in the manifest.

## 4. Preserved limits and honest holds

- No historical execution, numerical transformation, positive load, throughput or full functional-conservation claim.
- No raw respondent bytes, synthetic stand-in, invented run, fake pattern id or fabricated row.
- No claim that the legacy V552J packet is globally obsolete/non-input; it is canonical-nonrequired but legacy-read.
- No claim that exact respondent identity survives V551J/V552J/V553.
- No claim that modern diagnostics are a production-consumed successor to old MI/secondary/recursive products.
- No claim that the modern J-parity gate proves global absence of joint capability; it denies object parity for lack of authority.
- No G5 acceptance claim. The original frozen review remains `REVISE_EXACT_DEFECT` until HQ verification of this correction package.

## 5. Publication and stop

No git commit/push was made in this correction pass; HQ publishes. HQ should verify the explicit 11-ID checklist, then update #1060/#1059. Any focused independent closure must reuse the already-proved source and only the changed claims, not launch a new whole audit.

`STOP_FINITE_CORRECTION`.
