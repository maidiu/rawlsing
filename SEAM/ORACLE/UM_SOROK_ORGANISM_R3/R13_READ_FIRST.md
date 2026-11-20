# R13 immediate use

Frozen sourcefree parent #1199 `9db0e6f64bf568409e638ff2215af8b8a414487f`. New bounded first faults P072 and P073, pending independent receiving. From this ZIP's root run:

```
python -m unittest discover -s tests -q
python -O -m unittest discover -s tests -q
python -m pytest -q
python -m unittest tests.test_remontathon_r13 -v
python -m um_sorok_organism demo
```

Test-first red witness: `R13_RED_ON_FROZEN_R12.txt`; green: `R13_255_NORMAL.txt`, `R13_255_OPTIMIZED.txt`, `R13_255_PYTEST.txt`. Source byte identities `R13_SOURCE_SHA256.json`. No canonical HQ/PROGRAMMA rights, no protected write, no 3.11 or independent acceptance yet.
