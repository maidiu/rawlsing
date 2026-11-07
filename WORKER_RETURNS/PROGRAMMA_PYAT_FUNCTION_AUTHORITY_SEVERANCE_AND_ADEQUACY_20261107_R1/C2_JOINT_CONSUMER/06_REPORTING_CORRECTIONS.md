# C2 reporting corrections — independent review 638f75e7

Prior independently reviewed cut: `751fb3fab88ab0faef4b20afeb57a89801f7cce8`.
This is a reporting-only correction cut. No production, existing-test, peer, HQ,
reviewer, original-byte or authority change was made.

| ID | Correction | Exact edit / evidence |
|---|---|---|
| C2-R1 | Provider state no longer hardcoded as consumer vocabulary; derived from actual provider invocation log. | `probes/probe_joint.py` now selects `provide_empirical_possibility_slice` invocation and reads `outputs.provider_state`; corrected probe reports `EXACT_SUPPORTED_SLICE_PRODUCED` with `provider_state_source=actual_invocation_log:...`. `logs/probe_joint.json`; `03_TEST_RECEIPTS.md`. |
| C2-R2 | Prior term relabeled to same-process deterministic rebuild; persisted restore marked NOT_RUN. | Probe field renamed `same_process_deterministic_rebuild`; added `cross_process_persisted_restore=NOT_RUN__SAME_PROCESS_REBUILD_ONLY`. Updated `00_RETURN.md`, `03_TEST_RECEIPTS.md`, `01_CASES.jsonl`, `02_CASES.tsv`. |
| C2-R3 | Wrong-source and missing-registry negatives labeled observed, not asserted; no invented test. | Probe adds `negative_evidence_status`: wrong-order/false-pairing `ASSERTED_BY_NAMED_TEST`; wrong-source/missing-registry `OBSERVED_NOT_ASSERTED`. Typed errors remain `PositionedSubjectPossibilityError` and `EmpiricalQueryExecutionError`. Updated return/receipts. |
| C2-R4 | J-02 demand label reduced to bounded witness evidence. | `01_CASES.jsonl`, `02_CASES.tsv`, `04_MINIMAL_OWNER_ACTIONS.tsv` now use `NO_SELECTED_J_ISSUER_AT_O11__DEMAND_NOT_ESTABLISHED`; no historical-absence/no-justified-consumer claim. F17/F19/F20/F21 remain unmatched. |
| C2-R5 | Old-version/shadow/revocation NOT_RUN surfaced in concise return and limits. | `00_RETURN.md` limits and `03_TEST_RECEIPTS.md` blocked section now state `NOT_RUN__NO_SELECTED_J_ISSUER_OR_VERSION`; case G retains the same. |

## Corrected probe run

One corrected probe run executed:

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.../C2_JOINT_CONSUMER/tmp" \
python3 .../C2_JOINT_CONSUMER/probes/probe_joint.py \
> .../C2_JOINT_CONSUMER/logs/probe_joint.json 2> .../logs/probe_joint.err
```

- Exit `0`; stderr empty.
- Provider state observed/derived: `EXACT_SUPPORTED_SLICE_PRODUCED`.
- Composition state `SUPPORTED`; consumer state `EXACT_SUPPORTED`.
- Same arithmetic: denominators `32/16/8`; fractions `9/16`, `5/8`, `3/4`.
- Same observed typed errors: wrong-order/false-pairing `ConditionValueRelationMismatch`; wrong-source `PositionedSubjectPossibilityError`; missing-registry `EmpiricalQueryExecutionError`.
- Same-process deterministic rebuild matched step IDs, denominators, cells, evidence refs, consumer states.
- Cross-process persisted restore: `NOT_RUN`.
- Old-version/shadow/revocation: `NOT_RUN__NO_SELECTED_J_ISSUER_OR_VERSION`.
- Provenance remains UNPROVED; no equivalence or severance claim. No original J issuer/row was selected or created. Historic documents alone do not mandate issuer reinstatement or create a no-demand gate.

## Historical status

The prior cut `751fb3fab...` and its independently reviewed results remain historical.
The current corrections change reporting vocabulary/labels only; the real-owner
positive arithmetic and observed typed refusals are preserved.
