# R61 R01 R5 contract amendment — receipt-bound lineage and issue accounting

Status: frozen before R5 code. Inherits R61L/R61M and the R4 profile without
editing R4 artifacts. TEST_ONLY, sourcefree. No R03 wake.

## Generation convention (one version)

`RecurrenceParent.generation` is the generation that **produced** the parent:
root = 0; a child discovered by generation 1 is generation 1. An issue plan for
generation G requires:

- G=1: exactly one root parent at generation 0 and no receipt-bound parents;
- G>1: one or more non-root parents whose producer generation is G-1 (mixed
  generations, roots, duplicates or skipped labels refuse);
- G never exceeds D.

`activate_next_generation` records child parents with the producer generation
of the generation that discovered them, not the next scheduled label.

## Receipt-bound parent resolver / trust seam

Callers must supply `RecurrenceParentResolver`, created by
`load_recurrence_parent_resolver(path)` from the existing
`load_recursive_handoff_bundle` loader (or from a validated in-process tuple of
`RecursiveBranchHandoff`). The resolver is a declared trusted-coordinator
catalog; this module does not claim a protected issuer, signing service, global
durable uniqueness or R09 enforcement.

For every receipt-bound parent, issue and execution require:

- resolver lookup by `replay_binding_ref` and exact handoff/match;
- `parent.predicate` identity equals `handoff.winning_predicate`;
- `receipt_ref` equals `handoff.receipt_ref`; `replay_binding_ref` equals
  `handoff.ref`;
- canonical parent id recomputation equality;
- source-release set equality with the handoff and the actual execution release
  refs;
- existing owner authority closure and `replay_recursive_branch_membership`
  replay against the actual repository/releases before child issuance.

Missing, severed, altered, cross-source, stale or fabricated bindings are typed
refusals at the same N+1 consumer. Exploratory parents are explicitly
receipt-free and validate their source/risk predicate authority; they never
become winner receipts. Root parents are source-root predicates only.

## Issue-chain accounting

Each `RecurrenceIssuePlan` binds:

- `predecessor_plan_ref` and `predecessor_issued_count` (from the actual
  predecessor plan object, not an unbound integer);
- its own `cumulative_issued_count`;
- policy hash, root predicate ref, generation and exact expected operation ids;
- `state` in `ISSUED` or `STOPPED_BUDGET`.

Generation 1 has no predecessor. Later plans require the immediate predecessor
plan with matching policy/root and exact plan ref/count. Per-generation and
remaining total caps are checked before large materialization. Exhaustion
returns `STOPPED_BUDGET` with exact unissued entries and no native execution;
it is not a bare crash or a fabricated empty result. The law is trusted
coordinator append-only accounting at this module grain; R04/R09 service-level
durability/unique-fork enforcement is NOT_REACHED.

## Preserved

R3 A1-A3, conditioned JOINT/CO_TRAVEL native binding, root/parent comparators,
nonwinning exploration, D/K separation, finite adaptive accounting, R4 profile
parameters and all prior NOT_REACHED boundaries remain. No new scientific
threshold or source authority.
