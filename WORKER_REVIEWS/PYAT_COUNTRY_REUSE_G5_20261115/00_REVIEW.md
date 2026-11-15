# PYAT J5 — Independent G5 receiving review

**Review verdict:**
`REVISE_EXACT_DEFECT@G4_OPTIONS_AND_HANDOFF_CLAIMS`
**Measurement-scope disposition:**
`ACCEPT_SCOPED@SOURCEFREE_REUSE_COURT_REPRODUCED`
**Production / security / science acceptance:** none.
**G5 status:** distinct nonauthor review completed; no self-acceptance; no production edit.

**Review worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-country-reuse-g5-20261115`
**Review branch / HEAD:** `review/pyat-country-reuse-g5-20261115` / `6cb7866d6ccfcade7a7aaa92cbbd6398a5a672bb`
**Candidate:** `WORKER_RETURNS/PYAT_COUNTRY_REUSE_COURT_20261115` (46 hashed payloads; draft PR #1064)
**Immutable measured evidence:** `f7a7652258907129988504e53fae286da1dbf45d`
**Production cut:** accepted S2-D `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969` (unchanged in this worktree; `git diff 9d96a9c…HEAD -- rawlsing_next` is empty)
**Prior locality experiment:** `3e0ed0794498506520ae62c997a5c852ac672061` — separate; not rerun, not re-reviewed.
**#999 native repair:** `ce7704253f6a2381310c3eb2c7412a2d85c5596c`, independently accepted at `c18b7e087d5d5b178ed5acc92f9c82250a1743de`; exists in this repository object store, **not adopted** in this court. The benchmark below is therefore a valid-fixture benchmark only, not adversarial security qualification of the old `9d96a9c…` baseline.

---

## 1. One-screen result

The author's bounded measurement court is **independently reproducible**. With the author's probe copied byte-for-byte and only the disposable output root changed, the review run at `/usr/local/bin/python3` produced:

- **100/100** distinct cold query operations completed; **100/100** per-operation fact SHA-256 values, query refs, core ids, denominators and cell-state counts identical to the author.
- **80** exact condition/target cores + **20** governed-weighted measure variants; **100** unique query content hashes; **60** cores used once, **20** cores used by a raw + weighted pair; **0** duplicate raw `(condition AST, targets)` pairs.
- **43,130** row-group reads, **690,080** row-group rows, **576,774,322** compressed-byte metadata sum, **2,363,218,327** uncompressed-byte metadata sum, **94,068** family rows/objects, **29,343** event objects — all identical to the author.
- **100/100** exact cold-vs-native, grouped-256-vs-native, grouped-64-vs-native and grouped-256-vs-cold canonical fact parity.
- **Both public cold grouped guards refused** with the exact source messages; the cold `_DirectReleaseIdentity` still lacks `semantic_release_hash` and `source_release_manifest_hash`; two `indices_for` calls still return different index objects.
- In-memory grouped receipts: **80 builds + 20 hits** at `max_groups=256`; **64 builds + 20 hits + 16 capacity fallbacks** at default 64.
- **1,000-repeat invocation** probe: **1 build + 999 hits**, explicitly `REPEAT_INVOCATIONS_NOT_DISTINCT_OPERATIONS`.
- State probe: typed MISSING B (128 denominator), sparse D (12), repeated MR (5), impossible `A=1 AND A=0 → C` ZERO_SUPPORT (0); saved = native exact in all four.
- Focused existing tests: **16 passed**.

The review run was one sequential pass, exit **0**, total **178.800 s** (preflight 0.242 s; estate build 4.158 s; court 161.763 s; state probe 3.925 s; summary 0.061 s; focused tests 8.644 s). The cold 100-op batch was **65.661 s** in this pass versus the author's **51.929 s**; counters and facts are identical, wall/RSS/CPU are ambient. The native wall budget was not exceeded by the review pass; no 1,000-distinct cold run was attempted (projection 656.61 s at the review wall, over 300 s).

The **measurement** is accepted at the sourcefree test-only scope. The **handoff document is not accepted as written**: G4/00_RETURN call B a “measured candidate” although B has no implementation or run, and the handoff still describes #999 as pending when an independently accepted successor exists but is not adopted. The cold wall “stable at ~51.9–52.2 s” and the unfrozen “three passes” sentence are also not supported by frozen commands. These are claim/provenance defects, not a defect in the reproduced fact/counter/barrier evidence.

---

## 2. Custody and exact source contract

### 2.1 Verified production blobs at review HEAD

`git hash-object` at review HEAD `6cb7866d6`:

| File | Blob |
|---|---|
| `rawlsing_next/pre553_empirical_query.py` | `8885e637eb176946c8496671ff49ee70665b3bc6` |
| `rawlsing_next/_pre553_query_eval.py` | `9808a6b72c716e26ebce5cbd76ef5ef6f3b5c920` |
| `rawlsing_next/pre553_direct_estate_i03.py` | `8b4d5ca2c865e4ef5f5fb609cce15ca3ba64899e` |
| `rawlsing_next/pre553_saved_c11_admission.py` | `22749addc1fca5f0b90e12728847c390aafa7a84` |
| `rawlsing_next/pre553_carrier_execution.py` | `ad1164f21f5f7422a03a19b1b856636edb89cb03` |
| `rawlsing_next/pre553_source_direct_parquet_estate.py` | `0e4b34ce4973bb4d23b6105faea55b9056ecf373` |
| `rawlsing_next/pre553_empirical_objects.py` | `a61365b994e5c3c50de0f598fcf40e90abf757b6` |
| `rawlsing_next/pre553_c11_repository.py` | `c0cd4e835ceb8fe6c6025ebeb89e32223427f955` |
| `rawlsing_next/tests/test_pre553_i03_grouping.py` | `78683c4098f388eb72d686651b3282b9162e2ed2` |
| `rawlsing_next/tests/test_pre553_direct_estate_i03.py` | `970996b889e841d7e283b59ca245e9cac7594a55` |

These match G1. Production and accepted tests were read-only in this review.

### 2.2 Publication/evidence immutability

`git diff --name-status f7a7652258907129988504e53fae286da1dbf45d 6cb7866d6` is exactly:

```text
M WORKER_RETURNS/PYAT_COUNTRY_REUSE_COURT_20261115/G5_REVIEW_PENDING.md
M WORKER_RETURNS/PYAT_COUNTRY_REUSE_COURT_20261115/MANIFEST.json
```

All measured `evidence/`, `logs/` and `probe/` payloads are unchanged after `f7a765…`. The frozen 46-file manifest was independently verified: **46/46 entries match both byte counts and SHA-256**, with only `MANIFEST.json` itself unlisted.

### 2.3 Probe-source identity

The three accepted #1006 sources extracted into `probe/` are byte-identical to the accepted #1006 commit `2beb2b894076510cdedf8981aa73d15eafc7c816`:

| Probe | Blob |
|---|---|
| `fixture_1006.py` | `1487ad233c871d973b2a64c9649c37f100c46832` |
| `query_1006.py` | `5a15272043246e5293a51e2390adc038bd280e47` |
| `instrument_1006.py` | `a7559deaef5fd9dc9ee6c4d3dc03466c1c971f48` |

`diff -r` between the author `probe/` and the review `probe/` copy is clean. The only review-side change is the output root: the copy is placed under `WORKER_REVIEWS/PYAT_COUNTRY_REUSE_G5_20261115/probe/`, so `BASE` resolves to the review root and `REPO` remains the worktree. No probe semantics, fixture, tag, operation battery, instrumentation or test command was changed. A review `.gitignore` was added for `/.local-data/` and `__pycache__/`; it is not part of the probe.

### 2.4 Guard source verified directly

- `pre553_carrier_execution.py:464-466` raises `CarrierExecutionBindingError("grouped saved I03 scope awaits distinct S2-D qualification")` for `type(repository) is VerifiedDirectEstate` with a non-None `group_scope`.
- `pre553_empirical_query.py:756-757` raises `EmpiricalQueryExecutionError("grouped native I03 cache not yet qualified for cold sourcefree estate")` for `type(repository) is DirectEstateI03Session` with `group_scope is not None`.
- `pre553_saved_c11_admission.py:440` hard-codes `group_scope=None`.
- `pre553_direct_estate_i03.py:401-414` constructs a new `_ReleaseIndex` with `_DirectReleaseIdentity(release_ref, replay_manifest)` on each `indices_for` call; `pre553_empirical_query.py:562-582` `_index_identity` requires `release.semantic_release_hash`, `release.source_release_manifest_hash` and includes `id(index)`.

The review guard probe reproduced all of this; no guard was removed, monkeypatched away or bypassed.

---

## 3. Independent reproduction — exact commands, codes and outputs

### 3.1 Command

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-country-reuse-g5-20261115
PYTHONDONTWRITEBYTECODE=1 /usr/local/bin/python3 \
  WORKER_REVIEWS/PYAT_COUNTRY_REUSE_G5_20261115/probe/run_all.py
```

