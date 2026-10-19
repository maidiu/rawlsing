"""Metadata-only archival owner rows; no respondent artifacts opened."""
import csv,io,json,sys,hashlib
from pathlib import Path
import prepare_evidence as custody
csv.field_size_limit(sys.maxsize)
R=Path(__file__).resolve().parent
PIN='aece04ac3fa2e488c6993c6b9c88eda296b2e6b8'
PRE='data/ddm_build_copy/recovery_integration/portable_evidence/G1A_CLOSURE_R1_20260826/'
def key(r):
    return (r.get('source_family') or r.get('source'),r.get('canonical_wave') or r.get('wave'),r.get('question_name') or r.get('var_name') or r.get('var_code'))
def safe(r):
    # Values remain unaltered; host locator columns are omitted explicitly.
    return {k:v for k,v in r.items() if k not in {'raw_path','codebook_path'} and not (v and '/Users/' in v)}
def main():
    p2=json.loads((R/'sources/p2_only_exact_rows.json').read_text())
    blocked=json.loads((R/'sources/qra_blocked_exact_rows.json').read_text())
    targets={(x['row']['source_family'],x['row']['wave'],x['row']['source_variable_code'].casefold()) for x in p2}
    targets|={(x['row']['canonical_source'],x['row']['canonical_wave'],x['row']['var_code'].casefold()) for x in blocked}
    # Explicit physical-name candidates are retained as evidence, never applied as aliases.
    targets|={('Latinobarómetro','2024',v.casefold()) for v in ['P45ST','P47ST.A','P47ST.B','P47ST.C','P47ST.D','P8NCV.A','P8NCV.B','P8NCV.C','P8NCV.D']}
    paths={'register_A':PRE+'03_C3_REGISTER_LINEAGE/REGISTER_A/question_structure_register.csv',
           'register_B':PRE+'03_C3_REGISTER_LINEAGE/REGISTER_B/question_structure_register.csv',
           'v525b_semantic':PRE+'03_C3_V525B_D62/raw/v525b/questions_master_semantic.csv',
           'v525b_drivers':PRE+'03_C3_V525B_D62/raw/v525b/questions_master_drivers.csv',
           'd62_driver_provenance_only':PRE+'03_C3_V525B_D62/raw/d62/questions_master_drivers.csv'}
    out={}
    for label,path in paths.items():
        rows=list(csv.DictReader(io.StringIO(custody.read(PIN,path).decode('utf-8-sig'))))
        chosen=[]
        for i,row in enumerate(rows,1):
            fam,wave,var=key(row)
            if (fam,wave,(var or '').casefold()) in targets:
                chosen.append(dict(csv_record=i,exact_case_key=[fam,wave,var],row_sha256=hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':')).encode()).hexdigest(),row=safe(row)))
        out[label]=dict(total_rows=len(rows),selected_records=chosen,match_rule='same canonical family/wave and casefold variable; candidate relation ONLY, not identity issuance',omitted_host_locator_columns=['raw_path','codebook_path'])
    custody.dump('sources/owner_row_projections.json',out)
    for name in ['HARVEST-001_ADJUDICATION.md','HARVEST-003_ADJUDICATION.md','HARVEST-004_ADJUDICATION.md','HARVEST-005L_ADJUDICATION.md','USABLE_UNIVERSE_AND_BINDING_ADJUDICATION.md']:
        custody.read(custody.WG0R,custody.RP+'sources/local_archive/'+name,'sources/'+name)
    for path in ['PYAT_CONTROL_ROOM/R18_WG5_WG5I_SCIENTIFIC_SCOPE_CORRECTION_AND_INHERITANCE_RECOGNITION_20261018.md']:
        custody.read(custody.BASE,path,'sources/R18_INHERITANCE_CORRECTION.md')
    custody.read(custody.WG0R,custody.RP+'evidence/current35_conservation.json','sources/WG0R_author_repaired_accounting_claims.json')
    # Historical receipt is retained as receipt, not rerun or new source grant.
    prefix=custody.RP+'sources/lits_historical/'
    names=__import__('subprocess').check_output(['git','ls-tree','-r','--full-tree','--name-only',custody.WG0R,prefix],text=True).splitlines()
    for path in names:
        if path.endswith(('09_FINAL_AS2B_RETURN.json','09_FINAL_AS2B_RETURN.md')):
            custody.read(custody.WG0R,path,'sources/lits_historical/'+Path(path).name)
    prior=json.loads((R/'evidence/source_manifest.json').read_text())
    custody.dump('evidence/source_manifest.json',list({(x['commit'],x['path']):x for x in prior+custody.manifest}.values()))
    print(json.dumps({k:len(v['selected_records']) for k,v in out.items()}))
if __name__=='__main__':main()
