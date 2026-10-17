import pandas as pd, json, sys, hashlib, subprocess, tempfile
from pathlib import Path
B=Path(__file__).resolve().parents[1]; R=B/'RETURN'; T=B/'TEMPLATES'; A=B/'AUTHORITY'
errs=[]; checks=[]
def ok(name,cond,detail=''):
    checks.append({'check':name,'status':'PASS' if cond else 'FAIL','detail':detail})
    if not cond: errs.append(name+(' :: '+detail if detail else ''))
def jl(x):
    try: return json.loads(x) if str(x).strip() else []
    except Exception: return []
role=pd.read_csv(R/'SEMANTIC_ROLE_ASSIGNMENT.csv',dtype=str).fillna('')
role_t=pd.read_csv(T/'SEMANTIC_ROLE_ASSIGNMENT.csv',dtype=str).fillna('')
cand=pd.read_csv(R/'CANDIDATE_ADJUDICATION.csv',dtype=str).fillna('')
obj=pd.read_csv(R/'SOURCE_OBJECT_RULE_REVIEW.csv',dtype=str).fillna('')
obj_t=pd.read_csv(T/'SOURCE_OBJECT_RULE_REVIEW.csv',dtype=str).fillna('')
rels=pd.read_csv(R/'RELATION_IMPLEMENTATIONS.csv',dtype=str).fillna('')
r6=pd.read_csv(A/'R6_EXISTING_RELATIONS.csv',dtype=str).fillna('')
can=pd.read_csv(R/'CANARY_RECALL.csv',dtype=str).fillna('')
cov=pd.read_csv(R/'RULE_WAVE_COVERAGE.csv',dtype=str).fillna('')
anti=pd.read_csv(R/'EXPLICIT_ANTIJOINS.csv',dtype=str).fillna('')
gaps=pd.read_csv(R/'AUTHORITY_GAPS.csv',dtype=str).fillna('')
prop=pd.read_csv(R/'PROPAGATION_LEDGER.csv',dtype=str).fillna('')
qa=pd.read_csv(R/'HOSTILE_QA.csv',dtype=str).fillna('')
sp=pd.read_csv(A/'IMPLEMENTATION_SPINE.csv.gz',dtype=str,compression='gzip',low_memory=False).fillna('')
# Exact accounting / immutable keys
ok('semantic_role_rows_exact_710',len(role)==len(role_t)==710,str(len(role)))
key=['source_family','wave','semantic_unit_id']
ok('semantic_role_keys_immutable',role[key].equals(role_t[key]))
locks=role_t.t06_norm.str.startswith('LOCKED_')
ok('c3_t06_locks_preserved',role.loc[locks,'t06_norm'].equals(role_t.loc[locks,'t06_norm']),str(locks.sum()))
ok('source_object_rows_exact_328',len(obj)==len(obj_t)==328,str(len(obj)))
ok('source_object_keys_immutable',obj[['source_family','wave','object_id','rule_id']].equals(obj_t[['source_family','wave','object_id','rule_id']]))
ok('coverage_exact_54',len(cov)==54,str(len(cov)))
ok('all_qa_pass',(qa.status=='PASS').all(),str(len(qa)))
# deterministic compiler replay
with tempfile.TemporaryDirectory() as td:
    out=Path(td)/'cand.csv'
    subprocess.run([sys.executable,str(B/'CODE/compile_role_compatible_candidates.py'),str(R/'SEMANTIC_ROLE_ASSIGNMENT.csv'),str(A/'IMPLEMENTATION_SPINE.csv.gz'),str(out)],check=True,capture_output=True)
    exp=pd.read_csv(out,dtype=str).fillna('')
    ok('candidate_denominator_exact_replay',set(exp.candidate_id)==set(cand.candidate_id),f'exp={len(exp)} got={len(cand)}')
