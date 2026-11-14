# PROGRAMMA DELTA — PYAT #1006 independent locality/writer R2 recheck

## Change class

REVIEW + PROBE + EVIDENCE ONLY.  No production, accepted test, author harness
or author evidence file was edited.  New files are confined to
`WORKER_REVIEWS/PYAT1006_PHYSICAL_ECONOMICS_G5_R2/`.  R1 data was copied
byte-for-byte for isolation; it was not modified, deleted or committed.

## Result

**`ACCEPT_SCOPED@SOURCEFREE_LOCALITY_EXPERIMENT_HANDOFF_READINESS`.**

The three R1 defects are corrected: the old `_respondent_family ORDER BY ref` /
small-LRU cause is withdrawn; the five-file S2-D group is 29 (+2 separate
partial-binding, 31 total), not 36; and the 1k/10k RSS rows are whole-worker
peaks.

Independent R2 reproduction on the same R1 releases:

- 100k selected: R1 baseline 543.026 s / 204,125 reads → R2 candidate 294.087 s
  / 5,784 reads; identical fact ref `87c3f058…`, `SUPPORTED`, denominator
  50,000, release ref exact.  Candidate tree RSS 2,803,986,432 B, temp SQLite
  1,301,057,536 B.  Author paired run 580.548 → 265.680 s.
- 10k selected/F2/F4: 2.28×/2.36×/2.21× with exact fact/projection/replay/
  release and native-oracle parity.
- 1k selected/F2/F4/weighted: exact parity, 1.9–2.3×.
- New unequal-weight adversarial release: two-cell weighted and four-cell
  weighted F4 exact against baseline and native oracle with unequal exact
  fractions; traversal order does not change canonical facts/replay.
- Sort audit: only one physical respondent traversal per query; 100k values at
  100k, all other sorts fall back.  Three source respondent-sort sites only.
- Guards: candidate preserves denied CURRENT, wrong source, omitted locator,
  omitted family and changed/restore exactness.

Writer profile: independent 2k unprofiled 41.425 s; direct-I02 proof 27.629 s
inclusive (not SQLite-only), reread 13.364 s, root 0.202 s; cProfile 96,000
semantic hashes / 40,992 projections / 22,501 objects, SQLite execute 3.74–4.22%
of inflated wall.  The bounded memo remains a proposal only; no gain claimed.

## Accepted / held

Accepted: sourcefree measured locality experiment and handoff readiness at the
executed scopes; corrected R1 report; writer attribution with 2k limit.

Held: production patch/ABI or owner handoff; writer optimization; 100k F2/F4,
I05/grouped, all-seven and 10/10 repetitions; #999 native body-truth RED;
#997 issuer binding; #998 joined vertical; #1001 full 100k/6 GiB; #1007 rights;
science/CURRENT/issuer/protected merge.  Provider cost `UNOBSERVED`.

Stop after this terminal recheck; no repair loop, A/B campaign or downstream
dispatch.
