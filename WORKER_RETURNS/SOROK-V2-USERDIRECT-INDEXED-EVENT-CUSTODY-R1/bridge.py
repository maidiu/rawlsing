"""HQ325 B2 source-free bridge. Local witness allowlists are not production auth."""
from __future__ import annotations
from copy import deepcopy
from dataclasses import asdict, replace
import hashlib
import importlib.util
import json
import sqlite3
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent

def verify_import(path):
    relative=str(path.relative_to(ROOT))
    sources=json.loads((ROOT/'imported_sources.json').read_text())
    entry=next(row for row in sources if row['materialized_path']==relative)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']:
        raise RuntimeError('PINNED_SOURCE_INTEGRITY_FAILURE:'+relative)
    return entry['sha256']


def load(name,path):
    verify_import(path)
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

b1=load('b2_pinned_bfirst',ROOT/'imports/B1/bfirst.py')
p1=load('b2_pinned_p1',ROOT/'imports/P1/p1_contract.py')
RULE='B2_SYNTHETIC_WITNESSED_INGRESS@1'
ALIASES={'CHILD-1':'child','CARE-1':'caretaker','PEER-1':'peer'}
D1_SOURCE=ROOT/'imports/D1/07_CORRECTED_ABSENCE_CONTRACT_COURT.js'

def rehash(value,field):
    result=deepcopy(value);result.pop(field,None);result[field]=p1.digest(result);return result


def read_fixture(name):
    return json.loads((ROOT/'imports/P1/fixtures'/name).read_text())


def input_pair(state,number=1,alternative='ALT-CARE',other=None):
    """New B2 derivative fixture; never writes inherited P1 fixtures.

    Retain the full alternative set and append child's exact history prerequisite.
    Selection weights are a test coordinate policy, never psychological probabilities.
    """
    context=read_fixture('context_base.json');packet=read_fixture('packet_base.json')
    time=f'2026-10-{16+number:02d}T10:00:00Z'
    context['as_of']=time
    for opportunity in context['action_opportunities'].values(): opportunity['time']=time
    context['histories']['H-CHILD-1']['source']='B2_EXACT_SYNTHETIC_PREHISTORY'
    context['histories']['H-CHILD-1']['summary']='typed history digest '+b1.digest(state['history'])
    for ref in ('CARE-1','PEER-1'):
        person=(other or {}).get(ref,b1.participant(ALIASES[ref]))
        history=context['histories'][context['people'][ref]['history_ref']]
        history['source']='B2_INDEPENDENT_TYPED_PARTICIPANT'
        history['summary']='typed participant digest '+b1.digest(asdict(person))
    # Distinct already-generated history can make this derivative alternative ineligible.
    history_id=context['people']['CHILD-1']['history_ref']
    for c in packet['candidates']:
        c['time']=time
        c['prerequisites'].append(dict(kind='HISTORY_PRESENT',ref='CHILD-1|'+history_id))
    context=rehash(context,'context_hash')
    packet.update(as_of=time,context_hash=context['context_hash'],proposal_id='B2-PACKET-'+str(number))
    packet=rehash(packet,'proposal_hash')
    evaluation=p1.evaluate(packet,context)
    policy=read_fixture('policy_design_weights.json')
    policy['candidate_set_hash']=evaluation['candidate_set_hash']
    policy['policy_id']='B2-TEST-COORDINATE'
    policy['weight_units']={e['candidate_id']:int(e['candidate_id']==alternative) for e in evaluation['eligible_entries']}
    policy=rehash(policy,'policy_hash')
    return packet,context,policy


def capability_fixture(event_id='event1',time='2026-10-17',status='CAPABILITY_PRESENT'):
    witness=b1.sealed(dict(witness_id='comparison_task',actor='child',scope='garage',
        capability='C07',from_time='2026-01-01',until=None,outcome='OBSERVED_COMPARISON',
        evidence_grade='SYNTHETIC_WITNESSED_TASK',authority='B2_CAPABILITY_FIXTURE_AUTHORIZER'))
    packet=dict(actor=dict(id='child',phase='V3DP_DEVELOPMENT_ACTIVE',segments=[],
                access=[event_id],current_facts=[],capabilities=dict(C07=dict(actor='child',scope='garage',
                status=status,from_='2026-01-01',witness_refs=[witness['hash']]))),
        world=dict(events=[event_id],utterances=[],other_actors=['caretaker','peer'],witnesses=[witness['hash']],today=time),
        candidate=dict(event=event_id,scope='garage',capabilities=['C07'],required_access=[event_id],source_utterances=[]))
    packet['actor']['capabilities']['C07']['from']=packet['actor']['capabilities']['C07'].pop('from_')
    return packet,[witness]


