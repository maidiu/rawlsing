# FIABC Source-Split Alternate Runner — R1

Status:

`SOURCE_FREE_QUALIFICATION_BANKED__HQ_LAUNCH_AUTHORIZATION_PENDING`

This alternate path exists so LiTS-I and WVS7 may be measured concurrently on two materially equivalent Macs without modifying the already-qualified canonical six-cell launcher or protected execution code.

## Non-mutation guarantee

This work lives only on:

`agent/vozhd-fiabc-source-split-alternate-runner-r1`

Base PRE-MAIN at creation:

`0fe82197f3ec6476f165d1404870209870e7fa57`

Protected execution remains:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

at:

`3d8f2ad62600b6777dcb23a28404a067502e77a0`

The canonical qualified launcher remains untouched:

`HQ_HANDOFF/launchers/RUN_DISPOSITIVE_FIABC_SIX_CELL.sh`

The alternate files are:

- `HQ_HANDOFF/launchers/RUN_FIABC_SOURCE_LOCAL_SPLIT.sh`
- `HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py`
- `HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_MERGE.py`

## Execution design

One source-local invocation owns exactly one source block:

### LiTS machine

`LITS_I/A -> LITS_I/B -> LITS_I/C`

### WVS machine

`WVS7/A -> WVS7/B -> WVS7/C`

Each block:

- runs against exact protected execution head `3d8f2ad62600b6777dcb23a28404a067502e77a0`;
- consumes the unchanged full current six-cell execution manifest and T5 court contract;
- consumes the unchanged T3/STOP/oracle freeze;
- runs the unchanged exact process-isolated backend;
- uses the unchanged governed stage definitions and per-cell next-stage identities;
- preserves exact candidate process isolation and T4/T5 per-cell terminal machinery;
- owns a fresh persistent work root;
- requires zero candidate state before measured execution;
- does not execute the full six-cell S17 verifier;
- cannot claim P2 synthesis or architecture selection.

The source-local driver is court administration only. It imports all candidate/backend/accounting/semantic code from the exact protected execution checkout and verifies that checkout's branch/head/cleanliness before proceeding.

## Source law

Each machine needs only the selected raw source carrier:

- LiTS machine: exact canonical LiTS-I DTA;
- WVS machine: exact canonical WVS7 SAV.

Both machines still bind the complete frozen T3/STOP/oracle documents from Git. The non-local raw survey carrier is not required or opened.

The selected source SHA is verified before measured execution.

## Host law

The intended deployment is one physically equivalent Mac per source.

The source-local terminal records:

- governed runtime fingerprint;
- macOS version;
- hardware model;
- CPU brand;
- physical memory bytes;
- exact execution head;
- source SHA;
- runner/control identity.

The merge verifier requires identical:

- hardware model;
- CPU brand;
- memory;
- Python implementation/version;
- Darwin/x86_64 architecture;
- pyreadstat/pyarrow versions.

macOS version is recorded separately and may differ.

A macOS mismatch does **not** invalidate within-source A/B/C comparison because all three candidates for a source execute on the same machine. However the split design never admits absolute LiTS-vs-WVS physical timing as host-neutral, even when macOS versions match.

The admissible physical comparison unit is:

`A vs B vs C within one source`.

HQ later synthesizes the two source-local comparisons.

## Merge law

The merge verifier accepts exactly:

- one LiTS source-local terminal;
- one WVS source-local terminal.

It verifies:

- same protected execution head;
- same full current execution-manifest identity;
- exact A/B/C order in each source;
- compatible hardware/governed runtime;
- no source-local S17 overclaim;
- no pre-merge P2 synthesis;
- candidate-local failures and common blockers remain explicit.

Its positive terminal is only:

`READY_FOR_HQ_SPLIT_COURT_ADJUDICATION`

It does **not** emit or counterfeit:

`COURT_SEQUENCE_COMPLETE__S17_VERIFIED`

and does not authorize P2 itself.

## Current measured-use status

The dedicated source-free qualification is banked at:

`WORKER_RETURNS/FIABC-SOURCE-LOCAL-SPLIT-SOURCE-FREE-QUALIFICATION-R1/`

It exercised the alternate orchestration with synthetic manifests, temporary receipts, and fake backends. It did not open or hash LiTS-I/WVS7, decode survey data, create candidate outputs, launch candidate processes, execute S17, or authorize P2 synthesis. Its positive terminal qualifies this runner implementation only.

Do not run measured source-local A/B/C until HQ reviews this return and issues explicit measured-use authorization.

The banked qualification covers at minimum:

1. Python/shell syntax and packaging;
2. exact protected-module import provenance;
3. single-driver lock preservation;
4. selected-source-only raw-source access;
5. zero candidate state after source-local preflight;
6. exact stage ordering A->B->C within each source;
7. Candidate A/B/C process lifecycle equivalence to the canonical driver;
8. per-cell T4/T5 terminal equivalence;
9. proof that S17 cannot execute from the alternate runner;
10. common-source/common-court blocker preservation;
11. candidate-local failure propagation;
12. merge positive/negative fixtures, including OS-version mismatch;
13. byte identity of the canonical six-cell launcher before and after this branch.

Until HQ reviews the banked return and issues explicit measured-use authorization, this branch remains a qualified alternate runner without measured-court authorization.
