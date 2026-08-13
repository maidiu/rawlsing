# VOZHD ONE-SHOT — Phase-D empirical/semantic independence closeout R1

Base ancestry: commit `2455449a2acde5913de727e446511eeae8b5ee90` on `agent/phase-d-rank1-v550-surface-preflight-return-20260813`.

This task supersedes the prior rank-1-only diagnostic posture **for execution planning only**. It does not mutate M6, Job3-R3, the frozen candidate order, semantic verdicts, or the Phase-D successor contract.

## Goal

Close the remaining Phase-D successor anti-erase archetype by fixing any ordinary implementation defect that violates the constitutional separation between:

1. typed semantic truth / typed relation certification, and
2. respondent-grounded empirical same-respondent co-travel.

The core invariant is:

> empirical co-travel cannot create typed semantic truth, and semantic absence / REJECT / BLOCKED cannot erase lawful empirical co-travel.

The local-block archetype is already instantiated and must remain unchanged.

## Critical finding to test

Current V550 QUC derivation appears to tie the diagnostic empirical relation surfaces to the full V551 semantic certification gate. In particular, `derive_question_use_eligibility()` currently sets:

- `allowed_as_branch_relation_cosignature`
- `allowed_as_attitude_cloud_anchor`
- `allowed_as_attitude_cloud_feature`

from the same `v551 = not failed` gate used for `allowed_as_v551_relation_evidence`.

That coupling may violate the governing anti-erase invariant: a relation member can be semantically blocked/uncertified yet still participate in lawful same-respondent empirical morphology, provided the empirical surface is explicitly diagnostic and does not promote semantic authority.

Do **not** assume the code is wrong merely because this task says so. Prove the contract mismatch from the existing authority law, tests, and output semantics before patching.

## Frozen controls

Do not change:

- M6 ancestry or validator;
- Job3-R3 decisions;
- frozen candidate order or SHA `5ae32c7cdfd68d3e0c1816abd85fc6f77387f65a383e5b860d2ab9cf814235b2`;
- candidate membership or ranking;
- semantic authority rows;
- `BLOCKED_TYPED_RELATION` posture for the anti-erase candidate;
- routing meaning;
- response labels / directionality meaning;
- support thresholds;
- privacy rules;
- Phase-D matcher semantics;
- V550J family authority;
- V552/V552J/V553+.

Do not use respondent overlap alone as evidence. Only the contract-approved multi-question empirical surfaces qualify:

- `branch_relation_co_signature`
- `branch_co_signature`
- `question_response_attitude_cloud`
- governed V550J `joint_patterns`

V550J is optional and must remain `prepared_required`; database reopening from V550J is forbidden.

## Rank-1 factual posture

Frozen anti-erase rank 1:

- candidate: `O12C3-170d6968c83720edbae8f80a`
- source/wave/country: LiTS / II / SE
- vars: `q306c`, `q305_1`
- semantic posture: `BLOCKED_TYPED_RELATION`

Prepared substrate is healthy:

- 4,500 long-form rows
- 900 respondents
- `q306c`: 900 respondents
- `q305_1`: 900 respondents
- both governed non-missing: 838 respondents
- identity: `respondent_id_norm`

Current authority posture:

- `q305_1` is lawfully `STRUCTURAL_CONTEXT`, ranked-choice topology, preserved unsigned. **Do not promote it.**
- `q306c` is source-authority `RELATION_EVIDENCE`, binary contrast, source-anchored directionality `CERTIFIED`, but the active QUC is currently not eligible because response-semantics / structural-mapping / review gates are incomplete.

The current V550 native surfaces are zero-row schemas, not negative empirical evidence.

## Workstream A — prove the independence contract

Inspect the active code and authority laws, especially:

- `ddm_v550_authority_contract.py`
- `ddm_v550_question_use.py`
- `ddm_v550_clouds.py`
- Phase-D successor contract
- M5/M6 constitutional separation docs and tests

