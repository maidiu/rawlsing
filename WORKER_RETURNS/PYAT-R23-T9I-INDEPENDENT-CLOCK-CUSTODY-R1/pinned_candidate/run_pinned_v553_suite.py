"""Run the PINNED V553 consumer-contract suite against staged, blob-verified bytes only.

Custody guard: this host has an AMBIENT data/ddm_build_copy/ that can shadow the
pinned tree. sys.path is pinned and every resolved native module is asserted to
live inside this return before the suite is collected.
"""
import os, sys
from pathlib import Path

RET = Path(__file__).resolve().parent
NATIVE = RET / "native"
AMBIENT = Path("/Users/matthewsmith/Desktop/Rawlsing")

# hard-pin: drop every path that is not the pinned tree or the stdlib
sys.path[:] = [p for p in sys.path
               if p and not str(Path(p).resolve()).startswith(str(AMBIENT))]
sys.path.insert(0, str(NATIVE))

import data.ddm_build_copy as _probe  # noqa: E402
assert str(_probe.__file__).startswith(str(NATIVE)), f"AMBIENT DATA LEAK: {_probe.__file__}"

import pytest  # noqa: E402
rc = pytest.main(["-q", "-p", "no:cacheprovider",
                  str(NATIVE / "data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py")])
print("PINNED_V553_CONSUMER_CONTRACT_EXIT", rc)
sys.exit(rc)
