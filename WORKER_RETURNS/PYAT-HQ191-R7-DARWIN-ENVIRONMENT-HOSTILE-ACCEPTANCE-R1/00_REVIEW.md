# PYAT HQ191 — R7 DARWIN ENVIRONMENT HOSTILE INDEPENDENT ACCEPTANCE — R1

**Disposition:** `ACCEPT_R7_CLOSED__SEPARATE_HOST_PREFLIGHT_BLOCKER_REMAINS`

**Terminal:** `HQ191_R7_HOSTILE_ACCEPTANCE_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq191-r7-darwin-environment-hostile-acceptance-r1`
Commissioned startup SHA: `0e28823c7fa60e8b4869c3c6143b8b43b738f10a`
Reviewed worker tip: `def6d369878cb273ca06f97e08c4fb0a2964611e`
Substantive R7 result: `11f68e122c728dd8be6a6fd45bd7e8ef959060b7`

**Reviewer environment (observed):** DeepSeek Harness, DeepSeek V4.1 Flash. macOS 13.7.8
(Darwin 22.6.0), x86_64; git 2.39.1. Qualification interpreter used for all runtime
re-observation: `LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python` (CPython 3.11.3).

---

## 1. Bottom line

**R7 is genuinely closed.** I hashed the actual files myself rather than reading JSON
claims, and every digest matches to the full 64 hex; the durable environment is exactly
as declared (14/14 pins, `narwhals==2.26.0`, correct base interpreter, exact size); and I
independently **re-ran the six-file court twice: 55 passed, 55 passed** at the exact freeze.

I also found that a **separate, non-R7 host preflight blocker remains**, and it is worse
than the worker reported: disk headroom has fallen further and is **volatile**, with the
data volume repeatedly at 100% capacity and free space swinging between ~2.0 and ~6.0 GiB
inside a single minute. That is a live-run capacity blocker, not an R7 defect.

**Answer to the commission's pointed question:** with headroom oscillating in the 2–6 GiB
band and the volume repeatedly at 100%, a governed multi-gigabyte live C4 run on this host
is **not safe and not credible** today. It is not that C4 will necessarily fail — it is that
the failure mode is uncontrolled: an ENOSPC mid-run aborts after partial writes, producing
exactly the partial-evidence condition the programme treats as un-credible, and it can occur
at a different point on every attempt.

## 2. Mandatory startup (all verified before substantive review)

| # | Check | Result |
|---|---|---|
| 1 | `git fetch origin` (no blind pull) | OK |
| 3–4 | review branch == `0e28823c7…` | **MATCH** |
| 5 | worker branch == `def6d3698…` | **MATCH** |
| 6 | `11f68e122…` substantive result, ancestor of tip | **VERIFIED** |
| 7 | isolated clean review worktree | `review-hq191` |

The review tip is a single-file commit (the commission) whose parent is exactly the
worker tip; the substantive commit is 12 files of evidence/return only.

## 3. A — Runtime identity: **CLOSED on this host (independently reproduced)**

I measured every digest from the actual local bytes:

| Artifact | Claimed | Measured by reviewer | Match |
|---|---|---|---|
| base interpreter `bin/python3.11` | `11d6f541…c535f6` | `11d6f541…c535f6` | ✅ exact |
| `lib/libpython3.11.dylib` | `83d9b1e4…5efc0a` | `83d9b1e4…5efc0a` | ✅ exact |
| `_readstat_parser…so` | `7700fb3e…6b5834` | `7700fb3e…6b5834` | ✅ exact |
| `_readstat_writer…so` | `a5cd73f3…cc25ed` | `a5cd73f3…cc25ed` | ✅ exact |
| `_parquet…so` | `62a37af8…93b38c` | `62a37af8…93b38c` | ✅ exact |
| `_dataset_parquet…so` | `2a99f7b5…cd1678` | `2a99f7b5…cd1678` | ✅ exact |
| `_parquet_encryption…so` | `1f9de8f3…c3c1ee9` | `1f9de8f3…c3c1ee9` | ✅ exact |

**The prefix-completion claim is TRUE, and this was the load-bearing R7 defect.** I
programmatically checked all six historical 32-hex values against the newly measured full
digests: **all six are true prefixes of the full digests**, none is a separately invented
value. The prior fingerprint was *incomplete, not incorrect*. That is exactly the right
characterisation, and it is now complete.

**Independent corroboration the worker did not have to offer:** the three cross-environment
extensions (`_readstat_parser`, `_readstat_writer`, `_parquet`) in
`LOCAL_COURTS/python/fiabc-wvs7-3.11.3` are **byte-identical** to the R7 venv's. A third
provisioned environment yielding the same decoder binaries strengthens the C4C3 claim.

## 4. B — Durable environment: **verified on this host**

