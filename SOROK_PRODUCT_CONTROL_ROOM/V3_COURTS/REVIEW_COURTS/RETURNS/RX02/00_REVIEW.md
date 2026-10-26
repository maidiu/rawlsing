# SOROK V3 COURTS RX02 — INDEPENDENT HOSTILE PRESSURE-FLOW SOURCE REVIEW

**Target X02:** `b8ccf53f591a9b067a029e3c64ecad2874794d03` (`agent/v3court-x02-pressure-flow-interpressure-r1`)
**Sealed startup:** `b9ff1cf05721ea8609cb631489b4a07448ec287b`
**Reviewer branch:** `agent/v3court-review-rx02-pressure-source-r1`
**Source:** `<V3_SOURCE_ROOT>` (local historical V3, read-only)
**Terminal:** `RX02_PRESSURE_SOURCE_REVIEW__X02_CORE_REPRODUCED__PRECISE_REVISIONS_F3_F4_F5_SOURCE_IDENTITY__ZERO_COERCION_STALE_EXPRESSION_AND_COERCION_DOC_DEFECTS__SCIENCE_PARTIAL_WRONG_MEANING__NO_NATIVE_GRANT`

## 1. Independence, target and access

- Review independence: RX02 is not X02's author, HQ, scientific issuer, production editor or self-reviewer. The X02 worktree was not modified; only the X02 target commit and read-only source were read.
- Target remote readback: `git ls-remote` shows `refs/heads/agent/v3court-x02-pressure-flow-interpressure-r1 = b8ccf53f591a9b067a029e3c64ecad2874794d03`. The target is immutable for this review.
- Review branch was created from the sealed startup `b9ff1cf…`; no duplicate RX02 worktree/session was found.
- Source identity independently checked:
  - **19/19** X02-inspected files match the local source and the top-level staging-zip entries.
  - **31/31** S50 selected files match their recorded SHA-256.
  - **9/19** of X02's inspected files are **not** in the S50 31-file manifest (they are `channels.py`, `gating.py`, `insulation.py`, `vessels.py`, `domains.py`, `buffers.py`, `stability_inertia.py`, `autonomy_safety.py`, `persona_sheet.py`). They still match the local source and top-level zip exactly.
  - Local staging zip `3f2c5ed9…` ≠ TD-R05 archive `953c9149…`; archive-wide identity is **not** claimed. X02's caveat is correct.
- Actual environment: OpenCode with the configured DeepSeek V4.1-Flash session; macOS 13.7.8, Python 3.11.3, pytest 9.1.1, Ruby 2.6.10; sourcefree only. No external provider/model call, raw survey data or source edit.
- Evidence: `TEST_SOURCE_AND_LOGS/rx02_review_probe.json`, `x02_probe_rerun.json`, `x02_17files_pytest.log`, `x02_probe_flow_copy.py`, and this review.

## 2. Executive verdict

X02's **core engineering reproduction is substantially correct**: the exact charge arithmetic, conductance/groove behavior, single-winner channel selection, duplicate hostage formulas, expression-rate ratchet, buffer/route non-coupling, event-context absence and pre-route transaction residue all reproduce at sourcefree grain. The 82-test count is correct.

Three **precise revisions** are required:
1. **Source-provenance wording:** 10 of X02's 19 inspected files are in the S50 manifest; 9 are not. “31/31 exact” is true for the S50 manifest, not for all X02-inspected files.
2. **F3 broad history claim:** grooves do not select channels, but **route history can change next-cycle channel selection** through wound/spiritual scalar changes. X02's broad “history changes conductance/labels, not channel selection” is too strong; the groove-specific claim survives.
3. **F5 evidence/wording:** the pinned X02 transaction probe changes `affect_channel`/`baseline_load` only; `expression_rate`/`expressed_aim` are written pre-route but unchanged in that probe. A tailored high-hostage/low-energy state shows all four can survive failure. Also, the source promises transactional **route-object** commit, not whole-cycle atomicity; “partial transaction” should be scoped precisely.

