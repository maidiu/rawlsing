# PYAT #1006 — independent nonauthor G5 receiving

**Verdict: `REVISE_EXACT_DEFECT`.**

The measured sourcefree physical baseline is broadly real and independently
reproducible at the tested head, including the 100k writer and selected-query
cost.  The return is not accepted as a complete G5 because its G4 dominant-cost
causal attribution and proposed remediation are contradicted by an actual
ROWGROUPREAD counter profile, and its claimed S2-D test count is not
reproducible.  No production, accepted test, author harness or author evidence
file was edited.  No optimization was implemented.

## Tested identities and permissions

- Immutable author head: `51aabffef90399359008e00890f551a1e56c0da9`.
- Code/tests commit: `05e9ceacfd1a43aa8c21ff3144502550916deadd`.
- Frozen production head: `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`.
  `git diff 9d96a9ca..HEAD -- rawlsing_next` is empty.
- Accepted S2-C `b7b697b69f0acea12174937ee824c19ac34ac284`; S2-D
  `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`.
- Review branch: `codex/pyat1006-independent-economics-review-20261113-r1`.
- Fresh session: `ses_e285e6d52ffe5iAGMQAUd17dSx`; not the #1006 author,
  #1007 author or #1023 reviewer.
- Permission grade: **SOURCEFREE TEST_ONLY**.  No original35 respondent
  bytes, `.env`, keys, production CURRENT/issuer, protected merge, source
  bridge, #998 joined vertical, #1001 full court or #1007 rights were used.

## What independently reproduced

1. **Author artifact identity.** All 43 listed return files match
   `MANIFEST.json` (bytes and SHA-256); all nine production blob SHAs match
   `READER_ABI.md`; the 15-file published representative estate matches every
   member hash and its manifest hash.
2. **Fresh-process representative release.** The published 64-respondent
   estate was copied byte-for-byte to the review path and opened in a fresh
   process through `SavedC11Admission`.  All seven native queries and I05
   produced fact refs, semantic projections, release refs and receipt refs
   exactly equal to the native oracle and to `representative_receipt.json`.
3. **100k shape and census.** Regenerated from the unchanged author fixture
   helper: 100,000 distinct RespondentIdentity refs, 324,477 RespondentEvent
   rows, 1,448,965 total Parquet rows including the locator, 2,841 row groups,
   all 13 family members plus locator and manifest, family counts equal to the
   manifest, typed absences present (`DISTINCT_BY_DEFAULT`, two `DEFERRED`, two
   `NOT_APPLICABLE`), no retained SQLite or staging directory.
4. **100k writer economics.** Review measured 2,943.177 s write (author
   3,033.723 s), direct-I02 proof 2,218.465 s, reread/re-encode proof 710.960 s,
   `_row` 507.703 s, root hashing 11.005 s; stage peak 5,209,185,593 B,
   temporary proof SQLite 4,337,704,960 B, retained 310,178,695 B, writer tree
   RSS 281,415,680 B, minimum free disk 9,426,497,536 B.  All below the 6 GiB
   and 3 GiB-reserve limits.  The tag differs from the author's 100k tag, so
   tag-dependent body bytes/fact refs differ while counts and row groups match.
5. **100k selected-query cost.** Fresh process: admission 1.669 s, session build
   25.934 s, selected I03 543.026 s (author 562.362 s), query phase 517.092 s.
   The fact is `SUPPORTED` with denominator 50,000.  The 204,125 measured
   row-group reads and 103,133,313 decoded rows show the cost is real.
6. **10k/1k matched costs and native path.** 10k selected 54.006 s, reverse F2
   52.472 s, F4 three-way 57.871 s; 1k selected 5.327 s, native NORMAL 37.326 s,
   I05 11.928 s, batch 36.733 s, same-process selected p50 4.775 s,
   fresh-process p50 4.646 s.  These closely match the author table.
7. **Guards/hostiles.** The accepted S2-C/S2-D focused suite passed 31/31; the
   five-file RUNBOOK S2-D group passed 29/29; the partial-binding suite passed
   2/2; the author's own six tests passed 6/6.  These cover false EMPTY, member
   tamper, wrong/mixed root, revoked CURRENT, locator/body mismatch, no full
   C11 graph, no whole-table read, no source open on the saved path,
   changed/restore exactness, high-cardinality occurrence identity and
   SIGKILL-before-commit restart.

