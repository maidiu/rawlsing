# SYN02-RRM40 — evidence and acceptance docket

**Review:** independent hostile RRM40 source/crosswalk court.
**Review branch:** `agent/sorok-syn02-review-rrm40-source-r1`.
**Sealed startup:** `4fc21d74d5c585ba6c83b3de2e6ace2d5127b392`.
**Review target:** `653d356d773ab025c4ed22e9d70ba8fc25d6f839`; content commit `1ecc62ef1bfab9015967002be8fdd8b8874de092`.
**Architecture target:** `321fa29bb3e51849a43cb7caf1600625bf215539`.
**Evidence grades:** `EXECUTED` = rerun in this review; `SOURCE_INSPECTION` = exact mounted-source line/hash read; `INHERITED` = prior court evidence not rerun; `NOT_RUN` = not executed and not treated as a pass.

## 1. Immutable subject identity

Target RM40 files were read from Git object `653d356d...`, not inferred from a branch name.

| File | Git blob | SHA-256 |
|---|---|---|
| `RM40/00_RETURN.md` | `48aa329ac1d9c183a3496c4ba2a1e3e3ddaed180` | `53762e93b52f6e91f11660b8ada270fe2319fb5c374bec48456e7db38000a804` |
| `RM40/01_ALL40_ORIGINAL_TO_NEW_FUNCTION_PATCH_MATRIX.md` | `6e1132abe5be30dac33bd92797e857fa95c35cbd` | `a90f74a7ef3426db1ae441809fde9896b94f9e7df59bb3ac1cb183075b153008` |
| `RM40/02_VERIFIED_480_CELL_M_TO_N_CROSSWALK.json` | `4f66a95738786567d325824a4707874983a65da9` | `00d6e622f33ad5218d5517e017e1be8e451e0f232dbe35bce48b3ae720754390` |
| `RM40/03_TEN_DISCREPANCY_SOURCE_ADJUDICATION.md` | `be4475aeaafd3867396a2a7a846d01578b5b28f6` | `9631849c4bb60e87c73db934b44b5b7f11833bb1ccaee596795fb6e189740db1` |
| `RM40/04_LEGACY_MIGRATION_AND_PATCH_TEST_SPEC.md` | `97691ed3b2525fbad3b5ba22e11b0a4e0ffd3f86` | `0a7615077349d946776a498cacc5372b4c441dc6e5baed7117e1a216f2fb409f` |

`653d356d...` changes only `00_RETURN.md` relative to `1ecc62ef...`; the four substantive files are the content-commit files. The local staging ZIP `3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289` does not match TD-R05 `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`; no archive-wide exactness is claimed.

## 2. Executed 480-cell validator

Command run in the isolated review worktree:

```text
python3 /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrm40-evidence/validate.py
```

Independent parser outputs (S04/S05 read at `321fa29b...`; RM40 JSON read at `653d356d...`):

```text
S04: rows=40 cells=480 X=116 dash=364
S05: rows=40 cells=480 X=126 dash=354
S04/S05 mismatch: 10
M09/N01, M10/N01, M11/N01, M13/N01, M14/N02,
M18/N01, M19/N01, M24/N01, M36/N01, M39/N01
JSON: rows=40 cells=480 X=124 dash=356
JSON baseline_s05 X=126
unique source files=59; exact=59; missing/mismatch=0
S50 selected=31; exact=31/31
```

The final JSON relation counts are `DIRECT_CONDITIONAL=116`, `INDIRECT=8`, `UNSUPPORTED=2`, `NONE=354`. The JSON `changed_cells` array has ten adjudications; eight retain X and two remove X. Exact final matrix values are `124 X / 356 dash / 480`.

Acceptance: `ACCEPT_SCOPED` for 40/12/480 parsing, counts, exact mismatch set, 59/59 file hashes and 31/31 S50 selected hashes. This does not validate any psychological or native rule.

## 3. Ten disputed cells: exact source and line evidence

All paths are relative to `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging`. Hashes are SHA-256 of the exact mounted source files.

