# R4 FINAL CARDINALITY RECHECK — same distinct C

**Verdict: `ACCEPT_SCOPED_STAGE_SENSITIVE_ACCOMMODATION_DESIGN`.**
**Target:** `02594c18f8401855a0f9cecc45921b548fa9aed6`, author branch
`agent/anvil-r3-downstream-accommodation-20261117-r1`.
**Prior C:** `b61f98632cd78bea1b891e552a0a92e672548552` (one G1-REVERSE
residual); earlier `c996cf1a…`, `e4cda70a…`; R2 `d109ffa9…`.
**Package:** 8/8 payload hashes; 10 capability rows; 33 research ledger
entries; prior 32 entries byte-preserved; new `R3-RES-033`; product
`cea2d4d…` unchanged; protected `5d387a9…` rev11 unchanged.

## Cardinality defect — closed

`R3_FIELD_AND_ADAPTER_CONTRACT.md` §6.2 now states direction-specific
cardinality:

- `FORWARD (P(Y|D))`: `conditioner_roles = D (>=1)`;
  `target_roles = ordered Y1..Yk (k>=2)`.
- `REVERSE (P(D|Y))`: `conditioner_roles = ordered Y1..Yk (k>=2)`;
  `target_roles = D (>=1)`.
- No zero-length role list; exact role identity/order; per-direction
  risk/denominator/native fact/query/replay/weights/coverage/typed states;
  owner-held ratio; receipt; prospective consumer.
- `k>=3` must come from a native exact joint fact; fixed GT2 is not widened.

`R3-ARCHITECTURE_DECISION.md` §11 and `R3-CAP-04` repeat the direction-specific
rule; the falsifier explicitly refuses universal target `k>=2` for reverse.
`R3-RES-033` supersedes only the false cardinality sentence of `R3-RES-032`;
the prior 32 entries are preserved byte-for-byte, and `R3-RES-032` remains the
FF01-k product record.

## No pertinent regression

- Stable identity keys exclude mutable state/value and conflict content refuses
  (`TYPED_IDENTITY_CONTENT_CONFLICT`); legitimate repeat/rank, weight basis/
  scope/design, coordinate time and routing risk/rule distinctions remain.
- `SelectionMembership` carries full exact candidate/risk/denominator member
  refs and nonselected typed states; counts are diagnostic; the full
  `_ReleaseIndex` baseline remains valid.
- Selected page reads are separated from full `O(R)` population/routing/weight
  validation, member refs and output; no bounded-RAM/Q claim; 6 GiB unproven.
- `ExternalSourceArtifact` is a proposed owner-route contract with kind/ref/
  digest/source-lineage/native version/scope/rights/current/lookup/receipt/
  ambiguity/refusal; no existing general resolver and no false C11 preservation.
- Native adapter/`_ReleaseIndex`/`execute_empirical_query` path remains in the
  authoritative decision §3.2–3.3.
- G3/G5 remain settled: research refs resolve; F6 design/uncertainty inputs
  remain external/typed absent.
- Research ledger: 33 entries, prior 32 exact, new 033 accurate; no sampled
  fabricated execution or false native grade.

## Accepted scope

Acceptance is of the **whole R3 corrected downstream-accommodation design and
faithful research custody at stage-sensitive conceptual grade**, including the
13-family body; prepared-session-first; conditional source-derived Q2/full
physical proof with second-certificate fallback; conditional recovery;
durable index held; v1 fact/replay ABI; F1–F4/F2/F3 native route; FF01-2 narrow
count and proposed FF01-k direction-specific contract; G4 identity/membership/
cost; G2 external artifact owner route; G3/G5 research and F6 boundaries;
26 NOT_ADOPTED/14 HELD/F26/52-24-21.

## Remaining holds / qualification

External artifact registry/rights/current; FF01-k method/eligibility/ratio/
weighted estimand/implementation; compact exact membership index; H/S/Q/O
measurement; FF02 material power, F7 comparability, N9/N10W, SEAM encounter,
SOROK actor; original35/source/science/actor/native rights; 100k/6 GiB/
1–10/100; product implementation and protected receiving/H1.

No code, product, native/100k, performance, source/science/actor, protected
adoption or H1 acceptance is claimed. Coverage remains sampled; no exhaustive
141-row recensus.

**Return SHA:** final commit on this review branch; prior review evidence
preserved unchanged.
