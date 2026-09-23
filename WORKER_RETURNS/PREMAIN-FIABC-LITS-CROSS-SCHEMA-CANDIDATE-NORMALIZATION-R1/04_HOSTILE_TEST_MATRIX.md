# Hostile Test Matrix

The source-free court explicitly exercises these failure modes:

| Hostile case | Expected |
|---|---|
| Historical G02 hash changed, semantics fixed | fail closed |
| Current PRE553 hash changed, native preimage fixed | fail closed |
| Historical G02 hash injected as current PRE553 hash | fail closed |
| q301_2 mutated, empirical witness held fixed | fail closed |
| q310 mutated, empirical witness held fixed | fail closed |
| q311 mutated, empirical witness held fixed | fail closed |
| CONDITION predicate ref drift | fail closed |
| CONDITION query ref drift | fail closed |
| BASELINE predicate ref drift | fail closed |
| BASELINE query ref drift | fail closed |
| query-template semantic drift | fail closed |
| missing/out-of-frontier P2 parameter | fail closed |
| two distinct candidates forced onto one logical key | fail closed |
| arithmetic/displayed-value equality substituted for exact semantic identity | fail closed |
| role-risk-set topology drift | fail closed |
| F02 selector count/root/category permutation drift | fail closed |
| P0/P1/P2/P3/P4 empirical witness drift | fail closed |
| parity failure followed by oracle freeze attempt | freeze blocked |

Positive controls prove the immutable historical semantics and the actual current PRE553 frontier independently yield the same exact 50 logical keys while retaining different native provenance identities.
