# HQ197-R1 Return — physical-selected operation interpretation

**Disposition:** `PHYSICAL_SELECTED_MEANS_SOURCE_LAYER_PLUS_SELECTED_READER_MODE__USECOLS_ROUTE_COMPATIBLE`
**Branch:** `agent/rabochii-pyat-hq197-r2`
**Startup SHA (verified exact):** `740a355b3aef0255dc6ecbe1b99bc9382ec3c91f`
**Checkout mode:** `SPARSE_REQUIRED` — sufficient. No clone, no full materialisation.

Documentary forensics. Zero source access, zero source execution, zero production mutation.

---

## Determination: **A**

`PHYSICAL` names the **physical-source/witness layer and its proof-mode tier**. `SELECTED_VARIABLE_READ`
names the **reader-invocation mode and returned output scope**. The usecols route is compatible — but
only with an honest non-suppression disclosure.

I did not decide from implementation convenience. I weighed A and B independently, and the answer came
from four documentary grounds that have nothing to do with the current code.

---

## Where the terms were born

`git log --reverse -S<token>` dates each term's *first* introduction, not its latest use.

**1. `33dba5236` (2026-09-30) — first `PHYSICAL`.** The originating document is
`PYAT-C2-02-C4-PROVING-WORKLOAD-R1/02_PROPOSED_PROVING_SET.json`, and its vocabulary is a **workload
tier taxonomy**:

```
workload_tiers:
  full_route_empirical_anchors     → SRC27, SRC35
  bounded_physical_edge_witnesses  → SRC02/06/08/12/14/26
proposed_public_route:
  full_route_sources            → SRC27, SRC35
  bounded_physical_only_sources → SRC02/06/08/12/14/26
```

The term was **born as an evidence/access classification**. Each bounded physical source witnesses
exactly one narrow representational property — G01 user-missing, D01 BIG5, D02 opaque date, R05 header
divergence. `PHYSICAL` was never an I/O granularity.

**2. C4B carried it unchanged** as `read_economy.bounded_fresh_physical`, with
`semantic_route_status: NOT_SELECTED_AS_SEMANTIC_ROUTE_ANCHOR` on all six, versus real semantic
authority for SRC27/SRC35. The C4B commission itself calls it *"exact physical-only versus full-route
proof mode"* (line 33).

**3. `8ff40d37d` — first `expected_selected_reads` / `expected_full_reads`.** The name changed
`..._SELECTED_VARIABLE_READ_ONLY` → `..._SELECTED_VARIABLE_READ` at exactly the moment numeric counters
appeared. `READ_ONLY` had meant **"only a read is performed"** — bounded, non-retaining,
non-semantic. It was dropped when a qualitative adjective became a counted budget. It never meant
"only these bytes".

---

## The four decisive grounds for A

**A1 — the origin is a tier taxonomy** (above). `PHYSICAL` = witness tier.

**A2 — the sibling-account structure.** The C4 commission PHASE 6, the very instrument that introduced
the counters, enumerates:

> `selected-column reads` · `full reads` · `byte counts where measurable`

as **three siblings**. If a selected read were *defined* by byte suppression, byte counts would be a
**consequence** of it, not an independent account. HQ190-C independently grades `ACC-07_selected_reads
= E(1)` while grading `ACC-09_byte_counts = "—"` in the same object. A third and fourth lane do the same.

**A3 — the defining C3 authorities own no I/O whatsoever.** I traced them directly:

- G01 `authorized_sav_numeric_physical_material(source_sha256, variable_name, ordinal, native_code)` is a
  **pure representation lookup** — no read, no `usecols`.
- The accepted qualified tests for G01 and D02 contain **zero** `pyreadstat` / `read_sav` / `read_dta` /
  `usecols` references.

An authority that never invokes a reader cannot require or measure physical read suppression for its own
witness.

**A4 — the chain's own decoder realises scope at emission.** `pre553_physical_decoder.py` has **zero**
`usecols`; `_decode` accepts **no** variable parameter at all; `variables` is *every* metadata column;
`iter_batches` calls `read_file_in_chunks` unrestricted and emits `PhysicalCell` only for
`self.variables`. So the selected scope lives at the **cell-emission layer, downstream of a whole-file
read**. Under B, the defining implementation would violate its own ceiling at freeze time — not a
coherent reconstruction of intent.

