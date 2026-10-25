# R115 — complete owner-derived world/prefix identity

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r112-r06-world-consuming-successor-r1`
- Startup: `79e73d0a4188bd413211d7cc54aa5507daa4a811`
- Contract: `12e8154ce8f7c61a756bdd0cb425995d58ae5dd6`
- Code: `d4b4d9bdb488296702692835395eb1e821dafa13`
- Executor: existing OpenCode/DeepSeek `ses_e98c905cbffekusoHURfKyEUKG`,
  `opencode-go/deepseek-v4.1-flash`, variant `max`.
- Gate passed at exact cwd/branch/HEAD; only untracked pycache.

## Repairs

### 1. Owner-derived rows identity

Added `progressive_source_rows_identity(repository, release_ref)`. It resolves
the exact admitted `C11LogicalRelease` through the public repository API and
hashes its canonical `RespondentIdentity`/`RespondentEvent`/
`RoutingEligibilityFact` objects plus the exact release ref. The world
`rows_hash` is compared to this owner-derived identity, not to a caller-supplied
copy. Actual test rows identity:
`5f0e24a653b6f498485a74b1f8ab6fa9c99a2b70a0c1aff1bcdfa5e8b7542418`.

### 2. Required world source repository

A missing `world_empirical["source"]["repo"]` now refuses with
`PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH`; the conditional omission
bypass is closed. Present repository identity must equal the retained prefix
repository.

### 3. Mixed-prefix repository identity

All prefix repositories must be the same actual repository object and share
universe/release/risk/source identity. A copied/mixed prefix repository now
refuses before registration/serving.

## Preserved R112 function

The R112 world-conditioned successor owner is read-only and unchanged. It still
invokes actual pinned `product.nonparent.consume` per prefix, with:
- actual world structural routes (T0 `ELIGIBLE`/`WITHIN_MODELED_BUDGET`; T1
  `BLOCKED_BY_MODELED_RULE`/`RESOURCE_CONSTRAINED`);
- actual source support (prefix 1 denominator 40, balance 20; prefix 2
  denominator 30, balance 30; zero retained);
- actual N10E hashes and native receipts
  `57e23b1f…f6f5`, `058a7601…ec72`;
- `route_probability=null`.

Condition-value mutation, unlike target shape, empirical/world revocation and
restore, cold replay and actor firewall remain.

## Evidence

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py \
  rawlsing_next/tests/test_world_conditioned_progressive_service.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R115-R06-IDENTITY-COMPLETION-R1/junit.xml -o addopts=''
```

`32 passed`, 0 failed/errors/skips, `182.239s`.

Exact R111 successor probes: `5 passed`, 0 failed/errors/skips, `2.363s`
(previously 2 passed / 3 failed).

Exact R109 probes: `6 passed`, 0 failed/errors/skips, `3.385s`.

T0 view `8d73ef2e…c734`, receipt `07966542…abe4`; T1 view `37aa705a…7ed7`,
receipt `c7b04b7b…e47e`.

## Code blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_universal_world_binding.py` | `7519667ee6f085163d72789ad406ba5f9a472e3a` |
| `rawlsing_next/tests/test_universal_world_binding.py` | `78352cd4ba3bb7674606ff59e91a18b89d7feb3a` |

R112 service/test blobs remain `db573027…b31` and `c46af4ac…4b0` read-only.
Only the two R115 code paths changed. No historical packet/owner edit.

## Limits

- Sourcefree finite-shape only; no original 35/1890/F5/F6/F7/F8, source,
  actor/dyad/V3, R09/CI/prod, N11/N12, Sorok/J52/W52 or production adoption.
- No world-conditioned probability; native empirical support is preserved
  unchanged by world rules.
- Missing/low-support beyond the declared fixture remains unexpanded.
- Distinct independent reviewer required; no self-adoption.
