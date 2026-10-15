# Exact Accepted Owner Import and Computation

## Imports (module.__file__)

- `rawlsing_next.pre553_batch_runner` -> `/private/tmp/wg0p/rawlsing_next/pre553_batch_runner.py`
- `rawlsing_next.pre553_empirical_objects` -> `/private/tmp/wg0p/rawlsing_next/pre553_empirical_objects.py`
- `rawlsing_next.pre553_c11_repository` -> `/private/tmp/wg0p/rawlsing_next/pre553_c11_repository.py`

## Git blob identities (git hash-object)

- `pre553_batch_runner.py`: `2d291600b9a10c56d9c6f6de7f7d619f6c52e829` (matches commission pin)
- `pre553_empirical_objects.py`: `a61365b994e5c3c50de0f598fcf40e90abf757b6`
- `pre553_c11_repository.py`: `67c6eb6494522cd11aab1b93d0e73f9cef6036f3`

## Real invocation

`BatchExecutionRunner(manifest=..., repository=...).run(executors={"QUERY": binding})`
returns COMPLETED `UnitExecutionReceipt` per unit with `execution_performed=True`.

Release refs are opaque test-harness occupants in `C11Repository._by_ref`
(no C11 semantics manufactured), mirroring `test_pre553_batch_runner.py::_repo`.

## Computation

Pure executor maps each unit to an exact `Fraction` result ref.
Changed numerator/denominator on one unit changes only that unit's result ref.
Re-run is receipt-identical. Zero and minority fractions complete normally.
