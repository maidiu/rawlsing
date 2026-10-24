# R61-R03V R3 remaining failures and limits — REVISE

Verdict: **REVISE**. R3 fixes the full-strip refusal, root-release severance and
HELD/UNKNOWN separation, and retains the governed/D3/value positives. The exact
cold native fact/job identity is still self-referential: a fully self-consistent
single-fact removal, fact duplication or expected-job substitution is accepted.

## Prioritized remaining failures

### 1. Self-consistent native fact omission survives restore (blocking)

**Expected:** removing one meaningful native fact from the persisted R03 result
must make the same cold/consumer fact-closure assertion fail or refuse, even
when every internal hash is recomputed.

**Observed:** starting from a genuine governed ledger, remove one native fact
from all of:
- `native_facts`,
- top-level `fact_refs`,
- the owning receipt's `semantic_fields.empirical_fact_refs`,
- the corresponding operation row's `fact_refs`,

then recompute `ledger_hash`. `restore_governed_frontier_ledger` accepts. The
candidate validates internal coverage of the remaining facts but has no
independently retained expected fact set. The nominal operation/candidate IDs
are unchanged.

**Required minimal function:** retain an independently expected native fact
identity/multiplicity set (derived from the issued plan/workload and native
owner contract, not solely from the submitted ledger) and require exact equality
before accepting the cold result.

### 2. Self-consistent native fact duplication survives restore (blocking)

**Expected:** duplicating a native fact while preserving nominal operation IDs
must refuse.

**Observed:** duplicate a native fact in `native_facts`, top-level `fact_refs`,
one receipt's `empirical_fact_refs` and one operation row's `fact_refs`, then
recompute `ledger_hash`. Restore accepts; the internal `fact_by_key` mapping
collapses duplicates and no expected multiplicity/duplicate-fact check exists.

**Required minimal function:** compare exact expected fact identity
multiplicity, not set coverage/dict keying, and reject duplicate facts.

### 3. Self-consistent expected-job substitution survives restore (blocking)

**Expected:** substituting expected native job query/predicate identities while
keeping the nominal operation IDs must refuse.

**Observed:** change the ledger `expected_jobs` and the matching
`compilation.issued.expected_jobs` to forged query/predicate refs, recompute
`compilation_hash` and `ledger_hash`, and restore accepts. The check only
compares the ledger's expected jobs with the same (mutable) compilation
material; it does not verify them against the issued plan/workload or an
independent expected-job record.

**Required minimal function:** anchor expected jobs to the independently issued
plan/workload/native owner identities and compare exact query/predicate/job
identity and multiplicity before accepting the ledger.

## Fixed R2 requirements (retained)

- Full-strip of all native receipts/facts with recomputed hash is refused.
- Checkpoint-valid root source-release severance is refused; baseline D3
  binding, root/parent contrasts, minority and cold restore pass.
- HELD/UNKNOWN remain distinct in live and cold operation ledger; supported,
  valid-empty, unsupported and pending remain present.
- Author R3 suite: 13 passed; retained R01 suite: 32 passed.
- Governed frontier remains real: joint/conditional/co-travel/fork classes,
  147 supported / 3 unsupported / 150 receipts / 330 facts, explicit pending.
- U43 blob exact `31e84f49d624f5524906e9e7839d2873106f8249`; four-path scope and
  unchanged U43/binding/R01/R02/native owners.
- Physical source value mutation/restore remains green at the tested grain.

## Limits / not reached

Sourcefree TEST_ONLY local trusted host only; no source respondent access. R04
joined durable custody, R05 lifecycle/grades, F5-F8 global, original35/1890
N11, N12/Sorok, protected CI/production and J52/W52 remain NOT_REACHED. No
candidate repair, self-adoption, new worker, cryptographic issuer or
production merge.
