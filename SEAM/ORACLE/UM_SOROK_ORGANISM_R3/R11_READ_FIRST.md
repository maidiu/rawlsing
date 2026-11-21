# SOROK REMONT R11 — prospective trial integration and issuance repairs

Sourcefree author candidate: from REMONT R10 #1187 exact `9a1f2c4ba2a07d7760bd40940b014263bc1b2a19`, selectively adapting SORACLE R10 #1188 `d77cbf67aa1b11e710ef9908eea5876018a5fe5c`'s *trial-before-motive* pathway. **Not** a wholesale branch merge, issuer grant, or final psychological architecture. The sibling SORACLE branch has different constitutive R8/9 ancestors and more machinery than this integration.

Run from archive root:

```sh
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -q
python -m pytest -q
python -m um_sorok_organism demo
```

Focus files: `um_sorok_organism/prospective_horizon.py`, `constitution.py`, `semantics.py`, `runtime.py`, `development.py`, `types.py`; `tests/test_r11_soracle_integrated.py`, `tests/test_soracle_r10_remont_faults.py`.

The 213 inherited tests are retained unchanged. The 3 test-first #1189 probes and 16 new integration/falsification tests bring the complete locally executed court to 232. No parent or current protected PRE-MAIN write. Evidence, limits, original sources: `R11_REPAIR_RECEIPT.md`, `R11_SOURCE_SHA256.json`.
