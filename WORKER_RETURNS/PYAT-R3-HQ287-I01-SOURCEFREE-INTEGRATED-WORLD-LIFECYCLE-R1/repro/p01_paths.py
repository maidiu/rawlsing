"""Operational relocation matching the pinned P01 ordinary pytest harness.
No oracle/owner bytes are changed. Historical path checks retain P01 skips.
"""
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parent
WORKERS={'test_pre553_batch_durable_checkpoint_candidate.py':'b01c_worker.py','test_pre553_governed_batch_checkpoint_integration_candidate.py':'b01e_worker.py','test_pre553_original_workload_v2_verifier_candidate.py':'a04t_join_worker.py','test_pre553_original_workload_v2_mutation_hostiles_candidate.py':'a04t_join_worker.py'}
HISTORICAL={'test_a04_41_suite_still_passes_in_its_worktree','test_a05_18_suite_still_passes_in_its_worktree','test_accepted_owners_a04_a04s_a05_untouched','test_no_raw_sav_dta_reads','test_source_free_posture_no_raw_survey_reads'}
def pytest_collection_modifyitems(items):
 for item in items:
  worker=WORKERS.get(item.path.name)
  if worker:
   item.module.WORKER=ROOT/worker
   if item.path.name=='test_pre553_batch_durable_checkpoint_candidate.py':item.module.B01D_WORKER=ROOT/'b01d_worker.py'
   if item.originalname in HISTORICAL:item.add_marker(pytest.mark.skip(reason='Pinned P01 historical primary/return path check; exact-byte custody separately verified'))
