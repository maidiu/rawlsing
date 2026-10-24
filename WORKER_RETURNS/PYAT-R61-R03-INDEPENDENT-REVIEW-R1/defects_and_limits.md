# R61-R03V defects and limits — REVISE

Verdict: **REVISE** for the R03 total sourcefree native workload integration.
The recovered U43 module is byte-exact, the four-path scope is respected,
actual SAV/DTA native execution works for the unary administered item/value
subset, and the independent physical source VALUE fault/restore positive passes.
The candidate does not implement the commissioned complete finite
grammar/scientific-frontier lowering, exact receipt/fact native no-drop, typed
per-operation states, or genuine R01 D3 recursive composition. Candidate code
was not edited.

Repro commands (reviewer root):

```sh
/usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R61-R03-INDEPENDENT-REVIEW-R1/independent_probes/test_r03v_hostile.py \
  -q -o addopts=''
```

## D1 — Compiler is unary inventory enumeration, not grammar/scientific-frontier lowering (blocking)

**Contract:** R03 must lower the complete finite authorized sourcefront /
inventory + R01 `GrammarPolicy`/`ScientificFrontier` workload into native
operations, including conditional and joint operations, not a selected unary
list (R87 commission; U53A 07/11 U-R03; R03V commission).

**Observed:** `compile_universal_workload` accepts only
`bundle, as_of, host, purpose, measure_kind`; it has no grammar, policy,
frontier, parent or recursive input. It iterates `bundle.administered` and emits
one `UniversalOperation` per `(source_variable_code, response_value)` presence
pair (`pre553_universal_workload.py:129-212`). `UniversalOperation` has only
operation id, source variable, response value, occurrence identity, measure,
status and reason; `OperationFixture` has only target variable, response value
and measure. There are no ordered target tuples, condition tuples, condition
values, operation class, comparator/root/parent identity, J/K/D or joint-shape
fields.

**Repro (H1):** inspect the API and dataclass fields. The compiler has no
`grammar`/`frontier`/`scientific_frontier`/`expected_frontier` parameter, and
`UniversalOperation` cannot represent conditional/joint/root-parent operations.
The author's six tests also enumerate only unary item/value expectations.

**Required (minimal function):** accept the actual R01-issued grammar/finite
scientific frontier (or an equivalent independently issued operation/frontier
record) and emit every eligible conditional/joint/ordered/recursive operation
with exact role, unit/risk/measure, condition identity/value, operation class,
comparator/root-parent and J/K/D state. Extend `UniversalOperation`,
`OperationFixture` and the binding/anti-join accordingly. Administered unary
item/value presence may remain one supported shape, not the whole workload.

## D2 — Anti-join ignores native receipts, facts, results and expected jobs (blocking)

**Contract:** R03 must reconcile exact expected operation/receipt/fact identity,
content and multiplicity against the actual native execution, not counts or R03
operation IDs alone (R87 commission; U53A 07/11 U-R03; R03V commission).

**Observed:** `UniversalWorkloadResult.anti_join`
(`pre553_universal_workload.py:98-112`) compares only
`executed_operation_ids` against compiled operation IDs. `receipt_refs`,
`fact_refs`, `native_results`, `failed`, and the compilation's
`expected_jobs`/`expected_frontier_root` are not reconciled.

**Repro (H2):** take a passing result and replace it with
`receipt_refs=()`, `fact_refs=()`, `native_results=()`; `anti_join()` still
returns `no_drop_ok: true` because the R03 operation IDs remain. The author's
count-preserving test mutates only `executed_operation_ids`, so it never tests
receipt/fact substitution or omission.

**Repro (H3):** replace `compilation.expected_jobs` with `()`; `anti_join()`
still returns `no_drop_ok: true`. The actual U43/native `(job_kind, query_ref,
predicate_ref)` identities are not reconciled.

**Required (minimal function):** retain the exact expected native job,
receipt and fact identity sets/multiplicity (including operation-to-query/
predicate roles) in the compilation/result, and make the same-consumer
anti-join fail on missing, extra, substituted or duplicated receipts/facts/
native jobs even when the R03 operation-ID list is unchanged. Include actual
native receipt/fact substitution and omission tests, not only operation-ID
mutation.

## D3 — `bind_recursive_execution` decorates unrelated receipts rather than composing R01 D3 (blocking)

**Contract:** R03 must consume actual qualified R01 D3 parent/child,
root-versus-parent, minority/nonwinning recursive execution through the same
total workload ledger; a read-only ref extractor is not enough if it does not
drive a dependent R03 assertion (R87/R03V commission; R01 acceptance).

