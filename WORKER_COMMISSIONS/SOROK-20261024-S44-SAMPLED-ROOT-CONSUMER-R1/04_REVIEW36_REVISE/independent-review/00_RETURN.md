# S44 sampled-root consumer — REVISE

Decision: **REVISE**.

## Exact cut

- Candidate: `b623a9852e476c9427ec6077285819f0586bc39b`.
- Branch: `codex/sorok-s44-sampled-root-consumer`; remote matches.
- Base: accepted S43 `3edd631fb6c31751dfd2143ba2faa9fc31561e54`.
- Reused cuts: M35 `4170fbf…`, S36 `8da78d8…`, S37 `e1f3c1d…`, S39
  `e41513f…`, S40 `79b0357…`, S41 `c72a10d…`, S42 `2489f8c…`, S43
  `3edd631…`, language `8d2920d…`, JOIN-E `7bf2da3…`.
- Read HQ decision `f5305c6d6159ef7117bce52b95369b5618f5444c`
  (`35_SAMPLED_ROOT_GENERATION_DECISION/HQ_DECISION.md`) and the S44
  commission.
- Reviewed in a disposable fixture. No product edits, provider/model calls,
  extra agents, launcher/notifier changes, or native/science action.

## Executed checks

```text
PYTHONPATH=<S44 return> python3 -B -m pytest -q \
  <S44 return>/tests -p no:cacheprovider
8 passed in 5.45s
```

`run_s44.py` exits 0. It generates a sampled root, starts the actual S43/S42
consumer with the root lifecycle, emits the initial speech from root language
evidence, continues with a later workshop speech, cold-reopens with the same
root/actor identities, and keeps targetless C9 (`NO_CHANGE/NO_PROPOSAL`, zero
targets), native/English equivalence, and verify true. The root and consumer
substitution checks in the focused suite pass.

## Remaining defect

The advertised ADP-020 implementation does not match the authority’s exact
candidate and coordinate contract.

The generated draw receipt’s candidate entry is:

```json
{"candidate_id":"a_material_2","source_ref":"TEST_ONLY_S44_CANDIDATE_A_MATERIAL_2","value":2,"weight_units":1}
```

It is missing the authority-required fields:

```text
candidate_replay_hash
candidate_authority_id
candidate_authority_version
eligibility_or_admission_receipt_hash
```

The candidate-set hash is therefore computed over an incomplete
`ADP020_CANDIDATE_SET_V1` record, so “same candidate ID, changed payload” is not
covered by an immutable candidate replay hash. The draw coordinate also uses
`anchor_event_id` instead of the authority’s required
`anchor_event_id_or_init_checkpoint_hash`:

```json
{
  "anchor_event_id": "INIT:…",
  "coordinate_missing_required_fields": ["anchor_event_id_or_init_checkpoint_hash"],
  "candidate_missing_required_fields": [
    "candidate_replay_hash",
    "candidate_authority_id",
    "candidate_authority_version",
    "eligibility_or_admission_receipt_hash"
  ]
}
```

The current tests exercise determinism and replay but not this exact receipt
contract, so all eight pass while the advertised ADP-020 lineage is not
authority-compliant. This is a concrete contract violation, not a request for
new science or a broader architecture review.

## Required repair

- Require and persist every ADP-020 candidate field: stable candidate replay
  hash, candidate authority ID/version, eligibility/admission receipt hash, and
  the operation-relevant weight.
- Include those fields in the `ADP020_CANDIDATE_SET_V1` canonical record and
  candidate-set hash.
- Use the exact draw-coordinate field
  `anchor_event_id_or_init_checkpoint_hash` (and the authority’s required block
  fields) in replay identity and receipts.
- Add a focused contract assertion that a same-ID changed-payload candidate is
  rejected or receives a different replay identity, and that the coordinate
  fields match ADP-020 exactly.

## Receipt

- 8-test output: `evidence/s44-tests-8.out` SHA-256
  `961ebfa7c50ca4dee4e227f0b9c6d3cbd77f89e230fefacb76619b13ac7b2590`.
- Entrypoint: `evidence/s44-entrypoint.json` SHA-256
  `5e5880bedd1c9fceda46d794f1adbb3364bc240fbe9a6ae62d9ab0737986f914`.
- ADP-020 contract reproducer: `evidence/repro_adp020_contract.py` SHA-256
  `2b9392b8a3d1c3a22b17a7c9a7066d707541b9ed7c39212a1767b8da669148f7`;
  output `evidence/s44-adp020-contract.json` SHA-256
  `fe0b27f4a4d3e0acc76f4eeb6a59032d84cafc9a36ba408685909b5ae508c294`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
