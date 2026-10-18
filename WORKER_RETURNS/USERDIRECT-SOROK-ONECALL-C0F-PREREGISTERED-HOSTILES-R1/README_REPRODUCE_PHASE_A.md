# C0F exact Phase-A runnable Git custody

Frozen authoritative content: `frozen_oracle.py`, `preregistered_cases.py`, `test_phase_a_oracle.py`, `cold_replay_probe.py`, and `01_FROZEN_HOSTILE_MATRIX.json.gz`. The compressed matrix is **exact bytes** of the 32-case original JSON (SHA-256 `2d16c3fd3d8792e990cfc925a92092d1736d60b6b82638e303c80603a331dd27`, compressed blob SHA-1 `029ef637a729c96e4ca0e128d34d296c4628cf52`). Compression is transport, not oracle rewriting. Source Git blob identities were checked against the exact locally executed files before Git publication.

From this directory in a fresh authenticated Git checkout (no original surveys):
```sh
python -B materialize_frozen_matrix.py
python -B -m pytest -q --disable-warnings --junitxml=phase_a_rerun_junit.xml test_phase_a_oracle.py
```
Expected: 45 test cases; 32 independently predeclared A01–A32 plus 13 metamorphic/cold arms. The original **actually executed** JUnit is published separately as `phase_a_reference_junit.xml.gz` (decompress before comparison), not to be mistaken for a fresh C0 implementation run. Raw stdout `45 passed in 1.93s`. This court never loads C0 and has no real LLM calls, actor psychology, source or owner grant. Its reference tests' PASS is only a Phase-A oracle smoke test. C0 remains at its commission seal; Phase B not performed.

Distinct from the wider local portable archive linked in the worker return, these are independently fetchable, versioned Git contents.
