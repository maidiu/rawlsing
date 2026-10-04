# HQ200 — R9 warrant plan binding and outer route-pass account

**Disposition: `WARRANT_PLAN_BINDING_CANDIDATE_READY_FOR_INDEPENDENT_REVIEW`**
**Terminal: `HQ200_R9_WARRANT_PLAN_BINDING_RETURNED__HQ_REVIEW_REQUIRED`**

Source-free implementation lane. No real survey source, locator, warrant issuance,
live C4, C7 or actor/person work was performed. Nothing is adopted here.

## Identity

| Field | Value |
|---|---|
| Branch | `agent/rabochii-pyat-hq200-r1` |
| Startup SHA (exact) | `8b977a2e33a1f03e34ea3cc5b815bc2525f388ab` |
| Implementation base | `90ccbd54c549f67358d0c02ad18ff90b843cf3ee` |
| Implementation commit | `b8b4c99633c4aa849fd79614c5bffbd1321209b8` |
| Governing authorities | `e7ce39dade6b169ab068f5f786b7a0dea06846dd` (adjudication), `09e1325da6ee880374a4065ae748cc03de93c421` (seven-source plan), `302d4a5da513381e26066cea70bf3ec5be7d3636` (independent scope review) |

## What was built

One new production module, `rawlsing_next/pre553_execution_binding.py` (423 lines),
and one new court, `rawlsing_next/tests/test_pre553_execution_binding_court.py`
(416 lines).

**No pre-existing tracked file was modified or deleted.** `git diff --name-status`
against the startup SHA is empty; the change is a pure addition. No existing
production path imports the new module, so the new mechanism is inert to every
previously qualified behaviour.

### The outer full-route-pass account

`full_route_passes` is a separately typed OUTER workload account. It is not
`decoder_invocations`, `full_reads`, `chunk_reads`, `selected_reads`,
`metadata_reads`, `reader_invocations` or `path_opens`, and it never substitutes
for any of them. `LOWER_LAYER_ACCOUNTS` names the excluded set explicitly so the
separation is testable rather than asserted in prose.

The receipt exposes the commissioned field names verbatim:
`full_route_passes_observed`, `full_route_passes_max`, `full_route_passes_expected`,
`full_route_passes_expected_status`, `full_route_passes_completed_successfully`,
plus `plan_identity` provenance.

### Expectation, policy and observation kept apart

`AccountConstraint` is frozen and carries `kind` (`EXACT` / `FLOOR` / `MAXIMUM` /
`UNBOUND`) separately from `authority` (`FROZEN_AUTHORITY` /
`IMPLEMENTATION_POLICY`). `OBSERVED` is never a spec field; it is produced only by
a run. A one-open or one-decoder ceiling supplied by a caller is therefore recorded
as an implementation policy and can never be misreported as a historical expected
count.

`RoutePassSpec.expected` and `RoutePassSpec.maximum` are distinct fields and are
reported distinctly, with an `expected_status` of `EXACT` or `UNBOUND`.

### Fail-closed behaviour

- **Pre-operation.** `BoundSourceExecution._gate_route_pass` runs before the session
  performs identity, metadata or row work. With `maximum=1` a second attempt is
  refused with `ROUTE_PASS_LIMIT_REACHED` and every lower-layer account is left
  exactly where it was. With `maximum=0` the first attempt is refused and no session
  is even created.
- **Post-operation.** Caller-supplied exact/floor constraints are checked against the
  observed receipt; an unsatisfied constraint raises `POST_EXECUTION_CONSTRAINT_FAILED`
  rather than returning successfully. The outer `EXACT` pass expectation is checked
  the same way. No constraint is invented that the caller did not supply.
- **Failed pass.** `_passes_completed` increments only after the governed operation
  succeeds, so a failed first attempt is never reported as a completed pass and
  `retries` remains governed separately.

### Chunking cannot satisfy a full-read floor

