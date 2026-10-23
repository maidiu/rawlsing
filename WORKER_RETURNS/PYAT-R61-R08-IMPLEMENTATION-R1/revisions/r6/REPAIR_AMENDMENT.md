# R08 R6 repair amendment — signed provenance/export completeness

Extends R5 under the unchanged R61Q D1-D6 contract. No new trust, science,
authority or service decision.

## Signed execution provenance and local delivery context

`ExecutedEvidenceEnvelope@2` now signs `execution_provenance=CANONICAL_PRODUCER`
and `execution_mode=LIVE_TRUSTED_EXECUTION`. Result projection/equality includes
these fields. Served output reports:

- `original_execution_provenance` / `original_execution_mode` from the signed
  envelope;
- `local_delivery_context_unsigned` as an explicitly unsigned local transport
  label (`LIVE_TRUSTED_EXECUTION` or `VERIFIED_REPLAY`).

No `cache_trust_grade` or served trust grade is derived from unsigned
`EvidenceResult.provenance`. Cache transit therefore never asserts a new original
execution; it only labels local replay.

## Export completeness

`export_cache` validates the retained evidence/query/rule objects against the
signed envelope using the same `_objects_match_envelope` check as the reader. It
refuses before emitting any entry if nested evidence/query/rule content is
mutated. Export writes only the signed result projection plus validated canonical
objects.

Verifier-only resolvers retain imported owner/binding material, so they can
re-export an imported authenticated cache without live producer authority. The
re-exported entry preserves the original envelope/signature and is re-importable
to another verifier-only resolver with the same positive consumer result.

## Preserved

Live producer pin remains mandatory; missing pin is fail-closed before call.
Actual provider/evaluator 54/6/60, changed 54/16/70, observed zero,
ZERO_SUPPORT/UNKNOWN, valid-product states, Z UNRESOLVED16, currentness and
typed identities remain. Cache/result/envelope versions advance (`@4`, `@4`,
`@2`) so legacy records refuse. No J42/P41/E04 integration claim.
