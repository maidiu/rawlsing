# R61-R08V frozen expectations

Frozen before inspecting candidate code or author return conclusions.
UTC freeze: 2026-10-23T05:40:58Z.
Reviewer branch: agent/opencode-pyat-r61-r08v-independent-review-r1.
Startup/candidate: ad9c3088096ce291d61dfdd292141073b515fbca.
Commission: 9f8786417d4389d4f344396775aa473d243de71b:WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R08V/00_COMMISSION.md.
Original R08: same tree, R08/00_COMMISSION.md and R08/NODE.json.
Inputs read: INPUTS/CONTRACTS.md, INPUTS/TESTS.md, INPUTS/OVERLAYS.md at the same tree.
Role: independent reviewer, not author, not source/science issuer, not production/CI authority.
Model/account: opencode-go/deepseek-v4.1-flash, variant max, existing user-selected account.
Separation: distinct session/worktree from author; same provider account is not institutional scientific independence.
Budget: 60 minutes, bank by 45; no model/provider changes, no extra sessions or subagents.

## E1 Exact candidate identity and custody

- HEAD must equal ad9c3088096ce291d61dfdd292141073b515fbca; the tree, candidate blobs, author manifest and author proof refs must resolve from that exact commit.
- Candidate code is limited to the R08 allowlist: rawlsing_next/pre553_universal_evidence_binding.py and rawlsing_next/tests/test_universal_evidence_binding.py. Author report artifacts are limited to WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/.
- Reviewer must not modify candidate files, immutable commissions/INPUTS, historical returns, HQ state, decoder/C11/gate, workflows, configuration or lockfiles.
- Reviewer writes only WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/, including disposable probe copies, JUnit, outcomes, witness and manifest.
- The author's claimed test count is not independent qualification. Reviewer must rerun with reviewer-owned evidence and exact import paths/blobs, exit codes and skips.

Falsifiers: candidate source or report absent, unreachable blob, dirty candidate file, author manifest self-inconsistent, or import/test result that cannot be reproduced from the exact candidate.

## E2 Exact request key K

Acceptance expectation: the implementation has a versioned canonical encoding for the full request identity and rejects rather than best-matches on any missing or malformed component. K must bind at least:

1. schema/version and claim grade;
2. source, dataset, canonical wave plus authority-bound aliases, edition and byte/source digest;
3. instrument/decoder version and configuration;
4. occurrence identity: item, option, form, repeat, with duplicate/ambiguous occurrence keys rejected before dictionary construction;
5. sampled/reporting unit, respondent/household role and lawful link refs;
6. applicability/risk/predicate identity;
7. ordered target tuple and ordered condition tuples, each with occurrence, typed value, domain/state version and semantics;
8. operation class and arity;
9. population/sample estimand, weight/design/strata/cluster/uncertainty method refs;
10. target/condition direction, role and consumer-use authority;
11. grammar/model version;
12. release/custody identity and observation/reference/as-of/publication clocks.

Canonicalization expectation: tagged scalar types; bool distinct from int; explicit null distinct from absent; float not silently coerced to string or int; deterministic object keys; semantic order preserved; only owner-declared unordered sets sorted; no normalization that manufactures semantics.

Falsifiers: same-depth wrong condition, value, direction, role, edition, risk, design, estimand, occurrence, clock or source reuses a positive result; bool/int/null/absent/order collisions; request can omit a required identity component and still resolve; K is merely a human label, hash-of-label, target/depth tuple or row index.

## E3 Producer and cache trust boundary

Expected trust model: a checksum is an integrity check, not issuer authentication. The candidate may rely on an explicitly entrusted supervisor/caller or process boundary for provenance, but must not describe candidate-authored, self-sealed digests over arbitrary preimages as authenticated evidence. Production-grade cryptographic deployment is not demanded of this local prototype; honest trust labeling is.

Acceptable positive cache entry expectation: exact full K, producer identity/version, resolved source/edition/engine refs, validation state, authority/permission/currentness, clock/as-of validity and consumer-use scope all bind together. Cache lookup must not be by target/depth, arbitrary label or partial K.

Falsifiers:
- self-sealed forged producer/evidence/result preimage with recomputed digest accepted as exact support;
- digest over wrong request K accepted as evidence for requested K;
- cross-source/edition transposition accepted through the intended public API;
- cache entry replay after as-of/currentness, permission, source or clock change still yields positive;
- cache advertises cold/replay authority without a validated cold path;
- candidate-authored hashes or booleans are the only evidence of execution;
- untrusted cache input can choose its own producer identity and be trusted merely because the digest matches.

## E4 Request-to-actual-producer binding

Expected: resolve_empirical(K) must resolve the actual canonical provider computation or a cache entry whose producer preimage is the exact K-bound actual computation. A request label, wrapper, default object, nearest target/depth or trace dictionary is not a producer binding.

Reviewer will independently vary, at equal depth, the requested condition/value and retain/rebind a different actual predicate or producer; change source/edition/byte identity, risk, direction, role, design/weight/estimand, occurrence/form/repeat, as-of/release/currentness; and include bool/int/null/absent/order cases plus a legitimate positive different request where implementable.

Falsifiers: wrong-request rebinding produces the original requested positive; two distinct K values map to one unqualified producer result; different source/edition/risk/role/design/clock returns exact support with evidence null or mislabeled; legitimate changed request cannot produce its own legitimately changed result through the same actual consumer.

## E5 Actual evaluator call and unchanged consumer

