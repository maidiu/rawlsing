# ANVIL authenticated routing access — implementation

## Status

**Implemented and frozen for distinct independent review. No self-acceptance.**

- Branch: `agent/anvil-engineering-cut1-20261117-r1`
- Start HEAD: `15afd22f6d55fe3d208d0a3b63d802de2b4e6f13`
- Accepted product baseline: `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`
- **Code/test commit: `73b480080ede013770e0c887aa5aa82af3cfafb2`**
- Scope: exact session-owned routing locator slice
- Product changes outside authorized paths: **none**
- New tests/benchmarks/SQL/raw sources: only the authorized focused test; no SQL/raw.

## Changed paths

- `rawlsing_next/pre553_direct_estate_i03.py`
  - `DirectEstateI03Session.__init__`: exact `_RoutingLookup(self)` adapter.
  - `__enter__`: session SQLite `routing_locator` table with consumed
    respondent-first key order `(respondent,target,risk_set,fact_ref)` and
    physical `gid/off`.
  - `_build`: authenticates every routing body/ref/respondent/universe, checks
    physical family census and locator count, inserts locator rows once.
  - `_RoutingLookup.lookup`: exact respondent/target/risk query; validates
    physical ref and body identity; CURRENT before each yield; canonical ref
    order; all matching facts returned.
  - `indices_for`: passes exact adapter into `_ReleaseIndex`.
- `rawlsing_next/_pre553_query_common.py`
  - `_ReleaseIndex.routing_lookup: Any | None = None`.
- `rawlsing_next/_pre553_query_eval.py`
  - `_routing_fact_for` selection ingress only; existing conflict, absence,
    authority, member-set and evidence logic unchanged.
- `rawlsing_next/tests/test_anvil_authenticated_routing_access.py`

No reverse index, coordinate/weight access, persistent artifact, group cache,
SQL execution, or second evaluator.

## Bounded qualification

Existing tiny controlled prepared fixture; no raw or production source.

| Metric | Result |
|---|---:|
| Controlled respondents | 8 |
| Routing locator rows | 24 |
| Lookup calls / facts yielded | 40 / 40 |
| Prepared session S (build) | 58.398 ms |
| Parquet row-group reads total (build + two ops) | 220 |
| f4 candidate Q / baseline Q | 40.731 / 61.212 ms |
| f2 candidate Q / baseline Q | 28.639 / 39.734 ms |
| Result export O | 0.027 / 0.019 ms |
| Completed operations | 2 |
| Parent max RSS | 104,599,552 B |
| Retained/scratch | session SQLite temp only; no persistent artifact |
| H | Not separately isolated; fixture/admission outside timed session |

Exact parity for both f4 (weighted 3-target joint) and f2 (different target):
fact ref, full fact JSON, cells (including **1 observed-zero cell** in f4), risk
members, denominator members, used objects and authority refs. No performance
claim; the tiny fixture's 58 ms preparation is **not** amortized by the two
candidate-vs-baseline savings. Coordinate predicate case is absent from this
fixture; existing native focused suites cover coordinates/observed-zero.

Evidence: `evidence/qualification.json`, `qualification.out`,
`qualification.time`.


## Fixture readiness pin

`MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ROUTING_FIXTURE_READINESS_20261118` at
`ab0d54b18ffc8437f9736cd9534ed4536c4484b8` records **no retained weighted
k3 + coordinate combination**. The already-started matched comparison used the
tiny controlled f4 weighted 3-target joint and f2 different-target operation;
it was finished and not duplicated. No combined weighted-k3+coordinate claim
is made. Separate pinned existing nodes for coordinate, true-k3 and weighted
coverage passed: **3 passed, 29 deselected (0.19 s)**. The fixture lacks a
true distinct conflicting-routing candidate; locator multiple-yield and
CURRENT-between-yields are tested through a controlled test-only duplicate
locator row, while existing native conflict tests retain evaluator semantics.

## Regression

- Main focused/native/prepared/parquet/locality union:
  **86 passed, 0 failed, exit 0, 32.99 s**
- R03 v2 + prepared postconsumer + prepared Batch:
  **21 passed, 0 failed, exit 0, 21.32 s**
- Includes current/revocation, changed input/restore, missing/conflicting
  routing paths, bad body/locator, wrong root/source, native conflict/absence/
  authority handling, prepared Batch and first-consumer tests.
- New focused test also covers pinned full-family/authority parity, multiple yields,
  CURRENT between yields, locator removal, corrupt locator, CURRENT
  revocation, cleanup, and public parity.

Logs: `evidence/regression.txt`, `evidence/affected.txt`,
`evidence/focused.txt`.

## Key semantics

- The routing locator is derivative; all scientific semantics stay in the
  existing evaluator.
- Every matching routing fact is preserved in canonical ref order, including
  conflicting matches; existing conflict/absence/authority checks are unchanged.
- Filtered absence is trusted only after full routing family census and locator
  count validation.
- Every selected body is revalidated against held refs/respondent/universe/
  target/risk and physical locator.
- CURRENT is checked at session build/lookups and before each yield.
- Session SQLite is cleaned with the temp session; no durable generation.
- No second canonical dataset, fact cache, weight selection, coordinate index,
  alias authority, or PostgreSQL dependency.

## Limits / self-critical

- Tiny 8R fixture; not 128R/600, not 100k, no performance extrapolation.
- No coordinate predicate in the tiny fixture; covered only by existing native
  suites.
- H is not separately isolated; S/Q/O are scoped measurements.
- The new preparation is not amortized on two tiny operations.
- No old V550 product-parity claim.
- No protected merge/source/science/actor/current rights.
- Distinct independent review pending; no self-acceptance.

**STOP after commit/push/remote verification.**
