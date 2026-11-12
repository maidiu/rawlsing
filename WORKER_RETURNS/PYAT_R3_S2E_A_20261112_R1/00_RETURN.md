# PYAT R3 S2-E — Agent A go-firster frozen adversarial handoff

**Disposition:** \`A_SOURCEFREE_NATIVE_BOUNDED_BUILD_TESTED__HANDOFF_TO_B__NOT_G5_ACCEPTED\`.
This is a functioning, independently challengeable **first-turn implementation**; it is **not** a declaration that original P2-06, all five G gates or the whole native original35 mission are complete.

## 1. Exact artifact and reproducible commands

- Repository: \`maidiu/rawlsing\`.
- Original governed mission: [#919 S2-E](https://github.com/maidiu/rawlsing/issues/919), [#909 R3/R3C/R3S](https://github.com/maidiu/rawlsing/issues/909), P2-06.
- Source ancestor: PR [#948](https://github.com/maidiu/rawlsing/pull/948), isolated S1-B/S1-D/S2-F branch \`integration/pyat-r3-s1b-s1d-s2f-scoped-g5-20261112-r1\` **\`7064daa14d93109211629e72d08f3a6e705a0d57\`**.
- Independent A branch: \`agent/pyat-r3-s2e-a-go-firster-20261112-r1\`.
- **Frozen tested code/test cut: \`d7af5b8df922caa86bcd36a7baa0bbb55b43742d\`.** The subsequently appended return/JSON are metadata only; do not substitute their later HEAD for a fresh code-test run if code changes.
- Draft review/descendant: [PR #951](https://github.com/maidiu/rawlsing/pull/951), based on the unchanged PR #948 isolated branch. No protected merge and no paused W03/W04 changes.
- Production changes:
  - \`rawlsing_next/pre553_s2e_exact_conservation.py\` — full-native-output first-reader conservation, exact-query declared-domain comparison, typed byte-cap refusal, full-preimage digest/parity.
  - \`rawlsing_next/pre553_issued_workload.py\` — \`NativeWorkloadResult.exact_s2e_output_census(runtime_catalog=...)\`, a native result method rather than an invented engine.
- Executable tests: \`rawlsing_next/tests/test_pyat919_s2e_a_conservation.py\`, \`rawlsing_next/tests/test_pyat919_s2e_a_whole_native_batch.py\`.
- Actual CI: \`.github/workflows/pyat-r3-s2e-a.yml\`. Machine grade: \`01_G1_G5_RECEIPT.json\`.

At the repository root, Python 3.11 with \`pytest pandas pyreadstat pyarrow duckdb\`:

\`\`\`sh
PYTHONPATH=. python -B -m pytest -q -s -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat919_s2e_a_whole_native_batch.py \
  rawlsing_next/tests/test_pyat919_s2e_a_conservation.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_universal_workload_custody.py
PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat940_s2f_a_counter_provenance.py \
  rawlsing_next/tests/test_pyat940_s2f_b_negative_and_multisource.py \
  rawlsing_next/tests/test_pyat940_s2f_durable_closure.py \
  rawlsing_next/tests/test_pyat940_s2f_fresh_process.py
\`\`\`

**Exact-cut CI witness:** [Actions run 43275018294](https://github.com/maidiu/rawlsing/actions/runs/43275018294), **78 PASS** in S2-E native/hostile/inherited regressions, **19 PASS** in S2-F independent predecessor preservation, **0 FAIL**. The additional Pyat R61 sourcefree workflow at that SHA also passed. Do not attribute these results to any future amended code SHA.

## 2. Reconstructed governing contract and compatible shared keys

Source order: user commission P2-06 → #909 R3/R3C/R3S → #919 S2-E G1–G5 → current PROGRAMMA Pyat/Shared PRE-MAIN/MCR-lite. Reuse actual current code \`pre553_empirical_query.py\`, \`_pre553_query_eval.py\`, \`pre553_discovery_exact.py\`, \`pre553_batch_runner.py\`, \`pre553_issued_workload.py\`, and accepted S2-F \`pre553_durable_empirical_closure.py\`. Do **not** port an old V550J donor, reinterpret physical source permissions, or replace the native evaluator with a counting emulator.

The actual \`I03GroupedExecutionScope._core_key\` hashes a **measure-independent** core over:
- exact sealed release and manifest/replay identity, universe, original respondent-ref root, release-index identity and domain cardinalities;
- exact risk set ref/type, source-scope mode and response-state semantics;
- exact predicate plus grammar authority (therefore **direction matters**);
- full target topology, ordered or set semantics, every declared cell, target-domain replay refs, occurrence-relevant component topology, included response states and semantic authority refs;
- query authority refs and entire canonical authority-registry fingerprint.

**Not shareable as measured output:** raw/weighted numerator and denominator and output fact/replay. \`GOVERNED_WEIGHTED\` authority, exact per-respondent \`Fraction\` weights, design/estimand, and every query-specific EmpiricalFact are recomputed independently from a compatible cached *membership/target-resolution* core. Runtime source or authority-successor bindings force fallback. Capacity overflow falls back to original native evaluation, never silent cell truncation. That is inherited accepted code, **not my new optimization**.

Agent A's audit now requires actual Batch unit/output/receipt one-to-one closure, typed deferred/failed/not-run, exact query and release scope, exact source-universe fact provenance, denominator members subset of risk members, full counts and cell values, exact zero cells, full-domain identity from the **actual issued RuntimeObjectCatalog**, I05 evaluated candidate fates/ancestry and all executed query/predicate preimages, and SHA256 of complete canonical payloads. \`declared_domain_verified=false\` explicitly indicates the caller did **not** supply the original query catalog. This audit cannot authenticate the source issuer merely by hashing self-consistent data.

## 3. Strongest achieved native result

One **real** sourcefree sealed-C11 batch (not isolated four scripted counts) executed five units on 12 synthetic respondents:

- F1 \`Y\` marginal: \`Y=0:10\`, \`Y=1:2\`.
- F2 \`Y|X=1\`: independent denominator \`6\`, \`Y=0:5\`, \`Y=1:1\`.
- Reversed F2 \`X|Y=1\`: independent denominator \`2\`, \`X=0:1\`, \`X=1:1\`. Distinct member ref sets; different predicate prevents accidental grouped reuse.
- F3: actual authorized I05 bounded minority group C, supported minority departure; discovery retains negative/valid-empty fates in the inherited suite and every evaluated frontier candidate receipt.
- F4: actual same-respondent \`X×Y×Z\` **3-way joint**, full eight-cell domain. Four positive configurations with supports \`(0,0,0):5\`, \`(1,0,1):5\`, \`(1,1,0):1\`, \`(0,1,1):1\`; four additional zero cells retained. This is not a product of pairwise marginals.

A complete preimage census of the grouped/native Batch is **byte-for-byte equivalent by its canonical graph digest** to a second execution with grouped sharing disabled, and is also challenged against the independent manually stated 8-cell oracle. Witness graph SHA256: \`befb766af812995cdf06989d1afd83d3f250859df30a1f01968e6f808eef63d0\`.

The sourcefree Batch recorded **5 core builds and 1 core reuse hit**. At this tiny size grouped elapsed **0.032906 s** versus independent **0.028444 s**; thus **there is no demonstrated speedup** in this case. CI Python process maxrss **173012 KiB** is a process high-water, not isolated Batch or full process-tree peak. It measured zero *new source opens during Batch*, with the sealed release already constructed; it did **not** measure original ingestion/source opens or saved-store/scratch bytes. The 100k-cap and S2-D saved-store results are **NOT_RUN**. Never promote this to a production economy claim.

## 4. My hostile findings, repairs and actual attacks

- Initial CI exposed **three failures** in my original new code: one missing synthetic fixture directory and two incorrect equality checks between structured exact-ref representations. Corrected actual logic and reran **74 native + 19 S2-F PASS** at \`d360363296b1aa5b130bd46f0e1ce42373e5793b\`; no source evaluator changed to hide errors.
- A valid-looking \`COMPLETED\` Batch receipt that **drops all result refs** fails \`S2E_BATCH_RECEIPT_RESULT_GRAPH_LOSS\`. Losing a completed unit output also fails; partial/unrun statuses remain explicitly partial.
- A fabricated additional I05 declared candidate with no new receipt fails the candidate-fate check. Preserving the genuine result restores identical digest.
- **Rehash attack:** remove an *observed-zero* F4 cell (unchanged total support), construct a new canonical EmpiricalFact, and forge a matching completed Batch receipt. Without the issued query's target-domain truth, internal self-hashes alone could pass. The new \`_verify_declared_domain\` catches this as \`S2E_INCOMPLETE_OR_FOREIGN_DECLARED_DOMAIN\`. Untouched original reproduces the full graph.
- Source/release, universe and conditioning-direction checks are explicit in the auditor; actual inherited native suites additionally exercise unequal risk, absent overlap, routing UNKNOWN, missing weight basis, occurrence/topology limits, full-domain integrity and higher-order I05 candidate coverage. Not all of those have been driven through **one** five-unit mixed Batch; do not say otherwise.
- A caller-specified canonical proof-transcript byte ceiling cannot silently truncate; it throws \`S2E_EXACT_OUTPUT_BYTES_CAP_HOLD\`. Supplying precisely the full needed byte amount restores identical output. **This only caps serialized evidence updates**; it does not preemptively bound memory used to build native facts or serialize one large preimage.

## 5. Unresolved challenges, attack surfaces and proof boundaries

**Directly challenge these instead of accepting my narrative:**
1. Extend exact joined **native** representative workload over all applicable source/risk/condition/occurrence/authority keys; current A demonstration is 12 synthetic respondents, 5 units, not the complete original35 universe.
2. Challenge mixed weighted and RAW \`Fraction\` behavior, design/estimand/routing/UNKNOWN and repeated event occurrence in shared **multi-operation** batches, not just old single-query test names. Reproduce both conditioned denominator member sets and nonpositive states.
3. Challenge partial/resumed Batch historical output views: \`NativeWorkloadResult.exact_s2e_output_census\` requires full canonical output preimages; a complete receipt alone should not mint absent archived preimages. Determine whether an exact conversion or typed HOLD belongs to S2-E versus S2-D, with no silent restoration.
4. Challenge source/authority revocation **between** execution and audit; a complete self-hash is not current external issuer competence.
5. Challenge I05 discovery generated-query/source relation and all complete/unvisited/held branches under complex mixed first readers; a candidate count is not exhaustive proof.
6. Profile enough compatible operations to demonstrate real amortized efficiency. One hit and no speedup at 12 rows is not G4. Measure actual process-tree RSS, cold/repeat, output/scratch bytes, source opens, cap refusals; S2-D persistence remains held.
7. Exact working-code integration should not be mistaken for G5 independent receiving. A and B may develop/attack but only third-party G5 can accept; no protected merge.

**Significant alternatives rejected:** (i) new parallel F1–F4 calculator duplicating native semantics, (ii) reconstructing F4 from pairwise products, (iii) counts-only checksum, (iv) generic old V552 tensor/SRC04 all-pairs giant-output path, (v) treating a cache HIT as a speedup, (vi) blanket refusal of sourcefree computation because S2-D or original35 grants remain unissued.

**Proof grades:** G1 **PARTIAL** (exact scoped keys/domains, no all35 operation universe); G2 **PASS_SOURCEFREE_BOUNDED** (single actual native Batch and exact parity); G3 **A_SIDE_PASS_AT_TESTED_SCOPE; B ATTACK PENDING**; G4 **PARTIAL** (measurements and evidence cap; no large-scale economics); G5 **NOT_RUN_THIRD_PARTY**. Source/actor/original science permission unchanged; no new original35 native/structural causal/persona claim.

**STOP:** \`A_FIRST_TURN_FROZEN_HANDOFF_TO_B\`. The *duel* does not stop until B's actual descendant and independent G5. No invented council or procedural hold of lawful parallel engineering.
