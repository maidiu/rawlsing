# PROGRAMMA_DELTA — PYAT1007 early sourcefree fixture prep

- Added only `WORKER_RETURNS/PYAT1007_DUAL_SERIES_PREP_R1/`.
- Added one generic R157-metadata-driven `NONRESPONDENT_FIXTURE_ONLY`
  harness for three contrasting shapes: Arab Barometer SRC07 SAV, WVS
  SRC35 SAV, and unrelated hostile LiTS SRC28 DTA.
- Reused existing owners only: S1-B config/decoder/projection/factory,
  S2-B direct I02, accepted S2-C persisted Parquet/Zstd estate, accepted
  S2-D cold I03/I05/Batch. Production code and accepted tests are
  READONLY; no second decoder/writer/engine/bridge.
- Actual tests: 12 passed, exit 0; positive cold I03 for all three,
  route-UNKNOWN, missing/valid-zero, ranked occurrence/duplicate refusal,
  ID grain, weight-design typed absence, current/source/forged mismatch,
  cross-series joint prohibition, changed/restore, fresh-process cold I03,
  cold I05 oracle equality and Batch QUERY+DISCOVERY.
- Actual bounded resources: maximum RSS 112,820,224 B; all three persisted
  estates 1,760,894 B; under 1 GiB. Host was contended by existing #1006
  runner; isolated baseline NOT_RUN; no relative speed claim.
- Holds: real bytes `SOURCE_BYTES_UNAVAILABLE`, current permission
  `SOURCE_PERMISSION_HELD`, true #997 vertical `HOLD_DEPENDENCY`, #998/#999
  separate, #1002 historical grants not new permission, #1008/#1010
  outside control. No protected merge, no original35, no scientific or
  design/weight issuer claim, no automatic G5.
