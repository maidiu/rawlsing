# R3 RESIDUAL RECHECK — same distinct C

**Verdict: `REVISE_EXACT_CONSEQUENTIAL_GAP` — one exact residual.**
**Target:** `b5e4babe2835a18de3aeabe76a4bfa0f8b9928dd`, author branch
`agent/anvil-r3-downstream-accommodation-20261117-r1`.
**Prior review:** `c996cf1a69344efb2e76e92e9adc2b723c6a2503`.
**Package:** 8/8 payload hashes; 10 capability rows; 32 ledger entries; prior
27 entries byte-preserved; 5 new entries 028–032; product `cea2d4d…` unchanged;
protected `5d387a9…` rev11 unchanged.

Scope is the existing G1/G2/G4 residual and regression check only. No native/
100k, product implementation, benchmark matrix, source/science/actor authority,
protected adoption or H1.

## Residual counterexample — G1 FF01-k reverse cardinality

`R3_FIELD_AND_ADAPTER_CONTRACT.md` §6.2 lines 162–164 states
`direction = FORWARD (P(Y|D))` or `REVERSE (P(D|Y))`, then sets
`target_roles = ordered tuple k>=2` for both directions. The reverse form
`P(D|Y)` has target `D`, which need not be a k>=2 vector; the ordered
`Y1..Yk` set belongs on the conditioner side. `R3-RES-032` repeats “ordered
k>=2 roles” without direction-specific cardinality.

**Minimum correction:** make role cardinality direction-specific:
- `FORWARD`: `conditioner_roles = D` (>=1), `target_roles = Y1..Yk` (k>=2);
- `REVERSE`: `conditioner_roles = Y1..Yk` (k>=2), `target_roles = D` (>=1);
- retain exact per-direction risk/denominator, native fact/query/replay,
  weights/coverage/typed states, owner-held ratio, receipt and prospective
  consumer. Update the table, `R3-RES-032`, and any decision/capability wording
  that repeats `target_roles k>=2` unconditionally. No implementation or new
  science is required.

## Resolved residuals

| Residual | Disposition | Evidence |
|---|---|---|
| **G4-A** state-in-key contradictions | **RESOLVED** | Contract §2 lines 37–64 removes state/value from stable identity keys; checked content conflicts → `TYPED_IDENTITY_CONTENT_CONFLICT`; repeated/ranked events, weight basis/scope/design, coordinate time and routing risk/rule distinctions preserved. |
| **G4-B** count-only membership | **RESOLVED** | Contract §3 lines 66–92 requires exact ordered candidate/risk/denominator member refs and nonselected typed states; counts diagnostic; full `_ReleaseIndex` baseline valid; compact sidecar proposed/owner-qualified. |
| **G4-C** bounded selected RAM/Q | **RESOLVED** | Contract §4 lines 94–110 separates selected pages, full `O(R)` population/routing/weight validation, full membership and refs/output; explicitly no bounded-RAM/Q claim; 6 GiB unproven. |
| **G2EXT** external artifact | **RESOLVED AT PROPOSED ROUTE GRADE** | Contract §5 lines 112–140 defines proposed `ExternalSourceArtifact` kind/ref/digest/source-lineage/native version/scope/rights/current/lookup/receipt/ambiguity/refusal; no existing general resolver and no false current preservation claim. Genuinely unavailable metadata is typed absent/RIGHTS_HELD. |
| **Adapter retention** | **RESOLVED** | Native adapter/`_ReleaseIndex`/`execute_empirical_query` path remains in authoritative `R3_ARCHITECTURE_DECISION.md` §3.2–3.3; it was not lost when the field contract was replaced. |
| **G3** research refs | **SETTLED** | 32 entries, old 27 exact, new 028–032; 29 decision refs, 28 capability refs, 15 falsifier refs and 8 contract refs all resolve. |
| **G5** F6 design variance/PSU/strata | **SETTLED** | Corrected §5.3/CAP-03/08 retain explicit external/typed-absent F6 design/numeric inputs. |

## Research custody

New entries 028–032 accurately describe the residual corrections:
identity-vs-content, full membership, full cost, proposed external artifact and
FF01-k contract. Sources are exact product/contract cuts where inspected,
negative witnesses are present, and dispositions are conditional/owner-held, not
fabricated execution. `R3-RES-032` needs the direction-specific cardinality
correction with the FF01-k table. No sampled fabricated execution or false native
grade found.

## Settled / holds

**Settled:** 13-family canonical body; prepared-first; conditional Q2/full proof/
fallback; conditional recovery; durable index held; v1 fact/replay ABI;
FF01-2 fixed two-target count/no-ratio; G4 identity/membership/cost; G2 external
artifact proposed route; G3/G5; 26 NOT_ADOPTED/14 HELD/F26/52-24-21.

**Deliberate external holds:** external artifact registry/rights/current; FF01-k
method/eligibility/ratio/weighted estimand and implementation; exact compact
membership index; H/S/Q/O measurement; source/actor/science/native rights;
100k/6 GiB/1–10/100.

**Coverage ceiling:** no native/100k, product implementation, benchmark matrix,
full source recensus, source/science/actor authority, protected adoption or H1.

**Smallest next owner handoff:** author edits the FF01-k direction-specific role
cardinality in the table and `R3-RES-032`, then refreezes; no product or new
science work. The rest of the corrected package can stand.

**Return SHA:** final commit on this review branch; original review `c996cf1a…`
and prior R2/C roots preserved unchanged.
