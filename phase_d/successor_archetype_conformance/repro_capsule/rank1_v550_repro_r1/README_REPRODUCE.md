# Rank-1 V550 Reproduction Capsule

This capsule contains only the bounded LiTS II / SE rank-1 input needed to reproduce the V550 empirical-surface gate. It contains 1,800 minimized long-form rows: q306c and q305_1 for 900 deterministic pseudonymous respondents. The original governed prepared substrate had 4,500 rows and 900 respondents; this capsule retains the two frozen-candidate variables only.

## Validate

From the repository root:

```bash
python3 phase_d/successor_archetype_conformance/repro_capsule/rank1_v550_repro_r1/validate_capsule.py
```

Expected output begins with `CAPSULE_VALID PASS`.

## Reproduce

1. Start from the closeout branch and do not use PostgreSQL for this bounded reproduction.
2. Run the existing V550 prepared-input entry point with `input/prepared_rank1_slice.parquet` as the prepared input, using the authority files under `authority/` and the exact two-variable scope LiTS / II / SE.
3. Preserve diagnostic mode and the existing output schemas under `schemas/`.
4. Run the unchanged Phase-D matcher against the resulting non-respondent V550 surfaces.

The capsule is not semantic authority. It preserves the active QUC and upstream authority rows as evidence, including the conservative q306c state. It must not be used to promote q305_1 or to create V551 authority.
