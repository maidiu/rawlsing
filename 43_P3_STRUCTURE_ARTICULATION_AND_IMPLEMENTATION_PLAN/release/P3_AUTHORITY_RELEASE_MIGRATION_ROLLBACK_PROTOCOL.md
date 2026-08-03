
# P3 Authority Release, Migration, Promotion, and Rollback Protocol

## Purpose

This protocol governs publication and eventual runtime installation of P3 authority. The planning pack authorizes no live write.

## Release objects

Every release records:

- stable release ID and parent;
- input manifest hash;
- schema and builder versions;
- canonical and derived object counts;
- added, changed, superseded, deprecated, blocked, and unchanged object IDs;
- validation return hash;
- migration and rollback artifacts;
- status.

## Release statuses

`DRAFT → VALIDATED → SHADOW → PROMOTED`

Alternative terminal routes:

- `VALIDATED → SUPERSEDED`
- `SHADOW → ROLLED_BACK`
- `PROMOTED → SUPERSEDED`

There may be only one promoted release in the live authority namespace.

## File-based pilot release

P3A remains artifact-based. It publishes immutable files, manifests, hashes, evidence packets, decisions, and validation returns. It does not write live tables.

## Migration preparation

P3C produces:

1. PostgreSQL-compatible forward migration;
2. test-database validation queries;
3. shadow namespace installation script;
4. prior-versus-proposed comparison queries;
5. transactional promotion script;
6. rollback script;
7. release change ledger;
8. downstream impact report.

## Shadow gate

Promotion is prohibited unless:

- the user designates the current live repository/database;
- schema and current authority are inventoried;
- migration applies cleanly in isolation;
- shadow installation preserves historical authority;
- V550J/V551J/V552J comparison returns are complete;
- every changed family membership, certification, gap, or downstream output is explained;
- rollback is tested.

## Rollback

Rollback restores the prior promoted release without deleting the failed release or its evidence. The failed release remains queryable with status `ROLLED_BACK`.

## Historical reproducibility

Every runtime artifact records the exact semantic-family release, measurement release, structural release, builder version, and input manifest. Later revisions never rewrite historical outputs.