Expected: the real unchanged evaluate_positioned_subject_possibility path is invoked, its returned object inspected, and its values-read witnessed. Reviewer will independently recompute the expected arithmetic for the positive fixture. A separate probe will sever or change the upstream source/condition and require the same assertion to change or refuse.

A new wrapper calling a new helper is not, by itself, evidence that historical J42/P41 callers adopt it. A trace dictionary, marker, monkeypatched label, hash/outcome alone or unrelated default E04 success does not prove the evaluator was called.

Falsifiers: no observable actual call/returned object; output hash only with no witness; new wrapper presented as original caller integration; severance leaves the same productive assertion unchanged; unrelated default E04 success offered as proof of the requested progressive path.

## E6 Cold replay and hostile cache restore

Expected baseline: a fresh-process cold replay from the intended cache/public API, for the exact K, returns the same validated result and status as the warm actual computation, with provenance labeled CACHED and the producer/version still bound.

Expected hostile behavior: after source/edition/byte, permission, clock/as-of/currentness or request identity changes, restore must refuse or produce a legitimately changed same-consumer result; it must not resurrect the stale positive.

Falsifiers: cold baseline fails or needs process-global state; hostile restore serves stale positive; invalidation is only cosmetic; cache accepts a result without its exact K-bound producer/evidence preimage.

## E7 Total status axes and aggregate

Expected: separate eligibility, execution and result axes with exact upstream state preserved. The total aggregate must refuse a productive all-support/exact label when any required input is missing structural state, ZERO_SUPPORT or zero denominator, unknown/unsupported/held/refused, identity/permission/currentness mismatched or otherwise unresolved.

Expected distinctions: valid zero, valid null, diffuse and valid empty remain distinct from no support; all-missing Z stays UNRESOLVED with denominator 16 and no substantive support; a genuinely supported positive survives the same aggregate path.

Falsifiers: missing structural state or ZERO_SUPPORT yields exact/all-support; unknown is dropped from the denominator; eligibility, execution and result are collapsed into one enum; valid zero/null/empty conflated with unsupported; denominator or all-missing identity is rewritten; no positive control survives.

## E8 Reach and endpoint semantics

Expected: characterize separately (a) the new callable evidence-binding grain, (b) unchanged evaluate_positioned_subject_possibility/native provider values-read, (c) unchanged E04/nonparent endpoint fixed semantics where actually reached, and (d) full progressive J42/P41/E04 consumer wiring.

The positioned evaluator is not automatically whole progressive serving. If E04 is exercised, its actual fixed semantics and requested-endpoint association must be stated; an unrelated default E04 success cannot discharge a requested progressive C result. No new E04 court and no broad sweep.

Falsifiers: claimed end-to-end progressive coverage backed only by a new wrapper or default E04; unreached path described as covered; no reproducible covered/unreached boundary case.

## E9 Original J42/P41 caller ownership

Expected: the author's bounded REVISE for historical J42/P41 caller wiring is checked against the inherited exact refs (j42 blob 40f1e9f69fafff37f6bc44474b0189543d4997b3, p41 blob 7d428106c79bcc56973f7c0044fc273a2b354554, empirical blob 23167aa25291fb148b1e3cf210ac33fe7769b783, e04 blob 2181b832d3c4376d4b9428e13f4354f273be8f32). The reviewer must identify the exact maintained callsite/recovery target and the smallest needed owner/scope amendment if one is genuinely required. Archived returns remain immutable and are not live adopted production.

Falsifiers: claiming full end-to-end PASS without caller adoption; demanding edits to archived returns; proposing a broad rewrite; failing to name the concrete missing interface; treating integration permission as a local code defect without evidence.

## E10 Review outcome thresholds

ACCEPT_SCOPED_LOCAL is justified only if all of the following hold: exact candidate custody (E1); exact K binding survives hostile probes (E2/E4); cache trust is honestly bounded and hostile self-seal/replay changes fail (E3/E6); actual unchanged evaluator values-read and arithmetic are witnessed with severance (E5); total status aggregate refuses no-support cases and preserves positive/valid special values (E7); covered/unreached reach is exact (E8); and any remaining J42/P41 caller gap is precisely classified as local defect, integration permission, or consequential architecture/science decision (E9).

REVISE is required if any finite reproducible defect shows wrong-request or unsupported-positive serving, unauthenticated self-sealed cache trust presented as authentication, absent actual consumer/evaluator call, cold-replay false claim, status conflation, candidate/report custody violation, or an unreached path claimed as covered.

NOT_REACHED must name the exact path and reproducibly explain why. It is not a defect by itself when caused solely by the sealed allowlist or missing owner integration; it is a defect if the candidate claims that path as delivered.

## E11 Process and evidence expectations

- Own JUnit for replayed author tests and reviewer hostile/positive/cold tests; exact imports, module paths and blobs.
- Assertion-level mutation/restoration evidence, not import crashes.
- Candidate files unchanged; archived returns/HQ untouched.
- Finite defects ranked by severity with minimal reproduction.
- proof_witness.json with exact commands, exits, skips, session/model, candidate SHA, test refs and assertion outcomes.
- SHA256 manifest for all review artifacts with explicit self-exclusion; no future self-hash claim.
- RESUME.md with actual timing, capacity and stop line.
- Commit and non-force push only the reviewer branch; direct ls-remote verify the resulting SHA.
- No new evaluator, new broad court, original data/credential/external-home read, extra session, subagent, author repair or self-adoption.
