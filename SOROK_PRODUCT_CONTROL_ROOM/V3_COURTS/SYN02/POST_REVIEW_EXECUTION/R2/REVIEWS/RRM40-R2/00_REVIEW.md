# SYN02-RRM40-R2 — independent hostile all-40 source, 480-cell and adaptation court

**Status:** `RRM40_R2_INDEPENDENT_HOSTILE_COURT__480_AND_59_31_ACCEPT_SCOPED__M17_CORRECTED__M37_SECOND_RENDER_SOURCE_GAP_REVISE__MIXED_SYMBOL_KIND_MACHINE_GAP__F1_F2_F3_TEST_SPEC_ONLY__F1_1_HOLD_C12_FORK_RED__NO_NATIVE_GRANT`.

**Review branch:** `agent/sorok-syn02-review-rrm40-r2-literal-source-r1`.
**Sealed review startup:** `a7a6c781e158cd1317c0ecd0d6e1e542a4fd633d`.
**Immutable author target:** `a67f155ba06ebb33067769510e940012d71b3fa6` (`R2/RM40/` six-file return).
**Prior architecture/evidence refs:** SYN02-S/S-R, RP0/RM40/F0, RRP0/RRM40/RF0, R2 intake and C12 owner docket as pinned by the commission; C12 source owner decision is not this reviewer's grant.
**Source root:** read-only `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging`.
**Role:** fresh independent hostile I3 source/engineering reviewer; not R2 author, prior RRM40 reviewer, HQ, original CAN/ADP/SCI05/C8/C9/C12 issuer, production editor, or own adopter.
**Write scope:** this directory only. No source, target, production, C9/C12, CAN/ADP/Pyat, or other-reviewer edit.

## 1. Three separate verdicts

| Court | Verdict | Exact boundary |
|---|---|---|
| **ENGINEERING** | `REVISE_PRECISE / 480_MATRIX_ACCEPT_SCOPED / M17_FIX_ACCEPT_SCOPED / M37_SOURCE_GAP_REVISE / F1_F2_F3_TEST_SPEC_ONLY` | The 480-cell parse, ten adjudications, 59/59 and 31/31 identities, M17 actual callable, and most literal source locations reproduce. The source map is not yet a complete code-edit plan: one M37 second-render path is uncited, mixed-symbol rows lack machine per-symbol kinds, and all F1/F2/F3 test IDs are specifications, not executable tests. |
| **SCIENCE** | `HOLD_RULE_UNISSUED / SOURCE-LEVEL-ONLY` | Conditional historical links are not current imports, CAN008/CAN011 Rule A/T, an E2 semantic read, learning law, memory admission, or a formed person. Eight retained links are carrier-only; two are unsupported. |
| **AUTHORITY** | `NO_NATIVE_GRANT / HOLD` | No original C8 independent-B source, C9 actor storage freeze, C12 projection/fork repair, C11/Pyat weld, C12/A5 person, ADP/SCI05 admission, production permission, or scientific owner decision is issued. C12 fork remains an independent RED/owner decision. |

The target itself says `SCOPED_SOURCE_AND_ENGINEERING_REPAIR__PENDING_INDEPENDENT_REVIEW__NO_NATIVE_GRANT`; this review preserves that scope and rejects any promotion to code-ready, current-consumer, or native.

## 2. What independently passed

| Claim | Review result | Evidence |
|---|---|---|
| 40 M rows, 12 N cells each, 480 unique cells | `ACCEPT_SCOPED` | Independent parse of target JSON and S05: 40/40 rows, 12/12, 480 unique M/N. |
| Baseline S05 126 X/354 dash; corrected 124 X/356 | `ACCEPT_SCOPED` | Independent S04/S05 parse: S04 116/364, S05 126/354, final JSON 124/356; exactly the ten named mismatch cells. |
| Eight `INDIRECT_CARRIER_ONLY`, two `UNSUPPORTED` | `ACCEPT_SCOPED` | Exact set: M09/N01, M10/N01, M11/N01, M13/N01, M14/N02, M18/N01, M19/N01, M24/N01, M36/N01, M39/N01. M14/N02 and M39/N01 remove X; the other eight retain X as carriers. |
| 59/59 source files and 31/31 S50 selected | `ACCEPT_SCOPED` | Own SHA-256/byte rehash against the mounted source; no file mismatch. Archive-wide identity is not claimed. |
| M17 actual source name | `ACCEPT_SCOPED` | `apply_gift_disruption_shards_from_events` at `v3/engine/expectation_events.py:103`; called at `v3/engine/effects/delta_templates.py:361-362`. No `create_gift_shard_from_event`/`create_disruption_shard_from_event` definition exists. |
| M15/M22/M23/M24/M25/M30/M31/M37/M39 no longer masquerade as one literal callable | `ACCEPT_SCOPED_WITH_PRECISION_REPAIR` | The human `symbol_kind_detail` is honest, but the machine JSON has one row-level `symbol_kind`; it does not attach a kind to every symbol in each mixed row. |
| Source hashes and artifact hashes | `ACCEPT_SCOPED` | Target 00 hashes match the actual bytes for 01–05. The target 00 self-hash is deliberately not embedded. |
| Ten-cell nomenclature | `ACCEPT_SCOPED` | Ten adjudications, not ten mark changes; only two X removals. 126−2=124. |