| Cell | Source path:line | Source SHA-256 | Adjudication | Acceptance |
|---|---|---|---|---|
| **M09/N01** | `v3/core/state.py:151` (`Crack`); `v3/systems/cracks.py:25` (`update_cracks`); `v3/core/invariants.py:253` (`ensure_min_cracks`) | `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`; `b11a87e87be216d78c84f76ff645e26a39bb40512475558c95a279c78796bec3`; `81298f3fc51b46cda8d72d0db914b672b17b9a35e13004fe59a9b0e29dada5e3` | `INDIRECT_CARRIER_ONLY`; X retained | Tension/crack has no need axis, object, activity episode, or motive field. It can condition a later response only. `ACCEPT_SCOPED`; not direct/N01 coverage. |
| **M10/N01** | `v3/core/state.py:176` (`Buffer`); `v3/systems/buffers.py:73` (`update_buffers`) | `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`; `9c9ed09001dad364ab4011ee29e8ea2df3c332745db736b1a6e1dbe56e332b35` | `INDIRECT_CARRIER_ONLY`; X retained | Support/cost resource can condition activity; no need-object or motive target. `ACCEPT_SCOPED`; not direct/N01 coverage. |
| **M11/N01** | `v3/core/state.py:187` (`Framework`); `v3/systems/frameworks.py:33` (`update_framework_weights`) | `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`; `0d59fc6e177009da92e39eb61ea729eace97f50392baa93999cb6513f81dd2cb` | `INDIRECT_CARRIER_ONLY`; X retained | Interpreting mediator/capacity does not itself form the need or object. `ACCEPT_SCOPED`; not direct/N01 coverage. |
| **M13/N01** | `v3/core/state.py:231` (`PracticeStack`); `v3/systems/practices.py:19` (`update_practice_stack`) | `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`; `b984397e5e8c24b68d94a6ef06e7cdd7bb07513db45a5480b48f154ece79720d` | `INDIRECT_CARRIER_ONLY`; X retained | Practice category/scalar is not an activity episode, object, or motive. `ACCEPT_SCOPED`; not direct/N01 coverage. |
| **M14/N02** | `v3/core/state.py:257` (`PeakRouting`); `v3/systems/topology.py:50`; `v3/systems/boundary.py:43`; `v3/systems/coherence.py:18` | `19e...`; `4e3b9b64399dfcfad67a431729d9443767d5e074080ef6b51bc1c8df48711560`; `e8c2495f5bd0699f5737a9e137dd327ec3d8c6953af262460ab03998f249a9c4`; `1bf8c1bee7a4197e3fb1eea34c89aed115edd3602c92c91888ada6790f575c4a` | `UNSUPPORTED`; X removed | Loop/boundary/coherence has no caregiver, care act, availability, expectation, scope, or reception. `ACCEPT_SCOPED`; X must remain removed. |
| **M18/N01** | `v3/core/state.py:369` (`RuptureShard`); `v3/engine/effects/metabolization_effects.py:144` (`create_rupture_shard_from_event`) | `19e...`; `d4775271ca097e99e615cee19b381a478ad6d90a25051c5fce1b1e0e3c1adb1e` | `INDIRECT_CARRIER_ONLY`; X retained | A violated assumption/domain can disturb a later need response; it does not form need, object, or motive. `ACCEPT_SCOPED`; not direct/N01 coverage. |
| **M19/N01** | `v3/core/state.py:392` (`MetabolizationProcess`); `v3/engine/effects/metabolization_effects.py:358` (`compute_metabolization_delta`); `:521` (`update_metabolization_and_plasticity_step`) | `19e...`; `d4775271ca097e99e615cee19b381a478ad6d90a25051c5fce1b1e0e3c1adb1e` | `INDIRECT_CARRIER_ONLY`; X retained | Capacity/bias can condition response; no need/object/activity formation. The later prose→psyche route is a separate body defect. `ACCEPT_SCOPED`; not direct/N01 coverage. |
| **M24/N01** | `v3/core/state.py:560` (`stability_threshold_inertia`); `v3/systems/stability_inertia.py:17` (`stability_inertia_dissipation`) | `19e...`; `5a11c8b07eafe2b8f1d7e9864c9cb066a5c45f19c2c45a8d4223b3a64c394c78` | `INDIRECT_CARRIER_ONLY`; X retained | Residue/inertia conditions persistence; it is not a need or object. `ACCEPT_SCOPED`; not direct/N01 coverage. |
| **M36/N01** | `v3/core/state.py:305` (`NEED_AXES`); `v3/io/parent_baseline_from_behavior.py:25` (`infer_parent_baseline_and_regime`); `v3/engine/expectation_baseline.py:107` (`derive_child_expectation_baseline`) | `19e...`; `4e5be6448a5b76c413492ec2a83b62d9e9a2247ce131a094727d974a17cf750b`; `632e1e608bfc674a241e57bafa24e91834a2b8bdc3e4ed326dae6fca4e695d43` | `INDIRECT_CARRIER_ONLY`; X retained; primarily N02 | `NEED_AXES` is expectation vocabulary; no motive/object formation. `ACCEPT_SCOPED` only with explicit N02/carrier wording; never N01 coverage. |
| **M39/N01** | `v3/engine/effects/metabolization_effects.py:273` (`maybe_inject_rupture_at_band_age`); `server/generation/simulation.py:539` call | `d4775271ca097e99e615cee19b381a478ad6d90a25051c5fce1b1e0e3c1adb1e`; `5d68ffe3bc6902dc60b90625443a03127cf0d04b4eed4327270a3a0226bc78d1` | `UNSUPPORTED`; X removed | Age/RNG rupture injection has no need, object, activity, or motive. The old N01 warning is stale. `ACCEPT_SCOPED`; X must remain removed. |