def d1_gate(packet,registry):
    """Verify actual comparable witness records, then call the unchanged D1 judge in Node."""
    safe=deepcopy(packet);lookup={w['hash']:w for w in registry if b1.valid(w)}
    for cid in safe['candidate']['capabilities']:
        cap=safe['actor']['capabilities'].get(cid)
        if not cap or cap['status']=='CAPABILITY_UNKNOWN': continue
        refs=cap.get('witness_refs',[])+cap.get('counterevidence_refs',[])
        for ref in refs:
            w=lookup.get(ref)
            if not w or not (w['actor']==safe['actor']['id'] and w['scope']==safe['candidate']['scope']
                and w['capability']==cid and w['from_time']<=safe['world']['today']
                and (not w['until'] or safe['world']['today']<w['until'])):
                return dict(decision='REFUSED',code='INDEPENDENT_COMPARABLE_WITNESS_MISSING',mutations=0)
        if cap['status']=='CAPABILITY_ABSENT':
            if not cap.get('counterevidence_refs'):
                # The corrected D1 code, not a missing-data inference, decides this.
                pass
            elif any(lookup[r]['outcome']!='OBSERVED_INABILITY' for r in cap['counterevidence_refs']):
                return dict(decision='REFUSED',code='ABSENCE_COUNTERWITNESS_NOT_COMPARABLE',mutations=0)
        elif refs and any(lookup[r]['outcome']!='OBSERVED_COMPARISON' for r in cap.get('witness_refs',[])):
            return dict(decision='REFUSED',code='POSITIVE_WITNESS_NOT_COMPARABLE',mutations=0)
    expected_source=verify_import(D1_SOURCE)
    run=subprocess.run(['node',str(ROOT/'d1_gate.js'),str(D1_SOURCE)],input=json.dumps(safe),
                       text=True,capture_output=True,check=True)
    loaded=json.loads(run.stdout)
    if loaded['source_sha256']!=expected_source:raise RuntimeError('D1_IMPORTED_SOURCE_DIVERGENCE')
    return dict(loaded['result'],source_sha256=loaded['source_sha256'],frozen_self_tests=loaded['self_tests'])


def occurrence_witness(state,packet,context,alternative='ALT-CARE',number=1,
                       outcome='OCCURRED',other=None,observed=None):
    """Independent synthetic fixture author, outside model selection and response engine.

    Tests explicitly register this immutable observation. Merely rehashing or returning
    a P1 proposal cannot add it to the ingress allowlist.
    """
    candidate=next(c for c in packet['candidates'] if c['candidate_id']==alternative)
    people=[]
    for ref in candidate['participants']:
        if ref=='CHILD-1': continue
        person=(other or {}).get(ref,b1.participant(ALIASES[ref]))
        people.append(dict(p1_actor=ref,participant=asdict(person),
                           action=person.offer(),source_history_hash=b1.digest(asdict(person))))
    return b1.sealed(dict(schema='B2_INDEPENDENT_SYNTHETIC_OCCURRENCE_WITNESS@1',
        issuer='B2_WORLD_FIXTURE_AUTHORIZER',candidate_hash=p1.digest(candidate),
        proposal_hash=packet['proposal_hash'],context_hash=context['context_hash'],
        world_ref=context['world_ref'],parent_fact_hash=b1.digest(context['facts'][candidate['parent_event_ref']]),
        expected_actor_state_hash=b1.digest(state),number=number,event_id='event'+str(number),
        time=candidate['time'],place=candidate['place_ref'],participants=candidate['participants'],
        outcome=outcome,objective_occurrence='OBSERVED_INTERACTION_AFTER_MATERIAL_LOSS',
        project=state['project'],interrupted=number==1,other_actions=people,
        observed_interpretations=deepcopy(observed if observed is not None else
            json.loads((ROOT/'fixtures/independent_observations.json').read_text())['observations'][alternative]),
        world_facts=dict(known_thief=None,group_criminality='NOT_ESTABLISHED')))


