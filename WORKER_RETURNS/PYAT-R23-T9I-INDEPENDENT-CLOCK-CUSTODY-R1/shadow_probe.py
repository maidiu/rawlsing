"""Observe ambient module selection, refusing BEFORE unverified execution."""
import importlib.abc
import importlib.machinery
import json
from pathlib import Path
import sys
import os

RET=Path(__file__).resolve().parent
NATIVE=RET/'pinned_candidate/native'
AMBIENT=Path('/Users/matthewsmith/Desktop/Rawlsing')
mode=sys.argv[1]
record={'mode':mode,'cwd':str(Path.cwd()),'selections':[],'ambient_execution_permitted':False}
sys.dont_write_bytecode=True
os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'
sys.path.insert(0,str(NATIVE))

class RefuseAmbient(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname,path=None,target=None):
        if fullname=='data' or fullname.startswith('data.'):
            spec=importlib.machinery.PathFinder.find_spec(fullname,path)
            if spec and spec.origin:
                origin=str(Path(spec.origin).resolve())
                record['selections'].append({'module':fullname,'origin':origin})
                if not Path(origin).is_relative_to(NATIVE):
                    record['blocked_untrusted_origin']=origin
                    raise ImportError('T9I_BLOCK_BEFORE_AMBIENT_EXECUTION '+origin)
            return spec

class ConfigReceipt:
    def pytest_configure(self,config):
        record['rootdir']=str(config.rootpath);record['configfile']=str(config.inipath)
        if mode=='documented-bare-relative':
            parent=importlib.machinery.PathFinder.find_spec('data')
            child=importlib.machinery.PathFinder.find_spec('data.ddm_build_copy',parent.submodule_search_locations)
            record['selected_package_without_execution']=child.origin
            if not Path(child.origin).is_relative_to(NATIVE):
                record['blocked_untrusted_origin']=child.origin
                raise pytest.UsageError('T9I_REFUSE_AMBIENT_BEFORE_COLLECTION '+child.origin)

sys.meta_path.insert(0,RefuseAmbient())
import pytest
args=['-q','-p','no:cacheprovider']
if mode=='ambient-config-reenactment': args+=['-c',str(AMBIENT/'pytest.ini')]
args+=[('data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py' if mode=='documented-bare-relative'
        else str(NATIVE/'data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py'))]
record['argv']=list(args)
rc=pytest.main(args,plugins=[ConfigReceipt()])
record['exit']=int(rc)
(RET/'evidence'/f'shadow_{mode}.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
sys.exit(rc)
