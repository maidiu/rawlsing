# RFA-06A — Anthropic one-shot renderer feasibility court harness

**Status: PREPARED FOR LOCAL EXPERIMENT; NO PROVIDER CALLS; NO OUTPUTS OR SCORES.**

This directory extends the exactly sealed RFA-05B commit \`a406e1d289faac31fd51cca8b36a4bb47af93852\`. It does not modify any of the 20 RF001–RF010 WP/N packets, original RFA-05 laboratory fixtures, actor facts, output schema, scoring rubric, or architecture.

The scientific design is 10 cases × 2 input conditions × 3 independent provider generations = **60**. WP is the hand-curated \`WHOLE_PERSON_UPPER_BOUND\`; N is the exact inherited \`NARROW_CONTEXT_ABLATION\`. Their \`shared\` subtrees are byte-canonically equal within each case. No assumption about which condition will perform better is encoded in the runner.

## Files

- \`ANTHROPIC_BINDING_RECEIPT_R1.md\`: verified current model/API/SDK details and documented limitations.
- \`EXPERIMENT_CONFIG_R1.json\`: fixed provider, model, max tokens, source Git blob identities, dependency versions, retry and scheduling law.
- \`EXECUTION_MANIFEST_PRIVATE_R1.json\`: 60 pre-randomized assignments, with condition/replicate mapping — **never hand this to blinded scorers**.
- \`BLINDED_SCORING_MANIFEST_R1.json\`: 60 opaque RUN IDs only.
- \`court_common.py\`: offline source verification, deterministic request construction, JSON Schema projection, exact local validation helpers and exclusive atomic evidence writing.
- \`run_anthropic_renderer_court.py\`: preflight, freeze, intentional smoke, real primary execution, resumability, exclusive attempt IDs, local raw receipts and blind export.
- \`validate_renderer_court.py\`: entirely offline pre/post-execution integrity gate.
- \`LOCAL_EXECUTION_INSTRUCTIONS_R1.md\`: precise owner setup/commands.
- \`requirements.txt\`: exact package versions.
- \`results/raw/\`, \`results/blinded/\`, \`results/receipts/\`: result-safe tracked empty directories (\`.gitkeep\`), otherwise ignored.

## Execution principles

The **only** semantic prompt input is canonical JSON of \`packet["model_payload"]\`. The runner does not send packet IDs, \`audit_metadata_NOT_FOR_MODEL\`, canonical/evaluator source files, scoring oracles, private user state, or condition names. The output schema is enforced using Anthropic's currently supported \`output_config.format\` JSON mode plus **unaltered original Draft 2020-12 local validation**. The documented provider-unsupported keywords are transported as deterministic descriptions but still enforced locally. A schema failure remains evidence; no later model fixes the answer.

Each local result includes a complete raw provider response, exact semantic input and hashes, request hash, source-packet byte hash, timings, usage including thinking token details when returned, model ID, SDK binding, parse/schema status and structural findings. Raw evidence is private, attempt IDs are append-only and atomically published, a retry is not a new sample, and forced reruns never overwrite prior evidence. Normal reruns skip any terminal model result, including a poor or refused response. The only automatic retries are recorded provider/transport errors with no captured model result.

Blind export gives scorers \`RUN-XXXX.json\` files with only output, status and necessary deterministic structural diagnostics; no arm label, input byte count, prompt, provider usage, original audit data or mapping. The \`fixture_id\` inside the **model's own output** may still enable case-specific scoring; it is the identical mandated field in both arms.

**No raw output is automatically admitted into Rawlsing's canonical world and no character-quality scoring is performed here.**

## Procedure

Read \`LOCAL_EXECUTION_INSTRUCTIONS_R1.md\`. For zero-key offline source validation use:

\`\`\`sh
python3 validate_renderer_court.py --expect-empty
\`\`\`

Once the local owner intentionally installs exact dependencies and exports the key, use \`--preflight\`, then \`--freeze\`, optionally \`--smoke\`, then the main \`python3 run_anthropic_renderer_court.py\`, then \`--export-blinded\` and \`python3 validate_renderer_court.py --require-complete\`.

At handoff: \`MODEL_OUTPUTS_PRESENT = 0\`; \`ANTHROPIC_MESSAGES_CALLS_BY_COMMISSION = 0\`; \`SCORING = NOT_STARTED\`. All API functionality is prepared against published documentation but live provider/schema acceptance cannot be proven without an intentional owner call.
