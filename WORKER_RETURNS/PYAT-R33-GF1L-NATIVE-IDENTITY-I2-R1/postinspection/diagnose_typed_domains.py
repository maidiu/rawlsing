"""Machine-readable witnesses for the already executed supplemental failures."""
import importlib.util,json,os,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]; S=R/'stage'
E=S/'WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1'
G=S/'WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1'
os.environ.update(GF1G_COURT=str(E),GF1G_ORACLE=str(G/'01_FROZEN_ORACLE.json'),GF1J_GF1G_TEST=str(G/'phase_a/test_gf1g_precommitted.py'))
s=importlib.util.spec_from_file_location('typed_domains',R/'postinspection/test_gf1l_typed_domain_conservation.py')
t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
rows=[]
for role in ('condition','target'):
    for domain in ((0,False),(0,0.0),('0',0),('0','1'),(0,1)):
        rel=t.relation(role,domain)
        assert rel.content_hash==t.p.h.G.semantic_hash(rel.semantic_projection())
        ref_cells=[dict(condition_type=type(row['condition_state']).__name__,condition_value=repr(row['condition_state']),target_type=type(cell['target_state']).__name__,target_value=repr(cell['target_state']),count=cell['joint_support_count']) for row in rel.conditional_count_profile for cell in row['target_counts']]
        assert sum(cell['count'] for cell in ref_cells)==2
        witness=dict(role=role,domain=[dict(type=type(v).__name__,value=repr(v)) for v in domain],relation_hash=rel.content_hash,real_original_constructor=True,source_qualified_producer_output=False,independent_reference_support=2,independent_reference_separation='EXACT_PAIR_SEPARATION',cells=ref_cells)
        try:
            witness['actual']=t.p.h.CONS(rel)
        except Exception as exc:
            witness['exception']=dict(type=type(exc).__name__,message=str(exc))
        rows.append(witness)
(R/'postinspection/typed_domain_witnesses.json').write_text(json.dumps(rows,indent=2,default=str)+'\n')
print(json.dumps([dict(role=r['role'],domain=r['domain'],actual=r.get('exception') or {k:r['actual'].get(k) for k in ('decision_state','joint_support_total','separation_class')}) for r in rows],indent=2))
