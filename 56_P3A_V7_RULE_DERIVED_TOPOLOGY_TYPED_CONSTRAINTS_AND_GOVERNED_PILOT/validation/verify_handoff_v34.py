from pathlib import Path
import csv,json,hashlib,sys,zipfile
ROOT=Path(sys.argv[1]).resolve()
SEC=ROOT/'56_P3A_V7_RULE_DERIVED_TOPOLOGY_TYPED_CONSTRAINTS_AND_GOVERNED_PILOT'
fail=[]
def need(p):
    if not p.exists(): fail.append(f'missing {p.relative_to(ROOT)}')
    return p
def load_json(rel): return json.loads(need(SEC/rel).read_text())
def csv_rows(rel):
    p=need(SEC/rel)
    return list(csv.DictReader(p.open())) if p.exists() else []
# no generated caches
for p in ROOT.rglob('*'):
    if p.name=='__pycache__' or p.suffix=='.pyc': fail.append(f'generated python cache present: {p.relative_to(ROOT)}')
# forbidden production code/input references
forbidden=['P3_PREFLIGHT_CANDIDATE_INVENTORY_v7.csv','V32_DIRECT_INTERNAL_AUTHORITY_MISCLASSIFICATION.csv','V32_ATTACHMENT_BRIDGE_OMISSIONS.csv','V33_ATTACHMENT_SEED_META_NODE_ERRORS.csv','V33_PILOT_SELECTION_RULE_MISMATCH.csv','V33_TYPED_CONSTRAINT_GRAPH_GAPS.csv']
for sub in [SEC/'code']:
    for p in sub.rglob('*'):
        if p.is_file() and p.suffix in {'.py','.sql','.json','.md'}:
            t=p.read_text(errors='ignore')
            for token in forbidden:
                if token in t: fail.append(f'forbidden production reference {token}: {p.relative_to(ROOT)}')
# required reports
required_json=['outputs/v34_populated_validation_matrix_summary.json','P3A_V34_OBJECT_COUNTS.json','P3A_V34_PILOT_SELECTION_RETURN.json','P3A_V34_FIXTURE_RETURN.json','P3A_V34_TOPOLOGY_DERIVATION_RETURN.json']
for r in required_json: need(SEC/r)
required_csv=['P3A_V34_TYPED_CONSTRAINT_RECONCILIATION.csv','P3A_V34_SEED_META_NODE_RECONCILIATION.csv','P3A_V34_SIGNATURE_BLOCKER_RECONCILIATION.csv','P3A_V34_DATABASE_PACKET_CONVERGENCE.csv','P3A_V34_PILOT_STRATA_ELIGIBILITY.csv','P3A_V34_PILOT_SUBSTITUTION_LEDGER.csv','P3A_V34_QUERY_MATRIX.csv','P3A_V34_EXECUTION_FINDINGS.csv']
for r in required_csv: need(SEC/r)
# statuses
try:
    q=load_json('outputs/v34_populated_validation_matrix_summary.json')
    if q.get('status')!='PASS_WITH_PHASE_AWARE_OVERRIDES': fail.append('query matrix status not phase-aware PASS')
    if sorted(q.get('failures',[]))!=['q01b_postpromotion_pointer','q15b_no_unadjudicated_at_p3_close']: fail.append('unexpected query matrix failures')
    counts=load_json('P3A_V34_OBJECT_COUNTS.json')
    if counts.get('status')!='PASS': fail.append('object counts not PASS')
    c=counts.get('candidates',{})
    expected={'candidate_families':141,'candidate_revisions':141,'candidate_memberships':496,'internal_pair_rows':1129,'pair_level_closure_obligations':345,'diagnostic_blocker_rows':141,'collision_constraints':2,'unresolved_constraints':7,'redirect_constraints':1,'coordinate_constraints':1}
    for k,v in expected.items():
        if c.get(k)!=v: fail.append(f'candidate metric {k} expected {v} got {c.get(k)}')
    if c.get('origin_counts')!={'STRICT_RESPONSE_COMPONENT':94,'PROPOSITION_ONLY_SEED':25,'ATTACHMENT_REVIEW':22}: fail.append('origin counts mismatch')
    topo=load_json('P3A_V34_TOPOLOGY_DERIVATION_RETURN.json')
    if topo.get('status')!='PASS' or topo.get('candidate_count')!=141: fail.append('topology derivation not PASS/141')
    pilot=load_json('P3A_V34_PILOT_SELECTION_RETURN.json')
    if pilot.get('status')!='PASS' or pilot.get('selected_packet_count')!=40: fail.append('pilot selection not PASS/40')
    if len(pilot.get('governed_strata',[]))!=11: fail.append('pilot governed strata not 11')
    fix=load_json('P3A_V34_FIXTURE_RETURN.json')
    if fix.get('status')!='PASS': fail.append('fixture not PASS')
    if fix.get('main_p3a_canonical_families')!=0 or fix.get('main_p3a_adjudications')!=0: fail.append('fixture polluted main P3A release')
except Exception as e: fail.append(f'json validation error: {e}')
for rel in ['P3A_V34_TYPED_CONSTRAINT_RECONCILIATION.csv','P3A_V34_SEED_META_NODE_RECONCILIATION.csv','P3A_V34_SIGNATURE_BLOCKER_RECONCILIATION.csv','P3A_V34_DATABASE_PACKET_CONVERGENCE.csv']:
    rows=csv_rows(rel)
    if not rows: fail.append(f'{rel} empty')
    for i,r in enumerate(rows, start=2):
        if r.get('status')!='PASS': fail.append(f'{rel}:{i} status {r.get("status")}')
strata=csv_rows('P3A_V34_PILOT_STRATA_ELIGIBILITY.csv')
if len(strata)!=11: fail.append('pilot strata eligibility does not have 11 rows')
for i,r in enumerate(strata,start=2):
    if r.get('status') not in {'PASS','SHORTFALL_RECORDED'}: fail.append(f'bad pilot stratum status line {i}')
# packet/draft counts and validation
packets=list((SEC/'candidate_packets').glob('*.json'))
drafts=list((SEC/'draft_decisions').glob('*.json'))
if len(packets)!=40: fail.append(f'expected 40 packets got {len(packets)}')
if len(drafts)!=40: fail.append(f'expected 40 drafts got {len(drafts)}')
# CSV/TSV should not start with SET
for p in ROOT.rglob('*'):
    if p.suffix.lower() in {'.csv','.tsv'}:
        try:
            first=p.read_text(errors='ignore').splitlines()[0] if p.stat().st_size else ''
            if first.startswith('SET'): fail.append(f'SET-prefixed table artifact {p.relative_to(ROOT)}')
        except Exception as e: fail.append(f'cannot inspect {p.relative_to(ROOT)}: {e}')
print(json.dumps({'status':'FAIL' if fail else 'PASS','failures':fail},indent=2))
sys.exit(1 if fail else 0)
