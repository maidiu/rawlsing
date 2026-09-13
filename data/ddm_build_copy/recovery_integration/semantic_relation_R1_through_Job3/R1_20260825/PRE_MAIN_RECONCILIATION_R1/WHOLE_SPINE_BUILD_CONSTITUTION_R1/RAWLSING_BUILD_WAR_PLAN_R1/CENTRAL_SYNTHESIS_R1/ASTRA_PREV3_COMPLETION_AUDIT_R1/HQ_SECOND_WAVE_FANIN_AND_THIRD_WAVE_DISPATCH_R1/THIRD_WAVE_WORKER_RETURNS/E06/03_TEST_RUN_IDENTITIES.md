# E06 Exact Test / Run Identities

Grain: `PREV3_M3_FIREWALL_INDEPENDENT_HOSTILE_QUALIFICATION_R1_ONLY`

## Authority and implementation identities

- E06 exact branch: `agent/rabochii-prev3-w3-e06-m3-hostile-qualification-r1`
- E06 commission tip: `c09ef40bca2efd1b3e20ee751b00ece8453db2c0`
- D06 implementation branch: `agent/rabochii-prev3-w2-d06-m3-firewall-implementation-r1`
- D06 implementation commit: `44fb4b2c6b75425fc4893739a6bf4362d2c0350b`
- D06 return-seal commit: `f16d4efbf7660fbcfb82f2fa168bb55a9fea5b84`
- `rawlsing_next/m3_v556_higher_order_structural.py`: `9a4b26b214686364a43d108dabf0d57dac0ed3b2`
- `rawlsing_next/tests/test_m3_v556_higher_order_structural.py`: `0276bd18282216853ba1f92e558db767d8c1f9ec`
- `rawlsing_next/tests/test_pre553_source_relations.py`: `2487ed757c0254e7227cf43664abc6ae08f1dfb3`
- `rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py`: `e6a456865470fe587aae9480a81eb2ccbc8b7b51`
- `rawlsing_next/tests/pre553_reservoir_harness.py`: `c2c9752d745b06fa34c4e1c3345d90de7e66feea`

All five file identities above were hash-verified in the qualifying clean run before tests executed.

## Qualifying clean run

- GitHub Actions workflow run: `34774346186`
- job: `103769578263`
- tested head: `15c20a5b8c0c26eb69e3e9ed15fc4c579e03399a`
- conclusion: `success`
- runner: Ubuntu 24.04, Python 3.12.14

Exact observed courts:

1. Frozen M3 H01-H12 reproduction:
   - command: `python -m pytest -q -p no:cacheprovider rawlsing_next/tests/test_m3_v556_higher_order_structural.py`
   - result: `29 passed in 0.11s`
2. Independent E06 probe:
   - artifact: `02_INDEPENDENT_QUALIFICATION_PROBE.py`
   - result: `13/13 PASS`
3. Targeted M3 and guard regression court:
   - files: frozen M3 test, M2 atomic route, PRE553 source-relations guard, M1 ingress guard, M4 typed bridge
   - result: `145 passed in 0.57s`
4. Full relevant PRE-V3 regression court:
   - selected files: `35`
   - result: `714 passed, 1 skipped, 2 deselected in 11.13s`
   - deselected exact tests:
     - `rawlsing_next/tests/test_pre553_reservoir_preintegration.py::test_downstream_m1_m6_render_and_psepf_bytes_match_frozen_base_git_blobs`
     - `rawlsing_next/tests/test_pre553_whole_machine_hostile_acceptance.py::test_r15_h15_frozen_semantic_blobs_are_byte_exact`

The transient workflow removed itself after the successful court and pushed commit `fb6a5df2a` (`E06: remove transient M3 qualification workflow`), leaving no persistent CI workflow change.

## Non-qualifying setup attempt

For completeness, run `34774247793`, job `103769308564`, ended `failure` after the frozen M3 court had already produced `29 passed`. The failure was solely in E06's newly authored evidence harness import path (`ModuleNotFoundError: rawlsing_next`); it occurred before the independent probes or regression courts and did not identify a product/runtime failure. The runner invocation was corrected by supplying repo-root `PYTHONPATH`; no production code was changed. The subsequent clean run `34774346186` is the governing qualification run.

## Historical D06 run identities inherited from commission

- D06 targeted regression run: `34715577734`, job `103612094411`, `145 passed`.
- D06 full relevant regression run: `34768148484`, job `103752736322`, `714 passed`.

E06 independently reproduced the corresponding targeted and full counts on the frozen implementation identity above.
