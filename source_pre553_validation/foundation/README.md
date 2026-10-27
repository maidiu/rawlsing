# R157 P0 foundation return

This directory is the lane-ready P0 interface. It is finite and deliberately
does not implement all35 source configurations.

## Frozen files

- `P0_RETURN.json` — callable/schema paths, immutable evidence refs, lane
  inputs/write paths, actual validation results and the exact remaining P3
  factory/reader task.
- `FIXTURE_SPEC.json` — clearly nonrespondent fixture identity, provenance,
  shape coverage, exact cells and expected results.
- `VALIDATION_RESULTS.json` — actual schema, projection, native release and
  coverage results.
- `examples/SRC09_q101_fixture.config.json` — validated serialized example.
- `fixtures/SRC09_q101_nonrespondent.json` — distinct fixture byte identity;
  no original respondents.

## Reproduce

```sh
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py -q -o addopts=''
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.tools.publish_p0
```

The example is a P0 fixture example, not a lane configuration. Complete SRC09
coverage and original-source authority belong to the ASIAN lane. Original-source
execution was not performed.

## Lane consumption

Every lane starts at this P0 commit, reads its source IDs from
`rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json`, and uses the
frozen schema/validator/factory paths in `P0_RETURN.json`. Lane writes are only
the `rawlsing_next/source_configuration/data/SRCxx/` and
`source_pre553_validation/SRCxx/` paths named by `LANES.json`.
