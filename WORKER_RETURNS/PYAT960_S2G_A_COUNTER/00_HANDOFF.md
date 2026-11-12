# PYAT960-S2G — A counterattack handoff

## 1. Exact revised artifact

- Packet: S2-G / P2-08, original #919, successor #960.
- Contract SHA256: `635a423beea158a67653d8c03ea7aee9c158f21986d4d598018d0976db73552b`.
- Contract source cut: `WORKER_COMMISSIONS/PYAT_SUCCESSOR_960/contracts/S2-G_v1.md@63836a168cc99b0ed8f87f7f7a6e76192f7a1898`.
- Contract freeze: `63836a168cc99b0ed8f87f7f7a6e76192f7a1898`.
- Branch: `agent/pyat960-s2g-a-r1`.
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat960-s2g-a`.
- Protected base: `6a5c12f04323d74001f9632063ec907f4fc4468e`.
- Startup / B delivery: `220ebd3311fb0607079ed6a6e9a364d6681e5378`.
- B code cut: `0071aefb05d8ebbd75058a10c5e831d994a2f96f`.
- A prior delivery / B base: `eb8f097341738dcc08ae3172fa35aeebcdc061c3`.
- A counter implementation cut: `2beada4a0180721f963e59b48472f2c9e3e320eb`.
- Session: `ses_e3120ba1cffeO1w43uU5MLh4yq` / `opencode-go/deepseek-v4.1-flash#max`.
- Return directory: `WORKER_RETURNS/PYAT960_S2G_A_COUNTER/`.

A-counter code changes are only:

- `rawlsing_next/pre553_durable_learned_lifecycle.py`
- `rawlsing_next/tests/test_pyat960_s2g_a_counter_subset.py`

The existing M1/M2/B5/world/S2-F/I02/Parquet/query/discovery/FF/C11 owners remain read-only. No protected merge, model/provider/harness change, original-respondent read, source-native read, or production issuer was performed. Earlier A/B return directories were not edited.

## 2. B received as an equal capable opponent

I independently read B's handoff, receipt, code diff, new tests, and the actual frozen contract. B's code cut `0071aefb` is a real descendant of A's base; B did not replace the native chain or the base product. B's four claimed defects were reproduced, not accepted on assertion:

- **B-D1 (cross-chain M1 evidence, SEV-1): reproduced and accepted.** B's artifact using a foreign M1 fact/receipt chain under the base S2-F determinants previously served `LEARNED_CONSUMER_EXACT_SUPPORTED`. B's repaired code refuses at cold consume with `M1 input bundle discovery_receipts is not drawn from the declared S2F closure`. The base artifact remains exact.
- **B-D2 (unpinned/foreign as-of checkpoint, SEV-1): reproduced and accepted.** The unpinned foreign checkpoint now raises `DurableLearnedLifecycleUntrusted`; the same checkpoint pinned by its own hash raises `DurableLearnedLifecycleRefusal` because it is not on the retained event history. The artifact's own pinned checkpoint still resolves `CURRENT_SELECTED`.
- **B-D3 (B5 replay/learned-receipt/protocol conservation, SEV-1): reproduced and accepted.** Tampered replay event lists, learned-receipt event refs, protocol `product_family_ref`, and learned-receipt M2 authority provenance are refused under a new self-hash pin. The unmodified artifact still serves exact.
- **B-D4 (changed-input evidence, SEV-1 evidence gap): reproduced and accepted.** B changes real native physical cells in the same M01 route (`R1/X 1→0`, `R2/X 0→1`) and produces a changed S2-F root `586d39bd...`, M1 `9687134b...`, M2 `5ec7935c...`, B5 `b81a25b0...`, artifact root `84e99c5f...`, and world consumer hash `4cef580c...`. Restoring the original artifact reproduces root `852498f7...` and consumer `2690cdbe...` exactly. This is stronger G2 evidence than A's original family-rule-tag change.

B's exact test claim reproduces as part of the 153-test run: all 152 B-preserved owner/adapter/B tests pass, plus the A counter test. The separate S2-F regression command remains 19 passed. B's base artifact identities are preserved:

- artifact root `852498f72ed7c1940d55caae0a75bab6869aa854bb83f7a39451debc57be2fe5`
- artifact identity `bb14f54c88515f8c0e0d1806afc0457fa1439d9c4212ad07381b9f7bc8df23eb`
- checkpoint `327a56898cdf8cae9ca1fa3bd778e1d3ede88faea2c5b88f06ed16ec2a69794d`
- S2-F root `eae60b4aaec326ddd028419c640713e20abe347347e1d242ee9a65d6872152e2`
- consumer `2690cdbeadabb0e90179d726029fa8b765995a15a1da26d7fe72bba0819bd597`

