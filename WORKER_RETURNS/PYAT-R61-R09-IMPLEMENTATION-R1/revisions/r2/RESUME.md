# R09 R2 RESUME

## State

- Branch: `agent/opencode-pyat-r61-r09-local-runner-r1`
- Resume startup: `c8dbdd017b216e01dc43e0e15d4e044f3ec6d6e8`
- Independent review repaired: `05e9ce39640ca6a134031510e762e81fab7d4c57`
- R2 code/test commit: `77f8b4205d8a97f2e9f7ae9e93a3ff913c08a780`
- R2 tree: `272fd70478b0a46d55ac4be29a2009d27228f7fb`
- Local disposition: `HOLD` for R2 independent review.
- Production: `DEPLOYMENT_HOLD`.
- No self-adoption.

## What changed

- `CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py`
  - `TrustRoot` HMAC seal held outside the child.
  - `TrustedObservation` sealed mapping; plain dicts and edits refuse.
  - Entrypoint compiled from exact candidate commit bytes.
  - Custody import finder reads/hashes/compiles the same loaded bytes.
  - Parent compares every loaded repository module to its candidate-tree blob.
  - Durable `NonceLedger` with `fcntl.flock`, re-read per claim, fsync append.
  - Typed guarded digest failures.
- `tests/universal_runner/`
  - 14 focused tests.
  - Real existing C11 ingest/repository owner positive.
  - D1–D7 controls including real cross-process nonce claims and cold CLI replay.
  - Committed sourcefree C11 fixture modules.

## Cold rerun

```sh
/usr/local/bin/python3 -m pytest -q -p no:cacheprovider tests/universal_runner \
  --junitxml=WORKER_RETURNS/PYAT-R61-R09-IMPLEMENTATION-R1/revisions/r2/junit.xml
```

Expected: 14 passed, 0 failed, 0 errors, 0 skipped.

```sh
/usr/local/bin/python3 -m pytest -q -p no:cacheprovider tests/universal_execution_oracle \
  --junitxml=WORKER_RETURNS/PYAT-R61-R09-IMPLEMENTATION-R1/revisions/r2/existing_oracle_junit.xml
```

Expected: 48 passed, 0 failed, 0 errors, 0 skipped.

## R2 independent review focus

1. Verify direct remote SHA and exact changed paths, not author text.
2. Confirm accepted observations can only arrive as a `TrustedObservation` sealed by the expected external `TrustRoot`.
3. Confirm the key never enters the child and that the old dict/issuer attacks refuse without an import/signature crash.
4. Confirm entrypoint bytes come from the exact commit and imports use load-time digests compared to the tree.
5. Confirm out-of-tree, worktree-mutated and self-restoring modules refuse.
6. Confirm two cold processes cannot both claim one nonce and malformed ledgers fail closed.
7. Confirm the C11 positive executes the existing owner, not only a toy marker.
8. Repeat targeted mutation/restoration independently.

## Held boundary

No protected CI/workflow/admin check, external key service, OS sandbox, original data/science, actor, N11/N12, J52/W52 or production deployment. Local green is not generic promotion.
