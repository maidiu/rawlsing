"""Reject ambient module selection before executing any ambient project source."""
import importlib.machinery
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
STAGE = ROOT/'pinned_candidate/native'
sys.path.insert(0,str(ROOT/'.runtime'))
os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
sys.dont_write_bytecode = True
import pytest

# Controlled reenactment of a repository-prepending ambient pytest config. The
# original Phase A records also retain the then-existing actual ambient config.
config = ROOT/'scratch/ambient_pytest.ini'
config.parent.mkdir(exist_ok=True)
config.write_text('[pytest]\npythonpath = '+str(REPO)+'\n')
sys.path.insert(0,str(STAGE))
record = dict(control='explicit ambient-config reenactment in current checkout',
              candidate_native_root=str(STAGE), cwd=str(REPO), ambient_execution_permitted=False,
              original_actual_environment_receipts='../evidence/shadow_*.json')

class Check:
    def pytest_configure(self,config):
        record.update(rootdir=str(config.rootpath), configfile=str(config.inipath))
        parent = importlib.machinery.PathFinder.find_spec('data')
        child = importlib.machinery.PathFinder.find_spec('data.ddm_build_copy', parent.submodule_search_locations)
        record['selected_package_without_execution'] = child.origin
        record['namespace_locations'] = list(parent.submodule_search_locations)
        record['ambient_selected'] = not Path(child.origin).resolve().is_relative_to(STAGE)
        if record['ambient_selected']:
            raise pytest.UsageError('T9R_REFUSE_AMBIENT_BEFORE_COLLECTION '+child.origin)

os.chdir(REPO)
args = ['-q','-p','no:cacheprovider','-c',str(config),
        'data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py']
record['argv'] = args
rc = pytest.main(args,plugins=[Check()])
record['exit'] = int(rc)
(ROOT/'evidence/shadow_ambient_reenactment.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
sys.exit(rc)
