# FIABC SOURCE-SPLIT GLOBAL-ASSUMPTION CLOSURE — SECOND-PASS JOINED-RUNNER DIFFERENTIAL PARITY ADDENDUM

This addendum is MANDATORY and cumulative with `00_COMMISSION.md`.

No success terminal is lawful unless every burden below is closed for BOTH `LITS_I` and `WVS7`.

The governing question is stricter than "does the split runner run":

> For each source independently, does the split path reproduce the joined runner's lawful candidate-relevant A→B→C behavior, lifecycle, accounting, oracle gates, process isolation, filesystem preconditions, and terminal semantics, with every unavoidable difference caused by cutting the court explicitly classified as non-candidate / non-evidentiary / source-local administration?

Do not accept "tests pass" unless the tests use the actual protected manifest and actual protected orchestration objects wherever possible.

## P1 — EXACT JOINED-vs-SPLIT TRACE MODEL FOR BOTH SOURCES

Construct a machine-readable differential trace from the exact protected manifest at:

`3d8f2ad62600b6777dcb23a28404a067502e77a0`

For each source, enumerate:

- stages materialized during joined preflight;
- stages executed/materialized during joined measured `--run`;
- source-local preflight materialization;
- source-local measured-block materialization;
- disposition of each stage;
- candidate-process start/stop boundary;
- whether source bytes are available to the stage;
- whether physical-host measurement is required;
- next-stage-on-pass;
- next-stage-on-candidate-failure;
- whether the stage is mechanical/non-measured.

Required exact current-manifest facts to bind:

1. `LITS_I/A/S00_SOURCE_PREFLIGHT_IDENTITY` is before global `first_unfinished` and is materialized by joined `bind_initial_manifest_prefix()` during preflight.
2. A lawful split must NOT move that preserved LiTS S00 into candidate-relevant measured behavior merely to avoid the ProgressReporter crash.
3. The joined all-PASS graph contains 50 LiTS stages during measured run; LiTS/A/S00 is the preflight mechanical prefix.
4. The joined all-PASS graph contains 50 WVS stages but skips `WVS7/C/S00_SOURCE_PREFLIGHT_IDENTITY` while current terminal law still expects complete WVS/C stage closure.
5. The WVS C/S00 discrepancy must be explicitly adjudicated as a latent joined-control mechanical gap, not silently hidden by source-local list traversal.
6. Any source-local extra node relative to joined graph must be proven non-executable, non-measured, semantically required, and incapable of changing candidate physical state.

Produce:
`11_JOINED_SPLIT_DIFFERENTIAL_TRACE.json`

## P2 — MECHANICAL PREFIX / PRESERVED-STAGE PLACEMENT LAW

For each source, derive which preserved/skipped stages must exist BEFORE the first executable candidate stage.

Prove that moving a mechanical stage between preflight and measured orchestration cannot alter:

- candidate scratch/durable state;
- source-open/decode/reread counters;
- T4 candidate metrics;
- process start mode;
- oracle state;
- candidate process warm state.

LiTS/A/S00 must match joined preflight semantics.

WVS/C/S00 must receive a specific lawful placement decision with evidence.

Do not merely suppress progress telemetry for pre-cursor stages.

## P3 — PROCESS-ISOLATION LIFECYCLE DIFFERENTIAL

Use the actual protected `ProcessIsolationController` behavior source-free.

For both LiTS and WVS prove:

- exactly one main candidate process at a time;
- no A→B, B→C, LiTS→WVS, or failure edge retains a candidate process;
- same-cell retention occurs only for exact authorized adjacent lifecycle transitions;
- candidate-local failure stops the failed candidate process before later candidates;
- common-source and common-court blocker stop behavior is identical to joined law;
- S15 fresh-process replay child creation/attribution is unchanged by source splitting;
- source-local cutting cannot cause foreign-candidate warm-state inheritance.

Add actual-object hostile tests, not FakeBackend-only assertions.

Produce:
`12_PROCESS_LIFECYCLE_DIFFERENTIAL.json`

