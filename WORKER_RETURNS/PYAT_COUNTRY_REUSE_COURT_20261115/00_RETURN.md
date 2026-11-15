# PYAT J5 — Per-country many-operation reuse court

**Return status:** `MEASUREMENT_ACCEPT_SCOPED__HANDOFF_CORRECTED__NO_SELF_ACCEPTANCE`
**Grade:** `SOURCEFREE_TEST_ONLY`. The independent review `c5a71fcc59a45aa470720159a334ae57f365de11` reproduced the exact facts/counters and returned `ACCEPT_SCOPED@SOURCEFREE_REUSE_COURT_REPRODUCED` for measurement, with `REVISE_EXACT_DEFECT@G4_OPTIONS_AND_HANDOFF_CLAIMS` for the handoff. This is the corrected documentary handoff; it is **not** production/security/science acceptance and **not** self-acceptance.
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-country-reuse-court-20261115`
**Branch:** `agent/pyat-country-reuse-court-20261115`
**Review/correction base HEAD:** `6cb7866d6ccfcade7a7aaa92cbbd6398a5a672bb` (`git diff 9d96a9c…6cb7866 -- rawlsing_next` empty)
**Frozen measurement production cut:** accepted S2-D `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`
**Accepted writer:** `b7b697b69f0acea12174937ee824c19ac34ac284`
**Runtime:** Python 3.11.3; pyarrow 22.0.0; DuckDB 1.5.2; pyreadstat 1.3.2
**One-pass wall:** author 133.84 s court / 149.43 s total; independent review 161.763 s court / 178.800 s total. Both under the 300 s native benchmark budget; ambient-contended, not clean/stable throughput. No background jobs, no automatic repetitions.

## 1. One-screen result

One deterministic **sourcefree** saved estate: **128 distinct respondents**, 416 events, 640 routing facts, 128 weights, one source/wave/country-shaped universe, 13 complete Parquet families, typed missing B, routed sparse D, repeated MR, A/B/C/D marginals, forward/reverse conditionals and true multi-target joints.

Measured **100 distinct query operations** (80 distinct exact condition/target cores + 20 governed-weighted measure variants):

| | Result |
|---|---:|
| Cold saved ops completed | **100 / 100** author and independent |
| Cold wall | **51.929 s** author one pass; **65.661 s** independent review (ambient; no stable-throughput claim) |
| Cold throughput | **1.926 ops/s** author; **1.523 ops/s** independent |
| Cold per-op p50 / p95 | 0.519 / 0.738 s (author pass; ambient) |
| Cold session builds | 100 |
| Cold row-group reads (metadata-call proxy) | **43,130** (431.3/op) |
| Compressed / uncompressed row bytes (metadata-sum proxy) | **576.8 MB / 2.36 GB** (268× / 1,097× the 2.15 MB estate; not physical I/O/decompression timing) |
| Process-tree RSS inference (`max(before, after, self ru_maxrss)`) | 137.2 MB author (self 136.503 MB; 733,184 B difference); 127.6 MB review (equality in that pass) |
| Cold session `_build` share (instrumentation-inclusive) | 12.3% author / 12.4% review; not a full phase decomposition |
| Cold vs native oracle | **100/100 exact, 0 mismatches** author and review |
| `C11Repository.__init__` / `pq.read_table` | **0 / 0** real tripwires |
| Source opens | **INAPPLICABLE** (sourcefree synthetic fixture; not a measured tripwire) |
| 1,000 distinct cold ops | **NOT_RUN** — linear projection 519.29 s author / 656.61 s review > 300 s (`EXTRAPOLATION_NOT_MEASURED`) |

Existing **in-memory sealed-`C11Repository`** grouped path, same 100 operations:

| | Result |
|---|---:|
| Ungrouped wall | 4.304 s author one pass |
| Grouped `max_groups=256` wall | 4.216 s author (1.021×); independent review 1.199×; ambient, not a clean speed claim |
| Grouped core builds / hits | **80 / 20** |
| Grouped default-64 builds / hits / capacity fallbacks | 64 / 20 / **16** |
| Grouped vs ungrouped / cold parity | **100/100 exact** author and review |
| 1,000-repeat invocation grouped | 15.683 s vs 52.035 s author = **3.32×**; 15.925 s vs 56.238 s review = **3.53×**; 1 build / **999 hits** (not distinct ops) |
| Cold saved grouped | **REFUSED by both public guards**; no grouped positive manufactured |

**Exact cold barrier:** the cold `_DirectReleaseIdentity` lacks `semantic_release_hash` and `source_release_manifest_hash`; `indices_for` returns a **new** `_ReleaseIndex` per call while `_index_identity` includes `id(index)`; `SavedC11Admission.execute_i03` hard-codes `group_scope=None`. The two guards are:

- `CarrierExecutionBindingError("grouped saved I03 scope awaits distinct S2-D qualification")`
- `EmpiricalQueryExecutionError("grouped native I03 cache not yet qualified for cold sourcefree estate")`

The existing grouped scope is a **measure-variant/repeat cache**, not a many-distinct-operation substrate. No guard was removed and no production file was edited.

## 2. G1–G5

| Gate | Return |
|---|---|
| **G1 exact source/owner/test contract** | `G1_SOURCE_CONTRACT.md`: exact current blobs, accepted #1006 harness via `git show`, cold path, grouped path, both guards, missing stable cold index identity, tests, #999 chronology. |
| **G2 actual baseline cost** | `G2_COLD_COST.md`: 100/100 cold ops; 51.929 s author / 65.661 s independent; 43,130 row-group metadata-proxy reads, 576.8 MB / 2.36 GB metadata-sum proxies, 94,068 family rows, 29,343 event objects, 1.70 MB temp, exact native parity; RSS/proxy qualifiers. |
| **G3 qualified grouped parity OR precise barrier** | `G3_GROUPED_OR_BARRIER.md`: in-memory grouped parity 100/100 with 80 builds + 20 hits; cold saved grouped **REFUSED**; exact identity/stable-index barrier; 1,000 repeat is 3.32× author / 3.53× review but not distinct-operation evidence. |
| **G4 smallest A/B/C separately approved** | `G4_OPTIONS.md`: A existing grouping is narrow (measure variants only); B bounded prepared-session/iterator repair is a **source-grounded unmeasured hypothesis**, not a measured candidate, and requires a bounded owner-approved measurement; C layout intervention not demonstrated at this scale. No implementation; no production choice qualified. |
| **G5 distinct review** | independent review `c5a71fcc…` measurement `ACCEPT_SCOPED`, handoff `REVISE_EXACT_DEFECT`; corrected handoff in this return; distinct recheck of the correction remains, no self-acceptance. |

## 3. Scientific/state preservation

- **B marginal:** 128 denominator; cells `0`=61, `1`=59, exact typed `MISSING`=8; saved = native exact (`evidence/state_probe.json`).
- **D marginal:** 12 eligible; cells `0`=7, `1`=5; saved = native exact.
- **MR repeated:** denominator 5; 10 ordered occurrence cells, including `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`; saved = native exact.
- **Impossible `A=1 AND A=0 → C`:** `ZERO_SUPPORT`, denominator 0, both cells `ZERO_SUPPORT`; saved = native exact.
- Across the 100 ops: 287 `OBSERVED_POSITIVE` and 93 `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET` cells; all 100 operations `SUPPORTED`; raw denominators 2–128 (p50 21), weighted denominators 30–320.
- Focused existing tests: **16 passed** author and independent (`test_pre553_i03_grouping.py` + cold grouped-refusal test), including special states, zero support, poisoned memo, authority deny, capacity and cleanup.
- `UNKNOWN`/`INAPPLICABLE` routing were not generated by the accepted #1006 fixture; the production special-state tests exercise that matrix and passed. No state was collapsed into zero.

## 4. Exact write and authority boundary

- Only `WORKER_RETURNS/PYAT_COUNTRY_REUSE_COURT_20261115/` and disposable `.local-data/` scratch were written.
- Production and accepted tests READONLY. No guard removal, no native/bodytruth edit, no 3-sort production patch, no new index/store, no full-object-first reopen/engine, no science/eligibility change, no source rights, no original35, no governed QUERY issuance (J3 remains separate), no protected merge.
- **#999 chronology:** the native repair `ce7704253f6a2381310c3eb2c7412a2d85c5596c`, independently accepted at `c18b7e087d5d5b178ed5acc92f9c82250a1743de`, was created after this author started and is **not adopted** in the `9d96a9c…` measurement cut. The old baseline is a valid-fixture benchmark only, not adversarial security qualification of the accepted successor. Any J1/B production work must adopt/qualify the accepted successor under the owner’s exact reader/evaluator/file grant; it must not wait for a new #999 acceptance.
- The 100 queries are TEST_ONLY sourcefree operations; they do not masquerade as original governed issuance.
- Prior #1006 100k/10k locality results are cited only as prior evidence; no 100k/10k A/B, writer profile, or #1035/#1036 review was rerun.

## 5. Evidence index

| File | Purpose |
|---|---|
| `G1_SOURCE_CONTRACT.md` | source/blobs/guards/identity barrier |
| `G2_COLD_COST.md` | cold 1/100 cost, counters, parity, forecast |
| `G3_GROUPED_OR_BARRIER.md` | grouped parity and exact cold barrier |
| `G4_OPTIONS.md` | A/B/C handoff, no implementation |
| `G5_REVIEW_PENDING.md` | independent G5 received; corrected handoff and recheck status (legacy filename retained) |
| `CORRECTION_MAP.md` | defect/qualifier → exact changed cells/paragraphs; frozen raw data ↔ corrected interpretation |
| `SELF_CRITIQUE.md` | limitations, proxy qualifiers and negative guards |
| `RUNBOOK.md` | exact commands and reproduction |
| `evidence/preflight.json` | runtime, load, process/CPU contention |
| `evidence/estate_receipt.json` | 128-respondent estate, I02/manifest/member SHAs |
| `evidence/ops_manifest.json` | 100 exact query refs, 80 cores, 20 measure variants |
| `evidence/cold_1op.json` | one cold operation counters |
| `evidence/cold_100ops.json` | 100 distinct cold operations, per-op records |
| `evidence/guard_probe.json` | both guard refusals + missing identity contract |
| `evidence/parity.json` | cold/native/grouped exact parity 100/100 |
| `evidence/state_probe.json` | missing/sparse/repeated/zero-support probes |
| `evidence/repeat_1000_grouped.json` | 1,000 repeat invocations (not distinct ops) |
| `evidence/summary_derived.json` | compact derived metrics |
| `evidence/commands.json` | exact commands, exit codes, logs |
| `logs/` | stdout/stderr for each command |
| `probe/` | test-only probes, accepted fixture sources, instrumentation |

## 6. Self-critical summary

This is a **100-operation** court, not a 1,000-operation completion. It is synthetic/sourcefree, not original35. The author's 51.929 s and the independent review's 65.661 s are two ambient-contended passes with identical facts/counters; no clean or stable throughput is claimed. Read counts and byte sums are metadata proxies, not physical I/O/decompression timing; the `_build` share is instrumentation-inclusive; object materialization counts are native work, not tripwires; process-tree RSS is an inference, not a sampled high-water. The in-memory grouped path is not a cold saved consumer; no cold grouped positive exists. B is a source-grounded hypothesis, not a measured implementation or production choice; a bounded owner-approved measurement is required before any gain claim. The 20 weighted variants are distinct estimands but only 20/100 share a core; the 80 distinct cores do not. `UNKNOWN`/`INAPPLICABLE` states were not generated on the saved estate; the production special-state tests covered them. No changed/restore was run on this 128 estate; exact parity and the accepted #1006 harness rest/change evidence are separate. The independent G5 accepted the measurement scope and rejected the earlier handoff claims; this correction is not self-accepted. These are deliberate limits, not hidden passes. See `SELF_CRITIQUE.md`.

**Next action:** distinct recheck of this corrected handoff; then, if the owner needs distinct-operation reuse, adopt the accepted #999 successor `ce770425…`/`c18b7e08…` under the exact reader/evaluator/file grant and authorize a bounded B measurement. No production patch, guard removal, new engine/layout choice or B gain is authorized by this return. Stop finite correction.
