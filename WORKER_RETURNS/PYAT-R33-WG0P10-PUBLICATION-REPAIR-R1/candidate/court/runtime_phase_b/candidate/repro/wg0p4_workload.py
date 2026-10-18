"""WG0P4 sourcefree compiler using unchanged accepted C11/I03/Batch owners.

Trust boundary: fixture owner state is separate from request/plan/checkpoint.
It is a local TEST_ONLY harness owner, never an original source/EE issuer.
An attacker controls exported requests/checkpoints, not the owner directory,
Python code, interpreter or signing key. No production/semantic owner is patched.
"""
from __future__ import annotations
import copy, hashlib, hmac, importlib.util, json, os, pathlib, secrets, sys
from collections import Counter
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Any

R = pathlib.Path(__file__).resolve().parents[1]
PINNED = R / 'pinned'
sys.path.insert(0, str(PINNED))
# Every read-only staged file, including actual owner preimages, is verified.
for _row in json.loads((R/'source_selector.json').read_text())['files']:
    _data=(PINNED/_row['staging_path']).read_bytes()
    if hashlib.sha1(b'blob '+str(len(_data)).encode()+b'\0'+_data).hexdigest()!=_row['git_blob_sha1']:
        raise RuntimeError('PINNED_SOURCE_IDENTITY_MISMATCH:'+_row['staging_path'])
_sp=importlib.util.spec_from_file_location('_wg0p3_original',PINNED/'predecessors/p3/repro/wg0p3_workload.py')
base=importlib.util.module_from_spec(_sp);sys.modules[_sp.name]=base;_sp.loader.exec_module(base)
from rawlsing_next.pre553_batch_runner import BatchExecutionRunner,BatchManifest,BatchUnitSpec,ExecutionOutcome,ExecutorBinding,UnitExecutionReceipt,BatchIntegrityError
from rawlsing_next.pre553_empirical_objects import ExactRef,EmpiricalFact,EmpiricalQuerySpec,canonicalize,semantic_hash
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_c11_repository import C11Repository

NativeItem=base.NativeItem;OperationCandidate=base.OperationCandidate;Disposition=base.Disposition
AuthoritySnapshot=base.AuthoritySnapshot
PERMITTED_GRANT='GRANTED_FIXTURE'
VERSION='WG0P4_NATIVE_FRONTIER_COLD@1'
class IdentityError(ValueError): pass
class FrontierError(ValueError): pass
class RevocationError(PermissionError): pass
class ColdRestartError(ValueError): pass
class NativeDataError(ValueError): pass

# Immutable prospective expectation files were committed before this implementation.
FROZEN_SHA256={'ORIGINAL_FRONTIER.json':'1af4d869c1b63046d0439ef607642f649dd13727394ae796a86399bc9e22023f','CONDITIONAL_FRONTIER.json':'2f6826e52f46cfecf5c96f0abccd48891e3220ffe0e88f222924f66f15804abe'}
def frozen(name):
    data=(R/name).read_bytes()
    if hashlib.sha256(data).hexdigest()!=FROZEN_SHA256[name]:raise FrontierError('EXTERNAL_FROZEN_ORACLE_CHANGED')
    return json.loads(data)
