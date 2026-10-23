# R61-R01V R4 independent native qualification return — REVISE

**Verdict: `REVISE` for R01 A4 at the generic recurrence interface.** The
candidate demonstrates a real three-generation native chain and preserves R3
A1–A3, but the new recurrence consumer does not authenticate the receipt-bound
parent or enforce generation continuity. The same next-generation I05 consumer
therefore accepts a severed/forged receipt binding and accepts a root operation
relabelled as generation 2. A4 remains **not qualified** at the commissioned
grain. This is not R03 issuance/adoption and not original science.

## Exact identity and separation

- Commission: `2cae526625b41b59e590c025370c9214ae6cba00`
  `WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R01V/revisions/r4/00_COMMISSION.md`.
- Candidate/startup: `5c77413365b9d45375b25dbaa29cb3da497bcb10`.
- Reviewer branch: `agent/opencode-pyat-r61-r01v-r4-independent-review-r1`;
  direct remote at start/end required to match the pushed reviewer commit.
  Author branch `agent/opencode-pyat-r61-r01-generic-grammar-r1` was the same
  SHA at review start.
- Profile freeze `f3601f418d79c83d467ce8dd0ed1c0113c31d7e8` preceded code and
  the two profile files are byte-identical at the candidate.
- R4 changed code paths are only `rawlsing_next/universal_grammar/native_map.py`
  and `rawlsing_next/tests/test_universal_grammar.py`; both are in the R01
  allowlist. `types.py` and `enumerate.py` retain R3 blobs.
- Four code blobs: `types.py` `e7b196efe5b1f86134c27a80bfdd8f472be76e5d`,
  `enumerate.py` `fd9203a0b272f98771c24070d01a9e5287c9b099`,
  `native_map.py` `c21d896d0c25a4352f379fe32fca0c1546e1a88d`,
  `test_universal_grammar.py` `2b15177a7c60499c81c506245a5899055f63bfe3`.
- All eight author report artifacts match the author SHA-256 manifest; the
  manifest excludes itself. No candidate file was edited by this reviewer.
- Reviewer session is distinct from author `ses_e98c905cbffekusoHURfKyEUKG`;
  same provider/account is disclosed and is not institutional independence.
  Browser whole-native runtime remains unqualified.

## Independent replay

| Suite | Result | Evidence |
|---|---|---|
| Author R4 suite | 24 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Prior R3 A1–A3 controls on candidate | 10 passed, 0 failed/error/skip | `replay/r3_controls_junit.xml`, `.log` |
| Own R4 probes | 7 passed (defect demonstrations are intentional) | `replay/own_probes_junit.xml`, `.log` |

The author suite exercises a real unchanging-I05 chain for generations 1–3,
exact per-generation anti-join, a cold subprocess loading persisted handoffs, a
nonwinning exploratory parent, a neutral-aggregate hidden-differentiation case,
and typed K/D/cap refusals. Those are genuine positive capabilities of the
candidate. R3 A1 conditioned JOINT/CO_TRAVEL, A2 canonical operation ID, and A3
empty/unsupported/pending controls still pass unchanged.

Own probe B6 confirms that for a non-root receipt-bound parent the two profile
comparators have distinct baseline predicate hashes and distinct expected
condition sets, and both execute. Value-level opposite-direction arithmetic was
not independently recomputed because the blocking identity defect below
prevents upgrading A4; it remains a follow-up falsifier, not a claimed pass.

## Blocking findings (minimal reproducible)

All probes are in `probes/test_r01v_r4_reviewer.py`; exact commands are in
`proof_witness.json`.

