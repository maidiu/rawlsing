# SOROK V3CORE-R1 — scientific quarantine and authority holds

## Authority statement

This return is **TEST_ONLY_SOURCEFREE**. It issues no CAN, ADP, SCI05, CAN011,
ADP016/017 or other developmental-science rule. It does not claim a native
person, native source, native C9/C12 actor, original-author identity, Pyat N11
world, or canonical Sorok actor. It does not self-review or self-adopt.

The historical V3/V2 source is a donor of computational mechanism. The adapter
keeps the state/derived/scheduler/transaction/render/readiness skeleton and
refuses the historical defaults that manufacture psychological content.

## Quarantine table

| Mechanism | Exact historical source | SHA-256 prefix | Why excluded | Active path |
|---|---|---|---|---|
| M08 identity-seeded wound | `v3/psyche/channels.py::seed_wound_vector_from_identity` | `2d00bf6b8720879e` | Class, minority status, religiosity and age cannot manufacture wound sensitivity. | `EXCLUDED_FROM_ADAPTER`; `wound_vector` zeroed and marked `QUARANTINED_UNSET`. |
| M15/M36 missing-parent 50/50/50 | `v3/io/parent_baseline_from_behavior.py` | `4e5be6448a5b76c4` | Unknown care cannot be converted to a midpoint baseline. | `EXCLUDED_FROM_ADAPTER`; no parent baseline is read. |
| M15/M36 hopeful default | `v3/engine/expectation_baseline.py` | `632e1e608bfc674a` | An unobserved need axis cannot be seeded `hopeful`. | `expectation_baseline` stays empty; any value blocks the year. |
| M31 Enneagram/type determinism | `v2/parent_type_inference.py::infer_parent_type_most_likely` | `b05632d01c48f52a` | Type inference is not an issued developmental rule and cannot determine the person. | `child_model` refuses `enneagram`/`personality_type`/`type`. |
| M34 synthetic fallback practice | `v3/engine/llm_contract.py` | `f024debf7b8a637e` | An empty candidate packet is not a lived year. | `EXCLUDED_FROM_ADAPTER`; no fallback event can be admitted. |
| M34 first-candidate fallback | `v3/engine/run_llm_band.py` | `120e177462219e8c` | Selecting the first candidate when scoring selects nothing fabricates occurrence. | `EXCLUDED_FROM_ADAPTER`; only actual source event records enter. |
| M35 placeholder cracks/frameworks | `v3/core/invariants.py::ensure_min_cracks/ensure_min_frameworks` | `81298f3fc51b46cd` | Placeholders are not lived content; degraded diagnosis is preserved, repair is not executed. | `EXCLUDED_FROM_ADAPTER`; `cracks`/`frameworks` remain empty. |
| M39 random age-band rupture | `v3/engine/effects/metabolization_effects.py` | `d4775271ca097e99` | Rupture requires an admitted event ledger, not a random age ritual. | `EXCLUDED_FROM_ADAPTER`; `rupture_shards`/`metabolization_processes` remain empty. |

`v3core_adapter/quarantine.py` carries the live manifest with full SHA-256
values. `test_quarantine_and_defaults.py` asserts every hash, every mechanism,
the empty fresh state, the rejection of injected defaults, and the module-level
import scan.

## Scientific constraints preserved

1. **Source fact ≠ durable actor state ≠ derived computation ≠ expression.** The
   ledger stores the actual event/access/response; `BackboneState` stores only
   source-grounded material fields; `PublishedDerived` is a separate frozen
   read-only result; `rendered_output` is expression only.
2. **No event, no annual developmental occurrence.** `event_sampling` is actual
   ingress, not sampling. Removing an event yields
   `HELD_SOURCE_EVENT_WITHDRAWN`; an empty year yields `HELD_NO_EVENT_SOURCE`.
3. **Three clocks stay separate.** `CURRENT_C12_ACTOR_WORLD_CLOCK` is accepted
   only through an explicit `V3_M25_ANNUAL_SCHEDULE` annual binding. Sorok Neo
   N11 event recursion and Pyat N11 objective-world acceptance are refused as
   annual events.
4. **No universal conserved psychological charge.** `run_pressure_flow_cycle` is
   available only as an explicitly enabled test probe on a copy; its result is
   labeled `TEST_ONLY_CONSERVED_CHARGE_MODEL_NOT_SCIENCE`. The live state is
   never mutated. Material memory tracks recorded deltas, not charge. The
   historical flow module transitively imports the wound-channel seeder; the
   adapter imports the flow module lazily inside the opt-in probe and never
   calls the seeder.
5. **No identity or class inference.** No ethnicity, religion, class origin,
   minority status, Enneagram, personality type or typography is read by the
   adapter. The first consumer's source is one actual I1 offscreen work event.
