# Parity and Identity-Domain Holding

## Holding

**Substantive parity is a normalization problem, not an object-hash substitution problem.**

The accepted ASTRA typed learned product and the current carrier-neutral execution receipt are different canonical schemas. Their whole-object hashes encode different material. Direct equality is therefore meaningless even when both objects describe the same empirical world.

The baseline correctly stopped using historical ASTRA product identity as the current product identity, but then over-corrected: current admission became cardinality/terminal-count only. The lawful middle is an explicit cross-representation normalization of constituent empirical facts.

## Same-domain equality gates

Direct hash equality is legitimate where both sides are provably the same canonical domain:

- LiTS exact source bytes → source SHA;
- exact same candidate identity schema → candidate hash;
- exact same frozen frontier construction → frontier seal;
- exact same R2/R7/R27 risk-set root construction → risk-set root;
- exact same selector-row/subset root construction → q310/q311 row/selector roots;
- exact same authority object/ref schema → authority content hash / ExactRef;
- repeated materializations of the same ASTRA product schema → ASTRA product/run byte identity;
- repeated materializations of the same current receipt schema → current receipt identity.

These comparisons are identity/provenance conservation. They are not sufficient by themselves to prove cross-representation empirical parity.

## Cross-domain hashes that must never be equality-gated

Do not require equality between:

1. `semantic_hash(ASTRA_D04_R2_TYPED_LEARNED_EMPIRICAL_PRODUCT@1.0.0)`
   and
   `semantic_hash(PRE553_LEARNED_EMPIRICAL_EXECUTION_RECEIPT@1.0.0)`.

2. ASTRA's run/product byte SHA `47d36b1459...`
   and a current neutral execution receipt/exact-output identity.

3. ASTRA's historical semantic replay identity `301735d456...`
   and a current replay identity when the canonical replay schemas/material differ.

4. ASTRA role/candidate ledger hashes
   and current receipt-collection hashes when ordering/schema/canonical material changed.

5. a frozen oracle identity
   and either the historical ASTRA product identity or a raw current execution identity.

A hash cannot carry semantics across a representation boundary it does not share.

## Immutable-anchor checks vs parity checks

Two different assertions are required:

### A. Immutable historical anchor check
Prove the ASTRA evidence has not moved:
- accepted product identity is exactly the historical accepted identity;
- accepted replay/source receipt is the expected accepted artifact;
- source/frontier/workload identity in that artifact is exact.

### B. Current substantive parity check
Using current full empirical preimages, deterministically normalize the current result into the ASTRA substantive domain and compare the values enumerated in `02_ASTRA_SUBSTANTIVE_TRUTH_INVENTORY.md`.

A passes does not imply B.
B passes does not authorize replacing current hashes with historical hashes.

## What current execution actually retains

Immediately after current neutral I05:

`result.empirical_facts`

contains full `EmpiricalFact` objects. Each fact includes exact:
- typed state;
- query/predicate/risk-set/measure/replay refs;
- raw numerator;
- raw denominator;
- target topology, including complete cell semantic projection where applicable.

The discovery receipts preserve:
- candidate identity;
- query roles;
- role→fact refs;
- coverage/typed state;
- support-uncertainty state.

The generic evaluator itself computes:
- distribution difference from complete cell projections;
- joint dependence from joint + marginal exact counts;
- target-cell support from exact cell counts;
- reversal from exact cell fractions.

Therefore a fresh source decode is **not** needed merely to establish ASTRA parity once the current neutral I05 result exists.

## What is lost by current reduction

`learned_empirical_execution_receipt(result)` retains:
- object refs;
- counts;
- coverage claim;
- candidate count;
- valid-empty flag;
- replay ref;
- current execution identity.

It does **not** contain the constituent P0/P1/P2/P3/P4 values.

`_constituent_i03(...)` checks that full fact preimages exist, but the emitted global fact manifest reduces each fact to ref + typed state. This proves closure, not empirical parity.

The parity comparator must therefore run while full `EmpiricalFact` preimages are still present, or persist an explicit normalized parity preimage before reduction.

## Exact freeze boundary

Required causal order inside fresh LiTS oracle production:

`neutral source decode`
→ `current common C11`
→ `current neutral I05`
→ `full I03 fact preimages retained`
→ **`normalize current facts to ASTRA substantive truth schema`**
→ **`compare exact accepted ASTRA substantive facts`**
→ **`emit parity PASS receipt`**
→ `construct current learned-product identity envelope`
→ `build_lits_i_oracle()`
→ `freeze_oracle()`.

On mismatch, the function must terminate before `build_lits_i_oracle()`; no standard LiTS oracle document may be written.

## Specific evasions a correct comparator must block

### P4 permutation
A comparator that sees only 25/25 supported, total support, or a multiset can miss swapped cells. Compare exact cell key → exact support.

### P2 witness drift
A candidate can remain `EVALUATED_SUPPORTED` after its first differing cell/count changes. Compare exact condition tuple + exact target/baseline + exact canonical witness.

### P3 wrong-reason valid-empty
`VALID_EMPTY` is an outcome class, not a reason. Preserve exact eight fractions and sign vector so “still non-reversal, but for different data” fails.

### Denominator drift
The same numerator under a different governed risk set is a different empirical proposition. Bind every relevant support to its exact denominator/risk-set identity.

## Current baseline vulnerability

At baseline, `_bind_current_lits_execution_to_astra()` can accept arbitrary well-formed current semantic/execution hashes provided:
- 50 candidates;
- 77 roles;
- terminal counts 49/1.

The source-free unit test intentionally demonstrates this by passing synthetic `current-neutral-execution` and `current-neutral-semantic-replay` hashes and expecting success. That is sound as an identity-domain test but simultaneously proves that the function is not a substantive parity gate.

The repair must preserve the identity-domain separation while inserting an independent normalized empirical comparator.
