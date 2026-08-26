# M6 Response-Map Cache Contract

The global response-option map remains the sole authority. Per-wave or per-scope files are derived, content-addressed execution caches only.

Each cache manifest must contain:

- parent global-map SHA-256;
- parent row count and schema hash;
- source family, canonical wave, and country scope;
- partition row count and SHA-256;
- cache compiler version;
- creation timestamp;
- whether the partition is exact or a documented family-level fallback.

V550 must refuse a cache whose parent hash, schema hash, or scope metadata does not match the requested execution. It must not select a file by arbitrary basename or search order. If no exact partition exists, the resolver must report that fact explicitly and require an intentional, audited fallback decision.

The cache must never be committed alongside respondent-level data. It may be regenerated from the parent authority map.
