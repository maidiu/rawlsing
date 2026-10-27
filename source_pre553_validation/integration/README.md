# R157 P3/P5 integration return

P5 portable delivery lives in `P5_RETURN.json`, `COMMANDS.md`,
`SOURCE_LIBRARY_INDEX.json`, `SOURCE_LIBRARY_INDEX.sqlite`,
`READINESS_MATRIX.json`, `EXCEPTION_AGGREGATE.json` and `DEPENDENCY_LOCK.json`.
It indexes the current accepted sources and does not claim all35 completion
while WVS SRC33-35 remain pending accepted returns. `P5_CASE_DEFECT_WITNESS.json`
preserves the prior wrong-case index witness; `P5_RETURN.json` records the exact-case
repair and the 32/35 result.

# R157 P3 integration return

`P3_RETURN.json` records the shared-seam implementation and actual native
results for:

1. qualified exact-SHA `identity.reader` transport through the existing
   `decode_with_source_read_permission` / physical decoder;
2. exact `row_native_keys` witnesses from a configured source-native key slot,
   with typed unknowns for missing key cells;
3. the R154 loader's prepared-configuration delegation to the existing
   source-backed C11 owner, with separately issued original workloads still a
   separate boundary.

`examples/SRC09_q101_keyed_fixture.config.json` is a P3 integration fixture
config derived from the frozen P0 nonrespondent example. It configures the
country slot as a key witness to exercise repeated-value, row-bound identities.
It is not an original-source config and does not replace lane data.

Reproduce:

```sh
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.tools.build_p3_example
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.tools.publish_p3
```

Scope limits are in `P3_RETURN.json`: no original respondent reads, no issued
original empirical workload, no all35 lane-authoring, and no downstream
FF/M1/N11 scope. Source-lane data directories are untouched.
