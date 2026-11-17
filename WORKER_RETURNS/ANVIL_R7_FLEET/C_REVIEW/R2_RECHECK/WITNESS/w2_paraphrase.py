#!/usr/bin/env python3
"""R2 recheck W2 paraphrase witness: false T4/T6/T7 actor/world science in coherent
alternative prose that avoids the gate's exact blacklist while retaining valid
claim_grade, authority owner and empty forbidden_promotions."""
import json, pathlib, shutil, sys, tempfile

R2 = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW/WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R2_RECHECK')
TS=(R2/'LOGS/STAMP').read_text().strip(); PKG=R2/f'COLD/FRESH_{TS}/ANVIL_R7'; TOOLS=PKG/'tools'
sys.path.insert(0,str(TOOLS))
from r7_integrated import check  # noqa: E402
REPO='/Users/matthewsmith/s2b-work/rawlsing'; ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=R2/'WITNESS/W2_PARAPHRASE'; OUT.mkdir(parents=True,exist_ok=True)
tmp=pathlib.Path(tempfile.mkdtemp(prefix='w2_',dir=str(OUT))); ev=tmp/'EVIDENCE'; shutil.copytree(PKG/'EVIDENCE',ev); source=ev/'SOURCE_118'
c=json.loads((ev/'C.json').read_text())
c['boundary_court']['T4']['positive']=('The measured attitude distribution supplies the operative institutional control relation; '
    'a separately sourced material issuer is optional for this boundary.')
c['boundary_court']['T4']['negative']=('No independent structural issuer is needed because the survey distribution already carries '
    'the material relation for this selected world.')
c['boundary_court']['T6']['positive']=('Observed answers are available to the actor as mental content even where no encounter '
    'is recorded in the selected history.')
c['boundary_court']['T6']['negative']=('Later conduct may use the observed answer content without a separate access event or '
    'actor-local learning record.')
c['boundary_court']['T7']['positive']=('The performed fictional change is written into the empirical release as an updated '
    'observation for the next situation.')
c['boundary_court']['T7']['negative']=('No separate observable/fictional time split is needed once the branch is committed; '
    'the next situation may use the revised empirical content.')
c['scientific_and_owner_boundary']=('Observed attitude content is available to the actor and to material-world selection '
    'without a separate encounter or independent structural issuer.')
c['historical_no_loss_assessment']=('The focal person may retain a survey-compatible biography while later events use the '
    'observed answer content without an access event; no independent Other history is required.')
def put(name,obj):
    b=(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode(); (ev/name).write_bytes(b)
put('C.json',c)
res=check('C_INTEGRATED',c,ev,source,REPO,ZIP)
report={'schema':'C_REVIEW_R2_W2_PARAPHRASE','C_INTEGRATED':res,
        'verdict':'PARAPHRASE_CONFIRMED_IF_PASS' if res['status'].startswith('PASS') else 'PARAPHRASE_REFUSED'}
(OUT/'w2_result.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
