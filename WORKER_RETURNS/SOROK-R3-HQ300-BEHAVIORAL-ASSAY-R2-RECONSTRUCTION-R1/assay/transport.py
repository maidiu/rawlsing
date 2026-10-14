"""Mock-only authenticated permits, immutable freeze checks and durable budgets.

There is intentionally NO live adapter. MockIssuer is NOT a model-use issuer.
The journal is a local test accounting artifact, not provider billing evidence.
"""
import copy
import fcntl
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
from datetime import datetime,timezone
from .architecture import canonical,digest
from .architecture import build_packet,variants,DerivedCache
from .mock_policy import POLICIES,respond

MOCK_MODEL='sha256:'+hashlib.sha256(b'INERT_MOCK_POLICY_V2').hexdigest()
LABEL='MOCK_ONLY_NOT_BEHAVIORAL_EVIDENCE'


class Denied(ValueError):pass
class TransportError(RuntimeError):pass


class Frozen:
    def __init__(self,root,manifest_path):
        self.root=Path(root);self.path=Path(manifest_path)
        self.manifest_bytes=self.path.read_bytes();self.identity=hashlib.sha256(self.manifest_bytes).hexdigest()
        self.manifest=json.loads(self.manifest_bytes);self.verify()
        self.cases={x['id']:x for x in json.loads((self.root/self.manifest['corpus_file']).read_text())}
        rows=json.loads((self.root/self.manifest['schedule_file']).read_text())
        self.rows={x['id']:x for x in rows}
        if len(self.rows)!=len(rows):raise Denied('DUPLICATE_FROZEN_TRIAL')

    def approved(self,trial):
        row=self.rows[trial];packet,_=build_packet(self.cases[row['case']],row,DerivedCache())
        if row.get('variant'):packet=variants(packet,row['variant'])
        return packet,row

    def verify(self):
        if self.path.read_bytes()!=self.manifest_bytes:raise Denied('FREEZE_MANIFEST_CHANGED')
        for name,want in self.manifest['files'].items():
            p=(self.root/name).resolve()
            if not p.is_relative_to(self.root.resolve()):raise Denied('FREEZE_PATH_ESCAPE')
            if hashlib.sha256(p.read_bytes()).hexdigest()!=want:raise Denied('FROZEN_BYTES_CHANGED:'+name)


class MockIssuer:
    """Ephemeral test authority. Keys never written or returned in captures."""
    def __init__(self):
        self.identity='LOCAL_MOCK_AUTHORITY_ONLY';self._key=secrets.token_bytes(32)

    def sign(self,value):
        return hmac.new(self._key,canonical(value),hashlib.sha256).hexdigest()

    def issue(self,body):
        return dict(body=copy.deepcopy(body),signature=self.sign(body))


FIELDS={'mode','issuer','endpoint','model','privacy','use','retention','retention_until','expires_at',
        'freeze','schema','price_class','quota','spend_cap_micro','per_attempt_cost_bound_micro',
        'per_trial_call_budget','total_call_budget','total_retry_budget','allowed_trials'}


def positive_int(x,allow_zero=False):
    return type(x) is int and x >= (0 if allow_zero else 1)


