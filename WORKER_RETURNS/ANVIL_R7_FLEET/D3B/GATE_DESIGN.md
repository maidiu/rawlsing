# GATE_DESIGN — D3B minimal executable correction to the ANVIL R7 instrument

**Status:** local, sourcefree instrument correction in a private package copy. **No architecture selected.** No source/native/science/actor/protected/H1 authority is created. This is an author return awaiting the HQ integrator and a distinct C.

**R2 source-custody correction (HQ receiving):** the r1 `source_kind` field was caller-controlled and `_verify_file` skipped Git verification when it was set to `SUPPLIED_ZIP`; the aggregate grade then credited the skipped check as Git-verified. The attack was reproduced against the immutable r1 commit. R2 removes caller provenance selection: every family is bound in code to an independently pinned Git commit/path/blob/byte hash or to the original supplied ZIP SHA-256 plus exact member. `--repo` is required for Git families and `--zip` is required for ZIP families; omission is RED, not an unverified PASS. The mixed grade is `GIT_AND_ZIP_PINS_VERIFIED`; it is never reported as all-Git.

## 0. Exact inputs and currentness

| Item | Exact pin |
|---|---|
| Protected PRE-MAIN / currentness | `31291d08179890852246c8742700e055168e9933`; PYAT progress rev10 |
| K3 protected documentary cut | `7fc00289dd801d2d0a8ce159986c7595fc27a4d9` |
| K3 29 TSV | Git blob `a91214b9fd89ab97897ec1c3cd48cb5285b7029c`, file SHA-256 `0dfe6539f1a1f7f028c5968c0e85078cbf5f80a847d0c94ea1929f57d20c052d` |
| K3 26 TSV | Git blob `1f5a3ae8a40593dccf34753c9fa9577155ebf163`, file SHA-256 `6d0766ecc637ee03a705c1772e7bcda39c09c9534f0672cd36a27cfa85e0dfa2` |
| K3 14 TSV | Git blob `5a84ca8cb0a2b16d4a68b2200fa426fd9451b343`, file SHA-256 `8adf74cfbf2e916f41641f5836ab82305059b59e1665a2e1647dfb6bdeb0e9d3` |
| SEAM/25 | `596f1230258ff50f98d8543dec42a80e696720f4`, blob `181ab1aaee26d71524dd7401a59c2ca550b4a81c`, file SHA-256 `589379644edbb9f59734d5fe40787683e6836b073a3ba69649cfd5035432c17e` |
| SEAM/26 | `796452b8cb788fa5a02f37a7ce86eafce8312dfe`, blob `a05c21dd0b7b1d404fc500c0ef36c81aee67c96e`, file SHA-256 `a53c62b3f68a54947a26be2e8878d1f89bff1ad057833ef4f8c80f38ab9fb50c` |
| ANVIL/15 | `3cc09bba3d0e26c226da0ddca4b64c43dd74e493`, blob `6253a632d10f201e0bf446f055f96c82fb4a479f`, file SHA-256 `0e09bc34235923b7f7b34d272b8e7cddcea0d4e524953f56665843bba6a0c50a` |
| Supplied ZIP | SHA-256 `526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332`, 280 files |
| `02_BOUNDARY_CONTRACTS.json` | file SHA-256 `89db35d554bbc693eac14595964ab1fe5574bc521e1ab9438e677c48c256502a` |
| `03_FROZEN_SOURCE_CUTS.json` | file SHA-256 `cf26afb1264ce0ff44c1159e4143a261928f8712db33a7a07c1d0763565ba854` |
| Built 118 inventory | SHA-256 recorded in `TEST_TRANSCRIPT.json`; 118 entries, counts 29/26/14/10/8/8/7/16 |

The shared source and product code were not modified. All edits are under `WORKER_RETURNS/ANVIL_R7_FLEET/D3B/PACKAGE/ANVIL_R7/`.

## 1. Observed defects in active `tools/r7_integrated.py`

