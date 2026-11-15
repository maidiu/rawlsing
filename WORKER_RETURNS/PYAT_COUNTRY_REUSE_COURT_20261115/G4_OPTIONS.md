# G4 — Smallest owner-authorized options (not implemented)

**No implementation is performed or authorized by this return.** The three options are recorded separately because they have different owners, risks and evidence. B is a **source-grounded but unmeasured hypothesis**, not an implemented candidate or a measured optimization. Do not choose C merely because the cold path is slow.

## A. Existing qualified grouping (already lawful, narrow)

**What exists:** `I03GroupedExecutionScope` on a sealed `C11Repository`; measure-independent exact core reuse with per-operation measure/fact/replay rebuild.

**Measured:** 100 distinct operations → 80 core builds + 20 core hits (the 20 governed-weighted measure variants). Default `max_groups=64` adds 16 capacity fallbacks; `max_groups=256` has none. Exact parity 100/100. Repeat invocations of one operation: 1,000 → 1 build + 999 hits; the author's grouped repeat wall was 15.683 s versus 52.035 s ungrouped (3.32×) on the in-memory path. The independent review reproduced the receipts; its repeat walls were 15.925 s versus 56.238 s. Wall is ambient-contended; the receipts and exact parity are the strong evidence.

**Cold saved scope:** refused by both public guards. The cold `_DirectReleaseIdentity` lacks `semantic_release_hash` and `source_release_manifest_hash`, and `indices_for` returns a new index object per call, while `_index_identity` includes `id(index)`.

**Smallest A qualification:** a versioned cold release/index identity adapter plus a stable exact prepared index across operations. Even then A would share only exact same-core measure variants, **not** the 80 distinct predicates/targets. A is therefore not a solution for hundreds/thousands of distinct operations; it is a measure-variant/repeat cache.

**Owner/files:** #960/W05-P03/#1006 performance owner with the semantic I03 evaluator/iterator owner; `rawlsing_next/pre553_empirical_query.py::I03GroupedExecutionScope._index_identity/_core_key/evaluate`, `rawlsing_next/pre553_direct_estate_i03.py::_DirectReleaseIdentity/indices_for`, `rawlsing_next/pre553_saved_c11_admission.py::execute_i03`, `rawlsing_next/pre553_carrier_execution.py::CarrierNeutralResearchExecutor.execute_i03`.

**Test falsifiers:** exact cold/native parity for all operations; core hits only for exact same core; 80 distinct cores still build; no cross-predicate/target reuse; no guard removal; existing 16 grouped tests still pass; cold current/revocation and bodytruth negatives unchanged.

## B. Bounded iterator / prepared-session repair — source-grounded hypothesis, NOT measured

**Status:** **hypothesis only**. There is no B implementation, no B patch, no prepared-session/iterator code change, and no B A/B run in the frozen evidence. The court measured the **cold cost target** that motivates B; it did not measure B, and it does not qualify any B performance gain.

**Measured target:** the cold 100-op author pass paid 100 cold session builds, 43,130 row-group reads, 94,068 family rows, 29,343 event object materializations and a metadata-sum proxy of 576.8 MB compressed / 2.36 GB uncompressed reads for a 1,451-row, 2.15 MB estate. The instrumentation-inclusive `_build` wrapper was 6.38 s of 51.93 s (12.3%); the repeated respondent/family/event traversal is the motivation, not a directly attributed time decomposition.

**Hypothesis:** a lawfully qualified per-execution prepared saved session could reuse the exact posting index, row-group offset ranges and exact respondent-family/event reads across many operations, without materializing a full C11 repository, without a new store/engine, and without changing facts. It must retain per-operation query/predicate identity, authority/current/revocation checks, fact/replay construction and all negative guards. It may require a versioned iterator/prepared-view contract in `DirectEstateI03Session` and a lawful call surface in `SavedC11Admission`/`CarrierNeutralResearchExecutor`.

**Why it is worth a bounded measurement:** it is the only option that would address the 80 distinct condition/target cores; A only covers measure variants. It is consistent with the historical V550 per-country prefetch/harmonization reuse target, but it is not a port of old estimator semantics, not permission to merge sources/populations, and not a production choice.

**Owner/files:** #960/W05-P03/#1006 performance owner; the exact semantic I03 evaluator/iterator owner; the S2-C/S2-D reader owner. Files/symbols: `pre553_direct_estate_i03.py::DirectEstateI03Session._build/_selected_events/_respondent_family/indices_for` and any indispensable same-file prepared-read helpers; `pre553_saved_c11_admission.py::execute_i03`; `pre553_carrier_execution.py::CarrierNeutralResearchExecutor.execute_i03`; `_pre553_query_eval.py` only if exact iteration-order/iterator compatibility is required. The `_pre553_query_eval.py` three-sort candidate from #1006 is **not** authorized by a `_respondent_family`-only grant.

**Prerequisites:** the independently accepted #999 native body-truth successor `ce7704253f6a2381310c3eb2c7412a2d85c5596c` (accepted at `c18b7e087d5d5b178ed5acc92f9c82250a1743de`) was created **after this author started** and exists but is **not adopted** in the `9d96a9c…` measurement cut. Any B implementation must adopt/qualify that successor under the owner’s exact current reader/evaluator file/symbol grant. It must not wait for a new #999 acceptance, and it must not assume the old baseline is adversarial-security qualified. No bodytruth edit, guard removal, science/eligibility change, new index/store/engine or protected merge.

**Test falsifiers before any gain claim:** a bounded owner-approved measurement with 100/100 exact cold/native fact+replay+release parity; both existing cold grouped guards either lawfully re-qualified or explicitly preserved; zero full `C11Repository` builds and zero whole-table reads; source-open INAPPLICABLE for the sourcefree fixture; exact missing/zero/UNKNOWN/INAPPLICABLE state handling; current revocation before/after/mid-batch refuses; changed input → changed fact → exact restore; bounded memory/temp/disk; no hidden second body corpus; no fact/replay drift under reused preparation; no unaudited cross-session identity. Without that measurement, B remains `HYPOTHESIS_NOT_MEASURED`.

## C. Demonstrated layout intervention (not supported by this court)

**What would justify it:** a measured, layout-caused bottleneck at the qualified scale (row-group/row ordering, column encoding, compression), with exact parity and an owner-approved physical change.

**What this court found:** the 128-respondent cold cost is dominated by per-operation session/family/event traversal, not by a single proven layout defect. The prior accepted #1006 100k locality experiment (204,125 → 5,784 row-group reads with a runtime respondent-sort experiment) is a different estate/scale and is not re-run or generalized here. A small-estate layout change would not be justified by “the cold path is slower than in-memory.”

**Disposition:** `NOT_DEMONSTRATED_AT_THIS_SCOPE`. C requires a separate measured 100k/large-estate contract and explicit owner approval; do not choose C merely because one path is slow.

## Recommendation (no implementation, no production choice)

1. Preserve all current guards and production behavior.
2. If the owner only needs measure-variant/repeat reuse, A is already lawful on the sealed in-memory path; cold saved A remains unqualified by the exact identity barrier.
3. B is a **hypothesis**, not a measured candidate. If the owner needs hundreds/thousands of distinct operations, authorize a bounded owner-approved B measurement only after adopting the accepted #999 successor and the exact reader/evaluator grant. Do not claim a B gain before that measurement.
4. C is not supported by this court at this scale.

No production grant is issued or inferred. No B implementation is claimed or authorized.
