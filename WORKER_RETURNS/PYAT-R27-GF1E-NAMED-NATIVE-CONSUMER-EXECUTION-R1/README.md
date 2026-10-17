# GF1E — actual native pair-support consumer (reproduction kit)

Delivered: `gf1_pair_support_consumer.py` (at the frozen import site
`WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1/court/runtime_root/`),
plus this return's evidence.

## Layout

| path | meaning |
| --- | --- |
| `00_IMPLEMENTATION_STATUS.md` | outcome, court results, classification table |
| `01_CONSUMER_SOURCE_AND_CONTRACT.json` | module identity + frozen contract |
| `02_EXECUTED_CONSUMER_EVIDENCE.json` | executed outputs + import identities |
| `03_COLD_PROCESS_REPLAY.md` | two-process bit-identical reconstruction |
| `04_AUTHORITY_BOUNDARIES.md` | ceilings and next edge |
| `tests/test_gf1e_consumer_differential.py` | 9 new cases (4 patterns + F2 + identity + real-native + cold) |
| `tests/conftest.py` | locates the GF1 court runtime |
| `repro/gf1e_relations.py` | the four differential-pattern relation builders |
| `repro/cold_consumer_child.py` | one cold OS process |
| `repro/observe_consumer.py` | rebuilds `02_…json` |
| `observations/` | JUnit, stdout, cold outputs, baseline failure log |

## Reproduce

The GF1 native tree is already committed under the GF1 court `runtime_root/`
(74 objects re-attested by `gf1_bootstrap`). From the repository root:

```sh
R=WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1
# frozen 44 (unchanged) — expect 44/0/0/0
(cd "$R/court/repro" && PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q test_gf1_generic_pair.py \
  --import-mode=importlib -p no:cacheprovider)

# GF1E differential + cold — expect 9/0/0/0
(cd WORKER_RETURNS/PYAT-R27-GF1E-NAMED-NATIVE-CONSUMER-EXECUTION-R1 && \
  PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_gf1e_consumer_differential.py \
  --import-mode=importlib -p no:cacheprovider)
```

The consumer is committed at `court/runtime_root/gf1_pair_support_consumer.py`
(SHA256 `06dd484b…`, Git blob `75670c69dc58…`). The frozen 44 test file and
oracle are untouched.
