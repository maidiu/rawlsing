# Exact continuation after P3C closure

## Restore and verify

Restore the packaged PostgreSQL dump as `rawlsing_p3c_work`, then run:

```bash
python 84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/validation/validate_p3c_governed_replay_v1.py \
  --section 84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION \
  --dsn 'host=127.0.0.1 port=55432 dbname=rawlsing_p3c_work user=oai'
```

The expected return is 37/37 PASS. The file `validation/P3C_POSTCLOSE_QUERY_MATRIX_v1_raw.txt` must contain 56 PASS lines and no FAIL line.

## Integration inputs

Use these authority exports:

- `authority/P3C_CANONICAL_FAMILY_AUTHORITY.csv`
- `authority/P3C_CANONICAL_FAMILY_MEMBERSHIP.csv`
- `authority/P3C_CANONICAL_FAMILY_REVISION_HISTORY.csv`
- `authority/P3C_CANONICAL_SIGNATURE_FIELDS.csv`
- `authority/P3C_CANONICAL_VARIANT_AUTHORITY.csv`
- `authority/P3C_FAMILY_EXCLUSION_AUTHORITY.csv`
- `authority/P3C_PAIR_RESOLUTION_AUTHORITY.csv`
- `authority/P3C_COLLISION_DISPOSITION_AUTHORITY.csv`
- `authority/P3C_STRONGER_BOUNDARY_AUTHORITY.csv`
- `authority/P3C_SPLIT_SUCCESSOR_AUTHORITY.csv`
- `authority/P3C_ADJUDICATION_AUTHORITY.csv`

The PostgreSQL database remains the authoritative normalized state; the CSV files are deterministic integration surfaces.

## Next implementation task

Produce canonical non-GSS question-family authority files in the existing GSS schema. Preserve:

- exact canonical family and lineage identities;
- explicit response-form variants;
- named exclusions and split boundaries;
- append-only revision history;
- source and evidence provenance;
- `NOT_AUTHORIZED_BY_P3` for response-value portability.

Then install those files into the family-aware pipeline and proceed through V550J, V551J, and V552J. Do not redesign P3C unless a concrete downstream invariant fails.
