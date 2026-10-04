# HQ198-R1 Return — R9 technical-value freeze candidate

**Disposition:** `NO_NEW_VALUES_LAWFULLY_BINDABLE`
**Branch:** `agent/rabochii-pyat-hq198-r2`
**Startup SHA (verified exact):** `bf6dcf17a17f41285f2c1e2b1f10a79417c7c393`
**Base successor:** `2410eb7b215f904fa428df82e47fb05ede91ee21`
**Candidate analysed:** `4b6335ca5fc485108b0ffb1d682a29a02e1eee51` (code-bearing repair `a483cb661`)
**Checkout mode:** `SPARSE_REQUIRED` — sufficient. No clone, no full materialisation.

---

## Headline

**The repaired broker is a large advance on enforceability and no advance at all on authority.**

Of 78 accounts: **64 are now measurable and cap-able before the operation**, 40 were already bound by frozen
authority, **38 remain pending**, and **zero numeric budgets were bound in this lane.**

| | count |
|---|---|
| accounts total | 78 |
| already bound by frozen authority | 40 |
| still pending | 38 |
| **newly bound this lane** | **0** |
| measurable + enforceable now | 64 |
| measurable but no numeric budget | 31 |
| not measurable — no owner at all | 7 |

Delta versus the base successor: **none**.

---

## The two facts, kept apart

The commission's central instruction was to distinguish these, and the whole answer turns on it:

- **`measurable_enforceable`** — the candidate can count it and cap it **before** the operation.
- **`numeric_budget_known`** — an exact/floor/zero/max **pre-launch** value actually exists.

64 accounts now satisfy the first. 31 of those still fail the second. Reporting an enforceable-but-unbounded
account as a bound budget would fabricate authority. The repaired broker closes the first gap entirely; it
does not touch the second.

---

## Why nothing could be bound

The binding law allows a value to move from pending only if frozen authority supplies it, **or** the
candidate's control flow makes it exact and source-independent **at the governed scope**.

Gate 2 fails uniformly, and I checked the commission's own premise first:

> `GovernedSourceSession` — the type named in the commission — **does not exist**. `git grep` over the
> candidate tree returns zero occurrences.

The nearest real type is `SourceAccessBroker`, and it is constructed **inside `_decode`**. So its scope is
**one decode call, not one warrant source entry**. Concretely:

1. No per-source session registry, no `session_for(source)`, no `per_source` mapping anywhere in the tree.
2. Nothing enforces or records that exactly one `_decode` occurs per source. A caller that decodes twice
   produces two opens and **nothing at the warrant layer detects or forbids it**.
3. Broker release is caller-responsible via `close_source_access()`, with **no `__del__` and no finalizer** —
   the governed open's lifetime is not frozen.
4. `SourceBackedC11SessionCache` caches derived C11 releases keyed by SHA-256. It is not a physical session
   owner.

### What the candidate's own audit proves — and what it doesn't

The closure audit is genuinely good work: a positive-controlled static AST walk of the accepted C4 closure
(21 accepted modules + broker = 22) finds **exactly one source-path open *site*** at `broker:326`, and zero
raw path strings reaching pyreadstat. The auditor reports 2 raw-path calls on the out-of-closure WVS7
materializer, so the zero is a real negative rather than a broken query, and it documents three of its own
false-zero defects it found and fixed.

But **a count of open *sites* is not a count of opens *per source*.** And `SourceAccessBudget.path_opens`
defaults to `1` — while its own docstring says the caps are "policy ceilings whose purpose is to STOP a run;
they are not claims about expected behaviour."

So I did **not** bind `path_level_opens = 1`.

---

## Path opens — the specific trap, declined

The commission warned against binding 1 "merely because the broker is capable of one open." It is. But
capability is not scope. **GOV-SCOPE-001** stays open, with the missing owner named: a warrant/execution-
surface-level per-source session owner, constructed once per bound source entry, shared by every admitted
operation for that source, closed deterministically rather than by caller discipline, and making aggregate
per-source counts enforceable at that scope.

That single defect blocks *every* remaining numeric budget at once, which makes it the highest-value item in
the programme.

---

## Reader bytes — enforceable, still no number

The repair is real: the limiter never raises inside the read callback (a raised exception in a file-like
object a C extension calls from arbitrary state can be swallowed, become a short read, or hang). It
shortens each request to the remaining allowance and returns `b''` at exhaustion, surfacing a typed
`READER_BYTES_LIMIT_EXCEEDED` at the outer decode boundary. Measured: cap 611 completes, cap 610 refuses at
exactly 610 bytes, `within_cap_in_every_case: true`.

