# PROGRAMMA DELTA — PYAT #1006 independent nonauthor G5

## Change class

REVIEW + PROBE + EVIDENCE ONLY.  No `rawlsing_next` production or accepted test
file was edited, replaced or merged.  No author harness or evidence file was
modified.  New files are confined to
`WORKER_REVIEWS/PYAT1006_PHYSICAL_ECONOMICS_G5_R1/`.  No new engine,
architecture, authority store, codec, producer, controller or timer exists.

## Result

**`REVISE_EXACT_DEFECT`.**

Independently reproduced: author artifact identity; sourcefree 13-family
materialization; 100k distinct respondents / 324,477 events / 1,448,965 rows /
2,841 row groups; 100k writer 2,943.177 s, staging peak 5,209,185,593 B,
retained 310,178,695 B, writer tree 281,415,680 B; 100k selected query 543.026 s;
10k and 1k query/native-reader costs; representative native fact/replay/oracle
parity; changed/restore; no-fallback and hostile guards; cold negatives.

Exact defects:

1. **G4 cause/proposal is wrong.**  The measured churn comes from native
   respondent traversal in ref-key order across physically ordered row groups,
   not from `ORDER BY ref` within one respondent.  A/B counter: 10k routing
   reads 10,043 hash-order versus 258 physical-order; 2,000 respondents mostly
   have all side-family rows in one gid.  The proposed per-respondent `(gid,off)`
   ordering cannot fix this, and the separate event-read cache is not covered.
2. **Claimed 36 S2-D tests is 29.**  The exact RUNBOOK five-file command passes
   29; the author evidence files 26 + 3 = 29.  Adding the separate
   partial-binding suite gives 31, still not 36.
3. **Minor label:** the 1k/10k "writer process-tree RSS" rows are whole-worker
   peaks, not writer-only.  Writer-only 10k is 214,261,760 B.

## Accepted / held

Accepted at sourcefree measured scope: sourcefree C11 physical
materialization/retained/staging economics; 100k writer and selected-query
budget; 1k/10k query and native costs; representative native parity and
changed/restore; executed guards.

Held: G4 remediation and any S2-C/D owner handoff; the 36-test claim; 100k
F2/F4 independent reproduction (`NOT_INDEPENDENTLY_REPRODUCED`); 100k all-seven
and 10/10 repetitions; true source decode (#997); #998 joined vertical; #1001
full 100k/6 GiB vertical; #999 engine-wide native body truth (known RED);
original35 rights, science, CURRENT/issuer and protected merge.

## Next action

The #1006 author/owner should correct the causal counter profile and proposal,
correct the test-count claim, and, if still warranted, request an explicit
narrow S2-C/D handoff with a measured fix that addresses respondent traversal
or the per-family row-group cache (including events).  This reviewer did not
repair production or author code and grants no optimization authority.

No `ACCEPT_SCOPED` is claimed for G4 or downstream completion.  A qualified
baseline cost finding is not an optimized engine, native integrity acceptance
or full 100k vertical acceptance.
