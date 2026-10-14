"""The actual frozen-plan entrypoint: inert local policies only."""
import json
from pathlib import Path
from datetime import datetime,timedelta,timezone
from .transport import Frozen,MockIssuer,MockTransport,Runner,MOCK_MODEL,Denied,LABEL
from .scoring import score,paired,fraction,blind_free_text,UNIVERSE
from .oracle import check_key


def mock_permit(issuer,frozen,rows,**changes):
    """Creates only a signed LOCAL MOCK permit, never provider authority."""
    now=datetime.now(timezone.utc);n=len(rows)
    body=dict(mode='MOCK_ONLY',issuer=issuer.identity,endpoint='mock://in-process',model=MOCK_MODEL,
              privacy='ALLOW_SYNTHETIC_LOCAL_ONLY',use='ALLOW_INERT_MOCK_ONLY',retention='ALLOW_LOCAL_CAPTURE',
              retention_until=(now+timedelta(days=1)).isoformat(),expires_at=(now+timedelta(hours=1)).isoformat(),
              freeze=frozen.identity,schema='R2_TYPED_RESPONSE@2',price_class='INERT_MOCK_UNITS',quota='LOCAL_ONLY',
              spend_cap_micro=n*2,per_attempt_cost_bound_micro=1,per_trial_call_budget=2,
              total_call_budget=n*2,total_retry_budget=n,allowed_trials=[r['id'] for r in rows])
    return issuer.issue(body|changes)


def code_capture(raw,row):
    if raw is None:return ''
    if row.get('response_format')!='free_text_fixture':return raw
    try:
        x=json.loads(raw)
        if set(x)!={'text','belief_report','standing_report','origin_claim'}:return ''
        return blind_free_text(x['text'],x['belief_report'],x['standing_report'],x['origin_claim'])
    except (ValueError,TypeError,KeyError):return ''


def run_mock(root,freeze_path,out,policy='lawful',phases=None):
    """No provider parameter or live transport injection is accepted."""
    root=Path(root);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    frozen=Frozen(root,freeze_path)
    rows=[r for r in frozen.rows.values() if phases is None or r.get('phase','primary') in phases]
    key=json.loads((root/frozen.manifest['oracle_file']).read_text())
    check_key(list(frozen.cases.values()),key,UNIVERSE)
    issuer=MockIssuer();grant=mock_permit(issuer,frozen,rows);transport=MockTransport(policy)
    captures={};holds=[]
    with Runner(grant,issuer,frozen,transport,out/'ledger.jsonl') as runner:
        for row in rows:
            packet,_=frozen.approved(row['id'])
            try:raw=runner.call(row['id'],packet,row.get('max_tokens',256),row.get('response_format','typed'))
            except Denied as exc:raw=None;holds.append(dict(id=row['id'],hold=str(exc)))
            captures[row['id']]=code_capture(raw,row)
        summary=dict(evidence_label=LABEL,freeze=frozen.identity,policy=policy,n_planned=len(rows),
                     mock_dispatches=len(transport.requests),real_model_calls=0,actor_runs=0,
                     reserved_mock_micro_units=runner.spent,transport_attempts=runner.used,holds=holds)
    records=score(rows,captures,key)
    summary['correctness_fraction_plumbing_only']=fraction(records)
    summary['per_phase']={}
    for phase in sorted({r.get('phase','primary') for r in rows}):
        phaseids={r['id'] for r in rows if r.get('phase','primary')==phase}
        subset=[r for r in records if r['id'] in phaseids]
        summary['per_phase'][phase]=dict(n=len(subset),fraction=fraction(subset))
    primaryids={r['id'] for r in rows if r.get('phase','primary')=='primary'}
    primary=[r for r in records if r['id'] in primaryids]
    summary['paired_primary']={}
    if primary:
        for k in sorted({r['k'] for r in primary}):
            subset=[r for r in primary if r['k']==k]
            summary['paired_primary'][k]={c:paired(subset,comparator=c) for c in ['B','C']}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'coded_captures.json').write_text(json.dumps(captures,sort_keys=True)+'\n')
    return summary,records
