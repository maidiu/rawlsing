# VC4 C06 — REPLAY, EXACTREF & INTEGRITY COURT

Status: `PREPARED__NOT_LAUNCHED`
Branch: `agent/vozhd-chetiri-c06-replay-integrity`
Write scope: `.../VOZHD_CHETIRI_COMPILER_PERSISTENCE/returns/C06/`
Runtime writes: `FORBIDDEN`
Raw source probing: `FORBIDDEN`

## MISSION

Determine the minimum persistent identity/provenance/integrity material required for a source-backed or hybrid compiler path to reproduce exactly the same lawful empirical meaning without a permanent full event carrier.

## DEPENDENCIES

None beyond campaign launch and common contract. Coordinate logically with C02 but do not depend on its conclusions.

## ADDITIONAL READ-FIRST

Read C11 integrity/repository/publication law, ExactRef/content-hash definitions, current R5 semantic projection/inventory/root behavior, V557/V558 publication/repository integrity law, whole-machine replay closure.

## EXACT PROCEDURE

1. Enumerate every identity used from source through C11/I03/I05/I04 and later structural provenance.
2. Separate semantic identity from physical-carrier identity.
3. For each identity/hash/ref, list exact determinant set.
4. Determine whether the determinant set remains available after deletion of transformed empirical copies.
5. Define the minimum persisted roots/manifests/receipts necessary to detect source/authority/compiler drift.
6. Define cache invalidation identity so stale caches cannot acquire authority.
7. Determine whether a semantic release root can be reproduced by streaming source-backed projection.
8. Determine what receipt is needed to re-audit one compiled structural product without requiring analyst trust in a deleted carrier.
9. Test corruption, partial publication, wrong source, wrong authority root, wrong decoder config, stale cache, interrupted build and fresh-process replay conceptually against the proposed contract.
10. Apply terminal checksum; replay must preserve epistemic boundaries rather than merely reproduce values.

## REQUIRED IDENTITY MATRIX COLUMNS

`identity_or_receipt,semantic_owner,determinants,persisted_determinants,recomputed_elements,physical_carrier_dependency,invalidation_rule,integrity_failure_mode,downstream_reference_use,minimum_persistence_class,unresolved`

## MANDATORY COVERAGE

- source snapshot SHA;
- decoder config/version;
- authority snapshot/root;
- respondent replay coordinate;
- variable/question identity;
- event occurrence identity where applicable;
- object_id;
- content_hash;
- ExactRef;
- predicate/discovery/admission replay identity;
- compiled structural product provenance;
- semantic release root;
- cache key/invalidation root;
- deterministic fresh-process replay;
- corruption/TOCTOU/partial publication.

## REQUIRED OUTPUTS

- `SOURCE_BACKED_REPLAY_AND_INTEGRITY_CONTRACT.md`
- `PROVENANCE_MINIMUM_SUFFICIENT_RECEIPT.md`
- `IDENTITY_DERIVATION_MATRIX.csv`
- `C06_RESULT.json`
- common return files.

## BLOCKING CONDITIONS

- any required semantic identity cannot be reconstructed exactly without persistent event payload;
- integrity becomes dependent on trusting optional cache state;
- semantic hashes become physical-layout hashes;
- deletion prevents exact structural provenance/audit;
- terminal checksum reveals epistemic collapse.

## FINAL DISPOSITIONS

- `C06_PASS__REPLAY_INTEGRITY_SOURCE_ROOTED_WITHOUT_FULL_EVENT_PERSISTENCE`
- `C06_PASS__NAMED_CANONICAL_RECEIPTS_OR_SPARSE_MATERIAL_REQUIRED`
- `C06_BLOCK__FULL_EVENT_PERSISTENCE_REQUIRED_FOR_EXACT_IDENTITY_OR_INTEGRITY`
- `C06_BLOCK__REPLAY_PROVENANCE_STARVATION`
- `C06_RETURN__NAMED_EVIDENCE_REQUIRED`

STOP token: `VC4_C06_RETURNED`
