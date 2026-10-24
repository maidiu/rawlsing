# R95 R06 author return — source-separated world selected-view binding

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r95-r06-world-consumer-integration-r1`
- Startup: `a7f5cc70520e5236c24bbac241fad071c026d881`
- Contract commit: `2f1d67e87a9803d3db6db2773cf3b2589877999c`
- Initial N10E code: `7f28ca4ad241a749e85ce6bbdac8f25795b80468`
- Actual joined J42/N9/N10W/E04 code: `0b64393b2f4b8c28131f868738499475335496ed`
- Executor: existing OpenCode DeepSeek V4.1-Flash MAX/Global.

## Delivered

1. `select_world_view`: source-separated two-field binding over the actual
   unchanged N10E positioned-subject consumer via
   `compose_positioned_subject_possibility`, with source/release/unit/role/
   clock/transport validation and typed refusal.
2. `select_joined_world_view`: adapter over the **actual pinned J42/P41
   N9/N10W/E04 joined consumer** (`f53cb0d2...`). The test materializes the
   packet from Git and runs its frozen build in a fresh subprocess; it does not
   use a fixture dictionary echo or replacement evaluator.

Actual two fields (`training_access`, `civil_sanction`) change the same joined
E04 view's structural assertion and canonical hash. Actual permitted clock-mode
selection (`TEST_CURRENT` -> `HISTORICAL`, `valid_at` 2027-09-01 -> 2026-06-01)
changes the same receipt/view. A second fresh build reproduces the exact cold
view, N10E steps and N10W payload.

Hostile controls cover wrong source/release, fewer than two fields, duplicate/
absent fields, person/household pooling without transport, contextual-as-
structural, unobserved temporal pair, revoked currentness, and substituted
consumer identity. Original restore passes.

## Commands

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R95-R06-WORLD-CONSUMER-INTEGRATION-R1/junit.xml -o addopts=''
```

Exit `0`; `7 passed`, `0 failed/errors/skips`; `158.74s`.

## Blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_universal_world_binding.py` | `71cb2c79386bc3a9accc5eee09ab1d0c0f2b0456` |
| `rawlsing_next/tests/test_universal_world_binding.py` | `304e109563a6c58229a0c71e3e1472fee63aec96` |

Manifest excludes itself. Existing W41/F43/FF/temporal/J42/P41/N9/N10W/E04 and
accepted R03/R04/R05/R08 bodies were not edited.

## Explicit limits / unmet requirements

- The temporal positive is an actual permitted clock-mode/as-of selection, not
  an actually observed F7 comparison pair of measured waves. The observed-pair
  positive remains NOT COMPLETE.
- The accepted R05 candidate learned product is not the learned input to the
  joined J42 packet; J42 carries its own pinned E04L learned-release readthrough.
  This is disclosed rather than silently bridged by source overlap.
- Cross-unit transport is validated, but no linked indexed cross-unit query is
  invented or claimed.
- No original source/science, FF/F6/F7/F8 issuance, R04/R05 replacement,
  CI/prod/N11/N12/Sorok/J52/W52. Distinct reviewer required; no self-adoption.
