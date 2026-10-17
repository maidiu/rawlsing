# SOROK VOZHD-2 HQ324 P1 — bounded implementation return

**VERDICT:** `IMPLEMENTED_SOURCEFREE_AUTHOR_TESTS_PASS__NOT_SEMANTICALLY_ADOPTED__INDEPENDENT_I2_REQUIRED`.

## Custody / independent boundary

- Exact sealed startup and remote launch HEAD: `44f17132110274b07701bd4fea5bb1cbd10a5287`.
- Target branch: `agent/rabochii-sorok-v2-hq324-p1-llm-alternative-admission-r1`.
- Write terrain: **only** `WORKER_RETURNS/SOROK-V2-HQ324-P1-PROPOSAL-ADMISSION-R1/`.
- Role: one source-free bounded contract author, neither HQ nor semantic issuer nor independent I2 reviewer.
- Governing reads: sealed full commission; Sorok 00D at seal and 00C from earlier available verified repo revision (00C is absent from the shallow HQ324 branch tree); source-graded B-first `03`, bike theft `02`, architecture `00/01`, TD-R05 §22, ADP019 §§7–9, ADP020 §§5–12/15–16, ADP010 encounter/exposure authority.

## Implementation

Self-contained standard-library Python `p1_contract.py`, `run_demo.py`, `make_fixtures.py`; 13 frozen source-free context/proposal/policy JSON fixtures; pytest adversarial court; B1 compatibility and authority-separated interface guide. The fabricated source-free context establishes the exact bike theft **without a known culprit**; caregiver and peer alternatives are attributed unverified utterances with separate independent actor histories. Candidate decisions use exact context hashes, closed family and action-opportunity refs, permission/readset/temporal/visibility checks, future-person owner deferral, optional external immutable proposal-ID collision registry, typed refusals, unchanged history, no first-item rescue and lawful nonoccurrence. Model output is proposal-only and cannot supply state deltas, admission, actual culprit, numeric authority, or cross-actor mutations.

An authored external policy makes reproducible seed/coordinate-dependent **TEST_ONLY** stochastic choices with rational integer weight units and complete explicit provenance. This selection is **not native ADP020** and its design weights are emphatically `PROVISIONAL_NOT_CALIBRATED`. The receipt contains no CAN008-positive actor response or CAN011 durable updates; P1 `ADMIT` is merely eligibility, not actual ADP019 event issuance. There is no permitted route from this package to real person/world/history mutation.

## Actual tests

- Runtime: Python `3.13.5`, pytest `9.0.2`, POSIX filesystem and subprocess VERIFIED.
- `python -m compileall -q p1_contract.py run_demo.py make_fixtures.py tests/test_p1_contract.py` → `PASS`.
- `python -m pytest -q tests/test_p1_contract.py --junitxml=evidence/p1_junit.xml` → **66 PASS, 0 FAIL, 0 SKIP**; JUnit and stdout saved.
- `python run_demo.py --coordinate 11` → `PASS`; exact noncausal demonstration captured.
- Intermediate test precedence RED `52 PASS / 1 FAIL` (expected knowledge-refusal changed to earlier visibility-refusal) resolved; historic first suite `53 PASS`. All statuses recorded in `evidence/test_history.md` and log files.
- **NOT_RUN:** real LLM API; original survey-source operations; native B1/CAN008/CAN011/ADP019/020; independent I2 review; any actor-lifetime integration, delivery, perception or production effect.

## Authority limitations / HQ handoff

1. P1 canonical JSON is NOT RFC8785_JCS_ADP019_V1, and its P1 candidate set is NOT ADP020_CANDIDATE_SET_V1. Real coupling requires owner-issued exact schemas/canonicalization and registered ADP020 stream and rule/weight authority; no implicit promotion of the mock.
2. `ADMIT` naming is local P1 candidate eligibility, while ADP019 `ADMIT` creates an objective event. This exact discrepancy needs explicit adaptation, not a silent cast.
3. `BFirstScenarioRequest`, `BFirstCandidateDecision`, `BFirstAtomicReceipt` are shared provisional research handshake types, not adopted. This worker deliberately emits no atomic receipt or durable transition. New-person proposals are deferred to independent person/history authority.
4. The authored design policy is content-hashed for replay integrity, not cryptographically attested against an external adversary or empirically calibrated. Open-text model hypotheses are not independently semantically truthful; exact registered owner rules must arbitrate if promoted.
5. Source-free success neither proves a historically generated human mind nor resolves B1's still-open concrete positive CAN008 rule and CAN011 target-owner decision.

**Next owner:** HQ to obtain independent High I2 review and B1 adapter/owner adjudication. **Self-adoption denied**. No autonomous host/model/harness switch and no private source disclosure or paid LLM calls.

Remote commit SHA and direct remote proof supplied in the user-visible final return after the pushed ref is checked; a commit cannot honestly embed its own SHA in its own preimage.


## Post-return completion extension (17 October 2026, same assigned branch)

An independent-in-time **author-side** audit reexecuted the original frozen 66 tests, then added eight hostile completion controls without altering the original test file or the 13 frozen JSON fixtures. Five controls were reproducible RED against the preceding branch revision (`a9c4398346dee7eefa47fa2fa944d5330deac5c4`): (i) one actor's course claimed another actor's permitted action, (ii) a private caregiver state passed as a world-fact prerequisite, (iii) caregiver falsely bound a child's independent history to themselves, (iv) a downstream mutated/forged eligibility set was selected, and (v) replay accepted an incomplete non-positive receipt by comparing absent identity fields. Three completion controls passed initially.

Code repair: bind courses to their own action actor, enforce objective epistemic class on WORLD_FACT prerequisites, require contextual history owner equality, detect post-evaluation edits and incoherent eligible-entry/set projections with a canonical unkeyed `evaluation_hash`, and compare full recomputed receipts on replay. Explicitly bound mock weight arithmetic to supported 256-bit tickets. **The evaluation hash is corruption/coherence protection only; it is not a key, owner signature or adversarial identity grant.**

* `python -m pytest -q tests/test_p1_contract.py tests/test_p1_completion.py --junitxml=evidence/p1_junit_completion.xml` — **74 PASS, 0 FAIL, 0 SKIP**, stdout in `evidence/p1_pytest_completion.log`.
* Prior rejected behavior — **5 RED / 3 PASS**, preserved in `evidence/p1_completion_initial_red.log`; failures were neither silenced nor xfailed.
* `python -m compileall -q p1_contract.py run_demo.py make_fixtures.py tests/test_p1_contract.py tests/test_p1_completion.py` — PASS.
* `python run_demo.py --coordinate 11` — PASS, selection object byte-identical to the original committed demo receipt (evaluation adds the new evaluation_hash).
* Native B1, CAN008, CAN011, ADP019, ADP020, live LLM and empirical/actor grants — **NOT_RUN**. No new production rule or scientific adoption follows.

**Return-grade remains SOURCEFREE_IMPLEMENTATION_AUTHOR_TEST_PASS, I2_PENDING.** The actual remote follow-up SHA and direct branch read must be recorded outside the commit (self-hash cannot be inserted into its own preimage).
