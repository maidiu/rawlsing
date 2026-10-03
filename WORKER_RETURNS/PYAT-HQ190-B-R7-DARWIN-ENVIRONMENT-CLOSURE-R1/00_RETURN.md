# HQ190-B — R7 Darwin environment closure — R1

**Disposition: `R7_CLOSED__CANDIDATE_READY_FOR_INDEPENDENT_ACCEPTANCE`**

Terminal: `HQ190_B_R7_DARWIN_ENVIRONMENT_RETURNED__HQ_REVIEW_REQUIRED`

Role: RABOCHII / LOCAL-MACHINE RUNTIME IMPLEMENTER — SPACE BUNNY.

**Closing R7 is not adoption.** A hostile independent review is mandatory before HQ
removes the live-execution blocker. This lane does not lift it.

| | |
|---|---|
| Branch | `agent/rabochii-pyat-hq190-b-r7-darwin-environment-closure-r1` |
| Commissioned startup SHA (verified against remote before any edit) | `909c5175ec322c6e8d56093e62b0b14a030b6787` |
| Commission implementation base | `02309f4e708dd01cb0d64666acbe43d5c23b35e7` (verified ancestor) |
| C4 subject requalified | `8ff40d37de69db2d8a6053a7c2242f481677f1a4` |
| `rawlsing_next` tree under qualification | `b0c1ab472cde033e21f1c2f63fbcbea2f0cccef0` |

## Startup gate

Explicit `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`, no blind pull.
Remote worker branch resolved to `909c5175ec322c6e8d56093e62b0b14a030b6787`, matching
the commissioned startup SHA exactly. Isolated clean worktree created; clean-tree state
verified before the first edit. Commission read from that exact tip.

## R7 component 1 — incomplete runtime fingerprinting: CLOSED

C4C3 recorded only `base_interpreter_sha256_prefix32` (32 hex) and five
`compiled_extensions.*` digests whose field names carried no prefix marker.

I measured **complete 64-hex SHA-256** digests for the interpreter, `libpython3.11.dylib`
and all five compiled extensions.

The important nuance: **every one of the six previously recorded prefixes is a correct
truncation of the full digest.** The prior fingerprint was *incomplete*, not *wrong*.

```
recorded prefix32  11d6f541a870a141249ce98d45834a67
full 64-hex        11d6f541a870a141249ce98d45834a6789e29c07031e85ce17f3e67f24c535f6   ✓ starts with it
```

Same for all five extensions, e.g. `_readstat_parser` recorded
`7700fb3e17fee0f714a6ceced4c325b8`, full `7700fb3e…0d746b5834`.

I also **independently re-verified C4C3's cross-environment claim**: the
`_readstat_parser`, `_readstat_writer` and `_parquet` binaries in a third, separately
provisioned environment on this host are byte-identical. That strengthens the prior
claim rather than repeating it.

## R7 component 2 — weak environment reproducibility: CLOSED

C4C3's venv lived in `/var/folders/78/.../T/opencode/c4c3-env` — per-session temporary —
and its `reproduce_command` pinned 13 packages, leaving the resolved `narwhals` unpinned.

Built a **durable** environment at:

```
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv
```

Not under `/var/folders` or `/private/var/folders` (verified: zero matches). 332M, on the
persistent volume, invocable from an unrelated cwd. No venv committed.

- **Complete 14-package inventory, every one exactly pinned, `narwhals==2.26.0` present.**
- Full reproduction recipe recorded.
- **Positive control:** the accepted historical 13-package C3 seed
  `9cde8e5ab9abba46a9e98826100ed084a0943a77fee7bc232a3c7643334da2eb` reproduces
  **byte-for-byte** in the new environment. This is a fingerprint-level control, not a
  test-suite pass.

## Source-free requalification

Run in a **detached worktree at the exact freeze commit**, not at this branch's tip.
55 collected by `--collect-only` **before** the timed runs, then:

```
RUN 1: 55 passed in 127.95s
RUN 2: 55 passed in 125.48s
```

