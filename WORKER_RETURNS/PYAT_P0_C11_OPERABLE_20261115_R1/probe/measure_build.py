from __future__ import annotations
import json, shutil, sys, time
from pathlib import Path
HERE=Path(__file__).resolve().parent; BASE=HERE.parent; REPO=BASE.parents[1]
sys.path[:0]=[str(REPO),str(HERE)]
from wide_fixture import build_source
from rawlsing_next.tests import test_pre553_direct_estate_i03 as s2c
root=BASE/'.local-data'
root.mkdir(mode=0o700, exist_ok=True); root.chmod(0o700)
t=time.monotonic(); source,candidate=build_source(); source_seconds=time.monotonic()-t
t=time.monotonic(); _root,receipt=s2c._cold(BASE/'.local-data', candidate, source['universe'].ref, 'wide-build-measure'); write_seconds=time.monotonic()-t
retained=sum(p.stat().st_size for p in Path(receipt.path).rglob('*') if p.is_file())
out={'schema':'PYAT_P0_WIDE_BUILD@1','source_fixture_seconds':source_seconds,'writer_seconds':write_seconds,'retained_bytes':retained,'family_counts':dict(receipt.family_counts),'manifest_sha256':receipt.manifest_sha256,'release':receipt.reconstructed_v1_release_ref.as_dict()}
(BASE/'evidence'/'wide_build.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
shutil.rmtree(root/'wide-build-measure', ignore_errors=True)
