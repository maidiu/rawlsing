from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
PINNED = HERE / "_pinned"
REPORT = HERE.parent
REPO = Path(os.environ.get("P53T_REPO_ROOT", REPORT.parents[1])).resolve()
RECEIPTS = REPORT / "receipts"
RECEIPTS.mkdir(exist_ok=True)

for path in (
    PINNED / "j42/runtime",
    PINNED / "j42/vendor/p41/runtime",
    PINNED,
    REPO,
):
    text = str(path)
    if text in sys.path:
        sys.path.remove(text)
    sys.path.insert(0, text)

PINNED_BLOBS = {
    "g50/enumerate.py": ("d379bafe36b8d89da27ea5bf33614d33aca7f2d2", "f610ef2dea39519a51a5b57fd35bbe245fb9dc9b"),
    "g50/types.py": ("d379bafe36b8d89da27ea5bf33614d33aca7f2d2", "a376edad00a3b40f69fc3a87c83658b4406bc67b"),
    "g50/native_map.py": ("d379bafe36b8d89da27ea5bf33614d33aca7f2d2", "b7a0d3193667013b81dae9eeeef07d26da88fcc3"),
    "g50/fixture.py": ("d379bafe36b8d89da27ea5bf33614d33aca7f2d2", "41b6191cdd62a387800fd76f36ceb6b6f5a2fdcf"),
    "j42/runtime/j42_join.py": ("f53cb0d2bce52640268c844c398bbd8007d28edc", "40f1e9f69fafff37f6bc44474b0189543d4997b3"),
    "j42/vendor/p41/runtime/p41_service.py": ("f53cb0d2bce52640268c844c398bbd8007d28edc", "7d428106c79bcc56973f7c0044fc273a2b354554"),
    "j42/vendor/p41/runtime/vendor/product/nonparent.py": ("f53cb0d2bce52640268c844c398bbd8007d28edc", "2181b832d3c4376d4b9428e13f4354f273be8f32"),
    "b53h/09_trusted_oracle_prefilter.py": ("026a6ba3075817b7f0370619843ee7227967bc8e", None),
    "b53h/10_test_trusted_oracle_prefilter.py": ("026a6ba3075817b7f0370619843ee7227967bc8e", None),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_blob(path: str, commit: str | None = None) -> str:
    import subprocess
    args = ["git", "-C", str(REPO), "rev-parse", f"{commit}:{path}"] if commit else [
        "git", "-C", str(REPO), "hash-object", str(PINNED / path)]
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()


def dump_receipt(name: str, payload) -> Path:
    import json
    path = RECEIPTS / name
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO


@pytest.fixture(scope="session")
def fresh_e41(tmp_path_factory):
    import json
    import subprocess
    out = tmp_path_factory.mktemp("e41") / "e41_fresh_run.json"
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(
        [sys.executable, str(PINNED / "j42/runtime/e41_driver.py"), "--out", str(out)],
        cwd=str(REPO), env=env, capture_output=True, text=True, timeout=600)
    if proc.returncode != 0:
        raise RuntimeError(proc.stdout[-4000:] + proc.stderr[-4000:])
    payload = json.loads(out.read_text())
    dump_receipt("e41_fresh_run.json", payload)
    return payload


@pytest.fixture(scope="session")
def prepared_p41():
    import j42_join  # noqa: F401  installs the staged P41 apparatus
    from fixture import prepare
    return prepare()
