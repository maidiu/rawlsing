from pathlib import Path
import sys,subprocess,shutil,json
R=Path(__file__).resolve().parents[1];RT=R/'runtime_root';src=RT/'pv2i_cold';dest=RT/'pv2i_actual_receipt_attack';shutil.copytree(src,dest)
p=next((dest/'ledger').rglob('b01e_side_effects.jsonl'));lines=p.read_text().splitlines();v=json.loads(lines[0]);before=v['result_refs'][0];v['result_refs'][0]={'kind':before['kind'],'object_id':'urn:rawlsing:pre553:EmpiricalFact:sha256:'+'f'*64,'content_hash':'f'*64};lines[0]=json.dumps(v,sort_keys=True);p.write_text('\n'.join(lines)+'\n')
cmd=[sys.executable,str(R/'repro/cold_child.py'),str(dest),'replay','cold_actual_result_ref_tamper'];c=subprocess.run(cmd,capture_output=True,text=True);(R/'observations/cold_actual_result_ref_tamper.stdout').write_text(c.stdout+c.stderr)
out={'actual_changed_field':'journal[0].result_refs[0]','original_ref':before,'forged_ref':v['result_refs'][0],'argv':cmd,'exit':c.returncode,'stdout':c.stdout,'stderr':c.stderr,'classification':'REFUSED' if c.returncode else 'ACCEPTED_OR_IGNORED_NEEDS_ADJUDICATION'}
(R/'observations/cold_actual_result_ref_tamper.json').write_text(json.dumps(out,indent=2)+'\n');print('ACTUAL_RECEIPT_REF_TAMPER_EXIT',c.returncode)
