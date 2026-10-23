# R61-R08V independent evidence/consumer qualification — return

Verdict: **REVISE (bounded, local defects).** The candidate implements a real callable evidence-binding grain and the positive actual-provider/cold/actual-evaluator path is witnessed. It does not meet the hostile K-to-actual-producer and cache-ingress requirements: wrong request K can be rebound to the same actual P1 producer and served as exact support (D1), and a self-sealed cross-source cache forgery is accepted and can serve forged values (D2). A medium status-summary conflation remains (D3). The author's separate bounded REVISE for historical J42/P41 caller wiring is accurate and is classified as an integration-permission/owner-interface gap, not a local module defect.

## Exact candidate custody

- Startup/exact candidate: `ad9c3088096ce291d61dfdd292141073b515fbca`.
- Code commit: `f93cf87948ce092a9b8623b60c00722ae048bda2`.
- Branch: `agent/opencode-pyat-r61-r08v-independent-review-r1`; worktree `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v`.
- Candidate module: `rawlsing_next/pre553_universal_evidence_binding.py`, blob `464a2190a811816c52e9d9c244ab126dc950c564`.
- Candidate test: `rawlsing_next/tests/test_universal_evidence_binding.py`, blob `2512c29e7fa1b780e24a82d111e7c336fae506de`.
- Author manifest hashes independently recomputed OK: `00_RETURN.md` `1b21bb58...`, `RESUME.md` `1a4cc459...`, `junit.xml` `38879345...`, `proof_witness.json` `af0fed74...`.
- Candidate files were not modified. Reviewer writes are confined to `WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/`.

## Frozen expectations and reads

`EXPECTATIONS.md` was committed first (`38ace1678`) before candidate code/return inspection. The commission, original R08 commission/NODE, and `INPUTS/CONTRACTS.md`, `INPUTS/TESTS.md`, `INPUTS/OVERLAYS.md` were read at `9f878641...` before author conclusions. The reviewer also read the exact inherited J42/P41/E04 recovery refs listed below. No original survey/data/credential/external-home read occurred.

## Independent test results

Environment: `/usr/local/bin/python3` Python 3.11.3, pytest 9.0.2. `pyreadstat` 1.3.2 was not used. No skips.

| Evidence | Result |
|---|---|
| Author test replay (`test_universal_evidence_binding` + `test_pre553_analytical_composition`) | 21 passed, 0 failed/error/skipped, 6.314 s (`junit/author_replay.xml`) |
| Reviewer baseline positive/cold/severance/status controls | 7 passed, 0 failed, 2.775 s (`junit/reviewer_baseline.xml`) |
| Reviewer hostile K/cache probes | 8 tests: 7 failed as expected defects, 1 passed (observed-zero control), 3.047 s (`junit/reviewer_hostile.xml`) |
| Reviewer actual archived E04 fixed-semantics probe | 1 passed, 0.054 s (`junit/reviewer_e04.xml`) |
| Reviewer reach/static association probe | 3 passed, 0.121 s (`junit/reviewer_reach.xml`) |

The baseline independently computed the AT07 forward law from `at07_rows()` (60 P1 respondents: 54 yes, 6 no), witnessed a real call to the unchanged `evaluate_positioned_subject_possibility` with a delegating spy, reproduced the returned object material, replayed the cache in a fresh process (denominator 60, same consumer hash), and showed upstream evidence severance refuses the same consumer assertion. It also preserved an actual observed-zero target cell (denominator 60, `no=0`, `yes=60`) and refused actual `ZERO_SUPPORT` from the consumer/summary.

## Defects

Ranked details, expected/observed, exact lines and minimal correction directions are in `defects.md`.

1. **D1 (critical): wrong K rebind authenticates the same actual producer.** Requests naming `POSITION=P2`, BOOLEAN `true`, NULL, INTEGER 1, an extra/reordered condition tuple, or changed edition/digest/as-of/direction/role/design/weight/source were bound to the unchanged forward P1 producer and resolved `SUPPORTED` denominator 60. The values-read carried the wrong request labels and the consumer reader accepted them. `EmpiricalProducerBinding.__post_init__` and resolution do not tie most K fields (especially ordered conditions/typed values and authority/clock/edition labels) to actual owner determinants.
2. **D2 (critical): self-sealed cache forgery accepted; forged values served.** A resealed cache entry using the victim request key but the changed-source (`CHANGED_SOURCE_LAW`, different universe/release) evidence/query/rule was imported successfully. `resolve(victim)` returned `SUPPORTED` denominator 999; `EvidenceConsumerReader.read()` returned denominator 999. The cache carries no full K preimage and does not bind evidence/query/rule/source/target/conditions/clocks/permission to K. `AUTHENTICATED_CACHE` is only a SHA-256 self-seal; the author's limits acknowledge this, but the public ingress still accepts the forgery.
3. **D3 (medium): valid null/diffuse/empty products collapse to `support_state == "NO_SUPPORT"`.** A single `VALID_NULL`, `DIFFUSE`, `VALID_EMPTY`, or `OBSERVED_ZERO` result yields `support_state "NO_SUPPORT"` while `productive_all_required` is true and `result_counts` retains the valid state. This conflates valid products with no support in the top-level summary.

