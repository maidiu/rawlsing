# R2 ACCOUNTING CORRECTION — READ BEFORE USING R2 PAIR WALL/S

The frozen R2 pair was **not** a matched positive-cost comparison:

- baseline wall `80.624 s` has no negative/restore phase;
- prepared wall `78.047 s` includes one separate negative/restore phase `14.803 s`;
- prepared S `5.498 s` includes the restore session build `2.772 s`;
- prepared RSS and row-group counts also include the restore phase.

Accounting-only subtraction, **only if the phase boundary is accepted**:

- prepared timed wall ≈ `78.047 - 14.803 = 63.245 s`;
- prepared timed S ≈ `5.498 - 2.772 = 2.726 s`.

This is bookkeeping from existing fields, not a new measurement or a speedup claim. The independent G5 auditor should perform raw phase correction. Do not cite `80.6 vs 78.0` or the `8.9 s S saving` as an unqualified matched comparison. R3 uses a single profiled `f4_three_raw` query and does not rerun the pair.
