# P3 additive independent qualification — actual return

## Status

**ACCEPT_SCOPED_TEST_ONLY — additive three-test proof accepted.**

**Original sourcefree TEST_ONLY engineering goal can be completed with the stated limits.**
No runtime, tests, fixtures, contracts, accepted source, PROGRAMMA, checkpoint,
prior evidence or authority records were edited. This is a continuation of the
accepted focused runtime review `e85b6f6a`, not a new broad review.

- Frozen HQ cut: `9abb3eee3d59c76ce20d5131d5b60151f7ca98ae`
- Accepted runtime: `16275d03fc4724a694c48ed9d447c4eeadbe25f2`
- Implementation: `486d42a4aa5dcd449564b95567ae93b59c4679a4`
- Protected start: `c852d7516e23fcb6cf2215e9be7c5fa268503516`
- Additive source: `036787c1f0c227cdc47828ba521a62b76c57a903`
- Goal audit: `140b585f9b7321984725cf6f38ae95c2cb2bf89c`
- Review branch: `review/sorok-p3-additive-qualification-20261107-r1`
- Additive test SHA-256: `7fcd6c48a33b0aecb0f689149b235d714599b50d115f1272a7e06dd2b14260d8`
- B1 source SHA-256: `478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3`

## Execution actually performed

