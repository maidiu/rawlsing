# Locality candidate — TEST_ONLY runtime experiment

**EXPERIMENT_NOT_IMPLEMENTED.** Production is unchanged. The probe only
patches the module-global `sorted` lookup in `_pre553_query_eval` so native
respondent traversal follows the session's physical insertion order.
All integrity, routing, predicate, risk, fact and replay owners remain the
accepted code.

## Matched same-release results

| case | query | baseline wall s | candidate wall s | factor | baseline RGR | candidate RGR | rows decoded B/C | fact/replay exact |
|---|---|---:|---:|---:|---:|---:|---|---|
| diag-10k | selected | 49.066 | 21.812 | 2.25x | 20157 | 588 | 10288362/299094 | True |
| diag-10k | f2_reverse | 51.790 | 21.116 | 2.45x | 20153 | 614 | 10285996/312088 | True |
| diag-10k | f4_three | 56.624 | 24.665 | 2.30x | 20161 | 588 | 10290410/299094 | True |
| diag-1k | selected | 4.390 | 2.046 | 2.15x | 1784 | 61 | 887770/29807 | True |
| diag-1k | f2_reverse | 4.545 | 1.993 | 2.28x | 1785 | 63 | 887943/30492 | True |
| diag-1k | f4_three | 5.002 | 2.468 | 2.03x | 1784 | 61 | 887770/29807 | True |
| hist-100k | selected | 580.548 | 265.680 | 2.19x | 204125 | 5784 | 104482267/2959415 | True |

## Interpretation

- The 100k selected query falls from 580.548 s / 204,125 row-group reads
  to 265.680 s / 5,784 reads with exact fact, projection, replay and
  release refs.  Tree RSS is 2.81 GiB versus 2.95 GiB; temp SQLite is
  1.301 GB in both.
- 10k selected/F2/F4 fall from 49.1/51.8/56.6 s to 21.8/21.1/24.7 s,
  with exact parity; 1k falls from 4.4/4.5/5.0 s to 2.0/2.0/2.5 s.
- Candidate row-group reads per unique gid: at 100k, events 634/634 =
  1.0 and routing 2,513/977 = 2.57; baseline events 100,050/634 = 157.8
  and routing 101,438/977 = 103.8.
- Remaining candidate 100k selected time is native object/predicate
  evaluation (about 247.8 CPU s) and session build; the read churn is
  removed.  This is a candidate for a narrow S2-C/D handoff, not an
  optimized engine acceptance.

## Limits

- 100k reverse F2/F4 were NOT_RUN in this follow-through; 10k matched
  F2/F4 exact parity is the scale proxy and the original 100k F2/F4
  remain NOT_INDEPENDENTLY_REPRODUCED.
- Candidate is a runtime override, not a production patch, owner
  acceptance, or G5 acceptance.  #999 native body-truth RED remains.
