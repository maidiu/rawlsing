"""A41 test configuration: resolve the return root and shared fixtures."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

RETURN_ROOT = Path(__file__).resolve().parents[1]
if str(RETURN_ROOT) not in sys.path:
    sys.path.insert(0, str(RETURN_ROOT))

from a41.gitpreimage import GitPreimage  # noqa: E402
from a41 import receipt_bank, estate_assessor  # noqa: E402

REPO = RETURN_ROOT.parents[1]


def _load(name):
    return json.loads((RETURN_ROOT / "evidence" / name).read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def return_root():
    return RETURN_ROOT


@pytest.fixture(scope="session")
def gp():
    return GitPreimage(REPO)


@pytest.fixture(scope="session")
def scope():
    return _load("expected_scope_frozen.json")


@pytest.fixture(scope="session")
def bank():
    return _load("receipt_bank_frozen.json")


@pytest.fixture(scope="session")
def ingested(scope, bank, gp):
    return receipt_bank.ingest_bank(bank, gp, expected_scope=scope)


@pytest.fixture(scope="session")
def accounting(scope, ingested):
    return estate_assessor.assess(scope, ingested)
