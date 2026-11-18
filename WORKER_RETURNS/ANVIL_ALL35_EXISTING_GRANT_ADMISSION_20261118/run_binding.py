#!/usr/bin/env python3
"""Request-only SRC04 binding and SRC17 reuse-scope check; no source I/O."""
from __future__ import annotations
import json,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
SNAP=Path(os.environ.get('ANVIL_R157_SNAPSHOT','/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/anvil-aee954-r157')).resolve()
sys.path.insert(0,str(SNAP))
from existing_grant_binding import ConfigBinding, ExternalTrust, bind_existing_grant, check_src17_reuse_scope
cfg=ConfigBinding(
 **{k:v for k,v in json.loads((HERE/'fixtures/SRC04_CONFIG_BINDING.json').read_text()).items() if k!='metadata_freeze_refs'},
 metadata_freeze_refs=tuple(json.loads((HERE/'fixtures/SRC04_CONFIG_BINDING.json').read_text())['metadata_freeze_refs']),
)
tp=json.loads((HERE/'TRUST_POLICY.json').read_text());trust=ExternalTrust(**{k:tp[k] for k in ('grant_sha256','config_file_sha256','config_canonical_sha256','config_binding_sha256','current_issuer','current_public_key_hex','current_evidence_sha256')})
cur=os.environ.get('ANVIL_CURRENT_EVIDENCE')
res=bind_existing_grant(grant_path=HERE/'fixtures/SRC04_FULL_SOURCE_GRANT.json',config=cfg,trust=trust,current_evidence_path=Path(cur) if cur else None)
(HERE/'SRC04_BINDING.json').write_text(json.dumps(res.as_dict(),indent=2,sort_keys=True)+'\n')
scope=check_src17_reuse_scope(grant_path=HERE/'fixtures/SRC17_USER_GRANT.json',authentication_path=HERE/'fixtures/SRC17_GRANT_AUTHENTICATION.json',expected_grant_sha256='d6272ba68d737fa9da27704e18bf6ee00ef1d31f685ba76f84f4a0dcc4764e3d',expected_authentication_sha256='f7fb429bb77779556e2e0a591ea2b089bf1f0a97d85d059545baf5fd66dd052b')
(HERE/'SRC17_SCOPE.json').write_text(json.dumps(scope,indent=2,sort_keys=True)+'\n')
print(json.dumps({'src04_status':res.status,'grant':res.grant_sha256,'src17_reuse':scope['reusable_for_src04_binding'],'src17_i03_i05':scope['reusable_for_i03_i05']},sort_keys=True))
