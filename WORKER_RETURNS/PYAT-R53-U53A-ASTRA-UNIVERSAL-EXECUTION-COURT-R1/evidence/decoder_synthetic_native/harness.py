"""Native numeric SAV/DTA custody characterization; synthetic source files only."""
from pathlib import Path
import sys,json,hashlib,os
T=Path(__file__).resolve().parent
q=json.loads((T/'qualification.json').read_text())
sys.path.insert(0,str(T/'source'))
import pyreadstat,pandas as pd
from rawlsing_next import pre553_physical_decoder as decoder
assert Path(decoder.__file__).resolve()==T/'source/rawlsing_next/pre553_physical_decoder.py'
assert hashlib.sha256(Path(decoder.__file__).read_bytes()).hexdigest()==q['source_sha256']
assert pyreadstat.__version__=='1.3.6'
fixtures=T/'synthetic_fixtures';fixtures.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def values(i):return [c.raw_value for c in i.iter_cells(batch_size=1)]
results=[]
for kind in ['sav','dta']:
 path=fixtures/('fixture.'+kind);replacement=fixtures/('replacement.'+kind)
 writer=pyreadstat.write_sav if kind=='sav' else pyreadstat.write_dta
 reader=decoder.decode_sav if kind=='sav' else decoder.decode_dta
 writer(pd.DataFrame({'synthetic_value':[1.0,2.0]}),str(path))
 before=sha(path);inc=reader(path,expected_source_sha256=before);meta=inc.physical_metadata_digest
 assert inc._frame is None and inc.row_count==2
 assert values(inc)==[1.0,2.0] and inc.source_sha256==before
 results.append({'case':kind+'_immutable_control','pass':True,'values':[1.0,2.0],'sha256':before})
 writer(pd.DataFrame({'synthetic_value':[91.0,92.0]}),str(replacement));after=sha(replacement);assert before!=after
 os.replace(replacement,path)
 observed=values(inc)
 assert observed==[91.0,92.0] and inc.source_sha256==before and inc.physical_metadata_digest==meta
 results.append({'case':kind+'_path_replacement','pass':True,'engineering_result':'NEW_BYTES_EMITTED_UNDER_OLD_INCIDENCE_DIGEST','old_source_sha256':before,'actual_source_sha256':after,'reported_source_sha256':inc.source_sha256,'metadata_digest_unchanged':inc.physical_metadata_digest==meta,'observed_values':observed,'original_row_count':inc.row_count})
 try:reader(path,expected_source_sha256=before)
 except decoder.DecoderError as e:
  assert 'source sha256 mismatch' in str(e);results.append({'case':kind+'_stale_expected_hash_rejected_on_new_decode','pass':True,'refusal':str(e)})
 else:raise AssertionError('new decode accepted stale hash')
 fresh=reader(path,expected_source_sha256=after);assert values(fresh)==[91.0,92.0] and fresh.source_sha256==after
 results.append({'case':kind+'_new_expected_hash_control','pass':True,'sha256':after})
assert len(results)==8
receipt={'schema':'U53A_DECODER_NATIVE_SYNTHETIC_CUSTODY@1','passed':8,'failed':0,'cases':results,'source_blob':q['source_blob'],'source_sha256':q['source_sha256'],'original_source_reads':0,'scope':'Direct exact decoder; two generated numeric formats; unchanged metadata/schema and changed cell values; no C11/backend/Batch propagation tested','no_semantic_or_authority_issuance':True}
(T/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'passed':8,'failed':0,'format_findings':['SAV_REPLACEMENT_REPRODUCED','DTA_REPLACEMENT_REPRODUCED'],'receipt':str(T/'receipt.json')}))