**Observed:** `bind_recursive_execution` reads a campaign snapshot execution
preimage and returns operation/rule, receipt, handoff, fact and release refs.
No API path feeds that fragment into `compile_universal_workload`,
`execute_universal_workload`, `UniversalWorkloadResult.anti_join`, or any
consumer assertion. The author test only asserts that the returned refs are
nonempty, that two fragments differ, and that binding does not create a new
execution. It never makes an R03 workload/fact assertion depend on the R01
fragment.

**Repro (H4):** `execute_universal_workload` accepts only `compilation` and
`source_factory`; it has no campaign, execution ref or recursive-fragment
input, and `UniversalWorkloadResult` has no recursive ledger field. The fragment
therefore cannot affect the R03 result.

**Required (minimal function):** integrate the retained R01 execution fragment
as an explicit part of the R03 compilation/result and consumer assertion
(exact recursive operation/receipt/handoff/fact/release identities, parent/
root/child relation and D3 state), with sever/mutation making the same R03
assertion fail and restoration passing. Do not create a second lineage engine;
consume the R01 owner by reference.

## D4 — Actual native typed states are not retained per operation (blocking)

**Contract:** R03 must preserve supported, unsupported, error, unrun, pending,
held, unknown and valid-empty distinctions; failed/unrun must not become
valid-empty or disappear (R87/R03V commission; U53A 07/11).

**Observed:** `UniversalWorkloadResult` has no per-operation typed state
ledger. `execute_universal_workload` catches every non-binding exception into a
generic `ERROR` entry and ignores the actual U43/Batch receipt states and typed
native outputs. The compiler marks only binding refusals as
`UNSUPPORTED_RUNTIME`; unsupported/error/valid-empty/pending are not a complete
disjoint partition.

**Repro (H5):** the result dataclass has no `operation_states`/
`typed_states`/`status_by_operation`; a wrong-edition run yields generic
`ERROR` failures and no actual native typed state. The author test asserts
`failed` is nonempty but does not inspect the native receipt states or
distinguish error from unsupported/unrun/valid-empty.

**Required (minimal function):** expose one checked per-operation native-status
projection sourced from the actual U43/Batch/receipt results, with disjoint
supported/unsupported/error/unrun/pending/held/unknown/valid-empty states and
exact reasons; do not collapse all exceptions to `ERROR`.

## D5 — Author source-fault test proves edition refusal, not value sensitivity (evidence gap; independently repaired)

The author fault test replaces `physical_stream.source_sha256` with a wrong
edition and observes refusal before values are evaluated. That proves edition
binding, not that a physical source VALUE change alters the dependent fact.
The reviewer independently built baseline and one-value-mutated SAV bundles,
executed both, and observed different dependent native fact refs; restoring the
baseline reproduced the original refs (P1 passes). The candidate behaviour is
therefore value-sensitive at this unary grain, but the author return's claimed
proof is narrower than the contract. The missing per-operation typed/ledger
functions above remain.

## Positive findings retained (not acceptance)

- Recovered U43 issued module is byte-exact blob
  `31e84f49d624f5524906e9e7839d2873106f8249`.
- Candidate diff from startup is exactly the four allowed code/test paths plus
  the author contract; R01/R02/native owner bodies are unchanged.
- Author six tests pass under the reviewer harness.
- Actual SAV and DTA unary native execution uses the existing U43/Batch/RouteB/
  I03/I05/C11 path; source edition mismatch fails before executed IDs; the
  operation-ID list can detect count-preserving ID substitution.
- Independent physical source VALUE fault/restore changes and restores
  dependent facts at the unary grain.
- `bind_recursive_execution` is read-only and does not create a second lineage
  engine or rerun discovery; it does expose exact retained refs.

## Minimal missing function summary

`rawlsing_next/pre553_universal_workload.py` and the binding:

1. Consume the actual R01-issued grammar/scientific frontier and emit complete
   conditional/joint/ordered/recursive operations; extend the operation/fixture
   model and binding.
2. Reconcile exact expected native jobs, receipts and facts by identity/content/
   multiplicity in the same anti-join; fail on missing/substituted/duplicate
   native material.
3. Compose the R01 D3 recursive fragment into the R03 compilation/result/
   consumer assertion.
4. Retain a complete per-operation typed native status ledger from actual U43/
   Batch/receipt outputs.
5. Add native receipt/fact substitution/omission and physical value-fault tests
   to the author proof.

## Preserved limits

Sourcefree TEST_ONLY trusted-host only. No source respondent access. R04 joined
custody/durability, R05 grades, R06/F6-F8, R07/N11, N12/Sorok, original35/1890,
production/CI and J52/W52 remain NOT_REACHED. No self-adoption, production edit
or new architecture/lineage engine.