Additional independent source defects found:
- **Zero-as-missing coercion:** `or 50/80` converts legitimate 0 values (`expression_rate`, `activation_threshold`, `vitality`, `inner_load`, `spiritual`) to defaults. X02's ratchet probe sets `activation_threshold=0`, but the code silently uses 80.
- **Stale `expressed_aim`:** `apply_expression_gating` skips `load<=0` without clearing `expressed_aim`; a prior 80 survives a zero-load cycle.
- **Docstring/implementation mismatch:** `apply_expression_gating` mentions high coercion, but the code reads only hostage, vitality, inner load, rate and threshold; no coercion value.

**Court result:** ENGINEERING `PASS_WITH_RED_AT_SOURCE_GRAIN`; SCIENCE `PARTIAL_WRONG_MEANING / HOLD`; AUTHORITY `NO_NATIVE_GRANT`. X02's overall “not conserved psychological energy, not multi-stream personhood, no current C9/C12” verdict is correct.

## 3. Per-primary-claim matrix

| X02 claim | Verdict | Core evidence / correction |
|---|---|---|
| F1 charge conservation is bookkeeping | **AGREE_SCOPED** | `flow.py:268-284,406-465`; 81.6/71.6/1.062/76.039 reproduced. Groove 100 gives trace 101.171 > current 81.6; no global conservation. |
| F2 one winner per domain | **AGREE_SCOPED** | `channels.py:190-201`; `DomainState.affect_channel` is one `str`; no secondary vector. Historical memory stores aggregate totals, not simultaneous recruitment. |
| F3 grooves raise conductance but not selection | **AGREE for grooves / REVISE_PRECISE for history** | Groove 0→100: conductance 1.062→1.413, same channels. But a route cycle followed by the next default cycle can flip `body_self` `somatic_irritability`→`quiet_organizing` after route raises anger/spiritual scalars. |
| F4 scalar/categorical writes, no relation rewiring | **AGREE_SCOPED / REVISE_PRECISE wording** | `flow.py:500-544` writes values/labels only; no learned relation/edge/scope. But fixed regime switches exist (`frameworks.py` acute→chronic by tenure; topology hysteresis; conspiracy categorical). “No function change” is too broad; “no learned relation/edge/scope” is correct. |
| F5 pre-route mutations survive route failure | **AGREE_FINDING / REVISE_EVIDENCE** | Route objects are deep-copied; pre-route writes occur before `_simulate...` (`flow.py:753-805`). Pinned probe changed `affect_channel`/`baseline_load`; tailored high-hostage/low-energy case changes all four. Existing transaction test disables pre-route steps. |
| F6 duplicate hostage index | **AGREE_SCOPED** | `derived.py:34-58` weights sum 1.0; `gating.py:61-71` weights sum 2.15; same state 17.0 vs 35.2. Source conflict; owner must declare authority. |
| F7 expression-rate ratchet | **AGREE_SCOPED** | `gating.py:152-188`; 100→30→9→2.7 reproduced; no reset assignment in inspected code. Intended/recovery remains an owner decision. |
| F8 buffers/fatigue mostly readouts/costs | **AGREE_SCOPED** | Buffer 0 vs 100 leaves charge/conductance/trace identical; buffer strength affects insulation score/metadata/vitality readouts, not route. No standard `Buffer` seeding. |
| F9 event semantics absent | **AGREE_SCOPED** | `flow.py:203-226` counts types only; charge/route/memory ignore event content. Label/ID-only change leaves charge/trace/memory identical; history event_context may still record type counts. |
| F10 no current Sorok integration proven | **AGREE_SCOPED / HOLD** | No current `v3.psyche.flow` import was located in the reviewed target and available HEAD return trees; the S50 historical fixture is separate and its actual root remains held. This is not proof of global absence. |
| Source identity 19 files / S50 31/31 | **REVISE_PRECISE** | 19/19 local+zip exact; 31/31 S50 selected exact; only 10/19 X02 files are in S50. Fix the sentence in `00_RETURN`. |
| 82 focused tests passed | **AGREE_COUNT / REVISE_RECEIPT** | Reproduced 82 with the 17 grouped files. Log is aggregate only; no per-test names/individual receipts. Coverage gaps below. |

