# FIABC-LM1-R1A — Historical Parentage Adjudication

## Holding

HISTORICAL_R5_PARENTAGE_NOT_PROVED

The repository contains strong contemporaneous evidence that the exact preserved LiTS-I Candidate-A R5 was freshly built. It does not contain the complete immutable parentage chain required by current R35 law.

## Required chain versus evidence

| Required link | Holding | Evidence / defect |
|---|---|---|
| canonical LiTS-I SHA | PROVED | 7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09 appears in the contemporaneous first-build receipt and current canonical estate |
| exact source verification before/during build | PARTIAL | first-build receipt records exact source SHA, bytes, source-open/decode counts and candidate-neutral preflight; no FIABC_CANONICAL_SOURCE_VERIFICATION_RECEIPT identity from that build exists |
| exact reader/config | PARTIAL | contemporaneous evidence gives decode_dta(source_path, encoding=latin1) and execution runtime pyreadstat 1.3.6; it does not bind the full current R35 reader_config object as a sealed receipt |
| exact authoritative builder/blob | BUILDER AUTHORITY PROVED; CONTEMPORANEOUS LINK ABSENT | accepted Route-A evidence proves R5CompactLongShardedBuilder at 92e364b31eaf27be1bca2081eff65f6ffb779c3d; E01 never binds that Git blob |
| exact build operation/config | PARTIAL | fresh absent-target R5 first-build is contemporaneously stated and build telemetry is present; exact R5BuildConfig and builder blob/config identity are not sealed into E01 |
| exact R5 derivative identity | PROVED | physical_root_id e8f37557493b816e4562f5f47df110cf49b429e9ead54e5b624d6638ee07aa3d plus 34,745,595 rows, 2,121 shards and de8f060aa72eff7e45f8355ed683cb8ee4b6aca7ff255167cb41bcf8e5a7e3d6 |
| currentness/ownership sufficient for R35 | NOT PROVED | later owner/runtime qualification cannot retroactively parent the old derivative; no accepted bridge law does so |

Any inferred link fails the commission's required chain. The builder can be identified from later accepted repository evidence, but attributing that exact Git blob to the historical build would still be an inference because the first-build receipt does not bind it.

## Strongest evidence

WORKER_RETURNS/EE-P2X/01_LITS_I_A_FIRST_BUILD_STAGE.json was first committed by 02a7ff71ae65b1aa8c52add0b315244a9eaea9df as the LiTS-A first-build stage receipt.

It is classified:
CONTEMPORANEOUS_FIRST_BUILD_EVIDENCE__INSUFFICIENT_FOR_R35_GENERIC_PARENTAGE

It records:
- canonical LiTS-I SHA and byte size;
- decode_dta(..., encoding=latin1);
- Candidate A / R5_LONG_COMPACT_V2__SERIAL_V4__AUDIT69__C05R2A_FACADE;
- exact physical root;
- exact canonical row count;
- final shard count;
- logical stream digest;
- projection/C11/replay identities;
- observed first-build telemetry.

This is genuine first-build evidence. It is not a generic parentage bundle.

## Why later evidence cannot repair the chain

Accepted Route-A qualification later verifies the builder/runtime object set. P2R6O later preserves the historical first-build reference. LM1 later verifies the old carrier's internal physical facts. These are all useful evidence.

None is a contemporaneous source-verification receipt cryptographically parented into a derivative receipt from the first build.

R35-I02 explicitly requires the external receipt and explicitly refuses to synthesize one from an already-existing carrier. The embedded canonical source SHA in the R5 root is therefore corroboration, not ancestry proof.

## Result

Historical parentage under current R35 law is not proved. No retrospective parentage receipt should be minted from present carrier contents or later repository knowledge.
