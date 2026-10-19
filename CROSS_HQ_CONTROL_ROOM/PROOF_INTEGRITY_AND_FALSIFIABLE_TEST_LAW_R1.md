# RAWLSING — shared proof-integrity and falsifiable-test law R1

**Status:** USER-DIRECTED MANDATORY PRE-MAIN / PYAT / SOROK AUTHORING AND HQ-INTAKE DISCIPLINE, 2026-10-18.
**Scope:** all new or substantively revised code tests, worker returns, scientific/integration claims, and HQ adoption decisions on any provider/model. **Effective prospectively.** Existing historical code and verdicts remain historical evidence, not retrospectively invalidated by this law alone.
**Not:** a new reviewer round, universal stop-work, raw-source right, semantic/model/actor issuance, production promotion, HQ succession, Sorok authority transfer or an excuse to duplicate tests.

## Why

E04JR exposed two **different** failure modes: (a) vacuous assertions (such as `assert x or True`, optional-field `else True` and no-op verification loops) that produce green suites without checking anything; and (b) real, falsifiable assertions that compare two outputs without proving the claimed dependency between the downstream consumer and the supposed upstream release. An author's mutation breaking a different, unrelated field does not vindicate the intended claim.

## Single-pass rule: one implementation, one discriminating proof

1. **Write the required claim and counterfactual before relying on a green suite.** For every material integration/scientific acceptance claim identify: (i) the *actual owner path and terminal consumer*, (ii) the *specific edge* the claim says exists, (iii) the *observable positive*, (iv) a defect that would make the claim false, and (v) the expected RED when that exact edge is disabled or corrupted. Freeze the expected response before the candidate implementation's output is used as its oracle. Commission owners should specify this at launch; if not, the worker must freeze it before development, not invent it after seeing green output.
2. **No inert tests.** No unconditional truth, `or True`, `if ... else True` for asserted requirements, no-op `for ...: pass` verification, self-comparison, swallowed failure, no-skip-without-scoped-disposition, optional-field fallback that hides absent required contracts, or hash-length/prefix-only assertions misrepresented as pinned preimage equality. A genuinely optional field may be tested conditionally only when the claim itself explicitly treats absence as valid, with a separate positive existence witness where required. Green counts and JUnit XML never substitute for semantic coverage.
3. **Direct dependency severance for integrations.** Execute the **real downstream consumer** with the alleged upstream component or release deliberately severed, substituted, revoked, misbound or changed while irrelevant inputs are held fixed. If the consumer still passes as if correctly connected, the integration claim is NOT PROVED. A different source causing parallel producer/consumer changes is not evidence of learned-release → consumer dependence. Preserve negative controls as executable tests or a reproducible bounded mutation witness.
4. **Mutation efficacy is claim-specific.** The control must fail the named test **by its relevant assertion**, not merely trigger an import error, unrelated exception, test runner error, changed fixture checksum or arbitrary other test failure. Check the baseline and mutated test in fresh processes where state/replay matters. If an injected mutation fails elsewhere while the critical test stays green, that mutation **did not kill the claim**.
5. **Adversarial independence without extra rounds.** The implementing worker runs its own positive and fault-injection in the **same normal pass**. Existing I2/scientific acceptance responsibilities continue; no new compulsory stand-alone reviewer, ritual commission, or repeated test campaign is imposed. The independent reviewer, when already required, challenges the commissioned observable and selected fault, not just replays the author's green suite. Review cannot upgrade author-defined coincident outputs to causal integration.
6. **Claim-grade truth.** Separately record `EXECUTED_GREEN`, `ASSERTION_EFFICACY_PROVED`, `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED`, `NOT_PROVED`, and `NOT_RUN`. An author may report an executed green suite while the actual claimed integration remains `NOT_PROVED`. Do not aggregate unrelated test events to inflate proof strength. Declare inherited/unrelated REDs separately.
7. **Cost and scope.** Apply to newly written/revised tests and newly promoted material claims. Do not mechanically reopen every frozen historical test or serialize unrelated branches. A lightweight linter runs on changed tests; an executable focused negative-control witness runs inside the worker's existing qualified Python/CI surface. Existing source/semantic/actor permissions remain unchanged.

## Executable enforcement and honest limits

- The shared checker is `CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py`. Its AST gate rejects mechanically recognizable inert checks in **changed** Python tests; the existing governed-court pull-request workflow runs this gate automatically.
- For any **new or revised integration-claim test** (join, lifecycle, consumer, integration, weld or end-to-end), publish a sibling `<test_filename>.proof.json` with a named test node and at least one exact source-code fault injection. The same checker can run the positive test, introduce the fault, require an assertion-level RED on that named test, and restore the source. Such a witness must execute in a qualified environment; `NOT_RUN` is not a PASS.
- These automated gates are **necessary but not sufficient**: a selected mutation may be irrelevant or the tested consumer may be a stand-in. The claim/edge/consumer must be accurately identified in the frozen commission and HQ's ordinary scientific judgment. No claim that arbitrary test quality is mathematically guaranteed.
- Historical tests are linted only when touched; this law neither deems the pre-existing codebase sound nor revokes earlier accepted scope wholesale. Evidence that a particular existing accepted claim relied on inert assertions or a missing edge **is** grounds for targeted regrading at its exact proof grain, not a universal stop-work.


### Minimal executable per-test proof contract

Place `test_<name>.py.proof.json` **beside the changed Python integration test**. Use actual repository-relative paths and exact unique source text. The fault MUST affect the alleged producer/release/consumer edge, not a decorative flag.

```json
{
  "schema": "RAWLSING_PROOF_INTEGRITY_R1",
  "claims": [{
    "claim_id": "EXACT_COMMISSIONED_EDGE",
    "actual_consumer": "the real consumer API and product",
    "claimed_dependency": "selected release -> dereference -> consumer values-read",
    "positive_node": "WORKER_RETURNS/.../tests/test_actual_join.py::test_release_drives_consumer",
    "fault": {
      "path": "WORKER_RETURNS/.../actual_bridge.py",
      "old": "exact unique source text for the real binding",
      "new": "source text that severs the real binding"
    }
  }]
}
```

Execute the witness as part of normal testing: `python CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness path/to/test_actual_join.py.proof.json --root . --receipt evidence/proof_witness.json`. The runner asserts the positive named test passes and the same named test fails **via its assertion** under the injected fault, restoring the original source afterward. It refuses absent/non-unique mutation text, an attempted mutation of the test itself, an unowned contract, missing tests, skips and error-only mutants. CI invokes the same checker for new/changed integration tests; the report still needs competent scrutiny that the mutation genuinely represents the commissioned edge. The worker's qualifying environment must contain the native imports and pytest. Run from a qualified clean or dedicated worktree; protect unpushed work as under 00D.

## Mandatory commissioning / worker return fields

For a material implementation or consumer claim: `claim_id`, `actual_target_consumer`, `claimed_dependency`, `frozen_positive_oracle`, `fault_injection_target_and_expected_RED`, `positive_test_node`, `actual_negative_control_result`, `proof_grade`, `exact_source_and_test_refs`, and any `NOT_RUN/NOT_PROVED` residual. Preserve normal provider/model/effort, warm host, source authority, JUnit, cost, Git SHA and independent-review controls.

**Binding rule:** no positive scientific integration or functional-completion adoption where the claimed edge has not been actually exercised and shown to fail when severed. No extra reviewer round is required to enforce this law. 
