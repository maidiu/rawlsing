# DDM VOSKRES #1059 — R2 independent G5 review

**Reviewer session:** `ses_e21ca08a9ffe4wtn6NR7YhSTer`  
**Candidate:** `docs/voskres1059-r2-composed-author-20261115`  
**Candidate commit:** `7ebd363dedc36cdc34b3a6ef53e32603f291c84e`  
**Parent:** `819dc54c69633dd75b6d13ac0ee8c3bbfd624853`  
**Original source pin:** `25830fe7462bb9e29bc4087e6ae14f3f84cec377`  
**Modern cuts checked:** `3e0ed0794498506520ae62c997a5c852ac672061`; protected `6a5c12f04323d74001f9632063ec907f4fc4468e`  
**Mode:** documentary source-only; no scientific execution, tests, CI, raw respondent bytes, product edits, protected merge, subagents, or new A/B inventory.  
**Write scope:** `WORKER_REVIEWS/DDM_VOSKRES1059_R2_G5/` only.  
**Overall verdict:** `REVISE_EXACT_DEFECT` for G1/G2/G3/G4; G5 performed. The source-executable core is substantially sound, but the candidate is not a complete canonical accounting or a complete composed-input graph. One bounded correction package is required; HQ publishes; no further review round.

## 1. Custody and method

I read the user five-job slate, the mandatory `1059_METHODOLOGICAL_CORRECTION.md`, the frozen A/B/HQ R1 returns, and all nine R2 payload files. I inspected the original sources with `git show` at the cited pin and modern sources at `3e0ed079` and `6a5c12`; I did not checkout a huge archive, clone, or execute scientific functions.

Independently verified:

- All nine R2 payload hashes match `WORKER_RETURNS/DDM_VOSKRES1059_R2/MANIFEST.json`.
- `git diff --name-only 819dc54c..7ebd363d -- A_R1 B_R1 HQ_R1` is empty. The raw first-pass returns were preserved; only R2 files changed.
- The candidate worktree HEAD is exactly `7ebd363d`; parent is exactly `819dc54c`.
- The C4R1 return blob `efe49ce5b9b93d19a49e321a44e8148987fad67b` and crosswalk blob `2d56586980f768303f21567ce93922edddf605cb` match the candidate citations.
- The cited source blobs (`ddm_v550_branching.py` `8f6d40e0...`, `build_determinicity_repository_v550.py` `04f3a364...`, `ddm_v552_structural.py` `0df56d70...`, `ddm_v551j_packets.py` `740bae4c...`, `ddm_v552j_handoff.py` `476e6173...`, `ddm_v553_canonical_harmonization.py` `1951ada5...`, `ddm_v553_harmonization.py` `153f3dbe...`) match.

The candidate's self-critical holds are real: this is source-only, not historical execution. That honest historical HOLD is preserved. It does not excuse the concrete machine-cell and documentary defects below.

## 2. G1 — canonical accounting: `REVISE_EXACT_DEFECT`

### Accepted subset (S1)

- `G1-01`/`G1-02` are correct. `ddm_v550_branching.py:269` selects one primary by `max(mutual_information, cramers_v, n_unweighted)`; `:276-289` loops over remaining candidates and evaluates `joint_mask = primary_mask & candidate_mask`. That is at most `k-1` primary-vs-candidate joint evaluations, not all-pairs `O(k^2)`. The entropy/groupby cost inside each evaluation remains unbounded, as the candidate says.
- `G1-03`..`G1-06` are correct. `branch_nodes_rows(..., max_depth: int = 3)` is a default; `:397-399` stops on depth/support/no indicators; `:419-425` stops on no gain and expands the top two values. The wave shard exposes `--max-depth` default 3 at `build_determinicity_wave_shard_v550.py:856` and passes `args.max_depth` at `:1633`. `pure_or_near_pure` is a label at node creation, not the early-return test.
- `G1-07`..`G1-10` are correct for the targeted cells. `_question_checkpoint_exists` at `build_determinicity_repository_v550.py:972-992` requires the complete marker, a readable/nonempty `question_use_contract` parquet, a nonempty saved hash, and equality with the recomputed contract hash. `:995-1002` writes the table/marker. The narrow scope (one table plus marker, not all bodies) is accurately stated.
- The raw first-pass files remain immutable in the candidate commit. `G1_CANONICAL_ACCOUNTING.tsv` is a valid supersession ledger for the ten rows it actually addresses.

