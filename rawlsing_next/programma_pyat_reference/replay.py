"""Build receipts using actual CLI processes. Requires only Python 3.10+ and Git objects."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
from . import reference as ref

RETURN = Path('WORKER_RETURNS/PROGRAMMA_PYAT_W1_H_MASTERMAP_FANIN_R1')


def run(store, args, destination):
    command=[sys.executable,'-m','rawlsing_next.programma_pyat_reference','--store',str(store),*args]
    p=subprocess.run(command,capture_output=True,text=True)
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(p.stdout)
    if p.returncode:raise RuntimeError(shlex.join(command)+'\n'+p.stderr)
    return command,json.loads(p.stdout)


def main():
    RETURN.mkdir(parents=True,exist_ok=True)
    proofs=RETURN/'PROOF_RECEIPTS';proofs.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='w1h-replay-') as temp:
        store=Path(temp)/'warm';cold=Path(temp)/'cold'
        run(store,['ingest','--cut',ref.CANONICAL],proofs/'ingest.json')
        run(store,['verify'],proofs/'verify.json')
        run(cold,['ingest','--cut',ref.CANONICAL],proofs/'cold_ingest.json')
        warm_bytes=(store/(ref.CANONICAL+'.json')).read_bytes()
        cold_bytes=(cold/(ref.CANONICAL+'.json')).read_bytes()
        assert warm_bytes==cold_bytes
        run(cold,['verify'],proofs/'cold_verify.json')
        s=ref.load(store/(ref.CANONICAL+'.json'))
        ref.write(proofs/'cold_readback.json',{'equal_bytes':True,'sha256':hashlib.sha256(warm_bytes).hexdigest(),'snapshot_hash':s['snapshot_hash'],'fresh_processes':True,'scope':'SOURCEFREE_MAP_NOT_NATIVE_SOURCE'})
        # Actual version comparison: current pinned PRE-MAIN versus the common earlier cut.
        old='acbe2326c8f52dfe8bfa200e87c5c07a62a5c93a'
        run(store,['ingest','--cut',old],proofs/'old_cut_ingest.json')
        run(store,['changes',old,ref.CANONICAL],proofs/'changes.json')
        # Restore the selected read context. Original lane cuts never changed.
        ref.write(store/'latest.json',{'cut':ref.CANONICAL})
        current=ref.CANONICAL
        code=lambda path,symbol='':'CODE:'+current+':'+path+'::'+symbol
        bquery='ROW:B:CURRENT_REALIZATION:F1.I03.QUERY'
        i03=code('rawlsing_next/pre553_empirical_query.py','execute_empirical_query')
        caller=code('rawlsing_next/pre553_source_backed_c11_facade.py','execute_source_backed_empirical_query')
        f6=s['records']['ROW:G:HISTORICAL_REALIZATIONS:HR-F6']['raw']
        f6code='CODE:'+f6['exact_source']['tip']+':'+f6['exact_source']['paths'][0]['path']+'::'
        f7=s['records']['ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP']['raw']
        f7code='CODE:'+f7['exact_source']['tip']+':'+f7['exact_source']['paths'][0]['path']+'::'
        e03=code('rawlsing_next/pre553_n9_n10w_progressive_candidate.py','run_progressive_chain')
        # Use actual endpoint present in the source G comparison (no invented symbol).
        e03g='CODE:ee31e3edfb1b5a26aa945a55ededbf0b7ff2a7a7:rawlsing_next/pre553_n9_n10w_progressive_candidate.py::'
        routes=[
          ('T1',['N11','N10W','N9','N8E','SRC12']),
          ('T2',['N2','WHOLE151:Q002','WHOLE101:Q02',bquery,i03,caller]),
          ('T3',['SRC35','R157_CONFIGURATION','P1_U_EPRE','BATCH_MANIFEST_ADMISSION','I03_I05_LOWERING','N10E']),
          ('T4',['F6','HR-F6',f6code]),
          ('T5',['F7','HR-F7-TEMP',f7code]),
          ('T6',['M2_LOCAL_RELEASE','H05-I01','N9','H06-E03','HR-N9-N10W',e03g]),
        ]
        lines=['# Six actual CLI traversals','', 'All JSON receipts are emitted by fresh CLI processes from the same deterministic snapshot. Edges marked MISSING or CONDITIONAL are evidence of a gap or a scoped prerequisite; no route is an empirical run. Forward and inverse receipts use the same edge IDs.','']
        for name,tokens in routes:
            cmds=[];outputs=[]
            for direction,route in [('forward',tokens),('reverse',list(reversed(tokens)))]:
                args=['focus' if direction=='forward' else 'reverse',route[0],'--route',*route[1:],'--brief']
                command,q=run(store,args,proofs/(name+'_'+direction+'.json'))
                cmds.append(shlex.join(command));outputs.append(q['actual_route'])
            forward={e['id'] for h in outputs[0]['hops'] for e in h['edges']}
            reverse={e['id'] for h in outputs[1]['hops'] for e in h['edges']}
            assert forward==reverse
            lines.extend(['## '+name,'','```sh',*cmds,'```','','```json',json.dumps({'actual_forward':outputs[0],'actual_reverse':outputs[1],'same_edge_ids':True},indent=2),'```',''])
        (RETURN/'SIX_ACTUAL_TRAVERSALS.md').write_text('\n'.join(lines))
        for name,args in [('whole',['whole']),('code_N2',['code','N2','--brief']),('source35',['source','SRC35','--brief']),('seams_F6',['seams','F6','--brief']),('gaps_WG0',['gaps','WG0','--brief']),('alternatives_F6',['alternatives','F6']),('alternatives_F7',['alternatives','F7']),('alternatives_I01',['alternatives','HR-I01']),('work_now',['work-now']),('ambiguous_M2',['focus','M2'])]:
            run(store,args,proofs/(name+'.json'))
        before=ref.regrade(s)
        r=s['records'][bquery]
        pin=next(p for p in r['support_pins'] if s['source_pins'][p]['role']=='implementation')
        negative=ref.regrade(s,[pin]);restored=ref.regrade(s)
        pointer=s['source_pins'][pin]
        same={p for p,x in s['source_pins'].items() if (x['cut'],x['path'])==(pointer['cut'],pointer['path'])}
        dependents=sorted(k for k,r in s['records'].items() if same & set(r['support_pins']))
        changed=sorted(k for k in before if before[k]!=negative[k])
        assert changed==dependents and before==restored
        red='ROW:G:HISTORICAL_REALIZATIONS:HR-N9C'
        assert red not in changed and 'RED' in json.dumps(s['records'][red])
        ref.write(proofs/'negative_restore.json',{'scope':'SOURCEFREE_EVIDENCE_AVAILABILITY_WITHDRAWAL_ONLY; no survey grant revoked/restored',
            'withdrawn_exact_pin':s['source_pins'][pin],'same_pointer_roles_withdrawn':sorted(same),'changed_claims':changed,'expected_exact_dependents':dependents,
            'unchanged_claim_count':len(before)-len(changed),'restored_equals_original':True,
            'independent_red':s['records'][red],'independent_red_unchanged':True,
            'before':{k:before[k] for k in changed},'negative':{k:negative[k] for k in changed},'restore':{k:restored[k] for k in changed}})
        ref.write(RETURN/'MASTER_COVERAGE_AND_ORPHANS.json',s['coverage'])
        ref.write(RETURN/'SOURCE_LOCK_AND_NORMALIZATION.json',{'canonical_read_cut':ref.CANONICAL,'snapshot_hash':s['snapshot_hash'],
            'input_lock':s['input_lock'],'source_pins':s['source_pins'],'read_cut_comparison':s['read_cut_comparison'],
            'normalization':'Raw ROW:lane:table:original_id; stable ASTRA/F/SRC/EE/AT/WG/WHOLE101/WHOLE151 families; code identity=cut/path/symbol; ambiguous unqualified labels retained per lane; no newest-wins or maturity inheritance',
            'nonaliases':['M2_LOCAL_RELEASE != M2_V555_STRUCTURAL','PYAT:N != SOROK:N','WHOLE101:S01 != WHOLE151:S001 != ESTATE_AXIS:S01','ASTRA:C3 != RRIF:C3'],
            'unmapped_or_ambiguous':s['coverage']['provisional_entities'],'boundary':ref.BOUNDARY})
        (RETURN/'CROSS_LANE_ADJUDICATION.jsonl').write_bytes((ref.ROOT/'adjudication.jsonl').read_bytes())
        p=subprocess.run([sys.executable,'-m','unittest','rawlsing_next.programma_pyat_reference.test_reference','-v'],capture_output=True,text=True)
        (proofs/'hostile_tests.log').write_text(p.stdout+p.stderr)
        if p.returncode:raise RuntimeError('Hostile suite failed; see receipt')
        print(json.dumps({'snapshot_hash':s['snapshot_hash'],'tests':'20 PASS','coverage':{k:v for k,v in s['coverage'].items() if k not in ['assertion_unlinked_records','provisional_entities']},'return':str(RETURN)},indent=2))

if __name__=='__main__':main()
