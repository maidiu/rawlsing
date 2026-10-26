# R129 — exact commands

Run from `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01` with the
existing R128 private exports. No checkpoint, raw survey, source hash, decoder,
or C11 respondent snapshot is reread.

## Producer evidence lookup

```sh
git show \
  6286c15bea78758a91686d60e036680bb26c6674:WORKER_RETURNS/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/source_retry_evidence/zero_source_resume_receipt.json
```

The owner catalog is under
`audit.common_execution_binding.runtime_catalog.authorities`; its exact object
refs, not a caller-created selection, bind the snapshots used by the M1 input.

## Actual bounded call

```sh
PYTHONPATH=. python3 \
  WORKER_RETURNS/PYAT-R128-RETAINED-REAL-NATIVE-ARTIFACTS-R1/revisions/r2/runtime/m1_catalog_replay.py \
  --private .r61/r128-retained-native/private \
  --out WORKER_RETURNS/PYAT-R128-RETAINED-REAL-NATIVE-ARTIFACTS-R1/revisions/r2
```

The wrapper:

1. replays the preserved R128 all-24 refusal;
2. loads the 12 exact producer-catalog authority refs from the receipt;
3. resolves each of the six duplicate `AuthorityRef`s to the exact producer
   object ref;
4. adds only the one uniquely required full-custody support snapshot;
5. calls the existing `build_m1_adjudication_input_bundle` and
   `adjudicate_learned_empirical` (family binding absent, empty registry);
6. severs one required snapshot and checks the native refusal;
7. restores the exact catalog and checks the same family-rule refusal.

Outputs:

- `CATALOG_BINDINGS.json`
- `exactNATIVE_CALL_RECEIPT.json`

## Exact selected artifact refs

- Selected receipt:
  `urn:rawlsing:pre553:DiscoveryResultReceipt:sha256:006df79b240d7314d113a86d37ab28c02325af642681c40460977a69d70547b8`
- Selected fact:
  `urn:rawlsing:pre553:EmpiricalFact:sha256:33ee917ffc0ffd217ae5085e5aa37c3ceb0b89f600e65d7cf85c30d79d7e51a6`
- M1 bundle:
  `urn:rawlsing:pre553:m1:M1AdjudicationInputBundle:sha256:e4683f0baf36848a1f26b228d793db642fd47a33802f7893ea91b75d61673d9a`
- Next disposition:
  `urn:rawlsing:pre553:m1:LearnedEmpiricalDisposition:sha256:50cc3a0b1a6f85fd3c824213208b4b54bd8c0697e5f01c5e1d71c960a61ff6dc`

## Constraints held

- No whole-checkpoint `read_bytes` / full JSON load / re-extraction.
- No raw-source, source hash, metadata decode, or respondent snapshot
  restoration.
- No M1 core edit, permissive validator, new authority, snapshot merge, hash
  rewrite, or arbitrary dedup.
- No M2/B5/FF/N10E positive.
- Private `.r61` custody remains the full R128 store; only the invocation-scoped
  exact refs appear in the tracked outputs.
