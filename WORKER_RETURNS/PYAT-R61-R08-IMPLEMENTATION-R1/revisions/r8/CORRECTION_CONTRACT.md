# R08 R8 bounded correction contract

Authority: commission `622ae1c76f9b14936df78917a70d8d13e7374862`; R61AF
`e349da0d886d8e365648afccf40a2e6b8e105ff7`; R7 review
`fc4597fb8398b8012367d8d9d1fa36502b3d798e`; startup
`ea39bd324d297a93bb9e87ede9b9da75dfa8750a`.

## Single missing function

`EvidenceResolver._replay_cache` must preserve the explicit cache-configuration
refusal code raised by `_check_cache_configuration` / `_check_descriptor_pin`
instead of collapsing it to `STALE_OR_UNAUTHENTICATED_CACHE`:

- nonempty legacy `trusted_binding_hashes` on a primary resolve cache hit ->
  typed `UNKNOWN` / `LEGACY_BINDING_PINS_REQUIRE_MIGRATION`;
- wrong/missing `trusted_descriptor_hashes` on a cache hit ->
  typed `UNKNOWN` / `CACHE_OWNER_DESCRIPTOR_NOT_PINNED` (existing enforcement,
  now explicit on the resolve path);
- missing verifier -> `NO_CONFIGURED_TRUST_ROOT` preserved;
- genuine stale/unauthoritative cache state still uses
  `STALE_OR_UNAUTHENTICATED_CACHE`.

No schema, security, ownership, envelope, positive-path or native-owner change.
Import/export explicit limits remain. No new names/refactor beyond preserving
the existing typed code.

## Qualification

- live first resolve remains SUPPORTED 54/6/60, cache hit returns the exact
  configured refusal code;
- descriptor pins remain enforced with explicit replay code and no support;
- native positive/changed, descriptor-owner inventory, verifier-only replay and
  cold positives remain unchanged;
- same-consumer fault/restore and exact exit/JUnit evidence recorded;
- full J42/P41/E04 remains NOT_REACHED; no self-adoption.