### Exact defects

**G1-D1 — an unconditional depth-3 machine cell remains authoritative.**  
`WORKER_RETURNS/DDM_VOSKRES1059_B_R1/COST_CARDINALITY.tsv:9` (blob `ed7499943a33e24af9c9ff55d6bab6874a0e85b9`) still says:

> `nodes <= 2^(depth+1)-1 with depth<=3; each node scans up to 12 indicators and expands top 2 values`

`G1_CANONICAL_ACCOUNTING.tsv` has no row for `B_R1/COST_CARDINALITY.tsv`. A machine consumer reading the B first-pass cost table finds no supersession and keeps `depth<=3` as a hard cap. The candidate's own `SELF_CRITICAL_HELD_EDGES.tsv` H-09 correctly says depth is a default, not a cap, so the omission is internally inconsistent. This is exactly the false cell the correction was required to supersede. `MANIFEST.json:58` overstates the result as “canonical machine cells corrected for ... unconditional depth-3”.

**G1-D2 — the supersession keys are not uniformly machine-joinable.**  
The `source_row_key` column mixes three different key types. `G1-01/03/07` use the A cost table's `family` value; `G1-04/05/08/09` use stable `tsm_id`/`id` values; `G1-02` and `G1-10` use prose prefixes (“row beginning …”) because `A_R1/SOURCE_LEDGER.tsv` (blob `086eab1a51fa17c13b5d44337d364a1c134b9f62`) has no `claim_id` column. Worse, the G1-10 prefix also occurs inside the correction row `CORR-A-01` at `A_R1/SOURCE_LEDGER.tsv:33`, so a textual prefix search can match the false row and its correction. There is no `source_row_number`, `source_column`, or `source_file_sha256` to disambiguate. The ten rows are a useful ledger, but not an unambiguous usable canonical view.

### Least correction (owner: R2 author; HQ publishes)

1. Add `G1-11` for `B_R1/COST_CARDINALITY.tsv:9`, using the same correction as G1-03 and the exact source lines `ddm_v550_branching.py:372,397-399,425` plus `build_determinicity_wave_shard_v550.py:856,1633`.
2. Add stable machine coordinates to every G1 row: `source_file_sha256`, `source_row_number`, `source_column`, and `source_cell_value` (or an equivalent canonical corrected TSV with a `superseded_by` column). Replace the two prose prefixes with row numbers 5 and 14 and column `claim`.
3. Re-freeze the corrected G1 file and update `MANIFEST.json:58` so it no longer claims completeness it does not have.

## 3. G2 — composed graph and all V553 inputs: `REVISE_EXACT_DEFECT`

### Accepted subset (S1)

- Ordinary `V550 -> V551 -> V552` edges `O-01..O-07` are source-grounded: per-country prefetch/harmonization, answer distributions, bridge lanes, direct-table atom promotion, coverage, and V552 pressure observation/denominator rules all match the cited code.
- Joint `V550J -> V551J -> V552J` edges `J-01..J-09` are source-grounded: prepared country substrate, same-person pattern counts/denominators, exact V551 atom matching, component/certification gates, producer-bound join, and V553 compatibility exports match the cited code.
- The V552J reduced-carrier finding is correct. `compile_v552j_structural_handoff.py` loads the V551J certified/review packets and V552 facts/keys; `ddm_v552j_handoff.py:79-142` does not load the V551J component index or same-grain component vectors. The V553 canonical adapter at `ddm_v553_canonical_harmonization.py:500-640` does not dereference V551J and leaves its V551J root/certified/reviewable fields empty.
- The canonical V553 surface checks join/input/handoff row-count equality, exact frame equality, declared-vs-actual probe/temporal counts, and temporal field `False`. The `V-01..V-04` stage semantics are correct.
- The prior C4R1 seven information-loss gaps and `0/9` positive load are accurately cited as banked prior evidence.

### Exact defects

