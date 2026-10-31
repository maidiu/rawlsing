# Compatibility architecture and priority

## 1. Decision

`RECOVER_CORE_AND_ADAPT__DO_NOT_MERGE_OLD_ENGINE`.

The archive supplies a usable **state/derived/scheduler/flow/render skeleton**. It does not supply a current C9/C12/A0 engine, native rule, or valid psychology. The first implementation should be a narrow adapter around the portable core; a new psyche engine would duplicate working historical code and create a second unqualified authority.

## 2. Portable historical core

| Priority | Module | Keep | Why |
|---|---|---|---|
| P0 | `v3/core/state.py` (`BackboneState`, `YearRecord`) | data containers, IDs, provenance slots | persistent state is real; fields are not canonical C9/C12 law |
| P0 | `v3/core/derived.py` (`compute_all_derived`) | stored-vs-derived separation | test `test_no_derived_fields_in_backbone_state` passes |
| P0 | `v3/core/year_record.py` | year/replay record | selected source hash matches TD-R05 |
| P1 | `v3/v3_yearly_step_order.yaml` + `v3/engine/yearly_step.py` (`run_one_year`) | dependency spine, fail-fast order | 19-step core spine is real; mutation kills the named assertion |
| P1 | `v3/engine/step_runner.py` (`run_n_years`) | multi-year driver | usable slow-time layer only |
| P2 | `v3/psyche/flow.py` (`run_pressure_flow_cycle`, `_domain_charge_ledger`, `_channel_conductance`, `_update_memory`) | transactional membrane, history/memory, analyst/surface split | 24 selected pressure-flow tests pass; charge is not a conserved psyche substance |
| P2 | `v3/psyche/vitality.py`, `v3/psyche/insulation.py` | bounded derived profiles | part of flow evidence, not native kinds |
| P3 | `v3/render/phenomenology.py` (`render_year`) | render-only nonmutation | `test_llm_no_backbone_mutation` passes |
| P3 | `v2/conversation_engine.py` (`prepare_conversation_turn`) | V2 surface consumer | one-way V3→V2 membrane; no C9 writer |
| P4 | `v3/core/invariants.py` | fail-fast limits, degraded diagnostics | exclude placeholder **repair**; keep assertion/telemetry |

M37 structural stubs remain quarantined: the archive’s persona-sheet and distillation exclusions are the correct treatment. M38 fail-fast equality is retained. M40 clean/degraded/blocked readiness is retained as a product/engine readiness check, not native science.

## 3. Required compatibility adapters

1. **State adapter** — map `BackboneState` fields to exact actor/world/event/access identities and C9/C12 owner records. Do not treat the large heterogeneous dataclass as canonical state. Preserve field provenance, scope and uncertainty.
2. **Derived adapter** — expose `DerivedIndices` as computed projections only. No derived value may be persisted as actor history or used as a source rule.
3. **Slow-time/event-time adapter** — keep M25 `run_one_year` as optional slow-time annual projection. N11 owns 3–5 event batches and N/N+1 two-call interaction. Expose explicit `schedule_mode`; never infer an event from an absent LLM proposal.
4. **Flow membrane adapter** — map multi-interpressure inputs to the old charge/conductance ledger only after scientific owner approval. Remove universal coefficients and the “one winning channel” interpretation; retain transactional history/memory and analyst/surface separation.
5. **C9/C12 consumer adapter** — only after owner selection. Current BP2P4J/R31J are distinct cuts; `R31JProduct`/`JoinedProduct` do not import old V3. An adapter must consume a real C8 occurrence/actor-access receipt, not a legacy `BackboneState` blob.
6. **Provenance/access adapter** — preserve objective event vs actor access vs memory vs helper/tool; no “charge” and no invented motive.

## 4. N11 / M25 / 101 coexistence

- **M25 (old):** config-driven 19-step annual spine; `run_one_year` advances year/age and runs pressure-flow post-year. It is a slow-time scheduler, not an event batch.
- **N11 (required):** 3–5 conditional events, sequential resolution, no ordinary LLM calls between events; call N+1 first-half retrospective memory/meaning, second-half next batch.
- **101 two-call (current Sorok):** first/second half interaction; not the old Pass 1/Pass 2 LLM contract.
- **Versioned coexistence:** expose `schedule_mode = ANNUAL_SLOW_TIME | EVENT_BATCH_3_5 | MIXED_DECLARED`; require an explicit bridge object with world/actor/observer clocks. M25 may project a year only after the event batch’s actual state changes; it must not create missing events or multiply learning by age.

## 5. Current BP2P4J / R15 comparison

- Current BP2P4J `JoinedProduct`/`R31JProduct` at `5b3e657…`/`64fec28c…` are sourcefree material/action/C12 consumers. They are not old V3 call sites.
- Old V3 `BackboneState` is not a C12 actor record; `compute_all_derived` is not a C9 semantic receipt; `render_year`/`prepare_conversation_turn` are V2 surfaces.
- Current Pyat R15 execution apparatus is a separate source/qualification path; it is **not** old V3 R15 or M25. No cross-cut acceptance is borrowed.
- **Selected initial downstream consumer proposal:** a narrow state/derived adapter feeding the current `R31JProduct` p01 material/action test path, with tests `test_g17_material_history_consumer.py` and `test_g17i_independent.py`, only after owner approval. Current actual first consumer of old V3 remains the historical `run_one_year`/`run_pressure_flow_cycle` test harness; current product consumer **NOT PROVEN**.

## 6. Quarantine / remove

- M08 identity-seeded wound; M15/M36 missing-parent defaults and hopeful/50-50-50; M34 fallback event; M35 placeholder cracks/frameworks; M39 random age-band rupture; M31 type-determines-person; `personality_assigned_from_parent_profile`/type labels.
- M37 stub years must not become scenes or memories; only the accounting/quarantine remains.
- Remove age-as-development multiplier, universal “charge,” fixed winning channel, and any fabricated no-change.

## 7. Rollback / why-not alternatives

- **Why not direct import:** field schema, actor/world provenance, C9/C12 source cuts, invalid defaults/placeholders and render/LLM contracts are incompatible.
- **Why not new engine:** the state/derived/scheduler/flow skeleton is already present and tested; a replacement would duplicate it and lack original-source continuity.
- **Rollback:** keep the archive read-only; adapters are feature-flagged and independently tested; if adapter tests fail, return to source analysis/HOLD without merging or deleting the archive. No native adoption.

## 8. Owner decisions

1. Original V3/V2 owner approves the portable core and quarantine list.
2. Neo N01–N12 owners determine which requirements the old mechanisms may serve and which need new science.
3. CAN/ADP/CAN011/ADP016/017 owners decide whether the adapted state/flow can enter their jurisdictions.
4. C9/C12/A0 consumers select the first real downstream interface.
5. Incumbent HQ and a separate reviewer approve any adapter; no self-adoption.