def validate(grant,issuer,frozen,now=None):
    if type(issuer) is not MockIssuer:raise Denied('UNTRUSTED_ISSUER_CLASS')
    if not isinstance(grant,dict) or set(grant)!={'body','signature'}:raise Denied('NO_SIGNED_GRANT')
    g=grant['body']
    if not isinstance(g,dict) or set(g)!=FIELDS:raise Denied('GRANT_SCHEMA')
    if not hmac.compare_digest(str(grant['signature']),issuer.sign(g)):raise Denied('BAD_ISSUER_SIGNATURE')
    if g['mode']!='MOCK_ONLY' or g['issuer']!=issuer.identity:raise Denied('LIVE_MODE_OR_ISSUER_DENIED')
    if g['endpoint']!='mock://in-process' or g['model']!=MOCK_MODEL:raise Denied('ENDPOINT_OR_MODEL_NOT_PINNED')
    if (g['privacy'],g['use'],g['retention'])!=('ALLOW_SYNTHETIC_LOCAL_ONLY','ALLOW_INERT_MOCK_ONLY','ALLOW_LOCAL_CAPTURE'):
        raise Denied('NONAFFIRMATIVE_PERMISSION')
    if g['freeze']!=frozen.identity or g['schema']!='R2_TYPED_RESPONSE@2':raise Denied('FREEZE_OR_SCHEMA_BINDING')
    if g['price_class']!='INERT_MOCK_UNITS' or g['quota']!='LOCAL_ONLY':raise Denied('PRICE_QUOTA_BINDING')
    for field in ('spend_cap_micro','total_retry_budget'):
        if not positive_int(g[field],True):raise Denied('NONNEGATIVE_INTEGER_REQUIRED:'+field)
    for field in ('per_attempt_cost_bound_micro','per_trial_call_budget','total_call_budget'):
        if not positive_int(g[field]):raise Denied('INTEGER_REQUIRED:'+field)
    if g['per_trial_call_budget']>2:raise Denied('AT_MOST_ONE_TRANSPORT_RETRY')
    if not isinstance(g['allowed_trials'],list) or not g['allowed_trials'] or len(set(g['allowed_trials']))!=len(g['allowed_trials']) or any(not isinstance(x,str) or len(x)!=32 or any(c not in '0123456789abcdef' for c in x) for x in g['allowed_trials']):raise Denied('INVALID_TRIAL_SCOPE')
    if not set(g['allowed_trials'])<=set(frozen.rows):raise Denied('UNFROZEN_TRIAL_SCOPE')
    now=now or datetime.now(timezone.utc)
    try:
        expiry=datetime.fromisoformat(g['expires_at']);retention=datetime.fromisoformat(g['retention_until'])
        if expiry.tzinfo is None or retention.tzinfo is None or expiry<=now or retention<expiry:raise ValueError()
    except (TypeError,ValueError):raise Denied('EXPIRY_OR_RETENTION')
    frozen.verify()
    return g


class MockTransport:
    """The only dispatch implementation; policy receives provider-safe bytes."""
    __slots__=('policy','fail_first','requests')
    def __init__(self,policy='lawful',fail_first=0):
        if policy not in POLICIES:raise Denied('UNREGISTERED_POLICY')
        if not positive_int(fail_first,True):raise Denied('FAULT_INJECTION_TYPE')
        self.policy=policy;self.fail_first=fail_first;self.requests=[]

    def send(self,raw):
        self.requests.append(bytes(raw))
        if self.fail_first:
            self.fail_first-=1;raise TransportError('INERT_SIMULATED_TRANSPORT_FAILURE')
        return respond(json.loads(raw),self.policy)


