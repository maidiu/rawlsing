# UNIVERSAL35 C — measured selected-reader projection, r2

**R3 STATUS:** Genuine SRC27–SRC30 DTA physical execution evidence is in `05_R3_ORIGINAL_DTA_EXECUTION.md`. All four projected reads executed. SRC27/SRC30 full-cell baselines completed with exact selected digest/source/metadata parity; SRC28/SRC29 full-frame baselines failed closed on unselected string decoding (SRC28 `ReadstatError` invalid byte sequence, SRC29 UTF-8 byte 0xb5), while projected selected reads succeeded. Code stays `7a404b0d…`; no new kernel.

**R2 STATUS:** Independent review `20dee349…` returned REVISE on DTA snapshot chunking and zero-row frame handling. The bounded repair is code `7a404b0dcaac0e4dd027b9edb98c9038d89dbd9a`; see `04_R2_DTA_AND_EMPTY_FRAME_REPAIR.md`.

**FINDING:** The current D-style filtered generator is not eager tuple materialization, but it still creates every physical cell before filtering. On genuine SRC09 with D's `max_items=1` selection, it created **5,972,763** cells to yield **41,334** selected cells and took **46.4–47.6 s per pass**. The smallest generic column-projected path in this module used the existing content-bound snapshot plus reader `usecols`/chunking, created only the **41,334** selected cells, and took **0.44–0.53 s per pass**. Selected-cell sequence equality and SHA-256 digest were exact (`1d23d781…`), and native-package release ref, replay ref, semantic release hash and public-object count matched.

**INTERPRETATION:** Column pushdown fixes the measured physical selected-input bottleneck, not the whole native pipeline. The native-package probe itself still took ~42–47 s on SRC09 for 62,009 public objects; therefore this return does **not** claim to explain or fix D's published 600 s end-to-end native attempt result. The earlier 226 MB tuple-versus-101 MB stream comparison is retained only as an eager diagnostic, not as the current D first-consumer baseline. Latin1 compatibility sources are already full-frame decoded before this helper; projection cannot erase that frame memory.

**ACTION:** HQ can route the frozen producer to D. D should use `bounded_physical_cell_stream(incidence, include_variables=selected_response_plus_coordinate_names)` in place of its current filter-every-cell closure. Full-grid `include_variables=None` remains the current factory path. Genuine C11 release still fails at A-owned unbound source/config values; no value inference is made.

**OWNER:** HQ plus distinct nonauthor reviewer for this adapter; A/B source-pack owner for unbound mapping/value binding; D for native pipeline lowering and the remaining 600 s end-to-end behavior; source/science owners for native use; protected integrator for CAS.

## Exact source identity

- Branch: `codex/pyat-universal35-physical-stream-20261106-r1`
- Base: `d129eebdb0472b0c3625efa281826a858bd0a384`
- Implementation commit: `7a404b0dcaac0e4dd027b9edb98c9038d89dbd9a` (r2; prior r1 `fd18faf0…`)
- Production file: `rawlsing_next/pre553_original35_physical_stream.py`
- Matching test: `rawlsing_next/tests/test_pre553_original35_physical_stream.py`
- No existing decoder/facade/factory/admission/A/B/D/E module edited.
- No source bytes, respondent rows, native keys or absolute source root in Git.

## Frozen producer API

```python
bounded_physical_cell_stream(
    incidence: PhysicalSourceIncidence, *, batch_size: int = 10_000,
    include_variables: Sequence[str] | None = None,
) -> ExactPhysicalCellStream
```

- `include_variables=None`: exact full row/column grid for the source-backed C11 factory.
- explicit unique names: exact selected columns over every declared source row, same source SHA and full metadata digest, in decoder global column order, for D selected-item native compiler input.
- The module never opens source bytes or creates a read decision; caller supplies the permitted `PhysicalSourceIncidence`.
- For a still-open content-bound snapshot it uses `read_file_in_chunks(usecols=...)`; for an already materialized frame it projects that frame without claiming memory reduction.
- It reuses decoder `_physical_value`, `classify_physical_value`, exact `PhysicalVariable` metadata/labels and global ordinals. It does not reinterpret values, labels, missingness or held states.

## Evidence

- Adapter tests: **7 passed** (r2 adds DTA multi-window and zero-row frame).
- Focused ABI/read-admission/original35-operations/source-config suite: **37 passed**.
- SRC31 D-style filtered baseline: 574,056 all cells created, 33,768 selected, 2.45–2.72 s/pass.
- SRC31 projected path: 33,768 selected cells, 0.14–0.17 s/pass, same selected sequence.
- SRC09 D-style baseline: 5,972,763 all cells created, 41,334 selected, 46.4–47.6 s/pass; two exact passes.
- SRC09 projected path: 41,334 selected cells, 0.44–0.53 s/pass; exact selected digest and two-pass replay.
- SRC09 native-package outputs equal: release `38f8d092…`, replay `ded005be…`, 62,009 public objects.
- Existing fixture: full factory release/replay/public-object parity; native-package parity.
- DTA sourcefree fixture: selected windowed read matches full-decode selected cells exactly.
- Genuine DTA SRC27–SRC30: all four projected streams executed; SRC27/SRC30 baseline exact parity; SRC28/SRC29 baseline failed closed on unselected strings. See `05_R3_ORIGINAL_DTA_EXECUTION.md`.
- Zero-row frame: exact empty full/projected streams, no unbound variable.
- D actual attempts `115fe70e…`: SRC31 C11 refusal 8,442 rows / 94.603 s / 1.66 GB; SRC09/10/11/15 native-R03 `max_items=1` did not finish 600 s before facts. This is full-D evidence, not claimed fixed here.
- SRC13 latin1 decode ~806 MB before any projection; frame projection keeps that history.
- DTA SRC27/30 full-frame baseline retained at 1.23/1.75 GB and 119/175 s; projection did not remove that full-frame cost where it succeeds.

## Boundaries and finite residuals

- Original bytes remain external/read-only; no native, science, actor, all35 or 16-GiB claim. All35 and 16-GiB tests **NOT_RUN**.
- A owns unbound source/config mapping. D owns F2/F3/F4 lowering, native-package cost and any remaining 600 s end-to-end failure.
- Independent nonauthor review of `fd18faf0…` is required; no self-review or protected merge.
- Next proof after A/D repairs: genuine SRC09/SRC31 C11 and native-package end-to-end parity, then wider source/all35.
