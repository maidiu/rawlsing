# R61-R01V R3 independent review return — ACCEPT_SCOPED_LOCAL

**Verdict: `ACCEPT_SCOPED_LOCAL` at the R01/R03-facing generic lowering grain.**
A1, A2 and A3 are repaired and independently reproduced. A4 is an honest,
explicit `EXACT_CONTRACT_GAP`, not a silent collapse and not a D13 PASS.
This is **not** full whole-node R01 qualification for independent recurrence
and is not R03 execution/adoption. No source, science, production, N11/N12 or
J52/W52 claim.

## Exact review target and separation

- Candidate/startup: `9fbf1ec3bbd569b5fd83cfd9e20cb931523a42c5`.
- R3 code commit: `89774b01990a7d18c10cf4f6e819895776a1a633`; parent/prior
  candidate `f0c602eddaee14a58d6f0935a587a46fcf96c6db`.
- Base: `a54893657ba65e44c1049f763208b0b4b6ed5eb9`.
- Prior independent R2 review: `3ac1e498a08648950d31df0bf52750f9335d24fa`
  (REVISE; A1 blocking, A2/A3/A4 secondary).
- R3 repair commission: `3470da602618b5c04b1f28885b5ad1835169e2d5`.
- R3 review commission: `ed6cb8675baacc266ec9c85a566380048d30dded`.
- Reviewer branch: `agent/opencode-pyat-r61-r01v-r3-independent-review-r1`;
  worktree `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r3`.
- Author session `ses_e98c905cbffekusoHURfKyEUKG` is distinct from this
  reviewer session. Same provider account (`opencode-go/deepseek-v4.1-flash`,
  variant max, existing Global) is disclosed; this is role/session separation,
  not institutional scientific independence. Browser whole-native runtime
  remains unqualified.
- Reviewer `EXPECTATIONS.md` was committed before R3 code/author inspection:
  `1db7de32131a1ec4191fde6bbe3633a08894c357` (parent startup
  `9fbf1ec3b...`).

## Startup, remote, blobs, manifest and allowlist

- Direct `git ls-remote` at review start: author branch
  `agent/opencode-pyat-r61-r01-generic-grammar-r1` =
  `9fbf1ec3bbd569b5fd83cfd9e20cb931523a42c5`; reviewer branch also started at
  `9fbf1ec3b...`.
- All four R3 code blobs match the author manifest:
  - `rawlsing_next/universal_grammar/types.py` = `e7b196efe5b1f86134c27a80bfdd8f472be76e5d`
  - `rawlsing_next/universal_grammar/enumerate.py` = `fd9203a0b272f98771c24070d01a9e5287c9b099`
  - `rawlsing_next/universal_grammar/native_map.py` = `ea09c02efd273c92970b697397b78558647eb214`
  - `rawlsing_next/tests/test_universal_grammar.py` = `785ba9e13deba10ac72e1389add35c5914b4e7f2`
- All six R3 author report artifacts match their SHA-256 manifest entries; the
  manifest explicitly excludes itself and claims no future hash.
- `git diff --name-only f0c602ed..9fbf1ec3` is exactly the four R01 allowlist
  code paths plus the author R3 return root. Immutable prior author reports,
  reviewer returns, commissions, INPUTS and native owners are unchanged.
- Evidence: `evidence/startup_and_identity.txt`,
  `evidence/startup_and_identity.json`.

## Test replay (reviewer-owned JUnit)

| Suite | Result | Evidence |
|---|---|---|
| Author `test_universal_grammar.py` | 20 passed, 0 failed/error/skip | `replay/author_suite_junit.xml` / `.log` |
| Prior focused reviewer controls | 20 passed, 0 failed/error/skip | `replay/adapted_prior_probes_junit.xml` / `.log` |
| Own R3 A1-A4 probes | 10 passed, 0 failed/error/skip | `replay/own_probes_junit.xml` / `.log` |

The prior 20 controls were retained by exact identity except one meaningful R3
replay: the forged-direction probe now recomputes the canonical `op_id` before
lowering, because R3 correctly checks canonical identity before policy
revalidation. That is an adaptation to changed behavior, not a weakened
assertion; the original stale-ID path is independently covered by own A2 probes.
No deselected, import-crashed or stale path-derived result is counted as a
safety pass.

