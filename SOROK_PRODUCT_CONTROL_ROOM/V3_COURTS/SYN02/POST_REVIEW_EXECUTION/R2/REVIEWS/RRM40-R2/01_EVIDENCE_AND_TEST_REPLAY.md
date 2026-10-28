# SYN02-RRM40-R2 / 01 — evidence and test replay

**Review:** independent hostile all-40 source, 480-cell and F1/F2/F3 gate.
**Review branch:** `agent/sorok-syn02-review-rrm40-r2-literal-source-r1`.
**Sealed startup:** `a7a6c781e158cd1317c0ecd0d6e1e542a4fd633d`.
**Author target:** `a67f155ba06ebb33067769510e940012d71b3fa6`; target parent `2da83f77d820b327169673386d52c4acefbbdd46`.
**Source root:** `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging` (read-only).
**Evidence grades:** `EXECUTED` = own command/probe; `SOURCE_INSPECTION` = exact source read; `INHERITED` = prior pinned evidence not rerun; `NOT_RUN` = not executed and not a pass.

## 1. Target identity and artifact hashes

The target contains six files under `R2/RM40/`; it does not contain the R2 commission/intake files, which live at the review startup. This review read the target files from the immutable commit and the commission/intake from startup. Target `00_RETURN.md` is 6,183 bytes and has SHA-256 `066f6d997f2d44291f5f2963f2c8d6085cf3ac9c872c85c61aee6cb818a4a045`; its own hash is correctly not embedded.

| Target file | Bytes | SHA-256 |
|---|---:|---|
| `00_RETURN.md` | 6,183 | `066f6d997f2d44291f5f2963f2c8d6085cf3ac9c872c85c61aee6cb818a4a045` |
| `01_ALL40_LITERAL_SYMBOL_CALLSITE_PATCH_PLAN.md` | 80,838 | `6d96c83b472e2d9a97af21df16318e03701106a3c3da49195f26aea67a0b3ff0` |
| `02_CORRECTED_SOURCE_GRADED_40X12.json` | 856,819 | `e332787287b92b6efdfdb63eafd2fc68a69327807be310162b6e97f02f2cce0e` |
| `03_TEN_CELL_ADJUDICATION_AND_M17_CORRECTIONS.md` | 9,638 | `e4a47903bbb317cff7c4cd9b5d2001058952c567d0c5ecff067e6fed77ab0e4c` |
| `04_F1_F2_F3_TESTABLE_MIGRATION_PATCHES.md` | 18,122 | `2625e7ca41ba08f0101a62779ed87cf6581675b5099aa3173855fd744995f25c` |
| `05_VALIDATE_R2.py` | 5,059 | `cb9f9b5606764fc324daa785ee1e7cc1559d4ecc86c34414121dd7a2109ce0b2` |

`EXECUTED` artifact hash check: all six bytes/hashes match. The target has no old V3 source edit and no target/source file was modified by this review.

## 2. Recorded validator replay

Command:

```text
python3 /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrm40r2-review-evidence/target/05_VALIDATE_R2.py \
  --json /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrm40r2-review-evidence/target/02_CORRECTED_SOURCE_GRADED_40X12.json \
  --source-root /Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging
```

Exact output (`EXECUTED`):

```text
PASS: 40 rows, 480 unique cells, 126/354 baseline, 124/356 final, 10 changed, 8 carrier, 2 unsupported
PASS: 59/59 source hashes, 31/31 S50 hashes, 40 unique consumers/test IDs, all exact symbols present
PASS: no fake M17 symbols; X remains scoped historical source, never permission
```

This is a valid structural/source-subset check. It does not verify source line content, per-symbol kinds, registry completeness for callsites, executable tests, current consumers, or F1/F2/F3 code.

## 3. Independent 480-cell replay

Own S05 parser at `321fa29bb3e51849a43cb7caf1600625bf215539` (`EXECUTED`):

```text
S05 rows=40 cells=480 X=126 dash=354
JSON rows=40 cells=480 unique=480
JSON marks=124 X / 356 dash
changed=10 exact set
S05→JSON mark changes:
  M14/N02 X→dash UNSUPPORTED
  M39/N01 X→dash UNSUPPORTED
  (all eight other discrepancies retain X as carrier-only)
```

Exact changed set: `M09/N01`, `M10/N01`, `M11/N01`, `M13/N01`, `M14/N02`, `M18/N01`, `M19/N01`, `M24/N01`, `M36/N01`, `M39/N01`. Relation counts in target JSON: `NONE=354`, `DIRECT_CONDITIONAL=116`, `INDIRECT_CARRIER_ONLY=8`, `UNSUPPORTED=2`. The arithmetic is 126−2=124, not ten removals.

