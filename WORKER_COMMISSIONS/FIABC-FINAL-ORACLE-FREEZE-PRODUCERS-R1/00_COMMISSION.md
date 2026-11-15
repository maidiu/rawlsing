# FIABC FINAL ORACLE + T3 FREEZE PRODUCERS — R1

**AGENT TYPE: BROWSER / GITHUB ONLY**
**MODEL: GPT-5.6 Sol High**

Repository: `maidiu/rawlsing`

Exact base:
`4c05a5289d0dd2fb6d475e90a039cce1360b38e3`

Branch:
`agent/rabochii-premain-fiabc-final-oracle-freeze-producers-r1`

Return:
`WORKER_RETURNS/FIABC-FINAL-ORACLE-FREEZE-PRODUCERS-R1/`

## Hard prohibitions

Do not use the user's Mac/local runtime.
Do not open or materialize raw LiTS/WVS source bytes in this lane.
Do not run Candidate A/B/C.
Do not run measured P2X.
Do not trigger GitHub Actions.
Do not change candidate semantics, P2 workload, Lock1/Lock2 law, metric definitions, or P3.
Do not wait for sibling workers.

## Mission

Close exactly launch blockers B03, B05, and B06 from:

`WORKER_RETURNS/FIABC-FINAL-LOCAL-LAUNCH-PACK-R1/05_BLOCKERS_IF_ANY.md`

Produce deterministic CLIs/glue. Do not fabricate resulting local oracle identities because this browser-only worker cannot execute the real sources.

### B03 — standardize accepted successor WVS oracle

Accepted R1M input:

`WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json`

Accepted identity:
`3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800`

Truth payload:
`eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405`

Add one deterministic source-free adapter/launcher that:

- consumes only accepted R1M wrapper/truth plus already-frozen successor authority;
- maps it into the existing standard live WVS materializer contract;
- calls existing `freeze_wvs7_oracle_from_common_material()` / standard freeze law;
- emits `RAWLSING_FIABC_CANDIDATE_NEUTRAL_PARITY_ORACLE@1.0.0`;
- starts zero candidate processes;
- reads zero raw WVS bytes;
- consults zero candidate-owned roots;
- self-verifies with `verify_frozen_oracle()`.

Do not treat the R1M wrapper itself as if it already were the standard T5 oracle.

### B05 — LiTS current exact oracle producer CLI

Add one candidate-neutral local producer CLI that is allowed, when later run by the user locally, to read the exact LiTS source and accepted common semantic/runtime authority.

It must produce the missing current pieces:

- `CURRENT_STANDARDIZED_CONSTITUENT_I03_FACT_REFS`
- `CURRENT_CONSTITUENT_I03_CLOSURE_IDENTITY`
- `CURRENT_OBSERVATION_SHAPED_EXACT_REF_MANIFEST`

Then call existing `build_lits_i_oracle()` and `freeze_oracle()`.

Hard law for the CLI:

- zero A/B/C processes;
- zero candidate-owned roots;
- accepted LiTS product/replay identities unchanged;
- 50 candidates / 77 roles exact;
- candidate-neutral;
- deterministic output paths and receipts;
- fail closed on source/authority/hash mismatch.

Do not execute it in this worker lane.

### B06 — final two-source T3 freeze producer

Add deterministic CLI that consumes:

- exact LiTS source identity;
- exact WVS source identity;
- accepted authority/workload identities;
- standard frozen LiTS oracle document/path/SHA;
- standard frozen WVS oracle document/path/SHA;

and emits exactly:

`RAWLSING_FIABC_CANDIDATE_NEUTRAL_FREEZE@2.0.0`

with:

- `candidate_neutral=true`
- `frozen_before_candidate_execution=true`
- `candidate_outputs_seen=0`
- `candidate_owned_roots_consulted=[]`
- `candidate_owned_state_reused=false`
- `state=FROZEN_READ_ONLY`
- exact freeze order source -> authority/workload -> oracle.

Self-validate using existing `load_frozen_upstream_receipt()`.

## CLI / launch requirement

Produce real argparse/module CLIs that the final local launch pack can invoke without inline hand-written Python glue.

The returned docs must show exact intended command shapes using actual committed modules and explicit output arguments.

## Required source-free tests

Author tests proving:

- R1M WVS adapter is deterministic and source-free;
- adapter rejects predecessor authority / wrong wrapper identity;
- standard WVS oracle verifies under live schema;
- LiTS producer cannot consult candidate roots or candidate outputs;
- LiTS producer contract preserves 50/77;
- T3 freeze refuses missing/nonstandard/unverified oracle docs;
- T3 freeze self-validates and records zero candidate outputs.

Do not execute source data or candidates.

## Required outputs

- `00_RETURN.md`
- `01_WVS_STANDARDIZATION_CONTRACT.md`
- `02_LITS_LOCAL_ORACLE_PRODUCER_CONTRACT.md`
- `03_T3_FREEZE_PRODUCER_CONTRACT.md`
- `04_EXACT_CLI_SHAPES.md`
- `05_TESTS_AND_EXPECTED_ASSERTIONS.md`
- `RETURN.json`

## PASS law

PASS only if B03/B05/B06 have truthful committed producer CLIs and no current authority/semantic choice is invented.
