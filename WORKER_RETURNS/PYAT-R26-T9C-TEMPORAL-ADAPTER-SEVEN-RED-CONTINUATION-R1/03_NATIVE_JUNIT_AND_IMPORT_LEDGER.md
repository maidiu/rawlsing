# 03 — native JUnit and import ledger (PYAT R26 T9C)

Role: **original T9B temporal adapter author continuation**. Not independent T9I
reviewer, not HQ, not an EE12 issuer. Writes confined to
`WORKER_RETURNS/PYAT-R26-T9C-TEMPORAL-ADAPTER-SEVEN-RED-CONTINUATION-R1/`.

---

## 1. Four separate courts

These are separate courts. They are **not** aggregated into a single acceptance
percentage.

| Court | Cases | Passed | Failed | Errors | Skipped | Exit | JUnit sha256 |
|---|---:|---:|---:|---:|---:|---:|---|
| 1. Frozen independent T9I suite (byte-identical transport) | 48 | 47 | 1 | 0 | 0 | 1 | `add067428c0dd9843a21a0c2e6a2d034dca428a8bde31c4f23eef0674adda9b6` |
| 2. Own T9C repair suite | 52 | 52 | 0 | 0 | 0 | 0 | `a0ade6b4d4b16c56df245873c1f3c09c28871eae84874e6c82981de1a7b6e6de` |
| 3. Inherited original V553 consumer-contract suite (unchanged) | 8 | 8 | 0 | 0 | 0 | 0 | `a823af531c4c7a51204f3159d5c7c5c50ac9beea4dfc4cc21d5c46efdc320007` |
| 4. Unchanged original T9B author suite | 28 | 28 | 0 | 0 | 0 | 0 | `26d7af91b702379038f66975898ce129cf91432de9f9363bc8a3c7113bf1c90d` |

Runner: `python3 -B run_all.py`. Complete stdout/stderr for every court is in
`logs/<court>.log`. Machine-readable assembly is
`evidence/t9c_four_court_execution.json`.

**The single failure in court 1 is `test_two_time_original_consumer_and_numerical_products_reproduced`**
and it is the disclosed, deliberate consequence of repairing defect R5. See §4.

---

## 2. Preserved inventories

| Inventory | Required | Observed | Status |
|---|---:|---:|---|
| Original T9B author positives | 28 | 28 | preserved, unmodified source, in place |
| Inherited original V553 native tests | 8 | 8 | preserved, unmodified source |
| Independent T9I test cases | 48 | 48 | reproduced from byte-identical transport |
| Independent T9I RED assertions at the court | 10 | 10 | reproduced (38/10) and then repaired 10/10 |
| Commission-mandated arithmetic | — | matched | see `01_SEVEN_DEFECT_CONTRACTS.json` |

### The original independent split is reproduced exactly

The frozen transport, run against the **original T9B adapter**, is used to generate
the counterexamples in `02_ACTUAL_ORIGINAL_V553_AND_CONSUMER.json`. Those
counterexamples independently tally **10 failed assertions** across the seven
classes, with the same per-class distribution the independent court recorded
(R1:1, R2:3, R3:1, R4:1, R5:1, R6:2, R7:1). The per-case crosswalk against the
independent court's own `junit/independent.xml` is
`evidence/03_T9I_RED_TO_GREEN_CROSSWALK.json`:

```
T9I independent court : 38 pass  10 fail
T9C repaired adapter  : 47 pass   1 fail
red -> green          : 10
newly red             :  1   (test_two_time_original_consumer_and_numerical_products_reproduced)
```

---

## 3. Native import ledger

`evidence/t9c_native_import_ledger.json` lists every staged native file with its
git blob SHA-1 in this return, the canonical repository blob at the sealed startup
commit `79cf24ee615ec24bee2dc8584b31fb6b240fd3cf`, and the byte-identity check.

| Property | Value |
|---|---|
| Staged Python sources | **22** |
| Staged bytes | 584,404 |
| Byte-identical to repo at `79cf24ee` | **22 / 22** |
| Original T9B copied files | 1,259 (12,332,400 bytes) |
| Unrelated Python excluded from runnable closure | 317 |
| JSON excluded from runnable closure | 920 |

