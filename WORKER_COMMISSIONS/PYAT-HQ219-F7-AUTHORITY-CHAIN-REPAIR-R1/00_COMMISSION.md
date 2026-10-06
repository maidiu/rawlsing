# PYAT HQ219 — F7 AUTHORITY-CHAIN FINAL REPAIR — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** Space Bunny authority-sensitive bounded implementation repair worker  
**MODEL / INTELLIGENCE:** **Space Bunny Max**  
**BRANCH:** `agent/rabochii-pyat-hq219-f7-authority-chain-repair-r1`  
**EXACT STARTUP TIP:** `136223506eaaf8d7c031a2822f2bfb6ac5bd420e`  
**PRIOR FINAL REREVIEW:** `agent/reviewer-pyat-hq218-f7-final-rereview-r1 @ 1c8b8ce186682d212ceec460b7b707421b6f0d27`  
**PRIOR DISPOSITION:** `F7_FINAL_BOUNDED_REPAIR_PARTIAL__NAMED_DEFECT`  
**ACCEPTED CONTRACT:** `c57a96897788108db7b194e4e51691d1ca8ab729`  
**CHECKOUT:** SPARSE_REQUIRED  
**SELF-ADOPTION:** FORBIDDEN

Read:
- `PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`
- HQD-216 from exact control object:
  `e0e7ce0e596e4e5ea7ec96c265ec949b9fe801a2:PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md`

The candidate lineage predates HQD-216. Read the exact Git object if the file is absent locally.

## Mission

Close exactly the three blocking authority-chain defects found by HQ218. Do not reopen F7 architecture and do not add authority kinds, relation states, reason-code families, source ontology, or actor semantics.

HQ218 sustained the rest of the HQ217 repair.

## Blocking repair A — F7-RR-02B: missing use-scope coverage

Current defect:

`require_use_scope=True` can still accept a positive authority snapshot when its scope omits `target_use_refs`.

Required behavior:

1. A use-scoped authority MUST have explicit governed-use coverage for the exact complete target-use ExactRef(s) required by the operation.
2. Absence of `target_use_refs` on a scope that is required to be use-scoped MUST fail closed.
3. Do not interpret omission as wildcard/unrestricted coverage unless an already-adopted authority contract contains an explicit unrestricted representation and this exact path lawfully recognizes it.
4. Complete ExactRef identity is required; object_id-only matching remains forbidden.
5. Apply this to every F7 authority path that declares use-scope required, including TEMPORAL_COMPARABILITY and TARGET_USE_PERMISSION.

Hostile witness:
- same positive authority material as a lawful case, but remove `target_use_refs`;
- it must no longer authorize the positive path.

## Blocking repair B — F7-RR-03: temporal identity must be owner-resolved

Current defect:

`temporal_identity_contract_ref` can be satisfied by caller-authored/hash-bound material rather than actual TEMPORAL_EVIDENCE-owned identity material.

Required behavior:

1. The temporal identity contract/ref MUST resolve through the existing TEMPORAL_EVIDENCE authority/owner path that owns identity material.
2. Caller-provided material may identify what is requested, but may not itself constitute authorization.
3. The positive path must consume the owner-resolved material and derive identity/joint-satisfaction from it.
4. A caller-minted self-consistent identity object/ref must not reach a positive comparable receipt.
5. Do not invent a new identity owner, registry, or authority kind.

Hostile witnesses:
- caller-minted identity material with correct-looking hashes/ref;
- stale/wrong identity material;
- owner-resolved lawful identity material.

## Blocking repair C — F7-RR-04: positive source-relation adjudication required

Current defect:

F7 calls `source_relation_resolver.resolve_exact` on an `Any` resolver and accepts the returned relation object without requiring the source-relation owner's positive adjudication. A stub, DENIED, wrong-kind, or wrong-pair relation can satisfy the object half while an independent positive SOURCE_EQUIVALENCE snapshot satisfies the authority half.

Required behavior:

1. Cross-universe F7 comparison MUST consume an actual positive source-relation owner decision from the existing adopted source-relation authority path.
2. Exact object lookup alone is insufficient.
3. Reject:
   - duck-typed/stub resolver returning arbitrary material;
   - owner decision DENIED/refused/not-admitted;
   - wrong relation kind;
   - wrong source/universe pair;
   - relation object not bound to the positive owner adjudication.