Exit code: **0**. Full stdout/stderr: `review_run_all.stdout.log`, `review_run_all.stderr.log`; per-step commands, argv, cwd, exit codes and stdout/stderr tails: `evidence/commands.json`; per-step logs: `logs/`.

| Step | Exit | Wall (review) |
|---|---:|---:|
| preflight | 0 | 0.242 s |
| build_estate | 0 | 4.158 s |
| run_court | 0 | 161.763 s |
| state_probe | 0 | 3.925 s |
| summarize | 0 | 0.061 s |
| focused_existing_tests | 0 | 8.644 s |
| **total `run_all`** | **0** | **178.800 s** |

All six `commands[*].exit_code` are 0; `all_exit_zero=true`. The review `run_court` wall is 161.763 s, under the 300 s native budget. It includes the cold 100-op batch (65.661 s), guard probe, native oracle and grouped passes, and the 1,000-repeat probe.

### 3.2 Author vs review — identity and counter comparison

| Item | Author `f7a765…` | Review | Match |
|---|---|---|---:|
| Estate manifest SHA-256 | `22640e2dca76011a3abb27ba4e97a174bf101a8814cb0691a16dd77d1e7e1fc0` | same | yes |
| Reconstructed release | `92db570ab1d722fb56d4eb2084b3ca20c3875f622dbdc5b9c0837f812b786310` | same | yes |
| 15 member SHA-256 map | exact | exact | yes |
| Family counts / retained bytes | 13 families / 2,153,366 B | same | yes |
| `ops_manifest.json` SHA-256 | `86972dcee412aed40541830b1a2551e27dfd8cf36cc094e9b35762ff80f05f0f` | same | yes |
| Distinct ops / cores / weighted | 100 / 80 / 20 | 100 / 80 / 20 | yes |
| Unique query content hashes | 100 | 100 | yes |
| Cold 1-op wall | 0.549 s | 0.499 s | ambient |
| Cold 1-op counters | 426 reads; 5,721,849 / 23,326,183 B; 513 event / 640 family objects | identical | yes |
| Cold 100 wall | 51.929 s | 65.661 s | ambient |
| Cold 100 row-group reads / rows | 43,130 / 690,080 | identical | yes |
| Cold 100 compressed / uncompressed | 576,774,322 / 2,363,218,327 B | identical | yes |
| Family rows / objects; event objects | 94,068 / 94,068; 29,343 | identical | yes |
| Session builds / opens | 100 / 100 | 100 / 100 | yes |
| Session `_build` / enter | 6.380 / 8.138 s | 8.168 / 10.979 s | ambient |
| `_build` share of cold wall | 12.29% | 12.44% | stable ratio |
| SQLite temp peak | 1,703,936 B | 1,703,936 B | yes |
| Retained / scratch after | 2,153,366 / 2,153,366 B | same | yes |
| C11Repository tripwire | 0 | 0 | yes |
| Whole-table `read_table` | 0 | 0 | yes |
| Per-op fact SHA-256 | 100 exact | 100 exact | yes |
| Cold vs native ungrouped | 100/100 | 100/100 | yes |
| Grouped-256 vs native | 100/100 | 100/100 | yes |
| Grouped-64 vs native | 100/100 | 100/100 | yes |
| Grouped-256 vs cold | 100/100 | 100/100 | yes |
| Grouped-256 receipt | 80 builds / 20 hits / 0 fallback | same | yes |
| Grouped-64 receipt | 64 builds / 20 hits / 16 fallback | same | yes |
| Cold grouped guards | both REFUSED | both REFUSED | yes |
| Cold index fields | `release_ref`, `replay_manifest`; missing both hashes; `same_index=false` | same | yes |
| Repeat-1000 receipt | 1 build / 999 hits | same | yes |
| Repeat walls ungrouped / grouped | 52.035 / 15.683 s | 56.238 / 15.925 s | ambient |
| State probe saved facts | exact | exact | yes |
| Focused tests | 16 passed | 16 passed | yes |