**G2-D1 — `G2_V553_INPUTS.tsv` omits four canonical V553 inputs that the candidate's own `V-02` says are checked.**  
`ddm_v553_canonical_harmonization.py:47-51` defines `manifest.json`, `manifest/v552j_v553_handoff_manifest.json`, `packets/v552j_structural_join_index.parquet`, and `audits/v552j_join_audit.parquet`; `:86-88` lists the join and audit as required canonical artifacts; `:414-520` reads the manifest, handoff manifest, join index, input index, and handoff index, and `:510` uses `join_df` for row-count equality. `G2_V553_INPUTS.tsv:2-11` lists the input index, handoff index, readiness, V552 facts/keys, overlays, thin readiness, sidecar, V551J pointer, and obsolete packet, but not the producer manifest, join index, join audit, or handoff manifest. The table is labeled “all actual V553 input surfaces”, so this is a material omission, not a naming preference.

**G2-D2 — the “obsolete” packet and V551J dereference are still actual legacy V553 inputs.**  
`ddm_v553_harmonization.py:386-387` reads `packets/v552j_structural_handoff_packet.json` when present; `:391-408` dereferences the V551J certified/reviewable packet frames and collects relation/target/driver IDs; `:399-412` loads the V552 optional pressure tables (relation axis, target entity, driver facet, structural channel, horizon constraint). The candidate's `V-04` includes `ddm_v553_harmonization.py:340-465,519-655` as the wave bundle, yet `G2_V553_INPUTS.tsv` IN-09 says V551J is “upstream provenance only” and IN-10 says the packet is “obsolete/non-authoritative” without noting the legacy read. The canonical adapter does not depend on the packet; the legacy harmonization does. “All actual V553 inputs” must distinguish canonical vs legacy.

**G2-D3 — `J-07` omits the V551J candidate bundle.**  
`compile_v552j_structural_handoff.py:108` verifies three V551J artifacts: `v551j_joint_packet_candidate_index.parquet`, `v551j_certified_joint_packet_index.parquet`, and `v551j_review_surface.parquet`; `:117-121` requires the candidate index to enrich review rows. `G2_COMPOSED_GRAPH.tsv:16` lists only “V551J certified/review bundles”. The candidate bundle is an actual V552J producer-verification input.

**G2-D4 — the V550J respondent-membership output and its loss at V551J are omitted.**  
`ddm_v550j_joint_patterns.py:3514-3550` builds and `:5280` emits `joint_pattern_respondent_membership` with respondent identity/weight/answered-item data. `compile_v551j_joint_evidence_packets.py:1140-1210` has no membership path. The prior D11 aggregate result (in-tree at the original pin) records exact respondent membership as stranded after V550J. `G2_COMPOSED_GRAPH.tsv:11` omits this output, and `G3_SELECTED_JOINT_PATH.md` does not state that exact respondent identity is lost when only aggregate item membership reaches V551J. This is a substantive knowledge-loss edge, not a formatting omission.

### Least correction (owner: R2 author; HQ publishes)

1. Add `V553-IN-11..14` for the canonical manifest, join index, join audit, and handoff manifest, with the exact reader/role/evidence lines above.
2. Add `V553-IN-15..17` for the legacy packet, V551J certified/reviewable frames (dereferenced, not merely provenance), and V552 optional pressure tables; label the reader `ddm_v553_harmonization._load_wave_bundle` and keep the canonical adapter rows distinct.
3. Add the V551J candidate bundle to `J-07`/`J-08` input fields and evidence.
4. Add `joint_pattern_respondent_membership` as a V550J output and a `V550J -> V551J` loss/refusal row: aggregate pattern/item membership survives; exact respondent identity does not. Cite `ddm_v550j_joint_patterns.py:3514-3550,5280`, `compile_v551j_joint_evidence_packets.py:1140-1210`, and the D11 §8 result.
5. Re-freeze `G2_COMPOSED_GRAPH.tsv`, `G2_V553_INPUTS.tsv`, and `MANIFEST.json:59`.

## 4. G3 — concrete respondent-joint path: `REVISE_EXACT_DEFECT`

### Accepted subset (S1)

