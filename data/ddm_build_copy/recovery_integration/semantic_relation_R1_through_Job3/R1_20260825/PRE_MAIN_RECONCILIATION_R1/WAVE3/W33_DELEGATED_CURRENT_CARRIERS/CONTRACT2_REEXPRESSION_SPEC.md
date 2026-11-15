# W33 CONTRACT@2 LOSSLESS REEXPRESSION SPEC

## Decision

Reexpression uses **exact source bytes**. No adaptation is necessary against `daffee545fc60a8cd635aee9aafbe77a920f4c19` because the Contract@2 materializer imports only Python standard-library modules and binds project authority through explicit immutable carrier refs/hashes supplied at execution.

W33 therefore places the exact source blobs in the W33 canonicalization node rather than installing them as a global runtime owner:

- `compile_contract2.py` = Git blob `71f965a792b1791fd9b8c590b4444676aded4ead` from terminal Contract@2 range;
- `test_contract2.py` = Git blob `507cc385d5333fef25333f999807f4021b6941c9`.

This is a physical reexpression only. It does not mint new routing authority.

## Contract preserved exactly

`CURRENT_ROUTING_LEDGER_CONTRACT@2` has 14 projected fields:

`contract_version`, `question_implementation_id`, `source_family`, `wave`, `source_variable_code`, `disposition`, `source_court`, `source_commit`, `source_carrier_ref`, `source_carrier_identity`, `source_row_selector`, `source_row_record_sha256`, `unresolved_token_kind`, `unresolved_token`.

Identity/disposition is projected exactly; nonprojected evidence, scope, predicates, replay material, and adjudication provenance remain in the immutable source carrier/sidecars bound by exact refs/hashes. W33 does not denormalize them back into the obsolete Contract@1 26-column schema.

## Frozen input authority

- C02 `2177fb8767d363ecb77697f5e259f1e10bd05c0b`: 6,021 rows, SHA-256 `0197c20dc6d48106d6070d8b1ba390d43815cd36d92e2f03e70cad04a0a1be4d`.
- C03 `cbaa97ac11c4e8d517b49663f2037f8ea0e04267`: 3,443 rows, canonical SHA-256 `b08b5e4b539cd7936ad24c04a45d8b8e672913f1656482ffc0d3dce5437a095c`.
- C04 `2fe01e4a9508b64f041d6bc13d3c9880661489d3`: 3,425 rows, SHA-256 `c3148341c5a6315c4b060f665595c93c4aa935dfc171aa5faf4c14628f914f90`.
- C05 `509dacadaf863be88d0c6e0d95e9aff6f401af23`: 5,387 rows, exact compact carrier blob `de6872c8089d2e8caa08eb1130868583b95f47cd`, ordered-ID hash `319a74f2bd00d6cd4f3ef434aafbc4ebee635597e6a68d17a86a07462da9ae62`, pair-stream hash `1d72efe346cced887b65e396b0f69645e668415e7dd9cbc69b9e69d420498013`.

The exact 18,276-row Phase-0 catalog is membership/identity-coordinate validation only, never semantic evidence authority.

## Nonfabrication

C05 emits aggregate unresolved blocker counts without row-level blocker allocation. Contract@2 therefore preserves `unresolved_token_kind=NOT_EMITTED_AT_ROW_GRAIN` and blank `unresolved_token` for C05 unresolved rows. Any attempt to assign aggregate blocker classes to individual C05 IDs is a hard failure.

No other source may acquire a disposition, predicate, provenance, scope, or unresolved taxonomy absent from its frozen carrier.

## Durable carrier

The canonical authority remains the content-addressed composite carrier, not a new flat-file authority owner. W33 freshly rehashed the existing durable carriers:

- routing ledger carrier: 5,535 bytes, 18,276 rows, SHA-256 `5fe7fc719453479397fb759a00341dd6dc51184c8547306f7955220091405dde`;
- unresolved carrier: 1,460 bytes, 14,386 rows, SHA-256 `36bd6f3be7f12e938183285dbee30c1db5198a65beab3890f889990e5d8c82ed`.

The compiler remains a deterministic materializer for the full row view when the exact catalog and C02/C04 Library inputs are supplied; C03/C05 are reconstructed by exact immutable Git refs.

## Authority ceiling

`DELEGATED_ACCEPTED_AUTHORITY + PROJECT_CURRENT within CURRENT_JOINT_ROUTING grain + HQ_UNBANKED + NO_GLOBAL_SOVEREIGNTY_EFFECT`.

Integration into W35 cannot widen this ceiling.
