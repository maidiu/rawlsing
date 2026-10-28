# SYN02-RRM40-R2 — independent hostile all-40 source and 480-cell review

**Status:** `RRM40_R2_INDEPENDENT_HOSTILE_REVIEW__480_AND_59_31_ACCEPT_SCOPED__M17_ACCEPT_SCOPED__M37_M25_M27_SOURCE_CALLSITE_REVISE__MACHINE_PER_SYMBOL_KIND_REVISE__F1_F2_F3_SPEC_NOT_CODE__F1_1_C12_HOLD__NO_NATIVE_GRANT`.

**Review branch:** `agent/sorok-syn02-review-rrm40-r2-literal-source-r1`
**Sealed startup:** `a7a6c781e158cd1317c0ecd0d6e1e542a4fd633d`
**Immutable author target:** `a67f155ba06ebb33067769510e940012d71b3fa6`
**Target parent:** `2da83f77d820b327169673386d52c4acefbbdd46`
**Source root:** `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging` (read-only)
**Role:** independent hostile I3 source/engineering reviewer; not the R2 author, prior reviewer, Sorok/Pyat HQ, original source/science issuer, production editor, or own adopter.

## 1. Three separate verdicts

| Court | Verdict | Boundary |
|---|---|---|
| **ENGINEERING** | `REVISE_PRECISE` | The 40×12 arithmetic, S05 126/354 baseline, corrected 124/356, ten exact adjudications, eight carrier-only/two unsupported links, 59/59 file hashes, 31/31 S50 hashes, and M17 correction reproduce independently. The source map is not complete: M37's final render route and the M25/M27 `run_and_print` callsites are absent from the 59-file identity registry; mixed rows lack per-symbol machine kinds; future consumers and test IDs are labels, not actual consumers/tests; F1/F2/F3 contain cross-artifact type/API conflicts and no code. |
| **SCIENCE** | `HOLD_RULE_UNISSUED / SOURCE_LEVEL_ONLY` | The 480 cells are conditional historical source relevance, not current imports, Rule A/T, CAN008/CAN011 issuance, an E2 semantic read, a formed person, or a learning law. Eight X cells are carrier-only; two are removed as unsupported. |
| **AUTHORITY** | `NO_NATIVE_GRANT / HOLD` | No C8 independent-B source, C9 actor storage freeze, C12 fork repair, C11/Pyat weld, C12/A5 person, ADP/SCI05 admission, production permission, or owner science decision is issued. F1.1 remains `WAIT_FOR_C9_C12_STORAGE_OWNER_FREEZE`; the separate C12 fork perception-loss RED is not repaired by this target. |

The target's own `00_RETURN` says `SCOPED_SOURCE_AND_ENGINEERING_REPAIR__PENDING_INDEPENDENT_REVIEW__NO_NATIVE_GRANT`; this review preserves that boundary and rejects promotion to code-ready, current-consumer, executable-test, or native status.

## 2. Independently accepted claims

| Claim | Review result | Evidence |
|---|---|---|
| 40 M rows × 12 N cells = 480 unique cells | `ACCEPT_SCOPED` | Independent parse of target `02`; 40 ordered M rows, 480 unique `(M,N)`, 12 per row. |
| S05 baseline 126 X / 354 dash; final 124 X / 356 | `ACCEPT_SCOPED` | Independent parse of S05 at `321fa29bb3e51849a43cb7caf1600625bf215539` and target `02`: 126/354 baseline, 124/356 final. |
| Ten exact adjudications, eight carrier-only, two unsupported | `ACCEPT_SCOPED` | Exact set below. Only M14/N02 and M39/N01 change X→dash; M36/N01 remains carrier-only to N02 expectation vocabulary. |
| 59/59 source hashes and 31/31 S50 selected hashes | `ACCEPT_SCOPED_AS_SUBSET` | Own SHA-256/byte rehash against mounted source; all listed files exact. This proves the 59 listed files, not that the registry is complete for all cited callsites. |
| M17 actual callable and absence of fake aliases | `ACCEPT_SCOPED` | `apply_gift_disruption_shards_from_events` at `v3/engine/expectation_events.py:103`; call at `v3/engine/effects/delta_templates.py:361-362`; source probe created one GiftShard and one DisruptionShard; fake names absent. |
| M19 narrator feedback source fact | `ACCEPT_SCOPED` | `update_metabolization_and_plasticity_step` reads `state.rendered_output` at `v3/engine/effects/metabolization_effects.py:549` and builds NarrationSupport before psychological deltas. |
| M25 19 core / 20 configured route | `ACCEPT_SCOPED` | YAML has 19 `core_steps` and 20 `steps` including `active_magnets_update`; `run_one_year` iterates the configured list. |
| M26 hidden derived writes | `ACCEPT_SCOPED` | `compute_all_derived` writes `state.metabolic_style` and `state.registers` at `v3/core/derived.py:332/334`; the fixed-name invariant does not cover them. |
| M29 immediate renderer and M37 final route | `SOURCE_FACT_ACCEPTED / TARGET_CITATION_INCOMPLETE` | `render_year` sets `state.rendered_output`; `run_and_print.py:152` calls it again after the year loop. The second route is real source, but is absent from target M37 and the 59-file registry. |
| M31/M33/M39 replacement, M34–M36 removal | `ACCEPT_SCOPED_SOURCE` | Source dispositions and hazards match; no current native replacement is implemented. |
| Target artifact hashes | `ACCEPT_SCOPED` | Target 01–05 hashes match bytes; target 00 correctly does not embed a self-hash. |

