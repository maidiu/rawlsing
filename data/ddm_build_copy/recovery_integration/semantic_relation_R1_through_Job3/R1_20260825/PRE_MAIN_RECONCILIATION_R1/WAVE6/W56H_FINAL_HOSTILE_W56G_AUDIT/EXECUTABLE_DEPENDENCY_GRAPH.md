# EXECUTABLE DEPENDENCY GRAPH

## Intended graph

`validate_enforcement_candidate_from_canonical.py`

→ Python interpreter

→ stdlib names: `argparse`, `csv`, `json`, `re`, `subprocess`, `sys`, `pathlib`, `typing`

→ Git executable invoked directly with `subprocess.run`

→ no explicit Rawlsing-module import

→ no candidate governance script subprocess.

Classification by commanded categories:

- A Python stdlib: declared imports only.
- B Git executable: yes, allowed.
- C repository files trusted as data: protected manifest + hostile authorization/result schemas, intended canonical-loaded.
- D environment/import search state: **security-relevant and not pinned**.
- E explicit imported Rawlsing modules: `0`.
- F candidate-controlled executable dependency routes: **nonzero** through Python module search-path shadowing.

## Blocking edge

Normal script execution places the script directory on Python's module search path. Therefore names that are intended to denote stdlib modules are not provenance-bound to stdlib bytes. A future candidate may add `tools/argparse.py`, `tools/json.py`, `tools/subprocess.py`, etc. while leaving the predecessor script byte-identical to canonical.

Import occurs before any self-integrity check. A malicious shadow module can execute arbitrary Python at import time and can alter `sys.modules`, monkeypatch imported facilities, or otherwise influence the predecessor gate.

The self-check proves only the bytes of the top-level script after interpreter/import startup; it does not prove the provenance of imported modules.

Result: `TRANSITIVE_EXECUTABLE_DEPENDENCY_REMAINS`.

Potentially shadowable imported non-built-in stdlib module names in the source: `argparse`, `csv`, `json`, `re`, `subprocess`, `pathlib`, `typing` = 7. `sys` is built-in and is not the identified route.