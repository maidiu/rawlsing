# PYAT #1006 measured physical/query baseline

ALL ROWS ARE SOURCEFREE SYNTHETIC TEST_ONLY. NOT ORIGINAL35, NOT #1001, NOT PRODUCTION CURRENT. TRUE SOURCE SNAPSHOT/DECODE IS NOT_RUN_PENDING_997.

## Host and software

- host: `oldMac.lan`, Darwin x86_64, macOS 13.7.8 (22H730), 16 GiB RAM, 16 vCPU, disk 408 GiB with ~16-17 GiB free at dispatch.

- Python 3.11.3; pyarrow 26.0.1; pandas 3.1.1; pyreadstat 1.3.7; pytest 9.2.0; psutil 7.2.2; task-local `.venv` inside the return directory.

- process-tree ceiling: 6,442,450,944 B (6 GiB), sampled every 20 ms; disk reserve 3 GiB. No shape hit the RSS ceiling.

- exact tested heads: assigned branch `codex/pyat1006-physical-baseline-20261113-r1` at `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`; accepted S2-C `b7b697b69f0acea12174937ee824c19ac34ac284`; accepted S2-D G5 `ba8d760cd8e31a9baff9b45698bd4117f4baa456`.

## Shape table

| shape | status | resp | events | ev/resp | write s | I02 proof s | reread/reencode s | row proj s | root hash s | Parquet B | rowgroups | stage peak B | proof SQLite B | cold admit s | session build s | temp SQLite B | selected s | same p50/p95 (n) | fresh p50/p95 (n) | F2 rev s | F4 3 s | I05 s | batch s | writer tree RSS B | query tree RSS B |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| diag-1k | MEASURED | 1000 | 3245 | 3.2450 | 17.442 | 11.577 | 5.341 | 4.567 | 0.117 | 3185373 | 38 | 51093725 | 43216896 | 0.026 | 7.616 total/41 | NOT_RUN | 4.945 | 4.748/4.860 (10) | 4.688/5.259 (10) | 4.622 | 5.685 | 11.925 | 36.257 | 502263808 | NOT_RUN |
| diag-10k | MEASURED | 10000 | 32450 | 3.2450 | 191.808 | 130.416 | 60.033 | 46.572 | 1.102 | 31117712 | 294 | 524699536 | 437809152 | 0.127 | 81.663 total/34 | NOT_RUN | 51.069 | 58.288/67.730 (10) | 57.400/60.271 (10) | 58.742 | 60.486 | 145.307 | 316.502 | 1394810880 | NOT_RUN |
| skew-1k | MEASURED | 1000 | 5245 | 5.2450 | 19.906 | 13.140 | 6.418 | 5.356 | 0.131 | 3750171 | 46 | 65941275 | 56639488 | 0.018 | 7.018 total/33 | NOT_RUN | 4.832 | 4.812/4.902 (5) | 4.563/4.609 (5) | 4.795 | 5.363 | 12.284 | 22.717 | 710381568 | NOT_RUN |
| scale-50k | MEASURED_PARTIAL_STOPPED_AFTER_WRITE | 50000 | 162240 | 3.2448 | 1528.039 | 1126.259 | 391.798 | 269.477 | 6.605 | 155137666 | 1425 | 2605780098 | 2169520128 | 0.687 | 14.555 | 650412032 | 297.986 | NOT_RUN | NOT_RUN | 295.457 | 497.799 | NOT_RUN | NOT_RUN | 233308160 | 1833365504 |
| hist-100k | MEASURED_PARTIAL_STOPPED_AFTER_WRITE | 100000 | 324477 | 3.2448 | 3033.723 | 2249.700 | 761.224 | 492.834 | 11.101 | 310163264 | 2841 | 5257841984 | 4385796096 | 1.520 | 33.508 | 1300910080 | 562.362 | NOT_RUN | NOT_RUN | 873.655 | 908.507 | NOT_RUN | NOT_RUN | 295211008 | 3690455040 |

## Native-reader subtable (1k/10k/skew only)

| shape | normal s | completed s | partial s | absent s | batch units | batch states |
|---|---|---|---|---|---|---|
| diag-1k | 35.476 | 2.268 | 31.516 | 36.423 | selected,f2_forward,f2_reverse,f4_three,f4_four,i05 | COMPLETED,COMPLETED,COMPLETED,COMPLETED,COMPLETED,COMPLETED |
| diag-10k | 416.878 | 30.739 | 308.536 | 481.108 | selected,f2_reverse,f4_three,i05 | COMPLETED,COMPLETED,COMPLETED,COMPLETED |
| skew-1k | 38.910 | 2.623 | 33.764 | 38.135 | selected,f4_three,i05 | COMPLETED,COMPLETED,COMPLETED |

## 100k physical family ledger

