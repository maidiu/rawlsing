#!/usr/bin/env python3
"""Portable MCR-lite/R5 launch structural proxy; NOT canonical Rawlsing repository checker."""
import json,re,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
FILES=['07_CODEX_HQ_MASTER_LAUNCH.md','08_DEEPSEEK_A_LAUNCH.md','09_DEEPSEEK_B_LAUNCH.md','10_BROWSER_C_LAUNCH.md']
fields=['MCR','REPOSITORY','AGENT_TYPE','INTELLIGENCE_LEVEL','SINGLE_AGENT_FULL_DELIVERABLE','EXECUTION_SURFACE','USER_SELECTED_EDITOR_MODEL_PAIR','MODEL','REASONING','PROVIDER/EDITOR_HARNESS','MODEL_MAX_AVAILABILITY','HOST_ACCOUNT_QUOTA_COST','BRANCH','STARTUP_SHA','ACTIVE_WORKER_NO_DISTURBANCE','BROWSER?','DEEPSEEK?','CODEX_6_1_HIGH_NECESSARY?','OTHERWISE_MIDDLE?','WHY_NOT_BROWSER','WHY_NOT_FLASH','WHY_NOT_CODEX_HIGH','WHY_NOT_MIDDLE','SCIENCE_SOURCE_ACTOR_AUTHORITY','POST_RETURN_INDEPENDENT_REVIEW','COMMISSION_KIND','CONTRACT_ID','CONTRACT_SOURCE_CUT','WORK_SCOPE_AND_FLIGHT','TERMINAL_CONSUMER_AND_EFFECT','FROZEN_ORACLE_AND_COUNTEREXAMPLE','EXECUTION_AND_AUTHOR_PREFLIGHT','CLOSURE_AND_OUT_OF_SCOPE']
out=[]
for f in FILES:
    txt=(ROOT/f).read_text();e=[]
    if txt.count('```text')!=1 or txt.count('```\n')!=1:e.append('MISSING_EXACT_SINGLE_CODE_FENCE')
    prompt=txt.split('```text\n',1)[-1].split('```\n',1)[0]
    heads=dict(re.findall(r'^([^\n:]+):\s*(.*?)$',prompt,re.M))
    for k in fields:
        if not heads.get(k):e.append('MISSING_HEADER:'+k)
    if heads.get('MCR')!='LITE' or heads.get('REPOSITORY')!='maidiu/rawlsing' or heads.get('SINGLE_AGENT_FULL_DELIVERABLE')!='YES':e.append('MCR_SCOPE_INVALID')
    if heads.get('STARTUP_SHA')!='7fc00289dd801d2d0a8ce159986c7595fc27a4d9':e.append('BAD_HISTORICAL_START_CUT')
    if not re.match(r'[^@\s]+@[0-9a-f]{40}$',heads.get('CONTRACT_SOURCE_CUT','')):e.append('BAD_SOURCE_PIN')
    if not heads.get('BRANCH','').startswith(('agent/','proposal/','review/')):e.append('BAD_BRANCH_NAME')
    for key in ('ANVIL_SPINE_R5','P15','ANVIL_STAGE_R5','NO_NEW_PRODUCT_ADVANCE','FUTURE','SEAM','SOROK','K3','CURRENT_PROGRESS','independent'):
        if key.lower() not in prompt.lower():e.append('MISSING_R5_CRITICAL_REQUIREMENT:'+key)
    for cmd in ('tools/anvil.py','tools/test_r5.py','tools/check_stage.py'):
        if cmd not in prompt or not (ROOT/cmd).exists():e.append('PROMPT_CALLS_UNAVAILABLE_TOOL:'+cmd)
    out.append({'name':f,'status':'PASS_PORTABLE_FORMAT_PROXY' if not e else 'RED','errors':e,'prompt_chars':len(prompt)})
print(json.dumps({'status':'PASS_FORMAT_ONLY_CANONICAL_REPO_CHECKER_NOT_RUN' if all(not x['errors'] for x in out) else 'RED','launches':out},indent=2))
if any(x['errors'] for x in out):sys.exit(2)