## 4. Detailed claim review

### F1 — “Charge” is per-domain bookkeeping, not a psychological conservation law
**AGREE_SCOPED.** `_derive_current_charge` (`flow.py:268-284`) computes `baseline_load × (0.90+inner_load/500) × (0.92+wound_mean/625)`. `_domain_charge_ledger` (`406-465`) sets `overt=min(expressed_aim,current)`, `internal=current-overt`, `trace=internal×conductance`. Reproduced exactly: 80/60/50 → current 81.6; overt 10; internal 71.6; conductance 1.062; trace 76.039; `overt+internal=current`.
The stronger fact: with a 100-point groove, conductance 1.413 and trace **101.171 > current 81.6**. The source itself calls trace “effect strength, not additional charge” (`flow.py:451-452`) while the module docstring says “internally_routed_charge is conserved charge.” That is a local bookkeeping identity, not a global or psychological conservation law. X02 is correct.

### F2 — One channel per domain
**AGREE_SCOPED.** `_pick_channel` (`channels.py:190-191`) returns a single `max` with fixed priority; `DomainState.affect_channel` is a `str` (`state.py:83`). Tie probe `{humor_irony:10, hyper_competence:10, quiet_organizing:10}` → `humor_irony`; no secondary field. `pressure_flow_memory` stores aggregate dominant/recent channels and lifetime totals, but not a simultaneous current recruitment vector. X02's N04 gap is correct.

### F3 — Grooves vs channel selection, and the broader history claim
**AGREE for grooves.** `assign_sublimation_channels` (`channels.py:194-201`) reads wound/practice/domain scores, not `pressure_flow_memory`; grooves are read only in `_channel_conductance` (`flow.py:366-403`). Groove 0→100: conductance 1.062→1.413; selected channels identical with/without grooves. X02's groove claim is correct.

**REVISE_PRECISE for “history changes conductance/labels, not channel selection.”** Route effects write `wound_vector.anger` (`flow.py:533-535`) and `practice_stack.spiritual` (`512-517`), both of which are inputs to `assign_sublimation_channels` (`channels.py:103-150`). A route cycle with a body-self somatic route followed by the next default cycle flips the body channel:
- before: `body_self = somatic_irritability`; anger 59.0; spiritual 50.0;
- after route: anger 63.008; spiritual 57.728;
- next default cycle: `body_self = quiet_organizing` (all five domains change in the probe).
This is history-dependent channel selection through scalar inputs, not the groove memory. It does not rescue N02/N05/relation rewiring, but X02's broad sentence is false as written. The precise statement should be: **grooves do not select; route history can change selection by changing scalar wound/practice inputs; no learned relation/edge/scope is shown.**

### F4 — Scalar/categorical writes vs relation rewiring
**AGREE_SCOPED.** `_apply_single_domain_route` (`flow.py:500-544`) writes only capacity/psych-capacity/practice/peak/style/wound values; conspiracy sets `peak_routing.theory_of_change_style` categorically. No `active_magnets`, `strata_salience`, relationship edge, access rule or framework mapping is created/changed by pressure-flow route.
**REVISE_PRECISE wording:** “No operator changes another component's function” is too broad. `frameworks.py:60-108` switches framework acute→chronic by tenure; `topology.py` uses hysteresis to change `loop_topology`; the conspiracy route changes a categorical theory label. These are fixed regime/label switches, not learned relation rewiring. The defensible claim is “no learned relation/edge/scope transfer,” not “no function change.”

