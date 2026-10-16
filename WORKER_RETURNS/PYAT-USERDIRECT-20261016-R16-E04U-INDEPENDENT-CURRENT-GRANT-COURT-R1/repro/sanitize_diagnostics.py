"""Portable new diagnostics only; never alter frozen original input bytes."""
import pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1];rows=[]
files=[*sorted((R/'observations').rglob('*.json')),*sorted((R/'observations').rglob('*.stdout')),*sorted((R/'observations').rglob('*.xml')),R/'03_TESTS_AND_ORIGINAL_JUNIT_RECONCILIATION.json',R/'07_ACTUAL_NATIVE_IMPORT_AND_CALL_PROOF.json']
for p in files:
 before=p.read_bytes();s=before.decode();token='&lt;RETURN&gt;' if p.suffix=='.xml' else '<RETURN>';home='&lt;USER_HOME&gt;' if p.suffix=='.xml' else '<USER_HOME>'
 after=s.replace(str(R),token).replace(str(pathlib.Path.home()),home).encode()
 if after!=before:
  p.write_bytes(after);rows.append(dict(path=str(p.relative_to(R)),raw_sha256=hashlib.sha256(before).hexdigest(),portable_sha256=hashlib.sha256(after).hexdigest()))
report=R/'DIAGNOSTIC_NORMALIZATION.json'
if rows:report.write_text(json.dumps(dict(method='Only generated diagnostic paths normalized. XML placeholders escaped. Frozen original code/oracle/assertion files excluded. Values, refs, case IDs and exits untouched.',files=rows),indent=2)+'\n')
print('Normalized generated diagnostic files:',len(rows))
