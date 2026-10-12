// RFA05 hand-authored laboratory structural check; intentionally no network, no model execution.
const fs=require('fs'), path=require('path');
const dir=__dirname, files=Array.from({length:10},(_,i)=>'RF'+String(i+1).padStart(3,'0')+'.json');
const required=["fixture_identity","canonical_precontact_history","durable_person_owner_refs","objective_relationship_history","current_world_slice","exact_user_event","actor_perception_opportunity","can008_receivability","can008_uptake_appraisal","can008_recruitment","can008_response_streams","actor_accessibility_and_uncertainty","actor_realization_candidate","objective_occurrence_admission","user_phenomenal_allowlist","forbidden_knowledge_and_invention","status_and_provenance"];
const all=["fixture_identity","canonical_precontact_history","durable_person_owner_refs","relation_scoped_person_organization","relation_class_generalization","nadia_model_of_user","objective_relationship_history","nadia_perceived_relationships","independent_projects_and_competencies","current_world_slice","current_material_organismic_state","exact_user_event","machine_event_interpretation","actor_perception_opportunity","can008_receivability","can008_uptake_appraisal","can008_recruitment","can008_response_streams","actor_accessibility_and_uncertainty","current_focality_and_self_explanation","communicative_intention_and_inhibition","pff_interaction_context","pff_actor_local_fast_carryover","expression_action_constraints","actor_realization_candidate","unresolved_materialization_permissions","objective_occurrence_admission","owner_specific_durable_effect_candidates","effect_commit_or_defer_receipts","user_phenomenal_allowlist","user_attention_recognition_access","user_phenomenal_output","user_exposure_and_interpretation","forbidden_knowledge_and_invention","status_and_provenance"];
const valid=["PRESENT","VALID_EMPTY","UNKNOWN","DEFERRED","UNAUTHORIZED","NOT_APPLICABLE","INTEGRITY_FAILURE"];
const unresolved=['relation_class_generalization','nadia_model_of_user','independent_projects_and_competencies','unresolved_materialization_permissions'];
const assert=(ok,msg)=>{if(!ok)throw Error(msg)};
const data={};
for(const name of files){
 const o=JSON.parse(fs.readFileSync(path.join(dir,name),'utf8'));data[name]=o;
 assert(JSON.stringify(Object.keys(o).sort())===JSON.stringify(all.slice().sort()),name+': mismatched top-level RFA-R fields');
 for(const key of required)assert(Object.hasOwn(o,key),name+': missing '+key);
 for(const [k,s] of Object.entries(o)){
  for(const x of ['state','value','evidence_refs','source_owner','causal_time','scope'])assert(Object.hasOwn(s,x),name+' '+k+' missing '+x);
  assert(valid.includes(s.state),name+' '+k+' illegal state');
  assert(s.evidence_refs.length>0&&Array.isArray(s.evidence_refs),name+' '+k+' missing evidence');
  assert(typeof s.source_owner==='string'&&typeof s.causal_time==='string',name+' '+k+' source/time');
  assert(s.scope===name.replace('.json',''),name+' '+k+' wrong scope');
  assert(s.notes.includes('HAND_AUTHORED_LAB_SURROGATE_ONLY'),name+' '+k+' no surrogate marker');
 }
 for(const k of unresolved)assert(o[k].state==='UNAUTHORIZED'&&o[k].value===null,name+' unresolved owner populated: '+k);
 assert(o.actor_realization_candidate.state==='DEFERRED'&&o.objective_occurrence_admission.state==='DEFERRED',name+' model outcome fabricated');
 assert(o.user_phenomenal_output.state==='NOT_APPLICABLE',name+' compositor leaked into first phase');
 assert(o.exact_user_event.value.speaker==='P0',name+' inconsistent interaction speaker');
}
assert(!data['RF004.json'].expression_action_constraints.value.actor_safe_projection.scene_documented_refs.includes('W09'),'unseen hall notice leaked to actor');
assert(data['RF008.json'].exact_user_event.value.exact_speech===data['RF009.json'].exact_user_event.value.exact_speech,'relation pair utterance differs');
assert(data['RF008.json'].objective_relationship_history.value.events.length===4,'RF008 relation unexpected');
assert(data['RF009.json'].objective_relationship_history.value.events.length===6,'RF009 copy-on-write relation missing');
assert(data['RF006.json'].owner_specific_durable_effect_candidates.state==='VALID_EMPTY','RF006 should be valid empty');
for(const name of ['NADIA_LAB_CANON_R1.json','NADIA_LAB_WHOLE_PERSON_RENDER_SUBSTRATE_R1.json','NADIA_LAB_RELATION_USER_R1.json','NADIA_LAB_WORLD_STATE_R1.json','NADIA_LAB_FIELD_PROVENANCE_R1.json','OBJECTIVE_OCCURRENCE_OUTPUT_SCHEMA_R1.json'])JSON.parse(fs.readFileSync(path.join(dir,name),'utf8'));
console.log('RFA05 structural checks: PASS (10 cases; RFA-R slot envelope; no renderer outputs scored).');
