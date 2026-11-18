#!/usr/bin/env python3
"""Fresh-process cold reopen and full-family count verification."""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
HERE=Path(__file__).resolve().parent;b=json.loads((HERE/'proof'/'build.json').read_text());r=b['roots']
estate=VerifiedDirectEstate(HERE/'estate'/'private',exact_path=b['path'],independently_held_manifest_sha256=b['manifest_sha256'],independently_held_i02=ExternalI02Roots(**b['i02']),current_authorizer=lambda _roots:True)
# Explicit family list keeps the check machine-readable without importing product internals.
families=('EmpiricalUniverse','RespondentIdentity','QuestionVariableBinding','RespondentEvent','RoutingEligibilityFact','EmpiricalCoordinateFact','WeightMeasureFact','AuthoritySnapshot','SourceUniverseRelation','EmpiricalPredicateReplayBinding','ComparatorReplayBinding','DiscoveryBranchReplayBinding','StructuralAdmissionReplayBinding')
counts={f:sum(1 for _ in estate.iter_family(f,batch_size=2)) for f in families}
assert counts==b['family_counts'],(counts,b['family_counts'])
(HERE/'proof'/'reopen.json').write_text(json.dumps({'schema':'ANVIL_TESTONLY_Q2_REOPEN@1','sourcefree_test_only':True,'family_counts':counts,'manifest_sha256':b['manifest_sha256']},indent=2,sort_keys=True)+'\n')
print(json.dumps({'reopen':'PASS','families':len(counts),'objects':sum(counts.values())},sort_keys=True))
