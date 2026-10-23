# R61-R08V R5 independent review — defects

## R5-D3/D4-01 — SAME reader serves an unsigned provenance/trust grade

Severity: decisive for the complete signed/served projection obligation.

Location: `rawlsing_next/pre553_universal_evidence_binding.py`

- `_envelope_result_projection` (~2252) and `_result_matches_envelope` (~2273)
  enumerate the signed result relation but omit `EvidenceResult.provenance`.
- `ExecutedEvidenceEnvelope` has `trust_grade` but no signed execution
  provenance/mode (live producer vs authenticated cache).
- `EvidenceConsumerReader.read` (~2519) returns `envelope.consumer_values_read`
  (good) but then sets `cache_trust_grade` (~2539) from
  `self.result.provenance`, an unsigned field.
- `EvidenceResult.__post_init__` permits a SUPPORTED result to carry either
  `CANONICAL_PRODUCER` or `AUTHENTICATED_CACHE`; a public `dataclasses.replace`
  can switch them without touching the signed envelope.

Independent reproducer (public APIs only):

1. Produce the canonical positive through the configured host:
   `SUPPORTED`, denominator 60, `provenance=CANONICAL_PRODUCER`, signed envelope
   `trust_grade=TEST_ONLY_SCOPED_LOCAL_TRUSTED_HOST`.
2. `mutated = dataclasses.replace(produced, provenance="AUTHENTICATED_CACHE")`.
3. `EvidenceConsumerReader(request, mutated, verifier=<same configured>).read()`
   succeeds and returns
   `cache_trust_grade=FULL_K_PRODUCER_ASSOCIATION_SHA256`.
4. Reverse case: import the legitimate exported cache into a verifier-only
   resolver; `restored.provenance=AUTHENTICATED_CACHE`; replace it with
   `CANONICAL_PRODUCER`; the same reader succeeds and omits
   `cache_trust_grade`.

Observed JSON: `outcomes/r5_observations.json` key
`provenance_grade_mutation`:

```json
{
  "canonical_signed_provenance": "CANONICAL_PRODUCER",
  "canonical_supplied_provenance": "AUTHENTICATED_CACHE",
  "canonical_read_cache_trust_grade": "FULL_K_PRODUCER_ASSOCIATION_SHA256",
  "cache_signed_provenance": "AUTHENTICATED_CACHE",
  "cache_supplied_provenance": "CANONICAL_PRODUCER",
  "cache_read_cache_trust_grade": null
}
```

Probe: `probes/test_r08v_r5_independent_boundary.py::test_provenance_mutation_must_not_serve_unsigned_grade`
(assertion fails, recording the defect).

Missing function: sign the execution provenance/mode or a canonical grade
projection in `ExecutedEvidenceEnvelope`, include it in the projection/equality,
and never derive a served trust label from `result.provenance` alone.

## R5-D3-02 — cache export emits unsigned evidence/query/rule objects

Severity: decisive for the "no unsigned metadata or state through export"
obligation.

Location: `export_cache` (~1978):

- It verifies the envelope signature and `_result_matches_envelope(result,
  result.execution_envelope)` (~2000), which covers scalar result fields.
- It then writes `_evidence_material(result.evidence_object)` (~2025),
  `result.consumer_query_object.material()` (~2026) and
  `result.model_rule_object.material()` (~2027) without checking those objects
  against `envelope.evidence_ref`/`evidence_content_hash`,
  `envelope.consumer_query_ref`/`consumer_query_material_hash` or
  `envelope.model_rule_hash`.
- The reader already performs exactly those checks at `~2477` onward.

Independent reproducer:

1. Produce a legitimate positive; keep the returned `EvidenceResult`.
2. In-place mutate the public nested evidence mapping:
   `produced.evidence_object.geometry["cells"][0]["raw_numerator_support"] = 999`.
3. `EvidenceConsumerReader(request, produced, verifier=<same configured>).read()`
   correctly raises `EvidenceAssociationError` (content digest mismatch).
4. `resolver.export_cache()` nevertheless accepts and returns an entry whose
   `evidence` mapping shows 999 under the original signed envelope.
5. A fresh configured resolver refuses that exported cache with
   `EvidenceCacheIntegrityError: envelope/evidence/query/rule association
   mismatch`.

Observed JSON: `outcomes/r5_observations.json` key
`export_mutated_evidence_object`:

```json
{
  "reader_refused_mutated_object": true,
  "export_accepted": true,
  "exported_evidence_raw_support": 999,
  "downstream_import_refused": true,
  "signed_envelope_evidence_hash": "e02259ecaf044e40bb17960455627a8e9ae4e7c7e391fa8509b64ecca5a07d49"
}
```

Probe: `probes/test_r08v_r5_independent_boundary.py::test_export_must_reject_mutated_evidence_object`
(assertion fails, recording the defect).

Missing function: reuse the reader's evidence/query/rule content checks in
`export_cache` and refuse before emitting any entry, or construct the exported
objects only from the signed/retained execution.

## Partial obligation — verifier-only re-export

A verifier-only resolver imports and replays a legitimate authenticated cache
(positive 60, same consumer hash), but `export_cache()` on that imported
resolver raises:

```text
EvidenceCacheIntegrityError: cache entry lacks its admitted owner binding
```

This is not a served-value bypass; the replay itself is correct. It means the
claimed resolver import/export/replay path is incomplete. Observation:
`outcomes/r5_observations.json` key `cold_process_positive` (`reexport`).
A minimal completion would retain imported producer bindings in `_bindings` or
build the export payload from `_binding_materials` plus the signed envelope.

## What did pass

- Independent positive 54/6/60, changed native 54/16/70, cold same-hash replay.
- R4 scalar/value and metadata mutations now raise `EvidenceAssociationError`;
  restored result reads 60.
- Missing live producer pin: substituted callable call count 0,
  `UNKNOWN/OWNER_ADMISSION_UNRESOLVED`; legitimate binding without pin likewise
  refused.
- No-config, wrong-root, attacker-issuer, cache forged-evidence and
  missing-envelope controls refuse.
- Author suite replay: 34 passed, 0 failed/errors/skipped.
- R4 immutable probe replay: 7 passed, 2 failed; both failures are lawful
  `EvidenceAssociationError` refusals, not TypeError/import/setup errors.
