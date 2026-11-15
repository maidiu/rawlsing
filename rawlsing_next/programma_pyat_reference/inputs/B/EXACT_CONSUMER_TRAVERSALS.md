# EXACT_CONSUMER_TRAVERSALS — forward and reverse

**Method:** source/import graph and direct source reads at PRE-MAIN
`9809203fd915a84bae056a67210e9213879840db`; selected sourcefree tests only.
Arrows are observed import/call relations unless marked `MISSING`. No native
source run, N11/N12 issuance or production deployment is claimed.

## T1 — Physical source → C11 → Route B → I03/I05 → Batch → first consumer

**Forward (observed):**

`pre553_physical_decoder.decode_sav/decode_dta`
(blob `4b89c459...`) → `pre553_source_backed_c11_facade.build_validated_source_backed_c11_release`
(blob `8a761119...`, calls `validate_c11_source_release` line 603) →
`pre553_route_b_production.execute_route_b_production`
(blob `2385cd32...`) → `pre553_issued_workload.execute_issued_workload`
(call line 300) → `pre553_batch_runner.BatchExecutionRunner`
(line 331) → `pre553_empirical_query.execute_empirical_query` / `pre553_discovery_exact.execute_exact_bounded_discovery`
through the carrier/query path.

**Reverse (observed):**

`BatchExecutionRunner` → `pre553_issued_workload` → `execute_route_b_production`
→ C11 façade → C11 ingest validator → physical decoder. This is the strongest
current sourcefree producer/consumer chain in the inspected estate.

**First real consumer:** `pre553_issued_workload.execute_issued_workload` is the
first current non-test caller of Route B at this cut. It is a sourcefree transport
owner, not a deployed Pyat application.

**Missing / not proved:**
- real original35 source pack and source-use authority;
- actual measured C11 release from original source bytes;
- production application consumer and persistent native custody;
- F1/F2/F3/F4 positive measurements, rather than sourcefree fixtures.

**C3 review:** `E4FR@7cd2206` accepted the exact C3 sourcefree repair; PR #602
merged `0075c15...`; 45 PASS and selected 194 PASS/1 SKIP. This does **not** prove
the full chain above on original source.

## T2 — C11 → I03/I05 → analytical composition → N10E → progressive candidate

**Forward (observed):**

`pre553_c11_ingest.validate_c11_source_release` →
`pre553_empirical_query.execute_empirical_query` (called by façade line 659;
analytical composition lines 1038/1074) →
`pre553_analytical_composition.compose_positioned_subject_possibility`
(blob `604c8d59...`) →
`pre553_empirical_possibility_provider.provide_empirical_possibility_slice`
(blob `23167aa2...`, call at line 574) →
`pre553_n9_n10w_progressive_candidate.run_single_conditioner_step`
(line 327) → `consume_step_with_f8` / `run_progressive_chain`.

**Reverse (observed):**

`run_progressive_chain` → provider receipt → analytical composition → exact I03
query → C11 release. The reverse path keeps exact producer/consumer refs and
does not create a new semantic layer.

**First real consumer:** the progressive candidate at
`pre553_n9_n10w_progressive_candidate.py` is the first consumer of N10E, but that
module is imported only by its test file. It explicitly says N9 and N10W are not
implemented anywhere in the repository.

**Missing / not proved:**
- actual selected original measured world;
- G0b N10E model/use authority;
- N9 whole-world snapshot and N10W world-conditioned service;
- production consumer and human/actor use.

**Coverage:** N10E provider 43 tests PASS; progressive candidate 18 PASS;
analytical composition 13 PASS; output is sourcefree/candidate only.

## T3 — Empirical joint fact → Field Forge → GT12 bridge → M1/M2 → M4/M5 objective publication

**Forward (observed source identities):**

`pre553_empirical_query` / I03 joint fact → `field_forge_conditional_support.produce_exact_conditional_support_profile`
(blob `a70decb2...`) → `gt12_c_to_d_relation_bridge.bridge_gt12_c_relation_to_d_evidence`
(line 93) → `m1_admitted_field_forge_relation_v554_ingress.evaluate_m1_admitted_field_forge_relation_v554`
(blob `0aeacd9e...`) → `gt12_d_to_m4_typed_bridge.admit_gt12_c_relation`
(line 131) → `m4_m1_evaluation_binding` / `m4_v557_v558_publication_repository`
→ `m5_runtime_rsc_peer_prior` / objective publication adapters.

**Reverse (observed):**

From M4/M5 objective publication, the reverse path reaches M1/M2/M3/M4 records,
then GT12 D→C bridge, then Field Forge relation. The M1/M2/M3/M4 modules do have
sourcefree importers beyond tests (M4→M5/objective adapters), but the Field
Forge → GT12 → M1 ingress segment is test/bridge-only.

**First real consumer:** `gt12_c_to_d_relation_bridge` is the first module that
consumes Field Forge output; it is imported only by
`tests/test_gt12_e2b_actual_object_consumer_harness.py`. `gt12_d_to_m4_typed_bridge`
is imported only by tests. Therefore the Field Forge structural path has
**NO_PRODUCTION_CALLER_PROVED**.

**Missing / not proved:**
- actual structural target-use authority;
- production M4/M5 consumer of a Field Forge relation;
- real I03 joint fact from original source;
- F5 positive admitted structure rather than a test/bridge fixture.

## T4 — F6/F7/N9/N10W/N11/N12: guard and dossier path

**Forward (observed):**

`pre553_source_relations.SourceRelationResolver` / composite guards
(blob `5b67e3f9...`) → only `tests/test_pre553_source_relations.py` at PRE-MAIN.
`pre553_learned_product_lifecycle.resolve_current_as_of` (blob `dadf2362...`)
provides as-of current selection for learned products; `m1_temporal_v554_admission_dedup`
gates temporal/signature completeness. Neither is a comparable-wave empirical
producer. N11/N12 are `nodes/N11.md` / `nodes/N12.md` dossiers marked
`PROPOSED_NOT_COMMISSIONED`.

**Reverse (observed):**

From `nodes/N12.md`, the reverse chain requires `N11`, which requires `N0` and
`N10W`; `N10W` requires `N9` + `N10E`; `N9` requires actual world content. The
reverse chain stops at missing N9/N10W and missing N8E/N8S producers. F6 stops at
the test-only source-relation guard. F7 stops at temporal gating/currentness
pieces.

**First real consumer:** none for F6; none for F7; none for N9/N10W/N11/N12.
The only consumers are tests/dossiers.

**Missing / not proved:**
- two eligible independent field contributions and a composed-world consumer
  (F6);
- N8E comparable-wave producer, N8S structural temporal pressure and comparison
  authority (F7);
- N9 whole-world snapshot, N10W progressive world-conditioned service, N11
  joined acceptance, N12 explicit wake/defer decision;
- original source authority, real products and human/product evaluation.

## Cross-traversal conclusion

The strongest current state is a **sourcefree engineering chain**:
physical decoder → C11 → I03/I05 → Route B/Batch, with 526 targeted tests passing.
The strongest recent unintegrated additions are R157 configuration preparation
(119 paths, 0 current) and the PROGRAMMA P1 original35 constructor (18 + 16
author tests, absent from PRE-MAIN). The largest present gap is not missing
generic code: it is the absence of a real source pack, production consumer and
F5–F8/N9–N12 world realization. This return does not claim that any missing edge
is complete.
