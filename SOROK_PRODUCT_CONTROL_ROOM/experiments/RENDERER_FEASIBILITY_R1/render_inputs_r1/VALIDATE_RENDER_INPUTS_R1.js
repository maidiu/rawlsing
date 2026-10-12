// RFA-05B offline input/parity validator, Node 18+. No network/provider calls.
const fs=require('fs'),path=require('path'),dir=__dirname,root=path.join(dir,'..','lab_fixture');
const read=(p)=>JSON.parse(fs.readFileSync(p,'utf8')),assert=(x,m)=>{if(!x)throw Error(m)};
const man=read(path.join(dir,'INPUT_PARITY_MANIFEST_R1.json'));
const ids=Array.from({length:10},(_,i)=>'RF'+String(i+1).padStart(3,'0'));
for(const id of ids){
 const origin=read(path.join(root,id+'.json')),n=read(path.join(dir,id+'_N.json')),w=read(path.join(dir,id+'_WP.json'));
 assert(JSON.stringify(n.model_payload.shared)===JSON.stringify(w.model_payload.shared),id+' shared mismatch');
 assert(JSON.stringify(n.model_payload.shared.actor_projection_exact_from_RFA05)===JSON.stringify(origin.expression_action_constraints.value.actor_safe_projection),id+' narrow changed');
 assert(!Object.hasOwn(n.model_payload,'whole_person_extension')&&Object.hasOwn(w.model_payload,'whole_person_extension'),id+' arm contamination');
 assert(n.model_payload.shared.exact_user_event.exact_speech===origin.exact_user_event.value.exact_speech,id+' stimulus changed');
 const refs=n.model_payload.shared.scene.facts.map(x=>x.source_ref);
 assert(JSON.stringify(refs)===JSON.stringify(origin.expression_action_constraints.value.actor_safe_projection.scene_documented_refs),id+' world mismatch');
 assert(refs.every(x=>!['W09','W10','W11'].includes(x)),id+' private world');
 const p=JSON.stringify(w.model_payload);
 for(const x of ['evaluator_only_oracle','evaluator_only_hidden_causal_summary','objective_truth_register','user_phenomenal_output','user_attention_recognition_access','Mara accepted a job','closing 18:00','"provenance"'])assert(!p.includes(x),id+' unexpected model input '+x);
 const pr=w.audit_metadata_NOT_FOR_MODEL.WP_provenance;
 assert(pr.length>20&&pr.every(x=>x.source_artifact&&x.source_field_id&&x.origin_class&&x.why_relevant&&x.actor_conscious_knowledge&&typeof x.may_narrate==='boolean'&&typeof x.expression_only==='boolean'&&x.time_scope),id+' incomplete provenance');
 const row=man.cases.find(x=>x.case_id===id);assert(row,id+' missing manifest');
 assert(row.sizes.N.bytes===Buffer.byteLength(JSON.stringify(n.model_payload)),id+' N size mismatch');
 assert(row.sizes.WP.bytes===Buffer.byteLength(JSON.stringify(w.model_payload)),id+' WP size mismatch');
}
const a=read(path.join(dir,'RF008_N.json')).model_payload.shared.exact_user_event.exact_speech;
const b=read(path.join(dir,'RF009_N.json')).model_payload.shared.exact_user_event.exact_speech;
assert(a===b,'RF008/RF009 utterance differs');
console.log('PASS 10 WP/N pairs; unchanged narrow projection; actor-only world; separated provenance; no provider execution.');