1. **False S1 blockage / forced synthetic spine.** `check_frame` required `historical_source_spine.schema` to be `ANVIL_SPINE_R5` or `ANVIL_SPINE_R6` and required the transfer coverage to equal the spine coverage. R5 provenance says the campaign was `PREPARED / LOCALLY STRUCTURALLY TESTED / NOT DISPATCHED`; a completed P2 SPINE was an expected **output**, not a historical accepted input. A genuine source-only inventory therefore could not pass without inventing a fake spine.
2. **Circular transfer.** `r7_transfer_conservation.py` copies a coverage dictionary and hashes the same bytes. Equality/hash checks prove internal consistency, not source identity. A synthetic spine authored together with a synthetic transfer passes.
3. **False S3 no-loss acceptance.** `check_decision` reconciled only `frame.requirements` (nine mission domains in the test fixtures). It never required the 118 mixed identities to receive candidate-specific dispositions. A decision could print local PASS while silently omitting/retiring most of the historical/prospective universe.
4. **False C acceptance.** `check_C` checked prose, card shape and decision re-validation, but not T1–T7 positive/negative/restore evidence, not a typed producer/authority/time/consumer graph, and not an actual builder handoff.
5. **Local H1 leakage risk.** Nothing in the active packet explicitly forbade a local field/flag from claiming H1 or protected receiving; the old R5 `anvil.py` had stronger local ceilings and six deterministic projections that the active gate did not restore.

## 2. Corrected S1/FRAME boundary

**Required input:** `source_inventory` pointer to `ANVIL_R7_SOURCE_IDENTITY_INVENTORY` in the evidence root. The inventory is source-authenticated by exact bytes and, when `--repo` is supplied, by Git commit→path→blob→bytes verification.

**S1 checks (all must hold):**

- exactly 118 entries and exact group counts `K1_CAP=29`, `PYAT_PC=26`, `P4R=14`, `SEAM_B=10`, `SEAM_S=8`, `ANVIL_L=8`, `BOUNDARY=7`, `TERMINAL=16`;
- exact IDs match `03_FROZEN_SOURCE_CUTS.json` mandatory groups (K3 IDs also re-censused from the TSVs, not from the inventory);
- every K3 row has exact raw row SHA-256 at the protected commit and file blob;
- every B/S/L row has an exact excerpt present in the pinned SEAM/ANVIL file;
- every T1–T7 and terminal ID is present in the supplied ZIP contracts;
- `PYAT_PC` entries have `adopted: false`; `P4R` entries have `closed: false`; no entry may claim adoption/closure;
- each entry has an independently pinned canonical origin (commit/path/blob/bytes or `526d…` ZIP member/bytes), not a caller-chosen `source_kind`;
each entry has non-vacuous `source_semantics`, `negative_meaning`, `consumer_or_hold`, `why` and an origin hash;
- source-file hash mutation, caller `source_kind` reclassification, wrong/nonexistent commit/path/blob, replacement bytes with matching caller hashes, false ZIP member, missing row, missing B-10, omitted `--repo`/`--zip`, or false adoption/closure fails RED.

**No disposition is allowed at S1.** A source inventory that claims `PRESENT_PRESERVED`/`FUTURE_NONPRECLUDED` is over-claiming; dispositions live only in S3.

**Legacy spine:** if present, it is optional historical transfer evidence only. It is checked for its own internal history shape but **cannot substitute** for `source_inventory`. A frame with only a synthetic R5/R6 spine is RED.

## 3. Corrected S3/DECISION boundary

**Required:** every one of the 118 identities receives one candidate-specific row in `identity_dispositions`, with:

```json
{
  "identity_id": "K1-CAP-01",
  "disposition": "PRESENT_PRESERVED | FUTURE_NONPRECLUDED | EXACT_OWNER_HOLD | BLOCKING_LOSS | REFUSED_AUTHORITY | RETAINED_HISTORICAL_NONADOPTED",
  "status_assertion": "RETAINED | NOT_ADOPTED | HELD | INCLUDED_NOT_ADOPTED",
  "evidence_grade": "DOCUMENTARY | CODE_STATIC | EXECUTED_SOURCEFREE | EXECUTED_NATIVE | UNVERIFIED_HELD",
  "design_effect": "non-vacuous candidate-specific effect",
  "first_consumer_path": "non-vacuous path or named hold",
  "conservation_or_refusal_witness": "non-vacuous positive/refusal/restore witness",
  "origin_sha256": "must equal the verified inventory row hash",
  "adopted_by_this_decision": false,
  "closed_by_this_decision": false,
  "evidence": {"path": "...", "sha256": "...", "exact_excerpt": "..."}
}
```

