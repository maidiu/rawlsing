# R61-R03V R2 remaining failures and limits — REVISE

Verdict: **REVISE**. The R2 successor closes the governed-frontier structural
gap and adds a real D3 recursive binding, but the exact native
receipt/fact/expected-job cold assertion and the held/unknown state separation
still fail. This is one finite prioritized list of reproducible failures; no
R04/R05/original-science demand is made.

## Prioritized remaining failures

### 1. Native receipt/fact/expected-job ledger is not independently validated (blocking)

**Expected:** deleting, swapping or duplicating meaningful native receipts,
fact refs or expected native jobs while leaving nominal operation IDs unchanged
must make the same `no_drop_ok` fail or refuse; positive restoration must pass.

**Observed:** `restore_governed_frontier_ledger` checks only `ledger_hash`,
schema and field presence. A self-consistent forged ledger with:
- all `native_receipts`, `receipt_refs`, `native_facts`, `fact_refs` and
  `batch_receipt_refs` removed,
- every operation row's `fact_refs`, `receipt_refs`,
  `received_candidate_ids`, `candidate_typed_states` and
  `expected_candidate_ids` stripped,
- recomputed `ledger_hash`

is accepted, while its stored `candidate_anti_join`/`operation_anti_join`
still report true.

Separately, `native_receipt_anti_join` ignores `empirical_fact_refs`: removing
one native receipt's fact refs leaves `no_drop_ok: true`. Candidate identity and
rule counts are checked, but fact content/multiplicity is not.

**Required minimal function:** persist the independently expected native job,
receipt and fact identity/multiplicity set in the ledger; make the same
cold/consumer assertion re-derive and reconcile it against the native receipts
and facts; refuse self-consistent strips/duplications and live fact-ref
removal. Add expected native job identity to the result ledger (the current
ledger has no `expected_jobs` at all).

### 2. Held/unknown normalized result state is collapsed (blocking)

**Expected:** supported, valid empty, observed zero, unsupported,
unissued/pending, held, unknown and error remain separate per operation.

**Observed:** for constructed frontier operations with `disposition=HELD` and
`disposition=UNKNOWN`, the operation ledger preserves the reason strings
`FRONTIER_ELIGIBILITY_HELD`/`FRONTIER_ELIGIBILITY_UNKNOWN` but normalizes
`result_state` to `NOT_ELIGIBLE` for both. A consumer reading the normalized
state cannot separate held/unknown from prohibited/inapplicable/not-eligible.
Observed-zero and error were not independently demonstrated at the R03 ledger
grain.

**Required minimal function:** carry the actual eligibility/execution/result
axes (at least HELD, UNKNOWN, PROHIBITED, INAPPLICABLE_PROVED and the native
observed-zero/error states) into the per-operation ledger and its cold
projection instead of collapsing all non-supported frontier operations to
`NOT_ELIGIBLE`.

### 3. R01 root-lineage severance is accepted by `bind_recursive_workload` (secondary)

**Expected:** actual R01 receipt/parent/handoff/root-parent results reach an
R03 consumer that changes or refuses on meaningful lineage severance.

**Observed:** a snapshot wrapper with `payload.root.source_release_refs=[]`
(and no other change) is accepted by `bind_recursive_workload`, which returns
`anti_join.no_drop_ok: true` and an empty `source_release_refs`. Missing
declared receipt, missing preimage receipt, missing handoff and altered expected
plan are correctly refused, and the real baseline binds exact D3
operations/receipts/facts with root/parent contrasts and minority. The root
release severance is the remaining gap; the binder also accepts any object
exposing `snapshot()` rather than authenticating the retained R01 campaign
identity.

**Required minimal function:** validate the retained campaign/snapshot root
identity and source release set against the execution receipt/preimage before
accepting the binding; a severed root release must refuse or make the same D3
consumer assertion fail.

## Retained positives (not acceptance)

- Author suite: 120 passed, 0 failed/error/skip under the reviewer harness.
- Governed frontier: real bundle/inventory/policy/frontier input, 150 eligible,
  147 supported, 3 unsupported, conditional/joint/co-travel/fork classes,
  candidate and operation anti-joins true, 150 receipts, 330 facts.
- Pending budget operations are explicit and not executed.
- D3 recursive binding baseline binds exact expected operations to
  receipts/facts, exposes root/parent contrasts and minority, and refuses
  missing receipt/plan/handoff mutations; cold rebinding preserves content and
  fact refs.
- U43 blob `31e84f49d624f5524906e9e7839d2873106f8249` is exact; the four-path
  scope and unchanged R01/R02/native owners are preserved.
- The prior unary value-fault positive is retained, and the R2 author governed
  value mutation/restore test passes within the 120 suite.

## Limits / not reached

Sourcefree TEST_ONLY local trusted host only; no source respondent access. R04
joined durable custody, R05 lifecycle/grades, F5-F8 global, original35/1890
N11, N12/Sorok, protected CI/production and J52/W52 remain NOT_REACHED. No
candidate repair, self-adoption, new worker or model swap.
