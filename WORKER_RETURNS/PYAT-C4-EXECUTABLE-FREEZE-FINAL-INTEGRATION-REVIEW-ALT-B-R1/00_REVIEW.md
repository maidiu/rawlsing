# PYAT C4 — Executable freeze final independent integration review — R1 (ALT-B LANE)

**Disposition: `APPROVE_AT_DECLARED_GRAIN`**

Terminal: `C4_EXECUTABLE_FREEZE_FINAL_INTEGRATION_REVIEW_ALT_B_RETURNED__HQ_ADJUDICATION_REQUIRED`

Branch `agent/reviewer-pyat-hq181-c4-executable-freeze-final-integration-review-alt-b-r1`,
review base `8ff40d37de69db2d8a6053a7c2242f481677f1a4`, commissioned tip
`2836f6259c932c2308b9c15351d4051d18ba7e60`. Fan-in under review
`8ff40d37de69db2d8a6053a7c2242f481677f1a4`, commissioned fan-in tip
`012569770c551aca60c16eb20482c3435399c5d1`.

Governing authority: Omega-1 `01762d7379be4e423dad3e21bcdcee47c536902d`
(`A_GO_WITH_EXACT_C4_CONDITIONS`), O1-C01 through O1-C11.

I did not read the parallel A-lane review branch, its commission, or any return
packet on it. No speculation about the other reviewer's findings is recorded here.
Every judgement below is my own, formed from git objects and imported documentary
evidence only.

## What this approval means, and what it does not

Accepted: the **source-free** C4 executable freeze at its declared grain.

It permits HQ to resolve and fill the seven source access locators and to issue or
obtain the exact O1-C06 warrant. It does **not** authorise raw-source execution. No
source locator was discovered, searched for, or inferred in this review.

## Result

| Condition | Fan-in claim | My independent adjudication |
|---|---|---|
| O1-C01 combined tree | `CLOSED_BOUND` | **CONFIRMED** — 14/14 pinned blobs exact (13 declared + Route-B producer) |
| O1-C02 workload | `CLOSED_BOUND` | **CONFIRMED** — 8/8 SHA-256 agree 4-way; ordinals and read economy agree 3-way |
| O1-C03 oracle custody | `CLOSED_BOUND` | **CONFIRMED** at declared grain; 2 typed residuals |
| O1-C04 D02 | `CLOSED_BOUND` | **CONFIRMED** — payload string matches C4C3 byte-for-byte |
| O1-C05 runtime | `CLOSED_BOUND` | **CONFIRMED**; residuals elevated — see R7 |
| O1-C06 warrant | `CANDIDATE_ONLY__NOT_ISSUED` | **CONFIRMED** — SHA recomputed exact; R9 repair required before issuance |
| O1-C07 / C08 | frozen before warrant | **CONFIRMED**; zero-retry does **not** conflict with any frozen retry law |
| O1-C09 / C10 | preserved, 280 cells | **CONFIRMED** — arithmetic recomputed; zero PASS cells anywhere |
| 16/16 source-free checks | asserted | **NOT ACCEPTED ON ITS FACE** — re-derived independently; see §12 |

I did not accept the fan-in's 16/16, 34/34 or 13/13 because the packet said so. I
recomputed each one. All substantive claims hold; three denominators are
mis-stated, always in the conservative direction (see R11).

## §1 Commit graph and integration law — count discrepancy adjudicated

Exact graph, reconstructed from parents:

```
8ff40d37  fan-in final
  └ f8c8e2e4  import C4B + D2P by exact blob
      └ 39015a90  merge C4C3   parents = (01256977, 1df64cc5)
          ├ 01256977  HQ179 bind fan-in
          └ 1df64cc5  C4C3 return → eba2f4249 (HQ174 bind)
8f7efe690  C4A combined tree
  └ 9a5752a8  C4A ancestry-preserving merge  parents = (603795eb, 30686b18)
```

The apparent discrepancy is **purely a counting-basis difference and hides no
unreviewed work**:

- `01256977..8ff40d37` first-parent = **3** (the fan-in's own commits)
- `01256977..8ff40d37` total reachable = **5** (the same 3, plus `eba2f4249` and
  `1df64cc59` — both on the declared C4C3 merge side)

Both extra commits are the C4C3 return and its HQ bind. Nothing else is reachable.

Requirements met:

- C4A exact tree `8f7efe690` **is** an ancestor of head.
- C4A merge `9a5752a8` **is** an ancestor of head.
- C4C3 merge **lawful**: `merge-base(1df64cc5, 8f7efe690)` is exactly `8f7efe690`,
  i.e. C4A is an ancestor of C4C3, so the merge introduced no unrelated ancestry.
- C4B `c2af4f61` and D2P `41bd7a7c` are **not** ancestors of head; both were
  correctly imported by exact path/blob. `merge-base(C4B, 8f7efe690)` =
  `149c3d263`; `merge-base(D2P, 8f7efe690)` = `bc207de1d`.
- **No unrelated ancestry imported.** The three fan-in commits add **47 files,
  0 modifications, 0 deletions**, all confined to four `WORKER_RETURNS/`
  directories. `data/`, `LOCAL_CUSTODY/`, `LOCAL_COURTS/`, `.rabochii/`,
  `PYAT_CONTROL_ROOM/`, `HQ_HANDOFF/` and `rawlsing_next/` are untouched.
- **Zero `rawlsing_next/**` changes.** Tree `b0c1ab472cde033e21f1c2f63fbcbea2f0cccef0`
  is identical at `9a5752a8`, `8f7efe690`, `01256977`, `39015a90`, `f8c8e2e4`,
  `8ff40d37` and at my review tip. Tree identity is a superset guarantee: it covers
  every production and test file, not only the pinned ones.

## §2 Blob conservation

All **14** blobs recomputed by me at head, at C4A and at C4C3 — identical at all
three, and equal to every declared value:

5 C1 owner blobs, 6 accepted C3 blobs, the C11 facade, the named positioned-subject
consumer, and the Route-B producer — **14/14 exact, zero drift**.

Imported evidence: the fan-in's `01` artifact lists 36 entries. I recomputed each
path's head blob against its blob at the pinned source commit:
**36/36 exact, zero drift** (C4B 10, D2P 16, C4C3 10).

## §3 O1-C01 combined tree, and the Route-B producer question

The combined tree genuinely binds every identity O1-C01 names. AT07 successor
identities agree **4-way** across Omega-1, C4B, the fan-in lineage artifact and the
executable freeze.

**The Route-B producer binding is correct, and I established that independently
rather than accepting the fan-in's word for it.** C4B's authority freeze names six
components and no Route-B producer, so the fan-in's disclosure
`FAN_IN_OBSERVED__NOT_NAMED_BY_C4B` is factually accurate. My independent
determination:

- `rawlsing_next/pre553_route_b_production.py` is the **only** module in the whole
  330-file `rawlsing_next/` tree declaring
  `PYAT_M01_ROUTE_B_PRODUCTION_COMPOSITOR@1.0.0`.
- It is the **only** module exposing `execute_route_b_production`.
- Its docstring and imports show it does exactly the planned job: it packages
  already-governed PRE553 owners (source-backed C11 facade, C11 repository,
  discovery-exact, empirical authority/objects, carrier execution) into a
  deterministic Route-B production result and replay receipt, and explicitly
  creates no new semantic authority.
- Its blob `2385cd32…` predates the fan-in (`903c262e4`) and is unchanged at C4A
  and head. The fan-in added the *binding*, not the module — consistent with zero
  production changes.

**Conclusion: this is the correct current Route-B production/compositor owner for
the planned C4 full LiTS route, not an incidental module.** The fan-in's own
labelling was conservative and correct.

Three typed residuals follow (R1, R2, R3 in `06`).

## §4 Source-free court continuity

- **C1 454/454.** The 15 declared per-file counts sum to exactly 454, and the
  receipt belongs to this lineage through the verified ancestor merge `9a5752a8`.
- **Authoritative C3 court is exactly six files / 55 tests**, per-file
  `[9, 8, 13, 9, 6, 10]` = 55, reproduced identically across two invocations
  (77.79 s and 44.25 s), on the combined tree `8f7efe690`, with `rawlsing_next`
  tree hash identical at both its own HEAD and the qualified tree.
- **No supplementary failure was promoted into, or removed from, the authoritative
  denominator.** Both wider sweeps survive as labelled residual evidence: C4A's
  25-file `530 passed / 3 failed` and C4C3's supplementary `48 passed / 11 failed /
  1 skipped`. Every failure has a named root-cause class and none is attributed to
  the anchor runtime.
- The one direction of movement is an **inclusion**, disclosed and explained: C4C3
  retired C4A's exclusion of `test_pre553_source_backed_c11_facade.py` (10 tests)
  into the authoritative court, because C4A's exclusion was purely a missing-pandas
  artefact. That is not a silent promotion.

## §5 O1-C02 workload freeze

All eight source SHA-256s agree across **Omega-1, C4B, the fan-in and the warrant
candidate**. Read economy agrees 3-way: fresh full route `{SRC27}`, bounded fresh
physical-only `{SRC02, SRC06, SRC08, SRC12, SRC14, SRC26}`, retained comparator
`{SRC35}`, excluded fresh reads 0, substitutions 0.

D01 for SRC08/SRC12 remains **metadata-only** with zero row-data reads, zero
selected columns and no full-source decode — no semantic widening. The physical-only
six remain physical-only. LiTS B01 bindings resolve exactly to C4B's accepted
values: respondent event slots `q301_2`/`q301_7`, coordinate fact slots
`country, city, region, tablec, tabled`, `default_weight_measure_fact false`, and
projection authority URN
`urn:rawlsing:pre553:as2a:lits1-projection-authority:sha256:9dd1e6b7…`.

## §6 O1-C03 oracle and preimage custody

All fourteen Omega-1 `identity_rules.full_route_oracles` values match the freeze
exactly — LiTS source/closure/checkpoint/oracle identities and the 50/77/60/50
counts; WVS source/release/replay/oracle/frontier identities and candidate count 46.

I **independently upgraded two things** that the fan-in only carried:

- WVS `oracle_document_sha256` `9d11a480…` is the exact SHA-256 of git blob
  `9eecf801afa2c9f3d9140b4e5fb79fb14fc1fe20`, which is
  `WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json`
  at head. Verified against bytes.
- Packet manifest `46b38c21…` is the exact SHA-256 of `08_PACKET_MANIFEST.json`.
  Verified against bytes. All **9 of 9** `SHA256SUMS.txt` entries recomputed and
  matched.

I reproduced the D2P closure counts from the in-repo packet: 24 AuthoritySnapshot
rows, 208 per-object rows (50 receipt + 60 fact + 35 predicate + 63 query), 50
candidate-receipt rows with 50 distinct candidate hashes and 50 distinct receipt
refs, 50 P2 rows with 18 memberwise mappings and 50 distinct candidate hashes.

**Adjudication on sufficiency at this grain: sufficient.** The checkpoint *document*
SHA-256 plus the byte-verified in-repo packet, with `zero_reconstructed_semantic_rows:
true` and D2P's ruling that nothing was inferred or summarised, is adequate
executable custody for a source-free freeze. Fresh output may not author expected
truth; the seven difference classes must be classified before the run continues and
an unclassified difference is itself a STOP; unexpected differences fail closed.

**I did not upgrade, and expressly decline to upgrade, `checkpoint_identity
3fab15f3…` or `canonical_closure_identity f264dd8f…`.** D2P's own packet marks both
`NOT_VERIFIED_HERE`, and D2P instructed HQ in writing not to read them as verified.
The fan-in preserved them as labels. Correct.

## §7 O1-C04 D02

SRC14 binding is exact: SHA `5469e3b3…`, variable `v372`, ordinal 466, fixture
`EVS08_DATE_MISSING_V372`, fixture blob `12f6adb7…` which I confirmed resolves at
its named tip `3bc063aa` at the exact declared path, rendered witness
`1582-10-13`, counts `1917 / 64363 / 0 / 66280` (1917 + 64363 + 0 = 66280 —
arithmetically consistent), class `TYPED_DATE_USER_MISSING_SENTINEL`, authority
nonsemantic.

C4C3's synthetic source-free observation is real and I checked its details against
probe `D02-5`: built-in `datetime.date`, carrier `python.datetime.date@1`, pandas
dtype `object`, and payload `06 2e 0a 0e` (big-endian `>HBB`, year 1582, month 10,
day 14). The fan-in's payload string matches C4C3 **character for character**.

The decisive control `dates_as_pandas_datetime=False` is present and `False` in
both C4C3's freeze and the fan-in's.

**The historical rendering was not used to infer the subclass, and could not have
been.** Probe `D02-1` shows the accepted codec normalises `date`, `datetime` and
`time` by exact runtime *type*, producing different payload widths for each. The
carrier therefore comes from the reader's arrival type, not from the rendered
witness. Real SRC14 runtime subclass correctly remains a warrant-time observation,
and the freeze says so.

## §8 O1-C05 runtime and reader-lane law

Execution surface confirmed against C4C3's environment lock:
`C4C3-DARWIN-X86_64-ANCHOR/CPYTHON-3.11.3/PYREADSTAT-1.3.6/PYARROW-25.0.1/PANDAS-2.3.3/NUMPY-2.4.6/PYTEST-9.1.1`
on macOS 13.7.8 (22H730), Darwin 22.6.0, x86_64.

- **Actual executing interpreter, not a zero-byte launcher.** C4C3 executed
  `/…/c4c3-env/bin/python`, resolving to the `cpython-3.11.3-macos-x86_64-none`
  standalone with version string `3.11.3 (main, May 7 2023, 19:01:25) [Clang
  16.0.3]` and a recorded base-interpreter SHA-256 prefix.
- **Historical C3 freeze hash reproduced byte-for-byte**, `9cde8e5a…`, with zero
  differences across all 13 historical packages.
- **Reader options: 5 explicit + 11 inherited.** I compared all 11 inherited values
  key by key against C4C3's `frozen_reader_contract_for_C4.inherited_and_frozen`.
  **11/11 agree**, including `dates_as_pandas_datetime: False`.
- No install-on-import (0), no silent dependency upgrade (0), duckdb deliberately
  absent and confirmed off-path.
- **P2X gates are not on the C4 path — and I re-derived this independently.** My
  own static transitive-import closure over the five declared C4 layers is
  **exactly 21 modules and reproduces C4C3's list exactly**, module for module.
  The delta modules introduce no dynamic-loading primitive, no `subprocess`, no
  `duckdb`, and no edge to any `ee_p2x_*` or `fiabc_*` module. The only `__import__`
  hit is the stdlib-literal `__import__('json')` C4C3 already classified benign.
- The physical-metadata digest is correctly reader-lane bound, with the measured
  latin1-vs-None digest pair and its cause (encoding and authority_status inside
  the digest payload).

**RES-1 / RES-2 / RES-3 — each correctly nonblocking for the freeze and correctly
constrained for future live execution.**

- **RES-1** Stata extended-missing dual-shape branch is not source-free round-trip
  testable in pyreadstat 1.3.6 (`write_dta` does not surface `missing_user_values`;
  reader reports both `missing_user_values` and `missing_ranges` empty). C4C3
  classified it `UNPROBED`, not a pass, and deferred it to explicit real-LiTS
  observation under the warrant, with a STOP law if the observed token shape falls
  outside accepted dual-shape handling. The repository independently corroborates
  it with its own skip at `test_pre553_sr06_decoder_carrier.py:268`. Correct.
- **RES-2** `pandas.Timestamp` subclasses `datetime.datetime`, so the exact-type
  check misses it and `_jsonable` collapses it to `str`; naive and tz-aware
  renderings differ (measured in `D02-3`). It did not arise in this lane. The freeze
  forbids widening the carrier and makes a Timestamp arrival a fail-closed STOP.
  Correct.
- **RES-3** numpy `datetime64` unit determines arrival typing. Correctly bounded by
  numpy 2.4.6, with the freeze stating that a different numpy voids the O1-C04
  binding. One incompleteness in the restatement — R6.

## §9 O1-C07 / C08 accounting and failure law

- **Workload pass is not OS-level open.** The freeze states this explicitly and
  correctly, and its hardened SRC27 note (existence check, full hash pass, metadata
  read, full compatibility read — four separate accounts) matches Omega-1's exact
  prohibition on reading "one pass" as "one file open".
- Existence, hash passes, path-level opens, metadata reads, header-prefix reads,
  decoder invocations, selected-column reads, full reads, byte counts and retries are
  ten separate mandatory accounts, each requiring a stated measurement basis.
- Required zeros all present and mutually consistent across the warrant and the
  accounting law: WVS fresh reads 0, excluded fresh reads 0, Candidate A/B/C 0,
  measured P2X 0, respondent pooling 0, new cross-source joins 0, SRC08/SRC12 row
  data reads 0.
- Ten stop triggers, six absolute prohibitions, null-with-typed-reason reporting
  with a worked example, and corrected rerun requiring new HQ-bound authority.

**Zero-retry challenge — adjudicated: NO CONFLICT.** C4B froze immediate-stop on any
hash/config/authority/oracle mismatch and set **no numeric retry budget**. Its
"retries must be separately counted and reason-coded" clause is a *governance* law
conditioned on a retry occurring, not an authorisation of one. Omega-1 O1-C08
routes any corrected execution through "separately bound authority/commit/runtime
and the issued new-run/retry law", which is exactly what the freeze does. A budget
of 0 is strictly tighter than C4B, is the correct direction given no permitted
variation remains to explore, and contradicts no frozen required retry law. The
fan-in disclosed its reasoning rather than inventing headroom. Correct.

One repair is required, but at issuance — R9.

## §10 O1-C09 / C10 retention and the all-35 ledger

Recomputed from C4B's ledger independently:

- 35 sources, source ids complete and equal to `{01..35}`.
- 280 cells, exactly `{F1…F8} × 35`, **uniform 8 cells per source**, 35 distinct
  sources.
- 8 selected, 27 excluded; 8 + 27 = 35.
- 64 selected cells, 216 excluded cells.
- **Zero cells carry a PASS or PROVED state.** Every one of the 280 is pre-C4
  `NOT_ASSESSED`, and every one carries the explicit `update_law`: no cell changes
  state without an exact C4 receipt at that cell's proved grain.
- Excluded sources retain explicit dispositions and none disappears from accounting.

Selected-set success therefore **structurally cannot** become `ALL35_PASS`,
eight full semantic routes, or unrestricted F6/F7.

All nine claim ceilings are identical in content *and order* across Omega-1, C4B and
the fan-in. The C2 epistemic-origin residual is preserved as
`UNRESOLVED__NOT_MISSING_PROVED`. The C1 fresh-process bridge limitation is
preserved, and the *forbidden* provider→consumer→lifecycle bridge is recorded as
forbidden rather than glued. C7 remains `HELD`. Eleven retention requirements and six
separately-labelled evidence grades are preserved.

## §11 O1-C06 warrant candidate

Every commission-required property holds:

- `warrant_status` = `CANDIDATE_ONLY__NOT_ISSUED__NO_RAW_ACCESS_AUTHORIZED`
- `signed` false, `authorizes_access` false, `issued` false,
  `execution_authorized` false, `issued_by` null, `issue_date` null.
- Exactly 7 fresh-read sources; **SRC35 absent from `authorized_sources.keys`**
  with an explicit exclusion reason. Its SHA-256 correctly appears only under
  `oracle_bindings`.
- All seven `access_locator` values are the explicit unfilled placeholder
  `<REQUIRED_FILL_IN_SLOT__SOURCE_LOCATOR_FILL_REQUIRED_BEFORE_WARRANT_ISSUANCE>`.
- Source SHA, operations, reader lane, runtime/surface, authority, D02 witness
  binding, failure law, retry budget (0 per source) and retention/privacy are all
  bound per source.
- No raw-storage search was performed, and hashing/stat/metadata explicitly count as
  source access.

**Independent corroboration of the no-search claim, structurally.** I swept the
entire twelve-file fan-in packet for absolute paths of any form
(`/Users/`, `/Volumes/`, `/private/`, `/var/folders/`, `/mnt/`, `C:\`): **zero
hits**. Every `.sav` / `.dta` string in the packet is a bare *filename* from
`source_file`, never a path. If a locator had been searched for or discovered, it
would very likely have leaked into an artifact. The structural evidence corroborates
the asserted negative.

**I recomputed the candidate SHA-256 from the git blob at head:**

```
d57420f8016bf49cc0353f39dcd2271e6f370c3bd9b7e81f08466c0a1f574e0a
```

This matches the declared value exactly.

**Adjudication on locator fill: correctly a warrant-issuance blocker only, not a
source-free freeze blocker.** Omega-1 O1-C06's acceptance operates *under* the
warrant; the freeze sits upstream of issuance and its own
`issuance_blockers_summary` correctly lists the locator fill alongside the two
unset approvals, the unsigned state, and the outstanding independent review. The
commission forbade searching raw storage, and no search occurred.

## §12 Internal consistency and cross-artifact hashing

- All **10** JSON artifacts in the fan-in packet parse. (The fan-in claimed 7.)
- All **8** `lane_internal_references` digests recomputed against head blobs: **8/8
  agree**, including the warrant candidate's own digest.
- D2P `SHA256SUMS.txt`: **9/9 recomputed and matched.**
- Source SHA agreement across workload, oracle custody and D02 binding: confirmed.
- All-35 arithmetic: confirmed above.
- D02 fixture blob resolves at its named tip: confirmed.
- The two anchor pinpoints Omega-1 forbids inheriting by name alone are kept
  distinct, with the finding that the C3 source-free anchor records no OS,
  architecture, or reader-library version and is therefore not reader-side physical
  evidence.

**Three denominators are mis-stated in the fan-in, always conservatively (R11).**
No evidence is missing and nothing is overstated.

## §13 Open items — my adjudication

| # | Fan-in open item | My classification |
|---|---|---|
| 1 | Seven source locators unfilled | **Blocking to warrant issuance / live execution only.** Correctly typed. Not a freeze blocker. |
| 2 | Route-B producer is fan-in-observed | **Advisory / nonblocking** — and I now supply the independent evidence that the binding is correct and unique. What remains is HQ confirmation, not repair. |
| 3 | No repository dependency lock | **Advisory at freeze grain; blocking to live execution unless re-qualified.** I independently confirmed zero lock files — and found **three further non-durability facts** the fan-in did not disclose. Elevated to **R7**. |
| 4 | Zero-byte framework launcher; qualified interpreter separate | **Advisory / nonblocking.** Verified: the executing interpreter is the 3.11.3 standalone with a recorded hash prefix. The same durability caveat as R7 attaches to that binary. |
| 5 | 3.4 GB checkpoint not present on StarriyMac | **Advisory / nonblocking.** Correctly scoped. It *was* verified on NoviyMac by D2P (`identity_gate: PASS`, observed SHA `2704fd3f…`, observed bytes 3 404 445 161). Open only against StarriyMac custody, structurally impossible there. |
| 6 | 120 giant deferred-member digests checkpoint-side | **Advisory / nonblocking.** Confirmed arithmetic: 60 `EmpiricalFact` rows × 2 deferred members = 120. D2P accepted this at B002 grain by explicit ruling. |
| 7 | D2P extraction not byte-replayed on StarriyMac | **Advisory / nonblocking.** Structurally impossible there; open against NoviyMac custody. |
| 8 | Two identity labels recorded-but-unverified | **Advisory / nonblocking — and MUST NOT be upgraded.** D2P marks both `NOT_VERIFIED_HERE` and instructed HQ in writing not to read them as verified. The fan-in preserved them as labels. I did not upgrade them. |

Two further findings of my own require action at a later stage:

- **R9 — blocking to warrant issuance, nonblocking to this freeze.** C4B's warrant
  template carried a per-source `source_access_accounting` block with seven
  `REQUIRED_EXACT_COUNT` slots for all seven sources. The fan-in's warrant candidate
  replaced these with a single global account list; the per-source slots are gone
  from the warrant instrument. O1-C06 requires the warrant to bind per-source
  *read limits*. Per-source expected counts do exist — but in artifact `07`, not in
  the warrant. Restore the per-source accounting slots at issuance.
- **R7 — blocking to live execution unless re-qualified, nonblocking to this
  freeze.** The qualified environment is not durable and not
  repository-reconstructible.

Full typed residual schedule with severities in
`06_OPEN_ITEMS_AND_RESIDUALS.json`.

## Why this is an approval and not a rework

No finding invalidates any of the fan-in's O1-C01…O1-C05 closures. The freeze is
lineage-clean, blob-exact, correctly scoped, internally consistent on every
substantive claim, and honest about its limits — it disclosed its own Route-B
provenance gap, its own authoring error, its own unverified identity labels and its
own non-verifications rather than glossing them.

The two genuinely new substantive items I found are both repairable before the
stage that needs them, and one of them (the closure-figure tension) I have already
closed affirmatively with my own computation. The three bookkeeping errors are all
in the conservative direction. Nothing here warrants `CHANGES_REQUIRED` at the
source-free grain, and nothing rises to `ESCALATE_WITH_COUNTEREXAMPLE`.

An approval here is not a licence to execute. HQ may resolve and fill the seven
locators, restore the per-source accounting slots, and then issue or obtain the
exact O1-C06 warrant. It must not itself authorise raw-source execution.

## Constraints observed by this review

Raw survey source access **0**. No file opened, stat-ed, hashed, metadata-read,
decoded or materialised. No raw-source storage searched. No source locator
discovered, inferred or filled. C4 not executed. No live reader invoked. No
production code mutated. Warrant not issued. No self-adoption. No reading of the
parallel A-lane review branch. No merge of the three unreachable authority inputs
into this branch — all were read with `git show <ref>:<path>`.