- Path exists at `/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv`; **not** under `/var/folders` (not per-session temp).
- **Exact interpreter resolves as claimed:** `pyvenv.cfg` has `home = …/cpython-3.11.3-macos-x86_64-none/bin`, `executable = …/python3.11`, `include-system-site-packages = false`; `sys.base_prefix` at runtime is exactly that toolchain root.
- **Inventory complete and exactly pinned: 14/14** — measured by `pip freeze` and byte-compared against the claim (`Pygments 2.21.0`, `iniconfig 2.3.0`, **`narwhals==2.26.0`**, `numpy 2.4.6`, `packaging 26.3`, `pandas 2.3.3`, `pluggy 1.6.0`, `pyarrow 25.0.1`, `pyreadstat 1.3.6`, `pytest 9.1.1`, `python-dateutil 2.9.0.post0`, `pytz 2026.4`, `six 1.17.0`, `tzdata 2026.4`).
- `import narwhals` → **2.26.0**; science-stack import smoke passes.
- **Size matches exactly:** claimed `348213248` bytes; measured `340052 KiB` = `348213248` bytes.

**Durable on this host ≠ portable to another host.** The interpreter is *not*
version-controlled (`committed_to_git: false` is accurate) and the venv is not tracked.
The recipe pins versions but reconstruction depends on an external package index. So: durable
here, **not** independently reconstructible elsewhere from this repository alone. The worker
states this correctly.

## 5. C — Source-free requalification: **independently re-executed**

I created my own detached worktree at the exact freeze and ran the court myself with the
qualification interpreter:

| Check | Claim | Reviewer observation |
|---|---|---|
| freeze commit | `8ff40d37…` | present, `rawlsing_next` tree = **`b0c1ab47…`** ✅ |
| collect-only before run | 55 | **55 collected** (5.45s) ✅ |
| per-file split | 9/8/13/9/6/10 | **9 / 8 / 13 / 9 / 6 / 10** ✅ |
| run 1 | 55 passed | **55 passed** (209.99s) ✅ |
| run 2 | 55 passed | **55 passed** (163.03s) ✅ |
| failures/errors/skips | 0/0/0 | 0/0/0 ✅ |
| six-file court identity | 3 pinned blobs | all 3 pinned blobs **MATCH**; all six files present ✅ |
| narrowing | none | confirmed — the same six-file court, not a substitute ✅ |
| `.pytest_cache` written into tree | none | worktree clean afterwards ✅ |

**Closure and edge audit — reproduced independently via AST (no imports, nothing executed):**

- The declared **23-module union contains zero fabricated members**; every named file exists at the freeze with the claimed real imports.
- **Edge-audit property holds at the declared grain:** over the closure modules, the *only* non-empty pattern class is `__import__`, in exactly one module (`pre553_discovery_exact.py`). No `importlib`, `exec_module`, `spec_from_file_location`, `module_from_spec`, `subprocess`, `os.system`, `os.popen`, `exec(`, `eval(`, `os.environ`, `os.getenv`, `duckdb`, or `ee_p2x`/`fiabc_` edge at the claimed evidence grain.

**One honest count note (not a defect):** my direct-import closure from the roots I chose
measured **20**, not 23. The three extras (`pre553_carrier_execution`,
`pre553_empirical_possibility_provider`, `pre553_route_b_production`) are genuine **root**
modules that nothing else in the union imports — not phantoms and not evidence of hidden
reachability. The closure counts are therefore **definition-dependent** (root set breadth),
and the union *membership* is what carries the substance. This does not weaken the claim.

## 6. D — Incident and retry honesty: **verified**

- **No test failure was retried until green.** The two disclosed infrastructure failures are real and correctly classified as invocation/host issues, not court failures:
  - *Failure 1* root cause is a genuine shell-word-splitting hazard — I reproduced the mechanism (`P="a.py b.py"; pytest $P` passes one argv token).
  - *Failure 2* (PATH `python3` hazard): **the host has since changed.** The framework symlink `python3.11 → python3.11-intel64` was repointed `Oct 2 18:47`, and `/usr/local/bin/python3` now executes (`Python 3.11.3`). The hazard was real when recorded and the mitigation — bind an absolute interpreter path — remains correct; if anything this change *strengthens* the case for absolute binding, since PATH resolution is demonstrably not stable on this host.
- **`__pycache__` incident (INC-1):** the delete targeted a directory *name* with no `git ls-files` guard, removing **4 tracked `.pyc` custody artifacts**. I verified recovery independently:
  - all 4 present files are **byte-identical** to their committed blobs (`git hash-object` == `git rev-parse HEAD:path`);
  - **no commit in the R7 lane range deletes anything** (`--diff-filter=D` over the lane range is empty);
  - the only `*.pyc` deletion in repository history is `d58242fce` "D06: remove transient Python cache artifacts" from **2026-09-12**, which is **not an ancestor** of the substantive commit and belongs to unrelated earlier history.
  - **Final freeze tree clean:** my own post-run `git status` showed only untracked `__pycache__`, no tracked modification.

## 7. E — Host-bound operational blockers: **one is a NEW separately typed live blocker**

