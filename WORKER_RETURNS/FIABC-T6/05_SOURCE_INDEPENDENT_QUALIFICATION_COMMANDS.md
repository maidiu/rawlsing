# FIABC-T6 — Combined Source-Independent Qualification Commands

## Worker execution status

**NOT EXECUTED.**

The T6 worker used GitHub/browser repository tooling only.

Observed GitHub Actions runs on the T6 branch during implementation: **0**.

No test PASS is claimed.

No command below opens a canonical raw survey carrier unless explicitly labeled as a later local materialization step.

## A. R35 focused implementations

### R35-I01

```bash
python -m unittest rawlsing_next.tests.test_r35_i01_physical_metadata
```

### R35-I02

```bash
python -m unittest discover -s tests -p 'test_fiabc_derivative_parentage.py' -v
```

### R35-I03

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_r35_i03_physical_equivalence.py
```

## B. R35 hostile court

```bash
python -m pytest -q tests/test_r35_generic_guard_court.py
```

This freezes the 18 hostile + 11 positive R35-Q01 fixtures, including:

- alternate same-name/shape raw source;
- asserted SHA without parent receipt;
- reader/config drift;
- compatibility promoted to semantic authority;
- raw-header mismatch normalized away;
- display replacing storage;
- all-missing drop;
- MR flattening;
- occurrence deduplication;
- form/routing carrier loss;
- equal-vector dictionary collapse;
- weight/default selection;
- detached WVS preimage;
- stale LiTS R5;
- subset/cache promoted to whole-source;
- I05 semantic PASS promoted into physical PASS.

## C. T6 live convergence tests

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_t6_live_r35_convergence.py
```

This verifies:

- exact current S35 edge classes for LiTS-I/WVS7;
- physical PASS remains nonsemantic/noncertifying;
- semantic-equal physical drift rejects;
- missing Candidate C physical realization rejects;
- old T4 mini-contract is not independently accepted;
- T4 compatibility adapter consumes a valid canonical R35 bundle.

## D. Existing physical-decoder/facade regressions

Run the repository's PRE553 physical-decoder/facade suites alongside the R35 courts. At minimum:

```bash
python -m pytest -q rawlsing_next/tests/test_r35_i01_physical_metadata.py
```

Do not weaken source-native physical assertions to make older normalized-only fixtures pass.

## E. Live T1-T5 regression/hostile court

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py
python -m pytest -q rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py
python -m pytest -q rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py
python -m pytest -q rawlsing_next/tests/test_fiabc_t4_live_accounting.py
python -m pytest -q tests/test_fiabc_telemetry_semantics.py
python -m pytest -q tests/test_fiabc_lifecycle_accounting.py
python -m pytest -q rawlsing_next/tests/test_pre553_independent_parity_oracle.py
python -m unittest discover -s rawlsing_next/tests -p 'test_fiabc_succession_preflight.py' -v
python -m pytest -q rawlsing_next/tests/test_fiabc_p2_terminal_verifier.py
python -m pytest -q rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py
```

## F. Static identity gate

On the exact T6 checkout, verify the Git blob identities recorded in:

`WORKER_RETURNS/FIABC-T6/04_PRESERVATION_AND_IDENTITY_LEDGER.csv`.

Required static conditions include:

- live driver still `4500cbb149fa187a766aca71568dc1f205a4c367`;
- physical decoder `86109c4a0b7ebd9b66e3b531b6334bfb48f03f78`;
- generic parentage `95d806a709ef4f4a0f33a8bf15b122a721a72e68`;
- physical-equivalence module `acdbc3f99f38d228d20d6a27ab7e89558af354af`;
- T3 isolation blobs unchanged;
- T4 telemetry/lifecycle unchanged;
- T5 terminal/preflight/verifier unchanged.

## G. Later LOCAL-only physical materialization

Not part of source-independent browser qualification.

Before a real physical-guard PASS can be claimed:

1. supply the actual governed LiTS-A historical first-build generic parentage bundle and pin its derivative receipt identity;
2. with exact WVS7 raw source locally available, materialize/verify WVS structural parentage through the current backend;
3. produce the candidate-neutral R35-I03 canonical physical expectations for LiTS-I and WVS7 under their exact S35 edge classes;
4. produce current A/B/C physical realizations;
5. call the T6 live two-source physical guard and require its physical-only PASS receipt.

Do not derive any missing receipt from a derivative's self-asserted source SHA.

## H. Later P2 execution gates

Only after the entire combined source-independent suite and static identity court pass may the existing local-only sequence continue:

- R6X reconciliation;
- exact source-backed oracle materialization/freeze;
- real I07 current-head preflight;
- six-cell capability/accounting closure;
- current two-source physical-guard closure;
- measured P2X last.

Nothing in T6 itself authorizes measured P2X.
