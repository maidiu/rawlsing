# FIABC-R35-I02 — LiTS R5 and WVS7 Structural-Preimage Bindings

## LiTS-I × Candidate A preserved R5

### Current admission inputs

The consumer requires three independently named inputs:

- preserved carrier root: `RAWLSING_EE_P2X_LITS_A_R5_ROOT`;
- external parentage bundle: `RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT`;
- frozen derivative receipt identity: `RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT_IDENTITY`.

Path binding alone is rejected.

### Exact derivative evidence

The expected derivative class is:

`LITS_A_PRESERVED_R5_CARRIER`.

The receipt binds:

- canonical LiTS-I SHA `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- R5 `physical_root_id` as derivative identity/hash;
- `logical_stream_digest`;
- canonical row count;
- member inventory path/SHA/byte length/member count;
- build config;
- complete R5 release identity;
- embedded source-artifact reference;
- exact builder identity `R5CompactLongShardedBuilder`;
- frozen R5 builder blob expected by the production backend;
- frozen Candidate-A consumer adapter blob `d4915e7e6755ba1850756aebff72f982f73a332b`;
- exact LiTS projection identity;
- runtime catalog `5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02`;
- active binding `a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308`;
- runtime release `192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f`;
- candidate ownership = `A`;
- physical-only latin1 compatibility configuration with pyreadstat `1.3.6`.

Before bundle admission the backend independently checks the R5 root's embedded canonical parent and the member-inventory file SHA/length. The R5 reader/adapter retains its existing member and logical-stream integrity machinery.

### Historical receipt rule

The old estate did not expose the exact external first-build receipt demanded by S35. This implementation does not synthesize one from current root contents. Qualification must supply a receipt actually tied to the governed first build and pin its exact derivative-receipt identity. Otherwise LiTS-A stops.

That is what rejects an old/copied/self-consistent root with the right asserted source SHA.

## WVS7 structural preimage

### Producer path

The governed producer is the exact WVS7 projection materializer blob:

`11b28416aac5a4899706150721f2f8ac8bb6ee43`.

When the canonical raw SAV is available, the accepted materializer itself hashes the raw file before metadata/B_COUNTRY extraction. The backend additionally freezes the reader version/config and seals the source-verification receipt.

### Persisted artifacts

Under the candidate durable root:

- `wvs7_projection_structural_input.json`;
- `wvs7_projection_structural_input.parentage.json`;
- backend durable state containing frozen bundle/source/derivative/structural identities.

The structural JSON's own `structural_input_identity` remains useful as derivative identity. It is not ancestry proof.

### Source-free reopen

Source-free reopen requires:

1. structural JSON present;
2. external parentage bundle present;
3. prior governed parentage freeze present in candidate durable state;
4. exact bundle identity match;
5. exact source receipt identity match;
6. exact derivative receipt identity match;
7. exact structural input identity match;
8. canonical WVS7 SHA closure;
9. exact materializer producer/blob/version;
10. exact reader/config;
11. exact projection/Lock2 currentness;
12. exact candidate/root/process lineage;
13. materializer's existing structural self-hash/geometry checks.

A copied JSON whose self-hash is recomputed has a new derivative identity and cannot satisfy the frozen receipt chain.

## Non-implications

Neither binding grants semantic text authority, source certification, documentary repair, weighting authority, or population authority.
