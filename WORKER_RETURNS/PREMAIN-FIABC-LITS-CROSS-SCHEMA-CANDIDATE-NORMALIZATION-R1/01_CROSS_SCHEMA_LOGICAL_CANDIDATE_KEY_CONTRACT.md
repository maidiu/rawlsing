# Cross-Schema Logical Candidate Key Contract

Contract:

`FIABC_LITS_CROSS_SCHEMA_LOGICAL_CANDIDATE@1.0.0`

The shared logical key is the semantic hash of an explicit logical-candidate envelope containing the frozen D02 lane/rule/family/form semantics, exact parameters, validation law, abstract query-template identities, and logical condition atom identities.

It is a **comparison identity**, not a replacement provenance identity.

For each logical candidate K:

1. historical G02 semantics independently produce K;
2. current PRE553 compiled semantics independently produce K;
3. historical G02 native hash remains separately verified;
4. current PRE553 native hash remains separately verified;
5. parity is permitted only after the logical identities agree.

The exact logical frontier contains 50 unique keys:

- P0: 5
- P1: 1
- P2: 18
- P3: 1
- P4: 25

The current runtime materializer emits the logical binding from actual PRE553 compiled candidates. The oracle path requires those bindings; it cannot silently fall back to native cross-schema hash equality.