1. **Receipt-bound parent binding is not authenticated (blocking).**
   `execute_recurrence_generation` checks only
   `discovery_authority.candidate_grammar_ref` against the generated grammar.
   It never checks `RecurrenceParent.receipt_ref`, `replay_binding_ref`,
   `handoff`, `source_release_refs`, or that `parent.predicate` equals
   `handoff.winning_predicate` / the canonical parent id. Probe B1 replaces a
   valid parent's receipt and replay refs with bogus `ExactRef`s: the generated
   grammar and every expected operation ID are identical and the SAME I05
   next-generation consumer passes its anti-join. Probe B5 constructs a
   `PARENT_RECEIPT_BOUND` parent with `receipt_ref=None`, `replay_binding_ref=None`,
   `handoff=None` and a caller-chosen predicate; generation 2 executes and the
   anti-join passes. This directly violates commission item 2 (severing/altering
   the parent receipt/binding must affect or refuse the same consumer) and the
   "exact canonical persisted parent" requirement. Wrong source/edition/replay
   is likewise not separately validated; the parent's `source_release_refs` are
   not compared with the execution `release_refs`.
2. **Generation continuity is not enforced (blocking).**
   `build_recurrence_issue_plan` checks only `1 <= generation <= D`. Probe B2
   builds a `generation=2` plan whose only parent is `PARENT_ROOT,
   generation=0`; it executes natively and passes the anti-join. This is exactly
   the prohibited "repeated root calls with new generation labels" masquerading
   as recurrence.
3. **Cumulative budget is caller-declared, but the return claims enforcement
   (secondary).** Probe B3 builds the same generation with
   `total_issued_before=8` versus `0` under a wider cap; the understated caller
   state issues more operations. Probe B7 shows total exhaustion raises
   `RECURRENCE_GENERATION_ISSUED_NO_OPERATIONS` instead of returning an explicit
   unissued/PENDING record. `total_issued_before` is not carried in
   `RecurrenceIssuePlan.material()`, so the plan does not bind the cumulative
   ledger it used. The author return/matrix claim a "cumulative" cap; it is only
   a trusted scheduling input. This is acceptable only after it is declared as
   such and the per-plan ledger state is bound; otherwise an actual cumulative
   ledger seam is required.

## Minimal missing function / owning seam

`rawlsing_next/universal_grammar/native_map.py`:

- `execute_recurrence_generation` / `build_recurrence_issue_plan` must validate
  receipt-bound parents before issuing: canonical parent id recomputation,
  `parent.predicate == handoff.winning_predicate`, `receipt_ref ==
  handoff.receipt_ref`, `replay_binding_ref == handoff.ref`, exact source
  release equality with the execution releases, and typed refusal for
  missing/stale/forged binding. Exploratory parents must remain explicitly
  receipt-free and source/risk-valid.
- Enforce `generation == max(parent.generation) + 1` (root only for generation
  1) or make the parent generation/lineage part of the authenticated contract.
- Either enforce an append-only cumulative issued ledger (exact prior plan/root
  hash + issued count) or declare `total_issued_before` as a trusted caller
  scheduling input and stop claiming cumulative enforcement in the return;
  represent exhaustion as explicit unissued/PENDING, not a bare no-operations
  error.

## A4 / R03 status

- A4 is **not qualified** at the generic interface grain. The positive D=3
  mechanism is real for the author-controlled chain, but the consumer does not
  bind the parent receipt/binding or the generation relation.
- R61-R03 prerequisite evidence still missing: authenticated receipt-bound
  parent lineage, enforced generation continuity, source/edition/replay
  negatives, and honest cumulative issued-set accounting. R03 must remain
  NOT_STARTED.
- Preserved limitations: the reference numbers are TEST_ONLY; the legacy
  unconfigured-A4 gap label remains distinguishable; runtime/cardinality
  capacity recorded by the author (3 generations, 12 operations, ~0.41 s,
  ~31 MB) is unchanged. No original 35/1890, global F6/F7/F8, N11/N12, Sorok,
  production/CI, J52/W52, source or science claim is made.

## Artifacts

`EXPECTATIONS.md` (frozen before candidate inspection), `defects.md`,
`probes/`, `replay/`, `evidence/startup_and_identity.txt`,
`independent_oracle_results.json`, `proof_witness.json`, `RESUME.md`,
`SHA256manifest.json` (explicit self-exclusion).
