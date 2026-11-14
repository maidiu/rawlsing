# PROGRAMMA DELTA — #1006 follow-through r2

## Change class

HARNESS + TEST + PROFILE + RETURN ONLY.  No production or accepted-test edit.
No new engine/cache authority, no persistent index, no source bridge, no
optimization acceptance.  Reviewer-retained estates were opened read-only.

## Delta

1. Corrected the independent-G5-named defects: 29 (not 36) five-file S2-D
   tests plus 2 separate partial-binding tests; whole-worker vs writer-only RSS
   labels; and the disproved `_respondent_family ORDER BY ref`/small-LRU cause.
2. Measured the actual cause (native ref-key respondent traversal across
   physical row groups plus separate event cache) and implemented one runtime
   experiment, labeled `EXPERIMENT_NOT_IMPLEMENTED`, that traverses respondents
   in physical insertion order.  Exact fact/projection/replay/release parity is
   preserved at 1k, 10k and 100k selected; 10k reverse F2 and 3-way F4 also
   preserve parity.
3. Measured before/after: 100k selected 580.548 s / 204,125 reads -> 265.680 s
   / 5,784 reads; 10k selected/F2/F4 2.25x/2.45x/2.30x; 1k 2.15x/2.28x/2.03x.
4. Profiled the unchanged direct-I02 writer at 2k with call-boundary and
   cProfile receipts.  The inclusive proof is dominated by canonical semantic
   projection/identity/object validation and body_json reconstruction, not
   SQLite alone.  One smallest owner-consistent proposal is banked: per-build
   memoization of the already-computed immutable projection/hash for validation
   and insertion without removing any check.
5. Preserved known #999 native body-truth RED and all #997/#998/#1001/#1007
   ownership holds.  No blanket native correctness, optimized-engine
   acceptance or self-G5.

## Decision

`REVISE_EXACT_DEFECT_RECONCILED`; candidate available for a narrow S2-C/D
handoff after the qualified S2-A native body-truth descendant.  Stop.
