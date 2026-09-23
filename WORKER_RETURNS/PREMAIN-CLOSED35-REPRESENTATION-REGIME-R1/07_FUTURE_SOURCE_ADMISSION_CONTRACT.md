# Future Source Admission Contract

Schema intent: `PREMAIN_CLOSED35_FUTURE_SOURCE_ADMISSION_CONTRACT@1.0.0`.

A source 36+ may terminate only as:

- `EXACT_EXISTING_REGIME_APPLIES`, or
- `NEW_REPRESENTATION_LAW_REQUIRED`.

There is no "close enough" state.

## Mandatory evidence

Before an existing regime may be applied, bind all of:

1. exact source SHA-256 and byte size;
2. source format and exact decoder;
3. decoder/library versions and reader configuration, including encoding;
4. exact variable/storage locator for every governed surface;
5. exact Python physical type before normalization;
6. exact physical missing state;
7. exact source-missing declaration;
8. exact R5 typed token;
9. exact physical binding key;
10. exact governed rule key or explicit bounded representation authority;
11. exact join/bridge witness;
12. provenance of every historical/current key- or hash-producing dependency.

## Decision law

For each governed surface:

- direct exact key match under one proven regime -> `EXACT_TYPED_JOIN_PASS`;
- exact enumerated bounded authority applies -> `EXACT_BOUNDED_BRIDGE_PASS`;
- repeated physical pattern lacks authorized key law -> `GENERIC_LAW_GAP`;
- exact source locator/carrier defect prevents application -> `SOURCE_SPECIFIC_REPRESENTATION_GAP`;
- exact rule/value-key authority is absent -> `AUTHORITY_BLOCKED`.

A new source is `EXACT_EXISTING_REGIME_APPLIES` only when all governed surfaces terminate in an admitted pass state and all required generic physical carriers are implemented.

Otherwise it is `NEW_REPRESENTATION_LAW_REQUIRED`.

## Noncoercion

The admission contract explicitly forbids:

- int/float equality as physical identity;
- float/Decimal equality as physical identity;
- Decimal exponent normalization as physical identity;
- label or display-text equivalence as value-key authority;
- cross-wave authority inheritance from family membership;
- historical/current hash or key equivalence without a shared canonical domain.

## Historical replay

Dynamic loading of an old file is insufficient. Historical replay must prove one of:

- hermetic pinned transitive dependencies;
- explicit current successor dependency;
- byte-identical ambient dependency, with byte identity proved;
- otherwise fail as `ACCIDENTAL_CURRENT_DEPENDENCY_LEAK`.

## Acquisition provenance

Transport archives are not representation identity. When explicitly authorized, already-materialized payloads may be measured only if each payload independently matches the canonical source registry by filename, exact byte size, and SHA-256. The acquisition method must be recorded, and source substitution remains forbidden.
