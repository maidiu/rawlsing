# PYAT HQ231 — F7 SEALED OWNER-STATE CUSTODY REPAIR — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** bounded authority-sensitive implementation worker  
**MODEL / INTELLIGENCE:** **GPT-5.6 Sol High**  
**MACHINE:** unknown  
**WORKTREE:** not established  
**BRANCH:** `agent/rabochii-pyat-hq231-f7-sealed-owner-state-custody-r1`  
**EXACT STARTUP TIP:** `d8a03fcdf77ca791d7f66ce58e2ed3b3d894bbb1`  
**BLOCKING REVIEW:** `agent/reviewer-pyat-hq228-f7-full-owner-path-final-rereview-r1 @ 11eb7488895665a15b4f820c57f41909e0201fef`  
**BLOCKING DISPOSITION:** `F7_FULL_OWNER_PATH_PARTIAL__NAMED_DEFECT`  
**SELF-ADOPTION:** FORBIDDEN

Read HQD-216 and the complete F7 repair/review chain.

## Exact blocker

`F7-RR-04F__LIVE_AUTHENTICATED_OWNER_STATE_IS_EXPOSED_AND_POSTCONSTRUCTION_REPLACEABLE`

Current defect:

- `_load_owner_state(resolver)` returns the live `_AuthenticatedResolverState`;
- that object is frozen only at the dataclass API level;
- a hostile caller can use `object.__setattr__` to transplant valid custody from one exact resolver into another after construction;
- the authenticated entrypoint then consumes transplanted custody that the victim constructor never admitted.

This is a local custody/provenance defect. No new relation semantics or authority kind is required.

## Mission

Make the accepted source-relation owner state **constructor-bound and non-transplantable through caller-accessible live state**, while preserving the existing exact P07 owner semantics.

The repaired path must establish:

`constructor-admitted relation + registry custody`
→ sealed/authenticated owner state
→ exact relation validation
→ exact authority snapshot validation
→ exact RelationDecision
→ F7 positive authority closure

A caller may inspect diagnostics only if inspection cannot mutate or replace the state used by authenticated adjudication.

## Required design properties

### 1. No live authenticated state exposure

No module-visible/publicly callable helper may return the exact mutable-in-memory object that the authenticated adjudication path later trusts.

If inspection/debug access remains necessary, return:
- detached immutable material;
- canonical serialized material;
- or a fresh copy whose mutation cannot alter owner custody.

Do not treat underscore naming or `frozen=True` as security/provenance.

### 2. Constructor custody remains private to the owner path

The load path used by authenticated adjudication must retrieve state from a store not replaceable through ordinary caller-held resolver fields or a module-visible live-state accessor.

A closure/lexical store, immutable serialized custody capsule, or equivalent is acceptable if:
- the court proves the caller cannot transplant source custody into victim custody through supported/reflection surfaces already in the hostile model;
- the owner revalidates exact semantic hashes/replay identity at positive use.

### 3. Exact registry provenance remains pinned

Preserve HQ227’s closure of nested registry provenance:
- exact concrete `AuthorityRegistry`;
- constructor-admitted snapshots;
- exact snapshot semantic/hash validation;
- later resolver `_registry` replacement has no effect;
- registry subclasses/overrides cannot redirect owner adjudication.

### 4. No duplicated semantic owner

Do not reimplement P07 relation semantics in F7.

F7 must continue to consume the adopted source-relation owner’s exact authenticated decision.

## Mandatory hostile court

Build a discriminating same-fixture court covering at minimum:

1. **Exact source→victim custody transplant**
   - source resolver contains genuine positive authorized relation;
   - victim resolver was constructed with no such relation;
   - attempt the HQ228 attack using every remaining callable owner-state inspection path;
   - victim must remain nonpositive.

2. **`object.__setattr__` on any returned diagnostic state**
   - mutation must not affect authenticated owner state.

3. **Replacement of resolver-visible `_by_ref`, `_by_key`, `_registry`**
   - must not redirect authenticated owner result.

4. **AuthorityRegistry subclass override**
   - must not redirect exact snapshot resolution.

5. **Injected relation object never admitted by victim constructor**
   - must not become available through authenticated decision.

6. **Stale/corrupt relation semantic hash or replay identity**
   - must fail.

7. **Wrong snapshot body under same outer AuthorityRef shape**
   - must fail.

8. **Monkeypatch module-visible `decide`, `require`, `resolve_exact`, validation helpers**
   - prove the load-bearing authenticated seam remains the intended owner path under the accepted hostile model.

9. **Positive concrete service**
   - legitimate constructor-admitted cross-universe positive relation remains authorized.

### Fail-capability

Include a targeted break that restores the pre-repair live-state exposure or substitutes the authenticated custody loader with a transplantable state path. The same court must fail for the intended reason.

Do not use another stale/non-load-bearing patch.

## Runtime requirement

If a lawful governed runtime surface is available, execute:

- exact F7 court;
- directly relevant source-relation court;
- M1 regression court previously used for F7 qualification.

Record:
- interpreter/environment;
- exact commands;
- pass/fail/skip/error counts;
- hostile transplant witness execution.

If runtime is unavailable, report that honestly; source-level completion may still return for hostile review but may not self-adopt.

## Sustained F7 law

Preserve all previously closed requirements:

- RelationDecision authority cross-binding;
- exact compared-source TEMPORAL_EVIDENCE identity scope;
- explicit unrestricted tokens only;
- 12 relation states;
- 19 authority kinds;
- exact-zero/no tolerance;
- total precedence;
- 3+ anchor refusal;
- exact measure/use binding;
- same-universe / zero / increase / decrease / lawful cross-universe positive paths;
- no F8/ranking/selection/interpolation/trajectory/causation/currentness/pooling/equivalence-creation/actor authority.

## Write terrain

Permitted production:
- `rawlsing_next/pre553_source_relations.py`
- `rawlsing_next/pre553_temporal_comparability.py` only if a narrow call-site adjustment is required.

Permitted courts:
- `rawlsing_next/tests/test_pre553_temporal_comparability.py`
- directly relevant source-relation court if required.

No other production mutation.

## Required return

Write only:

`WORKER_RETURNS/PYAT-HQ231-F7-SEALED-OWNER-STATE-CUSTODY-R1/`

Required:
- `00_RETURN.md`
- `01_SEALED_CUSTODY_DESIGN.json`
- `02_LIVE_STATE_EXPOSURE_AND_TRANSPLANT_ATTACK.json`
- `03_REGISTRY_PROVENANCE_AND_OWNER_PATH.json`
- `04_RUNTIME_PRODUCTIVE_PATH_AND_REGRESSION.json`
- `05_FINAL_DISPOSITION.json`

Allowed:
- `F7_SEALED_OWNER_STATE_CUSTODY_COMPLETE__READY_FOR_FINAL_REREVIEW`
- `F7_SEALED_OWNER_STATE_CUSTODY_PARTIAL__NAMED_DEFECT`
- `F7_SEALED_OWNER_STATE_CUSTODY_REQUIRES_OWNER_CONTRACT_CHANGE`
- `F7_SEALED_OWNER_STATE_CUSTODY_REVEALS_ARCHITECTURE_CONFLICT`

Commit/push only this branch and report exact remote SHA.
