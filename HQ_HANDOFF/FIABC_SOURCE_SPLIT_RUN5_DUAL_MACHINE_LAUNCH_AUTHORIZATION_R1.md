# FIABC Source-Split RUN5 Dual-Machine Measured Launch Authorization — R1

Status:

`AUTHORIZED__FRESH_DUAL_MACHINE_SOURCE_LOCAL_MEASURED_RETRY`

Governing protected execution:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

Exact protected head:

`3d8f2ad62600b6777dcb23a28404a067502e77a0`

Canonical qualified source-split control:

`agent/vozhd-fiabc-source-split-alternate-runner-r1`

Exact control head:

`4f0ee6bbc7e3387fb1c71837c1ae8bea658f64a2`

Governing runtime:

- CPython 3.11.3
- pyreadstat 1.3.6
- pyarrow 25.0.1
- pandas 2.3.1
- numpy 2.3.2
- Darwin x86_64

## LiTS host

Protected checkout:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_QUALIFICATION/FIABC-LITS-LAUNCH-READY-R1/worktrees/protected-execution-fresh-20260925`

Control checkout:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_QUALIFICATION/FIABC-LITS-LAUNCH-READY-R1/worktrees/source-split-control`

Python:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_QUALIFICATION/FIABC-LITS-PRIMARY-MACHINE-BOOTSTRAP-R1/runtime-py3113/bin/python`

Source:

`/Users/matthewsmith/Desktop/Rawlsing/data/Data/LiTS_I.dta`

Verified source SHA-256:

`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

Fresh work root:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/FIABC-P2X-SOURCE-SPLIT-RUN5/LITS_I`

Auto logout disabled. Host is on AC. AC idle sleep remains enabled, so launch must be wrapped with `caffeinate -i -s`. Work root was verified empty during readiness and must be rechecked immediately before launch.

## WVS7 host

Protected checkout:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/Rawlsing-retry-r1/protected-execution`

Control checkout:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/Rawlsing-retry-r1/source-split-control`

Python:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/python/fiabc-wvs7-retry-r1-3.11.3/bin/python`

Source:

`/Users/matthewsmith/Desktop/Rawlsing/WVS Wave 7.sav`

Verified source SHA-256:

`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Fresh work root:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/FIABC-P2X-SOURCE-SPLIT-RUN5/WVS7`

Auto logout disabled. AC system/disk/display sleep are disabled. Work root was verified empty during readiness and must be rechecked immediately before launch.

## Runner identities

- source-local launcher blob: `f178cd510e41bedced3411ffcd5aa18301a1e20d`
- source-local driver blob: `e77f9165f93d3b1c3c5cfc8dbfa23a3a827040c1`
- merge verifier blob: `51c254a3b254e84b71a6304a99eaef05ac49e919`

## Baseline tracked local-court files

The protected execution tree contains tracked historical/baseline JSON files under `EE-P2X/LOCAL_COURT/cells`. This does not constitute measured candidate state for RUN5.

The protected driver function `_candidate_roots(root, source, candidate)` constructs all candidate-owned measured roots exclusively under the external supplied work root:

`WORK_ROOT/cells/<source>/<candidate>`

Therefore the tracked repository baseline files are inert with respect to RUN5 candidate state.

## Authorized measured sequence

LiTS host:

`LITS_I/A -> LITS_I/B -> LITS_I/C`

WVS host:

`WVS7/A -> WVS7/B -> WVS7/C`

The two source-local blocks may execute concurrently.

## Launch law

Immediately before starting each source block, verify:

1. protected checkout clean and exact head;
2. control checkout clean and exact head;
3. exact expanded runtime tuple;
4. selected source file present;
5. selected source SHA matches canonical identity;
6. designated RUN5 work root has zero entries;
7. session-safety state remains effective.

Launch through the qualified source-local launcher only.

Use `nohup` and `caffeinate -i -s` so execution is independent of an interactive terminal and the host remains awake.

## Once measured execution begins

No adaptive repair.

No silent retry.

No code/package modification.

No work-root cleanup.

No resume of a terminated measured attempt.

Preserve terminal receipts and logs exactly.

A source-local candidate failure does not authorize repair or retry during RUN5.

## Forbidden claims

Neither host may:

- execute or claim the full six-cell S17 verifier;
- perform P2 synthesis;
- rank/select A/B/C;
- make architecture-selection conclusions.

P2 remains blocked until both source-local terminals are returned and HQ completes the source-split merge/adjudication.

## Prior evidence

Do not mutate, clean, reuse, or resume:

- the prior WVS source-local measured root that exposed the missing-pandas common runtime defect;
- the prior blocked LiTS pre-candidate root.

## Authorization

Both machine-readiness returns are accepted.

RUN5 fresh dual-machine measured launch is authorized now.
