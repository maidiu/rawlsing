# Current PRE553 Real Frontier Witness

The repair does not rely on synthetic historical hashes masquerading as current identities.

The exact runtime materializer:

`rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py`

compiles the actual current PRE553 discovery grammar and candidate frontier and emits:

`cross_schema_logical_candidate_bindings`

for all 50 candidates.

Executable proof establishes:

- candidate count = 50;
- query-role count = 77;
- logical keys = 50 unique;
- current PRE553 native hashes = 50 unique;
- each logical key hashes its exact logical material;
- each PRE553 native hash hashes its exact PRE553 native preimage;
- each PRE553 candidate ID is consistent with that native hash;
- all 50 current logical keys equal the independently reconstructed historical logical frontier.

For P2, atom recovery occurs from the actual compiled CONDITION predicate structure. The exact A1V1/A1V5, Q310V1..3 and Q311V1..3 atom tuple is recovered from current predicate semantics, not inferred from empirical outcomes.
