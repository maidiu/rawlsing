"""NEIGHBORMULCH sourcefree one-writer encounter-side research consumer.

The *existing* UM-SOROK ResearchLedger is the sole world/actor transaction
writer. Visitors are world participants, NOT fictitious psychological actors.
P6/MIII sensory distinctions are recovered into actor-qualified world evidence;
P6's separate session writer is never called. MII remains a private reader.

This is a bounded first-consumer candidate, not native P2/P6 integration,
identity authentication, developmental science or a complete human encounter.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from um_sorok_organism.types import digest, stable_id
from um_sorok_organism.world import add_cue


class EncounterRefusal(ValueError):
    """A user cannot create world, actor, source or sensory rights by prose."""


_ALLOWED = frozenset({'SAY', 'MOVE', 'WAIT', 'LEAVE'})


def _text(value: Any, label: str, maximum: int = 500) -> str:
    if type(value) is not str or not value.strip() or len(value) > maximum:
        raise EncounterRefusal('INVALID_' + label)
    return value


def _bound_source(world: dict) -> dict:
    conditions = world.get('neighbor_sensory_source')
    if not isinstance(conditions, dict) or conditions.get('grade') != 'SOURCEFREE_TEST_ONLY':
        raise EncounterRefusal('NO_QUALIFIED_SENSORY_SOURCE')
    return conditions


def sensory_evidence(world: dict, actor: dict, visitor: dict, operation: str,
                     origin: str | None, destination: str, event_ref: str) -> list[dict]:
    """MIII law: auditory evidence can arrive behind; visual identity cannot.

    Sourcefree geometry is *precommitted* in this same world, never supplied by
    an interpretive LLM or the caller at the decision moment. These are
    materially possible signs, NOT proof of actor attention or understanding.
    """
    source = _bound_source(world)
    row = source.get('actor_conditions', {}).get(actor['id'])
    if not isinstance(row, dict):
        return []
    if world['positions'].get(actor['id']) != destination:
        return []
    sound = row.get('hearing') is True and row.get('sound_path') == 'audible'
    visible = (row.get('visual') is True and row.get('light') == 'lit'
               and row.get('sightline') == 'unobstructed'
               and row.get('facing') == 'entrance')
    grade = 'SOURCEFREE_TEST_ONLY'
    result = []
    if operation == 'MOVE' and sound:
        result.append({'event_ref': event_ref, 'actor': actor['id'],
                       'modality': 'auditory', 'kind': 'visitor_footsteps',
                       'tags': ['footsteps', 'approach'], 'description': 'Footsteps nearby.',
                       'grade': grade, 'visual_identity_known': False})
    if operation == 'SAY' and sound:
        # Audibility is not lexical comprehension. The world retains exact
        # user-authored words, but an immature hearer receives only a sourced
        # sound opportunity, not the adult analyst's propositional knowledge.
        # This is a provisional sourcefree capacity gate, not speech science.
        language = actor.get('body', {}).get('language', 0)
        if type(language) not in (int, float) or not 0 <= language <= 1:
            raise EncounterRefusal('INVALID_ACTOR_LANGUAGE_CAPACITY')
        verbal = language >= 0.35
        result.append({'event_ref': event_ref, 'actor': actor['id'],
                       'modality': 'auditory', 'kind': 'visitor_speech',
                       'tags': ['speech'] if verbal else ['voice', 'speech_sound'],
                       'description': visitor['spoken_text'] if verbal
                                      else 'Speech sounds nearby.',
                       'grade': grade, 'speaker_identity_confirmed': False,
                       'lexical_comprehension': 'SOURCEFREE_CAPACITY_ELIGIBLE' if verbal
                                                else 'NOT_ESTABLISHED'})
    if operation == 'MOVE' and visible:
        result.append({'event_ref': event_ref, 'actor': actor['id'],
                       'modality': 'visual', 'kind': 'visitor_arrival',
                       'tags': ['movement', 'visitor'],
                       'description': 'A visitor enters the workspace.',
                       'grade': grade, 'gaze_intention_known': False})
    return result


class NeighborEncounter:
    """Encounter-side writer request and MII viewer; no new psyche or world DB.

    Only ledger.commit determines world/event history. runtime.step is the
    existing independent organism decision/world/afterlife transaction. No
    user text is allowed to select an actor motive, project or reaction.
    """

    def __init__(self, runtime, user_id: str, *, mii_module=None):
        self.runtime = runtime
        self.user_id = _text(user_id, 'USER_ID', 100)
        if user_id in runtime.ledger.actors():
            raise EncounterRefusal('USER_CANNOT_IMPERSONATE_ACTOR')
        self.mii = mii_module
        self._last_actor_tip = None  # read-only, process-local; never a world fact
        self._last_actor_ref = None

    def _world(self):
        return self.runtime.ledger.world(self.runtime.world_id)

    def install_sourcefree_conditions(self, conditions: dict, *, request_id: str):
        """Explicit immutable demo conditions; never an implicit universal sensor law."""
        _text(request_id, 'REQUEST_ID', 120)
        if type(conditions) is not dict or conditions.get('grade') != 'SOURCEFREE_TEST_ONLY':
            raise EncounterRefusal('UNQUALIFIED_SENSORY_CONDITIONS')
        actor_conditions = conditions.get('actor_conditions')
        if type(actor_conditions) is not dict or not actor_conditions:
            raise EncounterRefusal('MISSING_ACTOR_CONDITIONS')
        actors = self.runtime.ledger.actors()
        if not set(actor_conditions).issubset(actors):
            raise EncounterRefusal('UNREGISTERED_SENSORY_ACTOR')
        # User phenomenal eligibility has an independent physical source.
        # Co-presence alone never licenses a visible body, readable object or
        # actor-expression tip. A private MII gaze cannot invent geometry.
        user_conditions = conditions.get('user_conditions')
        if type(user_conditions) is not dict or not user_conditions:
            raise EncounterRefusal('MISSING_USER_SENSORY_CONDITIONS')
        for site, view in user_conditions.items():
            if site not in self._world()[1]['sites'] or type(view) is not dict:
                raise EncounterRefusal('INVALID_USER_VIEW_SITE')
            if (view.get('light') not in ('lit','dark','unknown') or
                view.get('sightline') not in ('unobstructed','partial','blocked','unknown') or
                type(view.get('hearing')) is not bool or
                view.get('sound_path') not in ('audible','blocked','unknown')):
                raise EncounterRefusal('INVALID_USER_SENSORY_CONDITIONS')
        for actor_id, row in actor_conditions.items():
            if type(row) is not dict or any(key not in row for key in
                ('facing', 'hearing', 'visual', 'light', 'sightline', 'sound_path')):
                raise EncounterRefusal('INCOMPLETE_SENSORY_CONDITIONS')
            if row['facing'] not in ('entrance', 'away') or any(
                    type(row[k]) is not bool for k in ('hearing', 'visual')):
                raise EncounterRefusal('INVALID_SENSORY_CONDITIONS')
        version, world = self._world()
        existing = world.get('neighbor_sensory_source')
        if existing is not None:
            if existing != conditions:
                raise EncounterRefusal('SENSORY_SOURCE_ALREADY_BOUND')
            return {'status': 'ALREADY_BOUND', 'source_hash': digest(existing)}
        world['neighbor_sensory_source'] = deepcopy(conditions)
        world['clock'] += 1
        receipt = self.runtime.ledger.commit(self.runtime.world_id, version, world,
            {}, {}, 'NEIGHBOR_SOURCEFREE_GEOMETRY', None,
            {'request_id': request_id, 'source_hash': digest(conditions),
             'not_native_sensor_law': True})
        return {'status': 'SOURCEFREE_BOUND', 'receipt': receipt['id'],
                'source_hash': digest(conditions)}

    def contribute(self, request_id: str, operation: str, *, text: str | None = None,
                   destination: str | None = None):
        """One user-authored world event with derived actor-eligible signs.

        Retries are idempotent *against the durable world request index*;
        different payload under one request ID is refused. No second writer,
        no narrative coactor consent and no user-psyche interpretation.
        """
        request_id = _text(request_id, 'REQUEST_ID', 120)
        if operation not in _ALLOWED:
            raise EncounterRefusal('UNKNOWN_USER_OPERATION')
        if operation == 'SAY':
            text = _text(text, 'USER_SPEECH')
        elif text is not None:
            raise EncounterRefusal('UNAUTHORED_EXTRA_SPEECH')
        if operation == 'MOVE':
            destination = _text(destination, 'DESTINATION', 100)
        elif destination is not None:
            raise EncounterRefusal('UNAUTHORED_DESTINATION')
        version, world = self._world()
        req_key = self.user_id + ':' + request_id
        payload_hash = digest({'user': self.user_id, 'operation': operation,
                               'text': text, 'destination': destination})
        prior = world.get('neighbor_user_requests', {}).get(req_key)
        if prior:
            if prior['payload_hash'] != payload_hash:
                raise EncounterRefusal('REQUEST_REPLAY_CHANGED_PAYLOAD')
            existing = next((e['id'] for e in self.runtime.ledger.events()
                if e['kind'] == 'NEIGHBOR_USER_CONTRIBUTION'
                and e['envelope']['payload'].get('user_event_ref') == prior['event_ref']), None)
            if existing is None:
                raise EncounterRefusal('REQUEST_INDEX_WITHOUT_COMMITTED_EVENT')
            return {'status': prior['status'], 'event_ref': prior['event_ref'],
                    'idempotent_replay': True, 'receipt': existing}
        participants = world.setdefault('neighbor_users', {})
        person = deepcopy(participants.get(self.user_id, {'present': False, 'location': None}))
        origin = person['location']
        if operation != 'MOVE' and operation != 'LEAVE' and not person['present']:
            raise EncounterRefusal('USER_NOT_PRESENT')
        status = 'PERFORMED'
        loc = origin
        if operation == 'MOVE':
            if destination not in world['sites']:
                status = 'BLOCKED'
            elif person['present']:
                routes = world.get('neighbor_routes', {})
                if destination not in routes.get(origin, []):
                    status = 'BLOCKED'
            elif destination not in ('home', 'workshop'):
                status = 'BLOCKED'
            if status == 'PERFORMED':
                loc = destination
                person.update(present=True, location=destination)
        elif operation == 'LEAVE':
            person['present'] = False
        world['clock'] += 1
        ref = stable_id('neighbor_user', {'user': self.user_id,
            'request_id': request_id, 'payload_hash': payload_hash})
        evidence = []
        if status == 'PERFORMED' and operation in ('MOVE', 'SAY'):
            _bound_source(world)
            for actor_id, actor in self.runtime.ledger.actors().items():
                eligible = sensory_evidence(world, actor,
                    {'spoken_text': text}, operation, origin, loc, ref)
                for sign in eligible:
                    # A transient user sound remains physically transient.
                    # R21's pre-action constitution read records the eligible
                    # cue ref; later *subjective* uptake must be separately
                    # earned by its competent owner. Extending the lifetime
                    # cannot authorize an actor memory or perception.
                    cue = add_cue(world, sign['kind'], sign['tags'],
                        location=loc, modality=sign['modality'],
                        description=sign['description'], source_actor=None,
                        private_to=actor_id)
                    evidence.append({'actor': actor_id, 'event_ref': ref,
                                     'cue_ref': cue['id'], 'modality': sign['modality'],
                                     'basis': sign['kind'], 'grade': sign['grade']})
        participants[self.user_id] = person
        event = {'event_ref': ref, 'request_id': request_id, 'user': self.user_id,
                 'operation': operation, 'payload_hash': payload_hash,
                 'authored_text': text, 'origin': origin, 'destination': loc,
                 'clock': world['clock'], 'status': status,
                 'perceptual_candidates': evidence,
                 'no_inference_of_actor_uptake': True}
        world.setdefault('neighbor_user_events', []).append(event)
        world.setdefault('neighbor_user_requests', {})[req_key] = {
            'event_ref': ref, 'payload_hash': payload_hash, 'status': status,
            'ledger_receipt': None}
        receipt = self.runtime.ledger.commit(self.runtime.world_id, version, world,
            {}, {}, 'NEIGHBOR_USER_CONTRIBUTION', None,
            {'user_event_ref': ref, 'source': 'SOURCEFREE_USER_SUBMITTED',
             'user': self.user_id, 'payload_hash': payload_hash,
             'performed': status == 'PERFORMED',
             'candidate_cue_refs': [e['cue_ref'] for e in evidence],
             'no_actor_motive_or_consent_issued': True})
        # The world record already contains durable request idempotency. Its
        # canonical event ref is the source for later actor reads, not this
        # returned envelope ID; never make a second write to attach it.
        return {'status': status, 'event_ref': ref, 'receipt': receipt['id'],
                'idempotent_replay': False, 'potential_actor_evidence': evidence,
                'actor_uptake': 'NOT_ESTABLISHED'}

    def independent_actor_beat(self, actor_id: str):
        """Use the actual continuing actor's own plan, not a supplied reply."""
        if actor_id not in self.runtime.ledger.actors():
            raise EncounterRefusal('NO_CONSTITUTED_ACTOR')
        result = self.runtime.step(actor_id)  # NEVER pass requested_action
        _, world = self._world()
        self._last_actor_tip = (result.get('receipt'), world['clock'],
                                result.get('public_tip'))
        self._last_actor_ref = actor_id
        return result

    def continue_independent_life_during_visit(self, *, profile=None):
        """One genuinely independent actor/world beat while a visitor is present.

        This is NOT an LLM-selected scene or player request for a particular
        person's response. Reuse the existing organism initiative scheduler,
        actor/world writer and MII bounded visitor surface. One new performed
        user contribution is the causal *opportunity* for at most one beat;
        retries must not create an extra actor event.
        """
        _, world = self._world()
        visitor=world.get('neighbor_users',{}).get(self.user_id)
        if not isinstance(visitor,dict) or visitor.get('present') is not True:
            raise EncounterRefusal('VISITOR_NOT_PRESENT_FOR_LIVE_OCCASION')
        # User may not supply a target actor or an action: the existing
        # independent actor scheduler owns the decision opportunity.
        history=self.runtime.ledger.events()
        user_indices=[i for i,event in enumerate(history)
            if event.get('kind')=='NEIGHBOR_USER_CONTRIBUTION'
            and event.get('envelope',{}).get('payload',{}).get('user')==self.user_id
            and event.get('envelope',{}).get('payload',{}).get('performed') is True]
        if not user_indices:
            raise EncounterRefusal('NO_QUALIFIED_USER_LIFE_OCCASION')
        source_index=user_indices[-1]
        source_event=history[source_index]
        source_ref=source_event['envelope']['payload']['user_event_ref']
        subsequent=history[source_index+1:]
        # A later committed life transition is enough to conservatively
        # refuse to create another one on an identical preceding user turn.
        # No extra marker store, no second world author, no fabricated event.
        if any(e.get('kind')=='ACTOR_LIFE_TRANSITION' for e in subsequent):
            return {'status':'ALREADY_ADVANCED_AFTER_USER_OCCASION',
                    'source_user_event_ref':source_ref,
                    'new_world_event':False,'actor_response_not_commanded':True}
        from um_sorok_organism.initiative import choose_next_actor
        selected=choose_next_actor(world,self.runtime.ledger.actors())
        if selected is None:
            return {'status':'NO_ELIGIBLE_INDEPENDENT_ACTOR',
                    'source_user_event_ref':source_ref,
                    'new_world_event':False,'actor_response_not_commanded':True}
        result=self.independent_actor_beat(selected['actor'])
        if result.get('selection_grade')=='INJECTED_NOT_NATIVE_ACTOR_CHOICE':
            raise EncounterRefusal('LIVE_OCCASION_FORGED_ACTOR_SELECTION')
        _, updated=self._world()
        view=self.private_surface(profile) if profile is not None else None
        return {'status':'INDEPENDENT_ACTOR_WORLD_EVENT_COMMITTED',
                'source_user_event_ref':source_ref,
                'actor_event_receipt':result['receipt'],
                'world_clock':updated['clock'],
                'actor_selected_by_existing_initiative':selected['actor'],
                'actor_operation':result['attempt'],
                'actor_status':result['status'],
                'visitor_surface':view,
                'new_world_event':True,
                'no_visitor_selected_actor_intention_or_response':True,
                'no_unseen_private_psychology_on_visitor_surface':True,
                'grade':'SOURCEFREE_RESEARCH_PROVISIONAL'}

    def private_surface(self, profile: dict, *, command: str | None = None,
                        target: str | None = None):
        """Real MII operations over finite, public facts; no world/actor writes."""
        if self.mii is None:
            raise EncounterRefusal('MII_READER_NOT_INSTALLED')
        _, world = self._world()
        visitor = world.get('neighbor_users', {}).get(self.user_id)
        if not visitor or not visitor['present']:
            raise EncounterRefusal('USER_NOT_PRESENT')
        loc = visitor['location']
        source = _bound_source(world)
        user_view = source.get('user_conditions', {}).get(loc, {})
        visible = (user_view.get('light') == 'lit' and
                   user_view.get('sightline') == 'unobstructed')
        audible = (user_view.get('hearing') is True and
                   user_view.get('sound_path') == 'audible')
        # Only already admitted public material objects with an explicit
        # observer-eligible surface may supply optional details. Never infer
        # a secret story from the object or an actor's hidden constitution.
        available = {}
        for key, obj in world.get('material_objects', {}).items():
            if (visible and type(obj) is dict and obj.get('location') == loc and
                    type(obj.get('public_glance')) is str):
                available[key] = obj['public_glance']
        selected, basis = self.mii.select_detail(available, profile,
            command=command, target=target, offered=available)
        mandatory = [{'kind': 'LOCATION', 'text': loc}]
        for actor_id, actor_loc in sorted(world['positions'].items()):
            if visible and actor_loc == loc:
                mandatory.append({'kind': 'CO_PRESENT_ACTOR',
                                  'actor_ref': actor_id, 'interpretation': 'NONE'})
        if self._last_actor_tip is not None:
            _, at_clock, tip = self._last_actor_tip
            # A sourcefree speaker expression is not automatically audible to
            # a visitor in another room, an occluded chamber or a dark room.
            # Conservatively require co-location AND a sourced sensory path.
            actor_location = world['positions'].get(self._last_actor_ref)
            if (at_clock == world['clock'] and actor_location == loc and
                    (visible or audible) and type(tip) is str and tip.strip()):
                mandatory.append({'kind': 'PUBLIC_TIP', 'text': tip[:500],
                                  'source': 'EXISTING_ORGANISM_PUBLIC_EXPRESSION'})
        view = self.mii.surface(room=loc, orientation='SOURCEFREE_UNKNOWN',
            exit_name='SOURCEFREE_UNQUALIFIED', available=available,
            candidates=available, offered=available, selected=selected,
            basis=basis, narration=mandatory, recognition={})
        self.mii.record_exposure(profile, turn=world['clock'], clock=world['clock'],
            available=available, candidates=available, offered=available,
            selected=selected, rendered=view, basis=basis,
            request_id=None, context={'room': loc, 'world': self.runtime.world_id})
        return view

    def new_private_profile(self):
        if self.mii is None:
            raise EncounterRefusal('MII_READER_NOT_INSTALLED')
        root = self.runtime.ledger.events()[0]['id']
        scope = {'root': root, 'branch': self.runtime.world_id, 'user': self.user_id}
        return self.mii.default_profile(scope)