Source-hash strings above are exact for the files cited; repeated `19e...` is `v3/core/state.py` `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2` (26,310 bytes). The cited files are inside the 59-file identity. M36's own source register lists `parent_baseline_from_behavior.py` and `expectation_baseline.py`; `NEED_AXES` is the shared `state.py` constant already cited in the broader 59-file register.

## 4. Source-callable corrections

| M | RM40 claim | Exact source finding | Required acceptance |
|---|---|---|---|
| **M15** | `NEED_AXES; derive_child_expectation_baseline; infer_parent_baseline_and_regime` | `NEED_AXES` is a tuple constant at `v3/core/state.py:305`; functions at `v3/engine/expectation_baseline.py:107` and `v3/io/parent_baseline_from_behavior.py:25` | Split constant from functions. `REVISE_PRECISE`; source identity is otherwise exact. |
| **M17** | `create_gift/disruption_shard_from_event` | No such function. Actual: `apply_gift_disruption_shards_from_events` at `v3/engine/expectation_events.py:103`; called from `v3/engine/effects/delta_templates.py:361-362`; creates `GiftShard`/`DisruptionShard` | Replace name and cite actual call site. `REVISE_PRECISE`; this is a false literal name, not merely shorthand. |
| **M21** | `derive_vitality/insulation` | `derive_vitality_profile` at `v3/psyche/vitality.py:85`; `derive_insulation_profile` at `v3/psyche/insulation.py:72`; route at `v3/psyche/flow.py:753` | Split both functions and preserve the route finding. `REVISE_PRECISE`. |
| **M22** | `child_model; backbone_state_from_identity; PASS1_SYSTEM` | `child_model` is a field at `v3/core/state.py:549`; the other symbols are not one literal function | Mark field/constant/callable separately. `REVISE_PRECISE`. |
| **M23** | `autonomy_drive/safety_drive; autonomy_condition/safety_condition; autonomy_safety_micro_drift` | Fields around `v3/core/state.py:554-558`; only `autonomy_safety_micro_drift` is a function at `v3/systems/autonomy_safety.py:27` | Mark fields and function separately. `REVISE_PRECISE`. |
| **M25** | Primary `v3/v3_yearly_step_order.yaml`; `run_one_year; step_one_year; run_n_years; test_step_order_immutable` | Production functions at `v3/engine/yearly_step.py:12/102` and `v3/engine/step_runner.py:16`; `test_step_order_immutable` is test code, not a production callable | Keep YAML as config evidence; cite functions/tests separately. `REVISE_PRECISE`. |
| **M31** | Primary `v2/ENNEAGRAM_EMERGENCE_SYSTEM.md`; three function names | Functions at `v2/enneagram_wisdom.py:615`, `v2/parent_type_inference.py:33/143`; markdown is design evidence | Label docs vs callables. `REVISE_PRECISE`; replacement decision remains. |
| **M37** | `distill_memory filtering` | `distill_persona_sheet_backstory` at `v3/tools/distill_memory.py:218`; `_preprocess_backstory` at `:72`; server simulator at `server/generation/simulation.py:71` | Name functions; preserve two-render-path finding. `REVISE_PRECISE`. |
| **M39** | `_maybe_inject_rupture_at_band_age; maybe_inject_rupture_at_band_age` | Definition `v3/engine/effects/metabolization_effects.py:273`; server import `simulation.py:13`; call `:539`; `_maybe` is alias | Label alias/call site/function separately. `REVISE_PRECISE`. |

