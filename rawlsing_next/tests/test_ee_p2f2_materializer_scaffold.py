import runpy


def test_ee_p2f2_materialization_scaffold():
    ns = runpy.run_path("WORKER_RETURNS/EE-P2F2/09_verify_ee_p2f2_lock2.py")
    ns["test_ee_p2f2_lock2_materialization"]()
