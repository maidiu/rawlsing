from __future__ import annotations
import json, sys
from pathlib import Path
import pytest
RETURN_ROOT = Path(__file__).resolve().parents[1]
if str(RETURN_ROOT) not in sys.path:
    sys.path.insert(0, str(RETURN_ROOT))
from frozen_a41.a41.gitpreimage import GitPreimage
from a42 import core
REPO = RETURN_ROOT.parents[1]

@pytest.fixture(scope="session")
def gp(): return GitPreimage(REPO)
@pytest.fixture(scope="session")
def scope(gp): return core.load_scope(gp)
@pytest.fixture(scope="session")
def bank():
    return json.loads((RETURN_ROOT/"evidence"/"r41_receipt_bank_v2.json").read_text())
@pytest.fixture(scope="session")
def a41(gp): return core.a41_receipts_v2(gp)
@pytest.fixture(scope="session")
def r41(bank, gp, scope): return core.ingest_r41_bank(bank, gp, scope)
@pytest.fixture(scope="session")
def receipts(a41, r41): return a41 + r41
@pytest.fixture(scope="session")
def w41reg(gp): return core.load_w41_register(gp)
@pytest.fixture(scope="session")
def old_manifest(gp):
    return json.loads(gp.blob_at(core.A41_COMMIT, core.A41_DIR+"/estate_acceptance_manifest.json"))
@pytest.fixture(scope="session")
def acc(scope, receipts, w41reg, old_manifest): return core.assess_v2(scope, receipts, w41reg, old_manifest)
