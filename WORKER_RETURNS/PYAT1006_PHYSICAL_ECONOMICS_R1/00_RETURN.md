# PYAT #1006 — sourcefree physical economics baseline return

## 1. Verdict

**`REVISE_EXACT_DEFECT_RECONCILED` — baseline material query-cost failure
stands; one measured TEST_ONLY locality candidate is available for a conditional
S2-C/D handoff.**

No production code was edited.  The accepted S2-C writer and S2-D readers are
sound at the tested sourcefree scope and exact oracle parity, but the measured
100k query path is not economically usable as-is: selected I03 562.362 s,
reverse F2 873.655 s, same-respondent 3-way F4 908.507 s on the same sealed
release.  Independent G5 `0169fac9...` corrected the original causal claim; the
follow-through measured physical-order respondent traversal and preserved exact
fact/replay while reducing 100k selected to 265.680 s / 5,784 reads.  The
candidate is `EXPERIMENT_NOT_IMPLEMENTED`, not production or G5.  No self-review
is claimed.

## 1a. Independent G5 reconciliation — 2026-11-13 ET

Fresh nonauthor review `0169fac9f3840800796c664eee462bbb8984bb42` (draft
PR #1034) returned **`REVISE_EXACT_DEFECT`** and is accepted here as the
controlling disposition of this baseline.  It independently reproduced the
100k writer (`2,943.177 s`), selected query (`543.026 s`), 13-family census,
representative oracle parity, changed/restore and guard suites, and identified
three exact report defects which the follow-through at
`followthrough_r2/` corrects:

1. the old `_respondent_family` `ORDER BY ref` / small-LRU causal proposal was
   **wrong**; the actual churn is native respondent traversal in ref-key order
   across physically ordered row groups, plus the separate event cache;
2. the claimed 36-test S2-D group is **29** for the named five files and **31**
   only when the separate 2-test partial-binding suite is added;
3. the 1k/10k "writer RSS" rows were whole-worker peaks, not writer-only.

Known #999 coherent native body-poison RED remains external and is not
repaired, hidden, or promoted by this follow-through.

## 2. Exact tested frozen head and permissions

- Assigned branch/worktree: `codex/pyat1006-physical-baseline-20261113-r1`
  at `/Users/matthewsmith/.codex/worktrees/sorok-duel-b01/Rawlsing`.
- Frozen production head used by every run:
  `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`.
- Accepted S2-C: `b7b697b69f0acea12174937ee824c19ac34ac284`.
- Accepted S2-D G5: `ba8d760cd8e31a9baff9b45698bd4117f4baa456`.
- Original harness commit: `05e9ceacfd1a43aa8c21ff3144502550916deadd`.
- Independent G5: `0169fac9f3840800796c664eee462bbb8984bb42`
  (`REVISE_EXACT_DEFECT`, draft PR #1034).
- Follow-through branch: `codex/pyat1006-locality-writer-profile-20261113-r1`,
  descendant of `51aabffef90399359008e00890f551a1e56c0da9`.
- Follow-through commit: `1ca1c735a577a7524a0a26c15df8879cd88704e3`.
  The tested production tree remains the frozen head above.
- Write lease used: **only new files** under
  `WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1/`.
- All `rawlsing_next` production and accepted test files were READONLY.
- Permission grade: **SOURCEFREE TEST_ONLY**.  No original35 respondent
  microdata, native source access, production CURRENT/issuer, science or
  protected-merge authority was used or claimed.

## 3. G1 — storage and measurement contract

Pinned chain: synthetic sourcefree 13-family generator -> accepted
`SourcefreeDirectI02Sections` -> accepted S2-C direct I02 + Parquet/Zstd
writer -> externally held manifest/direct-I02 roots -> accepted S2-D
`VerifiedDirectEstate` / `DirectEstateI03Session` / `SavedC11Admission` ->
native I03/F2/F4/I05/Batch/normal/resume.

Fixture shapes (all sourcefree, all 13 families, weights, typed missing B,
routed D/MR, repeated ranked MR, A/B/C same-respondent joints):

| shape | respondents | events | events/respondent |
|---|---:|---:|---:|
| diag-1k | 1,000 | 3,245 | 3.2450 |
| diag-10k | 10,000 | 32,450 | 3.2450 |
| skew-1k | 1,000 | 5,245 | 5.2450 |
| scale-50k | 50,000 | 162,240 | 3.2448 |
| hist-100k | 100,000 | 324,477 | 3.2448 |

The historical W03 shape was 100k rows / 200k events.  The frozen F2/F4
requirement (genuine same-respondent 3+ question joint) requires at least 3
events per fully joint respondent; this fixture is the closest executable
shape and is **not** an apples-to-apples W03 rerun.  No historical improvement
or regression claim is made.

Retained physical files at 100k: 13 family Parquet members + event locator +
manifest; 310,163,264 B retained; 2,841 row groups.  Staging peak
5,257,841,984 B; temporary direct-I02 proof SQLite 4,385,796,096 B; session
temporary SQLite 1,300,910,080 B.  These are distinct phases, not one copy.
No persistent second body corpus was created.  Per-family byte/row/row-group
ledger: `evidence/baseline_table.md`.

Counters: fixture source opens 0 (synthetic in-process); full
`C11Repository`/`C11LogicalRelease` builds on the saved path 0 (tripwire);
whole-table `pq.read_table` 0 (tripwire); source-extension opens during saved
readers 0.  `_row`/body_json is invoked twice per object (write + post-write
re-encode proof).

## 4. G2 — actual persistence and fast query baseline

Full table: `evidence/baseline_table.md`; raw compact receipts:
`evidence/baseline_summary.json`.  Absolute highlights on `oldMac.lan`
(Darwin x86_64, macOS 13.7.8, 16 GiB RAM, 16 vCPU, Python 3.11.3, pyarrow
26.0.1, Zstd via PyArrow):

| stage | 1k | 10k | 50k | 100k |
|---|---:|---:|---:|---:|
| write total s | 17.442 | 191.808 | 1,528.039 | 3,033.723 |
| direct I02 semantic/proof s | 11.577 | 130.416 | 1,126.259 | 2,249.700 |
| reread/re-encode proof s | 5.341 | 60.033 | 391.798 | 761.224 |
| `_row`/body_json s | 4.567 | 46.572 | 269.477 | 492.834 |
| root hashing s | 0.117 | 1.102 | 6.605 | 11.101 |
| cold admission s | 0.026 | 0.127 | 0.687 | 1.520 |
| all-event session build s | 0.186 avg / 41 calls | 2.402 avg / 34 calls | 14.555 | 33.508 |
| selected I03 s | 4.945 | 51.069 | 297.986 | 562.362 |
| reverse F2 s | 4.622 | 58.742 | 295.457 | 873.655 |
| same-respondent 3-way F4 s | 5.685 | 60.486 | 497.799 | 908.507 |
| I05 s | 11.925 | 145.307 | NOT_RUN | NOT_RUN |
| same-process selected p50/p95 (n) | 4.748/4.860 (10) | 58.288/67.730 (10) | NOT_RUN | NOT_RUN |
| fresh-process selected p50/p95 (n) | 4.688/5.259 (10) | 57.400/60.271 (10) | NOT_RUN | NOT_RUN |
| whole-worker tree RSS B (1k/10k) | 502,263,808 | 1,394,810,880 | n/a | n/a |
| writer-only tree RSS B (50k/100k; 1k/10k corrected) | 194,072,576 (1k) | 214,261,760 (10k, review) | 233,308,160 | 295,211,008 |
| query phase tree RSS B | (whole-worker) | (whole-worker) | 1,833,365,504 | 3,690,455,040 |
| 6 GiB cap | PASS | PASS | PASS | PASS |

Native readers on the same releases: 1k/10k/skew exercised actual Batch,
NORMAL, COMPLETED, PARTIAL and ABSENT; all returned `COMPLETED`/expected
resume states and exact native output refs (see `evidence/baseline_table.md`).
100k all-seven native readers and 10/10 repetitions are **NOT_RUN**: the
measured single-query seconds make that court impractical in this dispatch;
no substitute claim.

Small qualified oracle: 64-respondent weighted release, exact native oracle
parity for selected I03, both F2 directions, 3-way F4, 4-way F4, weighted,
repeated occurrence and I05; exact fact refs, semantic projections, release
refs and receipts equal.  Changed C value changes the exact fact; the old
sealed root restores the exact old fact.  Representative retained estate and
receipt: `evidence/representative-estate/`,
`evidence/representative_receipt.json`.

## 5. G3 — falsifiers and hostile receipts

Executed:

- Accepted S2-C/S2-D hostile suites: **31 passed** (direct estate writer/cold
  I03: false EMPTY, missing member, tamper, self-rehash, posting forgery,
  symlink/root, duplicate/omitted locator, full-family census, fresh process,
  change/restore).
- Accepted S2-D RUNBOOK five-file saved/adversarial/five-reader/source-scope
  group: **29 passed**.  A separate partial-binding-order suite adds
  **2 passed**.  The old "36 passed" claim was unreproducible and is withdrawn;
  these are 29 + 2, not one 36-test selection.
- Own fixture tests: **6 passed** (full family/oracle parity, changed/restore,
  false EMPTY/tamper/denied CURRENT/wrong root, no full graph/whole table/
  source open, high-cardinality skew occurrence identity, SIGKILL-before-commit
  no manifest + restart).  Follow-through locality tests add **2 passed**
  (candidate exact oracle/change/restore and candidate hostile checks).
- Source opens during saved readers: 0.  Full C11 graph builds: 0.  Whole
  `pq.read_table`: 0.  Persistent second body corpus: 0.
- Current/external-root guards: denied authorizer refuses before estate bytes;
  wrong direct-I02 source root refuses; missing/tampered member refuses;
  changed body/locator under a repinned manifest refuses before a false fact.
- Failed workload shape: earlier unsplit 50k attempt timed out at 2,400 s with
  process tree 1,654,665,216 B (no cap breach, no committed-release claim);
  `evidence/failed_50k_timeout.json`.  The split 50k writer run completed and
  is the authoritative writer receipt.

NOT_RUN / explicit holds: original35 source rights, production CURRENT,
#997 source snapshot/decode bridge, #998 joined vertical, #1001 100k
whole-vertical/6 GiB certification, #1007 rights, full 100k all-seven native
readers, 100k 10/10 same/fresh repetitions.  No subset is presented as the
complete commission.

## 6. G4 — economical remediation

The runnable baseline table (`evidence/baseline_table.md`) was published
**before** any proposal.  The measured material failure is query-time economics, not the 6 GiB process
cap.  Independent ROWGROUPREAD counters show the actual cause is **native
respondent traversal in ref-key/hash order** while physical row groups follow
insertion order: at 10k, routing reads are 10,043 in hash order versus 258 in
physical order with the same per-respondent SQL; at 100k the selected query
issued 101,438 routing reads and 100,050 event reads with zero consecutive-gid
cache hits.  Within one respondent the side-family rows already occupy one
(rarely two) gid, so per-respondent `(gid,off)` ordering cannot fix the churn;
event reads use a separate cache in `VerifiedDirectEstate._events_from_postings`.

The follow-through runtime experiment (production unchanged, labeled
`EXPERIMENT_NOT_IMPLEMENTED`) changes only the module-global respondent sort in
`_pre553_query_eval` to physical insertion order.  On the same reviewer-retained
releases it preserves exact fact/projection/replay/release refs for selected,
reverse F2 and 3-question F4, while reducing:
- 100k selected: 580.548 s / 204,125 reads -> 265.680 s / 5,784 reads (2.19x);
- 10k selected/F2/F4: 49.1/51.8/56.6 s -> 21.8/21.1/24.7 s (2.25/2.45/2.30x);
- 1k selected/F2/F4: 4.4/4.5/5.0 s -> 2.0/2.0/2.5 s (2.15/2.28/2.03x).

This is a measured candidate for a narrow S2-C/D owner handoff, not a
production patch, optimized-engine acceptance or G5 acceptance.  100k
reverse-F2/F4 remain `NOT_INDEPENDENTLY_REPRODUCED`; 10k matched F2/F4 is the
scale proxy.  The writer profile at
`followthrough_r2/WRITER_PROFILE.md` corrects the "SQLite proof" shorthand:
the direct-I02 inclusive stage is dominated by canonical semantic
projection/identity/object validation and body_json reconstruction, with
SQLite execute only about 4.2% of the inflated 2k profile wall.  The one
smallest owner-consistent writer proposal is a per-build memo of the already
computed immutable semantic projection/hash for validation+insert; it is
**not implemented** and must not remove any check.  See
`followthrough_r2/PROGRAMMA_DELTA.md` for the ordinary follow-through delta.

## 7. Required #997 handoff and #998/#1001 boundaries

#997 still owns the authentic one-pass source snapshot/decode/13-family body
tee into `SourcefreeDirectI02Sections`, plus the postconsumer receipt/fate
join.  This return shows the physical reader ABI accepts lazy one-shot
13-family iterators and exact held roots, but true source decode time remains
**NOT_RUN_PENDING_997**.  #998 owns joined integration; #1001 owns the full
100k distinct-respondent whole-vertical 6 GiB court; #1007 owns original
source rights.  This standalone comparison is not #1001 certification.

## 8. Return artifacts

- `00_RETURN.md` — this receipt.
- `PROGRAMMA_DELTA.md` — delta, verdict and one proposal.
- `READER_ABI.md` — exact pins, derivation note and reusable ABI.
- `RUNBOOK.md` — environment, representative fixture and exact regeneration/
  test commands.
- `evidence/baseline_table.md`, `evidence/baseline_summary.json` — measured
  baseline and per-shape compact receipts.
- `evidence/representative-estate/`, `evidence/representative_receipt.json` —
  retained small same-fixture estate and exact roots/fact refs.
- `evidence/accepted_s2c_s2d_focused.txt`,
  `evidence/accepted_s2d_five_readers.txt`,
  `evidence/accepted_s2d_source_scope.txt`,
  `evidence/own_baseline_tests.txt` — test stdout.
- `evidence/query_probe_monitored.json`,
  `evidence/failed_50k_timeout.json` — query tree/process facts and the typed
  failed shape.
- `fixture_1006.py`, `query_1006.py`, `instrument_1006.py`,
  `resources_1006.py`, `shape_worker.py`, `query_probe.py`,
  `fresh_probe.py`, `session_probe.py`, `run_suite.py`, `summarize.py`,
  `make_tables.py`, `make_representative.py`, `test_1006_baseline.py` — the
  independent harness/tests.
- `MANIFEST.json` — tracked-file checksums and representative estate
  checksums.

Provider token/cost: **UNOBSERVED** (no provider billing data available in
this session).  No secrets, credentials, global permissions or server/provider
settings were read or changed.  No production repair or downstream work was
started.  STOP after return; independent G5 is not this worker's act.
