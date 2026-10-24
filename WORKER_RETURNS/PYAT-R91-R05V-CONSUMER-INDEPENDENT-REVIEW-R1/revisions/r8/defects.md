# R91 R05V R8 independent review — defects

No remaining scoped defect found at the configured local trusted-coordinator
grain.

## R7-P1 closed

`TrustedNativeGraphCoordinator.execute` now uses `slot = admitted` after the
base match, so request-supplied actual M1/M2/B5/currentness/topology/discovery/
recursive/E41/witness/native fields cannot rewrite the retained original.

Independent evidence:

- Forged request actual fields with the same admitted id/base: original digest
  remains `404694252163970084c9dd4cc94b9a6e3d450b015e1e4b9251638e276d5d8ddc`;
  admitted learned consumer exact.
- R7 alternate-request M1 attack now returns non-exact refusal (R7 probe 1/1).
- Nested admitted witness identity mutation is refused by native
  `ConditionValueRelationMismatch`, not silently served.
- Executor-only fallback still cannot retain a trusted original; trusted consumer
  refuses.

## Retained controls

Author 40/40; prior probes 23/23; provider 43/43; C1 13/13; actual discovery/
recursive/joint/E41 coordinator positives; typed axes/Z16; accepted owner bodies
unchanged.
