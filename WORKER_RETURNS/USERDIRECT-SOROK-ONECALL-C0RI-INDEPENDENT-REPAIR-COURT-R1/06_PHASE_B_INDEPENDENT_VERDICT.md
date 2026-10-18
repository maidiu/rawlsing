# SOROK ONECALL-C0RI — independent post-author Phase B scientific court

**Terminal disposition: `C0RI_REVISE_HOLD__HISTORICAL_C0F_REPAIR_POSITIVE_AT_TRUSTED_SOURCEFREE_GRAIN__FOUR_NEW_CUSTODY_AND_DIRECT_APPEND_REDS__NO_NATIVE_ACCEPTANCE`.**

## Independent/sealed provenance
Assigned sealed C0RI startup `b48837d84d01077091386dfa14c1eedae9955ad5`; original preregistration frozen **before** C0R implementation inspection at `76be43f3cd65999c93371f28d41571d04a7399fb`, then the separate stronger blind addendum at `5f6ab4821c63d1f7de98ad615bc3990b0272fba4`. Exact final C0R author: `98fdbdf0794da76485b40b155fa4396370a04025`, verified remote branch and return-only scope 16 paths, 0 behind.

Source: repaired C0R `onecall_c0.py` exact Git blob SHA-1 `76bd3a6ea26fd72ef59816d62013fd694bf8e774`, SHA-256 `298ff2bdbf4f916049ae21167e238767d2da682f369820a29c7d5ffa1a5461f9`, **29,383 bytes**. Actual imported byte-identical source independently reconstructed in an isolated real Python 3.13.5 / pytest 9.0.2 filesystem; original C0 retained separately, Git blob `f45e4f5573495f060503f92b7630ec83531ced4d`, SHA-256 `3f0da92095f8355c7512d49ac546c846b6026d3775533ba56be7e148e11abfa1`, **18,378 bytes**. No original test expected value, C0 or C0R source edited.

## Actual test results: separate, unmodified and honest
| Physical court | PASS | RED | Precise failure |
|---|---:|---:|---|
| Original C0 + unchanged author32 | 32 | 0 | Historical sourcefree author positive |
| Original C0 + untouched C0F 44 | 26 | 18 | Historical 18 red independently reproduced |
| Original C0 + blind H01-H18 | 6 | 12 | Historical original-counterexample set |
| Original C0 + stronger blind S01-S04 | 1 | 3 | S01/S02/S04 RED |
| Repaired C0R + unchanged author32 | 31 | 1 | Original R08, source-incompatible semantic expectation |
| Repaired C0R + untouched C0F 44 | **43** | **1** | Original-source SHA pin R42 only (ORIGINAL_ONLY) |
| Repaired C0R + frozen blind H01-H18 | **17** | **1** | Original-source SHA pin H18 only (ORIGINAL_ONLY) |
| Repaired C0R + stronger blind S01-S04 | **4** | **0** | All original target repairs positively tested |
| Repaired C0R + newly independent postfreeze I01-I14 | **10** | **4** | New I08/I10/I13/I14 RED |

All tests executed with genuine Python and produced **real JUnit XML, stdout, and complete failure traces**, delivered in independently verified downloadable archive. Original frozen expectations were neither rewritten, xfailed, skipped nor generated into an algorithm. The original C0R author's **54/54 PASS** is separately verified as *authored JUnit publication* (`repair_junit.xml`, Git blob `cd71254493c2d710e64dfd94b8ba16ab26c2babd`) and **was not independently rerun in this court**.

The old author's R08 expects a cosmetic relevance-label change to change the canonical event hash, which would violate independent R35; preserve R08 historical RED. Original R42/H18 correctly demand original C0 source preimages and cannot pass on different repaired source; new I01 physically verifies exact repaired module SHA-256 and Git SHA-1 instead.

## Four freshly found independent REDs

**I08 — forged historical receipt silently imported:** Input `run(initial=state)` with an existing `observed:2020:practice` record bearing `source_ref=FORGED_SOURCE`, `hash=FORGED_EVENT_DIGEST` and `prior_state_hash=FORGED_PRESTATE`. C0R accepted this forged prior event and continued with its own mock activity. Its initial-state checks validate top-level synthetic source label and integer event clocks but not historic event owner, source or hash preimage. **Actual RED under untrusted imported prestate; trusted internally constructed state positive remains.**

**I10 — late material substitution with unchanged source-reference string:** After packet validation but immediately before append, injected `world.material_version += 500` through a controlled Python monkeypatch without changing the literal `SYNTHETIC_WORLD@1` source ref. C0R rechecks only that symbolic ref and admits `observed:2020:practice` with the changed material snapshot. **Actual source-content/epoch custody RED in injected mutable-state interleaving; no claim that real multithreaded native execution was performed.** Author M01's changed-ref refusal remains a genuine narrower positive.

**I13 — exported direct append accepts invalid time:** Independent direct call to `apply_admitted(state,candidate(2021,day=366,...),year=2020,mock_rules)` appended `observed:2020:future`; the called API did not recheck candidate.year/day, though the normal `run→validate_packet→apply_admitted` flow would refuse. **Lower-level API authorization RED; not a demonstrated normal scheduler bypass.**

**I14 — exported direct append accepts unvalidated proposal field:** Direct `apply_admitted` on otherwise permitted neutral candidate containing `CAN011_UPDATE` committed objective occurrence because the lower-level function checks selected owner fields but not full packet schema. **No psychological effect was applied**, but the unissued field was not refused at this externally callable boundary. Again distinguish this from the properly validated normal run path.

**I09 qualification:** The 14-case suite reports a generic denial on an initial ledger with duplicated existing IDs, but the denial happens later in render's duplicated historical-fact list; that is **not independent proof of an authenticated initial-ledger or cold-prestate validator**.

## Independently confirmed positives and ceilings

C0R's trusted-sourcefree normal orchestration reproduces sourcefree event ordering, literal reference-substitution denial, default-deny `rules={}`, optimized-Python `-O` issuer refusal, named other-person refusal, separate narrative/proposal output, noncausal-label hash invariance, parent accepted/refused implications, explicit unsupported 90-day failure (NOT an implemented 90-day scheduler), lawful no-event intervals, and identical 3/4/0 mock-count one/two/fixed mode causal receipts. Two **fresh independent OS interpreters** at PYTHONHASHSEED 17 and 791 yielded the identical original author's **18,384-byte** complete output, SHA-256 `1949122dd8761e9c742477b502f6a73b82dd98670408361b5002473b5581dbdf`. No real LLM API was invoked; mock count is not cost/quality.

The historical 18 C0F sourcefree failures are repaired at the actual tested ordinary boundary, with only legitimate source/version and frozen semantic R08 incompatibilities retained. Nevertheless general sourcefree *untrusted prestate/append custody* cannot receive C0RI I2 ACCEPT while I08/I10/I13/I14 remain RED. The existing test-only closed-fixture demonstration receives an independent **mechanical positive**, not production, source, native CAN/ADP or actor grant.

**Required independent recommendation:** bounded REVISE/HOLD. Either explicitly make direct append unreachable beyond one authenticated owner and prove trusted-prestate admission preconditions, or implement immutable prior-ledger preimages/content-epoch custody and recheck full time/schema/owner at final append. Then rerun unchanged C0F and C0RI suites, including I01-I14, independently. Native B3/CAN008/CAN011/ADP016/017, actor/world issuance, original source science, deployed V3, real provider comparisons and original F1 **17 REDs** remain separate and unissued. No reviewer self-adoption or branch mutation outside own return.
