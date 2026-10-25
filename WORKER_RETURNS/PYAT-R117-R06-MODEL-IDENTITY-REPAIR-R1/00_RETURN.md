# R117 — shared prefix model identity guard

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r112-r06-world-consuming-successor-r1`
- Startup: `73b7d62c391f444a0dd4cd60532ac071543ac14d`
- Contract: `647b380b99418c7edca88b5912fb56ab726c468e`
- Code: `3e8275cf45820f82c27da8f729e838b78d68bb20`
- Executor: existing OpenCode/DeepSeek `ses_e98c905cbffekusoHURfKyEUKG`,
  `opencode-go/deepseek-v4.1-flash`, variant `max`.
- Gate passed at exact cwd/branch/HEAD; only untracked pycache.

## Repair

`_progressive_model_identity` now derives a canonical identity from each
prefix's existing `PositionedSubjectPossibilityModelRule`:

- `rule_hash`;
- canonical existing `material()`: model/walkback authority refs, source
  universe refs, walkback steps, positive proxy refs, rule/algorithm ids.

`_progressive_prefix_identity` requires every prefix to share that identity
alongside universe/release/risk/repository. A mixed model registers a typed
invalid context; `progressive_world_view` refuses
`PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH` before serving. A fully
consistent alternate admitted model remains valid under its own rule hash (test
produces selected view with the alternate hash on every step).

## Preserved

R112 native world+empirical consumer, R115 owner-derived rows/repository checks,
R110 empirical/world revocation and N10E binding, condition/world mutation,
unlike shapes, cold replay, minority/zero and actor firewall are unchanged.
R112 service/test remain read-only (`db573027…`, `c46af4ac…`).

## Evidence

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py \
  rawlsing_next/tests/test_world_conditioned_progressive_service.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R117-R06-MODEL-IDENTITY-REPAIR-R1/junit.xml -o addopts=''
```

`34 passed`, 0 failed/errors/skips, `181.31s`.

Exact R116 native probes: `5 passed` (`3.37s`); exact R111+R109 probes:
`11 passed` (`5.41s`).

Actual shared model hash on both base steps:
`fa549221d39fbda539703bbaac6b7b52013fec44a798d1410a05a260d780e594`.
T0 view `8d73ef2e…c734`, T1 `37aa705a…7ed7`; native receipts
`57e23b1f…f6f5`, `058a7601…ec72`.

## Code blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_universal_world_binding.py` | `dfb1e9fb72f1ee4b50fd7138fe978ce50db49f37` |
| `rawlsing_next/tests/test_universal_world_binding.py` | `ae7f7bad72ac6118ab8f07c9ba19b22ea933950b` |

Only the two R117 code paths changed. R112 successor owner/test and historical
packets remain read-only.

## Limits

- Sourcefree finite-shape only; no original 35/1890/F5/F6/F7/F8, source,
  actor/dyad/V3, R09/CI/prod, N11/N12, Sorok/J52/W52 or production adoption.
- No world-conditioned probability; `route_probability=null`.
- No invented model merging; mismatched model identities refuse, while a
  consistent shared alternate model remains usable.
- Distinct independent reviewer required; no self-adoption.