- The stage formulas in `G3_SELECTED_JOINT_PATH.md` are source-grounded: V550J pattern counts/probabilities/denominators; V551 direct-lane atom promotion; V551J exact scope/question/var/response matching and certification; V552 pressure denominator/weight/sign rules; V552J exact-scope semantic score and permission gates; V553 canonical/probe-only consumer. The `mutual_information` mislabel, the non-collapsible denominators, the V551 derived-lane exclusion, the V552 unresolved-denominator refusal, and the V552J temporal-field prohibition are correctly stated.
- The historical HOLD is valid. C4R1 §5 records `POSITIVE_LOAD_PROVED = NO`, `0/9` coverage, and no respondent-level substrate; `section85/CURRENT_STATE.json` independently records `real_empirical_j_chain_status = NOT_RUN_REQUIRES_LIVE_RESPONDENT_DATABASE_AND_PYARROW` and `archive_contains_respondent_level_substrate = false`. No raw source or invented run is required to correct the documentary defects.

### Exact defects

**G3-D1 — no concrete respondent-joint family is selected.**  
`G3_SELECTED_JOINT_PATH.md:16` says the path is instantiated by “any exact `(run_id, source/source_family, canonical_wave, country_code, family_id, pattern_id, item_order, question_id, var_code)` tuple that satisfies the gates. All fields named below are real producer/consumer fields.” That is a field schema, not a concrete family. The task requires at least one concrete respondent-joint family traced as far as evidence permits, with exact missing links. The candidate never names a `family_id`, source/wave/country, or item set.

An authorized aggregate lead is available and was not used: `data/ddm_build_copy/manifests/question_family_registry.yaml:7` defines `gss_abortion_condition_family`; `section85/authority/bounded_joint_configuration_authority.csv` row `JCFG-GSS-ABORTION-CONDITIONS` (GSS 2010 US, six items) and `bounded_joint_configuration_item_crosswalk.csv` rows for `abdefect`, `abhlth`, `abrape`, `abany`, `absingle`, `abnomore` give a concrete configuration. The candidate could trace that family to the exact missing V550J run/prepared substrate, pattern/item rows, V551 manifest/atoms, V551J packet, V552 fact, V552J join, and V553 output, without reading raw respondent bytes.

**G3-D2 — the headline serializes independent branches into a false causal chain.**  
The headline at `G3_SELECTED_JOINT_PATH.md:5` is:

> `V550J same-person joint pattern -> V551 directional atom -> V551J certified joint packet -> V552 structural pressure fact -> V552J exact-scope join -> V553 canonical/probe consumer`

The actual graph is a diamond, not a serial chain. V551 atoms come from ordinary V550 `answer_distribution`/`country_answer_distribution` direct-lane bridge rows (`ddm_v551_atoms.py:21,123,141-158`), not from the V550J pattern. V550J patterns and V551 atoms converge at the V551J component matcher (`ddm_v551j_packets.py:1114-1160`); V551 atoms independently feed V552 structural facts (`ddm_v552_structural.py:100-199`); V551J packets and V552 facts converge at V552J (`ddm_v552j_handoff.py:79-142`). The G3 table's J3 row actually names the ordinary V550 distribution inputs, and J4 names “V551 atom + one V550J pattern item”, so the table contradicts its own headline. The headline as written asserts a non-existent `V550J pattern -> V551 atom` edge and hides the parallel input graph.

### Least correction (owner: R2 author; HQ publishes)

1. Select one concrete family, preferably `JCFG-GSS-ABORTION-CONDITIONS` / `gss_abortion_condition_family` (GSS 2010 US, six items above), or another bounded-nine family with a clear authority. State the exact family/source/wave/country and ordered items.
2. Trace that family through each stage with real authority identities and explicit missing links: family registry/crosswalk -> V550J prepared substrate (missing run/manifest) -> V550J pattern/item/relation (missing pattern_id/rows) -> V551 atoms (missing V551 manifest/atom rows) -> V551J packet (missing certified/review packet) -> V552 fact (missing structural fact) -> V552J join (missing join) -> V553 output (missing canonical output). Mark `SOURCE_EXECUTABLE` vs `HISTORICAL_EXECUTED = NO`.
3. Replace the headline with the actual parallel/diamond input graph: `(V550J prepared pattern/index) || (V550 ordinary distributions -> V551 atoms)` converge at V551J; V551 atoms also feed V552 facts; V551J packet + V552 fact converge at V552J; V552J -> V553 probe. No `V550J -> V551 atom` edge and no `V551J -> V552 fact` edge.
4. Add the exact-respondent membership loss from G2-D4 to the concrete path.
5. Re-freeze `G3_SELECTED_JOINT_PATH.md`.

