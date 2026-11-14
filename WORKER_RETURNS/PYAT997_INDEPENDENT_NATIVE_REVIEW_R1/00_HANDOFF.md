# PYAT #997 — independent nonauthor native review (G5)

**Decision:** `REVISE_EXACT_DEFECT` · **G5:** `FAIL` · **Integration:** `UNMERGED`
**Reviewer:** `ses_e30a442d8ffeYBbXi7rPUpPxoc`, distinct from Browser A/B and native executor `ses_e3120ba1cffeO1w43uU5MLh4yq`.
**Model:** `opencode-go/deepseek-v4.1-flash#max`; branch `review/pyat997-native-independent-r1`.

## 1. Exact reviewed cuts

| Item | Value |
|---|---|
| Contract source cut | `WORKER_COMMISSIONS/PYAT_S01_S05_FLIGHT_997_1002/sources/issue_997.md@cecfc154262eaa140d003e9e704811f44b940455` |
| Contract SHA-256 | `d3717f25d12b09d16f2fb9db1fa7f50f7d9fa387aff7ea9a48af0265cd78b6ca` |
| Original #918 / #909 SHA-256 | `7476fd6f…` / `24a0ec94…` |
| Native evidence HEAD | `11d6f480349a09b871414c3dc1c3f4fa3e680797` |
| Browser candidate | `2c476e739a263dd0069b54706c6cfa63b07190c1` |
| Executable product cut | `534fb6602cce60fd991abd7972ebd95c92f3146c` |
| Test patch | `e79990e0c650924ab989a5cdc1b0777d1314032281ebcec0148261783cf4ca35` |
| Product code equal at Browser/product/native HEAD | yes |

The new P0/P1 code is `pre553_source_saved_body_bridge.py` (`eddaa9a5…`) and `pre553_source_postconsumer_receipts.py` (`fad3a96b…`), over the unchanged Q2/S2-C/S2-D/native owners. I wrote only `WORKER_RETURNS/PYAT997_INDEPENDENT_NATIVE_REVIEW_R1/`; I applied the exact test patch only to a private proof copy.

## 2. Material defect — the R3 Batch QUERY/F4 is self-issued and prohibited

The R3 claim “1 QUERY + 1 DISCOVERY, actual compiler-catalog joint F4” does not survive the actual compiler record.

`compile_governed_frontier` returns a compiler-issued TEST_ONLY workload with:

```text
workload.requests    = 0
workload.discoveries = 1
record.expected_jobs = [("DISCOVERY", ...)]
```

`issued_batch_f4_r3/harness.py::_materialize` then separately constructs:

```text
NativeWorkload(requests=(joint_query,), discoveries=(discovery.ref,))
IssuedWorkloadRecord(decision_ref=urn:test:pyat997:r3:..., expected_jobs=QUERY+DISCOVERY)
TestOnlyIssuedWorkload(...)
compilation = replace(compilation, issued=manual)
```

The selected q101/q102/q103 catalog query is **not present in any `plan.records` query_refs**. All 12 matching F4-like frontier operations are `PROHIBITED` (`JOINT`/`CO_TRAVEL`, `SAMPLE`). The test patch’s own receipt says the frozen issued workload has **0 QUERY / 1 DISCOVERY** and records `BATCH_QUERY_UNIT_NOT_ISSUED`.

`witness_issuer_binding.py` (runnable, exits 1 on the RED) reports:

```text
compiler_has_query_unit: false
manual_has_query_unit: true
same_compiler_record: false
same_compiler_workload: false
joint_query_in_compiler_plan: []
f4_like_dispositions: ["PROHIBITED"]
red: true
```

The postconsumer join compares the manual `workload` to the **already replaced** `compilation.issued.record`, so it cannot detect the substitution. The R3 F4 eight-cell/denominator-5 result is mechanically real native output, but it is a self-issued prohibited query, not an original source-qualified eligible operation or compiler-issued Batch unit. This is a false positive attribution, not a test-only label nuance.

### Minimal rightful owner path

1. Do not replace `compilation.issued`. Execute only the actual compiler-issued one-DISCOVERY workload and mark Batch QUERY `NOT_ISSUED`/`HOLD`; report q101 direct I03 separately.
2. Or have the R03/issuer owner emit an exact QUERY job for an **eligible** operation with its own decision/envelope/expected jobs; make `join_saved_source_operation_fates` require the unchanged compiler record and add a negative test that a manually replaced record is refused.
3. Browser test owner adopts the exact test patch; no reviewer patch.

## 3. What is real and banked

