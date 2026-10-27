# SYN02 F0-R2 — replay receipts and changed-file hashes

**Date:** 2026-10-27
**Branch:** `agent/sorok-syn02-f0-r2-source-custody-repair-r1`
**Startup:** `9903a30d8d9cd4594f58c46bec80e538610a1851`
**Host:** Darwin 22.6.0 x86_64; Python 3.11.3; pytest 9.1.1
**Mode:** sourcefree local Python/pytest; no paid product/provider call, no native C8/C9/C12/C11/A5, no production/survey execution.
**Reviewer:** this is the implementer's receipt, not independent acceptance.

## 1. Baseline 58-test replay

Environment for every suite: `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` outside the source tree, pytest cache provider disabled; all `S52_G18_SOURCE`, `S51_G18_SOURCE`, `G18_SOURCE`, `M35_G18_SOURCE`, and `S52_ALLOWED_ROOTS` unset.

### Repository root

```text
cd $W
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/tests
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/tests
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1/tests
```

| Suite | Result |
|---|---:|
| S52 | 18 passed in 142.91s |
| S48 | 14 passed in 15.50s |
| S51 | 13 passed in 48.64s |
| S49 | 13 passed in 39.77s |
| **Total** | **58 passed** |

### Alternate working directory `/tmp`

Same suites with absolute paths:

```text
cd /tmp
python3 -B -m pytest -q -p no:cacheprovider $W/WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests
python3 -B -m pytest -q -p no:cacheprovider $W/WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/tests
python3 -B -m pytest -q -p no:cacheprovider $W/WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/tests
python3 -B -m pytest -q -p no:cacheprovider $W/WORKER_RETURNS/SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1/tests
```

| Suite | Result |
|---|---:|
| S52 | 18 passed in 143.57s |
| S48 | 14 passed in 17.63s |
| S51 | 13 passed in 48.18s |
| S49 | 13 passed in 39.45s |
| **Total** | **58 passed** |

This removes the RF0 alternate-CWD failure: the S52 portability test now reads its source files through `REPO`, not the process cwd.

## 2. R2 adversarial suite

```text
cd $W
PYTHONPATH=$W/WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY \
  python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/tests
# 21 passed in 24.01s

cd /tmp
PYTHONPATH=$W/WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY \
  python3 -B -m pytest -q -p no:cacheprovider \
  $W/WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/tests
# 21 passed in 24.45s
```

The 21 tests cover:

- fake `opencode` on PATH with no explicit selection -> typed `S48_PRODUCT_CLI_MISSING`, no directories, no invocation;
- explicit CLI/provider/model/variant/account -> coherent config with `enabled_providers=[provider]`;
- wrong provider/model pair, missing model/account, non-executable/relative CLI -> typed refusal before subprocess;
- full G18 package manifest coverage and 31-file bounded closure verification;
- G18 root symlink, G18 file symlink, traversal/absolute path, conflicting env source, changed G18 `__init__`/`core`, wrong manifest role/provenance;
- changed G18 source and poison preloaded `lab_sgi1` -> failure before S49 import; no side effect from the changed `__init__`;
- base S51 `ok=True` while malformed S52 candidate cold-open refuses;
- moved cold-fork root refused, original root remains clean;
- unexpected parent exception not masked;
- false verify and verify exception close the session; verify is non-mutating and `native=False`.

## 3. Source manifest

The portable registry is `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/source_manifest.json`. It contains 31 entries:

| Root | Files |
|---|---:|
| S48/S49/S51/S52 F0-managed packages | 20 |
| accepted G18 `lab_sgi1` package | 5 |
| accepted R30A package | 6 |

`build_source_manifest.py` regenerates it from resolved roots and reports `verified=31`. The manifest contains relative paths and SHA-256 only; root provenance declares:

```text
repo: F0_R2_SOURCE_TREE / SOROK_SYN02_F0_R2_IMPLEMENTER / sourcefree_test_only / 2026-10-27
g18:  ACCEPTED_G18_PACKAGE / R31J_GM01_SOURCE_PERSON / accepted_vendor_source / 2026-10-21
r30a: ACCEPTED_R30A_PACKAGE / R30A_FIRST_NEIGHBOR_SESSION / accepted_dependency_source / 2026-10-22
```

