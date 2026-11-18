#!/usr/bin/env python3
"""Fresh-process cold reopen and full-family count verification."""
from __future__ import annotations
import json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError, VerifiedDirectEstate
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
HERE=Path(os.environ.get('ANVIL_TESTONLY_ROOT', str(Path(__file__).resolve().parent))).resolve();b=json.loads((HERE/'proof'/'build.json').read_text());r=b['roots']
mode=os.environ.get('ANVIL_REOPEN_MODE','positive')
held_i02=ExternalI02Roots(**b['i02'])
if mode=='wrong_root':
    from dataclasses import replace
    held_i02=replace(held_i02,logical='0'*64)
    held_manifest=b['manifest_sha256']
else:
    held_manifest=b['manifest_sha256']
def current(roots):
    if mode=='revoked':
        return False
    if mode=='wrong_root':
        return True
    return roots==held_i02
try:
    estate=VerifiedDirectEstate(HERE/'estate'/'private',exact_path=b['path'],independently_held_manifest_sha256=held_manifest,independently_held_i02=held_i02,current_authorizer=current)
    # Explicit family list keeps the check machine-readable without importing product internals.
    families=('EmpiricalUniverse','RespondentIdentity','QuestionVariableBinding','RespondentEvent','RoutingEligibilityFact','EmpiricalCoordinateFact','WeightMeasureFact','AuthoritySnapshot','SourceUniverseRelation','EmpiricalPredicateReplayBinding','ComparatorReplayBinding','DiscoveryBranchReplayBinding','StructuralAdmissionReplayBinding')
    counts={f:sum(1 for _ in estate.iter_family(f,batch_size=2)) for f in families}
    assert counts==b['family_counts'],(counts,b['family_counts'])
    (HERE/'proof'/'reopen.json').write_text(json.dumps({'schema':'ANVIL_TESTONLY_Q2_REOPEN@1','sourcefree_test_only':True,'family_counts':counts,'manifest_sha256':b['manifest_sha256']},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'reopen':'PASS','families':len(counts),'objects':sum(counts.values())},sort_keys=True))
except DirectEstateError as exc:
    if mode=='positive': raise
    proof={'schema':'ANVIL_TESTONLY_Q2_REOPEN_REFUSAL@1','sourcefree_test_only':True,'refused':True,'mode':mode,'error_type':type(exc).__name__,'error':str(exc),'before_estate_open':True}
    (HERE/'proof'/f'reopen_refusal_{mode}.json').write_text(json.dumps(proof,indent=2,sort_keys=True)+'\n')
    print(json.dumps(proof,sort_keys=True))
