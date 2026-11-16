# OPS-04R — Corrected C4 decision packet (C1 withdrawn)

Status: `PENDING_EXTERNAL_ASTRA_ADJUDICATION__NOT_AN_ADOPTION_DECISION__DOES_NOT_LIFT_HQ182_HOLD`.

Successor to `00_C4_CONSOLIDATED_DECISION_CLAIMS.md`. That document is
preserved unmodified. HQ186 supersedes its finding **C1** only. C2–C5 stand.

## C1 — WITHDRAWN IN FULL

HQ183 asserted: *"Sol shadow HQ's byte-identity justification is false —
the producer blob at the freeze is `2385cd32`, at M01 bounded-court time it
was `6560d7a9`, changed by `903c262e4`."*

**That finding is wrong. HQ withdraws it without qualification.**

The user supplied Sol's explicitly named qualified candidate
`46f3bec824c1c9da7037bacf94ec08923bc33506` and the M01 court-run head
`74a067742a370d4f6296c56140c28cc8acc53e63`. HQ reproduced the comparisons:

| File | `46f3bec82` | `8ff40d37d` (freeze) | |
|---|---|---|---|
| `rawlsing_next/pre553_route_b_production.py` | `2385cd32…` | `2385cd32…` | **MATCH** |
| `rawlsing_next/pre553_carrier_execution.py` | `e7cda773…` | `e7cda773…` | **MATCH** |
| `rawlsing_next/tests/test_pre553_route_b_production.py` | `d244eaaa…` | `d244eaaa…` | **MATCH** |
| `rawlsing_next/tests/test_pre553_carrier_execution.py` | `bc0db646…` | `bc0db646…` | **MATCH** |

Producer at the M01 court-run head `74a06774` = `2385cd327dced3c5b887b59085aa0d21b04d78c3`
— identical to the freeze.

Both commits are ancestors of C4A `8f7efe690`.

### Why HQ was wrong

HQ read the **first** M01 court binding instead of the **final** one. The
bounded court was rebound four times, and HQ inspected only the earliest:

```
295d270c3  Temporarily bind bounded court to HQ117 M01 qualification
903c262e4  Fix M01 authority preimage canonical verification   <- HQ treated this as post-court
c0f538b6c  Rebind M01 court after verifier fix          -> semantic_candidate_sha = 903c262e4
a1545aeef  Tighten M01 hostile assertions to owner semantics
ddf0ccfee  Rebind M01 court after hostile assertion correction -> semantic_candidate_sha = a1545aee
46f3bec82  Compare canonical topology refs by exact serialized identity
74a06774  Rebind M01 court after exact-ref assertion correction -> semantic_candidate_sha = 46f3bec82
```

`74a06774` changed **only** `.rabochii/court_spec.json` (1 insertion,
1 deletion), repointing `semantic_candidate_sha` from `a1545aee…` to
**`46f3bec82…`**. Its `tests` array is exactly the four bounded-court files.
The 61/61 PASS therefore binds to the freeze's exact bytes.

HQ's error was inferring chronology from commit messages and dates instead
of reading the court binding. That is the same failure mode as HQ182's C2,
where a truncated grep was completed by guessing. It is recorded here as a
recurring HQ failure mode, not a one-off.

### Corrected finding

**Sol's shadow ground (1) is CORRECT.** The producer and carrier at the
freeze are byte-identical to the M01-qualified candidate. The M01 bounded
court (61/61: 11 + 4 + 14 + 32, GitHub Actions run 36302391261) qualifies
the exact freeze bytes.

**HQ183's substitute basis is not needed and is withdrawn as the primary
basis.** The C4A combined-court observation (the producer's 11 tests sit
among the 76 passed; the 3 failures are `test_fiabc_*`, triaged INHERITED)
remains factually true but is corroboration, not the load-bearing argument.

**No counterexample exists.** HQ attempted to produce one and could not.

## Findings that stand unchanged

| ID | Verdict | Note |
|---|---|---|
| C2 | UPHELD | R7 wording is "from **this path alone**", not "from the repository", and the record supplies a pinned 13-package `reproduce_command`. R7 = fingerprint incompleteness |
| C3 | UPHELD | 38 SHA-256 prefixes (32×16-hex + 6×32-hex) **+ 2 complete 40-hex Git SHA-1 tree identities**; HQ182's "40 truncated SHA-256" was wrong |
| C4 | UPHELD | R9 narrowed: per-source constraints survive in artifact 07; only explicit per-source read-limit counters are absent from the warrant |
| C5 | UPHELD | R10 full digest `7dfb62362b983b92dee2774d862a46c0c0ce3ca2c3bb48850e0f400346936908`, recovered from C4B, not guessed |

## Stage-separated blockers — unchanged by this correction

- **Freeze acceptance: 0**
- **Warrant issuance: 1** — R9, add explicit per-source read-limit counters bound to artifact 07's frozen expectations
- **Live execution: 1** — R7, preserve durably with a complete interpreter digest, or re-qualify from the pinned recipe
- **Advisory: 9**
- **Counterexamples: 0**

C1's withdrawal *removes* a claimed counterexample. It does not unblock any
stage and does not weaken any hold.

## Corrected permanent wording, if later authorized

> The exact frozen source-free implementation is accepted at the declared
> grain. The Route-B producer and carrier at the freeze are byte-identical to
> the M01-qualified candidate `46f3bec82`, whose bounded source-free court ran
> 61/61 under GitHub Actions run 36302391261, rebound at `74a06774`.
> C4C3's 21-module trace is a downstream trace beginning below M01; the
> producer-inclusive static closure is 23 modules. No claim is made that the
> complete producer-inclusive M01 path was freshly rerun on Darwin.

Terminal: `OPS04R_C1_WITHDRAWN__C2_C5_UPHELD__PENDING_ASTRA__NO_ADOPTION__NO_SOURCE_ACCESS`