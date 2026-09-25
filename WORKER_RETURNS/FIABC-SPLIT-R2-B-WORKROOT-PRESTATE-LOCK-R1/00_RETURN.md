# FIABC SPLIT R2 — Worker B Return

## Terminal

`BLOCKED__SPLIT_R2_B_WVS_JOINED_BYTECODE_CACHE_PRESTATE_NOT_EXACTLY_REPRODUCED`

This is a deliberate fail-closed return, not a failure to complete the assigned investigation. Worker B closed the worktree-lock, combined-runtime, pair-readiness, exact-HEAD/postrun-delta, and source-byte prestate defects in alternate split control. The remaining P6 defect is narrower and dispositive: **joined LiTS can leave Python bytecode/import-cache software state that changes later WVS S01 measured build/open work, and the current source-free prestate does not exactly reproduce that state.**

Do not promote this return to `PASS__SPLIT_R2_B_WORKROOT_PRESTATE_LOCK__READY_FOR_FANIN` merely because the other gates are implemented.

## Immutable context

- Common base: `e1b82095c83dd15a64b409dba0e4ae7d4f4460c6`
- Worker commission: `0b0f284b952869f828660aa47c45cd174ae89358`
- Worker branch: `agent/rabochii-fiabc-split-r2-b-workroot-prestate-lock-r1`
- Protected execution branch: `agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`
- Protected execution head: `3d8f2ad62600b6777dcb23a28404a067502e77a0`
- Protected execution modified: **NO**
- Implementation/test head before documentary return commits: `673c47ab9f158ebdd8858b3cfca7ee2295ffd01d`

Implementation blobs at that head:

- `HQ_HANDOFF/launchers/FIABC_SPLIT_R2_WORKROOT_GATES.py` — `ad202e936923113b8fcf55b6ebc413f1060146a2`
- `HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py` — `700cdb38f1ce241e3f97486f352654e9656f0157`
- `HQ_HANDOFF/launchers/RUN_FIABC_SOURCE_LOCAL_SPLIT.sh` — `70c6a70d9257989b0531060470354f9c3d5f05ac`
- `rawlsing_next/tests/test_fiabc_split_r2_b_workroot_gates.py` — `118894b9caadbbe11352431b31a1a7cb4b43f293`

## What Worker B established and changed

### P5 — cross-source work-root residual state

The split helper now treats WVS joined-prestate reproduction as a C0 source-free operation. It can prepopulate only the exact immutable source bytes that joined LiTS would already have materialized before WVS:

- four R5 support modules absent from the protected checkout under `_be1_immutable/<owner-commit>/rawlsing_next/`;
- exact A/B/C owner source bytes under `_exact_owner_modules/<owner-commit>/<candidate>/`.

The helper verifies the Git blob identity before writing and then requires the two allowed prestate namespaces to contain **exactly** the expected file set—no extra file is admissible.

It explicitly forbids preprovision of:

- `_be1_lits_projection`
- `_lits_common_representation`
- `cells`

Thus no LiTS semantic projection, common representation, candidate carrier, candidate durable state, or candidate receipt is smuggled into WVS C0.

See `14_CROSS_SOURCE_WORKROOT_RESIDUAL_STATE.json`.

### P7 — worktree-safe single-driver lock

The prior source-local code used `WORK_ROOT` as the lock namespace whenever `.git` was a file, which is the ordinary linked-worktree case. That made two distinct roots capable of running against one protected checkout concurrently even though the backend writes repo-local live evidence.

The driver now resolves the exact Git worktree administrative directory with:

`git rev-parse --path-format=absolute --git-dir`

and gives that directory to the protected `DriverInstanceLock`. Lock identity is therefore a function of the protected checkout/worktree, not the external measurement root.

A hostile linked-worktree double-lock fixture is banked.

See `16_WORKTREE_LOCK_CLOSURE.json`.

### P8/P9 — legitimate dirty post-run checkout

Preflight and measured-run entry still require an exact clean protected checkout.

Post-terminal `--verify-only` no longer treats all dirt as equivalent. Before measurement, the split driver records:

- exact protected branch/head;
- exact HEAD live-evidence tree using Git object bytes, including tracked baseline files that already exist;
- filesystem live-evidence state;
- all ignored-file state.

After the run, only the following are admissible:

- selected-source live evidence;
- tightly classified selected-source common-court administration;
- Python `__pycache__/*.pyc` deltas as non-evidentiary runtime byproducts.

The following fail closed:

- governed code/config mutation;
- nonselected-source live evidence;
- arbitrary ignored/untracked files;
- rename/copy mutation;
- evidence deletion;
- anything outside the classified live-evidence surface.

See `17_POSTRUN_DIRTY_CHECKOUT_VERIFICATION.json`.

### P10 — combined import/ABI gate

The launcher no longer accepts dependency metadata alone. Before measurement, one interpreter must jointly import:

