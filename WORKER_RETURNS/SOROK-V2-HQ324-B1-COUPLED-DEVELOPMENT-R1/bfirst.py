"""Source-free B1 adapter v1; no production imports or semantic registry writes."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import sqlite3

GRADE = 'PROVISIONAL_MODEL_HYPOTHESIS'
SCHEMA = 'B1_CANDIDATE_ADAPTER@1.0.0'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def sealed(value):
    return dict(value, hash=digest(value))


def valid(value):
    return value.get('hash') == digest({k: v for k, v in value.items() if k != 'hash'})


# Content includes executable predicate specification; source hash also banked at return.
RESPONSE_RULE = sealed(dict(authority_id='TEST_ONLY_CAN008_B1', authority_version='1',
    rule_id='situated_plan_comparison', rule_version='1', grade=GRADE,
    predicates=['admitted fixture occurrence; actor can compare enacted plans',
                'interrupted active project; counterpart offers executable plan',
                'prior enacted counterpart recognition -> joint_check',
                'prior imposed counterpart plan -> private_check',
                'later offer recruits ACTIVE exact project/counterpart mediator only'],
    composition='independent source streams coexist; no scalar winner',
    effect_kind='TRANSFORM', numeric_policy='NONE', stochastic_policy='NO_DRAWS'))
UPDATE_RULE = sealed(dict(authority_id='TEST_ONLY_CAN011_B1', authority_version='1',
    rule_id='scoped_plan_mediator', rule_version='1', grade=GRADE,
    predicates=['CREATE only; exact actor/project/counterpart',
                'independently recheck interruption, offered plan and enacted history',
                'payload joint_check or private_check from matching history',
                'explicit TEST_ONLY owner grant; before hashes; causal parents'],
    state_kind_id='V3MS_MEDIATOR', role='REGULATORY_PROTECTIVE'))
REGISTRY = sealed(dict(registry_id='V3_DEVELOPMENTAL_MIDDLE_STATE_REGISTRY',
    registry_version='1.0.0', candidate_scope='TEST_ONLY',
    state_kinds=['V3MS_MEDIATOR'], roles=['REGULATORY_PROTECTIVE']))


class Refusal(Exception):
    pass


def require(condition, code):
    if not condition:
        raise Refusal(code)


@dataclass(frozen=True)
class HistoryEpisode:
    episode_id: str
    actor_id: str
    counterpart: str
    project: str
    time: int
    activity: str
    outcome: str
    actor_access: str
    parent_refs: tuple[str, ...]
    provenance: str = 'SYNTHETIC_PREHISTORY_FIXTURE'


@dataclass(frozen=True)
class Participant:
    actor_id: str
    project: str
    history: tuple[HistoryEpisode, ...]

    def offer(self):
        """Independent practical history determines action, without reading focal child."""
        enacted = {h.outcome for h in self.history if h.project == self.project}
        if 'tools_available' in enacted:
            return 'joint_inventory'
        if 'deadline_due' in enacted:
            return 'secure_alone'
        return 'no_plan'


@dataclass(frozen=True)
class Event:
    event_id: str
    actor_id: str
    time: int
    world_ref: str
    objective_occurrence: str
    project: str
    relation_refs: tuple[str, ...]
    power_ref: str
    offers: tuple[tuple[str, str, str], ...]  # counterpart, attributed words, actual plan
    interrupted: bool
    admission_grade: str = 'ADMITTED_SYNTHETIC_FIXTURE_ONLY'
    provenance: str = 'B1_AUTHORED_SOURCEFREE'


def initialize(history, project='repair_route'):
    """No mature traits: materialize only a typed, authorized synthetic prehistory."""
    return dict(schema=SCHEMA, actor_id='child', project=project,
                capabilities=['compare_enacted_plans'],
                history=[sealed(asdict(h)) for h in history],
                epistemic=dict(beliefs=['locking_reduces_access'],
                               unknown=['thief_identity', 'thief_motive'],
                               inaccessible=[h.episode_id for h in history
                                             if h.actor_access == 'INACCESSIBLE']),
                middle=[], responses=[], transitions=[])


def prehistory(outcome='recognized_plan', counterpart='caretaker', project='repair_route'):
    root = HistoryEpisode('init', 'child', counterpart, project, 0,
                          'learn_object_check', 'check_enacted', 'EXPLICIT', ())
    later = HistoryEpisode('shared_task', 'child', counterpart, project, 1,
                           'compare_plans_in_task', outcome, 'INACCESSIBLE', (digest(asdict(root)),))
    return [root, later]


def participant(actor_id='caretaker', outcome='tools_available'):
    h = HistoryEpisode(actor_id + '_work', actor_id, 'workshop', 'own_work', 0,
                       'organize_work', outcome, 'EXPLICIT', ())
    return Participant(actor_id, 'own_work', (h,))


def episode(number=1, people=None, project='repair_route', label=None):
    people = people or [participant()]
    return Event('event' + str(number), 'child', number + 1, 'world:garage',
                 label or ('bike_stolen' if number == 1 else 'shared_tool_offer'),
                 project, tuple('relation:child:' + p.actor_id for p in people),
                 'power:caretaker_controls_tools',
                 tuple((p.actor_id, 'Let us check what can be secured.', p.offer()) for p in people),
                 number == 1)


def mode_for(state, event, counterpart):
    """Immediate response candidate; concrete, falsifiable and deliberately narrow."""
    relevant = [h for h in state['history'] if h['counterpart'] == counterpart
                and h['project'] == event['project'] and h['time'] < event['time']
                and h['activity'] == 'compare_plans_in_task']
    return [(h, 'joint_check' if h['outcome'] == 'recognized_plan' else 'private_check')
            for h in relevant if h['outcome'] in ('recognized_plan', 'imposed_plan')]


def propose(state, event):
    require(valid(event), 'EVENT_INTEGRITY_FAILURE')
    require(event['admission_grade'] == 'ADMITTED_SYNTHETIC_FIXTURE_ONLY', 'EVENT_NOT_ADMITTED')
    require(event['actor_id'] == state['actor_id'], 'ACTOR_MISMATCH')
    require('compare_enacted_plans' in state['capabilities'], 'CAPABILITY_UNBOUND')
    require(all(valid(h) and h['provenance'] == 'SYNTHETIC_PREHISTORY_FIXTURE'
                for h in state['history']), 'HISTORY_INTEGRITY_FAILURE')
    seen = {}
    for h in state['history']:
        require(h['actor_id'] == state['actor_id'] and all(p in seen and seen[p] < h['time'] for p in h['parent_refs']),
                'HISTORY_LINEAGE_INVALID')
        seen[h['hash']] = h['time']
    for m in state['middle']:
        require(m['middle_state_record_hash'] == digest({k: v for k, v in m.items()
                    if k != 'middle_state_record_hash'}), 'MIDDLE_STATE_INTEGRITY_FAILURE')
        require(any(t['record'] == m and t['decision']['decision'] == 'ALLOW'
                    for t in state['transitions']), 'MIDDLE_STATE_LINEAGE_INVALID')
    require(all(h['time'] < event['time'] for h in state['history']), 'FUTURE_CONDITIONING')
    require(not state['responses'] or event['time'] >= state['responses'][-1]['time'], 'TIME_REVERSED')
    effects, uptake, recruited, actions = [], [], [], []
    if event['project'] == state['project']:
        for counterpart, words, plan in event['offers']:
            require('relation:child:' + counterpart in event['relation_refs'], 'RELATION_UNBOUND')
            stream = digest([event['hash'], counterpart])
            history_modes = mode_for(state, event, counterpart)
            uptake.append(dict(stream=stream, counterpart=counterpart, words=words,
                               propositional='UNDECIDED_ATTRIBUTED_ASSERTION',
                               affective=['recognized' if m == 'joint_check' else 'constrained'
                                          for _, m in history_modes]))
            if event['interrupted'] and plan == 'joint_inventory':
                for h, mode in history_modes:
                    recruited.append(h['hash'])
                    actions.append('compare_current_plan:' + counterpart)
                    payload = dict(project=event['project'], counterpart=counterpart, mode=mode,
                                   origin_access='INACCESSIBLE', belief_effect='NONE')
                    identity = digest([state['actor_id'], event['hash'], h['hash'], mode])
                    effects.append(sealed(dict(proposal_id=identity, actor_id=state['actor_id'],
                        state_kind_id='V3MS_MEDIATOR', target_middle_state_id=identity,
                        operation='CREATE', proposed_effective_time=event['time'],
                        proposed_role_tags=['REGULATORY_PROTECTIVE'],
                        semantic_object_ref='test_only:scoped_plan_comparison',
                        target_refs=[event['project'], counterpart],
                        proposed_payload_delta_or_replacement=payload,
                        causal_parent_refs=[event['hash'], h['hash']],
                        source_update_rule_ref=UPDATE_RULE,
                        evaluator_or_predicate_receipts=[h['hash']],
                        numeric_rule_ref=None, stochastic_receipt_ref=None,
                        provenance_refs=['B1_SOURCEFREE', GRADE], stream=stream,
                        effect_kind='TRANSFORM')))
            elif not event['interrupted'] and plan != 'no_plan':
                matches = [m for m in state['middle'] if m['lifecycle_status'] == 'ACTIVE'
                           and m['target_refs'] == [event['project'], counterpart]]
                for m in matches:
                    recruited.append(m['middle_state_record_hash'])
                    actions.append(m['governed_payload']['mode'] + ':' + counterpart)
                if not matches:
                    actions.append('inspect_alone:' + counterpart)
    return sealed(dict(schema=SCHEMA, actor_id=state['actor_id'], event_ref=event['hash'],
        time=event['time'], response_rule_ref=RESPONSE_RULE,
        prior_response_history_hash=digest(state['responses']), before_state_hash=digest(state),
        before_target_hash=digest(state['middle']), uptake=uptake, recruited=recruited,
        practical_activity=actions, target_proposals=effects,
        actor_surface=dict(actions=actions, origin_explanation='NOT_ACCESSIBLE'),
        status='RESPONSE_TRANSACTION_COMMITTED' if effects or actions else 'RESPONSE_EFFECTS_VALID_EMPTY'))


class TestOnlyCAN011Owner:
    """Independent destination predicate court. Never accepts CAN008's verdict as proof."""
    def __init__(self, authorized_grants=()):
        self.grants = set(authorized_grants)

    @staticmethod
    def permission(state, response):
        return sealed(dict(issuer='TEST_ONLY_CAN011_FIXTURE_AUTHORIZER', scope='TEST_ONLY',
            actor_id=state['actor_id'], before_target_hash=digest(state['middle']),
            response_hash=response['hash'], proposal_hashes=[p['hash'] for p in response['target_proposals']],
            update_rule_hash=UPDATE_RULE['hash']))

    def validate(self, state, event, response, permission):
        require(permission and valid(permission) and permission['hash'] in self.grants,
                'FOREIGN_OWNER_PERMISSION_DENIED')
        require(permission == self.permission(state, response), 'PERMISSION_BINDING_INVALID')
        require(response['before_target_hash'] == digest(state['middle']), 'STALE_TARGET')
        results = []
        existing = {m['middle_state_id'] for m in state['middle']}
        for p in response['target_proposals']:
            require(valid(p) and p['source_update_rule_ref'] == UPDATE_RULE, 'UPDATE_RULE_INTEGRITY')
            require(p['state_kind_id'] == 'V3MS_MEDIATOR' and p['operation'] == 'CREATE'
                    and p['proposed_role_tags'] == ['REGULATORY_PROTECTIVE'], 'INVALID_TARGET')
            require(p['actor_id'] == state['actor_id'] and p['target_middle_state_id'] not in existing,
                    'TARGET_IDENTITY_INVALID')
            require(p['proposed_effective_time'] == event['time'], 'TARGET_TIME_INVALID')
            parents = p['causal_parent_refs']
            h = next((h for h in state['history'] if h['hash'] in parents), None)
            require(h is not None and valid(h) and event['hash'] in parents, 'STALE_CAUSAL_PARENT')
            payload = p['proposed_payload_delta_or_replacement']
            require(event['interrupted'] and state['project'] == event['project']
                    and 'compare_enacted_plans' in state['capabilities'], 'TARGET_PREDICATE_DENIED')
            require(h['actor_id'] == state['actor_id'] and h['time'] < event['time']
                    and h['activity'] == 'compare_plans_in_task'
                    and h['project'] == event['project'], 'TARGET_HISTORY_DENIED')
            require(h['outcome'] in ('recognized_plan', 'imposed_plan'), 'TARGET_HISTORY_DENIED')
            expected_mode = {'recognized_plan': 'joint_check', 'imposed_plan': 'private_check'}[h['outcome']]
            expected = dict(project=event['project'], counterpart=h['counterpart'], mode=expected_mode,
                            origin_access='INACCESSIBLE', belief_effect='NONE')
            require(payload == expected and p['target_refs'] == [event['project'], h['counterpart']],
                    'TARGET_PAYLOAD_DENIED')
            require(any(o[0] == h['counterpart'] and o[2] == 'joint_inventory' for o in event['offers']),
                    'TARGET_OFFER_DENIED')
            require(p['numeric_rule_ref'] is None and p['stochastic_receipt_ref'] is None,
                    'NUMERIC_OR_STOCHASTIC_UNBOUND')
            existing.add(p['target_middle_state_id'])
            results.append(dict(proposal_hash=p['hash'], owner='TEST_ONLY_CAN011', decision='ALLOW',
                                permission_ref=permission['hash'], rule_ref=UPDATE_RULE))
        return results