## P4 — T5 SOURCE-LOCAL DEPENDENCY GRAPH

Prove the live T5 dependency graph before S17.

Required findings must be mechanically demonstrated:

- A and B S05 oracle matches consume only their own source/candidate observation + that source's frozen oracle.
- C S05 three-way parity consumes A/B/C observations for the SAME source only.
- S16 cell terminal consumes the current cell's T4/accounting/observation/match + current source freeze/manifest law.
- Cross-source live output is first required only by full-court S17/final composition, which the split runner must not execute.

Then hostile-test failure paths:

- A fails before S05, B/C continue;
- B fails before S05, C continues;
- A or B fails after S05;
- C fails before/at/after S05.

If current protected T5 C-three-way logic crashes because an earlier candidate-local failure leaves a missing A/B observation, classify that precisely as a PRE-EXISTING JOINED-RUNNER FAILURE-PATH DEFECT, not a split defect.

Do not hide it with a fake T5 layer. Either:
- prove joined law actually handles it; or
- return a separate protected-code repair requirement before any claim that A/B/C candidate-local failure paths are robust.

Produce:
`13_T5_SOURCE_LOCAL_DEPENDENCY_AND_FAILURE_PATHS.json`

## P5 — CROSS-SOURCE WORK-ROOT RESIDUAL STATE

Inventory every path outside `WORK_ROOT/cells/<source>/<candidate>` that candidate execution may read or create.

At minimum inspect:

- `_be1_immutable`
- `_exact_owner_modules`
- `_be1_lits_projection`
- `_lits_common_representation`
- court/oracle state
- global progress/ledger state
- any other dynamically discovered global path.

Important exact current-state fact:

Four of the five R5 support modules used by `_ensure_r5` are absent from the protected checkout and are deployed under top-level `WORK_ROOT/_be1_immutable` on first use. `_deploy` records first-time writes through T4 when active.

In the joined court, LiTS/A runs before WVS/A and can leave those immutable bytes present. A WVS-only fresh work root may therefore charge first-time immutable deployment writes/time to WVS/A that joined WVS/A would not pay.

Likewise exact-owner modules are deployed under top-level `_exact_owner_modules`; joined LiTS can prepopulate A/B/C owner bytes before WVS, whereas a WVS-only work root begins empty.

This is a critical source-split measurement-equivalence burden.

For every global residual object classify:

- immutable candidate-neutral support;
- source-local semantic state;
- candidate-specific state;
- evidentiary output;
- administrative output.

Then prove one of:

A. no candidate metric can differ due to its presence/absence; OR
B. source-local pre-state must reproduce the exact joined-court state before selected-source measurement; OR
C. split measurement is not physically equivalent and must remain blocked.

Do not invent ad hoc normalization after measurement.

If pre-provisioning is the lawful solution, it must:
- be source-free;
- occur before candidate measurement;
- reproduce exact bytes/identities;
- be explicitly C0/non-candidate;
- be verified not to seed semantic/candidate state;
- be identical and deterministic;
- not hide candidate-owned build cost.

Produce:
`14_CROSS_SOURCE_WORKROOT_RESIDUAL_STATE.json`

## P6 — SOURCE-HOST HISTORY / CACHE-STATE DIFFERENCE

Compare joined and split prehistory:

Joined canonical launcher:
- hashes LiTS and WVS;
- full preflight verifies both;
- LiTS runs first;
- WVS begins only after the whole LiTS block.

Split:
- each host verifies only its selected raw source;
- WVS may begin without prior LiTS workload on that host.

Determine whether this can materially alter any governed within-source physical metric through:
- filesystem cache state;
- immutable support prepopulation;
- thermal/process history;
- repo object/cache state.

Distinguish:
- software state that MUST be reproduced for measurement equivalence;
- unavoidable host-history/environmental difference already covered by "host nested within source" law.

Be explicit: a two-host split cannot claim identical absolute physical host history to a serial one-host joined court.

