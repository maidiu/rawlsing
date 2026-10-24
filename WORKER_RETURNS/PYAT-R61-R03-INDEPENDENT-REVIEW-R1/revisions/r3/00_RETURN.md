# R61-R03V R3 independent native qualification return — REVISE

**Verdict: `REVISE` for the R3 successor.** R3 fixes the full-strip refusal,
root-source-release severance and HELD/UNKNOWN normalization, and retains the
governed-frontier/D3/value positives. The cold native fact/job identity remains
self-referential: self-consistent single-fact removal, fact duplication and
expected-job substitution are accepted. R03 is not accepted; no self-adoption,
production merge or downstream wake.

## Exact identity and separation

- Commission: `36c8e6ab123562de902f0b53ae9846a3b3560df5`.
- Exact candidate/startup: `5b28d09602a35d4c5d5f060f450956c612ab3580`.
- Author contract: `8f2864ff648f63542746f69e6687de0d36117294`.
- Author code: `f87166a27d0e2e54ccc7e31fac58fa5487888035`.
- Previous R2 review: `3853c2a8c609e53cbc6d6ebf852540faa40bd6c2`; R1
  EXPECTATIONS remains the claim oracle.
- Reviewer branch: `agent/opencode-pyat-r61-r03v-r3-independent-review-r1`.
- Mandatory first-tool preflight passed exactly at the stable worktree, branch
  and HEAD, with only untracked pycache.
- Reviewer EXPECTATIONS were frozen and committed (`7ac6bf910`) before R3
  candidate code inspection.
- Reviewer is the existing distinct R03V reviewer, not author/HQ; same
  account/provider is disclosed and is not institutional or OS isolation.

## Independent replay

| Suite | Result | Evidence |
|---|---|---|
| Author R3 suite | 13 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Retained R01 suite | 32 passed, 0 failed/error/skip | `replay/r01_suite_junit.xml`, `.log` |
| Reviewer successor probes | 3 passed, 3 failed required behaviours | `replay/hostile_probes_junit.xml`, `.log` |

The three failures are product gaps, not setup/import crashes:

1. Remove one native fact from `native_facts`, top-level `fact_refs`, the owning
   receipt's `empirical_fact_refs` and the operation row `fact_refs`, recompute
   `ledger_hash`: `restore_governed_frontier_ledger` accepts.
2. Duplicate one native fact in the same ledger structures with recomputed hash:
   restore accepts; no expected-fact multiplicity/duplicate check.
3. Substitute expected job query/predicate refs in both `ledger.expected_jobs`
   and `compilation.issued.expected_jobs`, recompute both hashes: restore
   accepts; expected jobs are not anchored independently to the issued
   plan/workload.

The three passing probes confirm the governed contract, checkpoint-valid root
release severance refusal, and live/cold HELD/UNKNOWN separation.

## Retained positive evidence

- Author R3 suite 13 passed; retained R01 suite 32 passed.
- Governed frontier: real inventory/policy/frontier, joint/conditional/
  co-travel/fork classes, 147 supported / 3 unsupported / 150 receipts / 330
  facts, explicit pending, candidate/operation anti-joins true.
- Real D3 binding: exact expected operations to receipts/facts, root/parent
  contrasts, minority, cold; checkpoint-valid root release severance refused.
- Full-strip of all native receipts/facts with self-rehash is refused.
- U43 blob `31e84f49d624f5524906e9e7839d2873106f8249` exact; four-path scope;
  unchanged U43/binding/R01/R02/native owner bodies.
- Physical source value mutation/restore remains green at the tested grain.

## Exact minimal missing function

Retain an independently expected native fact/job identity and multiplicity set
outside the mutable submitted ledger/compilation, derived from the issued plan/
workload/native owner contract, and require exact equality on cold restore. In
particular:
- compare expected fact identity multiplicity, not set/dict coverage, and
  reject duplicate facts;
- verify expected job query/predicate identities against the issued plan/
  workload, not only against the same mutable compilation material;
- a self-consistent removal/duplication/substitution with all internal hashes
  recomputed must refuse.

## Limits and NOT_REACHED

Sourcefree TEST_ONLY trusted-host only; no source respondent access. R04 joined
custody/durability, R05 lifecycle/grades, F5-F8 global, original35/1890 N11,
N12/Sorok, protected CI/production and J52/W52 remain NOT_REACHED. No candidate
repair, self-adoption, new worker, cryptographic issuer or production merge.

## Artifacts and remote verification

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/` JUnit/logs, `evidence/`, `proof_witness.json`,
`manifest.json`, `RESUME.md`. The reviewer branch was pushed non-force. Evidence commit
`781bdfcc1b7bc69d6406c1c3061859298bee7d02` was directly read back at the
remote, as recorded in `evidence/remote_readback.txt`; the final branch tip is
also verified by direct remote readback and reported to the coordinator. The
candidate branch remained at `5b28d09602a35d4c5d5f060f450956c612ab3580`.
