# W04 policy and cache contract

## Governed activation

The compact accelerator is still a derived cache, never a canonical source or
scientific authority. A host activates it with a policy file referenced by
`RAWLSING_C11_ACCELERATOR_POLICY`; the policy is authoritative and is validated
before any write.

Required policy schema:

```json
{
  "schema": "PYAT_C11_ACCELERATOR_POLICY@1",
  "enabled": true,
  "root": "/absolute/private/host/root",
  "source_permission": "NONRESPONDENT_SOURCEFREE",
  "authorization_id": "host-owner-decision-id",
  "retention_budget": {
    "max_bytes": 268435456,
    "max_files": 16,
    "max_age_seconds": 86400
  }
}
```

The policy file must be an owned regular non-symlink file with no group/world
write bits; the root must exist, be owned by the caller, be a real directory,
and have no group/world permissions. Missing policy, malformed policy, invalid
root, unauthorized source permission or invalid budget returns no cache policy
and therefore performs no cache write. A configured invalid policy never falls
back to a bare directory environment variable.

The legacy `RAWLSING_C11_ACCELERATOR_DIR` path remains accepted only by the
pytest-only temporary-root fallback used by existing focused tests; it is not a
deployment grant. The new tests use the policy file and a test-owned temporary
root.

## Cache identity and invalidation

The cache key and Parquet metadata envelope bind:

- accelerator schema;
- source artifact identity;
- decoder/transport/physical binding;
- projection identity;
- authority snapshot root;
- exact release and release manifest;
- replay manifest;
- member selector root;
- independent trusted policy/root identity (`trusted_root_id`).

A cache hit requires the envelope to equal the current expected envelope. A
changed authority/source/projection/release/replay/schema/policy root or a poison
body is a safe miss; the current exact C11 release is rebuilt. A cached file is
never accepted solely because its pathname or environment root exists.

## Atomicity and retention

Cache publication stages in the authorized root, writes bounded Parquet row
groups, fsyncs the staged file, atomically replaces the destination, and fsyncs
the directory. Retention removes only disposable `c11-events-*.parquet` files;
it never touches the canonical Parquet carrier. The post-write budget check
removes the new cache file if it cannot fit or retain within the policy budget.

`ParquetC11Carrier` remains canonical. Its `persist` path now fsyncs each table
and manifest, atomically replaces the staged release directory and fsyncs the
parent. Interrupted publication leaves no accepted partial release; reopen
validates the manifest, member hashes, relation digests, semantic root and
content-addressed path.

## Scope limits

- Sourcefree S2 only; no original35/source/science/actor/native claim.
- The policy is an explicitly authorized host configuration, not a new
  scientific or source-rights issuer.
- The cache is disposable; deletion does not remove canonical data.
- No second store or query engine exists.
- Full 12-ID MCR-C acceptance and independent economic review remain with HQ.
