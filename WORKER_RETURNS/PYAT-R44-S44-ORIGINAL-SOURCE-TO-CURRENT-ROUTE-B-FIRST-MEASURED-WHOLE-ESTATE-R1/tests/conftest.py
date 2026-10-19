from __future__ import annotations
import json, sys
from pathlib import Path
import pytest
RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
for p in (RETURN, REPO):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
from frozen_a42.frozen_a41.a41.gitpreimage import GitPreimage
from s44 import historical, handoff

@pytest.fixture(scope="session")
def gp(): return GitPreimage(REPO)
@pytest.fixture(scope="session")
def hist(gp): return historical.verify_historical(gp)
@pytest.fixture(scope="session")
def ho(gp, hist): return handoff.handoff(gp, hist)
