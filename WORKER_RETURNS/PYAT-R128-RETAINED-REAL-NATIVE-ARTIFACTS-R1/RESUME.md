# R128 resume — retained real native artifacts

## Status

`ARTIFACT_RECOVERY_PASS__M1_INPUT_REFUSED__CONFLICTING_AUTHORITY_SNAPSHOT_PREIMAGES__FULL_CONSUMER_NOT_REACHED`

- Branch: `agent/opencode-pyat-r128-retained-real-native-artifacts-r1`
- Startup: `979d31366454e0fe9e085f7da3972ad34746c6cf`
- Return: `WORKER_RETURNS/PYAT-R128-RETAINED-REAL-NATIVE-ARTIFACTS-R1/`
- Input: exact final-success LiTS checkpoint, 3,404,445,161 bytes, SHA-256
  `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`.
- Private custody: `.r61/r128-retained-native/private/`
- Source access: zero. The checkpoint is a retained artifact, not raw source.

## Reached

- Independently verified checkpoint size/hash, internal checkpoint identity,
  closure schema, and closure identity `f264dd8f…6f415`.
- Recovered 234 exact native object preimages into private content-addressed
  custody: 60 facts, 63 queries, 35 predicates, 24 authorities, 1 discovery
  authority, 50 discovery receipts, 1 universe.
- Verified all 234 native constructor round-trips and exact content hashes.
- Preserved full fact member/provenance/topology material privately.
- Historical ASTRA summary retained separately from native objects.
- Existing M1 input owner reached and refused:
  `M1IntegrityError: conflicting exact authority snapshot preimages`.
- Identity/ref severance rejects; exact restoration passes.

## Immediate blocked edge

Six retained `AuthorityRef`s each have two different exact
`AuthoritySnapshot` preimages. The existing M1 input owner refuses to canonicalize
both, so no M1 bundle exists and no family validator/admission can be reached.
The exact conflict groups are in `CONSUMER_RECEIPT_OR_REFUSAL.json`.

R128 did not select a preimage, mint a replacement authority, or invent family
law.

## Next

1. Owner-approved exact resolution of the six duplicate authority preimages, or
   an exact unique snapshot per `AuthorityRef`.
2. Rebuild the real M1 input bundle.
3. Bind the exact existing family rule/validator/admission required by the
   retained evidence.
4. Then attempt M1 -> M2/B5 and the actual FF/V553/N10E consuming edge.

## Holds

No source/current measurement, original-survey access, actor/dyad/V3, CI/prod/
R09, N11/N12, Sorok, J52/W52, full35/1890/F1–F8/globalF6F7F8/LongMemory, or
parallel C5 action was performed or authorized. Historical counts are
conservation checks, not current scope.
