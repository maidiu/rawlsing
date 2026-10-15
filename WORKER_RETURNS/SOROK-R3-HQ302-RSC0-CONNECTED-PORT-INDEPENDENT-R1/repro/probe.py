"""Live, read-only marker/import/source verification."""
import datetime, hashlib, importlib, importlib.metadata, json, os, pathlib, platform, subprocess, sys
RET=pathlib.Path(os.environ['RSC0_RETURN']); RT=pathlib.Path(os.environ['RSC0_RUNTIME'])
selector=json.loads((RET/'source_selector.json').read_text())
for row in selector['files']:
 raw=(RT/row['staging_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()==row['git_blob_sha1']
 assert hashlib.sha256(raw).hexdigest()==row['sha256']
modules={}
for name in ['port.adapter','port.envelope','port.provider_a','port.provider_b','port.pinned_producer','rawlsing_next.pre553_analytical_composition','rawlsing_next.pre553_empirical_possibility_provider','rawlsing_next.pre553_postastra_pe_generic_world_possibility','rawlsing_next.tests.n10e_empirical_slice_fixture']:
 m=importlib.import_module(name); p=pathlib.Path(m.__file__).resolve(); rel=p.relative_to(RT).as_posix()
 raw=p.read_bytes(); row=next(x for x in selector['files'] if x['staging_path']==rel)
 modules[name]=dict(file='$RSC0_RUNTIME/'+rel,git_blob_sha1=row['git_blob_sha1'],sha256=hashlib.sha256(raw).hexdigest(),verified=True)
marker=(RT/'runtime_marker.json').read_bytes()
obj=dict(schema='RSC0_LIVE_ENVIRONMENT_PROBE@1',at=datetime.datetime.now(datetime.timezone.utc).isoformat(),marker=json.loads(marker),marker_digest=hashlib.sha256(marker).hexdigest(),python=platform.python_version(),pytest=importlib.metadata.version('pytest'),jsonschema=importlib.metadata.version('jsonschema'),git=subprocess.check_output(['git','--version'],text=True).strip(),model='gpt-6.1-sol',effort='high',model_verification='Own current-session turn_context; no model/harness changes',modules=modules,verified_source_files=len(selector['files']),branch=subprocess.check_output(['git','branch','--show-current'],cwd=RET,text=True).strip(),head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=RET,text=True).strip(),source_grade='TEST_ONLY_SYNTHETIC; NO_SURVEY_MODEL_OR_ACTOR_CALLS')
(RET/'repro/live_environment_probe.json').write_text(json.dumps(obj,indent=2)+'\n')
print('LIVE_VERIFIED',len(modules),'PRIMARY_IMPORTS',len(selector['files']),'SOURCE_DATA_FILES',obj['marker_digest'])
