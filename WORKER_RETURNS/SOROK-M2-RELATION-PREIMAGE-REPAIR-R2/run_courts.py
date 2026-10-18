"""Execute supplied bytes and frozen compatibility courts with explicit imports."""
from pathlib import Path
import os,sys,subprocess,json,hashlib,tarfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
M2='5c2fbe14ccfa5027becfabc682206a1e61aaf986'
M3='49dfcb30971310756a12f659961600d9f2eb4a11'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def stage(commit,path,dest):
    b=git('show',commit+':'+path);dest.parent.mkdir(parents=True,exist_ok=True)
    blob=git('rev-parse',commit+':'+path).decode().strip()
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
    if dest.exists():assert dest.read_bytes()==b
    else:dest.write_bytes(b)
    return dict(commit=commit,path=path,git_blob_sha1=blob,sha256=hashlib.sha256(b).hexdigest(),local=str(dest.relative_to(ROOT)))
def main():
    out=ROOT/'evidence';out.mkdir(exist_ok=True)
    original=ROOT/'.runtime/original_m2';original.mkdir(parents=True,exist_ok=True)
    sources=[stage(M2,'WORKER_RETURNS/SOROK-V2-HQ328-M2-M1-SOURCE-TIME-REPAIR-R1/kernel.py',original/'kernel.py'),stage(M3,'WORKER_RETURNS/SOROK-V2-HQ329-M3-M2-INDEPENDENT-SCIENCE-R1/05_SOURCE_PREIMAGE_RED_REPRODUCER.py',ROOT/'frozen_m3/test_original_preimage.py')]
    for a,dest in [('M1_original_exact_7e91c198.tar.gz','m1'),('I2_strict_exact_19f1e86a.tar.gz','i2')]:
        path='WORKER_RETURNS/SOROK-V2-HQ328-M2-M1-SOURCE-TIME-REPAIR-R1/frozen_inputs/'+a
        archive=ROOT/'m2_patch/frozen_inputs'/a;assert archive.read_bytes()==git('show',M2+':'+path)
        sources.append(dict(commit=M2,path=path,git_blob_sha1=git('rev-parse',M2+':'+path).decode().strip(),sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),local=str(archive.relative_to(ROOT))))
        with tarfile.open(archive) as t:
            for item in t.getmembers():
                p=ROOT/'.runtime'/dest/item.name
                assert not item.issym() and not item.islnk() and p.resolve().is_relative_to((ROOT/'.runtime'/dest).resolve())
                if item.isfile():
                    b=t.extractfile(item).read();p.parent.mkdir(parents=True,exist_ok=True)
                    if p.exists():assert p.read_bytes()==b
                    else:p.write_bytes(b)
    (ROOT/'source_refs.json').write_text(json.dumps(sources,indent=2)+'\n')
    runs=[]
    bootstrap="import sys,json,hashlib;sys.path.insert(0,sys.argv[1]);import kernel,pytest;print('LOADED_KERNEL '+json.dumps({'file':kernel.__file__,'sha256':hashlib.sha256(open(kernel.__file__,'rb').read()).hexdigest()}),flush=True);sys.exit(pytest.main(sys.argv[2:]))"
    patch=ROOT/'m2_patch';m1=ROOT/'.runtime/m1';i2=ROOT/'.runtime/i2/test_i2_strict.py'
    plans=[('M2_41',patch,patch/'test_m2.py',0),('M3_lawful_32',patch,patch/'test_m3_independent.py',0),('packaged_M3_three',patch,patch/'test_m3_unresolved.py',0),('additional_15',patch,patch/'test_source_preimages.py',0),('exact_git_M3_patch',patch,ROOT/'frozen_m3/test_original_preimage.py',0),('exact_git_M3_original',original,ROOT/'frozen_m3/test_original_preimage.py',1),('M1_original',m1,m1/'test_kernel.py',0),('I2_on_M1',m1,i2,1),('M1_on_original_M2',original,m1/'test_kernel.py',1),('I2_on_original_M2',original,i2,1),('M1_on_patch',patch,m1/'test_kernel.py',1),('I2_on_patch',patch,i2,1),('local_hostile',patch,ROOT/'test_local_hostile.py',0)]
    for name,kernel,tests,expected in plans:
        args=[sys.executable,'-c',bootstrap,str(kernel),'-q',str(tests),'--import-mode=importlib','--junitxml='+str(out/(name+'.xml'))]
        p=subprocess.run(args,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
        (out/(name+'.log')).write_text(p.stdout+p.stderr)
        row=dict(label=name,command=args,exit=p.returncode,expected_exit=expected)
        tree=ET.parse(out/(name+'.xml'));row['counts']={k:sum(int(n.get(k,0)) for n in tree.iter('testsuite')) for k in ('tests','failures','errors','skipped')}
        runs.append(row);(ROOT/'execution_receipts.json').write_text(json.dumps(runs,indent=2)+'\n')
        print(name,p.returncode,row['counts'],flush=True)
        assert p.returncode==expected,(name,p.stdout,p.stderr)
    args=[sys.executable,'-c',bootstrap,str(patch),'-q',str(ROOT/'test_relation_custody.py'),'--import-mode=importlib','--junitxml='+str(out/'relation_regressions.xml')]
    p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True)
    (out/'relation_regressions.log').write_text(p.stdout+p.stderr)
    tree=ET.parse(out/'relation_regressions.xml')
    runs.append(dict(label='relation_regressions',command=args,exit=p.returncode,expected_exit=0,
        counts={k:sum(int(n.get(k,0)) for n in tree.iter('testsuite')) for k in ('tests','failures','errors','skipped')}))
    (ROOT/'execution_receipts.json').write_text(json.dumps(runs,indent=2)+'\n')
    assert p.returncode==0,(p.stdout,p.stderr)
    subprocess.run([sys.executable,str(ROOT/'record_relation_probe.py')],cwd=ROOT,check=True)
if __name__=='__main__':main()