The exact ten adjudications are: M09/N01, M10/N01, M11/N01, M13/N01, M14/N02, M18/N01, M19/N01, M24/N01, M36/N01, M39/N01. Eight retain X as `INDIRECT_CARRIER_ONLY`; M14/N02 and M39/N01 are `UNSUPPORTED` and removed. Final X is 126−2=124, not 126−10.

## 3. Findings, evidence, rival explanation, repair, owner, future consumer

| ID | Finding | Evidence | Rival explanation | Finite repair | Owner | First future C12/A0–A5 consumer |
|---|---|---|---|---|---|---|
| **RRM40R2-01** | M37 final render route is not source-identified in M37. Target `01` says “final rerender”/“final path overwrites”; target `02` M37 `source_location`, `source_files`, and registry omit `v3/run_and_print.py`. | Actual `v3/run_and_print.py:150-152` says “Re-render so rendered_output matches current state” and calls `render_year`; SHA-256 `f2c1bbcbbdd39dda37e1334e035383535a8c04bfa6feb2d8253687576805eb60`, 9,441 bytes. S04 explicitly records both server per-year render and run_and_print final rerender. | The server per-year path alone might be considered the intended M37 route, but then the target's “two routes/final overwrite” claim is false. | Add `v3/run_and_print.py:152` with hash/bytes to M37 and source files/registry (registry becomes 60 or is explicitly scoped as excluding the CLI route), or remove the dual-route/final-path claim. | V3 source engineer / RM40 source-map owner. | C9/ADP016 annotation separation; `TO_BUILD`, not live. |
| **RRM40R2-02** | M25 and M27 cite `run_and_print.py` callsites, but no such file is in the 59-file source registry or their `source_files`; the target also uses basename rather than exact `v3/run_and_print.py`. | Independent audit of target `callsite` fields found `M25 run_and_print.py:123` and `M27 run_and_print.py:139`; source registry contains neither. Actual file identity above; lines 123 and 139 verified. | These may be intentionally out-of-scope external callers, but then they must be marked `SOURCE_HELD` and excluded from “exact original source path/hash” claims. | Add `v3/run_and_print.py` with exact hash/bytes and lines, or mark M25/M27 callsites `SOURCE_HELD` and remove them from the exact-callsite claim. | RM40 source-map owner. | M25 event sequence/C12 batch; M27 event realization proposal queue; both future/held. |
| **RRM40R2-03** | Machine JSON does not carry per-symbol kind. Each row has one `symbol_kind` and a semicolon string of symbols; mixed rows therefore cannot be mechanically mapped. | Target `02` rows expose `symbols` as `str`; no `symbols[]` objects. Mixed examples: M15 constant+functions, M22 field+constant+function, M23 four fields+function, M25 config+functions+test, M30 prose+functions, M31 prose+functions, M37 callsite/functions, M39 function+alias. | A human `symbol_kind_detail` and row-level kind may be considered sufficient for a human plan; it is not sufficient for the commission's code-generator/machine court. | Add per-symbol `{name, kind, path, line, sha256, role}` arrays to `02`, and derive `symbol_kind` from them. | RM40 machine-map owner. | Future patch generator; `TEST_SPEC_ONLY`. |
| **RRM40R2-04** | The 40 “first future consumer” strings are not 40 concrete grounded consumers. Several are compound/non-actor labels: M26 “all read-only C9 views”, M21 “ANALYST-only”, M25 “C9.event_sequence / C12 batch”, M14 “C9.configuration_read / SYN02-C”, M04 “C9.support_load_read / world interval”. | Target `02` `first_future_consumer` values and 39 `TO_BUILD`/1 `RULE_HELD` grades; own listing identifies the compound strings. | Unique strings could satisfy a syntactic count, but they do not identify a first actual call surface. | Keep all current-consumer claims `HELD`/`FUTURE_CONSUMER_LABEL`; nominate exactly one future adapter call per M and preserve compound alternatives as secondary. | Architecture owner + C9/C12/V2 interface owners. | Future C9/C12/V2 adapter, not live. |
| **RRM40R2-05** | 40 `T-M…` IDs and the F1/F2/F3 `T-F…` IDs are test specifications, not executable tests; the target validator only checks strings/structure. | Target `00` says sourcefree behavioral tests are `NOT_RUN`; `04` is prose/code sketches; `git ls-tree` target has no `neo_v3` module, fixture, or test file; `05` does not execute any test ID. | A future implementer could create these tests; that is not current test evidence. | Rename to `TEST_SPEC_ONLY`; add fixture/test files and independent replay before any PASS claim. | F1/F2/F3 implementers plus independent tester. | No current consumer; future E2/C12 gate. |
| **RRM40R2-06** | F1/F2/F3 cross-artifact API/type conflicts prevent a code-edit merge. M26/M38 use `DerivedViewValue` and `compute_view(snapshot, view_id)` in `neo_v3/derived/registry.py` and `derived/schedule.py`; F1.1 uses `DerivedViewValueV1` and `compute_view(snapshot, request)` in `read_port.py`. M30 uses `ActorVisibleSurface`; F2.2 uses `ActorVisibleSurfaceV1`; M29 uses `SurfaceRecord`; F2.1 uses `SurfacePacketV1`. | Target `02` M26/M30/M38 `new_adapter`; target `04` F1.1/F2.1/F2.2 patch ledger and code blocks. | These could be intentionally versioned layers, but no mapping/import is given and two `compute_view` ownership paths collide. | Freeze one type and one canonical function per seam; make F1.1 call the registry/schedule adapter; add explicit mapping for SurfaceRecord→SurfacePacket→ActorVisibleSurface. | RM40 map/F1/F2 owners plus C9/C12/V2 interface owner. | Derived view read, V2 surface read; `HOLD` until mapped. |
| **RRM40R2-07** | F2.2 does not contain the all-half2 SCI05 quarantine required when a denied/held N+1 first-half self-account could contaminate the entire 3–5 second-half prospect set. | Target `04` F2.2 only states missing hidden fact/self-change refusal; no `half1`, `half2`, entire-set quarantine, or independent-certificate exception. | The optional N+1 pointer may imply quarantine, but an implication is not a fail-closed test/contract. | Add: denied/held half1 self-account marks every potentially dependent half2 prospect `HELD`; no member may be admitted without separate SCI05/ADP016-017 certificate. | SCI05/ADP016/017 + C8/C12 owners. | N+1 future prospect gate; `HOLD`. |
| **RRM40R2-08** | F3.3 says the shell can be exercised as a dry run, but `run_guarded_sequence` unconditionally raises `NotImplementedError`, so no dry-run path exists. | Target `04` F3.3: function body raises `NotImplementedError("WAIT_FOR_WORLD_FAILURE_PARTIAL_POLICY")`; immediately following paragraph says “can be exercised as a dry run only.” | The raise might be a deliberate safety placeholder; then the dry-run claim should be removed, not treated as implemented. | Separate `run_dry_sequence` (proposal/admission, no world call) from `run_world_sequence` (raises until policy); test both. | C6/C8/C9/C12/product batch owner. | C9/C12 future batch; `HOLD/POLICY_UNDECIDED`. |
| **RRM40R2-09** | F1.1 remains storage-held, and the independent C12 fork perception-loss RED is not repaired or tested here. | R2 intake and C12 owner docket; target F1.1 `WAIT_FOR_C9_C12_STORAGE_OWNER_FREEZE`; target no C9/C12 implementation. | Sourcefree C9 SQL probes may pass, but they are not native C9/C12 authority and cannot cure a C12 fork. | Keep F1.1 held; require C12 fork patch/guard and C9/C12 owner freeze before build. | C12 source/storage owner + C9 owner. | C12 cold/fork/A0–A5; `HELD`. |
| **RRM40R2-10** | No science or native authority follows from source hashes, 480 cells, M17 correction, or test IDs. | Target's own science/authority HOLD; no Rule A/T, C8/B, C11/C12/A5, ADP/SCI05 admission. | A complete source map could be mistaken for a scientific validation; it is not. | Keep science/authority HOLD; require original issuers and independent native tests. | CAN/ADP/SCI05/C8/C9/C12/Pyat owners. | E2/A5 future; `NO_NATIVE`. |

