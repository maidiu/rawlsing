"""Original retained P1 -> unchanged native M1 integrity and authority boundary.

No I03/Batch rerun and no family-rule/FF permission is issued. The frozen claim
expects a rule-authority hold; the observed earlier authority-closure hold is
retained as a RED, rather than weakening that expected terminal.
"""
import gzip
import json
from pathlib import Path
import sys
from time import perf_counter

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]));sys.path.insert(0,str(HERE))
import retained_catalog
from rawlsing_next.pre553_carrier_execution import materialize_public_object
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_learned_empirical_adjudication import (
    build_m1_adjudication_input_bundle,adjudicate_learned_empirical,
    M1ValidatorRegistry,M1IntegrityError,
)

JOINT_HASH='fb8bd6e50f27d77ed97827ba3ff712df5951e438d60b5a0194f9953107e3614b'


def original_p1_authorities(catalog):
    """Append the uniquely retained projection dependency, without reissuing it."""
    freeze=json.loads((HERE/'evidence/P1_AUTHORITY_BINDING_CORRECTION_FREEZE.json').read_text())
    expected=freeze['exact_existing_public_snapshot_hash']
    docs=[d for d in retained_catalog.retained_documents()
          if d['schema_id']=='AuthoritySnapshot' and d['content_hash']==expected]
    if len(docs)!=1:
        raise ValueError('exact retained projection snapshot preimage unavailable')
    snapshot=materialize_public_object(docs[0])
    if snapshot.authority_ref.as_dict()!=freeze['actual_missing_authority']:
        raise ValueError('retained projection snapshot authority triple substituted')
    if any(a.authority_ref==snapshot.authority_ref for a in catalog.authorities):
        raise ValueError('original scoped catalog unexpectedly contains projection authority')
    return (*catalog.authorities,snapshot)


def record_local_result(result):
    """Retain only refs, aggregate support and terminal timing for proof replay."""
    target=HERE/'.runtime/continuation/p1/native_M1_latest_result.json'
    target.write_text(json.dumps(result,indent=2)+'\n')
    return result


def run_consumer():
    start=perf_counter()
    freeze=json.loads((HERE/'evidence/CONTINUATION_P1_FREEZE.json').read_text())
    facts=[]
    for role,spec in freeze['facts'].items():
        with gzip.open(HERE/'.runtime/continuation/p1'/(role+'.json.gz'),'rt',encoding='utf-8') as f:
            doc=json.load(f)
        fact=materialize_public_object(doc)
        if fact.content_hash!=spec['hash'] or fact.raw_denominator_support!=spec['raw_denominator']:
            raise ValueError('recovered original P1 Fact or support substitution')
        facts.append(fact)
        del doc
    facts=tuple(facts)
    support=json.loads((HERE/'evidence/continuation_p1_support_preimages.json').read_text())
    receipt=materialize_public_object(support['receipt'])
    discovery=materialize_public_object(support['discovery_authority'])
    catalog=retained_catalog.build_original_scoped_catalog()
    authorities=original_p1_authorities(catalog)
    loaded=perf_counter()
    try:
        bundle=build_m1_adjudication_input_bundle(
            requested_claim_family_id='O35B_RETAINED_P1_INTEGRITY_AUDIT',
            requested_claim_rule_id='NO_FAMILY_VALIDATION_RULE_ISSUED',
            selected_discovery_receipts=(receipt,),discovery_authority_catalog=(discovery,),
            empirical_fact_catalog=facts,
            empirical_query_catalog=catalog.queries,empirical_predicate_catalog=catalog.predicates,
            authority_snapshots=authorities,
            requested_scope={'purpose':'EXACT_RETAINED_P1_READ_ONLY_NATIVE_BOUNDARY_AUDIT'},
        )
    except M1IntegrityError as exc:
        return record_local_result({'state':'NATIVE_INPUT_BUNDLE_REFUSED','detail':str(exc),'M1_run':False,
                'raw_reads':0,'new_I03_Batch_executions':0})
    built=perf_counter()
    result=adjudicate_learned_empirical(bundle,None,validator_registry=M1ValidatorRegistry())
    adjudicated=perf_counter()
    return record_local_result({'state':result.status_token,'adjudication_outcome':result.adjudication_outcome,
            'result_ref':result.ref.as_dict(),'bundle_fact_refs':[f.ref.as_dict() for f in bundle.empirical_facts],
            # These disposition refs may be copied from a blocked input summary;
            # their presence does not establish completed verification.
            'consumed_fact_refs':[r.as_dict() for r in result.validation_fact_refs],
            'raw_denominators':{role:next(f.raw_denominator_support for f in facts if f.content_hash==spec['hash'])
                                for role,spec in freeze['facts'].items()},
            'M1_run':True,'raw_reads':0,'new_I03_Batch_executions':0,
            'stage_seconds':{'materialize':round(loaded-start,3),'bundle':round(built-loaded,3),
                             'adjudicate':round(adjudicated-built,3)},
            'claim_grade':'RETAINED_ORIGINAL_OBJECT_VERIFICATION_TO_TYPED_HOLD__NOT_OPERATION_COMPLETION'})


if __name__=='__main__':
    print(json.dumps(run_consumer(),indent=2))
