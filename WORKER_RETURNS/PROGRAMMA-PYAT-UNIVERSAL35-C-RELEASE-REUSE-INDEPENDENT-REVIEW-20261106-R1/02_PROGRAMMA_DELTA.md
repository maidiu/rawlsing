# PROGRAMMA_DELTA — C release reuse/hook review

| Field | Delta |
|---|---|
| `VERDICT` | **REVISE** at target `6f9e41f3…`, code `8c5e8236…`; published review head reported in final delivery. |
| `RELEASE_REUSE` | FAIL/REVISE: baseline exact release/replay reuse and source/projection mismatch refusals pass, but a sealed release tampered via `replace(..., semantic_release_hash="0"*64)` is accepted because only stream SHA/projection strings are checked. |
| `COORDINATE_HOOK` | PARTIAL: exact one-rule/name/ordinal and UNKNOWN-state behavior pass; wrong-source `CoordinateSlotRule` with correct name/ordinal is accepted; actual SRC15 join NOT_RUN. |
| `TESTS` | Scale 2 passed; facade 10 passed; author 28+3 reusable; no favorable timing claim. |
| `SCALE` | SRC10 materialize 169.265 s + compile >425.861 s at 601.8 s ceiling, 0 facts; SRC09 materialize >347 s; no full-plan success. |
| `LIMITS` | Actual original facts 0; C adapter join NOT_RUN; no source/native/S3/science/protected adoption, original data, 600 s/full estate, or C repair. |
