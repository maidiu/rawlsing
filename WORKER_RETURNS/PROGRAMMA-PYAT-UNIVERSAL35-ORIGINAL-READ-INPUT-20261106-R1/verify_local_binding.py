import json, shutil, tempfile
from pathlib import Path
from dataclasses import replace
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.source_configuration.reader import source_read_request_from_config
import sys
sys.path.insert(0,'WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-ORIGINAL-READ-INPUT-20261106-R1')
from local_engineering_resolver import LocalEngineeringResolver
from rawlsing_next.pre553_source_read_admission import SourceReadAdmissionRefusal
p='.local-logs/pyat-universal35/original-read-input/local-engineering-read-grant.json'
r=LocalEngineeringResolver(p); lib=SourceConfigLibrary.from_pinned_r157()
valid=0
for sid in lib.source_ids():
 cfg=lib.load_original(sid); req=source_read_request_from_config(cfg,host=r.grant['host'],purpose=r.grant['purpose'],consumer_use=r.grant['consumer_use'],semantic_use_scope=r.grant['semantic_use_scope'])
 d=r.resolve_current(req); assert d.currentness=='CURRENT_GRANTED'; valid+=1
print('valid_decisions',valid)
req=source_read_request_from_config(lib.load_original('SRC09'),host=r.grant['host'],purpose=r.grant['purpose'],consumer_use=r.grant['consumer_use'],semantic_use_scope=r.grant['semantic_use_scope'])
for label,kw in [('host',{'host':'wrong-host'}),('purpose',{'purpose':'WRONG'}),('consumer',{'consumer_use':'WRONG'}),('scope',{'semantic_use_scope':('OTHER',)}),('sha',{'source_sha256':'f'*64})]:
 try: r.resolve_current(replace(req,**kw)); print(label,'UNEXPECTED_PASS')
 except SourceReadAdmissionRefusal as e: print(label,'REFUSED',e.code)
# changed/revoked grant copies
with tempfile.TemporaryDirectory() as td:
 g=json.load(open(p)); g['revocation_ref']={'kind':'REVOCATION','object_id':'urn:test:revoked','content_hash':'a'*64}
 gp=Path(td)/'revoked.json'; gp.write_text(json.dumps(g)); 
 try: LocalEngineeringResolver(gp,expected_grant_sha256=None,expected_user_authorization_sha256=None); print('revoked_instantiation_unexpected_pass')
 except SourceReadAdmissionRefusal as e: print('revoked_grant','REFUSED',e.code)
 g2=json.load(open(p)); g2['host']='changed-host'; gp2=Path(td)/'changed.json'; gp2.write_text(json.dumps(g2))
 try: LocalEngineeringResolver(gp2); print('changed_digest_unexpected_pass')
 except SourceReadAdmissionRefusal as e: print('changed_digest','REFUSED',e.code)
