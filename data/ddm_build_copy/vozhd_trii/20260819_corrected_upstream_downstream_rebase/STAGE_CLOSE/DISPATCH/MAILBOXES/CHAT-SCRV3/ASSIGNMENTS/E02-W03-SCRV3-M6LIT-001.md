# E02-W03-SCRV3-M6LIT-001

Status: `ISSUED`
Worker slot: `3`
Permanent chat ID: `CHAT-SCRV3`
Most recent submitting agent ID: `SCRV3`
New worker class: `SUB-VOZHD`
New agent/unit ID: `SCRV3_M6_HANDOFF_LITERALIZATION`
Authority: `NARROW_SCRV3_OWNED_INTERFACE_COMPLETION_ONLY`

Repository: `maidiu/rawlsing`
Exact semantic launch base: `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`
Mission branch: `agent/vozhd-trii-dr-r03-seam-v3-m6-handoff-literalization`
Branch precondition: branch must be exactly identical to the semantic launch base before writing.
Write ONLY under:
`data/ddm_build_copy/vozhd_trii/20260819_corrected_upstream_downstream_rebase/STAGE_CLOSE/SEAMS/V3_M6_HANDOFF_LITERALIZATION/`

## Binding authorities

- SCRV3 exact contract blob `f7f4b6a004e09f7297fdcec459efc3125d6a598a` (`V3EmpiricalPossibilityInput@1.1.0`).
- SCRV3 result blob `64d048d3b8e571acc885bfeb4d4bb70c013f85fe`, token `SCRV3_WAITING_ONLY_FOR_EXACT_FINAL_SEAM`.
- SCRV3 seam handoff blob `61f03d413d2d54681d5bc60bc87972cae5bc704a`.
- ADP-017 / `V3_ACTOR_KNOWLEDGE_ACCESSIBILITY_RULE@1.0.0` exact authority blob `eece4f3f2f3f9288ab9bbc645dc81e20a99e1280`, accepted owner binding commit `614775fa05c5d904adff4b53f353637b869e6842`.
- SCRV2APP accepted head `24f8811bb7d2eaa18cfac1cb907c48bba8d08f23`; its negative firewall/local receiver contract remains frozen.
- M6 preflight token `M6_PREFLIGHT_COMPLETE`, RESULT blob `42ddcb56c6134f900da684bcd48af7c007921d3d`.
- Command Review 01 disposition: `NARROW_SCRV3_M6_HANDOFF_LITERALIZATION_REQUIRED`; no broad SCRV3 causal-contract reopening.
- Parent authorities 24/25 and accepted R03 broad topology remain binding.

## Mission

Complete only the exact machine literals required to make the already-governed ADP-017 `ActorAccessibleRenderEnvelope` consumable by final M6 without inference.

Freeze, from existing accepted semantics rather than invention:

1. exact `ActorAccessibleRenderEnvelope` schema/type version;
2. exact deterministic envelope identity and content-hash serialization rule, including which fields are identity-bearing and canonical serialization requirements;
3. exact actor binding and source V3 state/memory/epistemic hash binding;
4. exact `as_of_causal_time` / currentness relationship;
5. exact currentness/invalidation predicate: when a previously valid envelope becomes stale after relevant V3 state/accessibility/memory/epistemic changes;
6. exact terminal receiver-visible mapping for: no renderable entries, explicit deny, defer/missing authority, stale envelope, integrity failure, and partial accessibility;
7. exact first-person permission vocabulary and non-widening rule already owned by ADP-017;
8. exact handling of actor-perceived relationship views and component-scoped partial accessibility;
9. exact opaque-provenance audit-only/reference shape and raw-upstream exclusion surface;
10. exact replay-reference closure sufficient to reproduce envelope identity/hash and detect stale/integrity failure.

The task is literalization/interface completion only. If any required literal cannot be derived from accepted SCRV3/ADP-017 authority without adding new actor semantics, return harmonization/authority conflict rather than inventing it.

Do NOT turn disclosure willingness, situational salience, conversational inhibition, affective foregrounding, interlocutor-specific openness, or V2 phenomenological variability into ADP-017 semantics here. Those are downstream consciousness/phenomenology-expression concerns and are outside this narrow task unless already explicitly required by the frozen actor-accessibility boundary.

## Forbidden

- No production code.
- No broad-topology amendment.
- No rewrite of the accepted SCRV3 causal/input/metabolism contract.
- No new belief, memory, knowledge, relationship, persona, affect, or disclosure semantics.
- No raw PSEPF/RSC/repository/analyst truth in actor-safe payload.
- No V2 permission widening.

## Required outputs

- `RESULT.md`
- `RESULT.json`
- `ACTOR_ACCESSIBLE_RENDER_ENVELOPE_EXACT_CONTRACT.md`
- `ACTOR_ACCESSIBLE_RENDER_ENVELOPE_EXACT_CONTRACT.json`
- `TERMINAL_STATE_MAPPING.csv`
- `CURRENTNESS_INVALIDATION_CONTRACT.md`
- `M6_HANDOFF.json`
- `HOSTILE_TEST_ORACLE.md`

Return exactly one finite token with the exact mission head SHA:

- `SCRV3_M6_HANDOFF_LITERALIZATION_COMPLETE`
- `SCRV3_M6_HANDOFF_LITERALIZATION_RETURN_FOR_HARMONIZATION`
- `SCRV3_M6_HANDOFF_LITERALIZATION_AUTHORITY_CONFLICT`
- `BROAD_TOPOLOGY_CONTRADICTION_FOUND`
