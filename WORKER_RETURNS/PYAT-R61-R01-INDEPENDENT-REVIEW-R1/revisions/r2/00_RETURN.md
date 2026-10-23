# R61-R01V R2 independent review return — REVISE

**Verdict: `REVISE`.** Finite, evidence-backed. Not `ACCEPT_SCOPED_LOCAL`.
R03 remains **NOT_STARTED**. No candidate code/test was edited; no source,
science, adoption, production, N11/N12 or J52/W52 claim.

## Exact review target and separation

- Candidate/startup: `f0c602eddaee14a58d6f0935a587a46fcf96c6db`
  (matches `.r61/launch.json` `startup`).
- Code commit: `d56e53301aaa0203e83fc1b60a0bcafb86b17892`; parent/startup
  `fcf9fe9f8662c9e98801e670d0d4357072d8d453`; base
  `a54893657ba65e44c1049f763208b0b4b6ed5eb9`.
- Author branch remote head: `f0c602ed...` (direct `git ls-remote`).
- Reviewer branch/worktree:
  `agent/opencode-pyat-r61-r01v-r2-independent-review-r1` at
  `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r2`.
- Author session `ses_e98c905cbffekusoHURfKyEUKG` is distinct from this
  reviewer session. Same provider account (`opencode-go/deepseek-v4.1-flash`,
  variant max, existing Global) is disclosed; this is not organizational
  scientific independence. Browser whole-native runtime remains unqualified.
- Changed paths from startup are exactly the four R01 allowlist code paths plus
  the author's R2 report root. Immutable v1 reports, prior reviewer tree and R61
  INPUTS are unchanged (empty git diff). Six R2 report hashes verified;
  manifest explicitly excludes itself. Own `EXPECTATIONS.md` was committed first
  (`515c1d704`).

## What was independently reached

1. **Author suite replay** with reviewer JUnit and actual imports: exit 0,
   `18 passed`, 0 failures/errors/skips (`replay/author_suite.log`).
2. **Retained + adapted prior reviewer probes**: 20 passed, exit 0 after
   explicitly adapting only obsolete R2 behavior (topology capability at
   lowering, forged-direction refusal, MULTI_SELECT_SET eligibility) and the
   path-derived cold helper (`replay/adapted_prior_probes.log`).
3. **Own native proof**: actual imported
   `rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery` with
   synthetic C11/I03 objects; reviewer-owned expected candidate set compiled
   from the current native owner/catalog (not from returned receipts).
   Baseline positive passes; a condition-atom mutation that preserves
   `rule_id` fails both the reviewer join and the candidate
   `native_receipt_anti_join`; restoration passes; a cold subprocess reproduces
   the same case (`replay/native_positive.log`).
4. **Exact frontier identities**: independent ordered target/condition sets,
   typed bool/int/string/null/absent, duplicate refusal, admin false/unknown,
   structured holds, budget pending IDs, partition/cold recomputation and
   count-preserving substitution refusal (adapted prior probes + own probes).

## Primary blocking defect (R03)

**A1 — conditional `JOINT`/`CO_TRAVEL` is lowered `SUPPORTED` while its exact
condition value is silently dropped from native execution.**
The candidate's own policy makes four `(JOINT|CO_TRAVEL) x (q_gamma=0|1)`
operations eligible on ordered targets `(q_alpha,q_beta)`. Lowering returns
`SUPPORTED` / `JOINT_DEPENDENCE` with `expected_candidate_count=1`, but the
condition atom is present only in `record.atoms`; the rule has no condition
reference and every expected query role uses the all-response baseline
predicate. The two condition values therefore execute the same joint/marginal
queries; only the operation-hash-derived `rule_id` differs. Required behavior is
exact condition/typed-value binding in the executed candidate (CONTRACTS
Revision 2; R01V R2 commission items 4–5), or a typed refusal. This is an R01
lowering defect, not an R03 Batch/R04 custody gap, so **R03 cannot start on this
candidate**. Exact repro/evidence: `evidence/conditional_joint_repro.txt`,
`probes/test_r01v_r2_reviewer.py::test_conditional_joint_condition_has_native_semantic_role`.

Exact finite repair options (R01 scope, choose one):
1. Typed-refuse conditioned `JOINT`/`CO_TRAVEL` until the current owner/catalog
   exposes exact conditioned joint/marginal refs and objects; keep the
   scientific operation eligible but runtime-unsupported with a typed reason.
2. Extend `NativeCatalog` with conditioned joint/marginal refs keyed by the
   ordered condition tuple and use them.
