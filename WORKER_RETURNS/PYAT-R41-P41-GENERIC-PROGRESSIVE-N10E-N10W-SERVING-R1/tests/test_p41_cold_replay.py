"""P41 cold replay: two fresh interpreter processes produce the identical
progressive receipt content hash (and match the in-process hash)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from p41_service import P41Service

PACKET = Path(__file__).resolve().parents[1]
SCRIPT = PACKET / "tests/replay_receipt.py"
WORKTREE = PACKET.parents[1]


def test_two_fresh_processes_identical_receipt_hash():
    assert SCRIPT.is_file()
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    hashes = []
    for _ in range(2):
        proc = subprocess.run([sys.executable, str(SCRIPT)], env=env,
                              cwd=str(WORKTREE), capture_output=True, text=True,
                              timeout=600)
        assert proc.returncode == 0, proc.stderr[-2000:]
        hashes.append(proc.stdout.strip())
    assert hashes[0] == hashes[1]
    assert hashes[0] == P41Service().progressive()["content_hash"]
