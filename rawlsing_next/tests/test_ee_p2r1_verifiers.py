from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _run(path: str):
    env = dict(os.environ)
    root = str(Path.cwd())
    env["PYTHONPATH"] = root + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    completed = subprocess.run(
        [sys.executable, path],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    assert completed.returncode == 0, completed.stdout + "\n" + completed.stderr
    return completed.stdout


def test_wvs_lock2_runtime_catalog_fresh_process():
    out = _run("WORKER_RETURNS/EE-P2R1/01_verify_wvs7_runtime_catalog.py")
    assert "PASS__EXACT_F2_PREIMAGES_MATERIALIZED__LOCK2_FRONTIER_RECOMPILED" in out


def test_full_35_wave_contract_calibration_fresh_process():
    out = _run("WORKER_RETURNS/EE-P2R1/02_verify_35_wave_calibration.py")
    assert "PASS__GENERIC_EXECUTION_SEAM_CALIBRATED_AGAINST_GOVERNED_CLOSED_35_WAVES" in out


def test_lits_c_real_binding_materialization_fresh_process():
    out = _run("WORKER_RETURNS/EE-P2R1/03_materialize_lits_c_real_bindings.py")
    assert "PASS__REAL_ACCEPTED_ROUTE_C_CACC1_CACC2_BINDINGS_MATERIALIZED" in out
    assert '"role_count": 19' in out


def test_adapter_matrix_and_wvs_c_disposition_fresh_process():
    out = _run("WORKER_RETURNS/EE-P2R1/04_verify_adapter_matrix.py")
    assert "PASS__LAWFUL_FINAL_P2_CELLS_BINDABLE__WVS_C_PORTABILITY_FAILURE_PRESERVED" in out
    assert "WVS7_C__CURRENT_PORTABILITY_FAILURE" in out
