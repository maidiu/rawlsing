from __future__ import annotations
import json, sys
from pathlib import Path
import pytest
RETURN_ROOT = Path(__file__).resolve().parents[1]
REPO = RETURN_ROOT.parents[1]
for p in (RETURN_ROOT, REPO):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
from frozen_a42.frozen_a41.a41.gitpreimage import GitPreimage
from b43 import frontier, feeder

@pytest.fixture(scope="session")
def gp(): return GitPreimage(REPO)
@pytest.fixture(scope="session")
def fr(gp): return frontier.load_frontier(gp)
@pytest.fixture(scope="session")
def docket(fr): return frontier.decision_docket(fr)
