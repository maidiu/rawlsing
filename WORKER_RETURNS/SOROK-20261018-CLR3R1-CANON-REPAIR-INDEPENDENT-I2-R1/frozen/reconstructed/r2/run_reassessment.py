"""Reproduce R1 in a new evidence directory, then run claim-scope audits.

R1 is never rewritten. Exit 1 preserves the six old prospective REDs.
"""
from pathlib import Path
from datetime import datetime,timezone
from dataclasses import asdict
import ast,hashlib,json,os,platform,re,subprocess,sys
import xml.etree.ElementTree as ET
from audit_support import ROOT,R1,m,intervene,ancestors
from court import threshold_variant
OUT=ROOT/'evidence'
REPO=ROOT.parent.parent

def write(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')

def verify_r1():
    for line in (R1/'SHA256SUMS').read_text().splitlines():
        expected,name=line.split('  ',1)
        assert hashlib.sha256((R1/name).read_bytes()).hexdigest()==expected,name
    for name in ('world_intersection.py','test_world_intersection.py'):
        rel='inherited/causal_experiment/'+name
        b=(R1/rel).read_bytes()
        assert b==subprocess.check_output(['git','show','0c718dfc69a453510bfad921ef60f0b3c271d648:'+str((R1/rel).relative_to(REPO))])


def run():
    OUT.mkdir(exist_ok=True); verify_r1()
    suites=[]
    for name,cwd,test in [
        ('inherited',R1/'inherited/causal_experiment','test_world_intersection.py'),
        ('controls',R1,'test_controls.py'),
        ('original_falsifiers',R1,'test_falsifiers.py'),
        ('adjudication',ROOT,'test_adjudication.py')]:
        xml=OUT/(name+'.xml')
        args=[sys.executable,'-m','pytest','-v','-p','no:cacheprovider',test,'--junitxml='+os.path.relpath(xml,cwd)]
        p=subprocess.run(args,cwd=cwd,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        stdout=p.stdout.replace(str(REPO),'<WORKTREE>').replace(sys.executable,'<PYTHON>')
        (OUT/(name+'.log')).write_text(stdout)
        xml.write_text(re.sub(r'hostname="[^"]*"','hostname="local-host"',xml.read_text()).replace(str(REPO),'<WORKTREE>'))
        suite=ET.parse(xml).getroot().find('testsuite')
        suites.append(dict(suite=name,command=['python3',*args[1:]],cwd=str(cwd.relative_to(REPO)),exit_code=p.returncode,**{k:int(suite.attrib[k]) for k in ('tests','failures','errors','skipped')}))
    baseline=m.output_table()
    write('baseline.json',baseline)
    write('baseline_traces.json',{w:asdict(m.simulate(w)) for w in m.WORK_OUTCOMES})
    cases={
        'baseline':m.WorldParameters(),
        'cash_reserve_220':m.WorldParameters(father=m.FatherHistory(cash_buffer=220)),
        'protected_care_24':m.WorldParameters(father=m.FatherHistory(protected_care_min=24)),
        'no_prior_joint_repair':m.WorldParameters(father=m.FatherHistory(joint_repair_episodes=0)),
        'large_reserve_protected_care':m.WorldParameters(father=m.FatherHistory(cash_buffer=400,protected_care_min=35)),
        'child_no_practice_slots':m.WorldParameters(child=m.ChildHistory(weekday_practice_slots=0)),
        'child_prior_episodes_3':m.WorldParameters(child=m.ChildHistory(practical_bicycle_episodes=3)),
        'neighbor_unrelated_garden':m.WorldParameters(neighbor=m.NeighborHistory(independent_project='garden',independently_scheduled_shift_day4=False))}
    write('sensitivity.json',{name:dict(parameters=asdict(p),rows=m.output_table(params=p)) for name,p in cases.items()})
    write('threshold_sensitivity.json',{str(k):[dict(workplace=w,behavior=dict(father=dict((t:=threshold_variant(k).simulate(w)).get('father_response').facts),child_actions=t.actor_actions,count=t.child_practice_count,later=t.child_project_after)) for w in m.WORK_OUTCOMES] for k in (2,3,4)})
    write('dag.json',{label:dict(nodes=[e.id for e in t.events],edges=[[p,e.id] for e in t.events for p in e.parents]) for label,t in ((w,m.simulate(w)) for w in m.WORK_OUTCOMES)})
    compare={}
    for name in ('baseline.json','baseline_traces.json','sensitivity.json','threshold_sensitivity.json','dag.json'):
        compare[name]=json.loads((OUT/name).read_text())==json.loads((R1/'evidence'/name).read_text())
    assert all(compare.values())
    write('original_output_comparison.json',compare)
    cells=[]
    for wage in (-175,0):
        for overtime in (0,32):
            t=intervene(dict(kind='OPAQUE',wage_delta=wage,required_overtime_min=overtime,job_security_warning=False))
            cells.append(dict(wage_delta=wage,required_overtime_min=overtime,father=dict(t.get('father_response').facts),child_actions=t.actor_actions,count=t.child_practice_count,trace_sha256=t.content_digest()))
    write('factorial_material_controls.json',cells)
    write('execution_receipts.json',dict(observed_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),pytest=subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),reassessed_commit='0c718dfc69a453510bfad921ef60f0b3c271d648',suites=suites,redaction='Host checkout/interpreter prefixes and JUnit hostname only; test values unchanged',scope='Author reassessment; positive audit observations are not fixes to old falsifiers'))
    source=Path(m.__file__).read_text(); tree=ast.parse(source)
    imports=[]
    for node in tree.body:
        if isinstance(node,ast.ImportFrom):imports.append(node.module)
        elif isinstance(node,ast.Import):imports.extend(alias.name for alias in node.names)
    write('candidate_coverage.json',dict(imported_module='R1/inherited/causal_experiment/world_intersection.py',source_sha256=hashlib.sha256(source.encode()).hexdigest(),imports=imports,top_level_functions=[node.name for node in tree.body if isinstance(node,ast.FunctionDef)],event_days=sorted({e.day for e in m.simulate('ROUTINE').events}),implemented=['exogenous workplace category selector','fixed-history material feasibility policy','child activity policy','recorded event DAG','practice counter and later action threshold'],not_implemented_in_this_bounded_candidate=['age/habitus/computational-person schema','recursive cross-coupled Rawlsing state advancement','ongoing between-encounter formation-pressure computation','runtime LLM scenario and factor proposal','post-computation narrative realization','canonical narrative persistence and future consumption'],scope='Absence from this candidate does not establish absence from Rawlsing or a defect against its declared limited scope'))
    verify_r1()
    assert all(row['errors']==0 and row['skipped']==0 for row in suites)
    assert [(r['tests'],r['failures'],r['exit_code']) for r in suites]==[(24,0,0),(23,0,0),(6,6,1),(18,0,0)]
    print(json.dumps(suites,indent=2))
    return 1 if any(row['exit_code'] for row in suites) else 0

if __name__=='__main__':
    raise SystemExit(run())
