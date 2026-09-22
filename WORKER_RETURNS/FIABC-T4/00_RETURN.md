# FIABC-T4 — Live Telemetry / Lifecycle / Preserved-Work Transposition

Branch: `agent/rabochii-premain-fiabc-t4-accounting-lifecycle-transposition-r1`

Required parent: `agent/vozhd-premain-fiabc-live-transposition-t3-fanin-r1`

Exact parent tip used: `58019599e8dc2ae1c8d21ea02806c87e73c576e3`

Implementation tip before this return packet: `d48cebeb3b8acff92cf0dbbe06e00255750d4fb4`

## Disposition

**IMPLEMENTATION COMPLETE — SOURCE-INDEPENDENT QUALIFICATION NOT EXECUTED ON THIS BROWSER-ONLY WORKER SURFACE.**

No measured P2X was executed. No source carriers were opened by this worker. No merge was performed.

T1 → T2 → T3 remains the governing live ancestry.

## What was transposed

The accepted Wave-3 accounting components were added without semantic rewriting:

- `rawlsing_next/fiabc_telemetry_semantics.py`
  - Git blob: `d061cd0f3c595c100ea728520fb0892404a2ca9b`
  - accepted I06B implementation copied byte-for-byte;
- `rawlsing_next/fiabc_lifecycle_accounting.py`
  - Git blob: `a2977ea22fe67858a2a811917bd7ac0f4b7350c7`
  - accepted I06C implementation copied byte-for-byte.

The live T3 seam is:

- `rawlsing_next/fiabc_live_accounting_binding.py`
  - Git blob at implementation tip: `3ca3a1ce90f18fbcb2d7b5c7e3a25d41dd4b0c4e`;
- `rawlsing_next/ee_p2x_darwin_court_driver.py`
  - Git blob: `9d9492f96d849a3f2e67e187507d443ed593aa72`;
- `rawlsing_next/ee_p2x_darwin_stage_backend.py`
  - Git blob: `f32fc0441efd649bcb7196a91354cc7311bc384b`.

## Live execution order preserved

T4 does not move or reinterpret the T3 gates. The live ordering remains:

`SOURCE IDENTITY FREEZE`
→ `AUTHORITY/WORKLOAD FREEZE`
→ `INDEPENDENT ORACLE MATERIALIZE/FREEZE`
→ `FRESH CANDIDATE PROCESS`
→ `C11`
→ `I03`
→ `I05`
→ `LIFECYCLE`
→ `TERMINAL`.

The T4 bridge consumes the T3 process envelope only after a backend stage has executed. Lifecycle-scoped telemetry is admitted only after the corresponding I06C action observation validates.

## Telemetry law now live

The live accounting path now binds:

- immutable/write-once canonical metric slots;
- exact source SHA / candidate / phase / process / lifecycle provenance;
- candidate-total CPU from non-overlapping process-self deltas;
- replay/recovery child processes as separate child envelopes charged exactly once;
- per-phase parent-process CPU retained separately and never summed into candidate CPU a second time;
- candidate-local RSS and candidate peak RSS by **max**, never sum;
- candidate-neutral C0 freeze/oracle production excluded from candidate numeric cost;
- C1 source access recorded as candidate-local input access;
- typed null for uncaptured/unreached telemetry, never synthetic zero;
- observed I/O events without promoting endpoint directory size to I/O;
- accepted scratch high-water semantics without promoting endpoint snapshots to peaks;
- separate cold/warm metric fields;
- telemetry receipts that explicitly state semantic disposition was not modified.

The live finalizer deliberately leaves I/O and scratch peak fields typed null until complete event-level coverage exists. It does **not** backfill those fields from endpoint size.

## Lifecycle law now live

The old surrogate lifecycle bodies were removed as accounting authority.

Current live handlers now perform or bind:

- cold first realization, bound to the exact T3 absent-state observation;
- warm retained-state use, bound to the candidate-owned retained session;
- deletion/regeneration using actual session deletion and regeneration lineage;
- source invalidation using actual invalidation + recomputation;
- authority/semantic invalidation using actual invalidation + recomputation;
- stale-state exercise using a governed candidate-state determinant, detection, and recovery;
- corrupt-state exercise using actual corruption, detection, and recovery;
- interruption recovery by interrupting a governed replay process and executing recovery;
- fresh-process replay through a new Python process executing C11/I03/I05 and reproducing the governed terminal identity;
- audit/revalidation from an actually executed audit primitive.

Formula-derived rebuild counts, law hashes, generic temp files, and declarative-only actions do not satisfy I06C.

## Child-process accounting closure

T3's candidate process uses process-self counters. T4 therefore records each replay/recovery subprocess as an explicit child process envelope. I06B sums the main candidate process and each child process-self CPU delta exactly once, while peak RSS is the maximum across candidate-local process envelopes.

## Preserved work

LiTS-A historical first-build telemetry is not automatically promoted.

At the current live seam it remains:

`PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY`

unless and until exact field-by-field compatibility is proved for workload, runtime binding, state binding, isolation, operation, and metric definition. Numeric credit can then occur only through the accepted I06C conditional preserved-work path.

LiTS-B's accepted cacheless C11 receipt remains semantic-only with no invented numeric telemetry.

Pre-P2 calibration remains calibration-only.

Historical stops do not manufacture ordinary unreached numeric metric rows.

## Derivative parentage gate

A preserved/prebuilt R5 derivative is no longer accepted merely because its embedded `source_artifact_ref` names the canonical LiTS source SHA.

LiTS-A R5 consumption now additionally requires:

`RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT`

with schema:

`FIABC_T4_DERIVATIVE_PARENTAGE@1.0.0`

binding the exact consumed derivative identity to:

- governed producer identity;
- governed operation identity;
- governed config identity;
- canonical source SHA;
- exact evidence refs.

Path presence is not parentage. Derivative identity is not parentage. Missing or drifting parentage fails closed as source authority.

## T1–T3 invariants left intact

T4 does not alter:

- T1 packaging paths/hashes;
- T2 six-cell manifest;
- Candidate-C exact-source fallback law;
- WVS-C zero-accelerator law;
- T3 independent oracle freeze;
- T3 generic source-freeze schema;
- T3 fresh source×candidate process isolation;
- historical stopped evidence.

No PRE-MAIN shared file was copied wholesale over a live T1–T3 file.

## Qualification boundary

The focused source-independent tests are committed and exact commands are recorded in `05_TEST_COMMANDS.md`.

No GitHub Actions workflow fired for this branch, and this browser-only worker surface does not expose a repository execution shell. Therefore no test PASS is claimed here.

No measured P2X was run.

Terminal:

`FIABC_T4_LIVE_TELEMETRY_LIFECYCLE_ACCOUNTING_TRANSPOSED__READY_FOR_PREFLIGHT_TERMINAL_LAYER`
