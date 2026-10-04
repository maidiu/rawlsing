# PYAT HQ196 — R9 broker + selected-read hostile review — R1

**Disposition:** `BROKER_ROUTE_CONFIRMED__SELECTED_READ_IMPLEMENTATION_GAP_CONFIRMED`

**Terminal:** `HQ196_R9_BROKER_SELECTED_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq196-r9-broker-selected-hostile-review-r1`
Commissioned startup SHA: `98899701e80e13e9f716416aaf6cd8d7a21753d9` — **verified equal**.
Checkout mode: `SPARSE_REQUIRED` — **honored**. No clone, no full worktree, sparse checkout
not widened; historical code read by exact Git object. The parallel HQ196 implementation
branch was **not inspected**.

Reviewer identity: DeepSeek Harness, **DeepSeek V4.1 Flash**.

---

## Headline

**Part A — the broker route is real, and I confirmed it from source plus synthetic
reproduction.** pyreadstat 1.3.6 ships a public file-object seam that installs Python bridge
handlers and hands the compiled reader an *empty path* with a *no-op open handler*. But my
attack found **three material design constraints the feasibility claim did not carry** — most
importantly that **enforcing a budget by raising inside `read()` hangs the reader** instead of
failing loudly.

**Part B — the selected-read gap is worse than "a missing counter".** The frozen expectation
is a *selected-variable physical read* with `expected_full_reads=0`; the executed route
performs a full-column read and zero selected reads. **The operation itself is missing**, not
merely its accounting owner. And `usecols` — which pyreadstat does expose — is a **post-read
projection** that changes nothing physically, so adding it would not create the account and
claiming otherwise would be over-claiming.

## 1. Startup and method

| Step | Result |
|---|---|
| `git fetch origin` (no blind pull) | OK |
| review branch == `98899701e…` | **MATCH** |
| commission read from exact object | OK |
| sparse worktree via canonical helper | `SPARSE_WORKTREE_READY` |
| sparse checkout widened | **NO** |
| parallel implementation branch read | **NO** |
| environment | R7 venv (CPython 3.11.3, pyreadstat 1.3.6), read-only |
| carriers | synthetic SAV/DTA generated with `pyreadstat.write_*` — no survey data |

Because the wheel ships `_readstat_parser.pyx`/`.pxd` **and** the generated C, I read the seam
as **source** rather than inferring it from behaviour.

## 2. Part A — the broker seam (source control flow)

The seam is explicit and public:

- `pyreadstat.py:56` — `class FileLike(Protocol)`, documented as *"Should work with any
  file-like object that has read and seek methods"*; `FilePathorBuffer = FilePathLike | FileLike`.
- `_readstat_parser.pyx:1252` — `if hasattr(filename_path, 'read') and hasattr(filename_path, 'seek'): file_obj = filename_path`
- `_readstat_parser.pyx:1254` — `filename_bytes = b""  # Empty path - will be ignored when file_obj is used`
- `_readstat_parser.pyx:965` — `if file_obj is not None:` installs **all four** bridge handlers and sets `io_ctx` to the file object:

| Handler | Body |
|---|---|
| `pyobject_open_handler` | *"File is already open - this is a no-op"* → `return 0` |
| `pyobject_close_handler` | *"User manages file lifetime - this is a no-op"* → `return 0` |
| `pyobject_read_handler` | `file_obj.read(nbyte)` → `memcpy` into the ReadStat buffer |
| `pyobject_seek_handler` | `file_obj.seek(...)` → `return file_obj.tell()` |

So on this route the compiled reader gets an **empty path** and **cannot** perform a
source-path open: there is no path for it to open, and its open hook is a no-op. The
strongest confirmation is behavioural — **`io.BytesIO` works**, and it has neither a path nor
a file descriptor, so every byte provably arrived through the Python bridge.

**Confirmed:** app-owned open is the complete literal path-open account on this route; reads
and bytes are observable there; no rebuild and no privilege required; R7 identity unchanged.

## 3. Part A — three constraints the feasibility claim missed

**(a) Enforcing a ceiling by raising HANGS the reader.** `pyobject_read_handler` wraps the
call in a **bare `except:` that returns `-1`**. I built a broker that raises past a read-count
ceiling — the process **hung and had to be killed at 12 s**. Returning a **premature EOF
(`b""`)** instead produces a prompt, loud `ReadstatError: Unable to read from file` on **both
SAV and DTA**, at every cap tested. So a governed ceiling is achievable and loud, but **only
via premature EOF**; a "fail-closed by raising" implementation would hang in production.

