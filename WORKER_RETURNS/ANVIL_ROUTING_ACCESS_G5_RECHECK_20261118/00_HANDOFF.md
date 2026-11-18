# ANVIL routing access G5 recheck

## Result

**ACCEPT_SCOPED_CORRECTNESS** — the exact repair findings from `1a02f528` are closed for the frozen repaired routing cut. No consequential defect was found in the independently exercised scope. No product patch was made.

- Repaired code: `aee95429609c372564e996c2d3d3eb30e9253cbf`
- Repaired evidence: `a99cc83250898bcce521ba480cdc1a75f936bc5b`
- Prior code: `73b480080ede013770e0c887aa5aa82af3cfafb2`
- Prior review: `1a02f52800734bcb68d165cef67f79efa0be3d72`
- Accepted product baseline: `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`
- Contract: `15afd22f6d55fe3d208d0a3b63d802de2b4e6f13`
- Review boundary: `e01a2bd7800cd906b12394dda8dcd1ebdf6eb961`

## Closure

- **B1 symbol boundary:** the module-level `_RoutingLookup` and `_routing_lookup` state are gone. `_routing_facts` is a same-class private method of `DirectEstateI03Session`; `indices_for` binds it as the callable `routing_lookup`.
- **B2 index/column:** `routing_locator_resp_idx` and the unused `member_set` locator column are removed. The table is respondent/target/risk/fact_ref/gid/off with the composite primary key.
- **R1 cache:** `_routing_facts` uses the existing one-row-group `_row_group_cache` for `RoutingEligibilityFact`; there is no per-lookup `gids` accumulation.
- **B3 conflict:** the repaired focused test includes a controlled C11 candidate with two genuinely distinct canonical routing facts for the same respondent/target/risk; the physical locator returns both in canonical ref order and `_routing_fact_for` refuses the conflict. A separate adapter witness confirms distinct nonconflicting facts both enter `used` and authority validation.
- **B4 malformed preparation:** a controlled malformed routing body/projection refuses at preparation, before filtered absence can be trusted.

## Independent verification

I unpacked the exact candidate from `aee954...` into an isolated review archive and ran:

- `rawlsing_next/tests/test_anvil_authenticated_routing_access.py`: **8 passed in 4.46 s**
- The suite includes exact full-fact serialization/parity, physical distinct conflict, malformed preparation, CURRENT between yields, revocation/cleanup, missing/corrupt locator, source/root restore, and actual first-consumer paths.

Author evidence at the frozen path was read for comparison (`focused 11 passed`, `existing checks 3 passed/29 deselected`, `changed restore 1 passed`), but is not claimed as independent. Evidence commit `a99cc...` has no product changes relative to `aee954...`; product diff from baseline is exactly the four authorized paths.

## Scope limit

No matched performance court, heavy run, native/raw source, survey-scale, 100k, production, protected, or persistent-substrate claim is made. The physical conflict witness is a controlled C11 candidate, not raw source. The matched runner and its H/S/Q/O accounting are deliberately separate.

## Custody

Own return only: `WORKER_RETURNS/ANVIL_ROUTING_ACCESS_G5_RECHECK_20261118/`. No product edits, no provider switch, no broad backend/research work.
