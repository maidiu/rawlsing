# C reuse/hook evidence

## Release-reuse probe

Sourcefree `build_s3` bundle, baseline `build_source_backed_c11_repository`.

- Baseline: accepted, 23 objects, release ref
  `4c119588fb679b2865e34ddd8765cec5f8a0a636f421ec11daa90ea03af4eb99`.
- Wrong source SHA: refused `prebuilt release source SHA mismatch`.
- Wrong projection identity: refused `prebuilt release projection identity mismatch`.
- Tampered sealed release via `dataclasses.replace(release,
  semantic_release_hash="0"*64)`: **accepted**; returned zero release hash.

## Coordinate-hook probe

Sourcefree SAV/config with `SCORE` administered and `OCCASION` coordinate.

- Base rule from the materialized projection; UNKNOWN value rule accepted by the
  author test; empty rule tuple refuses `COORDINATE_SLOT_RULE_MATCH_REQUIRED`.
- Rule with same slot name `OCCASION` and ordinal `2` but foreign
  `native_coordinate_ref` `urn:wrong:source`: **accepted**.
- No SRC15 actual join or A-produced SRC15 rule execution was run.

## Direct tests

```text
TMPDIR=$PWD/.local-logs/pyat-universal35/c-reuse-review/tmp \
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
  rawlsing_next/tests/test_pre553_original35_scale.py
# 2 passed in 0.97s

TMPDIR=$PWD/.local-logs/pyat-universal35/c-reuse-review/tmp \
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py
# 10 passed in 1.45s
```

Author 28+3 receipts remain reusable for unaffected components; no full estate
or original read was performed.

## Retained scale negatives

SRC10: decode 1.431 s, stream 0.078 s, first C11 materialize 169.265 s /
242,567 public objects, compile >425.861 s and still running at 601.8 s ceiling;
0 facts. SRC09 first materialize >347 s / 1.64 GB, not completed. No measured
full-plan success, no favorable timing claim.

## Limits

Actual original facts 0; C adapter join NOT_RUN; no SRC15 zero-unbound/native/
science claim. No C/product/guide/controller/protected edit; no source/600 s/
full-estate run.
