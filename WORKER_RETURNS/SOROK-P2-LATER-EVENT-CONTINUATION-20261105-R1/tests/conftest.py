from __future__ import annotations

import sys
from pathlib import Path

import pytest

RETURN = Path(__file__).resolve().parents[1]
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from p2_continuation.bootstrap import load  # noqa: E402


@pytest.fixture(scope="session")
def shipped():
    return load()


@pytest.fixture(scope="session")
def positive_report(shipped, tmp_path_factory):
    from p2_continuation.continuation import run_positive

    state = tmp_path_factory.mktemp("p2-positive") / "state"
    return run_positive(state)


@pytest.fixture(scope="session")
def scheduled_report(shipped, tmp_path_factory):
    from p2_continuation.continuation import run_scheduled

    state = tmp_path_factory.mktemp("p2-scheduled") / "state"
    return run_scheduled(state)


@pytest.fixture(scope="session")
def cut_report(shipped, tmp_path_factory):
    from p2_continuation.continuation import run_cut_restore

    state = tmp_path_factory.mktemp("p2-cut-restore") / "state"
    return run_cut_restore(state)