**(b) The broker must be a real seekable stream.** A naive object exposing `read`/`seek` with
raw semantics fails with *"Unable to seek within file"* — the seam wants genuine `tell()`
semantics. Not a blocker; a trap.

**(c) A single broker cannot drive chunked reads.** `read_file_in_chunks` **re-invokes** the
read function per chunk (plus a `metadataonly=True` probe) and never resets position, so a
reused broker fails on the second invocation (*"This version of the file format is not
supported"*). A **fresh broker per reader invocation** yields correct chunks
(`[(0,200),(200,200),(400,100)]`) *and* complete per-invocation accounting. Today the freeze
decoder passes raw `str(source)` at all three reader call sites, so none of this is wired yet.

## 4. Part B — the selected-read gap

The freeze law requires, per source:

| Source | `expected_selected_reads` | `expected_full_reads` |
|---|---|---|
| SRC02 (Q10B) | 1 | 0 |
| SRC06 (Q101, Q2061B) | 1 | 0 |
| SRC14 (v372) | 1 | 0 |

**The freezer decoder has no `usecols` anywhere.** Its three reader invocations are the
metadata probe (line 496), a compatibility full read (line 502), and the chunked row-data
read (line 155) — none configures selected columns.

**1. Does any other layer supply an equivalent restriction?** **No.** The only fresh-read
entry points are `_decode` and `PhysicalSourceIncidence.iter_batches`. Downstream consumers
receive `PhysicalCell` objects already materialised from a full-column frame, so a downstream
filter cannot un-read columns. The `usecols=['B_COUNTRY']` uses that do exist are on the
**retained comparator / WVS7 projection** routes, not the fresh C4 route. Crucially,
downstream *selected-variable exactness* constrains which variables are **used**, not which
columns are **read** — and the account in question is a read account.

**2. Does pyreadstat support a `usecols`-style restriction?** **It accepts one — but it is a
projection.** `read_file_in_chunks` forwards `usecols` via `**kwargs` and the returned frames
are genuinely column-filtered. Yet measured physical I/O is **identical** with and without it:

| Format (4000 rows) | no `usecols` | `usecols=['Q10B']` |
|---|---|---|
| SAV | 4050 reads / 160869 bytes | **4050 reads / 160869 bytes** |
| DTA | 4055 reads / 163751 bytes | **4055 reads / 163751 bytes** |

**3. Owner-missing, or operation-missing?** **The operation itself is missing.** A missing
*counter* is repaired by instrumenting the existing operation; here the existing operation is
the **wrong operation** relative to the frozen expectation, so instrumenting it would
faithfully count a full read while the warrant authorises a selected read.

**4. Material pre-live gap?** **Yes** — it changes what the run physically does to three of
eight sources, and the frozen `expected_full_reads=0` would be violated, which the contract
treats as a **STOP**, not a reportable variance. C4 also forbids opportunistic repair during
governed execution.

## 5. Honest nuance I will not paper over

Even with `usecols` added, pyreadstat 1.3.6 would **not** reduce physical I/O. An
implementation that adds `usecols` and then claims a physically distinct selected read would
be **over-claiming**. Whether the frozen account is satisfied by a projection-filtered full
decode (honestly accounted as a full read plus a selection step) or requires a genuinely
column-restricted physical read is an **authority question for HQ** — this review does not
resolve it.

## 6. What this review did not establish

Per the HQ196 adjudication's outstanding-proof list: that **every** relevant reader call site
can be brokered with no raw path-string escape (I enumerated three, all currently raw paths —
the full audit is implementation-lane work), and full source-free **corpus** equivalence
between path and broker routes (verified here on synthetic carriers only).

## 7. Contract ceiling respected

I did not reopen the settled meaning: budgets/instrumentation/basis frozen before launch,
exact observed counts measured at return, and literal path opens not relabelable as
reader/decoder invocations. **No concrete contradiction was found** that would justify
reopening it.

## 8. Holds observed

Zero real survey/source access (synthetic carriers only); zero locator discovery; zero
warrant issuance; zero live C4; no production mutation; no C7 or actor/person work. Nothing
written outside the commissioned return directory; the sparse checkout was never widened.
