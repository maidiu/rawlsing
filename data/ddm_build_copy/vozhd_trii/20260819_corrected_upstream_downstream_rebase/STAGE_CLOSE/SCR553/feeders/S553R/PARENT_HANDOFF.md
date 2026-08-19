# S553R PARENT HANDOFF — SCR553 / M1

**Status:** `S553R_FEEDER_COMPLETE`  
**Authority:** non-dispositive feeder evidence only  
**Broad topology:** no counterexample found; remains frozen  
**Primary seam:** SCR553 governed-use temporal routing + M1 SCR553/SCR554 ingress/negative precedence

## 1. One-sentence handoff

Freeze V553 routing as an **exact governed-use decision**, not an admission-global classification: a direct basis may be lawful for `U1`, while `U2` over the same admission must route through V553 when it newly requests V553-owned temporal/comparability semantics; any required source relation/comparability authority is a separate prerequisite that V553 cannot infer, and any applicable temporal/source negative for `U2` blocks direct positive fallback for `U2`.

## 2. Candidate SCR553 routing contract

S553R recommends that SCR553 freeze a machine contract equivalent to:

```text
INPUT:
  A = exact positive StructuralEmpiricalAdmission
  U = exact governed downstream use identity
  Rsrc = separately-owned source relation/applicability/comparability refs + typed state
  Rtemp = requested V553 temporal operation(s) + exact authority refs
  N = applicable temporal/source negative/limit refs

PRECONDITIONS:
  A is applicable to U
  all source prerequisites required by U are exact and positively governed
  OR exact negative/unknown state is preserved as such

NEEDS_V553(A,U):
  true iff U requires new V553-owned temporal/comparability meaning
  not already lawfully complete in A for U

DECISION:
  if source prerequisite required by U is MISSING/UNKNOWN/DENIED/NONCOMPARABLE:
      no positive cross-source temporal result
      TEMPORAL_LIMIT only if exact V553 limit rule owns the attempted operation
  else if NEEDS_V553(A,U):
      require exact V553 operation authority
      if present: produce exact TEMPORAL_* result(s)
      if absent: negative/limit where governed, else no positive route
  else:
      V553 not required for U
      downstream direct basis may proceed only under its own exact rule/applicability authority
```

The contract must explicitly state:

```text
ROUTE(A,U1) != permanent routing class for A
```

and:

```text
HAS_TIMESTAMP | HISTORICAL_SOURCE | SAME_YEAR | ARTIFACT_PRESENT
!= NEEDS_V553
```

## 3. Candidate source-comparability contract

The source gate should be typed by **operation**, not a global `sources_are_equivalent` boolean.

At minimum distinguish:

- source relation not required for this single-source use;
- source relation positive for one exact temporal comparison/harmonization operation;
- source relation explicitly noncomparable for the operation;
- source relation missing/unknown/ambiguous;
- respondent linkage authority, if any, as a separate grant;
- pooling/sample/weight/nonduplication authority, if any, as a separate grant;
- estimand composition authority, if any, as a separate grant.

Required nonimplications:

```text
same year != source comparability
same label != source comparability
same canonical value != source comparability
same geography string != source comparability
provenance dereference != source comparability
source comparability != respondent linkage
source comparability != pooling
source comparability != estimand composition
TEMPORAL_KEY equality != source-universe equality
```

V553 may consume a positive/negative source relation result and create its own temporal semantic/limit under exact authority. It may not become the source relation court.

## 4. Candidate temporal-negative precedence

For one exact use `U`:

```text
APPLICABLE_TEMPORAL_OR_SOURCE_NEGATIVE(U)
=> DIRECT_POSITIVE_BASIS_FOR_THE_BLOCKED_SEMANTIC(U) is forbidden
```

Examples:

