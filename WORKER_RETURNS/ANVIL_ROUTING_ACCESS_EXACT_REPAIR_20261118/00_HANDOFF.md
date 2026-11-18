# Routing access exact repair

## Status

**REVISE findings repaired. Frozen for same independent reviewer. No self-acceptance.**

- Branch: `agent/anvil-engineering-cut1-20261117-r1`
- Start HEAD: `1620f625d086d4e102c10112a4628b07f1689137`
- Prior code: `73b480080ede013770e0c887aa5aa82af3cfafb2`
- **Repair code/test SHA: `aee95429609c372564e996c2d3d3eb30e9253cbf`**
- Review pinned: `1a02f52800734bcb68d165cef67f79efa0be3d72`
- Product changes: original three paths + one focused regression only
- Prior failed/evidence commits preserved.

## Repairs

### B1 — symbol boundary

Removed module-level `_RoutingLookup` and `_routing_lookup` session state. Locator lookup is now the same-class private
`DirectEstateI03Session._routing_facts`, bound through `indices_for`.
`_ReleaseIndex.routing_lookup` is a callable defaulting to `None`.

### B2 — redundant index and unused column

Removed `routing_locator_resp_idx`; the composite primary key provides the
exact respondent-first access/order. Removed unused `member_set` column.
Authoritative body member-set replay semantics remain in the canonical body/
evaluator.

### R1 — bounded row-group access

`_routing_facts` uses the existing session `_row_group_cache`, holding one
routing row group at a time. No per-lookup dict accumulates decoded groups.
Canonical ref order, exact keys and CURRENT before lookup/each yield remain.

### B3 — genuine distinct conflict

Added a controlled test-only C11 candidate with two genuinely distinct
canonical routing facts for the same respondent/target/risk, with different
routing state and member-set semantics. Through the **actual physical locator**:

- both exact facts are returned in canonical ref order;
- native `_routing_fact_for` conflict refusal occurs;
- a separate actual-fact adapter witness verifies multiple nonconflicting
  matches both enter `used` and authority validation without reordering the
  evaluator checks.

### B4 — eager malformed preparation refusal

Added a focused controlled corruption of the routing projection/body path that
proves session preparation refuses before any filtered absence can be trusted.

## Tests

- Focused locator + prepared sessions: **11 passed, 0 failed, 6.73 s**
- Existing coordinate/weight/true-k3 nodes: **3 passed, 29 deselected, 0.20 s**
- Existing changed-source/restore node: **1 passed, 0.99 s**
- No full earlier suite repetition, heavy benchmark, 100k, raw source or SQL.

Evidence:

- `evidence/focused.txt`
- `evidence/existing_checks.txt`
- `evidence/changed_restore.txt`

## Measurement correction

The prior same-session Q timer comparison is **superseded as an end-to-end
or amortization measurement**. It only toggled the adapter on one candidate
session. No end-to-end gain, no full H/S/Q/O accounting, and neither measured
amortization nor measured failure to amortize incremental preparation is
claimed here. This repair adds no new performance run.

Fixture readiness pin `ab0d54b18ffc8437f9736cd9534ed4536c4484b8` still records
no retained weighted-k3+coordinate combination. No duplicate matched
comparison was run; the prior already-started comparison is not repeated.

## Limits

- Tiny controlled 8R fixture; no survey-scale/100k.
- Actual physical conflict test uses a controlled C11 candidate, not raw source.
- No persistent artifact, reverse index, coordinate/weight locator, group cache
  or second dataset.
- No source/science/actor/CURRENT/protected/issuer/writer authority.
- Distinct independent review pending.

**STOP after commit/push/remote verification.**
