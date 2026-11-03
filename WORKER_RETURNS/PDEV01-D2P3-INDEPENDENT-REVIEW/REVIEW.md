# PDEV01 / D2P3 independent engineering review

## Verdict

- **Engineering:** `PASS_SCOPED_ENGINEERING`
- **Source science:** `HOLD`
- **Authority:** `HOLD`

Candidate is read-only. The review was executed from a disposable `git archive` snapshot of `cfe7dc6111afcb8eda26eb9a54f6cad43b6d1584`; the candidate worktree remained clean and no source/protected adoption was performed.

## Identity and scope

- Candidate: `cfe7dc6111afcb8eda26eb9a54f6cad43b6d1584`
- Baseline: `d6a184ed0f430cd008163c41756f032f7d79d292`
- Branch/worktree: candidate branch `agent/userdirect-pyat-20261014-r6-d2p3-one-registry-repair-r1`
- Session/provider/model verified: `ses_e98c8dfe6ffewNYOqJpvqK21a6`, `opencode-go`, `deepseek-v4.1-flash`, variant `max`
- All 40 changed paths are inside the candidate returnroot; no production/policy code changed.
- Source PDF bytes, publisher rights, real issuer, N5/N6, EE13, N9/OC05, V3, actor, and production adoption remain held.

## Independent results

### New suite

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<snapshot-returnroot>:<snapshot> \
  python3 -m pytest <snapshot-returnroot>/new/tests/test_d2p3_single_registry.py \
  -q -p no:cacheprovider -o addopts=''
```

**13 passed in 0.06s.**

### Adapted seven

**7 passed in 0.04s** for the seven adapted cases (`test_new_01` through `test_new_07`).

### Preserved original negative oracles

**7 failed in 0.08s** — expected historical RED, preserving the original D2P/N9C defect evidence. The seven adapted cases pass against the new one-registry path.

### Direct transport

`new/d2p/direct_trace.py` executed through the actual accepted `compose_direct_producer` module in the snapshot.

- Terminal state: `SOURCEFREE_TEST_ONLY_TWO_FIELDS_BOUND`
- Reason: `DIRECT_PRODUCER_ROUTE_EXACTLY_AUTHORIZED`
- Route: `DIRECT_PRODUCER`
- Determinant refs exactly match producer field refs:
  - `D2P_TESTONLY_FIELD:2b00177b2685b4a2171bfc27ec77a17f7e59b603bf4bd1e0fc10dc8575908f40`
  - `D2P_TESTONLY_FIELD:de36df435bd086fe265af2c3207e0ce4b4e14b66a2c8a148829bf027567c0587`
- N5/N6, EE13, OC05: false.
- Direct trace SHA-256: `25dbd9131c407ed4f58c962e7ecb3c6bb5dc4c5261b8a57361f78a02bf5d0f2d`

### Producer/reader witness

- Producer refs **equal** reader `selected_refs` and `dependency_readset`.
- GSS mutation changes only GSS ref/value/snapshot; NCA ref/value unchanged.
- NCA mutation changes only NCA ref/value; GSS ref/value unchanged.
- Revocation yields `PARTIAL_TEST_ONLY_NOT_POSITIVE`, retains both attempted refs, and records `FIELD_REGISTRY_REVOKED` with no orphan read.
- As-of: 2022-02-23 refused, 2022-03-01 partial/nonpositive, 2022-07-08 positive; cold replay equal; separate registry cold read equal.
- Wrong identity/mutation codes: `FIELD_CONTENT_REF_MISMATCH`, `ISSUER_FORGERY`, `OFFICIAL_PUBLISHER_IDENTITY_MISMATCH`, `GSS_ELECTRICITY_SUBTYPE_IDENTITY_MISMATCH`, `NATIVE_UNIT_OR_MEASURE_MISMATCH`.
- Witness SHA-256: `4dcfd622333a7d76f10d076ccde3f174375e99cc88431312d9781a82b1a24cd6`

## Allowlist and hashes

- Candidate diff: 40 paths, all under `WORKER_RETURNS/PYAT-USERDIRECT-20261014-R6-D2P3-PRODUCER-READER-LINEAGE-R1/`.
- Candidate worktree tracked dirty state: false.
- Key code/test pins:
  - `new/d2p/single_registry.py`: `f1a06fbe98580329b287406479b1ecaf70e97aa6c84b631b384d71a5be1a2f74`
  - `new/d2p/direct_trace.py`: `82ff25f6518aea6ed8984a9a4fdfd2d707481abe53c68fcdd81b96338b168443`
  - `new/tests/test_d2p3_single_registry.py`: `84702ee2bd8c370e4beb13fa6a1491f23a1e510261f39ca8de4e1d24b66a2a26`
- Logs: `new13.log`, `adapted7.log`, `original7_red.log`; source-pin evidence `SOURCE_PINS.json`.

## Limits

TEST_ONLY synthetic GSS/NCA fixture and sourcefree direct transport. No original PDF bytes, source custody, publisher/issuer authority, N5/N6, EE13, operative N9/OC05, V3, actor deployment, or production adoption. No source reads, protected merge, CI/prod, new workers/model/provider, or writes outside the allowed reviewer returnroot.
