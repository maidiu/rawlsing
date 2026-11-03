# Same-source R04 resume → R05/P41 consumer focused review

## Verdict

**PASS_SCOPED_SAME_SOURCE_RESUME_CONSUMER**

Same distinct reviewer; candidate is read-only. Model/provider/variant verified from session metadata before work: `opencode-go` / `deepseek-v4.1-flash` / `max`.

## Custody and scope

- Candidate: `agent/pyat-same-source-resume-consumer-20261103-r1`
- Candidate HEAD: `ea503425a6f3de29649b78587c7bcb0c2051b7ee`
- Base: `8779504a638ff39d6904ed2faf5a718242084c4e`
- Prior scoped review: `e24b70eac51d0894c7e5af7604ab7afc2376dbe6` (unchanged A/B/C acceptance; R00/R09 not reopened)
- Exactly three code/test files changed; all candidate pins match. No source/test bytecode at HEAD.
- No original source, respondents, CI/prod, protected adoption, new worker/model/provider, or host authority.

## Actual connected path

The new test creates one synthetic physical source/release/universe and runs:

R03 governed/query compilation → R04 mixed query+discovery issued execution → real partial prefix → checkpoint capture → cold restore/resume with no completed-unit rerun → actual resumed graph → R05/M1 learned disposition → M2 learned release → actual unchanged P41 consumer.

Measured positive evidence from `LINEAGE_WITNESS.json`:

- Source SHA: `927ea5873281f71ea0d11c5ddda9206fcedafd2c2967739fc2923b4f35cc1528`
- Release: `R56-SYNTHETIC-RELEASE` / `a8ba3347...`
- Universe: `485887b9...`
- R04 route replay identity: `f3a2d7e4...`
- R04 selected receipt: `02d5f0f3...`
- M1 disposition: `2dca454d...`
- M2 release: `dc007e16...`
- Learned receipt: `9c45050b...`
- Consumer result: `fefd3b88...`
- P41 view: `R05_WORLD_SELECTED_VIEW`, temporal changed true, view hash `7ee6cfb0...`
- T0 training `ELIGIBLE`; T1 training `BLOCKED_BY_MODELED_RULE`
- Negative controls: source mismatch and revocation `WorkloadAdmissionError`; upstream evidence severance `R05_N10E_EVIDENCE_BINDING_MISMATCH`; restored same consumer returns the positive view.

The new test explicitly asserts the P41 conditioner identity equals the actual STEP conditioner list, not a hard-coded `X=1`.

## Tests

New connected path:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest \
  rawlsing_next/tests/test_universal_world_binding.py::test_same_source_r04_partial_resume_reaches_actual_p41 \
  -q -p no:cacheprovider -o addopts=''
```

**1 passed in 54.92s.**

Focused custody + actual positive/severance:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest \
  rawlsing_next/tests/test_universal_workload_custody.py \
  rawlsing_next/tests/test_universal_world_binding.py::test_r06r2_actual_r05_learned_to_p41_world_with_synthetic_pair \
  rawlsing_next/tests/test_universal_world_binding.py::test_r06r3_actual_step_severance_refuses_restore \
  -q -p no:cacheprovider -o addopts=''
```

**8 passed in 21.86s.**

## Fresh-process reproducibility

Independent parent/child run under the test’s `PYTHONHASHSEED=0` and `PYTHONDONTWRITEBYTECODE=1` conditions reproduced all selected identities: source SHA, route replay identity, selected receipt, M1/M2 refs, learned receipt, consumer result, evidence ref, view state, and view hash. No downstream instability was observed in this run.

The author’s caveat about possible test-only M1 evidence ordering remains a limit for universal byte-identity language. This review claims only the measured synthetic scope and does not claim universal byte-stable replay across arbitrary environments.

## Limits

- TEST_ONLY synthetic nonrespondent source and modeled temporal pair; not original respondents, source science, F5/F6/F7, or production adoption.
- No CONTEXT structural/cross-unit pooling or real temporal pair authority.
- R00/R09 behavior and central R09 host hold are unchanged/not reopened.
- No new engine, source reader/compiler/decoder, worker, model/provider, CI/prod, N11/N12, Sorok, J52/W52, or actor grant.
