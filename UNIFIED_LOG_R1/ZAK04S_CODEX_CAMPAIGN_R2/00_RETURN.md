# ZAK-04S R2 — protected N9/N10W world-serving chain and the F6 entry boundary

**Return root:** `UNIFIED_LOG_R1/ZAK04S_CODEX_CAMPAIGN_R2/`. **Worktree startup:** `ba20eeeea2243edd71febe0af0bc184d1cfeef1e`. **Protected source cut:** `6a5c12f04323d74001f9632063ec907f4fc4468e`. **Session/model:** `ses_e22bd21eeffeH5GWvx2XBKwSEw`, `opencode-go/deepseek-v4.1-flash#max`. **Scope:** one finite documentary tract, S0–S1 static source only; no tests, scripts, execution, product edits or commits.

## 1. Direct answer

At protected `6a5c12f...`, the actual **N9/N10W sourcefree world-serving path** is:

`pre553_evidence_world_consumer.configure_evidence_world_context` (L66) → `read_prefix_evidence` (L35) exact R08 reader-to-prefix match → `pre553_universal_world_binding.configure_progressive_world_context` (L1117) → `SelectedWorldCatalog` T0/T1 snapshots → `progressive_world_view` (L1337) → `_progressive_world_receipt` (L1229) → local `sourcefree_world.p41_service.P41Service.progressive` (L108) + `pre553_world_conditioned_progressive_service.consume_world_conditioned_prefixes` (L110) → `sourcefree_world.nonparent.consume` (L6).

That path produces a **`PROGRESSIVE_WORLD_SELECTED_VIEW`** carrying:
- `n9_world`: selection mode, `valid_at`, `published_asof`, five modeled rules, `permission_root=TEST_ONLY_E04_SOURCE_ROOT`, `currentness=CURRENT_TEST_ONLY_SELECTION`;
- `n10e_steps`: exact denominator and raw cell support with exact evidence/producer refs;
- `n10w`: positioned consumptions and progressive update identity;
- `world_routes`: `training`, `civil`, `exit_constraint`;
- `actor_state="NOT_TOUCHED"`, `z_unresolved=True`.

**No F6 numerical evidence legitimately enters this chain.** The R08/evidence shape is an exact-denominator/raw-cell shape; F6P is a covered-subprobability/uncovered-mass partial-identification shape. `P41Service.progressive` requires `EXACT_SUPPORTED`, integer denominator > 0 and non-empty cells; `SelectedWorldCatalog` accepts an empirical identity and publishes fixed modeled E04 fields, with `grade='SYNTHETIC_NOT_OBSERVED'`. There is no adapter, field, or consumer edge that accepts `covered_subprobability`, `uncovered_target_mass`, or partial bounds. The bounded result is **`F6_NUMERIC_WORLD_ENTRY_NOT_PROVED`**, not global absence.

**Production status:** the protected functions exist and are internally coherent, but at this cut there is no external non-test production entrypoint. The only non-test imports are internal chain composition (universal binding lazily imports the evidence adapter and `sourcefree_world`; the adapter lazily imports universal binding); all external callers found are tests. The path is protected **test-only** code, not an operative selected N9 world.

## 2. Exact accepted input shape

### 2.1 R08 evidence reader
`configure_evidence_world_context(*, target_ref, conditions, prefixes, world_empirical, evidence_readers, ...)` requires exactly one `EvidenceConsumerReader` per prefix. `read_prefix_evidence` requires:
- `reader.request.source_universe_ref == prefix.consumer_query.source_universe_ref`
- `reader.request.release_ref == prefix.release_ref`
- target ref, consumer query ref, producer query ref, predicate ref/hash, canonical risk set, model-rule hash, ordered target refs, and condition count/value identity all match.

