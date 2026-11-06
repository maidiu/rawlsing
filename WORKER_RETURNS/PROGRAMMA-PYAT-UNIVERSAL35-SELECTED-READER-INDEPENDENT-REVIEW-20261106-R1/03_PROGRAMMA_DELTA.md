# PROGRAMMA_DELTA — selected-reader independent review r1

| Field | Delta |
|---|---|
| `VERDICT` | **REVISE** at target `89a41589c7541f625c6d2f9346436629d374b93e`; implementation `fd18faf0340f9d3751ffd9042799a0b7d58519bb`; prior wrapper `be7e831f41e1c699890b7987cd2fea25be3f65d3`; published review head reported in final delivery. |
| `IDENTITY` | Independent nonauthor S2 physical-reader review. No product, test, guide, progress, controller, or protected edit. |
| `FUNCTION` | Verify selected physical-cell projection over the existing content-bound snapshot and current NativePackage/factory consumers, with exact row/column identity and typed refusal behavior. |
| `INPUT_TRANSFORM_TYPED_OUTPUT` | SAV selected path: `PhysicalSourceIncidence` + unique selection -> exact selected cells, full global rows/ordinals, source SHA, metadata digest, replay. DTA selected path currently fails at `read_file_in_chunks(read_dta, /dev/fd/...)`; zero-row frame fallback raises `UnboundLocalError`. |
| `ROOT` | Runtime root supplied only by the local read-only binding alias; no root in review return or module. |
| `SCHEMA` | Existing `ExactPhysicalCellStream`, `STREAM_TRANSPORT = BOUNDED_REPLAYABLE_ORIGINAL35_PHYSICAL_SOURCE_INCIDENCE@1`; no new semantic schema, authority, compiler, or source-ID branch. |
| `CLOCK` | Local macOS/x86_64, Python 3.11.3, pyreadstat 1.3.2; co-tenant measurements. |
| `PERMISSION` | Scoped engineering physical review only; no native/science/actor grant or source-publication right. Source-read admission tests pass, including revocation refusal. |
| `ACTUAL_FIRST_CONSUMER` | SRC31 NativePackage release/replay/semantic-hash/public-object parity PASS. Fixture C11 factory full-grid parity PASS. D `execute_native_compiler_source` end-to-end and genuine C11/native release remain NOT_RUN. |
| `EVIDENCE` | Adapter 5 PASS; focused 35 PASS. SRC31 574,056 all cells -> 33,768 selected, exact digest `2461996e…`, 2.36 s -> 0.173 s; release `73700af5…`, replay `b7f2736d…`, 59,102 objects equal. SRC09 selected 41,334, digest `1d23d781…`, 0.404 s. DTA selected probe failed before any cell; zero-row frame probe failed with `UnboundLocalError`. |
| `PRESERVED_NEGATIVE` | Old 226 MB tuple-versus-101 MB wrapper comparison remains diagnostic only, not the D baseline. The corrected claim is filter-every-cell versus actual column pushdown. |
| `AFFECTED_EXISTING_IDS` | `S03.2/S-C11` physical realization input; D selected native compiler input; original35 DTA paths SRC27–SRC30. No semantic output change. |
| `CONDITIONAL_UNLOCKS` | After DTA selected support/typed refusal and zero-row guard are repaired and tested, SAV evidence can support D integration. Full C11 remains A-owned; D end-to-end remains D-owned. |
| `NEXT_ACTION` | Author repairs the DTA snapshot/read route or explicitly refuses DTA while preserving full-grid behavior, guards empty frames, adds regression tests, and resubmits. Reviewer does not repair product or mint authority. |
