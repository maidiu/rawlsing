# FIABC Source-Split Pandas Runtime Repair Promotion — R1

Status:

`SOURCE_SPLIT_PANDAS_RUNTIME_REPAIR_ADOPTED__FRESH_RETRY_PREPARATION_AUTHORIZED`

Protected execution remains:

`3d8f2ad62600b6777dcb23a28404a067502e77a0`

Canonical source-split control branch now:

`agent/vozhd-fiabc-source-split-alternate-runner-r1`

Exact promoted control head:

`4f0ee6bbc7e3387fb1c71837c1ae8bea658f64a2`

Exact tested implementation head:

`5c7aef690e4d04ebc1676d3448c0314a5c4c2d89`

Qualification packet commit:

`4f0ee6bbc7e3387fb1c71837c1ae8bea658f64a2`

Qualification terminal:

`PASS__SOURCE_FREE_ALTERNATE_RUNNER_QUALIFICATION`

## Runtime law

The promoted source-split runtime is exactly:

- CPython 3.11.3
- pyreadstat 1.3.6
- pyarrow 25.0.1
- pandas 2.3.1
- numpy 2.3.2
- Darwin x86_64

## Qualification

19/19 tests passed with zero failures/errors/skips.

Source-free telemetry:

- raw source opens: 0
- survey source SHA passes: 0
- survey decoder calls: 0
- candidate process launch attempts: 0
- candidate processes/outputs: 0/0
- measured execution: false

Tested runner identities:

- source-local launcher blob: `f178cd510e41bedced3411ffcd5aa18301a1e20d`
- source-local driver blob: `e77f9165f93d3b1c3c5cfc8dbfa23a3a827040c1`
- merge verifier blob: `51c254a3b254e84b71a6304a99eaef05ac49e919`

The qualification packet commit contains only qualification return files after the tested implementation head; measured runner bytes are unchanged.

## Adjudication of prior attempt

The previous WVS source-local root is immutable evidence and must never be resumed.

Its three candidate-local terminal labels are void as candidate architecture evidence because all three were masked by the same shared missing-pandas runtime defect.

The earlier blocked LiTS root is also preserved and must not be reused.

## Fresh retry preparation

Before a fresh measured retry:

- both machines must sync canonical source-split control to `4f0ee6...`;
- both machines must use the exact expanded runtime tuple above;
- WVS must use a brand-new clean protected-execution checkout at `3d8f2ad6...` because the old one retained evidence/cache files;
- LiTS should also use a clean protected checkout;
- both sources require brand-new empty persistent work roots;
- prior roots remain untouched.

No further source-split code qualification is required if these machine gates pass.

Measured launch itself remains subject to explicit HQ launch authorization after both machine-preparation returns are green.
