# Hostile independent S04→FF01 receiving — **candidate**, not accreditation

**Base frozen:** #1150 live head `a0e68e349afe0414ef2ebfbb91d4c8ffd3f848b2` (the frozen user handoff `135c3454…` was two commits older). #1149 remains independently authored at `1f32f15eb1302fb1c25dc9e76a6f08e71b46aa10`; #1148 at `fced774b4aa8d32e6cb03b490c793ad4e1146a33`. This independent branch does not modify either author branch, protected PRE-MAIN, native I03/C11 physical reader, source grant or PROGRAMMA.

## Reproduced in exact static source, not a claimed executed RED

1. #1150 `test_pre553_s04_ff01_read_conservation.py` calls `receive_s04_i03_research(query,execution)` and `receive_ff01_observed_joint(query,execution)` **independently** and asserts equal fields. The FF01 recipient does not take S04 knowledge: an architectural missing-first-consumer edge.
2. #1150 S04 `receive_s04_i03_research` originally required full cells but did not compare exact `fact.target_domain_identity` and `fact.target_topology["target_domain_identity"]` to the native selected query's canonical domain identity. #1149 FF01 checked this correctly. This allows a source-integrity mismatch to pass through the upstream boundary.
3. Historical user `160 PASS/1 FAIL` concerned the test text expecting `widen` on reserved STRONG_CAUSAL; #1149 corrected its test by separately covering protected use and lawful-label subset widening. No independently executed replay in this environment.
4. #1150 newer two commits after `135c…` correct I05 frozen mappingproxy empirical fact refs by normalizing `exact_ref` before set membership; do not discard the repair.

## Bounded isolated repair

`pre553_s04_observed_research.py` now rejects canonical selected native joint-domain mismatches with a source-exact identity, including explicit full-domain set completeness; this changes no source decoding, issuer or FF domain ABI.

NEW `pre553_s04_ff01_consumer.py` makes an **existing** `FF01ObservedJoint` from the **already published S04 joint**. It retains the exact I03 `QueryExecutionResult` only for independent hash/issuer/source/replay cross-check against potentially counterfeit rehashed S04 JSON. This is not a second empirical query or a new respondent engine; the S04 projection validation does reread the in-memory aggregate for trust. It imports the #1149 existing FF permission/domain helpers and maintains the current downstream FF01 ABI. No causal/scientific rights or N10E source-aware issuing are invented.

NEW tests compare value- and ref-exact with direct FF01 oracle, false self-rehash, alien release, negative LOW_SUPPORT, prohibited permissions, wrong domain identity, 3-way parity, F2 direction, and one cold persisted I03 same-release first consumer. The **direct FF01 oracle runs only in tests**, never in the new production adapter.

**Evidence grade:** source/code authored on independent branch, tests **NOT EXECUTED** until a real sourcefree runner receipt is supplied. Current #1150 CI previously failed without source-level step proof. No true #997/#998 joined source→S05, native original SRC04 source decode, 100k/6GiB economy, scientific determinicity ranking, original-source permission, independent G5, or protected receiving. Do not claim terminal #1009.

**Required local command**: `EXPECTED_S04_SEAM_HEAD=<THIS_BRANCH_EXACT_HEAD> bash rawlsing_next/tests/run_pyat_s04_hostile_seam_local.sh`. Existing sourcefree ancestor checks and exact downstream usage, not a second research programme. If a RED occurs, repair this same independent branch, replay and have separate nonauthor reviewer verify.

## Additional original-source/cold-reader adversarial findings

- Codex `b3dd74d16` and S04/FF01 parent `a0e68e34` have **identical blob hashes** for native `pre553_empirical_query.py` (`8885e637`), `pre553_source_direct_parquet_estate.py` (`e8622ac6`), `pre553_c11_ingest.py` (`37cd35fa`) and `pre553_batch_runner.py` (`8320f284`).
- They **differ** in `pre553_direct_estate_i03.py` (`d662fc57` vs `9fd39efb`), `_pre553_query_common.py` (`da536ff7` vs `402186dd`) and `_pre553_query_eval.py` (`87849f7c` vs `7372290e`). The parent has a more recent routing-locator/cold-query path; tests on the Codex witness **cannot prove this exact separate code**, or vice versa. This independent branch does not modify or prefer either physical owner version.
- The previous manifest's direct FF01 exact-relation/condition and N10E crossread are not full same-source **one-pass** N10E value production: N10E remains independently executed, exactly as its prior code declares.
- The new `test_real_existing_n10e_crossreader_consumes_s04_derived_ff01` checks the **actual accepted N10E crossreader** from an FF01 receipt created from S04 and original native I03; result must have forward conditional denominator 60, yes=54/no=6. This confirms one additional first-consumer edge **if and only if executed successfully**. It does not claim no extra N10E I03 query, original source rights, or selected N10W world.

**Self-attack:** the first attempt at S04 native-domain guard incorrectly converted unary F1 scalar domain to a one-value array. A separate follow-up commit repaired it; inherited native one-target F1 test is explicitly in the full runner. All new tests remain `NOT_RUN` here, not a green receipt.
