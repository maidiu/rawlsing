# R61-R03V R2 independent native qualification return — REVISE

**Verdict: `REVISE` for the R2 repaired complete native workload.** The governed
frontier, real joint/conditional/D3 native facts, pending accounting and
heterogeneous source path are genuine improvements, and the author 120-test
suite passes. The exact native receipt/fact/expected-job cold assertion and the
held/unknown normalized states still fail. R03 is not accepted; no
self-adoption, production merge or downstream wake.

## Exact identity and separation

- Commission: `7d18e0a467db28e37079340f596ead83ef9dc20a`.
- Exact candidate/startup: `2d32d68e2a5acb9cac136c313e82068dfb8e6ba1`.
- Previous independent review: `efb1822552bdb017adedc8617e268f9ad5719de8`
  against old candidate `5f3cee7cb7a9b53af266b05a4c8db01a53a13add`; its
  EXPECTATIONS remains the claim oracle and its files were not modified.
- Reviewer branch: `agent/opencode-pyat-r61-r03v-r2-independent-review-r1`.
- Mandatory first-tool preflight passed exactly at the stable worktree, branch
  and HEAD, with only untracked pycache.
- Reviewer EXPECTATIONS were frozen and committed (`d61f4ded4`) before R2
  candidate code inspection.
- Reviewer is the existing distinct R03V reviewer, not the author or HQ; same
  account/provider is disclosed and is not institutional or OS isolation.

## Independent replay

| Suite | Result | Evidence |
|---|---|---|
| Author R2 suite | 120 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Reviewer successor probes | 1 passed, 5 failed required behaviours | `replay/hostile_probes_junit.xml`, `.log` |

The five failures are product gaps, not import/setup crashes:

1. A self-consistent forged governed ledger with all native receipts, facts,
   expected candidate IDs and typed states stripped is accepted by
   `restore_governed_frontier_ledger`; only `ledger_hash` and field presence are
   checked.
2. Removing a native receipt's `empirical_fact_refs` leaves
   `native_receipt_anti_join` `no_drop_ok: true`; fact identity/content is not
   reconciled.
3. The governed result ledger exposes no expected native job identities, and
   expected candidate/typed-state rows can be stripped with a recomputed ledger
   hash and still restore.
4. `bind_recursive_workload` accepts a snapshot with the root
   `source_release_refs` severed and still returns `no_drop_ok: true`; missing
   declared receipts, preimage receipts, handoffs and altered plans are
   correctly refused.
5. Constructed HELD and UNKNOWN frontier operations preserve their reason
   strings but both normalize `result_state` to `NOT_ELIGIBLE`; a consumer
   reading the normalized state cannot separate held/unknown.

The single passing probe confirms the governed frontier contract: bundle,
inventory, policy and frontier are consumed; JOINT/CO_TRAVEL/CONDITIONAL/FORK
classes are present; the baseline anti-join is true.

## R1 oracle adaptation

The previous R1 probes were adapted only for the repaired API paths:

- R1 H1 checked the unary compiler signature; the successor probe checks the
  new `compile_governed_frontier` contract and governed ledger. The original
  full-finite-frontier assertion is preserved.
- R1 H2/H3 checked the unary `UniversalWorkloadResult.anti_join`; the successor
  probes check the governed same/cold assertion
  (`restore_governed_frontier_ledger`) and `native_receipt_anti_join` while
  preserving the original deletion/swap/duplicate requirement.
- R1 H4 checked the unary execution signature; the successor probe checks
  `bind_recursive_workload` root-lineage severance while preserving the original
  D3-must-drive-consumer assertion.
- R1 H5 checked unary result fields; the successor probe checks the governed
  per-operation ledger's HELD/UNKNOWN states while preserving the original
  typed-state separation requirement.

No original assertion was silently waived.

## Retained positive evidence

- Author R2 suite: 120 passed, 0 failed/error/skip.
- Governed frontier: 150 eligible, 147 supported, 3 unsupported, 150 native
  receipts, 330 facts, candidate/operation anti-joins true; 24 valid-empty
  result rows; pending budget records explicit and not executed.
- Actual D3 recursive binding: exact expected operations to receipts/facts,
  root and parent contrasts, minority, cold rebinding; missing receipt/plan/
  handoff mutations are refused.
- U43 issued module exact
  `31e84f49d624f5524906e9e7839d2873106f8249`; four-path scope and unchanged
  R01/R02/native owners.
- Prior unary value-fault positive retained; R2 author governed value
  mutation/restore test passes inside the 120 suite.

## Limits and NOT_REACHED

Sourcefree TEST_ONLY trusted-host only; no source respondent access. R04 joined
custody/durability, R05 lifecycle, F5-F8 global, original35/1890 N11,
N12/Sorok, protected CI/production and J52/W52 remain NOT_REACHED. The required
minimal functions are listed in `defects_and_limits.md`; no candidate repair or
new architecture is authorized here.

## Artifacts and remote verification

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/` JUnit/logs, `evidence/`, `proof_witness.json`,
`manifest.json`, `RESUME.md`. The reviewer branch is pushed non-force; direct
remote readback of the evidence commit and final tip is recorded in
`evidence/remote_readback.txt` and reported to the coordinator. The candidate
branch remains at `2d32d68e2a5acb9cac136c313e82068dfb8e6ba1`.
