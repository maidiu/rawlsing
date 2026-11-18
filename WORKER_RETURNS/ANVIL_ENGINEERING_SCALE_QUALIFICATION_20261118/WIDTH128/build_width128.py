#!/usr/bin/env python3
"""One 128 respondent x 600 question-binding sourcefree width build."""
from __future__ import annotations
import argparse,json,sys,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2];MP=REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--snapshot',required=True);ap.add_argument('--out',required=True);ap.add_argument('--respondents',type=int,default=128);ap.add_argument('--questions',type=int,default=600);a=ap.parse_args();sys.path[:0]=[str(Path(a.snapshot).resolve()),str(MP),str(MP/'vendor')]
 from fixture_1006 import ShapeSpec,build_context
 from width_fixture import build_width
 from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate
 shape=ShapeSpec('width128',a.respondents,include_weights=True,tag='PYAT-1006-WIDTH128-600-20261118');ctx=build_context(shape);w=build_width(ctx,a.questions);root=Path(a.out).resolve();root.mkdir(mode=0o700,parents=True,exist_ok=True)
 for p in list(root.iterdir()):
  import shutil;shutil.rmtree(p) if p.is_dir() else p.unlink()
 rec=write_direct_estate(w.sections,ctx.universe.ref,root,chunk_rows=512)
 c={'schema':'ANVIL_WIDTH128_ESTATE_CONTRACT@1','grade':'SOURCEFREE_TEST_ONLY','integrated_commit':'68aa7cac7cce7057fefd458ef4a06bec2dede1b2','fixture':'R2 response-populated width_fixture','tag':shape.tag,'respondents':a.respondents,'questions':a.questions,'width_audit':dict(w.audit),'family_counts':dict(rec.family_counts),'retained_bytes':rec.retained_bytes,'root':str(root),'exact_path':rec.path,'manifest_sha256':rec.manifest_sha256,'i02':{k:getattr(rec.i02,k) for k in ('logical','physical','release','source','replay','universe','schema')},'reconstructed_v1_release_ref':rec.reconstructed_v1_release_ref.as_dict(),'source_pins':{'width_fixture_blob':'5e044f74fc16e1ed2608dbb5224e5de9ef8e148fd0e78c5fb45e56ec0ede4bfe'}}
 (HERE/'fixture_contract_width128.json').write_text(json.dumps(c,indent=2,sort_keys=True)+'\n');print(json.dumps({'estate':rec.path,'events':rec.family_counts['RespondentEvent'],'routing':rec.family_counts['RoutingEligibilityFact'],'weights':rec.family_counts['WeightMeasureFact'],'bindings':rec.family_counts['QuestionVariableBinding'],'retained':rec.retained_bytes},sort_keys=True))
if __name__=='__main__':main()
