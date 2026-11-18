#!/usr/bin/env python3
"""Request-only SRC04 grant binding and SRC17 reuse-scope check; no source I/O."""
from __future__ import annotations
import json,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
SNAP=Path(os.environ.get('ANVIL_R157_SNAPSHOT','/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/anvil-aee954-r157')).resolve()
sys.path.insert(0,str(SNAP))
from existing_grant_binding import ConfigBinding,ExternalTrust,ExistingGrantResolver,bind_existing_grant,check_src17_reuse_scope
raw=json.loads((HERE/'fixtures/SRC04_CONFIG_BINDING.json').read_text())
cfg=ConfigBinding(**{k:v for k,v in raw.items() if k!='metadata_freeze_refs'},metadata_freeze_refs=tuple(raw['metadata_freeze_refs']))
tp=json.loads((HERE/'TRUST_POLICY.json').read_text());trust=ExternalTrust(**{k:tp[k] for k in ('grant_sha256','grant_path','config_file_sha256','config_canonical_sha256','config_binding_sha256')})
res=bind_existing_grant(grant_path=HERE/'fixtures/SRC04_FULL_SOURCE_GRANT.json',config=cfg,trust=trust)
resolver=ExistingGrantResolver(HERE/'fixtures/SRC04_FULL_SOURCE_GRANT.json',trust,res.request)
# Existing callback contract: same decision on both pre/post boundaries.
pre=resolver.resolve_current(res.request); post=resolver.resolve_current(res.request)
assert pre==post==res.decision and resolver.calls==2
(HERE/'SRC04_BINDING.json').write_text(json.dumps({**res.as_dict(),'resolver_calls_pre_post':resolver.calls,'pre_post_decision_identical':pre==post},indent=2,sort_keys=True)+'\n')
scope=check_src17_reuse_scope(grant_path=HERE/'fixtures/SRC17_USER_GRANT.json',authentication_path=HERE/'fixtures/SRC17_GRANT_AUTHENTICATION.json',expected_grant_sha256='d6272ba68d737fa9da27704e18bf6ee00ef1d31f685ba76f84f4a0dcc4764e3d',expected_authentication_sha256='f7fb429bb77779556e2e0a591ea2b089bf1f0a97d85d059545baf5fd66dd052b')
(HERE/'SRC17_SCOPE.json').write_text(json.dumps(scope,indent=2,sort_keys=True)+'\n')
print(json.dumps({'src04_status':res.status,'grant':res.grant_sha256,'decision':res.decision.decision_ref.key,'src17_reuse':scope['reusable_for_src04_binding'],'src17_i03_i05':scope['reusable_for_i03_i05']},sort_keys=True))