## 3. B's strongest falsifiers — results

B explicitly challenged the repaired boundaries. I ran the most consequential attack rather than merely restating B's own tests.

### 3.1 Same-closure subset fact versus producing receipt — **B was incomplete; A-C01 found**

B's B-D1 repair checks that M1 receipt refs, query refs, predicate refs, facts and source release are subsets of the declared S2-F closure; it did not check that a retained discovery receipt's **owned facts** are still in the M1 disposition and bundle after a coherent mutation.

At B code cut `0071aefb`, I published a mutant whose consumer discovery receipt remained in the M1 disposition, but one fact owned by that receipt was removed from both:

- `m1_evidence.input_bundle.semantic_fields.empirical_facts`
- `m1_disposition.empirical_fact_refs`

The determinant receipt's `input_bundle_ref` and content hash were consistently recomputed, the disposition was recomposed through the actual M2/B5 owners, and the new artifact was opened under its own external pin. B's code accepted it and the actual existing world consumer returned:

```text
artifact root: 92ba894b4fa08916...
consumer state: LEARNED_CONSUMER_EXACT_SUPPORTED
consumer hash: 2690cdbeadabb0e90179d726029fa8b765995a15a1da26d7fe72bba0819bd597
```

This is the same frozen G1/G2 failure class B identified: the M1 product was not the product of the evidence owning the consumer receipt. B's B-D1 repair caught a foreign chain but not a same-closure receipt/fact omission. The pre-repair RED is preserved in:

- `evidence/b_cut_receipt_fact_omission_red.txt`

The exact RED record is `B_CUT_RED Failed: DID NOT RAISE` from the counter test run against B cut `0071aefb`.

### 3.2 A-C01 repair

At implementation cut `2beada4a`, `_m1_evidence_binding` now additionally requires, for every discovery receipt retained by the M1 disposition:

- the receipt is present in the declared S2-F closure;
- all facts owned by that receipt's `empirical_fact_refs` and `validation_fact_refs` are present in the M1 disposition's empirical fact refs;
- those facts are present in the stored M1 input-bundle fact rows;
- those facts are present in the declared S2-F closure facts.

The mutant now refuses at cold consume:

```text
DurableLearnedLifecycleError:
M1 disposition omits a fact owned by a retained discovery receipt
```

The original base artifact still serves exact. The focused counter test is:

```text
rawlsing_next/tests/test_pyat960_s2g_a_counter_subset.py::test_a_counter_receipt_fact_omission_is_refused
1 passed
```

The repair is intentionally narrow: it closes the reproduced receipt/fact relation, not a new optional benchmark or a redesign.

### 3.3 Multi-release closure / different consumer release

I inspected the release binding rather than claiming a defect without a consequence. B's code requires:

- the consumer's determinant release to be in the M1 input bundle's additional dependency refs;
- the consumer discovery receipt's `source_release_refs` to contain that release;
- the consumer receipt/query/predicate to be in the disposition;
- the M1 bundle/disposition evidence to be in the same closure.

B's current tests and the base chain use one release. I did not manufacture a multi-release positive artifact strong enough to prove a false acceptance or false refusal. **No material multi-release defect is claimed.** The residual boundary remains a next falsifier: a lawful multi-release product whose receipt facts span releases may require an explicit all-release dependency check, and a future receipt with `validation_fact_refs` distinct from `empirical_fact_refs` may test whether the A-C01 check is too literal. No repair was added without reproduction.

### 3.4 Multi-product B5 history

B's tests cover retained replay/receipt/protocol history. I also re-ran the existing supersession/as-of history tests; they pass. B's product-event equality check and retained-event prefix logic do not produce a false refusal in the exercised one- and two-selection chains. No new multi-product defect was reproduced. The next receiver should still test a genuinely multi-product B5 executor where two releases coexist and a learned receipt's event set is a valid product subset.

### 3.5 Fully coherent rehash plus a new external pin

A fully coherent rewrite of every artifact field plus a caller-supplied new pin is a different artifact by construction. The external pin is the sole trust anchor; self-hash alone never grants CURRENT. This is a documented trust boundary, not a defect. No production issuer exists here.

