# SOROK RCF-A — original V3 × Neo developmental machine source recovery

**Disposition:** `SOURCEFREE_SOURCE_ARCHITECTURAL_RECOVERY__40_M_12_N_19_CA__ENGINEERING_SCOPED__SCIENCE_AND_AUTHORITY_HELD`.

The historical V3/V2 source archive is present and was read directly. The key TD-R05 source files match their pinned hashes; the enclosing ZIP hash does **not** match TD-R05’s recorded archive hash, so this return claims selected-file provenance, not whole-container provenance. The 40 historical mechanisms are source-mapped, but the old runtime is not a current person engine and is not adopted.

## Identity and custody

- Repository: `maidiu/rawlsing` (private).
- Return branch: `agent/sorok-rcf-a-v3-developmental-sourceclose-20261030-r1`.
- Current PRE-MAIN read cut: `750548ddbb9b4392a16ce93097b856f349e16182`.
- Historic source pin: `299f41e97a43c67be9cc76a79fa49b48f4e12e54`.
- Historical archive path: `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging.zip`; observed SHA-256 `3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289`. TD-R05 expects `953c9149…`; **container mismatch**, but selected file hashes below match TD-R05.
- Host: `oldMac` (local `scutil` verification); harness OpenCode; agent `opencode`; model `opencode-go/deepseek-v4.1-flash`; MAX requested, actual effort `UNVERIFIED`; UI title/ID unknown.
- Worktrees: return `.../opencode/rcf-a-return`; source audit read-only archive at `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging`.
- No original author/reviewer, PRE-MAIN, PR #514/#516/#519/#521, native source/respondent corpus or current product code was modified or executed beyond the sourcefree archive tests. PyYAML 6.0.3 was installed only into a temporary test target because the host lacked the archive’s `pyyaml>=6.0` dependency.

## FINDING — source mechanisms are real; not a unified current engine

The archive contains actual V3 implementation files and tests, not just README summaries. `01_FUNCTION_SOURCE_OWNER_RECEIVER_LEDGER.json` maps all **40 M IDs** to canonical archive paths, exact SHA-256 values, verified functions/fields and tests. It also maps all **12 N requirements** and all **19 C/A milestones**, with M↔N and N↔C/A links.

Key source identity:

- `v3/core/state.py` SHA-256 `19e968d4…`, `BackboneState` at line 501.
- `v3/core/derived.py` SHA-256 `e479fc3e…`, `compute_all_derived` at line 322.
- `v3/core/invariants.py` SHA-256 `81298f3f…`, limit/placeholder checks at lines 132–329.
- `v3/v3_yearly_step_order.yaml` SHA-256 `90496a2c…`; 19-step core spine.
- `v3/engine/yearly_step.py` SHA-256 `da3147c3…`, `run_one_year` at line 12.
- `v3/engine/step_runner.py` SHA-256 `5a737c17…`, `run_n_years` at line 13.
- `v3/psyche/flow.py` SHA-256 `6da4effd…`: `_channel_conductance` line 366, `_domain_charge_ledger` line 406, `_update_memory` line 678, `run_pressure_flow_cycle` line 753.
- `v3/render/phenomenology.py` `render_year` line 55; `v2/conversation_engine.py` `prepare_conversation_turn` line 2079.
- `v3/core/generation_integrity.py` `GenerationIntegrityAccumulator` line 13; `server/generation/store.py` readiness functions lines 77/245; `server/session_state.py::_generation_state_is_ready` line 53.

The selected source files match TD-R05 for 36/40 M rows (at least one file per row); the remaining four rows use direct archive files outside the selected manifest. Full row-level status is in `01`.

## Actual test execution — 40 selected tests, one named mutation

All runs used the exact archive code, with `PYTHONPATH` set to the archive plus the temporary PyYAML target.

| Test file | Actual result |
|---|---:|
| `v3/tests/test_architecture_invariants.py` | **4 passed** |
| `v3/tests/test_step_logic.py` | **12 passed** |
| `v3/tests/test_v5_pressure_flow.py` + `test_v5_pressureflow_golden_run.py` | **24 passed** |

The architecture tests include `test_step_order_immutable`, `test_llm_no_backbone_mutation`, `test_events_cannot_write_domains_or_peak_routing`, `test_no_derived_fields_in_backbone_state`; step logic includes `test_run_one_year_advances_and_derived_valid`; pressure-flow tests exercise `run_pressure_flow_cycle`, conductance, memory and transaction boundaries.

**Mutation severance:** in a copied V3 tree, moving `render_layer` before `field_update` in the `steps` order makes the unchanged `test_step_order_immutable` fail with the named core-spine subsequence `AssertionError`; it is not an import or unrelated setup failure. The original archive remained unmodified.

**NOT_RUN:** TD-R05’s reported 80-test aggregate as one current suite; full V3/V2 historical suite; LLM calls; native source/respondent data; current C9/C12/A0–A5 integration; production. No 80-test claim is made.

## What is real, what is invalid, what is reusable

**Strong preserved mechanisms:** persistent `BackboneState`/`YearRecord`, stored-versus-derived separation, 19-step dependency spine, transactional pressure-flow membrane, per-domain history/memory/groove bookkeeping, render-only nonmutation, V3-under-V2 one-way membrane, fail-fast derived-schedule consistency, and clean/degraded/blocked readiness.

