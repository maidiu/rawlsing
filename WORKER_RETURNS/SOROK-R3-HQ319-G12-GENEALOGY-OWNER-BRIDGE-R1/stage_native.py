"""Stage reviewed native candidate owner closure and the actual production guard."""
from stage_sources import ROOT,git
import hashlib,json
def main():
    rows=[]
    sets=[('native_candidate','ee6a48b40247b113c614fe2099d4c443e8dd7bb7',
           'WORKER_RETURNS/SOROK-R3-HQ308-CAN2-LAW-CAUSAL-REPAIR-R1/candidate',
           ['adopted_contract.py','candidate_registry_fixture.py','can008_candidate_rule.py','owner_transitions.py','positive_chain.py']),
          ('production','9aa7e19817823aa1642c7c222093098d701c08fe','rawlsing_next',
           ['v3_psepf_zero_positive_guard.py'])]
    for alias,commit,prefix,names in sets:
        for name in names:
            path=prefix+'/'+name;b=git('show',commit+':'+path)
            blob=git('rev-parse',commit+':'+path).decode().strip()
            assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
            d=ROOT/'sources'/alias/name;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(b)
            rows.append(dict(commit=commit,path=path,git_blob_sha1=blob,sha256=hashlib.sha256(b).hexdigest(),staged_path=str(d.relative_to(ROOT))))
    (ROOT/'native_source_manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('Verified native closure:',len(rows))
if __name__=='__main__':main()
