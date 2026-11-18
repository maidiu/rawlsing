# ANVIL production locality — independent G5

**Decision:** `ACCEPT_SCOPED_PRODUCTION_LOCALITY_CORRECTION`  
**Reviewer:** `ses_e30a442d8ffeYBbXi7rPUpPxoc` — existing independent native S1E/R6 reviewer; not the locality author.
**Branch:** `agent/anvil-engineering-cut1-owner-20261117-r1`  
**Frozen product archive:** `60e767a53ecdffaae289a11fc5ce6c40e5c4ecd0`  
**Baseline:** `347baec696c8b395d750ac3b9e74417a6490c223` / product blob `8825832f8…`  
**Current product:** blob `d662fc578…` / SHA-256 `6dcb875bf…`  
**New test:** blob `7373c1704…` / SHA-256 `f763231c9…`

Only `rawlsing_next/pre553_direct_estate_i03.py::DirectEstateI03Session._respondent_family` changed, plus the new locality test. No numerical, writer, schema, issuer or other production file changed.

## Execution custody

I took an isolated `git archive 60e767… rawlsing_next` snapshot under my own return `tmp/snapshot`; the snapshot product hash is `6dcb875bf…` and new test hash `f763231c9…`. I did not execute the old OWNER baseline (blob `8825832f8…`) and did not mutate product/tests. Product/test imports resolved to the snapshot.

## Actual production witness

### Revocation after first yield and canonical order

`witness_revocation_order.py`, sealed R2 estate, actual production method, old R4 adapter only as RED control:

- R4 old adapter: second routing ref yielded after revocation — **bypassed**
- actual production: first ref yielded, CURRENT revoked, second `next()` → `DirectEstateError: current source/operation authority refused`
- actual production valid iteration: **600 refs, sorted**, first/last exact
- adapter restored; `all_expected=true`

### Actual production f4 on sealed R2

`qualify_snapshot.py` under `supervise_qualification.py`; actual `admission.prepared_i03()`/`session.execute_i03`; no test-only adapter or monkeypatch.

- operation wall **2.654351s** unprofiled; **not comparable** with profiled 18.296/7.583s
- row-group reads **50**; rows **25,472**; family object materializations **9,600**; family calls **16**
- `read_table_calls=0`; C11 repository tripwire hits **0**; session builds **0**
- exact parity over **32 common fields**, including fact/semantic/risk/denominator/member/ref/replay and `raw_denominator_support=[5]`
- fact `ff607ebd…`; semantic `63b82285…`; replay `9708fccb…`; denominator members `5a5be896…`
- external supervision: exit 0, no abort, wall **6.539s**, sampled process-tree RSS **131,907,584 B**, scratch **30,368,896 B**, caps 120s/2GiB/2GiB

### Eager later-row refusal and buffer scope

`witness_later_row_eager.py` on the actual product session, corrupting the **last** routing member ref for one respondent after session build:

- first `next(generator)` → `DirectEstateError: native I03 cold family body/index identity mismatch`
- **0 objects yielded before the error**
- respondent/family scope **600 rows**, family total **9,600** — per-respondent list, not whole-estate buffer
- exception timing is the documented eager behaviour, not a semantic/order change

### Existing suites

- `test_anvil_production_locality_20261118.py` + direct-estate/body/parquet/prepared: **36 passed in 8.61s**
- native empirical query + prepared Batch: **37 passed in 6.13s**
- Covers changed valid source → changed native fact → old-root restore, body/ref/locator/routing/repeated/UNKNOWN-zero negatives, prepared/cold I03/I05/Batch behavior; no test weakening.

## Verdict

`ACCEPT_SCOPED_PRODUCTION_LOCALITY_CORRECTION` for the exact sourcefree production locality fix. No consequential defect reproduced. The change preserves canonical external order, restores canonical refs after physical `gid/off` traversal, applies CURRENT before every yield, and keeps a per-respondent/family bounded buffer.

This is not production service/science/actor/CURRENT/protected acceptance. No original35, no full 100k, no full native matrix, no Batch pair rebuild. The separate postconsumer G5 and combined integration are untouched. No product/test edits, no author repair, no self-acceptance, no background jobs.

Evidence: `WORKER_RETURNS/ANVIL_ENGINEERING_LOCALITY_G5_20261118/`.