## A1 — conditioned JOINT / CO_TRAVEL: PASS

Reviewer-owned independent case: eight eligible SAMPLE conditioned
`JOINT`/`CO_TRAVEL` operations on ordered targets `(q_alpha,q_beta)` with one
typed condition from `q_gamma`/`q_delta` values 0/1.

- All eight lower `SUPPORTED` with a derived predicate in the joint baseline.
- Every `JOINT` and `MARGINAL_*` expected query role uses that derived
  predicate ref; none uses the all-response baseline.
- Values 0/1 produce disjoint derived predicate refs and distinct actual I05
  candidate identities.
- A multiple-conditioner `JOINT` produces one AND-derived predicate whose
  `dependency_refs` contain both exact condition predicate refs; all roles use
  it; actual I05 execution passes the reviewer exact join.
- Same-rule-id/atom-id mutation of the derived predicate makes both the
  reviewer-owned exact candidate/query-role join and the candidate
  `native_receipt_anti_join` fail; restoration passes; a cold subprocess
  reproduces the baseline/mutation/restoration result.
- Bijective item renaming preserves the eligible logical condition/frontier
  shape; enumeration has no values/observations input, so membership is not
  data-dependent.

This is a real capability delta from R2: the condition value is now consumed by
executed native predicate/query roles, not merely stored in `record.atoms` or
encoded in `rule_id`.

Evidence: `evidence/conditional_joint_repro.txt`,
`probes/test_r01v_r3_reviewer.py::test_A1_*`.

## A2 — canonical operation identity: PASS

- A forged `op_id` not equal to `urn:r61:op:<canonical_hash>` is typed-refused
  (`OPERATION_ID_NOT_CANONICAL`) and cannot retain `SUPPORTED`.
- A semantic condition change while retaining the old `op_id` is typed-refused.
- Recomputing the canonical ID for the changed operation lowers `SUPPORTED`
  normally, so revalidation is not a blanket refusal.
- Evidence: `probes/test_r01v_r3_reviewer.py::test_A2_*`.

## A3 — empty / unsupported / pending: PASS

- A nonempty eligible frontier with a catalog supporting no claims retains its
  exact unsupported operation IDs and reports `allow_empty_frontier=False`.
- A truly empty complete frontier reports `allow_empty_frontier=True` with no
  records.
- A budget-limited frontier with exact pending IDs reports
  `allow_empty_frontier=False`.
- Lowering records form a disjoint total partition over supported, unsupported
  and not-eligible identities, conserving all scientific operation IDs.
- Evidence: `probes/test_r01v_r3_reviewer.py::test_A3_*`.

## A4 — recurrence/baseline: honest preserved limitation

R3 does **not** implement independent governed recurrence/baseline
enumeration. It reports:

```text
kind = RECURSION_BASELINE_NOT_ENUMERATED
state = EXACT_CONTRACT_GAP
reason = R01_DECLARES_FORK_OVER_CONDITIONERS_ONLY_NO_INDEPENDENT_RECURRENCE_CHAIN
```

Independent findings:

- FORK rows carry `branch_depth` 1/2 and an independent `recursion_depth=0`;
  D is no longer used as a disguised conditioner-depth bound.
- `recursion_relation_ref`, `baseline_policy_ref` and exact parent
  `baseline_ref` are carried; D=3 is not exercised as an independent chain;
  D13 is not claimed PASS.
- The inherited contracts require D bounds and recursion/baseline identity
  (`INPUTS/CONTRACTS.md:24,30`) but define no typed recurrence relation or
  baseline issuer policy. `GrammarPolicy` stores only opaque string refs
  (`rawlsing_next/universal_grammar/types.py:437-438`); the enumerator only
  records the deferred gap (`rawlsing_next/universal_grammar/enumerate.py:489-497`).
  `rawlsing_next/pre553_recursive_handoff.py` consumes a caller-supplied parent
  predicate/replay binding; it does not define policy semantics for these refs.
- This is a generic synthetic/software contract gap, not an original-source
  scientific issuance requirement. R3 did not manufacture a scientific issuer
  blocker and did not invent a recurrence chain.