class Bridge:
    def __init__(self,path,initial=None,witnesses=(),capability_witnesses=()):
        self.store=b1.Store(path,initial)
        self.witnesses={w['hash']:deepcopy(w) for w in witnesses if b1.valid(w)}
        self.capability_witnesses=deepcopy(capability_witnesses)
        # SQLite maintains this derived lookup for every writer, including B1.
        # One-time construction scans legacy rows; entry uses an indexed lookup.
        self.store.db.execute("CREATE INDEX IF NOT EXISTS b2_occurrence_event_id "
            "ON occurrence(json_extract(body, '$.event_id'))")
        self.store.db.execute('CREATE TABLE IF NOT EXISTS b2_ingress (id TEXT PRIMARY KEY, body TEXT)')
        # One global ID in this bounded registrar: actor/world/issuer are immutable
        # content, never additional namespace columns permitting ID reuse.
        self.store.db.execute('''CREATE TABLE IF NOT EXISTS b2_event_identity
            (event_id TEXT PRIMARY KEY NOT NULL, binding TEXT NOT NULL,
             event_ref TEXT NOT NULL, ingress_ref TEXT NOT NULL)''')

    def close(self):self.store.close()

    def advance(self,packet,context,policy,witness,capability,*,seed='0f'*32,coordinate=0,
                frozen_envelope=None,
                journal_only=False,grant=True,fault=None):
        # B1 uses autocommit admission but does not commit an enclosing transaction.
        # Hold the actual write lock through validation, prestate reconciliation,
        # occurrence + ingress + identity insertion. Response has its own B1 txn.
        try:
            self.store.db.execute('BEGIN IMMEDIATE')
            return self._advance(packet,context,policy,witness,capability,seed=seed,
                coordinate=coordinate,frozen_envelope=frozen_envelope,
                journal_only=journal_only,grant=grant,fault=fault)
        except sqlite3.Error:
            if self.store.db.in_transaction:self.store.db.execute('ROLLBACK')
            return b1.sealed(dict(schema='B2_VERTICAL_RECEIPT@1',rule=RULE,
                status='DENIED',reason='SYNTHETIC_INGRESS_STORAGE_FAILURE',
                event_admission='NOT_PERFORMED',b1_invoked=False,
                after_hash=b1.digest(self.store.state())))
        finally:
            if self.store.db.in_transaction:self.store.db.execute('ROLLBACK')

    def _advance(self,packet,context,policy,witness,capability,*,seed,coordinate,
                 frozen_envelope,journal_only,grant,fault):
        before=self.store.state();before_hash=b1.digest(before)
        evaluation=p1.evaluate(packet,context)
        selection=p1.select_test_only(evaluation,policy,seed_hex=seed,coordinate=coordinate)
        receipt=dict(schema='B2_VERTICAL_RECEIPT@1',rule=RULE,
            eligibility=evaluation,selection=selection,before_hash=before_hash,
            status='DEFERRED',event_admission='NOT_PERFORMED',b1_invoked=False)
        def stop(code,status='DENIED'):
            receipt.update(status=status,reason=code,after_hash=b1.digest(self.store.state()))
            return b1.sealed(receipt)
        if frozen_envelope is not None:
            from f1_boundary import envelope_gate
            gate=envelope_gate(frozen_envelope)
            if gate is not None:
                receipt['frozen_boundary_gate']=gate
                return stop('|'.join(gate['reasons']),gate['status'])
        if selection.get('selected_candidate_id') is None:
            status={'DEFER':'DEFERRED','REJECT':'DENIED','VALID_EMPTY':'VALID_EMPTY'}.get(selection.get('decision'),'DENIED')
            return stop(selection.get('reason','NO_ELIGIBLE_ALTERNATIVE'),status)
        candidate=next(c for c in packet['candidates'] if c['candidate_id']==selection['selected_candidate_id'])
        if not witness or not b1.valid(witness) or self.witnesses.get(witness['hash'])!=witness:
            return stop('INDEPENDENT_OCCURRENCE_WITNESS_REQUIRED')
        # Bind the complete witnessed payload and readset, including fields not
        # represented by B1.Event (wall clock, issuer, parent, attributed speech).
        # Capabilities/grants are downstream conditions and may be retried.
        binding=b1.canonical(dict(rule=RULE,actor='child',witness=witness,
            packet=packet,context=context,policy=policy,
            selected_candidate_id=candidate['candidate_id']))
        event_id=witness.get('event_id')
        if not isinstance(event_id,str) or not event_id:
            return stop('EVENT_ID_REQUIRED')
        identity=self.store.db.execute(
            'SELECT binding,event_ref,ingress_ref FROM b2_event_identity WHERE event_id=?',
            (event_id,)).fetchone()
        # Direct B1 writes can precede or follow this registrar's mapping. Recheck
        # the complete ID under the writer lock, including before replay returns.
        occurrences=self.store.db.execute(
            "SELECT hash,body FROM occurrence WHERE json_extract(body, '$.event_id')=? LIMIT 2",
            (event_id,)).fetchall()
        if identity is not None:
            if identity[0]!=binding:return stop('EVENT_IDENTITY_CONFLICT')
            if len(occurrences)!=1 or occurrences[0][0]!=identity[1]:
                return stop('EVENT_IDENTITY_LEDGER_INTEGRITY_FAILURE')
            event_row=self.store.db.execute('SELECT body FROM occurrence WHERE hash=?',(identity[1],)).fetchone()
            ingress_row=self.store.db.execute('SELECT body FROM b2_ingress WHERE id=?',(identity[2],)).fetchone()
            if (not event_row or not ingress_row
                or not b1.valid(json.loads(event_row[0]))
                or not b1.valid(json.loads(ingress_row[0]))
                or json.loads(event_row[0])['hash']!=identity[1]
                or json.loads(ingress_row[0])['hash']!=identity[2]
                or json.loads(event_row[0])['event_id']!=event_id
                or json.loads(ingress_row[0])['event_ref']!=identity[1]):
                return stop('EVENT_IDENTITY_LEDGER_INTEGRITY_FAILURE')
            if witness['expected_actor_state_hash']!=before_hash:
                # Re-admission is successful and inert even after later events.
                # Never re-run an old response against the new checkpoint.
                receipt.update(event_admission=json.loads(ingress_row[0]),
                    admitted_event=json.loads(event_row[0]),
                    admission_replay='EXACT_EVENT_ALREADY_ADMITTED',response_status='DENIED')
                # Retain the existing response stale-state reason; admission is
                # idempotent while response rebinding is still forbidden.
                return stop('WITNESS_BINDING_OR_STALE_STATE','ALREADY_ADMITTED')
        elif occurrences:
            # No retrospective provenance invention for old/direct B1 admissions.
            return stop('EVENT_IDENTITY_UNBOUND_LEGACY')
        child_history=context['histories'].get('H-CHILD-1',{})
        if (context['people']['CHILD-1']['history_ref']!='H-CHILD-1'
            or child_history.get('source')!='B2_EXACT_SYNTHETIC_PREHISTORY'
            or child_history.get('summary')!='typed history digest '+b1.digest(before['history'])):
            return stop('CONDITIONING_HISTORY_PROJECTION_MISMATCH')
        if (witness.get('schema')!='B2_INDEPENDENT_SYNTHETIC_OCCURRENCE_WITNESS@1'
            or witness.get('issuer')!='B2_WORLD_FIXTURE_AUTHORIZER'):
            return stop('WITNESS_SCHEMA_OR_ISSUER_INVALID')
        checks=(witness['candidate_hash']==p1.digest(candidate)
                and witness['proposal_hash']==packet['proposal_hash']
                and witness['context_hash']==context['context_hash']
                and witness['expected_actor_state_hash']==before_hash
                and witness['world_ref']==context['world_ref']
                and witness['time']==candidate['time'] and witness['place']==candidate['place_ref']
                and witness['participants']==candidate['participants']
                and witness['parent_fact_hash']==b1.digest(context['facts'][candidate['parent_event_ref']]))
        if not checks:return stop('WITNESS_BINDING_OR_STALE_STATE')
        if witness['world_facts'] != dict(known_thief=None,group_criminality='NOT_ESTABLISHED'):
            return stop('PEER_PREJUDICE_LAUNDERED_AS_FACT')
        if witness['outcome']=='DENIED':return stop('OBJECTIVE_EVENT_DENIED')
        if witness['outcome']=='NONOCCURRENCE':
            return stop('WITNESSED_NONOCCURRENCE','VALID_EMPTY')
        if witness['outcome']!='OCCURRED' or candidate['family']=='NONOCCURRENCE':
            return stop('SELECTION_WITNESS_CONTRADICTION')
        if 'CHILD-1' not in candidate['visibility']:return stop('CHILD_NOT_EXPOSED')
        if witness['observed_interpretations']!=candidate['interpretations']:
            return stop('UTTERANCE_NOT_INDEPENDENTLY_WITNESSED')
        offers=[]
        actors=[]
        for fact in witness['other_actions']:
            ref=fact['p1_actor']
            if ref not in candidate['participants'] or ref=='CHILD-1' or ref not in ALIASES:
                return stop('INDEPENDENT_ACTOR_ROLE_INVALID')
            person=fact['participant']
            agent=b1.Participant(person['actor_id'],person['project'],tuple(b1.HistoryEpisode(**h) for h in person['history']))
            if (agent.actor_id!=ALIASES[ref] or b1.digest(asdict(agent))!=fact['source_history_hash']
                or agent.offer()!=fact['action']):return stop('INDEPENDENT_ACTOR_ACTION_FORGED')
            if any(h.actor_id!=agent.actor_id or h.project!=agent.project for h in agent.history):
                return stop('INDEPENDENT_ACTOR_HISTORY_FORGED')
            history_projection=context['histories'][context['people'][ref]['history_ref']]
            if (history_projection.get('source')!='B2_INDEPENDENT_TYPED_PARTICIPANT'
                or history_projection.get('summary')!='typed participant digest '+fact['source_history_hash']):
                return stop('PARTICIPANT_HISTORY_PROJECTION_MISMATCH')
            role=context['people'][ref]['role']
            if role not in ('CAREGIVER','PEER'):return stop('INDEPENDENT_ACTOR_ROLE_INVALID')
            for i in candidate['interpretations']:
                if i['speaker_actor_ref']==ref:
                    offers.append((agent.actor_id,i['utterance'],fact['action']))
            actors.append(agent.actor_id)
        expected={ref for ref in candidate['participants'] if ref!='CHILD-1'}
        if {f['p1_actor'] for f in witness['other_actions']}!=expected:
            return stop('INDEPENDENT_PARTICIPANT_WITNESS_MISSING')
        event=b1.Event(witness['event_id'],'child',witness['number']+1,witness['world_ref'],
            witness['objective_occurrence'],witness['project'],tuple('relation:child:'+a for a in actors),
            'power:caretaker_controls_tools',tuple(offers),witness['interrupted'])
        # Occurrence admits independently of downstream response/capability or target permission.
        admitted=self.store.admit_fixture(event)
        ingress=b1.sealed(dict(rule=RULE,witness_ref=witness['hash'],event_ref=admitted['hash'],
            proposal_ref=packet['proposal_hash'],selected_candidate_id=candidate['candidate_id'],
            status='ADMITTED_SYNTHETIC_FIXTURE_ONLY',attributed_claims=candidate['interpretations'],
            objective_world_facts=witness['world_facts']))
        self.store.db.execute('INSERT OR IGNORE INTO b2_ingress VALUES (?,?)',(ingress['hash'],b1.canonical(ingress)))
        if identity is None:
            self.store.db.execute('INSERT INTO b2_event_identity VALUES (?,?,?,?)',
                (event_id,binding,admitted['hash'],ingress['hash']))
        elif identity[1:]!=(admitted['hash'],ingress['hash']):
            return stop('EVENT_IDENTITY_LEDGER_INTEGRITY_FAILURE')
        # This is the sole admission commit; downstream denials preserve it.
        self.store.db.execute('COMMIT')
        receipt.update(event_admission=ingress,admitted_event=admitted)
        cap=deepcopy(capability)
        # Reject caller trying to use capability context for a different event or actor.
        if (cap['actor']['id']!='child' or cap['candidate']['event']!=event.event_id
            or cap['candidate']['scope']!='garage' or cap['world']['today']!=witness['time'][:10]
            or cap['world']['events']!=[event.event_id]
            or cap['candidate']['capabilities']!=['C07']
            or cap['candidate']['required_access']!=[event.event_id]
            or cap['actor']['access']!=[event.event_id]
            or cap['candidate']['source_utterances'] or cap['world']['utterances']):
            return stop('CAPABILITY_EVENT_BINDING_INVALID')
        decision=d1_gate(cap,self.capability_witnesses);receipt['capability_decision']=decision
        if decision['decision']!='PROPOSABLE_ONLY':
            return stop(decision['code'],'DEFERRED' if decision['code'] in ('CAPABILITY_UNKNOWN','ABSENCE_EVIDENCE_MISSING') else 'DENIED')
        try:
            response=b1.propose(before,admitted)
        except b1.Refusal as exc:return stop(str(exc))
        permission=b1.TestOnlyCAN011Owner.permission(before,response)
        owner=b1.TestOnlyCAN011Owner([permission['hash']] if grant else [])
        joint=self.store.commit(admitted,response,owner,permission,journal_only=journal_only,fault=fault)
        receipt.update(b1_invoked=True,response=response,joint=joint,
            actor_safe=response['actor_surface'] if joint['status']=='COMMITTED' else
                       dict(actions=[],origin_explanation='NOT_ACCESSIBLE',status='RESPONSE_ABORTED'),
            after_hash=b1.digest(self.store.state()),
            status=joint['status'],permission=permission)
        return b1.sealed(receipt)


