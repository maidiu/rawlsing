# M5 FINAL — V3 STRUCTURAL PEER-PRIOR SEAM

**Assignment:** `E02-W07-M5-FINAL-001`  
**Permanent chat:** `CHAT-SV3M`  
**Agent:** `M5_FINAL`  
**Authority:** `DISPOSITIVE_M5_STRUCTURAL_PEER_PRIOR_SEAM_ONLY`  
**Repository:** `maidiu/rawlsing`  
**Semantic launch base:** `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`  
**Mission branch:** `agent/vozhd-trii-dr-r03-seam-m5-v3-peer-prior`  
**Production code modified:** `NO`  
**Broad topology amended:** `NO`

## 1. Disposition

`M5_ACCEPTED__V3_STRUCTURAL_PEER_PRIOR_SEAM_CLOSED`

M5 closes the exact M4 `ResolvedStructuralContext -> V3` structural-peer-prior validation and authority seam without changing M4/SCR5578 or SCRV3 semantics.

The binding theorem is:

```text
ResolvedStructuralContext != V3EmpiricalPossibilityInput != ActorCausalState
```

The two upstream peer priors remain independently typed, independently permissioned and independently current/refreshable. `ActorCausalState` remains V3-owned generated causal truth and is not a prior.

## 2. Exact authorities bound

M5 binds:

- M4 accepted final head `988fa8abe755eee636e52a6b6eb09072b5a0f111` and token `M4_ACCEPTED__SCR5578_EXACT_CONTRACT_CLOSED`;
- M4 `RESULT.json` blob `c83c9d83e5bd8050d81b483319fcdd2e65d5a2ce`;
- M4 `M5_RSC_HANDOFF.json` blob `d54efeb22b5514584df4bff8a7e42fc4adda81ef`;
- `SCR5578_PUBLICATION_REPOSITORY_RESOLUTION_EXACT_CONTRACT@1.0.0`, SHA-256 `7522e3066ec7cd03de36faf065e089925e42356b4a6833d7420d00f6a139f88c`;
- SCRV3 current local head `818bcd9dda100ea5d9b6f1417c5a99c64d4734c7`, token `SCRV3_WAITING_ONLY_FOR_EXACT_FINAL_SEAM`;
- SCRV3 `V3EmpiricalPossibilityInput@1.1.0`;
- `V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.1.0`, SHA-256 `e0cd3c8a4443c59b7e97cc151a7db9298310f7a7e766b593fb90968546d66939`;
- `SCRV3_READ_PERMISSION_MATRIX@2.0.0`, SHA-256 `6a4227bb3df913b8564ba0d994ce5c2be81bf0f6e8d8b5a164ba546db59fa2d1`;
- accepted non-dispositive SV3F head `4de8188fe3b31f8edc3f8e9924ebe8c651076558`, token `SV3F_FEEDER_COMPLETE`;
- parent 24/25, the accepted R03 broad DAG, and the whole-machine closure gate.

The mission branch was verified identical to `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d` before writing.

## 3. M4 structural peer is now exactly bound

The structural peer type is exactly:

`SCR5578_RESOLVED_STRUCTURAL_CONTEXT@1.0.0`.

At actual runtime consumption V3 must receive an **actual RSC instance** with exact `context_id`, `context_content_hash`, repository/query/policy, resolution receipt, resolved entries, preserved negatives, deferred/unresolved entries, all SelectionRecord refs/hashes, fidelity, refresh metadata and provenance.

M4 and M5 fabricate no runtime RSC instance.

The accompanying verification checksum is exactly:

`M4_TO_M5_RSC_MACHINE_SIGNATURE@1.0.0`.

It is nonsemantic. It does not replace RSC identity, producer identity, permission, or actor state. V3 recomputes it from the actual runtime RSC bindings and requires equality with the transported signature.

Missing or invalid runtime RSC fails closed with zero structural-peer effect.

## 4. Permission noncollapse

The structural permission invariant remains:

```text
resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses
```

