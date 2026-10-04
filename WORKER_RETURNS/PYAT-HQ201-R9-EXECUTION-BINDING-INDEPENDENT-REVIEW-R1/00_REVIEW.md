# PYAT HQ201 — R9 execution-binding independent review — R1

**Disposition:** `EXECUTION_BINDING_MATERIAL_DEFECTS__BOUNDED_REPAIR_REQUIRED`

**Terminal:** `HQ201_R9_EXECUTION_BINDING_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq201-r1`
Commissioned startup SHA: `f064dff8fe2262ad6dc0ccb87e2b835ecb2c022b` — **verified equal**
Clean tip: `35ffa48204672e6c7180cd010a7c1adde9f18cd7`; code-bearing `b8b4c99633c4aa849fd79614c5bffbd1321209b8`
Checkout mode: `SPARSE_REQUIRED` — honored; no clone, no full worktree, sparse checkout not widened. The parallel HQ201 hardening return was **not** inspected.

---

## Headline

**All four HQ-bound attacks found material defects — and every court is green anyway.** That gap
is itself a finding: the existing binding court encodes one defect as intended behaviour and
bypasses the public wrapper for another.

**Courts:** binding **21/21**, session **15/15**, broker **20/20**, R7 **55 collected then 55/55
twice**. 166 tests, zero failures.

## Attack A — route-pass applicability: DEFECT

The successor gives SRC27 a `governed_full_route_passes` account (**EXACT 1**, labelled
`workload (NOT an access account)`) and gives the other six sources **no such account** — i.e.
exact 0. The wrapper cannot express that while still running them:

| Configuration | Result |
|---|---|
| `expected=0, maximum=0` | **refused before any operation** (`ROUTE_PASS_LIMIT_REACHED`), no session created — the source's admitted SELECTED operation can never run |
| `expected=0, no maximum` | the operation **ran** (path_opens=1, selected_reads=1), then failed after the fact (`POST_EXECUTION_CONSTRAINT_FAILED`) |

**Cause:** `execute()` does `self._passes_completed += 1` after **every** successful `session.run()`,
with no test of whether the plan constitutes a full route pass. A route-pass maximum of zero
therefore means "no operation at all" — exactly what the commission forbids.

## Attack B — failed attempt / retry zero: DEFECT

Exercised through the **public** `execute()`, with the source transiently unavailable then
restored:

```
attempt 1: FAILED SOURCE_BYTES_UNAVAILABLE   passes_completed=0  existence=1 decoder=1 retries=0
attempt 2: SUCCEEDED                          passes_completed=1  existence=2 hash=1 metadata=1 retries=0
```

**Two source operations under one bound execution whose frozen retry budget is 0, and the
`retries` account never moved.** There is no retry gate: `_gate_route_pass()` keys on
**completed** passes, so a failed attempt leaves it open. A permanently mismatched SHA also
permitted three consecutive attempts, each performing pre-pass source operations.

**The three quantities are not kept distinct** — only completed passes exist. `_pass_attempted`
is a boolean, not an account.

## Attack C — completion semantics: DEFECT

Ordering in `execute()` is: operation returns → **`_passes_completed += 1`** → constraint checks.
With a caller-bound `FLOOR 999` on `metadata_reads`, the operation returned, the postcondition
failed, and **`_passes_completed` was left at 1**. It is worse for the outer check itself: when
the outer EXACT expectation fails, the very check that detects it runs *after* the count has
recorded success.

**Required rule:** a governed full route pass completes only when the whole bound execution
succeeds — operation returned **and** all post-operation EXACT/FLOOR/MAXIMUM constraints hold
**and** the outer expectation holds.

## Attack D — dependency injection: DEFECT

`BoundSourceExecution.__init__` accepts `pyreadstat_module` and **never stores it**;
`_ensure_session()` hard-codes `pyreadstat_module=None`. Measured with a sentinel:
`session.broker.pyreadstat is supplied → False`, `is real pyreadstat → True`.

This is not merely testability. The successor binds an exact `execution_surface`
(`PYREADSTAT-1.3.6/…`) per source; the binding layer cannot assert or demonstrate the bound reader
identity, and the discard is **silent** — no warning, no error, no receipt field.

## Warrant compatibility

The successor is **representable in principle but not executable** by this binding for six of
seven sources. I verified the type-level distinctions hold: expected vs maximum vs floor vs
observed remain distinct; `FROZEN_AUTHORITY` vs `IMPLEMENTATION_POLICY` are labelled;
`full_route_passes` is refused as a lower-layer constraint; `chunk_reads` cannot satisfy the
`full_reads` floor; and no source-dependent byte ceiling is invented. So this is a **runtime/
binding defect, not a warrant/runtime contract conflict** — the successor is coherent and the
runtime simply cannot yet realize it.

## Why the green courts are not evidence here

- `test_zero_ceiling_refuses_before_the_operation` **asserts the Attack-A behaviour** (zero
  ceiling → `ROUTE_PASS_LIMIT_REACHED`, no session) and only covers a FULL plan, never the
  non-route sources it breaks.
- `test_failed_first_attempt_is_not_reported_as_a_completed_pass` calls `ex.session.run()`
  **directly**, bypassing the public wrapper, and positively asserts
  `route_pass.admits(...) is True` — that a retry *would* be admitted — without testing whether a
  second `execute()` then performs a second source operation.
- No court exercises a transient-failure-then-success retry, a post-operation constraint failure
  followed by inspecting the counter, or an injected module arriving.

## Required repairs (all blocking)

| ID | Requirement |
|---|---|
| `ROUTE-PASS-01` | increment the outer account **only** for plans that are governed full route passes; `maximum=0` means "no route pass admitted", not "no operation" |
| `RETRY-01` | add a pre-operation retry/attempt gate and counter, distinct from completed passes; refuse a second attempt under max 0 **before** any source operation |
| `COMPLETION-01` | increment the completed-pass counter only after all post-operation constraints hold, or roll it back |
| `INJECTION-01` | store and forward the supplied module, or remove the parameter; record the resolved reader identity |

Plus the five test-coverage repairs in `07_FINAL_DISPOSITION.json`.

## Disposition rationale

Not `…ACCEPTABLE__WARRANT_SUCCESSOR_COMPATIBLE` (four blocking defects). Not either `PARTIAL`
variant (each names only a subset of four). Not `R7_REQUALIFICATION_FAILURE` (all courts pass).
Not `WARRANT_RUNTIME_CONTRACT_CONFLICT` (the successor is coherent; the defect is bounded and
runtime-side). The accepted `GovernedSourceSession` mechanism was **not** reopened — no
contradiction in it was found.

## Holds observed

Synthetic carriers only; zero real survey/source access; zero locator discovery; zero warrant
issuance; zero live C4; no production mutation; no C7 or actor/person work. No adoption or
self-adoption. Nothing written outside the commissioned return directory.