6. **No psychological default injection.** A fresh projection zeroes every
   ungrounded field and records its status. A nonzero wound, a hopeful parent
   baseline, a placeholder crack/framework, a random metabolization process, an
   Enneagram key, or a midpoint narration support blocks the year.
7. **No hidden derived mutation.** `compute_all_derived` runs on a deep copy;
   `BackboneState.metabolic_style` and `registers` stay zeroed, and
   `assert_no_derived_fields_in_backbone` passes. `PublishedDerived` is frozen.
8. **No renderer mutation.** The exact historical renderer is used without an
   LLM callback. Any backbone mutation is rolled back and returned as
   `HELD_RENDERER_MUTATION`. The renderer module imports `llm_contract` for its
   optional Pass 2 branch; the adapter never passes `render_packet` or
   `llm_callback`, so `parse_render_output`, the prompts and the synthetic
   fallback never execute. The module-level import scan forbids direct active
   imports of the fallback symbols.

## Typed holds

| Status | Meaning |
|---|---|
| `HELD_MISSING_RULE` | No competent transition rule is registered. |
| `HELD_RULE_NOT_ISSUED` | A scientific rule exists but no CAN/ADP authority issued it. |
| `HELD_MISSING_PERCEPTION` | No actor access record for the bound event. |
| `HELD_MISSING_RESPONSE` | No performed response record. |
| `HELD_FOREIGN_ACTOR` | Event actor differs from the projection actor. |
| `HELD_CLOCK_MISMATCH` | N11/Pyat/foreign clock or mismatched access/response clock. |
| `HELD_CLOCK_BINDING_MISMATCH` | No or wrong explicit annual binding. |
| `HELD_SOURCE_EVENT_WITHDRAWN` | A binding references an absent source event. |
| `HELD_DUPLICATE_EVENT` | Already applied event id. |
| `HELD_ACCOUNTING_MISMATCH` | Recorded material delta and consumer snapshot disagree, or event is unowned. |
| `HELD_FORBIDDEN_DEFAULT` | A quarantined default is present; no commit. |
| `HELD_RENDERER_MUTATION` | Renderer changed non-expression backbone state; rolled back. |
| `HELD_DERIVED_MUTATION` | Derived computation changed live state; no commit. |
| `HELD_TRANSACTION_ABORTED` | Atomic ledger save failed; old ledger retained. |
| `HELD_NO_EVENT_SOURCE` | No actual event and the caller did not explicitly admit an empty year. |
| `HELD_NO_ADMITTED_EVENT` | All supplied events were held. |
| `HELD_MISSING_ISSUED_RULE` | One of the 16 unadmitted annual steps. |
| `HELD_CONSERVED_CHARGE_MODEL` | The historical charge-conservation model was not issued. |
| `BLOCKED_AUTHORITY` | A blocking generation/readiness diagnostic. |

`NO_CHANGE_EVALUATED` is a committed, genuinely evaluated test-only result with
zero material delta. It is not the same terminal as `HELD_MISSING_RULE` or
`HELD_RULE_NOT_ISSUED`. The test
`test_evaluated_test_only_zero_is_no_change_not_missing_rule` asserts the
difference.

## Authority holds and owners

| Surface | Hold |
|---|---|
| Original V3/V2 source | Original owner must accept the restricted adapter and the quarantine list. |
| CAN/ADP/SCI05 developmental rules | No issuance. The 16 unadmitted steps remain `HELD_MISSING_ISSUED_RULE`. |
| Sorok HQ / PRE-MAIN | No merge, adoption or branch mutation beyond this return. |
| C9/C12 / I1 | The adapter reads I1's actual event and does not write C12. Durable C9/C12 cold reopen and the external anchor remain owner-held. |
| CP-A5 | No A3-A5 native person; the first consumer is sourcefree and material-only. |
| Pyat N11/N12 | No native world acceptance, no C0 actor input. |
| Independent review | This return is not self-reviewed and is not an approval. |

## What is reusable now

- exact `BackboneState` dataclass and `state_to_dict`/`state_from_dict`;
- exact 19-step step order and derived schedule;
- exact `compute_all_derived` on a copy;
- exact `render_year` with a nonmutation court;
- exact `GenerationIntegrityAccumulator` readiness semantics;
- the historical transactional flow/memory pattern, explicitly quarantined;
- a typed source-record ingress and durable projection ledger.

## What is not established

No full person, no native actor, no issued psychological transition, no
conserved-charge science, no identity-derived trait, no synthetic event, no
placeholder personality, no original-author claim, no canonical C9/C12 store,
no merge, and no independent review.
