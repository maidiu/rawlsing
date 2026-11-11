# SAVED_ACCESS_CONTRACT_R1 — commands and evidence

**Review worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-engineering-review-r1`
**Branch/head (unchanged):** `review/pyat-w03-w04-api-binding-recheck-r1` / `475035790098d11751012308b7fd62576987502d`
**Source implementation read:** `16f97fe23e395d6807a13a4fa5ea0c2b96bccd69` in `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-completion-r1`
**Production equivalence:** `f329b8c041af1f70291535a27cfde13af1b59642`

## 1. Source and AGENTS reads

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-completion-r1 rev-parse 16f97fe23e395d6807a13a4fa5ea0c2b96bccd69
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-engineering-review-r1 rev-parse HEAD
cat /Users/matthewsmith/Desktop/Rawlsing/AGENTS.md
```

Result:

```text
16f97fe23e395d6807a13a4fa5ea0c2b96bccd69
475035790098d11751012308b7fd62576987502d
AGENTS.md read (7 lines; SHA-256 118e95eb20949dc4e9b0c94578be5a6315fefb1b65baaabf05f3f3a56a0c9931)
```

The cited files were read with `git show 16f97fe:<path>` only; no checkout/reset/rebase of this worktree and no production edit. `git diff 16f97fe f329b8c04 -- <all cited files>` is empty, so the reviewed implementation is production-equivalent at the cited scope.

## 2. Exact source files read and SHA-256

```text
6cbb07a755fa910154ebbe7e97435f46a4a9fabe29eac468d816ddc10d2a3d51  rawlsing_next/pre553_parquet_carrier.py
77ec0997b8aab0bb00c7d0ca93997fb3f3a041ace1c6661c1efb1185c9affad2  rawlsing_next/pre553_c11_repository.py
6299bf18eb185b11df2bc82c10f7a8140784f55dcfedbab5016e549eb8d7aeea  rawlsing_next/_pre553_c11_execution_view.py
bb0093fa0ad8f19e324f2ecd01cc1faad4e690f2152f6cb7316ee91b5a033e93  rawlsing_next/_pre553_w03_cold_compact.py
59beb313602eb6fffdd4960576090e78bee1ce769f23f885580ea6da635fbcfb  rawlsing_next/_pre553_query_predicate.py
969fb4c38eb86bb7a9be72c9af98e410c7130d74d4816618c9062e6e7c0b4913  rawlsing_next/_pre553_query_common.py
23b7d5cbcca4fe07a3334d133020c2850e14ab9ad0ab4c159df4a2e48dbef33f  rawlsing_next/pre553_carrier_execution.py
5071bde0180db05f59386884d5de2bdea503cd26db2024806a92887d2a5a1e04  rawlsing_next/pre553_batch_runner.py
7cd7fd4f8ccf79cb07b037ef9cdda5e60ed3c3ba0631c9f4030d09f4d666be94  rawlsing_next/pre553_empirical_query.py
ec9558c68a2138de7d44796986db39df28a679ccc1506785b79929d624d32034  rawlsing_next/field_forge_conditional_support.py
e3a3d9b9b1c4836c519b6714b0e14013cbf32e9c65ddacd457745f21c1bb1c1e  rawlsing_next/pre553_source_backed_c11_facade.py
3963facef5c8ae2981991ffa8c5c5c9b717fb4e09f342eec277198fc5cf38a33  rawlsing_next/pre553_c11_integrity.py
9cd1d71440a7e8c1861dda73274529e07211edc14335583e93ad91c0833e9ab4  rawlsing_next/pre553_empirical_objects.py
```

Evidence tests read at the same cut (not re-executed; no heavy S2/100k):

```text
b155afeeb839a99e8542532c380587629c490f1b5272e4fa053054c8021e22fe  rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py
675ad4d5e014e81ab3db19ab45b30d62adfc4e2b4c356630cdb8883ebe88aeaa  rawlsing_next/tests/test_pre553_w03_w04_cold.py
f62cbd2263487ee2a8c8c395434d84b100b0c0cbc7548458282ddafa32a1fa07  rawlsing_next/tests/test_pre553_w03_w04_completion.py
```

## 3. Exact API/owner evidence and line references

