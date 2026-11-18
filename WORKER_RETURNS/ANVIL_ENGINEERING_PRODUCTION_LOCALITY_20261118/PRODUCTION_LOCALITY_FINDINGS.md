# PRODUCTION LOCALITY CORRECTION — CUT2

**Status:** `PRODUCTION_LOCALITY_IMPLEMENTED_RED_GREEN_PARITY`  
**Scope:** exact user-authorized production edit of `pre553_direct_estate_i03.py::DirectEstateI03Session._respondent_family`, plus new focused locality tests and this return. No architecture/issuer/writer/schema/numerical/full-scale change.  
**Baseline product:** `347baec696c8b395d750ac3b9e74417a6490c223` / cut1 G5 `092bf29ffa6724d477abb4ccfc770e3bc492250d`.  
**Baseline product blob:** `8825832f8067c7fce7a99a94505743cbb4eada06`.  
**Current product blob:** `d662fc578a1ecb42d54ec8b4bdab87fd7ecec176`.  
**New test blob:** `7373c1704e21bcb4155eb690b17de5ecd8bf22dc`.

## 1. Actual production diff

Only `DirectEstateI03Session._respondent_family` changed:

- member query order: `ORDER BY ref` → `ORDER BY gid,off`;
- materialize the selected respondent/family rows into a bounded local list;
- retain every original exact type/ref/body/respondent/universe/locator check;
- sort by `obj.ref.key` before yielding, restoring the externally observable canonical order;
- call `self._require_live()` immediately before **every** yield;
- document the deliberate eager-exception timing: a malformed later row refuses before the first yield, unlike the old streaming loop.

Full diff: `PRODUCTION_DIFF.diff`. No helper, evaluator, writer, schema, issuer, routing optimization or whole-estate corpus.

## 2. RED → GREEN (actual independent witness shape)

`production_revocation_witness.py` on the sealed R2 estate, `RoutingEligibilityFact`, first yield then revoke CURRENT:

| Case | Second call |
|---|---|
| R4 old test-only adapter | second routing ref yielded, **no error** — RED |
| Actual production method | `DirectEstateError: current source/operation authority refused` — GREEN |
| Canonical valid iteration | 600 refs, ref-sorted, no revocation |

`all_expected=true`; adapter restoration assertions true. This witness uses the actual product method for GREEN; no test-only monkeypatch is enabled for production qualification.

## 3. Actual production f4 observation

One bounded existing `f4_three_raw` on the frozen sealed R2 estate; no build/new estate/new pair/matrix/repeats/100k.

| Metric | Value |
|---|---:|
| Operation wall (production, no cProfile) | 2.770 s |
| Admission outside operation | 0.264 s |
| Index build outside operation | 2.958 s |
| Row-group reads | **50** |
| Row-group rows | 25,472 |
| Compressed read bytes | 7,942,218 |
| Uncompressed read bytes | 76,150,826 |
| Family object materializations | 9,600 |
| Event object materializations | 37 |
| Full semantic/identity/refs/member/replay parity | **exact** |
| External supervision | exit 0, no abort, 6.524 s |

External RSS sampled 134,471,680 B; scratch 30,368,896 B; caps 120 s / 2 GiB / 2 GiB. The 2.770 s is not comparable to the profiled 7.583/18.296 s; it is the actual production method without cProfile. It demonstrates the same 50-read geometry and full parity, not a matched speedup.

## 4. Tests actually run

| Command | Result |
|---|---|
| `pytest -q test_anvil_production_locality_20261118.py test_pre553_direct_estate_i03.py test_pre553_source_direct_parquet_estate.py test_pre553_prepared_saved_i03.py` | **36 passed in 9.06 s** |
| `pytest -q test_pre553_empirical_query.py test_anvil_prepared_saved_batch_cut1.py` | **37 passed in 6.67 s** |

The focused production test covers:
- canonical ref order on live valid iteration;
- CURRENT revocation after first yield → refusal;
- selected fact exact parity to the native oracle.

Existing focused suites cover changed legitimate input → changed fact → old-root restore, body/ref/event-locator poison, missing/routing/repeated/UNKNOWN zero negatives and native I03/I05/Batch behavior. No existing test was edited.

## 5. Fixtures / source pins

- Sealed R2 estate manifest `c209d3a198b25e5392dd422878fcc9111ada5c72aeb146d5d2a07388586bbc8b`.
- Contract `R2_PILOT/fixture_contract_pilot.json` `e928ebd17016c005efd1c8fee19a19b27e35fb360c6b8f85dd489cc9371b8f28`.
- Product baseline/blob and current blob above; `pre553_direct_estate_i03.py` is the only product file edited.
- R2/R3/R4/R5 historical evidence and corrected canonical measurement table remain immutable.

## 6. Limits / self-critical incompletions

- Per-respondent/family buffer is bounded at 600 routing facts in this witness; not full estate. The list is eager, so exception timing changes for a malformed later row; documented, not silently redefined.
- Product method is tested on the existing focused fixtures and one sealed f4 operation; no 100k, full matrix, fresh Batch, original35, source/science/actor/CURRENT issuance or production speedup.
- The edit is user-authorized for this exact symbol only; the distinct nonauthor reviewer (`ses_e30c...`) remains reserved. No self-acceptance.
- The production symbol permission under #1006 is not claimed; user GO authorizes this exact edit, not broader code/source/native rights.
