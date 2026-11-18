#!/usr/bin/env python3
"""One bounded actual-production f4 on sealed R2 estate, frozen 60e767 snapshot."""
from __future__ import annotations
import hashlib, json, sys, time
from pathlib import Path
OWNER=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/OWNER')
SNAP=OWNER/'WORKER_RETURNS/ANVIL_ENGINEERING_LOCALITY_G5_20261118/tmp/snapshot'
MP=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117')
sys.path[:0]=[str(SNAP),str(MP),str(MP/'vendor')]
import measure_cut1_prepared as harness
from court_instrumentation import CourtInstrumentation
CONTRACT=MP/'R2_PILOT/fixture_contract_pilot.json'
PILOT=MP/'R2_PILOT/FIRST_PAIR_RESULT.json'
LABEL='f4_three_raw'
OUT=OWNER/'WORKER_RETURNS/ANVIL_ENGINEERING_LOCALITY_G5_20261118/qualification.json'

def main():
    contract,_ctx,bundle,ops=harness.load_contract(CONTRACT)
    estate=contract['estate']
    query,predicate=next((q,p) for label,q,p in ops if label==LABEL)
    admission,admission_metrics=harness.admission_open(estate,bundle.catalog,lambda _roots:True,prepared=True)
    entry=time.monotonic()
    with admission.prepared_i03() as session:
        index_seconds=time.monotonic()-entry
        instrumentation=CourtInstrumentation()
        with instrumentation.phase(forbid_c11_repository=True) as counters:
            q_start=time.monotonic(); result=session.execute_i03(query_ref=query.ref,predicate_ref=predicate.ref); operation_wall=time.monotonic()-q_start
        serial_start=time.monotonic(); snapshot=harness.fact_snapshot(result); serialization=time.monotonic()-serial_start
        receipt=session.receipt().as_dict()
    pilot=json.loads(PILOT.read_text())
    baseline=next(row for row in pilot['baseline']['rows'] if row['label']==LABEL)
    # Compare every common payload field, not only the five historical hashes.
    ignore={'label','wall_seconds','serialize_seconds'}
    common=set(snapshot)&set(baseline)
    mismatches=sorted(k for k in common-ignore if snapshot[k]!=baseline[k])
    required=['identity_sha256','semantic_sha256','refs_sha256','member_refs_sha256','risk_member_refs_sha256','denominator_member_refs_sha256','replay_sha256','raw_denominator_support','weighted_denominator_support','fact_refs','query_ref','release_refs','typed_states','fact_count','member_ref_count','risk_member_ref_count','denominator_member_ref_count','source_scope_mode','topology_ref_count']
    absent=[k for k in required if k not in snapshot or k not in baseline]
    payload={
      'schema':'ANVIL_ENGINEERING_LOCALITY_G5_QUALIFICATION@1',
      'product_file':str(SNAP/'rawlsing_next/pre553_direct_estate_i03.py'),
      'product_sha256':hashlib.sha256((SNAP/'rawlsing_next/pre553_direct_estate_i03.py').read_bytes()).hexdigest(),
      'estate_manifest_sha256':estate['manifest_sha256'],
      'contract_sha256':hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
      'label':LABEL,
      'operation_wall_seconds':operation_wall,
      'admission_outside_operation':admission_metrics,
      'index_build_outside_operation_seconds':index_seconds,
      'serialization_seconds':serialization,
      'counters':counters.material(),
      'snapshot':snapshot,
      'parity':{'exact':not mismatches and not absent,'common_fields_compared':len(common-ignore),'mismatches':mismatches,'required_absent':absent},
      'session_receipt':receipt,
      'buffer_limit':'per-respondent/family materialized list; 600 routing facts in sealed witness; not whole estate',
      'limits':['one existing operation; no build/new estate/new pair/geometry','no test-only adapter/monkeypatch','no original35/native/100k/6GiB/science/actor/CURRENT/production acceptance']}
    OUT.write_text(json.dumps(harness.plain(payload),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS' if payload['parity']['exact'] else 'FAIL','operation_wall':operation_wall,'row_group_reads':counters.material().get('row_group_reads'),'family_objects':counters.material().get('family_object_materializations'),'parity':payload['parity']},sort_keys=True))
    return 0 if payload['parity']['exact'] else 2
if __name__=='__main__': raise SystemExit(main())
