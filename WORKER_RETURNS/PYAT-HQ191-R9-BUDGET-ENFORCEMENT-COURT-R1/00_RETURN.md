# PYAT HQ191 — Return: R9 source-free budget realizability and enforcement court

Lane: **PYAT HQ191 — R9 source-free budget realizability and enforcement court — R1**
Role: **RABOCHII / source-free execution-accounting implementer — Space Bunny**
Repository: `maidiu/rawlsing`
Worker branch: `agent/rabochii-pyat-hq191-r9-budget-enforcement-court-r1`
Commissioned startup SHA: `631e7586001a5f2736656c4a7d6c1bf055d8c0d1`

## Final disposition

`R9_PARTIAL__SPECIFIC_ACCOUNTS_STILL_UNGOVERNABLE`

Startup tip matched exactly (confirmed by `ls-remote`); parent verified as the
declared base `c782b455d`; isolated worktree; clean tree.

---

## 1. The answer

> **Can lawful, conservative hard maximum authorization budgets be designed,
> source-free qualified, and actually enforced against the exact reader/code
> paths using synthetic carriers?**

**YES for 7 of the 10 mandatory O1-C07 accounts. NO for 3, plus one the
exercised path never performs.**

I instrumented the exact current code, generated tiny legal synthetic
carriers, ran success and failure paths, and proved the guard aborts
**before** the unauthorized operation in **8** C3 guard cases plus **2**
decoder-native fail-closed cases.

| | Accounts | Status |
|---|---|---|
| Governable, enforcement demonstrated | **7** | hard maxima proposed and provably enforced |
| Not governable at any enforceable layer | **3** | blocker preserved |
| Performed nowhere in the exercised path | **1** | no ceiling proposed |

**Not governable:** path-level opens + measurement basis (OSL-01) ·
selected-column reads (SEL-01) · byte counts (BYT-01)
**Not performed:** header-prefix reads (HDR-01)

---

## 2. The decisive measurement: the enforceable layer

The lowest reliably enforceable layer is the **python reader/decoder
invocation layer**.

Each `pyreadstat` reader invocation is a distinct, separately interceptable,
separately cappable logical source access. I patched four surfaces — all
reversible, no production file touched:

`pathlib.Path.is_file` · `pre553_physical_decoder._sha` ·
`pyreadstat.read_sav` · `pyreadstat.read_dta`

**The layer below is not enforceable, and I proved it empirically rather than
asserting it:**

```
python_builtins_open_calls_observed_during_reader_call : 0
reader_read_succeeded                                  : true
```

Zero Python-visible opens during a read that demonstrably succeeded. pyreadstat
is a compiled Cython/C extension; its internal `open(2)` calls are invisible to
Python interception. **I did not fabricate an OS-open ceiling.**
`builtins.open` was patched as an *observability probe only* and deliberately
never used as a gate.

What is provided instead is candidly labelled: capping reader invocations
bounds **logical source accesses** (each invocation necessarily opens the
source at least once). That is an **upper bound on accesses — not an account of
opens**, and it is not relabelled as one.

---

## 3. Enforcement, before the operation

The property under test: *a maximum must abort **before** the unauthorized
additional operation, not after it happened.*

| Case | Maximum | Result |
|---|---|---|
| N1 second existence check | 1 | `ABORTED_BY_C3_GUARD`, `underlying_operation_executed: false` |
| N2 second hash pass | 1 | same |
| N3 second metadata read | 1 | same |
| N4 first existence check | **0** | `REFUSED_FIRST_OPERATION` |
| N5 first hash pass | **0** | `REFUSED_FIRST_OPERATION` |
| N6 first reader invocation | **0** | `REFUSED_FIRST_OPERATION` |
| N7 zero-retry law | retries 0 | first retry refused before any second decode |
| N8 SRC27-shaped four accounts | 1 each | second decode aborted at the existence layer |

N4–N6 matter: the guard can refuse the **first** operation, not merely a repeat.

**Decoder-native fail-closed, measured as its own probes:**

- **D1** SHA mismatch → `DecoderError` at the hash comparison. **Zero reader invocations** — it refuses before any read.
- **D2** encoding not in the frozen exact-SHA allowlist → `DecoderError`. **Zero reader invocations.**

---

## 4. Observed access shape (C2 — synthetic only)

| Probe | existence | hash | metadata read | full read | frame | reader inv |
|---|---|---|---|---|---|---|
| metadata-only decode | 1 | 1 | 1 | 0 | 0 | **1** |
| compatibility decode (latin1) | 1 | 1 | 1 | **1** | **1** | **2** |
| SHA-mismatch refusal | 1 | 1 | — | — | — | **0** |
| unlisted-encoding refusal | 1 | 1 | — | — | — | **0** |

**One decode *entry* is not one reader *invocation*.** The compatibility path
issues two. Capping entries and capping invocations are different ceilings and
both are stated.

---

## 5. SRC27 — four accounts, preserved separately

| Account | C3 maximum |
|---|---|
| existence/access check | 1 |
| full-file SHA-256 hash pass | 1 |
| metadata read | 1 |
| full compatibility read | 1 |

