"""Test bootstrap and shared fixtures for the BP2P4J joined court."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

RETURN = Path(__file__).resolve().parents[1]
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

import bp2p4  # noqa: E402

bp2p4.install()


def pytest_configure(config):  # noqa: ARG001
    bp2p4.verify_sources()


@pytest.fixture(scope="session")
def intact(tmp_path_factory):
    """One real BP2 joined run shared by read-only courts."""
    from bp2p4 import reunion

    root = tmp_path_factory.mktemp("bp2_intact") / "joined"
    return reunion.build_fresh(root)


@pytest.fixture(scope="session")
def origin_literal():
    """The surviving literal BP2 origin runtime, when present."""
    from bp2p4 import reunion

    runtime = reunion.origin_runtime_available()
    if runtime is None:
        pytest.skip("BP2_ORIGIN_RUNTIME_ABSENT (local-only literal cross-check)")
    evidence = RETURN / "vendor" / "bp2" / "evidence" / "joined_positive_receipt.json"
    return reunion.load_origin_literal(runtime, evidence_path=evidence)
