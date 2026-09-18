# EE-P2R6L ZIP TRANSPORT AUTHORIZATION + R6T SUPERSESSION — 2026-09-18

Status: `R6L_LOCAL_PASS_PENDING_REMOTE_SEAL__ZIP_TRANSPORT_AUTHORIZED__R6T_SUPERSEDED__P2X_HELD`

Decision:

`HQD-2026-09-18-053`

Semantic PRE-MAIN remains:

`1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

## Trigger

EE-P2R6L-R2 locally PASSed at unpushed commit:

`32cc3ab101104d33eb625176299d7dc09cf29190`

with terminal:

`EE_P2R6L_PASS__ACCEPTED_I02_SUCCESSOR_RELEASE_MINTED_AND_VERIFIED__READY_FOR_CONCRETE_REALIZATION_BINDING_ISSUANCE`

Push failed only because:

`WORKER_RETURNS/EE-P2R6L/RUN_OUTPUT/successor_release_replay_manifest.json`

is 118,508,673 bytes and exceeds GitHub's 100 MB per-file limit.

The local PASS commit never became remote repository authority.

## Exact logical replay-manifest identity

Logical artifact:

`successor_release_replay_manifest.json`

Exact byte length:

`118508673`

Exact file SHA-256:

`aa3b6026d4dbc3df8b142725704974eaef810e5dbf5b31d14b19c88cf8ecafd5`

Exact ReplayManifest content hash:

`30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08`

The logical JSON remains the governed semantic artifact.

## Exact ZIP transport identity

Authorized Git transport artifact:

`successor_release_replay_manifest.json.zip`

Exact byte length:

`17663792`

Exact ZIP SHA-256:

`9d2c608f21d9d93111c7418bce945f6245340389d7e8c2ccff70b18af358dd70`

The ZIP contains exactly one member:

`successor_release_replay_manifest.json`

whose uncompressed bytes must exactly match the logical identity above.

ZIP compression is transport-only and creates no new semantic ReplayManifest identity.

## Library archival copy

A durable ChatGPT Library archival copy exists at:

`/Rawlsing/Evidence/EE-P2R6L/successor_release_replay_manifest.json.zip`

Library file identity:

`libfile_ec261ab2a6a48191b13802065af9f249`

Current backing file id:

`file_00000000195481f6ad19378009c5914b`

The Library copy is evidence storage only. GitHub remains authoritative for HQ state and the repository return.

## Authorized unpushed-history rewrite

HQ explicitly authorizes rewriting the **unpushed local commit/history only** that contains the oversized JSON.

This is not a rebase of shared history and not a semantic rewrite.

The remote R6L branch is still:

`26d530c6ed762c4702845b7143c4ea91ae95cec7`

The local worker may replace its unpushed commit `32cc3ab...` with a new commit descended directly from the remote authorized tip, provided:

1. all four governed output logical identities remain unchanged;
2. the three Git-sized JSON outputs remain committed exactly;
3. the oversized raw replay-manifest JSON remains preserved locally byte-for-byte but is **not** committed;
4. the exact authorized ZIP above is committed instead;
5. the governed R6L return and local execution receipt are updated only to add the ZIP transport/archive metadata and to distinguish logical-artifact identity from transport-artifact identity;
6. the receipt continues to bind the original logical JSON SHA-256, byte length, ReplayManifest content hash, and exact runtime release ref;
7. the receipt additionally binds ZIP SHA-256, ZIP byte length, exact inner filename, and Library archival path/file identity;
8. no carrier/source access or driver/verifier rerun occurs;
9. no empirical output is regenerated or semantically changed.

A safe local implementation may reset the unpushed commit to the remote authorized tip with a non-destructive mode that preserves working-tree bytes, then stage the allowed files while excluding the oversized raw JSON.

Commands that discard local files, including destructive reset/clean behavior, remain forbidden.

## Authorized Git return shape

The new pushed R6L return may contain:

- `WORKER_RETURNS/EE-P2R6L/00_RETURN.md`
- `WORKER_RETURNS/EE-P2R6L/01_LOCAL_EXECUTION_RECEIPT.json`
- the three ordinary-size governed JSON sidecars
- the exact authorized `successor_release_replay_manifest.json.zip`
- already-authorized R6L support/commission files.

It must not contain the >100 MB raw replay-manifest JSON.

## Downstream reconstruction law

Before any future Browser binding issuance uses the replay manifest:

1. verify the committed ZIP SHA-256 and byte length;
2. extract exactly one member with the expected filename;
3. verify extracted JSON byte length and SHA-256;
4. verify ReplayManifest content hash and normal R6B/R6R semantic checks;
5. use the reconstructed raw JSON only as a transient verification input.

No downstream semantic law may treat the ZIP itself as the ReplayManifest.

## R6T supersession

EE-P2R6T branch:

`agent/rabochii-prev3-ee-p2r6t-large-json-transport-packaging-r1`

commission tip:

`c0102511c5a65e6b54c160cb9bcf6c7b396ceba0`

is superseded before worker movement.

Disposition:

`SUPERSEDED_UNSTARTED__ZIP_TRANSPORT_PROVED_SUFFICIENT__DO_NOT_EXECUTE`

The five-chunk transport design is unnecessary.

## Next wake

After the rewritten R6L PASS return is pushed, HQ must independently adjudicate it.

On adoption, wake Browser concrete ReleaseRealizationBinding candidate issuance using:

- adopted R6R repaired R5B verifier;
- refreshed R6B issuer/verifier chain;
- reconstructed exact replay-manifest JSON from the committed ZIP;
- contemporaneous exact zero-active-binding epoch snapshot.

P2X remains held.

Terminal:

`ZIP_TRANSPORT_AUTHORIZED__R6T_SUPERSEDED__AWAIT_REWRITTEN_PUSHED_R6L_PASS_RETURN`
