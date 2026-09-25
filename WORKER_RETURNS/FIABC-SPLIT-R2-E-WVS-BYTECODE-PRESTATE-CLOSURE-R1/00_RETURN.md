# FIABC SPLIT R2-E — WVS JOINED BYTECODE/PRESTATE CLOSURE — RETURN

## Terminal

`BLOCKED__SPLIT_R2_E_WVS_BYTECODE_PRESTATE_EQUIVALENCE_REMAINS`

Worker E found a real physical-equivalence solution, but it is **not lawful to mark the present split green**. The solution requires a new cache-neutral measurement law to be adopted identically by the joined runner and split runner. Current protected execution at `3d8f2ad62600b6777dcb23a28404a067502e77a0` does not use that law.

Worker E did not mutate protected execution and did not weaken Worker B's fail-closed WVS gate.

## Provenance

- Branch: `agent/rabochii-fiabc-split-r2-e-wvs-bytecode-prestate-closure-r1`
- Commission: `2f813045ffec137b8a3f48d1294245e88a0d49be`
- Exact parent / Worker B implementation head: `673c47ab9f158ebdd8858b3cfca7ee2295ffd01d`
- Worker E exact implementation head: `3b3529133da5e92bba41b357464b501af9580675`
- Protected execution: `3d8f2ad62600b6777dcb23a28404a067502e77a0`
- Protected execution modified: **NO**

## The decisive finding: exact current joined cache replay is not source-free derivable

Worker B was right to stop rather than guess.

Canonical joined LiTS can create valid Python bytecode caches in:

- `WORK_ROOT/_be1_immutable/**/__pycache__`
- `WORK_ROOT/_exact_owner_modules/**/__pycache__`
- `REPO/rawlsing_next/**/__pycache__`
- source-backed standard/site-package cache trees.

Those can later eliminate source compilation inside WVS candidate work.

But there is no single statically derivable cache snapshot to reproduce. The exact witness is `pre553_r5_seam.py`: its R5 batch normalization imports NumPy only when an actual physical batch satisfies `_all_finite_floats(batch)`. Whether that import occurs is therefore a function of raw LiTS physical values. This court is forbidden to inspect those values.

The current split readiness path introduces a second asymmetry: Worker B's strengthened combined ABI gate imports `pyreadstat`, `pyarrow`, `pandas`, and `numpy` before measurement, while the canonical joined runtime gate does not execute the identical import sequence. So even “fresh checkout” does not define a common software-cache prehistory.

See `01_EXACT_IMPORT_CACHE_INVENTORY.json`.

## Why `compileall` is not the answer

A blanket precompile is not joined equivalence. It can create a cache superset for modules joined LiTS never imported, handing split WVS compile-elision that the joined WVS segment did not necessarily have.

A selective precompile has the inverse problem: the realized import set is partly data-dependent. It also inherits exact pyc burdens—interpreter version/magic, invalidation mode, source metadata, destination/path and code-object filename semantics. Import-priming exact owners to discover the set would execute top-level candidate code in C0.

Worker E therefore rejects both exact-snapshot fabrication and “compile it all and hope.”

See `02_PYC_EQUIVALENCE_ANALYSIS.json`.

## The real closure: remove pyc state from measurement

The scientifically clean successor law is:

```
PYTHONDONTWRITEBYTECODE=1
PYTHONPYCACHEPREFIX=<WORK_ROOT>/court/_python_cache_neutral_prefix
RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR=1
```

with the alternate prefix created empty and required to have **zero descendants** before, between, and after candidate execution.

This is not cosmetic. Under CPython, `sys.pycache_prefix` moves cache lookup as well as cache output away from ordinary source-tree `__pycache__`. With an empty alternate prefix, existing work-root/repo/site-package pycs cannot be consumed. `PYTHONDONTWRITEBYTECODE=1` prevents the first candidate from seeding that prefix for later candidates.

The protected process envelope already copies the parent's environment before starting the main candidate child. S15 starts its fresh replay child without an `env=` override, so it inherits the same environment. A successor should receipt-bind those facts rather than leave them implicit.

Worker E banked the successor-only control at:

`HQ_HANDOFF/launchers/FIABC_PYTHON_CACHE_NEUTRALITY_SUCCESSOR.py`

It deliberately refuses to convert a split receipt into parity unless a joined successor identity is bound.

See `04_CHOSEN_CLOSURE_STRATEGY.json` and `05_SUCCESSOR_REQUIRED_PATCH.md`.

## Why the terminal is still BLOCKED

This cache-neutral law changes physical measurement conditions. Current joined WVS can sometimes consume warmed bytecode; the successor forbids that and forces source compilation in each fresh candidate process. Candidate wall/CPU/RSS and S01/build-open costs can therefore change.

So the scientifically valid move is a **new shared physical-measurement epoch**, not a split-only patch:

1. adopt the cache-neutral environment on the future joined six-cell launcher;
2. adopt the identical law on the split source-local launcher;
3. add process-envelope and S15 cache-law attestations;
4. repeat source-free qualification under exact CPython 3.11.3;
5. then remeasure future joined/split courts under the same successor if physical metrics are required.

Until that joined successor exists, the current WVS split entry remains blocked.

See `03_WVS_ENTRY_PRESTATE_CONTRACT.json`.

## Hostile evidence

Worker E banked source-free hostile tests covering:

- fail closed without joined-successor adoption;
- environment propagation into the protected main candidate child;
- S15 inheritance;
- raw-value-dependent import witness;
- current launcher non-adoption;
- explicit rejection of compileall/precompiled admission;
- a real valid-pyc hostility fixture.

The last fixture was also executed in the available CPython 3.13.5 container: a valid timestamp pyc encoded `cachex` while same-mtime/same-size source encoded `source`. Normal import returned `cachex`; cache-neutral import returned `source` and left the alternate prefix without files. This is supporting evidence only. The commission's governed runtime is CPython 3.11.3, and that exact-runtime fixture remains mandatory before successor promotion.

No raw survey source, source hash pass, decoder, candidate process, candidate output, or measured P2X was used by Worker E.

See `06_SOURCE_FREE_HOSTILE_TESTS.json`.

## Worker B repairs

All four Worker-B implementation/test blobs remain byte-identical at Worker E's implementation head. Its worktree lock, combined import gate, pair compatibility, postrun dirty verification, exact source-byte preprovision and source-hash sequence law are retained.

See `08_WORKER_B_REPAIRS_RETAINED.json`.

## Required next action

Adopt the exact cache-neutral successor contract on **both** joined and split execution. Do not set Worker B's current cache field to `EXACTLY_REPRODUCED`; that would be false. The lawful successor classification is cache **nonparticipation**, not cache reproduction.

After exact CPython 3.11.3 source-free qualification, the new court may establish:

`WVS_BYTECODE_PRESTATE_NEUTRALIZED_BY_SHARED_JOINED_SPLIT_SUCCESSOR_LAW`

Worker E current terminal remains:

`BLOCKED__SPLIT_R2_E_WVS_BYTECODE_PRESTATE_EQUIVALENCE_REMAINS`