## 4. Per-M disposition

| M | Verdict | Correction / limitation |
|---|---|---|
| M01 | `ACCEPT_SCOPED_SOURCE` | Class/hash/integrity source and future ActorHistory adapter. |
| M02 | `ACCEPT_SCOPED_SOURCE` | Material carrier; no 50/class defaults. |
| M03 | `ACCEPT_SCOPED_SOURCE` | Regulation/vitality; no scalar-as-ability law. |
| M04 | `ACCEPT_SCOPED_SOURCE` | Constraint/hostage source; one support-load authority; derived file included. |
| M05 | `ACCEPT_SCOPED_SOURCE` | Appraisal/access; derived projection. |
| M06 | `ACCEPT_SCOPED_SOURCE` | Estrangement/write-site source; no phantom fields. |
| M07 | `ACCEPT_SCOPED_SOURCE` | Access/persona; one-way V2 only. |
| M08 | `ACCEPT_SCOPED_SOURCE` | Sensitivity; archive demographic seeds. |
| M09 | `ACCEPT_SCOPED_SOURCE` | Crack/tension; N01 carrier-only. |
| M10 | `ACCEPT_SCOPED_SOURCE` | Buffer/support; N01 carrier-only. |
| M11 | `ACCEPT_SCOPED_SOURCE` | Framework/mediator; N01 carrier-only. |
| M12 | `ACCEPT_SCOPED_SOURCE` | Collective infrastructure→world owner. |
| M13 | `ACCEPT_SCOPED_SOURCE` | Practice; N01 carrier-only. |
| M14 | `ACCEPT_SCOPED_SOURCE` | PeakRouting; M14/N02 remains UNSUPPORTED. |
| M15 | `ACCEPT_SCOPED_SOURCE / KIND_REPAIR` | `NEED_AXES` constant plus functions; per-symbol kind missing. |
| M16 | `ACCEPT_SCOPED_SOURCE` | Striving; no age/random spawn. |
| M17 | `ACCEPT_SCOPED_SOURCE` | Actual function and call site verified; no fake aliases. |
| M18 | `ACCEPT_SCOPED_SOURCE` | Rupture; N01 carrier-only; no age ritual. |
| M19 | `ACCEPT_SCOPED_SOURCE / F1_GUARD` | Rendered-output→NarrationSupport read verified; no prose causality in new design. |
| M20 | `ACCEPT_SCOPED_SOURCE` | Magnet/relation; exact entity refs. |
| M21 | `ACCEPT_SCOPED_SOURCE` | Route source; no conserved-substance psychology; analyst-only future view. |
| M22 | `ACCEPT_SCOPED_SOURCE / KIND_REPAIR` | Field/constant/functions; per-symbol kind missing. |
| M23 | `ACCEPT_SCOPED_SOURCE / KIND_REPAIR` | Four fields + micro-drift; per-symbol kind missing. |
| M24 | `ACCEPT_SCOPED_SOURCE / KIND_REPAIR` | Field + dissipation; per-symbol kind missing. |
| M25 | `REVISE_PRECISE` | 19 core/20 configured source is true, but `run_and_print.py:123` callsite is unregistered; source identity incomplete. |
| M26 | `REVISE_PRECISE` | Hidden writes verified; derived API/type conflicts with F1.1; full-snapshot test absent. |
| M27 | `REVISE_PRECISE` | Premerge source verified; `run_and_print.py:139` callsite unregistered. |
| M28 | `ACCEPT_SCOPED_SOURCE` | No premerge/admission source; no executable admission. |
| M29 | `ACCEPT_SCOPED_SOURCE / TYPE_MAPPING_REQUIRED` | Immediate render body source; `SurfaceRecord`/packet/read-surface types unmapped. |
| M30 | `REVISE_PRECISE` | Prose/functions source; `ActorVisibleSurface` vs F2 `ActorVisibleSurfaceV1`. |
| M31 | `ACCEPT_SCOPED_PROSE / RULE_HELD` | V2 docs/functions; optional noncausal archive only. |
| M32 | `ACCEPT_SCOPED_SOURCE` | Inert source refs; fail-closed field injection. |
| M33 | `ACCEPT_SCOPED_SOURCE / REPLACE` | Mechanical event sampler source; no random causality. |
| M34 | `ACCEPT_SCOPED_SOURCE / REMOVE` | Fallback source as evidence; no fabricated event. |
| M35 | `ACCEPT_SCOPED_SOURCE / REMOVE` | Placeholder source as evidence; valid-empty only. |
| M36 | `ACCEPT_SCOPED_SOURCE / REMOVE` | Unknown-parent hopeful source; M36/N01 carrier-only. |
| M37 | `REVISE_PRECISE` | Final `run_and_print.py:152` route missing from M37/source registry; add source or remove dual-route claim. |
| M38 | `REVISE_PRECISE` | Derived schedule/cache source; duplicate `compute_view` and `DerivedViewValue` conflict. |
| M39 | `ACCEPT_SCOPED_SOURCE / KIND_REPAIR` | Function/alias/call source; N01 X removed; per-symbol kind missing. |
| M40 | `ACCEPT_SCOPED_SOURCE` | Readiness source; multi-gate, no stored-persona clean-ready. |

