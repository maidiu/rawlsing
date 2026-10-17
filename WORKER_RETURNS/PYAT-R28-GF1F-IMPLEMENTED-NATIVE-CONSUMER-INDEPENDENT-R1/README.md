# GF1F — independent computed pair-consumer court

Independent review of GF1E `eeb726357204653b22458dc267dd70ba0009bd77`
(`gf1_pair_support_consumer.py`, sha256 `06dd484b…`).
Verdict: `PASS_SOURCEFREE_BOUNDED_GENERIC_PAIR_CONSUMER_METHOD_ONLY`
(`00_I2_GF1_VERDICT.md`).

## Layout

| path | meaning |
| --- | --- |
| `00_I2_GF1_VERDICT.md` | verdict, courts, limits, independence disclosure |
| `01_INDEPENDENT_FROZEN_PAIR_ORACLE.json` | 81-relation universe + 8 named cases, frozen before observation |
| `02_REAL_FROZEN44_AND_CONSUMER_VALUES.json` | executed consumer values + import identities |
| `03_DENOMINATOR_ROLE_GRANT_AND_COLD_CUSTODY.md` | denominator/role/grant/cold analysis |
| `tests/test_gf1f_independent_consumer.py` | 100 independent cases |
| `repro/build_oracle.py` | first-principles oracle builder |
| `repro/independent_relation.py` | reviewer's own relation builder |
| `repro/cold_child.py` | one cold OS process |
| `repro/observe.py` | rebuilds `02_…json` |
| `candidate/` | exact GF1E candidate court staged for review |
| `observations/` | JUnit for the independent court, frozen44 and GF1I19 |

## Reproduce

```sh
cd WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1
python3 repro/build_oracle.py                       # writes the frozen oracle
python3 -m pytest -q tests/test_gf1f_independent_consumer.py \
  --import-mode=importlib -p no:cacheprovider       # 100/0
(cd candidate/court/repro && python3 -m pytest -q test_gf1_generic_pair.py \
  --import-mode=importlib -p no:cacheprovider)      # frozen 44/0
python3 repro/observe.py                            # executed values
```

No Field Forge S1–S9 semantic issuance, original source35 grant, OC05,
N11/N12, actor activation or method adoption is granted by this court.
