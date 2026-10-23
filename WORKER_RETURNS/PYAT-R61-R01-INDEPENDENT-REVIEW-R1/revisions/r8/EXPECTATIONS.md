# R61-R01V R8 independent expectations — frozen before R8 code/author inspection

Status: reviewer-owned successor oracle frozen and committed before reading R8
candidate code, R8 author tests, R8 author return or any R8 author contract.
Sourcefree TEST_ONLY. Reviewer is the existing distinct session
`ses_e96304356ffeC8HSvwFluWOjG1`, never author
`ses_e98c905cbffekusoHURfKyEUKG`. Same opencode-go/deepseek-v4.1-flash
MAX/Global account; role/session/worktree separation only, not institutional
independence and not proven OS isolation.

## Exact target, startup and write scope (verified before freeze)

- Commission: `d5e9d097966401eee88005bba87084d6339e2685`
  `WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R01V/revisions/r8/00_COMMISSION.md`.
- Exact candidate/startup: `813775c07f0831605b6484a1d82afada30d85968`.
- Reviewer branch: `agent/opencode-pyat-r61-r01v-r8-independent-review-r1`.
- Mandatory first-tool preflight passed exactly in
  `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r5`, same top level,
  expected branch, no tracked changes.
- Reviewer writes only
  `WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r8/`.
  Probes, versioned adapters, snapshots, JUnit and witness remain below that
  root. Candidate, native owners, R5/R6/R7 oracles, director/HQ checkout, other
  nodes, original data, CI/prod/N11/N12/Sorok/J52/W52 stay untouched.
- Governing inputs read before this freeze: R8 commission; exact previous R7
  review `bfebaeefa452eac90e4b2153c05d17b018347551` (return, defects, probes,
  oracle); full R61AF
  `e349da0d886d8e365648afccf40a2e6b8e105ff7`; full R61V
  `8c03f95ca77a4c874449fff67a4032f83d9d0a02`; R61L E1-E6
  `3cb1d659bc9efb10b307e66db5cf26af3256f1f5`; R61M S1/S2
  `37dba2837c94ddb71287ffbc18260d051fc9765a`.
- Four R01 code paths remain the expected allowlist:
  `rawlsing_next/universal_grammar/types.py`,
  `rawlsing_next/universal_grammar/enumerate.py`,
  `rawlsing_next/universal_grammar/native_map.py`,
  `rawlsing_next/tests/test_universal_grammar.py`.
  Author report root `WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r8/`;
  its manifest must self-exclude and its report hashes plus four code blobs must
  be independently reproduced. Author passes are supporting only.

## R8 scope: targeted remaining R7 defects, not architecture

The R61V/R61AF whole-function contract remains. R8 must repair the actual
remaining R7 validation defects without reopening architecture or replacing the
productive retained owner.

The exact remaining R7 defects are:

1. `target_label` is not bound to the actual query target. A wrong label with
   the original query, and a correct label with a different query target, were
   both accepted and executed.
2. A condition catalog `(key, value)` is not bound to the predicate's actual
   typed response semantics. `(s1,0)->s1=1` was accepted and executed under the
   false `s1=0` label.
3. A malformed public `issue(condition_refs)` key raises raw `AttributeError`
   instead of a typed `RecurrenceRefusal`.
4. Duplicate condition refs raise bare `ValueError` with
   `RECURRENCE_DUPLICATE_CONDITION_PREDICATE` instead of `RecurrenceRefusal`
   (secondary but part of typed-refusal consistency).

The expected fix must use the shared create/execute/restore validator so the
same rules apply live and cold; no divergent checks per API; no new engine,
pin service, native-owner edit or scientific authority.

## Independent oracle and required evidence

### 1. Targeted R8 hostile successor
- H1 target label mismatch: `target_label="wrong-label"` with the original
  `t` query must typed-refuse at create; the correct label must still create.
- H2 query target mismatch: `target_label="t"` with a query targeting `s3`
  must typed-refuse; a matching `t` query must still create.
- H3 catalog semantics: `(s1,0)` bound to the `s1=0` predicate must create;
  `(s1,0)` bound to the `s1=1` predicate must typed-refuse. A valid catalog
  with both correct conditions must still create/issue/execute.
- H4 malformed condition key: `condition_refs=(("s1",0),)` must raise
  `RecurrenceRefusal`, not AttributeError, and leave no issuance record.
- H5 duplicate condition refs: must raise `RecurrenceRefusal`, not bare
  ValueError, and leave no issuance record.
- Restore must reject a snapshot whose target/query or condition inventory
  differs from the frozen context through the same validator; genuine snapshot
  must restore and cold-activate.

### 2. Retained R7 positive/control/cold regressions
Reuse the immutable R7 independent probes via versioned adapters only below the
R8 root; do not edit archived probes. Required retained results:
- Author R8 suite (supporting) and prior R3 A1-A3 controls with reviewer JUnit.
- Changed-data D=3 owner positive: independent expected operation sets and
  multiplicity, independently recomputed root/parent typed states, neutral
  aggregate hidden 75/25 opposition, nonwinning exploration.
- In-process and fresh-process cold restore, including post-activation and
  completed-prefix pre-activation restore -> real activation -> N+1 without
  rerunning or recounting the original execution.
- Chronological issue head independent of generation: >=2 generation-1 batches
  with exact counts; later-generation batches; stopped/no-work records advance
  the head with zero work and no refund.
- Fixed original pin refuses altered/rehashed snapshot and missing pin; genuine
  restore passes. Forged-both-inputs remains a documented host-trust
  demonstration, not an in-scope refusal gate.
- Retry has no second native call/budget charge; run-local concurrency is
  serialized or typed-refused; inflight/ambiguous stays typed HOLD.
- Deep-detached inspect and no public view/record injection; missing
  receipt/handoff/ancestry/cumulative/activation closure refuses; typed receipt
  states are retained; legacy no-owner helpers cannot feed the campaign.
- SAME configured coordinator baseline -> meaningful source/receipt/parent/
  history mutation refusal/failure -> restoration PASS.

### 3. F1-F6 and API matrix
Record the full F1-F6 matrix, actual commands/exits/skips, native imports/blobs,
exact operation sets/content/multiplicity, runtime/memory where used, JUnit,
probe outcomes, assertion fault/restoration, proof witness, manifest with
explicit self-exclusion and RESUME. Distinguish actual product refusals from
setup/import/signature crashes. No all-refuse pseudo-success.

## Verdict rule

`ACCEPT_SCOPED_LOCAL` only if the targeted R7 defects are actually fixed through
the shared validation path and the retained R7 native/cold/hostile positives
still pass at the exact candidate, under the declared local trusted
coordinator/TEST_ONLY profile. Otherwise `REVISE` with the exact minimal
reproducible missing function. R03 remains NOT_STARTED. No original/world/
full-machine/science qualification follows. Reviewer does not repair or adopt.
R08/R61Q is a separate lane and is not inspected, repaired or certified here.

## Artifacts and stop

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/`, `evidence/`, `proof_witness.json`,
`manifest.json` with explicit self-exclusion, `RESUME.md`. Max 35 minutes/bank
25; stop after decisive bounded review. No candidate edit, no self-adoption,
no R03 wake, no new court, no review-of-reviewer.
