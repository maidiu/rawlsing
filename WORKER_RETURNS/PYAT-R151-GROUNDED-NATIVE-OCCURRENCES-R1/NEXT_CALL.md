# R151 next calls

## Source preparation call

```sh
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R151-GROUNDED-NATIVE-OCCURRENCES-R1/runtime/render_grounded_native_input.py --source-id SRC35
```

The WVS7 record now contains two actual Occurrences, two NativeSourceRules and
one explicitly incomplete SourceInventory. The LiTS-I records contain exact
domain/risk/unit fields with topology and other fields retained as exact
item-level gaps.

## Still blocked

- Current source access/edition hash and exact response-read grant/current resolver.
- Complete native U/Epre and exact remaining item-level unit/topology/risk/domain fields.
- Grounded scientific roles/frontier and query/discovery authority.
- M1/M2/FF receiving-use authority.

The current planner/lowerer is not invoked on the incomplete WVS7 inventory.
No survey file or old response checkpoint is accessed.
