"""Run isolated historical/ported courts; preserve real exits, complete logs/JUnit."""
import hashlib,json,os,pathlib,subprocess,sys,time,xml.etree.ElementTree as ET
R=pathlib.Path(__file__).resolve().parents[1];P=R/'pinned';ROOT=R.parents[1]
MODES={
 'historical_p2':(P/'predecessors/p2/repro/test_wg0p2_repair.py',[P/'predecessors/p2/repro']),
 'historical_p3':(P/'predecessors/p3/tests/test_wg0p3_repair.py',[P/'predecessors/p3/repro']),
 'historical_k_on_p3':(P/'predecessors/k/repro/test_wg0k_full_module_hostiles.py',[P/'predecessors/p3/repro']),
 'historical_j':(P/'predecessors/j/tests/test_independent.py',[P/'predecessors/p2/repro',P/'predecessors/j/repro']),
 'ported_j':(R/'tests/test_wg0j_adapter_v1.py',[R/'repro']),
 'ported_k':(R/'tests/test_wg0k_adapter_v1.py',[R/'repro']),
 'wg0p4':(R/'tests/test_wg0p4.py',[R/'repro']),
}
def clean(t):
    return t.replace(str(ROOT),'<WORKTREE>').replace(str(pathlib.Path.home()),'<HOME>')
def run(name,argv,mods):
    env=dict(os.environ,PYTHONPATH=os.pathsep.join(map(str,[P,*mods])),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    started=time.time();pr=subprocess.run(argv,cwd=R,env=env,text=True,capture_output=True)
    raw=R/'runtime/raw_logs';raw.mkdir(parents=True,exist_ok=True);(raw/(name+'.stdout')).write_text(pr.stdout+pr.stderr)
    (R/'observations'/(name+'.stdout')).write_text(clean(pr.stdout+pr.stderr))
    result={'name':name,'command':[clean(x) for x in argv],'cwd':'<RETURN>','pythonpath':[clean(str(p)) for p in [P,*mods]],'exit':pr.returncode,'seconds':time.time()-started,'log_redaction':'Only personal filesystem root aliases; otherwise complete real stdout/stderr. Unredacted local execution output kept ignored runtime/raw_logs.','source':'Exact frozen sources for historical modes; separately versioned implementer compatibility adapters for ported modes.'}
    result['candidate_sha256']=hashlib.sha256((R/'repro/wg0p4_workload.py').read_bytes()).hexdigest()
    result['test_file_sha256']=hashlib.sha256(pathlib.Path(argv[argv.index('-c')+2]).read_bytes()).hexdigest() if '-c' in argv else None
    xml=R/'observations'/(name+'.xml')
    if xml.exists():
        tree=ET.parse(xml);cases=tree.findall('.//testcase');result.update(tests=len(cases),failures=len(tree.findall('.//failure')),errors=len(tree.findall('.//error')),skips=len(tree.findall('.//skipped')))
        xml.write_text(clean(xml.read_text()))
    (R/'observations'/(name+'.terminal.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result));print((pr.stdout+pr.stderr)[-1500:]);return pr.returncode
if __name__=='__main__':
    for name in sys.argv[1:]:
        if name=='prepare_native':
            run('prepare_native',[sys.executable,str(R/'repro/prepare_evidence.py')],[R/'repro']);continue
        if name=='prepare_historical_j':
            target=P/'predecessors/j';(target/'observations').mkdir(exist_ok=True)
            for job,args in [('probe',[]),('cold',['orchestrate'])]:run('historical_j_'+job,[sys.executable,str(target/'repro'/f'{job}.py'),*args],[P/'predecessors/p2/repro',target/'repro'])
            continue
        target,mods=MODES[name]
        run(name,[sys.executable,'-m','pytest','-c',str(R/'pytest.ini'),str(target),'-vv','--tb=short','--junitxml='+str(R/'observations'/(name+'.xml'))],mods)
