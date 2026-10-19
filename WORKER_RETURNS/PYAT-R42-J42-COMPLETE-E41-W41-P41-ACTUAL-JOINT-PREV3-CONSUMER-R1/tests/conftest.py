"""J42 test bootstrap: one fresh isolated producer run per session."""
import os
import subprocess
import sys
from pathlib import Path

import pytest

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

PACKET = RUNTIME.parent
REPO = PACKET.parents[1]
sys.path.insert(0, str(REPO))

import j42_join as J  # noqa: E402


def run_driver(script, out_path):
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run([sys.executable, str(RUNTIME / script), "--out",
                           str(out_path)], env=env, cwd=str(REPO),
                          capture_output=True, text=True, timeout=1800)
    assert proc.returncode == 0, proc.stdout[-1500:] + proc.stderr[-1500:]
    import json
    return json.loads(Path(out_path).read_text())


@pytest.fixture(scope="session")
def fresh(tmp_path_factory):
    directory = tmp_path_factory.mktemp("j42fresh")
    e41 = run_driver("e41_driver.py", directory / "e41.json")
    w41 = run_driver("w41_driver.py", directory / "w41.json")
    return e41, w41


@pytest.fixture(scope="session")
def joined(fresh):
    e41, w41 = fresh
    return J.build_join(e41, w41)


@pytest.fixture(scope="session")
def reverse_receipt(fresh):
    e41, w41 = fresh
    return J.reverse_join(e41, w41)


@pytest.fixture(scope="session")
def p41_rows_hash():
    from fixture import prepare
    prepared = prepare()
    return prepared.native_provider.world["rows_hash"]
