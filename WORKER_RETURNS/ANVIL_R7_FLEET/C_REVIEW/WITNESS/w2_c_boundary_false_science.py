#!/usr/bin/env python3
"""Independent C-review witness W2: the T1-T7 C court checks string length and a
local excerpt, not the boundary's negative semantics. A C_HOLD packet can assert
survey->actor private knowledge, survey->structural power, and fictional->observed
backflow while the candidate gate still returns PASS."""
import json, pathlib, shutil, sys, tempfile

ROOT = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW')
INT = ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION'
COLD = sorted((ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/TEMP').glob('COLD_*'))[-1]
TOOLS = COLD/'ANVIL_R7/tools'
sys.path.insert(0, str(TOOLS))
from r7_integrated import check  # noqa: E402

REPO='/Users/matthewsmith/s2b-work/rawlsing'
ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/WITNESS/W2_C_BOUNDARY_FALSE_SCIENCE'
OUT.mkdir(parents=True, exist_ok=True)
tmp=pathlib.Path(tempfile.mkdtemp(prefix='w2_',dir=str(OUT)))
ev=tmp/'EVIDENCE'; shutil.copytree(INT/'EVIDENCE',ev)
source=ev/'SOURCE_118'
c=json.loads((ev/'C.json').read_text())

# Contradict the actual source vetoes while preserving every pointer, boundary ID,
# positive/negative/restore field and length requirement.
c['boundary_court']['T4']['positive']=(
    'Survey opinion frequency is institutional power; the survey marginal directly establishes '
    'material control, sanctions and causal structural force without any independent source.')
c['boundary_court']['T4']['negative']=(
    'An independent structural producer is refused because the observed survey distribution is '
    'treated as sufficient proof of institutional control.')
c['boundary_court']['T6']['positive']=(
    'Survey answers directly give the actor private knowledge, motive and memory without an admitted '
    'encounter or any independently owned actor-access event.')
c['boundary_court']['T6']['negative']=(
    'An actor who never encountered an event nevertheless learns it automatically from source '
    'correlations, and no no-change or nonaccess outcome is permitted.')
c['boundary_court']['T7']['positive']=(
    'A fictional performed action edits the observed empirical source and rewrites the sealed C11 '
    'past automatically, with no separate world or science authorization.')
c['boundary_court']['T7']['negative']=(
    'No distinction is kept between observed source time, fictional actor time and the next '
    'situation; any branch may overwrite the measured source.')
c['scientific_and_owner_boundary']=(
    'Observed survey answers are allowed to cause actor-private psychology and material power '
    'directly, with no independent scientific issuer, actor consent or world-authority boundary.')
c['historical_no_loss_assessment']=(
    'The pair of independent actors is replaced by a survey-compatible narrative; the focal actor '
    'may acquire offscreen knowledge without access and no no-change case is retained.')

def put(name,obj):
    b=(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    (ev/name).write_bytes(b)
    return {'path':name,'sha256':__import__('hashlib').sha256(b).hexdigest()}
put('C.json',c)
res=check('C_INTEGRATED',c,ev,source,REPO,ZIP)
report={'schema':'C_REVIEW_WITNESS_W2','mutations':[
 'T4 positive/negative assert survey opinion = institutional causal power',
 'T6 positive/negative assert survey answers give actor private knowledge without encounter',
 'T7 positive/negative assert fictional action overwrites observed source',
 'C scientific/owner and no-loss prose assert the same firewall breach'],
 'C_INTEGRATED':res,
 'verdict':'WITNESS_CONFIRMED_IF_PASS' if res['status'].startswith('PASS') else 'WITNESS_REFUTED'}
(OUT/'w2_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
