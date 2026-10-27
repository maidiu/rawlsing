# R157 source-configuration foundation

This package is the frozen P0 interface for the bounded R157 task. It maps a
validated, serialized source configuration onto the **existing**
`GovernedC11Projection` / source-backed C11 owner. It is not a replacement
engine and it does not infer missing source semantics.

## Frozen callables

```python
from rawlsing_next.source_configuration.schema import load_source_config, validate_source_config
from rawlsing_next.source_configuration.factory import (
    build_governed_c11_projection,
    build_validated_c11_release_from_config,
    build_source_backed_c11_repository_from_config,
)
from rawlsing_next.source_configuration.fixture import load_fixture_stream
```

- `validate_source_config(document)` — closed validator; raises
  `SourceConfigurationSchemaError`.
- `load_source_config(path)` — load JSON and validate.
- `build_governed_c11_projection(config, *, source_sha256=None, row_count=None)`
  — construct the actual `GovernedC11Projection`. The optional SHA/row count
  repeat the active binding after a permitted decode and must match it.
- `build_validated_c11_release_from_config(config, *, stream=None, incidence=None)`
  — call the existing source-backed C11 validator.
- `build_source_backed_c11_repository_from_config(config, source)` — call the
  existing repository/facade owner.
- `load_fixture_stream(path)` — load an explicitly nonrespondent fixture.
- `row_native_keys_from_transport(config, stream=...|incidence=...)` — extract
  exact per-row key witnesses from a configured key slot; missing key cells stay
  `TypedAbsence(UNKNOWN)`. The release/repository wrappers auto-populate this.
- `source_read_request_from_config(config, ...)` and
  `reader_configuration_from_config(config)` — carry the exact qualified
  `identity.reader` facts into the existing source-read admission owner.
- `decode_config_with_source_read_permission(config, ...)` — use the existing
  zero-I/O-before-current-permission admission path with the configured reader.

## Evidence

`evidence/` is the portable, read-only common evidence package:

- `SOURCE_ROSTER.json` — 35 source identities, counts, lane assignment,
  metadata witnesses and qualified reader facts.
- `PHYSICAL_SLOTS.jsonl.gz` — 18,413 current physical slots.
- `CODEBOOK_ROWS.jsonl.gz` — 18,276 current codebook rows.
- `ITEM_EVIDENCE.jsonl.gz` — 18,276 original items joined to the full H48
  index, P2 row and exact full-relation row (18,250 exact joins; 26 explicit
  unmatched IDs preserved).
- `UNMATCHED_RELATIONS.json` — the 26 exact unmatched implementation IDs.
- `EVIDENCE_MANIFEST.json` — pinned Git/P2 refs, hashes, bytes and counts.

`evidence.py` provides read-only accessors and `verify_evidence_manifest()`.

## Nonnegotiable distinction

- An `ORIGINAL_SOURCE` config keeps the original source SHA and may not carry a
  fixture SHA, fixture universe, fixture authority or `TEST_ONLY` universe.
- A `NONRESPONDENT_FIXTURE` config binds a distinct fixture byte identity and
  requires fixture-only authority snapshots. It does not establish original
  source authority.
- The factory creates respondent/value witnesses only when a permitted physical
  stream is projected. It does not pre-invent respondent rows.
- Original-source execution remains a separate permission/issuance boundary.

## Commands

```sh
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py -q -o addopts=''
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.tools.build_evidence --help
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.tools.publish_p0
```

The remaining P3 seam is the qualified reader-configuration transport through
the existing source-read/decoder owner; the P0 constructor signature is frozen.
