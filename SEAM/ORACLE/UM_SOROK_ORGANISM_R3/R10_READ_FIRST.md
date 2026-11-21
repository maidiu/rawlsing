# R10 combined SOROK REMONT sourcefree runtime

This archive is a reproducible software-engineering integration candidate **based on R9**, not a scientific law or protected native implementation. Read `R10_REPAIR_RECEIPT.md` and `SOURCE_SHA256.json` for exact ancestry, test provenance and limits.

Commands from archive root:

```shell
python -m unittest discover -s tests -q
python -O -m unittest discover -s tests -q
python -m pytest -q
python -m um_sorok_organism demo
```

The 36 R4/R5/R6 tests are **adapted** from frozen GitHub test contracts because earlier R6 fixtures used an empty pseudo-respondent and attempted public access to private activity history. Test-port provenance is explicit in each new file. No code tries to make parents accept absent survey observations, gives users another actor's private history, or writes a second psychic owner.
