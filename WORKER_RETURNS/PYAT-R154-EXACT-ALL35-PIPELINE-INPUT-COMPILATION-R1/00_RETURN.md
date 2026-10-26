# R154 — exact all35 pipeline-input compilation

**Status:** `ALL35_METADATA_COMPILED__NATIVE_INPUTS_PARTIAL__CURRENT_EXECUTION_BLOCKED`
**Scope:** metadata-only acquisition, no response rows/export, no source grant. Continues the same R154 job and preserves prior physical receipts.

## Delivered

- Canonical SQLite store: `store/r154_all35.sqlite`
  - 35 sources, 18,413 physical columns, 18,276 codebook rows,
    4,493 B49/typed-preparation evidence records, 35 native input packages.
  - normalized tables: sources, physical_columns, codebook_rows,
    reconciliation, evidence, requirements, source_requirements, tasks,
    native_packages, meta.
- Per-source JSON exports: `exports/SRC01.json` … `SRC35.json`, plus compact
  `SUMMARY.json` and `TASKS.json`.
- Actual native loader: `runtime/r154_load.py`.
  - Cold-loads all 35 sources.
  - Constructs actual `NativeSourceIdentity`, `OriginalWaveIdentity`, and
    `SelectedSourceRulePackage` objects per source.
  - Refuses `build_native_workload` until exact current source-read grant and
    scientific issuance arrive.
- Exact requirement schema: `REQUIREMENTS.md` and store `requirements` table.
  It binds actual owners/types/fields/stages through I03, I05, M1, M2,
  persistence and FieldForge, with conditional requirements kept conditional.
- Per-source reconciliation: `RECONCILIATION.md`, store `reconciliation` and
  exports, with physical-only/codebook-only lists. No column or codebook row is
  silently dropped.
- Exact HQ dependency requests: `HQ_ACQUISITION_AND_DECISION_REQUESTS.json`.

## Acquisition result

- 33 staged physical header receipts plus exact metadata-only Latin-1
  compatibility retries for SRC13/SRC14; all 35 current file hashes, formats,
  columns/types/labels/missing/MR/value-label metadata and row/column counts
  are represented.
- User-authorized metadata inspection only: no respondent rows decoded or
  exported; byte hashes are identity only.
- 35/35 current codebooks consumed (18,276 rows).
- 4,493 B49/typed preparation records consumed; 38 typed surfaces accounted;
  3,804 context records and 26 unmatched relation identities preserved.
- Physical/codebook reconciliation exposes 538 physical-only and 401
  codebook-only columns in aggregate; exact lists are in the store/exports.

## Task ledger

The store contains 213 task rows with **0 RUNNING**:

| State | Count |
|---|---:|
| DONE | 108 |
| DONE_WITH_EXACT_UNRESOLVED_FIELDS | 35 |
| BLOCKED | 70 |

BOOTSTRAP, all PHYSICAL/CODEBOOK/EVIDENCE/OCCURRENCES work, ASSEMBLE and
VERIFY_DELIVER are recorded. The 70 blocked rows are exactly 35
WORKLOAD + 35 PACKAGE tasks, each carrying the precise dependent missing
authority/field. They are not counted as done.

## Actually grounded vs blocked

Grounded: current physical identity/headers/types/labels/missing/MR metadata;
codebook rows and exact joins; B49/typed evidence; 35 native source identities,
wave identities and selected B49 packages; store cold load and exports.

Blocked: current source-read grant/resolver; remaining per-item unit/form/
topology/administration/role semantics where exact evidence is absent; complete
native occurrence/source inventory; scientific frontier/U/Epre; NativeWorkload
issuance; I03/I05 empirical execution; M1/M2 learned products; persistence/
retrieval of executed products; FieldForge receiving use. Exact WVS7 form/unit/
administration and source read grants are in the HQ request file.

## Commands

```sh
# rebuild store and exports
PYTHONPATH=. /usr/local/bin/python3 WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/runtime/r154_compile.py

# focused checks
PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/tests/test_r154_store.py \
  -q -o addopts='' --basetemp=.r61/r154-test

# cold load / status
PYTHONPATH=. /usr/local/bin/python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, str(Path("WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/runtime").resolve()))
from r154_load import load_all, build_native_workload
print(len(load_all()))
try:
    build_native_workload("SRC01")
except Exception as e:
    print("expected constraint:", e)
PY
```

Actual source execution requires exact current source-read grant/edition plus
scientific issuance; this return stops at that existing boundary. No empirical,
learned, FF, source-grant or full-U/Epre claim is made.

## Verification

- Focused checks: 5 passed (`checks/focused.log`).
- Verified: 35 source store rows, 18,413 physical columns, 18,276 codebook rows,
  4,493 evidence rows, 35 native packages, cold reload/refusal, no decoder call.
- Physical metadata 35/35 with SRC13/SRC14 Latin-1 metadata-only retries.
- No respondent rows decoded/exported; no source response execution.

Full35/1890/F1–F8/global/LongMemory/C5 and all R09/CI/prod/N11/N12/Sorok/
J52/W52/actor holds remain. Native core read-only at `44e7ace44d9e1b023a15d14ee1ead9b176d0e522`.