- `pyreadstat==1.3.6`
- `pyarrow==25.0.1`
- `pandas==2.3.1`
- `numpy==2.3.2`

under:

- CPython `3.11.3`
- Darwin
- `x86_64`

A hostile fixture makes metadata report the pinned versions while `pyarrow` import fails; the expected result is a pre-candidate block.

### P11 — prelaunch machine-pair compatibility

The launcher now supports source-free machine readiness before `SOURCE_PATH` is even required. Each readiness receipt binds:

- assigned source and canonical source SHA identity;
- exact fresh `WORK_ROOT`;
- protected branch/head;
- qualified split-control head and launcher/driver/helper bytes;
- combined runtime;
- hardware model;
- CPU brand;
- actual `hw.memsize`;
- architecture;
- macOS version.

The pair verifier requires exact runtime/protected-control/hardware identity and exact LITS/WVS assignment before either measured launch is admitted. macOS-version mismatch is recorded separately under existing host-within-source law; the verifier does **not** authorize absolute cross-source physical comparison.

Each measured host revalidates its own readiness, pair membership, control bytes, hardware, runtime, and exact work-root identity before the first raw-source SHA pass.

See `18_PRELAUNCH_PAIR_COMPATIBILITY.json`.

### P12 — raw-source access/hash sequence

Worker B itself performed **zero** raw-source opens, hashes, or decodes and launched **zero** candidate processes.

Documentary code tracing establishes the same selected-source administrative sequence for joined and split paths:

1. launcher SHA-only pass;
2. separate preflight-driver `ensure_source_verified` pass;
3. separate measured-driver `ensure_source_verified` pass before the first empirical stage.

That is three SHA-only passes per selected source and zero decoder calls before candidate execution in both paths. Readiness and C0 prestate are source-free and add no raw-source access.

See `19_SOURCE_ACCESS_HASH_SEQUENCE.json`.

## Dispositive P6 blocker — Python import-cache prestate

The protected process envelope proves that candidate **in-memory** module/session state does not cross source×candidate boundaries: each cell gets a fresh child process.

That does **not** eliminate filesystem software-cache inheritance.

During joined LiTS measured execution:

1. LiTS can deploy R5 source modules into `WORK_ROOT/_be1_immutable`.
2. LiTS can deploy and import exact owner modules under `WORK_ROOT/_exact_owner_modules`.
3. Those imports can create persistent `__pycache__/*.pyc` files in those work-root namespaces.
4. Imports of protected dependencies can also create ignored `REPO/rawlsing_next/**/__pycache__/*.pyc` files.
5. The later joined WVS child is a fresh process, but it can consume those filesystem bytecode caches.

This matters because protected WVS S01 executes `_bind` under the governed `build_or_open_wall_ns` measurement, and that bind path imports R5 support / exact owner / protected support modules. Therefore a pre-existing valid bytecode cache can remove source-compilation work **inside a governed WVS physical metric**.

The source-byte C0 repair closes first-deployment source writes, but it does not close that compile-cache asymmetry.

Worker B did not fabricate a bytecode snapshot. An exact joined cache is runtime-generated and depends on path/mtime/import closure; importing candidate-owner code merely to create it would violate the candidate-free character of this lane, while precompiling a synthetic deterministic cache has not been proven physically equivalent to the canonical joined cache path.

Accordingly the implementation now records:

`BLOCKED__JOINED_LITS_GENERATED_PYTHON_BYTECODE_CACHE_NOT_REPRODUCED`

for WVS joined prestate, and `verify_joined_prestate` rejects WVS measured entry unless a later qualified control proves:

`joined_import_cache_state == EXACTLY_REPRODUCED`

This is the remaining exact blocker.

See `15_SOURCE_HOST_HISTORY_EQUIVALENCE_LIMITS.json`.

## Test/qualification truth

Hostile tests are banked in:

`rawlsing_next/tests/test_fiabc_split_r2_b_workroot_gates.py`

They cover the lock, ABI/import gate, pair hardware mismatch, prestate namespace closure, tracked-HEAD/live-evidence distinction, nonselected-source evidence, governed-code mutation, arbitrary ignored files, and launcher ordering.

**They were not executed in this worker lane.** The branch has no CI/check run that executes this new test file; the commission forbids use of the user's Mac, and this browser/GitHub lane had no permitted remote Python execution surface. No test PASS is claimed.

See `20_STATIC_QUALIFICATION.json`.

## Fan-in law

The dedicated integration branch is:

`agent/vozhd-fiabc-split-r2-fanin-r1`

Worker B did **not** mutate it.

Fan-in may inspect or integrate the noncontroversial control repairs, but it must not classify Worker B green or authorize fresh WVS split measurement until the P6 bytecode/import-cache software-prestate burden is independently closed.

The exact Worker-B terminal remains:

`BLOCKED__SPLIT_R2_B_WVS_JOINED_BYTECODE_CACHE_PRESTATE_NOT_EXACTLY_REPRODUCED`
