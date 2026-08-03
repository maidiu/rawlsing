from __future__ import annotations
from pathlib import Path
import json,hashlib,itertools,sys
from referencing import Registry,Resource
from jsonschema import Draft202012Validator

def loadj(p):return json.loads(Path(p).read_text())
def schema_registry(sec):
 pairs=[]
 for p in sorted((sec/'schemas').glob('*.json')):
  o=loadj(p);pairs.append((o['$id'],Resource.from_contents(o)))
 return Registry().with_resources(pairs)
def fail(msg):raise ValueError(msg)
def validate_packet(packet_path,decision_path=None):
 packet_path=Path(packet_path);sec=Path(__file__).resolve().parents[1];p=loadj(packet_path);reg=schema_registry(sec)
 Draft202012Validator(loadj(sec/'schemas/candidate_packet.schema.json'),registry=reg).validate(p)
 c=p['candidate_family'];members=set(c['member_ids'])
 def evidence_surface(o):
  cc=o['candidate_family']
  return {'candidate_family_id':cc['candidate_family_id'],'candidate_revision_id':cc['revision_id'],'member_ids':sorted(cc['member_ids']),'signature_hashes':sorted((x['subject_id'],x['content_hash']) for x in o['proposition_signature_matrix']),'response_refs':sorted((x['subject_id'],x['reference_id'],x.get('response_contract_hash')) for x in o['response_contract_matrix']),'pair_projections':sorted((x['projection_id'],x['pair_fact_id'],x['left_subject_id'],x['right_subject_id'],x['projection_basis']) for x in o['pair_projections']),'internal_pairs':sorted((x['left_id'],x['right_id'],x['pair_state'],x.get('pair_fact_id'),x.get('pair_projection_id'),tuple(sorted(x['collision_ids'])),tuple(sorted(x['closure_obligation_ids']))) for x in o['internal_pair_matrix']),'collisions':sorted(x['collision_id'] for x in o['hard_collisions']),'obligations':sorted(x['obligation_id'] for x in o['closure_obligations']),'exact_evidence_links':sorted(o['exact_evidence_links'])}
 computed_hash=hashlib.sha256(json.dumps(evidence_surface(p),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
 if computed_hash!=p['evidence_bundle_hash']:fail('evidence bundle hash does not recompute')
 source_members=[x for xs in p['members_by_source'].values() for x in xs]
 if len(source_members)!=len(set(source_members)) or set(source_members)!=members:fail('members_by_source must partition candidate members exactly')
 sigs=[x['subject_id'] for x in p['proposition_signature_matrix']]; rcs=[x['subject_id'] for x in p['response_contract_matrix']]
 if len(sigs)!=len(set(sigs)) or set(sigs)!=members:fail('exactly one signature per member')
 if len(rcs)!=len(set(rcs)) or set(rcs)!=members:fail('exactly one response contract reference per member')
 expected={tuple(sorted(x)) for x in itertools.combinations(members,2)}
 projections={x['projection_id']:x for x in p['pair_projections']}
 if len(projections)!=len(p['pair_projections']):fail('duplicate pair projection id')
 rows=p['internal_pair_matrix']
 for row in rows:
  if row['pair_state'] in ('DIRECT_POSITIVE','DIRECT_COLLISION','DIRECT_UNRESOLVED','HIERARCHICAL_ONLY'):
   proj=projections.get(row['pair_projection_id'])
   if not proj:fail('direct internal pair lacks delivered projection')
   if {proj['left_subject_id'],proj['right_subject_id']}!={row['left_id'],row['right_id']}:fail('projection endpoints do not match internal pair subjects')
   if proj['pair_fact_id']!=row['pair_fact_id']:fail('projection pair fact mismatch')
 used={x['pair_projection_id'] for x in rows if x.get('pair_projection_id')}
 if used!=set(projections):fail('pair projection surface must equal projections used by direct internal pairs')
 actual=[tuple(sorted((x['left_id'],x['right_id']))) for x in rows]
 if len(actual)!=len(set(actual)) or set(actual)!=expected:fail('internal pair matrix must equal n choose 2 member pairs exactly')
 counts={'DIRECT_POSITIVE':'direct_positive','DIRECT_COLLISION':'direct_collision','DIRECT_UNRESOLVED':'direct_unresolved','HIERARCHICAL_ONLY':'hierarchical_only','UNRULED':'unruled','SIGNATURE_CONFLICT':'signature_conflict','SIGNATURE_COMPATIBLE':'signature_compatible'}
 calc={v:0 for v in counts.values()}
 for x in rows:calc[counts[x['pair_state']]]+=1
 calc['expected_pairs']=len(expected)
 if calc!=c['internal_pair_counts']:fail('internal pair counts do not reconcile')
 def keys(xs):return {tuple(sorted((x['left_id'],x['right_id']))) for x in xs}
 if keys(p['unresolved_pairs'])!={k for k,x in zip(actual,rows) if x['pair_state']=='DIRECT_UNRESOLVED'}:fail('unresolved summary mismatch')
 if keys(p['unruled_pairs'])!={k for k,x in zip(actual,rows) if x['pair_state']=='UNRULED'}:fail('unruled summary mismatch')
 collisions={x['collision_id'] for x in p['hard_collisions']}; obligations={x['obligation_id'] for x in p['closure_obligations']}
 linked_coll={z for x in rows for z in x['collision_ids']};linked_obl={z for x in rows for z in x['closure_obligation_ids']}
 if linked_coll!=collisions:fail('collision links do not reconcile')
 if linked_obl!=obligations or set(c['closure_obligation_ids'])!=obligations:fail('closure links do not reconcile')
 if c['evidence_bundle_hash']!=p['evidence_bundle_hash']:fail('candidate and packet evidence hashes differ')
 if p['fixture_status']=='AUTHORITY_PACKET' and p['evidence_bundle_hash']=='0'*64:fail('authority hash cannot be placeholder')
 rank=c['ranking']
 if rank['candidate_revision_id']!=c['revision_id'] or rank['lineage_count']!=len(members) or rank['source_count']!=len(p['members_by_source']):fail('ranking counts or revision mismatch')
 density=calc['direct_positive']/len(expected) if expected else 0
 if abs(rank['direct_positive_density']-density)>1e-12:fail('ranking density mismatch')
 if not any(x['exclusion_type']=='RULE_BASED' for x in p['explicit_exclusions']):fail('rule-based exclusion required')
 origin=c['candidate_origin_type']
 if origin in ('STRICT_RESPONSE_COMPONENT','PROPOSITION_ONLY_SEED') and (not c['component_ids'] or c['attachment_projection_ids']):fail('base candidate origin mismatch')
 if origin=='ATTACHMENT_REVIEW' and not c['attachment_projection_ids']:fail('attachment candidate requires projections')
 if origin=='NONCONNECTIVE_DIAGNOSTIC_CASE' and (c['component_ids'] or c['attachment_projection_ids']):fail('diagnostic origin cannot borrow connectivity')
 d=loadj(decision_path) if decision_path else p['decision_form']
 schema='adjudication_decision.schema.json' if d.get('decision_status') else 'adjudication_decision_draft.schema.json'
 Draft202012Validator(loadj(sec/'schemas'/schema),registry=reg).validate(d)
 if d['candidate_family_id']!=c['candidate_family_id'] or d['candidate_revision_id']!=c['revision_id']:fail('decision candidate mismatch')
 if d['evidence_bundle_hash']!=p['evidence_bundle_hash'] or d['authority_release_id']!=c['authority_release_id']:fail('decision evidence/release mismatch')
 if d.get('decision_status'):
  dispositions=[('ACCEPT',x) for x in d['accepted_members']]+[('EXCLUDE',x) for x in d['excluded_members']]
  dispositions += [('HIERARCHICAL',x['narrower_object_id']) for x in d['hierarchical_relations']]
  unresolved={x['left_id'] for x in d['unresolved_boundaries']}|{x['right_id'] for x in d['unresolved_boundaries']}
  dispositions += [('UNRESOLVED',x) for x in unresolved if x in members]
  ids=[x for _,x in dispositions]
  if set(ids)!=members or len(ids)!=len(set(ids)):fail('completed decision must partition every candidate member exactly once')
  if d['decision_status']=='SPLIT_REQUIRED':
   results=d['split_results'];groups=[set(x['member_ids']) for x in results]
   if len(groups)<2 or set().union(*groups)!=members or sum(map(len,groups))!=len(members):fail('split results must be disjoint and cover all members')
  if d['decision_status'] in ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS'):
   accepted=set(d['accepted_members'])
   promoted={x for v in d['variant_promotions'] for x in v['member_ids']}
   if d['decision_status']=='ACCEPTED_WITH_VARIANTS' and promoted!=accepted:fail('canonical variant promotions must cover accepted members exactly')
   excluded=set(d['excluded_members']);mapped={x for e in d['exclusion_promotions'] for x in e['excluded_member_ids']}
   if mapped!=excluded:fail('canonical named exclusion promotions must cover excluded members exactly')
 return {'status':'PASS','members':len(members),'internal_pairs':len(expected),'decision_status':d.get('decision_status')}

if __name__=='__main__':
 try:print(json.dumps(validate_packet(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None),indent=2))
 except Exception as e:print(json.dumps({'status':'FAIL','error':str(e)},indent=2));raise
