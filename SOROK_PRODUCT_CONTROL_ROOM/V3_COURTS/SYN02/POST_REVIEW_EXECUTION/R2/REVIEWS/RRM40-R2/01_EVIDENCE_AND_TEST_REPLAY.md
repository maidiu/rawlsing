# SYN02-RRM40-R2 / 01 — evidence and test replay

**Review:** independent hostile RRM40-R2 source and 480-cell court.
**Review branch:** `agent/sorok-syn02-review-rrm40-r2-literal-source-r1`.
**Sealed startup:** `a7a6c781e158cd1317c0ecd0d6e1e542a4fd633d`.
**Author target:** `a67f155ba06ebb33067769510e940012d71b3fa6`.
**Source:** `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging` (read-only).
**Evidence grades:** `EXECUTED` = own run; `SOURCE_INSPECTION` = exact source read; `INHERITED` = prior pinned evidence not rerun; `NOT_RUN` = not executed and not treated as a pass.

## 1. Immutable target identity

Target files read from `a67f...`; hashes independently computed:

| File | Bytes | SHA-256 |
|---|---:|---|
| `R2/RM40/00_RETURN.md` | 8,862 | `066f6d997f2d44291f5f2963f2c8d6085cf3ac9c872c85c61aee6cb818a4a045` |
| `R2/RM40/01_ALL40_LITERAL_SYMBOL_CALLSITE_PATCH_PLAN.md` | 80,838 | `6d96c83b472e2d9a97af21df16318e03701106a3c3da49195f26aea67a0b3ff0` |
| `R2/RM40/02_CORRECTED_SOURCE_GRADED_40X12.json` | 856,819 | `e332787287b92b6efdfdb63eafd2fc68a69327807be310162b6e97f02f2cce0e` |
| `R2/RM40/03_TEN_CELL_ADJUDICATION_AND_M17_CORRECTIONS.md` | 9,638 | `e4a47903bbb317cff7c4cd9b5d2001058952c567d0c5ecff067e6fed77ab0e4c` |
| `R2/RM40/04_F1_F2_F3_TESTABLE_MIGRATION_PATCHES.md` | 18,122 | `2625e7ca41ba08f0101a62779ed87cf6581675b5099aa3173855fd744995f25c` |
| `R2/RM40/05_VALIDATE_R2.py` | 5,059 | `cb9f9b5606764fc324daa785ee1e7cc1559d4ecc86c34414121dd7a2109ce0b2` |

The target 00 artifact-hash claims for 01–05 match these bytes. The 00 self-hash is intentionally not embedded by the author and was computed here only for readback.

The target is six files under `R2/RM40/`, not the prior RM40 target. No target or source file was edited.

## 2. Executed structural/source validator

Command:

```text
python3 /Users/matthewsmith/Desktop/Rawlsing_Worktrees/rrm40r2-evidence/target/05_VALIDATE_R2.py \
  --json /Users/matthewsmith/Desktop/Rawlsing_Worktrees/rrm40r2-evidence/target/02_CORRECTED_SOURCE_GRADED_40X12.json \
  --source-root /Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging
```

Exact output:

```text
PASS: 40 rows, 480 unique cells, 126/354 baseline, 124/356 final, 10 changed, 8 carrier, 2 unsupported
PASS: 59/59 source hashes, 31/31 S50 hashes, 40 unique consumers/test IDs, all exact symbols present
PASS: no fake M17 symbols; X remains scoped historical source, never permission
```

The validator is a useful structural/source identity check. It does **not** verify:

- source line numbers against definitions;
- per-symbol kind for mixed rows;
- that `T-M…` IDs are executable tests;
- that `TO_BUILD` consumers exist or have source authority;
- F1/F2/F3 implementation or C9/C12 behavior.

Those gaps are reviewed separately below.

## 3. Independent 480-cell replay

Own parser of S04/S05 at `321fa29bb3e51849a43cb7caf1600625bf215539`:

```text
S04: rows=40 cells=480 X=116 dash=364
S05: rows=40 cells=480 X=126 dash=354
S04/S05 mismatch: 10
M09/N01, M10/N01, M11/N01, M13/N01, M14/N02,
M18/N01, M19/N01, M24/N01, M36/N01, M39/N01
JSON: rows=40 cells=480 X=124 dash=356
JSON baseline_s05 X=126
baseline field mismatches vs S05: 0
final marks differing from S05: only M14/N02 and M39/N01, both X→dash
```

Relation counts in target JSON:

```text
NONE=354
DIRECT_CONDITIONAL=116
INDIRECT_CARRIER_ONLY=8
UNSUPPORTED=2
```

The ten changed cells are exactly the ten named; eight retain X and two remove X. `M36/N01` is carrier-only and is not N01 need/object formation. `M14/N02` and `M39/N01` are unsupported and removed.

## 4. Independent source identity

Own rehash against the mounted source:

```text
unique source_registry paths: 59
59/59 SHA-256 and byte lengths exact
s50_selected_files: 31
31/31 SHA-256 and byte lengths exact
no missing path, no changed hash
```

The source root has exact file identity. The staging archive is not adopted as TD-R05; the target correctly uses file identity. Source hashes prove file identity, not semantic validity or current import.

## 5. Source line audit

A separate Python line audit parsed every `source_location` entry:

```text
file:line references: 139
unique source files referenced by locations: 56
out-of-range references: 0
unparsed/prose entries: 3
  M30: v3/V3_UNDERLIES_V2_ARTICULATION.md (prose; no callable line)
  M31: v2/ENNEAGRAM_EMERGENCE_SYSTEM.md (prose; no callable line)
  M31: v2/PROBABILISTIC_ENNEAGRAM_SYSTEM.md (prose; no callable line)
```

