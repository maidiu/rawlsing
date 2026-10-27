# M07 — public/private/inner registers: X05 direct-source dossier

**Court:** X05 historical source / material-actor-world bridge. **Evidence grade:** `HISTORICAL_SOURCE_AUDITED`; `CURRENT_INTEGRATION: UNTRACED`; `THEORY: PROPOSED_NOT_ISSUED`; `AUTHORITY: NO_NATIVE_GRANT`.  
**Direct source:** `v3/core/state.py` `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`; `v3/core/derived.py` `e479fc3eba21734752c372742fb2ee247cbdde6a73ac42545dc30b5039301360`; `v3/psyche/gating.py` `4a82c7c91828b87bb61cd651c777159f04b5733e64158f8679a24efcec1ccfc6`; `v3/psyche/flow.py` `6da4effde2b1ccb7c346f73b17632ceee3a7a8c37a63a10f096753d070ab1d3d`.

## 1. Exact as-built map

| Element | Source | Inputs / state reads | Operation | State writes / outputs | Consumers |
|---|---|---|---|---|---|
| `Registers` | `v3/core/state.py:114-123` | `public_expression_gate`, `private_expression_gate`, `inner_load`; default 50 | dataclass; clamp | stored `state.registers` | JSON codec; LLM summary; pressure-flow |
| `compute_registers_from_state` | `v3/core/derived.py:272-319` | psychological `aperture`, `binding`, `vitality`; wound vector; `hostage_index` | `public = clamp(aperture - hostage*0.4)`; `private = clamp((binding+vitality)/2)`; `inner_load = clamp(50 + sum(max(0,wound-50))/4)` | returns `Registers` | `compute_all_derived` writes `state.registers` (`derived.py:334`) |
| `apply_expression_gating` | `v3/psyche/gating.py:152-188` | private `_derive_hostage_index`, `psychological_capacity.vitality`, `registers.inner_load`, per-domain `baseline_load`, `expression_rate`, `activation_threshold` | hostage brake (.3/.6), fatigue brake (.5/.75), multiply rate, set `expressed_aim` if above threshold | `domain.expression_rate`, `domain.expressed_aim` | pressure-flow pre-route (`flow.py:770-772`) |
| LLM exposure | `v3/engine/llm_contract.py:767-776`; `v3/engine/prompts.py:31` | registers | summary includes all three values; Pass-1 prompt tells the LLM low public gate means “exposed but cannot show it” | candidate plausibility only | event proposal |
| Surface posture | `v3/psyche/flow.py:331-335,576-587` | `structural_consideration_gate` from domain `A` label | maps gate to `public/private/inner` posture label | `surface_psyche_profile.domains.*.public_private_inner_posture` | V2 surface context; not the `Registers` values |
| V2/persona exposure | `v3/io/persona_sheet.py`; `v2/run_conversation_chat.py:243-253` | — | **no `registers` key is emitted in the persona sheet**; the V2 loader may copy sidecar `state_final.json` `registers` into `history.metadata["registers"]`, but no V2 consumer of that metadata was found | — | no V2 expression consumer found |

**Defaults and hidden laws.** All three gates default to 50. `inner_load` is computed only from wound excess, not from actual unspoken content; it is a scalar pressure, not a memory or accessible meaning. `public_expression_gate` is derived from `aperture` and the canonical `hostage_index`. `private_expression_gate` is derived from `binding` and `vitality`. These are **analyst/engine constructs**, not actor-accessible content. The old code has no field for “what the actor can say in private but not in public”, only a number.

## 2. What this actually models, and what it does not

The code models **bounded expression gates** that can suppress expressed aim under high hostage/fatigue. It does not model:

- a content-specific secret, taboo, shame, loyalty or danger;
- the difference between what an actor knows, what they can say, and what they will say;
- another person's access (ADP017) or the actor's own fallible access to memory;
- private vs public *audience* with different consequences;
- narrator/analyst knowledge being excluded from actor speech.

The `public/private/inner` posture in the surface profile is **not** the register value: it is a label derived from `structural_consideration_gate` (`flow.py:331-335`). The registers are not emitted in the persona sheet, so V2 chat does not consume them. The only consumers are the LLM Pass-1 summary and the pressure-flow expression gate.

