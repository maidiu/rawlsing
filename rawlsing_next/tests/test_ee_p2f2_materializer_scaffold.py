import os
import runpy
from pathlib import Path


def test_ee_p2f2_materialization_scaffold():
    # Temporary court-only extraction scaffold. The governed materializer itself
    # remains under WORKER_RETURNS and performs no source/outcome access.
    os.environ["PYTHONPATH"] = str(Path.cwd())
    ns = runpy.run_path("WORKER_RETURNS/EE-P2F2/09_verify_ee_p2f2_lock2.py")
    ns["test_ee_p2f2_lock2_materialization"]()
    raise AssertionError("EE_P2F2_EXTRACTION_ONLY__MATERIALIZER_AND_FRESH_PROCESS_REPLAY_PASSED")
