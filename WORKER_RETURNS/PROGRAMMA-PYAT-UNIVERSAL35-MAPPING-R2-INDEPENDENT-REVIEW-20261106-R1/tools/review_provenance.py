"""Independent provenance/denominator probes for A R2 mapping review."""
from __future__ import annotations
import copy, json, subprocess, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
import sys
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
R157='1924499ef52403a0f331b8aff9b7c7eff99bf1e2'
from rawlsing_next.source_configuration.corrections import SourceCorrectionError, apply_source_config_corrections
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.source_configuration.provider import GitObjectProvider
from rawlsing_next.source_configuration.schema import load_source_config_bytes


def sh(*args): return subprocess.check_output(args,text=True).strip()
def base(path): return json.loads(GitObjectProvider().read_bytes(path).decode('utf-8'))
def outcome(fn):
    try: return {'state':'OK','value':fn()}
    except Exception as exc: return {'state':'REFUSED','error':type(exc).__name__+':'+str(exc)}


def main():
    lib=SourceConfigLibrary.from_pinned_r157()
    paths={sid:lib.record(sid)['original_config_path'] for sid in ('SRC31','SRC32','SRC04','SRC16','SRC24','SRC25','SRC33','SRC26')}
    doc32=base(paths['SRC32']); doc31=base(paths['SRC31'])
    right=lambda d,p: apply_source_config_corrections(d,base_commit=R157,base_config_path=p)
    _, applied32=right(doc32,paths['SRC32']); _, applied31=right(doc31,paths['SRC31'])
    no_prov=apply_source_config_corrections(doc32)[1]
    wrong_sha=copy.deepcopy(doc32); wrong_sha['identity']['expected_source_sha256']='f'*64
    wrong_base=copy.deepcopy(doc32); wrong_base['config_revision']+=1
    wrong_sha_applied=apply_source_config_corrections(wrong_sha,base_commit=R157,base_config_path=paths['SRC32'])[1]
    wrong_base_applied=apply_source_config_corrections(wrong_base,base_commit=R157,base_config_path=paths['SRC32'])[1]
    wrong_commit=outcome(lambda: apply_source_config_corrections(doc32,base_commit='f'*40,base_config_path=paths['SRC32']))
    wrong_path=outcome(lambda: apply_source_config_corrections(doc32,base_commit=R157,base_config_path='wrong/SRC32.config.json'))
    raw=GitObjectProvider().read_bytes(paths['SRC32'])
    wrong_loaded_path=outcome(lambda: load_source_config_bytes(raw,base_commit=R157,base_config_path='wrong/SRC32.config.json'))
    class FakeProvider:
        commit='f'*40
        def __init__(self): self.real=GitObjectProvider()
        def read_bytes(self,p): return self.real.read_bytes(p)
        def exists(self,p): return self.real.exists(p)
        def sha256(self,p): return self.real.sha256(p)
    fake=SourceConfigLibrary(provider=FakeProvider())
    wrong_provider=outcome(lambda: fake.load_original('SRC32'))
    # Tamper a scratch registry copy, not the resource.
    registry=json.loads(Path('rawlsing_next/source_configuration/corrections/SOURCE_CONFIGURATION_CORRECTIONS.json').read_text())
    for entry in registry['entries']:
        if entry['source_id']=='SRC32': entry['base_config_path']='wrong/SRC32.config.json'
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'registry.json'; p.write_text(json.dumps(registry))
        registry_path=outcome(lambda: apply_source_config_corrections(doc32,registry_path=p,base_commit=R157,base_config_path=paths['SRC32']))
        registry_commit=outcome(lambda: apply_source_config_corrections(doc32,registry_path=p,base_commit='f'*40,base_config_path=paths['SRC32']))
    restored32=right(doc32,paths['SRC32'])[1]; restored31=right(doc31,paths['SRC31'])[1]
    curr=json.loads(sh('git','show',f'{R157}:{paths["SRC31"]}').rstrip())
    prev=json.loads(sh('git','show','ef43bbbbb16ac8925056f7c5bed522d6b1200ea5:rawlsing_next/source_configuration/corrections/SOURCE_CONFIGURATION_CORRECTIONS.json'))
    now=json.loads(Path('rawlsing_next/source_configuration/corrections/SOURCE_CONFIGURATION_CORRECTIONS.json').read_text())
    def entry(reg,sid): return next(e for e in reg['entries'] if e['source_id']==sid)
    src31_unchanged=json.dumps(entry(prev,'SRC31'),sort_keys=True)==json.dumps(entry(now,'SRC31'),sort_keys=True)
    fixture_empty=lib.load_fixture_config('SRC32').corrections_applied==() and lib.load_fixture_config('SRC31').corrections_applied==()
    unrelated_empty=lib.load_original('SRC09').corrections_applied==()
    counts={sid:len(lib.load_original(sid).corrections_applied) for sid in paths}
    baseline=lib.document.get('baseline')
    payload={'schema':'PYAT_UNIVERSAL35_MAPPING_R2_PROVENANCE_REVIEW@1','right_counts':{'SRC31':len(applied31),'SRC32':len(applied32)},'no_provenance_applied':len(no_prov),'wrong_source_sha_applied':len(wrong_sha_applied),'wrong_base_hash_applied':len(wrong_base_applied),'wrong_commit':wrong_commit,'wrong_path':wrong_path,'wrong_loaded_path':wrong_loaded_path,'wrong_provider_commit':wrong_provider,'tampered_registry_path':registry_path,'tampered_registry_commit':registry_commit,'exact_restore':{'SRC31':len(restored31),'SRC32':len(restored32)},'src31_entry_unchanged':src31_unchanged,'fixture_empty':fixture_empty,'unrelated_empty':unrelated_empty,'correction_counts':counts,'index_baseline':baseline,'source_count':len(lib.source_ids()),'index_sources':len(lib.document['sources'])}
    out=ROOT/'WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-MAPPING-R2-INDEPENDENT-REVIEW-20261106-R1/results/provenance_probe.json'
    out.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps(payload,sort_keys=True)[:8000])

if __name__=='__main__': main()
