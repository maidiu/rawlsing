"""Reproduce the review using exact Git objects in a temporary source directory."""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

PIN = "895980397cc0533043c7ca0e493ebbb455666c1e"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
with tempfile.TemporaryDirectory(prefix="p02r-c02j-") as directory:
    archive = subprocess.check_output(["git", "archive", PIN, "rawlsing_next"], cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        source.extractall(directory)
    env = dict(os.environ, PYTHONPATH=directory, PYTHONDONTWRITEBYTECODE="1")
    commands = {
        "owners": [sys.executable, "-m", "pytest", "-q",
            "rawlsing_next/tests/test_pre553_learned_product_lifecycle.py",
            "rawlsing_next/tests/test_pre553_learned_product_release.py",
            "rawlsing_next/tests/test_pre553_empirical_objects_authority.py"],
        "baseline": [sys.executable, "-m", "rawlsing_next.repro.c02j_owner_court"],
        "review": [sys.executable, str(HERE / "review.py")],
    }
    exits = {}
    for name, command in commands.items():
        result = subprocess.run(command, cwd=directory, env=env, text=True, capture_output=True)
        (HERE / (name + (".txt" if name == "owners" else ".jsonl"))).write_text(result.stdout)
        if result.stderr:
            (HERE / (name + ".stderr.txt")).write_text(result.stderr)
        exits[name] = result.returncode
    (HERE / "exits.json").write_text(json.dumps(exits, indent=2) + "\n")
    print(json.dumps(exits, sort_keys=True))
    # The review intentionally exits 1 when interface requirements fail.
    sys.exit(1 if any(exits.values()) else 0)
