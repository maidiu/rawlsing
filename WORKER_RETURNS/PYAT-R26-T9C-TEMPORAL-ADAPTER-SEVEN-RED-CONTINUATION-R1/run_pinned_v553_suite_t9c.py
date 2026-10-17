"""Run the INHERITED ORIGINAL V553 consumer-contract suite (8 tests) against the
minimal, byte-verified 22-source closure staged in THIS return.

This is the same custody shape as the accepted T9B
`run_pinned_v553_suite.py` (author commit edf3494b1b11cb71a78540aba950aa15da900c8a):
the ambient repository root has a `data/ddm_build_copy/` that can shadow the pinned
tree, so sys.path is pinned and the resolved package is asserted to live inside this
return before any collection.

The eight tests themselves are UNCHANGED native code. This return does not modify
any accepted V553 source.
"""
import sys
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

rc = pytest.main(["-q", "-p", "no:cacheprovider", "-p", "no:randomly",
                  "--rootdir", str(RET),
                  "-c", str(RET / "frozen_t9i_court/pytest_t9i_frozen.ini"),
                  f"--junitxml={RET / 'junit/inherited_original_v553_native_8.xml'}",
                  str(NATIVE / "data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py")])
print("INHERITED_ORIGINAL_V553_CONSUMER_CONTRACT_EXIT", rc)
sys.exit(rc)