# Courts 7–8 — Freeze Ordering and Identity Domains

## Court 7 — freeze ordering

**PASS**

Actual `produce_lits_local_oracle()` order:

```
_neutral_lits_material()
    -> current source/C11/current candidate-neutral I05
    -> current full empirical facts + current F02 selector scan
    -> current ASTRA-shaped summary

git-show immutable ASTRA product / role receipt / replay receipt
    -> verify exact historical blobs
    -> normalize immutable expected summary

assert_substantive_parity()

write astra_substantive_parity_receipt.json

build_lits_i_oracle()

verify_frozen_oracle()

write standard LiTS oracle
```

Thus current expected truth is not frozen before parity.

## Failure proof

The integrated hostile suite substitutes a drifted current summary and a mocked oracle builder.

For both:

- ordinary substantive drift; and
- F02 selector substrate drift,

the expected behavior is:

- parity exception;
- builder never called;
- standard oracle path absent.

The PASS-path hostile test makes the mocked builder assert that the parity receipt already exists on disk when builder entry occurs.

Ordering is therefore causally tested, not merely documented.

## Court 8 — whole-object identity discipline

### PASS dimensions

The repair correctly does **not** require equality between:

- ASTRA whole learned-product SHA;
- current PRE553 execution receipt identity;
- ASTRA semantic replay identity;
- current I05 replay identity;
- frozen oracle identity.

The parity receipt explicitly states:

- `historical_current_whole_object_hash_equality_required = false`
- `whole_object_hashes_compared_across_schema_domains = false`

D03 roots are used in their exact adopted root domain.

F02 roots are used only after actual same-canonical-material proof.

### FAIL dimension — candidate identity

The preceding declaration is not fully true in practice.

The comparator directly equality-gates historical ASTRA `candidate_hash` against current PRE553 `candidate_hash`.

Historical side is proven to be G02 `execution_candidate_hash`:

- accepted G02 terminal ledger contains every one of ASTRA's 25 recorded P0/P1/P2/P3 hashes;
- historical producer blob `7a9b8b...` defines that hash over the G02 execution contract + D02/F02 identities + historical candidate-semantics envelope.

Current side is PRE553 I05 candidate hash:

- current code blob `ee054411...`;
- hash material is PRE553 I05 contract + winning predicate ref + role predicate/query refs + validation + ancestry.

No common canonical construction has been proven because the constructions are visibly different.

No explicit logical identity normalization intervenes.

Therefore candidate hash is an **incompatible old/current identity domain** presently being compared directly.

## Holding

Freeze order is correct.

Identity-domain discipline is not complete.

This is a pre-oracle source-free blocker because the parity comparison sits before oracle construction and candidate identity is part of the asserted equality.
