# ANVIL CUT2 R5 — locality revocation repair closure

## Verdict

**`ACCEPT_SCOPED_TESTONLY_LOCALITY_FINDING`**

Author target: `cdee48f9d0403cb1e2f46e8c6630872b0e5623b3`
R5_LOCALITY_REVOCATION_REPAIR. Prior R4 review: `07c2409e...`.
Product remains `347baec...` / `a13d69c...`; cut1 G5 `092bf29...` untouched.

The exact R4 adapter defect is resolved and independently reproduced:

- **R4 old adapter:** after first yielded routing fact, revoke CURRENT; second
  fact yielded with no error — RED.
- **R5 corrected adapter:** same sequence; typed
  `DirectEstateError: current source/operation authority refused` — GREEN.
- **Original product control:** same typed refusal.
- Both adapter restorations asserted true.
- Valid iteration with CURRENT allowed: **600 routing refs**, canonical sorted,
  and exactly matches original product order.

## Minimal source delta

`CHANGED_SCRIPT.diff` adds only:

```diff
     for obj in sorted(materialized, key=lambda item: item.ref.key):
+        self._require_live()
         yield obj
```

No numerical, validation, ordering, index, schema, evaluator, store or product
change. The adapter remains test-only. The original product method is installed
only during the profile/witness process and restored in `finally`.

## Frozen corrected observation

From target `RESULT`/`child_result`/`raw.prof`/call tree (audited, not rerun):

- row-group reads: **3,965 → 50**
- profile Q wall: **18.296033755 → 7.582851973 s**
- row-group rows: 2,012,160 → 25,472
- compressed bytes: 634,219,540 → 7,942,218
- uncompressed bytes: 6,011,490,388 → 76,150,826
- full identity/semantic/refs/member/replay parity: **exact**
- cProfile `_object_from_row`: **9,637**; raw adapter counter `0` is the known
  wrapper blind spot
- external: exit `0`, no abort; wall **11.346635818 s**; sampled RSS
  **127,127,552 B**; scratch **30,368,896 B**; 40 samples; caps 120 s/2 GiB/2 GiB.

This is one sourcefree `f4_three_raw` instrumented observation, not a production
speedup. No new performance query, build, matrix, Batch, or 100k was run.

## Ordering / memory / exception limits

- Canonical ref order is restored before yield; valid 600-row order matches the
  original exactly.
- The adapter buffers one respondent/family list (600 routing facts in witness),
  not the full estate. No full-estate memory claim.
- Buffering still means a later malformed row raises before earlier objects would
  have streamed; this streaming exception-timing difference remains a test-only
  limitation and was not changed by R5.
- Process-tree RSS/scratch are sampled, not continuous; OS cache uncontrolled.

## Manifest / product identity

- R5 `MANIFEST.json`: **19** payload files; all SHA-256 verified.
- Product source unchanged: `pre553_direct_estate_i03.py` `8825832f...`,
  product `347baec...`, code/test `a13d69c...`.
- No product edit; no new store/index/evaluator/schema/science/issuer.
- The target `MANIFEST.json` still carries the prior `REVISE_EXACT_DEFECT`
  disposition metadata; the R5 findings/result and independent witness show the
  exact defect is resolved. This is a nonblocking author-manifest metadata
  correction; no self-acceptance.

## Owner handoff

Requested: `#1006` comment `6969187403` — **REQUESTED, NOT GRANTED**.
Production symbol remains `rawlsing_next/pre553_direct_estate_i03.py::
DirectEstateI03Session._respondent_family`. Required production change:
physical `gid,off` traversal + canonical ref-order restoration +
`_require_live()` before every yield + revocation-after-first-yield and full
parity regressions. No production adoption is claimed.

## Grades

- Engineering: exact R4 defect resolved at test-only adapter grade; locality
  mechanism supported as one observation.
- Science/authority: no original35/native/current/science/actor/protected grant.
- Integration: UNMERGED.
- No full-scale/100k performance claim.

## Artifact

`REVIEW_VERDICT.json`, `RECOMPUTED_LOCALITY.json`, `SOURCE_CHECKS.tsv`,
`revocation_witness.py`, `evidence/r5_closure_witness.json/.out`,
`snapshot/` frozen R5 target, `commands.txt`, `MANIFEST.sha256`.
