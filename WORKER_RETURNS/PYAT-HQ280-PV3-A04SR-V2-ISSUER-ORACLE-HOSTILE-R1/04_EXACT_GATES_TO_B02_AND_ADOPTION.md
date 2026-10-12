# A04SR — exact gates to B02 and adoption

## Separate grades
| dimension | grade |
|---|---|
| `TECHNICAL` | **narrow acceptance** — v2 is a real, self-consistent, better-modelled contract (26/26) |
| `INDEPENDENT_EXPECTATION_PROVENANCE` | **FAIL / NOT PROVEN** — hash + asserted timestamp ≠ authenticated principal or ordering |
| `REAL_CONSUMER` | **MODELLED_NOT_EXECUTED** |
| `SOURCE_ISSUER` | **NOT ESTABLISHED** |

## Gates that must close before B02
1. **G1 — true preimage mapping.** Replace the copy-translation with an explicit, verified, **injective** v2→A05 (or v2-native oracle) key mapping. Copying a key into a foreign slot is not a mapping.
2. **G2 — fail closed on non-injective dispatch.** `SEMANTIC_TO_DISPATCH` is 3→1 with `fail_closed_on_multiple: false`; a dispatch job must not silently absorb three semantic operations.
3. **G3 — independent custodian.** An owner outside the candidate must hold the expected set **before** execution and publish an authenticated commitment with a time source the candidate cannot set. Until then `INDEPENDENT_EXPECTATION_PROVENANCE` cannot pass — no amount of hashing changes this.
4. **G4 — real consumer.** Bind one qualified product to one actual pre-existing **C1 / Field Forge / learned** consumer and persist the consumer receipt. A synthetic receipt never satisfies an obligation.
5. **G5 — carry the rich identities across the join.** `measure_kind` and `condition_order` must survive into whatever consumes v2; otherwise v2's improvement is lost at the boundary (the A04R defect restated).

## Exact still-open holds
`INDEPENDENT_EXPECTATION_PROVENANCE` · `REAL_CONSUMER` · `SOURCE_ISSUER` · no G0b/EE12/model/world/actor/canonical grant · no self-adoption.

## Verdict on the central question
**A04S does NOT close A04R's interoperability defect. It moves the incompatibility into a translation layer** while correctly declining to reuse A05's schema token.
