# SOROK S45-S47 causal regression harness

**Grade:** `TEST_ONLY_ENGINEERING_CAUSAL_REGRESSION_NOT_INDEPENDENT_FINAL_REVIEW`

This is a separate executable harness. It does not modify pinned S45-S47 source
behavior, expected psychology, or another worker return. It can run directly
against the shipped product import closure (`--package-closure`), or use the
historical git-extraction mode that stages exact pinned source into
`.runtime/source-tree`. Both modes verify source bytes, check import origins and
exercise the performed-versus-scheduled causal chain through the actual S47 C9
path and S45 `DO_HELP`.

## Commission and pins

- Whole-person receiving commission base:
  `078d9c57bc835a34e90b3671bdef6c28a0f43747`
- S45: `f26a138e20d53c809d611cf8d834ec647b0804bf`
- S46: `f0ef39b92ce2e4add5c0a699389e12f1d7ae434e`
- S47: `765a441f87292aa4c17794745b65cb54e6aaa83f`
- Exact dependency cuts, including the S42/S37 seam-carrying trees, are in
  `harness/pins.py`. The S42/S37 seam files are taken from the S47 cut because
  that is the actual admitted S47 import closure.

## Package-closure run (integration mode)

From the checkout root:

```text
python3 WORKER_RETURNS/SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1/run_causal_harness.py \
  --package-closure WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product \
  --original-tests none
```

This mode installs the shipped `sorok_s45_s47` package closure, verifies its
424-file source manifest, confirms load-bearing modules resolve under the
package vendor tree, and runs the causal scenarios against that exact package.
It does not extract pins independently and does not duplicate full author
suites (`original_tests` is recorded as `NOT_RUN`).

## Git-extraction run

From the checkout root:

```text
python3 WORKER_RETURNS/SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1/run_causal_harness.py \
  --original-tests all
```

The default non-package invocation extracts all pins from the local git object
store, re-runs the original focused suites (S45 21, S46 17, S47 17), runs the
causal scenarios, and writes:

- `evidence/harness_run.json`
- `evidence/junit/s45_full.xml`, `s46_full.xml`, `s47_full.xml`
- `logs/s45_full.log`, `s46_full.log`, `s47_full.log`
- `logs/harness_stdout.log` when the caller tees stdout

## Explicit pinned paths

The harness also accepts explicit pinned paths. They are copied into the
in-worktree stage, then verified byte-for-byte against the pinned git blobs
before any import:

```text
python3 WORKER_RETURNS/SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1/run_causal_harness.py \
  --source-root /path/to/rawlsing \
  --s45-return /path/to/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1 \
  --s46-return /path/to/SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1 \
  --s47-return /path/to/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1 \
  --join-e-return /path/to/SOROK-20261022-SAME-PERSON-JOIN-R1 \
  --language-return /path/to/LANGUAGE_MEDIATION_R1 \
  --original-tests all
```

Any pin can be overridden with `--pinned-path KEY=PATH`; keys are listed in
`harness/pins.py`. `--package-root` is an alias for `--source-root`.

## Options

- `--package-closure PATH`: run against the shipped product import closure.
- `--original-tests {all,s47,none}`: original focused test scope.
- `--test-timeout SECONDS`: per-suite timeout.
- `--stage-dir`, `--work-dir`, `--logs-dir`, `--evidence-dir`, `--json-out`.
- `--reuse-stage`: keep an existing extracted stage, then verify it.
- `--keep-work`: keep transient scenario state under `--work-dir`.

## Exit status

- `0`: every scenario, pin, import and requested original-test check passed.
- `1`: a harness check failed; see `evidence/harness_run.json`.
- `2`: staging, pin verification, import or execution error; see
  `evidence/harness_failure.json`.

## Boundary

All roots and material are TEST_ONLY synthetic. The harness does not issue
native C8/C9/C12, CAN008/CAN011, ADP, Pyat or human authority. It is engineering
causality evidence for the receiving commission, not an independent final
review or acceptance.
