# RFA-06C2 — quote-invariant, nonselective-smoke successor (offline repair)

**Separate successor** to the already frozen RFA-06C; never write into `anthropic_cross_model_screen_r1/`. Branch startup `b4fd4855c1b7608d06481b5ac55f577af1476e06`. **This repository does not contain the owner-local smoke or Opus responses**. No new Anthropic calls were made by this commission.

The RFA-05 source requires exact speech content in corresponding prose quotations. R2's inherited double-quote-only regex incorrectly rejects an unchanged utterance in single quotes. `quote_invariant.py` checks ordered identical speech strings under straight/curly single or double quote delimiters, distinguishing contractions from delimiters. Original historical R2 issues are retained; corrected candidate issues are calculated separately, without altering provider outputs.

Smoke gates now test provider/schema/fixture/transport custody rather than any renderer structural or substantive quality. An original structurally invalid but exact-schema-valid candidate is eligible; its defects remain recorded. `smoke_custody.py` checks both original local smoke receipts against predecessor frozen *request* hashes, packet and schema, full message, provider response identity, settings and payload. It proves **both** before append-only import. The predecessor's frozen source hash may reflect its earlier manifest-key defect; source file identity is not silently reattributed. If request-level custody fails or private files are absent, reuse is HOLD. Never infer PASS from this README or owner-reported statuses.

RFA-05B source packets, R2 request compiler/transport, 40 ordered primary calls (20 Sonnet + 20 Haiku), selected 20 Opus observations, 40 Opus secondary replicates, and 60-slot blinding/15-dimension scoring are reused unchanged. New freeze is `EXPERIMENT_FREEZE_R2.json` (local and ignored), including all 42 request fingerprints plus all successor checker, gate, custody and scoring source hashes. Existing RFA-06C freeze is not modified.

Start with `python3 -m unittest -v test_quote_and_smoke_r2`, then follow `LOCAL_EXECUTION_INSTRUCTIONS_R2.md`. Any new generation requires a deliberate owner-local command and successful successor freeze. See `SPEECH_PROSE_VALIDATION_DEFECT_RECEIPT_R1.md`, `SMOKE_GATE_AND_CUSTODY_RECEIPT_R1.md`, and `COMPARABILITY_PROOF_R2.md`.

**Claim ceiling:** renderer-only hand-built surrogate screen. No statement about V3 production or model quality follows from smoke admission.
