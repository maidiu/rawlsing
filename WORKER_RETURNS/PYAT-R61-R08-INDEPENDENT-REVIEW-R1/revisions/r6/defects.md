# R61-R08V R6 independent review — defects

## R6-D2/D5-01 — cache producer-binding metadata is not authenticated

Severity: decisive for the full R61Q D2/D5 cache/export obligation; served
measurement values remain canonical 54/6/60.

Location: `rawlsing_next/pre553_universal_evidence_binding.py`

- `import_authenticated_cache` (~2056) validates:
  - `producer_binding["request_key"]` against the request key;
  - the `binding_hash` self-hash;
  - `owner_identity_material` hash against the signed
    `envelope.owner_identity_hash` (~2107-2132);
  - the context labels/refs and `validated_conditions` against the request.
- It does **not** compare the duplicated top-level binding fields
  (`producer_query_ref`, `predicate_ref`/`predicate_hash`, `release_refs`,
  `consumer_query_ref`, `model_rule_hash`, `source_universe_ref`,
  `risk_set_ref`, `target_ref`, `context_ref`/`context`, `actual_conditions`,
  `consumer_binding_fingerprint`) to `owner_identity_material`.
- It does **not** verify the producer admission token at all.
- `export_cache` (~1988) rebuilds `owner_identity_material`/hash from retained
  material (~2030) but copies the rest of the raw binding payload, so altered
  top-level metadata is re-exported.

The signed `owner_identity_material` is canonical; the duplicated transport
record is not. An attacker can mutate a public cache entry, recompute the public
`binding_hash` and entry `seal`, and the verifier-only re-export path will carry
the forged record forward.

Independent reproducer (`probes/test_r08v_r6_independent_boundary.py::test_producer_binding_metadata_must_not_survive_altered`):

1. Produce a legitimate positive and `cache = resolver.export_cache()`.
2. Deep-copy `cache["entries"][0]`; replace
   `producer_binding["producer_query_ref"]` with a forged exact ref; recompute
   `binding_hash` and `seal`.
3. `EvidenceResolver(admission_verifier=<configured verifier>).import_authenticated_cache(...)`
   accepts; `resolve` returns 60.
4. `export_cache()` returns the forged `producer_query_ref`; a second
   verifier-only resolver imports and reads 60.
5. Replacing `producer_binding["admission"]["token"]` with `"0"*64` is likewise
   accepted on import.

Observed JSON (`outcomes/r6_observations.json` key
`producer_binding_metadata_mutation`):

```json
{
  "altered_producer_query_import_accepted": true,
  "reexported_producer_query_ref": {
    "kind": "FORGED_PRODUCER_QUERY",
    "object_id": "urn:forged:producer-query"
  },
  "second_import_denominator": 60,
  "altered_admission_token_import_accepted": true
}
```

The signed envelope, evidence/query/rule objects and 54/6/60 values are still
canonical; the cache/export producer-binding record is not.

### Minimal missing function

- At import, require every duplicated producer-binding field to equal the
  authenticated `owner_identity_material` (or reconstruct the duplicates from
  it), and verify the producer admission token against the configured verifier
  and owner material, or drop the admission from cache transport.
- At export, rebuild the producer-binding payload from the authenticated owner
  identity material plus request/conditions, and refuse if the retained binding
  record is inconsistent.
- Keep the signed envelope/owner material as the sole authority; no new crypto
  or service is required.

## Observations not scored as separate defects

### Local delivery label

`read()` sets `local_delivery_context_unsigned` from unsigned
`EvidenceResult.provenance`. A cache result mutated to `CANONICAL_PRODUCER`
reports local `LIVE_TRUSTED_EXECUTION`. The label is explicitly unsigned; the
signed `original_execution_provenance`/`original_execution_mode` remain
canonical/live and no `cache_trust_grade` is served. Recorded in
`outcomes/r6_observations.json` key `provenance_semantics`, not scored as a
separate served-trust defect.

### Ephemeral issuer label on verifier-only re-export

A cache exported with `TrustedCacheIssuer` has `issuer_grade`/`issuer_seal`.
Importing it into a verifier-only resolver without that issuer and re-exporting
drops those optional local labels; the original envelope signature, signed
projection and 60 result are preserved. This is a local cache-label downgrade,
not a grade upgrade or served-value change.

### Author test isolation

`test_export_refuses_mutated_evidence_query_and_rule_objects` restores the
mutated evidence cell to 60 rather than its original 6. Its subsequent query
mutation is therefore not isolated from the evidence mutation. The independent
reviewer probe mutates/restores evidence and query separately and confirms both
are refused and the restored export succeeds. Author 38/38 remains regression
evidence, not independent qualification.
