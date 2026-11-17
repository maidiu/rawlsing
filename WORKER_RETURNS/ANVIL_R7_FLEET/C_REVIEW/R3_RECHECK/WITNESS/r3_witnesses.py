#!/usr/bin/env python3
"""R3 finite four-defect recheck plus usability countercheck.

Uses only the fresh R3 extraction and copies EVIDENCE into R3-local temp dirs.
No R1/R2 or candidate writes.
"""
import copy, json, pathlib, shutil, sys, tempfile

R3=pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW/WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R3_RECHECK')
TS=(R3/'LOGS/STAMP').read_text().strip(); PKG=R3/f'COLD/FRESH_{TS}/ANVIL_R7'; TOOLS=PKG/'tools'
sys.path.insert(0,str(TOOLS))
from r7_integrated import check, digest, sha  # noqa: E402
REPO='/Users/matthewsmith/s2b-work/rawlsing'; ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=R3/'WITNESS'; OUT.mkdir(parents=True,exist_ok=True)
BASE=R3/f'COLD/FRESH_{TS}/ANVIL_R7/EVIDENCE'

def load_ev(tag):
    d=pathlib.Path(tempfile.mkdtemp(prefix=tag+'_',dir=str(OUT)))/'EVIDENCE'
    shutil.copytree(BASE,d); return d

