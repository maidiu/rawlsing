# Launch guard qualification-closure fix

The first local pre-candidate attempt at head
`43023d8da462cc4f7ad95424e4b1a16a9e858431` stopped at the source-free
repository-diff guard before runtime or source access.  The guard correctly
identified this post-code-head path but incorrectly omitted it from its exact
qualification-closure allowlist:

`WORKER_RETURNS/CANONICAL-REINTEGRATION-FIABC-R1/01_SOURCE_FREE_LOCAL_QUALIFICATION.sh`

Head `d7ddf3347744824bf0b6bc04c243d0730d6c4700` adds only that exact qualified
path to the pre-candidate and measured launcher allowlists.  The allowlist
continues to reject other files in that directory and all unqualified runtime
paths.

Mechanical positive and hostile-path checks passed, both launchers passed
`bash -n`, and the complete governed source-free qualification then produced:

- `172 passed, 28 subtests passed in 26.83s`
- `RAWLSING_RECONCILED_FIABC_STATIC_CROSS_LANE_ASSERTIONS_PASS`
- `RAWLSING_CANONICAL_REINTEGRATION_SOURCE_FREE_QUALIFICATION_GREEN__READY_FOR_PRE_CANDIDATE_FREEZE`

No source bytes, oracle construction, T3 freeze, candidate process, or measured
P2X work was used by this repair or qualification.  A fresh local
source-backed pre-candidate court remains required.
