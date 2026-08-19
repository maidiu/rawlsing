# SCR554 — Hostile test oracle

**Oracle:** `SCR554_V554_HOSTILE_ORACLE@1.0.0`  
**Purpose:** executable acceptance targets for later implementation; no production implementation is authorized here.

| ID | hostile case | required result |
|---|---|---|
| H01 | Positive admitted structural proposition; `SIG-001`; exact governed time/scope sufficient; no new V553 semantics | exactly one direct semantic basis; one `ELIGIBLE` F1 |
| H02 | Same as H01 but V553 compatibility object is also physically present and adds no rule-required meaning | direct basis counts once; V553 object is rejected-duplicate/reference-only; F1 ID unchanged |
| H03 | `SIG-002` requires exact temporal point meaning | direct admission cannot count; exact V553 key+observation basis required |
| H04 | `SIG-003` requires persistence/change/comparability | direct admission cannot count; exact V553 relational basis required |
| H05 | Admission carries a source year but no rule-required temporal transform exists | year metadata alone does not force V553; direct remains lawful if all other gates pass |
| H06 | Temporal completeness cannot be proved | `UNKNOWN_FAIL_CLOSED`; no positive route/F1 |
| H07 | Required source relation/comparability authority is missing/unknown | fail closed; K06/K07 as applicable; no inferred equivalence |
| H08 | Temporal relational basis is explicitly `NONCOMPARABLE` and direct copy of same proposition is also present | no F1; K08; no downgrade to direct |
| H09 | Required temporal support is gapped/absent and direct copy is also present | no F1; K09; absence is not zero |
| H10 | Exact target-use denial plus maximal legacy strength/readiness/confidence | no F1; K05; scores are inert |
| H11 | Exact observed value is numeric zero with complete positive authority | zero remains measurement; F1 may be `ELIGIBLE` |
| H12 | Two candidates have identical proposition text but different source universes | not duplicates; preserve independently if each rule-eligible |
| H13 | Same text/source but different estimand or measure/weight authority | not duplicates; preserve independently |
| H14 | Same source/measure but materially different semantic authority version/hash | not duplicates unless governing authority proves semantic equivalence |
| H15 | Direct and V553 candidates share collision probe but one material equivalence component cannot be dereferenced | `EQUIVALENCE_UNKNOWN`; affected collision set emits no F1 |
| H16 | Reissued/aliased direct admissions are exactly semantically equivalent | count once; one canonical semantic basis; preserve sorted alias refs |
| H17 | Multiple equivalent V553 physical rows/objects arrive in different order | count once; semantic IDs invariant to order |
| H18 | Two exact lawful distinct structural bases overlap in geography/time | preserve two candidates/F1s; no netting, averaging, winner, or majority |
| H19 | Only interpolation/backfill/nearest-wave/country-year projection supplies apparent temporal support | no F1 from that support |
| H20 | Basis identity can be reconstructed only by shared label/proposition text/fuzzy match | fail closed; no semantic rematch |
| H21 | Raw `EmpiricalFact` sent directly to V554 | reject presemantically; no F1/F2 |
| H22 | `DiscoveryResultReceipt` or PSEPF sent as V554 basis | reject presemantically |
| H23 | K01/K02/K03 runtime binding is unresolved but static authority is complete | preserve F1; emit exact deferred F2; do not convert to K06/K07 |
| H24 | Required static authority is missing but implementation calls it “deferred” | reject; K06; no F1 |
| H25 | Required static authorities conflict; no producer precedence | K07; no score/recency/majority tie-break |
| H26 | Exact producer-governed precedence resolves a same-jurisdiction authority conflict | obey producer precedence exactly; no V554-local heuristic |
| H27 | Input row/file order is permuted | identical equivalence groups, support count, F1/F2/B1 IDs |
| H28 | Legacy seed scores/readiness are mutated with semantic authority unchanged | canonical result unchanged |
| H29 | V554 rule version/hash changes with otherwise identical evidence | identity/fingerprint changes; no silent reuse |
| H30 | Source-universe or estimand identity changes with same proposition label | identity changes; no collapse |
| H31 | Rejected duplicate V553 compatibility object is added/removed around a lawful H01 direct basis | F1 identity/support count unchanged |
| H32 | Coherent run has zero eligible candidates | `VALID_EMPTY`; zero F1; no dummy seed |
| H33 | Integrity/hash/reference corruption occurs before semantic evaluation | `INTEGRITY_FAILURE`; no semantic denial/F2 fabricated |
| H34 | Producer-backed nonpositive K05-K09 context is published through B1 | `allowed_v555_structural_use=false`; exact negative refs survive |
| H35 | Positive F1 + K01/K02/K03 deferred conditions | B1 may be structurally usable; V555 transports exact F2 refs, not satisfaction |
| H36 | V555 attempts to reconstruct eligibility from StructuralEmpiricalAdmission/V553/legacy seed without F1/B1 | reject; V554 semantic object is missing |
| H37 | Same proposition/admission feeds one static rule and one temporal rule | separate rule/use invocations; static may use direct, temporal must use V553; no cross-rule dedup |
| H38 | A V553 object contains extra temporal semantics irrelevant to a `SIG-001` invocation | extra irrelevant semantics do not manufacture independent support; V553 basis counts zero for `SIG-001` |
| H39 | Applicable temporal negative governs a temporal invocation, while a genuinely separate independently identified direct invocation is outside that negative's scope | temporal invocation blocked; separate direct invocation evaluated independently; no broadening of negative |
| H40 | File name says “canonical” but immutable content hash/authority ref mismatches | fail closed; names never repair identity |

## Required invariants

1. One proposition/use/rule equivalence group contributes at most one semantic support basis.
2. `basis_kind` does not force non-equivalence.
3. Source/universe/estimand/measure/weight/semantic-authority distinctions survive when material.
4. `EQUIVALENCE_UNKNOWN` never proceeds.
5. No latest/score/readiness/majority/file/row-order precedence exists.
6. Temporal/source negatives cannot be downgraded into direct positive support.
7. F1 is positive `ELIGIBLE` only.
8. F2 remains exactly the nine ADP-001/CAN-001 kinds.
9. B1 preserves exact canonical F1/F2 identity and typed nonpositive context without reownership.
10. Replay is permutation-invariant and content/authority-version sensitive.