Fail-closed rules:

- missing/extra/duplicate identity, or 53-row partial crosswalk substituted for 118 → RED;
- any `PYAT_PC` `adopted_by_this_decision` not false or `status_assertion=ADOPTED` → RED;
- any `P4R` `closed_by_this_decision` not false or `status_assertion=CLOSED` → RED;
- any `RETAINED_HISTORICAL_NONADOPTED` on a K1/B/S/L/T/terminal identity → RED (silent historical retirement);
- `BLOCKING_LOSS` with `AUTHOR_PROPOSED_PENDING_C` → RED; `EXACT_OWNER_HOLD` on a present-hard frame requirement → RED;
- any origin hash drift, wrong source excerpt or missing evidence → RED;
- local `h1_received_by_local_check` or `protected_received_by_local_check` true → RED;
- local **typed whole-machine graph** must have nodes with producer, producer-authority, input/output types, time mode and first consumer, and edges with data type, authority grade, temporal mode, negative/refusal, invalidation and T1–T7 boundary; every T boundary needs an edge; fictional/modeled → observed backflow is RED.

The decision grade remains `AUTHOR_PROPOSED_PENDING_C`; local PASS is not architecture acceptance.

## 4. Corrected C_INTEGRATED boundary

A distinct C packet must include:

- `boundary_court` for **T1–T7**, each with non-vacuous `positive`, `negative`, `restore`, `grade` (`EXECUTED_AT_SCOPE`, `SOURCE_STATIC_CONSERVED`, `NOT_RUN`), `first_consumer_or_hold`, and exact evidence; missing any of positive/negative/restore → RED; `NOT_RUN` requires an exact hold; admit-with-NOT_RUN → RED;
- `graph_audit` with `producer_authority_time_consumer_checked: true`, `holes: []`, and all seven boundary edges checked; a hole → RED;
- `builder_handoff_review` non-vacuous; `actual_first_reader_verified: true` only if a real reader was executed; otherwise C must say `C_HOLD_EXACT`;
- two builder cards (present/future); `EXACT_BUILDER_HOLD` is honest but cannot support `C_CONDITIONALLY_ADMIT_DESIGN`;
- no self-declared independence (`reviewer_relationship` must stay `DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION`), no surviving choice-reverser on admit, no fake source/owner grant, and no local H1/protected claim.

**C is not H1.** The gate only checks that the C packet is structurally complete and honest; external independence, actual execution and protected receiving remain outside.

## 5. Restored R5 source-byte validation and six projections

`tools/r7_inventory.py` restores the useful R5 mechanics for the active instrument: exact file bytes, Git blob/commit/path verification, per-row hashes, exact excerpt presence, ID census, and false-promotion checks. It does **not** import an R5 SPINE.

`tools/r7_build.py` deterministically projects the verified decision into six first-reader artifacts:

1. `DESIGN_DECISION.md`
2. `IDENTITY_DISPOSITIONS.tsv`
3. `BOUNDARY_CONTRACT_MAP.json`
4. `TYPED_GRAPH.json`
5. `EVIDENCE_INDEX.jsonl`
6. `BUILDER_HANDOFF.json`

`verify` re-derives and byte-compares all six plus `MANIFEST.json`; a changed projection is RED; restore is byte-identical. See `COLD_BUILDER_OUTPUT_SPEC.md`.

## 6. Required positive / negative / restoration matrix (actually run)

Commands and exact return codes are in `TEST_TRANSCRIPT.json`; the suite is `tools/test_r7_integrated.py` (24 tests, local sourcefree).

