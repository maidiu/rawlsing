# PROGRAMMA PYAT — Universal35 D r5: exact post-consumer decision and selected-alias repair

**STATUS:** `D_R5_POSTDECISION_EXACTNESS_AND_HELD_ALIAS_REPAIRED__F_SOURCEFREE_POSITIVE_PRESERVED__NATIVE_FACTS_HOLD`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**INPUT:** `43d35eed654d2fc98ea0f176bf5c4bd92f524da1` / code `ea4fb3796faa3ad4635763dc653395b7c25e4407`
**F R4 REVIEW:** `f2d2bdea7e7c1073421bc8cdd3e3545aa0291a66`

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R5-1. Post-consumer source-read decision must equal the exact pre-decode decision.** The bridge records the resolver decision before decode and compares the post-consumer decision by full dataclass equality, not only `CURRENT_GRANTED`/revocation flags. Any changed host, purpose, grant, scope, metadata-freeze refs, decision ref or other material refuses `SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER`. | F's `changed_after` accepted defect is closed without editing the admission owner. Same exact decision restore remains positive. | F independent focused closure. | D + source-read owner |
| **R5-2. Alias validation is limited to exact selected/current frontier operations.** `_bundle_with_plan_aliases` now derives required OriginalIDs only from the plan-derived frontier targets/conditions. Held/unselected physical code `Y` remains typed plan/held accounting and no longer causes `PHYSICAL_CODE_NOT_IN_BUNDLE:Y`. Selected missing physical codes and cross-source/conflicting OriginalIDs still refuse. | The false full-plan alias requirement is closed without dropping eligible operations, bypassing exact frontier membership or inventing refs. | Preserve selected/held distinction. | D/B + F |
| **R5-3. F sourcefree positive remains the production-wrapper evidence.** F independently observed the real wrapper on faithful sourcefree SAV/config: 30 facts, 15 expected operations, 18 candidates, anti/op-anti true, `native=false`, compilation hash `fdc6f3f9…`, ledger hash `233d2272…`. | This is TEST_ONLY_SOURCEFREE engineering, not original source/native/science permission. The two repairs preserve the same positive path. | Keep F receipt; recheck exact cut. | D + F |
| **R5-4. All35 scope remains explicit and narrow.** Plan: 18,276 items / 18,413 slots / 18,467 operations. Route-qualified executable frontier: 7 sources / 694 operations / 683 eligible / 11 held; 28 sources no explicit route-qualified frontier. Prior 20/991 non-F1 account remains historical. | No invented all35 candidate facts, no F2-F4 requests for sources with none, no silent drop. | Preserve both scopes and route labels. | D/B + HQ + F |

## 2. TESTS

```text
rawlsing_next/tests/test_pre553_original35_operations.py
9 passed in 28.26s

rawlsing_next/tests/test_pre553_original35_execution.py
3 passed in 116.51s
```

The B suite now includes held/unselected `Y` positive with a partial A/B native bundle and selected-missing negative refusal. D suite preserves manifest/path/no-current-decision refusals. F's actual production-wrapper positive remains the independent sourcefree integration receipt.

## 3. EVIDENCE / LIMITS

- `evidence/all35_frontier_accounting.json`, `evidence/route_qualification.json`, `evidence/native_bridge.json`.
- Plan ref `aae15f52877e4eb0c61bfbfb47efc2d650d3289036ce38d3a76acee1b1e84e20`; counts `5630/4655/8131/51/0`; route `676/4705/249`.
- Actual original native facts and E handshake remain `NOT_RUN`: no genuine current original source-read decision supplied.
- No fabricated resolver/issuer/authority, A/C/E semantic edit, protected merge, self-review, native/science grant or global change.

## 4. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r5 exact postdecision/alias repair
- Identity: codex/pyat-universal35-d-20261106-r1@<returned-commit>; input 43d35eed6.
- Function: full plan route-qualified F1/F2/F3H -> exact plan frontier -> governed compiler/facts; pre/post source-read decision must be identical; aliases only selected frontier IDs.
- Evidence: B 9 tests; D 3 tests; F sourcefree positive 30 facts/15 ops/18 candidates preserved; all35 18276/18413/18467; frontier 7/694/683/11.
- Limits: actual original facts/E handoff NOT_RUN; no current original source-read decision; no native/science/protected acceptance.
```

## 5. F REQUEST

Same F independent closure is requested on this exact frozen head: reproduce changed postdecision RED/fixed refusal/restore and held-unselected `Y` positive/selected-missing negative while preserving the 30-fact sourcefree positive.
