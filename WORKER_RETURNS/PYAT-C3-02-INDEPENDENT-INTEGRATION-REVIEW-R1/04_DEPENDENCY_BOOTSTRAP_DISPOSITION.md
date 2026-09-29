# C3-02 dependency-bootstrap disposition

Disposition: `CHANGES_REQUIRED`

## Finding

The import-time pandas bootstrap in `rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py` is defective qualification architecture.

The governed workflow installs `pytest` before test execution. The bounded-court implementation then constructs a pytest command from the validated test-path list. Dependency provisioning is therefore an execution-environment concern, not semantic test behavior.

The worker's preserved first run proves the actual capability gap: collection of the unchanged facade regression failed because pandas was absent. The later green run did not merely rerun in a correctly provisioned court; instead, the D02 test acquired a new side effect that changes the runtime during module import.

## Adjudication

### C3 execution/capability routing

`FAIL`.

A semantic allowlisted test should observe the environment supplied by the court. It should not repair an environment dependency by invoking the package manager. Doing so collapses the distinction between the thing being qualified and the capability substrate performing qualification.

### Hermeticity / reproducibility

`FAIL`.

The command is unpinned and reaches mutable package-index/network state. Whether collection succeeds can vary with connectivity, index contents, resolver behavior, platform wheels and future pandas releases. The resulting pandas version is not part of the court spec or receipt.

The repository already demonstrates the correct responsibility boundary: existing source-free workflows such as `fiabc-lm2-r1j-sav-representation-authority.yml` and `fiabc-lm2-r1e-browser-prep-source-free.yml` provision `pytest pandas` in workflow setup rather than inside a test.

Moving an unpinned install into workflow setup would fix the ownership inversion but would still leave dependency-version mutability. A stronger qualification should pin or otherwise immutably identify the pandas environment used.

### Effect on the worker's 53-test PASS

The worker's run `36615231777` and independent reviewer run `36619077886` both demonstrate that the six-file suite can pass when the D02 test is permitted to bootstrap pandas. Those runs are valid `SOURCE_FREE_EXECUTED` behavioral evidence.

They are **not accepted as reproducible court qualification** for C3-02 because successful collection depends on a semantic test mutating the environment.

The earlier collection failure `36614460693` remains preserved evidence of the environment gap and must not be erased.

## Minimal repair grain

1. Remove `importlib.util`, `subprocess`, `sys`, and the conditional `pip install pandas` block from the D02 semantic test.
2. Provision pandas before pytest in the governed execution environment/court, preferably with pinned/immutable dependency identity recorded in evidence.
3. Rerun the exact six-file C3-02 court with package installation impossible from semantic test import.
4. Preserve semantic candidate identity separately from any execution-environment/court repair identity.

No production semantic widening follows from this disposition.
