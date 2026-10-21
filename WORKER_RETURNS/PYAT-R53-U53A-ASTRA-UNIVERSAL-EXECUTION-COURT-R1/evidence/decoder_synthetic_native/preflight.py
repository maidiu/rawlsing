from pathlib import Path
import sys,json,hashlib,platform,importlib.metadata
T=Path(__file__).resolve().parent
import pyreadstat,pandas,numpy
for m in (pyreadstat,pandas,numpy):assert Path(m.__file__).resolve().is_relative_to(T/'venv')
assert sys.prefix==str(T/'venv')
assert sorted(str(p.relative_to(T/'source')) for p in (T/'source').rglob('*') if p.is_file())==['rawlsing_next/pre553_physical_decoder.py']
p=T/'source/rawlsing_next/pre553_physical_decoder.py';digest=hashlib.sha256(p.read_bytes()).hexdigest();assert digest=='a75a8ff72310949b84adbe682a01375c5dcf5dcee69e94e2a4a8a9b39e17017b'
installation=json.loads((T/'installation.json').read_text());packages=[{'name':x['metadata']['name'],'version':x['metadata']['version'],'distribution_sha256':x['download_info']['archive_info']['hash'].split('=',1)[1]} for x in installation['install']]
q={'schema':'U53A_DECODER_SYNTHETIC_QUALIFICATION@1','source_commit':'f148f9ba34deb0ae2ad3983fe94bbcef8f004b03','source_path':'rawlsing_next/pre553_physical_decoder.py','source_blob':'d2a074a41fb556a1cd5928a5fe1421ef3672a4e5','source_sha256':digest,'same_blob_at_observed_live_integration':'b21152852d1518236901733fd3c786a6e8857a0c','python':sys.version,'platform':platform.platform(),'isolated_venv':True,'system_site_packages':False,'invocation':'venv/bin/python -I -B harness.py','packages':packages,'scope':'Direct SAV/DTA decoder immutable-path and replacement-between-decode-and-iteration characterization; numeric synthetic fixtures only','not_qualified':'No original source run, historical census, C11/Batch chain, native date/MR/encoding qualification or external science/authority','source_files_allowlisted':1,'raw_original_files':0,'initial_source_inventory_verified':True,'preflight_correction':'pip22 installation report uses archive_info.hash, not hashes. Initial preflight stopped at report parsing before synthetic fixture generation; corrected metadata reader only.'}
(T/'qualification.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps({'qualified':True,'source_sha256':digest,'packages':[(x['name'],x['version']) for x in packages]}))