## Exact defects requiring revision

### 1. G4 causal attribution and proposed fix are misdirected

Author claim: `_respondent_family` reads member rows `ORDER BY ref`, which is
not row-group order, so the single-row-group cache thrashes.

Actual counter evidence:

- 10k: routing `ROWGROUPREAD` count is **10,043** when respondents are traversed
  in native hash/ref order, versus **258** when the same session traverses the
  same respondents in physical insertion order.  The same per-respondent
  `ORDER BY ref` runs in both passes.
- 1k: 917 reads in hash order versus 26 in physical order.
- 2,000 sampled 10k respondents: routing rows occupy one gid for 1,984
  respondents and two gids for only 16; coordinate and weight rows occupy one
  gid for all 2,000; events occupy one gid for 1,992 and two for 8.
- At 100k the selected query issued 101,438 routing reads across 977 gids and
  100,050 event reads across 634 gids, with zero consecutive-gid cache hits.

The actual cause is the native evaluator's respondent order:
`sorted(index.respondents.values(), key=lambda item: item.ref.key)` in
`rawlsing_next/_pre553_query_eval.py:448` and `:697`, while physical row groups
follow insertion/respondent order.  Consecutive hash-order respondents map to
random gids.  Ordering one respondent's member rows by `(gid, off)` cannot
change that cross-respondent order.  A "small bounded LRU" is unquantified and
would need to retain most of the 977/634 row groups to avoid re-decoding; and
the proposal does not cover event reads, which use the separate cache in
`VerifiedDirectEstate._events_from_postings`, about half of the measured
selected-query reads.  The author's proposed "one smallest fix" is therefore
not demonstrated to address the dominant measured cost.  A corrected profile
and a measured proposal are required before any S2-C/D handoff request.

### 2. Claimed S2-D test count is not reproducible

The return states 36 passed for "S2-D saved admission/adversarial/five readers/
source scope".  The exact RUNBOOK five-file command passes **29**, not 36, and
the author's own evidence files sum to 29 (26 + 3).  Adding the separate
partial-binding suite gives 31, still not 36.  The return must identify the
actual 36-test selection or correct the count.

### 3. Minor resource-label correction

The 1k/10k "writer process-tree RSS" rows in the author table come from the
whole shape worker, including queries and native readers, not the writer alone.
The review measured writer-only 10k tree RSS at 214,261,760 B versus the table's
1,394,810,880 B.  The 50k/100k rows are writer-only because those runs stopped
after write.  This does not change the cost verdict, but the label is wrong.

## Preserved known REDs and scope holds

- #999 coherent native body poison still produces a wrong native fact
  (owner `native_build` exception pending).  Passing old public/guard suites does
  not make the engine fully sound.  This review did not touch or re-commission
  that repair.
- #997 remains 0 QUERY / 1 DISCOVERY at the governed frontier; issuer binding is
  another owner's work and was not duplicated.
- #998 joined integration, #1001 full 100k whole-vertical/6 GiB certification,
  #1007 source rights and protected merge remain held.
- 100k reverse F2 and F4 three-way were not independently rerun; their 10k
  matched paths and the representative oracle were.  Author 100k F2/F4 seconds
  are `NOT_INDEPENDENTLY_REPRODUCED`.
- 100k all-seven native readers and 10/10 same/fresh repetitions remain
  `NOT_RUN_HELD`.
- Provider quota/cost is `UNOBSERVED`.

## Accepted versus held axes

Accepted at sourcefree measured scope: artifact identity; 13-family physical
materialization and typed absences; 100k writer/staging/retained budget;
100k selected-query cost; 10k/1k query and native-reader costs; representative
fact/replay/oracle/change/restore parity; guard/hostile tests; no-fallback
tripwires; cold fresh-process admission.

Held/revise: G4 causal explanation and remediation proposal; 36-test claim;
100k F2/F4 reproduction; 100k all-seven and 10/10 repetitions; true source
decode (#997); joined/full vertical (#998/#1001); engine-wide native soundness
(#999 RED); original35/science/production/protected authority.

A qualified baseline cost finding is not an optimized engine, native integrity
acceptance, or full 100k vertical acceptance.
