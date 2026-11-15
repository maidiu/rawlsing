# CURRENT_ROUTING_LEDGER_CONTRACT@2 — lossless normalized routing carrier

## Decision

R2 takes **Path B**. The admitted C06 v1 26-column row schema is not the authority itself; it is a denormalized execution representation. Frozen C02-C05 returns preserve the actual current routing adjudications and their evidence/provenance/predicate material in heterogeneous row carriers plus immutable sidecars/manifests. Requiring every sibling to restate that material in C06's exact 26 columns would require fabrication, especially for C05.

`CURRENT_ROUTING_LEDGER_CONTRACT@2` therefore supersedes the physical v1 row contract while conserving all information actually emitted by the frozen workers. It does **not** supersede any routing adjudication.

## Canonical row projection

A materialized Contract@2 row has exactly these fields:

1. `contract_version`
2. `question_implementation_id`
3. `source_family`
4. `wave`
5. `source_variable_code`
6. `disposition`
7. `source_court`
8. `source_commit`
9. `source_carrier_ref`
10. `source_carrier_identity`
11. `source_row_selector`
12. `source_row_record_sha256`
13. `unresolved_token_kind`
14. `unresolved_token`

The first six fields are the exact current identity/disposition projection. The next six bind the projection back to the immutable frozen source row. The last two preserve unresolved taxonomy at exactly the grain the source worker emitted.

## Losslessness rule

Evidence, scope, predicates, replay proof, and adjudication provenance are **not discarded** merely because they are not duplicated into Contract@2 rows. They remain authoritative in the exact frozen carrier/sidecar identified by `source_commit`, `source_carrier_ref`, `source_carrier_identity`, and `source_row_selector`. The materialized row additionally hashes the entire source row record.

The field-by-field proof is in `FIELD_LOSSLESSNESS_MATRIX.csv`.

## C05 non-fabrication law

C05's compact exact carrier emits a 5,387-element ordered disposition code stream and verifies it against the exact current catalog. Its blocker manifest emits **aggregate** unresolved blocker counts, but does not map those counts back to individual unresolved IDs. Therefore:

- C05 unresolved rows use `unresolved_token_kind = NOT_EMITTED_AT_ROW_GRAIN`;
- `unresolved_token` is empty;
- the aggregate blocker manifest remains preserved by immutable reference;
- the compiler rejects any attempt to allocate aggregate blocker counts to C05 rows.

That preserved absence is part of the lossless contract.

## Membership and catalog use

The exact 18,276-row current catalog is used only to verify current membership and `(source_family, wave, source_variable_code)` coordinates, and to perform the exact C05 reconstruction expressly defined by C05's frozen carrier. It is never used to invent evidence, predicates, provenance, or dispositions.

## Canonical durable representation

Because the frozen authority is already split across Git and Library backends, the canonical durable output is a **content-addressed composite carrier**, stored in Library and pinned by a Git manifest. `compile_contract2.py` is its deterministic materializer. In a full Git checkout with the exact Library C02/C04 bytes and exact catalog bytes, it reconstructs C03 and C05 from their frozen Git commits, validates the full 18,276-row join, and emits:

- `CURRENT_ROUTING_DISPOSITION_LEDGER.csv`;
- `UNRESOLVED_TAXONOMY_INPUT.csv` filtered to the exact 14,386 unresolved rows.

The composite carrier is backend-neutral at the semantic level: backend locations are immutable source locators, while content hashes are the identity.

## Fail-closed conditions

Compilation aborts on carrier hash drift, C03 chunk/XZ/canonical drift, C05 ordered-ID or pair-stream drift, duplicate/missing/extra IDs, identity-coordinate drift, disposition-vector drift, non-unresolved taxonomy tokens, or any C05 row-level blocker synthesis.
