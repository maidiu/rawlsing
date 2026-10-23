# R61 R01 R4 — bounded adaptive recurrence TEST_ONLY contract/profile

Status: frozen before implementation. Sourcefree TEST_ONLY only. This profile is
not original-source science, a production search policy, or an R03 wake.

## Settled basis

- R61L engineering rules E1–E6 at `3cb1d659bc9efb10b307e66db5cf26af3256f1f5`.
- R61M user-approved S1/S2 principles at `37dba2837c94ddb71287ffbc18260d051fc9765a`:
  preserve source-root context and immediate-parent differentiation as distinct
  views; spend finite effort on hidden internal/minority/counterpattern
  structure; exploratory activation is not a finding.
- R61 grant `3189a0db1433095c95bfe0294af53a40355fa1dd`; R3 accepted A1–A3 and
  left A4 an exact contract gap at `9fbf1ec3bbd569b5fd83cfd9e20cb931523a42c5`.

## Versioned policy shape

`RecurrencePolicy@r61.r4.1` carries:

- exact policy id/version/grade/owner refs and counting convention
  `ANCESTOR_CONDITIONS_COUNT_TOWARD_K`;
- separate J (target arity), K (issued conditioner count including ancestors),
  and D (actual discovery generations);
- root predicate/replay binding and per-parent source/risk predicate/replay
  binding; receipt-bound parents must resolve through the existing recursive
  handoff; exploratory parents must be source/risk/native-constructed
  predicates with no fabricated winner receipt;
- explicit activation rule/reason, breadth/followup caps, protected
  minority/counterpattern slot, deterministic tie order, stage issue rule,
  finite operation budget and stop rules;
- distinct comparator specs for `ROOT_RELATIVE` and
  `IMMEDIATE_PARENT_RELATIVE`; complement is optional and never mandatory;
- issued operation identity, activation ledger, execution/result axes and
  exact consumer/custody refs.

## Reference profile (TEST_ONLY demonstration parameters)

- J=2, K=3, D=3 (three generations add one ancestor-conditioned split each; K counts ancestors honestly).
- Root generation 0 issues the source-root comparison jobs; generations 1..D
  are issued from active parents only.
- Per generation: breadth cap 2, followup cap 2, protected exploration slot 1.
- Tie order: canonical operation id ascending.
- Per-generation issued operation cap 4; total issued operation cap 12.
- Comparators: root-relative and immediate-parent-relative are separate jobs;
  when parent and root predicates coincide the two job identities remain
  distinct views; complement is not issued by default.
- Activation: supported/neutral/minority children are eligible for finite
  follow-up under the caps; a nonwinning exploratory parent may be activated
  through its exact source/risk predicate without a winner receipt.
- Stop: D reached, no active parents, budget exhausted, invalid parent/replay,
  unsupported native capability, or explicit held/out-of-release boundary.
- Unexamined/unissued work is not empty or inapplicable; it is waiting/stopped
  with exact reason. Adaptive bookkeeping never claims confirmatory inference.

## Second profile

`transformed` changes names, source namespace, B=1 breadth cap, protected slot
1, D=2, total cap 6. It must produce the same mechanism under renaming and
different caps, not a selected-question hardcode.

## Native reuse

Only existing owners: PRE553 I05 exact discovery, recursive handoff
(`execute_exact_bounded_discovery_with_handoffs`, `RecursiveBranchHandoff`,
`recursive_parent_atom`, `replay_recursive_branch_membership`) and C11/I03
objects. No new engine, owner edits, source authority or scientific threshold.
