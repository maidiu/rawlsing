# Locality experiment — independent R2 counters, parity, guards and budgets

All runs are sourcefree TEST_ONLY.  The R1 estates were copied byte-for-byte to
the R2 path; no R1 file was modified.  R2 capsules change only `root` and
`exact_path`; manifest, I02, release, query refs and all 15 member hashes equal
the R1 originals.

## Same-estate before/after

| case | query | baseline s | candidate s | baseline reads | candidate reads | factor | exact |
|---|---|---:|---:|---:|---:|---:|---|
| 1k | selected | 4.975 | 2.275 | 1,784 | 61 | 2.19× | yes |
| 1k | reverse F2 | 4.715 | 2.295 | 1,785 | 63 | 2.05× | yes |
| 1k | 3-way F4 | 4.934 | 2.575 | 1,784 | 61 | 1.92× | yes |
| 1k | weighted | 5.467 | 2.365 | 2,033 | 63 | 2.31× | yes |
| 10k | selected | 52.195 | 22.896 | 20,157 | 588 | 2.28× | yes |
| 10k | reverse F2 | 51.264 | 21.721 | 20,153 | 614 | 2.36× | yes |
| 10k | 3-way F4 | 56.011 | 25.372 | 20,161 | 588 | 2.21× | yes |
| 100k | selected | R1 543.026 | 294.087 | 204,125 | 5,784 | 1.85× | fact ref equal |

“Exact” means fact ExactRef, full semantic projection SHA-256, replay ref and
release refs all equal between baseline and candidate; 1k/10k also equal the
native oracle and the R1 baseline fact refs.  100k candidate fact ref
`87c3f0589e4ee1a8a3a695b2bbb0b7585ed7f87cb10dcb15074cb5c8b446a986` equals
the R1 baseline fact ref; candidate release ref equals the capsule release.

100k candidate: wall 294.087 s, CPU 263.166 s, tree peak 2,803,986,432 B,
temporary SQLite 1,301,057,536 B, fact `SUPPORTED`, denominator 50,000.
Author paired run: 580.548 → 265.680 s.  Cross-run wall factors are indicative;
read counts and fact identity are exact.  The author's “2.81 GiB” is 2.81
decimal GB (2.61 GiB), not a cap issue.

100k candidate reads by phase: query evaluation 3,147 reads / 1,610,461 rows
decoded; session build 2,637 reads / 1,348,954 rows.  Query evaluation:
`RespondentEvent` 634 reads / 634 gids / 324,477 rows (1.0 per gid);
`RoutingEligibilityFact` 2,513 reads / 977 gids / 1,285,984 rows (2.57 per gid).

## Sort-override audit

Candidate override returned physical insertion order only when the sorted values
were all `RespondentIdentity`:

| scope | physical respondent returns | respondent values | fallback key sorts | fallback other |
|---|---:|---:|---:|---:|
| 1k (4 queries) | 4 | 4,000 | 4,016 | 17 |
| 10k (3 queries) | 3 | 30,000 | 30,012 | 12 |
| 100k (selected) | 1 | 100,000 | 100,004 | 4 |

Source inspection finds exactly three respondent traversals in
`rawlsing_next/_pre553_query_eval.py` (lines ~364, ~448, ~697).  All other sorts
in that module are over refs/events/authorities/dict items and fall back.
`_canonical_refs`, `_canonical_authorities`, `_cell_projection` and `used_objects`
canonicalization sort their output, which the exact projections/replay refs
confirm.

## Unequal-weight adversarial case

Sourcefree release: 128 respondents, 416 events, exact weights cycling through
`1/3, 5/7, 11/13, 17/19, 0.1, 0.2, 0.30000000000000004, 7/3, 2/9, 13/11`.
The weighted query has two unequal cells:

- cell 0: weighted `958736/21945`; cell 1: weighted `534236/21945`.

The two-target weighted F4 has four cells with nonzero unequal fractions
including `214/133` and `116/33`.  Baseline, candidate and native oracle have
equal fact ref, projection SHA-256, replay ref and release ref for both queries
(`076d1fa3…` and `09524cb5…` are the fact/projection hashes).  This directly
checks canonical exact fraction/probability invariance under traversal order
change.

## Native oracle, changed/restore and guards

Independent R2 48-respondent weighted original/changed pair:

- selected, reverse F2, 3-way F4, weighted and repeated: candidate equals
  baseline, baseline equals native oracle, changed equals changed native oracle,
  old root restores exact old fact.
- denied CURRENT, wrong source root, omitted locator and omitted family member:
  all refuse.
- candidate selected still returns the exact baseline fact with
  `C11Repository.__init__` and `pq.read_table` both blocked; no full-graph or
  whole-table fallback.

## Resource bounds

| run | tree peak RSS B | min free disk B |
|---|---:|---:|
| 1k baseline/candidate | 340,369,408 / 209,793,024 | 17,550,647,296 |
| 10k baseline/candidate | 687,104,000 / 566,874,112 | 15,275,646,976 |
| 100k candidate | 2,803,986,432 | 15,185,276,928 |
| 2k writer profile | 274,927,616 | 16,356,896,768 |
| guard probe | 139,632,640 | 15,297,708,032 |

All below 6 GiB; minimum free disk remains above the 3 GiB reserve.  One
workload child at a time; no resource hold.

## Evidence index

- `evidence/identity_verification.json`
- `evidence/r2_measurements.json`
- `data/runs/*.json` and `*.monitored.json` (full run receipts; gitignored)
- `data/adversarial-weight/adversarial_weight.json` (full projection material;
  gitignored)
- `logs/run_*.log` (raw stdout/stderr), `logs/author_locality_candidate_tests.txt`
- `probes/r2_locality_probe.py`, `probes/r2_adversarial_weight.py`,
  `probes/r2_guard_probe.py`, `probes/r2_writer_profile.py`
