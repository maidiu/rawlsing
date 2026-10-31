# Integration plan — bounded sourcefree PE/V2K recovery

**No production merge.** This plan is a sourcefree candidate and test handoff, not a PRE-MAIN integration or source/science grant.

## 1. PE reversed-issuer repair

**Candidate:** `candidate/pre553_postastra_pe_generic_world_possibility.py` (blob `31de8f21e7b7fee17a155880b6204d8a191c83df`) derived from original `58484f4c...` at `e61a26ce...`.

**Exact change:**
- Keep `_auth` as shape normalization only.
- Add `_reversal_authority_competent(authority_registry, ref, target_ref, denominator_basis_ref)`.
- For `ROLE_REVERSE`, require the exact `TARGET_USE_PERMISSION` snapshot in the issuer registry, positively scoped to `REVERSE_TARGET_VALUE_TO_SUBJECT`, target use and denominator/risk set.
- Refuse forged, unregistered or wrong-scope reversal authority with the existing typed refusal; never accept a mere non-null caller `AuthorityRef`.

**Sourcefree test environment:**
- The original PE fixture creates a synthetic reversal `AuthorityRef` but does not register an `AuthoritySnapshot`; the repaired candidate therefore requires the exact reversal snapshot to be added to the sourcefree test registry. The candidate test fixture adds a `TARGET_USE_PERMISSION` snapshot with exact content hash matching `make_role_reversal_authority`; the exact patch is `candidate/PE_TEST_FIXTURE_AUTHORITY.patch`.
- No production source, actor or world permission is involved.

**Tests:**
- 21 author tests: **21 passed**.
- 13 independent strict tests: repaired candidate **5 passed / 8 failed** (only failed assertions preserved). The original exact-blob pin was changed to the repaired candidate blob only for the repaired-receiver test copy; no assertion was changed.
- Candidate-specific reversed-issuer tests: **2 passed**.
- Remaining 8 failures: strict SC0 value-bearing/schema fields not implemented by the whole PE contract. Do not call the whole PE contract READY.

**Current first consumer:** no PRE-MAIN consumer. The only consumers are branch-local author/independent tests. Do not merge PE.

**Owner/reviewer:** original PE/SC0 owner must decide whether to implement the missing SC0 fields; a distinct I3 reviewer must rerun the same 13 assertions and the repaired-issuer negative on the exact repaired SHA.

## 2. V2K exact dependency restoration

**Original:** `694fb450...`; source `e3ef9a24...`.

**Decision:** current `pre553_issued_workload.py` (`31e84f49...` at current PRE-MAIN `5fc1d43e...`) is a **different API**, not a compatible V2K successor. Do not manufacture a new contract and do not transplant the old module into current source.

**Isolated restoration blobs:**
- `pre553_original_workload_contract_v2_candidate.py` `08bb75c4...`
- `pre553_original_workload_binder_candidate.py` `7d8b3902...`
- `pre553_v2_durable_consumer_integration_candidate.py` `dc146e92...`
- `pre553_original_workload_v2_verifier_candidate.py` `996c8e90...`
- `pre553_batch_durable_checkpoint_candidate.py` `719c8d87...`
- dependency test helpers `0b9f1add...` and `3218f280...`
- `PV_RETURN` oracle directory from `694fb450`.

**Tests:**
- Four V2K suites: **63 passed** (including the 24-test candidate suite).
- Exact dependency/owner suites: **50 passed / 1 source-cut check failed**; the failure is `test_no_accepted_owner_modifications` comparing the current tree to historical `0f8c6d08...`, not a V2K semantic failure.
- Without dependency: **collection error**, not green.
- 111-test owner aggregate: not available as one exact suite at this cut; do not claim 111/111.

**Current first consumer:** none for V2K. Current issued-workload consumers are a distinct native workload API. No transplant.

**Owner/reviewer:** original U/E/source and V2K owner must decide whether to provide a compatible current ABI adapter or preserve V2K as historical evidence only. Independent I3 reviewer must verify dependency severance and foreign-issuer/held-row rejection.

## 3. Negative dependency-severance

`tests/test_v2k_dependency_severance.py` proves:
- current `pre553_issued_workload.py` lacks V2K symbols;
- blocking `pre553_original_workload_contract_v2_candidate` makes V2K import fail closed.

Result: **2 passed** with current-ABI + V2K source tree.

## 4. Integration order (if an owner later authorizes)

1. PE owner decides `_auth` repair acceptance and whether to implement the 8 SC0 fields.
2. PE owner + independent reviewer rerun 21 author and 13 strict tests on exact repaired SHA.
3. V2K owner decides exact historical dependency vs current ABI adapter; do not transplant without semantics/ABI reconciliation.
4. V2K owner + independent reviewer rerun exact available suites and negative severance.
5. Only then consider a sourcefree integration candidate; no PRE-MAIN merge or native/science/actor permission follows automatically.

## 5. Blockers

- PE whole contract: 8 SC0 strict gaps remain; no current consumer.
- V2K: no current compatible ABI or consumer; 111 aggregate not available; foreign-issuer/held-row unadopted.
- No source/native/science/world/actor permission.
- No independent I3 review yet.