class Runner:
    def __init__(self,grant,issuer,frozen,transport,journal):
        if type(transport) is not MockTransport:raise Denied('LIVE_OR_CUSTOM_TRANSPORT_FORBIDDEN')
        self.grant=copy.deepcopy(grant);self.issuer=issuer;self.frozen=frozen;self.transport=transport
        self.g=validate(self.grant,issuer,frozen);self.grant_hash=digest(self.grant)
        self.journal=Path(journal);self.journal.parent.mkdir(parents=True,exist_ok=True)
        self.lock=open(str(self.journal)+'.lock','a')
        try:fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            self.lock.close();raise Denied('LEDGER_BUSY')
        self.entries=[];self.used=0;self.spent=0;self.retries=0;self.attempts={};self.request_hashes={};self.done=set();self.consecutive=0
        try:
            if self.journal.exists():
                for line in self.journal.read_text().splitlines():
                    entry=json.loads(line);body=entry['body']
                    if entry['signature']!=issuer.sign(body) or body['previous']!=(digest(self.entries[-1]) if self.entries else 'GENESIS') or body['grant_hash']!=self.grant_hash:raise Denied('CORRUPT_OR_DIFFERENT_GRANT_LEDGER')
                    self.entries.append(entry);self._apply(body)
            else:self._append(dict(op='START'))
        except Exception:
            self.close();raise

    def _apply(self,b):
        if b['op']=='RESERVE':
            tid=b['trial'];self.used+=1;self.spent+=b['reserved_micro']
            if tid in self.attempts:self.retries+=1
            self.attempts[tid]=self.attempts.get(tid,0)+1;self.request_hashes[tid]=b['request_hash']
        elif b['op']=='CAPTURE':
            self.done.add(b['trial']);self.consecutive=0
        elif b['op']=='ERROR':self.consecutive+=1
        elif b['op']!='START':raise Denied('UNKNOWN_LEDGER_OPERATION')

    def _append(self,body):
        b=body|dict(previous=digest(self.entries[-1]) if self.entries else 'GENESIS',grant_hash=self.grant_hash,evidence_label=LABEL)
        entry={'body':b,'signature':self.issuer.sign(b)}
        with open(self.journal,'ab') as stream:
            stream.write(canonical(entry)+b'\n');stream.flush();os.fsync(stream.fileno())
        self.entries.append(entry);self._apply(b)

    def call(self,trial,packet,max_tokens=256,response_format='typed'):
        g=validate(self.grant,self.issuer,self.frozen)
        if trial not in g['allowed_trials'] or packet.get('response_id')!=trial:raise Denied('TRIAL_SCOPE')
        if trial in self.done:raise Denied('UNREPORTED_REDRAW_FORBIDDEN')
        if not positive_int(max_tokens) or max_tokens>256:raise Denied('TOKEN_BUDGET')
        approved,row=self.frozen.approved(trial)
        if packet!=approved or max_tokens!=row.get('max_tokens',256) or response_format!=row.get('response_format','typed'):raise Denied('UNFROZEN_REQUEST')
        raw=canonical(dict(model=g['model'],temperature=0,seed=row['model_seed'],max_tokens=max_tokens,packet=packet,response_format=response_format))
        request_hash=hashlib.sha256(raw).hexdigest()
        while True:
            validate(self.grant,self.issuer,self.frozen)
            previous=self.attempts.get(trial,0)
            if self.consecutive>=3:raise Denied('CONSECUTIVE_TRANSPORT_STOP')
            if previous and self.request_hashes[trial]!=request_hash:raise Denied('RETRY_BODY_CHANGED')
            if previous>=g['per_trial_call_budget']:raise Denied('PER_TRIAL_CAP')
            if self.used>=g['total_call_budget'] or self.spent+g['per_attempt_cost_bound_micro']>g['spend_cap_micro']:raise Denied('TOTAL_CALL_OR_SPEND_CAP')
            if previous and self.retries>=g['total_retry_budget']:raise Denied('RETRY_CAP')
            self._append(dict(op='RESERVE',trial=trial,request_hash=request_hash,request_raw=raw.decode(),reserved_micro=g['per_attempt_cost_bound_micro']))
            try:
                response=self.transport.send(raw)
                if not isinstance(response,str):raise TypeError('Mock response must be raw text')
            except TransportError as exc:
                self._append(dict(op='ERROR',trial=trial,error=str(exc),request_hash=request_hash))
                if self.attempts[trial]>=g['per_trial_call_budget']:return None
                continue
            except Exception as exc:
                self._append(dict(op='ERROR',trial=trial,error=type(exc).__name__,request_hash=request_hash))
                raise Denied('UNTYPED_PROVIDER_ERROR_NO_RETRY') from exc
            self._append(dict(op='CAPTURE',trial=trial,response_raw=response,request_hash=request_hash))
            return response

    def close(self):
        if hasattr(self,'lock') and not self.lock.closed:
            fcntl.flock(self.lock,fcntl.LOCK_UN);self.lock.close()

    def __enter__(self):return self
    def __exit__(self,*args):self.close()
