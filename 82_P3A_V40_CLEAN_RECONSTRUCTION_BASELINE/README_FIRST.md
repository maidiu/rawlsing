# P3A v40 clean reconstruction baseline

This section records a clean PostgreSQL reconstruction from the verified v41 executable base (Sections 00–62). No P3C recovery-ledger decision was imported.

Hard results:

- 13,526 source-local lineages
- 18,276 implementations and lineage memberships
- 19,175 governing pair facts
- 38,350 resolved endpoints
- 119 candidate components
- 141 R40 candidate revisions
- 141 immutable candidate snapshots
- 345 P3C closure obligations
- 141/141 candidate evidence hashes exactly equal the inherited v40 checkpoint
- applicable q01–q54 gates pass; only the deliberately future-facing post-promotion and P3C-close gates remain false

The only source repair is the read-only v40 reporting seam documented in `91_RECONSTRUCTION_CONTROL/REPORTING_SEAM_REPAIR.md`.
