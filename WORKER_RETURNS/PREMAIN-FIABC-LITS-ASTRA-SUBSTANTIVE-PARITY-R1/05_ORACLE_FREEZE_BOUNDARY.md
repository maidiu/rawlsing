# Oracle Freeze Boundary

## Required ordering

The LiTS producer now has this ordering:

```
current candidate-neutral PRE553 execution
    ↓
normalize_current_lits_summary()
    ↓
load immutable ASTRA-D04-R2 product / 77-role receipt / replay receipt
    ↓
verify exact historical Git blob identities
    ↓
normalize_accepted_astra_summary()
    ↓
assert_substantive_parity()
    ↓
persist astra_substantive_parity_receipt.json
    ↓
build_lits_i_oracle()
    ↓
verify_frozen_oracle()
    ↓
persist oracle
```

This is implemented in `produce_lits_local_oracle()`.

## Failure semantics

`assert_substantive_parity()` raises before `build_lits_i_oracle()` when any canonical section differs.

The hostile test `test_parity_failure_prevents_oracle_freeze` stubs the neutral materializer source-free, mutates one P0 support, and substitutes a build function that would mark itself called. The expected behavior is:

- parity exception raised;
- build marker remains false;
- oracle output path does not exist.

## Receipt-before-freeze semantics

The hostile test `test_parity_pass_persists_receipt_before_oracle_build` stubs all source/candidate execution and makes the mocked build function assert that the parity receipt already exists on disk when build is entered.

Thus successful ordering is not merely post-hoc audit.

## No cross-schema whole-hash gate

`build_lits_i_oracle()` still validates the historical ASTRA product and replay identities **inside their own historical domain**.

The new substantive gate does not compare either of those identities to current PRE553 execution/replay identities.

Current identities are separately recorded in the parity receipt.

## WVS7 boundary

No WVS7 freeze ordering or standardization implementation is modified by this repair.