Answer with executable evidence:

1. Which native V550 empirical surfaces are diagnostic only and explicitly `not_direct_evidence=True`?
2. Which per-question properties are truly required for a question to be an empirical anchor or co-travelling feature?
3. Which properties are semantic-certification-only and should not suppress empirical observation?
4. Is `STRUCTURAL_CONTEXT` allowed to co-travel as an empirical feature under any existing native V550 surface while remaining structural context?
5. Is the present `v551`-gated cloud permission an implementation defect, or an intended constitutional rule?

If the existing governing contract actually requires full V551 certification for all three native empirical surfaces, stop with a precise governance contradiction report; do not change policy.

## Workstream B — repair only the proven implementation defect

If Workstream A proves that semantic certification is improperly erasing diagnostic empirical co-travel, repair the V550/QUC permission model so that:

- semantic role remains independent of empirical observability;
- `BLOCKED_TYPED_RELATION`, `REJECT`, `NO_GOVERNED_TYPED_RELATION`, or uncertified typed-relation status cannot by themselves suppress lawful diagnostic same-respondent co-travel;
- empirical diagnostic permissions do **not** imply `allowed_as_v551_relation_evidence`;
- empirical diagnostic rows remain `diagnostic_artifact=True`, `not_direct_evidence=True`;
- no empirical row can promote or synthesize semantic authority;
- structural-context items remain structural context;
- unsafe admin / missingness / generation-forbidden / technical identifiers remain excluded;
- response semantics must still be sufficient to distinguish governed substantive values from special/missing values where the builder requires that distinction;
- routing/respondent-universe compatibility remains enforced independently;
- exact question/implementation identity remains required downstream.

Prefer a small explicit contract decomposition over a one-off LiTS special case. Add or repair unit/regression tests that directly encode the constitutional separation.

## Workstream C — repair stale authority propagation only where already decided

Separately audit `q306c`'s active QUC against the already-existing source/deep authority.

If the active QUC is stale/incomplete because existing authoritative artifacts already establish:

- semantic role,
- response semantics,
- directionality,
- structural mapping,

then repair the propagation/materialization path and regenerate QUC with provenance. Do not perform a new semantic adjudication merely to satisfy this probe.

If any required authority is genuinely absent or contradictory, leave it absent/contradictory and record that exact blocker. Do not fabricate structural coordinates, response semantics, or directional atoms.

## Workstream D — build a reusable bounded reproduction capsule

Create a privacy-safe self-contained capsule so Vozhd can reproduce the exact bounded V550 failure/success without the full Postgres database.

Package under:

`phase_d/successor_archetype_conformance/repro_capsule/rank1_v550_repro_r1/`

Include at minimum:

- exact prepared rank-1 respondent slice needed by V550, with respondent IDs deterministically pseudonymized and no direct identifiers;
- only fields actually required by the bounded V550 run;
- exact response-option map rows for the two variables;
- exact source/deep semantic authority rows consulted;
- exact directionality authority rows consulted;
- exact source-structure / structural-mapping rows consulted;
- exact routing/respondent-scope authority rows consulted;
- exact QUC inputs and generated QUC rows;
- V550 invocation config/manifest and CLI command;
- all bounded audit outputs needed to explain gate decisions;
- a machine-readable manifest with SHA-256 for every capsule artifact;
- `README_REPRODUCE.md` with a single deterministic run sequence from a clean repo checkout;
- a validator that asserts row counts, respondent counts, pseudonymization, no direct identifiers, expected authority hashes, and expected V550 surface schema.

Do not package the whole database. Do not include names, emails, free text, or raw identifiers. If the bounded prepared slice itself is sufficient, that is preferred to a PostgreSQL dump.

If extraction behavior itself becomes disputed, additionally create a minimal schema-only + bounded-row database fixture or SQL/CSV import script; otherwise do not add Postgres complexity.

## Workstream E — execute rank 1 to a lawful terminal

