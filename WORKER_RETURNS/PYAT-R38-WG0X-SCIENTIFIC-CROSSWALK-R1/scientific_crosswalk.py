"""Deterministic source-qualified research crosswalk, without identity issuance."""
from collections import Counter
import csv,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent

def load(name): return json.loads((R/name).read_text())
def lines(name):return [json.loads(x) for x in (R/name).read_text().splitlines()]
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def dump(name,obj):(R/name).write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n')

PHYSICAL_CANDIDATES={'Q45ST':'P45ST','Q47STC':'P47ST.C','Q8NCVA':'P8NCV.A','Q8NCVB':'P8NCV.B','Q8NCVC':'P8NCV.C'}
BLOCKED_NOTES={
 ('Afrobarometer','R1','pid'):('POSSIBLE_RENAMED_SUBSTANTIVE_ITEM','party','V525b party affiliation has 112 options; QSR pid is a codebook-only reference and party a real 112-label source column. Text/category-count correspondence is candidate evidence; no issued alias or directional driver transfer.'),
 ('Afrobarometer','R1','respnumb'):('POSSIBLE_RENAMED_CARRIER','casenumb','Codebook stem absent from source; casenumb is a retained source-extra respondent-number carrier. No respondent namespace equivalence is issued.'),
 ('Latinobarómetro','1995','P15'):('CODEBOOK_REFERENCE_WITH_ITEM_BATTERY','P15A|P15B|P15C|P15D|P15E','Historical codebook reference is absent as a source column. Five separately identified active child items exist; parent cannot become another measured response or be deleted from authority accounting.'),
 ('Latinobarómetro','1995','P43'):('POSSIBLE_RENAMED_CONTEXT_ITEM','p43a','EU-awareness codebook reference absent as a source column; p43a source-extra is a candidate. Accepted V525b genderEquality and later imperialAlignment assignments differ; no semantic succession is inferred.'),
 ('Latinobarómetro','1995','P47'):('CODEBOOK_REFERENCE_WITH_ENTITY_SUBITEMS','p47a|p47b|p47c','Parent refers to US/Europe/Japan; retained P2 has three distinct entity responses. Accepted V525b temporalOrientation differs from later imperialAlignment; neither label licenses collapsing entity responses.'),
 ('Latinobarómetro','2024','Q12STGBS'):('CODEBOOK_STEM_WITH_SPLIT_SUBITEMS','Q12STGBSA|Q12STGBSB','QSR marks absent codebook stem; active democracy and economy subitems remain separate. Source forms/physical bindings require owner validation.'),
 ('Latinobarómetro','2024','Q28ST'):('CODEBOOK_STEM_WITH_SPLIT_SUBITEMS','Q28STA|Q28STB|Q28STC|Q28STD|Q28STE','Absent stem; five distinct future-outlook dimensions remain individually governed. Do not treat a later metadata driver as proof that the child measurements are administrative.'),
 ('Latinobarómetro','2024','Q47ST'):('DUPLICATE_KEY_DISTINCT_ACCEPTED_MEANINGS','Q47STC|P47ST.C|P47ST.D','Accepted V525b retains two rows under Q47ST: printed press and social media. QRA retained social-media text; P2-only Q47STC is printed press. Keep both accepted assertions and native C/D columns; never last-row or stem alias them.'),
 ('Latinobarómetro','2024','Q56ST'):('CODEBOOK_STEM_WITH_ENTITY_SUBITEMS','Q56ST*|Q56N*','Absent codebook stem for leader evaluations; native/codebook entity codes differ. Preserve each named target and do not infer scalar psyche, causal authority or one generic leader response.')}


