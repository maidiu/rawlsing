#!/usr/bin/env python3
"""R2 recheck W1/W4 paraphrase witness: a coherent alternative phrasing of a
pairwise-only F4 rule and an I07-guard-as-F6-numeric claim, preserving all IDs,
typed obligations, source excerpt hashes and required vocabulary. Tests whether
the new phrase guards are an actual semantic court or only a blacklist."""
import copy, hashlib, json, pathlib, shutil, sys, tempfile

R2 = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/INTEGRATION/WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION/R3_WITNESS')
TS = (R2/'LOGS/STAMP').read_text().strip()
PKG = R2/f'COLD/FRESH_{TS}/ANVIL_R7'
TOOLS = PKG/'tools'
sys.path.insert(0, str(TOOLS))
from r7_integrated import check, digest, sha  # noqa: E402

REPO='/Users/matthewsmith/s2b-work/rawlsing'
ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=R2/'WITNESS/W1_PARAPHRASE'
OUT.mkdir(parents=True, exist_ok=True)
tmp=pathlib.Path(tempfile.mkdtemp(prefix='w1_',dir=str(OUT)))
ev=tmp/'EVIDENCE'; shutil.copytree(PKG/'EVIDENCE',ev); source=ev/'SOURCE_118'
frame=json.loads((ev/'FRAME.json').read_text())
decision=json.loads((ev/'DECISION.json').read_text())

# Coherent pairwise-only claim: keeps all required words, avoids exact forbidden
# phrases, avoids 'sufficient' and 'substitute' beside 'pairwise'.
PAIR=('The three-way same-person joint is retained as an audit label, but the selected F4 result '
      'uses the pairwise product; higher-order membership is informational only and is not required '
      'for the operative result.')
req=next(r for r in frame['requirements'] if r['id']=='REQ-MULTIWAY-JOINT')
for k in ('substantive_requirement','why_needed','loss_if_missing','first_consumer','architectural_consequence','proof_or_owner_hold'):
    req[k]=PAIR+' '+str(req.get(k,''))
# keep positive/negative probes; they are still present in the frame
cov=next(x for x in decision['requirement_dispositions'] if x['requirement_id']=='REQ-MULTIWAY-JOINT')
cov['actual_design_effect']=PAIR
cov['specific_first_consumer_path']='The pairwise F4 product reader is the operative first consumer; the three-way same-person joint is retained only as an audit label.'

# K1-CAP-11: source meaning/negative untouched; design/witness now permit pairwise-only.
k11=next(x for x in decision['identity_dispositions'] if x['identity_id']=='K1-CAP-11')
k11['design_effect']=PAIR
k11['conservation_or_refusal_witness']=('Positive: the three-way same-person joint is retained as a label; negative: the pairwise product is accepted '
    'for the operative F4 result; restore: exact bytes. Higher-order membership is informational only and is not required for the result.')

# K1-CAP-17: guard-as-numeric in alternative prose.
GUARD=('The I07 guard is the accepted F6 numeric implementation; interval and uncovered-mass work is covered by that guard '
       'and further estimation is not required for the selected result.')
k17=next(x for x in decision['identity_dispositions'] if x['identity_id']=='K1-CAP-17')
k17['design_effect']=GUARD
k17['conservation_or_refusal_witness']=('Positive: the I07 guard is the accepted F6 numeric implementation; negative: further estimation is not required; '
    'restore: exact bytes. The guard covers the interval and uncovered-mass result.')

def put(name,obj):
    b=(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    (ev/name).write_bytes(b); return {'path':name,'sha256':sha(b)}
put('FRAME.json',frame)
decision['common_frame']={'path':'FRAME.json','sha256':sha((ev/'FRAME.json').read_bytes())}
decision['frame_sha256']=digest(frame)
put('DECISION.json',decision)
fr=check('FRAME',frame,ev,source,REPO,ZIP)
de=check('DECISION',decision,ev,source,REPO,ZIP)
report={'schema':'C_REVIEW_R2_W1_PARAPHRASE','pairwise_text':PAIR,'f6_text':GUARD,
        'FRAME':fr,'DECISION':de,
        'verdict':'PARAPHRASE_CONFIRMED_IF_BOTH_PASS' if fr['status'].startswith('PASS') and de['status'].startswith('PASS') else 'PARAPHRASE_REFUSED'}
(OUT/'w1_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