| Required case | Test | Observed |
|---|---|---|
| valid source-only 118 inventory S1 PASS at documentary grade | `test_source_only_118_inventory_s1_pass` | PASS (`GIT_AND_ZIP_PINS_VERIFIED`) |
| caller `source_kind`/ZIP bypass | `test_caller_source_kind_bypass_is_red` | RED |
| optional `--repo`/`--zip` omission | `test_optional_repo_or_zip_cannot_authenticate` | RED |
| wrong/nonexistent commit/path | `test_wrong_commit_path_and_nonexistent_path_red` | RED |
| caller replacement bytes with matching hashes | `test_caller_replacement_bytes_with_matching_hashes_red` | RED |
| false ZIP member | `test_false_zip_member_red` | RED |
| synthetic SPINE as fake original RED | `test_synthetic_r5_spine_alone_is_not_a_source` | RED `FRAME:NO_SOURCE_IDENTITY_INVENTORY` |
| missing row/blob RED | `test_missing_k3_row_red`, `test_source_byte_mutation_red_and_restore` | RED then restore PASS |
| missing B10 RED | `test_missing_b10_red` | RED count drift |
| 26 newly adopted or 14 closed RED | `test_26_adopted_or_14_closed_red`, `test_new_adoption_or_closure_in_decision_red` | RED both layers |
| 53 rows complete but one historical identity missing → DECISION RED | `test_53_rows_complete_but_one_identity_missing_red` | RED incomplete 118 + 53 substitute |
| seven T contract negative/restore missing → C RED | `test_c_missing_boundary_negative_red_and_restore`, `test_c_missing_restore_red` | RED then restore PASS |
| typed graph producer/authority/time/consumer hole → C RED | `test_typed_graph_hole_red`, `test_c_graph_hole_red` | RED |
| no full-rival A/B required | `test_no_mandatory_ab_or_rival`, `test_optional_duel_requires_same_exact_evidence` | PASS/optional duel only |
| local fake H1 accepted → RED | `test_local_h1_claim_red`, `test_c_local_h1_red` | RED |
| six projections deterministic/restore | `test_six_projections_deterministic_and_restore` | PASS, then RED on byte change, then PASS |

**Full inherited R7 runner:** `python3 tools/run_r7_quality.py` → `PASS_LOCAL_SYNTHETIC_AND_FORMAT_ONLY`, 12 commands, all exit 0. R2 focused run: 29 tests OK. This does not authenticate native source, independent C or H1.

## 7. Why this is the least nonceremonial machinery

It adds **one inventory file, one 118-row disposition table, one C boundary court and one deterministic builder**. It does not add a tribunal, a new science owner, a new status bank, a mandatory rival architecture, or a mandatory full A/B. It removes a fake prerequisite (accepted R5 SPINE) and makes the existing S3/C claims falsifiable at the exact grain they were already supposed to cover.

## 8. Strongest alternative and counterexample

**Alternative considered:** keep the legacy SPINE path and merely add a `source_inventory` cross-check. Rejected because the synthetic path would remain sufficient whenever the cross-check is omitted/bypassed; the only safe rule is that a legacy SPINE is optional evidence and never identity truth. **Counterexample:** two rows with identical ID text but different meanings; ID-only coverage passes, while exact row hash + excerpt + origin fails. **Second counterexample:** a 118-row decision where one row says `PRESENT_PRESERVED` but its origin hash and first-consumer path are copied from another row; the gate fails on origin drift/vacuity (and C must inspect the actual consumer). **Third:** a C packet with all seven labels but identical generic positive/negative/restore text; the gate rejects short/vacuous fields, but only an external C can judge semantic adequacy — local PASS is deliberately not H1.

## 9. Honest limits / owner holds

- No native original SAV/DTA source execution, no 100k/6 GiB production benchmark, no independent C, no protected H1.
- The R5/R6 A/B comparators remain historical specialists; not mandatory.
- The inventory is **S1 documentary identity accounting**, not 118 accepted functions and not source rights.
- The 26 `PYAT_PC` rows remain `NOT_ADOPTED`; the 14 `P4R` rows remain `HELD`; no K4.
- The current `r7_integrated.py` decision schema still requires a candidate graph and 118 dispositions; it intentionally does not choose the physical architecture.
- No peer draft/worktree/branch was read; no sibling worker was dispatched. The trailing controller launch snippet was not executed because it conflicts with the explicit D1/D2 prohibition and controller/lease law.
