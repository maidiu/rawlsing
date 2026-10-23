# R61-R08V R7 independent review — defects

## R7-AF-01 — legacy binding-pin cache replay loses the explicit migration code

Severity: bounded contract/refusal-code defect; no support, measurement,
ownership, admission or root bypass.

Location: `rawlsing_next/pre553_universal_evidence_binding.py`,
`EvidenceResolver._replay_cache`.

- `_check_cache_configuration()` correctly raises
  `EvidenceCacheIntegrityError("LEGACY_BINDING_PINS_REQUIRE_MIGRATION")` when
  `trusted_binding_hashes` is nonempty.
- `_replay_cache` wraps that check in
  `except (Pre553IntegrityError, KeyError, TypeError, ValueError)` and returns
  `_result_refusal(request, REFUSAL_STALE_CACHE)`.
- Import/export preserve the explicit code; a `resolve` cache hit does not.

Reproducer
(`probes/test_r08v_r7_independent_boundary.py::test_legacy_binding_pin_cache_replay_has_explicit_migration_code`):

```python
resolver = _resolver(trusted_binding_hashes=("a" * 64,))
resolver.bind(binding)
first = resolver.resolve(request)   # SUPPORTED 60 (live, not a cache op)
second = resolver.resolve(request)  # cache hit
# observed:  UNKNOWN / STALE_OR_UNAUTHENTICATED_CACHE
# expected:  UNKNOWN / LEGACY_BINDING_PINS_REQUIRE_MIGRATION
```

Observed JSON (`outcomes/r7_observations.json` key
`legacy_pin_cache_replay`):

```json
{
  "first_state": "SUPPORTED",
  "second_state": "UNKNOWN",
  "second_typed_refusal": "STALE_OR_UNAUTHENTICATED_CACHE",
  "expected": "LEGACY_BINDING_PINS_REQUIRE_MIGRATION"
}
```

The cache replay refuses before serving anything; the defect is the lost
explicit migration/configuration limit on the primary resolve path, contrary to
R61AF's "explicit typed migration/configuration limit" and the frozen R7
contract's named `LEGACY_BINDING_PINS_REQUIRE_MIGRATION` refusal.

### Minimal missing function

In `_replay_cache`, preserve the explicit
`LEGACY_BINDING_PINS_REQUIRE_MIGRATION` refusal instead of collapsing it to
`STALE_OR_UNAUTHENTICATED_CACHE`. A consistent explicit
`CACHE_OWNER_DESCRIPTOR_NOT_PINNED` replay code for the distinct descriptor-pin
configuration is desirable but the contract only requires enforcement there
(it is enforced, with no support served). Add a resolve-path assertion for the
configured legacy pin.

## What passed

- R61AF normal form: cache @5, descriptor @1 six fields, all 13 owner classes,
  descriptor hash distinct from live binding hash, no admission/duplicate
  producer transport.
- Independent 13-class public mutation/removal/duplicate/type-alias inventory
  with recomputed descriptor/entry seals: import/read/re-export/second import
  refused; pristine baseline restored 60.
- Trusted synthetic signed owner-envelope disagreements for all 13 classes
  refused by reader and cache import.
- Unknown/admission fields at descriptor/owner/entry/envelope refused; legacy
  @4/@3 schemas and old envelopes refused; descriptor pins enforced.
- Independent positive 54/6/60, changed 54/16/70, observed zero 60/no=0,
  ZERO_SUPPORT 0, typed bool/int/null, currentness, Z UNRESOLVED16.
- Missing live producer pin call count 0; verifier-only replay/re-export never
  invokes a producer; cold process 60 with separate stdin key; original
  envelope signature/provenance preserved; no unsigned local delivery label.
- Fixtures/harness bytes independently verified against startup/original blobs;
  harness only redirects fixture paths.
- Author 126/126. Independent R7 probes 75/76 (this defect is the one failure).
  R6 immutable 9 pass/2 removed-transport/local-label superseded; adapters 3/3.
  R5 6/2 superseded old grade/import expectations; R4 7/2 lawful
  `EvidenceAssociationError`.
