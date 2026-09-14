# PRE-V3 SOURCE-STATE/TARGET-DISPOSITION PRODUCTION INDEPENDENT QUALIFICATION R1

Status: **BLOCKER**

Branch: `agent/rabochii-prev3-w10-l02-source-state-target-independent-qual-r1`

Commission tip: `44d19b442d480df0585507b99d9eec3e0cdd8539`

Candidate under court: `639aec0e6b8310f07283922faf0afdc7e3dc7c48`

Grain: `PREV3_SOURCE_STATE_TARGET_DISPOSITION_PRODUCTION_INDEPENDENT_QUALIFICATION_R1_ONLY`

Authority ceiling: independent qualification only; **zero repair authority**.

## Smallest exact blocker

K02 was commissioned to productionize the accepted J02 source-state → target-disposition contract. The exact accepted J02 schema is blob `a4d916a553b6c5039c57ea8607a15c5ac2df5c47` under J02 return `4c86fb44d06e27763b004dbd3181271cfb83efc1`.

K02's production core narrows/renames that accepted schema without authority:

| Accepted J02 surface | Accepted token | K02 production behavior |
|---|---|---|
| `source_local_governed_state.state_class` | `SOURCE_NOT_APPLICABLE_OR_INELIGIBLE` | rejected by `normalize_contract` as unknown source-local state class |
| `product_target_disposition.disposition` | `TYPED_MISSING_NONRESPONSE` | rejected by `normalize_contract` as unknown product-target disposition |
| `product_target_disposition.disposition` | `NOT_APPLICABLE_OR_INELIGIBLE` | rejected by `normalize_contract` as unknown product-target disposition |

The K02 core instead exposes source class `NOT_APPLICABLE_OR_INELIGIBLE` without J02's `SOURCE_` prefix and restricts product dispositions to `TARGET_MEMBER`, `RESOLVED_NON_TARGET`, and `UNRESOLVED`.

This is an exact production-contract incompatibility, not a naming-style objection. A generic caller that emits a lawful J02 contract object with the accepted tokens cannot pass through K02's production normalizer.

## Typed-missing denominator finding

The court also establishes the narrowness of the blocker. K02 can map a typed-missing source state to `UNRESOLVED`; that remains fail-closed and does not silently delete that member from the denominator. Therefore this return does **not** accuse K02 of typed-missing self-deletion. The failure is that K02 cannot faithfully accept/represent the exact J02 contract it was commissioned to productionize.

## Exact candidate bindings

The hostile court pins K02's exact producer content:

- `rawlsing_next/source_state_target_disposition_contract.py` SHA-256 `8c75d41d846363329147ad30187bd30cbfd6dc2e1105f2304e3d94db4150f1d4`
- `rawlsing_next/pre553_source_state_target_disposition.py` SHA-256 `918f0a7e7c8622cc07b9234740e260ac2e4e7560a5aab3ddf534db9b3c36aa6e`
- `evidence/selftest/prev3_source_state_target_disposition_production.py` SHA-256 `663f3ec3ea0d1d838b8a75b1ee75759a6d971b4ef2cbae9a37d1cb09545ee220`

It separately pins accepted J02 schema Git blob SHA-1 `a4d916a553b6c5039c57ea8607a15c5ac2df5c47`.

## Governed independent court

A temporary **draft** PR was used solely as the repository's governed execution surface, with frozen K02 producer branch as base. It was never merged and has been closed.

- temporary PR: `#368`
- base: `agent/rabochii-prev3-w9-k02-source-state-target-production-integration-r1`
- base SHA: `639aec0e6b8310f07283922faf0afdc7e3dc7c48`
- workflow run: `34806152954` / run number `417`
- evidence execution SHA: `a72f8d571fd2d7d103700be00600e6cb2cc6d6a2`
- semantic candidate SHA: `639aec0e6b8310f07283922faf0afdc7e3dc7c48`
- synthetic PR SHA: `d512a81eff8d1719da0005ac10ac81c66f241211` — execution-only synthetic merge identity; no merge occurred
- court spec SHA-256: `59d2d94b73cf6cd6af8c8d652180fedc32ebac4e5cca44018cdef8f4d081ebae`
- protocol self-tests: **20 passed in 0.06s**
- hostile court: **5 passed in 0.03s**
- receipt artifact ID: `10333235919`
- receipt artifact ZIP SHA-256: `96d03830e7375e93150ebd7a72b61840856fcdcfcfde69f8669f6ac0efe747f2`

A green hostile court means the blocker reproduced deterministically; it is **not** a K02 qualification PASS.

## Court test identities

`rawlsing_next/tests/test_prev3_source_state_target_disposition_independent_qualification.py`

1. `test_exact_k02_candidate_and_j02_authority_are_frozen`
2. `test_k02_rejects_j02_lawful_source_not_applicable_class`
3. `test_k02_rejects_j02_lawful_typed_missing_product_disposition`
4. `test_k02_rejects_j02_lawful_not_applicable_product_disposition`
5. `test_blocker_is_schema_drift_not_denominator_self_deletion`

## Commission disposition

Per the commission's `PASS or smallest exact blocker` law, qualification terminates at this exact blocker. No repair was attempted. Because a producer that rejects the accepted parent contract cannot be independently qualified as that contract's generic production implementation, further hostile closure cannot convert this candidate into PASS.

No K03 source-specific return was consumed as proof. No learned workload was executed. No production file was modified. No structural/causal/person-state semantics were introduced. PRE-V3 remains objective-world only. Quarantined OBL063 driver/type/person-terminal semantics were not revived. MAIN and PRE-MAIN were not mutated.

## Successor gate

**K02 is not qualified.** A competent producer-owner repair/recommissioning must restore exact compatibility with accepted J02 law, after which a fresh independent qualification is required. HQ must not treat L02 as converged with L03 for learned positive re-execution while this blocker remains.
