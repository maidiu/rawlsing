# S44 → A42 executable receiving interface

**Status:** READY FOR A REAL, COMPETENTLY ISSUED SOURCE-POSITIVE RECEIPT.
No S44 receipt exists; the real A42 artifacts therefore stay at **0** original
measured cells.

## Where

`s44_adoption_socket.py`

* `validate_s44_source_positive(receipt, scope, issuance_attestation=..., allow_synthetic_witness=False)`
* `to_a42_original_receipt(receipt, validation)` → `A42_NATIVE_RECEIPT@2.0.0` at
  grade `ORIGINAL_MEASURED_OCCUPANCY`
* `scope_with_issuance_overlay(scope, issuance_attestation)` → copy of the frozen
  A42 scope with only the attested wave marked `ISSUED_AND_RECONCILED` and an
  explicit `_s44_issuance_overlay` provenance block (base `scope_digest` preserved)

Then call the unchanged A42 intake:

```python
from a42 import core as a42core
accepted = a42core.ingest_r41_bank({"receipts": [a42_receipt]}, gp, overlay_scope)
acc = a42core.assess_v2(overlay_scope, base_receipts + accepted, w41_register, old_manifest)
```

## Real receipt (`S44_CURRENT_SOURCE_POSITIVE_RECEIPT@1`) — required fields

| Block | Required content |
|---|---|
| identity | `receipt_id`, `origin_commit`, `claim_id` |
| `source` | `source_id`/`wave`, `source_edition`, `source_sha256`, `release_tag`, `native_item_ids` |
| `grant` | `grant_ref`, `issuer_ref`, `host`, `purpose`, `operations`, validity window, not revoked |
| `u_e_pre` | `issued: true`, `issuer_ref`, `issuance_ref`, `scope_hash`, exact `wave`, `eligible_operation_ids` covering every measured operation |
| `clock` | `archive_or_current: CURRENT`, `as_of` inside the estate clock and grant window |
| `measured` | non-empty `operations` with `operation_id`, `fact_state: SUPPORTED`, positive integer `denominator`, in-scope `axis_ids`, no route probability; non-empty declared `consumer_read_refs` |
| `artifacts` | Git artifact records (`commit`, `path`, `blob_sha1`, `sha256`, `bytes`) verified at intake |

## Issuance attestation (`S44_COMPETENT_U_EPRE_ISSUANCE@1`) — separate competent owner

`competent_issuer: true`, `issuer_ref`, `issuance_ref`, `scope_hash`, `wave`,
`eligible_operation_ids`. The socket verifies it matches the receipt exactly; it
**cannot create** this attestation. Synthetic attestations (`issuer_ref` beginning
`SYNTHETIC_WITNESS_NOT_ISSUED`) are accepted only in explicit witness mode and are
never written into the real artifacts.

## Refusals already proven

`S44_MISSING_GRANT`, `S44_GRANT_REVOKED`, `S44_GRANT_HOST_REQUIRED`,
`S44_GRANT_PURPOSE_REQUIRED`, `S44_GRANT_SCOPE_MISSING_OPERATION`,
`S44_U_E_PRE_NOT_ISSUED`, `S44_COMPETENT_U_EPRE_ISSUANCE_ATTESTATION_REQUIRED`,
`S44_SYNTHETIC_*_REQUIRES_EXPLICIT_WITNESS_MODE`, `S44_CLOCK_NOT_CURRENT`,
`S44_CLOCK_VIOLATION`, `S44_UNKNOWN_USER_CONSUMER_REF`, `S44_WAVE_OUT_OF_SCOPE`,
`S44_AXIS_OUT_OF_SCOPE`, `S44_NO_MEASURED_PRODUCT`, `S44_NON_SUPPORTED_FACT`,
`S44_NON_POSITIVE_DENOMINATOR`, and artifact preimage errors.

## What the external decisions must supply

1. Current source + edition + host + purpose + operation grant.
2. Independently frozen eligible U/E_pre for the exact wave/scope.
3. Nonrespondent aggregate/artifact custody (no respondent rows in Git).
4. The declared consumer(s) that actually read the measured product.
5. The method/purpose admission for any F6/F7/N9 use — separate from the source grant.

The socket is transport and validation only; it grants nothing.

---

## R45 continuation — S44 return already ingested

**Returned S44 head:** `cde76f61f10c7f54e0be1582fc7179e23e33979d`.

The S44 return is now part of the merged A42 bank as two extra receipts:

* `S44-AS2B-LITS-I-HISTORICAL` — `HISTORICAL_SCOPE_POSITIVE` at
  `923f2c00b6145182a5e2be5038f579845951da19`, covering SRC27.S19/S21. It adds **2
  retained cells** and reduces missing by **1**; original measured stays **0/1,890**.
* `S44-SOURCE-RUNTIME-HANDOFF` — documentary: one exact SRC27 decision, qualified
  runtime contract, all35 deferred ledger, prospective E_pre **NULL**.

WVS7 remains precedent-only. No current source grant, current selected-B read,
measured original output, F6 transport, observed F7 pair, N11 acceptance or N12 wake
exists. The socket below is the exact place a real S44 source-positive receipt will
enter once the external competent owner signs the SRC27 decision.
