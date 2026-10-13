# RFA-06C — post-generation referent admission contract R2

**Authority:** `REFERENT_ADMISSION_ONTOLOGY_AUDIT_R1.md` and exact RFA-05/RFA-05B source schema. This is a **local corrected review**, not a replacement for the original model schema, actor instructions, physical permission court, or human evaluator.

## Typed compiler

The `referent_admission.compile_grounding(packet)` function creates an allowlist for **one exact case and one exact arm**, only from these explicit model-visible paths:

1. `shared.scene.facts[*].source_ref` for documented W-world entities;
2. literal actor `NADIA` and current participant `P0`;
3. `shared.actor_projection_exact_from_RFA05.actor_accessible_refs` with exactly accepted original ID + optional textual qualification (e.g. `H006 partial`, `MEM01 fragment`, `T02 known false to actor`, `T03 actor-private`);
4. WP *only*: ID-bearing `whole_current_developed_person`, `selectively_retrieved_biographical_anchors`, `event_relevant_accessible_memory_or_safe_effects`, and typed arrays under `differentiated_relations`.

It does **not** use arbitrary regex matches on string values or instructions, the evaluator fixture's objective truth register, complete canon, files from other cases, identifiers in other arms, or a global union across RF cases. A physical W ID mentioned anywhere except the documented scene cannot become a new physical target. Source field paths and delivery classes remain attached to every accepted grounding reference.

## Admission split

- **Atom grounding:** `SPEECH`, `PAUSE`, `GESTURE`, `SILENCE`, `BODY_ACTION`, `OBJECT_ACTION` may carry a listed semantic grounding ID. The ID indicates a documented reason/history/reference relevant to an outward proposal; it need not be visible matter.
- **Object interaction:** `OBJECT_ACTION` must also identify at least one **documented physical scene W referent**; semantic-only references cannot make absent objects manipulable.
- **World effects:** `world_effect_proposals[*].referent_id` must be an actual physical scene W ID. The existing original R2 physical referent and effect checks are retained.
- **Source delivery:** any `BEHAVIOR_ONLY` component still prohibits treating its inward content as a disclosed cause merely because the ID is attached. The returned `semantic_review_flags` requires substantive review, not automatic narrative permission.
- **Unknown/other-case/evaluator-only:** unrooted IDs, W09–W11 excluded scene refs, foreign branch R14B/R15B in RF008, invented people, and phantom history are rejected or withheld; IDs explicitly present in RF009 are lawful only in that specific case and arm.
- **Noninterference:** no changed `model_payload`, request JSON, provider-side `fixture_id` const, exact user event, schema semantics, sample schedule, prompt wording, renderer instruction, scoring rule, or post-response candidate content.

## Record keeping

For each candidate the court records `original_r2_issues` **and** `corrected_issues`, with each examined referent's source field, class and source-delivery condition, plus any semantic review flags. For all 60 locally available Opus R2 outputs, `OPUS_R2_FULL_RECHECK_R1.json` separately records old status/old issues and new referent check/status without changing their raw receipt. New Sonnet/Haiku outputs retain full source schema validation and receive exactly the same corrected checker.

Even a corrected mechanically valid candidate may fail separate substantive Nadia evaluation. The inherited RFA-05 rubric and permitted-world admission remain authoritative.

## Machine-testable contrasts

`validate_cross_model_court.py` tests all ten cases in N and WP against every compiled allowed ID; disallows W09/W10/W11, unknown H999, nonrooted ZZ999, cross-case R99B, and evaluator labels; tests branch-local R14B present for RF009 WP but absent for RF008 WP; tests an object action with only semantic grounding is blocked while the same action with scene W grounding is structurally permitted; tests a world write to a nonphysical semantic ID remains blocked.

If the source or ID schema changes, fail closed rather than constructing new ad hoc adapters.

**Comparability verdict:** `PASS__NO_OPUS_RERUN_REQUIRED` provided static/dynamic source request parity holds. An inherited R2 request is cloned exactly for the new models and **only the provider model identifier is changed**; correction is never model-visible.
