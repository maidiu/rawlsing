# PYAT HQ192 — Return: R9 OS accounting interposition and higher-layer completion

Lane: **PYAT HQ192 — R9 OS accounting interposition and higher-layer completion — R1**
Role: **RABOCHII / source-free low-level accounting implementer — Space Bunny**
Worker branch: `agent/rabochii-pyat-hq192-r9-os-accounting-interposition-r1`
Commissioned startup SHA: `fdaf71c4c08d3f21778eeab335b5b928cc78fb7b`

## Final disposition

`R9_PARTIAL__LOWER_LAYER_STILL_UNGOVERNABLE`

Startup tip matched exactly (confirmed by `ls-remote`); parent verified as
declared base `491dac21b`; isolated clean worktree.

**Part A failed. Part C succeeded. Part B's account has no owner. Part D is
partial.**

---

## PART A — OS-level interposition: **UNAVAILABLE**. Blocker preserved.

I attempted two mechanisms, then stopped. Both failed, and I did not fake a count.

### Attempt 1 — plain symbol definitions
`DYLD_INSERT_LIBRARIES` with functions named `open/openat/fopen/read/pread/close`.
Library loaded, constructor ran, `__interpose` section absent — **zero events**,
including for a *direct* `ctypes` `libc.open()` call.

That last part is the diagnosis: because even a direct libc call produced nothing,
this was **my mechanism failing, not pyreadstat bypassing it.** Finding **MECH-01**.

### Attempt 2 — `__DATA,__interpose` tuples
Section present (96 bytes). CPython then **fails to start**:

| Interposed | Interpreter | rc | Result |
|---|---|---|---|
| none | uv / C4C3 | 0 | OK |
| `getpid` | uv / C4C3 | **139** | SIGSEGV |
| `stat` | uv / C4C3 | 1 | *Could not find platform independent libraries `<prefix>`* |
| `open` | uv / C4C3 | **139** | SIGSEGV |
| none | framework | 0 | OK |
| `getpid` | framework | **139** | SIGSEGV |
| `stat` | framework | 1 | prefix-discovery failure |
| `open` | framework | **139** | SIGSEGV |

Identical failure on **both** interpreters — and for `getpid`, a completely cold
symbol. So this is a property of **this host**, not of `open` and not of one
interpreter.

`dtruss`/`fs_usage`/`opensnoop`/`ktrace` exist as binaries but require root; the
commission forbids sudo.

**Conclusion: lawful process-local libc interposition is not available on this
host. O1-C07's path-level-open account remains unsatisfiable. Reproducible via
`run_interposition_probe.sh`.**

**What zero means:** zero *observed*. It is **not** a count of what the reader
did — the read succeeds, so the reader certainly opens the file.

---

## PART C — SRC26 header prefix: **CLOSED at the Python layer.** ✓

HQ191 recorded this account as *not performed*. That was true of the path it
exercised — but the owner **exists**:

```c
// rawlsing_next/pre553_physical_decoder.py :: _raw_layout_declarations  (372-389)
prefix_size = 176 if source_format == "SAV" else 512
with source.open("rb") as handle:
    prefix = handle.read(prefix_size)
```

This is **pure Python**, so unlike the compiled reader it **is** visible to
`builtins.open`/`Path.open` interception — and governable.

**Measured (C2, synthetic):** 1 operation per decode, returning 176 bytes (SAV) /
512 (DTA).

**Enforcement proven:** an excess header-prefix read is **refused before any open
or read on the carrier** — `operation_executed: false`.

Operation count and byte count are reported separately, as the commission
required. This emits `header_prefix_length` and `header_prefix_sha256`.

**Important limit:** this is a *Python-layer* operation. It does **not** substitute
for the Part A OS-level blocker.

---

## PART B — Selected-column: **no executable owner.** Finding SEL-02

`usecols` occurs **zero** times in the entire 23-module closure. All three
reader-invocation sites are whole-file or metadata-only.

The warrant's `SELECTED_VARIABLE_PHYSICAL` entries for SRC02 (Q10B/58), SRC06
(Q101/20, Q2061B/19) and SRC14 (v372/466) are **declarative contracts**. What is
real and enforced is **selected-variable exactness** — court assertions plus
O1-C08's stop trigger on an absent variable, absent ordinal, or *unexpected*
selected column.

**I did not create a selected-read count.** It would guard an operation the
decoder never performs. Exactness is a different account and is labelled as such
rather than relabelled into a read count.

---

## PART D — Byte accounting: **partial**

Python-level reads are observable and enforceable. Compiled-reader byte counts are
**not**, because that depends on Part A.

Exact arithmetic, both verified:

```
SAV:  587 (whole-file hash) + 176 (header prefix) = 763
DTA: 2117 (whole-file hash) + 512 (header prefix) = 2629
```

**No byte ceiling is proposed for the compiled reader.** Synthetic byte totals
are **not** predictions about real survey files.

---

## Also newly measured — beyond HQ191's scope

| Finding | What |
|---|---|
| **Python-level opens** | **2 per decode** — the whole-file hash pass *and* the bounded header-prefix read. HQ191 counted neither. |
| **Python-level byte volumes** | 763 / 2629 bytes. HQ191 measured none. |
| **RDR-02** | `iter_batches` (lines 140–146) issues `pyreadstat.read_file_in_chunks` — a **third** reader-invocation site performing a whole-file chunked read. HQ191 exercised decode entries only and never measured it. |

---

## Why no successor candidate

A complete non-authorizing candidate cannot be produced without omitting either
the path-level-open account or the selected-read account. Presenting a partial
instrument as complete would be worse than preserving the blocker. **No candidate
was produced.**

---

## Three categories, kept apart

- **C1 historical** — `expected_header_prefix_bytes: 176` for SRC26, unchanged,
  not relabelled.
- **C2 observed** — every measurement here, on synthetic carriers only.
- **C3** — the header-prefix ceiling used to demonstrate refusal is a
  **C3-DEMO** demonstration ceiling, **not** an adopted policy maximum.

**C2 or C3 values relabelled as C1: 0.**

---

## Holds

| Hold | State |
|---|---|
| Real-source stat / hash / open / decode / materialization | **0** |
| Locator discovery / fill | **0 / 0** |
| Source-directory discovery | **0** |
| Warrant issued | **no** |
| Live C4 | **not executed** |
| Production mutation | **none**; `rawlsing_next` 0 files changed |
| C7 / actor work | **none** |
| `HQ_HANDOFF/**`, HQ190-C/HQ191 diagnostics, warrant artifacts | **not edited** |
| sudo / system install | **none** |

Interposition was process-local and reversible. Synthetic carriers lived in a
`TemporaryDirectory` outside the repository.

---

## What HQ must decide

1. **OS-level open account** — accept the Python-layer bound as a *different*
   account with the basis limitation recorded; keep the blocker; or require an
   OS-level audit mechanism outside this lane's reach (privileged tracing, a
   non-SIP host, or a differently-built interpreter).
2. **Selected-read** — accept exactness as the account, or commission an actual
   bounded selected read.
3. **RDR-02** — commission measurement of the `iter_batches` chunked-read site,
   which remains unmeasured.

**Hostile independent review is mandatory.** Nothing here has been reviewed by any
party other than this lane — including the Part C positive finding.

Terminal:
`HQ192_R9_OS_ACCOUNTING_RETURNED__HQ_REVIEW_REQUIRED`