`EvidenceRequest` (L450+) carries source/dataset/wave/edition/byte digest/instrument, sampled/reporting unit, links, risk set, predicate, ordered targets/conditions, estimand, weight method, design, uncertainty method, direction/role/use, grammar, model rule, release/custody, four clocks, permission, producer/consumer query refs and consumer-binding fingerprint. `EvidenceResult` (L1078) carries `request_key`, eligibility/execution/result states, provenance, `denominator:int|None`, `cells: tuple[Mapping]`, evidence/producer refs, consumer result hash/values and typed refusal. `EvidenceConsumerReader.read()` (L2531) returns the signed envelope values plus `consumer_result_hash`, `consumer_result_state`, `consumer_result_material`, execution provenance/mode.

### 2.2 World empirical envelope
`world_empirical` must carry:
`source` (`universe`, `release_ref`, `risk_refs`, `qrefs`, `repo`), `release_ref`, `risk_refs`, `rows_hash` derived by `progressive_source_rows_identity(repository, release_ref)`, and `publication`. The source/release/risk/rows/repo must match every prefix; otherwise `PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH` is returned. In the accepted tests this envelope is built from synthetic `L01`/`R107` rows; `AdmittedEvidenceContext` uses `source_id='L01_SYNTHETIC'`, `dataset_id='L01_TEST_ROWS'`, `permission_ref=SOURCEFREE_TEST_ONLY`.

### 2.3 World output
`SelectedWorldCatalog` publishes five keys (`training_access`, `training_fee`, `exit_cost`, `civil_open`, `civil_sanction`) as `E04_MODELED_FIELD_VALUE@1`, `epistemic_class='MODELED_NOT_OBSERVED'`, `source_root='TEST_ONLY_E04_SOURCE_ROOT'`; its `empirical_identity()` hardcodes `grade='SYNTHETIC_NOT_OBSERVED'`. The progressive output is therefore a modeled, test-only selected-world view, not a source-native world.

## 3. Where F6 could legitimately enter — and why it does not today

F6P output (`016870e8...`) carries `covered_subprobability` (category/probability cells), `uncovered_target_mass` (rational string), disagreement/bias bounds, `decision=PARTIAL_IDENTIFICATION_ONLY` and `target_joint_status=NO_COMPLETE_TARGET_JOINT`. The world path expects:

| World path requirement | F6P actual | Result |
|---|---|---|
| `EvidenceResult.denominator` integer | no denominator | cannot bind |
| `cells[].raw_numerator_support` | probability cells | shape mismatch |
| `result_state='EXACT_SUPPORTED'` | `PARTIAL_IDENTIFICATION` possible | rejected by P41/N112 |
| `world_empirical.source/release/risk/rows/publication` | no such envelope | cannot construct selected world |
| modeled E04 field key/value | no field mapping | no entry |

A legitimate future entry would require an owner-issued **world-field or evidence adapter** that converts F6 covered/uncovered partial bounds into a new typed field with estimand, denominator/coverage semantics, uncertainty, permission and as-of scope. That adapter does not exist at `6a`; inventing it here would be new architecture/engineering, which is out of scope. An IF/OR direct route is legitimate only if a real owner issuer defines such a field; it is not a compulsory serial F6→N9 path.

## 4. Roadmap claim reconciliation

| Dated claim | Exact counterevidence at 6a | Grade |
|---|---|---|
| S09 POST-CAS3 says L01 reviewed R08 and R118 per-prefix sourcefree world service are protected via #702 | L01 adapter and R112 progressive service exist; `configure_evidence_world_context` and `progressive_world_view` are protected; but there is no external non-test entrypoint and output is `operative_N9=False` / `SYNTHETIC_NOT_OBSERVED` | `CODE_PRESENT_TEST_ONLY`; “protected sourcefree” true, “actual selected N9” NOT_PROVED |
| Earlier R2 note says R118 branch-only and R08 binder not statically imported by the P41 path | At 6a the R08 adapter exists and is lazily imported by `configure_progressive_world_context` via `_progressive_step` (`read_prefix_evidence`); but still test-only | dated note stale for source presence, correct for production adoption |
| “Old P41 Git-object executable dependency removed” | `_pinned_p41_runtime` returns local `rawlsing_next/sourcefree_world` package (L38-41, docstring: “historical pin is provenance only”); `P41_COMMIT`/`P41_PACKET` remain provenance constants; `_execute_p41_world` imports local `P41Service`/`SelectedWorldCatalog`; `_purge_p41_modules` has no caller | `LOCAL_RUNTIME_REPLACEMENT_CONFIRMED`; no Git-object execution |
| Roadmap says S09.1/S09.3/S09.4 `MISSING_PRODUCER_OR_READER`, native N9 held | Code shows modeled test-only world and no external non-test entrypoint; consistent | `CONSISTENT_WITH_CODE` |

