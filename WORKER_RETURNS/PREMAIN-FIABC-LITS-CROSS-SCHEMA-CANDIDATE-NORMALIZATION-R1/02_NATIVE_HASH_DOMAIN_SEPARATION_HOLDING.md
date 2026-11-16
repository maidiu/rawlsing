# Native Hash Domain Separation Holding

Historical native domain:

`G02_EXECUTION_CANDIDATE_HASH`

Current native domain:

`PRE553_I05_CANDIDATE_HASH`

These domains are **not equal-by-law** and parity never requires equality between them.

Historical G02 hashes are recomputed from the accepted native preimage:

- G02 contract;
- immutable D02 frontier blob;
- frozen F02 frontier read-option hash;
- canonical historical candidate semantics.

Current PRE553 hashes are recomputed from the exact PRE553 native preimage:

- I05 contract;
- family;
- rule;
- winning predicate ref;
- ordered query-role predicate/query refs;
- validation;
- ancestry refs.

Current candidate ID must also agree with the recomputed PRE553 digest.

All 50 current PRE553 native provenance identities are preserved. The 25 historical P0-P3 G02 hashes exposed in the ASTRA product are independently verified; P4 historical logical identity is reconstructed from the immutable 5x5 semantic frontier while current P4 native PRE553 identities remain preserved.

Hostile tests prove that:

- changing a G02 native hash while holding semantics fixed fails;
- changing a PRE553 native hash while holding the PRE553 preimage fixed fails;
- injecting a historical G02 hash as the current PRE553 hash fails;
- a native hash cannot substitute for the shared logical key.