### 3.6 Cold base and changed consumer

The base artifact reopens cold and returns `LEARNED_CONSUMER_EXACT_SUPPORTED` / `2690cdbe...`. B's changed native artifact returns `4cef580c...`. Exact restoration returns the base root and base consumer. The fresh-process runner reports `source_opens=[]` and `matches_expected=true`.

## 4. Full test evidence

Selected owner + S2-G + B + A-counter command:

```text
python3 -m pytest \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  rawlsing_next/tests/test_pre553_learned_empirical_adjudication.py \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py \
  rawlsing_next/tests/test_universal_learned_consumer.py \
  rawlsing_next/tests/test_pyat960_s2g_durable_lifecycle.py \
  rawlsing_next/tests/test_pyat960_s2g_fresh_process.py \
  rawlsing_next/tests/test_pyat960_s2g_b_adversarial.py \
  rawlsing_next/tests/test_pyat960_s2g_a_counter_subset.py -q
```

Actual:

```text
153 passed in 46.49s
```

This preserves B's 152 tests and adds the A counter. The output is retained at `evidence/selected_153.txt`.

S2-F regression:

```text
python3 -m pytest \
  rawlsing_next/tests/test_pyat940_s2f_durable_closure.py \
  rawlsing_next/tests/test_pyat940_s2f_fresh_process.py \
  rawlsing_next/tests/test_pyat940_s2f_b_negative_and_multisource.py \
  rawlsing_next/tests/test_pyat940_s2f_a_counter_provenance.py -q
```

Actual:

```text
19 passed in 8.57s
```

The mandatory G01-G09 and B01-B05 commands/results are recorded in `receipt.json`; all are green at the isolated fixture grade. The exact A-C01 RED/GREEN evidence is recorded separately.

## 5. Resource / storage evidence

Measured on the fresh base artifact with the current adapter after the A-C01 check:

| Measure | Value |
|---|---:|
| Artifact root | `852498f72ed7c1940d55caae0a75bab6869aa854bb83f7a39451debc57be2fe5` |
| Retained disk | `32,499` bytes |
| Compressed blob | `31,987` bytes |
| Manifest | `512` bytes |
| Logical preimage | `283,854` bytes |
| Peak scratch | `31,987` bytes (B measurement) |
| Cold open | `0.145` s |
| First consumer | `0.062` s |
| Repeat consumer | `0.063` s |
| Parent test process peak RSS | `107,925,504` bytes |
| Fresh child process peak RSS | `29,110,272` bytes |
| B fresh child peak RSS (candidate) | `41,558,016` bytes |
| Source opens | `0` |
| 6 GiB cap | PASS at fixture grade |
| Integrated 100k / 6 GiB | NOT_RUN |

These are fixture-grade measurements. The fresh child RSS is a single child process `RUSAGE_SELF` peak, not a multi-process-tree benchmark; the parent peak is reported separately. No 100k matrix was run and no integrated cap is claimed. Full evidence: `evidence/s2g_counter_evidence.json`.

## 6. Original G1-G5 mapping

- **G1 — exact M1/M2/B5/consumer contract and non-loss:** PASS candidate at `S2_SOURCEFREE_ISOLATED_FIXTURE`. B's M1-to-S2F binding, M2/B5/replay/protocol/learned-receipt conservation, and A-C01 receipt-owned fact conservation are all enforced at cold consume. Exact M1 bundle/family-rule/determinant receipt, M2 subject/five closures/release, B5 checkpoint/history/subject/protocol/selection/replay, learned receipt and consumer determinants are retained and reconstructed.
- **G2 — durable cold change and exact restore:** PASS candidate. B01 native-cell change reaches M1→M2→B5→existing `evaluate_learned_world_consumer`; changed consumer `4cef580c...`; exact base restore `published=false`, root `852498f7...`, consumer `2690cdbe...`; fresh process exact.
- **G3 — hostile negative and preservation:** PASS candidate. B's cross-chain M1, foreign/unpinned as-of, replay/receipt/protocol/M2 provenance tampering, plus A-C01 receipt-fact omission, all refuse. Revoked/wrong-purpose/stale/wrong-root/missing-pin attestations and wrong as-of refuse; true no-current and supersession/as-of history are preserved; crash-before-manifest recovery works.
- **G4 — provenance/custody/recovery/resources:** PASS candidate at fixture grade. One compressed content-addressed artifact plus 512-byte manifest; atomic staging/CAS/fsync; external pin; cold fresh process; exact restore; retained/peak disk, scratch, timings and source opens measured; 6 GiB cap PASS; integrated 100k NOT_RUN.
- **G5 — independent terminal receipt:** NOT_RUN. No distinct nonauthor reviewer other than A/B has received the exact SHA. This is `DELEGATED_CANDIDATE`, not PASS.

