# PYAT1002 — one highest-impact exact competent grant request

**Decision:** `NATIVE_SOURCE_ISSUER_HOLD`  
**Requested unlock:** `SRC04` Arab Barometer Wave I  
**Status of this request:** not granted here; no permission was minted

This is the single highest-impact exact grant the user/competent source steward
must provide to unlock a real first source reader. It is not a source licence
created by this return, not a claim of scientific sufficiency, and not a
substitute for independent receiving.

## Why SRC04 is the selected unlock

SRC04 is the smallest credible existing fixture-positive first-reader candidate:

- 181 original items / 181 physical slots;
- 178 configured response slots;
- 7,337 declared source rows, 181 columns, 1,531,099 bytes;
- no configured weight slot in the R157 counts;
- a surviving nonrespondent fixture `PASS` at `R157_FIXTURE_RELEASE/SRC04`;
- exact historical source SHA
  `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`;
- exact local artifact filename `Arab Barometer Wave 1.sav` is present and its
  current size matches the declared size.

This does **not** make SRC04 scientifically complete. The matrix preserves:

- 179 items with `SOURCE_ROUTING_UNRESOLVED`;
- 2 blocked response-authority gaps;
- no exact form/ballot/administration evidence;
- a source weight slot identified by the exception ledger, without
  design/estimand authority;
- no original respondent positive.

SRC17 is not selected because it has 60 held items (51 continuous, 5
administrative, 2 coordinate, 1 row key, 1 weight held) and an explicit
`ROUTING_UNKNOWN` / sample-frame unresolved state. SRC04 is the cleaner first
engineering unlock.

## Exact competent actor

The grant must come from the **Arab Barometer principal investigator / data
steward or an authorized Arab Barometer archive** with authority over the exact
`Arab Barometer Wave 1.sav` source. It cannot come from:

- the local operator;
- HQ or an issue/contract;
- a model or Browser textual reconstruction;
- a GitHub commit;
- a filesystem mount or `stat` result;
- a user "GO" to sourcefree engineering;
- a nonrespondent fixture authority.

The actor must be able to bind the exact host, purpose, consumer use, semantic
scope, retention/export limits, effective interval, currentness and revocation.

## Exact requested decision shape

The existing historical interface is
`rawlsing_next/pre553_source_read_admission.py::SourceReadRequest` and
`IssuedSourceReadDecision`, resolved through
`SourceReadDecisionResolver.resolve_current(request)`. The request must match
the following proposed fields exactly.

```json
{
  "source_id": "SRC04",
  "source_sha256": "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18",
  "source_format": "SAV",
  "custody_locator_binding": "SRC04_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING",
  "host": "RAWLSING_LOCAL_DARWIN_SOURCE_HOST",
  "purpose": "PYAT1002_SOURCE_NATIVE_S01_S02_FIRST_READ_VALIDATION",
  "consumer_use": "NATIVE_FIRST_READER_I02_I03_ENGINEERING_VALIDATION",
  "read_operation": "SOURCE_RESPONSE_DECODE",
  "physical_read_extent": "EXACT_FILE",
  "metadata_freeze_refs": [
    {
      "kind": "R154_PHYSICAL_METADATA",
      "object_id": "urn:rawlsing:r157:metadata:WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/records/physical/SRC04_PHYSICAL_METADATA.json",
      "content_hash": "6b98d33a8c7598934fcad38cecb3b23e0db7a3031990b302c3df113d295351fb"
    }
  ],
  "semantic_use_scope": [
    "SOURCE_NATIVE_SELECTED_COLUMN_DECODE",
    "U_EPRE_CLAIM_GRADED_OPERATION",
    "RAW_INCIDENCE_LOCAL_ONLY"
  ]
}
```

The competent issuer must return an exact current
`IssuedSourceReadDecision` containing at least:

