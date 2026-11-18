# R3 — ONE TARGETED Q-BOTTLENECK PROFILE

**Status:** `PROFILE_COMPLETE_PARITY_MATCH`  
**Scope:** ONE profiled execution of existing `PreparedI03Session.execute_i03` for `f4_three_raw` on the sealed R2 estate.  
**Grade:** sourcefree TEST_ONLY profile. Not a new benchmark pair, not a speedup, not native/100k/science/actor/economics acceptance.

**Product:** candidate `347baec696c8b395d750ac3b9e74417a6490c223`; cut1 G5 review `092bf29ffa6724d477abb4ccfc770e3bc492250d`.  
**Estate:** sealed R2 `.local-data-pilot` estate, manifest `c209d3a198b25e5392dd422878fcc9111ada5c72aeb146d5d2a07388586bbc8b`, contract `R2_PILOT/fixture_contract_pilot.json`.  
**No rebuild, no new estate, no new query, no source write.**

## 1. Method

One fresh child process:

1. open `PreparedSavedC11Admission` on the frozen estate;
2. enter one `PreparedI03Session`; admission and index build are measured **outside** the profile;
3. install a transparent observer around `PreparedI03Session.execute_i03` that returns the original result unchanged;
4. run **one** `session.execute_i03(query_ref=f4_three_raw, predicate_ref=...)` under cProfile + existing `CourtInstrumentation`;
5. compare the returned full semantic/identity/ref/member/replay digests to the frozen R2 pilot `f4_three_raw` row.

No baseline rerun. No automatic retry. External caps: 120 s child wall, 2 GiB process-tree RSS, 2 GiB scratch; 0.25 s supervision sampling; process-group abort mechanics. Actual: external wall 22.57 s, sampled RSS peak 172,122,112 B, scratch peak 30,390,928 B, exit 0, no abort.

Profiled wall `18.296 s` includes cProfile and transparent wrappers; **not** a matched timing. Admission outside profile `0.461 s`; index build outside profile `2.889 s`; prepared receipt operations = 1.

## 2. Concrete Q call tree / hotspots

From `top_cumulative.txt` / `top_tottime.txt`:

| Cumulative s | Function | Observation |
|---:|---|---|
| 18.296 | `profile_q.py:58(observed_exec)` | transparent observer wrapper |
| 18.296 | `pre553_prepared_saved_i03.py:85(execute_i03)` | actual prepared call |
| 18.295 | `pre553_empirical_query.py:734(execute_empirical_query)` | existing native evaluator |
| 18.280 | `_pre553_query_eval.py:640(_evaluate_index_group)` | group evaluation |
| **18.222** | `_pre553_query_eval.py:51(_routing_fact_for)` | **16 calls; main hotspot** |
| 18.020 | `pre553_direct_estate_i03.py:100(__getitem__)` | `_ColdFamilyRows` routing lazy load |
| **18.003** | `pre553_direct_estate_i03.py:398(_respondent_family)` | 6.059 s internal; 18.003 s cumulative |
| 6.774 | `pre553_parquet_carrier.py:131(_object_from_row)` | 9,637 calls; reconstruct/exact-body validation |
| 6.770 | `CourtInstrumentation.py:235(family_object)` | 9,600 routing + 37 event objects |
| 5.035 | `pre553_empirical_objects.py:377(CanonicalSemanticObject.__init__)` | 9,638 calls; semantic hash/validation |
| 3.685 | `pyarrow/parquet/core.py:436(read_row_group)` | **3,965 row-group reads** |
| 2.786 | `pre553_empirical_objects.py:181(canonicalize)` | 666,379 calls |
| 2.393 | `pre553_empirical_objects.py:220(semantic_hash)` | 9,642 calls |
| 0.882 | JSON decode inside `_respondent_family` | 105,933 `json.loads` calls |
| 0.011 | `sqlite3.Connection.execute` | 53 calls; **not the bottleneck** |

Counters for the one profile: `row_group_reads=3,965`, `row_group_rows=2,012,160`, `row_group_uncompressed_bytes=6,011,490,388`, `row_group_compressed_bytes=634,219,540`, `family_rows_yielded=9,600`, `family_object_materializations=9,600`, `event_object_materializations=37`, `selected_events_yielded=37`, `read_table_calls=0`, `session_builds=0` (build outside profile).

## 3. What the profile actually shows

### The dominant cost is routing materialization, not numerical counting

`_routing_fact_for` (`_pre553_query_eval.py:51`) executes:

```python
matches = [
    fact for fact in index.routing_by_respondent[respondent.ref.key]
    if _question_matches(fact, target_ref)
    and _ref_field(fact, "risk_set_ref") == risk_set_ref
]
```