class Store:
    """SQLite commits response, owner transition and checkpoint in one transaction.

    Admission is separately committed beforehand, so response rollback preserves occurrence.
    Use one event per invocation; unresolved same-time actor transitions fail closed.
    """
    def __init__(self, path, initial=None):
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.execute('CREATE TABLE IF NOT EXISTS checkpoint (id INTEGER PRIMARY KEY, body TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS occurrence (hash TEXT PRIMARY KEY, body TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS joint_receipt (hash TEXT PRIMARY KEY, body TEXT)')
        if initial is not None:
            self.db.execute('INSERT INTO checkpoint VALUES (1, ?)', (canonical(initial),))

    def close(self):
        self.db.close()

    def state(self):
        return json.loads(self.db.execute('SELECT body FROM checkpoint WHERE id=1').fetchone()[0])

    def admit_fixture(self, event):
        value = sealed(asdict(event))
        require(event.admission_grade == 'ADMITTED_SYNTHETIC_FIXTURE_ONLY', 'EVENT_NOT_ADMITTED')
        self.db.execute('INSERT OR IGNORE INTO occurrence VALUES (?,?)', (value['hash'], canonical(value)))
        return json.loads(canonical(value))

    def commit(self, event, response, owner, permission=None, journal_only=False, fault=None):
        before = self.state()
        try:
            self.db.execute('BEGIN IMMEDIATE')
            before = self.state()
            state = self.state()
            require(valid(event) and self.db.execute('SELECT body FROM occurrence WHERE hash=?',
                    (event['hash'],)).fetchone() == (canonical(event),), 'EVENT_NOT_ADMITTED')
            require(valid(response) and response['before_state_hash'] == digest(state), 'STALE_RESPONSE')
            require(response == propose(state, event), 'RESPONSE_RULE_DIVERGENCE')
            require(not state['responses'] or event['time'] > state['responses'][-1]['time'],
                    'SAME_TIME_ORDER_UNRESOLVED')
            decisions = []
            if response['target_proposals'] and not journal_only:
                decisions = owner.validate(state, event, response, permission)
                for p, decision in zip(response['target_proposals'], decisions, strict=True):
                    record = dict(actor_id=p['actor_id'], middle_state_id=p['target_middle_state_id'],
                        registry_id=REGISTRY['registry_id'], registry_version=REGISTRY['registry_version'],
                        registry_snapshot_hash=REGISTRY['hash'], state_kind_id=p['state_kind_id'],
                        mediator_role_tags=p['proposed_role_tags'], semantic_object_ref=p['semantic_object_ref'],
                        target_refs=p['target_refs'], lifecycle_status='ACTIVE', effective_from=event['time'],
                        effective_to=None, governed_payload=p['proposed_payload_delta_or_replacement'],
                        creation_or_update_rule_ref=UPDATE_RULE, causal_parent_refs=p['causal_parent_refs'],
                        source_context_receipt_refs=[event['hash']], prior_middle_state_record_hash=None,
                        provenance_refs=p['provenance_refs'])
                    record['middle_state_record_hash'] = digest(record)
                    state['middle'].append(record)
                    state['transitions'].append(dict(proposal=p, record=record, decision=decision))
            state['responses'].append(response)
            receipt = sealed(dict(joint_transaction_id=response['hash'], admitted_event_ref=event['hash'],
                before_hash=digest(before), after_hash=digest(state), owner_decisions=decisions,
                rules=[RESPONSE_RULE, UPDATE_RULE], status='COMMITTED',
                mode='JOURNAL_ONLY_CONTROL' if journal_only else 'B_FIRST', rng_draws=0))
            self.db.execute('UPDATE checkpoint SET body=? WHERE id=1', (canonical(state),))
            if fault == 'after_checkpoint':
                raise Refusal('INJECTED_STORAGE_FAILURE')
            self.db.execute('INSERT INTO joint_receipt VALUES (?,?)', (receipt['hash'], canonical(receipt)))
            self.db.execute('COMMIT')
            return receipt
        except (Refusal, sqlite3.Error, KeyError, TypeError, ValueError) as error:
            if self.db.in_transaction:
                self.db.execute('ROLLBACK')
            require(self.state() == before, 'ROLLBACK_INTEGRITY_FAILURE')
            return sealed(dict(status='TRANSACTION_ABORTED_ROLLBACK',
                reason=str(error) if isinstance(error, (Refusal, sqlite3.Error))
                       else 'INPUT_SCHEMA_INVALID:' + type(error).__name__, before_hash=digest(before)))


