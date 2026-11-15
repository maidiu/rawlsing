# FIABC Source-Split Alternate Runner — HQ Admission R1

Status:

`SOURCE_SPLIT_RUNNER_SOURCE_FREE_QUALIFIED__MEASURED_USE_CONDITIONALLY_AUTHORIZED_PENDING_MACHINE_READINESS`

Governing protected execution:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

Exact execution head:

`3d8f2ad62600b6777dcb23a28404a067502e77a0`

Alternate source-split control branch:

`agent/vozhd-fiabc-source-split-alternate-runner-r1`

Exact qualified/published control head:

`1e701f10258831b6f453db8ad9d7ddbcba0bf247`

Source-free qualification return:

`WORKER_RETURNS/FIABC-SOURCE-LOCAL-SPLIT-SOURCE-FREE-QUALIFICATION-R1/`

Terminal:

`PASS__SOURCE_FREE_ALTERNATE_RUNNER_QUALIFICATION`

## HQ holding

The alternate source-local runner is admitted as a lawful measured orchestration option for the next fresh FIABC court, subject to machine-level launch gates.

The qualification passed 18/18 source-free tests with:

- zero raw-source opens;
- zero survey-source hash passes during qualification;
- zero decoder calls;
- zero candidate-process launch attempts;
- zero candidate outputs;
- zero measured execution.

The qualified runner files at control head `1e701f10258831b6f453db8ad9d7ddbcba0bf247` have the same Git blob identities as the implementation exercised by the qualification:

- `FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py`: `c6549d62db847699e5dd177eafa18c87cae7cbf2`
- `FIABC_SOURCE_LOCAL_SPLIT_MERGE.py`: `51c254a3b254e84b71a6304a99eaef05ac49e919`
- `RUN_FIABC_SOURCE_LOCAL_SPLIT.sh`: `5ff364bef2ec9e315e9603877594a19834a8e39e`

Although the control checkout was dirty while qualification evidence was being assembled, the measured runner/merge/launcher bytes at the committed published head are exactly the bytes qualified. Therefore no exact-head qualification ambiguity remains.

The canonical six-cell launcher and protected execution branch remain unchanged by this admission.

## Qualified behavior

The source-split runner is admitted to execute only:

### LiTS host

`LITS_I/A -> LITS_I/B -> LITS_I/C`

### WVS host

`WVS7/A -> WVS7/B -> WVS7/C`

Each source block:

- imports governed candidate/backend/accounting/semantic machinery from exact protected execution head `3d8f2ad6...`;
- preserves exact candidate A/B/C order;
- preserves process-isolated backend law;
- preserves the single-driver lock;
- binds the selected source only;
- preserves candidate-local failure propagation;
- preserves common-source/common-court blockers;
- never executes or claims full six-cell S17;
- never performs P2 synthesis;
- emits a source-local terminal for later HQ merge/adjudication.

The merge verifier:

- requires the same protected execution head and current execution-manifest identity;
- requires compatible hardware/governed runtime;
- records macOS-version mismatch;
- rejects hardware mismatch, receipt tampering, and false S17 claims;
- preserves candidate failures and common blockers;
- never treats absolute LiTS-vs-WVS physical metrics as host-neutral;
- returns only for HQ split-court adjudication.

## Comparison law

The admissible physical-comparison units are:

- A vs B vs C within LiTS-I on the LiTS host;
- A vs B vs C within WVS7 on the WVS host.

Host is nested within source.

Absolute LiTS-vs-WVS timings/RSS/IO metrics are not treated as hardware-neutral cross-source quantities.

## Remaining launch gates

Measured launch is NOT authorized until both machines separately prove:

1. exact protected execution branch/head:
   `3d8f2ad62600b6777dcb23a28404a067502e77a0`;
2. exact source-split control head:
   `1e701f10258831b6f453db8ad9d7ddbcba0bf247`;
3. clean protected and control worktrees;
4. pinned runtime:
   CPython 3.11.3 / pyreadstat 1.3.6 / pyarrow 25.0.1 / Darwin x86_64;
5. exact canonical selected source SHA;
6. fresh persistent measured work root;
7. automatic logout disabled;
8. user-session/sleep persistence safe for a multi-hour run;
9. no prior candidate state in the measured root.

The LiTS machine does not require the WVS raw source.

The WVS machine does not require the LiTS raw source.

## Measurement boundary

Once either source-local measured block begins:

- no adaptive repair;
- no silent retry;
- no cleanup/rewrite of that work root;
- preserve a failure exactly as evidence.

A failure in one source block does not authorize patching the other block.

P2 synthesis and architecture selection remain prohibited until both source-local returns are presented to HQ and the split merge/adjudication is complete.

## Current authorization state

`WAITING_FOR_BOTH_MACHINE_BOOTSTRAP_RETURNS`

If and only if both machine-readiness returns are green, HQ may issue the final dual-machine launch order without another source-split code-qualification cycle.
