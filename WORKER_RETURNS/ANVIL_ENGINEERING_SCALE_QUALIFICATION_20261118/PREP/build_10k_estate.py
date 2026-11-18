#!/usr/bin/env python3
"""Construct the smallest compatible 10k sourcefree estate from #1006 fixture.

PREP ONLY.  Not executed by this return.  Uses the integrated 68aa7 snapshot
and the exact fixture_1006 blob; no original35/source read.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--snapshot',required=True)
    ap.add_argument('--out',required=True)
    ap.add_argument('--respondents',type=int,default=10000)
    ap.add_argument('--chunk-rows',type=int,default=512)
    ap.add_argument('--tag',default='PYAT-1006-SCALE-10K-20261118')
    a=ap.parse_args(); snap=Path(a.snapshot).resolve(); vend=Path(__file__).resolve().parents[2]/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'/'vendor'
    sys.path[:0]=[str(snap),str(vend)]
    from fixture_1006 import ShapeSpec, build_context
    from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate
    shape=ShapeSpec('scale-10k',a.respondents,include_weights=True,tag=a.tag)
    ctx=build_context(shape); root=Path(a.out).resolve(); root.mkdir(mode=0o700,parents=True,exist_ok=True)
    for p in root.glob('*'): 
        if p.is_dir(): import shutil; shutil.rmtree(p)
        else: p.unlink()
    receipt=write_direct_estate(ctx.direct_sections(),ctx.universe.ref,root,chunk_rows=a.chunk_rows)
    contract={
      'schema':'ANVIL_SCALE_10K_ESTATE_CONTRACT@1','grade':'SOURCEFREE_TEST_ONLY',
      'integrated_commit':'68aa7cac7cce7057fefd458ef4a06bec2dede1b2',
      'fixture':'fixture_1006.ShapeSpec 5-question base','tag':a.tag,
      'respondents':a.respondents,'questions':5,
      'event_count':int(receipt.family_counts['RespondentEvent']),
      'routing_count':int(receipt.family_counts['RoutingEligibilityFact']),
      'weight_count':int(receipt.family_counts['WeightMeasureFact']),
      'question_bindings':int(receipt.family_counts['QuestionVariableBinding']),
      'family_counts':dict(receipt.family_counts),'retained_bytes':receipt.retained_bytes,
      'width_note':'5 native questions only; this is respondent-scale, not 600-column width',
      'root':str(root),'exact_path':receipt.path,'manifest_sha256':receipt.manifest_sha256,
      'i02':{k:getattr(receipt.i02,k) for k in ('logical','physical','release','source','replay','universe','schema')},
      'reconstructed_v1_release_ref':json.loads(json.dumps(receipt.reconstructed_v1_release_ref.as_dict())),
      'source_pins':{'fixture_1006_blob':'1487ad233c871d973b2a64c9649c37f100c46832','fixture_1006_sha256':'74cd928d050ec7a8720e526dea00101e4c0f718a1b2ab72e5677deb64360b827'},
    }
    out=Path(__file__).resolve().parent/'fixture_contract_10k.json'; out.write_text(json.dumps(contract,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'contract':str(out),'estate':receipt.path,'respondents':a.respondents,'questions':5,'events':receipt.family_counts['RespondentEvent'],'routing':receipt.family_counts['RoutingEligibilityFact'],'retained_bytes':receipt.retained_bytes},sort_keys=True))
if __name__=='__main__': main()
