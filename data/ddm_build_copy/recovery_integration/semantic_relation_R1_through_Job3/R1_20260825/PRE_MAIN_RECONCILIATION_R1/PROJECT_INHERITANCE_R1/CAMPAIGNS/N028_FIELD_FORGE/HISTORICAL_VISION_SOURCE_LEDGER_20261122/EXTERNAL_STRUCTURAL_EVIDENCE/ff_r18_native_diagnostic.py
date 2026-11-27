"""R18 local source diagnostic, NOT the C11/I03 producer or an issuance.
Run with the user-held archive; no respondent IDs or individual rows emitted.
No across-country pooling, imputation, weighting or causal/actor inference.
"""
import argparse
import hashlib
import io
import json
import tempfile
import zipfile
from pathlib import Path

import pandas as pd

STEM = 'Rawlsing 35 waves of savs & dtas/'
DATA = STEM + 'Source savs & dtas/LiTS_IV.dta'
BOOK = STEM + 'Codebooks/LiTS-IV-codebook.csv'
DATA_SHA = '14e1032755c4f42d8d3dc61647097ccd7605ba281551e53953c76d22a223cd1c'
BOOK_SHA = 'c88ab0ecd3effcfe4a88816263620482c339c40dc61ec2468aa120148d283d07'
FIELDS = ('country', 'q310', 'q109b', 'q110b', 'q111b', 'q401f', 'q405e')


def run(archive):
    with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
        raw = z.read(BOOK)
        if hashlib.sha256(raw).hexdigest() != BOOK_SHA:
            raise ValueError('different codebook bytes')
        book = pd.read_csv(io.BytesIO(raw)).set_index('var_name')
        path = Path(tmp) / 'source.dta'
        digest = hashlib.sha256()
        with z.open(DATA) as src, path.open('wb') as dst:
            while block := src.read(1 << 20):
                digest.update(block)
                dst.write(block)
        if digest.hexdigest() != DATA_SHA:
            raise ValueError('different native source bytes')
        with pd.io.stata.StataReader(path) as reader:
            labels = reader.variable_labels()
            values = reader.value_labels()
            # Diagnostic metadata introspection only; exact runtime version recorded.
            native = {k: {int(a): b for a,b in values[reader._lbllist[reader._varlist.index(k)]].items()} for k in FIELDS}
        df = pd.read_stata(path, columns=list(FIELDS), convert_categoricals=False)
    metadata = {k: {'native_label': labels[k], 'codebook_label': str(book.loc[k,'question_text']),
                    'native_values': native[k]} for k in FIELDS}
    expected = {'q310': {1:'Paid employee',4:'Self-employed with employees'},
                'q401f':{4:'Agree',5:'Strongly agree'},'q405e':{1:'Yes',2:'No'}}
    for k, pairs in expected.items():
        if any(native[k].get(v) != label for v,label in pairs.items()):
            raise ValueError('native response domain changed: '+k)
    results = []
    for country, frame in df.groupby('country', sort=True):
        for role in (1,4):
            group = frame[frame.q310.eq(role)]
            full = group[group.q401f.isin(range(1,6)) & group.q405e.isin((1,2))]
            joint = full.groupby(['q401f','q405e']).size()
            cells = [{'q401f':a,'q405e':b,'n':int(joint.get((a,b),0))}
                     for a in range(1,6) for b in (1,2)]
            assert sum(c['n'] for c in cells)==len(full)
            results.append({'country':int(country),'name':native['country'][int(country)],
                'role':role,'country_rows':len(frame),'role_rows':len(group),
                'full_case_n':len(full),'excluded_unresolved_n':len(group)-len(full),
                'cells':cells})
    return {'grade':'LOCAL_RAW_DESCRIPTIVE_DIAGNOSTIC_NOT_C11_OR_SOURCE_ISSUANCE',
            'native_sha256':DATA_SHA,'codebook_sha256':BOOK_SHA,'pandas':pd.__version__,
            'source_rows':len(df),'metadata':metadata,'country_role_joints':results,
            'limits':['role is reported main-job status, not generalized class or political power',
                      'only complete cases of the two items; asked eligibility and survey weights not established',
                      'q405e label is not a complete question stem; no inferred payment instrument',
                      'no cross-country pooling, no publication or native scientific authorization']}

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('output');a=p.parse_args()
    Path(a.output).write_text(json.dumps(run(a.archive),ensure_ascii=False,indent=2)+'\n')
