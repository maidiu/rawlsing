"""Run exact V2 tests with the exact worker relocated to the P01 return.

Old primary-worktree/branch-specific checks are explicitly deselected; exact
Git blob checks are supplied separately by the P01 manifest court.
"""
from pathlib import Path
import sys
root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root))
import rawlsing_next.tests.test_pre553_original_workload_v2_verifier_candidate as T
T.WORKER = Path(__file__).resolve().parent / 'a04t_join_worker.py'
import rawlsing_next.tests.test_pre553_original_workload_v2_mutation_hostiles_candidate as M
M.WORKER = T.WORKER
import pytest
exclude = ['test_a04_41_suite_still_passes_in_its_worktree',
           'test_a05_18_suite_still_passes_in_its_worktree',
           'test_accepted_owners_a04_a04s_a05_untouched',
           'test_no_raw_sav_dta_reads']
raise SystemExit(pytest.main(['-q', '--import-mode=importlib', '-k',
    ' and '.join('not '+name for name in exclude),
    'rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py',
    'rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py']))
