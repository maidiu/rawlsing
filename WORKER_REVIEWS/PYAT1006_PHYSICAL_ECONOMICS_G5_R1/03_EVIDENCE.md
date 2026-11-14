# Evidence — matched fixture, profile, budgets, parity, cold/guard proofs

All data below was produced by this review session on the assigned checkout.
Review scripts live in `probes/`; full generated estates and writer metrics stay
in `data/` (large, gitignored); compact receipts and logs are committed.

## 1. Identity and artifact verification

- Author `MANIFEST.json`: 43/43 files match bytes and SHA-256; only the manifest
  itself is unlisted by design.
- Production blobs equal `READER_ABI.md` at HEAD:
  `pre553_source_direct_parquet_estate.py 0e4b34ce...`,
  `pre553_direct_estate_i03.py 8b4d5ca2...`,
  `_pre553_direct_i02_sourcefree.py 45172751...`,
  `_pre553_external_i02_certificate.py cd5368e4...`,
  `pre553_saved_c11_admission.py 22749add...`, plus the five other listed files.
- `git diff 9d96a9ca..HEAD -- rawlsing_next` is empty; 05e9ceac..HEAD changes
  only return documentation.
- Published representative estate: all 15 files match the receipt and manifest;
  byte-identical copy opened in the review path.  All seven queries and I05 are
  exactly equal to the native oracle and the author receipt.

## 2. 100k fixture and physical census

Unchanged author fixture formula, `chunk_rows=512`, weights, A/B/C always,
sparse D, two ranked MR occurrences, typed missing B.

| member | rows | row groups | bytes |
|---|---:|---:|---:|
| AuthoritySnapshot | 5 | 1 | 15,684 |
| ComparatorReplayBinding | 0 | 1 | 2,975 |
| DiscoveryBranchReplayBinding | 0 | 1 | 2,975 |
| EmpiricalCoordinateFact | 100,000 | 196 | 29,739,830 |
| EmpiricalPredicateReplayBinding | 0 | 1 | 2,975 |
| EmpiricalUniverse | 1 | 1 | 13,278 |
| QuestionVariableBinding | 5 | 1 | 15,437 |
| RespondentEvent | 324,477 | 634 | 86,950,094 |
| RespondentIdentity | 100,000 | 196 | 20,450,901 |
| RoutingEligibilityFact | 500,000 | 977 | 123,457,753 |
| SourceUniverseRelation | 0 | 1 | 2,975 |
| StructuralAdmissionReplayBinding | 0 | 1 | 2,975 |
| WeightMeasureFact | 100,000 | 196 | 29,715,254 |
| event_locator | 324,477 | 634 | 19,802,439 |

- Distinct RespondentIdentity refs: 100,000.  Events: 324,477.
- Total Parquet rows including locator: 1,448,965; row groups: 2,841.
- Family counts equal the manifest; typed absences:
  `SourceUniverseRelation DISTINCT_BY_DEFAULT`,
  `EmpiricalPredicateReplayBinding NOT_APPLICABLE`,
  `ComparatorReplayBinding DEFERRED`,
  `DiscoveryBranchReplayBinding DEFERRED`,
  `StructuralAdmissionReplayBinding NOT_APPLICABLE`.
- File set is exactly 13 family members + event locator + manifest; no retained
  SQLite, staging directory, pickle or second body corpus.

## 3. Author claim versus independent measurement

| Quantity | Author | Review | Status |
|---|---:|---:|---|
| 100k write s | 3,033.723 | 2,943.177 | reproduced (tag differs) |
| 100k direct-I02 proof s | 2,249.700 | 2,218.465 | reproduced |
| 100k reread/re-encode s | 761.224 | 710.960 | reproduced |
| 100k `_row` s | 492.834 | 507.703 | reproduced |
| 100k root hashing s | 11.101 | 11.005 | reproduced |
| 100k retained B | 310,163,264 | 310,178,695 | reproduced (tag bytes) |
| 100k staging peak B | 5,257,841,984 | 5,209,185,593 | reproduced |
| 100k proof SQLite B | 4,385,796,096 | 4,337,704,960 | reproduced |
| 100k session SQLite B | 1,300,910,080 | 1,301,057,536 | reproduced |
| 100k writer tree RSS B | 295,211,008 | 281,415,680 | reproduced |
| 100k query tree RSS B | 3,690,455,040 | 3,002,982,400 selected-only | not directly comparable |
| 100k cold admission s | 1.520 | 1.669 | reproduced |
| 100k session build s | 33.508 | 25.934 profile / 37.588 isolated | reproduced |
| 100k selected s | 562.362 | 543.026 | reproduced |
| 100k F2 reverse s | 873.655 | not rerun | NOT_INDEPENDENTLY_REPRODUCED |
| 100k F4 three s | 908.507 | not rerun | NOT_INDEPENDENTLY_REPRODUCED |
| 10k write s | 191.808 | 197.202 | reproduced |
| 10k selected s | 51.069 | 54.006 | reproduced |
| 10k F2 reverse s | 58.742 | 52.472 | reproduced |
| 10k F4 three s | 60.486 | 57.871 | reproduced |
| 1k write s | 17.442 | 17.820 | reproduced |
| 1k selected s | 4.945 | 5.327 | reproduced |
| 1k native NORMAL s | 35.476 | 37.326 | reproduced |
| 1k I05 s | 11.925 | 11.928 | reproduced |
| 1k Batch s | 36.257 | 36.733 | reproduced |
| 1k same-process selected p50 | 4.748 | 4.775 | reproduced |
| 1k fresh-process selected p50 | 4.688 | 4.646 | reproduced |

