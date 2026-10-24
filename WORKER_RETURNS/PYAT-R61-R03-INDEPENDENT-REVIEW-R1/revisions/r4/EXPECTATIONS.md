# R61-R03V R4 independent expectations — frozen before candidate code inspection

Status: reviewer-owned successor oracle frozen and committed before reading the
R4 candidate code or drawing conclusions from the R4 author return. Sourcefree
TEST_ONLY, trusted-host only. Reviewer is the existing distinct R03V reviewer,
not the author/HQ. Same OpenCode Go DeepSeek V4.1-Flash MAX/Global account;
role/session separation only, not institutional or OS isolation.

## Exact target, startup and write scope

- Commission: `3e7d0df8a9c3d6dd37949b1e9abc490afcef739a`
  `WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R03V/revisions/r4/00_COMMISSION.md`.
- Exact candidate/startup: `8c506f8f239204b004e4b677572898c8dba06811`.
- Reviewer branch: `agent/opencode-pyat-r61-r03v-r4-independent-review-r1`.
- Prior independent review: `7d8396329ed8ac2df86c82bb46e785a0dc487cde`
  against R3 candidate `5b28d09602a35d4c5d5f060f450956c612ab3580`.
- Governing R61AV decision:
  `7a36e8091eda463c736f4ca0528d47f061b26cce`
  `PYAT_CONTROL_ROOM/CONTINUOUS_DEVELOPMENT/R61AV_R03_COLD_RESTORE_FIXED_PIN_DECISION.md`.
- Original full R03 claim oracle/positive scope remains inherited; architecture,
  product/science and R03 scope are not reopened.
- Reviewer writes ONLY
  `WORKER_RETURNS/PYAT-R61-R03-INDEPENDENT-REVIEW-R1/revisions/r4/`.
  R1/R2/R3, author, code/test, old oracles, PRE-MAIN HQ, science, CI/prod,
  original respondents, Sorok, N11/N12 and J52/W52 stay untouched.
- No candidate repair, new worker/provider/Codex, cryptographic issuer, new
  persistent pin service or R04 custody requirement.

## Settled R61AV requirement

The prior cold API accepted only the submitted ledger; its jobs, compilation,
facts, refs and self-hashes could all be changed consistently. R61AV fixes one
trust boundary: the trusted coordinator captures the canonical checkpoint of
the ORIGINAL validated live R03 result and retains it separately from the
submitted ledger. Cold restore requires that exact separately supplied original
reference; structural/closure validation remains.

Required public behavior:
1. Live result exposes a trusted-host capture interface (e.g.
   `freeze_restore_checkpoint() -> str`) that verifies successful
   candidate/operation no-drop, eligible accounting, complete expected
   operation/job/candidate mapping, native receipt/fact closure and valid
   multiplicities, and returns the canonical whole-result checkpoint. A failed
   or incomplete live result cannot acquire a completed restore checkpoint.
2. Cold API `restore_governed_frontier_ledger(ledger, *,
   expected_checkpoint_ref: str | None = None)` requires the separately
   retained original pin. Missing/malformed/mismatched pin refuses with
   `WorkloadBindingRefusal` before any restored result. No unpinned compatibility
   fallback.
3. Compute canonical material hash excluding only `ledger_hash`; require both
   the submitted self-hash and the independently supplied original checkpoint to
   equal it; retain schema and full structural/closure validation. Preserve
   ordered fields ordered and unordered collections as canonical multisets;
   do not erase multiplicities.
4. Genuine fresh-process restore with the separately provisioned original pin
   releases the original result without native execution, new issuance or
   budget charge.
5. A byte/content mutation retaining advertised fact refs must change committed
   canonical material and refuse. Duplicate native fact-object catalogue
   identities must be rejected; lawfully shared facts referenced by multiple
   receipts remain lawful. Failed candidate/operation anti-join or invalid fact
   multiplicity cannot acquire a completed checkpoint.
6. A different trusted host supplying both a forged ledger and its forged pin
   is outside the fixed-host trusted-runtime promise (R61AF boundary), not an
   in-scope product refusal. Same-UID/private-state/root replacement remains
   excluded.

## Independent falsifiers (same fixed coordinator/source/plan/pin)

- Capture the genuine live checkpoint with the trusted host; store it
  separately from the ledger; fresh-process restore with that pin passes with no
  native rerun/new budget.
- Re-run the three prior coordinated cold probes against the fixed original pin:
  single native fact deletion, native fact duplication, expected query/predicate
  job substitution — each with all internal hashes recomputed — must refuse.
- Missing pin, malformed pin, wrong pin and pin selected from submitted payload
  must refuse; a genuine restore between/after faults must pass.
- Content mutation retaining advertised fact refs, dropped/swapped receipts/
  facts, duplicate native fact catalogue entries and invalid expected
  candidate/job correspondence must fail before successful capture/restore.
- Preserve real governed joint/conditional/D3/root-parent/minority/pending/
  source-value and HELD/UNKNOWN positives; focused R4 15 and retained R01 32
  suites plus necessary independent fixed-host controls.
- No new broad audit/census; no R04 durable custody/cryptographic issuer.

## Verdict rule

`ACCEPT_SCOPED_LOCAL` only if the fixed-original-pin cold restore genuinely
binds the complete canonical original result and all prior cold fact/job
faults refuse at the same configured ingress, with genuine restore/no-rerun and
retained positives. Otherwise `REVISE` with the finite reproducible necessary
gaps. No self-adoption or candidate repair.

## Artifacts and stop

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/`, `evidence/`, `proof_witness.json`,
`manifest.json` with explicit self-exclusion, `RESUME.md`. Bank 45 minutes;
stop by 75 on a finite verdict; commit/push own branch non-force and direct
remote verify.
