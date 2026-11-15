# B06 — Final Two-Source T3 Freeze Producer Contract

Producer:

`python -m rawlsing_next.fiabc_final_oracle_freeze_producers freeze-t3 ...`

## Required inputs

- one standard frozen LiTS-I oracle document;
- one standard frozen WVS7 oracle document;
- `WORK_ROOT` for candidate-root exclusion;
- explicit T3 output path.

Each oracle must independently:

- use `RAWLSING_FIABC_CANDIDATE_NEUTRAL_PARITY_ORACLE@1.0.0`;
- name the expected source;
- pass `verify_frozen_oracle()`;
- bind the exact canonical source identity;
- carry mapping-valued `frozen_authority_identity` and `frozen_workload_identity`;
- have zero candidate outputs/roots/state reuse in its freeze receipt.

The producer computes and records each oracle document's byte SHA itself.

## Emitted law

Schema:

`RAWLSING_FIABC_CANDIDATE_NEUTRAL_FREEZE@2.0.0`

Required invariant values:

- `candidate_neutral=true`
- `frozen_before_candidate_execution=true`
- `candidate_outputs_seen=0`
- `candidate_owned_roots_consulted=[]`
- `candidate_owned_state_reused=false`
- `state=FROZEN_READ_ONLY`

Freeze order:

- source identity: 10
- authority/workload: 20
- oracle materialization: 30

The source roots are exact LiTS-I and WVS7 canonical SHAs and point to the current T2 source-root authority. Authority/workload identities are lifted verbatim from the verified standard oracle court constitutions, so T3 does not create a second authority encoding.

Each oracle entry binds:

- `oracle_identity_sha256`
- `oracle_freeze_authority_ref`
- `oracle_document_path`
- `oracle_document_sha256`

Paths are deterministic relative paths from the T3 receipt directory.

## Self-validation

After atomic write the producer calls existing `load_frozen_upstream_receipt()`, checks byte identity, then calls live T5 `load_frozen_source_oracle()` for LiTS-I and WVS7. The final file is therefore consumable by both the generic candidate-process envelope and the live T5 oracle loader.
