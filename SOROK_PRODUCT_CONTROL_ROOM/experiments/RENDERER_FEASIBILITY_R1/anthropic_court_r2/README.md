# RFA-06B — separately issued R2 actor-renderer court

**Prepared, not run or scored.** Exact predecessor: RFA-06A `4a6bf4dafbe113ae61ab6fc2423acec6619dc0f9`.

R1 is closed as `ABORTED_DIAGNOSTIC_COURT__OUTPUT_IDENTITY_NOT_MODEL_AVAILABLE`. The model was asked for a current exact `fixture_id` without being told which of the ten case IDs was required. The first three primary responses reported by the owner are preserved as diagnostic evidence and excluded from capability estimates. See `R1_ABORT_AND_DEFECT_RECEIPT_R1.md`.

R2 repairs **only experiment bookkeeping**: the unchanged WP/N `model_payload` is wrapped with a current `required_fixture_id` and one fixed transport instruction; the provider output schema is deep-copied and its `fixture_id` is constrained to the same value. The original source output schema remains unchanged. Every run must pass the four-way identity equality check against model message, provider schema, execution manifest and local validator.

The original twenty RFA-05B packets, all Nadia facts, full-person extension, world/event/instructions, original output semantics, model `claude-opus-5-5`, `high` effort, `16384` max tokens, absent system message, and three replicates remain unchanged. The new manifest has 60 freshly shuffled opaque `R2RUN-XXXX` primary IDs, seed `0x5A0B2026` (schedule only), plus `R2SMOKE-0001` non-primary.

## Contents

- `court_common_r2.py`: source hashes, original WP/N parity, exact envelope and provider-schema binding, per-run identity proof, freeze fingerprints, append-only evidence handling.
- `run_anthropic_renderer_court_r2.py`: preflight, freeze, deliberate smoke, smoke acceptance gate, resumable execution, blind export.
- `validate_renderer_court_r2.py`: offline pre- and post-execution integrity verification.
- `EXPERIMENT_CONFIG_R2.json`, `EXECUTION_MANIFEST_PRIVATE_R2.json`, `BLINDED_SCORING_MANIFEST_R2.json`: static frozen provider and R2 randomization setup.
- `ANTHROPIC_BINDING_RECEIPT_R2.md`, `OUTPUT_REQUIREMENT_AUDIT_R2.md`, `R1_ABORT_AND_DEFECT_RECEIPT_R1.md`, `STATIC_VERIFICATION_RECEIPT_R2.md`: contract evidence.
- `LOCAL_EXECUTION_INSTRUCTIONS_R2.md`: exact operator sequence.
- `results/raw/`, `results/blinded/`, `results/receipts/`: separate result-safe ignored directories.

The runner never scores Nadia, substitutes a different provider, modifies source fixtures, retries semantically poor generations, or admits proposed changes into canonical history. The original expected case ID is now plainly available and also hard-constrained.

**Start with `python3 validate_renderer_court_r2.py --expect-empty` and follow local instructions.** Before main execution, the owner must freeze the R2 request and obtain a separately persisted schema-valid R2 smoke result with the exact fixture ID; otherwise R2 remains on HOLD.

**Do not resume R1 or migrate R1 diagnostic outputs into R2.** R2's independent 60 calls are the first potential valid primary data; a positive feasibility judgement would require separately blinded evaluation afterward.
