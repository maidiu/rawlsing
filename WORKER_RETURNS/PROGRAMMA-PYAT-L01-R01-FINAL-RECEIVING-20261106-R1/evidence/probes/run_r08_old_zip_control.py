import hashlib, os, subprocess, sys
from pathlib import Path
ROOT=Path('/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/r01-cold-702')
EVID=Path('/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/r01-receive-evidence')
f=ROOT/'rawlsing_next/pre553_universal_evidence_binding.py'
before=f.read_text()
new='''    out = []
    # Predicate AND leaves are canonically sorted; consumer bindings preserve
    # requested prefix order. Associate by exact coordinate, never position.
    remaining = list(leaves)
    for conditioner in bindings:
        matches = [leaf for leaf in remaining
                   if canonicalize(_leaf_semantic_ref(leaf))
                   == canonicalize(conditioner.empirical_coordinate_ref.as_dict())]
        if len(matches) != 1:
            raise EvidenceBindingMismatch("producer leaf/conditioner exact coordinate association ambiguous")
        leaf = matches[0]
        remaining.remove(leaf)
'''
old='''    out = []
    for leaf, conditioner in zip(leaves, bindings):
'''
assert before.count(new)==1, before.count(new)
sha=hashlib.sha256(before.encode()).hexdigest()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
env['PYTHONPATH']=str(EVID/'pydeps')+os.pathsep+env.get('PYTHONPATH','')
try:
    f.write_text(before.replace(new,old,1))
    p=subprocess.run([sys.executable,'-B',str(EVID/'r08_reorder_probe2.py')],cwd=ROOT,env=env,text=True,capture_output=True,timeout=600)
finally:
    f.write_text(before)
restored=hashlib.sha256(f.read_text().encode()).hexdigest()==sha
out=(p.stdout+p.stderr)
print('returncode',p.returncode,'source_restored',restored)
print(out[-3500:])