The post-operation checker reads the named account only. A `CHUNKED_FULL` execution
reports `full_reads == 0` and `chunk_reads > 0`, so a `full_reads` FLOOR 1 constraint
fails closed. Chunking cannot stand in for the frozen full-read floor.

### One session, owned

`BoundSourceExecution` creates exactly one `GovernedSourceSession` and owns its
deterministic, idempotent close. The spec is a frozen dataclass, so neither the plan
nor the budget can be swapped after binding; `with_plan()` deliberately derives a NEW
spec. No raw-path fallback exists.

## Courts

| Court | Result |
|---|---|
| `test_pre553_execution_binding_court.py` | **21 passed**, deterministic over 3 consecutive runs |
| `test_pre553_source_session_court.py` | 15 passed |
| `test_pre553_source_access_broker_court.py` | 20 passed |
| R7 exact six-file court (collect-only) | 55 collected |
| R7 exact six-file court, run 1 | **55 passed** in 45.61s |
| R7 exact six-file court, run 2 | **55 passed** in 46.41s |

R7 environment: the governed R7 interpreter, `PYTHONHASHSEED=0`,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONPATH` at the sparse worktree root,
`-p no:cacheprovider`.

The new court covers the seven documentary plan SHAPES on synthetic SAV/DTA carriers
only: selected single-variable, selected two-variable, metadata-only declared-encoding
(two encodings), selected exact-variable, metadata-only + 176-byte prefix, and the
full declared-encoding DTA carrying an outer route pass with exact/max 1. It also
asserts the SRC27-shaped count law, second-pass refusal with unmoved accounts,
chunk/floor separation, the expectation-versus-policy law, spec immutability,
zero-ceiling pre-operation refusal, and raw-path containment.

## Source-agnostic proof

`test_production_binding_module_has_no_source_specific_constants` parses the
production module and asserts that no `SRC02`/`SRC06`/`SRC08`/`SRC12`/`SRC14`/`SRC26`/
`SRC27`/`SRC35` token and no documented variable name (`Q10B`, `Q101`, `Q2061B`,
`v372`) appears in any code string literal or identifier. Docstrings are excluded
from the literal scan because prose may discuss the shapes. The shapes live only in
the court.

## Closure and suppression audit

- Raw-path reader calls with a bare variable path across the production package: **0**.
- All three modules import cleanly under warnings-as-errors.
- Production module files: 140.
- The new module is imported by exactly one file: its own court.

## Full-suite regression

`333 failed, 2550 passed, 1 skipped, 62 errors, 28 subtests passed in 401.71s`
(`--continue-on-collection-errors`). Against the HQ197 recorded baseline, 12 failure
IDs appear that were not in that baseline.

**All 12 were proven pre-existing and unrelated to HQ200.** With both new files moved
out of the tree entirely, the same 12 IDs fail identically (`8 failed, 8 passed,
4 errors`). This is consistent with the tracked-file diff being empty, and with those
tests never importing the new module. The 11 baseline IDs that no longer fail are
explained by the HQ198 sparse-manifest completeness change, which added the two
fixture paths that repair `test_fiabc_lm2_r1i_physical_native_hostile.py` and
`test_fiabc_lm2_r1j_sav_representation_authority.py`.

Unrelated pre-existing environment gaps were not retried and are not in scope:
`test_pre553_sr06_decoder_carrier.py` fails on `ModuleNotFoundError: No module named
'duckdb'`, and `WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py` remains
outside the C4 closure with raw-path reader calls, untouched here.

## Holds preserved

- No real source access, locator discovery or warrant issuance.
- No self-adoption; the disposition is a candidate for independent review.
- R9 remains open at authority level. SRC27's historical "multiple path-level opens"
  normativity is NOT decided by this lane; a one-open ceiling here is typed as an
  implementation policy and is not presented as a frozen historical count.
- Write terrain respected: one new `pre553_*execution_binding*.py` module, one test
  file, and this return directory. Nothing else was touched.

## Terminal

`HQ200_R9_WARRANT_PLAN_BINDING_RETURNED__HQ_REVIEW_REQUIRED`
