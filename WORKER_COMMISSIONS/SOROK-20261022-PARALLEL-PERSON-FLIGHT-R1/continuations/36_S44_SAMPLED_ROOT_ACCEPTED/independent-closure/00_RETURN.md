# S44 ADP-020 contract closure — ACCEPT_SCOPED

Decision: **ACCEPT_SCOPED**.

## Exact cut

- Corrected candidate: `923278fbe6b030e2ffdd10fe42d7a18266344611`.
- Prior reviewed candidate: `b623a9852e476c9427ec6077285819f0586bc39b`.
- Prior review receipt: `edbaf4264a621f62bda09b3fe140b9cc1b7917a4`.
- Branch: `codex/sorok-s44-sampled-root-consumer`; remote matches.
- Base: accepted S43 `3edd631fb6c31751dfd2143ba2faa9fc31561e54`.
- Reused cuts: M35 `4170fbf…`, S36 `8da78d8…`, S37 `e1f3c1d…`, S39
  `e41513f…`, S40 `79b0357…`, S41 `c72a10d…`, S42 `2489f8c…`, S43
  `3edd631…`, language `8d2920d…`, JOIN-E `7bf2da3…`.
- Reviewed in the existing fixture/review evidence paths. No product edits,
  provider/model calls, extra agents, launcher/notifier changes, or
  native/science action.

## Executed checks

```text
PYTHONPATH=<S44 return> python3 -B -m pytest -q \
  <S44 return>/tests -p no:cacheprovider
10 passed in 5.78s

adp020/changed-candidate contract subset: 2 passed, 8 deselected
```

The unchanged prior ADP-020 contract oracle now exits **0** and reports:

```text
candidate_missing_required_fields: []
coordinate_missing_required_fields: []
coordinate_has_anchor_event_id: false
candidate_set_identity_mode: SET_CANONICAL
```

The actual entrypoint exits 0 with the sampled root, root language evidence,
initial and later native/English speech, cold reopen with the same root/actor
identities, targetless `NO_CHANGE/NO_PROPOSAL` C9, zero target proposals, and
verify true.

## Repair verification

Candidate entries now carry actual sealed/payload-bound
`candidate_replay_hash`, `candidate_authority_id`,
`candidate_authority_version`, `eligibility_or_admission_receipt_hash`, and
`weight_units`. The eligibility payload/hash and replay hash are validated
against the candidate contents, stale same-ID changed payloads are refused,
and properly re-proved payload changes alter the candidate-set and decision
identity. The coordinate contains
`anchor_event_id_or_init_checkpoint_hash` and no legacy `anchor_event_id`;
the draw receipt carries block/uniform/raw fields and its replay hash.

These changes preserve the accepted generated-root → S43/S42 consumer path,
root language evidence, native/English equivalence, cold reader, and
`NO_CHANGE`/zero-target behavior. No broader component review was repeated.

## Receipt

- 10-test output: `evidence/s44-closure-tests-10.out` SHA-256
  `0799c94bed7b9580474ef216cf4f28c4d5a49de7c54b3f7aef528b3ed1b7ff9a`.
- Contract negatives: `evidence/s44-contract-negatives.out` SHA-256
  `b86c2349a287d0508890da8b7598a6b26f353fbd27116ef7666f2047d71f3628`.
- Entrypoint: `evidence/s44-closure-entrypoint.json` SHA-256
  `f436bc26c143b4d4eb09dac3895c9c21f3070ed28e8c6da2e76b8ea0150addfe`.
- Preserved oracle: `evidence/adp020-contract.json` SHA-256
  `d31ad567192f5231bb4200a44f6690a7404279ce231736adc96d8487e32dd959`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