Writer stage overlap versus wall at 100k: 2,218.465 + 710.960 + 11.005 =
2,940.430 s against 2,943.177 s wall; `_row` 507.703 s is nested inside the two
proof passes.  Writer dominance is therefore direct-I02 proof (~75.4%) plus
reread/re-encode (~24.2%), with root hashing ~0.37%.

Resource limits: writer tree 281,415,680 B and query process 3,002,982,400 B are
below 6 GiB; minimum free disk was 9,426,497,536 B, above the 3 GiB reserve; no
shape was killed.  The author 1k/10k "writer RSS" rows are whole-worker peaks;
writer-only 10k measured here is 214,261,760 B.

## 4. Actual ROWGROUPREAD counter profile and causal finding

100k selected query, fresh process:

| phase | reads | rows decoded | read_row_group s |
|---|---:|---:|---:|
| session build | 2,637 | 1,348,954 | 1.002 |
| query evaluation | 201,488 | 103,133,313 | 169.332 |

Query evaluation by family:

| family | reads | unique gids | rows decoded | consecutive-gid cache hit ratio | read s |
|---|---:|---:|---:|---:|---:|
| RoutingEligibilityFact | 101,438 | 977 | 51,923,040 | 0.0 | 96.549 |
| RespondentEvent | 100,050 | 634 | 51,210,273 | 0.0 | 72.782 |

So the selected query materialized about 51.2M event rows for 324,477 real
events (157.8×) and 51.9M routing rows for 500,000 real rows (103.8×).

Respondent-order A/B on the same session and the same per-respondent
`ORDER BY ref` query:

| shape | hash/ref respondent order | physical insertion order |
|---|---:|---:|
| 1k routing reads | 917 | 26 |
| 10k routing reads | 10,043 | 258 |
| 10k routing pass seconds | 28.411 | 11.734 |

Within-respondent gid shape (2,000 sampled 10k respondents):

| family | one gid | two gids |
|---|---:|---:|
| EmpiricalCoordinateFact | 2,000 | 0 |
| RoutingEligibilityFact | 1,984 | 16 |
| WeightMeasureFact | 2,000 | 0 |
| RespondentEvent | 1,992 | 8 |

Conclusion: the dominant measured cost is real repeated row-group
materialization, but it is caused by the native evaluator traversing respondents
in **ref-key order** (`pre553_empirical_query.py:448` and `:697`) across
physically ordered row groups.  Within one respondent, rows are already in one
gid, so the author's proposed per-respondent `(gid, off)` ordering cannot remove
the churn.  Event reads use a separate cache in
`VerifiedDirectEstate._events_from_postings` and are not covered by the
`_respondent_family` proposal.  A corrected profile and measured proposal are
required.

## 5. Native fact/replay/oracle/change/restore and cold/negative proof

- Representative 64-respondent fresh process: selected, F2 forward/reverse,
  F4 three/four, weighted, repeated and I05 equal native oracle fact refs,
  semantic projections, release refs and receipts.
- Own six tests: full-family oracle parity, changed C changes the fact and the
  old sealed root restores the exact old fact, false EMPTY/member tamper/wrong
  root/denied CURRENT refuse, no full C11 graph/whole-table/source open,
  high-cardinality 602-occurrence identity, SIGKILL before commit leaves no
  manifest and restart succeeds.
- 100k cold negatives: wrong held manifest hash, forged source root and denied
  current each refuse before a query result (`logs/100k_cold_negatives.log`).
- 1k native issued workload: NORMAL, COMPLETED, PARTIAL and ABSENT all
  `COMPLETED`; six Batch units all `COMPLETED`; I05 covers 1/1 candidate.
- No-fallback tripwires pass; saved path never constructs `C11Repository` and
  never calls `pq.read_table`.

## 6. Evidence index

- `evidence/artifact_verify.json` — author manifest, git blobs, representative
  estate, fresh queries and oracle equality.
- `evidence/measured_shapes.json` — review measurement extraction.
- `evidence/author_claim_vs_review.json` — claim/measurement reconciliation.
- `evidence/100k_physical_ledger.json` — actual 100k census.
- `evidence/family_gid_shape_10k.json` — within-respondent gid shape.
- `evidence/commands.json` — exact commands and exits.
- `logs/` — test stdout, writer/query logs, cold negative log.
- `data/diag-1k/query_profile.json`, `data/diag-10k/query_profile.json`,
  `data/hist-100k/query_profile.json` — full counter receipts.
- `data/hist-100k/writer_metrics.json` — full writer receipt.