The closure may still admit within-source A/B/C comparison only if it proves the remaining environmental difference does not violate the intended source-local comparison law.

Produce:
`15_SOURCE_HOST_HISTORY_EQUIVALENCE_LIMITS.json`

## P7 — WORKTREE-SAFE SINGLE-DRIVER LOCK

Current split code chooses:

`repo_root/.git` only when it is a directory, otherwise `WORK_ROOT`.

In a Git worktree, `.git` is normally a file. Therefore two different work roots can acquire two different locks while sharing the same protected checkout, even though the backend writes repo-local live evidence.

Close this.

The lock must bind to the actual protected checkout/Git worktree administrative identity independent of external work root.

Use a path such as the exact Git worktree dir returned by Git, not a candidate/source work root.

Hostile test:
- two source-local runners with distinct work roots but same protected checkout;
- second must fail lock acquisition.

Also prove independent protected checkouts on separate machines remain independent.

Produce:
`16_WORKTREE_LOCK_CLOSURE.json`

## P8 — POST-RUN VERIFICATION ON A LEGITIMATELY DIRTY PROTECTED CHECKOUT

The backend legitimately writes:
- tracked/untracked live evidence under `WORKER_RETURNS/EE-P2X/LOCAL_COURT`;
- Python cache files during measured execution.

Current `_require_exact_execution_checkout` rejects any dirty checkout before all modes, including `--verify-only`.

Prove that successful post-run source-local verification/portable closure is actually executable.

Implement mode-aware law:

- preflight/run require exact clean checkout;
- post-terminal verification may accept only a precisely bound expected mutation set produced by that source-local run;
- any governed code/config mutation still fails closed;
- nonselected-source live evidence mutation fails;
- arbitrary untracked files fail unless explicitly classified non-evidentiary runtime byproduct.

Do not simply disable cleanliness checking.

Produce:
`17_POSTRUN_DIRTY_CHECKOUT_VERIFICATION.json`

## P9 — REPO-LOCAL LIVE EVIDENCE BASELINE VERSUS TRACKED BASELINE FILES

Fresh protected clones already contain tracked baseline JSONs under `EE-P2X/LOCAL_COURT/cells`.

The source-local evidence-delta mechanism must distinguish:
- repository baseline at exact protected HEAD;
- modified tracked live-evidence files;
- newly created live-evidence files;
- Python caches;
- governed source-code/config changes.

Hash the exact HEAD baseline directly from Git, not from assumptions about an empty directory.

A source-local terminal/closure must prove every modified/new live evidence object belongs to the selected source or approved source-neutral administration.

## P10 — COMBINED IMPORT / ABI RUNTIME GATE

Version metadata alone is not enough.

Before measured entry the launcher must prove the exact runtime can jointly import:

`pyreadstat, pyarrow, pandas, numpy`

under:
- CPython 3.11.3
- pyreadstat 1.3.6
- pyarrow 25.0.1
- pandas 2.3.1
- numpy 2.3.2

Add a hostile fixture where package metadata reports the pinned versions but a combined import fails. Launch must stop before candidate execution.

## P11 — PRE-LAUNCH PAIR COMPATIBILITY GATE

Do not wait until post-run merge to discover the two machines are incompatible.

Before either fresh dual-host court is authorized, produce two source-free machine readiness receipts and an HQ/pair verifier that checks:

- hardware model;
- CPU brand;
- physical memory;
- architecture;
- exact runtime tuple;
- exact protected head;
- exact qualified split-control implementation;
- assigned source;
- canonical source SHA;
- fresh work-root state.

macOS-version mismatch remains separately recorded under existing law.

The pair verifier must fail before measurement on incompatible hardware/runtime.

This is especially important because earlier human descriptions of the two Macs' memory configuration were not authoritative; use actual `hw.memsize`, not prose.

Produce:
`18_PRELAUNCH_PAIR_COMPATIBILITY.json`

## P12 — EXACT SOURCE ACCESS / HASH SEQUENCE