## 3. Source-level defect found — M37 second render path is uncited

M37 is not fully sourced in the target:

- Target `01` M37 cites `server/generation/simulation.py:71`, `v3/io/persona_sheet.py:579/470`, and `v3/tools/distill_memory.py:218/72`; its `source_files` list contains only those three files.
- Target `01`/`04` nevertheless says M37 has a final rerender path (“final path overwrites”, “two routes”).
- The actual second path is `v3/run_and_print.py:152`:

```text
v3/run_and_print.py
SHA-256 f2c1bbcbbdd39dda37e1334e035383535a8c04bfa6feb2d8253687576805eb60
bytes 9441
line 152: render_year(state, derived, config)
```

`v3/run_and_print.py` is **not** in the target 59-file registry, is not in M37’s `source_files`, and is not in the M37 `source_location`/`callsite`. The target’s M37 “two render paths” claim therefore has one unsourced leg. This is a `REVISE_PRECISE` source-identity defect, not a reason to reject the 480 arithmetic.

Required repair: add `v3/run_and_print.py:152` with SHA/bytes to M37 (and either expand the source registry to 60 or explicitly scope the 59 registry as excluding the CLI route), or remove the “two routes/final path” claim from M37. The actual `v3/run_and_print.py` final render is real and must not be inferred from the server module.

## 4. Other source-level precision findings

### 4.1 Mixed rows need per-symbol kinds

The target correctly changes the row-level primary kind for mixed rows, but the machine JSON does not carry a machine-readable per-symbol kind. Important examples:

| M | Row `symbol_kind` | Mixed symbols actually present |
|---|---|---|
| M15 | `constant` | `NEED_AXES` constant plus two functions |
| M22 | `field` | `child_model` field, `PASS1_SYSTEM` constant, `backbone_state_from_identity` function |
| M23 | `field` | four state fields plus `autonomy_safety_micro_drift` function |
| M24 | `field` | state field plus `stability_inertia_dissipation` function |
| M25 | `config` | YAML schedule plus production functions and test |
| M30 | `prose_abstraction` | prose design plus two functions |
| M31 | `prose_abstraction` | two docs plus three functions |
| M37 | `callsite` | server function/calls plus persona/distillation functions |
| M39 | `callsite` | function plus server import/call alias |

The human `symbol_kind_detail` is not a substitute for a code generator or a mechanical source court. Required: a `symbols[]` array or equivalent with `{name, kind, path, line, sha256, role}` per symbol. The row-level kind is not false, but it is insufficient for the claimed “literal symbol” machine map.

### 4.2 First consumers are future labels, not current consumers

All 40 target rows are `TO_BUILD` except M31 (`RULE_HELD`). None is `LIVE`, `IMPLEMENTED_UNWIRED`, `TEST_ONLY`, or an actual imported C9/C12/V2 reader. The 40 strings are unique, but several are not single concrete consumers:

- M26: `all read-only C9 views` (not one first consumer)
- M21: `CAN008.route_trace_read → ANALYST-only` (not an actor consumer)
- M25: `C9.event_sequence / C12 batch` (two targets)
- M14: `C9.configuration_read / SYN02-C` (two labels)
- M04: `C9.support_load_read / world interval`

The validator’s unique-string count does not prove 40 grounded first consumers. Required: mark these as `FUTURE_CONSUMER_LABEL`/`TEST_SPEC_ONLY`, nominate one future adapter call per row, and keep all current-consumer claims `HELD`.

### 4.3 Test IDs are specifications, not executed tests

