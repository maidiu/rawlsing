# ROADMAP CLAIM vs CODE — S09 dated claims at protected 6a

**Source:** `PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/09_N9_WORLD.md` at `6a5c12f04323d74001f9632063ec907f4fc4468e`, blob `67ee4fd085f670e8e03978a0bf8006457e4ad1e4`. **Method:** full read; dated claims treated as candidate claims, not law; verified against actual protected code.

| Dated S09 claim | Exact code at 6a | Verified meaning |
|---|---|---|
| POST-CAS3: “L01 reviewed R08 signed evidence and R118 actual per-prefix sourcefree world service now protected via #702” | `pre553_evidence_world_consumer.py` L66 adapter and `pre553_world_conditioned_progressive_service.py` L110 exist; `configure_progressive_world_context` L1117 and `progressive_world_view` L1337 exist | **Protected sourcefree code present**; not a selected/native N9 first reader |
| POST-CAS3: “old P41 historical Git-object executable dependency is removed at sourcefree scope” | `_pinned_p41_runtime` L38-41 returns local `rawlsing_next/sourcefree_world` package; docstring “historical pin is provenance only”; `_execute_p41_world` L701-702 imports local `P41Service`/`SelectedWorldCatalog`; `_purge_p41_modules` L56 has no caller | **Local-runtime replacement confirmed**; `P41_COMMIT`/`P41_PACKET` remain provenance constants, not execution |
| Earlier R2 note: “R118 reviewed per-prefix world consuming successor is branch-only, not current protected N9; R08 exact evidence binder is not statically imported by this P41 execution path” | At 6a, the R08 adapter exists and `configure_progressive_world_context` lazily imports `read_prefix_evidence` inside `_progressive_step` L1181; there is no external non-test entrypoint | **Source presence supersedes the stale branch-only wording**; production adoption still not proved |
| S09.1/S09.3/S09.4: `MISSING_PRODUCER_OR_READER`; native actual N9 held | `SelectedWorldCatalog` publishes modeled E04 fields with `MODELED_NOT_OBSERVED`; `empirical_identity()` hardcodes `SYNTHETIC_NOT_OBSERVED`; no external non-test entrypoint; `actor_state=NOT_TOUCHED` | **Consistent with code** |
| S09.1: “No general original35 N9 world receiver or native source issuance verified” | No real structural field producer; world fields fixed BASE values; fixture uses `L01_SYNTHETIC`/`L01_TEST_ROWS` | **Verified as NOT_PROVED** |

## Dated-grade conclusion

- `SOURCE_PRESENT`: yes, protected sourcefree adapter and world view exist.
- `SELECTED_SOURCE_NATIVE`: no; modeled synthetic fields.
- `CURRENT_FIRST_CONSUMER`: no; direct callers are tests.
- `NATIVE_ORIGINAL35`: no; not claimed.

The roadmap’s “protected” and “missing producer/reader” statements are compatible only when “protected” means **protected test-only sourcefree code**, not an operative selected N9 world.