### F5 — Route transaction vs pre-route mutations
**AGREE_FINDING.** The route objects are applied to a `deepcopy` (`flow.py:547-567`) and committed only after snapshot/memory/surface/analyst construction (`570-573`, `803-805`). But `run_pressure_flow_cycle` runs `assign_channels`, `compute_pressure`, `apply_gating` before that (`753-772`), writing `affect_channel`, `baseline_load`, `expression_rate`, `expressed_aim` live. A forced `_update_memory` failure leaves them behind.
**REVISE_EVIDENCE/SCOPE:** X02's pinned state changes only `affect_channel` and `baseline_load`; `expression_rate` remains 50 and `expressed_aim` 0. A tailored high-hostage/low-energy state changes all four (15 field entries across domains), including `expression_rate 100→15` and `expressed_aim 0→15`. The existing `test_transactional_failure_after_route_projection_does_not_mutate_live_state` disables `assign_channels`, `compute_pressure`, `apply_gating` (`test_v5_pressure_flow.py:113-128`), so it tests route objects only.
**Precise wording:** the source promises transactional **route-object** commit, not whole-cycle atomicity. “Partial transaction” is a scope characterization, not a broken all-cycle promise. Owner should decide whether pre-route writes should be included.

### F6 — Duplicate hostage index
**AGREE_SCOPED.** `derived.compute_hostage_index` (`derived.py:34-58`) uses v3config weights dependents .25, housing .20, legal .15, debt .15, job .15, care .10 (sum 1.0). `gating._derive_hostage_index` (`gating.py:61-71`) uses housing .35, legal .25, dependents .60, debt .30, job .30, care .35 (sum 2.15). The state used by X02 gives **17.0 vs 35.2**; the private gating formula can saturate much faster. `apply_expression_gating` uses the private formula; `compute_all_derived`/registers use the canonical one. This is a real semantic conflict. Whether it is a “bug” or an intended separate gate is an owner decision; no canonical authority is declared in source.

### F7 — Expression-rate ratchet
**AGREE_SCOPED.** `apply_expression_gating` (`gating.py:152-188`) multiplies the stored `expression_rate` by .3/.6 (hostage) and .5/.75 (energy); `compute_baseline_load` preserves the value (`gating.py:148`). Probe: 100→30→9→2.7 under constant high hostage; no reset/recovery assignment was found in the inspected code. This is a persistent multiplicative gate, not documented as memory or learning. The additional zero-coercion defect (below) matters: a legitimate `expression_rate=0` is converted to 50 before use.

### F8 — Buffers, insulation, vitality
**AGREE_SCOPED.** `_channel_conductance` reads raw vitality/agency/aperture, not buffer strength or `derived.insulation_score`; `_apply_single_domain_route` does not read buffers. Buffer 0 vs 100 leaves charge/conductance/trace identical. Buffer strength does affect `compute_insulation_score` and thus insulation/vitality **metadata/readouts** (`derived.py:78-83`, `vitality.py:92`, `insulation.py:72-147`), and buffer costs pay capacity in `buffers.py:45-70`; it is not route-causal. `identity_to_backbone` seeds `buffer_type` labels, not `Buffer` objects; `state.buffers` is empty on the standard path. X02's “mostly readouts or costs” is fair.

### F9 — Event semantics
**AGREE_SCOPED.** `_compact_event_context` (`flow.py:203-226`) counts event/micro-trace types; `_derive_current_charge`/`_domain_charge_ledger`/route/memory do not read `event_context`. Label/ID-only change leaves charge/trace/memory identical. The snapshot/history does record type counts; if an event has no `type`/`event_type`, the id fallback can change the history context, but still not the causal route. X02's N03/N08 gap is correct.

### F10 — Current integration
**AGREE_SCOPED / HOLD.** X02's evidence is historical V3; no current C9/C12 consumer was traced. A search of the reviewed target tree and available HEAD return trees found no current `v3.psyche.flow` import; the S50 historical fixture is a separate held source and its actual root remains a source-owner hold. This supports X02's ceiling but is not proof of universal absence. Owner: incumbent Sorok implementation/HQ; separate current-consumer commission.

