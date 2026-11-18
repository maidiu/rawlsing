#!/usr/bin/env python3
"""Diagnostic copy of width512 harness: same geometry, owns all stage/contract writes."""
from __future__ import annotations
import argparse,json,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117')
MP=REPO/'MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--snapshot',required=True);ap.add_argument('--out',required=True);ap.add_argument('--respondents',type=int,default=512);ap.add_argument('--questions',type=int,default=600);a=ap.parse_args();sys.path[:0]=[str(Path(a.snapshot).resolve()),str(MP),str(MP/'vendor')]
 from fixture_1006 import ShapeSpec,build_context
 from width_fixture import build_width
 from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate
 tag='PYAT-1006-WIDTH512-600-20261118';stages={'schema':'ANVIL_WIDTH512_STAGES@1','tag':tag}
 root=Path(a.out).resolve()
 if root.exists(): raise SystemExit(f'UNIQUE_ROOT_ALREADY_EXISTS:{root}')
 root.mkdir(mode=0o700,parents=True)
 t=time.monotonic();shape=ShapeSpec('width512',a.respondents,include_weights=True,tag=tag);ctx=build_context(shape);stages['context_seconds']=time.monotonic()-t;stages['stage']='context';stages['estate_root']=str(root);(HERE/'BUILD_STAGES.json').write_text(json.dumps(stages,indent=2)+'\n')
 t=time.monotonic();w=build_width(ctx,a.questions);stages['width_population_seconds']=time.monotonic()-t;stages['width_audit']=dict(w.audit);stages['stage']='width_population';(HERE/'BUILD_STAGES.json').write_text(json.dumps(stages,indent=2)+'\n')
 t=time.monotonic();stages['stage']='writing';(HERE/'BUILD_STAGES.json').write_text(json.dumps(stages,indent=2)+'\n')
 rec=write_direct_estate(w.sections,ctx.universe.ref,root,chunk_rows=512);stages['writer_publication_seconds']=time.monotonic()-t;stages['stage']='published';(HERE/'BUILD_STAGES.json').write_text(json.dumps(stages,indent=2)+'\n')
 c={'schema':'ANVIL_WIDTH512_ESTATE_CONTRACT@1','grade':'SOURCEFREE_TEST_ONLY','integrated_commit':'68aa7cac7cce7057fefd458ef4a06bec2dede1b2','fixture':'R2 response-populated width_fixture','tag':tag,'respondents':a.respondents,'questions':a.questions,'width_audit':dict(w.audit),'family_counts':dict(rec.family_counts),'retained_bytes':rec.retained_bytes,'root':str(root),'exact_path':rec.path,'manifest_sha256':rec.manifest_sha256,'i02':{k:getattr(rec.i02,k) for k in ('logical','physical','release','source','replay','universe','schema')},'reconstructed_v1_release_ref':rec.reconstructed_v1_release_ref.as_dict(),'source_pins':{'width_fixture_sha256':'5e044f74fc16e1ed2608dbb5224e5de9ef8e148fd0e78c5fb45e56ec0ede4bfe'}}
 (HERE/'fixture_contract_width512_timed.json').write_text(json.dumps(c,indent=2,sort_keys=True)+'\n');(HERE/'BUILD_STAGES.json').write_text(json.dumps(stages,indent=2)+'\n');print(json.dumps({'estate':rec.path,'events':rec.family_counts['RespondentEvent'],'routing':rec.family_counts['RoutingEligibilityFact'],'weights':rec.family_counts['WeightMeasureFact'],'bindings':rec.family_counts['QuestionVariableBinding'],'retained':rec.retained_bytes,'stages':stages},sort_keys=True))
if __name__=='__main__':main()