## 7. B strengths accepted, B limits retained

Accepted as genuine improvements:

- B-D1 foreign-chain refusal.
- B-D2 independent as-of pin plus retained-history prefix check.
- B-D3 replay/learned-receipt/protocol/M2 provenance conservation.
- B-D4 same-chain native-cell change and exact restore.
- B's base identities, 152 tests, 19 S2-F regressions, external pin, CAS/fsync/crash recovery and no-current/supersession behavior.

B's repair was incomplete at the exact boundary B itself named: a receipt can remain in the M1 disposition while its owned fact is removed from the disposition/bundle. That survived B's tests and was accepted by the actual consumer. A-C01 repairs it. This is the only consequential defect I reproduced; no other speculative repair was added.

## 8. Own worst vulnerability, missing proof, strongest next falsifier

**Worst vulnerability:** the M1 evidence binding is enforced at cold consume, not at publication. A foreign or internally inconsistent M1 artifact can be stored on disk, but it cannot serve through the declared first consumer. The new receipt-fact check covers the reproduced omission, but a future lawful M1 receipt whose `validation_fact_refs` are not represented in `disposition.empirical_fact_refs`, or a multi-release product whose receipt facts span multiple releases, could expose either an under-check or a false refusal. A fully coherent rewrite plus a new external pin is a different artifact by construction.

**Missing proof:** no production current/as-of issuer or revocation service; no accepted complete S2-E/S2-D joined upstream; no scientific M1 family validator/science rule; no original35 source; no integrated 100k/6 GiB run; no independent nonauthor G5.

**Strongest next falsifier:** build a multi-release S2-F closure where the consumer receipt and determinant release differ from the release recorded for another fact in the M1 product, and verify that the M2/M1 dependency closure and receipt-fact checks still refuse a partial chain. Also try a valid receipt with distinct validation facts to test the A-C01 check for false refusal.

## 9. ABI / scope / authority

- ABI classification: **LOCAL**. One adapter validation plus one new test; no existing owner API changed. Adapter APIs remain the B-repaired versions.
- Affected task relationship: S2-E/S2-G/S1-D dependency/consumer only; no running contract silently changed.
- Breaking interface: false. Source/authority change: false. Scientific hold: true.
- Engineering grade: `S2_SOURCEFREE_ISOLATED_FIXTURE`, `READY_FOR_RECEIVING` at that grade.
- Scientific grade: `NONE_VERIFIED`; TEST_ONLY native validator only.
- Authority grade: TEST_ONLY external current/as-of stand-in; production issuer, revocation/current authority and protected merge are HOLD_EXTERNAL.
- Disposition: `HOLD_EXTERNAL` for full original S2-G; integration `UNMERGED`; independent G5 `NOT_RUN`.

## 10. Next turn

The next actor is one distinct nonauthor G5, other than A and B, at exact code cut `2beada4a0180721f963e59b48472f2c9e3e320eb` (or the final return-freeze tip) and the stated isolated grade. Focused review should re-run the cold base/changed/restored consumers, the B-D1/B-D2/B-D3 controls, and A-C01. No broad reconnaissance, optional benchmark matrix, or endless A/B loop is warranted. If G5 finds a reproduced in-scope SEV-0/1/2, at most one precise repair/handoff remains.

## 11. Quick reproduction

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat960-s2g-a
python3 -m pytest \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  rawlsing_next/tests/test_pre553_learned_empirical_adjudication.py \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py \
  rawlsing_next/tests/test_universal_learned_consumer.py \
  rawlsing_next/tests/test_pyat960_s2g_durable_lifecycle.py \
  rawlsing_next/tests/test_pyat960_s2g_fresh_process.py \
  rawlsing_next/tests/test_pyat960_s2g_b_adversarial.py \
  rawlsing_next/tests/test_pyat960_s2g_a_counter_subset.py -q
```

Expected: `153 passed`.

```bash
python3 -m pytest rawlsing_next/tests/test_pyat960_s2g_a_counter_subset.py -q
```

Expected: `1 passed`; the same test against B cut `0071aefb` produces `DID NOT RAISE`, recording the A-C01 defect.