The bounded closure deliberately excludes stdlib/site-packages and prior accepted S36/S37/M35/language/JOIN-E roots; those are outside this R2 source-custody boundary and are not newly certified.

## 4. Changed-file hashes

SHA-256 values were computed from the final working tree. `02_TEST_RECEIPTS.md` is omitted from its own table because self-embedding would change its bytes.

| Status | Path | SHA-256 |
|---|---|---|
| M | `.../S48.../s48/product.py` | `29fe4f70e9f3190e0f989ab9d3075b9a1d10138cf250b45964d712c234cf6d1d` |
| M | `.../S48.../tests/test_f0_product_portability.py` | `d879438b48c7c31d78fa5b914ffd01702ec6a0b91918693c677344009c297244` |
| M | `.../S51.../s51/bootstrap.py` | `b180c81c145fd2d16b13b4067058a02681e6007689ee4573e87a3a7af81d6531` |
| M | `.../S51.../s51/source_binding.py` | `a5ecf0c60efd6aaa9dee279b4176cd72789b4573d4939186d361be3e4d6997cb` |
| M | `.../S52.../s52/bootstrap.py` | `e6461605dc96fbb8957da8eaec1d769b699d3fab58f0596c88152b6cf29b3373` |
| M | `.../S52.../s52/source_registry.py` | `8881d97b83ef8bfd59c2cb9796881f58e39066a479a6d90a8158218a0692863d` |
| M | `.../S52.../tests/test_f0_source_portability.py` | `f75b0c70b4844537b4ae2b0613820b855fe30c6886ce65781e299024750060f6` |
| A | `.../SOROK-SYN02-F0-R2-PORTABILITY/source_manifest.json` | `7120d3077a6687957c02d0eba880a11329a4a4fcc29ad9fe17ef92a92600b84d` |
| A | `.../SOROK-SYN02-F0-R2-PORTABILITY/build_source_manifest.py` | `8bae025cd2cabedeba239a77cc940781fb85b984f4b10eeee0239895c3a82efa` |
| A | `.../SOROK-SYN02-F0-R2-PORTABILITY/tests/conftest.py` | `4359dc1a62021886c02007bc257ac01ce9e65b25dfb4151f7540f0719ef33c02` |
| A | `.../SOROK-SYN02-F0-R2-PORTABILITY/tests/test_provider_selection_r2.py` | `5f06c3adaad3a338dc021732b21215ef9ce6a254989197c62074637fb4ec21cc` |
| A | `.../SOROK-SYN02-F0-R2-PORTABILITY/tests/test_source_custody_r2.py` | `73cc40ef2702adee612dc2c2b1e9f781b0c352ed4b5568d249c9b0fe7672a56d` |
| A | `.../SOROK-SYN02-F0-R2-PORTABILITY/tests/test_cold_open_r2.py` | `26522e2f28cad9678e7577572cf62c85e7b0bdb56b82bc3dc603b3d90824e11e` |
| A | `.../SOROK-SYN02-F0-R2-PORTABILITY/00_RETURN.md` | `d95fe621314b86615b5a83dee3655f2fb40a35543ed61ec7da56c2667bfe4b75` |
| A | `.../SOROK-SYN02-F0-R2-PORTABILITY/01_OWNER_SCOPE.md` | `d5b95eca0eac96d9b9e40109f16f2e90d33994d3a62472e2ac0cb0ffb4357d84` |

The source manifest itself contains the final hashes for all 31 source files, including the five modified source files above.

## 5. Not run / residual

- Real paid CLI/provider/model call: **NOT_RUN**.
- Native C8/C9/C12/C11/A5, actor/person or source survey: **NOT_RUN**.
- `run_s52_evidence.py`: **NOT_RUN**; it was not changed because the approved R2 scope did not include an evidence-script exception. It writes evidence directories into the source tree.
- S48/S51 evidence scripts still contain historical `/Users/` paths; they were not changed and are outside this R2 source-custody claim.
- The bounded manifest does not certify prior S36/S37/M35/language/JOIN-E roots.
- Historical F0 branch/extra-file custody remains unresolved; the user's prospective R2 approval does not waive it.

**Implementer disposition:** `F0_R2_IMPLEMENTED_SCOPED_SOURCEFREE__PENDING_INDEPENDENT_REVIEW`. No self-adoption, no native grant, no production edit.