| member | bytes | rows | row groups |
|---|---|---|---|
| AuthoritySnapshot.parquet | 15644 | 5 | 1 |
| ComparatorReplayBinding.parquet | 2975 | 0 | 1 |
| DiscoveryBranchReplayBinding.parquet | 2975 | 0 | 1 |
| EmpiricalCoordinateFact.parquet | 29743711 | 100000 | 196 |
| EmpiricalPredicateReplayBinding.parquet | 2975 | 0 | 1 |
| EmpiricalUniverse.parquet | 13307 | 1 | 1 |
| QuestionVariableBinding.parquet | 15445 | 5 | 1 |
| RespondentEvent.parquet | 86984723 | 324477 | 634 |
| RespondentIdentity.parquet | 20446391 | 100000 | 196 |
| RoutingEligibilityFact.parquet | 123402709 | 500000 | 977 |
| SourceUniverseRelation.parquet | 2975 | 0 | 1 |
| StructuralAdmissionReplayBinding.parquet | 2975 | 0 | 1 |
| WeightMeasureFact.parquet | 29720478 | 100000 | 196 |
| event_locator.parquet | 19805981 | 324477 | 634 |

## Counts and negative facts

- 100k shape: 100,000 distinct respondents, 324,477 RespondentEvent rows (3.24477 events/respondent), 1,448,965 total Parquet rows, 2,841 row groups.

- `_row`/body_json reconstruction is called twice per object: once at write and once in the post-write reread/re-encode proof. At 100k, row calls: RespondentEvent 649,587; RoutingEligibilityFact 1,000,000; RespondentIdentity 200,000; EmpiricalCoordinateFact 200,000; WeightMeasureFact 200,000. Total `_row` time 492.834 s.

- 100k retained Parquet 310,163,264 B; staging peak 5,257,841,984 B; temporary I02 proof SQLite peak 4,385,796,096 B; session temporary SQLite 1,300,910,080 B. These are distinct files/phase costs, not one copy.

- 100k writer process-tree peak 295,211,008 B; 100k query process-tree peak 3,690,455,040 B; both below 6 GiB. 50k query peak 1,833,365,504 B.

- 100k cold admission 1.520 s; cold all-event posting-index build 33.508 s / 324,477 events / 700,000 member rows; selected query 562.362 s total, so query-time evaluation dominates the session build by ~16x.

- 50k cold admission 0.687 s; session build 14.555 s; selected 297.986 s; F2 reverse 295.457 s; F4 3-way 497.799 s.

- Source opens on the fixture producer: 0 (synthetic in-process generator). Full C11 repository builds on the saved path: 0 (tripwire). Whole `pq.read_table` calls: 0 (tripwire). Persistent second body corpus: none; each release has 13 family Parquet members + locator + manifest.

- Exact small-oracle parity: 48-respondent weighted fixture with A/B/C/D question families, reverse F2, same-respondent 3-way and 4-way joint, repeated occurrence, weighted query and I05; saved fact refs, semantic projections, release refs and I05 receipts equal native oracle. Changed C value changes the fact; old root restores exact old fact. Tests in `test_1006_baseline.py`: 6 passed.

- Accepted hostile regression suite reused proportionately: 31 passed (S2-C/S2-D direct estate) and 36 passed (S2-D saved admission/adversarial/five readers/source scope). See `evidence/`.


## Historical-shape difference

The Nov 11 historical W03 shape was 100k rows / 200k events. Preserving F2/F4 with genuine same-respondent 3+ question joints requires at least 3 events for each fully joint respondent; this fixture therefore uses 100k distinct respondents / 324,477 events (A,B,C always; sparse D; repeated MR; typed missing B). This is the closest executable shape under the frozen requirement, not an apples-to-apples W03 rerun. No comparison or improvement claim against the historic W03 777.5 s / 5,923,426,304 B persistence RSS is made.


## Dominant measured cost

At 100k the writer's dominant stage is the direct I02 semantic/identity/SQLite proof: 2,249.700 s of 3,033.723 s write (74.2%), with 761.224 s reread/re-encode proof (25.1%) and 492.834 s `_row`/body_json (overlapping both passes). Root hashing is 11.101 s (0.37%). Query economics are dominated by per-respondent native query evaluation after a 33.508 s session build: selected 562.362 s, F2 reverse 873.655 s, F4 3-way 908.507 s at 100k. The cold session is not the dominant query cost.


## Rejected assumptions

- The 6 GiB process-tree cap was not the failure at 100k: writer 295 MB, query 3.69 GB. The material failure is time/query economics and repeated cold evaluation, not RSS.

- O(N) session build is real but bounded (33.5 s at 100k, 1.3 GB temp SQLite); it is not the dominant selected-query cost.

- The accepted writer does not create a full C11 graph, does not reopen source and does not retain a second body corpus; its cost is exact canonical body/identity proof and JSON/SQLite work.


## NOT_RUN / holds

- TRUE source snapshot/decode/projection cost: NOT_RUN_PENDING_997 accepted bridge handoff. The fixture generator is synthetic and in-process.

- 100k x 10 same-process and 10 fresh-process repetitions: NOT_RUN_MEASURED_COST. 1k and 10k meet n=10; skew has n=5; 50k/100k have one measured query each because the measured per-query seconds make the 10/10 court impractical in this dispatch. No substitute claim.

- Full 100k all-seven native readers (Batch/NORMAL/COMPLETED/PARTIAL/ABSENT plus I05/F2/F4) and #1001 whole-vertical 6 GiB certification: NOT_RUN. The all-seven readers were exercised at 1k/10k/skew against this same physical reader ABI; #1001 remains separate.

- #997 source bridge, #998 joined integration, #1001 full 100k/6 GiB, #1007 original-source rights: not owned here.