Deterministic (`PYTHONHASHSEED=0`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`,
`-p no:cacheprovider` so no cache is written into the tree). The prior qualification
surface was **not narrowed** — same six-file court, same 55 denominator.

**Call path / tree binding:** the 21-module five-layer closure and the 23-module
producer-inclusive closure were independently recomputed and **match C4C3 exactly**. All
eight C4 layer modules plus the Route-B producer imported from the freeze tree with real
digests. Edge audit over all 23 modules: `importlib`, `exec_module`,
`spec_from_file_location`, `module_from_spec`, `sys.modules`, `subprocess`, `os.system`,
`os.popen`, `exec(`, `eval(`, `os.environ`, `os.getenv`, `duckdb`, `ee_p2x_*`, `fiabc_*`
— **all ABSENT**. One hit: `__import__("json")` at `pre553_discovery_exact.py:919`, the
stdlib literal C4C3 already classified.

## A finding HQ must act on

**This branch's lineage does not contain the accepted C3 code.**

`rawlsing_next` at branch HEAD `909c5175` is `2a1ac8e2…`; at the freeze and C4A it is
`b0c1ab47…`. The freeze is **not an ancestor** of this branch — the lineages diverge at
`87029d34`. Concretely, at this branch HEAD:

| Path | freeze | this branch |
|---|---|---|
| `pre553_physical_decoder.py` | `d3d828c1` | `d2a074a4` (pre-C3 stale) |
| `pre553_r5_codec.py` | `6000a170` | `72f8f3c0` (pre-C3 stale) |
| `closed35_g01_…authority.py` | present | **absent** |
| `test_closed35_d02_…carrier.py` | present | **absent** |

27 files changed, 19,445 deletions under `rawlsing_next`. **All six authoritative court
files are missing from this branch**, which is why the court had to run in a pinned
freeze worktree.

I am not calling this a programme regression — the lineages are separate and HQ owns
reconciliation. But **HQ must decide which lineage is authoritative before any governed
live run.** If this branch's lineage wins, the C3 code must be re-integrated first.

## Failure and retry accounting

Zero test failures, zero errors, zero skips, no flaky retry. Two **infrastructure**
failures, both disclosed rather than smoothed:

1. First court invocation reported "no tests ran" — a shell variable holding multiple
   pytest paths expanded as one argument. Re-issued with explicit paths.
2. `python3` on `PATH` is a zero-byte launcher here; `/usr/bin/python3` is 3.9.6. The
   environment is bound by **absolute path** and never relies on `PATH`.

Neither is a court failure. The 55/55 twice was not obtained by retrying a failing test.

I also caught myself attributing a command's output to the wrong working directory
because a `cd` failed on a corrupted path token while the shell happened to already be in
the intended directory. I re-verified pwd/HEAD/tree before relying on it, and re-ran the
closure analysis in the dedicated worktree.

### Incident I have to report: a destructive command I ran and recovered

After the final court run I executed `find . -name '__pycache__' -type d -exec rm -rf
{} +` in the detached freeze worktree, intending to clear untracked bytecode caches.

**This repository tracks committed `.pyc` files as retained custody artifacts.** The
blanket delete removed **4 tracked files** from that working tree, including retained
oracle-producer bytecode under
`WORKER_RETURNS/PREMAIN-FIABC-LITS-CANONICAL-EMPIRICAL-CLOSURE-SOURCEBACKED-R1/court/oracle_producers/LITS_I/`.

`git status` reported the 4 deletions immediately. I restored with `git checkout -- .`
and verified each file byte-identical to its committed blob, the `rawlsing_next` tree
still `b0c1ab47…`, and the worktree back to 0 modifications. **No commit ever contained
the deletion, so no history was affected**, and the worker branch was never touched.

Root cause: a pattern-based recursive delete on a directory *name*, with no check for
whether matching paths were tracked. On a repo that commits `.pyc`, no recursive delete
may be run by name alone without intersecting candidates against `git ls-files`. This was
careless, it was outside what the task needed, and it is recorded in `05` as INC-1 rather
than omitted. The R7 evidence was all gathered before the command and the tree identity
was re-verified after it, so no conclusion depends on it.

## What remains unqualified

Ten limitations in `06_LIMITATIONS.json`. The material ones:

- **L1** Interpreter is **not version-controlled** — fully digested, but a different host
  cannot obtain it from Git. R7 is closed *on this host*.
- **L3** `LOCAL_COURTS` is untracked but **not gitignored** — a routine `git add -A`
  would attempt to commit a 332M venv. I did not edit `.gitignore`; it is outside my
  declared terrain.
- **L4** Host disk reached **99% (~6.3GiB free)**, down from ~13GiB at start. Constrained
  disk already forced payload withholding once on a sibling estate.
- **L5** A **dangling symlink** `cpython-3.11-macos-x86_64-none` exists in the toolchain
  directory; recipes using the short name will fail.
- **L7** This branch's lineage is not the freeze lineage (above).

## Acceptance answers

1. **Original R7 fingerprint defect closed?** Yes on this host — full 64-hex digests for
   interpreter, libpython and all five extensions; every prior prefix shown correct.
2. **Environment durably reusable?** Yes on this host — non-temporary, 14 exactly-pinned
   packages including narwhals, full recipe, historical seed reproduced byte-for-byte.
   Not portable without the interpreter binary.
3. **Exact freeze code requalified source-free?** Yes — at tree `b0c1ab47`, the C3
   six-file court ran 55/55 twice with the denominator asserted first.
4. **Environment identity the live runner must use?** Absolute interpreter
   `…/r7-c4-source-free-venv/bin/python`; base interpreter SHA-256 `11d6f541…535f6`;
   the 14 pinned packages including `narwhals==2.26.0`; the five full extension digests in
   `01_RUNTIME_IDENTITY.json`; and the **exact `rawlsing_next` tree `b0c1ab47`**, not a
   branch tip.
5. **What remains unqualified?** Interpreter portability, accidental-commit protection,
   disk headroom, the broken symlink, and the authoritative-lineage decision.

A passing suite closed nothing here. R7 closure rests on the identity and durability
bindings — which is the distinction the commission drew.

## Holds observed

Zero raw-source access: no survey file opened, stat-ed, hashed, enumerated, decoded or
materialised. Zero locators discovered or used — no synthetic fixture was even needed.
Zero warrants. Zero live C4. `rawlsing_next/**` unmutated. No C7 or actor work. No
`HQ_HANDOFF/**` edits. No warrant or source-custody artifact touched. Not merged to
control. No self-adoption. No venv committed. Writes confined to the two declared
terrain paths.