## Author REVISE and full reach

The author's bounded REVISE is verified as a real missing integration, not a completed end-to-end claim:

- Historical J42 `E41ProviderAdapter.step` (blob `40f1e9f69fafff37f6bc44474b0189543d4997b3`, lines 215-219) appends a trace named `evaluate_positioned_subject_possibility` with `same_evidence_object=True`; the body contains no actual evaluator call.
- Historical P41 `progressive` (blob `7d428106c79bcc56973f7c0044fc273a2b354554`, lines 132-148) consumes trace entries by index and falls back to `source="CACHED_PRODUCTION_CONSUMPTION"` with `same_evidence_object=True`.
- Actual archived E04 `product/nonparent.py::consume` (blob `2181b832d3c4376d4b9428e13f4354f273be8f32`, lines 19-24) returns top-level `OPTIONS_AND_SOURCE_SUPPORT_PRODUCED` when the empirical state is `PRODUCTIVE_TEST_ONLY`, even if a step is `ZERO_SUPPORT` denominator 0. The reviewer reproduced that exact unchanged function behavior; the candidate's E04-compatible step does not repair the terminal.
- At the candidate tree, `git grep pre553_universal_evidence_binding -- '*.py'` finds only the module and its own test. There is no live non-test caller. The historical J42/P41 bodies are archived recovery targets outside the R08 allowlist, not live adopted production; editing them would be false adoption.

Covered: exact callable K-to-producer/cache grain, actual canonical provider values-read, unchanged evaluator call, cold-process cache baseline, observed-zero/zero-support controls. NOT_REACHED: live J42/P41 progressive adoption and a repaired E04 terminal. The remaining full-progressive issue is **integration permission/owner interface**, not a local module defect. The smallest amendment is a separately granted live-owner integration at the exact adapter/service/terminal boundaries described in `outcomes/reach.json`; no archived return should be edited and no new broad court is requested. There is no new architecture/science necessity card.

## Commands and exact evidence

```text
/usr/local/bin/python3 -m pytest -q rawlsing_next/tests/test_universal_evidence_binding.py rawlsing_next/tests/test_pre553_analytical_composition.py --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/junit/author_replay.xml
exit 0; 21 passed

/usr/local/bin/python3 -m pytest -q WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/probes/test_r08v_baseline.py --junitxml=.../junit/reviewer_baseline.xml
exit 0; 7 passed

/usr/local/bin/python3 -m pytest -q WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/probes/test_r08v_hostile.py --junitxml=.../junit/reviewer_hostile.xml
exit 1; 7 failed (D1/D2), 1 passed (observed-zero)

/usr/local/bin/python3 -m pytest -q WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/probes/test_r08v_e04_fixed_semantics.py --junitxml=.../junit/reviewer_e04.xml
exit 0; 1 passed

/usr/local/bin/python3 -m pytest -q WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/probes/test_r08v_reach.py --junitxml=.../junit/reviewer_reach.xml
exit 0; 3 passed
```

`proof_witness.json` records exact commands, exits, candidate/tree/blob refs, session separation, assertion-level observations and the forged-cache/wrong-K witnesses. `outcomes/hostile_observations.json` records the concrete K rebind and forged-cache values. `outcomes/reach.json` records exact covered/NOT_REACHED classification and the owner/scope amendment. `SHA256manifest.json` hashes every review artifact except itself.

## Process and limits

Reviewer model/account: `opencode-go/deepseek-v4.1-flash`, variant max, existing user-selected account. Reviewer harness process: `OPENCODE_PID=52345`, harness session id `01a15c1e-5446-7ef3-80bb-9ff5c2cb27da`; distinct worktree/branch from author session `ses_e98c8dfe6ffewNYOqJpvqK21a6`, which was not used. Same provider account is not institutional scientific independence. All evidence is TEST_ONLY source-free; no original data, source/science/CI/production/N11/N12/Sorok authority or model/provider change. No author repair or self-adoption. Branch-only non-force push and direct SHA verification are performed after this return is committed.