A4 is therefore an **honest preserved limitation**, not a new blocking defect.
It is **not** full R01 generic recurrence functionality. The smallest generic
engineering option is to define a typed dyadic recurrence relation plus a
baseline selection policy and enumerate repeated generations up to D; that is a
contract/issuer decision, not something this reviewer may invent.

Evidence: `evidence/recursion_diagnostic.txt`,
`probes/test_r01v_r3_reviewer.py::test_A4_*`.

## Separate exact findings

### (i) Demonstrated R3 capability delta and remaining defects

- Delta: A1 conditioned joint/co-travel now binds exact typed condition
  predicates in the joint and every marginal role, with actual I05 execution,
  same-rule-id mutation/refusal/restoration and cold proof. A2 canonical
  operation-ID revalidation is enforced. A3 unsupported-only/PENDING no longer
  masquerades as a valid empty frontier, and all partitions conserve identities.
- Remaining defects: **none blocking A1-A3**.
- Preserved limitation: A4 independent recurrence/baseline enumeration is
  explicitly not delivered and not claimed as D13 PASS.

### (ii) Full R01 contract qualification

- `ACCEPT_SCOPED_LOCAL` for the R03-facing prospective frontier/lowering
  interface with A1-A3 repaired and A4 honestly bounded.
- **Not full R01 whole-node qualification**: independent recurrence/baseline
  functionality remains unimplemented pending a competent generic contract.
  This limitation must travel with any R03 or downstream claim.

### (iii) R03 actual start prerequisite

- Contract basis: `INPUTS/USER_GRANT.json`
  `r03_start_condition = "Independently qualified R01 and accepted R02; no R03
  execution before condition satisfied"`; `00_FLIGHT.md` same condition.
- R02 is independently accepted in the inherited record:
  `WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/revisions/r2/00_RETURN.md`
  at reviewer commit `da9a8c4e0ce66baf5a55a6b44a9c0e0139a47cec` (remote readback
  `e1f0aeb65...`), disposition
  `ACCEPT_SCOPED_LOCAL__R02V_R2_AFFECTED_REQUALIFICATION_PASS`, candidate
  `6f4be33854c0437a52e1c49b977104db111ac327`.
- R01 is now independently qualified at the scoped generic lowering grain.
  Therefore the R03 start prerequisite is met **for supported/non-recurrence
  operations**. It is **not** met for total recursive/minority R03 coverage
  until the A4 generic contract gap is resolved by a competent issuer/HQ
  decision. This reviewer supplies evidence only; no HQ wake authority.

## NOT_REACHED / unchanged holds

R03 total issuance/U43/Batch and recursive/minority execution; R04
authenticated byte custody, serialized restore/resume and revocation; R05 five
proof grades/canonical N10E values-read; R06 F5/F6/F7/F8 and observed temporal
pairs; original 35/1,890 and original `U/E_pre`; N11/N12; production/protected
CI; J52/W52; Browser runtime; source/science/adoption. All original35/1890/
globalF6F7F8/Z UNRESOLVED16 holds remain unchanged.

## Evidence index

- `EXPECTATIONS.md` — reviewer oracle committed before candidate inspection.
- `defects.md` — A1-A4 exact disposition and preserved limitation.
- `probes/test_r01v_r3_reviewer.py` — own A1-A4 hostile probes.
- `probes/prior_test_r01v_independent.py` — retained focused controls with one
  meaningful R3 canonical-ID adaptation.
- `replay/author_suite_junit.xml`, `.log` — author suite replay.
- `replay/adapted_prior_probes_junit.xml`, `.log` — retained controls.
- `replay/own_probes_junit.xml`, `.log` — own probes.
- `evidence/conditional_joint_repro.txt` — A1 baseline/mutation/restoration.
- `evidence/recursion_diagnostic.txt` — A4 exact gap/identity diagnostic.
- `evidence/startup_and_identity.txt`, `.json` — startup/remote/blobs/hashes.
- `evidence/junit_summary.txt` — reviewer JUnit counts.
- `independent_oracle_results.json` — independent outcome summary.
- `proof_witness.json` — commands, exits, mutations, limits.
- `SHA256manifest.json` — all artifacts except itself, explicit self-exclusion.
- `RESUME.md` — exact reproduction commands.
