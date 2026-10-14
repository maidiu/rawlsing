# Owner Reuse and Test Receipts

## Commands and exits

```
cd WORKER_RETURNS/PYAT-USERDIRECT-20261014-R2-T8F-TEMPORAL-INTEGRITY-R1/repro
python3 -m pytest test_t8f_temporal_integrity.py -v
```
Exit 0, 29 passed in 0.06s

## Code blobs

- `t8f_temporal_integrity.py` -- temporal integrity repair module
- `test_t8f_temporal_integrity.py` -- 29-test suite

## HQ214 Comparator

T8R could not import HQ214 owner (network failure). Test double proves local method only. Real reuse requires source-issued per-wave measures.

## N9C Pattern

N9C has defensive-copy and hash-verified numeric read pattern for GSS/NCA aggregates. Not authorized for Ghana temporal N8E.