It materializes **all routing facts for a respondent** through `_ColdFamilyRows.__getitem__` before filtering to the exact target. The profile has 16 `_routing_fact_for` calls and 9,600 routing objects for the 16 respondents; only the matching target facts are used for the fact/risk/denominator result. Numerical counting and fact assembly are small relative to this routing materialization path.

### The row-group read count is thrash, not index-query cost

`_respondent_family` (`pre553_direct_estate_i03.py:398`) queries:

```sql
SELECT ref,gid,off FROM members WHERE family=? AND respondent=? ORDER BY ref
```

then uses a **single-row-group** cache:

```python
if cache.get("gid") == gid:
    rows = cache["rows"]
else:
    rows = physical.read_row_group(gid, columns=["body_json", "ref"]).to_pylist()
    cache.clear()
    cache.update({"gid": gid, "rows": rows})
```

Because `ORDER BY ref` does not follow physical `gid/off`, the refs for one respondent alternate across row groups and the one-entry cache thrashes. The profile records 3,965 row-group reads and 3,964 cache clears; a gid/off-ordered access would need on the order of one read per visited row group, not one per ref transition. `sqlite3.execute` itself is only 0.011 s / 53 calls, so the SQLite index query is **not** the cost.

### Object reconstruction/validation/hash is the second layer

`_object_from_row` (9,637 calls, 6.774 s), `CanonicalSemanticObject.__init__` (9,638 calls, 5.035 s), `canonicalize` (666,379 calls, 2.786 s) and `semantic_hash` (9,642 calls, 2.393 s) are exact-body/identity validation and canonicalization. They are not numerical counting, but they are required for exact body/ref/event/routing identity and cannot be disabled to obtain a green profile.

### Q versus physical/parity/reference/hash

- **Q numerical counting:** small relative to the listed routing/materialization frames; it is inside `_evaluate_index_group` but not the dominant hotspot.
- **Physical materialization/parity:** `_routing_fact_for` + `_respondent_family` + `_object_from_row` + row-group reads dominate.
- **Hash/ref validation:** `canonicalize`/`semantic_hash`/object init are significant but secondary.
- **Reference/fact assembly:** `_build_fact` is not a top hotspot in this profile.

No validation, receipt, current-math or member/parity check was disabled.

## 4. Parity

Returned result exactly matches frozen R2 pilot `f4_three_raw` for:

- `identity_sha256`, `semantic_sha256`, `refs_sha256`, `member_refs_sha256`, `replay_sha256` — all true.

The prepared receipt records exactly one operation on the frozen estate. No claim is made if parity fails; here it matched.

## 5. Smallest lawful corrective experiment

**Smallest production-symbol change:** in `pre553_direct_estate_i03.py` `DirectEstateI03Session._respondent_family` (lines 412–414), change the member query from `ORDER BY ref` to physical `ORDER BY gid,off` (or an equivalent covering index/order), preserving the exact returned facts and validation. This is a measured, low-risk first experiment: it attacks the 3,965 row-group reads / 3,964 cache clears without changing the scientific evaluator or disabling validation.

**If that is insufficient:** add an exact routing selector keyed by `(family, respondent, question_or_target, risk_set, state)` so `_routing_fact_for` does not materialize all 600 routing facts per respondent. This requires a derived selector/index and an owner grant in `pre553_direct_estate_i03.py` / `_pre553_query_eval.py`; it is not a new evaluator or persistent engine.

**Alternative not justified by this profile:**

- SQLite query/index tuning alone: `sqlite3.execute` is 0.011 s; not the bottleneck.
- Numerical-counting rewrite: not the measured hotspot.
- Bypassing `_object_from_row`/`semantic_hash`/validation: would weaken exact body/ref/parity; rejected.
- A new store/index/backend: not needed to address the measured routing-read thrash; would add non-loss/resource risk.
- 1/10/100 or Batch rerun: not justified by one profile; next step is one owner-granted corrective experiment and one re-profile at the same f4/estate.

**Competent owner grant needed:** S2-C direct-reader owner and native I03 evaluator owner for the exact `_respondent_family` query-order change and, if chosen, the routing selector. No grant is asserted here.

## 6. Limitations

- cProfile and transparent instrumentation inflate the profiled wall; not a performance comparison.
- One operation (`f4_three_raw`) on one sourcefree 16R/600Q geometry; not all 600 items, not native/original/100k.
- Process-tree RSS is 0.25 s sampled/external; OS file cache uncontrolled.
- No product patch, no new estate, no baseline rerun, no retry, no 1/10/100.
- Sourcefree TEST_ONLY; no source/science/actor/100k/economic acceptance.