```json
{
  "decision_ref": "EXTERNAL_EXACT_DECISION_REF_REQUIRED",
  "source_permission_refs": [
    "EXTERNAL_EXACT_PERMISSION_REF_REQUIRED"
  ],
  "source_id": "SRC04",
  "source_sha256": "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18",
  "source_format": "SAV",
  "custody_locator_binding": "SRC04_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING",
  "host": "RAWLSING_LOCAL_DARWIN_SOURCE_HOST",
  "purpose": "PYAT1002_SOURCE_NATIVE_S01_S02_FIRST_READ_VALIDATION",
  "consumer_use": "NATIVE_FIRST_READER_I02_I03_ENGINEERING_VALIDATION",
  "read_operation": "SOURCE_RESPONSE_DECODE",
  "physical_read_extent": "EXACT_FILE",
  "metadata_freeze_refs": [
    {
      "kind": "R154_PHYSICAL_METADATA",
      "object_id": "urn:rawlsing:r157:metadata:WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/records/physical/SRC04_PHYSICAL_METADATA.json",
      "content_hash": "6b98d33a8c7598934fcad38cecb3b23e0db7a3031990b302c3df113d295351fb"
    }
  ],
  "semantic_use_scope": [
    "SOURCE_NATIVE_SELECTED_COLUMN_DECODE",
    "U_EPRE_CLAIM_GRADED_OPERATION",
    "RAW_INCIDENCE_LOCAL_ONLY"
  ],
  "effective_interval": "2026-11-14T00:00:00Z/2026-12-14T23:59:59Z",
  "currentness": "CURRENT_GRANTED",
  "revocation_ref": null,
  "retention_export_limits": {
    "raw_source_bytes": "LOCAL_ONLY_NO_PUBLIC_EXPORT",
    "derived_respondent_level": "LOCAL_ONLY_NO_PUBLIC_EXPORT",
    "derived_aggregate_typed_receipt": "PUBLIC_SAFE_ALLOWED_NO_RESPONDENT_IDS",
    "retention_after_independent_receipt": "30_DAYS",
    "delete_on_revocation": "IMMEDIATE"
  }
}
```

Exact-ref placeholders are intentional: only the competent issuer can supply
the real `decision_ref` and `source_permission_refs`. A placeholder is never
accepted as proof.

`revocation_ref: null` means no revocation is asserted at issuance, not that
revocation is forbidden. The issuer must publish an exact revocation artifact
and set `revocation_ref` if one exists; the existing resolver must re-check
currentness and revocation before every read.

## Requested host binding

`RAWLSING_LOCAL_DARWIN_SOURCE_HOST` is a proposed exact public-safe host
binding for the current local Darwin source host. The issuer must authenticate
that exact binding or replace it with an exact authenticated host string in both
the request and decision. A matching string alone is not authentication; the
issuer's signed/authenticated decision supplies the authentication.

Observed local host context (metadata only):

- host class: `LOCAL_DARWIN_WORKSTATION`
- platform: `macOS-13.2.1-x86_64-i386-64bit`
- source root reference: `RAWLSING_LOCAL_DATA_ROOT`
- artifact relative path: `Data/Arab Barometer Wave 1.sav`
- observed size: `1,531,099` bytes (matches R157 declared size)
- host authentication in this return: `NOT_ESTABLISHED`

## Requested purpose and scope

**Purpose:** local, non-commercial engineering validation of the existing
source-native S01/S02 first-read path.

**Permitted semantic scope:**

- selected-column source decode for the declared supported slice;
- U/Epre claim-graded operation over the exact selected source slice;
- local RAW observed-incidence evidence only.

**Explicitly not requested / not authorized by this grant:**

- public release of respondent-level bytes, identifiers or microdata;
- redistribution or resale;
- population, design-based or weighted inference;
- temporal comparability or trend claims;
- causal claims;
- any other source;
- production CURRENT, protected merge, current-world claim or new issuer;
- any sourcefree 309/150/330 or 100k fixture result promoted into original35.

Optional absent weights do not block a proven RAW observed-incidence operation.
They do block population inference, which remains a separate gate.

## Requested retention and export limits

- Raw source bytes: local only; no public export; no GitHub upload.
- Derived respondent-level artifacts: local only; no public export.
- Public evidence: typed aggregate receipts only, with no respondent IDs,
  credential data or private payloads.
- Retention after independent receiving: 30 days, then delete unless the
  competent owner directs otherwise.
- On revocation: stop and delete the local derived artifacts immediately;
  preserve only the revocation/refusal receipt required by the existing audit
  contract.

## What happens after the grant

Only after an exact current `IssuedSourceReadDecision` is supplied:

1. Bind the exact decision to the exact source SHA and metadata freeze refs.
2. Execute the existing selected-column native source reader only through the
   existing permission-gated owner; assert zero source opens before decision.
3. Run the U/Epre claim-graded operation for the declared selected slice.
4. Produce a changed/restored proof and typed source-native negatives.
5. Persist I02 only if the existing accepted writer/ABI is compatible; first I03
   native fact only if the actual first consumer is available.
6. Submit the exact positive SHA and evidence to a distinct nonauthor for G5.
7. Do not self-accept and do not promote to original35 scientific completion.

If the grant is not supplied, this request remains a hold. Do not retry the same
inventory as if it were a grant.