The line contents match the named classes/functions/config/test/call sites for the audited rows, including:

- M01 `class BackboneState` and `hash_jsonable`;
- M17 `apply_gift_disruption_shards_from_events` at `expectation_events.py:103` and call at `delta_templates.py:361-362`;
- M19 `update_metabolization_and_plasticity_step` at `:521` and its `state.rendered_output` read;
- M25 YAML `core_steps` 19 / appended `active_magnets_update` 20;
- M26 `compute_all_derived` at `derived.py:322` writing `metabolic_style`/`registers`;
- M29 `render_year` at `phenomenology.py:55`;
- M37 server callsite/persona/distillation lines;
- M39 function/alias/call-site lines.

Exceptions/limits:

- M06 line 318 is a write site inside `apply_deltas_to_state`, not a new definition; the row’s `symbols` list correctly names the function.
- M30/M31 prose artifacts have no callable line by design; their callable functions are listed separately.
- `M37` line audit cannot cover the uncited `v3/run_and_print.py` path (see §6).

## 6. M17 correction replay

Own source grep:

```text
v3/engine/expectation_events.py:103  def apply_gift_disruption_shards_from_events(
v3/engine/effects/delta_templates.py:361  from v3.engine.expectation_events import apply_gift_disruption_shards_from_events
v3/engine/effects/delta_templates.py:362  apply_gift_disruption_shards_from_events(state, events)
```

No `def create_gift_shard_from_event` or `def create_disruption_shard_from_event` exists. The target’s M17 correction is source-true. It remains a source-level repair: `ImpressionRecord` is future (`TO_BUILD`), not a current import.

## 7. M37 second render path gap

Actual source:

```text
v3/run_and_print.py
SHA-256 f2c1bbcbbdd39dda37e1334e035383535a8c04bfa6feb2d8253687576805eb60
bytes 9441
line 152: render_year(state, derived, config)
```

The target M37 `source_location` and `source_files` do not contain `v3/run_and_print.py`; the target source registry has 59 files and excludes it. Target `01` says M37 has a final render/overwrite path; target `04` also refers to the final path. That claim is **not fully source-identified**. Required repair: add the file/hash/line and update the registry count, or remove the “two routes/final path” claim and scope M37 to the server/persona/distillation path.

This is the only source-row gap of this kind found. It does not alter the 480 marks or M17 correction.

## 8. Target JSON content checks

Own checks:

```text
rows: 40 unique M01..M40
cells: 480 unique (M,N)
dispositions: 31 ADAPT; 3 REPLACE (M31/M33/M39);
              3 REMOVE (M34/M35/M36)
              REUSE: M26/M30 invariant, M29 immediate body
changed_cells: 10 exact adjudications
source_registry: 59 unique paths
s50_selected_files: 31
first_future_consumer strings: 40 unique
first_future_consumer grades: 39 TO_BUILD, 1 RULE_HELD
test_id strings: 40 unique
current_consumer_status: 280 RULE_HELD, 40 each TEST_ONLY/
  SOURCE_HELD/MEMORY_HELD/BATCH_HELD/NATIVE_HELD
```

These are string/structural counts, not proof of 40 source-grounded consumers or executable tests. Several future consumer labels are compound or non-actor-specific (`all read-only C9 views`, `ANALYST-only`, `C9.event_sequence / C12 batch`, `C9.configuration_read / SYN02-C`, `C9.support_load_read / world interval`). They must remain `FUTURE_CONSUMER_LABEL`, not current evidence.

## 9. F1/F2/F3 test replay

No F1/F2/F3 implementation or fixture exists in target. `04` is a specification. The target 00 explicitly says:

- sourcefree behavioral tests in `04`: **NOT_RUN**;
- real model/product calls: **NOT_RUN**;
- full repository suite: **NOT_RUN / not applicable**.

Own attempt to run the old V3 architecture/metabolization tests:

```text
python3 -m pytest -q v3/tests/test_architecture_invariants.py v3/tests/test_metabolization_effects.py
=> collection ERROR: ModuleNotFoundError: No module named 'yaml'
```

This is an **environment HOLD**, not a target failure; the source tree’s test dependency is absent. No behavioral target test was run. No sourcefree F1/F2/F3 result is accepted.

## 10. C12 and RP0/C9 status

C12 fork perception loss is an R2 intake/owner-decision RED at actual source. This RM40-R2 target does not repair it and F1.1 correctly says `WAIT_FOR_C9_C12_STORAGE_OWNER_FREEZE`. No C9/C12 live authority, C12 fork repair, or native C12/A5 is proved. The RP0-R2 sourcefree SQL probes are not this target and are not a native authority.

F0 is a separate R2 return; its 58+21 test claims are worker-reported and not rerun here. F0 is not RM40-R2.

## 11. NOT_RUN / inherited

- **NOT_RUN by this reviewer:** full V3 behavioral suite; F1/F2/F3 tests; actual adapter imports; current C9/C12 assembled runtime; C12 fork repair; C11/Pyat; A0–A5; provider/model calls.
- **INHERITED:** C12 actual fork perception-loss RED and owner docket from intake; prior S/S-R/RP0/RM40/F0/RRP0/RRM40/RF0 evidence at pinned refs, not re-adopted as native.
- **Worker-reported, not accepted as own PASS:** target’s validator, target’s source claims, F0 58+21, prior actor SQL probes.

## 12. Evidence conclusion

`EXECUTED` facts: 480/ten-cell arithmetic, S04/S05 comparison, 59/59 and 31/31 source hashes, target artifact hashes, M17 source truth, line audit, and M37 source gap.

`NOT_PROVEN`: 40 executable tests, 40 current consumers, F1/F2/F3 implementation, C9/C12 storage authority, C12 fork safety, source science, native person.

**No source or target file was edited by this review.**