**None is derived from the operation-level route-pass budget.** Each is
independently cappable; exceeding any stops the run regardless of the
route-pass count. Preserved: exactly one governed full Route-B pass, maximum
one, zero retries.

**The hardened note's "at minimum one of each" is recorded as a FLOOR. I did
not promote it to a ceiling.** The maxima above are new C3 policy values
supported by enforceability evidence — not historical expectations.

**SRC35** stays retained-only, `fresh_reads: 0`, `NONE__RETAINED_ONLY`, global
hard zero. It gets no access account because it performs none — **not because
it is unconstrained.**

---

## 6. The three categories, kept apart

- **C1 historical** — read only from frozen artifacts, preserved verbatim. **This court emitted nothing under a C1 label.**
- **C2 observed** — every number in `03_OBSERVED_FIXTURE_COUNTS.json`, on synthetic carriers. Not evidence about any real survey file.
- **C3 policy** — every proposed ceiling in `04_PROPOSED_HARD_MAXIMA.json`. Safety constraints whose purpose is to **stop** a run. Not claims about history.

**C2 or C3 values relabelled as C1: 0.**

**HQ190-C's refusal to fabricate four missing account classes is preserved,
not overturned.** Where the evidence was silent or the layer unobservable, I
recorded silence or unobservability rather than a number.

---

## 7. Does the enforceable layer satisfy O1-C07?

**`PARTIAL__SUBSTANTIVELY_BOUNDED_BUT_LITERALLY_INCOMPLETE`**

Access bounding is lawfully enforceable and demonstrated. But O1-C07 names
*path-level opens **and their measurement basis*** as a mandatory separate
account. That account is neither observable nor enforceable from Python.
Omega-1's acceptance — *"freeze expected budgets before launch"* — can now be
met for 7 of 10 accounts and **cannot** be met for that one.

Per the commission's own instruction — *"if O1-C07 genuinely requires a lower
layer that cannot be enforced, return blocker preserved"* — **R9 is preserved
for that account.**

---

## 8. PRQ-07

Not reopened. No concrete contradiction found. HQ's
`DISCHARGED_BY_COMPLETED_INDEPENDENT_C4_REVIEW_CHAIN` stands. It does not close
R9 and does not authorize source access.

---

## 9. One incidental R7 observation — not an adjudication

The C4C3-qualified environment the environment lock declared **NOT durable**
in a per-session temp directory **still exists**, and still reproduces the
frozen 13-package seed digest exactly:

```
9cde8e5ab9abba46a9e98826100ed084a0943a77fee7bc232a3c7643334da2eb   MATCH
```

with `narwhals 2.26.0` present, exactly as the record states.

This bears on R7 remediation option (a), *durable exact environment
preservation*. **I make no R7 finding and do not adjudicate R7.** Recorded as
an observation for HQ.

---

## 10. Incident disclosed

A blanket `__pycache__` cleanup during this lane briefly deleted **four
tracked `.pyc` files** committed in the repository. Caught by `git status`
before commit; all four restored via `git checkout`; working tree verified
clean of tracked changes. **No tracked file is modified by this lane.**
Recorded rather than quietly fixed.

---

## 11. Holds — all observed

| Hold | State |
|---|---|
| Real-source stat / hash / open / decode / materialization | **0** |
| Locator discovery / fill | **0 / 0** |
| Directory inspection for sources | **0** |
| Warrant issued | **no** |
| Live C4 | **not executed** |
| Production mutation | **none**; `rawlsing_next` 0 files changed |
| C7 / actor-person work | **none** |
| `HQ_HANDOFF/**` | **not edited** |
| Historical warrant artifacts / HQ190-C diagnostic | **not edited** |
| Astra / self-adoption / merge | **no / no / no** |

Synthetic carriers were written only to a `tempfile.TemporaryDirectory()`
outside the repository, and deleted with it.

---

## 12. Files

**Court** (`OPS-04/R9-BUDGET-ENFORCEMENT-COURT-R1/`): `synthetic_carriers.py`,
`r9_budget_enforcement.py`, `run_court.py`, `run_supplementary.py`,
`09_HARD_MAX_BUDGET_CANDIDATE.json` (unsigned, unissued,
`authorizes_access: false`, `execution_authorized: false`, 7 locator
placeholders), plus both raw observation records.

**Return**: `00_RETURN.md`, `01`–`08`.

---

## 13. What HQ must decide

1. Whether to **adopt** the proposed C3 maxima as policy. This lane proposed; it did not adopt.
2. Whether the **path-level-open account** is to be (a) preserved as a permanent blocker, (b) satisfied by an accepted upper-bound-on-accesses formulation with the basis limitation recorded, or (c) met by an OS-level audit mechanism outside Python.
3. Whether the **producer/carrier consumer path** needs its own budget layer — this court exercised decode entries, not the full run.

**Hostile independent review is mandatory before HQ removes R9.** Nothing here
has been reviewed by any party other than this lane.

Terminal:
`HQ191_R9_BUDGET_COURT_RETURNED__HQ_REVIEW_REQUIRED`