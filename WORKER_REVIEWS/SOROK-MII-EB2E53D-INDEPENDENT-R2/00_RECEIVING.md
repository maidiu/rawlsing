# MII checkpoint independent receiving — eb2e53d

**Checkpoint verdict:** `REVISE_CHECKPOINT` — the repaired early findings hold, but one concrete E3 exposure-ledger defect remains; final full acceptance is not granted.

**Author checkpoint:** `eb2e53d89d2acef556da6b6fb7ceb6622c9604dc`
**Reviewer branch:** `review/sorok-mii-eb2e53d-r2`
**Prior references preserved:** published early findings `319a2060d`; reviewer test commit `d33e58d5b4b8b841227f7e2356a970d44171508d`.
**Commission:** replacement complete-construction commission in the review workspace.

## Executed evidence

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider --basetemp "$PWD/.mii-review-state" \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_mii.py

# 10 passed in 406.73s
```

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider --basetemp "$PWD/.mii-review-state" \
  WORKER_REVIEWS/SOROK-MII-EB2E53D-INDEPENDENT-R2/test_eb2e53d_adverse.py

# 4 passed in 89.48s
```

The independent tests exercise the real `run_p6.experience` path. They confirm repaired observer identity, forged-recognition rejection, the offered/independent weight distinction, and the remaining exposure-record defect.

## Positive evidence

- `house.py`/`run_p6.py` now enforce `presentation_conditions.observer` through `mii.glance_available` and `mii.close_available`; foreign-observer optional detail and close inspection are denied.
- `mii._normalize` rejects hash-tampered exposures and `mii.merge_recognition` rebuilds recognition from committed inspection events; the independent forged-profile probe does not render the forged identity.
- Adaptive `look` on a previously selected target gets weight 1; a previously omitted available target gets weight 2 through the same P6 consumer.
- Duplicate exposure requests, corrupt profile recovery, profile scope mismatch, and control isolation from the P4 ledger pass the author suite.
- The new gallery fixture is exercised through `new --scene gallery` and `look hinge`, returning the committed brass-hinge identity rather than house-specific data.

## Concrete defect: exposure ledger drops unselected available candidates

`run_p6.py:145-168` computes `detail_candidates` (all eligible in-room details) but then replaces `offered` with only the selected entry:

```python
offered = ({selected: detail_candidates[selected]}
           if selected in detail_candidates else {})
exposure = mii.record_exposure(..., offered=offered, selected=selected, ...)
```

The exposure record therefore cannot distinguish “offered candidates” from “the one selected detail”; `mii.py:192-227` stores only that reduced `offered` map. The surface correctly reports `omitted_available`, but the durable exposure ledger does not.

Minimal independent reproduction: `test_exposure_ledger_omits_unselected_available_candidate` in `test_eb2e53d_adverse.py`.

Observed:
- `available == ["bench", "mug"]`
- `mii_surface["omitted_available"] == ["mug"]`
- `exposures[-1]["offered"]` contains only the selected target (`bench`), not `mug`

This violates E3’s requirement to record availability/offered/selected provenance before later action linkage. The smallest correction is to pass the full candidate map (or a separate `candidates` field) into `record_exposure`, preserving `offered` versus `selected` distinctly.

## Untested or still incomplete scope

- **E1 source denial/restore:** no direct committed-source mutation and restore through the actual P6 reader was executed here; the occlusion test is a fixture condition change, not a public-source denial/restore proof.
- **E2:** observer identity is now enforced, but the fixture still supplies one global viewer-condition object rather than independently qualified per-feature/per-object sources. This is a remaining qualification gap, not a failure of the repaired observer check.
- **E3:** beyond the concrete `offered` loss, interrupted append recovery and real fork/branch exposure isolation remain unproven at this checkpoint.
- **E5:** competing hypotheses and simple decay exist, but contradictory-evidence and correction-linked stale-evidence behavior were not independently executed.
- **E8:** corrupt/missing profile recovery is covered; real P2/P6 branch-fork isolation and interrupted persistence remain author-pending.
- **E9:** `measurements.json` and `measure_mii.py` are present, but this reviewer did not independently rerun the measurement suite.
- **E10/44:** the author return maps all 44 IDs, but several mappings are `PASS_SCOPED_BY_ABSENCE`, and the dedicated M01/M02/M04/M05 fixtures and real fork/performance additions are explicitly pending; the 44 mapping is not yet a complete independent execution report.
- **Not claimed:** native science, human validity, production privacy approval, live provider behavior, protected merge.

## Disposition

`REVISE_CHECKPOINT`: preserve the repaired observer/recognition/adaptive findings and the passed MII suite, but retain an exact E3 exposure-record defect and the listed finite scope. No implementation or other tracked source was modified; only this reviewer test/report is owned here.
