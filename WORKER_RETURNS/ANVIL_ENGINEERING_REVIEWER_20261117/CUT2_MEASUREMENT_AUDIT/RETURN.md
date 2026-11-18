# ANVIL R2 first bounded pair — measurement audit

## Verdict

**`ACCEPT_SCOPED_MEASUREMENT_WITH_ALIGNED_PHASE_CORRECTIONS`**

Target: `495796e5f7f10a0e25122d0ccc45e40b703c885c` — R2 first bounded
16-respondent / 600-question-binding / 8,622-event sourcefree pair.

This is a measurement/data acceptance at sourcefree TEST_ONLY grade, not a
performance, native, original35, 100k, science, current or protected acceptance.
No product edit, no rerun, no second pair.

## Aligned positive phase (derived from frozen raw JSON)

| Phase | Baseline | Prepared as-run | Prepared aligned positive |
|---|---:|---:|---:|
| Wall | 80.6244 s | 78.0472 s | **63.2445 s** |
| S index build | 14.3780 s | 5.4978 s | **2.7261 s** |
| Q native evaluator | 65.4039 s | 72.1034 s | **60.1765 s** |
| O export serialization | 0.0191 s | 0.0173 s | 0.0173 s |
| H admission (outside wall) | 0.2726 s | 0.2874 s | 0.2874 s |

- prepared positive wall = 78.0472 - negative/restore 14.8027 = **63.2445 s**
- prepared positive S = 5.4978 - negative 2.7718 = **2.7261 s**
- S saving = **11.6519 s**
- Q saving = **5.2274 s**
- wall saving = **17.3799 s**
- Q is **95.15%** of prepared aligned positive wall; S is **4.31%**
- The external child-wall cross-check is consistent: baseline 81.598 s;
  prepared 79.106 - 14.803 = 64.303 s; saving ~17.3 s.

The published headline `prepared 78.05 vs baseline 80.62` compares different
work because prepared includes the negative/restore phase. The aligned
comparison is the one above. This is one pair and **not a qualified speedup**.

## Corrections required to the author report

1. **Headline wall:** replace total-vs-total with the aligned positive wall; raw
   data support 63.2445 vs 80.6244, not 78.05 vs 80.62.
2. **S saving:** use 11.6519 s aligned, not 8.9 s computed from total prepared S
   that includes the restore build.
3. **Build row:** raw external supervision is 33.867 s / 199,135,232 B /
   100,068,948 B; the published 33.18 / 193,429,504 / 99,941,972 row is not
   supported by the raw samples.
4. **Scratch label:** 23,269,376 B is the internal session-component peak, not
   total scratch. External sampled scratch is 30,368,896 B for both modes; no
   separate total staging peak was measured.
5. **CPU/RSS/reads:** prepared aggregate fields include the negative/restore
   phase and have no separate aligned values. Do not present them as matched
   positive comparisons. Process-tree peak is 0.25 s sampling plus ru_maxrss,
   not continuous.
6. **Combined wall:** result top-level field is null; supervision carries
   `194.5758 s`.

## Geometry and payload claims verified

- 16 respondents, 600 native question bindings, 8,622 RespondentEvent,
  9,600 RoutingEligibilityFact, 16 weights, 7,099,520 retained bytes.
- Added 595 slots / 9,520 cells: 7,616 valid (80%), 952 typed MISSING (10%),
  952 NOT_ASKED (10%); 8,568 added events + 54 base = 8,622.
- Five distinct operations: selected weighted, F2 forward, F2 reverse, true
  same-person k3 F4, repeated MR. The 600 added slots are not all queried and
  are not a dense 600-event/respondent proof.
- Exact full semantic/identity/refs/member/replay parity true for all five.
- Full semantic/identity payload includes risk/denominator/provenance material;
  selected full semantic 35,256 B, identity 35,458 B, ref-only 234 B. The old
  1,885-byte refs-only smoke was a measurement defect and is correctly
  superseded.
- Q includes native fact construction/hash; O is post-call export serialization
  and is not added to Q. S is outside Q because `DirectEstateI03Session.__enter__`
  builds before `execute_empirical_query`. There is no Q/S/O double count.

## Supervision / limits

- Producer, baseline and prepared child exits: `0, 0, 0`; no abort.
- Caps: build 300 s, query 180 s, combined 720 s, process-tree RSS 2 GiB,
  scratch 2 GiB; actual combined `194.5758 s`; caps not exceeded.
- Process groups used; SIGTERM/SIGKILL on abort path; no actual abort occurred.
- OS page cache uncontrolled; one fresh pair is not a warm-cache claim.
- No native/original35/source/science/actor/current/100k/6 GiB, #998 or
  protected merge acceptance.

## Actionable cost decision

**Primary:** attack Q/native evaluator/read-path cost. Q is 60.1765 s, 95.15%
of prepared aligned positive wall.

**Strongest alternative:** index geometry/durability or Batch-forward wiring.
After reuse, S is only 2.7261 s / 4.31%; the S saving is already large (11.65 s)
but Q still dominates. Do not optimize O export serialization (0.017 s).

Do not start a 1/10/100 or fresh-Batch matrix until this measurement decision is
recorded. A qualified speedup, native, 100k or production claim is not made.

## Artifact

- `REVIEW_VERDICT.json`
- `ALIGNED_PHASE_TABLE.md`
- `RECOMPUTED_PHASES.json` / `.out`
- `recompute_phases.py`
- `SOURCE_CHECKS.tsv`
- `snapshot/` frozen target copy
- `MANIFEST.sha256`

Reviewer: `ses_e30c25800ffeT8XbyTuHekRCme`; same distinct nonauthor G5.
