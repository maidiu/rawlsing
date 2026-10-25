# R110 — world identity, empirical revocation and N10E binding repair

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW, with one exact stopped
P41-owner dependency. Not self-adopted.

## Identity

- Candidate baseline: `22280a3f43e751bab1bbebe0a9d8c601b3160120`
- Review: `e38a6a8c07ea6535a0d4de38053c15e4278934d7`
- Branch: `agent/opencode-pyat-r110-r06-progressive-binding-repair-r1`
- Contract: `53981ac013755407ebf7de88f894add2f1dc2858`
- Code: `b6acb241366b1a940c613a779037f97351bd0d85`
- Executor: existing OpenCode/DeepSeek `ses_e98c905cbffekusoHURfKyEUKG`,
  `opencode-go/deepseek-v4.1-flash`, variant `max`, stable `r61-r01`.
- Gate passed at exact cwd/branch/HEAD; only untracked pycache.

## Repairs completed

### 1. World/prefix identity binding

`configure_progressive_world_context` now derives and compares, across every
actual producer prefix:

- source universe ref;
- source/release refs and consumer release;
- risk-set ref;
- empirical-universe membership;
- repository identity.

The governed world's source universe, release, risk and repository must agree.
A mismatch registers a typed invalid context and
`progressive_world_view` refuses
`PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH` before serving. The R109
foreign-world-release probe now refuses instead of returning concrete routes.

### 2. Empirical permission/revocation

The pinned P41 world block now carries the selected snapshot `empirical` state.
`StructuralService.possibilities` reads the actual catalog empirical state. An
empirically revoked world returns
`PROGRESSIVE_WORLD_UNAVAILABLE` /
`WORLD_EMPIRICAL_REVOKED_OR_UNAVAILABLE`, with
`n9_world.empirical.state="REVOKED"`; a clean context restores the selected
view. Field revocation/restore remains.

### 3. Actual N10E → N10W consumption binding

Each prefix now invokes the actual
`evaluate_positioned_subject_possibility` on its actual computed evidence and
requires its result hash to equal the producer/extension consumer hash. The P41
provider emits real `evaluate_positioned_subject_possibility` trace entries, so
`n10w.positioned_consumptions` contains the actual N10E hashes with
`source="LIVE_TRACE"`, not cached null placeholders.

Actual positive:

- prefix 1: denominator 40, cells 10/30, consumer
  `8be7de896d99ed4da15c1342dd851bb8080c037f8e31909ec8df5938a6cf4f4c`;
- prefix 2: denominator 30, cells 0/30, consumer
  `6980707e8ce06495bd627e24aec078b57f30874cb90bbb9fde224c5a6b29afb4`;
- both positioned entries are `LIVE_TRACE` and match those hashes.

## Stopped dependency: N10W world-value binding

T0/T1 world changes still alter actual N9/E04 routes, but the pinned P41
`n10w` block remains a function of target/ordered conditions only. The exact
owner gap is:

`f27d1101048638bba395143a48efb7ef00bfcda4:WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-N10E-N10W-SERVING-R1/runtime/p41_service.py`,
`P41Service.progressive` lines 133 and 149–171: `provider.progressive(target,
ordered)` receives no world/snapshot; `n9_world` is computed separately, and
`n10w.progressive_update_identity`/`positioned_consumptions` do not include the
selected world. The smallest amendment is to extend that P41 provider call or
add a world-conditioned provider contract and include the selected
world/snapshot binding in the `n10w` consuming assertion. This is outside the
two-path R110 allowlist; no cosmetic hash was added. Full N10W world-value
consumption is therefore **not claimed**.

## Evidence

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R110-R06-PROGRESSIVE-BINDING-REPAIR-R1/junit.xml -o addopts=''
```

`26 passed`, 0 failed/errors/skips, `207.629s`.

Independent R109 probes replayed exactly:

```text
PYTHONPATH=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01 \
  /usr/local/bin/python3 -m pytest <R109 probes/test_r109_progressive.py> -q \
  --junitxml=WORKER_RETURNS/PYAT-R110-R06-PROGRESSIVE-BINDING-REPAIR-R1/r109_probes_junit.xml -o addopts=''
```

`6 passed`, 0 failed/errors/skips, `3.260s` (previously 3 passed / 3 failed).
The R109 probes now pass foreign-world refusal, empirical revocation, N10W
consumer-hash binding, condition-value mutation, unlike target and field
revocation/restore.

T0 view `2905709b…0e42`, receipt `c642a98b…2078`; T1 view
`b4eaf07e…2fa7`, receipt `f6276d1c…6f93`. The second target/prefix shape returns
`decad366…75fe`.

## Code blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_universal_world_binding.py` | `fe167820246ace0881d33870442064f85a04da10` |
| `rawlsing_next/tests/test_universal_world_binding.py` | `f78b983b514f1a0a78bf16c5f05ddc2adfaf2bc8` |

Only these two tracked code paths changed. P41/R05/W41/F43/J42/FF/temporal/
service/evaluator bodies and old returns were read-only.

## Limits

- Sourcefree synthetic finite-shape release; not original source, F5/F6/F7,
  35/1890/global F6/F7/F8, actor or production evidence.
- N10W world-value dependency is held at the exact P41 owner/API above; only
  N9/E04 world dependence is currently demonstrated.
- No probability reweighting, causal law, dyad/cross-unit joint, actor state or
  V3/N12/Sorok wake. R09/CI/prod/N11/N12/Sorok/J52/W52 remain held.
- Distinct independent reviewer required; no self-adoption.
