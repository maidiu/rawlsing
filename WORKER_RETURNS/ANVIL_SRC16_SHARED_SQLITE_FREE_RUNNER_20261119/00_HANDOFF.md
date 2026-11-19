# Source-neutral raw lane — exact mapped control and joint I03 proof

## Scope

Sourcefree only.  Frozen runtime/candidates and all original data remain
read-only.  This return contains the isolated handoff and predicate-guard copies
with reproducible `-U0` patches.  No `.sav`, source read, GSS launch, I05/Batch
execution, or new research was performed.

## Mapped-parity defect corrected

The prior test used `raw_mapped <= base_mapped`, which allowed silent mapped
support loss.  It is replaced by an independently defined mapped set and a
separate mapped-only matched control:

- expected physical positions derive from fixture input and the mapped-only
  config, not from raw output;
- a separate control build uses a copied mapped-only config on the same source;
- each expected position produces exactly one event, with exact cardinality;
- comparison is exact equality of the full event ref and canonical semantic
  projection, including raw value, response state, native/canonical/component
  refs, topology, multiplicity/order, occurrence, and payload;
- no subset operator and no expected-row restriction from actual output;
- deleting one still-mapped control row makes the comparison fail.

`shared_raw_lane_test.out`:

| fixture | expected mapped | raw mapped | control mapped | exact | deletion fails |
|---|---:|---:|---:|---|---|
| SAV 3-row | 1 | 1 | 1 | yes | yes |
| DTA 4-row | 2 | 2 | 2 | yes | yes |

Raw/witness/declared-missing/invalid-physical checks remain PASS.  The two
fixture shapes are still SAV and DTA.

## Joint-target saved I03

Added an actual saved-native first-consumer case with two targets (`Y`, `X`),
one unresolved `Y` event, and a mapped `X` event.  The mixed condition remains:

`AND(INVALID_UNRESOLVED diagnostic, NOT(SUBSTANTIVE_RESPONSE))`

Actual `write_direct_estate` + `CarrierNeutralResearchExecutor.execute_i03`
results:

| case | before | after |
|---|---|---|
| joint mixed (`Y`,`X`) | denominator 1, risk 2, `UNRESOLVED` | denominator 0, risk 0, guard hold |
| simple mixed | denominator 1, risk 2 | denominator 0, risk 0 |
| simple NOT / positive | denominator 1 / `SUPPORTED` | both held |
| standalone diagnostic | denominator 1, risk 2 | identical, allowed |
| known missing | denominator 1, risk 2 | identical, still distinct |
| mapped NOT | denominator 0, risk 2, `ZERO_SUPPORT` | identical; risk/replay unchanged |

`i03_consumer_guard_compare.out`: **PASS**.

The guard remains leaf-local in `_refuse_unresolved_value_leaf`; it is not a
whole-AST prepass and does not add a second query pass.  Only the individual
explicit `INVALID_UNRESOLVED` state leaf is exempt in a mixed predicate.

Component/occurrence selection variant: not available in this sourcefree
fixture builder (one occurrence/component per question); the joint target
variant is exercised, and no synthetic component/occurrence claim is made.

## I05/Batch

I05/Batch was not exercised and remains independent.  Inspected handoffs route
`execute_i05` through `execute_exact_bounded_discovery`; the exact remaining
join is the existing discovery terminal mapping of `UNRESOLVED` to
`UNAVAILABLE` / `EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY`
(`pre553_discovery_exact.py:862-870, 1027-1028`).  No Field Forge or PRE-V3
qualification is claimed.

## Private census verification

`gss_census_local_verify.out` remains PASS: 40,592 declared-missing range cells
covered, 18,105 observed-storage cells unresolved, 243 exact range rules, zero
missing/duplicate mapped positions, no tokens/source.

## Files

- `common/pre553_source_i02_handoff.worker.py`
- `common/handoff_raw_lane.patch`
- `common/pre553_query_predicate.worker.py`
- `common/query_predicate_guard.patch`
- `common/shared_raw_lane_test.py`
- `common/i03_consumer_guard_test.py`
- `common/i03_consumer_guard_compare.py`
- `common/sqlite_free_single_pass.py`
- `common/sqlite_free_witness.py`
- `common.patch`
- `shared_raw_lane_test.out`
- `i03_consumer_before.out`
- `i03_consumer_after.out`
- `i03_consumer_guard_compare.out`
- `gss_census_local_verify.out`
- `receipt.json`

No bytecode, raw tokens, private overlay, real/data source, protected edits,
I05/Batch changes, or DHIKR.
