# Integration readiness — PR #976

**Verdict:** `NOT_READY_FOR_GENERAL_INTEGRATION__SCOPED_P6_CLI_PATH_GREEN__DIRECT_HELPER_REVISE`

## What is green

- PR #976 head is exact and frozen.
- The review branch adds only the independent receiver probe and workflow.
- 37 tests pass, including actual P3/P4/P6 owner regressions and the existing four independent probes.
- The normal P6 CLI path uses the current operation receipt and was not demonstrated bypassed by the new probe.

## What blocks general integration

The exported `situated.current_p3_actor_access` helper accepts an old authentic `source_receipt` when a caller supplies an interval that includes the old event. The helper does not bind the receipt to the current operation or require the receipt interval to match. A direct caller can therefore replay a historical cue as current actor access; with a prior P3 mediator and a direct/injected decision, it can condition a later sourcefree utterance.

This is a real CG-A API-boundary defect, not a defect in the new receiving probe. It is consistent with the author handoff’s admitted direct-internal-caller limit, but the handoff’s current-operation claim is stronger than the code enforces.

## Required before integration

1. Bind the `source_receipt` to the current operation/request identity and/or require exact interval equality with the current operation.
2. Reject old/expanded intervals for outward cues.
3. Rerun the full 37-test suite and `test_hostile_stale_receipt.py`; both must pass.
4. Reissue the G5 verdict at the repaired exact SHA.

No protected merge, native science, actor/human authority or production promotion is authorized by this review.
