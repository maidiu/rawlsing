# P3 Authority Release, Migration, Shadow Promotion, and Rollback Protocol v3

1. Freeze input manifests and effective pair-authority precedence.
2. Build all canonical artifacts read-only and validate schemas/vocabularies/DDL.
3. Create an immutable release row, object snapshot, change ledger, and validation hash.
4. Generate forward migration and complete rollback artifacts.
5. Validate migration in an isolated database or schema.
6. Install into a shadow namespace in the user-designated live target.
7. Rebuild prior and proposed V550J/V551J/V552J outputs under identical runtime inputs.
8. Classify and reconcile every output difference.
9. Promote in one transaction only after all fatal gates pass.
10. On any failure, roll back completely and preserve the failed release and comparison evidence.

Release status changes are append-only events. One release may be current `PROMOTED`; prior promoted releases remain historically queryable. Family revisions and release snapshots are immutable.


## Emergency reactivation sequence
If a promoted successor must be rolled back after the prior release has already received `SUPERSEDED`, the transaction must: (1) append `ROLLED_BACK` to the successor; (2) append a guarded `PROMOTED` reactivation event to the prior release through the explicit `SUPERSEDED -> PROMOTED` transition; (3) update the singleton pointer to the prior release; and (4) run post-rollback validation before commit. Merely moving the pointer to a release whose latest event is `SUPERSEDED` is prohibited.