The review `state_probe.json` and `parity.json` are byte-identical to the author's frozen files. The review `ops_manifest.json` is byte-identical. `cold_100ops.json`, `guard_probe.json`, `estate_receipt.json`, `measurements.json` and `summary_derived.json` differ only where paths, timestamps, wall times, RSS samples or process index ids necessarily differ; every fact/counter/guard-field relevant to the court matches.

### 3.3 Review resource/contention snapshot

- Preflight: 16 CPUs, load `2.10 / 2.76 / 2.82`, **0** other Rawlsing processes, Python 3.11.3, pyarrow 22.0.0, DuckDB 1.5.2, pyreadstat 1.3.2, NumPy 2.3.2, pandas 2.3.1.
- Cold 100: CPU user 58.758 s / system 7.262 s; process-tree sample before 81,010,688 B, after 109,903,872 B, derived “peak” 127,598,592 B; self `ru_maxrss` 127,598,592 B.
- The review wall is **27% higher** than the author's cold wall and **20% higher** than the author's run_court wall under a *lower* preflight load. The counters/facts are stable; the wall is ambient- and host-sensitive. This is a direct counterexample to the claim that the cold wall was “stable at ~51.9–52.2 s”.

---

## 4. G1–G5 source-scoped dispositions

### G1 — source/owner/test contract: **ACCEPT_SCOPED**

