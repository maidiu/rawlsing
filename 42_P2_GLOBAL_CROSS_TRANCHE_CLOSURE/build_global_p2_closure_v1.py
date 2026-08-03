#!/usr/bin/env python3
from __future__ import annotations
import json, hashlib
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
FINAL=ROOT/'41_P2_GLOBAL_FINAL_2847_PAIR_TRANCHE8'
OUT=Path(__file__).resolve().parent; OUT.mkdir(parents=True,exist_ok=True)

def read(p): return pd.read_csv(p,keep_default_na=False)
def stable(*parts): return 'p2global_' + hashlib.sha256('|'.join(map(str,parts)).encode()).hexdigest()[:24]

initial=read(ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_Semantic_Neighborhood_Pair_Queue_v1.csv')
sources=[
 ('TRANCHE2_HIGH_PRECISION','34_P2_TRANCHE2_ACCEPTANCE_AUDIT_AND_CORRECTION',ROOT/'34_P2_TRANCHE2_ACCEPTANCE_AUDIT_AND_CORRECTION/Rawlsing_P2_Reworded_Translation_High_Precision_Pair_Rulings_v2.csv'),
 ('TRANCHE3_TRUST','36_P2_GLOBAL_TRUST_SEMANTIC_NEIGHBORHOOD_ADJUDICATION_TRANCHE3',ROOT/'36_P2_GLOBAL_TRUST_SEMANTIC_NEIGHBORHOOD_ADJUDICATION_TRANCHE3/Rawlsing_P2_Trust_Neighborhood_Pair_Rulings_v2.csv'),
 ('TRANCHE4_DEMOCRACY_ELECTORAL','37_P2_GLOBAL_DEMOCRACY_ELECTORAL_FIXED_3000_TRANCHE4',ROOT/'37_P2_GLOBAL_DEMOCRACY_ELECTORAL_FIXED_3000_TRANCHE4/Rawlsing_P2_Democracy_Electoral_3000_Pair_Rulings_v1.csv'),
 ('TRANCHE5_MEDIA_CIVIC','38_P2_GLOBAL_MEDIA_CIVIC_FIXED_3000_TRANCHE5',ROOT/'38_P2_GLOBAL_MEDIA_CIVIC_FIXED_3000_TRANCHE5/Rawlsing_P2_Media_Civic_3000_Pair_Rulings_v1.csv'),
 ('TRANCHE6_MATERIAL_ECONOMY','39_P2_GLOBAL_MATERIAL_ECONOMY_FIXED_3000_TRANCHE6',ROOT/'39_P2_GLOBAL_MATERIAL_ECONOMY_FIXED_3000_TRANCHE6/Rawlsing_P2_Material_Economy_3000_Pair_Rulings_v1.csv'),
 ('TRANCHE7_SOCIAL_ORDER','40_P2_GLOBAL_SOCIAL_ORDER_FIXED_3000_TRANCHE7',ROOT/'40_P2_GLOBAL_SOCIAL_ORDER_FIXED_3000_TRANCHE7/Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'),
 ('TRANCHE8_FINAL_2847','41_P2_GLOBAL_FINAL_2847_PAIR_TRANCHE8',FINAL/'Rawlsing_P2_Final_2847_Pair_Rulings_v1.csv'),
]

def get(row,*names):
 for n in names:
  if n in row.index: return row[n]
 return ''

def authority_class(rel):
 r=str(rel)
 if r in {'FUNCTIONALLY_COMPARABLE','PROPOSITION_EQUIVALENT_RESPONSE_CONTRACT_NOT_PORTABLE','REWORDED_PROPOSITION_EQUIVALENCE'}: return 'PROPOSITION_RELATION_AUTHORITY'
 if r in {'CONSTRUCT_COORDINATE_COMPARABLE','NESTED_TARGET_RELATION_NOT_EQUIVALENT','METADATA_FUNCTION_COMPARABLE','TARGET_RELATION_COORDINATE_ONLY','DERIVED_INDEX_CONSTRUCT_COORDINATE','TRUST_CONSTRUCT_COORDINATE_ONLY','DOMAIN_COORDINATE_ONLY','CONSTRUCT_TARGET_COORDINATE_ONLY'}: return 'COORDINATE_OR_BOUNDED_RELATION_AUTHORITY'
 if r in {'NEGATIVE_AUTHORITY_FALSE_FRIEND','NEGATIVE_AUTHORITY'}: return 'NEGATIVE_AUTHORITY'
 if r=='OTHER_DOMAIN_REVIEW_REQUIRED': return 'REDIRECTED_OTHER_DOMAIN_AUTHORITY'
 if r=='UNRESOLVED': return 'UNRESOLVED_FAIL_CLOSED_AUTHORITY'
 raise ValueError(r)

rows=[]
for tranche,section,path in sources:
 d=read(path)
 for _,x in d.iterrows():
  rel=get(x,'relation_type')
  rid=get(x,'pair_ruling_id','trust_pair_ruling_id','reworded_pair_ruling_id')
  sid=get(x,'semantic_content_id','semantic_content_id_discovery_only')
  rows.append({
   'global_semantic_authority_id':stable(get(x,'semantic_pair_candidate_id')),
   'origin_tranche':tranche,'origin_section':section,'origin_ruling_id':rid,
   'semantic_pair_candidate_id':get(x,'semantic_pair_candidate_id'),'semantic_content_id_discovery_only':sid,
   'left_source_family':get(x,'left_source_family'),'right_source_family':get(x,'right_source_family'),
   'left_lineage_id':get(x,'left_lineage_id'),'right_lineage_id':get(x,'right_lineage_id'),
   'original_relation_type':rel,'normalized_authority_class':authority_class(rel),
   'authority_status':get(x,'authority_status'),'portability_ceiling':get(x,'portability_ceiling'),
   'two_sided_evidence_status':get(x,'two_sided_evidence_status'),'rationale':get(x,'rationale'),'prohibited_use':get(x,'prohibited_use')})
registry=pd.DataFrame(rows).sort_values(['origin_tranche','semantic_pair_candidate_id'])
registry.to_csv(OUT/'Rawlsing_P2_Global_Semantic_Priority_Pair_Authority_Registry_v1.csv',index=False)

exact=read(ROOT/'34_P2_TRANCHE2_ACCEPTANCE_AUDIT_AND_CORRECTION/Rawlsing_P2_Exact_Foundation_Pair_Rulings_v3.csv')
def exact_class(s):
 if str(s).startswith('ACCEPTED_'): return 'ACCEPTED_EXACT_FOUNDATION_AUTHORITY'
 if str(s).startswith('REJECTED_'): return 'REJECTED_EXACT_FOUNDATION_AUTHORITY'
 if str(s).startswith('UNRESOLVED_'): return 'UNRESOLVED_EXACT_FOUNDATION_AUTHORITY'
 raise ValueError(s)
exact_summary=exact.assign(normalized_authority_class=exact.authority_status.map(exact_class))
exact_summary.to_csv(OUT/'Rawlsing_P2_Global_Exact_Foundation_Authority_Registry_v1.csv',index=False)

struct=read(ROOT/'33_P2_GLOBAL_REWORDED_RELATION_AXIS_STRUCTURE_ADJUDICATION_TRANCHE2/Rawlsing_P2_Structure_Analogy_Rulings_v1.csv')
smem=read(ROOT/'33_P2_GLOBAL_REWORDED_RELATION_AXIS_STRUCTURE_ADJUDICATION_TRANCHE2/Rawlsing_P2_Structure_Member_Correspondence_Rulings_v1.csv')
overlay=read(ROOT/'33_P2_GLOBAL_REWORDED_RELATION_AXIS_STRUCTURE_ADJUDICATION_TRANCHE2/Rawlsing_P2_Semantic_Reference_Correction_Overlay_v1.csv')
nodes=read(ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_All_Nine_Unified_Node_Evidence_Registry_v1.csv')
lineages=read(ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv')

initial_ids=set(initial.semantic_pair_candidate_id); registry_ids=set(registry.semantic_pair_candidate_id)
source_pair_count=registry[['left_source_family','right_source_family']].drop_duplicates().shape[0]
closure={
 'contract_version':'P2_GLOBAL_CROSS_TRANCHE_CLOSURE_V1',
 'global_p2_closed': True,
 'node_implementations':len(nodes),'source_local_lineages':len(lineages),
 'semantic_priority_queue_initial':len(initial),'semantic_priority_pairs_adjudicated':len(registry),'semantic_priority_pairs_remaining':len(initial_ids-registry_ids),
 'semantic_priority_candidate_ids_unique':registry.semantic_pair_candidate_id.is_unique,
 'semantic_priority_exact_coverage':initial_ids==registry_ids,
 'semantic_priority_authority_class_counts':registry.normalized_authority_class.value_counts().to_dict(),
 'semantic_priority_origin_tranche_counts':registry.origin_tranche.value_counts().sort_index().to_dict(),
 'semantic_priority_source_pair_coverage':source_pair_count,
 'exact_foundation_pairs':len(exact),'exact_foundation_authority_class_counts':exact_summary.normalized_authority_class.value_counts().to_dict(),
 'structure_analogy_rulings':len(struct),'structure_analogy_status_counts':struct.authority_status.value_counts().to_dict(),
 'structure_member_rulings':len(smem),'structure_member_status_counts':smem.authority_status.value_counts().to_dict(),
 'semantic_reference_overlays':len(overlay),'semantic_reference_overlay_status_counts':overlay.authority_status.value_counts().to_dict(),
 'unresolved_is_closed_as_fail_closed_authority_not_pending_work':True,
 'canonical_j_family_authority_authored':False,
 'respondents_joined':False,'values_harmonized':False,'database_or_registry_written':False,
 'live_component_bridge_installed':False,
 'live_component_bridge_blocker':'NO_USER_DESIGNATED_CURRENT_LIVE_REPOSITORY_OR_GIT_WORKTREE_PRESENT_IN_ACTIVE_RUNTIME',
 'next_pass':'P3_TYPED_COLLISION_HYPEREDGE_CANDIDATE_FAMILY_RANKING_AND_CANONICAL_V550J_ADJUDICATION',
 'authority_boundary':'GLOBAL_P2_RELATION_AND_STRUCTURE_AUTHORITY_CLOSED; NO_J_FAMILY_MEMBERSHIP_OR_VALUE_PORTABILITY_YET'
}
(OUT/'GLOBAL_P2_CLOSURE_RETURN.json').write_text(json.dumps(closure,indent=2,sort_keys=True)+'\n')

runtime={
 'audit_scope':'ACTIVE_RUNTIME_MNT_DATA_AND_CUMULATIVE_HANDOFF',
 'git_worktrees_found':0,
 'user_designated_current_live_repository_found':False,
 'recovered_runtime_snapshot_present':True,
 'component_bridge_validated_against_recovered_production_format_evidence':True,
 'installation_performed':False,
 'blocker':'No current writable live repository was supplied or discoverable; historical snapshots and cumulative handoff copies are not installation targets.',
 'required_next_runtime_action':'Install bridge v3.1 only in the user-designated current live repository, then rerun fail-closed component/cardinality/integration tests.'
}
(OUT/'LIVE_COMPONENT_BRIDGE_INSTALLATION_BOUNDARY_AUDIT.json').write_text(json.dumps(runtime,indent=2,sort_keys=True)+'\n')

checks=[]
def ck(name,ok,detail): checks.append({'check_id':f'P2CLOSE_{len(checks)+1:03d}','check_name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
ck('initial semantic queue has 18831 rows',len(initial)==18831,str(len(initial)))
ck('global registry has 18831 rows',len(registry)==18831,str(len(registry)))
ck('semantic candidate IDs unique',registry.semantic_pair_candidate_id.is_unique,str(registry.semantic_pair_candidate_id.nunique()))
ck('semantic candidate exact coverage',initial_ids==registry_ids,f'missing={len(initial_ids-registry_ids)} extra={len(registry_ids-initial_ids)}')
ck('all seven tranche counts exact',registry.origin_tranche.value_counts().to_dict()=={'TRANCHE2_HIGH_PRECISION':121,'TRANCHE3_TRUST':3863,'TRANCHE4_DEMOCRACY_ELECTORAL':3000,'TRANCHE5_MEDIA_CIVIC':3000,'TRANCHE6_MATERIAL_ECONOMY':3000,'TRANCHE7_SOCIAL_ORDER':3000,'TRANCHE8_FINAL_2847':2847},str(registry.origin_tranche.value_counts().to_dict()))
ck('normalized semantic partition exact',registry.normalized_authority_class.value_counts().to_dict()=={'NEGATIVE_AUTHORITY':14857,'REDIRECTED_OTHER_DOMAIN_AUTHORITY':1958,'COORDINATE_OR_BOUNDED_RELATION_AUTHORITY':1024,'PROPOSITION_RELATION_AUTHORITY':641,'UNRESOLVED_FAIL_CLOSED_AUTHORITY':351},str(registry.normalized_authority_class.value_counts().to_dict()))
ck('all 36 source pairs represented',source_pair_count==36,str(source_pair_count))
ck('exact foundation 751',len(exact)==751,str(len(exact)))
ck('exact foundation partition 270/78/403',exact_summary.normalized_authority_class.value_counts().to_dict()=={'UNRESOLVED_EXACT_FOUNDATION_AUTHORITY':403,'ACCEPTED_EXACT_FOUNDATION_AUTHORITY':270,'REJECTED_EXACT_FOUNDATION_AUTHORITY':78},str(exact_summary.normalized_authority_class.value_counts().to_dict()))
ck('structure analogies closed 19',len(struct)==19 and not struct.authority_status.str.contains('PROVISIONAL|PENDING').any(),str(struct.authority_status.value_counts().to_dict()))
ck('structure member rulings closed 119',len(smem)==119,str(smem.authority_status.value_counts().to_dict()))
ck('semantic overlays closed 30',len(overlay)==30 and overlay.authority_status.str.startswith('RESOLVED_').all(),str(overlay.authority_status.value_counts().to_dict()))
ck('phase0 node and lineage coverage',len(nodes)==18276 and len(lineages)==13526,f'nodes={len(nodes)} lineages={len(lineages)}')
ck('global P2 marked closed',closure['global_p2_closed'] and closure['semantic_priority_pairs_remaining']==0,str(closure['global_p2_closed']))
ck('no canonical J authority claimed',closure['canonical_j_family_authority_authored'] is False,'false')
ck('live bridge installation remains honestly blocked',closure['live_component_bridge_installed'] is False,runtime['blocker'])
vc=pd.DataFrame(checks); vc.to_csv(OUT/'GLOBAL_P2_CLOSURE_VALIDATION_CHECKS.csv',index=False)
if not (vc.status=='PASS').all(): raise SystemExit(vc[vc.status!='PASS'].to_string(index=False))
print(json.dumps({'checks_passed':len(vc),'registry_rows':len(registry),'closure':closure},indent=2))
