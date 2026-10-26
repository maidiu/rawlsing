# R147 — all35 current metadata + historical-label reconciliation

**Status:** `ALL35_CURRENT_METADATA_ADAPTED__HISTORICAL_LABELS_RECONCILED__CURRENT_SOURCE_ISSUANCE_PENDING`
**Base:** `e62b2447f04241d78b360f9381f0bb44c0a14159` (R146/R145 binder retained)
**Scope:** current codebook/metadata documents only. No survey file was opened, stat'ed, hashed or decoded; no current source/science/access grant.

## Result

The executable `runtime/current_metadata_reuse.py` consumes:

- **26** newly staged current codebooks from `.r61/r147-all35-current-metadata/inputs` with exact SHA/bytes pins;
- **3** prior R145 metadata bindings (SRC22, SRC23, SRC30) by exact git object;
- R146 all35 existing-binding records and CLOSED35/U53A/U43 source cards;
- exact completed L2/L2R treatment packets for affected sources.

It emits one `records/SRCxx_CURRENT_METADATA_PREPARATION.json` per source, full
row-evidence JSONL for the 26 staged codebooks under
`records/ROW_ACCOUNTING/`, plus `SUMMARY.json`, `STATE_MATRIX.json`,
`CURRENT_METADATA_AVAILABLE.json`, `MISSING_METADATA_DOCUMENTS.json` and
`ALL35_CURRENT_INDEX.jsonl`.

- Current metadata available: **29/35** sources; total current rows: **15695**.
- Missing current metadata: **6** sources — SRC04, SRC05, SRC06, SRC07, SRC11,
  SRC13. Their exact needed source/family/wave documents are named in
  `records/MISSING_METADATA_DOCUMENTS.json`; no historical null path is called
  evidence of absence.
- Full35 denominator: **35**; excluded from denominator: **0**. SRC35's
  historical Authority72 exclusion is preserved as provenance only and is not
  an automatic current exclusion.
- No scientific role is invented. Current staged rows retain full question/option/
  field evidence with `scientific_role=UNASSIGNED_PENDING_EXACT_SEMANTIC_AUTHORITY`;
  R146 role/routing/design/topology/index bindings are carried unchanged.

## Historical-label reconciliation

Historical labels remain provenance; none is an automatic current denial.

- **L2 residual (3):** SRC02, SRC03, SRC24 — exact residual sets remain frozen
  current semantic gaps; completed closures are carried separately.
- **L2 closed (3):** SRC13, SRC16, SRC17 — documentary authority closed and ready
  for source-specific realization; current source access/U/Epre remain pending.
- **L2R EVS 2008 (1):** SRC14 — documentary realization authorized; current
  release hash remains an exact gap.
- **Historical blocked without an applicable L2/L2R closure (11):** SRC01, SRC04,
  SRC05, SRC06, SRC08, SRC11, SRC12, SRC21, SRC27, SRC31, SRC33 — the 15-count
  historical BLOCKED label is reduced to provenance for these; the current
  representation authority is not established, not inherited as a false denial.
- **Historical exclusion (1):** SRC35 — provenance only; included in full35
  denominator and current metadata preparation.

## Exact current contradictions

Current codebook row counts contradict U43 research-identity counts for:

| Source | Current codebook rows | U43 count | Disposition |
|---|---:|---:|---|
| SRC01 | 144 | 146 | exact source-specific reconciliation; neither side dropped |
| SRC24 | 203 | 206 | same |
| SRC26 | 195 | 199 | same |

## Current gaps retained

Across 35/35: current access permission, current edition SHA, complete native U,
scientific Epre, response-read grant/current resolver. Additional exact gaps:
3 L2 residual sets, 1 release hash, 6 missing metadata documents, 3 row-count
contradictions, and current representation authority for the 11 labels above.
No source read is authorized.

## Next calls

```sh
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R147-ALL35-CURRENT-METADATA-R1/runtime/render_current_source_preparation.py --source-id SRC23
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R147-ALL35-CURRENT-METADATA-R1/runtime/render_current_source_preparation.py --source-id SRC01
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R147-ALL35-CURRENT-METADATA-R1/runtime/render_current_source_preparation.py --source-id SRC35
```

For the six missing metadata sources, stage the exact current document named in
`MISSING_METADATA_DOCUMENTS.json`, then rerun the same command. Actual response
execution still requires the separate exact source-read grant and current
resolver; a metadata document never authorizes decode.

## Verification

- Focused checks: **6 passed** (`evidence/focused.log`).
- Verified: 35/35 source records, 26 staged + 3 prior docs, 15695 current rows,
  6 exact missing docs, historical-label reconciliation, SRC35 included, L2/
  L2R treatment refs, row contradictions, row hash/evidence retention, refusal
  on unknown source/hash tamper, no decoder/survey call.
- CLI probes: SRC01, SRC23, SRC35 under `evidence/`.
- Receipt: `evidence/PROOF_RECEIPT.json`.

## Limits

No actual source/respondent access, no empirical/learned/FF/V553 execution, no
current U/Epre or source permission, no all35 qualification, no 1890/F1–F8/global
claim. Representative real empirical + learned-to-FF milestone remains parallel.
Full35/1890/F1–F8/global/LongMemory/C5 and all R09/CI/prod/N11/N12/Sorok/J52/W52/
actor holds remain. Native core is read-only at `44e7ace44d9e1b023a15d14ee1ead9b176d0e522`.
