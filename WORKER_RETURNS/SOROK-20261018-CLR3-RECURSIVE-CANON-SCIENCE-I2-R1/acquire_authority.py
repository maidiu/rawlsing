"""Read exact authority objects; never check them out or change owners."""
import json, subprocess
from reconstruct import ROOT, WT, START, materialize, git

CURRENT='49b585d01029d29230e4cb4b0c6d23cc12884f75'
TD='9cf9df5932c0826c028d95d4b0773e5264edd6c7'
RELEASE='data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/'
SYNTH='data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/'
GOV='data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/CANONICAL_GOVERNANCE_R1/'

if __name__=='__main__':
    refs=json.loads((ROOT/'reconstructed/clr3/sources/owner_authority_refs.json').read_text())
    requests={(r['commit'],r['path']) for r in refs}
    requests|={(CURRENT,r['path']) for r in refs}
    directories=['W0_AUTHORITY_FOUNDATION/ADP_008_V3_DEVELOPMENTAL_PHASE','W0_AUTHORITY_FOUNDATION/ADP_016_V3_CAUSAL_MEMORY','W0_AUTHORITY_FOUNDATION/ADP_019_V3_EXTERNAL_ADMISSION','W0_AUTHORITY_FOUNDATION/ADP_020_V3_CAUSAL_RNG','W1_CRITICAL_AUTHORITY_EXPANSION/ADP_017_V3_ACTOR_ACCESS','W1_CRITICAL_AUTHORITY_EXPANSION/ADP_021_V3_HYBRID_SCHEDULER','W1_CRITICAL_AUTHORITY_EXPANSION/CAN_008_V3_PRESSURE_FLOW_RESPONSE','W1_CRITICAL_AUTHORITY_EXPANSION/CAN_011_V3_MIDDLE_STATE','W2_AUTHORITY_CONTRACT_COMPLETION/ADP_007_V3_ACTOR_INITIALIZATION','W2_AUTHORITY_CONTRACT_COMPLETION/ADP_015_V3_RELATIONSHIP_GENEALOGY']
    for d in directories:
        for suffix in ['AUTHORITY.json','AUTHORITY.md']:
            requests.add((CURRENT,RELEASE+d+'/'+suffix))
    tddir='data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/recalibration/TD_R05_V3_DEVELOPMENTAL_RUNTIME/'
    for name in ['LATEST_EXTANT_V3_V2_SOURCE_MANIFEST.json','LATEST_EXTANT_V3_V2_BASELINE.md','BASELINE_AMENDMENT.md','RESULT.md']:
        requests.add((TD,tddir+name))
    for name in ['00_READ_ME_FIRST.md','CURRENT_PROGRESS.md','00C_HQ_PROMPT_DISPENSATION_AGENT_ROUTING_AND_ORCHESTRATION_CONSTITUTION_R1.md']:
        requests.add((START,'SOROK_PRODUCT_CONTROL_ROOM/'+name))
    for name in ['CURRENT_AUTHORITY_INDEX.tsv','CURRENT_SEMANTIC_LAW_INDEX.tsv','DELEGATED_AUTHORITY_INDEX.tsv']:
        requests.add((CURRENT,GOV+name))
    for path in ['state/CURRENT_STATE.md','integration/V3_COMPLETION_IMPLEMENTATION_RULING.md','integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md','integration/W1_AUTHORITY_EXPANSION_CLOSURE_RULING.md']:
        requests.add((CURRENT,'data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/'+path))
    requests.add((CURRENT,RELEASE+'W0_AUTHORITY_FOUNDATION/CAN_014_V3_DERIVED_SCHEDULE/AUTHORITY.json'))
    requests.add((CURRENT,RELEASE+'W1_CRITICAL_AUTHORITY_EXPANSION/ADP_010_V3_ENCOUNTER_EXPOSURE/AUTHORITY.json'))
    for path in ['rawlsing_next/v3_psepf_zero_positive_guard.py','rawlsing_next/wsc_gt0_v3_runtime.py']:
        requests.add((CURRENT,path))
    for name in ['02_HQ_CAN008_R2_ADOPTION_R1.md']:
        requests.add((CURRENT,SYNTH+'PFF_U1_SHARED_PERSON_TRANSITION_GATE_R1/CAN008_R2_AUTHORITY_CANDIDATE_R1/'+name))
    for name in ['03_VOZHD_HQ_U1C_U1H_SYNTHESIS_AND_CAN008_R2_DISPOSITION_R1.md','04_ACTIVE_CAN008_R2_GATE_R1.md']:
        requests.add((CURRENT,SYNTH+'PFF_U1_SHARED_PERSON_TRANSITION_GATE_R1/'+name))
    selected=[];missing=[]
    for ref,path in sorted(requests):
        entry=git('ls-tree',ref,'--',path).decode().strip()
        if not entry:missing.append(dict(commit=ref,path=path));continue
        blob=entry.split()[2]
        selected.append((ref,path,blob))
    # One bounded bulk fetch avoids per-file promisor fetch/repack churn.
    subprocess.run(['git','-C',str(WT),'-c','gc.auto=0','fetch','--no-tags','--no-write-fetch-head','origin','--stdin'],input='\n'.join(sorted({b for _,_,b in selected}))+'\n',text=True,check=True)
    rows=[]
    for ref,path,blob in selected:
        dest='authority/'+ref[:12]+'/'+path.split('/')[-2]+'/'+path.split('/')[-1]
        rows+=materialize(ref,path,dest)
    (ROOT/'evidence/authority_manifest.json').write_text(json.dumps(dict(files=rows,missing=missing,current_premain=CURRENT),indent=2)+'\n')
    print(json.dumps(dict(files=len(rows),missing=missing)))
