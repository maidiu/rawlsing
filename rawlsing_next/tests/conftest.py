"""P01 relocations for exact imported test sources; no owner/test edits.

Excluded historical primary paths and branch-specific checks are reported as
SKIP under ordinary pytest. P01 supplies exact-object replacement courts.
"""
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
REPRO = ROOT / 'WORKER_RETURNS' / 'PYAT-HQ282-P01-V2-DURABLE-CONSUMER-INTEGRATION-R1' / 'repro'
WORKERS = {
    'test_pre553_batch_durable_checkpoint_candidate.py': 'b01c_worker.py',
    'test_pre553_governed_batch_checkpoint_integration_candidate.py': 'b01e_worker.py',
    'test_pre553_original_workload_v2_verifier_candidate.py': 'a04t_join_worker.py',
    'test_pre553_original_workload_v2_mutation_hostiles_candidate.py': 'a04t_join_worker.py',
}
HISTORICAL = {
    'test_a04_41_suite_still_passes_in_its_worktree',
    'test_a05_18_suite_still_passes_in_its_worktree',
    'test_accepted_owners_a04_a04s_a05_untouched',
    'test_no_raw_sav_dta_reads',
    'test_source_free_posture_no_raw_survey_reads',
}


def pytest_collection_modifyitems(items):
    for item in items:
        filename = item.path.name
        worker = WORKERS.get(filename)
        if worker:
            item.module.WORKER = REPRO / worker
            if filename == 'test_pre553_batch_durable_checkpoint_candidate.py':
                item.module.B01D_WORKER = REPRO / 'b01d_worker.py'
            if item.originalname in HISTORICAL:
                item.add_marker(pytest.mark.skip(reason='Historical primary/return path or branch-specific check; replaced by exact_manifest_court and portable A05 court'))
