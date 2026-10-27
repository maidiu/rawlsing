# M30 — V3-under-V2 nonmutation / one-person architecture: X05 direct-source dossier

**Court:** X05 historical source / material-actor-world bridge. **Evidence grade:** `HISTORICAL_SOURCE_AUDITED`; `CURRENT_INTEGRATION: UNTRACED`; `THEORY: PROPOSED_NOT_ISSUED`; `AUTHORITY: NO_NATIVE_GRANT`.  
**Direct source:** `v3/V3_UNDERLIES_V2_ARTICULATION.md` `5a0f11276a830b959df72653016ca77848dbd81de4adb9fa641bd4244c4f4ced`; `v3/render/phenomenology.py` `f2f18c1d9ba705212846af41b33cb1dfd2ad986dae4b686873687c2e6d1a653d`; `v3/core/invariants.py` `81298f3fc51b46cda8d72d0db914b672b17b9a35e13004fe59a9b0e29dada5e3`; `v3/engine/effects/metabolization_effects.py` `d4775271ca097e99e615cee19b381a478ad6d90a25051c5fce1b1e0e3c1adb1e`; `v2/conversation_engine.py` `766bee296379f0faadbede55106bcee0123e9563c965d0e28f8806cedea06135`.

## 1. Exact as-built map

| Element | Source | Inputs / reads | Operation | Writes | Consumers |
|---|---|---|---|---|---|
| Design claim | `v3/V3_UNDERLIES_V2_ARTICULATION.md:9-34,67-78` | — | V3 is causal physics; V2 renders phenomenology; no parallel life simulation; Pass 2 render-only | — | architecture intent |
| `render_year` | `v3/render/phenomenology.py:55-156` | state, derived, config, optional render packet/LLM | writes only `state.rendered_output`; Pass 2 parses scene/dialogue | `rendered_output` | year record; persona sheet |
| render nonmutation test | `v3/core/invariants.py:338-343`; `v3/tests/test_architecture_invariants.py:51-67` | state dict minus `rendered_output` | `backbone_hash` before/after render must match | test result | architecture check |
| Persona sheet | `v3/io/persona_sheet.py:579-1001` | state, derived, rendered, identity, parent override | emits identity/current_state/bands/voice/backstory/backbone/rendered_output | persona sheet | V2 loader |
| V2 loader | `v2/run_conversation_chat.py:36-313` | persona sheet + optional `state_final.json`/`derived_final.json` | builds `PersonaHistory`; loads selected V3 metadata (`psychological_capacity`, `wound_vector`, `alienation`, `registers`, `surface_psyche`) | in-memory history | conversation engine |
| V2 context | `v2/spec.py:4946-5104`; `v2/conversation_engine.py:2079-2176` | PersonaHistory | builds identity/backstory/voice/life-state prompt; no V3 write-back found | prompt | reply LLM |
| **NarrationSupport feedback** | `v3/engine/effects/metabolization_effects.py:445-575` | **previous `state.rendered_output` text** | counts warm/coercive/accuracy words; derives `NarrationSupport`; uses it to choose metabolization mode and alter psychological capacity / downstream biases | `state.narration_support`, `state.psychological_capacity`, process mode/bias | next-year V3 steps |
| Parent narrative | `server/generation/simulation.py:350-475`; `v3/io/persona_sheet.py:470-520` | LLM parent-narrative calls | inserts `parent_birth_context` into persona backstory | persona sheet/V2 prompt | V2 chat |
| Age handling | `v2/run_conversation_chat.py:113-116` | sheet identity age | if age < 17, sets chat age to 35 for the life layer | in-memory `persona_history.identity.age` | V2 life simulation |

**Genuine one-person/nonmutation facts.** `render_year` only writes `rendered_output`; the invariant test proves the backbone hash is unchanged across a render. V2 chat does not directly mutate the V3 `BackboneState` object; it consumes a persona sheet/history. `surface_psyche` is allowlisted and `analyst_pressure_account`/`pressure_flow_history` are excluded from the V2 prompt by `_sanitize_surface_psych` (`v2/conversation_engine.py:214-295`). These are real affordances worth preserving.

**But the boundary is not hermetically one-way.** `update_metabolization_and_plasticity_step` reads the **previous year's rendered scene/dialogue** and derives `accuracy`, `warmth`, `coercion` by word counts (`metabolization_effects.py:445-518`). It then uses that `NarrationSupport` to:
- sample the next metabolization mode (`_sample_mode_from_priors_and_support`, `:91-122`);
- modulate psychological capacity and `downstream_biases` (`compute_metabolization_delta`, `:358-430`);
- influence `is_malheur` through narration availability (`:335-356`).

This is a causal path from V2 narrative prose into V3 psychic state. The text is LLM-rendered, not an independent caregiver event or actor-accessible impression. A scene that uses the word “love” or “must” can change next year's psychological capacity. That is the exact “narrator fabrication” risk the commission asks us to isolate.

**Other one-person risks.**
- `build_persona_sheet` inserts an LLM-generated `parent_birth_context` into the persona backstory (`persona_sheet.py`), which V2 then treats as the person's family story. It is not parent V3 history.
- The persona sheet’s identity fallback “never emit Unknown” substitutes country defaults for religion/ethnicity/language (`persona_sheet.py:618-700`). A missing fact can become a concrete identity.
- `load_persona_sheet_with_integrity` forces chat age to 35 for anyone under 17 (`run_conversation_chat.py:113-116`); a child persona can be rendered with adult life-layer assumptions.
- `build_persona_sheet(include_backbone=True)` includes the full backbone; the V2 loader reads only selected metadata, but the sheet is a raw state carrier and must not be treated as actor-accessible.
- The V3 `NarrationSupport` is stored in `BackboneState` and serialized; it is an analyst/engine construct, not a memory.