def execute(store, event, journal_only=False, fault=None):
    admitted = store.admit_fixture(event)
    response = propose(store.state(), admitted)
    permission = TestOnlyCAN011Owner.permission(store.state(), response)
    owner = TestOnlyCAN011Owner([permission['hash']])
    receipt = store.commit(admitted, response, owner, permission, journal_only, fault)
    return response, receipt


def demonstrate(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    evidence = {}
    for name, journal in [('positive', False), ('journal_only', True)]:
        path = directory / (name + '.sqlite')
        if path.exists():
            path.unlink()
        store = Store(path, initialize(prehistory()))
        first, receipt1 = execute(store, episode(), journal_only=journal)
        after_first = store.state()
        store.close()
        store = Store(path)  # proves actual disk persistence across connection lifetime
        second, receipt2 = execute(store, episode(2), journal_only=journal)
        evidence[name] = dict(first=first, first_receipt=receipt1, persisted_after_first=after_first,
                              second=second, second_receipt=receipt2, final_hash=digest(store.state()))
        store.close()
    assert evidence['positive']['second']['practical_activity'] == ['joint_check:caretaker']
    assert evidence['journal_only']['second']['practical_activity'] == ['inspect_alone:caretaker']
    (directory / 'positive_receipt.json').write_text(json.dumps(evidence, indent=2) + '\n')
    return evidence


if __name__ == '__main__':
    import sys
    result = demonstrate(sys.argv[1])
    print(canonical({k: dict(final_hash=v['final_hash'], later_action=v['second']['practical_activity'])
                     for k, v in result.items()}))
