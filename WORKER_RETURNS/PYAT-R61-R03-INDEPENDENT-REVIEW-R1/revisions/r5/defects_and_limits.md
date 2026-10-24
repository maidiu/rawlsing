# R61-R03V R5 defects and limits — ACCEPT_SCOPED_LOCAL

Verdict: **ACCEPT_SCOPED_LOCAL**. The R5 candidate closes the remaining R4
capture defects through one shared pin-free structural/closure/multiplicity
validator used by both live capture and cold restore. The fixed-original-pin
cold path, prior cold fault refusals, genuine restore, and the retained native
governed/D3/HELD/UNKNOWN positives all pass. No blocking defect remains.

## Fixed R4 capture defects

- `freeze_restore_checkpoint()` now builds `self.ledger()` and calls the same
  `_validate_governed_ledger_material` used by cold restore before returning a
  checkpoint. It no longer trusts anti-join flags/nonempty refs alone.
- Empty operation ledger and duplicated `fact_refs` with true flags now refuse
  checkpoint capture (reviewer H4/H4b).
- Missing/invalid expected job, candidate, operation, receipt/fact closure,
  duplicate native fact identity or invalid multiplicity cannot be blessed by a
  true flag.
- `restore_governed_frontier_ledger` still requires the separately provisioned
  original pin, checks the submitted self-hash and pin, then calls the same
  validator. No unpinned fallback.
- Lawful shared-fact receipt associations remain accepted; duplicate native
  fact-catalogue identities are rejected.

## Independent evidence

- Author R5 suite: 16 passed, 0 failed/error/skip.
- Retained R01 suite: 32 passed, 0 failed/error/skip.
- Reviewer fixed-pin/capture probes: 5 passed, 0 failed:
  - genuine original-pin restore passes; missing/wrong pin refuses;
  - fact deletion, fact duplication and expected query/predicate job
    substitution refuse against the genuine original pin with genuine restore
    between faults;
  - content mutation retaining advertised refs refuses;
  - empty operation ledger cannot capture a checkpoint;
  - duplicated `fact_refs` cannot capture a checkpoint.
- Retained real governed joint/conditional/D3/root-parent/minority/pending/
  source-value and HELD/UNKNOWN positives remain in the focused suite.
- U43 blob `31e84f49d624f5524906e9e7839d2873106f8249` exact; four-path scope;
  U43/binding/R01/R02/native owner bodies unchanged.

## Residual limits / non-blocking notes

- The R5 source contains a duplicated, immediately shadowed first definition of
  `restore_governed_frontier_ledger`. It is dead code and does not affect the
  executed second definition or any test; it is recorded as a code-cleanliness
  note, not a functional gap.
- Sourcefree TEST_ONLY local trusted host only; no source respondent access.
- Both pin and candidate replaced by a different trusted host is the R61AF
  excluded boundary, not an in-scope refusal requirement.
- R04 joined custody/durability, R05 lifecycle/grades, F5-F8 global,
  original35/1890 N11, N12/Sorok, protected CI/production and J52/W52 remain
  NOT_REACHED. No cryptographic issuer or durable custody is claimed.
- No candidate repair, self-adoption, new worker/provider, production merge or
  downstream R04/R05 wake.

## Minimal missing function

None for the commissioned R5 scope. The shared capture/restore validator is
present and independently falsified at the required boundaries.
