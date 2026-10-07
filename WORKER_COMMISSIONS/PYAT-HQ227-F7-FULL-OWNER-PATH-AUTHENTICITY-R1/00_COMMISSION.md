# PYAT HQ227 — F7 FULL OWNER-PATH AUTHENTICITY REPAIR — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** bounded authority-sensitive implementation worker  
**MODEL / INTELLIGENCE:** **GPT-5.6 Sol High**  
**BRANCH:** `agent/rabochii-pyat-hq227-f7-full-owner-path-authenticity-r1`  
**EXACT STARTUP TIP:** `45b721ee13209b9c0d9ecce3023cd1902de21302`  
**PRIOR REVIEW:** `agent/reviewer-pyat-hq226-f7-resolver-authenticity-final-rereview-r1 @ 2b8946bfef1506bae34b46a55833bad83bfb9d16`  
**PRIOR DISPOSITION:** `F7_RESOLVER_AUTHENTICITY_REPAIR_PARTIAL__NAMED_DEFECT`

Read HQD-216 and the full F7 chain.

## Exact blocker

`F7-RR-04D__EXACT_RESOLVER_INSTANCE_CAN_SHADOW_INTERNAL_OWNER_DISPATCH`

HQ225 hardened only the outer call. The base `SourceRelationResolver.decide` still dynamically reads mutable caller-supplied instance state and nested registry behavior. Exact top-level type is therefore not enough to prove exact owner provenance.

Reinforcing issue:
`F7-RR-04E__NESTED_AUTHORITY_REGISTRY_PROVENANCE_NOT_EXACT`.

Court defect:
`COURT-HQ226-01`: stale hostile witness still patches `require` even though F7 now calls `decide`.

## Mission

Establish a full non-forgeable adopted-owner path for F7 source-relation adjudication.

The repaired path must prove, before a positive F7 receipt:

1. exact resolver construction/provenance or equivalent full-state authentication;
2. exact relation custody;
3. exact relation semantic/hash/replay identity;
4. exact authority-registry provenance;
5. exact authority snapshot semantics at relation scope/use;
6. exact returned decision identity and cross-binding to F7 authority closure.

Do not solve this by duplicating the entire P07 semantic owner inside F7.

If the narrowest correct repair is an authenticated entrypoint/helper in `pre553_source_relations.py`, that owner file may be modified, but only to expose the already-adopted semantics through a non-forgeable path. No new relation semantics, authority kinds, or operations.

## Mandatory attacks

- exact resolver object with post-construction replacement of internal relation maps;
- exact resolver object with replaced/mutated registry;
- exact resolver carrying an AuthorityRegistry subclass that overrides `resolve_exact`;
- relation object injected without constructor validation;
- stale/corrupt replay identity;
- wrong positive authority snapshot with same outer AuthorityRef shape;
- hostile monkeypatch of `decide`, `require`, `resolve_exact`, or nested validation seam;
- concrete lawful positive owner path remains productive.

## Court repair

Replace the stale `require` targeted-break witness with a fail-capable break against the actual load-bearing seam.

The new court must fail against the pre-repair implementation for the intended reason.

## Sustained laws

Preserve:
- HQ220/HQ224 fixes;
- source-scope identity binding;
- exact two-token unrestricted law;
- 12 states / 19 authority kinds;
- exact-zero/no tolerance;
- measure/use binding;
- total precedence;
- 3+ anchor refusal;
- same-universe / zero / increase / decrease / lawful cross-universe positives;
- no F8/ranking/pooling/causal/actor authority.

## Write terrain

Permitted production:
- `rawlsing_next/pre553_temporal_comparability.py`
- `rawlsing_next/pre553_source_relations.py` **only if required to expose a non-forgeable existing-owner entrypoint**

Permitted courts:
- `rawlsing_next/tests/test_pre553_temporal_comparability.py`
- directly relevant source-relation court only if owner hardening is used.

No architecture widening.

## Runtime

Unlike HQ225, execute the exact targeted courts if a lawful runtime surface is available. Report environment and counts truthfully.

## Required return

Write only:
`WORKER_RETURNS/PYAT-HQ227-F7-FULL-OWNER-PATH-AUTHENTICITY-R1/`

Required:
- `00_RETURN.md`
- `01_OWNER_PROVENANCE_AND_STATE_AUTHENTICATION.json`
- `02_NESTED_REGISTRY_AND_RELATION_CUSTODY.json`
- `03_HOSTILE_FULL_PATH_COURT.json`
- `04_PRODUCTIVE_PATH_RUNTIME_AND_REGRESSION.json`
- `05_FINAL_DISPOSITION.json`

Allowed:
- `F7_FULL_OWNER_PATH_AUTHENTICITY_COMPLETE__READY_FOR_FINAL_REREVIEW`
- `F7_FULL_OWNER_PATH_AUTHENTICITY_PARTIAL__NAMED_DEFECT`
- `F7_FULL_OWNER_PATH_REQUIRES_OWNER_CONTRACT_CHANGE`
- `F7_FULL_OWNER_PATH_REVEALS_ARCHITECTURE_CONFLICT`

Push only this branch; report exact SHA.