The roadmap is therefore a **dated candidate guide**, not law. Its “protected” claim is true at the sourcefree code level but does not establish an operative selected N9/N10W world.

### 4A. P41 helper disposition at 6a

- **Active local path:** `_pinned_p41_runtime` returns `rawlsing_next/sourcefree_world`; `_execute_p41_world` imports local `P41Service`/`SelectedWorldCatalog`; `select_r05_world_view` invokes that local execution; `configure_progressive_world_context`/`progressive_world_view` invoke local P41 and R112. No `git archive` call was found.
- **Provenance/dead:** `P41_COMMIT` and `P41_PACKET` constants remain at L20-21 but are not used by `_pinned_p41_runtime`; `_purge_p41_modules` L56 has no caller. They are retained historical provenance, not active Git-object execution.
- **Alternate entrypoints:** `select_joined_world_view` validates caller-supplied J42/P41 receipts without executing them; generic `select_world_view` L230 is outside the N9/N10W progressive target and was not fully read.

## 5. What is supported / what proof edge is unexecuted

**Supported S1:**
- L01 adapter → R08 exact reader/prefix binding is implemented.
- `configure_progressive_world_context` enforces target/condition/prefix order, exact N10E/C1 extension support, source/release/risk/row/model identity.
- `progressive_world_view` emits a coherent test-only world view with N9 modeled routes, N10E exact steps, N10W positioned consumptions and `actor_state=NOT_TOUCHED`.
- `select_r05_world_view` executes the local P41 service from host-retained R05 inputs; test-only.
- `select_joined_world_view` validates caller-supplied J42/P41 receipts; it does not execute them.

**Unexecuted proof edge:** no external production entrypoint, no real selected C11/QSM release, no real source permission, no signed R08 execution at this cut. The only fixture is `L01_SYNTHETIC`/`L01_TEST_ROWS`; the world fields are modeled. Hence `CURRENT_FIRST_CONSUMER_PROVED` is not reached.

## 6. Five completeness grades

1. **Commission/identity:** 1/1 assigned R2 question addressed; prior R1 F6M/F6P, R7 and EV020 correction preserved by reference; 0 new canonical T.
2. **Historical discovery:** not a new historical T tract; current world chain inspected at one protected cut. Historical T universe remains open.
3. **Matrix coverage:** declared 12 finite cells; inspected 11; found 9; bounded NOT_FOUND 2; NOT_INSPECTED 1 (generic `select_world_view` outside the N9/N10W progressive path). See `COVERAGE.tsv`.
4. **Mechanism/consumer reconciliation:** 9 mechanisms traced; 0 non-test current first readers; 1 test-only world path; 1 test-only R05 path; 1 receipt validator.
5. **Evidence/closure:** all S1 static; 0 S2/native; reviewer OUTSTANDING. `ACCOUNTING_COMPLETE_AT_DECLARED_STRATUM`, not functional conservation.

**Terminal:** `ZAK04_R2_PROTECTED_WORLD_CHAIN_LOCATED__R08_EXACT_READER_AND_MODELED_E04_WORLD_TEST_ONLY__NO_EXTERNAL_NON_TEST_CALLER__NO_F6_NUMERIC_ENTRY__F6_WORLD_ADAPTER_NOT_PROVED`.

## 7. Residuals

- Generic `select_world_view` not fully read; outside the N9/N10W progressive target.
- No independent review; no actual selected source/QSM/version run.
- F6 numeric entry absent at this chain; an owner-issued adapter or alternate producer remains open.
- Do not expand to SOROK whole machine, original35, or new world design.