The 40 `T-M…` values are unique strings. `00_RETURN` says the sourcefree behavioral tests in `04` are `NOT_RUN`; `04` is a specification. `05_VALIDATE_R2.py` does not execute any `T-M…` test; it checks JSON structure, symbols as substrings, source hashes and string uniqueness. The target’s phrase “Runnable sourcefree test ID” in `01` is therefore too strong. Required: `TEST_SPEC_ONLY` labels and actual test files before any pass claim.

### 4.4 F1/F2/F3 are design specifications, not code-edit-ready adapters

- No `neo_v3` module, adapter, fixture, or test file exists in the target.
- F1.1 is explicitly `WAIT_FOR_C9_C12_STORAGE_OWNER_FREEZE`; its `C9ActorHistoryPort`/`C12DerivedStorePort` are placeholders.
- F1.1 uses `DerivedViewValueV1` in the function signature and `DerivedViewValue` in the patch ledger; the type contract is inconsistent.
- F2.2 contains no fail-closed **all-half2** SCI05 quarantine. It says a missing hidden fact or generated self-change is refused, but does not state that a denied/held N+1 half1 self-account quarantines the entire 3–5 half2 proposal set unless a separate competent source/SCI05/ADP certificate exists. That is an open S-R P0/G09 condition.
- F2.1 supplies a packet shape but no serializer implementation, exact allowlist implementation, or feature-removal test.
- F3.3 correctly raises `NotImplementedError("WAIT_FOR_WORLD_FAILURE_PARTIAL_POLICY")`; the shell is not executable and no irreversible world performance is permitted.
- No F1/F2/F3 behavioral test was run by this reviewer. Target 04 explicitly says `NOT_RUN`.

## 5. Per-M disposition

All 40 source rows have a valid source path, line reference (except explicit prose artifacts), and source hash. The only source-row correction with a missing selected file is M37. Mixed-kind rows are accepted only with the per-symbol repair in §4.1.

| M | Verdict | Correction / limitation |
|---|---|---|
| M01–M14 | `ACCEPT_SCOPED_SOURCE` | Literal classes/functions/call sites and source hashes reproduce. M06 line 318 is a write site, not a new callable; the row’s symbol list is still correct. |
| M15 | `ACCEPT_SCOPED_SOURCE / KIND_REPAIR` | `NEED_AXES` constant plus two functions; add per-symbol kind. |
| M16–M21 | `ACCEPT_SCOPED_SOURCE` | M17 actual function and call site verified; M19 prose→psyche and M21 route findings supported by source. No behavioral pass. |
| M22–M24 | `ACCEPT_SCOPED_SOURCE / KIND_REPAIR` | Field/constant/function mixtures; add per-symbol kind. |
| M25 | `ACCEPT_SCOPED_SOURCE / KIND_REPAIR` | YAML 19 core/20 configured; add per-symbol kind for config/functions/test. |
| M26 | `ACCEPT_SCOPED_SOURCE / F1_GUARD` | `compute_all_derived` writes `metabolic_style`/`registers`; F1.3 full snapshot is right, but no executable guard/test. |
| M27–M29 | `ACCEPT_SCOPED_SOURCE` | Premerge, immediate-render and source facts reproduce; F3/F2 remain spec-only. |
| M30–M31 | `ACCEPT_SCOPED_PROSE / NO_LINE` | Prose docs correctly have no callable line; functions are separate. M31 remains `RULE_HELD`. |
| M32–M36 | `ACCEPT_SCOPED_SOURCE` | Source/removal/replace dispositions reproduce; no behavioral test. |
| M37 | `REVISE_PRECISE` | Missing `v3/run_and_print.py:152`/hash for the second render path; add source or remove claim. |
| M38 | `ACCEPT_SCOPED_SOURCE / KIND_REPAIR` | Config and functions; per-symbol kind needed. |
| M39 | `ACCEPT_SCOPED_SOURCE / KIND_REPAIR` | Function plus alias/call site; N01 X remains removed. |
| M40 | `ACCEPT_SCOPED_SOURCE` | Source paths/lines and readiness finding reproduce; no native readiness. |

## 6. F1/F2/F3 and C12 gate