`ACTIVE_CAUSAL` means only that a structural object is eligible to be offered for an active-causal-context use. It is **not** V3 mutation permission.

Repository presence, collection readiness, index/locator hits, dependency reachability and a valid M4 signature grant no V3 actor-state authority.

The empirical peer remains separately governed by SCRV3. Current SCRV3 has:

```text
positive PSEPF actor-transition rows = 0
```

The only positive PSEPF row is the noncausal intake/dereference row `SCRV3-RP-V3M002-V2 / EXACT_GEOMETRY_DEREFERENCE`; by itself it has zero actor-transition effect.

SV3M/SV3F candidate positive owner-read suggestions therefore do not survive as current positive authority. They were non-dispositive and were subsequently tightened by SCRV3.

## 5. Named transition declaration

Every named V3 transition owner must independently declare:

- whether structural peer input is `REQUIRED`, `OPTIONAL_BY_EXACT_OWNER_RULE`, or `NOT_USED`;
- whether empirical peer input is `REQUIRED`, `OPTIONAL_BY_EXACT_OWNER_RULE`, or `NOT_USED`;
- the exact structural operation/rule binding when structural context is consumed;
- the exact SCRV3 empirical read-permission row when empirical possibility is consumed;
- effective-time and causal-parent rules.

Availability/currentness is never branch authority. No generic peer merger exists.

M5 defines the interface records `V3PeerPriorRequirementDeclaration@1.0.0` and `V3PeerPriorConsumptionReceipt@1.0.0`; they carry seam validation/provenance only and create no new actor-state semantics.

## 6. Causal nonassignment

M5 rejects all of the following:

```text
ResolvedStructuralContext -> PSEPF synthesis
PSEPF -> generated structural position
RSC/EPI -> generic prior bag
RSC/EPI -> hidden scalar/persona vector
repository permission -> V3 mutation permission
source disagreement -> actor contradiction
prior -> memory
prior -> belief/knowledge
prior -> relationship
prior -> action/response
prior -> persona/voice
provenance -> source composition/pooling/respondent linkage/estimand authority
```

A prior may be consulted only under a named owner rule; consultation does not itself make the prior an occurrence, witness, actor fact, memory, belief or causal parent.

## 7. Currentness and historical receipts

Structural and empirical currentness are orthogonal.

Structural re-resolution is controlled by exact SCR5578 repository/query/policy/generated-binding and refresh authority. Empirical `V3_REBIND` versus `UPSTREAM_REQUERY` remains controlled by SCRV3 comparator/source/query/field and V3 intake authority.

A change may independently trigger one seam, both seams, or neither. Neither refresh implies the other.

Committed transition receipts retain the exact historical RSC identity/signature and exact historical EPI/read receipts. Later refresh/requery cannot replace those references or launder committed causal history.

## 8. Divergence and replay

Same exact priors do not determine the same life.

Two runs may share exact RSC and EPI at a branch point and lawfully diverge through different later causal events or separately recorded ADP-020 decisions.

Conversely, the same exact authority versions/hashes, causal history, peer-consumption receipts and RNG receipts must replay deterministically.

`persona = f(RSC,EPI)` remains forbidden even if deterministic.

## 9. Conflicts

No blocking authority conflict remains.

The only material apparent tension was the older non-dispositive SV3M/SV3F positive-read candidate language versus current SCRV3. Current SCRV3 is dispositive for its local V3 contract and has rescinded those provisional positive actor-transition rows. M5 therefore binds the current zero-positive-row state without reopening either parent.

See `M5_CONFLICTS.json`.

## 10. Contract

The exact M5 seam contract is:

`M5_V3_STRUCTURAL_PEER_PRIOR_SEAM@1.0.0`

Canonical contract-core SHA-256:

`54b9d262ec60ff8794f34d9caf68227275d272dc7d6b2254a9c84c996622d9f2`

M5 closes the **validation/authority interface**, not a runtime occurrence and not production implementation.

## Final token

`M5_ACCEPTED__V3_STRUCTURAL_PEER_PRIOR_SEAM_CLOSED`