The commission asked for **minimal pinned native 22-source imports instead of 1,259
copied unneeded files where possible**. That is what is staged. The original T9B
return's 1,259-file tree is left exactly as published and is used only as the
in-place substrate for the unchanged author suite (court 4).

The critical native module is byte-identical in both trees, which is what makes
loading one cached native module while exercising both adapters legitimate:

```
native_module.byte_identical = True
staged_git_blob_sha1 == repo_blob_at_79cf24ee
```

---

## 4. Module receipts and ambient-shadowing control

`guarded_runner.py` pins `sys.path`, disables plugin autoload, and checks every
project module against its expected git blob preimage before any of its code runs.

`evidence/t9c_frozen_t9i_module_receipts.json` records 16 named loaded project
modules in the frozen court:

* 16 / 16 resolve **inside this return**
* 0 ambient leaks
* `t9b_temporal` resolves to this return's corrected module
* `data.ddm_build_copy.ddm_v553_temporal_pressure` resolves to this return's staged
  byte-verified copy

Guard negative controls (`test_independent_guard_rejects_untrusted_path_and_changed_preimage`)
are green: an untrusted path is rejected as `UNPINNED_PROJECT_MODULE`, a registered
module with changed bytes is rejected as `PREIMAGE_MISMATCH`, and no sealed source
is mutated.

The bare relative documented pytest command that T9I stopped before unverified code
execution (exit 4) is **not** used here. Every court passes `--rootdir` and `-c`
explicitly, so the ambient `pytest.ini` and ambient `data/ddm_build_copy/` cannot
shadow the pinned tree.

---

## 5. The one residual failure in court 1

`test_two_time_original_consumer_and_numerical_products_reproduced` compares the
repaired consumer output against the **original T9B published two-time artifact**
at `pinned_candidate/evidence/02_real_temporal_to_selected_world_two_times.json`.

Repairing R5 requires that a `PROBE_ONLY` read stop presenting a route as a
permission-valid open opportunity. The published artifact records
`opportunity_ids = ["ROUTE_DEFERRED_REVIEW"]` for the 1990 `PROBE_ONLY` read. Those
two facts cannot both hold. The repair takes precedence, and the deviation is
disclosed here rather than hidden.

Field-level diff (from `02_ACTUAL_ORIGINAL_V553_AND_CONSUMER.json` and the run above):

| Field | Stored T9B | Repaired T9C | Defect class |
|---|---|---|---|
| `1990.opportunity_ids` | `["ROUTE_DEFERRED_REVIEW"]` | `["ROUTE_BLOCKED_NO_SUPPORT"]` | **R5** |
| `1990.exploratory_route_ids` | *(absent)* | `["ROUTE_DEFERRED_REVIEW"]` | R5 disclosure |
| `1990.authorized_opportunity` | *(absent)* | `false` | R5 disclosure |
| `2000.*` semantic fields | unchanged | unchanged | — |

Every **semantic** field that the independent court actually endorsed is unchanged:
numerical values 0.20 / 0.60, pressure bands, `basis_wave_ids`, `uncertainty`,
`temporal_key`, `refused_code`, and the whole `provenance` block
(`source_family`, `edition`, `grain`, `world_id`, `institution`, `access_grants`,
`clock_question`, `publication_lag_wave_ids`, `t8f3_assignment_preserved`).

All other differences are **purely additive disclosure fields** introduced by the
repairs and are listed in full in `02_ACTUAL_ORIGINAL_V553_AND_CONSUMER.json`:

* `structural_world_fields` (R4) — complete structural/access world identity
* `source_families` / `editions` (R3) — basis-bound source custody
* `archive_context_wave_ids` (R7) — separate archive-context lineage
* `native_multi_wave_authorization_status` / `..._reason` (R1) — the native verdict
* `authorized_opportunity` / `exploratory_route_ids` (R5)
* `not_observed` / `rupture_qualified` (R1 / R6)

No arithmetic changed. The accepted original V553 machinery is untouched.