The exact production blobs, cold chain, grouped path, two guard messages, `_DirectReleaseIdentity` fields, transient `_ReleaseIndex` identity, `group_scope=None`, accepted #1006 probe sources and 16-test focused command all verify. No production/test edit or guard bypass. `C11Repository` and whole-table `read_table` are real tripwires; source-open is not a tripwire (see §5).

### G2 — cold cost: **ACCEPT_SCOPED with proxy qualifiers**

100/100 distinct cold operations, 43,130 row-group reads, 94,068 family rows, 29,343 event objects, exact parity, zero full-repository/whole-table hits, and a `_build` share around 12.3–12.4% are reproduced. The author's 51.929 s is one contended pass, not a stable performance constant. Row-group counts and compressed/uncompressed byte sums are metadata-call/sum proxies, not physical I/O or decompression measurements; this is correctly stated in `SELF_CRITIQUE.md` item 7 but should be carried into the headline. Process-tree “peak” is an inference (see §5). The 1,000-distinct cold operation result is correctly **NOT_RUN**; the review projection is 656.61 s, still over 300 s.

### G3 — grouped parity / exact barrier: **ACCEPT_SCOPED**

In-memory grouped parity 100/100 and receipts 80/20 and 64/20/16 are reproduced. The 1,000-repeat probe is 1 build + 999 hits and is explicitly not distinct operations. Both public cold grouped guards refuse; no cold grouped positive was manufactured. The missing stable exact cold release/index identity is source-verified. The hot full-`C11Repository` oracle is not cold grouping qualification, and the return says so.

