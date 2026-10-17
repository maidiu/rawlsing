"""Independent per-module preimage guard and pytest custody receipt."""
import hashlib
import importlib.abc
import importlib.machinery
import json
import os
import marshal
from pathlib import Path
import sys

RET = Path(__file__).resolve().parent
STAGE = RET/'pinned_candidate'
NATIVE = STAGE/'native'
MANIFEST = json.loads((RET/'evidence/staged_source_manifest.json').read_text())
EXPECTED = {(STAGE/r['relative']).resolve(): r for r in MANIFEST}
AUDIT = []

def verify(name, path, phase='before_exec'):
    path = Path(path).resolve()
    row = EXPECTED.get(path)
    if row is None:
        raise ImportError(f'UNPINNED_PROJECT_MODULE {name}: {path}')
    b = path.read_bytes()
    sha = hashlib.sha256(b).hexdigest()
    oid = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    if sha != row['sha256'] or oid != row['git_blob_sha1']:
        raise ImportError(f'PREIMAGE_MISMATCH {name}: {path}')
    AUDIT.append({'module':name,'__file__':str(path),'sha256':sha,'git_blob_sha1':oid,'phase':phase})

class Guard(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if not (fullname == 'data' or fullname.startswith('data.') or fullname == 't9b_temporal'):
            return None
        spec = importlib.machinery.PathFinder.find_spec(fullname,path)
        if spec is None: return None
        if spec.origin and spec.origin not in {'namespace','built-in','frozen'}:
            verify(fullname,spec.origin)
        elif fullname == 'data':
            locations = [str(Path(p).resolve()) for p in spec.submodule_search_locations]
            assert set(locations) == {str(NATIVE/'data')}, locations
            AUDIT.append({'module':fullname,'namespace_locations':locations,'phase':'before_exec'})
        return spec

def install():
    os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'
    sys.dont_write_bytecode=True
    sys.path[:] = [str(STAGE),str(NATIVE)]+[p for p in sys.path if p and 'Rawlsing' not in p and 'rawlsing' not in p]
    for name,module in list(sys.modules.items()):
        if name=='data' or name.startswith('data.') or name=='t9b_temporal':
            path=getattr(module,'__file__',None)
            if path: verify(name,path,phase='preloaded_before_collection')
            elif name=='data':
                assert set(module.__path__)=={str(NATIVE/'data')}
    sys.meta_path.insert(0,Guard())
    def before_exec(event,args):
        if event=='exec':
            path=Path(args[0].co_filename)
            if path.is_absolute() and path.resolve().is_relative_to(STAGE):
                verify('audit.exec:'+args[0].co_name,path)
    sys.addaudithook(before_exec)

class Receipt:
    def __init__(self): self.tests=[]; self.rootdir=None; self.configfile=None
    def pytest_configure(self,config):
        self.rootdir=str(config.rootpath);self.configfile=str(config.inipath)
        assert config.rootpath.resolve()==RET, self.rootdir
    def pytest_runtest_logreport(self,report):
        if report.when=='call' or report.failed or report.skipped:
            self.tests.append({'nodeid':report.nodeid,'phase':report.when,'outcome':report.outcome})

def main():
    suite=sys.argv[1]
    (RET/'scratch').mkdir(exist_ok=True)
    install()
    import pytest
    receipt=Receipt()
    tests={'author':str(STAGE/'test_t9b_temporal.py'),
           'legacy':str(NATIVE/'data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py'),
           'independent':str(RET/'tests/test_independent_clock_custody.py')}
    rc=pytest.main(['-q','-c',str(RET/'pytest.ini'),'--rootdir',str(RET),'-p','no:cacheprovider',
                    '--basetemp',str(RET/'scratch'/suite),'--junitxml',str(RET/'junit'/f'{suite}.xml'),tests[suite]],plugins=[receipt])
    resolved=[]
    for name,module in sorted(sys.modules.items()):
        if name=='data' or name.startswith('data.') or name=='t9b_temporal':
            path=getattr(module,'__file__',None)
            if path:
                verify(name,path,phase='after_execution')
                resolved.append({'module':name,'__file__':str(Path(path).resolve()),'sha256':EXPECTED[Path(path).resolve()]['sha256'],
                                 'git_blob_sha1':EXPECTED[Path(path).resolve()]['git_blob_sha1']})
    record={'suite':suite,'exit':int(rc),'rootdir':receipt.rootdir,'configfile':receipt.configfile,
            'actual_test_reports':receipt.tests,'imports_before_exec':AUDIT,'all_loaded_project_modules':resolved,
            'plugins_autoload_disabled':True,'environment':'direct local Python; no remote model executor'}
    all_modules=[]; cache={}
    for name,module in sorted(sys.modules.items()):
        spec=getattr(module,'__spec__',None)
        path=getattr(module,'__file__',None)
        item={'module':name,'spec_origin':getattr(spec,'origin',None),'__file__':path}
        if path and Path(path).is_file():
            resolved_path=str(Path(path).resolve())
            if resolved_path not in cache:
                b=Path(path).read_bytes()
                cache[resolved_path]={'resolved_file':resolved_path,'bytes':len(b),
                    'sha256':hashlib.sha256(b).hexdigest(),
                    'git_blob_sha1_NUL_preimage':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
            item.update(cache[resolved_path])
            item['pin_status']='CANDIDATE_EXPECTED_PREIMAGE' if Path(path).resolve() in EXPECTED else 'RUNTIME_INVENTORY_ONLY'
        elif not path:
            item['pin_status']='BUILTIN_FROZEN_OR_NAMESPACE_NO_FILE'
        if getattr(spec,'origin',None)=='frozen':
            loader=getattr(spec,'loader',None)
            try:
                item['frozen_marshaled_code_sha256']=hashlib.sha256(marshal.dumps(loader.get_code(name))).hexdigest()
            except Exception as exc: item['frozen_code_hash_limit']=type(exc).__name__
        all_modules.append(item)
    record['all_imported_module_preimages']=all_modules
    record['runtime_inventory_limit']='Third-party/stdlib file preimages are measured, not independently accepted source pins; frozen executed-code hashes are distinguished from disk files.'
    (RET/'evidence'/f'{suite}_execution.json').write_text(json.dumps(record,indent=2)+'\n')
    print(f'T9I_{suite}_EXIT={int(rc)} VERIFIED_PROJECT_MODULES={len(resolved)}')
    sys.exit(rc)

if __name__=='__main__':main()
