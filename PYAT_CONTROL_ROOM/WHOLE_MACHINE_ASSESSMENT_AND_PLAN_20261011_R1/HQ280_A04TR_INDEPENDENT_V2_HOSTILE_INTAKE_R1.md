# PYAT HQ280 PV3 — A04TR independent V2 verifier hostile intake R1

**Status:** EXACT_REMOTE_RETURN_VERIFIED__TECHNICAL_NARROW_POSITIVE__ONE_SELF_DEFEATING_TEST__INDEPENDENT_CHAIN_HOSTILES_PARTIAL__EXTERNAL_CUSTODY_REAL_CONSUMER_SOURCE_ISSUER_HELD.
**Governing:** HQD-2026-10-10-280. Canonical `integration/pre-main-reconciliation-r1 @ a70a069fa948e0f3c041b389edcc732b6b948a4f` and semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` unchanged by this HQ documentary report.

## Exact GitHub custody

Independent review branch `agent/reviewer-pyat-hq280-pv3-a04tr-independent-v2-verifier-hostile-r1` at **`db85d2b0d14ab828faa5a7264d9611c6235ad7e4`**, one commit ahead and zero behind exact sealed start `be553023c985c3e7f7a407c97773363b5440482c`. Exactly **four added return files**: `00_RETURN.md`, `05_MANIFEST.json`, `repro/a04t_44_suite.log`, `repro/owner_untouched_diff.txt`; **zero files altered outside return directory**. Review's commission separately listed `01_`-`04_` individual reports; those were not delivered. Their substantive points are in 00 but evidence-artifact completeness is partial; do not silently pretend exact prescribed reports exist.

Inherited reviewed A04T candidate `c1df9842b7531146f1d8e215f216915b9039e4d7`, verifier code blob `996c8e907f2befde93af09b60154b610c1ffeb63`, candidate test blob `5799900d58b9949ab2784ea489f170f1be2f14bc`.

## Decisive actual test defect — independently source-checked by HQ

At `rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py:795-802`, `test_accepted_owners_a04_a04s_a05_untouched` runs `git diff --name-only b68de0dd35a9885efcb46bcd8ec9cbe41dabf500 -- rawlsing_next/` and asserts the result is empty. Because A04T added `rawlsing_next/pre553_original_workload_v2_verifier_candidate.py` and its new test file after that sealed base, the assertion inevitably sees its own permitted changes. A04TR's clean Git tree observed exactly those two paths; accepted owners remain unchanged, but **the candidate suite is 43 PASS / 1 FAIL**, not 44/44 on this committed tree. Fix by explicitly checking accepted owner blobs/allow-list rather than demanding zero `rawlsing_next/` changes; ensure test works on committed state and doesn't conflate descendant review worktree dirt or untracked files with accepted owner edits.

## Narrow scientific/engineering grade

- **Technical V2-native verifier architecture:** POSITIVE, independent review credits separately raw-authored V2 expected payload and independent full key preimage recomputation; legacy A05 keys intentionally not coerced; actual C11/Route B/I03/I05/Batch chain included in candidate's real suite.
- **Full independent hostile coverage:** PARTIAL. A04TR did NOT independently inject omit/extra/raw-weighted/condition/zero-denominator/false-null/job collision/self-certified expectation/fabricated consumer against actual chain; grade UNKNOWN for those independent attacks. Candidate's existing tests do not substitute for reviewer-owned hostiles.
- **Provenance:** `EXTERNAL_CUSTODIAN_ISSUER_HOLD`. Structural recomputation and claimed `custodian_timestamp` cannot establish competent pre-execution external issuer, time or custody. Post-hoc rewritten consistent raw payload remains possible without independent third-party seal.
- **Consumer:** `REAL_CONSUMER_MODELLED_NOT_EXECUTED`. Source-free producer and modelled receipt is not actual C1/Field Forge/learned consumer.
- **Source scientific issuance:** NOT ESTABLISHED; no real source execution or B02 permission.
- **Adoption:** no real-source/G0b/EE12/N9/actor authority, no canonical merge.

## Smallest new correction / hostile gate

Issue A04TU on A04T code base, plus reviewer report as external evidence, **only** (a) correct candidate owner-integrity test, and (b) independently authored hostile mutations against real source-free produced and expected raw-field payloads, including same-count substitution, raw/weighted, order, missing jobs, zero-denominator, forged custodian and consumer-obligation laundering; record PASS/FAIL/UNKNOWN with actual runtime. If hostile yields actual verifier defect, repair only new V2 verifier candidate/test with exact patch, then return for separate independent acceptance. Do not redefine old A05 contract, or grant real source/consumer/custodian.

**Terminal:** `HQ280_A04TR_RECEIVED_43OF44_TEST_DEFECT_SCOPE_EXACT__V2_TECHNICAL_POSITIVE_INDEPENDENT_HOSTILES_PARTIAL__GATES_HELD`.
