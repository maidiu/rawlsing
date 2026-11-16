# FIABC FINAL TERMINAL COMPLETENESS GATE — R1

**AGENT TYPE: BROWSER / GITHUB ONLY**

**Recommended intelligence: GPT-5.6 Sol High**

Repository: `maidiu/rawlsing`

Exact base: `445c2fd534db61de0d0d348a6d77a11faa419cc3`

Branch: `agent/rabochii-premain-fiabc-final-terminal-completeness-r1`

Return: `WORKER_RETURNS/FIABC-FINAL-TERMINAL-COMPLETENESS-R1/`

## Hard law

Do not use the user's Mac/local runtime.
Do not open LiTS/WVS raw source bytes.
Do not run Candidate A/B/C.
Do not run measured P2X.
Do not change the frozen metric definitions or add a new score.
Do not reopen FIABC semantics/architecture courts.

## Mission

Strengthen S16/S17 so a completed qualifying court cannot PASS merely because a telemetry receipt exists and hashes correctly.

Current confirmed defect:
`validate_t4_terminal_accounting_receipt()` verifies receipt identity/integrity but does not require the frozen dispositive metric vector to be complete. T4 intentionally supports `MEASUREMENT_NOT_CAPTURED`, which was lawful during transposition but must not silently pass a final dispositive cell when the metric is required and reachable.

## Governing distinction

For a completed qualifying cell:
- required/applicable metric → must be `MEASURED`;
- frozen non-applicable metric → may be `NOT_APPLICABLE_BY_FROZEN_COURT`;
- lawful authorized early stop → may be `NOT_REACHED_AUTHORIZED_STOP`;
- historical/preserved evidence where numeric repetition is forbidden → only the exact frozen preserved-work disposition may apply;
- `MEASUREMENT_NOT_CAPTURED` for an otherwise required/reachable dispositive metric must fail closed.

Do not turn a lawful N/A into a fake zero.
Do not turn an authorized stop into a completed measurement.
Do not require metrics that the frozen court expressly declares inapplicable for that candidate/stage.

## Read first

- `HQ_HANDOFF/CHETIRI_FINAL_P2_COURT_MANIFEST_R1.json`
- `WORKER_RETURNS/FIABC-T4/02_TELEMETRY_BINDING_CONTRACT.md`
- `WORKER_RETURNS/FIABC-T4/04_PRESERVED_WORK_LIVE_LEDGER.csv`
- `WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json`
- `rawlsing_next/fiabc_telemetry_semantics.py`
- `rawlsing_next/fiabc_live_terminal_control.py`
- `rawlsing_next/fiabc_live_accounting_binding.py`

## Required implementation

Create a deterministic completeness validator that consumes the canonical T4 telemetry receipt plus current source/candidate/court applicability and fails closed if:
- any required applicable metric is absent;
- any required applicable metric is `MEASUREMENT_NOT_CAPTURED`;
- a metric uses an invalid disposition for the cell;
- a supposedly completed cell lacks process metrics or required lifecycle evidence;
- metric-definition hash drifts;
- telemetry claims completion while I/O/scratch completeness flags contradict required measurement coverage.

Bind this validator into the current S16/S17 terminal path so final court PASS is impossible without completeness.

The validator must remain selection-neutral: it decides whether evidence is complete, never which candidate is better.

## File ownership

Primary ownership:
- `rawlsing_next/fiabc_live_terminal_control.py`
- focused terminal-control/completeness tests
- optionally a new small completeness module if cleaner

Avoid edits to:
- `rawlsing_next/ee_p2x_darwin_stage_backend.py`
- `rawlsing_next/fiabc_live_accounting_binding.py`
- `rawlsing_next/ee_p2x_darwin_court_driver.py`

Worker A owns instrumentation. Worker C owns driver/progress. If their future outputs are needed, define the stable contract your validator expects, but do not invent measurements.

## Hostile tests

Prove at minimum:
- one missing required metric → BLOCK;
- one `MEASUREMENT_NOT_CAPTURED` required metric → BLOCK;
- legitimate N/A metric → PASS;
- authorized stop metric state → handled only under exact stop law;
- wrong metric-definition hash → BLOCK;
- missing CPU/RSS/wall process seal → BLOCK where required;
- incomplete I/O or scratch seal → BLOCK once those metrics are required by the cell;
- candidate B no-cache N/A behavior remains lawful;
- WVS/C zero-accelerator law does not create fake cache obligations;
- validator cannot rank candidates or emit a selection.

No real source execution.

## Return

Return the exact completeness law, code/test blobs, hostile test ledger, and explicit integration seam for Worker A telemetry receipts.

PASS terminal must mean: a future S17 cannot certify a qualifying completed court with materially missing dispositive measurements.
