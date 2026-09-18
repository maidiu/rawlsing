# EE-P2R6M governed return

Status: `PASS`

Terminal:

`EE_P2R6M_PASS__ADOPTED_R6L_IDENTITIES_EXACT__VALIDATED_C11_SNAPSHOT_EMITTED_AND_PUBLICLY_REHYDRATED__READY_FOR_BROWSER_R6A_POSITIVE_PROOF`

HQ was resolved at sealed checkpoint `20260918T1911-0400`, immutable handoff
`12ca7dd8e647249f8e2b1d2e049b069eb69bf5b2`, under controlling decisions
`HQD-2026-09-18-062` and `HQD-2026-09-18-063`.

Branch:
`agent/rabochii-prev3-ee-p2r6m-local-validated-c11-snapshot-materialization-r1`

The exact authorized carrier was used once: `LITS-2006-data.dta`,
29,002 x 1,198, SHA-256
`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`.
No other carrier was accessed and no second source replay was performed.

The exact adopted R6K blobs were verified before execution:

- schema `e81963d5e3015335b5db4dd13a340ddadb4e9f53`
- codec `d4427366f15b98ab2acd40578f7ff59ee574b2d0`
- materializer `3decd4055f97f6b55996417d5ad7b84f86c806e0`
- rehydrator `02d731e43b30a85ba2df39dd5b62211c51352981`
- adopted R5B driver `b819fdff50470a71f1c570aa8021e28b361fa986`

Adopted R6L identities matched exactly:

- release ID `LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669`
- semantic release hash `192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f`
- source release manifest hash `0546be4fa3f55239ee5d208234000066bdc84d832e89bc91d646ee623ed96714`
- candidate projection hash `23912633a23318d22bad0da08027867031320331d8d436d944e9c0b21eb086eb`
- ReplayManifest hash `30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08`

## Snapshot and transport

Logical snapshot: `validated_c11_candidate_snapshot.json`

- uncompressed size: `1447731437` bytes
- uncompressed SHA-256: `ca1e62ca14586bcd23392fc56d0af5f95c12d833bf994ef5a0ea09577ca1569b`
- deterministic gzip: compresslevel `9`, `mtime=0`
- compressed size: `116229878` bytes
- compressed SHA-256: `42bff5e6ffc9dd76283b74525f47a5ec99c91ca44d9b5a7537fd13b820ef8e04`

The compressed stream exceeded the 94,371,840-byte Git-safe threshold and was
transported as fixed 50,331,648-byte chunks, without semantic partitioning:

| Index | File | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| 0 | `validated_c11_candidate_snapshot.json.gz.part0000` | 50331648 | `9743cb7de71d470b305c91d3a9c55fd615d2d1544c3ae82bb33cf0e4f4d2ccb2` |
| 1 | `validated_c11_candidate_snapshot.json.gz.part0001` | 50331648 | `0a5b16e20bb16b3b1537ea9b8e15e308f9daa3656c7c6a2fa299a4b3bb9da6f3` |
| 2 | `validated_c11_candidate_snapshot.json.gz.part0002` | 15566582 | `84071bd29a466bbf4f8cfe0fe681749610e18f88fedcb1cd2573a7031b0b1869` |

The canonical JSON remains a single logical artifact; the fixed chunks are
transport only.

## Public rehydration

Public rehydration passed through:

`SERIALIZED_CANONICAL_CANDIDATE_BODIES`
→ `C11SourceReleaseCandidate`
→ `validate_c11_source_release`
→ genuine `C11LogicalRelease`
→ `C11Repository`
→ `resolve_release_exact`

The exact repository snapshot identity is:

`[{"content_hash":"192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f","kind":"C11LogicalRelease","object_id":"LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669"}]`

`resolve_release_exact` passed with one repository release. No binding was
activated, the corrected preimage
`a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308` was not
recomputed, and no R6A binding proof, A/B qualification, BE1, or P2X work was
performed.

Wake: `HQ_SNAPSHOT_ADJUDICATION_ONLY`.