- `INSUFFICIENT_COMPARABILITY` cannot fall back to direct basis for the cross-source comparison;
- `INSUFFICIENT_PERIODS` cannot fall back to the latest point as persistence evidence;
- `BASELINE_UNAVAILABLE` cannot invent/substitute a baseline;
- `CONFLICT` cannot select newer/higher-support/local source;
- `MISSING_AUTHORITY` cannot be reclassified as `TEMPORALLY_COMPLETE`.

This precedence is **use-scoped**. A negative on U1 does not globally invalidate the admission for a distinct U2 whose own predicates independently pass.

## 5. SCR553 local acceptance checks proposed

S553R recommends SCR553 refuse local closure unless all are machine-testable:

1. Exact governed use identity is present in the route decision.
2. The route decision names requested temporal semantic(s), not only time metadata.
3. Source relation/applicability prerequisites are exact refs with typed states.
4. V553 operation authority is exact/versioned for every positive transformation.
5. `TEMPORAL_LIMIT` is a first-class output and replay dependency.
6. Unknown/missing source relation cannot become positive comparability.
7. Unknown/missing V553 operation authority cannot become a direct positive basis for the same temporal semantic.
8. One admission can produce different route decisions for different uses.
9. Raw EmpiricalFact ingress is rejected.
10. Historical replay reproduces the exact route reason under historical authority snapshots.

## 6. M1 seam checks proposed

M1 should jointly prove SCR553 + SCR554 behavior for at least these cases:

- direct U1 / temporal U2 over same admission;
- direct point use despite timestamp/history metadata;
- source relation unknown -> no positive temporal basis and no direct comparative fallback;
- source relation positive for comparison but no pooling authority -> comparison may proceed, pooling does not;
- V553 negative physically coexists with direct admission -> negative blocks the same semantic use;
- same negative does not poison an unrelated direct use;
- no-op/legacy V553 artifact does not win precedence by existence;
- unknown equivalence/precedence remains SCR554 fail-closed work rather than a V553 routing guess.

## 7. Boundary with SCR554

S553R deliberately does **not** freeze:

- V554 duplicate-equivalence key;
- direct-versus-temporal basis serialization;
- V554 F1/F2/B1 canonical IDs;
- exact V554 precedence implementation.

Those remain SCR554/M1 jurisdiction.

S553R supplies the upstream ceiling SCR554 must not violate:

- basis eligibility is use-scoped;
- source distinctions remain exact;
- an applicable V553/source negative for the same use cannot be erased by choosing a direct basis;
- unknown source relation/temporal need/authority does not create a positive basis.

## 8. Boundary with later structural stages

S553R does not create source pooling/composition authority for V555/V556. If a later higher-order use combines source-derived routes, that later operation still requires its own exact composition/compatibility authority under the frozen R03 law.

A successful V553 temporal comparison proves only the semantic relation V553 was authorized to create. It does not imply a pooled respondent universe or higher-order structural interaction permission.

## 9. Preserved negatives

SCR553/M1 should ensure these remain distinguishable where applicable:

- `NONCOMPARABLE`;
- `MISSING_SOURCE_AUTHORITY`;
- `MISSING_TEMPORAL_OPERATION_AUTHORITY`;
- `INSUFFICIENT_PERIODS`;
- `BASELINE_UNAVAILABLE`;
- `CONFLICT`;
- `AMBIGUOUS_SUPPORT`;
- `MALFORMED_INPUT`;
- `UNKNOWN`;
- observed zero as a positive measurement state distinct from absence/noncomparability.

No negative may be converted into a positive absence/no-pressure claim merely because no positive temporal relation was emitted.

## 10. Escalation posture

S553R found:

- no authority conflict requiring `S553R_BLOCKED_AUTHORITY_CONFLICT`;
- no exact broad-topology contradiction requiring `S553R_BROAD_TOPOLOGY_COUNTEREXAMPLE_CANDIDATE`.

The remaining work is bounded SCR553/M1 contract closure under the already accepted R03 topology.

**Return token:** `S553R_FEEDER_COMPLETE`
