"""Test bootstrap for the BP2 joined producer court.

Only this return subtree is on ``sys.path`` for the new code; the exact pinned
upstream closures are added by ``bp2_joined.bootstrap``. No ambient pytest
configuration is relied on: every run in this return uses ``tests/pytest.ini``.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import bp2_joined  # noqa: E402

bp2_joined.install()


def pytest_configure(config):  # noqa: ARG001
    bp2_joined.bootstrap.verify_sources()
