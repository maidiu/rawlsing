# FIABC-S35-1 — Duplicate / Alternate Source Risk

Status: `CANONICAL_ROOT_SET_UNIQUE__NO_ALTERNATE_ROOT_ACCEPTED`

## Holding

The canonical CLOSED_35 root set contains exactly **35 physical source objects**. Cross-checking the accepted 35-source byte inventory against PREP72's 34-source ledger yields:

- 35/35 unique canonical filenames;
- 35/35 unique SHA-256 values;
- 34/34 PREP72 rows match the independent source-byte inventory on exact filename + SHA-256;
- WVS Wave 7 is the sole intentional PREP72 omission and its HB01 source gate matches the inventory exactly;
- no accepted evidence establishes two competing physical roots for any canonical wave.

This is a source-root result only. It does not certify the 34 Authority71/72 sources.

## Transport objects are not roots

Authority 71 explicitly defines Library bundles as transport only and makes the exact extracted source SHA-256 the source identity.

Non-root carriers therefore include:

- `surveys.zip` for the 33 non-WVS7/non-LiTS-I Authority71 sources;
- `LiTS_I.dta.zip` for LiTS I;
- `WVS Wave 7.sav.zip` for WVS7 HB01.

Archive identity, archive path, extraction location, and Library file ID must never replace the contained source object's exact SHA-256.

## Derived/runtime objects are not roots

The following are also non-root and must not compete with the physical source object:

- database receipts, historical loaders, caches, derived aggregates, or legacy database surfaces;
- PRE553/C11 logical releases and replay products;
- source-specific projection packages;
- P2/P2X deterministic structural preimages;
- runtime materializer packages;
- copied/exported metadata surfaces that do not reproduce the canonical source SHA-256.

The Source-Native Constitution makes source bytes primary physical evidence and rejects path/name/database `source_file` fields as substitutes for byte identity.

## Compatibility decoding does not mint an alternate source

Six PREP72 sources use explicit compatibility execution modes:

- EVS 1999;
- EVS 2008;
- LiTS I;
- LiTS II;
- LiTS III;
- LiTS IV.

In every case PREP72 classifies compatibility as execution/physical extraction only, not source-text encoding authority. The canonical root remains the same exact source bytes and SHA-256.

The remaining 28 PREP72 sources use no source-specific compatibility override. WVS7 HB01 uses a selected raw SAV/SPSS-bytecode decoder at a bounded numeric replay scope; that decoder does not mint a replacement source object or source semantics.

## Historical / alternate-export risk disposition

No accepted Authority71/72, A04, HB01, or R6S evidence reviewed by this worker proves an alternate export with equal authority to any canonical root.

Therefore:

`ALTERNATE_EXPORT_ROOTS = NONE_PROVED`

This is not a universal claim that no historical copy exists anywhere. It is the exact accepted-evidence holding: no second physical object has authority to answer the source-root question for any CLOSED_35 wave.

## Fail-closed rule

If any later packet presents a different filename, size, or SHA-256 for a canonical wave, it must not be silently substituted. It is a new candidate source snapshot requiring explicit source-identity adjudication against this registry.

Terminal:

`FIABC_S35_1_DUPLICATE_AND_ALTERNATE_ROOT_RISK_CLOSED__NO_COMPETING_CANONICAL_ROOT_ACCEPTED`