### G4 — options: **REVISE_EXACT_DEFECT (document/claim only)**

A is narrow existing measure-variant/repeat reuse; the cold saved A scope remains refused. C is not demonstrated at this scale, and no physical-layout necessity follows from the slow current route — correct. B is a **source-grounded hypothesis**, not a measured optimization. The return calls B “the only measured candidate” / “the smallest measured candidate” while also stating “No implementation is performed or authorized.” There is no B code path, no prepared-session/iterator implementation, and no B A/B run in the frozen evidence. The only measured quantity is the cold cost target used to motivate B. The handoff must relabel B accordingly and require a bounded owner-approved implementation/measurement; it must not present B as performance-qualified. This is the material G4 defect.

### G5 — this review: **COMPLETED, distinct nonauthor**

The measurement is independently reproduced and accepted at the sourcefree test-only scope. The handoff is not accepted as written because of the G4 claim and the stale #999/wall/evidence context below. No production, security, science, original35, J3 or optimized-engine acceptance follows.

---

## 5. Material corrections versus proxy/wording qualifiers

### Material corrections

1. **B is mislabeled as measured.** Exact counterexample:
   - `G4_OPTIONS.md:19` — “**B. Bounded iterator / prepared-session repair (the only measured candidate for distinct-operation reuse)**”.
   - `G4_OPTIONS.md:31` — “No implementation is performed or authorized by this return.”
   - `G4_OPTIONS.md:45` — “B is the smallest measured candidate”.
   - `00_RETURN.md:59` — “B bounded prepared-session/iterator repair is the only measured candidate for distinct ops”.
   There is no B implementation/run in `evidence/` or `probe/`. Required correction: label B a source-grounded, unmeasured hypothesis; state that the cost target is measured but the repair is not; require a separate bounded owner-approved measurement. Do not choose B as if already qualified.
2. **#999 handoff context is stale.** The candidate says the #999 successor is still pending / required (`G1_SOURCE_CONTRACT.md` §7; `00_RETURN.md` §4; `PROGRAMMA_DELTA.md` open obligation 3). The receiving record supplies the native repair `ce7704253f6a2381310c3eb2c7412a2d85c5596c`, independently accepted at `c18b7e087d5d5b178ed5acc92f9c82250a1743de`, created after the author started and **not adopted here**. `git diff 9d96a9c…HEAD -- rawlsing_next` is empty. Required correction: record that the accepted successor exists but is not adopted; the old `9d96a9c…` baseline is a valid-fixture benchmark only, not adversarial security qualification; any J1/B production work must adopt/qualify the accepted successor under the exact reader/evaluator/file grant. This changes the finite owner action from “obtain #999 acceptance” to “adopt the accepted successor + grant”.
3. **Cold wall stability / “three passes” are not frozen evidence.** The candidate's frozen `commands.json` contains **one** `run_court` pass (cold 51.929 s; grouped 1.021×). `SELF_CRITIQUE.md` item 5 says “The cold 100-op wall was stable at ~51.9–52.2 s”; `G3` says “three same-command passes observed roughly 1.02×–1.26×”. The review's independent pass measured **65.661 s** cold and **1.199×** grouped (receipts identical) under load 2.10/2.76/2.82. The stability/three-pass sentences are unfrozen author observations and are contradicted by a runnable independent pass. Required correction: report 51.929 s as one contended pass; report the independent 65.661 s/1.199× range; retain the exact counters/facts as the strong evidence; do not state a narrow stable wall range. The 1000-distinct projection remains over 300 s under both walls (519.29 s author basis; 656.61 s review basis).

### Proxy / wording qualifiers (not material measurement defects)

