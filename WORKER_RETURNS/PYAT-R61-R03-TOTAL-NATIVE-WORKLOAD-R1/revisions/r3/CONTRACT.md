# R61 R03 R3 successor repair contract — five demonstrated defects

Status: frozen before the R3 code commit. Sourcefree TEST_ONLY. Inherits R61AS,
R2 review and all holds. Owner `native_receipt_anti_join` remains unchanged.

## 1/3 — Cold and live native identity closure

The governed result ledger now binds:

- exact `expected_jobs` from the issued U43 record;
- exact expected candidate IDs from the frozen lowering;
- the complete compilation material/hash;
- native receipt and fact objects plus exact ref lists and Batch receipt refs;
- per-operation expected/received candidate IDs, typed/coverage states,
  receipt refs and fact refs.

`restore_governed_frontier_ledger` re-derives and checks compilation hash,
expected jobs/candidates, row uniqueness/multiplicity, native receipt/fact ref
identity and every receipt-to-row candidate/state/fact association, and exact
fact coverage. Self-consistent strips/duplicates/removals refuse.
`execute_governed_frontier` additionally checks live receipt fact refs resolve
to native facts and cover the native fact set before `no_drop_ok` can be true.
The unchanged owner anti-join remains unchanged; adapter/compositor supplies the
fact closure required by R03.

## 2 — HELD/UNKNOWN separation

Compilation carries `operation_dispositions`. Non-supported rows preserve
eligibility in `eligibility_state` and normalize `result_state` to HELD, UNKNOWN,
PROHIBITED or INAPPLICABLE_PROVED; unsupported stays UNSUPPORTED; pending stays
PENDING/UNKNOWN. Cold ledger restore preserves the same rows.

## 4 — Recursive root-lineage severance

`bind_recursive_workload` verifies snapshot checkpoint hash, campaign/root
identity, nonempty root source releases, and exact equality of every receipt's
source-release set with the retained root. Severed/missing releases refuse.

## 5 — Trust boundary

Local trusted-host TEST_ONLY only. No R04 durable custody, cryptographic
authority, global anti-fork, original source/science, CI/prod/N11/N12/Sorok/
J52/W52. Caller replacement of trusted baseline/runtime remains outside scope.