Only the three authorized targeted tests were run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
PYTHONPATH=WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1:WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1 \
python3 -B -m pytest -q -rs -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_goal_residuals.py
```

Actual result: **3 passed in 27.15s** (author reported 3 passed in 27.14s).
Log: `logs/three-targeted-tests.log`.

The 13-case matrix, PRIMARY, cold, crash, resource and 71-test inherited suites
were **not rerun** in this additive job. Their prior accepted results remain
historical evidence, not new execution by this review.

Runtime source hashes at the reviewed HQ cut equal the accepted `16275d03`
runtime exactly. The additive test/evidence commits `036787c1` and
`140b585f` are included in the frozen HQ cut. The only new reviewer writes are
in this evidence directory.

Initial review commit `01e0cb130956e90cf398fdb1fd91005469e15033` was pushed to
`review/sorok-p3-additive-qualification-20261107-r1` and directly verified at
the remote. After that verification, `git ls-remote` showed the agent branch at
`44fa2c115658de58a1b92d89bf477e73dbaf8730`, later than the frozen `9abb3eee`
cut. That later head was **not fetched, inspected or qualified** here; the
review target and runtime closure remain frozen at `9abb3eee` / `16275d03`.
The final review-branch head after this correction commit is reported in the
final return and was directly verified against the remote.

## Findings

### 1. Same-history FORMATION vs STABILITY control — PASS with an exact limit

`test_same_history_only_prior_formation_changes_later_response` holds the
sourcefree P2 root id, actor, branch, initial clock, source hash, history
hashes, later proposal and objective world fixed. The only authorized first
plan difference is FORMATION versus STABILITY.

Actual result:

- FORMATION writes two actual `V3MS_MEDIATOR` records (`joint_check`,
  `private_check`; head count 2).
- STABILITY writes zero records (head count 0).
- The later FORMATION response computes `joint_check`/`private_check`; the
  later control computes `inspect_alone`.
- The FORMATION later readset contains the exact prior record hashes; the
  control readset contains neither.
- Both responses require actual OBSERVED P2 participation and report
  `native_action_performed=false`; objective material eligibility is equal.
- P2 objective world after the later event, P2 root/actor/branch/clock and
  material eligibility are equal.

Exact preserved limit: the two cases are separately initialized deterministic
P2 roots with the same logical root binding, not one byte-identical P2
`StateIdentity` snapshot. Their full P2 `state_hash` is **not asserted equal**;
the author evidence records a difference from generated event/action/language
hashes. No independent full-state probe was run because only the three
authorized tests were permitted.

Response-relevant confound assessment: **none identified** in the inspected
path. `p3_owner._context` uses root/actor/branch/clock, project/counterpart,
interlocutor/relation/obligation, actor-observed status, objective material and
source refs. `test_rules.evaluate_event` uses source/registry binding, actual
event/access binding, objective material, history and same-scope records. It
does not choose a response mode from the opaque P2 `state_hash`; the event hash
is a provenance/readset anchor. The only mode-relevant difference is the prior
committed records. This is a valid causal control at the response-relevant
level, while the exact full-state difference is preserved and not denied.

### 2. Actual distinct P2 roots / cross-root denial — PASS

`test_distinct_sourcefree_root_rejects_cross_root_source_before_effects` uses
the supported `P2ProductFanin.start(..., seed=...)` path with a distinct seed:

- left actual root: `3bcb21fc22df3255269382ad249f706dd6dd5378cb886af26542991ff516a4f7`;
- right actual root: `b43c92c076ae9670986c31996d921af00bce804c6bb52bdff25890a6ce0d700c`;
- left has two actual records bound to the left root;
- presenting the left source to the right actual P2 owner raises
  `P3_SOURCE_IDENTITY:root` before any right P3 config/store creation;
- right P2 snapshot unchanged; no right `p3_owner_config.json` or
  `p3_psyche.sqlite3`; no record migration or source string mutation.

This qualifies **actual seeded distinct roots and foreign-source pre-effects
denial**. It does not prove, and this review does not claim, positive
psychological inheritance or migration across a fork.

### 3. Actual-chain B1 severance / exact restore / replay — PASS

`test_actual_chain_source_severance_and_exact_restore` uses a real P2/P3 owner:

- missing B1 path → `P3_B1_SOURCE_SEVERED`;
- altered B1 bytes → `P3_B1_SOURCE_SEVERED`;
- after both denials, P2 snapshot and P3 head are unchanged and no operation
  row exists;
- exact original B1 bytes restored at the exact owner path;
- the actual P2 → P3 event then returns `REALIZED`, accessible `OBSERVED`,
  operation phase `COMPLETE`;
- same-operation replay returns the identical event and leaves P2/P3 state
  unchanged.

No source bytes were edited, forged, retagged or weakened. This is actual-chain
severance/restore/replay, not a unit-only source check.

## Original-goal sufficiency

The three previously identified additive residuals are addressed:

1. the official primary control gap is covered by the same-history/no-mediator
   FORMATION vs STABILITY contrast;
2. the prior replica-only root boundary is covered by actual distinct seeded
   P2 roots and pre-effects foreign-source denial;
3. the prior unit-only B1 severance is covered by an actual P2 → P3 chain
   sever/alter/exact-restore/replay.

With the already accepted runtime review `e85b6f6a`, M1–M3 closure and the
published 13/13 author matrix at implementation `486d42a4`, the original
sourcefree TEST_ONLY engineering goal can be completed under the stated limits.

Precise unproved premise: **exact single actual P2 `StateIdentity`/full-state
snapshot or fork/remap, and positive psychological inheritance/migration across
a fork, are not proved.** The same-history proof is two deterministic roots
with matched response-relevant inputs; their full P2 `state_hash` differs. This
is a fixture/API limit, not a demonstrated response-relevant confound. If a
receiver requires byte-identical P2 state copy, that is an additional
dependency requiring an accepted P2 snapshot/fork/remap interface; it must not
be invented here or turned into a new gate.

The original goal is therefore **sufficient for sourcefree TEST_ONLY
engineering with the stated limits**. It is not native science, human
validation, actor-B evidence, production adoption, CAS, protected merge or
receiving authority.

## Executed versus inspected

**Executed:** only the three targeted tests; source/evidence hash checks against
the reviewed cut and accepted runtime.

**Inspected:** the additive test source; `goal-residual-proof/00_RETURN.md`,
`PROOFS.json`, `SOURCE_PINS.json`, `TEST_LOG.txt`, `TEST_TIME.txt`;
`goal-audit/00_RETURN.md` and `REQUIREMENT_MATRIX.md`; P3 `_context`/`_effect`;
`test_rules.evaluate_event`; the focused-recheck disposition and prior accepted
review as historical context.

**Not executed/rerun:** 13-case matrix, PRIMARY, cold, crash, resource and
71-test inherited suite. No new matrix acceptance is claimed.

## Holds

Native science, production rule/registry, source/B/human/receiving grants, CAS,
protected merge and final PR publication remain **HOLD**. Final PR publication
is held for receiving assembly; no one merges. The final delivery write-up
remains a separate author deliverable.

## Evidence files

- `EVIDENCE.json` — machine-readable execution, findings and limits.
- `SOURCE_CLOSURE.json` — exact SHA closure.
- `ENVIRONMENT_PASSPORT.json` — reviewer/model/environment.
- `logs/three-targeted-tests.log` — actual three-test output.
- `audit/source-pin-check.json` — source hash checks.
- `MANIFEST.json` — evidence file hashes.