The `02` source-file registers for these rows are correct; the defect is the “literal callable”/primary-symbol presentation in `01` and the return claim, not the file hashes.

## 5. Source identity execution

The mounted source is the actual historical staging tree, not a Git checkout:

```text
/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging
```

Results:

- 59 unique source paths in RM40 `02`: 59/59 exact SHA-256 and byte identity.
- 31 S50 selected files: 31/31 exact.
- No missing path, no changed hash.
- Archive ZIP mismatch is reported above; file-level identity is the only accepted identity.
- Source hashes prove selected file identity, not semantic validity, current import, or native rule.

The exact target `02` file itself has SHA-256 `00d6e622f33ad5218d5517e017e1be8e451e0f232dbe35bce48b3ae720754390`; the source register is therefore immutable. The review did not edit the source tree or RM40.

## 6. 40-row disposition and source-cell acceptance

The target disposition counts are correct: `REUSE=3`, `ADAPT=31`, `REPLACE=3`, `REMOVE=3`, `RESEARCH_UNDECIDED=0`.

| Decision | IDs |
|---|---|
| `REUSE` | M26 (pure-derived invariant only), M29 (immediate render body only), M30 (one-person/read-only V2 invariant only) |
| `ADAPT` | M01–M25, M27, M28, M32, M37, M38, M40 |
| `REPLACE` | M31, M33, M39 |
| `REMOVE` | M34, M35, M36 |

All 40 M rows exist once and each has 12 N cells. The matrix has no duplicate or missing M/N key. `DIRECT_CONDITIONAL` is still conditional historical relevance, not direct native coverage. `INDIRECT` is not a formed need/object. `UNSUPPORTED` is not a negative scientific result.

The machine JSON contains 11 distinct `first_potential_consumer` strings, repeated across 480 cells (`CAN008/C9 immediate read` 80 times; ten other strings 40 times each). These are design labels, not actual consumers. No current C9/C12 semantic consumer or no-change alternative is proved.

## 7. High-risk source evidence

