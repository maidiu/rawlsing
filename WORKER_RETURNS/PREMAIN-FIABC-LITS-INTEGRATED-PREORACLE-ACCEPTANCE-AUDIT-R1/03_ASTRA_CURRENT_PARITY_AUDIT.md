# Courts 3–5 — ASTRA Expected Side / Current Side / P0–P4 Conservation

## Overall result

**BLOCKED**

The expected/current provenance split is sound and the empirical projections are strong, but candidate identity conservation is not lawful across the historical/current schemas.

## Court 3 — immutable expected side

**PASS**

Production code loads accepted ASTRA-D04-R2 only from exact commit:

`e631de162c582423639b7067a4f36b29f8aa4d89`

Exact pinned Git blobs:

- product — `26fa18d10d242f3db212f6ee3e6f28abee3327ac`
- 77-role receipt — `211e19bb17cd8e3c63418b686ac20508072cb7d7`
- source/replay receipt — `b2c70e992955853b540e498214c296ccc0e25b83`

The producer uses exact `git show <commit>:<path>` and separately verifies exact `git rev-parse <commit>:<path>` blob identity.

The accepted summary is built only from those immutable historical documents.

No expected empirical value is read from the current I05 result.

## Court 4 — current empirical side

**PASS**

The current source is decoded once.

The same retained `incidence` is used for:

- LiTS projection;
- exact accepted legacy/successor C11 repository;
- frozen R5B/F02 q310/q311 source scan;
- current candidate-neutral I05.

The current normalizer receives the full `ExactBoundedDiscoveryResult`, not only the reduced learned receipt.

It resolves each role's exact fact refs back to the corresponding current `EmpiricalFact` preimages and reads:

- exact raw denominators;
- complete located cell projections;
- exact typed state;
- exact risk-member refs/cardinality.

No second decode is introduced solely for parity.

## Court 5 — empirical quantities

### Frontier / roles / risk topology

**PASS apart from candidate identity domain described below.**

The summaries exact-compare:

- 50 candidates;
- 77 roles;
- exact frontier seal;
- lane counts 5/3/36/8/25;
- all 77 role fact states `SUPPORTED`;
- role result reuse = 0;
- exact accepted R2/R7/R27 count/root records;
- exact lane/role→risk-root designation.

The current query evaluator's exact risk-set successor law supplies the membership, and each normalized role must have the corresponding exact accepted member count.

### P0

Empirical support/denominator conservation is exact:

- target 1: 4377 / 24897
- target 2: 6440 / 24897
- target 3: 5226 / 24897
- target 4: 6972 / 24897
- target 5: 1882 / 24897

Cell location is preserved. A support mutation fails.

**Candidate hash equality itself is not lawful; see blocker below.**

### P1

The comparator conserves:

- exact witness cell [1,1];
- joint 1485 / 24630;
- marginal 0: 4377 / 24897;
- marginal 1: 2889 / 28325.

The accepted parser independently verifies the non-product cross-multiplication inequality.

**Candidate hash equality itself is not lawful; see blocker below.**

### P2

All 18 exact first-difference witnesses are represented and current witnesses are independently recomputed from the complete current CONDITION/BASELINE cell projections.

However the required logical identity conservation is incomplete:

1. immutable ASTRA rows contain an explicit `parameters` object:
   - `q301_2`
   - `q310`
   - `q311`
2. the accepted-side normalizer **drops `parameters`**;
3. current receipt `candidate_identity.query_roles` contains exact:
   - role;
   - predicate ref;
   - query ref;
4. the current-side normalizer **drops the CONDITION and BASELINE predicate/query identities** and preserves only the role names.

Therefore a P2 summary row contains only:

- candidate hash;
- terminal;
- first witness.

The commissioned requirement to conserve candidate identity, condition identity, baseline identity and lane/parameter mapping is not met explicitly.

### P3

Empirical conservation is strong:

- exact target cell 5;
- exact eight pooled/stratum fractions;
- recomputed pooled sign;
- recomputed three stratum signs;
- exact `EVALUATED_VALID_EMPTY`;
- exact mechanism `VALIDATION_FALSE__NO_CONDITIONAL_REVERSAL`.

Current P3 additionally requires every one of the eight role facts to be `SUPPORTED` with positive denominator before that mechanism may normalize as accepted valid-empty.

Thus zero support/unresolved/noncomparable emptiness cannot masquerade as the accepted mechanism.

**Candidate hash equality itself is not lawful; see blocker below.**

### P4

**PASS.**

ASTRA does not record P4 candidate hashes. The parity key is the exact target cell.

All 25 supports are keyed by the 5×5 coordinate. A positive-support permutation fails even with the same support multiset and unchanged final terminal envelope.

## Root blocker — historical/current candidate hashes are different domains

Accepted historical ASTRA candidate hashes are not PRE553 candidate hashes.

Independent check:

- accepted G02 terminal ledger Git blob:
  `531b605d15f72125968e809824f1b903d260a9b8`
- ASTRA-D04-R2 product: immutable product above.

ASTRA records 25 hashes across P0/P1/P2/P3.

**All 25/25 are literally present as G02 `execution_candidate_hash` values in the accepted G02 terminal ledger.**

Historical G02 producer identity:

- path: `rawlsing_next/prev3_learned_real_execution_r2.py`
- blob: `7a9b8b53e36041b453eb62e7a22a52ff0d392c16`

Its candidate hash preimage includes:

- historical G02 execution contract;
- D02 frontier blob;
- F02 read-option hash;
- historical candidate semantics, including `parameters`.

Current PRE553 exact candidate code blob:

`ee0544115feb9d76c8c68b9dd773302c8fa8bb48`

Its hash preimage instead includes:

- PRE553 I05 contract;
- family;
- rule;
- winning predicate ref;
- exact role/predicate/query refs;
- validation;
- ancestry refs.

These are demonstrably different canonical constructions.

The integrated parity module nevertheless copies both into a field named `candidate_hash` and exact-compares them, both in the lane rows and in `frontier.recorded_candidate_hashes`.

That violates identity-domain discipline.

## Why green tests did not catch it

The synthetic current fixture accepts a `candidate_hash` argument and injects the **historical ASTRA hashes** directly into the synthetic current receipts.

It does not compile the actual current PRE553 frontier and establish a common logical candidate key.

Therefore the tests prove that identical supplied strings compare; they do not prove that historical G02 and current PRE553 candidate identities inhabit one hash domain.

## Required correction

Create an explicit cross-schema logical candidate normalization.

Do not compare G02 execution hashes directly to PRE553 candidate hashes.

For P2 the common logical key must include the exact historical parameter tuple and the equivalent current CONDITION/BASELINE semantic bindings.

Until that exists, current↔ASTRA substantive parity is not established and oracle freeze is not adoptable.
