# PYAT #1006 — independent G5 R2 locality/writer recheck

**Verdict: `ACCEPT_SCOPED@SOURCEFREE_LOCALITY_EXPERIMENT_HANDOFF_READINESS`.**

This is a finite defect-specific recheck of the same #1006 nonauthor session.  It
does not accept a production repair, an optimized engine, native integrity or a
full 100k vertical.  The three R1 report defects are corrected; the measured
locality experiment reproduces with exact fact/projection/replay/release parity
at every executed scope, including a new unequal-weight adversarial case; the
writer profile attribution is independently reproduced with honest 2k limits.

## Identity and permissions

- Immutable author head: `2beb2b894076510cdedf8981aa73d15eafc7c816`.
- Code/tests commit: `1ca1c735a577a7524a0a26c15df8879cd88704e3`.
- Frozen production: `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`; the production
  diff from that head is empty.
- Author manifest: 65/65 files verified; all nine READER_ABI production blobs
  unchanged.
- R1 review remains authoritative historically:
  `0169fac9f3840800796c664eee462bbb8984bb42` (PR #1034).  R1 retained data was
  read only; do not delete/alter or commit it.
- Permission grade: **SOURCEFREE TEST_ONLY**.  No original35 bytes, source
  bridge, `.env`/keys, CURRENT/issuer, scientific authority, protected merge,
  or owner handoff was used or granted.
- Branch: `codex/pyat1006-independent-locality-recheck-20261113-r2`; new writes
  only under `WORKER_REVIEWS/PYAT1006_PHYSICAL_ECONOMICS_G5_R2/`.

## R1 defects — corrected and independently checked

| R1 defect | R2 status | Evidence |
|---|---|---|
| Wrong `_respondent_family` `ORDER BY ref` / small-LRU cause and proposal | **CORRECTED.** Author withdraws it; actual cause is native respondent traversal in ref-key order across physically ordered row groups plus a separate event cache. R2 candidate confirms physical traversal removes 35.3× of row-group reads. | `02_CORRECTED_R1_AXES.md`, R2 candidate counters |
| Claimed 36 S2-D tests | **CORRECTED.** The named five-file RUNBOOK group is 29; separate partial-binding is 2 (29+2=31); focused 31; own 6. No 36-test selection exists. | Author reconciliation + R1 independent run + R2 logs |
| 1k/10k “writer RSS” labels | **CORRECTED.** Those rows are whole-worker peaks. Writer-only 10k is 214,261,760 B (R1); 50k/100k were already writer-only. | `02_CORRECTED_R1_AXES.md` |

## Independently reproduced locality experiment

The same R1 estates were copied byte-for-byte to the R2 path; every manifest,
member hash, capsule pinned field and 15-file release identity matches the R1
originals and the author's `reviewer_sources.json`.  No R1 file was modified.

| scope | baseline | candidate | read reduction | exact parity |
|---|---:|---:|---:|---|
| 100k selected (same estate) | R1 543.026 s / 204,125 reads | R2 294.087 s / 5,784 reads | 35.3× reads | fact ref `87c3f058…` equals R1 baseline; release ref exact |
| 10k selected | 52.195 s / 20,157 | 22.896 s / 588 | 34.3× | fact/projection/replay/release exact |
| 10k reverse F2 | 51.264 s / 20,153 | 21.721 s / 614 | 32.8× | exact |
| 10k 3-way F4 | 56.011 s / 20,161 | 25.372 s / 588 | 34.3× | exact |
| 1k selected | 4.975 s / 1,784 | 2.275 s / 61 | 29.2× | exact |
| 1k reverse F2 | 4.715 s / 1,785 | 2.295 s / 63 | 28.3× | exact |
| 1k 3-way F4 | 4.934 s / 1,784 | 2.575 s / 61 | 29.2× | exact |

100k candidate details: wall 294.087 s, CPU 263.166 s, tree RSS 2,803,986,432 B,
temporary SQLite 1,301,057,536 B, `SUPPORTED`, denominator 50,000.  The author's
paired run was 580.548 → 265.680 s; this review's R1 baseline was 543.026 s.
Different processes/loads mean the wall factor is indicative (R2 1.85× vs author
2.19×); read counts and fact identity are exact.  The author's “2.81 GiB” is
2.81 decimal GB (2.61 GiB); no cap issue.

Sort audit: the candidate override returned physical order only once per query
over all `RespondentIdentity` values (100,000 values at 100k), with 100,004
fallback key sorts and 4 fallback other sorts.  Source inspection finds exactly
three respondent traversals in `_pre553_query_eval.py` (lines ~364, 448, 697);
all other sorts are non-respondent and unchanged.  Output canonicalization sorts
risk/denominator refs, cell keys and used objects, which the exact parity
receipts confirm.

## New adversarial unequal-weight/order-sensitive case

A legitimate sourcefree 128-respondent release was built with exact unequal
weights `1/3, 5/7, 11/13, 17/19, 0.1, 0.2, 0.30000000000000004, 7/3, 2/9,
13/11`.  The weighted query has two cells with unequal fractions
(958,736/21,945 and 534,236/21,945); a two-target weighted F4 has four cells with
nonzero unequal fractions.  Baseline, physical-order candidate and native oracle
all produce the same fact ref, full projection SHA-256, replay ref and release
ref.  This is the required check that traversal order does not change canonical
probability/fact/replay output.

## Writer profile check

Independent 2k unprofiled wall: 41.425 s (author 38.277 s).  Direct-I02 proof is
inclusive at 27.629 s; reread/re-encode 13.364 s; root hashing 0.202 s; sum
41.195 s against 41.425 s wall.  First-pass `_Sink.add` 7.207 s contains
`_row` 6.685 s plus flush 0.518 s; verify `_row` 6.343 s; `_row` total 13.028 s
is nested, not additive.  cProfile wall 116.386 s is used only for relative
shares: 96,000 `semantic_hash` calls for 22,501 first-pass objects (4.266 per
object), 40,992 `semantic_projection` calls, SQLite `execute` 4.354 s = 3.74%
of inflated wall, `canonicalize` exclusive 12.470 s and `isinstance` 13.372 s.
The direct proof is therefore not “SQLite only”; canonical projection/identity/
object validation and JSON/body reconstruction dominate.  The bounded memo is a
**proposal only, not implemented and not measured as a gain**.  No writer
optimization is accepted.

## Guards and preserved holds

- Candidate-native 48-respondent oracle, changed C, old-root restore, weighted,
  repeated, F2 and F4: exact.
- Denied CURRENT, wrong source root, omitted locator and omitted family member:
  all refuse.  Candidate selected still succeeds with `C11Repository.__init__`
  and `pq.read_table` blocked, so no full-graph/whole-table fallback.
- #999 coherent native body-truth RED remains external and unrepaired.
- #997 issuer binding (0 QUERY / 1 DISCOVERY) remains another owner's hold.
- #998 joined vertical, #1001 full 100k/6 GiB vertical and #1007 source rights
  remain held.
- Candidate I05/grouped execution, 100k F2/F4, 100k all-seven readers and
  10/10 repetitions are **NOT_RUN**; no proxy claim.
- The candidate relies on `DirectEstateI03Session.respondents` being physical
  insertion/row-group order; that held for these estates, but any future reader
  that reorders the mapping needs requalification.
- #1008/#1010 Browser duels were not monitored, messaged, managed or fetched.
- Provider quota/cost: **UNOBSERVED**.

## Accepted / not accepted

Accepted at sourcefree measured scope: the R1 defects are corrected; the
physical-order locality experiment is an exact-at-executed-scope,
handoff-ready candidate; writer attribution and its 2k limits are honest.

Not accepted: production patch/ABI, owner handoff, optimized engine, writer
memo gain, native engine soundness, 100k F2/F4/I05/all-seven, true source
decode, #998/#1001 vertical, #1007 rights, science/CURRENT/issuer, protected
merge.  No repair or A/B campaign was performed; stop after this terminal
recheck.
