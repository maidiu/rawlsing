"""Derive P2 documentary matrices from pinned Git evidence; executes no project code."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parent.parent
C='a3d44f554e4e4fa01223679035599019ae2de527'
Q='6f6ab9dfe5ad8f9359630dd05abf43c3fd11a1b5'
BASE='WORKER_RETURNS/PYAT-C2-02-C4-PROVING-WORKLOAD-R1/'

def read_json(path):
    raw=subprocess.check_output(['git','show',Q+':'+path])
    blob=subprocess.check_output(['git','rev-parse',Q+':'+path],text=True).strip()
    return json.loads(raw),{'commit':Q,'path':path,'blob':blob,'sha256':hashlib.sha256(raw).hexdigest(),'line_count':len(raw.splitlines()),'review_mode':'PARSED_SELECTED_IDENTITY_ROLE_AND_ACCOUNTING_FIELDS__NOT_FULL_SEMANTIC_REVIEW','executed':False}

all35,a=read_json(BASE+'05_ALL35_HORIZONTAL_ACCOUNTING_PLAN.json')
selection,b=read_json(BASE+'02_PROPOSED_PROVING_SET.json')
selected={r['source_key']:r for r in selection['sources']}
rows=all35['rows']
assert len(rows)==35 and {r['source_id'] for r in rows}=={f'{n:02}' for n in range(1,36)}
assert len(selected)==8
idx=ROOT/'phases/P2_SOURCE_INDEX.json';records=json.loads(idx.read_text())
for x in [a,b]:
    if x not in records: records.append(x)
idx.write_text(json.dumps(records,indent=2)+'\n')
product_classes={
'F1':'Governed exact empirical substrate/query product at selected scope',
'F2':'Predictor/determinicity product conserving denominator and uncertainty',
'F3':'Majority/minority/counterpattern and recursive lineage product',
'F4':'Complete same-respondent joint/cloud product with order and member identity',
'F5':'Actor-independent admitted structural contribution at exact authorized use',
'F6':'Coherent source-indexed multi-source response or separately authorized composite',
'F7':'Comparable-wave result and separately authorized structural temporal contribution',
'F8':'Usable exact/proxy/typed-null positioned possibility with progressive/currentness contract'}
entries=[]
for source in rows:
    sid='SRC'+source['source_id'];picked=selected.get(sid)
    item={k:source[k] for k in ['source_id','source_file','canonical_sha256','format','family','wave','historical_representation_status','historical_terminal_classification']}
    item.update(source_key=sid,physical_identity_grade='DECLARED_IN_PINNED_C2_RECORD__NO_SOURCE_BYTES_READ_OR_REHASHED_IN_P2',identity_evidence=a,
        c4_preparation_selected=picked is not None,c4_role=None if picked is None else picked['selection_role'],
        role_evidence=None if picked is None else b,physical_operation_expectations=[] if picked is None else picked['exact_governed_operations'],
        preparation_ceiling='HQ133/HQ168 accepted preparation; physical-edge promises do not establish survey semantic service support',
        retained_product_evidence=[],functional_cells=[])
    if sid=='SRC02':item['retained_product_evidence']=[{'control_commit':C,'adoption':'HQ223 scoped retained GT2 Q86B→Q86A joint/risk/Field Forge/V554/CONTEXT; HQ235 local CONTEXT only; HQ227 GT2-specific V555 N/A','risk_set_rows_in_inherited_acceptance':19210,'joint_cells_in_inherited_acceptance':36,'source_reread_in_p2':False,'geometry_and_product_refs':'d966d4ec97839b09a3040fd2ad23a3d63677bba9:WORKER_RETURNS/PYAT-C5-C7E-NEXT-SCOPE-READINESS-R1/03_INPUT_AND_AUTHORITY_BINDINGS.json plus indexed HQ223/HQ235 records','world_or_parent_or_temporal_use_proved':False}]
    for gate,expected in product_classes.items():
        support='UNKNOWN_AT_DECLARED_FUNCTIONAL_SCOPE';status='UNBOUND_EXPECTATION';intrinsic=None;witness=None
        missing='Exact claim, variable/coordinate, routing/risk/measurement, authority, producer and consumer binding required before this source/function can be empirically tested.'
        if sid=='SRC02' and gate in ['F1','F4','F5']:
            support='SUPPORTED_AT_RETAINED_GT2_SLICE_ONLY';status='SCOPED_RETAINED_POSITIVE__FULL_GATE_UNPROVED'
            intrinsic='HQ223 retained respondent-backed Q86B→Q86A geometry; no whole-source semantic promotion.'
            witness='HQ223 20–28 / HQ235 43–64; current retained-input authority grain only'
            missing='Additional demanded scopes and exact final-world consumer remain unbound; reuse this accepted local context, do not reopen GT2 V555 by default.'
        elif sid=='SRC02' and gate in ['F2','F3','F8']:
            intrinsic='Retained 36-cell joint is potential analytical input; exact predictor/fork/parent query/model/use still unbound.'
        elif sid in ['SRC12','SRC14'] and gate=='F7':
            intrinsic='Candidate wave labels/physical edges only; no competent current products or positive pair authority.'
            missing='C7-BLOCK-CURRENT-COMPARABLE-WAVE-PAIR-001: bind competent products, exact universe keys and positive comparison/meaning authority; physical-only C4 is insufficient.'
        cell={'gate':gate,'contractual_product_class':expected,'source_supported_expected_product_class':expected if support.startswith('SUPPORTED_') else None,
            'support_status':support,'source_grounding':intrinsic,'empirical_expected_value':None,'intrinsic_na':None,'na_reason':'No independently supported source-intrinsic functional N/A established in P2.',
            'null_product_receipt':None,'development_or_input_blocker':missing,'accepted_positive_witness':witness,'consumer': 'V557/V558 local CONTEXT' if sid=='SRC02' and gate=='F5' else None,
            'current_occupancy_status':status,'integration_realization_at_demanded_service':'UNVERIFIED','estate_gate_acceptance':'NOT_CLAIMED','prev3_completion':'NOT_CLAIMED',
            'source_execution_permission_in_p2':False,'falsifier':'Exact competent source/use authority and authentic product→consumer→replay receipt, or source-backed independent N/A rationale.'}
        item['functional_cells'].append(cell)
    entries.append(item)
result={'schema':'PYAT_P2_SOURCE_SUPPORTED_EXPECTED_CAPABILITIES@1','status':'PROPOSED_DOCUMENTARY_EXPECTATIONS__NO_EXECUTION_OR_ADOPTION',
'control':C,'primary_identity_and_preparation_sources':[a,b],
'accounting':{'sources':35,'source_gate_cells':280,'physical_preparation_sources':8,'intrinsic_functional_na_cells_newly_established':0,'raw_source_executions':0},
'law':'Contractual desired product != source-supported expectation != empirical result != execution warrant. Unknowns remain null; missing authority never becomes valid emptiness.',
'known_claim_specific_na':[{'source':'SRC02','claim':'GT2 SIG-004 V555 continuation','status':'ADOPTED_NA_AT_EXACT_GT2_CONTRACT_GRAIN','basis':'HQ227; no general F5/F1–F8 source-intrinsic N/A inferred'}],
'minimum_empirical_scope_status':'NOT_READY_TO_SELECT_A_PROVEN_COMPLETE_SET__RETAINED_GT2_PLUS_CURRENT_COMPARABLE_PAIR_AND_OTHER_FAMILY_WORLD_CONTRIBUTION_NOT_ALL_BOUND',
'rows':entries}
(ROOT/'final').mkdir(exist_ok=True)
(ROOT/'final/P2_EXPECTED_CAPABILITIES.json').write_text(json.dumps(result,indent=2)+'\n')
md=['# P2 source-supported expected-capability analysis','','Proposed documentary matrix; no source execution, authority adoption or empirical outcomes. JSON retains all 35 source identities and 280 individually accountable F1–F8 cells. Source hashes are declarations from pinned C2 documents, not freshly rehashed raw files. Historical census P/B remains history.','','## What the retained evidence actually supports','','| Source/use | Supported expectation | Occupancy / unresolved boundary |','|---|---|---|',
'| SRC02 Afrobarometer R5 GT2 Q86B→Q86A | Exact respondent-backed risk/joint geometry and admitted Field Forge/V554→V557/V558 local CONTEXT | HQ223/HQ235 scoped positive; no full world, parent, multi-source or temporal use inferred |',
'| SRC02/06 | Exact G01 physical representation operations on frozen codes and variables | Physical expectation only; survey semantic analytical service not thereby certified |',
'| SRC08/12 | Exact declared-encoding physical admission | No semantic route or same-family comparison authority from decoding |',
'| SRC14 EVS2008 | Opaque date/time physical representation | EVS1990/2008 temporal pair remains product/authority unbound |',
'| SRC26 Latinobarómetro2024 | Preserve raw-header and dictionary-stream views | Physical conservation does not establish sociological world meaning |',
'| SRC27 LiTS I / SRC35 WVS7 | Selected full-route anchor/comparator contracts and retained-route documentary evidence | Current actual demanded products/use receipts must be bound; not a same-family temporal pair |',
'| Remaining 27 preparation-excluded sources | Source-specific expectations UNKNOWN until exact source/claim support is grounded | Exclusion is neither failure nor N/A; no all-35 acceptance claim |','','The eight-source C4 set was selected for physical and route edge coverage; it is not a source-supported proving set for all three demanded social services. EVS wave labels do not prove comparability; SRC02’s accepted local context is substantial reusable empirical capital. A desired predictor/parent result must not be assigned to every survey by survey name. No positive effect, modal winner, probability, temporal sign or null outcome is predetermined.','','## World-operation and consumer map','','| Field/operation | Competent input and role | Required output/use receipt |','|---|---|---|',
'| Structural context | Retained GT2 at existing exact structural-use grain | Coherent declared world response references context and preserves ceiling; context does not automatically modify probability |',
'| Source eligibility | Authenticated H-A/H-D applicability request/receipt and exact F8 rule | Admitted set survives unchanged; it does not rank, pool or compute conditioning |',
'| Empirical conditioning | Exact response or empirical position coordinate, subject preimage, predicate leaves and pairing authority | q(A)→q(A,B), distinct identities, complete joint/minority geometry and traceable denominator |',
'| Probability transformation | Only an explicitly authorized selected operation/model with actual compatible evidence | Before/after response and exact transformation provenance; no implicit world multiplier |',
'| Multi-source use | Distinct admitted fields at source-indexed coexistence scope, or separately authorized composite | Both contributions actually consumed; no synthetic pooled respondent or unauthorized joint |',
'| Temporal comparison | Competent exact wave products, identities, measure/risk/design/time and pair-specific positive authority | Signed increase/decrease/no-change or genuine noncomparable state; structural meaning and final consumer separately proved |',
'| Current/as-of serving | Exact release/selection/dependency/currentness closure | Snapshot and consumer receipt; mutation preserves unaffected products and denies/replaces affected current use |',
'| Parent/coparent possibility | Exact purpose/model/conditioning authority; sampling-unit authority for dyadic/household claim | Usable empirical distributions/alternatives at declared grain, actor firewall; individual possibility is not generated personhood |','','## State classification and completion programs','','Supported positive or weak/null/no-change outputs may satisfy an expected product. ZERO_SUPPORT is a zero risk/denominator state and is projected UNDERPOWERED by C1-03A; it is not VALID_EMPTY. A supported distribution can contain observed zero cells. VALID_EMPTY requires its exact producer semantics; NONCOMPARABLE must preserve why the comparison is unauthorized/inapplicable. Missing source, release, competence, model authority or security stays a blocker. GT2-specific V555 N/A is claim-specific adopted law, not broad source F5 N/A.','','The minimum empirical program must first bind inputs and authority for all three service families, then the actual rich/null/world consumer route and required operational edges. The existing record does not establish a complete competent minimum set. For a selected demand requiring two survey families plus two waves of one family, at least three source-wave identities are a logical lower bound; this is not a universal three-anchor temporal law or evidence of sufficiency. A single-source or source-free demonstration is an intermediate local proof. Full acceptance separately accounts for all 280 cells, supported N/A rationales, expected products, consumption and replay; no eight-source or synthetic canary extrapolation.','','## All-35 identity and accountability routing','','| Source | Wave / file | Historical census | Physical-preparation role | Full F1–F8 status |','|---|---|---|---|']
for x in entries:md.append(f"| {x['source_key']} | {x['family']} {x['wave']} / {x['source_file']} | {x['historical_representation_status']} | {x['c4_role'] or 'Excluded at preparation grain'} | {'Scoped GT2 positive only; other demands unknown' if x['source_key']=='SRC02' else 'UNVERIFIED / expectations unbound'} |")
md+=['','Exact primary files: C2 return `6f6ab9dfe5ad8f9359630dd05abf43c3fd11a1b5`, 02_PROPOSED_PROVING_SET and 05_ALL35_HORIZONTAL_ACCOUNTING_PLAN; HQ133/HQ168 preparation authority; HQ149 C7 readiness; current HQ223/HQ235 context scope; HQ125/HQ216 completion law. Source index records parsed field scope. No unsupported source semantics or empirical values added.']
(ROOT/'final/P2_EXPECTED_CAPABILITIES.md').write_text('\n'.join(md)+'\n')
print(json.dumps(result['accounting']))