| M | Exact source evidence | Review consequence |
|---|---|---|
| **M19** | `update_metabolization_and_plasticity_step` `v3/engine/effects/metabolization_effects.py:521` reads `state.rendered_output`, constructs `NarrationSupport`, and applies capacity/bias changes; no transaction/rollback. | F1/F2 must sever prose→psyche. `ACCEPT_SCOPED` source finding; causal use `HOLD`. |
| **M21** | `run_pressure_flow_cycle` `v3/psyche/flow.py:753`; pre-route writes and route trace/hysteresis. | Preserve route-scoped transaction/trace; never claim whole-actor rollback. `ACCEPT_SCOPED`. |
| **M25** | `run_one_year` `v3/engine/yearly_step.py:12`; YAML config `v3/v3_yearly_step_order.yaml` (19 core/20 configured, `active_magnets_update` appended). | Year is not the event/interval unit. `ACCEPT_SCOPED`. |
| **M26** | `compute_all_derived` `v3/core/derived.py:322` writes `state.metabolic_style` and `state.registers`. | A migration-only call must clone/freeze; live call reintroduces hidden writes. `REVISE_PRECISE`. |
| **M27/M28** | `v3/engine/llm_contract.py:87/159`; `v3/engine/scoring.py:32`; selected events are premerged/not canonical rows. | Require canonical event admission and per-event application; no model-created event. `ACCEPT_SCOPED`. |
| **M29** | `render_year`/immediate render body; full LLM band is not render-only. | Keep immediate render body only; no later prose causality. `ACCEPT_SCOPED`. |
| **M30** | One-person V2 jurisdiction survives; age<17→35 and parent-narrative substitution are unsafe. | One-person/read-only only. `ACCEPT_SCOPED`. |
| **M31** | Type functions at `v2/enneagram_wisdom.py:615`, `v2/parent_type_inference.py:33/143`. | Replace causal typology; optional forensic view only. `ACCEPT_SCOPED`. |
| **M33** | `v3/engine/event_engine.py` mechanical sampler. | Replace with source-owned event realization. `ACCEPT_SCOPED`. |
| **M34/M35/M36** | Fallback event, placeholder minimums, unknown-parent hopeful/default at `v3/core/invariants.py:253`, `v3/io/parent_baseline_from_behavior.py:25`, `v3/engine/expectation_baseline.py:107`. | Remove causal fallback/placeholder/hopeful default; hold unknown/valid-empty. `ACCEPT_SCOPED`. |
| **M37** | Server `run_simulation_for_session` `server/generation/simulation.py:71`; `v3/io/persona_sheet.py:470/579`; `v3/tools/distill_memory.py:218`. | Both render paths exist; annotation must not become memory/previous scene. `ACCEPT_SCOPED`. |
| **M38** | Derived schedule can leave unscheduled derived fields stale. | One canonical registry; fail-fast equality. `ACCEPT_SCOPED`. |
| **M39** | `maybe_inject_rupture_at_band_age` `v3/engine/effects/metabolization_effects.py:273`; server call `simulation.py:539`. | Replace age/RNG injection; archive shell only. `ACCEPT_SCOPED`; N01 X removed. |
| **M40** | Stored persona/name/country/`degraded_ready` is not a person; readiness is multi-gate. | Keep multi-gate readiness; no clean-ready by name/country. `ACCEPT_SCOPED`. |

The source findings above are `SOURCE_INSPECTION`; no old V3 behavioral suite was executed by this review.

## 8. F1/F2/F3 evidence and acceptance matrix

| Requirement | Target status | Review finding | Acceptance |
|---|---|---|---|
| F1 `DerivedView` pure, snapshot-keyed, no state write | Specified | Good intent; old `compute_all_derived` still writes unless called on a clone/read-only snapshot | `REVISE_PRECISE`; test snapshot/`registers`/`metabolic_style` invariance before/after |
| F1 source fingerprint/`SourceRef`/migration all-or-nothing | Specified | Useful contract; exact per-M old/new line/import/signature and source receipt missing | `REVISE_PRECISE` |
| F1 legacy quarantine | Specified | Correct quarantine set; no code/migration run | `ACCEPT_SCOPED_DESIGN`; build `HOLD` |
| F1 cross-store actor/world authority | Not specified | No C9 actor-version/decision/outbox authority, C12 world journal authority, CAS/unique idempotency key, watermark, crash/fork reconciliation or `SYNC_HELD` | `RED` for build; `F1.1 BUILD=NO` until RP0 + C9/C12 owner |
| F2 one-way surface, M29/M30/M37 separation | Specified | Direction correct; no actual adapter | `ACCEPT_SCOPED_DESIGN` |
| F2 actor-safe memory serialization | Concept only | `select_accessible_features` has no exact packet schema/allowlist, indirect count/order/gap prohibition, or feature-removal noninterference test | `REVISE_PRECISE`; semantic memory `HOLD` |
| F2 SCI05 implicit dependence | Partly specified | Says pointer absence is not proof, but does not default-hold all potentially dependent half2 proposals when SCI05 denied | `REVISE_PRECISE`; `HOLD` |
| F3 proposal-only 3–5 shell | Specified | Correct no-fallback/no-extra-LLM intent; no actual C6/C8/C9/C12 adapter | `ACCEPT_SCOPED_DESIGN` |
| F3 world batch policy | `POLICY_UNDECIDED` | Correct to hold; no owner-selected policy exists | `HOLD`; no irreversible batch |
| F3 Rule A/T separation | Specified | Correct held-missing-rule distinction; no issued rule | `HOLD` |
| Future F1/F2/F3 tests | Names/assertions listed | None executed; no test files, fixtures, or implementation | `NOT_RUN` |