**Invalid or contingent mechanisms to quarantine/remove:** M08 identity-seeded wound (`v3/psyche/channels.py:36` uses class/minority/religiosity/age), M15/M36 missing-parent 50/50/50 and hopeful defaults (`v3/io/parent_baseline_from_behavior.py`), M34 fabricated fallback practice (`v3/engine/llm_contract.py:173–207`; first-candidate fallback in `run_llm_band.py`), M35 placeholder cracks/frameworks (`v3/core/invariants.py:253–297`), M39 module-global random age-band rupture (`v3/engine/effects/metabolization_effects.py:273–332`), M31 Enneagram/type-determines-person (no current authoritative engine), and M37 structural stubs treated as lived scenes. M37/M38/M40 themselves remain useful only with the quarantine/fail-fast/readiness semantics preserved.

**Current comparison:** no direct old-V3 import into current BP2P4J/R31J A0–A3 is demonstrated. `BackboneState` is not a C12 actor record; `compute_all_derived` is not a C9 semantic receipt; `render_year`/`prepare_conversation_turn` are V2 surfaces, not current C9 writers. The old runtime is a source donor for adapted state/derived/scheduler/flow modules, not a mergeable engine. Current BP2P4J/R31J and the current Pyat R15 apparatus are distinct source cuts; R15 here is **not** the old V3 M25 scheduler.

## N11 / M25 / 101 coexistence

The old M25 `run_one_year` is a **slow-time annual scheduler** with a 19-step core subsequence. N11 is a 3–5 event batch with N/N+1 two-call interaction and no ordinary LLM calls between events. They must coexist as separate clocks/versions, not be collapsed:

1. Keep M25/`run_one_year` as an optional slow-time annual projection over actor/world state.
2. Use N11 as the event-level recursion owner; event N and N+1 consume actual changed state, not an annual multiplier.
3. Preserve world, actor and observer clocks separately; no numeric global-time bridge and no silent event fallback.
4. Any adapter must expose an explicit `schedule_mode` and test both annual and event-batch paths; do not make absence of an event manufacture a year event.

## Three courts

- **ENGINEERING:** `ACCEPT_SCOPED_SOURCE_ARCHITECTURAL_LEDGER` — 40 M source rows, 12 N, 19 C/A, 132 verified symbols, 40 selected tests plus named mutation. Not current integration.
- **SCIENCE:** `HOLD_ORIGINAL_DOMAIN_RULES__NO_NATIVE_PERSON` — old code is historical mechanism/substrate, not validated developmental science. No primary scientific texts were available in the archive; no passage claim is made.
- **AUTHORITY:** `HOLD_ORIGINAL_OWNERS_AND_CANONICAL_CAS__NO_ADOPTION` — no source/native/production/adoption right is transferred.

## FINDING → INTERPRETATION → ACTION → OWNER

**FINDING:** the actual archive contains 40 source mechanisms with real computational content, but also multiple identity/default/fallback/random mechanisms that are scientifically invalid or overclaimed.

**INTERPRETATION:** preserve the state/derived/scheduler/flow/render skeleton and quarantine invalid psychological content. A new engine is unnecessary; a bounded adapter is.

**ACTION:** original V3/V2 owner and Neo requirement owners should select the portable core modules, approve/reject N11 coexistence, and authorize any adapter to current C9/C12/A0 consumers. Do not merge the archive.

**OWNER:** original V3/V2 source owner; CAN/ADP/CAN011/ADP016/017 owners; Sorok HQ; separate reviewer. No self-adoption.

## DONE / REMAINING / CRITICAL BLOCKERS / LARGEST PRODUCTIVE MOVE / FLIGHT / DELTA

- **DONE:** 40 M source ledger, 12 N, 19 C/A, 132 verified symbols, 40 selected tests, named mutation, invalid-mechanism audit, archive/source hashes and freshness record.
- **REMAINING:** original-owner source selection; N11/M25 adapter design; current C9/C12/A0 first consumer; primary scientific reading; native permissions.
- **CRITICAL BLOCKERS:** archive container hash mismatch; no current first consumer; invalid defaults/placeholders/random rupture; no native domain science; current BP2P4J/R15 integration absent.
- **LARGEST PRODUCTIVE MOVE:** owner selects `BackboneState`/`compute_all_derived`/`run_pressure_flow_cycle`/`run_one_year` as the portable core and authorizes a narrow N11-compatible adapter with the state/derived boundary intact.
- **FLIGHT:** one sourcefree local archive audit; no current branch/native/LLM/production mutation.
- **DELTA:** replaces README-level inheritance with exact file/function/hash evidence and an explicit quarantine/reuse map; no new engine or native claim.

## First actual consumers

Historical: `run_one_year` consumes `compute_all_derived` and `run_pressure_flow_cycle`; `render_year` is consumed by `test_llm_no_backbone_mutation`; `prepare_conversation_turn` is the V2 surface consumer. Tests: `v3/tests/test_step_logic.py`, `test_v3/tests/test_architecture_invariants.py`, `v3/tests/test_v5_pressure_flow.py`. Current product first consumer: **NOT PROVEN**; the closest current comparative interfaces are BP2P4J `JoinedProduct`/R31J `R31JProduct` at the exact source cuts, not an old-V3 import.

## Final remote SHA

The ordinary push binds this return. Exact 40-hex SHA is read back externally and reported in the final response; it is not self-referential. No force-push, no PRE-MAIN mutation, no self-adoption.