S04 is a reviewed disposition table, not a second 480 status matrix; S05 is the matrix source used here. S04 independently records 31 ADAPT, three REPLACE (M31/M33/M39), three REMOVE (M34/M35/M36), and the three reuse cases (M26 invariants, M29 immediate body, M30 invariants). See `SOURCE_INSPECTION` in §4.

## 4. Source identity and line audit

Own rehash against mounted source (`EXECUTED`):

```text
source_registry: 59 unique paths; 59/59 SHA-256 and bytes exact
s50_selected_files: 31; 31/31 SHA-256 and bytes exact
```

Own `source_location` line audit (`EXECUTED`, script in evidence directory):

```text
111 file:line references across 56 unique files
out-of-range references: 0
unparsed prose tokens: 6
  M30 v3/V3_UNDERLIES_V2_ARTICULATION.md (prose; no callable line)
  M31 v2/ENNEAGRAM_EMERGENCE_SYSTEM.md (prose; no callable line)
  M31 v2/PROBABILISTIC_ENNEAGRAM_SYSTEM.md (prose; no callable line)
```

Symbol presence and exact source facts (`SOURCE_INSPECTION`):

- M01 `BackboneState` at `v3/core/state.py:501`, `hash_jsonable` at `v3/core/year_record.py:15`, `GenerationIntegrityAccumulator` at `v3/core/generation_integrity.py:13`.
- M04 `compute_hostage_index` at `v3/core/derived.py:45` and `_derive_hostage_index` at `v3/psyche/gating.py:61`; the target includes the derived file.
- M17 actual `apply_gift_disruption_shards_from_events` at `v3/engine/expectation_events.py:103`; call at `v3/engine/effects/delta_templates.py:361-362`; `GiftShard`/`DisruptionShard` at `v3/core/state.py:339/353`.
- M19 reads `state.rendered_output` at `v3/engine/effects/metabolization_effects.py:549` and builds `NarrationSupport` before psychological mutation.
- M25 YAML has 19 `core_steps` and 20 `steps` including `active_magnets_update`; `run_one_year` iterates 20 (`v3/v3_yearly_step_order.yaml:60-79/426`; `v3/engine/yearly_step.py:19-55`).
- M26 writes `state.metabolic_style` and `state.registers` at `v3/core/derived.py:332/334`.
- M29 `render_year` writes only `state.rendered_output` at `v3/render/phenomenology.py:155`; the immediate body is surface-only.
- M37 final route `v3/run_and_print.py:150-152` calls `render_year` after the year loop; SHA-256 `f2c1bbcbbdd39dda37e1334e035383535a8c04bfa6feb2d8253687576805eb60`, 9,441 bytes.
- M39 canonical function at `v3/engine/effects/metabolization_effects.py:273`; server import/call at `server/generation/simulation.py:13/539`.

The `source_location` line audit is a range check, not a proof that every line contains a symbol; the symbol-presence probe in §5 is separate.

## 5. Literal source probes

### 5.1 M17 actual function and fake aliases

`EXECUTED` against the mounted source:

```text
actual True
fake_gift False
fake_disruption False
gift 1 positive attachment
disruption 1 negative True
```

Probe setup: `BackboneState(year=2020, age=10)` with one active striving object `id=s1`, `need_axis=attachment`, `identity_load=70`, and one fulfillment plus one violation event. The actual function creates one `GiftShard` and one `DisruptionShard`; it does not create the prior fake symbols. This is a behavioral source probe of M17 only, not a psychological validation.

### 5.2 M25 scheduler counts

`EXECUTED` via Ruby YAML parse (Python `yaml` is unavailable in this environment):

```text
core=19
steps=20
extension_policy=append_only
active_magnets_update present after render_layer
```

The target's “19 core/20 executed” claim is source-true. Its `run_and_print.py:123` callsite remains unregistered.

### 5.3 M37 route

`EXECUTED` source read:

```text
v3/run_and_print.py:123  run_one_year(...)
v3/run_and_print.py:139  run_llm_band_year(...)
v3/run_and_print.py:152  render_year(state, derived, config)
```

The final rerender exists and is absent from M37's source location, source files, and the 59-file registry. S04 explicitly says both server per-year render and separate `run_and_print` final rerender exist.

### 5.4 M19/M26/M29 source facts

`SOURCE_INSPECTION`/`EXECUTED` static reads confirm: M19 prose→NarrationSupport→psyche, M26 `registers`/`metabolic_style` writes, M29 immediate `render_year` state surface write, M38 schedule/cache functions. These are hazards the target identifies; they are not current consumer proof.

## 6. Callsite and machine-map defects

### 6.1 Unregistered `run_and_print` callsites

Own callsite audit (`EXECUTED`):

