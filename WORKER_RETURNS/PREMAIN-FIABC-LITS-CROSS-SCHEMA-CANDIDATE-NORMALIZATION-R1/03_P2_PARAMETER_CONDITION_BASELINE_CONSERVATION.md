# P2 Parameter / CONDITION / BASELINE Conservation

The frozen historical P2 frontier is the exact Cartesian product:

`A1V1/A1V5 × Q310V1..3 × Q311V1..3`

yielding 18 logical candidates.

Each shared P2 logical envelope binds exact:

- `q301_2 ∈ {1,5}`;
- `q310 ∈ {1,2,3}`;
- `q311 ∈ {1,2,3}`;
- rule `D02_P2_HIGHER_ORDER_K3`;
- family `BOUNDED_K_WAY_RESPONSE_CONFIGURATION`;
- form `AND_CARTESIAN_GROUPS`;
- validation `DISTRIBUTION_DIFFERS_FROM_BASELINE`;
- CONDITION abstract query-template identity;
- BASELINE abstract query-template identity;
- logical condition atom set.

The current PRE553 binding additionally preserves the exact current CONDITION and BASELINE predicate/query refs.

Executable hostile tests prove fail-closed behavior for q301_2/q310/q311 drift with empirical witness held fixed, exact CONDITION or BASELINE ref mutation, query-template semantic drift, parameter substitution with native refs fixed, missing/out-of-frontier parameters, and forced logical-key collision.
