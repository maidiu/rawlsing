# Runtime rerun guide

All commands run from this return directory or the repository root; no absolute host path is required.

## 1. Build the two-epoch world product

```bash
cd runtime
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
  python3 two_epoch_world.py ../03_WORLD_TWO_EPOCH_CONSUMER_DELTA.json
```

## 2. Two cold child processes

```bash
cd runtime
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 runner_cold.py
```

Writes `02_PINNED_NATIVE_TEMPORAL_IMPORTS_AND_JUNIT/cold_a.json`,
`cold_b.json`, `cold_a.log`, `cold_b.log`, `cold_replay.json`.

## 3. Tests

```bash
cd runtime
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest tests -q \
  --junitxml=../02_PINNED_NATIVE_TEMPORAL_IMPORTS_AND_JUNIT/our_suite.xml
```

Original owner courts:

```bash
cd /path/to/repo
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider \
  rawlsing_next/tests/test_m4_v557_v558_publication_repository.py \
  rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R35-T35-TEMPORAL-WORLD-POSITIVE-R1/02_PINNED_NATIVE_TEMPORAL_IMPORTS_AND_JUNIT/original_m4_m5.xml

PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_empirical_possibility_provider.py \
  rawlsing_next/tests/test_pre553_empirical_query.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R35-T35-TEMPORAL-WORLD-POSITIVE-R1/02_PINNED_NATIVE_TEMPORAL_IMPORTS_AND_JUNIT/original_empirical_chain.xml

cd WORKER_RETURNS/PYAT-R35-T35-TEMPORAL-WORLD-POSITIVE-R1/runtime
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider \
  author_courts/test_product_r10.py -q \
  --junitxml=../02_PINNED_NATIVE_TEMPORAL_IMPORTS_AND_JUNIT/original_e04_author.xml
```

## 4. Layout

- `bootstrap.py` — adds the sealed checkout, the staged non-sealed owner modules, and the two extra native modules (N9C reader, progressive candidate) to the import path.
- `two_epoch_world.py` — actual M4/M5/E04/N9C execution, two epochs, clocks, source/rule matrix, revocation, mismatch, cold product.
- `n8e_sourcefree_comparator.py` — hypothetical-only N8E/EE12 admissibility and arithmetic specification; Ghana N03 state is a frozen null record.
- `v553_candidate_eval.py` — executes the sealed V553 modules against empty input and classifies the candidate method.
- `tests/` — 41 frozen cases.
- `author_courts/test_product_r10.py` — exact R10 E04 author court.
- `selected/product/` — exact R10 E04 product package blobs.
- `selected/e05_n9_selected_world_adapter.py` — exact R13 E05R adapter blob.
- `selected/native_extra/` — exact HQ297 N9C reader and HQ281-E03 progressive candidate blobs.
- `selected/fixtures/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json` — exact test-only GSS/NCA fixture.

**No original source file, respondent row, SAV/DTA, credential or external service is used.**
