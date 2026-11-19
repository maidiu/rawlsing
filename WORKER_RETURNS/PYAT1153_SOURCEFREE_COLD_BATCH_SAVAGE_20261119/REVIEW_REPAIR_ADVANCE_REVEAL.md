# PYAT #1097 full-stack continuation — SAVAGE ATTACK / REPAIR / MARATHON ADVANCE / REVEAL

**This return is SOURCEFREE AUTHOR WORK, NOT a science-owner method decision, original-source license, independent G5, verified passing new code, protected receiving or permission to analyze Codex SRC16.**

Repository: `maidiu/rawlsing`. Previous frozen adversarial [#1153](https://github.com/maidiu/rawlsing/pull/1153) at `ecf70102da9c1d85ed189e0355ffdd07a5f5d675`; this next isolated draft [#1154](https://github.com/maidiu/rawlsing/pull/1154) branches from #1153 without changing its author tree. Existing one PROGRAMMA remains [#1148](https://github.com/maidiu/rawlsing/pull/1148) and original #960/#1097 control the receiving route. Re-verify PR #1154 HEAD from the live PR before testing.

## 0. Actual user return, not model-invented tests

The user's attached `.pyat1097-review-proof.zip` was directly inspected from `/mnt/data`: ZIP SHA-256 `0f215a9cbf712245120de5270877341e1256557318861683d07f514fb4c7cb3a`, exact tested SHA `ecf70102da9c1d85ed189e0355ffdd07a5f5d675`, pytest/JUnit **229 tests, 6 failed, 0 errors**; log **223 passed, 6 failed in 43.50 seconds**, exit 1. The failures are two **three-case parametrized families**, not six unrelated scientific bugs:

- `test_pre553_distinct_cold_i03_batch.py:106`: tries to hash native frozen `mappingproxy` target-ref preimages. The query refs themselves remain exact. Repaired test using `exact_ref(q.target_refs[0], "batch target").key`, preserving the actual uniqueness assertion and rejecting collisions.
- `test_pre553_s04_research_batch.py:37`: attempts `canonical_json` directly on an integer-keyed conditioner mapping. Canonical I03 semantic mappings forbid non-string keys. Repaired test using the existing ordered typed axis/value selector instead of compromising the serialization contract.

**No implementation change was necessary to explain those six failures. New remote code and corrected test suites have NOT been executed.** Importing + passing the inherited tests alone is also not independent review or scientific accreditation.

## 1. SAVAGE ATTACK — still missing end-to-end route

[#1153](https://github.com/maidiu/rawlsing/pull/1153) implemented a significant physical improvement: one authenticated sourcefree native cold index across **1/10/100 genuinely different I03 queries**. Its `execute_distinct_native_cold_i03` returns a tuple of native I03 results, but does **not** send these distinct facts into S04 research or FF01 first-consumer custody. Independently, previous S04→FF01 entrypoint opens/receives **one I03** per call. Thus the optimized physical producer and scientific consumer were disconnected. Even a structurally correct one-session native I03 result is not yet proof of a useful research-to-FF01 service.

**Other identified risk:** If someone equates the sourcefree `VerifiedDirectEstate` carrier with authorization to analyze original source data, a C11-*construction-only* grant could be mistaken for I03 permission. A self-declared sourcefree assertion is weaker than a trusted source issuer; do not pretend otherwise.

## 2. Codex HQ ANVIL exact-head reconciliation

**Live full commit independently read:** `00ebc4a162e27a310b89c9a54e251fe063c7ee60`, `WORKER_RETURNS/ANVIL_SRC16_CONSTRUCTION_GRANT_ACTIVATION_20261119`.

- GSS 1972 `SRC16`: `GSS1972.sav`, source SHA-256 `e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204`, 1,613 rows, 216 physical columns; user consent authorizes the **exact original file for C11 construction only** on local host; local-runtime retention. Private 0700/0600 operative source grant is OUTSIDE Git.
- `CURRENT_GRANTED` in the metadata-only resolver, no revocation recorded. **Original source not read or statted/decoded; C11 writer not launched**. No Q2, I03, I05, S04, inference or export authority issued by this grant.
- Shared SQLite-free witness runner cannot yet inject SRC16's source-specific binding; this is a separate ANVIL construction-runner integration gap, **not** a reason to invent new per-wave writer.
- Previous SRC04/SRC17 grants unchanged; **32 other drafts pending**.
- **Exact blob comparison against #1153:** main empirical-query, empirical objects, C11 repo/ingest, direct Parquet estate, carrier executor, discovery/recursive and N10E provider are identical. **Different**: `_pre553_query_common.py`, `_pre553_query_eval.py`, `pre553_direct_estate_i03.py` (our later routing-locator/cold physical path). No protected merge or physical equivalence inferred.
- This new S04 bridge requires `SOURCEFREE_ONLY_ASSERTION` at every invocation and refuses original-SRC16 construction-only purpose text. **It cannot prove that a dishonest caller really used a synthetic fixture.** A distinct qualified source analysis grant/current/rights validator is still required for original sources.

## 3. REPAIR + MARATHON ADVANCE — actual code, not another plan

**`rawlsing_next/pre553_distinct_cold_s04_batch.py`** now composes the **unchanged existing I03 evaluator**, through the #1153 one-prepared-session function, with the existing #1151/#1152 true S04-first and optional FF01 consumers:

One original sourcefree C11 verified estate → one native cold postings preparation → 1/10/100 **distinct original-catalog queries and exact predicates** → separately retained original I03 facts → separate source-exact S04 knowledge per query → caller-selected contextual batch and optional genuine k≥2 FF01 first reader → canonical per-question fact/risk/release/typed-state/knowledge/consumer receipt. No pooling of respondent populations, false determinicity rank, second I03 engine, or new respondent repository.

**Guards before physical index work:** original query/predicate exact closure; no duplicate full query; every query's S04 owner-defined scalar topology and 16,384-cell budget; RAW/SINGLE_UNIVERSE; actual k≥2 if FF01 desired; typed conditioned target axes; protected-use permission guard; explicit synthetic-only scope. CURRENT is checked before/after the one I03 batch and on both sides of each S04 consumer. Any failure returns no partial batch. Legacy direct FF01 route is preserved.

**`rawlsing_next/tests/test_pre553_distinct_cold_s04_batch.py`** attacks native one-session 1/10/100, mixed unary+binary S04 and true FF01 parity with an independently computed native I03 oracle, context deduplication, revocation after first S04, duplicate/invalid/unauthorized preflight before any postings index and SRC16 construction-only negative. Tests written, NOT RUN.

**`tests/measure_pyat1097_distinct_saved_economics.py` + `run_pyat1097_distinct_economics_local.sh`:** observable separate-process comparison of the SAME 1/10/100 distinct sourcefree research questions via legacy per-query cold index versus shared one-preparation S04 path. Both routes must yield identical original I03/S04 fact/knowledge/risk IDs, then report ACTUAL measured wall seconds and peak whole-process RSS. No invented speedup or 100k limit claim. Four-respondent synthetic sourcefree fixture; **measurement NOT RUN**.

**`tests/check_pyat1097_fullstack_against_anvil_00eb.sh`:** byte-exact additive code overlay onto temporary detached corrected Codex C11 `00ebc4a16…` worktree; refuses overlap with any native physical file, validates candidate file SHA byte identity, runs the full exact-head sourcefree suite. This is physical compatibility experiment only; **NOT RUN**.

**Original `run_pyat1097_fullstack_review_local.sh`** updated to compile and test the new consumer bridge alongside the inherited 229-test court. Exact-head/clean tracked checkout and JUnit exit still required. New codes do not obtain automatic green from previous tests.

## 4. REVEAL — unresolved obligations

1. Six historical local RED assertions are repaired in Git, but **no new exact-head PASS** for the repairs or new composed S04 bridge. Proven local ancestor result is RED at #1153; no G5.
2. No original SRC16 analysis grant, no source-issued QSM or new source/semantic CURRENT receiver. Construction-only original-source authorization cannot be repurposed; synthetic assertion is **caller-only**.
3. Candidate ANVIL physical routing-locator code diverges from Codex `00ebc4a16` in three files. Sourcefree native overlay and matched actual query identities across branches remain unexecuted.
4. One prepared index for 100 queries is an *index-reuse structure*, not a measured improvement in wall time or entire process RSS. 1/10/100 separate-process benchmark is available, **not run**.
5. Full original 100k/high-width 6GiB/physical scratch target, original source rights, repeated/multiselect/wave, extraction cost are held. The new API retains every original I03 result/roster in memory; no bounded total-memory claim.
6. Original I03 outputs can contain partial/held cells. #1153 repairs conserve them; new bridge must prove they remain held through actual S04/FF01 receiving.
7. Scored determinicity estimator, design-weighted variance, rank stability, multiplicity, secondary recursive minority discovery/stopping and class/material FF02 science are not issued by sourcefree exact counts. Scientifically owner-held.
8. Default FF01 adoption and full S05 FIABC→M1/M2/B5 learned route, N10E one-pass consumer, FF02/N9/N10W/V3 and actual actor/person/family remain unfinished.
9. Host Git linked-worktree `bad object worktrees/code/HEAD` auto-GC defect remains a separate potential tool-integrity hazard, not repaired by Python tests.
10. No independently verified writer lease, independent nonauthor G5 for new code, original source-rights waiver or protected PRE-MAIN / paired CURRENT_PROGRESS CAS.

**Next bounded operation:** execute exact #1154 sourcefree suite, repair any real RED on #1154; then run exact 1/10/100 benchmark and Codex 00eb same-suite overlay. Distinct reviewer must challenge the new sourcefree entrypoint and its negative/rights/physical claims before authorized receiving into original PROGRAMMA.

**Final status:** `SAVAGE_AUTHOR_REPAIRED_SIX_OLD_LOCAL_REDS__ONE_INDEX_DISTINCT_I03_TO_S04_FF01_AUTHOR_CODE__ACTUAL_RUNTIME_AND_CODEX_OVERLAY_NOT_PROVED__SOURCE_SCIENCE_G5_PROTECTED_HOLD`.