## 5. F1/F2/F3 gate

| Area | Verdict | Reason |
|---|---|---|
| F1.1 pure derived | `REVISE_PRECISE / HOLD` | No implementation; type/signature conflict; F1.1 ports are placeholders. |
| F1.1 C9/C12 storage | `HOLD` | C9/C12 owner freeze absent; C12 fork RED; `WAIT_FOR_C9_C12_STORAGE_OWNER_FREEZE`. |
| F1.2 migration/quarantine | `ACCEPT_SCOPED_DESIGN / TEST_SPEC_ONLY` | Quarantine categories are correct; no migration code or fixture. |
| F1.3 full-snapshot invariant | `ACCEPT_SCOPED_DESIGN` | Correct response to M26 writes; no executable test. |
| F2.1 surface packet | `REVISE_PRECISE / TEST_SPEC_ONLY` | No serializer/allowlist implementation; surface types unmapped. |
| F2.2 one-way V2 | `ACCEPT_SCOPED_DESIGN` | One-way intent; no implementation. |
| F2.2 SCI05 implicit dependence | `REVISE_PRECISE / HOLD` | Missing set-wide half2 quarantine; no current admission. |
| F3.1 3–5 proposal | `ACCEPT_SCOPED_DESIGN / TEST_SPEC_ONLY` | Count/purity rules; no code. |
| F3.2 admission | `HOLD` | Requires C8/C9/CAN source/rule and canonical event owner. |
| F3.3 guarded shell | `REVISE_PRECISE / HOLD` | Dry-run claim contradicts unconditional NotImplementedError; world policy undecided. |
| 40 `T-M…` + F-test IDs | `TEST_SPEC_ONLY / NOT_RUN` | No test files; validator checks strings only. |

## 6. Whole-person and authority boundary

The target preserves the right design direction: one historical actor, external material world, source-qualified events, pure derived views, one-way V2 surface, explicit unknown/held/nochange, and no narrator-created psyche. It does not prove an actual person, current E2 semantic consumer, independent B, care/work/time, actor-safe memory, SCI05 admission, C11 weld, C12 cold/fork, or A0–A5.

The eight retained carrier links are historical source relations, not current import authority. M14/N02 and M39/N01 remain removed. No source file, target file, production, C9/C12, CAN/ADP, or Pyat artifact was edited by this review. No science or native authority is granted.

## 7. Terminal

`RRM40_R2_ENGINEERING_REVISE_PRECISE__480_AND_59_31_ACCEPT_SCOPED__M17_ACCEPT_SCOPED__M37_M25_M27_SOURCE_GAP__MACHINE_KIND_AND_CONSUMER_TEST_REVISE__F1_F2_F3_SPEC_ONLY__F1_1_C12_HOLD__SCIENCE_HOLD__AUTHORITY_HOLD__NO_SELF_ADOPTION`.