After any proven repair, rerun the bounded rank-1 V550 scope and the unchanged Phase-D matcher.

Possible rank-1 terminals:

### E1. `ARCHETYPE_INSTANTIATED`

Use only if one lawful approved empirical surface contains exact co-occurrence of the frozen candidate implementation IDs and the matcher returns:

- semantic: `BLOCKED_TYPED_RELATION`
- empirical: `OBSERVED`

Do not promote semantic authority.

### E2. `NOT_INSTANTIATED`

Use only if the pipeline has been made contract-correct and rank 1 is lawfully incapable of producing an approved empirical exact-match row for a precise reason such as:

- the frozen pair is not representable on any approved native empirical surface under unchanged authority;
- lawful surface materializes but the exact pair is genuinely not observed;
- support is insufficient under existing thresholds;
- exact lawful local-data unavailability.

Zero output caused by a known implementation/authority-propagation defect is **not** a lawful `NOT_INSTANTIATED` terminal.

Record exact evidence.

## Workstream F — autonomously continue the frozen anti-erase ladder

If and only if rank 1 reaches a lawful `NOT_INSTANTIATED`, advance to frozen rank 2 and continue sequentially. Do not rerank and do not skip.

For each rank:

1. verify frozen identity/membership before outcome access;
2. materialize only the bounded data/authority needed for that candidate;
3. use the same contract-correct V550 path;
4. run the unchanged Phase-D matcher;
5. record `ARCHETYPE_INSTANTIATED` or exact lawful `NOT_INSTANTIATED`;
6. stop immediately when anti-erase instantiates.

Continue through the existing 11 frozen anti-erase candidates if necessary. Do not return after each ordinary non-instantiation.

Stop for Vozhd adjudication only if proceeding would require:

- changing semantic authority;
- changing frozen order/membership;
- changing routing meaning;
- changing support/statistical thresholds;
- inventing V550J family authority;
- changing the Phase-D validator's substantive acceptance law;
- loosening privacy;
- architectural redesign outside the empirical/semantic separation defect.

## Workstream G — close Phase D if both archetypes now instantiate

The local-block archetype is already established by the GSS 2010 split-empty-intersection case and must remain unchanged.

If anti-erase now instantiates:

1. produce the complete successor return expected by `validate_phase_d_successor_archetype_return.py`;
2. run the unchanged validator;
3. require terminal exactly `PHASE_D_GATE_CLOSED`;
4. privacy scan must PASS;
5. package no respondent-level direct identifiers;
6. commit all code changes, tests, bounded reports, and the privacy-safe repro capsule;
7. report commit SHA and exact test/validator results.

Do not start V552/V552J/V553+ in this task.

## Required tests

At minimum add tests proving:

1. a semantic `BLOCKED_TYPED_RELATION` cannot be converted into a governed positive by an empirical observation;
2. a semantic block/absence does not erase a lawful diagnostic empirical same-respondent surface;
3. `STRUCTURAL_CONTEXT` is never silently promoted to `RELATION_EVIDENCE`;
4. admin/technical/missingness rows remain excluded from relation co-travel;
5. empirical diagnostic permissions do not imply V551 certification;
6. exact implementation-ID matching remains required by Phase D;
7. rank ordering remains frozen and outcome-blind;
8. no database reopening by V550J;
9. privacy capsule has no direct identifiers;
10. prior certified V550/V551 behavior does not regress.

## Return format

Return one consolidated report, not a sequence of micro-reports.

Include:

- root cause;
- exact files changed;
- authority-vs-implementation distinction;
- test suite results;
- rank-by-rank ladder results actually executed;
- anti-erase terminal;
- successor validator terminal;
- repro capsule path and manifest SHA;
- privacy result;
- final commit SHA.

The purpose of this task is forward movement: solve ordinary implementation problems autonomously, preserve authority boundaries exactly, and either close Phase D or stop only at a genuine governance decision.