1. **Source-open “tripwire” is INAPPLICABLE, not a measured zero.** The actual tripwires are `C11Repository.__init__` (0) and `pq.read_table` (0). The fixture is synthetic/sourcefree, so there is no original source file to open; the cold path reads the saved Parquet estate. `00_RETURN.md`'s “C11Repository / whole-table / source opens 0 / 0 / 0 tripwires” conflates two real tripwires with an inapplicable source-open state. `G2_COLD_COST.md` already parenthesizes “synthetic in-process fixture”; `SELF_CRITIQUE.md` item 14 only claims the two real tripwires. Correct the headline table to “C11Repository 0 / read_table 0 (tripwires); source-open INAPPLICABLE (sourcefree)”.
2. **Process-tree RSS “peak” is a sample/inference, not a tree high-water.** `run_court.py` sets `process_tree_rss_peak_bytes = max(before_tree, after_tree, self maxrss)`. It is not a sampled process-tree high-water; the process is effectively single-process, so `ru_maxrss` is the true process high-water. The author's evidence has tree sample 137,236,480 B vs self maxrss 136,503,296 B; `SELF_CRITIQUE.md` item 8's statement that the peak “equals the self max RSS” is therefore false by 733,184 B in the author's own data. The review run had equality (127,598,592 B). Correct the label/qualifier; do not treat it as a precise process-tree high-water.
3. **Row-group reads/bytes are metadata proxies.** `read_row_group` call counts and column-chunk metadata sums are not physical I/O counts or decompression timings; page cache and filesystem behavior are not instrumented. `SELF_CRITIQUE.md` item 7 says this correctly. The 00_RETURN/G2 headline should carry the same qualifier next to 576.8 MB/2.36 GB and 43,130 reads.
4. **`_build` share is instrumentation-inclusive and not a full time decomposition.** The 12.3–12.4% `_build` share is a wrapper-timed ratio including instrumentation overhead; the “dominant repeated work is traversal/selected-event materialization” conclusion is inferred from 43,130 reads/94,068 family rows/29,343 event objects, not from a direct per-phase time attribution. This is acceptable as a proxy, but should not be stated as a measured time decomposition.
5. **Object materialization counters are not tripwires.** The 94,068 family and 29,343 event `_object_from_row` calls are actual native evaluation materializations, not a “full-object-first reopen” tripwire. The `C11Repository` tripwire is the full-repository guard; the cold path still materializes row-level family/event objects as expected. The return should not imply the object counters are negative tripwires.
6. **Grouped in-memory wall is contended.** The review 1.199× grouped wall difference vs the author's 1.021× (receipts identical) is another ambient-contention observation; do not promote it to a clean speed claim. This supports, rather than contradicts, the author's conservative “not a clean performance claim” framing.

---

## 6. What was actually exercised — and what was not

**Exercised in this review (actual states):**

- 100 distinct query refs: 80 raw distinct condition/target cores + 20 governed-weighted measure variants; 20 raw/weighted core pairs; 100 unique query content hashes; 80 unique raw `(AST, targets)` pairs; no duplicate query.
- Cold saved execution through `SavedC11Admission.execute_i03` with `group_scope=None`; 100 new `DirectEstateI03Session` builds; no full `C11Repository`; no `pq.read_table`.
- In-memory grouped execution on the sealed `C11Repository`: 80/20 at 256; 64/20/16 at 64; exact parity.
- Both public cold grouped guards: actual refusals, exact messages, zero grouped core builds.
- 1,000 repeat invocations of `marginal_A` on the in-memory grouped path: 1 build/999 hits; explicitly not distinct.
- State probe: `MISSING` B (8 typed missing), sparse D (12 eligible), repeated MR (5 denominator/10 ordered cells), impossible `A=1 AND A=0 → C` ZERO_SUPPORT; saved = native exact.
- 16 existing production tests, including exact parity/share, capacity, special states/zero support, poisoned memo, authority deny, release separation/cleanup, warm hit/capacity, and cold grouped refusal.

**Not exercised / not claimed:**