def _plain(value):
    if isinstance(value,dict) or hasattr(value,'items'):return {str(k):_plain(v) for k,v in value.items()}
    if isinstance(value,(set,frozenset)):return sorted((_plain(v) for v in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,(list,tuple)):return [_plain(v) for v in value]
    if hasattr(value,'as_dict'):return _plain(value.as_dict())
    return value
def canonical(value):return json.dumps(_plain(value),sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(value):return hashlib.sha256(canonical(value)).hexdigest()
def _h(s):return hashlib.sha256(s.encode()).hexdigest()
def _ref(kind,label):return ExactRef(kind,'urn:wg0p4:test:'+label,_h(kind+':'+label))
def ref(d):
    if not isinstance(d,dict) or set(d)!={'kind','object_id','content_hash'}:raise IdentityError('CLOSED_EXACT_REF_REQUIRED')
    return ExactRef(**d)
def native_item(d):
    d=dict(d);d['options']=tuple(d['options']);d['missing_codes']=tuple(d['missing_codes']);return NativeItem(**d)
def independent_oracle_items():return [native_item(d) for d in frozen('ORIGINAL_FRONTIER.json')['native_items']]
def conditional_items():return [native_item(d) for d in frozen('CONDITIONAL_FRONTIER.json')['native_items']]
def receipt_row(o):return dict(op_id=o.op_id,op_class=o.op_class,target=o.target,conditioners=list(o.conditioners),item_ids=list(o.item_ids),disposition=o.disposition.value,disposition_reason=o.disposition_reason)
def original_rows():
    return sorted([dict(op_id=o['id'],op_class=o['class'],target=o['item_ids'][0],conditioners=o['item_ids'][1:],item_ids=o['item_ids'],disposition=o['disposition'],disposition_reason=o['reason']) for o in frozen('ORIGINAL_FRONTIER.json')['independent_oracle']['expected_opportunity_inventory']],key=lambda x:x['op_id'])
def expected_rows(mode):return original_rows() if mode=='original25' else sorted(frozen('CONDITIONAL_FRONTIER.json')['operations'],key=lambda x:x['op_id'])
def frontier_root(mode):return digest({'mode':mode,'rows':expected_rows(mode),'metadata':frozen('ORIGINAL_FRONTIER.json' if mode=='original25' else 'CONDITIONAL_FRONTIER.json')['native_items']})
def _mode(rows):
    ids={o['op_id'] for o in rows}
    if ids=={o['op_id'] for o in expected_rows('conditional4')}:return 'conditional4'
    return 'original25'
def validate_frontier(ops,*,mode=None):
    rows=sorted([receipt_row(o) for o in ops],key=lambda x:x['op_id']);mode=mode or _mode(rows)
    if rows!=expected_rows(mode):raise FrontierError('EXACT_EXTERNAL_FRONTIER_MISMATCH')
    return dict(Counter(o['disposition'] for o in rows))
def validate_frontier_receipts(receipts,expected_ops=None,*,mode=None):
    rows=sorted(_plain(receipts),key=lambda x:x['op_id']);mode=mode or _mode(rows)
    if rows!=expected_rows(mode):raise FrontierError('RECEIPTS_NOT_INDEPENDENT_ORIGINAL_FRONTIER')
    if expected_ops is not None:validate_frontier(expected_ops,mode=mode)

class WorkloadBuilder(base.WorkloadBuilder):
    def __init__(self):super().__init__();self._joint=None
    def add_joint_risk_authority(self,authority):
        if self._frozen:raise FrontierError('FRONTIER_ALREADY_FROZEN')
        if authority!=joint_risk_authority():raise IdentityError('UNKNOWN_OR_FOREIGN_JOINT_AUTHORITY')
        self._joint=copy.deepcopy(authority)
    def freeze(self):
        self._frozen=True
        return digest({'items':sorted([_plain(vars(i)) for i in self._items],key=lambda d:d['item_id']),'joint':self._joint})
    def enumerate(self):
        rows=super().enumerate()
        if self._joint:
            if sorted([_plain(vars(x)) for x in self._items],key=lambda d:d['item_id'])!=sorted(frozen('CONDITIONAL_FRONTIER.json')['native_items'],key=lambda d:d['item_id']):raise IdentityError('JOINT_NATIVE_CARRIER_MISMATCH')
            rid='OP-WG0P4-JOINT-RT-GIVEN-WG0P4-JOINT-ORD'
            rows=[replace(o,disposition=Disposition.PRODUCED,disposition_reason='QUALIFIED_TESTONLY_JOINT_RISK') if o.op_id==rid else o for o in rows]
        return rows

def joint_risk_authority():
    s=frozen('CONDITIONAL_FRONTIER.json')
    return {'kind':'TEST_ONLY_JOINT_ROUTING','frontier':frontier_root('conditional4'),'release':s['release'],'risk':s['risk_set'],'members':s['members'],'condition':s['condition'],'ceiling':'SOURCEFREE_NOT_REAL_ISSUER'}

COHORTS=base.COHORTS
EXPECTED_NATIVE_VALUES=base.EXPECTED_NATIVE_VALUES
EXPECTED_MR_PROFILES=base.EXPECTED_MR_PROFILES
EXPECTED_MR_INDICATOR_TOTALS=base.EXPECTED_MR_INDICATOR_TOTALS

def admit_native_rows(tag,questions,rows):
    try:
        base.admit_native_rows(tag,questions,rows)
        ids=[r['id'] for r in rows]
        if len(ids)!=len(set(ids)):raise NativeDataError('DUPLICATE_NATIVE_CARRIER')
    except (KeyError,ValueError,base.NativeDataError) as e:raise NativeDataError(str(e)) from e

def validate_mr_native_sets(tag,cohort):
    try:base.validate_mr_native_sets(tag,cohort)
    except base.NativeDataError as e:raise NativeDataError(str(e)) from e

def atomic_write(path,data):
    path=pathlib.Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp-'+secrets.token_hex(8))
    fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
    fd=os.open(path.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)

class FixtureOwner:
    """Separately provisioned, durable TEST_ONLY fixture grant/attestation owner.

    Files are outside untrusted checkpoint. Admin/host/key compromise is outside
    this local harness threat model. This is not deployed external source trust.
    """
    def __init__(self,directory):self.directory=pathlib.Path(directory)
    @classmethod
    def provision(cls,directory,cohorts):
        owner=cls(directory)
        if owner.directory.exists():raise IdentityError('REFUSE_OVERWRITE_EXISTING_FIXTURE_OWNER')
        owner.directory.mkdir(parents=True)
        atomic_write(owner.directory/'key.bin',secrets.token_bytes(32))
        state={'owner':'WG0P4_TESTONLY_FIXTURE_OWNER','epoch':secrets.token_hex(16),'version':1,'scope':'SOURCEFREE_ONLY','known_at':'2026-01-01','source_digests':{k:digest(v) for k,v in cohorts.items()},'grants':{'REL-A-W1':'GRANTED_FIXTURE','REL-A-W2':'GRANTED_FIXTURE','REL-B-W2':'WITHDRAWN'},'generation':0}
        atomic_write(owner.directory/'current.json',canonical(state))
        atomic_write(owner.directory/'issued.json',canonical({'facts':{},'receipts':{},'plans':{}}));return owner
    def state(self):
        d=json.loads((self.directory/'current.json').read_bytes())
        if d['owner']!='WG0P4_TESTONLY_FIXTURE_OWNER' or d['scope']!='SOURCEFREE_ONLY':raise RevocationError('UNTRUSTED_FIXTURE_OWNER')
        return d
    def revoke(self,tag):
        d=self.state()
        if tag not in d['grants']:raise RevocationError('UNKNOWN_RELEASE_NO_REVOCATION')
        d['grants'][tag]='WITHDRAWN';d['generation']+=1;atomic_write(self.directory/'current.json',canonical(d))
    def _sign(self,payload):return hmac.new((self.directory/'key.bin').read_bytes(),canonical(payload),hashlib.sha256).hexdigest()
    def verify(self,payload,signature):
        if not isinstance(signature,str) or not hmac.compare_digest(self._sign(payload),signature):raise ColdRestartError('UNTRUSTED_OR_SELF_REHASHED_CHECKPOINT')
    def _issued(self):return json.loads((self.directory/'issued.json').read_bytes())
    def _register_compiled_plan(self,plan):
        journal=self._issued()
        journal['plans'][hashlib.sha256(plan.contract).hexdigest()]={'source_material':hashlib.sha256(plan.source_material).hexdigest(),'owner_snapshot':hashlib.sha256(plan.owner_snapshot).hexdigest(),'science':plan.science_root}
        atomic_write(self.directory/'issued.json',canonical(journal))
    def assert_plan_issued(self,plan):
        expected={'source_material':hashlib.sha256(plan.source_material).hexdigest(),'owner_snapshot':hashlib.sha256(plan.owner_snapshot).hexdigest(),'science':plan.science_root}
        if self._issued()['plans'].get(hashlib.sha256(plan.contract).hexdigest())!=expected:raise IdentityError('PLAN_NOT_REGISTERED_BY_QUALIFIED_COMPILER')
    def assert_fact_issued(self,key,entry):
        if self._issued()['facts'].get(key)!=digest(entry):raise IdentityError('FACT_NOT_THE_NATIVE_ISSUED_RESULT')
    def assert_receipt_issued(self,receipt):
        if self._issued()['receipts'].get(receipt.receipt_hash)!=digest(receipt_to_json(receipt)):raise IdentityError('RECEIPT_NOT_ISSUED_BY_ACTUAL_NATIVE_BATCH_RUN')
    def compute_native(self,plan,spec,release):
        # Public computation API takes no caller-supplied fact or numeric answer.
        _check_plan(plan)
        result=execute_empirical_query(repository=release.repo,query=spec.query,predicate=spec.predicate,authority_registry=_registry_for(release),release_refs=(release.release_ref,))
        entries=[(f.ref,_plain(_fact_entry(spec.op_id,spec,f))) for f in result.facts]
        for f,e in entries:_validate_entry(f.key,e,plan)
        journal=self._issued()
        for f,e in entries:
            prior=journal['facts'].get(f.key)
            if prior is not None and prior!=digest(e):raise IdentityError('ISSUED_FACT_COLLISION')
            journal['facts'][f.key]=digest(e)
        atomic_write(self.directory/'issued.json',canonical(journal))
        return entries
    def _record_native_batch_receipts(self,receipts):
        journal=self._issued()
        for r in receipts:journal['receipts'][r.receipt_hash]=digest(receipt_to_json(r))
        atomic_write(self.directory/'issued.json',canonical(journal))
    def check_current(self,snapshot,tags):
        current=self.state()
        if current!=snapshot:raise RevocationError('FIXTURE_OWNER_EPOCH_VERSION_GRANT_OR_KNOWLEDGE_CLOCK_CHANGED')
        if any(current['grants'].get(tag)!=PERMITTED_GRANT for tag in tags):raise RevocationError('CURRENT_FIXTURE_GRANT_NOT_AVAILABLE')
        if current['source_digests']!={k:digest(v) for k,v in COHORTS.items()}:raise IdentityError('SOURCE_LEAF_CHANGED_SINCE_AUTHORIZED_SNAPSHOT')

class Releases(dict):pass

def build_all_releases(*,fixture_owner=None):
    for k,v in COHORTS.items():admit_native_rows(k,v['questions'],v['rows']);validate_mr_native_sets(k,v)
    if fixture_owner is None:
        # Explicit synthetic fixture bootstrap, not an original source grant.
        folder=R/'runtime'/('owner-'+secrets.token_hex(12))
        fixture_owner=FixtureOwner.provision(folder,COHORTS)
    if fixture_owner.state()['source_digests']!={k:digest(v) for k,v in COHORTS.items()}:raise IdentityError('OWNER_SOURCE_EDITION_MISMATCH')
    repo=C11Repository()
    out=Releases({tag:_ingest_native_fixture_release(tag,ns,repo=repo) for tag,ns in [('REL-A-W1','aw1'),('REL-A-W2','aw2'),('REL-B-W2','bw2')]});out.fixture_owner=fixture_owner
    return out

def _release_material(rel):
    actual=rel.repo.resolve_release_exact(rel.release_ref)
    universe=rel.repo.resolve_object_exact(rel.universe_ref)
    return {'tag':rel.release_tag,'release':rel.release_ref.as_dict(),'universe':rel.universe_ref.as_dict(),'wave':universe.raw_wave,'edition':rel.source_edition,'source_artifact':actual.source_artifact_ref.as_dict(),'qrefs':{k:v.as_dict() for k,v in rel.qrefs.items()},'risk_refs':{k:v.as_dict() for k,v in rel.risk_refs.items()},'authority_refs':[a.authority_ref.as_dict() for a in (*rel.authorities,rel.qauth)],'records_hash':digest([o.semantic_projection() for o in (*actual.public_objects,*actual.internal_records)])}

def _item_ref(item):return ExactRef('WG0P4_NATIVE_ITEM','urn:wg0p4:test:native:'+item.item_id,digest(vars(item)))

def _descriptor(item):
    # Source is chosen by qualified source-native tuple, never by nominal op_id.
    key=(item.source_id,item.wave,item.form_id,item.unit,item.response_kind,item.version)
    table={('WG0P-SRC-A','W1','Q-ORD-A','respondent','ORDINAL','v1'):('REL-A-W1','R_ORD',(('Q-ORD-A',('0','1','2','3','9')),)),('WG0P-SRC-A','W2','Q-ORD-A','respondent','ORDINAL','v1'):('REL-A-W2','R_ORD2',(('Q-ORD-A',('0','1','2','3','9')),)),('WG0P-SRC-B','W2','Q-ORD-A','respondent','ORDINAL','v1'):('REL-B-W2','R_ORDB',(('Q-ORD-A',('0','1','2','3','9')),)),('WG0P-SRC-A','W1','Q-RT-C','respondent','ROUTED','v1'):('REL-A-W1','R_RT',(('Q-RT-C',('yes','no')),)),('WG0P-SRC-A','W1','Q-HH-MR-B','household','MULTIPLE_RESPONSE','v1'):('REL-A-W1','R_HH',tuple((q,('yes','no')) for q in ('Q-HH-food','Q-HH-rent','Q-HH-health','Q-HH-edu','Q-HH-none')))}
    if key not in table:raise IdentityError('UNQUALIFIED_NATIVE_SOURCE_TUPLE')
    return table[key]

_branch_predicate_for=base._branch_predicate_for
_response_predicate_for=base._response_predicate_for
_registry_for=base._registry_for

def _query_for(release,predicate,targets,*,risk,tag):
    q=base._query_for(release,predicate,targets,risk=risk,tag=tag)
    fields=_plain(q.semantic_fields)
    for component in fields['target_arity_and_topology']['components']:component['included_states']=['SUBSTANTIVE_RESPONSE']
    return EmpiricalQuerySpec(typed_state=q.typed_state,authority_snapshot_refs=q.authority_snapshot_refs,dependency_refs=q.dependency_refs,producer_replay_locator_or_reference_root=q.producer_replay_locator_or_reference_root,**fields)

@dataclass(frozen=True)
class BoundSpec:
    op_id:str;release_tag:str;risk_name:str;targets:tuple;member_ids:tuple;grant:str;disposition:Disposition;native_item_ids:tuple;source_edition:str;full_identity_hash:str;query:Any;predicate:Any

class FactCustody:
    """Canonical bytes, detached exports and immediate atomic restore validation."""
    def __init__(self):self.__bytes={}
    @property
    def _facts(self):return MappingProxyType({k:json.loads(v) for k,v in self.__bytes.items()})
    def store(self,key,data):
        b=canonical(data)
        if key in self.__bytes and self.__bytes[key]!=b:raise IdentityError('EXACT_FACT_KEY_COLLISION')
        self.__bytes[key]=b
    def read(self,key):return json.loads(self.__bytes[key])
    def has(self,key):return key in self.__bytes
    def snapshot(self):
        facts={k:json.loads(v) for k,v in self.__bytes.items()}
        return {'facts':facts,'hashes':{k:hashlib.sha256(v).hexdigest() for k,v in self.__bytes.items()}}
    def restore(self,snapshot):
        if set(snapshot)!={'facts','hashes'} or set(snapshot['facts'])!=set(snapshot['hashes']):raise IdentityError('FACT_SNAPSHOT_CLOSED_KEYSET')
        prepared={k:canonical(v) for k,v in snapshot['facts'].items()}
        if any(hashlib.sha256(v).hexdigest()!=snapshot['hashes'][k] for k,v in prepared.items()):raise IdentityError('FACT_SNAPSHOT_HASH_MISMATCH')
        if any(k in self.__bytes and self.__bytes[k]!=v for k,v in prepared.items()):raise IdentityError('RESTORE_CONFLICTING_FACT_KEY')
        self.__bytes.update(prepared)

@dataclass(frozen=True)
class ExecutablePlan:
    manifest:Any;units_by_op:Any;op_specs:Any;releases:Any;release_refs:Any;repository:Any;frontier_receipts:tuple;source_issuer_grant:dict;freeze_hash:str;frontier_mode:str;science_root:str;fixture_owner:Any;owner_snapshot:bytes;source_material:bytes;contract:bytes
    fact_custody:FactCustody=field(default_factory=FactCustody)
    prior_receipts:tuple=()
    @property
    def expected_frontier_counts(self):return dict(Counter(x['disposition'] for x in self.frontier_receipts))


def build_executable_plan(ops,releases,*,freeze_hash,items_by_id):
    rows=[receipt_row(o) for o in ops];mode=_mode(rows);validate_frontier(ops,mode=mode)
    expected=frozen('ORIGINAL_FRONTIER.json' if mode=='original25' else 'CONDITIONAL_FRONTIER.json')['native_items']
    actual=sorted([_plain(vars(i)) for i in items_by_id.values()],key=lambda d:d['item_id'])
    if actual!=sorted(expected,key=lambda d:d['item_id']):raise IdentityError('NATIVE_ITEM_METADATA_NOT_QUALIFIED; HOLD_ALTERNATE_TUPLE')
    b=WorkloadBuilder()
    for it in items_by_id.values():
        if b.add_item(it)!='OK':raise IdentityError('DUPLICATE_NATIVE_CARRIER')
    if mode=='conditional4':b.add_joint_risk_authority(joint_risk_authority())
    if freeze_hash!=b.freeze():raise IdentityError('BUILDER_FREEZE_DOES_NOT_BIND_NATIVE_ITEMS_AND_JOINT_AUTHORITY')
    owner=getattr(releases,'fixture_owner',None)
    if not isinstance(owner,FixtureOwner):raise IdentityError('INDEPENDENT_TESTONLY_FIXTURE_OWNER_REQUIRED')
    snapshot=owner.state();owner.check_current(snapshot,[])
    science=frontier_root(mode);rootref=ExactRef('WG0P4_SCIENTIFIC_FRONTIER','urn:wg0p4:frontier:'+mode,science)
    units={};specs={}
    for o in sorted(ops,key=lambda x:x.op_id):
        if o.disposition!=Disposition.PRODUCED:continue
        item=items_by_id[o.target];tag,risk,targets=_descriptor(item);release=releases[tag]
        if o.op_class=='CONDITIONAL':
            cj=joint_risk_authority();cond=items_by_id[o.conditioners[0]]
            if mode!='conditional4' or _descriptor(cond)[0]!=tag:raise IdentityError('UNQUALIFIED_JOINT_SOURCE_OR_CARRIER')
            risk=cj['risk'];pred=_response_predicate_for(release,cj['condition']['form'],cj['condition']['value'],risk_name=risk,tag=o.op_id)
        else:
            members=tuple(sorted(set.intersection(*(set(COHORTS[tag]['risk_sets'][risk][q]) for q,_ in targets))))
            pred=_branch_predicate_for(release,members,tag=o.op_id,risk_name=risk)
        query=_query_for(release,pred,targets,risk=risk,tag=o.op_id)
        for q,domain in targets:
            if COHORTS[tag]['questions'][q]['domain']!=list(domain):raise IdentityError('NATIVE_DOMAIN_QUERY_MISMATCH')
        spec=BoundSpec(o.op_id,tag,risk,targets,tuple(sorted(COHORTS[tag]['risk_sets'][risk][targets[0][0]])),item.grant,o.disposition,o.item_ids,release.source_edition,digest(receipt_row(o)),query,pred)
        unit=BatchUnitSpec(job_kind='QUERY',job_ref=query.ref,release_refs=(release.release_ref,),semantic_input_refs=(*[_item_ref(items_by_id[i]) for i in o.item_ids],pred.ref,query.ref,rootref))
        units[o.op_id]=unit;specs[o.op_id]=spec
    manifest=BatchManifest(tuple(units.values()));repo=next(iter(releases.values())).repo
    if any(r.repo is not repo for r in releases.values()):raise IdentityError('RELEASES_NOT_ONE_ACCEPTED_REPOSITORY')
    source={k:_release_material(v) for k,v in releases.items()}
    contract={'manifest':manifest.semantic_projection(),'science':science,'freeze':freeze_hash,'bindings':{k:dict(unit=u.semantic_projection(),query=specs[k].query.semantic_projection(),predicate=specs[k].predicate.semantic_projection()) for k,u in units.items()}}
    plan=ExecutablePlan(manifest,MappingProxyType(units),MappingProxyType(specs),MappingProxyType(dict(releases)),MappingProxyType({k:r.release_ref for k,r in releases.items()}),repo,tuple(expected_rows(mode)),{'grant':PERMITTED_GRANT,'scope':'TEST_ONLY_HINT_CANNOT_ISSUE_PERMISSION'},freeze_hash,mode,science,owner,canonical(snapshot),canonical(source),canonical(contract))
    owner._register_compiled_plan(plan)
    return plan

def _check_plan(plan):
    plan.fixture_owner.assert_plan_issued(plan)
    validate_frontier_receipts(plan.frontier_receipts,mode=plan.frontier_mode)
    if plan.science_root!=frontier_root(plan.frontier_mode):raise FrontierError('STALE_OR_ALTERED_EXTERNAL_FRONTIER')
    if plan.source_issuer_grant!={'grant':PERMITTED_GRANT,'scope':'TEST_ONLY_HINT_CANNOT_ISSUE_PERMISSION'}:raise RevocationError('CALLER_GRANT_HINT_MUTATED; NOT_AUTHORITY')
    plan.fixture_owner.check_current(json.loads(plan.owner_snapshot),[s.release_tag for s in plan.op_specs.values()])
    if canonical({k:_release_material(r) for k,r in plan.releases.items()})!=plan.source_material:raise IdentityError('SOURCE_C11_READSET_CHANGED')
    contract={'manifest':plan.manifest.semantic_projection(),'science':plan.science_root,'freeze':plan.freeze_hash,'bindings':{k:dict(unit=u.semantic_projection(),query=plan.op_specs[k].query.semantic_projection(),predicate=plan.op_specs[k].predicate.semantic_projection()) for k,u in plan.units_by_op.items()}}
    if canonical(contract)!=plan.contract:raise IdentityError('UNIT_QUERY_PREDICATE_OR_SOURCE_BINDING_CHANGED')

def _fact_entry(op,spec,fact):
    return {'op_id':op,'fact_ref':fact.ref.as_dict(),'typed_state':fact.typed_state,'denominator':fact.raw_denominator_support,'cells':[{'cell':c['cell'],'n':c['raw_numerator_support'],'state':c['cell_state']} for c in fact.target_topology['complete_cell_semantic_projection']],'source_edition':spec.source_edition,'native_item_ids':list(spec.native_item_ids),'full_identity_hash':spec.full_identity_hash,'native_fact':fact.semantic_projection(),'query_ref':spec.query.ref.as_dict(),'predicate_ref':spec.predicate.ref.as_dict()}

def _validate_entry(key,entry,plan):
    try:
        projection=entry['native_fact'];f=EmpiricalFact(**{k:v for k,v in projection.items() if k!='semantic_fields'},**projection['semantic_fields'])
        s=plan.op_specs[entry['op_id']]
        if f.ref.key!=key or entry!=_plain(_fact_entry(entry['op_id'],s,f)):raise IdentityError('FACT_NATIVE_REF_OR_VALUE_READSET_MISMATCH')
        if entry['query_ref']!=s.query.ref.as_dict() or entry['predicate_ref']!=s.predicate.ref.as_dict():raise IdentityError('FACT_QUERY_PREDICATE_MISMATCH')
        # Genuine fact projection, not a caller-side count object.
        if f.condition_predicate_ref!=s.predicate.ref.as_dict() and _plain(f.condition_predicate_ref)!=s.predicate.ref.as_dict():raise IdentityError('NATIVE_FACT_CONDITION_MISMATCH')
        release=plan.releases[s.release_tag]
        if _plain(f.empirical_query_spec_ref)!=s.query.ref.as_dict() or _plain(f.risk_set_ref)!=release.risk_refs[s.risk_name].as_dict() or _plain(f.empirical_universe_refs)!=[release.universe_ref.as_dict()]:raise IdentityError('NATIVE_QUERY_RISK_UNIVERSE_READSET_MISMATCH')
        return f
    except (KeyError,TypeError,AttributeError,ValueError) as e:raise IdentityError('INVALID_NATIVE_FACT_PAYLOAD:'+str(e)) from e

def make_executor(plan):
    def execute(unit):
        _check_plan(plan)
        match=[k for k,u in plan.units_by_op.items() if u.job_ref==unit.job_ref]
        if len(match)!=1:raise KeyError('UNKNOWN_EXACT_JOB_REF_NO_FALLBACK')
        op=match[0];expected=plan.units_by_op[op];spec=plan.op_specs[op]
        if unit!=expected:raise IdentityError('ALL_UNIT_JOB_RELEASE_SEMANTIC_REFS_MUST_MATCH')
        release=plan.releases[spec.release_tag]
        prepared=plan.fixture_owner.compute_native(plan,spec,release)
        # No partially stored product on validation failure.
        trial=FactCustody();trial.restore(plan.fact_custody.snapshot())
        for f,e in prepared:trial.store(f.key,e)
        plan.fact_custody.restore(trial.snapshot())
        return ExecutionOutcome(result_refs=tuple(f for f,e in prepared),provenance_refs=(spec.query.ref,spec.predicate.ref))
    return execute

EXECUTOR_REF=_ref('EXECUTOR','WG0P4_QUERY_V1')
def run_plan(plan,executor,max_units=None):
    _check_plan(plan)
    runner=BatchExecutionRunner(manifest=plan.manifest,repository=plan.repository,prior_receipts=plan.prior_receipts)
    runner.run(executors={'QUERY':ExecutorBinding(EXECUTOR_REF,executor)},max_units=max_units)
    _validate_receipts(plan,runner.receipts,require_owner_receipt=False)
    plan.fixture_owner._record_native_batch_receipts(runner.receipts)
    object.__setattr__(plan,'prior_receipts',runner.receipts)
    return runner,runner.receipts

def _validate_receipts(plan,receipts,*,require_owner_receipt=True):
    runner=BatchExecutionRunner(manifest=plan.manifest,repository=plan.repository,prior_receipts=receipts)
    by_unit={u.unit_ref.key:op for op,u in plan.units_by_op.items()}
    for r in runner.receipts:
        if require_owner_receipt:plan.fixture_owner.assert_receipt_issued(r)
        if r.state!='COMPLETED':continue
        op=by_unit[r.unit_ref.key];s=plan.op_specs[op]
        if r.executor_ref!=EXECUTOR_REF or len(r.result_refs)!=1:raise IdentityError('FOREIGN_EXECUTOR_OR_WRONG_RESULT_CARDINALITY')
        for f in r.result_refs:
            entry=plan.fact_custody.read(f.key);_validate_entry(f.key,entry,plan);plan.fixture_owner.assert_fact_issued(f.key,entry)
            if entry['op_id']!=op:raise IdentityError('RESULT_REF_NOT_BOUND_TO_THIS_UNIT')
            if s.query.ref not in r.provenance_refs or s.predicate.ref not in r.provenance_refs:raise IdentityError('RECEIPT_QUERY_PREDICATE_READSET_CHANGED')
    return runner

def consumer_effects(plan,receipts):
    _check_plan(plan);runner=_validate_receipts(plan,receipts);effects={}
    for r in runner.receipts:
        if r.state!='COMPLETED':continue
        for f in r.result_refs:
            e=plan.fact_custody.read(f.key);effects.setdefault(e['op_id'],[]).append(e)
    return effects

@dataclass
class ColdCheckpoint:
    plan_freeze_hash:str;completed_units:dict;fact_custody_snapshot:dict;source_editions:dict;grant_state:str
    prior_receipts:tuple=();manifest_hash:str='';science_root:str='';source_material:str='';owner_snapshot:dict=field(default_factory=dict);signature:str='';checkpoint_hash:str=''
    def payload(self):
        return _plain({k:v for k,v in vars(self).items() if k not in ('signature','checkpoint_hash')})
    def __post_init__(self):self.checkpoint_hash=digest(self.payload())
    def to_json(self):return json.dumps({**self.payload(),'signature':self.signature,'checkpoint_hash':digest(self.payload())},sort_keys=True)
    @classmethod
    def from_json(cls,text,*,fixture_owner=None):
        try:
            d=json.loads(text);sig=d.pop('signature');h=d.pop('checkpoint_hash')
            if d['grant_state']!=PERMITTED_GRANT:raise ColdRestartError('CALLER_CANNOT_UPGRADE_FIXTURE_PERMISSION')
            if digest(d)!=h:raise ColdRestartError('CHECKPOINT_PREIMAGE_HASH_MISMATCH')
            custody=FactCustody();custody.restore(d['fact_custody_snapshot'])
            cp=cls(**d,signature=sig)
            if fixture_owner is not None:fixture_owner.verify(cp.payload(),sig)
            return cp
        except (ValueError,KeyError,TypeError) as e:raise ColdRestartError(str(e)) from e

def receipt_to_json(r):return {**r.projection(),'receipt_hash':r.receipt_hash,'receipt_ref':r.receipt_ref.as_dict()}
def receipt_from_json(d):
    d=copy.deepcopy(d);h=d.pop('receipt_hash');rr=ref(d.pop('receipt_ref'))
    for k in ['unit_ref','executor_ref']:
        if d[k] is not None:d[k]=ref(d[k])
    for k in ['result_refs','provenance_refs']:d[k]=tuple(ref(v) for v in d[k])
    r=UnitExecutionReceipt(**d)
    if r.receipt_hash!=h or r.receipt_ref!=rr:raise ColdRestartError('ORIGINAL_UNIT_RECEIPT_PREIMAGE_CHANGED')
    return r

def create_checkpoint(plan,receipts,completed_op_ids=None):
    _check_plan(plan);runner=_validate_receipts(plan,receipts)
    keys={f.key for r in runner.receipts if r.state=='COMPLETED' for f in r.result_refs}
    snapshot=plan.fact_custody.snapshot();snapshot={part:{k:v for k,v in values.items() if k in keys} for part,values in snapshot.items()}
    cp=ColdCheckpoint(plan.freeze_hash,{r.unit_ref.key:r.receipt_hash for r in runner.receipts if r.state=='COMPLETED'},snapshot,{k:r.source_edition for k,r in plan.releases.items()},PERMITTED_GRANT,tuple(receipt_to_json(r) for r in runner.receipts),plan.manifest.manifest_hash,plan.science_root,plan.source_material.decode(),json.loads(plan.owner_snapshot))
    cp.signature=plan.fixture_owner._sign(cp.payload());return cp

def restore_from_checkpoint(checkpoint,plan):
    _check_plan(plan);plan.fixture_owner.verify(checkpoint.payload(),checkpoint.signature)
    if checkpoint.grant_state!=PERMITTED_GRANT or checkpoint.plan_freeze_hash!=plan.freeze_hash or checkpoint.manifest_hash!=plan.manifest.manifest_hash or checkpoint.science_root!=plan.science_root or checkpoint.source_material!=plan.source_material.decode() or canonical(checkpoint.owner_snapshot)!=plan.owner_snapshot or checkpoint.source_editions!={k:r.source_edition for k,r in plan.releases.items()}:raise ColdRestartError('CURRENT_SOURCE_FRONTIER_MANIFEST_PERMISSION_OR_KNOWLEDGE_IDENTITY_CHANGED')
    prior=tuple(receipt_from_json(d) for d in checkpoint.prior_receipts)
    if checkpoint.completed_units!={r.unit_ref.key:r.receipt_hash for r in prior if r.state=='COMPLETED'}:raise ColdRestartError('COMPLETED_UNITS_DO_NOT_BIND_ACTUAL_RECEIPTS')
    required={f.key for r in prior if r.state=='COMPLETED' for f in r.result_refs}
    if set(checkpoint.fact_custody_snapshot['facts'])!=required:raise ColdRestartError('MISSING_OR_EXTRA_PRIOR_FACT_PAYLOAD')
    # Prepare a separate view; only commit custody + receipt update after every check.
    custody=FactCustody();custody.restore(plan.fact_custody.snapshot());custody.restore(checkpoint.fact_custody_snapshot)
    probe=replace(plan,fact_custody=custody)
    _validate_receipts(probe,prior)
    existing={r.receipt_hash:r for r in plan.prior_receipts};existing.update({r.receipt_hash:r for r in prior})
    merged=tuple(sorted(existing.values(),key=lambda r:(r.unit_ref.key,r.attempt_index)))
    _validate_receipts(probe,merged)
    plan.fact_custody.restore(custody.snapshot());object.__setattr__(plan,'prior_receipts',merged)

def resume_plan(plan,checkpoint,executor):
    restore_from_checkpoint(checkpoint,plan)
    already=len(plan.prior_receipts);runner,receipts=run_plan(plan,executor)
    return {'checkpoint_hash':checkpoint.checkpoint_hash,'restored_facts':len(checkpoint.fact_custody_snapshot['facts']),'remaining_units':len(receipts)-already,'resumed_receipts':len(receipts)-already,'receipts':receipts,'summary':runner.summary(),'consumer':consumer_effects(plan,receipts)}

def build_positive_conditional_frontier(releases):
    b=WorkloadBuilder();items=conditional_items()
    for i in items:b.add_item(i)
    b.add_joint_risk_authority(joint_risk_authority());f=b.freeze()
    return build_executable_plan(b.enumerate(),releases,freeze_hash=f,items_by_id={i.item_id:i for i in items})

def execute_positive_conditional(releases):
    # Compatibility convenience only: it delegates to the same ordinary chain.
    p=build_positive_conditional_frontier(releases);runner,rs=run_plan(p,make_executor(p));e=consumer_effects(p,rs)
    return {'plan':p,'receipts':rs,'effects':e,'summary':runner.summary()}


# WG0P4-owned fixture ingest: derived P3 producer, MISSING replaces invalid MISSING_CODE.
# Actual C11/I02 classes/functions below are unchanged pinned owners.
def _ingest_native_fixture_release(release_tag: str, question_namespace: str, repo: Any=None) -> base.IngestedRelease:
    """Real I02 issuance path with full identity binding."""
    cohort = COHORTS[release_tag]
    questions = cohort['questions']
    rows = cohort['rows']
    admit_native_rows(release_tag, questions, rows)
    validate_mr_native_sets(release_tag, cohort)
    expected_wave = 'W1' if 'W1' in release_tag else 'W2'
    source_edition = f'SRC-EDITION-{release_tag}-{expected_wave}-v1'
    source_auth = base._auth(f'source-{release_tag}', 'SOURCE_SEMANTICS_TOPOLOGY', families=('EmpiricalUniverse@1.0.0', 'RespondentEvent@1.0.0'))
    routing_auth = base._auth(f'routing-{release_tag}', 'ROUTING_RISK_SET', families=('RoutingEligibilityFact@1.0.0',))
    coord_auth = base._auth(f'coord-{release_tag}', 'COORDINATE_SEMANTICS', families=('EmpiricalCoordinateFact@1.0.0',))
    replay_auth = base._auth(f'replay-{release_tag}', 'REPLAY_PROTOCOL', families=('ReplayReceipt@1.0.0',))
    authorities = (source_auth, routing_auth, coord_auth, replay_auth)
    source_bytes_hash = base._h(f'source-bytes:{release_tag}:{json.dumps(rows, sort_keys=True)}')
    universe = base.EmpiricalUniverse(typed_state='UNIVERSE_IDENTIFIED', authority_snapshot_refs=(source_auth.authority_ref,), dependency_refs=(), producer_replay_locator_or_reference_root=base._ref('REPLAY_ROOT', f'universe-{release_tag}'), raw_source_identity=f'RAW-WG0P3-{release_tag}', source_family='SURVEY', study_product_release=f'STUDY-WG0P3-{release_tag}/REL-1', instrument_release=f'INST-WG0P3-{release_tag}', country_geography='US', sampling_geography='US-NATIONAL', raw_wave=expected_wave, canonical_wave_if_governed=None, field_or_reference_time='2026-01', target_population_and_sample_frame='ADULTS', sampling_design_regime='DESIGN-I03', respondent_namespace=f'NS-WG0P3-{release_tag}', source_artifact_import_lineage=f'SOURCE-LINEAGE-WG0P3-{release_tag}', harmonization_authority_ref=None, source_relation_refs=())
    question_names = sorted(questions)
    qrefs = {q: base._ref('QUESTION_NATIVE', f'{question_namespace}-{q}') for q in question_names}
    questions_objs = tuple((base.QuestionVariableBinding(empirical_universe_ref=universe.ref, native_question_ref=qrefs[q], instrument_question_version='1', canonical_question_ref_or_typed_absence=base.TypedAbsence('NOT_AUTHORIZED'), component_subitem_ref_or_typed_absence=base.TypedAbsence('NOT_APPLICABLE'), semantic_authority_ref=source_auth.authority_ref, topology_authority_ref=source_auth.authority_ref) for q in question_names))
    respondents = []
    respondent_by_id = {}
    respondent_keys: dict[str, Any] = {}
    for row in rows:
        respondent = base.RespondentIdentity(empirical_universe_ref=universe.ref, respondent_key=row['id'], source_native_respondent_key_ref_or_typed_absence=base._ref('SOURCE_RESPONDENT', f"{release_tag}-{row['id']}"), identity_map_authority_ref_or_typed_absence=base.TypedAbsence('NOT_APPLICABLE'))
        respondents.append(respondent)
        respondent_by_id[row['id']] = respondent
        respondent_keys[row['id']] = respondent.ref
    risk_sets = cohort['risk_sets']
    routing = []
    for risk_name, per_question in sorted(risk_sets.items()):
        risk_ref = base._ref('RISK_SET', f'{release_tag}-{risk_name}')
        for row in rows:
            respondent = respondent_by_id[row['id']]
            for q in question_names:
                members = per_question.get(q, set())
                state = 'ELIGIBLE_APPLICABLE' if row['id'] in members else 'NOT_ELIGIBLE'
                routing.append(base.RoutingEligibilityFact(typed_state=state, authority_snapshot_refs=(routing_auth.authority_ref,), dependency_refs=(), producer_replay_locator_or_reference_root=base._ref('REPLAY_ROOT', f"routing-{release_tag}-{risk_name}-{row['id']}-{q}"), empirical_universe_ref=universe.ref, scoped_respondent_ref=respondent.ref, question_or_target_ref=qrefs[q], risk_set_ref=risk_ref, routing_rule_ref=base._ref('ROUTING_RULE', f'{release_tag}-{risk_name}-{q}'), applicability_state=state, routing_state=state, parent_predicate_refs=(), member_set_replay_ref=base._ref('MEMBER_SET', f"{release_tag}-{risk_name}-{q}-{'-'.join(sorted(members)) or 'EMPTY'}")))
    events = []
    for row in rows:
        respondent = respondent_by_id[row['id']]
        for q, value in sorted(row.get('responses', {}).items()):
            topology_kind = questions[q]['topology']
            response_state = 'SUBSTANTIVE_RESPONSE'
            if value in ('9', '997', '998'):
                response_state = 'MISSING'
            events.append(base.RespondentEvent(typed_state=response_state, authority_snapshot_refs=(source_auth.authority_ref,), dependency_refs=(), producer_replay_locator_or_reference_root=base._ref('REPLAY_ROOT', f"event-{release_tag}-{row['id']}-{q}"), empirical_universe_ref=universe.ref, scoped_respondent_ref=respondent.ref, native_question_ref=qrefs[q], canonical_question_ref_if_authorized=None, component_or_subitem_ref=None, event_group_id=f"GROUP-{release_tag}-{row['id']}-{q}", response_event_id_or_deterministic_index=f"{row['id']}-{q}", raw_response_value=str(value), canonical_response_value_if_authorized=None, value_transform_authority_ref=None, response_topology_ref=base._ref('TOPOLOGY', f'{question_namespace}-{q}-{topology_kind}'), multiplicity_order_rank_fields={'kind': topology_kind, 'index': 0}, response_state=response_state))
    coordinates = []
    for row in rows:
        respondent = respondent_by_id[row['id']]
        coordinates.append(base.EmpiricalCoordinateFact(typed_state='OBSERVED_COORDINATE', authority_snapshot_refs=(coord_auth.authority_ref,), dependency_refs=(), producer_replay_locator_or_reference_root=base._ref('REPLAY_ROOT', f"coord-{release_tag}-{row['id']}-INERT"), empirical_universe_ref=universe.ref, scoped_respondent_ref=respondent.ref, native_coordinate_ref=base._ref('COORDINATE_NATIVE', f'{question_namespace}-INERT'), canonical_coordinate_ref_if_authorized=None, raw_coordinate_value='1', canonical_coordinate_value_if_authorized=None, unit_category_taxonomy_ref=base._ref('UNIT_TAXONOMY', f'{question_namespace}-INERT'), effective_or_reference_time='2026-01', coordinate_state='OBSERVED_COORDINATE', normalization_crosswalk_authority_ref=None, source_semantic_authority_ref=coord_auth.authority_ref))
    counts = {'EmpiricalUniverse': 1, 'RespondentIdentity': len(respondents), 'QuestionVariableBinding': len(questions_objs), 'RespondentEvent': len(events), 'RoutingEligibilityFact': len(routing), 'EmpiricalCoordinateFact': len(coordinates), 'WeightMeasureFact': 0, 'AuthoritySnapshot': len(authorities), 'SourceUniverseRelation': 0, 'EmpiricalPredicateReplayBinding': 0, 'ComparatorReplayBinding': 0, 'DiscoveryBranchReplayBinding': 0, 'StructuralAdmissionReplayBinding': 0, 'ReplayManifest': 1}
    manifest = base.SourceReleaseManifest(source_artifact_id=f'SOURCE-WG0P3-{release_tag}', source_artifact_content_hash=source_bytes_hash, source_family_id='SURVEY', study_product_id=f'STUDY-WG0P3-{release_tag}', release_id=f'REL-{release_tag}', instrument_release_id=f'INST-WG0P3-{release_tag}', ingest_contract_version=base.INGEST_CONTRACT_VERSION, declared_universe_refs=(universe.ref,), declared_authority_snapshot_refs=tuple((a.authority_ref for a in authorities)), declared_record_counts_by_logical_family=counts, source_snapshot_retention_ref=ExactRef('SOURCE_SNAPSHOT', f'urn:wg0p3:test:source-snapshot:{release_tag}', source_bytes_hash))
    candidate = base.C11SourceReleaseCandidate(source_release_manifest=manifest, empirical_universes=(universe,), respondent_identities=tuple(respondents), question_variable_bindings=questions_objs, respondent_events=tuple(events), routing_eligibility_facts_or_exact_rules=tuple(routing), empirical_coordinate_facts=tuple(coordinates), weight_measure_facts_or_typed_absence=base.TypedAbsence('NOT_APPLICABLE'), authority_snapshots=authorities, source_universe_relations_or_explicit_distinct_default=base.TypedAbsence('DISTINCT_BY_DEFAULT'), predicate_replay_bindings_when_retained_objects_require_them=base.TypedAbsence('NOT_APPLICABLE'), comparator_replay_bindings_or_typed_deferred_state=base.TypedAbsence('DEFERRED'), discovery_branch_replay_bindings_or_typed_deferred_state=base.TypedAbsence('DEFERRED'), structural_admission_replay_bindings_or_typed_not_applicable_state=base.TypedAbsence('NOT_APPLICABLE'), candidate_replay_manifest=None)
    replay = base.build_candidate_replay_manifest(candidate, replay_protocol_authority_ref=replay_auth.authority_ref, deterministic_tie_order_rules_ref=base._ref('ORDER_RULE', 'CANONICAL-REF-SORT'), replay_protocol_version='1.0.0')
    candidate = replace(candidate, candidate_replay_manifest=replay)
    if repo is None:
        repo = C11Repository()
    result = base.ingest_c11_source_release(candidate, repo)
    if not result.accepted:
        raise RuntimeError(f'I02 ingest refused: {result.errors}')
    qauth = base._query_authority(f'wg0p3-{release_tag}')
    return base.IngestedRelease(release_tag=release_tag, repo=repo, release_ref=result.release_ref, respondent_keys=respondent_keys, universe_ref=universe.ref, qrefs=qrefs, risk_refs={name: base._ref('RISK_SET', f'{release_tag}-{name}') for name in risk_sets}, authorities=authorities, qauth=qauth, source_edition=source_edition, source_artifact_ref=manifest.source_snapshot_retention_ref)
