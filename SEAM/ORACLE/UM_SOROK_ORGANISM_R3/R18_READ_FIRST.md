# REMONTATHON R18 — selected-purpose operation validation

Parent exact source: `maidiu/rawlsing` R17 draft #1230 at `6f2e98433822a4fb1246ff72c388b2e901c6ab7f`. This runnable archive is R16's inherited source and tests with R17's **exact hash-matched** `storage.py`, `tests/test_remontathon_r4.py`, `tests/test_r17_source_preflight.py`, then one additional P004 code repair and regression module. Neither parent nor protected PRE-MAIN is modified.

Sourcefree first fault: `activity.record_activity_afterlife` accepted actor-policy `purpose_selection` project refs even when a selected project was absent or its means omitted the performed action. It silently skipped the selected course; with multiple selected projects, a valid project was partially recorded while an incompatible selection was silently discarded.

To verify:

```sh
python -m unittest tests.test_remontathon_r18_p004_selected_means -v
python -m unittest discover -s tests -q
python -O -m unittest discover -s tests -q
python -m pytest -q
python -m um_sorok_organism demo --db /tmp/remont-r18-fresh.sqlite3
```

8 new tests (3 RED on frozen unmodified R17, 5 PASS) with full 296 normal/optimized and pytest +32 subtests author-executed using Python 3.13.5. Python 3.11 and independent review on this exact R18 SHA remain pending. All native privacy, source/authority and scientific obligations retained; P004 remains PARTIAL.