def run_two(directory,journal_only=False,history_outcome='recognized_plan'):
    path=Path(directory);path.mkdir(parents=True,exist_ok=True)
    db=path/'state.sqlite'
    if db.exists():db.unlink()
    initial=b1.initialize(b1.prehistory(history_outcome));history=[]
    bridge=Bridge(db,initial)
    for n in (1,2):
        packet,context,policy=input_pair(bridge.store.state(),n)
        witness=occurrence_witness(bridge.store.state(),packet,context,number=n)
        capability,registry=capability_fixture(witness['event_id'],witness['time'][:10])
        bridge.witnesses={witness['hash']:witness};bridge.capability_witnesses=registry
        receipt=bridge.advance(packet,context,policy,witness,capability,journal_only=journal_only)
        history.append(dict(packet=packet,context=context,policy=policy,witness=witness,
                            capability=capability,capability_registry=registry,receipt=receipt))
        bridge.close();bridge=Bridge(db) # durable checkpoint recruited through cold connection
    final=bridge.store.state();bridge.close()
    bundle=dict(initial=initial,episodes=history,final_hash=b1.digest(final),
                final_state=final,journal_only=journal_only)
    (path/'trace.json').write_text(json.dumps(bundle,indent=2)+'\n')
    return bundle


def replay(bundle,path):
    """Fresh process reconstruction of exact inputs and owner/witness registrations."""
    bridge=Bridge(path,bundle['initial']);receipts=[]
    for ep in bundle['episodes']:
        bridge.witnesses={ep['witness']['hash']:ep['witness']}
        bridge.capability_witnesses=ep['capability_registry']
        receipts.append(bridge.advance(ep['packet'],ep['context'],ep['policy'],ep['witness'],ep['capability'],
                                       journal_only=bundle['journal_only']))
    result=dict(receipts=receipts,final_hash=b1.digest(bridge.store.state()))
    bridge.close();return result


if __name__=='__main__':
    import tempfile
    if sys.argv[1]=='replay':
        bundle=json.loads(Path(sys.argv[2]).read_text())
        with tempfile.TemporaryDirectory() as directory:
            print(json.dumps(replay(bundle,Path(directory)/'replay.sqlite'),sort_keys=True))
    else:
        directory=Path(sys.argv[1])
        result={name:run_two(directory/name,journal) for name,journal in [('positive',False),('journal_only',True)]}
        print(json.dumps({k:dict(final_hash=v['final_hash'],later_actions=v['episodes'][1]['receipt']['response']['practical_activity']) for k,v in result.items()},sort_keys=True))