ok('candidate_count_11800',len(cand)==11800,str(len(cand)))
# state law
ok('candidate_every_row_adjudicated',cand.adjudication_status.isin({'POSITIVE_RELATION','PROVEN_NEGATIVE','BLOCKED_AUTHORITY_GAP'}).all())
neg=cand[cand.adjudication_status=='PROVEN_NEGATIVE']; blk=cand[cand.adjudication_status=='BLOCKED_AUTHORITY_GAP']; pos=cand[cand.adjudication_status=='POSITIVE_RELATION']
ok('candidate_negatives_have_mismatch',((neg.mismatch_dimension!='')&(neg.decision_basis!='')).all(),str(len(neg)))
ok('candidate_blocks_have_gap',(blk.authority_gap!='').all(),str(len(blk)))
ok('candidate_positives_have_relation',((pos.relation_id_if_positive!='')&(pos.decision_basis!='')).all(),str(len(pos)))
relids=set(rels.relation_id)
ok('candidate_positive_relation_ids_resolve',set(pos.relation_id_if_positive)<=relids,str(len(pos)))
opos=obj[obj.worker_structure_status=='POSITIVE_STRUCTURE']; oneg=obj[obj.worker_structure_status=='PROVEN_NEGATIVE']; oblk=obj[obj.worker_structure_status=='BLOCKED_AUTHORITY_GAP']
ok('object_every_row_adjudicated',obj.worker_structure_status.isin({'POSITIVE_STRUCTURE','PROVEN_NEGATIVE','BLOCKED_AUTHORITY_GAP','NOT_APPLICABLE','RETAIN_EXISTING_GOVERNED_AUTHORITY'}).all())
ok('object_negatives_have_mismatch',((oneg.mismatch_dimension!='')&(oneg.decision_basis!='')).all(),str(len(oneg)))
ok('object_blocks_have_gap',(oblk.authority_gap!='').all(),str(len(oblk)))
obj_rel_ids=set()
for x in opos.relation_ids_json:
    obj_rel_ids.update(jl(x))
ok('object_positive_relation_ids_resolve',obj_rel_ids<=relids,f'{len(obj_rel_ids)} ids')
# relation rows
ok('relation_ids_unique',not rels.relation_id.duplicated().any(),str(len(rels)))
implset=set(sp.question_implementation_id); suset=set(role.semantic_unit_id)
missing_impl=[]; missing_su=[]; recall_positive=[]
for _,x in rels.iterrows():
    for q in jl(x.member_implementation_ids_json):
        if q not in implset: missing_impl.append((x.relation_id,q))
    for s in jl(x.member_semantic_unit_ids_json):
        if s not in suset: missing_su.append((x.relation_id,s))
    if 'RECALL/' in x.evidence_refs_json: recall_positive.append(x.relation_id)
ok('relation_member_implementations_resolve',not missing_impl,str(missing_impl[:3]))
ok('relation_member_semantic_units_resolve',not missing_su,str(missing_su[:3]))
ok('positive_relation_evidence_not_recall',not recall_positive,str(recall_positive))
# all current R6 canaries: independent return member set matches current sealed expected after reconstruction
ok('canary_rows_exact_11',len(can)==len(r6)==11,f'can={len(can)} r6={len(r6)}')
ok('canaries_all_rediscovered',(can.worker_recall_status=='REDISCOVERED_POSITIVE').all(),str(len(can)))
canary_mismatch=[]
for _,rr in r6.iterrows():
    z=rels[rels.relation_id==rr.relation_authority_id]
    if len(z)!=1:
        canary_mismatch.append((rr.relation_authority_id,'relation_count',len(z))); continue
    expected={m.get('question_implementation_id','') for m in jl(rr.active_member_crosswalk_json)}
    got=set(jl(z.iloc[0].member_implementation_ids_json))
    if expected!=got: canary_mismatch.append((rr.relation_authority_id,'members',sorted(expected-got),sorted(got-expected)))
ok('canary_exact_current_member_sets_reconstructed',not canary_mismatch,str(canary_mismatch[:3]))
# T06: no false negative collapse / both compiler branches present
c6=cand[cand.rule_id=='T06']
ok('t06_both_branches_present',set(c6.branch)=={'STATED_INTENDED','REALIZED_O04_ENDPOINT'},str(c6.branch.value_counts().to_dict()))
ok('t06_unresolved_all_blocked',(c6.adjudication_status=='BLOCKED_AUTHORITY_GAP').all(),str(c6.adjudication_status.value_counts().to_dict()))
ok('novel_t06_positive_count_zero',len(rels[(rels.rule_id=='T06') & ~rels.relation_id.isin(set(r6.relation_authority_id))])==0)
# T09 exact-hostile denominator
r9=role[role.t09_directional_actor_recipient=='YES']
expected_t09={('EVS','2008','v135'),('LiTS','IV','q826a'),('Asian Barometer','W5','q62'),('Asian Barometer','W5','q63'),('Asian Barometer','W5','q91'),('Asian Barometer','W5','q108'),('Asian Barometer','W5','q112'),('Asian Barometer','W5','q113'),('Asian Barometer','W5','q122'),('Asian Barometer','W5','q143')}
got_t09=set()
for _,x in r9.iterrows():
    codes=jl(x.source_variable_codes_json)
    if len(codes)==1: got_t09.add((x.source_family,x.wave,codes[0]))
