# FIABC-LM2-R1J-C — Conditional R6S Reissue Plan

## Status

`READY_AS_A_CONDITIONAL_PATCH PLAN__DO_NOT APPLY UNTIL R1J-A AND R1J-B ARE ACCEPTED`

No real WVS7 representation authority is issued here and the current R6S materializer is not rewritten from an assumed decoder relation.

## Exact current defect site

Current R6S constructs response-rule physical keys in:

`WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py::_response_value_rules`.

For substantive codes and source-special codes it currently does, in effect:

`native Python int -> classify_physical_value(int, ...) -> physical_value_binding_key(int, ...)`.

R1I proved those int-built keys do not intersect the frozen Q291 float64 physical keys.

The C11 facade itself is correct and remains unchanged.

## Conditional replacement

After HQ accepts both independent fan-in premises and issues the exact bounded representation authority:

1. Package the accepted representation `AuthoritySnapshot` with the R6S authority closure.
2. Require it explicitly in the projection's `required_authority_refs`.
3. Add its immutable ref to the R6S projection authority material and parent/dependency material so projection identity changes honestly.
4. Replace only the substantive/special physical-key preimage construction in `_response_value_rules`:
   - input exact source SHA, variable ordinal/name, native code, and native response state;
   - call `resolve_authorized_physical_binding` with the accepted representation snapshot;
   - use the returned exact `physical_key`;
   - attach the representation authority ref as an extra response-event authority.
5. Preserve layer C independently:
   - substantive 1..5 retain `canonical_value=str(code)`;
   - substantive 1..5 retain R1E `MAPPING_AUTHORITY_REF` as `transform_authority_ref`;
   - specials retain `canonical_value=None`;
   - specials retain `transform_authority_ref=None`.
6. Preserve system missing separately:
   - `physical_value_binding_key(None, SYSTEM_MISSING, None)`;
   - response state `MISSING`;
   - canonical value `None`;
   - no new representation authority.
7. Recompute and reissue only identities whose semantic preimage now contains the representation authority or the newly authorized physical rule keys.
8. Rematerialize candidate-neutral common C11 from the already-frozen structural preimage plus the already-frozen Q291 carrier.
9. Run R15/R16 and freeze a fresh independent oracle.
10. Stop before Candidate A/B/C.

## Required R6S code shape

The lawful successor should conceptually use:

```python
binding = resolve_authorized_physical_binding(
    representation_snapshot,
    source_sha256=SOURCE_SHA256,
    variable_ordinal=variable.ordinal,
    variable_name=variable.name,
    native_code=code,
    native_response_state=response_state,
)
key = binding.physical_key
```

It must **not** use:

```python
if isinstance(raw, float) and raw.is_integer():
    raw = int(raw)
```

or any equivalent generic coercion.

The authorized decoder representation is an explicitly enumerated authority input, not a fact inferred from the observed carrier during C11 projection.

## Exact substantive rule disposition

For each of Q291G5/388 and Q291P5/394, and each native code 1..5:

- physical key: reissued from the exact accepted representation binding;
- response state: `SUBSTANTIVE_RESPONSE`;
- canonical value: unchanged exact string token `"1"`..`"5"`;
- transform authority: unchanged R1E mapping authority `76e63b2af0bf0b9a53319a74d2ded099c9ac175de99935d0741ac52f68086670`;
- extra authorities: source semantics + new representation authority.

## Exact special-state disposition

For each variable:

- -5 -> `MISSING`;
- -4 -> `NOT_ASKED`;
- -2 -> `SOURCE_SPECIFIC_SPECIAL`;
- -1 -> `DK`.

For all four:

- physical key: reissued from the exact accepted representation binding;
- canonical value: `None`;
- R1E transform authority: absent;
- extra authorities: source semantics + new representation authority.

The new authority proves representation only; source semantics still proves the state.

## Projection authority treatment

The existing R6S projection authority may remain a `SOURCE_SEMANTICS_TOPOLOGY` projection authority **only as a consumer/parent of the separate representation authority**. It may not itself be treated as the authority that licenses the physical/native relation.

The new A->B authority must be packaged and independently resolvable by exact ref. The projection material must name that ref, so any downstream projection snapshot/identity truthfully records the new premise.

## Binder changes at adoption

`bind_exact_projection_fields` must gain fail-closed checks that:

- exactly one accepted representation snapshot is packaged;
- its kind is `SOURCE_PHYSICAL_NATIVE_REPRESENTATION_BINDING`;
- its exact source/variable/native-code rows match the fan-in authority;
- every substantive and special response rule carries a physical key obtained under that authority;
- substantive rules still carry exactly the R1E transform authority;
- special rules carry no transform authority;
- system missing does not carry the representation authority.

Existing checks for exact Q291 response slots, Lock2 tie order, raw/unweighted law, and absence of canonical-question substitution remain.

## Files intentionally not changed by Worker C

Worker C does not mutate the live R6S materializer because doing so before A/B acceptance would either hard-code an unproved WVS representation or mint an authority from assumptions.

Prepared production seam:

- `rawlsing_next/pre553_physical_native_representation.py`

Prepared ontology extension:

- `rawlsing_next/pre553_empirical_authority.py`

Prepared hostile court:

- `rawlsing_next/tests/test_fiabc_lm2_r1j_c_representation_authority_prep.py`

This is the minimal architecture delta needed before the exact real authority instance and exact R6S successor can be issued at fan-in.