- **P0 source body bridge:** one source read/decode/cell pass, 13 typed families, no second decode, temporary journal cleaned, unchanged S2-C persisted estate, exact source/I02/replay/release. Patched 75/75; product 182 hashes unchanged.
- **Direct q101 native I03:** `SUPPORTED`, denominator 5, cell total 5; country-coordinate `UNAVAILABLE/RISK_SET_UNAVAILABLE` negative; changed q101 cell and exact baseline-byte restore.
- **P0 negatives:** missing body, wrong root, wrong CURRENT, source/transport drift; all fail closed.
- **Discovery/I05:** 150 native candidate receipts exactly joined; 147 positive-linked operations; 389 eligible pending; 2140 rows; 536 ELIGIBLE / 1076 HELD / 528 PROHIBITED. B R5 frontier/census/measure/source-realization guards pass.
- **Compiler-issued discovery NORMAL/COMPLETED:** pass; source opens 0, full C11 builds 0, one completed result/8 refs. This is the clean path.
- **All35 historical ledger:** 35 sources / 18,276 items / 18,413 slots / 26 unjoined pass in 3 focused tests; no original source execution.
- **Fresh process:** producer exit 0, source file deleted, consumer source opens 0, full C11 builds 0, I03 SUPPORTED, I05 150 receipts. Its Batch still includes the invalid manual QUERY.
- **Resource:** 5 respondents, 3 questions + country; 13-family counts `AuthoritySnapshot 7`, `RespondentEvent 15`, `RoutingEligibilityFact 15`, `EmpiricalCoordinateFact 5`, `QuestionVariableBinding 3`, `RespondentIdentity 5`, `EmpiricalUniverse 1`, others zero; 14 Parquet; retained 626,671 B; stage 913,391 B; self peak RSS 218,910,720 B; full C11 0. **100k/6 GiB NOT_RUN.**

## 4. Read coverage still incomplete / held

- R3 two-unit PARTIAL/ABSENT uses the manually issued QUERY. The actual compiler-issued workload has one DISCOVERY, so a genuine two-unit partial is not proved. The accepted S2-D five-reader direct-estate test is 7/7 but is not a Q2 estate substitute.
- No `UNKNOWN`/`DEFERRED`/`INAPPLICABLE` fate row is exercised in the 2140-operation fixture; `WeightMeasureFact` is zero. These original axes are not independently demonstrated at this 5-respondent cut.
- **Known S2-A native kernel:** candidate `pre553_direct_estate_i03.py` is `8b4d5ca2c865e4ef5f5fb609cce15ca3ba64899e`; prior independent G5 `f88a6c61…` reproduced a coherent body_json/projected+locator poison changing actual native I03 fact with no refusal. Public fix `5727db0…` is author-only/public, not native. I did not rerun the full S2A court; this is a native-owner HOLD.
- **Test patch adoption:** exact patch gives 75/75 in my private copy; canonical tests remain 68/7. The patch is not adopted; three patched test blobs are exact (`148c7c29…`, `c3077ce8…`, `3ca7396…`). No weakening found: baseline bytes for restore, exact compiled q101 target, country negative retained, declared 0/1 domain, exact guards, zero receipts after refusal.
- Original35 source/science/rights, production CURRENT, protected merge, #998 full joined, #1001 full scale, #1006 baseline, N11/N12 and 100k/6 GiB remain separate holds.

## 5. Three courts

- **Engineering:** P0 body bridge, q101 direct I03, discovery/I05, compiler-issued discovery normal/completed and all35 are real. The P1 Batch QUERY/F4 bridge is a material self-issued/prohibited-query defect.
- **Science:** Sourcefree TEST_ONLY 5-respondent generated SAV; no original35 science or production issuance. F4 is a real joint computation but attached to a prohibited operation; it is not accepted as an S1-E eligible positive.
- **Authority:** TEST_ONLY only; Q2/S2-C/S2-D/native owners read-only; S2-A native kernel and test adoption are external holds; integration `UNMERGED`; no protected/source/current/merge claim.

## 6. Verdict and next custody

`REVISE_EXACT_DEFECT` at native evidence `11d6f480…` / product `534fb660…`; G5 `FAIL`; no `ACCEPT_SCOPED`, no terminal closure, no original S1-E completion. Bank P0/direct-q101/discovery/normal/completed/all35/resource; repair the query issuer binding, adopt the exact test patch, and resolve/accept the S2-A native kernel owner dependency, then submit a new immutable SHA for fresh nonauthor G5. No new A/B campaign, no Q3 writer, no 100k, no protected merge.

Evidence: `WORKER_RETURNS/PYAT997_INDEPENDENT_NATIVE_REVIEW_R1/evidence/`, especially `issuer-binding-witness.json`, `coverage-matrix.json`, `r3-harness-summary.json`, `baseline-75-canonical.txt`, `patched-75.txt`, `completed-compiler-issued.json`, `all35-ledger-tests.txt`, `resource` fields and `known-kernel.txt`.
