# PYAT HQ198 — R9 repaired-candidate final independent acceptance — R1

**Disposition:** `ACCEPT_REPAIRED_BROKER_CANDIDATE__PHYSICAL_SELECTED_A_CONFIRMED`

**Terminal:** `HQ198_R9_FINAL_INDEPENDENT_ACCEPTANCE_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq198-r1`
Commissioned startup SHA: `69f9451501e348e739fbbf25872c285ca382e8cf` — **verified equal**
Clean tip reviewed: `4b6335ca5fc485108b0ffb1d682a29a02e1eee51`
Repair commit: `a483cb6619a84c4785296e923a8571447041ffa5`
Checkout mode: `SPARSE_REQUIRED` — honored; no clone, no full worktree, sparse checkout not widened.
Reviewer: DeepSeek Harness, **DeepSeek V4.1 Flash**.

---

## 1. Independence order observed

I reconstructed the frozen meaning of the four terms **from the authority chain alone** and
saved it as `01_PRECOMPARISON_PHYSICAL_SELECTED_INTERPRETATION.json` **before** opening the
worker return at `d43c7f86…`. Only then did I compare (§6).

**My independent determination: A** — `PHYSICAL` names the physical-source/witness *tier*;
`SELECTED_VARIABLE_READ` names the configured reader/output *scope*. The term does **not**
require byte-level suppression of unselected-column data.

## 2. The repaired candidate is accepted

| # | Criterion | Result |
|---|---|---|
| 1 | one application-owned open | **PASS** — `path_opens=1` across metadata/selected/full and across 10+ chunks |
| 2 | no raw path to pyreadstat in closure | **PASS** — one call site, always a `_GovernedView`, `RawSourcePathEscape` guard |
| 3 | DTA reset / fresh view | **PASS** — `row_offset` loop with position-zero views over one open |
| 4 | seam pinned, identity unchanged | **PASS** — pyreadstat 1.3.6; interpreter `11d6f541…` |
| 5 | `reader_bytes` genuinely enforced | **PASS on all six sub-properties** |
| 6 | selected mode honest about non-suppression | **PASS** — disclosure intact and measured |
| 7 | no unrelated production movement | **PASS** — delta is exactly the broker + its court |

## 3. `reader_bytes` is now a real limit

The repair arms a **bridge-safe allowance** for exactly one compiled-reader call; `_read`
shortens each request to the remaining allowance and returns `b""` once exhausted, and the
breach is raised as a typed error at the **outer** boundary. No exception is raised through the
pyreadstat callback — the docstring states the rationale, and the behaviour confirms it.

| Property | Evidence |
|---|---|
| exactly-enough **succeeds** | metadata cap=779 → success, consumed 779; full/selected cap=16779 → success |
| one-byte-short **fails** | cap=778/16778 → `READER_BYTES_LIMIT_EXCEEDED` in ≤0.001 s |
| consumed **never exceeds** cap | caps 0/1/10 → consumed exactly 0/1/10 and refused |
| **no callback raise** as the limit | prompt failures (no hang); the raw raising reproducer still hangs on an unguarded view |
| prompt + **typed** at outer boundary | `SourceAccessViolation` `READER_BYTES_LIMIT_EXCEEDED`; also enforced through the decoder (cap=5000 → consumed=5000) |
| **excludes hash/header** traffic | 8383-byte carrier: hash=8383, header=176, reader=531, total=9090, and `reader_bytes == total − hash − header` **exactly** |

Pre-repair this was dead configuration (HQ197: cap=10 allowed 12,691 bytes). Post-repair the
same cap consumes exactly 10 bytes and refuses.

## 4. R7 court and broker court

- Collect-only: **55 collected**, exit 0.
- Run 1: **55 passed** (64.81 s, exit 0). Run 2: **55 passed** (66.23 s, exit 0).
- Candidate's own broker court: **20 passed**.
- The three fixture patterns materialized natively — **no symlink needed**, as the commission
  anticipated.
- `chunk_rows` independently verified on a **1000-row** carrier: 7 → 143 chunks (max 7);
  100 → 10 chunks; 333 → 4 chunks; all within bound, `path_opens=1` throughout.

## 5. Production-delta isolation

Between `d5ce4ec`, `a483cb66` and the clean tip, the entire `rawlsing_next` delta is:

```
M rawlsing_next/pre553_source_access_broker.py
M rawlsing_next/tests/test_pre553_source_access_broker_court.py
```

The decoder is **unchanged**, and no closure-critical module changed. The repair is isolated.

## 6. Post-comparison with the worker interpretation

The worker also determined **A** — `PHYSICAL_SELECTED_MEANS_SOURCE_LAYER_PLUS_SELECTED_READER_MODE__USECOLS_ROUTE_COMPATIBLE`.
We **agree on substance**. The worker added genuine value I did not have:

- **Term provenance** — `git log --reverse -S` traces the first `PHYSICAL` to `33dba5236`
  (2026-09-30) in the C2-02 proposed proving set, whose vocabulary is explicitly a *workload
  tier taxonomy* (`full_route_empirical_anchors` vs `bounded_physical_edge_witnesses`). That
  independently confirms the tier reading from the term's birth.
- **Layer decomposition** — it records `PARSER BYTE TRAFFIC` as a layer whose governing term is
  **NONE**, and as a separate, separately-**unbound** account (HQ190-C ACC-09 grade `—`). That
  is the decisive structural argument: because byte traffic is its own account and is separately
  unbounded, the frozen law cannot have meant read-counts to be a proxy for byte traffic. My
  reconstruction reached the same place via the O1-C07 separation principle; the worker states
  the structural reason more directly.

**Residual (the worker's RES-1, with which I concur):** no artifact contains a *verbatim
definitional sentence* for "selected-column read"; the tokens were introduced as bare numeric
values. **A is therefore a reconstruction, not a quotation.** The worker supplied a
falsification test — produce any authority requiring unselected-column bytes to be avoided. I
applied it independently and it was **not met**. A is the only reading with textual support, so
I confirm it and recommend HQ **ratify it explicitly** rather than inherit it silently.

## 7. Advisories (non-blocking)

1. `SourceAccessViolation` exposes `.code` and the message in `args[0]` but no `.account`
   attribute — ergonomics only.
2. **Accounting question for HQ:** the default/unselected row-data route is the chunked
   all-column route and counts `chunk_reads`, not `full_reads`. Whether that route must be
   classified as a *full read* for the frozen per-source ledger (notably SRC27's single governed
   full-route pass) remains open and is outside this lane's acceptance criteria.
3. Explicit ratification of interpretation A is recommended.

## 8. Why not the other dispositions

- **`…_AUTHORITY_STILL_OPEN`** — the *wording* is under-defined, but the *meaning* is not
  genuinely open: every available ground supports A and no competing reading has textual
  support. The right answer is accept-with-ratification, not leave-open.
- **`REPAIRED_CANDIDATE_MATERIAL_DEFECT`** — the repair satisfies all six required properties.
- **`R7_REQUALIFICATION_FAILURE`** — 55/55 twice.
- **`MATERIAL_AUTHORITY_CONFLICT`** — my determination and the worker's agree; no text conflicts.

## 9. Holds observed

Synthetic carriers only; zero real survey/source access; zero locator discovery; zero warrant
issuance; zero live C4; no production mutation; no C7 or actor/person work. No adoption or
self-adoption. Nothing written outside the commissioned return directory.