ok('t09_exact_role_shore_10',got_t09==expected_t09,str(sorted(got_t09)))
c9=cand[cand.rule_id=='T09']
ok('t09_compiled_28_all_explicit_negatives',len(c9)==28 and (c9.adjudication_status=='PROVEN_NEGATIVE').all(),str(c9.adjudication_status.value_counts().to_dict()))
# Novel T08/T10 exact IDs and structural checks
nov=rels[~rels.relation_id.isin(set(r6.relation_authority_id))]
ok('novel_relation_count_3',len(nov)==3,str(nov[['relation_id','rule_id']].to_dict('records')))
ok('novel_rule_mix_2_t08_1_t10',nov.rule_id.value_counts().to_dict()=={'T08':2,'T10':1},str(nov.rule_id.value_counts().to_dict()))
nt=nov[nov.rule_id=='T10'].iloc[0]
roles=jl(nt.role_assignments_json) if False else json.loads(nt.role_assignments_json)
coords={(v.get('target_dimension'),v.get('condition_dimension')) for v in roles.values()}
targs={x for x,_ in coords}; conds={y for _,y in coords}
ok('novel_t10_complete_2x2',len(coords)==4 and len(targs)==2 and len(conds)==2 and coords=={(a,b) for a in targs for b in conds},str(coords))
# EVS T10 substrate exception is explicit, not silently synthesized
et=rels[rels.relation_id=='IQRA-R2-ead6ae8c1455b7105a04']
ok('evs_t10_canary_present_once',len(et)==1)
if len(et)==1:
    x=et.iloc[0]
    ok('evs_t10_exact_30_impls_no_synthetic_semantic_ids',len(jl(x.member_implementation_ids_json))==30 and len(jl(x.member_semantic_unit_ids_json))==0,f"impl={len(jl(x.member_implementation_ids_json))} su={len(jl(x.member_semantic_unit_ids_json))}")
    ok('evs_t10_substrate_gap_recorded',gaps.missing_authority.str.contains('SEMANTIC_UNIT_MATERIALIZATION_ABSENT_FOR_30_SEALED_Q5A_Q5B_MATRIX_MEMBERS',regex=False).any())
# q403 foreign investor antijoin
a403=anti[(anti.source_family=='LiTS')&(anti.wave=='IV')&(anti.rule_id=='T08')]
ok('q403_foreign_investor_explicit_antijoin',a403.decision_basis.str.contains('ACTOR_NOT_INSTITUTION',regex=False).any(),str(len(a403)))
# coverage accounting recompute
coverage_bad=[]
for _,x in cov.iterrows():
    cc=cand[(cand.source_family==x.source_family)&(cand.wave==x.wave)&(cand.rule_id==x.rule_id)]
    oo=obj[(obj.source_family==x.source_family)&(obj.wave==x.wave)&(obj.rule_id==x.rule_id)]
    rr=rels[(rels.source_family==x.source_family)&(rels.wave==x.wave)&(rels.rule_id==x.rule_id)]
    negn=(cc.adjudication_status=='PROVEN_NEGATIVE').sum()+(oo.worker_structure_status=='PROVEN_NEGATIVE').sum()
    blkn=(cc.adjudication_status=='BLOCKED_AUTHORITY_GAP').sum()+(oo.worker_structure_status=='BLOCKED_AUTHORITY_GAP').sum()
    vals=(int(x.compiled_candidate_count),int(x.positive_relation_count),int(x.proven_negative_count),int(x.blocked_count))
    exp=(len(cc),rr.relation_id.nunique(),int(negn),int(blkn))
    if vals!=exp: coverage_bad.append(((x.source_family,x.wave,x.rule_id),vals,exp))
ok('coverage_counts_recompute_exact',not coverage_bad,str(coverage_bad[:3]))
# propagation: explicitly bounded, no relation verdict propagation
ok('propagation_rows_8',len(prop)==8,str(len(prop)))
ok('propagation_no_relation_verdict_language',not prop.why_semantically_identical.str.contains('propagate.*positive|propagate.*negative|relation verdict',case=False,regex=True).any())
# worker boundary language in coverage
ok('no_freeze_claim_in_coverage',cov.notes.str.contains('DOES NOT CLAIM S14 FREEZE',regex=False).all())
# write report
out={'worker':'S14W02','status':'PASS' if not errs else 'FAIL','error_count':len(errs),'checks':checks}
(R/'HOSTILE_AUDIT_MACHINE.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'worker':'S14W02','status':out['status'],'checks':len(checks),'errors':errs},indent=2))
sys.exit(1 if errs else 0)
