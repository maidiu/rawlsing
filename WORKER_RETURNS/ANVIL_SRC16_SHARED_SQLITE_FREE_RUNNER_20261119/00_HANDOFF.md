# Source-neutral raw lane + I03 leaf guard — R4 mixed-predicate closure

## Scope

Sourcefree only.  The frozen runtime/candidate trees and all real source data
remain read-only.  The authored handoff and predicate guard are isolated copies
under this return, with executable `-U0` patches.  No `.sav` was opened and no
survey was launched.

## Raw construction lane (preserved)

The shared construction-only raw lane remains:

- unmapped observed storage -> `INVALID_UNRESOLVED`;
- source-declared missing -> `MISSING`;
- exact raw value in the existing `$raw_physical_value` witness;
- existing declared occurrence topology copied, not guessed;
- no substantive promotion, canonical recoding, or new authority.

Two differently shaped sourcefree fixtures (SAV and DTA) were written and
cold-reopened through the saved first reader.  Mapped matched records retain
their exact semantic signatures.  Invalid physical state still refuses.

## I03 guard (R4)

The prior guard had an exact bypass: a whole-AST diagnostic exemption let a
mixed predicate pass an unrelated value-dependent leaf.  R4 replaces it with a
**leaf-local** guard in the existing predicate evaluator:

`_refuse_unresolved_value_leaf(event, node)`

It is called only while the existing leaf already iterates its selected saved
events.  It:

- refuses `INVALID_UNRESOLVED` for a value-dependent response-state or
  response-value leaf;
- allows only that individual explicit `INVALID_UNRESOLVED` state leaf;
- does not recurse the AST before evaluation and does not perform a second
  full query pass;
- uses the same existing question/component/occurrence event selection as the
  guarded leaf;
- raises existing `EmpiricalQueryResolutionError`, which the existing I03
  consumer converts to its normal typed negative/hold fact.

The mixed predicate reproduced the exact bypass and is now held:

`AND(INVALID_UNRESOLVED state diagnostic, NOT(SUBSTANTIVE_RESPONSE))`

## Actual saved native first-consumer evidence

`i03_consumer_before.out` / `i03_consumer_after.out` were produced through
`write_direct_estate` and `CarrierNeutralResearchExecutor.execute_i03` on the
cold saved estate, not through `_eval_predicate` or selector filtering alone.

| case | before | after |
|---|---|---|
| unmapped NOT | denominator 1, risk 2, `UNRESOLVED` | denominator 0, risk 0, guard hold |
| unmapped positive | `SUPPORTED`, denominator 1 | denominator 0, risk 0, guard hold |
| mixed diagnostic + NOT | denominator 1, risk 2, `UNRESOLVED` | denominator 0, risk 0, guard hold |
| standalone diagnostic | denominator 1, risk 2, `UNRESOLVED` | identical, allowed |
| known missing NOT | denominator 1, risk 2, `UNRESOLVED` | identical, still distinct |
| mapped NOT | denominator 0, risk 2, `ZERO_SUPPORT` | identical, replay and risk unchanged |

`i03_consumer_guard_compare.out`: **PASS**, including mixed before RED, mixed
after hold, positive/NOT holds, standalone diagnostic parity, known-missing
parity, and mapped denominator/risk/replay parity.

## I05/Batch status

Inspected `pre553_prepared_saved_i03.PreparedI03Session.execute_i05` and
`SavedC11Admission.execute_i05`.  Both route to the existing
`execute_exact_bounded_discovery`; that owner calls `execute_empirical_query`
(guard included) per candidate.  I05/Batch was **not exercised** here.

The exact remaining join is in `pre553_discovery_exact.py`: an I03
`UNRESOLVED` fact is currently mapped by `_terminal_fact_class` (lines 862-870)
to `UNAVAILABLE` / `EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY` (lines
1027-1028), which conflates unresolved with missing/authority.  That is a
terminal-state/join decision beyond this narrow I03 guard cut.  No Field Forge
or PRE-V3 qualification is claimed.

## Private GSS census verification

`gss_census_local_verify.out` replayed the completed private aggregate census
without source access:

- 40,592 declared-missing range cells covered;
- 18,105 observed-storage cells remain unresolved;
- 243 exact range rules;
- missing/duplicate mapped positions: 0;
- coverage replay: PASS;
- no raw tokens published.

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

No bytecode, private overlay, raw tokens, real source, GSS retry, new corpus,
protected edit, second backend, or DHIKR was added.
