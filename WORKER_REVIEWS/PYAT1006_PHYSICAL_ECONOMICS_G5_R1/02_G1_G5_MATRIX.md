# Original G1–G5 matrix — independent #1006 review

| Point | Original requirement | Independent result | Disposition |
|---|---|---|---|
| G1 | Universal exact source→projection→external I02→13-family Parquet→identity/selector/replay→native cold query contract; enumerate retained physical files and bytes; 1k/10k/50k/100k shapes; source-read counters | 13 families + locator + manifest at 1k/10k/100k; family counts equal manifest; 100k = 100,000 distinct respondents, 324,477 events, 1,448,965 rows incl. locator, 2,841 row groups; retained 310,178,695 B; no second body corpus; source opens 0 on saved path; whole-table/full-graph tripwires pass | ACCEPTED at sourcefree measured scope; true source decode remains #997 |
| G2 | Execute accepted S2-C writer + cold fresh S2-D/I03/I05/Batch on same release; repeated selected, reverse F2, genuine same-respondent F4 3+, complex Batch; stage/query timings; 13-family/identity parity, changed/restore | 100k writer 2,943.177 s; 100k selected 543.026 s; 10k selected/F2/F4 54.006/52.472/57.871 s; 1k selected 5.327 s, native NORMAL 37.326 s, I05 11.928 s, Batch 36.733 s, same-process p50 4.775 s, fresh p50 4.646 s; representative all-query native oracle equality; changed/restore exact | ACCEPTED for measured shapes; 100k F2/F4 marked NOT_INDEPENDENTLY_REPRODUCED; 100k all-seven/10×10 NOT_RUN_HELD |
| G3 | Performance/security falsifiers: pathological cardinality, repeated rank, false EMPTY, coherent locator/body tamper, wrong root/CURRENT, crash/restart, whole-Parquet scan, second decode, eager full C11, duplicate copy, source leakage | Accepted S2-C/S2-D focused 31/31; five-file S2-D group 29/29; partial-binding 2/2; own six 6/6; false EMPTY, tamper, wrong/denied root/CURRENT, locator/body mismatch, no full graph, no whole-table, no source open, skew occurrence identity, SIGKILL restart pass; known #999 native body-truth RED preserved and not repaired | ACCEPTED for executed guards; #999 engine-wide native soundness held RED |
| G4 | Publish runnable baseline before any change; if material bottleneck, obtain explicit narrow S2-C/D lease then smallest general fix; preserve all semantics | Baseline published and independently reproduced. Dominant query cost is real (204,125 row-group reads / 103,133,313 decoded rows at 100k selected), but author attributes it to `ORDER BY ref` inside `_respondent_family` and proposes per-respondent `(gid,off)` ordering / small LRU. Actual A/B counter: 10k routing reads 10,043 hash-order vs 258 physical-order; 2,000 respondents have rows in one gid (routing 1,984; coordinate/weight 2,000; events 1,992). Cause is native respondent traversal sorted by ref key, and event reads use a separate cache. Proposed fix does not address measured cause and is unproven | **REVISE_EXACT_DEFECT**; no handoff granted; no production repair by reviewer |
| G5 | Distinct nonauthor receiving: execute same released fixture with real native first consumers, independently verify budgets, call-path no-fallback, corpus/selector completeness, crash/negative proofs, performance improvement; return ACCEPT_SCOPED / REVISE / RESOURCE_HOLD | Fresh nonauthor session; author identity 43/43; representative fresh process all queries + I05 oracle equal; 100k regenerated and measured; 10k/1k matched; counter-native first reader; guards pass; exact defects above. No optimization exists to accept | **REVISE_EXACT_DEFECT** (baseline axes accepted, G4 causal/proposal and test-count claim held) |

## Accepted scope key

`ACCEPT_SCOPED@SOURCEFREE_C11_MATERIALIZATION_ECONOMICS` applies only to the
axes actually qualified: sourcefree 13-family materialization, physical
retained/staging budget, measured 100k writer and selected-query cost,
1k/10k query/native costs, representative native fact/replay/oracle parity,
changed/restore, and the listed guard/hostile suites.

It does **not** accept: G4 remediation, a 36-test claim, 100k F2/F4
reproduction, 100k all-seven or 10/10 repetition, true source decode, #998
joined vertical, #1001 full 100k/6 GiB vertical, engine-wide native body truth,
original35 rights, science, CURRENT/issuer, or protected merge.