| ID | Finding | Classification |
|---|---|---|
| **F1** | cross-lineage: branch `rawlsing_next` = `2a1ac8e2…` vs freeze `b0c1ab47…`; freeze not an ancestor; **18-file** tree difference; six court files absent from branch | **Not a regression, not a blocker** — see §8 |
| **F2** | `LOCAL_COURTS` not gitignored | **Operational hazard.** Confirmed: `git check-ignore` fails, **0 tracked files**, so a `git add -A` would sweep in the 6.9 GiB estate (332 MiB qualification venv included) |
| **F3** | disk ~99% / ~6.3 GiB free | **NEW SEPARATELY TYPED LIVE-RUN PREFLIGHT BLOCKER** — see below |
| **F4** | dangling interpreter symlink | **Operational hazard.** Confirmed broken: `cpython-3.11-macos-x86_64-none → /Users/matthewsmith/LOCAL_COURTS/…` (wrong prefix; the estate is under `Desktop/Rawlsing/`). Real dir is `cpython-3.11.3-…`. A recipe naming the short path **fails** |

### F3 is worse than reported and is a live blocker

| Measurement | Value |
|---|---|
| Data volume | `/dev/disk2s6`, 408 GiB, **capacity 99–100%** |
| Free at R7 time (worker) | ~6.3 GiB |
| Free at review start | 6.34 GiB |
| Free during review | **1.99 → 5.99 → 2.99 → 4.98 GiB inside ~60 s**, volume repeatedly at **100%** |
| `LOCAL_COURTS` estate | **6.9 GiB** (`Rawlsing` 2.4G, `-hq105-readiness-r1` 1.7G, `-retry-r1` 1.2G, …) |
| workspace | 17 GiB |

The headroom is not merely low, it is **volatile** — APFS purgeable/snapshot churn moves it
by gigabytes within a minute. A governed multi-gigabyte C4 run needs a *stable* minimum, not
a lucky window. **Verdict: unsafe and non-credible today.** Minimum precondition: free
materially more than the run's worst-case write set, keep the estate off the run volume or
prune it, and enforce a checked minimum-free-space precondition in the live runner.

## 8. F — Lineage finding: expected, not a regression

The worker did **not** call ordinary cross-lineage evidence a regression, and I agree with
that restraint. The freeze is executed by **exact SHA pin**, the qualification was correctly
performed in a detached worktree at that SHA, and the branch lineage differing is a
programme-reconciliation question that HQ owns. It is a **pre-execution authority decision**
(“which lineage is authoritative for the live run”), not R7 unsoundness and not an execution
blocker *provided* the governed run stays SHA-pinned to `8ff40d37…`.

## 9. Review questions answered

1. **Fingerprint closed on this host?** **Yes** — all six digests reproduced from actual bytes; all six historical prefixes are true truncations.
2. **Environment durable enough for a governed later run on this host?** **Yes** — exists, non-temp, correctly resolved interpreter, 14/14 exact pins, exact size.
3. **Exact source-free requalification independently supported?** **Yes** — I re-ran it: 55 collected, 55 passed twice, correct six-file court, no narrowing, closure/edge properties reproduced (with the count-definition note in §5).
4. **Is R7 removable as the live-execution blocker?** **Yes, R7 itself is removable.** Its two components are independently verified.
5. **Does a new separately typed live-run blocker emerge?** **Yes — F3 disk capacity/volatility.** Separately typed; not folded into R7.
6. **Minimum action before live C4:** see §10.

## 10. Capability ceiling and minimum action

**Ceiling:** R7 closes *runtime identity* and *durable local qualification environment*. It
does **not** close live-execution readiness. No live C4 is authorised by this acceptance, and
source-free fixture qualification cannot establish live occupancy.

**Minimum action before live C4 (ordered):**
1. **Resolve disk (blocking).** Free a stable margin above the run's worst-case write set; prune or relocate the `LOCAL_COURTS` estate; enforce a checked minimum-free-space precondition in the live runner. Re-measure headroom immediately before launch.
2. **Add the `LOCAL_COURTS` ignore rule (F2).** One line; prevents a 6.9 GiB accidental commit.
3. **Remove/repair the dangling symlink (F4).** Otherwise any recipe using the short path fails.
4. **Decide authoritative lineage (F1)** for the governed run, or explicitly re-confirm execution stays pinned to `8ff40d37…`.
5. **Keep absolute interpreter binding.** Given the host's demonstrated PATH instability, never resolve the interpreter through PATH in the live runner.
6. **Version the interpreter or record its provenance/retrieval** if cross-host reconstruction is ever required; today it is durable-here only.

## 11. Holds observed

Zero raw-source access — I did not stat, hash, enumerate, inspect, decode or materialise any
real survey source, and I ran no code that touches a source path. Zero locator discovery.
Zero warrant issuance. Zero live C4. Zero production mutation. Zero C7/actor work. The R7
candidate was not modified (its artifacts still hash as committed). I wrote only the
commissioned return directory; my temporary freeze worktree was created under `/tmp` and
removed, and the only repository writes are this packet.

**Reviewer-side note:** my freeze worktree transiently consumed ~1.5 GiB and pushed the
volume to 100% itself. It has been removed. This is disclosed because it is the same class
of capacity hazard as F3 and reinforces that the run volume must be managed deliberately.
