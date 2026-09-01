# W56F COUNTEREXAMPLE REPLAY

W56F's exact route was:

canonical-looking top-level meta-validator
→ candidate `governance_r2_support.py` import
→ candidate controls predecessor semantics.

That exact edge is absent in W56G. The standalone script locally implements the former helper functions and canonical-loads trusted governance data.

Exact old route: `CLOSED`.

Equivalent-indirection search found a surviving route:

canonical top-level script
→ normal Python module search for non-built-in stdlib names
→ candidate file in the script directory with a colliding module name
→ candidate code executes before the canonical-script self-check
→ predecessor semantics can be influenced while the top-level script remains byte-identical.

The simplest concrete example is a candidate-created `GOVERNANCE_PROTOCOLS_R1/tools/argparse.py`. `argparse` is the first ordinary import in the predecessor source. Normal CPython script execution searches the script directory for such a module. No `-I`, `PYTHONSAFEPATH`, sanitized `sys.path`, or import-origin verification is enforced by the candidate protocol/script.

Therefore the broad W56F transitive-dependency counterexample is `NOT CLOSED`; it has moved from a Rawlsing-helper import to interpreter import-path provenance.