3. Compose a derived exact predicate from current I05 predicate primitives,
   bind it as the joint baseline and marginal condition, and add its exact
   ref/object to the grammar.

Secondary defects (fix in same repair, not the sole verdict driver):
- **A2** lowering accepts a forged `op_id` not equal to the canonical operation
  hash (`SUPPORTED`); revalidate operation identity at lowering.
- **A3** an unsupported-only scientific frontier advertises
  `allow_empty_frontier=True`; reserve `VALID_EMPTY` for a truly empty complete
  frontier.
- **A4** `FORK` recursion/baseline is still `conditioner_depth-1` under new
  field names; `D` is not independently exercised and `baseline_policy_ref` is
  not an operation field. Either enumerate a separate recurrence/baseline chain
  or state the FORK-over-K declaration as an explicit limitation (do not claim
  D13 PASS).

## Actual capability delta vs the prior R1 review

Genuinely improved: typed bool/int/string/null/absent identities and typed
native cells, source/wave/edition/digest and measure/estimand/weight/design/
variance/clock/currentness identity, separate eligibility/execution/result
axes, budget PENDING conservation, full `LoweringRecord` fields, exact
candidate/query-role receipt anti-join for `DIST`/`CONDITIONAL` (including a
same-rule-id condition mutation), typed non-injective codec refusal,
direction/policy/role/risk/unit/form/topology/scope/admin revalidation,
catalog-first topology lookup, structured holds, explicit risk-set policy, and
deterministic cold recomputation. Not yet delivered: semantic binding for
conditioned joint/co-travel operations (A1), canonical operation-ID
revalidation (A2), unsupported-vs-empty separation (A3), independent
recursion/baseline identity (A4).

## Actual native consumer and NOT_REACHED edges

- **Reached:** current I05 `execute_exact_bounded_discovery` with synthetic
  C11/I03, actual `DiscoveryResultReceipt` candidate identities and
  query-role/predicate/query refs; condition mutation/refusal/restoration and
  cold subprocess recompilation; G50-style frontier, lowering plan, typed
  codec and conservation anti-joins.
- **NOT_REACHED:** R03 total issuance/U43 `IssuedWorkloadRecord`/Batch proof or
  duplicate-discovery proof; R04 authenticated byte custody, serialized
  restore/resume and revocation; R02 row/occasion projection; R05 five proof
  grades/canonical N10E values-read; R06 F5/F6/F7/F8 and observed temporal
  pairs; original 35/1,890 obligations and original `U/E_pre`; N11/N12;
  production/protected CI; J52/W52; Browser runtime.
- Seven selected author mappings do not define the independent oracle and do
  not establish full native R03 execution. The reviewer native case is also
  mapping/boundary evidence only.
- R01 grain: deterministic cold *recompilation* is proved; serialized cold
  *restore* is correctly left to R04 and is not a verdict driver. R03 is
  blocked by A1 at R01's lowering boundary, not by the absence of R03/R04
  machinery.

## Evidence index

- `EXPECTATIONS.md` — frozen oracle, committed before R2 code inspection.
- `defects.md` — A1–A4 exact inputs/observed/required/ranks; D1–D16 disposition.
- `probes/test_r01v_r2_reviewer.py` — own hostile probes.
- `probes/prior_test_r01v_independent.py` — retained/adapted prior probe history.
- `replay/author_suite_junit.xml`, `replay/author_suite.log` — reviewer replay.
- `replay/adapted_prior_probes_junit.xml`, `.log` — retained prior probes.
- `replay/own_probes_junit.xml`, `.log` — own probes (2 pass, 3 required
  defect-assertion failures).
- `replay/native_positive_junit.xml`, `.log` — native mutation/restoration and
  cold positive (2 passed).
- `evidence/conditional_joint_repro.txt` — A1 exact output.
- `evidence/recursion_diagnostic.txt` — A4 exact output.
- `evidence/startup_and_identity.txt` — startup/remote/allowlist/manifest/
  imports/versions.
- `proof_witness.json` — commands, exits, counts, imports, mutants, limits.
- `SHA256manifest.json` — hashes of all artifacts except itself.
- `RESUME.md` — exact reproduction commands.

## Boundary and disposition

This is reviewer qualification only. It does not repair, adopt, issue source
permission, original `U/E_pre`, empirical support, science, N11/N12,
production/CI, F6/F7/F8, or restart J52/W52. A fresh candidate repair must be
independently reviewed again; the author must not treat this return as
self-adoption. R03 remains **NOT_STARTED** until R01 is requalified and R02 is
accepted.