## 5. Source identity and 82-test receipt

- 19/19 X02 files local exact; 19/19 top-level zip exact; 31/31 S50 selected exact; 9/19 not in S50. X02's file hashes are sound; the `00_RETURN` sentence conflates “S50 31/31 exact” with “all inspected files are in S50.” **REVISE_PRECISE** that sentence. The source_identity.json itself is closer to correct.
- 82 tests reproduced in **11.28s** with the 17 grouped files; `logs/pytest_x02_original_v3.log` at the target reports 82 passed in 6.94s. The target log is aggregate dots only; it does not list test names or individual assertions. **AGREE_COUNT / REVISE_RECEIPT_GRANULARITY.**
- Coverage gaps confirmed by reading the tests:
  - transaction test disables pre-route steps (`test_v5_pressure_flow.py:113-128`);
  - groove test checks conductance, not channel selection (`131-148`);
  - no test for duplicate hostage equality;
  - no repeated-cycle ratchet/recovery test;
  - no multi-stream/simultaneous recruitment test;
  - no buffer-route causality test;
  - no event-semantics causal test;
  - no categorical trace audit test;
  - no default pre-route transaction failure test;
  - no current C9/C12 integration test.
  The 82 tests are historical fixture/arithmetic/surface tests, not proof of developed personhood.

## 6. Independent additional defects

These are not required to falsify X02, but they are material source defects found during review:

1. **Zero-as-missing coercion.** `gating.py:148,160,161,169,185` uses `getattr(..., default) or default`; legitimate `expression_rate=0`→50, `vitality=0`→50, `inner_load=0`→50, `activation_threshold=0`→80. `channels.py:112` does the same for `spiritual=0`→50. Probe: zero values become 50/80. X02's ratchet probe sets `activation_threshold=0`, but the code silently uses 80; `expressed_aim=0` is not purely a rate effect. This can invalidate any claim about zero gates or zero inner load.
2. **Stale `expressed_aim`.** `apply_expression_gating` `continue`s when `load<=0` (`gating.py:164-167`) without clearing `expressed_aim`. Probe: prior expressed_aim 80 survives a later zero-load cycle (baseline_load 0, expressed_aim 80). This is a state residue/no-change defect not covered by X02.
3. **Coercion docstring/implementation mismatch.** `apply_expression_gating` docstring (`gating.py:153-157`) says “High coercion → avoid overt defiance,” but the function never reads `coercion`; it uses `_derive_hostage_index`, vitality and inner load. Coercion affects `baseline_load` via strata, not the expression gate.
4. **`_derive_hostage_index` weights sum 2.15**, not 1.0; the private gate saturates much faster than the v3config-derived index. X02 notes the duplicate; this is the quantitative reason.

## 7. Positive, NO_CHANGE and severed-edge evidence

**Positive (sourcefree arithmetic grain):** groove 0→100 raises conductance 1.062→1.413 and trace 76.039→101.171; this is a real, deterministic source edge. It is **not** a C9/C12 consumer-positive and does not establish a psychological law.

**NO_CHANGE:** the old code has no typed `NO_CHANGE` object. A zero-load/`route_internal_charge=False` cycle still records history/memory/surface; a zero-baseline domain can retain stale `expressed_aim`. This is bookkeeping/absence, not an admitted no-change decision. X02's proposed typed NO_CHANGE remains **NOT_EXECUTED** and must be issued by the competent rule owner.

**Severed-edge negative (executed):** removing the groove memory (0 vs 100) changes conductance/trace while leaving channel selection unchanged; removing the relational-field status changes conductance in the existing relation test. These are arithmetic/mediating edges, not semantic C9/C12 edges. A semantic severed-upstream edge (event access/expectation/relationship) is **NOT_EXECUTED** because no current consumer exists. The required future test is: actual E1 access/expectation/support → typed operation → E2 reads it; no-access/support-withdrawn E1 → explicit NO_CHANGE; label/hash-only E1 → no E2 change.

