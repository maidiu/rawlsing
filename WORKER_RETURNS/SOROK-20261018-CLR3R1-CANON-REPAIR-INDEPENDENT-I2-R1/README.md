# Independent CLR3R1 repair court

Read `00_RETURN.md`, then `01_RED_AND_FALSIFIER_MATRIX.md` and `02_NATIVE_OWNER_GAPS.md`.

`frozen/` contains exact Git material from the repaired return, including earlier evidence. `evidence/` contains this fresh review's executions. The independent runners never write to frozen sources.

Reproduction from this directory, using a local Python 3.11 environment with pytest 9.1.1 and PyYAML 6.0.2:

```sh
python run_court.py
python replay_independent.py
python audit_independent.py /path/to/available-sourcefree-code-archive.zip
```

Run `python materialize_frozen.py` first when reproducing from a fresh checkout. One original predecessor runner embeds a personal host path and is retained locally, ignored here, with its exact Git ref/blob/hash in `staging_manifest.json`. It is rehydrated without modification from that pin; no personal path is republished. The actual repaired wrapper, unchanged tests, all 65 runtime/config files and all 31 selected members are included. The historical runner is not used by this independent execution.

`run_court.py` deliberately exits 1 with six historical RED and two pre-repair I2 RED, while the four repaired suites total 89 PASS. Read per-suite receipts rather than interpreting the aggregate exit as a repaired-candidate failure. No missing dependency is automatically installed by these runners. The archive is not bundled, and its required whole-container mismatch stays HOLD.

No production/native execution or adoption is authorized. File hashes are sealed in `return_manifest.json` and `SHA256SUMS`; these seals exclude themselves to avoid self-reference. Publication evidence names a verified checkpoint rather than pretending to contain its own final Git commit hash.
