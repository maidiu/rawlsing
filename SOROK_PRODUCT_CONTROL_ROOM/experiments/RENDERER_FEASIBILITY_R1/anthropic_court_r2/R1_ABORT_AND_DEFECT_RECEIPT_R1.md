# RFA-06B — R1 diagnostic abort and independent identity-path proof

**Sealed R1 commit**: `4a6bf4dafbe113ae61ab6fc2423acec6619dc0f9`.
**R1 disposition**: `ABORTED_DIAGNOSTIC_COURT__OUTPUT_IDENTITY_NOT_MODEL_AVAILABLE`.
**R1 primary outputs admissible for renderer estimate**: **0 of the first 3**.
**R2 new experiment**: independently randomized, fresh 60-call schedule and separate evidence namespace; no R1 responses reused.

## Independent proof from exact source code

1. `anthropic_court_r1/court_common.py::request_for(run,c,t)` computes `packet_name = run["case_id"] + "_" + run["condition"] + ".json"`, but loads only `read(INPUT / packet_name)["model_payload"]`, minifies that `payload`, and sends the resulting text as the **sole user-role content**. Neither packet identity nor run case identity is sent as a separate request field.
2. The sealed original RFA-05B packet contains four top-level keys: `packet_id`, `condition`, `model_payload`, `audit_metadata_NOT_FOR_MODEL`. The specific `packet_id` is outside transmitted `model_payload`. Source packet `model_payload.shared.output_schema.properties.fixture_id` is a *global enum of RF001 through RF010*, not a current case identity. The repository's original `lab_fixture/OBJECTIVE_OCCURRENCE_OUTPUT_SCHEMA_R1.json` agrees.
3. `court_common.py::transport_schema` projects that same ten-value enum into the provider output schema; `request_for` does not replace it with the current case's singleton.
4. `anthropic_court_r1/run_anthropic_renderer_court.py::take_one` first checks the resulting JSON against the **original global schema**. It then calls `deterministic_candidate(candidate,run["case_id"],refs)`.
5. `court_common.py::deterministic_candidate` checks `candidate.get("fixture_id") != case_id` and emits `WRONG_FIXTURE_ID` when they differ. Thus an ID fully lawful under the provider-visible schema can fail a local condition not supplied to the model.
6. The transmitted payload may describe distinctive dialogue and scene facts, and occasionally mentions RF numbers in inherited cross-case context, but it supplies **no authoritative mapping** from this exact scene/history to its current RF identifier. No global list of allowed identifiers establishes which one is expected. Exact case identity is therefore not reliably recoverable.

**Finding:** `REQUIRED_OUTPUT_IDENTITY` was **not guaranteed by `MODEL_INPUT` or provider output schema**. The original primary trial is invalid as a test of Nadia-specific renderer capability even if its output happens to have the correct bookkeeping identifier.

## Reported local diagnostic evidence — not committed here

The repository owner reports that R1 was successfully frozen and deliberately executed for the first three primary samples:
- `RUN-0001` — schema-valid, `STRUCTURAL_INVALID` solely from `WRONG_FIXTURE_ID`.
- `RUN-0002` — schema-valid, `STRUCTURAL_INVALID` solely from `WRONG_FIXTURE_ID`.
- `RUN-0003` — schema-valid, `SCHEMA_VALID` with a coincidentally matching ID.

These observed statuses are **owner-reported**, not independently re-derived from uncommitted private raw model responses. The code-path defect above is independently verified from sealed repository files. Neither a fortunate third output nor later retrospective relabeling repairs the original experimental contract. All three R1 attempts remain privately preserved diagnostic evidence, explicitly `INVALID_FOR_PRIMARY_RENDERER_ESTIMATE`. The harness worker neither accessed nor overwrote them.

**No further R1 primary execution is scientifically authorized.** Do not resume R1; do not import R1 raw/blinded evidence into R2; do not commit raw provider responses or any API key.

## R2 repair and scope

R2 adds only a minimal transport envelope with `required_fixture_id` and a fixed instruction to copy it into `output.fixture_id`. A deep-cloned provider grammar binds this field to a request-specific **const**; the unchanged original global schema remains the local source of authority. No WP/N payloads, Nadia biographies, scenes, exact utterances, renderer instructions, output semantics, or scoring rubrics change. This repairs experiment bookkeeping, not Claude's ability to perform character realization.
