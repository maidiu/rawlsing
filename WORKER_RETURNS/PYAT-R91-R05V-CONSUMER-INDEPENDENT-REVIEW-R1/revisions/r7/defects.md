# R91 R05V R7 independent review — defects

## R7-P1 — Request slot actual fields rewrite the admitted learned association

`TrustedNativeGraphCoordinator.execute` admission comparison checks only base
fields: producer/consumer query, predicate, model hash, route, source universe,
release. It does not compare request vs admitted M1 disposition, M2 release, B5
selection/currentness, target arity/order, discovery result/receipt/frontier,
recursive handoff/lineage/root-parent, condition witness, E41 input or actual
repository/query/authority/consumer/model objects.

Execution uses admitted actual inputs, but `slot_records`/retained original use
the **request** slot's `m1_disposition`, `m2_release`, `b5_selection`,
`require_current_selection`, `target_arity` and `joint_order_semantics`. The
consumer's learned-association check then compares against the forged request
records.

Dynamic probe
`probes/test_r05v_r7_request_association_gap.py::test_request_slot_cannot_rewrite_admitted_learned_association`:
same admitted slot id/base; request M1 changed from `83220c...` to `049214...`;
admitted discovery executes; trusted consumer with alternate learned object
returns `LEARNED_CONSUMER_EXACT_SUPPORTED`.

Missing function: require full actual-field equality between request and admitted
slot, or build the retained original/slot records exclusively from admitted slots
and reject request-supplied actual associations. Request may select admitted slot
ids/metadata only.

## What R7 fixed/retained

- Executor-only/prebuilt fallback no longer stores a trusted original; R6 probe
  passes.
- Per-slot learned association check exists for the request-recorded original;
  R6 alternate-learned probe passes.
- Actual joint arity 2 and actual changed evidence run through admitted coordinator
  + trusted reader, refuse and restore; discovery/recursive/E41 coordinator
  positives remain.
- Author 40/40; prior probes 22/22; provider 43/43; C1 13/13; typed/Z16 retained.
