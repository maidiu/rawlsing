#!/usr/bin/env python3
"""Independent C-review witness: semantic hollowing of the 16-requirement roster and
F6 numeric-negative erasure while all 118 IDs, 16 headings, shapes, hashes and
booleans remain valid. Uses the candidate's own gate as the oracle.

Not a repair. Exact source/evidence copies are read-only inputs.
"""
import copy, hashlib, json, pathlib, shutil, sys, tempfile

ROOT = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/INTEGRATION/WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION/R2_C_WITNESS_OUTPUT')
INT = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/INTEGRATION/WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION')
COLD = pathlib.Path('/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/anvil-c-reviewr2-f47lroa6')
TOOLS = COLD/'ANVIL_R7/tools'
sys.path.insert(0, str(TOOLS))
from r7_integrated import check, digest, sha  # noqa: E402

REPO = '/Users/matthewsmith/s2b-work/rawlsing'
ZIP = '/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/INTEGRATION/WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION/R2_C_WITNESS_OUTPUT/W1_REQ_AND_F6_HOLLOW')
OUT.mkdir(parents=True, exist_ok=True)
tmp = pathlib.Path(tempfile.mkdtemp(prefix='w1_', dir=str(OUT)))
ev = tmp/'EVIDENCE'
shutil.copytree(INT/'EVIDENCE', ev)
source = ev/'SOURCE_118'

frame = json.loads((ev/'FRAME.json').read_text())
decision = json.loads((ev/'DECISION.json').read_text())

# 1. Hollow the choice-changing multiway-joint requirement while keeping ID/domain/binding.
req = next(r for r in frame['requirements'] if r['id'] == 'REQ-MULTIWAY-JOINT')
req['substantive_requirement'] = (
    'Pairwise marginals are a sufficient substitute for the three-way respondent joint; '
    'no same-person k>=3 F4 distinction need be preserved in the candidate.')
req['why_needed'] = (
    'The candidate deliberately uses a pairwise-only summary and treats it as an exact '
    'replacement for every whole-person joint analysis.')
req['loss_if_missing'] = (
    'No material distinction is lost when only pairwise marginals are stored; the three-way '
    'respondent pattern may be collapsed without a refusal or an owner hold.')
req['first_consumer'] = (
    'Pairwise marginal F4 summary reader authorizes itself without a same-person three-way reader.')
req['architectural_consequence'] = (
    'Accept the pairwise-only collapse, preserve no typed same-person k>=3 joint and expose no '
    'refusal for the missing higher-order pattern.')
req['proof_or_owner_hold'] = (
    'No proof or owner hold is required because pairwise marginal equality is accepted as an F6/F4 '
    'substitute by construction.')

# 2. Make the matching DECISION requirement disposition agree with the hollowed text.
cov = next(x for x in decision['requirement_dispositions'] if x['requirement_id'] == 'REQ-MULTIWAY-JOINT')
cov['actual_design_effect'] = (
    'The candidate stores pairwise marginals only and treats them as a complete replacement for '
    'the true same-person three-way respondent joint.')
cov['specific_first_consumer_path'] = (
    'The pairwise marginal summary reader consumes the collapsed product; no three-way F4 reader '
    'is named, required or preserved.')
cov['conservation_or_refusal_witness'] = (
    'No three-way joint is conserved and no refusal is issued; pairwise marginal equality is accepted '
    'as sufficient evidence for the F4 result.')

# 3. Erase the F6 numeric-vs-guard distinction on the exact F6 identity.
f6 = next(x for x in decision['identity_dispositions'] if x['identity_id'] == 'K1-CAP-17')
f6['design_effect'] = (
    'F6 numeric bounds are guaranteed by the I07 guard, so no separate numeric uncertainty interval, '
    'uncovered mass or methods owner is required.')
f6['first_consumer_path'] = (
    'The I07 guard is the F6 numeric first consumer; no qualified F6 methods/uncertainty reader is needed.')
f6['conservation_or_refusal_witness'] = (
    'Numeric uncertainty is fully conserved by the I07 guard; no additional F6 interval computation or '
    'negative witness is required.')
f6['status_assertion'] = 'HISTORICAL_FUNCTION_RETAINED'

def put(name, obj):
    b = (json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()
    (ev/name).write_bytes(b)
    return {'path': name, 'sha256': sha(b)}

# Re-pin only the changed packet files; source evidence and origins untouched.
put('FRAME.json', frame)
inv = json.loads((ev/'SOURCE_IDENTITY_INVENTORY.json').read_text())
frame['source_inventory'] = {'path': 'SOURCE_IDENTITY_INVENTORY.json', 'sha256': sha((ev/'SOURCE_IDENTITY_INVENTORY.json').read_bytes())}
put('FRAME.json', frame)
decision['common_frame'] = {'path': 'FRAME.json', 'sha256': sha((ev/'FRAME.json').read_bytes())}
decision['frame_sha256'] = digest(frame)
put('DECISION.json', decision)

fr = check('FRAME', frame, ev, source, REPO, ZIP)
de = check('DECISION', decision, ev, source, REPO, ZIP)
report = {
    'schema': 'C_REVIEW_WITNESS_W1',
    'question': 'Can a choice-changing scientific distinction be erased while IDs/headings/hashes remain valid?',
    'mutations': [
        'REQ-MULTIWAY-JOINT text replaced by explicit pairwise-only acceptance',
        'matching requirement disposition replaced by explicit pairwise-only acceptance',
        'K1-CAP-17 F6 numeric/guard distinction replaced by "guard is numeric bound"',
    ],
    'FRAME': fr,
    'DECISION': de,
    'verdict': 'WITNESS_CONFIRMED_IF_BOTH_PASS' if fr['status'].startswith('PASS') and de['status'].startswith('PASS') else 'WITNESS_REFUTED',
}
(OUT/'w1_result.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