| Area | Verdict | Reason |
|---|---|---|
| F1.1 pure derived | `HOLD` | No implementation; placeholder ports; source/actor storage contract absent; type name inconsistency. |
| F1.1 storage/C9/C12 | `HOLD` | F1.1 waits for a C9/C12 owner freeze; C12 fork perception loss is an independent RED owner decision. |
| F1.2 legacy migration | `ACCEPT_SCOPED_DESIGN / TEST_SPEC_ONLY` | Quarantine categories are directionally correct; no migration code or fixture. |
| F1.3 full-snapshot invariant | `ACCEPT_SCOPED_DESIGN` | Correct response to `compute_all_derived` hidden writes; no test file. |
| F2.1 surface packet | `REVISE_PRECISE` | No executable serializer/allowlist; event/count/gap labels need actual leak tests. |
| F2.2 one-way V2/SCI05 | `REVISE_PRECISE` | Missing explicit set-wide half2 quarantine on denied/held SCI05; no implementation. |
| F3.1 proposal 3–5 | `ACCEPT_SCOPED_DESIGN` | Rules are sensible; no parser/test code. |
| F3.2 admission | `HOLD` | Depends on C8/C9/CAN Rule A/T and canonical event owner; none is issued. |
| F3.3 shell | `HOLD` | Correctly refuses irreversible world performance; `POLICY_UNDECIDED`. |
| All `T-M…` tests | `NOT_RUN` | No test files or adapters; validator checks only strings/structure. |

C12 fork is not repaired or tested by this target. The R2 intake and C12 owner decision record an actual perception-loss RED; F1.1 cannot be accepted for build until C12 owner repair/guard and C9/C12 freeze. Sourcefree actor SQL from RP0-R2 is not a native C9 authority.

## 7. Full-person and authority boundary

The target preserves the right architecture at design level: one historical actor, external material world, source-qualified events, pure derived views, one-way V2 surface, explicit unknown/held/nochange, and no narrator-created psyche. It does **not** prove a full person, current E2 semantic consumer, independent B, care/work/time, actor-safe memory, SCI05 admission, C11 weld, C12 cold/fork, or A0–A5.

No science or native authority follows from source hashes, a passing JSON validator, 480 cells, M17 correction, or future test IDs. The target’s own science and authority verdicts are `HOLD`.

## 8. Findings, repairs and owners

| ID | Finding → finite repair | Owner | First future consumer |
|---|---|---|---|
| **RRM40R2-01** | M37 second render path `v3/run_and_print.py:152` is absent from source registry/location/files. Add its hash/bytes/lines or remove the two-route claim. | V3 source engineer / source-map owner | V2/ADP016 annotation path; **TO_BUILD** |
| **RRM40R2-02** | Mixed rows have only row-level `symbol_kind`; add per-symbol `{name,kind,path,line,sha256,role}`. | RM40 machine-map owner | future patch generator; **TEST_SPEC_ONLY** |
| **RRM40R2-03** | 40 consumer labels are future; M26/M21/M25/M14/M04 are not single concrete consumers. Mark `FUTURE_CONSUMER_LABEL`; nominate one future adapter. | architecture owner / C9-C12 consumer owner | future C9/C12/V2; **HELD** |
| **RRM40R2-04** | 40 `T-M…` IDs are not runnable tests. Mark `TEST_SPEC_ONLY`; add test files and actual results before PASS claims. | F1/F2/F3 implementers + independent tester | no current consumer |
| **RRM40R2-05** | F2.2 lacks all-half2 SCI05 fail-closed rule when half1 denied/held; optional pointer is not proof. Add entire-set quarantine and independent-certificate exception. | SCI05/ADP016/017 + C8/C12 | N+1 future prospect gate; **HOLD** |
| **RRM40R2-06** | F1.1 type mismatch `DerivedViewValueV1` vs `DerivedViewValue`; no actual storage ports. Freeze one type and one owner adapter. | C9/C12 storage owner | derived view read; **HOLD** |
| **RRM40R2-07** | C12 fork perception loss remains a source-owner RED; no F1.1 build/freeze on unverified fork. | C12 source/storage owner + independent reviewer | C12 cold/fork/A0–A5; **HELD** |
| **RRM40R2-08** | No current C9/C12/V2 consumer, Rule A/T, independent B, native C12/A5; only design labels. Keep science/authority `HOLD`. | original CAN/ADP/SCI05/C8/C9/C12/Pyat owners | future E2/A5; **NO_NATIVE** |

## 9. Terminal

`RRM40_R2_480_MATRIX_AND_59_31_ACCEPT_SCOPED__M17_CORRECTED_ACCEPT_SCOPED__M37_SECOND_RENDER_SOURCE_GAP_REVISE_PRECISE__MIXED_SYMBOL_KIND_MACHINE_REPAIR__F1_F2_F3_TEST_SPEC_ONLY__F1_1_AND_C12_FORK_HELD__NO_NATIVE_GRANT`.

No source edit. No production merge. No Rule A/T. No science or native C12/A5 grant. No self-adoption.
