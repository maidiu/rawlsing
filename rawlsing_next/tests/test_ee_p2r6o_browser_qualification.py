from __future__ import annotations
import importlib.util
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
DRIVER=ROOT/"WORKER_RETURNS/EE-P2R6O/09_AB_OWNER_SEAM_REQUALIFICATION_TEST.py"

def test_ee_p2r6o_governed_browser_requalification():
    spec=importlib.util.spec_from_file_location("ee_p2r6o_governed_driver",DRIVER)
    assert spec is not None and spec.loader is not None
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    module.test_r6o_ab_owner_seam_requalification()