The target's “largest lawful immediate tranche” is acceptable only as a **specified** tranche after F1.0/C9-C12 authority and source-owner gates. It is not an implemented or native tranche.

## 9. Current/native status and F0 boundary

Inherited current-state facts from S-R/D/RB remain controlling; this review did not rerun them:

- S36 production Rule A/T registries are empty.
- S37 is targetless/test-only; no current C12 positive.
- S42 is one-event test; S46/S47 are workshop interval; S48 is one-call transport; S49 natural B is empty; S52 is withheld/test-static.
- PRE-MAIN/C11 is unwired for native C12/A5; no native source/actor grant.
- No actual C9/C12 assembled runtime, provider call, natural B, SCI05 admission, Pyat C11, A0–A5, or full Mac behavioral suite was run here.

F0 is a separate branch, `agent/sorok-syn02-f0-source-portability-r1` at `9903a30d8d9cd4594f58c46bec80e538610a1851`. Its 58 sourcefree-test claim and branch/extra-file scope were **not** rerun or approved by RRM40; it is not the RM40 target. F0 gate remains open and cannot be replaced by RM40 matrix acceptance.

## 10. NOT_RUN and test commands

**NOT_RUN by RRM40:**

- Full historical V3 Mac behavioral/test suite.
- Forty independently executed focused old-M test suites.
- F1/F2/F3 implementation, migrations, or new tests.
- Current C9/C12 assembled runtime, S36/S37/S42/S48/S49/S52 execution.
- Actual natural B, SCI05, CAN008/010/011/012 Rules, Pyat C11, A0–A5.
- Provider/model/account call.
- F0 58 sourcefree tests or branch approval.
- Any native C12/A0–A5 evidence.

Future test commands in `04` are specifications only, including `pytest tests/neo_v3/test_pure_derived.py`, `test_legacy_migration.py`, `test_adp_memory_access.py`, `test_batch_3_5.py`, `test_c9_c12_receipt.py`, and `test_s48_s52_portability.py`. None were executed.

## 11. Acceptance and handoff

| Acceptance item | Result | Next owner/gate |
|---|---|---|
| 40 M rows × 12 N, 480 unique cells, 126/354 → 124/356 | `ACCEPT_SCOPED` | Evidence owner / atlas owner; keep conditional-X semantics |
| exact ten S04/S05 mismatch cells, eight indirect/two unsupported | `ACCEPT_SCOPED`; wording repair “ten adjudications, two mark removals” | RRM40/HQ evidence owner |
| 59/59 source files and 31/31 S50 selected hashes | `ACCEPT_SCOPED` | Source identity owner; file identity only |
| all 40 literal callable claim | `REVISE_PRECISE` | V3 source engineer |
| F1/F2/F3 code-edit-ready patch plan | `REVISE_PRECISE`; no F1.1 build | C9/C12 + source/ADP/SCI05 owners |
| full-person / current C9/C12 / cross-store / SCI05 | `RED`/`HELD` | C9/C12 storage owners, SCI05/ADP, native owners |
| science | `HOLD` | CAN008/010/011/012 + ADP/SCI05 original owners |
| authority | `NO_NATIVE` | HQ + original source custodians only |
| F0 | separate `NOT_RUN` / gate open | F0 owner/Pyat |

**Final RRM40 review terminal:** `480_CELL_SOURCE_MAP_ACCEPT_SCOPED__ALL40_LITERAL_CALLABLE_REVISE_PRECISE__TEN_ADJUDICATIONS_8_INDIRECT_2_UNSUPPORTED__PATCH_MAP_NOT_CODE_READY__F1.1_BUILD_NO__CROSS_STORE_SCIENCE_AUTHORITY_HELD__F0_SEPARATE_OPEN__NO_NATIVE_GRANT`.

No source edit, implementation, production merge, scientific issuance, or native grant.
