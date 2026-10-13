# RFA-06C2 immutable generation and study design proof

**Startup:** `b4fd4855c1b7608d06481b5ac55f577af1476e06`.
**Scope:** exclusively post-generation speech checker and smoke admission/custody logic; new R2 directory instead of in-place RFA-06C freeze mutation.

1. The successor `EXPERIMENT_CONFIG_R2.json` differs from `R1` only in `kind` (experiment label, not sent to provider); `screen_common.config()` enforces exact equality of all other settings. Effort high, 16384 tokens, API version `2023-06-01`, no system message, no sampling knobs, fixed exact model IDs remain unchanged.
2. The original Git blobs of `EXECUTION_MANIFEST_PRIVATE_R1.json`, `OPUS_EXISTING_SAMPLE_SELECTION_R1.json`, `BLIND_MAPPING_PRIVATE_R1.json`, `BLINDED_SCORING_MANIFEST_R1.json`, `score_and_unblind.py`, original referent authority documents, and 20 source packets are retained by Git object identity. `source_manifest()` still independently reconstructs the 40-call shuffle and balanced 60-slot mapping.
3. `screen_common.request_for_new()` remains semantically unchanged from RFA-06C. It delegates to sealed R2 `court_common_r2.request_for`, changes only the model scalar and enforces exact canonical byte parity after restoring the original Opus model. Exact original packet, fixture identity envelope, transport instruction, output schema, effort and max token checks persist for all 42 requests.
4. `freeze_fingerprints()` includes 42 exact compiled request/message/schema SHA-256 identities and all R2 code/doc/scoring/custody hashes; new `EXPERIMENT_FREEZE_R2.json` is a local-only, separate freeze. Prior freeze remains sealed.
5. Imported local smoke receipts are non-primary; Opus 20 already selected remain unregenerated, secondary 40 remain secondary, Sonnet N=20 and Haiku N=20 unchanged. Opus rerun prohibited. Fifteen unchanged blind-scoring dimensions remain unchanged.

**Machine-checkable gates:** source code enforces config, blob, request and model/fixture parity. Owner-local Python execution and real smoke custody are **not** established by static GitHub access alone; they require the commands in `LOCAL_EXECUTION_INSTRUCTIONS_R2.md`. Any mismatch is a HOLD rather than a modified model-visible request.

**Primary interpretation:** 60 observations in a balanced, exploratory renderer-only experimental comparison conditional on hand-made RFA-05B actor/world packets. Smoke transport validity never becomes model-quality screening or primary scoring.
