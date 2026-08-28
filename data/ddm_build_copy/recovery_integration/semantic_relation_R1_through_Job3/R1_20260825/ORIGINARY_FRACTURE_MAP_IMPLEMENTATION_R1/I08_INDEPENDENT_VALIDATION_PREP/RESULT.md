# I08 — INDEPENDENT FRACTURE-MAP ANTI-CHEAT / REPLAY VALIDATION PREP R1

Status: `COMPLETE__MERGE_INDEPENDENT_VALIDATION_CONTRACT_AND_SELFTEST_READY__INTEGRATED_I01_I04_NOT_CONSUMED`

Repository: `maidiu/rawlsing`

Worker branch: `agent/verkhovod-fracturemap-i08-independent-validation-prep-r1`

Mandated starting HEAD: `ee161a1d1f05fad02dfd44c56ade9f9b9e3b1e30`

Scope: Authority-37 independent anti-cheat/replay/noninterference preparation only.

## Verdict

A merge-independent validation surface can be frozen now without reading I01-I07 implementation findings. The validator does not know or assume the post-merge implementation API. HQ only needs a thin adapter after integrating I01-I04 that exports the exact evidence required by `I08_INDEPENDENT_VALIDATION_CONTRACT@1.0.0`.

The acceptance boundary is:

`INDEPENDENT_VALIDATOR_PREP_PASS != INTEGRATED_IMPLEMENTATION_ACCEPTANCE_PASS`

and:

`ORACLE_MAY_JUDGE_OUTPUT_AFTER_RUN != ORACLE_MAY_SEED_CONTROLLER_INPUT`.

G04/L02/L03 expected answers may be used by the later acceptance side only after an autonomous run. They may not appear in caller input, generated candidate reachability, supplied branch membership, secondary-splitter hints, grandchild paths or preselected co-signature targets.

## Governing evidence

Authority 37: `9bafaf2cb96cc3fb46fef6785d486f08987ab71c` / `37_ORIGINARY_FRACTURE_MAP_FULL_JOIN_AND_IMPLEMENTATION_AUTHORITY.md`.

Accepted prerequisite returns read exactly as authorized by the command:

- G04 hostile oracle: `8620265b95f5b3bf8c210674a7735e0ce8dac88c`;
- G05 autonomous-controller audit: `21b4bfbe4f609aeca7a5850a738eff7f663f3ba4`;
- L02 Lebanon real-data oracle: `c9acd7e9ff887dd3a4a29d91f45688cb9c0705a3`;
- L03 branch co-signature real-data oracle: `74834f5028cae0cdd3c525483494437f81c721e0`;
- D01 controller composition: `125fe2ee118dcf51239528a9a15b66fe8a2ef402`;
- D02 selection-law recovery: `ead65727cf1f46e038b1fa8cf94b9a83a3245d88`;
- D03 stop/retention-law recovery: `d088d1b10e63084c61e1ed31f42cc55e53b0a2d9`;
- D04 co-signature composition: `a99596e2692a71379d09c352ccd6fcd622509573`.

No I01-I07 implementation result or sibling return was read.

## Validation modes

The contract separates three independent modes.

### 1. Single-run structural anti-cheat

The post-merge adapter must expose enough immutable evidence to prove:

- no caller/oracle leakage of modal response, predictor winner, branch membership, secondary splitter, grandchild path or co-signature target;
- each generation frontier is canonical/hash-sealed before evaluation begins;
- an open I05 frontier is never mutated from partial results;
- every independently lawful candidate appears in the declared frontier and is evaluated exactly, with no score/top-k/prevalence pruning;
- `NOT P` is guarded by a resolved-coordinate predicate and never absorbs missing/not-asked/inapplicable/unresolved predictor states;
- `NM` is an explicit substantive nonmodal set and never absorbs DK/refusal/missing/not-applicable states;
- every discovered branch carries exact handoff/replay evidence rather than privately reconstructed membership;
- every stopped branch remains retained with an exact stop reason and remains in public map closure;
- J=3 evidence is a direct same-respondent three-target joint with direct joint fact refs, never a pairwise projection renamed J=3;
- J>3 fails closed under Authority 37 unless later authority supersedes it;
- the output jurisdiction remains empirical and contains no actor/V3/personality content.

### 2. Exact replay pair

Two runs with identical determinant values and exact authority identity must reproduce the same:

- sealed frontier identities;
- map identity;
- replay identity;
- dependency-addressable artifact identities.

Any drift is `NONDETERMINISTIC_REPLAY_IDENTITY`.

### 3. Determinant mutation / noninterference pair

The paired mutation validator uses the exact dependency graph. For each intentionally changed determinant:

`DEPENDENT_ARTIFACT -> IDENTITY MUST INVALIDATE`

and

`INDEPENDENT_ARTIFACT -> IDENTITY MUST REMAIN STABLE`.

The dependency graph itself may not mutate between the paired runs to excuse output drift.

The G04 R-only hostile perturbation is the canonical shape: changing only R may invalidate R-dependent topology, while response, P/Q/S, co-signature, J=3 and replay-independent topology remain stable.

## Adapter ceiling

The future post-merge adapter is evidentiary only. It MAY normalize exact evidence already emitted by the integrated implementation. It MUST NOT repair the implementation by:

- reconstructing respondent membership from prose or a private predicate execution when exact handoff/replay evidence is absent;
- inventing a lawful candidate catalog from the controller's own pruned frontier;
- inferring J=3 from pairwise output;
- recomputing a missing public retention record;
- synthesizing semantic or actor labels not emitted under authority.

If the integrated implementation does not expose evidence needed for an invariant, the validator must return an explicit fail/unverifiable disposition rather than infer a pass.

## Production-independent harness

`independent_validation_prep.py` implements the normalized structural, replay and mutation checks using Python standard library only. It imports no `rawlsing_next` module and no I01-I07 implementation surface.

The self-test exercises one valid normalized bundle plus adversarial mutations for all commanded failure classes. Final self-test result:

- checks total: `19`;
- checks passed: `19`;
- failed checks: `[]`.

This is a test of the independent validator itself, not a claim that the future integrated implementation passes it.

## G04/L02/L03 acceptance relation

The later HQ acceptance runner should keep generation-side inputs answer-blind, then compare emitted empirical outputs against the frozen independent oracles:

- G04 hostile synthetic topology, including its R-only mutation noninterference case;
- L02 Lebanon Wave-VIII real-data fracture-map oracle;
- L03 branch-conditioned same-respondent pair/J=3 real-data oracle.

The validator contract is intentionally generic enough to attach to all three without carrying raw proprietary source bytes or embedding their expected answers in the controller request.

## Noninterference receipt

- sibling-blind to I01-I07 implementation findings: yes;
- production semantics modified: no;
- production code modified: no;
- architecture selected: no;
- V3/actor semantics modified: no;
- integrated I01-I04 acceptance executed here: no;
- ready for HQ post-merge adapter + execution: yes.

`I08_INDEPENDENT_FRACTURE_MAP_VALIDATION_PREP_R1_COMPLETE`