## 5. G4 — old-to-FORGE mapping and conditional index: `REVISE_EXACT_DEFECT`

### Accepted subset (S1)

- `G4_CONDITIONAL_INDEX_TRACE.md` is source-grounded and correctly self-limited. `ddm_v551_conditional.py:157-236` defines `build_conditional_determinicity_index`; a tree-scoped search finds no in-tree importer/caller and no `__main__`; `compile_v552_structural_ddm.py:284-309` reads/passes the optional parquet but `ddm_v552_structural.py:253-259` only creates an empty audit; V551J's required inputs at `compile_v551j_joint_evidence_packets.py:1140-1210` do not include it. The disposition `HELD_LOCAL_UNCONSUMED_AUXILIARY_CAPABILITY_WITH_NO_PROVED_HISTORICAL_PRODUCER_OR_READER` is correct, and the distinction between local V552 non-use and global loss is preserved.
- The modern absence conclusion is independently true. `git grep` at both `3e0ed079` and `6a5c12` finds no `conditional_determinicity` in `rawlsing_next`; `v551j`/`v552j` appear only in `pre553_legacy_compat.py` and tests. `pre553_diagnostics.py` blob `32a2d063...` is identical at both cuts. No stale absence was found.
- G4-01/G4-02/G4-04/G4-05/G4-09/G4-10 are honest about partial, related, different-grain, or unproved conservation; they do not claim parity from a name or a primitive.

### Exact defects

**G4-D1 — producer/guard cells are labeled as “first reader/call site”.**  
`G4_OLD_TO_FORGE.tsv:4` (G4-03) names `produce_governed_diagnostics (pre553_diagnostics.py:622-752)` and `assert_diagnostic_only_use (:606-620)` as the modern first reader/call site. `produce_governed_diagnostics` is the producer; `assert_diagnostic_only_use` is a guard. At `3e0ed079` and `6a5c12`, the only consumers are tests (`rawlsing_next/tests/test_pre553_diagnostics.py`); there is no production first reader. `G4_OLD_TO_FORGE.tsv:7` (G4-06) similarly lists `execute_empirical_query -> produce_governed_diagnostics`, both producers. The dispositions are diagnostic-only/different-grain, but the “first reader” column overstates modern production consumption. The task requires actual product/first reader/evidence, not a producer presented as a reader.

**G4-D2 — the conditional-index modern absence is supported by a prior PROGRAMMA row, not a cut-scoped primary search.**  
`G4_OLD_TO_FORGE.tsv:8` (G4-07) cites the PROGRAMMA G3A row `G1A-FUNC-012` as the modern evidence. That row is a valid lead and its conclusion is true, but the task says PROGRAMMA is not a replacement for primary proof. The candidate should add the exact cut-scoped search result at `3e0ed079` and `6a5c12` (no `conditional_determinicity` in `rawlsing_next`) and the actual modern disposition `pre553_legacy_compat.py:112-123`, which disables `V551J_OBJECT_PARITY` and `V552J_OBJECT_PARITY` for lack of authority.

**G4-D3 — G4-08 omits the actual modern J-parity gate.**  
`G4_OLD_TO_FORGE.tsv:9` (G4-08) says “no modern V551J component/packet carrier or V552J equivalent was found” and cites C1 composition plus prior C4R1. The modern tree also contains `rawlsing_next/pre553_legacy_compat.py` (blob `5498ff8b979379386f1d5fa7a44ed22131721ece` at both cuts), whose docstring says it deliberately does not import/discover/parse/execute V550-V552 modules/artifacts (`:4-6`), and whose `V551J_OBJECT_PARITY`/`V552J_OBJECT_PARITY` rules are disabled at `:112-123` with `P04_DOES_NOT_NAME_OBJECT_SPECIFIC_J_NEUTRALITY_AUTHORITY` and `P04_NAMES_NO_J_OR_V552J_CARRIER_EQUIVALENCE_AUTHORITY`. That is the exact modern product/evidence for the J-family parity question and should be in the table.

