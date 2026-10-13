# RFA-06C — independent GitHub source and static-design validation receipt

Basis: exact sealed commit `4ce795413c2e77be04657a260cbda586610f4756`, read-only GitHub file contents and independent deterministic JavaScript comparisons. **Static verification is not a claim that Python was locally executed, that raw Opus R2 receipts were available, or that an Anthropic call was made.**

## Completed static checks

- `REFERENT_ONTOLOGY_SOURCE_AUDIT = PASS`: original atom schema does not restrict `referent_ids` to current-scene W references. The original contract separately restricts world-effect proposals to documented physical object state. RFA-05B lawful actor context includes historical, relational, task, organizational and developmental grounding identifiers.
- `INHERITED_REFERENT_CHECKER = OVERRESTRICTIVE`: R2 `deterministic_candidate` receives only scene references, plus `NADIA`/`P0`; it therefore mechanically rejects an actor-visible non-scene ID even when its use as a semantic ground is permitted.
- `20_ACTOR_INPUT_STRUCTURES_CHECKED = PASS`: RF001–RF010 in both N and WP inspected against sealed GitHub blobs. All actor-access annotations have recognized ID forms, scene-world references equal the declared scene ref set, and all 495 WP component rows (including relation subtrees) carry `id` and `delivery` fields. No N packet has a WP extension.
- `POST_GENERATION_ONLY_CHANGE = PASS (source comparison)`: R2 request compiler is imported without edits and clones request; the new-model request changes only `model`, then checks exact structural and canonical equality after restoring the Opus model. Corrected referent checking is invoked only after receiving and parsing a candidate.
- `OPUS_REPLICATE_1_SELECTION = PASS`: independently reconstructed all twenty case×condition selected R2 identities using only the sealed scheduling manifest, and separately tracked the remaining forty Opus replicates.
- `NEW_SCHEDULE = PASS`: independently reproduced xorshift/Fisher–Yates from `0x5A0C4020` across all forty interleaved new model/case/arm assignments.
- `60_BLIND_SLOTS = PASS`: independently reproduced blind mapping with distinct seed `0x5A0C5001`; exact 20 observations per model, one per case×arm, with scorer-visible manifest containing only fresh `BLIND-CM-XXXX` IDs.
- `MODEL_BINDINGS = VERIFIED_IN_CURRENT_OFFICIAL_DOCS`: Anthropic documents API IDs `claude-sonnet-5-5` and `claude-haiku-5-5` and an `effort` setting. See `MODEL_BINDING_RECEIPT_R1.md`.
- `SEPARATE_SMOKE_AND_FREEZE_LOGIC = STATIC REVIEW PASS`: the local code checks two distinct returned model IDs, original JSON schema, request fixture const and corrected structural validity, and requires both smokes before the forty-call loop. Freeze includes exact source fingerprints plus 42 compiled new-model requests.
- `SCORER_BLINDING_AND_SCORE_SEAL = STATIC REVIEW PASS`: scorer export is only blind ID, RF case and candidate. Fifteen source-rubric dimensions and all sixty judgements must be complete before SHA-256 seal; unblinding requires a separate explicit invocation.
- `OLD_NEW_STATUS_CUSTODY = STATIC REVIEW PASS`: local review records original Opus R2 structural issues and newly adjudicated referent statuses side-by-side and never rewrites R2 raw evidence.

## Unobserved work (held for owner)

`ANTHROPIC_MESSAGES_CALLS_BY_COMMISSION = 0`.
`LOCAL_PYTHON_VALIDATOR_RUN_BY_COMMISSION = NO`.
`RAW_OPUS_R2_RESPONSES_AVAILABLE_IN_GITHUB = NO`.
`NEW_MODEL_OUTPUTS_OR_SCORES = NONE`.
`LIVE_SONNET_HAIKU_SMOKE = NOT_ATTEMPTED`.
`REAL_RENDERER_CAPABILITY_BY_MODEL = UNMEASURED`.

A future owner-local `python3 validate_cross_model_court.py --expect-empty` must pass before a freeze, and both independently billed smoke calls must succeed before any primary new-model generation. Absent authentic local R2 Opus records, the balanced scorer bundle must remain on HOLD; reported percentages are not substitute evidence.

The comparison is a renderer-only conditional test over hand-built laboratory actor/world state; it does not imply full Rawlsing runtime feasibility.
