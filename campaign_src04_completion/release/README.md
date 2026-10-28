# SRC04 full completion — lane A

This lane implements the full SRC04 source-native C11 construction path, now
with the fixed lane-B observed-domain binding wired in. The initial target is
**163 already-qualified response fields plus two coordinates** (1,195,931 response
positions); after the pinned B v2 static repairs and stream-safe income-domain
builder, the target is **178 responses + 3 coordinates where source-qualified**,
not an arbitrary 163 cap. All 181 physical slots, the exact 15 held responses and
the exact held q701 coordinate remain accounted; q217 remains precise and
unresolved if the source facts are insufficient.

## Current status

A fresh full-source read/C11 grant is **PENDING**. No original SAV stat, hash,
open, or decode occurs in this checkout. The runner therefore returns:

`BLOCKED_MISSING_FULL_SOURCE_GRANT__CODE_READY`

The existing accepted 42-field product and D1 tally remain untouched.

## Grant requirements

The runner accepts only an exact full-source grant document with:

- schema `PYAT_FULL_SOURCE_READ_GRANT@1.0.0`
- `source_id: SRC04`
- source SHA `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`
- 7,337 rows, 181 columns, 1,531,099 bytes
- host `USER_LOCAL_MAC`
- purpose `FULL_SRC04_ORIGINAL_C11_CONSTRUCTION`
- consumer `EXISTING_PRE553_SOURCE_BACKED_C11`
- full scope `ALL_181_PHYSICAL_SLOTS__ALL_QUALIFIED_RESPONSE_FIELDS`
- `full_source: true`, `first_slice_only: false`, currentness/revocation fields
- exact file SHA-256 supplied separately

The fixed B join uses the read-only pinned inputs:

- B candidate commit `da23c65d1e211cb7e8ce416e98757f321b78d25e`
- config `rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json`
- config file SHA `5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5`
- builder `campaign_src04_completion.bindings.numeric_domain_binding.build_numeric_domain_runtime_config`

The builder is invoked only after the decoder admission has returned an admitted
transport and before all-slot selection. It consumes the admitted transport
without opening the source again, applies the exact observed income-domain
rules for `q715withoutmorocco` and `q716withoutmorocco`, and preserves source
country/currency literals and `ROUTING_UNKNOWN`.

Absent, first-slice, foreign-source, and foreign-purpose grants are refused before
any source I/O. The first-slice A grant is not expanded.

## Commands

```sh
# Source-free blocker/scope and grant negatives
PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode prepare

# Focused tests (includes a fixture-only 163+2 factory smoke)
PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode tests

# Replay blocker until a full local release exists
PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode replay

# After an exact full grant is supplied
PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode primary \
  --grant campaign_src04_completion/release/evidence/FULL_SOURCE_GRANT.json \
  --grant-sha256 <exact-grant-sha256>

# Pinned B v2 repaired input; 178 + 3 only where source-qualified
PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode primary \
  --grant campaign_src04_completion/release/evidence/FULL_SOURCE_GRANT.json \
  --grant-sha256 <exact-grant-sha256> \
  --repaired-config rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json \
  --repaired-config-sha256 5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5
```

The full-source read is **not** performed by these current commands because the
grant is absent. The prior 42-field and D1 local products are read-only inputs,
not edited.
