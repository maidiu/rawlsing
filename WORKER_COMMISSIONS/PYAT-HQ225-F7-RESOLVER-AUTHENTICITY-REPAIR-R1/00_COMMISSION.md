# PYAT HQ225 — F7 SOURCE-RELATION RESOLVER AUTHENTICITY REPAIR — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** bounded authority-sensitive implementation worker  
**MODEL / INTELLIGENCE:** **GPT-5.6 Sol High**  
**BRANCH:** `agent/rabochii-pyat-hq225-f7-resolver-authenticity-repair-r1`  
**EXACT STARTUP TIP:** `a190988b58ae1fe5d6a714e0691b19f84eb4e00e`  
**PRIOR REVIEW:** `agent/reviewer-pyat-hq224-f7-final-authority-closure-r1 @ 1b3648bb8a0ecfaafe05ca5d812236f068499b84`  
**PRIOR DISPOSITION:** `F7_FINAL_AUTHORITY_CLOSURE_PARTIAL__NAMED_DEFECT`  
**SELF-ADOPTION:** FORBIDDEN

Read HQD-216 and the full F7 review chain.

## Exact blocker

`F7-RR-04C__HOSTILE_SOURCE_RELATION_RESOLVER_SUBCLASS_CAN_FORGE_OWNER_DECISION`

Current F7 accepts `isinstance(resolver, SourceRelationResolver)`. A hostile subclass can override `require()` and return a request-shaped AUTHORIZED `RelationDecision` naming a genuine positive authority that the concrete owner never adjudicated.

This is a local F7 authority-authenticity defect.

## Mission

Establish a non-forgeable boundary to the adopted source-relation owner without widening architecture.

Required outcome:

- hostile subclass override cannot mint a positive F7 comparison;
- concrete adopted `SourceRelationResolver` path remains productive;
- F7 continues to consume the actual returned RelationDecision and exact relation-authority cross-binding;
- no duck-typed or subclass-shaped caller object may impersonate owner adjudication.

Do not blindly use `type(x) is SourceRelationResolver` without checking current production consumers. First census all production call sites and legitimate resolver construction paths. If exact concrete type is the current owner boundary, enforce it. If current owner law exposes another non-overridable provenance/authentication boundary, use that instead and prove it.

Do not modify `pre553_source_relations.py` unless an exact owner defect is independently demonstrated; this commission is F7-local.

## Mandatory hostile witnesses

At minimum:

1. subclass overrides `require()` and returns full-shaped AUTHORIZED decision with genuine positive B authority;
2. subclass returns right pair/kind/use but relation absent from base resolver;
3. subclass calls base then swaps authority/ref;
4. duck object with same API;
5. concrete resolver with DENIED decision;
6. concrete resolver wrong pair/kind/use.

All 1–4 must refuse before positive F7 receipt.

## Sustained positive paths

Preserve:
- same-universe;
- exact-zero;
- increase;
- decrease;
- genuine concrete-owner cross-universe positive path.

Preserve all existing F7 ceilings, 12 states, 19 authority kinds, source-scope binding, unrestricted-token law, exact use/measure binding, and no new semantic authority.

## Write terrain

Production:
- `rawlsing_next/pre553_temporal_comparability.py`

Court:
- `rawlsing_next/tests/test_pre553_temporal_comparability.py`

No other production mutation.

## Required return

Write only:
`WORKER_RETURNS/PYAT-HQ225-F7-RESOLVER-AUTHENTICITY-REPAIR-R1/`

Required:
- `00_RETURN.md`
- `01_PRODUCTION_RESOLVER_CALLSITE_CENSUS.json`
- `02_NONFORGEABLE_OWNER_BOUNDARY.json`
- `03_HOSTILE_SUBCLASS_AND_DUCK_COURT.json`
- `04_PRODUCTIVE_PATH_AND_REGRESSION.json`
- `05_FINAL_DISPOSITION.json`

Allowed:
- `F7_RESOLVER_AUTHENTICITY_REPAIR_COMPLETE__READY_FOR_FINAL_REREVIEW`
- `F7_RESOLVER_AUTHENTICITY_REPAIR_PARTIAL__NAMED_DEFECT`
- `F7_RESOLVER_AUTHENTICITY_REPAIR_REVEALS_OWNER_CONTRACT_GAP`

Push only this branch and report exact remote SHA.