**A5 — zero suppression vocabulary.** `suppress`, `column-level`, `byte-level`, `projection`,
`unselected`, `partial read`, `skip columns`: **0 hits** across all seven commissioned artifacts.
`usecols` itself: **0 hits**. A law that requires suppression states it. B's requirement appears nowhere.

---

## What `full_reads = 0` actually means

> **Zero reader invocations whose configured output scope is the whole source.**

For SRC02/SRC06/SRC14 the run may never issue an all-column row-data read. Every row-data invocation
must carry an explicit selected-column scope.

It does **not** mean zero bytes were consumed, not a single physical pass, not that the file went
unscanned, and — importantly — it does **not** license an unselected whole-file read. An invocation
without a selected-column scope **is** a full read by this definition and is a STOP.

One consistency finding worth HQ's attention: at freeze, `compatibility_full_read = encoding is not
None`, and SRC02/06/14 use the `SAV_ENCODING_NULL` lane, so `_decode` itself issues **no** compatibility
full read. But `iter_batches`, with no retained frame, issues an **all-column chunked read** — which is
a full read under this meaning. So `full_reads=0` is **not** satisfied by the frozen batch route. That
is R9-SEL-03, and it stays open regardless of which reading is adopted — under B it would be
unfixable on this runtime; under A it is fixable.

---

## The truthful accounting rule under A

Full rule set R1–R8 in `05_ACCOUNTING_RULE_UNDER_A.json`. The load-bearing parts:

- **R1** — `selected_reads = 1` requires exactly one invocation with an explicit selected-column scope
  equal to the bound set (Q10B@58 / Q101@20+Q2061B@19 / v372@466), names **and** ordinals validated
  against the real column inventory **before** any row-data read.
- **R4** — `full_reads = 0` is enforced by **refusing** any row-data invocation carrying no
  selected-column scope, **before it executes**.
- **R5** — the physical read calls and bytes go **only** into the byte/read-call accounts, never folded
  into `selected_reads`.
- **R6** — a machine-readable non-suppression disclosure is mandatory, and a court must **assert its
  presence** so it cannot be quietly dropped.
- **R7** — `selected_reads` must never be presented as evidence that unselected columns went unread.

The candidate at `d5ce4ecf` already conforms to R1–R6 and R8, and already carries
`selected_route_physical_column_suppression: NOT_ENFORCED_BY_READER` with a court asserting the
disclosure.

**What the rule does not buy:** it does not reduce physical I/O, does not implement the route, does not
close R9-SEL-03, and does not bound bytes — `byte_counts_where_measurable` is still UNBOUND.

---

## Why I did not return AMBIGUOUS

The honest weakness of A: **no artifact contains a verbatim definitional sentence** for
"selected-column read". The counters were introduced as bare numeric tokens, and Alt-B — the review
that *approved* them — did presence-and-consistency checking only, never asking what the figure
measures.

But that is a documentation gap, not a genuine ambiguity. The record **can** distinguish A from B, on
grounds independent of the current implementation (A1, A2, A3, A5). Returning ambiguity would leave
R9-SEL-03 blocked on a question the documentary record does answer.

So I recorded the residual rather than hiding it: **RES-3** states the falsification test — produce any
authority artifact requiring unselected-column bytes or column-level I/O to be avoided, and A collapses
to B or C. If HQ holds the ceiling was meant to bound *physical* rather than *logical* scope, that is a
ratification question, and it converts to B with an Astra decision.

---

## Holds

Zero source access, zero source execution, zero production mutation, no locator discovery, no warrant
issuance, no C7, no actor/person work. The runtime fact that usecols is projection-only was treated as a
fact about pyreadstat, **not** as the definition of the governing term.

## Artifacts

`01_TERM_ORIGIN_AND_CHRONOLOGY.json` · `02_AUTHORITY_CHAIN_TRACE.json` ·
`03_LAYER_SEPARATION.json` · `04_FULL_READS_ZERO_MEANING.json` ·
`05_ACCOUNTING_RULE_UNDER_A.json` · `06_A_VS_B_EVIDENCE.json` ·
`07_LIMITS_AND_RESIDUAL_AMBIGUITY.json` · `08_FINAL_DISPOSITION.json`

## Recommended next step for HQ

Ratify the A reconstruction explicitly and record the RES-3 falsification test, so it is inherited
deliberately rather than silently. Then commission the selected-reader implementation and the exact R7
six-file court, with the non-suppression disclosure as a mandatory asserted field.

`HQ197_R9_PHYSICAL_SELECTED_INTERPRETATION_RETURNED__HQ_ADJUDICATION_REQUIRED`