- No 1,000-distinct cold operation run. 100 is measured; 1,000 is an extrapolation over 300 s (author 519.29 s; review 656.61 s).
- No changed/restore run on this 128-respondent estate. The candidate does not claim one and this review does not borrow prior #1006 changed/restore execution.
- `UNKNOWN` / `INAPPLICABLE` routing states were not generated by this saved estate; the production special-state tests exercise that matrix, and the return says so. They are not claimed as saved-estate observations here.
- No cold grouped positive, no guard removal, no grouped cold qualification, no new index/store/engine, no full-object-first reopen, no source reopen.
- No original35, governed QUERY issuer eligibility, J3 issuance, science/eligibility change, protected merge, #998 integration or #1007 rights. The 100 queries are TEST_ONLY sourcefree fixture operations, not original governed issuance.
- No #999 repair adoption or adversarial security qualification of the old baseline. The accepted successor `c18b7e…` exists but is not in this worktree's production cut.
- No 10k/100k or old whole-matrix rerun; prior #1006 locality evidence is cited only as external context.

---

## 7. Evidence index and hashes (review root)

All review output is under `WORKER_REVIEWS/PYAT_COUNTRY_REUSE_G5_20261115/`; `.local-data/` is ignored bounded scratch (2.1 MB). Full review manifest: `REVIEW_MANIFEST.json`.

| Review artifact | Purpose |
|---|---|
| `00_REVIEW.md` | this frozen G5 review |
| `REVIEW_MANIFEST.json` | review file hashes, source cut, command/exit/verdict |
| `probe/` | byte-identical author probe copy (12 files) |
| `evidence/commands.json` | review commands, argv, exit codes, walls, log tails |
| `evidence/cold_1op.json` | review cold 1-op counters/fact |
| `evidence/cold_100ops.json` | review 100 cold ops, per-op facts/counters |
| `evidence/guard_probe.json` | review both guard refusals + missing identity |
| `evidence/parity.json` | review exact parity (byte-identical to author) |
| `evidence/state_probe.json` | review state probe (byte-identical to author) |
| `evidence/repeat_1000_grouped.json` | review repeat receipt/walls |
| `evidence/estate_receipt.json` | review estate members/hashes (root path differs only) |
| `evidence/ops_manifest.json` | byte-identical 100-op manifest |
| `evidence/measurements.json` | review court summary |
| `evidence/summary_derived.json` | review derived metrics |
| `evidence/preflight.json` | review host/load/runtime snapshot |
| `logs/` | per-step stdout/stderr |
| `review_run_all.stdout.log` / `.stderr.log` | review one-pass driver output |

Key review hashes:

```text
ops_manifest.json      86972dcee412aed40541830b1a2551e27dfd8cf36cc094e9b35762ff80f05f0f
parity.json            79d7a2e07059968393021d54291fb5322e3671fd9878b930800833575ea8afe8
state_probe.json       336bbd4d48b1f70343e61845c6f6cce93292bd0bc3f1aa878b8d90da2f98d965
cold_100ops.json       3b7e53e4061ec5121917c70b300abaae73f9fcb48d8ed4ca43c54bc83f8f656c
cold_1op.json          8f61f5b8b26628ff9acf6cae1e86e0278e64b3c119096b055d0dae32f3f0dbce
guard_probe.json       b83832c567be6e7dcd5e9b7a31660f65cc1e3f2b46fddfab5fbfde9bd1793e01
measurements.json      f2500afb454217c6fb24e54c1ee00ea347f49b3acf11ca9738726aee68281545
summary_derived.json   316f43d7f70802554e41b5250d085ee75d258ec11701026504c6f06f744c0ea4
estate_receipt.json    cc9b3bb723dad7b586bfb7953443f204fb616df775086d01cd00195b7c2cd7fa
```

The review `ops_manifest.json`, `parity.json` and `state_probe.json` are byte-identical to the author's frozen files. The review `estate_receipt.json` differs only in the review scratch root path; its 15 member hashes, manifest SHA, release ref, family counts and retained bytes are identical.

