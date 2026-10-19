"""Source/metadata audit of the retained C11 replay gap; never load survey rows.

This does not infer missing records from empirical results, manufacture a C11
seal, or execute a query. Native constructors and the retention writer define
the exact prerequisites; the custodian inventory defines the bounded artifact.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SEAL='1150e836ef58553255abc0f588e66c1327db4932'


def source(path):
    data=(ROOT/path).read_bytes()
    original=subprocess.check_output(['git','show',SEAL+':'+path],cwd=ROOT)
    if data!=original:
        raise ValueError('native source differs from seal: '+path)
    return ast.parse(data),{'path':path,'commit':SEAL,'bytes':len(data),
        'sha256':hashlib.sha256(data).hexdigest(),
        'git_blob_sha1':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\x00'+data).hexdigest()}


def audit(custody):
    inventory_path=custody/'canonical_object_inventory.json'
    data=inventory_path.read_bytes()
    manifest=json.loads((custody/'banked_artifact_manifest.json').read_text())
    declared=manifest['artifacts'][inventory_path.name]
    if len(data)!=declared['bytes'] or hashlib.sha256(data).hexdigest()!=declared['sha256']:
        raise ValueError('banked sourcefree inventory identity mismatch')
    inventory=json.loads(data)
    expected='f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415'
    if inventory['canonical_empirical_closure_identity']!=expected:
        raise ValueError('unexpected original empirical closure')
    ingest,ingest_ref=source('rawlsing_next/pre553_c11_ingest.py')
    producer,producer_ref=source('rawlsing_next/fiabc_final_oracle_freeze_producers.py')
    _,repository_ref=source('rawlsing_next/pre553_c11_repository.py')
    cls=next(n for n in ingest.body if isinstance(n,ast.ClassDef) and n.name=='C11SourceReleaseCandidate')
    sections=[{'field':n.target.id,'native_type':ast.unparse(n.annotation)}
              for n in cls.body if isinstance(n,ast.AnnAssign)]
    retention=next(n for n in producer.body if isinstance(n,ast.FunctionDef)
                   and n.name=='_lits_c11_release_retention_document')
    ret=next(n for n in ast.walk(retention) if isinstance(n,ast.Return))
    # Literal writer keys, not a guess from filenames or output counts.
    payload=ret.value.args[0]
    keys=[k.value for k in payload.keys]
    attrs=sorted({n.attr for n in ast.walk(retention)
                  if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name)
                  and n.value.id=='release'})
    counts=inventory['canonical_empirical_object_inventory']
    missing_carrier_families=[name for name in
        ('RespondentIdentity','QuestionVariableBinding','RespondentEvent',
         'RoutingEligibilityFact','EmpiricalCoordinateFact')
        if counts.get(name+'@1.0.0',0)==0]
    return {'schema':'O35B_C11_RETENTION_PREIMAGE_GAP_AUDIT@1',
        'scope':'EXACT_SUCCESS_CUSTODY_METADATA_AND_SEALED_NATIVE_SOURCE_ONLY; NOT_A_GLOBAL_ABSENCE_SEARCH',
        'inventory_sha256':hashlib.sha256(data).hexdigest(),
        'inventory_bytes':len(data),'closure_identity':expected,
        'public_empirical_object_count':sum(counts.values()),'public_empirical_inventory':counts,
        'native_candidate_sections':sections,'retention_document_literal_keys':keys,
        'retention_writer_release_attributes':attrs,
        'omitted_carrier_families':missing_carrier_families,
        'internal_record_preimages_in_release_writer':'NOT_SERIALIZED; writer does not access release.internal_records',
        'public_record_preimages_in_release_writer':'NOT_SERIALIZED; separate closure retains only selected public families',
        'source_release_manifest':'HASH_ONLY_IN_RETENTION_DOCUMENT; full original manifest still required',
        'candidate_replay_manifest':'COMPLETE_PREIMAGE_SERIALIZED_BY_WRITER; not sufficient for omitted sections',
        'zero_count_interpretation':'A zero in empirical inventory is not an exact TypedAbsence value for the C11 candidate; never infer weights, routing, or absence defaults',
        'validated_release_requirement':'Only validate_c11_source_release on the complete exact candidate may create the native validation seal',
        'retained_gap':'NO_COMPLETE_C11_CANDIDATE_PREIMAGE_IN_THIS_DECLARED_CLOSURE',
        'external_alternatives':'An independently retained complete original candidate/repository may exist elsewhere; otherwise a verified exact reconstruction warrant and competent owners are needed',
        'sources':[ingest_ref,producer_ref,repository_ref],
        'raw_source_reads':0,'row_values_output':0,'new_C11_seals':0,'new_I03_Batch_executions':0}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--custody-payload',type=Path,required=True)
    args=p.parse_args();result=audit(args.custody_payload)
    (HERE/'evidence/c11_retention_preimage_gap.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'public_empirical_objects':result['public_empirical_object_count'],
                      'native_candidate_sections':len(result['native_candidate_sections']),
                      'omitted_carrier_families':result['omitted_carrier_families'],
                      'new_C11_seals':0,'raw_source_reads':0}))
