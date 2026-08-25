from pathlib import Path
import csv, json, hashlib, sys
root=Path(__file__).resolve().parents[3]  # data/ddm_build_copy
errors=[]
A=root/'authority/semantic_relation_dag_recovery/R1_20260825'
B=root/'recovery_reservoir/semantic_relation_R1_through_Job3/R1_20260825'
C=root/'recovery_knowledge_graph/semantic_relation_R1_through_Job3/R1_20260825'
D=root/'recovery_memory/semantic_relation_R1_through_Job3/R1_20260825'
for p in [A,B,C,D]:
    if not p.exists(): errors.append(f'missing layer: {p}')
# validate object store across installed reservoir shards
idx=B/'OBJECT_INDEX.tsv'
if idx.exists():
    with idx.open() as f:
        for r in csv.DictReader(f,delimiter='\t'):
            p=B/r['object_relpath']
            if not p.exists(): errors.append(f'missing reservoir object {r["sha256"]}')
            else:
                h=hashlib.sha256(p.read_bytes()).hexdigest()
                if h!=r['sha256']: errors.append(f'hash mismatch {p}')
# graph endpoints
nodes=set()
if (C/'AUTHORITY_NODES.csv').exists():
    with (C/'AUTHORITY_NODES.csv').open() as f: nodes={r['node_id'] for r in csv.DictReader(f)}
if (C/'AUTHORITY_EDGES.csv').exists():
    with (C/'AUTHORITY_EDGES.csv').open() as f:
        for r in csv.DictReader(f):
            if r['from_node'] not in nodes: errors.append('missing graph source '+r['from_node'])
            if r['to_node'] not in nodes: errors.append('missing graph target '+r['to_node'])
# canonical layer validator
v=A/'validators/validate_semantic_relation_dag_recovery.py'
if v.exists():
    import subprocess
    cp=subprocess.run([sys.executable,str(v)],capture_output=True,text=True)
    if cp.returncode: errors.append('Layer A validator failed: '+cp.stdout+cp.stderr)
# invariants sanity
inv=json.loads((D/'EXECUTABLE_INVARIANTS.json').read_text()) if (D/'EXECUTABLE_INVARIANTS.json').exists() else {}
for k,vv in {'r16f_t06_recertified_count':7,'strict_t06_count':64,'t15_positive_count':188,'job3_candidate_count':1264,'job3_final_positive_count':1190}.items():
    if inv.get(k)!=vv: errors.append(f'invariant drift {k}')
if errors:
    print('R3 INHERITANCE VALIDATION FAIL')
    print('\n'.join(errors[:100]))
    raise SystemExit(1)
print('R3 INHERITANCE VALIDATION PASS')