`apply_expression_gating` has three source defects:
1. **Zero-as-missing:** `getattr(..., 50) or 50` and `getattr(..., 80) or 80` convert legitimate `expression_rate=0`, `vitality=0`, `inner_load=0`, `activation_threshold=0` to defaults (`gating.py:160-162,169,185`).
2. **Stale expressed aim:** if `baseline_load <= 0`, the function `continue`s without clearing a previously nonzero `expressed_aim` (`gating.py:164-167`).
3. **Coercion mismatch:** the docstring says “high coercion → avoid overt defiance”, but the function never reads coercion; it uses the private hostage index, vitality and inner load.

## 3. Coverage and disposition

| Target | Coverage | Reason |
|---|---|---|
| N04 multiple interpressures (adjacent) | `INFRASTRUCTURE_ONLY` | one gate per register; no simultaneous recruitment |
| N07 independent others/power/love | `INFRASTRUCTURE_ONLY` / `PARTIAL_WRONG_MEANING` | gates exist, but no audience/other actor/access relation |
| N09 fallible memory/meaning | `INFRASTRUCTURE_ONLY` | no memory or access model; inner load is a scalar |
| N12 actual C12 person | `INFRASTRUCTURE_ONLY` | no current C9/C12 consumer; not in persona sheet |

**Disposition: ADAPT.** Keep the three named gates as a derived **access/expression view** under an explicit owner. Remove the private hostage formula, zero-as-missing defaults, stale expression and the false coercion claim. Create an actor-access envelope (ADP017) and a real audience/relation record; V2 may render expression but may not author hidden memories or analyst knowledge.

## 4. Harmful defaults / defects to remove

1. **Default 50 for all gates** even when unknown; a mid gate is not evidence of access.
2. **`inner_load` = wound excess only**; no content, target, audience or memory.
3. **Private hostage formula** (sum 2.15) differs from canonical; can saturate.
4. **Zero-as-missing** and **stale expressed aim**.
5. **Docstring claims coercion gating that does not exist.**
6. **Registers stored as derived** (also M26) and **not emitted** to the persona/V2 surface; actual consumer is only the LLM summary.
7. **Surface posture label is not the register**; do not treat it as actor access evidence.

## 5. Proposed typed seam (nonissuing)

```text
ActorAccessEnvelope {
  actor_id; content_ref; audience_ref; relation_ref;
  can_know; can_recall; can_say_public; can_say_private;
  cost_if_said; source_event_refs[]; evidence; unknown;
}
ExpressionGateView {
  actor_id; public_gate; private_gate; inner_load;
  dependencies[]; source_refs[]; rule_version; computed_at;
}
```
The envelope is the actor-side permission/access record; the gates are derived views. V2 receives only the content the access envelope permits. A narrator or analyst ledger cannot create a memory, a secret, or a causal impression.

**Owner:** ADP017 (epistemic access), ADP016 (memory), CAN010/CAN011 (state), V2 (render), current C9/C12 (consumer). **Not issued by X05.**

## 6. Counterexamples and hostile alternative

**Counterexample (same gate, different access).** Two actors both have `public_expression_gate=30`; one has a dangerous political secret, the other is simply reserved. The old register cannot distinguish them. A later C9 event about state surveillance should treat them differently; the old gate cannot.

**Counterexample (V2 does not read registers).** The persona sheet has no `registers` key; changing the registers changes the LLM Pass-1 summary but not the V2 chat prompt. A test that only checks the persona sheet cannot show expression gating.

**Hostile alternative.** The observed expression difference may be produced by the V2 voice schema or by the LLM's own narrative, not by the registers. A hostile test holds the V2 prompt/voice schema fixed and changes only `state.registers`; if the chat output does not change, the registers are not a V2 consumer.

**Falsifier.** If two states with identical access envelopes but different gate scalars produce different semantic later reads, the scalar is being used as content. If identical envelopes produce no difference while gates differ, the old gate is decorative.

## 7. Tests and limits

- Historical tests read: `test_phase3_activation_gate.py` (gating arithmetic); `test_llm_contract.py` (summary includes registers); `test_v5_pressure_flow.py` (inner load).
- **NOT_RUN:** full old suite; V2 end-to-end chat; current C9/C12; native person.
- **No native rule or source permission is issued.**

**Required future reviewer:** independent V3 source/consumer reviewer for M07/N09; ADP017/ADP016 owners for access/memory; V2 render owner; current C9/C12 implementer. X05 does not self-adopt.
