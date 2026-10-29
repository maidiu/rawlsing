# PYAT POST-REGULAR-PREMAIN INTEGRATION SCOPE CORRECTION R1

**USER-DEFINED INDEXING JURISDICTION. This supersedes the 2,831-branch indexing commissions in `07_INDEXING_FIRST_RABOCHII_MASTER_COMMISSION.md` and `08_INDEXING_RABOCHII_SHARDS_AND_ACCEPTANCE.json`. Those older commissions are NOT TO BE LAUNCHED. Any recovery courts remain HOLD.**

## Temporal evidence for the actual stopped-integration problem

The canonical `integration/pre-main-reconciliation-r1` has continued updating HQ handoffs through 2026-10-27. That is **not** evidence that it continued accepting worker implementation code. Direct GitHub commit-history sampling on `rawlsing_next` found:

- Dense continuing integration: 2026-09-27, 31 implementation-tree commits, last tested commit `ef46892f8e2752b62eef0778b1bdb53a86d80e70` at **2026-09-27T18:56:30Z**.
- Transition/sparse implementation receipts: 2026-10-04 (1), 2026-10-05 (9), 2026-10-06 (2), 2026-10-09 (5). The last observed implementation-tree commit is `79e0e74e14d8e09cc2f3af061aa178a149cb1674` at **2026-10-09T22:31:19Z**.
- After that, recent PREMAIN head history contains HQ control/receipt/checkpoint churn; the direct `rawlsing_next` path history did not return any more late implementation-tree commits as of this evidence cut.
- Therefore **September 27** is the conservative regular-integration-stoppage boundary. October 9 is only a narrow **last code-touch** boundary. Both are tested, not conflated.

## Actual complete ref-head metadata measurement, not guessed count

A qualified *read-only GitHub Actions Git runner* fetched all remote branch-tip **commit objects only** (`git fetch --depth=1 --filter=tree:0`; no survey/implementation blobs opened). It enumerated 2,837 refs and 2,749 unique tip SHA objects. The 2026-10-29 UTC run is 40803520502, with a 45-day ZIP artifact `pyat-post-integration-head-date-census` retaining both complete name/date/cohort JSONs. `09_POST_PREMAIN_HEAD_DATE_SCOPE_EXTRACTOR.py` records exact algorithm and limitations.

| Temporal cohort | All recent tip refs | Pyat/shared names | Unknown relevant names | Sorok-only boundary refs | Nonmain Pyat potential |
| --- | ---: | ---: | ---: | ---: | ---: |
| Conservative since **Sep 27** | 1,133 | **815** | **30** | **287** | **845** |
| Strict after **Oct 9** | 806 | **494** | **30** | **281** | **524** |
| Difference / transition | 327 | 321 | 0 | 6 | **321** |

One PREMAIN ref appears in both all-recent counts and is not a worker. **845 is the correct conservative input cohort to index; 524 its priority core.** 2,831 names are archival scope, not commissioned. The historical predecessor modules outside that date are **referenced dependencies only** when a post-cutoff branch actually touches/reuses them. Sorok-only 287 recent refs require just boundary owner metadata, not Pyat recovery implementation audits.

### Fundamental date caveat
Git branch refs have no creation timestamp in a Git object. The query tests whether the **commit at a branch tip** is dated after the cutoff, not whether the **branch name first appeared** then. A branch created after Sep27 pointing to an old commit would be missed by this proxy; an old branch advanced in October would be included. Therefore the actual appointed HQ must add known PR creation times, worker return/commission chronology, and any available Push/Create event/audit receipts as a secondary *reconciliation* for old-tip/new-name exceptions. If those receipts are unavailable, report the limitation as a coverage hold. Do **not** falsely call time of branch creation proved.

## Corrected commissioning design — seven roles rather than ten plus seven historical name shards

**S0 — sourcefree exact cutoff and scoped cohort extraction**: already demonstrated once by hosted Git, but appointed HQ must adopt, pin and refresh a stable named snapshot with time evidence and exact SHA; machine JSON permanently banked in private repo. No original data.

**S1–S4 — four disjoint scoped branch content indexers**, selected from exactly the **845** post-Sep27 Pyat/shared/unknown candidate rows, prioritized 524 strict post-Oct9 and 321 Sep28–Oct9 transition. Each completes branch HEAD, changed paths/blobs, implementation exported functions, tests, worker return/reviewer evidence, current PREMAIN receiving equivalent/different/absent code, authority/consumer grades and honest unknowns. No recovery court or code modifications. Deduplicate identical tip SHA and blobs. Assign by the permanent `11_SCOPED_POST_CUTOFF_CANDIDATE_SHARDS_*.json` machine lists once they are banked, not by the previous `NAME_HEAD_CANDIDATES_01..05` historical shards.

**S5 — cross-shard capability/consumer lineage reconciler**, not recovery court: ancestor pre-Sep27 branches only if named from S1–S4 concrete dependencies. Separate current source science, F1–F8, N0–N13, EE01–EE16 and Field Forge/world from Sorok actor jurisdiction. Preserve original law even if implementation exists later.

**S6 — independent hostile INDEX completeness auditor**, exact SHA/cut, not author or reviewer of self. Check 845 names under cutoff (and scoped newer delta), 100% changed file metadata or explicit incomplete object-hold, all relevant code symbols, source/review/consumer/holder statuses, no uninspected branch silently excluded, 30 unknowns really inspected, duplicate tips proper, creation-date limitation explicit. If the post-cutoff scope is expanded by secondary creation audit, those additions must be indexed before acceptance.

**No recovery court until S6 INDEX_ACCEPT**. Engineering worker launch only after actual qualified Pyat HQ adopts exact commission, verifies live host/leases/model selection, and issues its own instructions. This proposal branch is neither a new HQ nor source/semantic issuer.

## Status
- Historical 2,831 name census: archived and preserved, **not** the commissioned work.
- Actual 845 temporal Pyat candidate heads: known as a **tip-date cohort**, **not yet completely content-indexed**.
- 524 strict-core refs: priority first, all 845 inclusive.
- Exact candidates, counts and raw response: GitHub Actions run 40803520502 (artifact, 45-day retention); permanent sourcefile `09_POST_PREMAIN_HEAD_DATE_SCOPE_EXTRACTOR.py` plus narrower commission to be adopted.
- Prior selected 17 recovery cases: evidence leads, **FROZEN**; source-level court work should not resume before accepted scoped index.