### Least correction (owner: R2 author; HQ publishes)

1. In G4-03 and G4-06, replace the producer/guard entries with `NONE_IN_PRODUCTION` for a first reader, and separately record the producer/guard roles and test-only consumers. Add exact paths/blobs/lines for `pre553_diagnostics.py:493-628,622-784` and `rawlsing_next/tests/test_pre553_diagnostics.py`.
2. In G4-07, add the cut-scoped `git grep` result at `3e0ed079` and `6a5c12`; keep the PROGRAMMA row as a lead, not the primary evidence. Add `pre553_legacy_compat.py:112-123`.
3. In G4-08, add `pre553_legacy_compat.py:4-6,112-123` as the actual modern J-parity gate, with disposition `COMPATIBILITY_GATE_DENIES_J_PARITY`, not a carrier and not a conservation proof.
4. Re-freeze `G4_OLD_TO_FORGE.tsv`; retain `G4_CONDITIONAL_INDEX_TRACE.md` unchanged as accepted S1.

## 6. G5 — independent gate, preserved results, and remaining finite obligations

This is the independent G5. It is not self-acceptance by the author, and it does not claim production or full scientific conservation execution. The accepted subset is documentary/source-executable only. The negative evidence is preserved: no historical V551J/V552J/V553 output row, no positive-load run, no raw respondent substrate, no modern same-grain J carrier, no proved conditional-index producer invocation or reader.

The bounded omission challenge used four alternate actual leads, without repeating the completed ZAK survey: the legacy V553 receiver `ddm_v553_harmonization._load_wave_bundle`; the V550J `joint_pattern_respondent_membership` output; the authorized aggregate bounded-nine GSS family authority; and the modern `pre553_legacy_compat.py` J-parity gate. These are aggregate/source artifacts, not raw respondent bytes.

### Preserved prior results

- G1's three technical corrections (k-1 primary comparisons, configurable depth default 3, marker+contract-hash resume) are source-proven and remain useful.
- G2's ordinary/joint stage graph, V552J reduced carrier, V553 canonical adapter behavior, and C4R1 seven-loss-gap citation are source-proven at the cited cuts.
- G3's stage formulas and historical HOLD (`0/9`, no substrate) are valid; no invented run or synthetic row was used.
- G4's conditional-index trace and `HELD_LOCAL_UNCONSUMED_AUXILIARY_CAPABILITY` disposition are accepted S1; the modern J-parity denial is additional negative evidence.
- The raw A/B/HQ R1 files are unchanged.

### Explicit HOLDs (indispensable artifacts, not required to correct the documentary defects)

- **G3 historical execution:** actual V550J/V551J/V552J/V553 output rows or a positive-load run receipt for a selected concrete family/wave/country. Status `HOLD_EXACT_EVIDENCE`. The concrete family trace can and should be done from the bounded-nine authority without this artifact.
- **G4 conditional-index historical producer/reader:** a real producer invocation writing `conditional_determinicity_index` with a run id and nonempty rows, or a real numeric/structural reader. Status `HOLD_EXACT_EVIDENCE`. The old-to-FORGE table can be corrected from source without this artifact.

### Remaining finite obligations

1. R2 author: apply the G1, G2, G3, and G4 least corrections above in one bounded pass under the existing write scope; do not start a new A/B survey, new general inventory, scientific execution, tests, CI, raw-data read, product edit, or protected merge.
2. R2 author: re-freeze the corrected R2 payload and update `MANIFEST.json` hashes and claims; HQ publishes to #1060/#1059.
3. HQ: no further review round is required for these exact corrections; if a new frozen candidate is separately commissioned, it must be a distinct source-aware G5. Do not self-accept.
4. If an authorized historical aggregate/output artifact later becomes available, close the G3/G4 HOLDs; do not manufacture a run or substitute synthetic data.

## 7. Stop

The finite pass stops here. The candidate is not accepted as a complete canonical accounting or complete composed-input graph. The exact defects are reproducible from the cited source cuts and machine cells; the least corrections are bounded and do not require an ungranted raw source or a new scientific execution. HQ owns publication and the #1060/#1059 update.
