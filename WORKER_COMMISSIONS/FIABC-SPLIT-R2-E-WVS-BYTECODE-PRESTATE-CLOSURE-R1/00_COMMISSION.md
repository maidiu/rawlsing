# FIABC SPLIT R2-E — WVS JOINED BYTECODE/PRESTATE CLOSURE — R1

You are **FIABC SPLIT R2-E — WVS JOINED BYTECODE/PRESTATE CLOSURE — R1**.

Repository:

`maidiu/rawlsing`

Branch:

`agent/rabochii-fiabc-split-r2-e-wvs-bytecode-prestate-closure-r1`

Your branch is based on Worker B's exact implementation head:

`673c47ab9f158ebdd8858b3cfca7ee2295ffd01d`

Worker B branch/return:

`agent/rabochii-fiabc-split-r2-b-workroot-prestate-lock-r1`

final return terminal:

`BLOCKED__SPLIT_R2_B_WVS_JOINED_BYTECODE_CACHE_PRESTATE_NOT_EXACTLY_REPRODUCED`

Read Worker B's full return packet first.

Protected execution remains immutable for this lane:

`3d8f2ad62600b6777dcb23a28404a067502e77a0`

## SOURCE / EXECUTION LAW

SOURCE-FREE / CANDIDATE-FREE only.

Do not open/hash/decode LiTS or WVS raw files.
Do not launch Candidate A/B/C.
Do not run measured P2X.
Do not mutate protected execution in this lane.
Do not touch prior measured roots.

## PROVED ISSUE

Joined execution is serial LiTS then WVS on one court root.

LiTS can leave source-neutral Python/software prestate before WVS, including:
- R5 support source deployed under `WORK_ROOT/_be1_immutable`;
- exact owner source under `WORK_ROOT/_exact_owner_modules`;
- generated `__pycache__/*.pyc` in those namespaces;
- potentially protected-checkout import caches.

A fresh WVS-only split root/checkout may not have identical cache state.

Because WVS S01 build/open timing and T4 I/O can include imports/binding, cache presence can alter governed physical metrics.

Worker B lawfully preprovisions exact immutable SOURCE bytes but blocks on exact Python bytecode/import-cache equivalence.

## MISSION

Close this remaining physical-equivalence burden without smuggling candidate work into C0 and without hand-waving Python caches away.

### E1 — EXACT IMPORT/CACHE SURFACE

Derive the exact Python module/import surface that canonical joined LiTS can make available before WVS/A begins.

Classify every cache-producing path:

- work-root immutable support;
- work-root exact owner modules;
- protected-repo modules;
- standard/site-packages;
- any other discovered path.

For each path determine whether cache state can affect governed WVS candidate metrics.

### E2 — LAWFUL CLOSURE STRATEGIES

Evaluate in order:

1. exact source-free reproduction of joined WVS-entry cache state;
2. deterministic source-free precompilation/priming proven equivalent;
3. standardized cache-neutral execution law applied identically to joined and split future courts.

Do NOT assume strategy 2 is equivalent merely because imports get faster.

If strategy 3 requires a protected/joined-runner successor change, do not mutate protected execution here. Produce the exact required successor patch/contract for HQ or the T5 repair fan-in to adopt.

### E3 — PYC IDENTITY / VALIDITY

If using precompiled caches, prove:
- interpreter magic/version identity;
- timestamp/hash invalidation mode;
- source size/hash/mtime conditions;
- `co_filename`/path effects;
- exact destination paths;
- import acceptance without recompilation;
- no module top-level execution during C0 if candidate-free law forbids it.

If byte-for-byte identity with joined runtime-generated cache is unnecessary, prove why physical behavior is equivalent under the governed metric definitions. Otherwise fail closed.

### E4 — PROTECTED CHECKOUT CACHE STATE

Resolve protected-repo `__pycache__` separately from work-root caches.

A split WVS host using a fresh protected checkout must not receive a physical advantage/disadvantage solely because joined LiTS would have imported protected modules first.

### E5 — SOURCE-NEUTRALITY

Any prestate closure must prove:
- zero raw source access;
- zero decoder calls;
- zero candidate processes;
- zero candidate semantic output;
- no candidate durable/scratch/carrier creation;
- no LiTS projection/common-representation state;
- no oracle consumption beyond immutable authority identity if needed.

### E6 — EXACT JOINED-vs-SPLIT WVS ENTRY RECEIPT

Produce a machine-readable WVS entry-prestate receipt that compares:
- exact expected joined software prestate;
- actual split WVS prestate;
- every metric-relevant filesystem/import-cache object.

WVS measured entry must fail closed unless equivalent under the proven law.

### E7 — LITS NON-REGRESSION

LiTS split execution must not be burdened with WVS-specific priming that changes LiTS metrics.

### E8 — WORKER B REPAIRS RETAINED

Preserve and requalify Worker B's already-implemented:
- worktree lock;
- combined import gate;
- pair compatibility;
- postrun dirty verification;
- immutable source preprovision;
- source-hash sequence law.

### E9 — FUTURE JOINED RUNNER PARITY

If the only scientifically clean solution is to normalize Python cache state for BOTH joined and split execution, return that conclusion explicitly with:
- exact code surface;
- exact environment/control change;
- exact expected physical effect classification;
- qualification burden.

Do not force a fake split-only parity.

## QUALIFICATION

Source-free only:
- raw source opens 0
- source hash passes 0
- decoder calls 0
- candidate process launches 0
- candidate outputs 0
- measured execution false

Actual CPython 3.11.3 cache behavior tests are strongly preferred.

## RETURN

Return under:

`WORKER_RETURNS/FIABC-SPLIT-R2-E-WVS-BYTECODE-PRESTATE-CLOSURE-R1/`

Required:
- 00_RETURN.md
- RETURN.json
- exact import/cache inventory
- pyc equivalence analysis
- joined-vs-split WVS entry-prestate contract
- chosen closure strategy
- source-free hostile tests
- implementation hash table
- exact implementation head

Success only if WVS physical prestate equivalence is actually closed:

`PASS__SPLIT_R2_E_WVS_BYTECODE_PRESTATE_EQUIVALENCE__READY_FOR_FANIN`

Otherwise:

`BLOCKED__SPLIT_R2_E_WVS_BYTECODE_PRESTATE_EQUIVALENCE_REMAINS`
