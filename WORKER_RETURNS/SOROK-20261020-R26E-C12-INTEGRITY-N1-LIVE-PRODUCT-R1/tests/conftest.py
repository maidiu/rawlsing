import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
TARGET = RET / "runtime" / "target"
N1 = RET / "runtime" / "n1" / "source"
for _path in (str(RET), str(TARGET), str(N1)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import bp2p4  # noqa: E402

bp2p4.install()

import pytest  # noqa: E402


@pytest.fixture(scope="session")
def artifacts(tmp_path_factory):
    from bp2p4 import reunion

    root = tmp_path_factory.mktemp("r26e_artifacts") / "bp2"
    return reunion.build_fresh(root)
