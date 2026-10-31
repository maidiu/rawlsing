# RRIF estate coverage and residual holds

**Status:** WORKING CANDIDATE — NOT HQ-ADJUDICATED. This is an RRIF sourcefree reconciliation, not a Programma, native science, world, actor or production release.

## Exact denominator

| Measure | Exact result |
|---|---:|
| Historical branch names | 845 |
| Distinct roster tips | 838 |
| Branch shards | S1 175, S2 175, S3 174, S4 161, S5 160 |
| Corrected historical families | 1,885 |
| Function IDs exact-once | 3,135 |
| Function shards | S1 1,279, S2 218, S3 398, S4 897, S5 343 |
| External zero-member families | 2 (`S6EXT-P41-SERVICE`, `S6EXT-R61-R09-NEGATIVE`) |
| Preserved S7FIX negative records | 2,595 |
| Post-S7FIX return negatives | 8 |
| Corrected boundary families | 11 (5 outer splits, 5 nested splits, 1 join) |
| Current implementation paths present | 892 families |
| Current exact source-blob families | 101 `ALREADY_CURRENT` |
| Behavioral equivalence proved | 0 |
| Independent reviewed full-family dispositions | 0 |
| Current fan-in accepted | 0 |
| Actual production recipients verified | 0 |

## Disposition counts

| Status | Families |
|---|---:|
| `EVIDENCE_ONLY` | 841 |
| `AUTHORITY_HELD` | 285 |
| `RETIRED_DEFECTIVE` | 190 |
| `NOT_RESOLVED` | 149 |
| `ALREADY_CURRENT` | 101 |
| `HISTORICAL_ONLY` | 95 |
| `CURRENT_DIFFERENT` | 80 |
| `NO_REAL_RECEIVER_VERIFIED` | 79 |
| `DUPLICATE_SUPERSEDED` | 53 |
| `CANDIDATE_ADAPT` | 9 |
| `CURRENT_TEST_ONLY` | 3 |
| **Total** | **1,885** |

| Decision | Families |
|---|---:|
| `PRESERVE_HISTORICAL` | 1,040 |
| `HOLD_EXACT_DECISION` | 602 |
| `RETIRE` | 243 |
| `ADAPT_MINIMAL` / `ADOPT` | 0 |

`ADAPT_MINIMAL`/`ADOPT` are zero because no family has the full set: named current receiving ABI, actual caller/consumer, fault-negative and positive receipts, original owner and independent reviewer. The nine `CANDIDATE_ADAPT` rows are candidates for a future owner decision, not production-ready changes.

## Current-state interpretation

- `ALREADY_CURRENT` means an exact historical source blob is present at PRE-MAIN. It does **not** mean the function is imported, behaviorally equivalent, scientifically issued or adopted.
- `CURRENT_DIFFERENT` means a current path exists but the historical implementation is not the current one. The six corrected boundaries are in this class or in `HISTORICAL_ONLY`; their S7FIX current-owner mapping is **RED**.
- `CURRENT_TEST_ONLY` and `EVIDENCE_ONLY` are test/evidence surfaces, not production capabilities.
- `NO_REAL_RECEIVER_VERIFIED` and `HISTORICAL_ONLY` do **not** mean the function is missing from the historical estate or that a future world service should be built. They mean no actual current receiver is proven.
- `AUTHORITY_HELD` preserves original source/permission holds; it does not grant a sourcefree substitute.
- `RETIRED_DEFECTIVE` preserves named historical failures; it does not erase the historical evidence or create a replacement.

## Six boundary correction

The S7FIX identity repair is accepted only at historical source-identity grade. The I3 hostile court found:

- 5/5 historical outer method ASTs exist in history, but **0/5** match current outer ASTs;
- 5 nested `_make_sealed_source_relation_owner` families have **no current nested owner**;
- the historical `PhysicalSourceIncidence.iter_batches.emit` join AST differs from current PR526 emit (`77d9be6c…` vs `4f7cd7cc…`);
- current `pre553_source_relations.py` is test-only, with no production import; current decoder static imports are not executed consumers.

Thus the 11 corrected families are not promoted to current equivalence. The ledger marks the owner mapping RED and keeps nested families historical-only.

## Independent-review and return status

- S7FIX structural identity: source-identity PASS; I3 current owner mapping **RED**.
- I3 reviewed the six boundary identities, not all 1,885 family dispositions.
- Recent C3/R9, P41/R08 and F7/P07 are author returns; their original-author tests are not independent acceptance. Independent courts #569/#570/#571 are **PENDING**.
- PE successor `a48c6acb…` and #564 are pending; original PE strict remains **4/13**.
- S7 map #565 is a different worker’s correction; this return does not edit it.
- PR #568 superseded stale R→O intake; PR #572 is three-return evidence intake only; PR #566 PROGRAMMA is **DEFERRED**.
- PR519 PRE-MAIN fan-in governance is a separate authority; this return does not self-CAS, merge or invent a gate.

## Finite RRIF blockers

1. Correct the S7 current ownership mapping (#565) and keep nested/historical identities separate.
2. Prove or explicitly retain the absence of a current production receiver for every candidate.
3. Obtain independent review of the 1,885-family disposition and the three recent returns.
4. Resolve owner decisions for D01/D02, R9 custody, P41/R08, selected-world seam, F7/P07, PE/V2K, R61-R09 and R157.
5. Keep the 841 evidence-only and 285 authority-held families as evidence, not missing capabilities; keep the 8 post-S7FIX PE/R9/F7/P07/S7/V2K/R157 negatives in `POST_S7FIX_RETURN_NEGATIVES.jsonl`.

## Post-RRIF product development (not this worker)

Native source/U/E_pre, N9/N10W/N11/N12, C11, world service, actor/person and A0–A5 remain post-RRIF product development. RRIF does not require finishing full PRE-V3 before closing this disposition, and this return starts no all35 empirical, world, N9, N11/N12 or actor campaign.

## Consequential exclusions

- **R9:** no transplant; PR526 custody must not be bypassed.
- **P07:** native owner unsafe; preserve OOB/leak/parity negatives.
- **PE overlay:** test-fixture-only RED; never merge sitecustomize or synthetic authority.
- **V2K:** historical interface retired scoped; R61 current is test-only.
- **R157:** 35-wave CONFIG preparation only; original U/E_pre unexecuted.
- **S7 current owner mapping:** RED; historical identity is not current equivalence.

## Exact source inputs

- S7FIX `80bc5d9bf6624c2ea04027322947a41c347330aa`, artifact blob `743f79e2e618d3e5f083c6033ba9f37f0d4c4c07`, SHA-256 `f7b7d4eeca135295f3d29571a13e076486be31ffab314e7308ae5e68316a71df`.
- S7FIX I3 `1b89fd49c330e4a2c976e6af8d6c1a5e6dbfb088`.
- PRE-MAIN `8e44ca9c751049d65e6def47600b5c073ee04b29`; `rawlsing_next` tree `1d88d3fbb1d18dadfda946d9cd7f309d84afa479`.
- C3/R9 `24847592f6a40fde3c4932d0f26173012c037078`; P41/R08 `aa6ca0d700f10bc349a98d98c4239c554ca221f8`; F7/P07 `f8fe03cc6e6a482f428bed9e03c08e50ce1e6479`.