**611 bytes is the requirement of a 3-column × 60-row synthetic SAV.** That is not a warrant budget, the
real requirement is source-size dependent, and I did not use it. `byte_counts_where_measurable` stays
pending under `GOV-BYTES`.

---

## Two findings the candidate did not flag

**`decoder_invocations` has no counter at all** (`GOV-DEC-003`). Zero occurrences in the broker.
`SourceAccessAccount` counts `reader_invocations` — compiled-reader calls of any kind — but there is no
decoder-entry counter, and the receipt's `measurement_basis` lists none. So an O1-C07 *mandatory* account has
**no owner**. `reader_invocations` is not a substitute: under the settled non-substitutability law a reader
invocation may not be renamed a decoder call. This accounts for all 7 unmeasurable entries.

**The header-prefix read is unconditional** (`GOV-HDR-002`). `decoder:639` calls
`broker.header_prefix(176 if SAV else 512)` for **every** source, outside any operation-class branch — the
R35-I01 metadata digest consumes it. But frozen authority admits a header-prefix read **only for SRC26**. So
on the SRC02/SRC06/SRC14 selected route and on SRC08/SRC12/SRC27 the candidate performs an operation the
admitted class does not cover. Binding `1` would authorise an unadmitted operation; binding `0` would
contradict the control flow. Both are wrong, so it stays typed and is raised as its own finding.

---

## SRC27 — special law fully preserved

`governed_full_route_passes` EXACT 1 (max 1); existence/hash/metadata/full each **FLOOR 1, not promoted**;
retries ZERO 0; lower-layer separation intact. `path_level_opens` **still UNBOUND** — authority's word
"multiple" is recorded verbatim and **not numerified**, because the candidate does not make the count
source-independent at the governed scope and SRC27's scope is the widest of the seven. **No selected-read
count invented.**

## Selected reads — frozen values untouched

Frozen `selected_reads=1` / `full_reads=0` for SRC02/SRC06/SRC14 remain bound at EXACT and were **not
loosened**. Only the newly *dependent interpretation field* is conditional, under
`PENDING_INDEPENDENT_HQ198_CONFIRMATION`. One enforcement upgrade is real though: the selected route now pins
`SourceAccessBudget(full_reads=0)`, so a full read is **refused before it executes**.

## PRQ-07 — deliberately not carried

The obsolete "independent integration review not completed" blocker is recorded as
`DISCHARGED__MUST_NOT_REAPPEAR` per HQ197 adjudication line 18, and is **not** carried into this candidate.

## One blocker I recorded without adjudicating

The candidate's exact R7 six-file court did **not** reach target: 55 collected, **49 passed / 6 failed**,
identically before and after the refinement, against a target of 55 passed twice. The candidate attributes
all six to `FileNotFoundError` on `WORKER_RETURNS` paths outside the commissioned sparse manifest, and states
the identical six fail at pre-candidate code. That is consistent with its account, but **this lane did not
reproduce the court**, so `CAND-R7-005` stays open rather than being accepted or rejected on its word.

---

## Status unchanged

`signed=false`, `issued=false`, `authorizes_access=false`, `execution_authorized=false`. Both approvals
`UNSET`. All seven locator placeholders unfilled. No locator search, no source access, no source execution,
no production mutation.

## Artifacts

`00_RETURN.md` · `01_ACCOUNT_BY_ACCOUNT_TECHNICAL_REVIEW.json` · `02_NEWLY_BINDABLE_VALUES.json` ·
`03_STILL_UNBOUND_VALUES.json` · `04_UPDATED_ISSUANCE_BLOCKER_MATRIX.json` ·
`05_UNSIGNED_TECHNICAL_VALUE_SUCCESSOR.json` · `06_FINAL_DISPOSITION.json`

## Recommended next step for HQ

Commission the **per-source session owner** (`GOV-SCOPE-001`) first — it is the one defect blocking every
remaining numeric budget simultaneously. In parallel: a decoder-entry counter (`GOV-DEC-003`) and resolution
of the unconditional header-prefix read against the admitted operation classes (`GOV-HDR-002`). Byte ceilings
need an authority-supplied *rule*, not a measurement. The selected-read interpretation needs the DeepSeek
lane's independent confirmation before its dependent fields un-pend.

`HQ198_R9_TECHNICAL_VALUE_FREEZE_RETURNED__HQ_REVIEW_REQUIRED`
