# RAWLSING HQ CHECKPOINT — 20260918T1736-0400

Status: `R6L_LOCAL_PASS_PENDING_PUSH__ZIP_TRANSPORT_AUTHORIZED__R6T_SUPERSEDED__P2X_HELD`

Semantic PRE-MAIN:

`1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

Controlling decision:

- `HQD-2026-09-18-053` — authorize ZIP transport for the oversized R6L replay manifest, authorize rewrite of unpushed local R6L return history only, and supersede unstarted R6T chunking.

Adoption/authorization record:

`HQ_HANDOFF/EE_P2R6L_ZIP_TRANSPORT_AUTHORIZATION_20260918.md`

## Pending R6L PASS

Reported unpushed local PASS commit:

`32cc3ab101104d33eb625176299d7dc09cf29190`

Remote branch remains:

`26d530c6ed762c4702845b7143c4ea91ae95cec7`

Logical replay artifact:

- filename: `successor_release_replay_manifest.json`
- bytes: `118508673`
- file SHA-256: `aa3b6026d4dbc3df8b142725704974eaef810e5dbf5b31d14b19c88cf8ecafd5`
- ReplayManifest content hash: `30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08`

Authorized ZIP transport:

- filename: `successor_release_replay_manifest.json.zip`
- bytes: `17663792`
- ZIP SHA-256: `9d2c608f21d9d93111c7418bce945f6245340389d7e8c2ccff70b18af358dd70`
- exactly one inner member: `successor_release_replay_manifest.json`

Library archival copy:

`/Rawlsing/Evidence/EE-P2R6L/successor_release_replay_manifest.json.zip`

Library ID:

`libfile_ec261ab2a6a48191b13802065af9f249`

The raw >100 MB JSON must remain byte-preserved locally but not be committed. The ZIP is transport-only and must never replace the logical ReplayManifest identity in semantic checks.

## R6T

`agent/rabochii-prev3-ee-p2r6t-large-json-transport-packaging-r1`

Disposition:

`SUPERSEDED_UNSTARTED__DO_NOT_EXECUTE`

## Next wake

Rewrite only the unpushed R6L local return commit so Git contains the exact ZIP transport plus updated receipts instead of the oversized raw JSON; push; then HQ adjudicates the pushed R6L PASS.

After R6L adoption:

`Browser concrete binding issuance using adopted R6R refreshed R6B chain + exact zero-active-binding epoch snapshot + transient extraction of exact replay JSON from committed ZIP`

P2X remains held.

Terminal:

`ZIP_TRANSPORT_AUTHORIZED__AWAIT_REWRITTEN_PUSHED_R6L_PASS_RETURN__P2X_HELD`
