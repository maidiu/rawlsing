# Frozen ABI and factory first consumer

## Producer

`rawlsing_next/pre553_original35_physical_stream.py`

```python
STREAM_TRANSPORT = "BOUNDED_REPLAYABLE_ORIGINAL35_PHYSICAL_SOURCE_INCIDENCE@1"

class Original35PhysicalStreamError(ValueError): ...

def bounded_physical_cell_stream(
    incidence: PhysicalSourceIncidence, *, batch_size: int = 10_000,
    include_variables: Sequence[str] | None = None,
) -> ExactPhysicalCellStream
```

`include_variables=None` returns the complete row/column grid required by the source-backed C11 factory. An exact unique column selection uses the existing content-bound snapshot plus reader `usecols`/chunk facilities (or the already-materialized frame) to construct only those cells, over every declared row and the same source SHA, in decoder global order, for D's `execute_native_compiler_source` selected response+coordinate input.

Input: an already current/authorized `PhysicalSourceIncidence` produced by the existing source-read admission and frozen decoder. The caller retains source-read decision custody.

Output: the unchanged existing `ExactPhysicalCellStream` with:
- exact source SHA,
- exact declared row count (full row range even when columns are filtered),
- decoder physical-metadata digest,
- replayable full-grid or exact-selected-column cells,
- `transport_identity = STREAM_TRANSPORT`.

No new semantic object, index, cache, canonical dataset, source grant, or kernel.

## Existing first consumer

`rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config(config, stream=producer_stream, ...)` calls the existing source-backed facade. The same stream is also accepted by `build_source_backed_c11_repository_from_config(config, stream, ...)`.

For D integration, the expected sequence is:

```python
stream = bounded_physical_cell_stream(permitted_incidence, batch_size=batch_size)
release = build_validated_c11_release_from_config(config, stream=stream, batch_size=batch_size)
repository, release = build_source_backed_c11_repository_from_config(
    config, stream, batch_size=batch_size,
)
selected_stream = bounded_physical_cell_stream(
    permitted_incidence, batch_size=batch_size,
    include_variables=selected_response_and_coordinate_names,
)
```

The adapter itself performs no source-open and no permission defaulting. A caller that has not completed the existing source-read decision cannot obtain a valid `PhysicalSourceIncidence` through this module. D's current `execute_native_compiler_source` builds a filter-every-cell closure from `incidence.iter_cells()`; it can replace that closure with `include_variables` on this producer while retaining full row/SHA identity. Measured genuine SRC09: 5,972,763 cells created / 46–48 s became 41,334 cells / 0.44–0.53 s, with exact selected-cell digest and native-package output identity.

## Exactness properties

- Full mode emits exactly `row_count * len(incidence.variables)` cells; projected mode emits exactly `row_count * len(include_variables)` selected cells, without constructing unselected cells.
- Cell sequence must be exact row-major `(row_ordinal, variable_ordinal, variable_name)` order; projected mode still requires every row and every selected column.
- Truncation, duplication/reordering, absent/duplicate selected column, wrong source custody SHA, invalid batch size, or changed source identity refuses.
- Already-materialized compatibility frames remain in memory; projection changes new selected-cell construction, not the decoder's prior full-frame history.
- Source snapshot stability is checked at producer construction and each full pass.
- No silent sampled row limit.
- `PhysicalCell` values and missing classifications come directly from the frozen decoder; no label/frequency/missingness inference.

## Measured dependency

Projection is necessary and measured for the selected physical path: SRC09 5,972,763 all-cell creation / 46–48 s became 41,334 selected cells / 0.44–0.53 s, exact digest, and equal native-package outputs. It is **not** sufficient for:
- unbound source-config response values/states (SRC31/SRC16 C11 refusal; A owns mapping),
- frozen latin1 compatibility full-frame decode (SRC13 ~806 MB after decode),
- logical native-package/C11 event/coord/weight materialization (SRC09 native-package probe remained ~42–47 s),
- D's published 600 s end-to-end native attempts.

Those remain exact upstream/consumer dependencies; no hidden workaround or full-D speedup claim was added.