```text
M25 callsite: run_and_print.py:123  -> not in source_registry/source_files
M27 callsite: run_and_print.py:139  -> not in source_registry/source_files
M37 callsite: server; persona; V2 (no exact path/line)
```

The actual file is `v3/run_and_print.py` with hash/bytes in §4. The target's 59/59 hash claim is true for the 59 listed files, but the registry is not a complete source identity map for the calls it cites. It must add the file or mark those callsites `SOURCE_HELD`.

### 6.2 Per-symbol kind is absent from the machine JSON

`EXECUTED` type check:

```text
row `symbols` type: str (semicolon-separated)
per-symbol objects: 0
```

Rows M15/M22/M23/M25/M30/M31/M37/M39 therefore have no machine-readable per-symbol `{name, kind, path, line, sha256}` mapping. The human `symbol_kind_detail` does not satisfy a mechanical source-map consumer.

### 6.3 Consumer and test labels

`EXECUTED` structural count: 40 unique `first_future_consumer` strings, 39 `TO_BUILD`, 1 `RULE_HELD`; 40 unique `T-M…` strings. This is a string-uniqueness result, not evidence of 40 concrete first consumers or executable tests. Compound labels include M26 “all read-only C9 views”, M21 “ANALYST-only”, M25 “C9.event_sequence / C12 batch”, M14 “C9.configuration_read / SYN02-C”, and M04 “C9.support_load_read / world interval”.

## 7. F1/F2/F3 implementation and test evidence

`git ls-tree` target:

```text
neo_v3 files: NONE
R2/RM40 test/fixture/adapter files: NONE
```

Target `04` has 30 unique `T-F…`/derived test IDs (and target `01` has 40 `T-M…` IDs), but no fixture, module, or executable test. The target's own `00` reports sourcefree behavioral tests `NOT_RUN`.

Cross-artifact API/type conflicts found by exact comparison:

- `02` M26/M38: `compute_view(snapshot, view_id) -> DerivedViewValue` in `neo_v3/derived/registry.py` and `neo_v3/derived/schedule.py`.
- `04` F1.1: `compute_view(snapshot, request) -> DerivedViewValueV1` in `neo_v3/derived/read_port.py`.
- `02` M30: `read_surface(...) -> ActorVisibleSurface`; `04` F2.2: `read_surface(...) -> ActorVisibleSurfaceV1`.
- `02` M29: `render_surface(...) -> SurfaceRecord`; `04` F2.1: `SurfacePacketV1`; no mapping.
- `04` F3.3: `run_guarded_sequence` raises `NotImplementedError("WAIT_FOR_WORLD_FAILURE_PARTIAL_POLICY")` while the prose says it can be exercised as a dry run.

No F1/F2/F3 code was run. No `T-M…`/`T-F…` behavioral test was run.

## 8. C12, science, authority, and environment

- **C12 fork RED:** `INHERITED` from the R2 intake and C12 owner docket at exact startup; not rerun here. The target does not repair it. F1.1 correctly says `WAIT_FOR_C9_C12_STORAGE_OWNER_FREEZE`, but that is a hold, not acceptance.
- **C9/C12 storage authority:** `NOT_PROVEN`; target has no C9/C12 implementation, schema, transaction, or live outbox. Sourcefree C9/SQL probes from another R2 return are not native authority.
- **Science:** `HOLD`; no Rule A/T, CAN008/CAN011 issuance, independent B, formed person, or E2 semantic read. The 480 cells remain conditional source relevance.
- **Authority:** `HOLD`; no C11/Pyat/C12/A5, ADP/SCI05 admission, production merge, or source-owner decision.
- **Environment:** Python V3 tests attempted with `python3 -m pytest -q v3/tests/test_architecture_invariants.py v3/tests/test_metabolization_effects.py`; collection failed with `ModuleNotFoundError: No module named 'yaml'`. This is an environment HOLD, not a target failure, and no behavioral pass is claimed. Ruby Psych parsed the YAML for the independent scheduler count.

## 9. Evidence conclusion

`EXECUTED`: target artifact hashes; author validator replay; independent S05/JSON 480 arithmetic; 59/59 and 31/31 source hashes; callsite audit; line-range audit; M17 actual function probe; M25 YAML counts; M37 route read.

`SOURCE_INSPECTION`: M19/M26/M29/M37/M38 source locations and write/read effects; S04 disposition table.

`NOT_RUN`: F1/F2/F3 implementation/tests; full V3 suite (blocked by missing PyYAML); native C9/C12/C12 fork; C11/Pyat; A0–A5; any paid model/product call.

`INHERITED`: C12 fork perception-loss RED and owner docket; prior pinned source evidence. No inherited claim is converted into a native grant.

No source, target, production, C9/C12, CAN/ADP, or Pyat file was edited by this review.
