# L2 negatives, unavailable authority and non-issuance court

**Status:** `L2_PARTIAL_CODE_AND_REPO_ASSET_PROOF__ORIGINAL_AUTHORITY_AND_NEO_SUCCESSION_HOLD`. This is a bounded V551/V552 return for parent [#716](https://github.com/maidiu/rawlsing/issues/716), not a scientific, original-data, or integration approval.

## Negative classes tied to exact code

| Class | Historical evidence | Type / consequence |
|---|---|---|
| Missing bridge or wrong run/scope | `compile_v551_relation_evidence_atoms.py:265-285,176-182` | CLI mandatory `--run-id`, `--bridge-path`; missing/unreadable raises; mismatched run/source/wave/shard raises `BLOCKED_V551_*`. CSV or Parquet input, no original-data read at V551. |
| Missing/unpinned scale registry | `ddm_v551_atoms.py:73-87` | `BLOCKED_MISSING_V551_SCALE_AUTHORITY`, schema/hash/duplicate-key/uncertified failures. Frozen actual CSV digest `d270f59d…e2a00fc8`, 145 keys. |
| Unknown exact response contract key | `ddm_v551_atoms.py:141-150` | `NONPROMOTABLE_REPAIRABLE:missing_exact_response_semantics_contract_authority`; no signed atom. The caller's hash is not minted by V551. |
| Direction or geometry unavailable | `ddm_v551_atoms.py:89-113,128-150` | Missing certified direction/intensity, invalid pivot/endpoints, negative directional magnitude, out-of-bounds coordinate or unsupported semantics gives a reasoned nonpromotable candidate, not inferred sign. |
| Semantic/structural/use missing | `ddm_v551_atoms.py:128-135` | Non-`RELATION_EVIDENCE`, noncertified semantic/response/direction, incomplete structural mapping, unmatched map, review flags or use denial prevents promotion. |
| Missing directionality stamp | `ddm_v551_directionality_expectation.py:38-49` | `MISSING_OR_INCOMPLETE_STAMP` audit count/reasons. Only a summary enters V551 manifest (`:242`), not the row-level audit; cannot claim a persisted stamp audit. |
| Incomplete distribution | `ddm_v551_atoms.py:160-166` and `ddm_v552_structural.py:159-174` | Repair debt `PARTIAL_WITH_REPAIR_DEBT` or `NO_PROMOTABLE`; V552 denies pressure for affected distribution rather than silently renormalizing unresolved mass. A run can still contain other promotable distributions. |
| Missing/tampered V551 bundle | `compile_v552_structural_ddm.py:165-238` | Manifest identity, v3, three Parquet declarations, hashes, row counts, frame scope and conservation checked; numerous `BLOCKED_V552_V551_*`. File consistency does **not** verify historic original source or manual authority issuance. |
| Unsupported conditional claim | `ddm_v551_conditional.py:18`, `compile_v552_structural_ddm.py:299-309`, `ddm_v552_structural.py:253-259` | At frozen code `ImportError` for `MIN_ATOM_SUPPORT` and `SOURCE_TABLE_PRIORITY`. V552 accepts optional conditional Parquet into a local variable but its output function never reads that variable; `conditional_determinicity_status_audit` is empty. **HOLD** any claimed conditional structural effect. |
| Weight authority missing | `ddm_v552_structural.py:137-146` | Chooses weighted percentage, unweighted percentage or count by local completeness/status heuristic. This is a computed fallback, **not** positive complex-survey weight-law acceptance. Weight-sensitive use must remain separately qualified. |
| Valid zero vs absence | `ddm_v552_structural.py:159-184` | Observed numerical zero is `OBSERVED_ZERO`, noncomputable `APPLICABLE_BUT_UNRESOLVED` with `DENY`, no promotable categories `NO_APPLICABLE_EVIDENCE`; do not conflate. |
| No direct V553 or actor grant | `ddm_v552_structural.py:220-241,253-259` | Temporal/source keys are V552J candidates only; `direct_v553_authorization=False`, `allowed_for_v553_temporal_field=False`, no runtime or actor permission. |
| Diagnostic privilege | `compile_v552_structural_ddm.py:401-429`, `ddm_v552_structural.py:242-251` | `--strict-handoff` is default true; `--no-strict-handoff` and `--diagnostic-only` prohibit downstream `ALLOW`. This controls invocation permission, not source scientific acceptance. |
| Stale in-process authority cache | `ddm_v551_atoms.py:36,73-87` | `_registry_cache` returns loaded rows without rechecking current files. Sourcefree pinned mutation on same process returns stale rule; fresh loader sees changed rule. Test in `05`. |
| Review-status gap | `ddm_v551_atoms.py:82-87` versus `ddm_v550_response_semantics_authority.py:161-169` | V551 requires a `review_status` **column**, but does not require `NO_REVIEW`. A synthetic REVIEW_REQUIRED row with appropriately changed manifest SHA loaded, whereas V550 producer's key-set loader explicitly rejects it. This is a code asymmetry, not evidence any real frozen row is uncertified. |
| Declared producer lineage only | `ddm_v551_atoms.py:137-155`; `compile_v552_structural_ddm.py:182-238` | V551 records QUC row/artifact hashes and the bridge SHA, V552 verifies V551 output bundles, but V552 neither reopens V550 bridge nor verifies historic source authority bytes. Content hashes of computed labels do not reissue manual decisions. |

## Exact unavailable assets and custodians

At protected historical tree `9ba4764bef551b1ce498e5772d60b73d69337d4b`, the tracked `data/ddm_build_copy/authority/` tree contains six entries, including four tracked files fetched and SHA-checked for this return. The scale-registry manifest **refers to 13 distinct files not found in the inspected tracked `data/ddm_build_copy` tree**:

- Nine `data/ddm_build_copy/reports/{afrobarometer,arab_barometer,asian_barometer,evs,gss,latinobarometro,lits,south_asia,wvs}_response_option_authority.csv`, individual claimed SHA-256 in `03_ASSET_REF_AND_FIRST_CONSUMER.csv`.
- `data/ddm_build_copy/authority/active_35wave_question_universe_v1.csv` (`6a5c325cdd48…` claimed).
- `data/ddm_build_copy/reports/35wave_active_response_semantics_contract_inventory.csv` (`0c8f14ba…` claimed).
- `data/ddm_build_copy/reports/35wave_response_scale_encoding_ruling_ledger.csv` (`c5064851…` claimed).
- `data/ddm_build_copy/reports/35wave_active_response_semantics_contract_validation.csv` (`96e56c65…` claimed).

These are **manifest references**, not independently read/recomputed original authority SHA proof. L5 owns exact estate reconciliation with the local file inventory/A02/P10; L1 owns original V550 issuer and semantic selection. The manifest declares 700 selected-question rows, 906 active authority rows, 145 certified distinct scales, 236 compact active bindings and 0 review-required registry rows. The 145/236 counts were independently confirmed on the two tracked CSVs; the 700/906 inputs were not fetched or recomputed.

No original respondent files, V550 bridge run Parquet, V551 three run Parquets/manifest, V552 runtime outputs, local original manual ruling files, or original accepted-law signatures were supplied to this runner. Exact physical SHA, run-level cache, native empirical mutation and all35 first-consumer verdict remain **S2_NATIVE_NOT_RUN**. Do not create synthetic equivalents for those assets.

## Competing authority / version/permission selection

- V551 scale paths are module-relative constants at `ddm_v551_atoms.py:26-28`. No CLI or environment override exists at that entrypoint; `--bridge-path` and `--output-root` are dynamic selections. A process-level global cached registry can outlive a changed disk manifest.
- V550 producer's response hash is selected at family/wave/var using the 236-row compact authority binding, not by recomputing from the V551 signed geometry (`ddm_v550_response_semantics_authority.py:203-260`). Original manual packet legitimacy is a separate L1/L5 question.
- V551's `_producer_lineage` considers a nonblank row+artifact hash `PRODUCER_ROW_AND_ARTIFACT_DECLARED` but does not cryptographically reopen the QUC file (`ddm_v551_atoms.py:137-139`).
- V552 treats `strict_handoff` as invocation permission; it does not create weight, structural mapping, response-meaning, or actor authority.
- `ddm_v552_contract.py` defines alternate earlier-version pure transformations. It is **not** imported by the scanned live v3 compiler/validator. Its caller coverage outside this graph is unresolved, not silently retired.

## Unvisited / unbound counts

- Core L2 designated executable/transitive/adjacent modules: **13 of 13 Python files inspected**. This includes two adjacent non-imported modules (`ddm_v552_contract.py` and `ddm_pipeline_boundary_consumer.py`); they were not silently called live entrypoint dependencies. A dynamically selected file read is not an enumerated runtime asset.
- L1 upstream sample: six files, **not** all of L1's dynamic source provider graph. L4 downstream sample: three files, **not** full joint court. L6 current sample: eight files, **not** a global neo-pre553 code census. Total unique scanned inventory: **34** (including four tracked authority files).
- **65 syntactic I/O-related call expressions** enumerated in `evidence/STATIC_IO_CALLSITES.csv` (48 L2 core and 17 sampled L4 downstream). These include writes, hash/read helpers and duplicate branches, so they are not 65 original authority calls. **41 semantically classified rows** appear in `02_LEGACY_CALLSITES.csv`; it includes meaningful transformations/guards without direct disk I/O. No uncovered static I/O sites among the 13 defined core modules; unresolved dynamic file *instances* and external stage callers are **UNKNOWN**, not zero.
- Future exact owner: L1 for original V550 and response/QCU; L5 for 13 referenced original assets and A02/P10; L4 for complete V552J readers; L6 for complete neo-PRE553 first consumers; L7 for independent acceptance. Protected merging remains CAS/HQ only.