- Carrier: `pre553_parquet_carrier.py` `_relation_objects:221-235`, `_write_tables:237-258`, `persist:260-295`, `_read_rows:297-300`, `reopen:301-376`, `_logical_digest:117-120`, `_object_from_row:140-158`, `verify_semantic_release_root:160-196`.
- Repository: `pre553_c11_repository.py` `C11LogicalRelease:26-67`, `_public_non_events:60-65`, `C11Repository:71-140`, `resolve_object_exact:107-113`, `_commit_validated:115-139`, `_make_validated_release:142-143`.
- Compact lane: `_pre553_c11_execution_view.py` `_EventRead:48-81`, `_CompressedBodies:85-112`, `_EventLane:114-131`, `_RespondentEvents:145-173`, `_CompactPublicObjects:175-206`, `_read_bodies:228-330`, `_write_bodies:367-389`, `_compact_public_objects:451-556`.
- Streaming builder: `_pre553_w03_cold_compact.py` `ColdCompactBuilder:38-147`, `finish:122-147`, `attach_governed_cache:215-256`.
- Query index: `_pre553_query_predicate.py` `_select_respondent_events:18-61`, `_build_release_index:63-128`; `_pre553_query_common.py` `_ReleaseIndex:159-172`, `_semantic_value:249-255`.
- Executor/Batch: `pre553_carrier_execution.py` `CarrierNeutralResearchExecutor:403-479`; `pre553_batch_runner.py` `BatchExecutionRunner:385-430,536-624`; `pre553_empirical_query.py` `execute_empirical_query:685+`.
- FieldForge: `field_forge_conditional_support.py` `_validate_common_closure:194-273`, `produce_exact_conditional_support_profile:467-580`.
- Construction/identity: `pre553_source_backed_c11_facade.py` `build_cold_source_backed_c11_release:896-1100`, `build_source_backed_c11_repository:1265-1300`; `pre553_c11_integrity.py` `ReplayManifest:305-330`, `make_m01_m18_coverage:510-560`; `pre553_empirical_objects.py` `canonical_json:215-220`, `RespondentEvent:516-535`.

Existing tests cited as contract evidence:

- `test_pre553_c11_cold_reopen_i03.py:22-130` — cold/full reopen, actual I03/I05 material equality, fresh process, corruption refusal.
- `test_pre553_w03_w04_cold.py:90-195` — eager/cold release identity, compact lane exactness, selector sequence/yield equality, ordered/repeated cases.
- `test_pre553_w03_w04_completion.py:328-345` — canonical Parquet survives accelerator deletion; exact consumer result.

## 4. Evidence versus inference

**Source evidence:** the exact carrier/repository/compact-lane/query/executor/FieldForge APIs and line references above; the existing tests show the compact lane and repository/executor are already integrated and exact at the tested scope; the current carrier persist/reopen full-materialization path is visible in source.

**Inference:** the expected memory/fresh-process benefit of a compact sidecar and the exact bounded-batch saving behavior; no heavy benchmark, 100k run, storage bakeoff, or new runtime matrix was performed. The next grant’s acceptance checks are exact-output/structural (I03/I05 canonical material equality, no event-row decode, hash/closure checks), not a performance claim.

**Not claimed:** whole MCR/12-ID/final code/economic receiving; original35/source/native/science/actor authority; universal35 support; production merge; a new query/authority engine; replacing the existing analytical engine; trusting the disposable accelerator cache.

## 5. Output hashes

```text
96bb4bd771acaf29bef0838fdea82b610853343423fc183f2e00df94b78b3860  00_DECISION.md
ef4d1d2cd72ebfb8565eafaacc2e69c62b62a32dfe9ae3e002870b026da7523d  01_API_REPRESENTATION_CONTRACT_AND_GRANT.md
```

## 6. Boundary

Writes are confined to this `SAVED_ACCESS_CONTRACT_R1/` lease. No source/runtime/existing-test/HQ/peer/protected edit, no original respondent/SAV/DTA/DB/source-byte read, no native/science/actor effect, no install/merge/new worker/model/provider/account/region/effort change. The separate repaired pilot worktree was not touched, run, or polled. This is a source-grounded engineering decision enabling a bounded carrier code grant, not whole-MCR acceptance.

**Decision:** `IMPLEMENT_WITH_EXISTING_CONTRACT`; the missing work is the carrier-side canonical compact sidecar plus `reopen_compact`, using the existing compact representation and unchanged repository/executor/query/Batch/FieldForge owners. No consequential semantic contract change or user decision is required for this seam.
