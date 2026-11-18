#!/usr/bin/env python3
"""Actual product later-row corruption: eager typed refusal before first yield."""
from __future__ import annotations
import json, sys
from pathlib import Path
OWNER=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/OWNER')
SNAP=OWNER/'WORKER_RETURNS/ANVIL_ENGINEERING_LOCALITY_G5_20261118/tmp/snapshot'
MP=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117')
sys.path[:0]=[str(SNAP),str(MP),str(MP/'vendor')]
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError, VerifiedDirectEstate
contract=json.loads((MP/'R2_PILOT/fixture_contract_pilot.json').read_text())
e=contract['estate']
estate=VerifiedDirectEstate(e['root'],exact_path=e['exact_path'],
 independently_held_manifest_sha256=e['manifest_sha256'],
 independently_held_i02=ExternalI02Roots(**e['i02']),
 current_authorizer=lambda _r:True)
out={}
with DirectEstateI03Session(estate) as s:
    respondent=next(iter(s.respondents))
    family='RoutingEligibilityFact'
    rows=list(s._db.execute('SELECT ref,gid,off FROM members WHERE family=? AND respondent=? ORDER BY gid,off',(family,respondent)))
    total=list(s._db.execute('SELECT COUNT(*) FROM members WHERE family=?',(family,)))[0][0]
    assert len(rows)>1
    first_ref=rows[0][0]; last_ref=rows[-1][0]
    s._db.execute('UPDATE members SET ref=? WHERE family=? AND respondent=? AND ref=?',('CORRUPT_LATER_ROW',family,respondent,last_ref))
    s._db.commit(); s._row_group_cache.clear()
    gen=s._respondent_family(family,respondent)
    yielded=[]; error=None
    try:
        while True:
            yielded.append(next(gen))
    except DirectEstateError as exc:
        error=f'{type(exc).__name__}: {exc}'
    except StopIteration:
        pass
    out={'family':family,'respondent':respondent,'family_total_rows':total,
         'respondent_rows':len(rows),'first_ref':first_ref,'corrupted_later_ref':last_ref,
         'yielded_count_before_error':len(yielded),'error':error,
         'eager_before_first_yield':len(yielded)==0 and error is not None,
         'typed_refusal':error is not None and 'body/index identity mismatch' in error,
         'buffer_scope':'per-respondent/family only; 600 rows for this respondent, not 9600 family total'}
print(json.dumps(out,indent=2,sort_keys=True))
raise SystemExit(0 if out['eager_before_first_yield'] and out['typed_refusal'] else 2)
