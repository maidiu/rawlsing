# RFA-05B — Whole-person renderer input compilation and narrow-context ablation

**State: PREPARED; NOT EXECUTED.** Sealed RFA-05 start `284b9b4bebbc281276ee65d3821fb05abdad42f2`; RFA-R reconciliation `e65846bbb1c38a366d79b54bb89be47da0f8502e`; Sorok architectural base `da6f3c5e43f7f12c8c33f0109f2894e37b482e7d`. Every source and generated actor fact is a hand-authored experimental surrogate, not future V3 output.

This directory contains twenty actor-input packet files, one matched WP/N pair for each original RF001–RF010. Nothing in `lab_fixture/` has been rewritten. The first feasibility condition is **WP: whole-person upper bound**; **N: narrow-context ablation** is the controlled first reduction, not old V2 and not a production candidate.

## Critical usage instruction

Submit **only `model_payload`** to the eventual Claude-class provider. The adjacent `audit_metadata_NOT_FOR_MODEL` contains provenance, source-state accounting, and experiment evidence **not** intended for the model. Never send the original full RF case, evaluator canon/truth register, RFA-05 scoring rubric, or parity manifest to the provider as a prompt.

Every pair has exactly the same `model_payload.shared` subtree: the original sealed `expression_action_constraints.value.actor_safe_projection` unchanged, exact admitted P0 speech, actor-permitted scene objects, one-shot renderer contract, and typed unadmitted occurrence output schema. WP alone adds `whole_person_extension`. The same frozen actor/event, relationship branch, CAN-008/PFF surrogate source state, schema, world bounds and admission rules underlie both conditions.

WP offers a substantial, read-only, distributed current person: context-specific and contradictory organization, body/material constraints, independent rooted obligations, differentiated competency/access, other distinct relationships, precise P0 relational episodes, and **selectively** retrieved actor-accessible historical episodes. Private causal accounts and evaluator-only objective facts are not supplied. The model may instantiate downstream expressive effects without claiming that Nadia knows their causes.

`INPUT_PARITY_MANIFEST_R1.json` records paired source fingerprints, equality checks and model-only payload sizes. Raw bytes refer to UTF-8 of compact JSON of `model_payload`. Approximate tokens are only `ceil(bytes/4)`, not a model tokenizer or financial estimate. Stable instructions, stable WP person portion and case-dynamic portions are itemized.

**Known inherited prompt-framing issue:** RFA-05's exact narrow actor projection sometimes contains test-boundary wording (RF008/RF009 cross-case reference; RF006 VALID_EMPTY). Preserving the narrow control unchanged retains these phrases in both arms. They are not evaluator truth-register disclosures, but they may influence later samples. Treat them as a documented inherited limitation rather than silently changing one arm.

Required files: `WHOLE_PERSON_INPUT_COMPILATION_RULE_R1.md`, `NARROW_INPUT_COMPILATION_RULE_R1.md`, `ABLATION_DESIGN_R1.md`, `RENDER_INPUT_SCHEMA_R1.json`, `INPUT_PARITY_MANIFEST_R1.json`, `RF001_WP.json`/`RF001_N.json` through `RF010_WP.json`/`RF010_N.json`. `VALIDATE_RENDER_INPUTS_R1.js` provides an offline test.

No Anthropic invocation, model output, user phenomenal compositor, score, runtime V3/CAN-008/PFF/V2 implementation or production admission is claimed.