## 8. Separate courts

### ENGINEERING
`PASS_WITH_RED_AT_HISTORICAL_SOURCE_GRAIN`.
- Reproduced X02's arithmetic, groove, single-winner, duplicate hostage, ratchet, buffer, event absence and transaction residue.
- 82/82 historical tests reproduced.
- REDs: source-provenance wording (9/19 not S50); broad F3 history claim; F5 evidence scope/transaction wording; F4 overbroad “no function change”; aggregate-only test receipt/coverage gaps; zero-as-missing coercion; stale expressed_aim; coercion docstring mismatch; duplicate hostage semantic conflict; ratchet; categorical trace omission; pre-route residue.
- No current C9/C12 integration.

### SCIENCE
`PARTIAL_WRONG_MEANING / HOLD`.
- The old module is a scalar accounting/hydraulic membrane. It does not establish conserved psychological energy, simultaneous recruited channels, scoped relational memory/access, event impression/appraisal, durable CAN011 change or repair. X02's science verdict is correct.
- The route-history selection counterexample means the old machine has more history-dependent **selection** than X02's broad sentence credited, but it is still selection through global scalar inputs, not a scoped relation. This does not rescue N02/N04/N05.
- Required owner: CAN008 R2 concrete impression rule, CAN011 target/transition rule, ADP015/016/017/019 effects/access; not RX02.

### AUTHORITY
`NO_NATIVE_GRANT`.
- Original V3 is historical read-only. No native actor/source/rule/C8/C9/C11/C12/Pyat/human permission was used or inferred.
- Current C12 person/consumer remains unproven; S50 actual root remains held. Archive-wide identity remains a source-custodian HOLD; file-level identities are exact.
- No production implementation, source edit, review adoption or PR merge.

## 9. Remaining defects / next actions

| Defect/gap | Owner | Next evidence |
|---|---|---|
| Source-provenance sentence conflates 19 X02 files with S50 31 | X02 author / source custodian | Correct wording; keep 31/31 S50 and 9 additional local/zip exact distinct. |
| Broad “history does not change channel selection” | X02 author / V3 science owner | Correct to groove-specific claim; add route-history selection counterexample. |
| F5 pinned evidence only two pre-route fields; transaction scope wording | X02 author / V3 implementation owner | Add tailored default failure test; distinguish route-object transaction from whole-cycle atomicity. |
| F4 “no function change” overbroad | X02 author | Narrow to “no learned relation/edge/scope”; list fixed regime switches. |
| Zero-as-missing coercion | V3 implementation/verifier owner | Add zero-value tests; decide whether 0 is valid; fix `or` defaults. |
| Stale expressed_aim on zero load | V3 implementation owner | Add zero-load/no-change test; decide reset vs explicit no-change. |
| Coercion docstring/implementation mismatch | V3 implementation owner | Correct docstring or implement the claimed coercion gate under an issued rule. |
| Duplicate hostage index | V3 implementation/science owner | Declare canonical formula or keep two explicitly named indices; add differential test. |
| Expression-rate ratchet | V3 implementation/science owner | Decide recovery/reset; if intended, issue rule and test. |
| Categorical trace omission | V3 implementation owner | Include categorical effects in audit or document audit as numeric-only. |
| Current C9/C12 integration | incumbent Sorok HQ/implementation owner | Separate current-consumer commission; no sourcefree fixture promotion. |

## 10. Return/remote

This review is committed only at `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/REVIEW_COURTS/RETURNS/RX02/` (including supporting `TEST_SOURCE_AND_LOGS/`). The final artifact/remote SHA is reported after push and `git ls-remote` readback in the handoff response and `REMOTE_READBACK.json`.

**No self-adoption. No implementation. No native grant.**
