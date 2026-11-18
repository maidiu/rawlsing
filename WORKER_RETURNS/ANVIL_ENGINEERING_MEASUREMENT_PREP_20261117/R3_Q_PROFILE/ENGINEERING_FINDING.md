# R3 ENGINEERING FINDING — ROUTING MATERIALIZATION THRASH

**Source pin:** product candidate `347baec696c8b395d750ac3b9e74417a6490c223`; cut1 G5 `092bf29ffa6724d477abb4ccfc770e3bc492250d`; `prepared` blob `bcb146edae680028e027e47cae45891693f63526`; actual source symbols below.  
**Scope:** one profiled `f4_three_raw` on the frozen R2 estate; sourcefree TEST_ONLY. Not a new pair, not a speedup, not native/100k.

## Finding

The native Q cost is dominated by **routing materialization and row-group thrash**, not numerical counting or SQLite lookup.

- `_pre553_query_eval.py:51(_routing_fact_for)` is 18.222 s cumulative over 16 calls. It list-comprehends `index.routing_by_respondent[respondent]` and filters by target/risk after materializing all 600 routing facts for each respondent.
- `pre553_direct_estate_i03.py:398(_respondent_family)` is 18.003 s cumulative / 6.059 s internal. Its SQL is `SELECT ref,gid,off FROM members WHERE family=? AND respondent=? ORDER BY ref`; a single-row-group cache is cleared on every gid transition. Profile: 3,965 `read_row_group` calls, 3,964 `dict.clear` calls, 2,012,160 rows, 6.0 GB uncompressed.
- `_object_from_row` 6.774 s / 9,637 calls; `CanonicalSemanticObject.__init__` 5.035 s / 9,638; `canonicalize` 2.786 s / 666,379; `semantic_hash` 2.393 s / 9,642. These are exact body/identity validation/hash, not numerical counting.
- `sqlite3.Connection.execute` 0.011 s / 53 calls. SQLite query/index tuning alone is not the measured bottleneck.
- Full semantic/identity/refs/member/replay parity is exact against frozen R2 `f4_three_raw` (`identity c912bcc4...`).

## Reusable lesson

Prepared-session reuse removes index-build repetition, but it does not remove per-query routing materialization: the query still asks for all 600 routing facts per respondent to find the exact target. A single-row-group cache combined with ref-ordered member rows turns that into thousands of row-group reads. Measure physical member-access geometry separately from numerical aggregation.

## Counterevidence / limits

- cProfile + transparent wrappers inflate wall; not a matched timing.
- 16 respondents/600 question bindings is sourcefree geometry, not original/native/100k.
- One operation only; does not establish a general ILP or all-query speedup.
- `_respondent_family` ordering may be semantically observable to callers that consume tuple order; the corrective experiment must preserve exact facts/parity.
- No validation/hash/current-math may be disabled to gain speed.

## Smallest lawful next experiment

Under S2-C direct-reader + native evaluator owner grant, change only the member ordering in `DirectEstateI03Session._respondent_family` from `ORDER BY ref` to physical `ORDER BY gid,off` (or an equivalent covering order), then re-profile the same `f4_three_raw` on the same frozen estate and require exact parity. If row-group reads do not fall near one-per-visited-group, the next bounded option is an exact routing selector keyed by respondent/target/risk/state; no new evaluator/store.