4. The positive cross-universe path must use the real adopted owner/factory/decision path, not a court-local stub that merely mimics method names.
5. Do not create equivalence authority. F7 consumes it only.

## Court authenticity repairs

Correct the per-file collection accounting. HQ218 reconstructs:
- F7 court: **96**
- M1 court: **27**
- aggregate: **123**

Do not report 98/25 unless the actual final committed collection changes and exact commands prove it.

Add discriminating/fail-capable witnesses for:
- missing `target_use_refs` under required use scope;
- caller-minted temporal identity;
- source relation resolved without positive owner adjudication;
- DENIED/wrong-kind/wrong-pair source relation;
- lawful owner-resolved identity;
- lawful positive source-equivalence owner decision.

Each new repair mechanism must have a targeted break proving the witness can fail for the intended reason.

## Productive adequacy — HQD-216

This lane MUST preserve the lawful positive F7 service.

Using competent lawful owner-backed fixtures, prove:
- same-universe comparable pair produces a positive comparable receipt;
- exact-zero produces the accepted no-change state;
- positive nonzero produces INCREASE when ordered inputs support it;
- negative nonzero produces DECREASE;
- cross-universe pair with genuine positive source-relation owner adjudication produces a positive receipt.

Do not solve the authority defects by closing all positive production.

A missing real estate input elsewhere is not a defect in this local F7 stage.

## Sustained invariants — do not reopen

Preserve:
- RR-01 exact comparability-requirement content binding;
- RR-02 complete ExactRef comparison where use scope is present;
- RR-05 measure binding and exact serialization;
- RR-06 accepted missing-order-basis typed terminal;
- RR-07 total precedence;
- resolution of every supplied target-use permission ref;
- exactly 12 relation states;
- exactly 19 authority kinds;
- exact-zero arithmetic with no tolerance/deadband/rounding;
- 3+ anchor refusal;
- prior-F7 mapping;
- negative receipt => NOT_COMPARABLE;
- live frozen backfill guard;
- no F8;
- no source selection/ranking;
- no interpolation/trajectory/causation;
- no currentness authority;
- no scalar pressure;
- no pooling;
- no equivalence creation;
- no actor/person power.

## Environment provenance

Do not repair or rewrite HQ214's historical 3.11.3/3.12.14 provenance conflict.

State this lane's own environment exactly once and truthfully.

## Write terrain

Production mutation is limited to:
- `rawlsing_next/pre553_temporal_comparability.py`

Court mutation is limited to:
- `rawlsing_next/tests/test_pre553_temporal_comparability.py`

Return artifacts only under:
- `WORKER_RETURNS/PYAT-HQ219-F7-AUTHORITY-CHAIN-REPAIR-R1/`

No raw source access, locator discovery, warrant issuance, live C4, C7, actor/person implementation, architecture reopen, merge, rebase, or self-adoption.

## Required return

- `00_RETURN.md`
- `01_USE_SCOPE_EXACT_COVERAGE_REPAIR.json`
- `02_TEMPORAL_IDENTITY_OWNER_RESOLUTION.json`
- `03_SOURCE_RELATION_POSITIVE_ADJUDICATION.json`
- `04_PRODUCTIVE_PATH_AND_DISCRIMINATING_COURTS.json`
- `05_FINAL_DISPOSITION.json`

Allowed dispositions:
- `F7_AUTHORITY_CHAIN_REPAIR_COMPLETE__READY_FOR_FINAL_REREVIEW`
- `F7_AUTHORITY_CHAIN_REPAIR_PARTIAL__NAMED_DEFECT`
- `F7_AUTHORITY_CHAIN_REPAIR_REVEALS_ARCHITECTURE_CONFLICT`

Commit only this lane's lawful changes, push only this branch, verify remote HEAD equals local, and report the exact pushed SHA.

Terminal:
`HQ219_F7_AUTHORITY_CHAIN_REPAIR_RETURNED__FINAL_REREVIEW_REQUIRED`
