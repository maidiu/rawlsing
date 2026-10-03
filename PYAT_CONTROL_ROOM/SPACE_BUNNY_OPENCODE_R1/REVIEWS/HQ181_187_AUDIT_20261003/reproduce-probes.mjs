import fs from 'node:fs';import os from 'node:os';import path from 'node:path';
import {pathToFileURL} from 'node:url';
if(!process.argv[2]) throw Error('Pass an absolute path to the audited dispatcher copy');
const {Store,validateTask,submitTask,publicationGate,deriveState,buildLaunchArgv}=await import(pathToFileURL(process.argv[2]).href);
const root=fs.mkdtempSync(path.join(os.tmpdir(),'pyat-independent-probe-'));
const task={task_id:'T',role:'worker',base_commit:'1'.repeat(40),worktree:root,terrain:['allowed/**'],acceptance:'UNBOUND',commission_path:'UNBOUND'};
const observations=[];
function probe(id,f){try{observations.push({id,...f()});}catch(e){observations.push({id,error:e.code||e.message});}}
probe('P01_UNBOUND_COMMISSION_ACCEPTED',()=>({accepted:validateTask(task)}));
probe('P02_MISSING_CANDIDATE_IDENTITIES_PASS_PUBLICATION',()=>({accepted:publicationGate(task,undefined,'arbitrary-review-label',undefined,[])}));
probe('P03_DUPLICATE_AT_CAPACITY',()=>{const s=new Store(path.join(root,'dup'));submitTask(s,task);submitTask(s,{...task,task_id:'T2'});try{return submitTask(s,task)}catch(e){return {duplicate_rejected_as:e.code,expected:'idempotent acknowledgement'}}});
probe('P04_CORRUPT_EVENT_SILENTLY_IGNORED',()=>{const s=new Store(path.join(root,'bad'));fs.appendFileSync(s.log,'not-json\n');return {events:s.all(),state:deriveState(s.all())}});
probe('P05_QUEUE_OMITS_RESUME_BINDINGS',()=>{const s=new Store(path.join(root,'resume'));submitTask(s,task);return {stored_keys:Object.keys(s.all()[0]),missing:['worktree','terrain','acceptance','commission_path','session_id'].filter(k=>!(k in s.all()[0]))}});
probe('P06_ARBITRARY_ACCEPTANCE_EVENT',()=>{const s=new Store(path.join(root,'accept'));s.append({task_id:'T',attempt:1,seq:1,state:'ACCEPTED'});return {derived:deriveState(s.all())}});
probe('P07_Q08_WRONG_STATES_CAN_PASS',()=>{const seen={queued:'BROKEN',queued2:'BROKEN',running:'BROKEN',waiting:'BROKEN',accepted:'BROKEN'};for(const n of ['UNKNOWN','QUEUED','RUNNING','WAITING_FOR_HQ','ACCEPTED'])if(seen[n]!==undefined&&seen[n]!==n)throw Error('rejected');return {incorrect_results_accepted:true}});
probe('P08_LAUNCH_IS_ARGV_ONLY',()=>({argv:buildLaunchArgv({worktree:root,role:'worker',prompt_path:'/commission.md'})}));
fs.rmSync(root,{recursive:true,force:true});
console.log(JSON.stringify(observations,null,2));
