# R61-R03V R5 independent expectations — frozen before candidate code inspection

Status: reviewer-owned successor oracle frozen and committed before reading the
R5 candidate code or drawing conclusions from the R5 author return. Sourcefree
TEST_ONLY, trusted-host only. Reviewer is the existing distinct R03V reviewer,
not the author/HQ. Same OpenCode Go DeepSeek V4.1-Flash MAX/Global account;
role/session separation only, not institutional or OS isolation.

## Exact target, startup and write scope

- Commission: `0f6acf2317ecd561e754af984da256c90c43be86`
  `WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R03V/revisions/r5/00_COMMISSION.md`.
- Exact candidate/startup: `c912497b25411ebbd3d796db139f32f5bebb6c4c`.
- Reviewer branch: `agent/opencode-pyat-r61-r03v-r5-independent-review-r1`.
- Prior independent review: `61356022db35254193605ae1cf749b1dff29794e`
  (`REVISE` against R4 candidate `8c506f8f239204b004e4b677572898c8dba06811`).
- Settled R61AV decision:
  `7a36e8091eda463c736f4ca0528d47f061b26cce`
  (`R61AV_R03_COLD_RESTORE_FIXED_PIN_DECISION.md`) remains the oracle.
- Fixed-original-pin cold restore is already qualified; no new trust boundary,
  pin service, R04 custody, cryptographic issuer or architecture is required.
- Reviewer writes ONLY
  `WORKER_RETURNS/PYAT-R61-R03-INDEPENDENT-REVIEW-R1/revisions/r5/`.
  R1/R2/R3/R4, author, code/test, old oracles, PRE-MAIN HQ, science, CI/prod,
  original respondents, Sorok, N11/N12 and J52/W52 stay untouched.
- No candidate repair, new worker/provider/codex, or expanded audit census.

## Exact remaining R4 capture defects to close

The R4 fixed-pin cold restore qualified, but the live capture interface
`GovernedFrontierResult.freeze_restore_checkpoint()` checked only anti-join flags
and nonempty refs. It accepted an empty operation ledger and duplicated
`fact_refs` while flags remained true. R5 must use the SAME structural/closure/
expected-mapping/multiplicity validator used for cold restore before returning a
checkpoint.

Required behavior:
1. Empty operation ledger, missing expected operation/job/candidate mapping,
   missing native receipt/fact closure, duplicate native fact identities or
   invalid fact multiplicity cannot acquire a completed checkpoint merely
   because the anti-join flags are true.
2. Real original live result validates, captures the canonical checkpoint, and
   restores with the separately retained original pin. Genuine fresh-process
   restore performs no native rerun/new issuance/budget charge.
3. Lawful shared-fact associations (one fact referenced by multiple receipts)
   remain accepted; only duplicate native fact-catalogue identities are
   invalid.
4. The prior fixed-pin hostile probes (fact deletion, fact duplication, expected
   query/predicate job substitution, content mutation retaining refs, missing/
   wrong pin) still refuse with explicit genuine original pins, and a genuine
   restore passes between/after faults. Missing-argument exceptions alone do
   not establish proof.
5. Retain real governed joint/conditional/D3/root-parent/minority/pending/
   source-value and HELD/UNKNOWN positives; focused R5 16 and retained R01 32
   plus indispensable independent capture/fixed-pin probes.
6. U43 blob `31e84f49d624f5524906e9e7839d2873106f8249`, four-path scope and
   U43/binding/R01/R02/native owners remain exact/unchanged.

## Independent falsifiers

- Build a genuine governed result, capture the real checkpoint, and verify:
  empty `operation_ledger` with true flags refuses capture; duplicated
  `fact_refs` with true flags refuses capture; missing expected candidate/job/
  operation mapping refuses; missing receipt/fact closure refuses; shared facts
  across receipts remain lawful.
- Verify genuine fresh-process restore with the original pin, no native rerun,
  no new issuance/budget charge.
- Reuse the R4 fixed-pin probes with explicit pins for the three prior cold
  faults; genuine restore passes between faults.
- Check the focused author 16 and retained R01 32 under the reviewer harness;
  author passes are supporting only.
- Preserve U43/native owner exactness and all inherited positives.

## Verdict rule

`ACCEPT_SCOPED_LOCAL` only if the shared capture/restore validator now genuinely
qualifies the commissioned functions and all prior fixed-pin/native positives
remain. Otherwise `REVISE` with only reproducible necessary gaps. No residual
uncertainty, R04/science/prod/CI/N11/N12/Sorok/J52/W52 expansion, self-adoption
or candidate repair.

## Artifacts and stop

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/`, `evidence/`, `proof_witness.json`,
`manifest.json` with explicit self-exclusion, `RESUME.md`. Bank 30 minutes;
stop by 60 on a finite verdict; commit/push own branch non-force and direct
remote verify.