---

## 8. Finite remaining owner action

1. **Correct the return claims** (document-only, no production edit): relabel B as a source-grounded hypothesis, not a measured candidate; update the #999 context to the accepted-but-not-adopted successor; replace the stable-wall/three-pass sentences with the frozen one-pass plus the independent review spread; correct the source-open/RSS/tripwire qualifiers in the headline tables.
2. **Owner decision among A/B/C remains.** A is narrow measure-variant/repeat reuse; cold saved A remains refused by both public guards. C is not demonstrated at this scale; the slow cold route does not by itself establish a physical-layout necessity. B, if chosen, requires a separate bounded owner-approved implementation and measurement.
3. **If B proceeds:** adopt/qualify the independently accepted #999 successor `c18b7e087d5d5b178ed5acc92f9c82250a1743de` (the old `9d96a9c…` baseline lacks `ce770425…`) and obtain the exact reader/evaluator/file/symbol grant. Preserve exact root/source/respondent/occurrence/authority/query identity/current/replay, both cold grouped guards, per-operation fact/replay construction, no full-object-first reopen, no source reopen, no new store/engine. Add changed/restore and mid-batch revocation to the future B court; do not borrow prior #1006 execution.
4. **J3 remains a separate obligation.** The sourcefree fixture queries here are not governed QUERY issuer eligibility. No original35, science, source-rights or protected-merge authority is created.
5. **No new architecture campaign.** The finite correction is document/claim scope plus, only if the owner chooses B, a bounded implementation/measurement under the exact grants.

---

## 9. Self-critique

- This review is **one independent pass**, not a clean performance laboratory. The review cold wall (65.661 s) is 27% above the author's (51.929 s) under a lower preflight load; the host was under visible disk pressure and ambient I/O. I treat wall/CPU/RSS as contended proxies and the exact counters/facts/guards as the strong evidence.
- I did **not** run 1,000 distinct cold operations; the measured 100-op wall projects over the 300 s budget in both passes. I did not run 10k/100k or the old matrix.
- I did **not** independently execute the accepted #999 successor `c18b7e…` or the repair `ce770425…`; I verified the commits exist and that they are not in this worktree's production cut. The review does not qualify the old baseline for adversarial/security use.
- I did **not** run changed/restore on the 128 estate; the candidate does not claim it. I did not generate `UNKNOWN`/`INAPPLICABLE` states on the saved estate; the 16 production tests cover that matrix, not this saved estate.
- I used the author's probe **unchanged**; only the output root and review `.gitignore` differ. I did not modify production, accepted tests, the author's frozen evidence or the candidate return.
- The review's own `df` observation (host free space fell to ~285 MiB) is not attributable to the 2.1 MB review scratch; no large recent file was found under the approved temp path. I did not run further heavy commands after observing it. Treat host disk headroom as an environment risk, not a candidate measurement.
- I did not use subagents, install packages, change providers/models/accounts or launch a new architecture campaign. The review is source-scoped and finite.

---

## 10. Frozen review statement

`REVISE_EXACT_DEFECT@G4_OPTIONS_AND_HANDOFF_CLAIMS` with `ACCEPT_SCOPED@SOURCEFREE_REUSE_COURT_REPRODUCED`.

The author's **measured court** is accepted at the sourcefree test-only scope: 100/100 distinct operations, 80/20 cores/variants, exact cold/native/grouped parity, both cold grouped guards refused, 43,130 row-group reads, 94,068 family rows, 29,343 event objects, 12.3–12.4% `_build` share, 1 build/999 hits repeat probe, and the state probe. The **handoff is not accepted as written** because B is presented as a measured candidate though only its cost target is measured, the #999 successor context is stale, and the cold wall stability/three-pass claims are not in the frozen commands and are contradicted by the review's 65.661 s pass. These corrections are document/claim-level and finite; no production correction, guard removal, optimized engine, original35/security/J3 acceptance or protected merge follows.

**STOP after this finite review.**
