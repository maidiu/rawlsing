# PYAT HQ263 R01 — G01 owner-only selected ingress independent hostile review — R1

**STATUS:** ISSUED_NEEDS_HUMAN_LAUNCH — no self-adoption
**REPOSITORY:** `maidiu/rawlsing`
**BRANCH:** `agent/reviewer-pyat-hq263-g01-owner-ingress-hostile-r1`
**FROZEN CONTROL:** `64b4e7ab1e67c139c7115430c711d459474cf31a` (HQ262 sealed, read live control first)
**CANDIDATE:** `agent/space-bunny-pyat-hq262-g1-owner-only-selected-entrypoint-r1 @ 22cd4976e3f9f860c7fe1bd889d3cc5faa44f8f3`
**ISSUED G01 TIP:** `63cdc0b5bb4c382acf558e040b3669b787fc245f`
**G01 COMPARE:** exactly 1 ahead / 0 behind, two NEW code/test files plus four commissioned return artifacts
**REVIEW ROLE:** independently evaluate the frozen candidate using an existing qualified independent review workflow and its actual configured model/runtime; do not invent a machine or model. If clean runtime is unavailable, issue an exact UNTESTED hold.

## Mission

Give an independently reproducible PASS/FAIL/HOLD decision on the *actual* G01 ingress, not on the fact that its author's 22 tests passed. G01 is a **candidate**, no production integration or EE14 permission has occurred. Read sealed `HQ_HANDOFF/LATEST.json`, pinned HQ262 checkpoint, `PYAT_CONTROL_ROOM/HQ262_G1_DATA_ONLY_ENTRYPOINT_AND_GHANA_METADATA_INSPECTION_LIMITS_R1.md`, the original G01 commission, G01 return reports and the two NEW code/test files pinned at candidate SHA. Verify SHA lineage and exact files before anything else.

G01 source blob:
`rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py @ e1c09957519f10b29ae2635f3277b4f3af0912c9`
G01 test blob:
`rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py @ f71c0ce87d4005acc6806cac9afe5bbbb76ad9bc`.

The original commission required owner-executed **C1→actual authenticated service applicability / adopted G2 permission-coherent binder→F8**, exact source-free same-four-respondent XOR q1 `q(C|A=1)` = (1/2,1/2) denominator 2 and q2 `q(C|A=1,B=0)` = (0/1) denominator 1, full unmodified C1 evidence/provenance, closed external DATA-ONLY client ingress, and adversarial tests. It did not authorize real EE14 G0b, deployment, source access, CURRENT selected service or a self-issued trust root.

## Mandatory hostile discriminators

1. **Actual G2, or a renamed hash?** In the new module, `scope_hash = semantic_hash({"contract":..., "scope": self._applicability_scope, ...})` immediately precedes a direct call to `evaluate_positioned_subject_possibility(...)`. The new module appears not to import/call either `pre553_service_source_applicability` or `pre553_service_f8_source_scope_binding`. Determine whether an authentic `CandidateClassApplicabilityReceipt` and G2 binding with exact permission-ref coherence and independent authoritative inputs are actually created, checked, and consumed; distinguish owner-held `TEST_ONLY_UNISSUED` dictionary material from one. Verify negative source/release/permission mismatches. **Do not pass** an invented stand-in.
2. **Genuine progressive conditioning?** In `_ingress()` the q1 and q2 cell dictionaries visibly specify the *same* producer `empirical_query`, `predicate`, `consumer_query`, and model rule; both use the same `_stratum()` helper. Prove whether any actual distinct same-respondent conditional result or required joint denominators are exercised. Compare `f8_result_hash` and full C1 producer identity for q1 vs q2; a different receipt due only to `cell` is not two distinct empirical conditionings. Do not rebrand the C1 AT07 fixture as the XOR demanded by the commission.
3. **Origin integrity and service threat.** Check that original C1 evidence objects, refs, denominator, risk set, C1 preimage are legitimately produced and bound, but do not treat an owner-computed semantic hash alone as authenticated origin. Assess trusted constructor/harness injection, mutable nested owner objects, `isinstance` vs exact plain type / subclass requests, and alternate low-level F8 route. Assess only the approved external DATA-ONLY caller boundary; same-process monkeypatch and deployed isolation must remain explicitly unproved.
4. **Hostile/typed negative coverage and test validity.** Demand effective altered in-flight provenance/authority mutation test (rather than an untested statement), exact release/source/permission mismatch, typed `VALID_EMPTY`, `NONCOMPARABLE`, `UNDERPOWERED`, `UNKNOWN_OR_UNRESOLVED` (or explicitly unsupported producer cases), cross-source/walkback refusal, no-invocation rules. Read the author's report identifying noncoverage; do not silently upgrade it.
5. **Clean committed execution.** Author's `22 passed` report names working HEAD `63cdc0...`, not final commit `22cd...`. Run test and any safe adversarial probes in an independent clean checkout pinned to candidate SHA on the qualified interpreter, record commands, exit codes and observed assertions. If unable, judge static defects honestly without saying independently green. Do not run raw survey.

## Decision rubric

`PASS_AT_DECLARED_G1_DEVELOPMENT_GRAIN` only if the commissioned technical flow actually exists and the required source-free q1/q2 are distinct/verified, owner-held permission material is not silently upgraded to G0b, and a defensible adversarial and negative court passes on committed SHA. If any necessary contract component is absent, `FAIL_REQUIRED_CORRECTION` with exact minimal code/test edit terrain and reproducible counterexample. If the accepted owners cannot lawfully realize a technical flow without a new model-use permission or owner edit, `HOLD_EXACT_AUTHORITY_OR_OWNER_BLOCKER`. No reviewer may create their own real grant or deem T1 complete.

## Write terrain

**NO changes to production code, candidate code, existing tests, frozen semantic PRE-MAIN, HQ control or source files.** Only these review artifacts under `WORKER_RETURNS/PYAT-HQ263-R01-G01-OWNER-INGRESS-INDEPENDENT-HOSTILE-REVIEW-R1/`:

- `00_BASE_CANDIDATE_AND_ACTUAL_CALL_GRAPH.md`
- `01_INDEPENDENT_CLEAN_COMMITTED_EXECUTION.json`
- `02_HOSTILE_COUNTEREXAMPLES_AND_REQUIRED_CORRECTIONS.md`
- `03_DISPOSITION.json`

Bank observed runtime and evidence, exact candidate SHA/blobs, unambiguous PASS/FAIL/HOLD, minimal correction requirements and authority ceiling. Commit/push only your review branch; verify its remote head. Do not self-adopt, issue successors, deploy or grant EE14/EE12/FF02. **STOP:** `HQ263_R01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`.
