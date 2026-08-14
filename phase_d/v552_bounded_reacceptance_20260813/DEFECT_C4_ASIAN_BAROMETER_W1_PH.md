# Superseded Asian Barometer W1/PH Finding

## Status

The original C4 classification was disproven by the required scale differential. The source authority and semantic directions are coherent; the V552 implementation had incorrectly allowed the ordinal fallback to override supplied response-scale coordinates.

The original blocked readiness was:

- pressure candidates: 4
- observed pressure: 0
- noncomputable pressure: 4
- invalid output-contract rows: 202
- input contract: PASS
- semantic/scale consistency: BLOCKED

## Resolution

The narrow V552 transform repair resolved the issue without changing authority. See `ASIAN_W1_PH_SCALE_DIAGNOSIS.md`.

## Historical record

This file is retained as the initial differential finding and is superseded by the source-native diagnosis.
