# GT12 Closure A3 — real GT2 I03 execution + deterministic replay R1

## Terminal

`PASS__REAL_GT2_SUPPORTED_19210__DETERMINISTIC_REPLAY`

## Identity and scope

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-gt12-closure-a3-real-gt2-r1`
- exact starting SHA: `2753d1abbcb702e9260f4ab60c528748fb28c7d2`
- terminal SHA: branch tip containing this receipt; exact SHA returned to HQ after commit
- Closure-A program: `a473091473f5729dd9aa6e54d68b88de49f9d608`
- frozen canary contract: `a9416094cbb4653dd2de2e4aa7b67577a355560c`
- A2 consumed: **NO**
- Closure B/C/D consumed: **NO**
- GT1 executed: **NO**

A3 owns only:

`A1 exact governed C11 -> GT2 Q86B x Q86A current-I03 execution -> deterministic replay -> execution receipt`.

## Exact A1 C11 reproof

The recreated governed FFP014/FFP017 carriers were loaded from the persistent Library handoff. No raw `.sav` bytes were present or acquired.

Before I03, A3 rehydrated the exact A1 claim-scoped execution view and independently reproduced:

- release: `C11LogicalRelease / R5_GT12_Q86A_Q86B_FROZEN / 8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`
- replay manifest: `c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa`
- source release manifest hash: `c1fd224e92c22875ef0390b2d26f17118aff73a7d9938397e70b6eb82fb15870`
- public objects: **96,057**
- internal records: **19,212**
- source rows retained as provenance: **51,587**
- exact claim members: **19,210**

Exact empirical universe:

`EmpiricalUniverse@1.0.0 / urn:rawlsing:pre553:EmpiricalUniverse:sha256:4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1 / 4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1`

## Exact A3 authority binding

The inherited A1 target-use material did not itself bind the derived empirical-universe ref required by current GT12-B law. A3 therefore constructed only the bounded claim-specific authority required after the exact universe was known.

PREDICATE_GRAMMAR:

`GT12-A3-GT2-I03-QUERY@1.0.0 / c0ec18e231c8b934acc1fd072b8cd26d59ee2d784c9fb5b29b345b944a757a16`

TARGET_USE_PERMISSION:

`GT12-A3-GT2-TARGET-USE@1.0.0 / 8be1db868deb8b1d613495a2120d2092df2fe55aa5f8884830d7a7e85e221a0e`

The permission remains exactly bounded to the frozen GT2 operation/use and actual empirical universe. No sibling-local general permission was created.

## Genuine current-I03 GT2 execution

Claim:

`GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1`

Exact order:

`Q86B -> Q86A`

- CONDITIONER = `Q86B`
- TARGET = `Q86A`
- state = `SUPPORTED`
- denominator = **19,210**
- raw resolved target support = **19,210**
- measure = `RAW`
- weights = `NOT_APPLICABLE`
- full source-native joint domain = **36 cells**
- typed administrative states preserved: `DK`, `NOT_ASKED`, `REFUSAL`, `MISSING`

Query:

`EmpiricalQuerySpec@1.0.0 / urn:rawlsing:pre553:EmpiricalQuerySpec:sha256:e91970c161736113201a3e9880034f8d088099aad67300a5aa689b7a08200670 / e91970c161736113201a3e9880034f8d088099aad67300a5aa689b7a08200670`

Fact:

`EmpiricalFact@1.0.0 / urn:rawlsing:pre553:EmpiricalFact:sha256:7bdb8752df31905a737d1a21c2ada61fe0c64d9cb4db17ea9bb748a1cf25b27f / 7bdb8752df31905a737d1a21c2ada61fe0c64d9cb4db17ea9bb748a1cf25b27f`

I03 replay:

`PRE553_I03_QUERY_REPLAY / urn:rawlsing:pre553:i03-query-replay:sha256:10c4c50af557fe92866c6033a424ba2ab56847400bf9f970e6666612f435cae0 / 10c4c50af557fe92866c6033a424ba2ab56847400bf9f970e6666612f435cae0`

### Observed nonzero joint cells

| Q86B | Q86A | count |
|---:|---:|---:|
| -1 | -1 | 6 |
| -1 | 1 | 9 |
| 0 | -1 | 1 |
| 0 | 0 | 2,112 |
| 0 | 1 | 4,493 |
| 0 | 9 | 178 |
| 1 | -1 | 1 |
| 1 | 0 | 491 |
| 1 | 1 | 11,232 |
| 1 | 9 | 63 |
| 9 | 0 | 40 |
| 9 | 1 | 250 |
| 9 | 9 | 334 |

The complete 36-cell payload, including all zero cells for source-native administrative states, is banked in `01_EXECUTION_RECEIPT.json`.

## Deterministic replay

Current authoritative `replay_empirical_query(...)` reproduced the original result exactly.

Exact equality closed for:

- query ref/hash
- empirical-universe ref/hash
- source/risk-set/release refs/hashes
- authority refs/hashes
- denominator
- full joint cell payload
- final EmpiricalFact ref/hash
- entire QueryExecutionResult

No equivalent-enough comparison was used.

## Scale repair

The real 19,210 execution verified the Closure-A lead in current `_pre553_query_predicate.py`: `DERIVED_BRANCH_COHORT` rebuilt/canonicalized the exact 19,210-member cohort for each respondent.

A3 changes only that hot path to cache the immutable exact member-ref set. The cache is nonsemantic, keeps the exact membership ref in its identity, does not mutate predicate bytes, and preserves all authority/ref/hash checks.

No routing, source, domain, permission, replay, or negative-state law was weakened.

## Timings

- governed carrier load/proof: **4.523257721 s**
- exact A1 release rehydration + release/replay hash reproof: **17.608385257 s**
- current I03 GT2 execution: **8.162428164 s**
- current I03 deterministic replay: **7.727469821 s**
- 16-case hostile matrix: **9.855508163 s**
- total accepted run: **48.388194526 s**

## Required hostiles

All 16 required classes passed:

- `01_Q86A_Q86B_ROLE_REVERSAL`: PASS
- `02_SEMANTIC_COMPONENT_ORDER_REVERSAL`: PASS
- `03_INDEPENDENT_MARGINALS_NOT_JOINT`: PASS
- `04_MEMBERSHIP_DRIFT`: PASS
- `05_DENOMINATOR_DRIFT`: PASS
- `06_TRUNCATED_RESPONSE_DOMAIN`: PASS
- `07_ADMIN_TYPED_STATE_LOSS`: PASS
- `08_WRONG_EMPIRICAL_UNIVERSE_AUTHORITY`: PASS
- `09_WRONG_SOURCE_SHA_REF`: PASS
- `10_WRONG_C11_RELEASE_REF_HASH`: PASS
- `11_WRONG_RISK_REF_HASH_MEMBERSET`: PASS
- `12_QUERY_REF_HASH_TAMPER`: PASS
- `13_AUTHORITY_REF_VERSION_HASH_TAMPER`: PASS
- `14_REPLAY_MISMATCH`: PASS
- `15_PERMISSION_WIDENING`: PASS
- `16_FF_PREV3_ACTOR_V3_PROMOTION_ATTEMPT`: PASS

The matrix includes exact role/order preservation, no marginal substitution, membership/denominator/domain/admin-state integrity, universe/source/release/risk/query/authority tamper rejection, replay mismatch rejection, permission nonwidening, and no FIELD FORGE/PRE-V3/actor/V3 promotion.

## Files changed

- `rawlsing_next/_pre553_query_predicate.py`
- this return
- `01_EXECUTION_RECEIPT.json`

No governed carrier/source bytes were added to Git.

## Explicit non-consumption / non-promotion

- A2: not consumed
- Closure B/C/D: not consumed
- FIELD FORGE relation: not produced
- I04/PRE-V3/M1: not invoked
- V553/V555/V556: not fabricated
- positive V3 authority or actor transition: not created
- PRE-MAIN: not moved
- `main`: not moved
- source acquisition: none
- Actions/export scaffolding retained: none

## Terminal

`PASS__REAL_GT2_SUPPORTED_19210__DETERMINISTIC_REPLAY`
