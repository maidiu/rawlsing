# R5 RED/GREEN — CURRENT AFTER FIRST YIELD

**Command:** `python3 R5_LOCALITY_REVOCATION_REPAIR/revocation_witness.py`  
**Exit:** 0, `all_expected=true`  
**Sealed estate:** `c209d3a198b25e5392dd422878fcc9111ada5c72aeb146d5d2a07388586bbc8b`  
**Family:** `RoutingEligibilityFact`

| Case | First ref | Second call after CURRENT revoked |
|---|---|---|
| R4 old adapter | `...000878d680...` | second ref `...000f3b80b6...`; **no error** (RED) |
| R5 corrected adapter | same | `DirectEstateError: current source/operation authority refused` (GREEN) |
| Original product control | same | `DirectEstateError: current source/operation authority refused` |

Live valid iteration with CURRENT allowed:

- count 600;
- `canonical_sorted=true`;
- `matches_original_order=true`;
- corrected adapter and original method restoration assertions true.

Exact evidence: `revocation_witness.json`. No product edit. Production owner grant remains `REQUESTED_NOT_GRANTED` (#1006 comment6969187403).
