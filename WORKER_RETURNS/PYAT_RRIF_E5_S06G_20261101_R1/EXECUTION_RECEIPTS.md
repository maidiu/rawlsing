# EXECUTION RECEIPTS

## Environment

- Host: `mainMac`, macOS 13.2.1 (22D68), x86_64, Intel i9-9880H.
- Python 3.11.3, pytest 9.0.2, OpenCode 1.18.34.
- Model surface: `opencode-go/deepseek-v4.1-flash`, local variant `max`; no provider-side MAX attestation.
- All commands: `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=.`, `-p no:cacheprovider`.
- No raw survey, native source, original U/E_pre, actor, Field Forge, CAN/ADP, N11/N12, C1/C11 or model-use execution.

## Unfiltered full suite

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py \
  rawlsing_next/tests/test_pre553_s06g_atomic_integrity.py \
  rawlsing_next/tests/test_pre553_e5_s06g_independent_hostile.py \
  rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  <S06G-return>/repro/reviewer_overlay/test_hq284_s06fr_native_review.py
```

**179 passed, 14 failed, exit 1.** Log: `test_receipts/unfiltered_full.log`.

| Suite | Passed | Failed |
|---|---:|---:|
| Accepted B5 | 39 | 0 |
| Accepted M2 | 26 | 2 |
| S06G new repair court | 42 | 0 |
| E2 independent court | 10 | 0 |
| Adjacent EE14 asof + world composition | 45 | 0 |
| S06FR overlay | 17 | 12 |

## Filtered selection (explicitly not a green full suite)

```sh
... -k 'not OBSERVED and not test_17_binding_cannot_resolve_different_release and not test_18_endpoint_failover_only_among_same_release'
```

**179 passed, 14 deselected, exit 0.** Log: `test_receipts/filtered_14_deselected.log`.

The deselection is exactly the 12 historical defect-presence assertions + the two accepted M2 fixture conflicts. It is a selection, not an adoption or a claim that the unfiltered suite is green.

## Per-court receipts

| Court | Command (abridged) | Result |
|---|---|---|
| Accepted B5 | `pytest -q rawlsing_next/tests/test_pre553_learned_product_lifecycle.py` | 39 passed |
| Accepted M2 | `pytest -q rawlsing_next/tests/test_pre553_learned_product_release.py` | 26 passed, 2 failed |
| S06G repair | `pytest -q rawlsing_next/tests/test_pre553_s06g_atomic_integrity.py` | 42 passed |
| E2 independent | `pytest -q rawlsing_next/tests/test_pre553_e5_s06g_independent_hostile.py` | 10 passed |
| Adjacent | `pytest -q test_pre553_ee14_selected_current_asof_hq260.py test_pre553_learned_world_composition.py` | 45 passed |
| S06FR overlay | frozen overlay at exact blob | 17 passed, 12 obsolete-defect failures |

## Differential evidence against current

From E2 `46a4ba7b`, the same 10 independent E2 tests:

- Current unpatched PRE-MAIN: **10 failed**.
- S06G candidate overlay: **10 passed**.
- E5 patched current (this branch): **10 passed**.

The current accepted B5 court was 39/39 and accepted M2 28/28 before the patch; after the patch B5 remains 39/39 and M2 becomes 26/28 because the two accepted fixture setups are refused earlier. No other accepted B5/M2 test regressed.

## Artifact hashes

| Artifact | Blob |
|---|---|
| lifecycle | `dadf2362f3195c28ebaf97655e28cdba72c04fb3` |
| release | `1cb7692399aad8fb272c8c9ce956719527829007` |
| S06G test | `9964464cd86c077ff5b9a99cea6fb0a41e516c80` |
| fixtures | `f3040bb40a246e7b0bdea243060458d2045ab43b` |
| S06F shim | `6974f7d5e2f4ed66bb36b6160ce2ced08574d5b5` |
| E2 test | `9a469ad0940216e02967c94159db943d2979154a` |

## What was not run

- No PRE-MAIN/main mutation, no source-native execution, no actor/model/science issuance.
- No OS-kill durability, multiprocess/cross-process custody, external issuer or protected CURRENT.
- No #580–#584 launch; no PROGRAMMA PYAT, Sorok or N11/N12 work.
