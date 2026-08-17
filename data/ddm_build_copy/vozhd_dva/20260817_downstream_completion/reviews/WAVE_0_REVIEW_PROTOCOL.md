# Vozhd Dva — Wave 0 Review Protocol

Worker completion is evidence, not acceptance. Vozhd Dva reviews every Wave-0 draft PR and its `RESULT.md` / `RESULT.json` before any merge to `agent/vozhd-dva-wave0-integration`.

## Review file location

Create one file per worker:

- `reviews/WAVE_0/R0-01_REVIEW.md`
- `reviews/WAVE_0/R0-02_REVIEW.md`
- `reviews/WAVE_0/R0-03_REVIEW.md`
- `reviews/WAVE_0/R0-04_REVIEW.md`
- `reviews/WAVE_0/R0-05_REVIEW.md`

## Required review sequence

### 1. Identity / reproducibility

Verify:
- worker ID and branch;
- stated base SHA;
- draft PR target is the Wave-0 integration branch;
- report files exist in the correct cell;
- tests/commands reported can be traced to the PR.

### 2. Scope discipline

Answer:
- Did the worker modify only its authorized write domain?
- Did reconnaissance remain bounded?
- Did the worker silently decide cross-stage semantics outside jurisdiction?
- Did the worker reopen V550–V552J without an explicit proved necessity?

Any unauthorized semantic expansion is presumptively `RETURN_FOR_FIX` even if tests pass.

### 3. Upstream authority preservation

Check that the work:
- consumes canonical upstream artifacts/contracts;
- does not recreate obsolete interfaces merely for convenience;
- preserves negative authority, absence, noncomparability, uncertainty, contradiction, and provenance where relevant;
- does not promote generated or inferred material into source authority.

### 4. Downstream adequacy

For every claimed completion, ask:
- What consumer depends on this output?
- Does the worker preserve the information that consumer needs?
- Did it collapse distinctions that later V555/V556/V558/V3 work will require?
- Are transformations explicit and semantically justified?

Local green status is insufficient if downstream information is starved.

### 5. Jurisdiction checks

Enforce:
- V553/V554: structural/temporal priors, no person instantiation.
- V555: mediation affordances/topology, no concrete biography/household facts.
- V556: structural pressure-flow / attractor prerequisites and topology, no finished actor psyche or Enneagram assignment.
- V557/V558: governed runtime boundary, no raw-evidence-to-dialogue shortcut.
- V3 target: actor-specific temporal/developmental realization.
- V2 target: phenomenological/conversational expression, not causal authority.

### 6. Evidence quality

Verify:
- tests actually exercise the claimed behavior;
- no semantic claim rests only on process exit code or nonempty artifact;
- fixture/mocks are identified as such;
- expected failures/current gaps are not presented as pass;
- `RESULT.json` findings have concrete producer, consumer, evidence, and recommended owner.

### 7. Cross-worker synchronization

For every accepted finding or interface proposal:
- identify affected workers/prongs;
- record whether an already-running worker assumption is invalidated;
- add the dependency/collision to `integration/WAVE_0_INTAKE_LEDGER.md`;
- do not merge conflicting local proposals until a Vozhd Dva ruling exists.

## Review dispositions

Use exactly one:

- `ACCEPT` — assignment complete; changes/findings coherent and ready for integration.
- `ACCEPT_WITH_FOLLOWUP` — useful/valid result with a nonblocking follow-up recorded.
- `FINDINGS_ACCEPTED_CODE_RETURNED` — analysis accepted but code must be corrected or excluded.
- `RETURN_FOR_FIX` — worker must amend within assignment jurisdiction.
- `HOLD_FOR_CROSS_HOOK` — correct local work depends on another worker/interface ruling.
- `REJECT` — result is not usable as project authority.
- `DEFER` — valid but outside current execution path.

## Review output structure

Each review file should contain:

1. worker / PR / head SHA;
2. terminal disposition;
3. scope verdict;
4. code-change verdict, if any;
5. accepted findings;
6. rejected/modified findings;
7. downstream obligations confirmed;
8. cross-hooks / synchronization actions;
9. tests independently checked;
10. merge decision and merge order;
11. control-room files that must be updated after acceptance.

## Wave-level rule

No individual worker result becomes a frozen cross-stage contract merely by being merged. After all five returns are reviewed, Vozhd Dva performs a **Wave-0 synthesis/adjudication pass** and updates the authoritative capability matrix, finite implementation register, and Wave-1 launch plan.
