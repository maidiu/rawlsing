# FIABC Source-Split Global-Assumption Stay — R1

Status:

`MEASURED_RELAUNCH_STAY__GLOBAL_SPLIT_ASSUMPTION_CLOSURE_REQUIRED`

Decision:

`HQD-2026-09-25-099`

Closure commission branch:

`agent/vozhd-fiabc-source-split-global-assumption-closure-r1`

Commission commit:

`f703d9e9b4c572622338baea36d36bce3110366d`

Commission:

`WORKER_COMMISSIONS/FIABC-SOURCE-SPLIT-GLOBAL-ASSUMPTION-CLOSURE-R1/00_COMMISSION.md`

## Observed RUN5 LiTS defect

The source-local runner reused the full-court `ProgressReporter`.

The current full-court manifest begins its progress universe at:

`LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD`

while the fresh source-local LiTS runner reconstructs:

`LITS_I/A/S00_SOURCE_PREFLIGHT_IDENTITY`

first.

The inherited progress plan excludes that pre-cursor address and throws before candidate work.

RUN5 LiTS is therefore pre-candidate split-orchestration failure evidence, not candidate evidence.

## Wider split-specific risk classes now under mandatory closure

1. full-court progress cursor reused in a source-local stage universe;
2. source-local traversal versus global next-stage graph equivalence;
3. source-cut correctness and S17 exclusion;
4. candidate failure and common blocker propagation across a partitioned court;
5. exact qualified control-runner binding;
6. protected backend live writes to repo-local `WORKER_RETURNS/EE-P2X/LOCAL_COURT` despite source-local work roots;
7. proof that mutable repo-local live evidence is not a cross-source input;
8. portable post-terminal binding of source-local repo evidence;
9. orchestration-failure receipts for nonzero driver exits;
10. merge verification of actual ledger/receipts/source SHA rather than only a self-hashed source terminal;
11. merge validation of source-local-only / no-S17 / no-synthesis flags;
12. merge control-runner compatibility;
13. actual-protected-manifest integration tests instead of FakeProgress-only qualification;
14. prior-root immutability and no-resume law.

No further source-split measured relaunch is authorized until the closure terminal is green and HQ promotes it.

Any WVS RUN5 process that was already running before the stay is not to be killed or modified. Let it reach its natural terminal, preserve the evidence, and defer admissibility.
