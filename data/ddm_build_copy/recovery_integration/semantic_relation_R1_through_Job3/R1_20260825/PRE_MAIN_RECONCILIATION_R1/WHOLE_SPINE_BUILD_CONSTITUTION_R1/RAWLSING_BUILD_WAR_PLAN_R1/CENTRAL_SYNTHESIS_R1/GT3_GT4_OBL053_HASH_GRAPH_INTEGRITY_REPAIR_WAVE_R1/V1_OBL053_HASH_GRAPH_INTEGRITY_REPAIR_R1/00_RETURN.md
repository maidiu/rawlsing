# GT3/GT4 V1 — OBL053 CONTENT-ADDRESSED HASH-GRAPH INTEGRITY REPAIR R1

## Terminal

`PASS__GT34_V1_OBL053_CONTENT_ADDRESSED_HASH_GRAPH_REPAIRED__NO_ADOPTION`

## Exact execution boundary

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-gt34-v1-obl053-hash-graph-integrity-repair-r1`
- exact starting / instruction ref: `6bc8b2372deab75655bd4fb251849770cdde5400`
- historical S1 candidate blob: `59c88df41b90f3ca932f52326fe4b275e84c4551`
- historical T1 evidence blob: `4cff92f4f6b8625a94eee7c8aa69dc3566026490`
- historical HQ adoption blob: `286ff7b851e920ff2760082d8b2fb194560ab127`
- repaired semantic candidate SHA: `d14454bf2b464617e617fec5406a11bc2a754c09`
- repaired candidate artifact blob: `14ff405cfb77ccfe30adbce16e9c0ff14fa540f9`
- evidence execution SHA: `e1afc3c1d8c746ffcc75f79c8a5f0c87689aa08e`
- governed court run: `34044557072`
- governed court job: `101517181138`
- protocol self-test: `20 passed in 0.08s`
- bounded repair court: `9 passed in 0.09s`
- receipt artifact ID: `9992689729`
- receipt artifact zip SHA-256: `2ea9d9aa6124d3a27ab396c76baa099db1a94510704cbdce945c02ad81d2bde5`
- OBL053 adopted: NO
- OBL054 touched: NO
- U1 touched: NO
- OBL052 closed: NO
- PRE-MAIN moved by worker: NO
- `main` moved: NO

Transient `.rabochii/court_spec.json` was removed after the exact governed evidence run.

## Historical defect reproduced

The executable court first reproduces the defect that forced this repair.

Against the exact historical S1 candidate:

- seed hash recomputes exactly;
- authority declared hash does not equal its exact persisted semantic projection hash;
- semantic-object declared hash does not equal its exact persisted semantic projection hash;
- objective-evidence-receipt declared hash does not equal its exact persisted semantic projection hash.

Therefore:

`T1_HASH_RECOMPUTATION_FINDING_SUPERSEDED_BY_MECHANICAL_REPAIR_EVIDENCE`

This supersedes only T1's exact hash-recomputation finding. It does not reject T1's constitutive semantic reading.

## Repaired identity graph

Exact repaired identities:

- seed hash:
  `b20687b91e0a7a9cc64a96e229e58244041d54b4ea9c73a182b2f9da0cd2ef53`
- authority hash:
  `867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29`
- semantic-object hash:
  `9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`
- semantic-object ID:
  `urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`
- objective-evidence-receipt hash:
  `153ff1cd67e27b435cb6ffa4127047802eb06edcc6dab7072cedf9cb3ede7d6c`

The graph was rebuilt recursively:

`seed -> authority -> corrected object bindings -> corrected object hash/ID -> corrected receipt bindings -> corrected receipt hash`.

The stale as-persisted object/receipt diagnostic hashes were not promoted as repaired identities.

## Semantic non-change proof

The governed court proves:

- generation-seed semantic projection is exactly unchanged;
- authority semantic projection is exactly unchanged;
- the five objective entity facts are exactly unchanged;
- semantic ceilings are exactly unchanged;
- object-projection changes are only corrected upstream authority-identity bindings;
- receipt-projection changes are only corrected authority/object identity bindings;
- cardinality remains exactly one seed / one object;
- no subject classifier is created;
- no actor/contact/use/encounter/exposure authority is created;
- no comparator/PSEPF/metabolism/CAN-008/V2/positive-V3 authority is created;
- no V3 `subject_ref` is materialized.

## Candidate status

This is a repaired candidate only.

`OBL053 != ADOPTED`

The historical HQ adoption remains immutable history but is not restored by this worker.

Required next sequence:

1. independent hostile review of exact repaired candidate `d14454bf2b464617e617fec5406a11bc2a754c09`;
2. only on hostile PASS may VOZHD issue a fresh OBL053 adoption;
3. only after fresh adoption may OBL054/U1 resume against the corrected root.

## Final

`PASS__GT34_V1_OBL053_CONTENT_ADDRESSED_HASH_GRAPH_REPAIRED__NO_ADOPTION`
