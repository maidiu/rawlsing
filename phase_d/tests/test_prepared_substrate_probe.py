import json, subprocess, sys
from pathlib import Path
import pandas as pd

SCRIPT = Path(__file__).parents[1] / "code" / "probe_prepared_substrate_relation_observability.py"

def run_probe(tmp_path, rows, members=None):
    ids = {
      "question_impl.phase0.881d5d09bf76e891f696":"Q2014", "question_impl.phase0.e8d34b3919db95a4ad22":"Q2012",
      "question_impl.phase0.17219d06fad537def5a1":"Q2015", "question_impl.phase0.330b4a6a537bf8d5a25a":"Q2011", "question_impl.phase0.7f7a79907d693d750021":"Q2013",
      "question_impl.phase0.0b8455f5bebf105fbfd3":"P15A", "question_impl.phase0.617913ae647c4a4d14d1":"P15B", "question_impl.phase0.645be92203aa2c5da96b":"P15C", "question_impl.phase0.2593fdb3cad3c14e0d18":"P15D", "question_impl.phase0.fc75feb0e293ff94608b":"P15E"}
    cw=tmp_path/'cw.csv'; pd.DataFrame([{'question_implementation_id':i,'source_family':'Arab Barometer','wave':'I','source_variable_code':v} for i,v in ids.items()]).to_csv(cw,index=False)
    for v in ids.values():
        for row in rows:
            row.setdefault(v, None)
    # The probe reads long-form rows; include every governed variable in the declared union.
    long=[]
    for row in rows:
        base={k:v for k,v in row.items() if k not in ids.values()}
        for v in ids.values():
            if row.get(v) is not None: long.append({**base,'var_code_norm':v})
    rows=long
    sub=tmp_path/'v550_shared_respondent_substrate.parquet'; pd.DataFrame(rows).to_parquet(sub,index=False)
    (tmp_path/'v550_shared_respondent_substrate_manifest.json').write_text(json.dumps({'v550_shared_extraction':True,'prepared_required':True,'forbid_database_access':True}))
    sel=tmp_path/'selection.csv'; ev=tmp_path/'evidence.csv'
    subprocess.run([sys.executable,str(SCRIPT),'--crosswalk',str(cw),'--arab-substrate',str(sub),'--latin-substrate',str(sub),'--selection-out',str(sel),'--evidence-out',str(ev)],check=True)
    return pd.read_csv(ev)

def test_support_classifications_and_no_ids(tmp_path):
    rows=[]
    for i in range(4):
        for v in ['Q2014','Q2012']:
            rows.append({'respondent_id_norm':f'r{i}','var_code_norm':v,'is_valid_substantive_response':True})
    for i in range(2): rows.append({'respondent_id_norm':f'u{i}','var_code_norm':'Q2014','is_valid_substantive_response':True})
    ev=run_probe(tmp_path,rows)
    assert ev.iloc[0].empirical_posture == 'OBSERVED'
    assert 'respondent_id' not in ev.to_csv(index=False)

def test_missing_union_fails_closed(tmp_path):
    rows=[{'respondent_id_norm':'r1','var_code_norm':'Q2014','is_valid_substantive_response':True}]
    try: run_probe(tmp_path,rows)
    except subprocess.CalledProcessError: return
    raise AssertionError('missing member did not fail closed')