def build():
    freeze=load('evidence/PREIMPLEMENTATION_FREEZE.json')
    for path,sha in freeze['inputs'].items():
        if hashlib.sha256((R/path).read_bytes()).hexdigest()!=sha:raise ValueError('FROZEN_INPUT_CHANGED:'+path)
    p2=lines('sources/p2_identity_projection.jsonl');qra=lines('sources/qra_identity_projection.jsonl')
    active=[q for q in qra if q['authority_status']!='EXCLUDED_INACTIVE_WAVE']
    excluded=[q for q in qra if q['authority_status']=='EXCLUDED_INACTIVE_WAVE']
    pb={p['exact_identity_sha256']:p for p in p2}
    qb={q['p2_exact_identity_sha256']:q for q in active if q['p2_exact_identity_sha256']}
    if len(pb)!=len(p2) or len(qb)!=18250:raise ValueError('IDENTITY_MULTIPLICITY')
    if not set(qb)<=set(pb):raise ValueError('UNEXPECTED_QRA_IDENTITY')
    left=[p for p in p2 if p['exact_identity_sha256'] not in qb]
    right=[q for q in active if not q['p2_exact_identity_sha256']]
    if (len(left),len(right),len(excluded))!=(26,9,259):raise ValueError('CENSUS_CHANGED')
    owners=load('sources/owner_row_projections.json')
    waves=load('sources/o35e_scope.json')['waves']
    wm={(w['canonical_source_family'],w['canonical_wave']):w for w in waves}
    evidence=[]
    def matches(fam,wave,var,label):
        return [dict(owner=label,csv_record=x['csv_record'],exact_case_key=x['exact_case_key'],row_sha256=x['row_sha256'])
            for x in owners[label]['selected_records'] if x['exact_case_key'][0:2]==[fam,wave] and x['exact_case_key'][2].casefold()==var.casefold()]
    for p in left:
        fam,wave,var=(p[k] for k in ['source_family','wave','source_variable_code'])
        exact=next(x for x in load('sources/p2_only_exact_rows.json') if x['row']['exact_identity_sha256']==p['exact_identity_sha256'])
        row=exact['row'];role=row['authority_semantic_role']
        ev=[dict(owner='P2_IMPLEMENTATION_AUTHORITY',csv_record=p['csv_record'],exact_identity_sha256=p['exact_identity_sha256'])]
        for label in ('register_A','register_B','v525b_semantic','v525b_drivers','d62_driver_provenance_only'):ev+=matches(fam,wave,var,label)
        pc=PHYSICAL_CANDIDATES.get(var) if (fam,wave)==('Latinobarómetro','2024') else None
        if pc:
            for label in ('register_A','register_B'):ev+=matches(fam,wave,pc,label)
        if role in {'admin','administrative_metadata'}:
            kind='ADMIN_OR_CARRIER';decision='PRESERVE_CARRIER_OR_DESIGN_INPUT__NOT_MEASUREMENT_TARGET_BY_P2_DISPOSITION'
        elif role=='structural_context':kind='SUBSTANTIVE_SOURCE_RESPONSE_WITH_STRUCTURAL_CONTEXT_ROLE';decision='CONTEXT_OR_CONDITION_CANDIDATE__NO_DIRECTED_ROLE_INFERRED'
        elif role=='relation_evidence':kind='SUBSTANTIVE_MEASUREMENT_CANDIDATE';decision='ACCEPTED_P2_RELATION_ROLE__EXACT_CURRENT_OPERATION_BINDING_HELD'
        elif role=='blocked_review':kind='COMPETENTLY_HELD_P2_REVIEW';decision='P2_BLOCKED_REVIEW_AND_RESPONSE_AUTHORITY_GAP_PRESERVED'
        else:kind='SUBSTANTIVE_MEASUREMENT_CANDIDATE';decision='ACCEPTED_P2_NONADMIN_ROLE__OPERATION_SPECIFIC_AUTHORITY_REQUIRED'
        if var.startswith('p46') and wave=='1995':
            note='Eight separately retained EU-country knowledge columns; QSR reports single_choice for each. Joint multi-response/battery scoring and option-selection topology are not issued by their shared prefix.'
        elif var=='party':note='Substantive nominal party affiliation, not administrative; 112 historical source labels. Do not infer directional or harmonized cross-country party scale. Candidate codebook pid alias remains unissued.'
        elif var=='xstronld':note='Retained harmonized cross-country tradeoff and source-extra single-choice response. Harmonized wording does not establish source country/form comparability or a directed scalar.'
        elif var=='p33b':note='P2 retains blocked_review despite a historical single_choice source-column classification. Classification alone cannot remove its competent hold.'
        elif pc:note='P2 question text and physical '+pc+' content support an explicit P/Q/dotted-name candidate; current source/version/form/routing/response-code authority crosswalk must be supplied. This report does not apply that alias.'
        elif var in {'p47a','p47b','p47c'}:note='Distinct named external-entity response; preserve target and support/oppose/neutral/unknown/missing classes from P2. Parent P47 is not another interchangeable response.'
        elif var=='wt':note='Weight/design input retained. No measure fact, national estimand or unit weight is inferred from its name or administrative status.'
        else:note='Preserve exact retained role and distinct code; no operation or respondent/form/route identity inferred from label.'
        evidence.append(dict(record_id='P2_ONLY:'+p['exact_identity_sha256'],side='P2_ONLY',family=fam,wave=wave,atlas_id=wm[(fam,wave)]['atlas_id'],variable=var,p2_implementation_id=p['question_implementation_id'],p2_exact_identity_sha256=p['exact_identity_sha256'],p2_csv_record=p['csv_record'],question_text=row['question_text'],inherited_role=role,inherited_response_binding=row['response_binding_status'],response_classes=row['response_classes'],historical_owner_artifact=row['question_authority_artifact'],classification=kind,source_specific_decision=decision,physical_alias_candidate=pc,scientific_note=note,evidence=ev,source_version=wm[(fam,wave)]['dataset_manifest_identity'],form='UNBOUND_REQUIRES_ORIGINAL_SOURCE_OWNER',respondent_carrier='UNBOUND_PERSON_HOUSEHOLD_NAMESPACE_NOT_INFERRED',routing_risk_weight='UNBOUND_OPERATION_SPECIFIC',current_operation_status='SOURCE_OR_OPERATION_HELD'))
    for q in right:
        fam,wave,var=(q[k] for k in ['canonical_source','canonical_wave','var_code'])
        cls,related,note=BLOCKED_NOTES[(fam,wave,var)]
        ev=[dict(owner='QRA_FINAL_R1',csv_record=q['csv_record'],governed_row_payload_hash=q['governed_row_payload_hash'])]
        for label in ('register_A','register_B','v525b_semantic','v525b_drivers','d62_driver_provenance_only'):ev+=matches(fam,wave,var,label)
        evidence.append(dict(record_id='QRA_BLOCKED:'+q['question_id'],side='QRA_BLOCKED',family=fam,wave=wave,atlas_id=wm[(fam,wave)]['atlas_id'],variable=var,qra_question_id=q['question_id'],qra_csv_record=q['csv_record'],governed_row_payload_hash=q['governed_row_payload_hash'],p2_exact_identity_sha256=None,inherited_role=q['authority_status'],classification=cls,source_specific_decision='PRESERVE_BLOCKED_IDENTITY__NO_AUTOMATIC_ALIAS_OR_PARENT_COLLAPSE',related_candidates=related,scientific_note=note,evidence=ev,source_version=wm[(fam,wave)]['dataset_manifest_identity'],country_scope_as_recorded=q['country_code_scope'],form='UNBOUND_REQUIRES_ORIGINAL_SOURCE_OWNER',respondent_carrier='UNBOUND_PERSON_HOUSEHOLD_NAMESPACE_NOT_INFERRED',current_operation_status='SOURCE_OR_OPERATION_HELD'))
    evidence.sort(key=lambda x:x['record_id'])
    union=[]
    for p in p2:
        q=qb.get(p['exact_identity_sha256'])
        union.append(dict(record_id='P2:'+p['exact_identity_sha256'],family=p['source_family'],wave=p['wave'],variable=p['source_variable_code'],p2_hash=p['exact_identity_sha256'],p2_record=p['csv_record'],qra_record=q['csv_record'] if q else None,qra_payload=q['governed_row_payload_hash'] if q else None,join='COMMON_EXACT_HASH' if q else 'P2_ONLY',operation_binding='HELD__NOT_ISSUED_BY_CROSSWALK'))
    for q in right:union.append(dict(record_id='QRA:'+q['question_id'],family=q['canonical_source'],wave=q['canonical_wave'],variable=q['var_code'],p2_hash=None,p2_record=None,qra_record=q['csv_record'],qra_payload=q['governed_row_payload_hash'],join='QRA_ONLY_BLOCKED',operation_binding='HELD__IDENTITY_UNRESOLVED'))
    counts=Counter((r['family'],r['wave'],r['join']) for r in union)
    bywave=[dict(atlas_id=w['atlas_id'],family=w['canonical_source_family'],wave=w['canonical_wave'],**{k:counts[(w['canonical_source_family'],w['canonical_wave'],k)] for k in ['COMMON_EXACT_HASH','P2_ONLY','QRA_ONLY_BLOCKED']}) for w in waves]
    roles=Counter(r['inherited_role'] for r in evidence if r['side']=='P2_ONLY')
    return dict(schema='WG0X_SCIENTIFIC_RESEARCH_CROSSWALK@1',grade='SOURCE_QUALIFIED_RESEARCH__NOT_SEMANTIC_ISSUANCE_OR_INDEPENDENT_ACCEPTANCE',counts=dict(p2=len(p2),qra_active=len(active),common=len(qb),p2_only=len(left),qra_only_blocked=len(right),net_delta=len(p2)-len(active),research_union=len(union),excluded_inactive=len(excluded),p2_only_roles=dict(roles)),rows=evidence,waves=bywave,union=union,excluded=excluded,original35_current_operation_permission='UNCHANGED_HOLD__NO_ISSUANCE',crosswalk_digest=digest(evidence))

def main():
    d=build();dump('01_EXACT_26_PLUS_9_CROSSWALK.json',{k:v for k,v in d.items() if k not in {'union','excluded'}})
    for name,key in [('evidence/union_identity_ledger.jsonl','union'),('evidence/excluded_inactive_ledger.jsonl','excluded')]:
        (R/name).write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n' for x in d[key]))
    fields=['side','atlas_id','family','wave','variable','p2_exact_identity_sha256','inherited_role','classification','source_specific_decision','physical_alias_candidate','related_candidates','form','respondent_carrier','current_operation_status','scientific_note']
    with (R/'01_EXACT_26_PLUS_9_CROSSWALK.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");writer.writeheader()
        writer.writerows({k:x.get(k,'') for k in fields} for x in d['rows'])
    dump('evidence/crosswalk_summary.json',{k:d[k] for k in ['counts','crosswalk_digest','waves','original35_current_operation_permission']})
    print(json.dumps(d['counts'],ensure_ascii=False))
if __name__=='__main__':main()