For joined and split paths, count and order all pre-candidate:
- source SHA passes;
- source file opens;
- decoder calls.

Do this separately for LiTS and WVS.

Prove that source-local orchestration does not add a source decode or candidate-semantic read before the joined runner would.

Hash-only preflight reads must be classified as court administration and excluded from candidate metrics exactly as joined law intends.

Any difference that can warm the selected source differently must be surfaced in P6, not ignored.

## P13 — FULL SOURCE-SPECIFIC STAGE MATRIX

Produce an exact 102-stage current-manifest table (51 LiTS + 51 WVS) containing:

- source;
- candidate;
- stage;
- disposition;
- joined placement: PREFLIGHT / MEASURED_RUN / GLOBAL_GRAPH_SKIPPED;
- split placement;
- empirical source access flag;
- physical measurement flag;
- candidate process involved yes/no;
- expected terminal disposition in all-pass case;
- pass next edge;
- candidate-failure next edge.

Every row must be accounted for.

This is the primary "nothing fell through the split" artifact.

Produce:
`19_EXACT_102_STAGE_PARITY_MATRIX.json`

## P14 — DIFFERENTIAL ORCHESTRATION SIMULATOR

Create a source-free differential simulator/test harness using the ACTUAL protected:
- StateMachine;
- StageSpec;
- StageLedger mechanics;
- process-envelope policy objects where feasible;
- current manifest.

Run two models:

1. joined runner through the selected source segment;
2. split runner through the same source.

Feed deterministic fake backend results but DO NOT replace protected orchestration helpers with FakeBase/FakeProgress.

For both LiTS and WVS compare:

- candidate backend call addresses;
- StageContext identities;
- source_path presence/absence;
- candidate root paths modulo source-local root prefix;
- process start/stop boundaries;
- mechanical terminal dispositions;
- T4 accounting stage addresses;
- candidate terminal dispositions;
- oracle-match dependency set;
- terminal stage inventory.

Required scenarios per source:
- all pass;
- A fails at S01;
- A fails at S05;
- A fails at S16;
- B fails at S01;
- B fails at S05;
- B fails at S16;
- C fails at S01;
- C fails at S05;
- C fails at S16;
- common-source blocker at early/middle/late;
- common-court blocker at early/middle/late.

Any differential beyond explicitly approved source-cut administration is a blocker.

## P15 — WVS RUN5 CONSERVATION BURDEN

If WVS RUN5 reaches a natural terminal under control `4f0ee6...`, do not automatically discard or accept it.

The compatibility analysis must answer:

- Did it encounter any defect repaired by this closure?
- Did it pay split-only global immutable/owner deployment costs that joined WVS would not?
- Can those costs be shown excluded from the governed physical vector, or are its physical metrics contaminated?
- Did it create WVS/C/S00 mechanically, and was that lawful?
- Are all repo-local artifacts still available and hash-bindable?
- Can its evidence be packaged and reverified under the strengthened portable closure without mutation?

If any measured metric was changed by source-split-only pre-state, WVS RUN5 is void for physical candidate comparison even if semantically terminal.

## P16 — SUCCESS CRITERION UPGRADE

The closure terminal:

`PASS__SOURCE_SPLIT_GLOBAL_ASSUMPTION_HOSTILE_CLOSURE__HQ_PROMOTION_REQUIRED`

is lawful only if BOTH source runners are demonstrated end-to-end source-free against the exact protected contract.

The final return must contain two explicit verdicts:

- `LITS_SPLIT_RUNNER_EQUIVALENT_TO_JOINED_SOURCE_SEGMENT__PASS`
- `WVS7_SPLIT_RUNNER_EQUIVALENT_TO_JOINED_SOURCE_SEGMENT__PASS`

"Equivalent" means candidate-relevant semantic, lifecycle, accounting, measurement, and terminal law; administrative differences must be enumerated and proved non-evidentiary.

If either cannot be proved:

`BLOCKED__SOURCE_SPLIT_GLOBAL_ASSUMPTION_REMAINS`

No measured retry.