## 2. What this actually models, and what it does not

The code models:

- a render-only V3 step;
- a V2 presentation layer driven by a persona sheet;
- a one-person state object with a V2 history wrapper;
- an allowlist that hides raw analyst pressure from the chat prompt.

It does not model:

- a strict information boundary from V2 prose back to V3;
- actor-accessible memory versus rendered narration;
- a grounded parent history rather than an LLM parent story;
- one person across age (the age-17 override is a discontinuity);
- a fallible memory that can misremember without becoming causal truth.

## 3. Coverage and disposition

| Target | Coverage | Reason |
|---|---|---|
| N09 fallible memory/meaning | `INFRASTRUCTURE_ONLY` | render surface exists; no actor memory/forgetting/access; narrator text can enter V3 |
| N10 ideology/cosmology (adjacent) | `INFRASTRUCTURE_ONLY` | V2 can render concepts; no grounded acquisition |
| N12 actual C12 person | `INFRASTRUCTURE_ONLY` | one-person boundary and render-only exist; no current C9/C12 consumer |

**Disposition: REUSE the render-only and one-person jurisdiction; ADAPT/SEVER the narrator feedback.** Preserve `backbone_hash`/`test_llm_no_backbone_mutation`, the surface allowlist, and the separation of analyst accounts. Remove the `rendered_output → NarrationSupport → psychological_capacity` causal edge unless a competent owner explicitly admits a different, source-qualified “narration as care” rule. Do not let LLM parent narrative or country-default identity become V3 fact. Fix the age override or make it an explicit chat contract.

## 4. Harmful defaults / defects to remove

1. **Narrator prose → NarrationSupport → V3 capacity/mode.** LLM word counts become causal care quality.
2. **LLM parent narrative as backstory fact.**
3. **Country defaults for missing religion/ethnicity/language** (also identity integrity).
4. **Age <17 → 35** for chat life layer.
5. **`rendered_output` is serialized in state** and read next year; it is not actor memory.
6. **No typed actor-access envelope.** V2 can see backstory, voice, surface psyche, and sidecar metadata; there is no per-content access proof.
7. **`analyst_pressure_account` exclusion is real but only for the surface allowlist**; the full `state_final.json` is not an actor artifact and must not be passed as one.

## 5. Proposed typed seam (nonissuing)

```text
ActorMemoryEnvelope {
  actor_id; content_ref; event_ref; access (recall/suppress/distort);
  source_ground; reconstructed_at; uncertainty; rule_version;
}
RenderInput {
  actor_id; permitted_memory_refs[]; permitted_state_views[];
  forbidden_analyst_refs[]; age; language; source_hash;
}
RenderOutput {
  scene/dialogue; provenance; claims[]; no_state_write;
}
```
V2 may render only from `RenderInput`. Any V2 text that is later used as causal input must first be admitted as an `ActorMemoryEnvelope`/event with a source, not inferred by word counts. The one-person invariant is preserved by one `actor_id` and one state/derived hash per render.

**Owner:** ADP016/ADP017 for memory/access; V2 render owner; CAN010/CAN011 for any state effect; C9/C12 for consumer. **Not issued by X05.**

## 6. Counterexamples and hostile alternative

**Counterexample (same state, different prose).** Hold V3 state and event history fixed; render two scenes, one with many “love/care” words and one neutral. `update_metabolization_and_plasticity_step` derives different warmth and can change next-year psychological capacity. That is a V2 prose effect on V3 state, not an objective care event.

**Counterexample (parent story).** A parent narrative generated by the LLM is placed in the backstory; V2 treats it as “the story you were born into.” The parent V3 actor may be absent or have a different behaviour record. The old code has no check that the narrative matches the parent state.

**Counterexample (age).** A 10-year-old persona is loaded into chat as age 35 for the life layer; the reply may contain adult work/relationship assumptions. The one-person invariant is broken at the age boundary.

**Hostile alternative.** The observed V2/V3 difference may be due to the selected event or state, not the rendered prose. A hostile test changes only the rendered text while holding state/events fixed and checks next-year V3; if nothing changes, the narrator edge is inert. If it changes, the narrator is causal.

**Falsifier.** Sever the `rendered_output` read in `update_metabolization_and_plasticity_step`; if next-year psychological capacity/process mode is unchanged, the narrator edge was not doing work. If a source-grounded `ActorMemoryEnvelope` produces the same effect while prose word counts do not, the envelope is the legitimate seam.

## 7. Tests and limits

- Historical test: `test_llm_no_backbone_mutation` (`test_architecture_invariants.py:51-67`); it proves render does not mutate the backbone, **not** that rendered text never becomes causal later.
- Tests read: `test_v5_v2_chat_prompt_no_raw_v5_leaks.py` (surface allowlist).
- **NOT_RUN:** full old suite; V2 end-to-end chat; current C9/C12; native person.
- **No native rule or source permission is issued.**

**Required future reviewer:** independent V3/V2 boundary reviewer for M30/N09/N12; ADP016/017 memory/access owner; V2 render owner; CAN010/CAN011 if any narrator effect is retained; current C9/C12 implementer. X05 does not self-adopt.