def put(ev,n,o):
    b=(json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode(); (ev/n).write_bytes(b)
    return {'path':n,'sha256':sha(b)}

def resync(ev,frame,decision,c=None):
    put(ev,'FRAME.json',frame)
    decision['common_frame']={'path':'FRAME.json','sha256':sha((ev/'FRAME.json').read_bytes())}
    decision['frame_sha256']=digest(frame)
    put(ev,'DECISION.json',decision)
    if c is not None:
        c['integrated_decision']={'path':'DECISION.json','sha256':sha((ev/'DECISION.json').read_bytes())}
        c['integrated_decision_sha256']=digest(decision)
        put(ev,'C.json',c)

def base():
    ev=load_ev('base'); f=json.loads((ev/'FRAME.json').read_text()); d=json.loads((ev/'DECISION.json').read_text()); c=json.loads((ev/'C.json').read_text()); return ev,f,d,c

report={'schema':'C_REVIEW_R3_WITNESSES','cases':{}}

# W1a false typed F4 machine assertion, true prose
ev,f,d,c=base(); r=next(x for x in f['requirements'] if x['id']=='REQ-MULTIWAY-JOINT'); r['machine_assertion']=dict(r['machine_assertion'],pairwise_product=True); resync(ev,f,d,c); report['cases']['W1a_false_typed_F4']={'FRAME':check('FRAME',f,ev,ev/'SOURCE_118',REPO,ZIP),'DECISION':check('DECISION',d,ev,ev/'SOURCE_118',REPO,ZIP)}

# W1b pairwise-only coherent prose, true typed machine assertion
ev,f,d,c=base(); r=next(x for x in f['requirements'] if x['id']=='REQ-MULTIWAY-JOINT'); txt=('The three-way same-person joint is retained as an audit label, but the selected F4 result uses the pairwise product; higher-order membership is informational only and is not required for the operative result.')
for k in ('substantive_requirement','why_needed','loss_if_missing','first_consumer','architectural_consequence','proof_or_owner_hold'): r[k]=txt+' '+str(r.get(k,''))
resync(ev,f,d,c); report['cases']['W1b_pairwise_prose']={'FRAME':check('FRAME',f,ev,ev/'SOURCE_118',REPO,ZIP),'DECISION':check('DECISION',d,ev,ev/'SOURCE_118',REPO,ZIP)}

# W1c false identity fate with true excerpt and source fields
ev,f,d,c=base(); x=next(x for x in d['identity_dispositions'] if x['identity_id']=='K1-CAP-11'); x['design_effect']=('The three-way same-person joint is an audit label; the operative F4 result uses the pairwise product and higher-order membership is informational only.'); resync(ev,f,d,c); report['cases']['W1c_false_identity_fate']={'DECISION':check('DECISION',d,ev,ev/'SOURCE_118',REPO,ZIP)}

# W1d absent typed witness
ev,f,d,c=base(); r=next(x for x in f['requirements'] if x['id']=='REQ-MULTIWAY-JOINT'); r.pop('machine_assertion',None); resync(ev,f,d,c); report['cases']['W1d_absent_witness']={'FRAME':check('FRAME',f,ev,ev/'SOURCE_118',REPO,ZIP)}

# W2a original paraphrase in boundary prose, typed true
ev,f,d,c=base(); c['boundary_court']['T4']['positive']=('The measured attitude distribution supplies the operative institutional control relation; a separately sourced material issuer is optional for this boundary.')
c['boundary_court']['T6']['positive']=('Observed answers are available to the actor as mental content even where no encounter is recorded in the selected history.')
c['boundary_court']['T7']['positive']=('The performed fictional change is written into the empirical release as an updated observation for the next situation.')
resync(ev,f,d,c); report['cases']['W2a_paraphrase']={'C':check('C_INTEGRATED',c,ev,ev/'SOURCE_118',REPO,ZIP)}

# W2b false typed T4 + coherent prose
ev,f,d,c=base(); c['boundary_court']['T4']['machine_assertion']=dict(c['boundary_court']['T4']['machine_assertion'],survey_is_material_power=True); c['boundary_court']['T4']['positive']='The survey distribution is accepted as the material-power relation for this boundary.'
resync(ev,f,d,c); report['cases']['W2b_false_typed']={'C':check('C_INTEGRATED',c,ev,ev/'SOURCE_118',REPO,ZIP)}

# W2c changed C prose only
ev,f,d,c=base(); c['scientific_and_owner_boundary']='Observed attitude content is available to the actor and material world without encounter or independent material issuer.'; resync(ev,f,d,c); report['cases']['W2c_c_prose']={'C':check('C_INTEGRATED',c,ev,ev/'SOURCE_118',REPO,ZIP)}

# W5a relabel F5 hold
ev,f,d,c=base(); n=next(n for n in d['whole_machine_graph']['nodes'] if n['id']=='F5'); n['first_consumer']='NAMED_TYPED_CONSUMER_OR_OWNER_HOLD'; n['exact_hold']=''; resync(ev,f,d,c); report['cases']['W5a_relabel']={'DECISION':check('DECISION',d,ev,ev/'SOURCE_118',REPO,ZIP),'C':check('C_INTEGRATED',c,ev,ev/'SOURCE_118',REPO,ZIP)}

# W5b disconnect F5 + filler edges, counts unchanged
ev,f,d,c=base(); g=d['whole_machine_graph']; removed=[e for e in g['edges'] if e['from']=='F5' or e['to']=='F5']; g['edges']=[e for e in g['edges'] if not (e['from']=='F5' or e['to']=='F5')]; template=next(e for e in g['edges'] if e['from']=='I03' and e['to']=='F4')
for i in (1,2):
    e=copy.deepcopy(template); e['id']='E_FILL_%d'%i; g['edges'].append(e)
resync(ev,f,d,c); report['cases']['W5b_disconnect']={'DECISION':check('DECISION',d,ev,ev/'SOURCE_118',REPO,ZIP),'C':check('C_INTEGRATED',c,ev,ev/'SOURCE_118',REPO,ZIP),'nodes':len(g['nodes']),'edges':len(g['edges']),'removed_F5_edges':len(removed)}

# W3 forged external flag / conditional admit
ev,f,d,c=base(); c['verdict']='C_CONDITIONALLY_ADMIT_DESIGN'; c['actual_first_reader_verified']=True; c['external_custody_attestation']='EXTERNAL_RUNNER_VERIFIED'; resync(ev,f,d,c); report['cases']['W3_forged_external']={'C':check('C_INTEGRATED',c,ev,ev/'SOURCE_118',REPO,ZIP)}

# Usability: changed proposal narrative, source/typed obligations preserved
ev,f,d,c=base(); d['architecture_description']='A lawfully changed candidate proposal with the same source-bound typed obligations.'; d['single_selected_strategy']='Same source obligations, changed proposal narrative.'; resync(ev,f,d,c); report['cases']['USABILITY_changed_proposal']={'DECISION':check('DECISION',d,ev,ev/'SOURCE_118',REPO,ZIP)}

# Usability: changed source-fate narrative without code version
ev,f,d,c=base(); x=next(x for x in d['identity_dispositions'] if x['identity_id']=='K1-CAP-11'); x['design_effect']='A lawfully changed source-bound fate narrative for the same identity.'; resync(ev,f,d,c); report['cases']['USABILITY_changed_source_fate']={'DECISION':check('DECISION',d,ev,ev/'SOURCE_118',REPO,ZIP)}

(OUT/'r3_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
