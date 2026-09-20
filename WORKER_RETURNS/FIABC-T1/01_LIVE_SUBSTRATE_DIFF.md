# FIABC-T1 — Live Substrate Diff

## 1. Execution-line resolution

Requested lineage:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

Previously audited tip:

`617c9c9426db12a3c0f7fea6b68a582c10759553`

Pre-mutation branch comparison: **identical** to `617c9c9426db12a3c0f7fea6b68a582c10759553` (0 ahead / 0 behind). Therefore `617c9c9426db12a3c0f7fea6b68a582c10759553` is the exact current governed execution-line tip used as the new branch base.

## 2. Why no whole-file PRE-MAIN winner was used

The accepted I04 backend was itself built from the exact audited live backend blob `b223d309b5f5fa45389badec719ce2882e672cca`. Comparing it with the live backend produced exactly three substitutions and no other byte-level delta.

| Live locator | Transposed stable locator |
|---|---|
| `WORKER_RETURNS/EE-P2R6S/SUPPORT/02_WVS7_P2F2_RUNTIME_PACKAGE.json` | `rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json` |
| `WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py` | `rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py` |
| `WORKER_RETURNS/EE-P2R6S/SUPPORT/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py` | `rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py` |

Resulting backend blob must be the accepted I04 blob:

`b0115ceffe7203c29646faffcbc5adfcfa373488`

This function/locator-level transposition preserves the live backend's R6W S17 orchestration/failure-path repair and all other later P2X behavior.

## 3. Added packaging surfaces

| Path | Exact Git blob | Role |
|---|---|---|
| `rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py` | `9406bacfd928393f6a159a46216aa1f7ec129f34` | stable LiTS runtime materializer |
| `WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py` | `504944f9533b7385d201076e2e834b8a9446dee8` | exact accepted Node4A support carrier |
| `rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json` | `e04e84b76f8b4eb53905276dd025938bf2e5f6fe` | stable WVS7 P2F2 runtime package |
| `rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py` | `11b28416aac5a4899706150721f2f8ac8bb6ee43` | stable WVS7 projection materializer |
| `rawlsing_next/runtime/ee_p2x/RUNTIME_PACKAGING_BINDING.json` | `25c56abf292175fa5894e5a65362e239eaa55db1` | accepted I04 identity/ownership manifest |
| `rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py` | `f8d49baecc0c08c0ca40dde2bfd189398b8c150b` | static hostile identity court |

## 4. Explicit non-diff

Not changed:

- `rawlsing_next/ee_p2x_darwin_court_driver.py`;
- any frozen candidate-owner implementation;
- P2X stopped receipts or historical evidence;
- R6X reconciler/history;
- continuation/reducer history;
- source roots;
- semantic authority/ownership;
- measured court state.

No PRE-MAIN governance/handoff history was merged.
