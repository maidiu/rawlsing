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
from pathlib import Path
from types import SimpleNamespace
from typing import Any
import fcntl

from um_sorok_organism.types import digest, stable_id, GRADE
from um_sorok_organism.world import add_cue
from um_sorok_organism.material_objects import material_objects_present
from um_sorok_organism.practical_inquiry import notices_present


class EncounterRefusal(ValueError):
    """A user cannot create world, actor, source or sensory rights by prose."""


_ALLOWED = frozenset({'SAY', 'MOVE', 'WAIT', 'LEAVE', 'LOOK', 'REPAIR', 'MAKE_OBJECT',
                      'SIGN_HALL_PETITION', 'SING', 'OFFER_FEED', 'PLEDGE_OFFER', 'WITHDRAW_PLEDGE', 'PROPOSE_MEETING', 'CHECK_IN_MEETING'})


def _text(value: Any, label: str, maximum: int = 500) -> str:
    if type(value) is not str or not value.strip() or len(value) > maximum:
        raise EncounterRefusal('INVALID_' + label)
    return value


def _bound_source(world: dict) -> dict:
    conditions = world.get('neighbor_sensory_source')
    if not isinstance(conditions, dict) or conditions.get('grade') != 'SOURCEFREE_TEST_ONLY':
        raise EncounterRefusal('NO_QUALIFIED_SENSORY_SOURCE')
    return conditions


def _public_material_projection(world: dict, location: str) -> dict:
    """Finite read projection of actual CO artifacts into protected MII.

    The existing material owner determines which actual artifacts are visible
    and where. No ownership, maker, objective labor/condition history or
    actor meanings enter this view. Keep R4's explicitly public fixture text
    for legacy objects; an actual CO artifact cannot be overridden by it.
    Appearance bands are the existing CO world INSPECT convention (.65/.95),
    provisionally mirrored for the visitor's close surface, not a material
    law or an inferred repair history. A shared owner helper is future work.
    """
    view = {}
    for ref, row in world.get('material_objects', {}).items():
        # An already exposed physical face is not a public institutional
        # assertion or an act of entrusting. Only explicitly staged fictional
        # face text is eligible. Never expose the interior, even at close.
        if type(row) is dict and row.get('kind') == 'INCIDENTALLY_EXPOSED_DOCUMENT':
            face = row.get('exposed_face')
            if (type(ref) is str and row.get('id') == ref
                    and row.get('location') == location
                    and row.get('visible') is True
                    and row.get('grade') == 'SOURCEFREE_TEST_ONLY'
                    and type(face) is str and face.strip() and len(face) <= 500):
                view[ref] = {'location': location,
                             'public_glance': 'An exposed document lies here.',
                             'public_close': face,
                             'grade': 'SOURCEFREE_TEST_ONLY',
                             'source_kind': 'INCIDENTALLY_EXPOSED_DOCUMENT'}
            continue
        if (type(ref) is str and type(row) is dict
                and row.get('location') == location
                and row.get('visible') is not False
                and row.get('kind') != 'WORKED_MATERIAL_ARTIFACT'
                and type(row.get('public_glance')) is str):
            view[ref] = {'location': location,
                         'public_glance': row['public_glance'],
                         'public_close': row.get('public_close'),
                         'grade': row.get('grade')}
    for row in material_objects_present(world, location):
        ref = row['id']
        condition = row.get('condition')
        if (row.get('kind') != 'WORKED_MATERIAL_ARTIFACT'
                or row.get('grade') != GRADE
                or world['material_objects'].get(ref) is not row
                or type(condition) not in (int, float)
                or not 0 <= condition <= 1):
            continue
        appearance = ('It appears worn.' if condition < .65 else
                      'It appears repaired.' if condition < .95 else
                      'It appears sound.')
        view[ref] = {'location': location,
                     'public_glance': 'A worked material object is here.',
                     'public_close': appearance,
                     'grade': 'SOURCEFREE_TEST_ONLY'}
    return view


def _public_encounter_projection(world: dict, location: str) -> dict:
    """Extend the same MII target set with existing institution-owned notices.

    CO notices_present owns spatial and temporal applicability. A readable
    inscription is the institution's published words, not proof of its
    underlying rule, motive, truth, access rights, or anyone's agreement.
    This read-only adapter never posts a notice or performs actor INSPECT.
    """
    view = _public_material_projection(world, location)
    notices = notices_present(world, location, world['clock'])
    counts = {}
    for row in notices:
        counts[row['id']] = counts.get(row['id'], 0) + 1
    for row in notices:
        ref = row['id']
        # Do not let duplicate source identities select a different body
        # of text or override a real material object's identity.
        if counts[ref] != 1 or ref in world.get('material_objects', {}):
            view.pop(ref, None)
            continue
        if row.get('public') is not True:
            continue
        words = row.get('public_text')
        view[ref] = {
            'location': location,
            'public_glance': 'A public notice is posted here.',
            'public_close': words if type(words) is str and words.strip()
                            and len(words) <= 500 else None,
            'grade': 'SOURCEFREE_TEST_ONLY',
            'source_kind': 'CO_PUBLIC_NOTICE',
        }
    return view


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
    if operation in ('SAY', 'LOOK') and sound and type(visitor.get('spoken_text')) is str:
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
    if operation == 'LOOK' and visible:
        # A possible visible orientation cannot establish what the visitor
        # read, meant or concealed; actor notice/interpretation is CO-owned.
        result.append({'event_ref': event_ref, 'actor': actor['id'],
                       'modality': 'visual', 'kind': 'visitor_glance',
                       'tags': ['visitor', 'visible_orientation'],
                       'description': 'A visitor visibly turns toward an object.',
                       'grade': grade, 'target_identity_known': False,
                       'visitor_knowledge_known': False,
                       'actor_notice_not_established': True})
    if (operation == 'PLEDGE_OFFER' and visible and sound
            and actor.get('body',{}).get('language',0)>=.35):
        # A structured outward undertaking. Not an actor's agreement,
        # comprehension, expected future receipt, or emotional appraisal.
        result.append({'event_ref':event_ref,'actor':actor['id'],
                       'modality':'auditory','kind':'visitor_offer_undertaking',
                       'tags':['visitor','food','future_offer'],
                       'description':'A visitor undertakes to offer food later.',
                       'grade':grade,'visual_identity_eligible':True})
    if (operation in ('PROPOSE_MEETING','CHECK_IN_MEETING') and visible and sound
            and actor.get('body',{}).get('language',0)>=.35):
        result.append({'event_ref':event_ref,'actor':actor['id'],
                       'modality':'auditory',
                       'kind':('visitor_meeting_proposal' if operation=='PROPOSE_MEETING'
                               else 'visitor_meeting_checkin'),
                       'tags':['visitor','meeting','particular_time'],
                       'description':('A visitor proposes a particular future meeting.'
                           if operation=='PROPOSE_MEETING' else
                           'A visitor checks in for the accepted meeting now.'),
                       'grade':grade,'visual_identity_eligible':True})
    if operation == 'OFFER_FEED' and visible:
        result.append({'event_ref': event_ref, 'actor': actor['id'],
                       'modality': 'visual', 'kind': 'visitor_food_offer',
                       'tags': ['food', 'offer'], 'description': 'A visitor offers food.',
                       'grade': grade, 'visual_identity_eligible': True})
    if operation == 'SING' and sound:
        result.append({'event_ref': event_ref, 'actor': actor['id'],
                       'modality': 'auditory', 'kind': 'visitor_vocal_practice',
                       'tags': ['voice', 'singing'], 'description': 'Singing nearby.',
                       'grade': grade, 'visual_identity_eligible': visible})
    if operation == 'SIGN_HALL_PETITION' and visible:
        result.append({'event_ref': event_ref, 'actor': actor['id'],
                       'modality': 'visual', 'kind': 'visitor_public_procedure',
                       'tags': ['public_procedure', 'visible_activity'],
                       'description': 'Someone makes a contribution to the posted procedure.',
                       'grade': grade, 'actor_notice_not_established': True})
    if operation in ('REPAIR','MAKE_OBJECT') and visible:
        # The world has actually settled repair before this projection.
        # No audible tool, identification, intent or approval is invented.
        result.append({'event_ref': event_ref, 'actor': actor['id'],
                       'modality': 'visual', 'kind': 'visitor_material_work',
                       'tags': ['material_work', 'visible_activity'],
                       'description': 'Someone works on a nearby object.',
                       'grade': grade, 'target_identity_known': False,
                       'actor_notice_not_established': True})
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
                view.get('sound_path') not in ('audible','blocked','unknown') or
                view.get('legibility', 'unknown') not in
                    ('readable', 'unreadable', 'unknown')):
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

    def configure_sourcefree_correspondence(self, route_ref, recipient, site, *, delay_ticks=1):
        """World-owner fixture only: not a visitor-granted access right or actor consent."""
        route_ref=_text(route_ref,'CHANNEL_REF',100)
        recipient=_text(recipient,'CHANNEL_RECIPIENT',100)
        site=_text(site,'CHANNEL_DEVICE_SITE',100)
        if type(delay_ticks) is not int or not 1<=delay_ticks<=24:
            raise EncounterRefusal('INVALID_CHANNEL_DELAY')
        v,world=self._world()
        if recipient not in self.runtime.ledger.actors() or site not in world['sites']:
            raise EncounterRefusal('UNQUALIFIED_CHANNEL_ENDPOINT')
        row={'id':route_ref,'sender':self.user_id,'recipient':recipient,
             'device_site':site,'delay_ticks':delay_ticks,'active':True,
             'grade':'SOURCEFREE_TEST_ONLY','issued_at':world['clock']}
        routes=world.setdefault('neighbor_correspondence_routes',{})
        if route_ref in routes:
            raise EncounterRefusal('CHANNEL_ALREADY_EXISTS')
        routes[route_ref]=row
        return self.runtime.ledger.commit(self.runtime.world_id,v,world,{}, {},
            'NEIGHBOR_CHANNEL_SOURCEFREE_GRANT',None,{'route':deepcopy(row)})['id']

    def revoke_sourcefree_correspondence(self, route_ref):
        """Prospective reachability change, not deletion or relational judgment."""
        v,world=self._world()
        row=world.get('neighbor_correspondence_routes',{}).get(route_ref)
        if not row or row['sender']!=self.user_id or not row['active']:
            raise EncounterRefusal('CHANNEL_NOT_ACTIVE')
        row['active']=False
        row['revoked_at']=world['clock']
        return self.runtime.ledger.commit(self.runtime.world_id,v,world,{}, {},
            'NEIGHBOR_CHANNEL_SOURCEFREE_REVOKE',None,{'route_ref':route_ref})['id']

    def send_correspondence(self, request_id, route_ref, text):
        """Actual authored asynchronous text, even when the visitor is absent.
        No model call, automatic delivery, reading, response or visitor psyche.
        """
        request_id=_text(request_id,'REQUEST_ID',120)
        route_ref=_text(route_ref,'CHANNEL_REF',100)
        text=_text(text,'MESSAGE_TEXT',500)
        v,world=self._world()
        key=stable_id('correspondence_send',{'sender':self.user_id,'request':request_id})
        rows=world.setdefault('neighbor_correspondence',{})
        old=rows.get(key)
        if old:
            if old['route_ref']!=route_ref or old['text']!=text or old['sender']!=self.user_id:
                raise EncounterRefusal('MESSAGE_REPLAY_CHANGED_PAYLOAD')
            return {'message_ref':key,'status':'SENT','idempotent_replay':True}
        route=world.get('neighbor_correspondence_routes',{}).get(route_ref)
        if not route or route['sender']!=self.user_id or not route['active']:
            raise EncounterRefusal('CHANNEL_SEND_NOT_AUTHORIZED')
        rows[key]={'id':key,'route_ref':route_ref,'sender':self.user_id,
                   'recipient':route['recipient'],'text':text,
                   'sent_clock':world['clock'],
                   'deliver_not_before':world['clock']+route['delay_ticks'],
                   'delivered_clock':None,'opened_clock':None}
        self.runtime.ledger.commit(self.runtime.world_id,v,world,{}, {},
            'NEIGHBOR_CORRESPONDENCE_SENT',None,{'message_ref':key,'route_ref':route_ref,
             'sender':self.user_id,'text_hash':digest(text),'no_receipt_inferred':True})
        return {'message_ref':key,'status':'SENT','idempotent_replay':False}

    def settle_sourcefree_correspondence_delivery(self, message_ref):
        """Explicit world transport tick; no actor call or fabricated reading.
        Revocation prevents an in-flight delivery; previously delivered
        correspondence remains on the recipient's modeled device.
        """
        v,world=self._world()
        row=world.get('neighbor_correspondence',{}).get(message_ref)
        if not row or row['sender']!=self.user_id:
            raise EncounterRefusal('MESSAGE_NOT_IN_SCOPE')
        if row['delivered_clock'] is not None:
            return 'ALREADY_DELIVERED'
        route=world.get('neighbor_correspondence_routes',{}).get(row['route_ref'])
        if not route or not route['active']:
            return 'TRANSPORT_ROUTE_REVOKED'
        if world['clock']<row['deliver_not_before']:
            return 'TRANSPORT_NOT_DUE'
        row['delivered_clock']=world['clock']
        self.runtime.ledger.commit(self.runtime.world_id,v,world,{}, {},
            'NEIGHBOR_CORRESPONDENCE_DELIVERED',None,
            {'message_ref':message_ref,'route_ref':row['route_ref'],
             'recipient':row['recipient'],'no_reading_or_comprehension_inferred':True})
        return 'DELIVERED'

    def surrender_entry_permission(self, request_id, site_ref):
        """Actual human relinquishment of their own controlled-site admission.

        Not a grant, a public-right waiver, an eviction, or a relationship
        verdict. Existing world site roster is the sole permission owner.
        No inferred actor perception, notification, motive or account exit.
        """
        request_id=_text(request_id,'REQUEST_ID',120)
        site_ref=_text(site_ref,'SITE_REF',100)
        version,world=self._world()
        key=stable_id('neighbor_entry_surrender',{'user':self.user_id,'request':request_id})
        prior=world.get('neighbor_entry_surrenders',{}).get(key)
        if prior:
            if prior['site_ref']!=site_ref:
                raise EncounterRefusal('ENTRY_SURRENDER_REPLAY_CHANGED_PAYLOAD')
            return {'status':'SURRENDERED','surrender_ref':key,'idempotent_replay':True}
        site=world['sites'].get(site_ref)
        if not site or site.get('access')!='controlled':
            raise EncounterRefusal('NO_CONTROLLED_ENTRY_PERMISSION')
        admitted=site.get('admitted')
        if (type(admitted) is not list or any(type(x) is not str for x in admitted)
                or admitted.count(self.user_id)!=1):
            raise EncounterRefusal('NO_OWN_ENTRY_PERMISSION')
        person=world.get('neighbor_users',{}).get(self.user_id,{})
        if person.get('present') is True and person.get('location')==site_ref:
            raise EncounterRefusal('DEPART_BEFORE_SURRENDER')
        site['admitted']=[x for x in admitted if x!=self.user_id]
        row={'id':key,'user':self.user_id,'site_ref':site_ref,'clock':world['clock'],
             'controller_ref':site.get('controller'),'no_actor_receipt_inferred':True}
        world.setdefault('neighbor_entry_surrenders',{})[key]=row
        receipt=self.runtime.ledger.commit(self.runtime.world_id,version,world,{}, {},
            'NEIGHBOR_ENTRY_PERMISSION_SURRENDERED',None,deepcopy(row))
        return {'status':'SURRENDERED','surrender_ref':key,'receipt':receipt['id'],
                'idempotent_replay':False}

    def _destination_permitted(self, world, destination):
        """Consume the continuing world's actual site rule, not a notice.

        Existing routes still determine reachability; public access is not a
        route. An unknown/malformed admission roster cannot confer rights.
        """
        site = world['sites'][destination]
        admitted = site.get('admitted', [])
        return (site.get('access') == 'public' or
                (type(admitted) is list and
                 all(type(x) is str for x in admitted) and
                 self.user_id in admitted))

    def contribute(self, request_id: str, operation: str, *, text: str | None = None,
                   destination: str | None = None, target_object_ref: str | None = None,
                   cover_text: str | None = None,
                   target_actor_ref: str | None = None,
                   due_clock: int | None = None,
                   target_commitment_ref: str | None = None):
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
        if operation == 'LOOK':
            # Private ATTEND remains MII-only. LOOK is the actual outward
            # bodily attempt, which an Other may have opportunity to see.
            target_object_ref = _text(target_object_ref, 'LOOK_TARGET', 100)
            if cover_text is not None:
                cover_text = _text(cover_text, 'COVER_SPEECH')
        elif operation == 'REPAIR':
            target_object_ref = _text(target_object_ref, 'REPAIR_TARGET', 100)
            if cover_text is not None:
                raise EncounterRefusal('UNAUTHORED_REPAIR_SPEECH')
        elif target_object_ref is not None or cover_text is not None:
            raise EncounterRefusal('UNAUTHORED_LOOK_OR_COVER')
        if target_actor_ref is not None:
            if operation not in ('SAY', 'SING', 'OFFER_FEED', 'PLEDGE_OFFER', 'PROPOSE_MEETING'):
                raise EncounterRefusal('UNAUTHORED_VOCAL_ADDRESSEE')
            target_actor_ref = _text(target_actor_ref, 'VOCAL_ADDRESSEE', 100)
        if operation in ('OFFER_FEED','PLEDGE_OFFER','PROPOSE_MEETING') and target_actor_ref is None:
            raise EncounterRefusal('FOOD_OFFER_REQUIRES_ADDRESSEE')
        if operation in ('PLEDGE_OFFER','PROPOSE_MEETING'):
            if type(due_clock) is not int or due_clock<0:
                raise EncounterRefusal('INVALID_HUMAN_OFFER_DEADLINE')
        elif due_clock is not None:
            raise EncounterRefusal('UNAUTHORED_DEADLINE')
        if operation in ('WITHDRAW_PLEDGE','CHECK_IN_MEETING'):
            target_commitment_ref=_text(target_commitment_ref,'COMMITMENT_REF',100)
        elif target_commitment_ref is not None:
            raise EncounterRefusal('UNAUTHORED_COMMITMENT_TARGET')
        version, world = self._world()
        req_key = self.user_id + ':' + request_id
        request_payload = {'user': self.user_id, 'operation': operation,
                           'text': text, 'destination': destination}
        if operation == 'LOOK':
            # Preserve existing operation event IDs and old replay hashes.
            request_payload.update(target_object_ref=target_object_ref,
                                   cover_text=cover_text)
        elif operation == 'REPAIR':
            request_payload['target_object_ref'] = target_object_ref
        elif operation == 'SAY' and target_actor_ref is not None:
            request_payload['target_actor_ref'] = target_actor_ref
        elif operation in ('SING', 'OFFER_FEED', 'PLEDGE_OFFER','PROPOSE_MEETING'):
            request_payload['target_actor_ref'] = target_actor_ref
            if operation in ('PLEDGE_OFFER','PROPOSE_MEETING'):
                request_payload['due_clock']=due_clock
        if operation in ('WITHDRAW_PLEDGE','CHECK_IN_MEETING'):
            request_payload['target_commitment_ref']=target_commitment_ref
        payload_hash = digest(request_payload)
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
                    'idempotent_replay': True, 'receipt': existing,
                    **({'meeting_ref':prior['meeting_ref']} if prior.get('meeting_ref') else {}),
                    **({'made_object_ref':prior['made_object_ref']}
                       if prior.get('made_object_ref') is not None else {}),
                    **({'human_offer_commitment_ref':prior['human_offer_commitment_ref']}
                       if prior.get('human_offer_commitment_ref') is not None else {})}
        participants = world.setdefault('neighbor_users', {})
        person = deepcopy(participants.get(self.user_id, {'present': False, 'location': None}))
        origin = person['location']
        if operation not in ('MOVE','LEAVE','WITHDRAW_PLEDGE') and not person['present']:
            raise EncounterRefusal('USER_NOT_PRESENT')
        status = 'PERFORMED'
        material_outcome = None
        made_object_ref = None
        policy_ref = None
        # An explicitly authored administrative withdrawal is possible
        # during absence, but its historical occurrence is not a bodily
        # visit, utterance, or recipient-directed communication.
        loc = None if operation=='WITHDRAW_PLEDGE' else origin
        if operation=='WITHDRAW_PLEDGE':
            origin=None
            owned=[r for r in self.own_food_commitments() if r['id']==target_commitment_ref]
            if len(owned)!=1:
                raise EncounterRefusal('HUMAN_WITHDRAWAL_NO_OWN_COMMITMENT')
            if (owned[0]['status']!='PENDING'
                    or world['clock']+1>=owned[0]['due_clock']):
                raise EncounterRefusal('HUMAN_WITHDRAWAL_WINDOW_NOT_PENDING')
        meeting_ref=None
        meeting=None
        if operation=='CHECK_IN_MEETING':
            from um_sorok_organism.continuity_clock import qualify_meeting_checkin
            try:meeting=qualify_meeting_checkin(world,self.user_id,target_commitment_ref,loc)
            except ValueError as exc:raise EncounterRefusal(str(exc)) from exc
            # Authored presence at the agreed site; not evidence the actor is here.
            target_actor_ref=meeting['recipient']
        # Reuse CO's objective, source-qualified conjunction reader. Thin
        # worlds need no upstream packet; richer worlds may actually alter
        # the same authored operation. Unresolved authorization is not an
        # affirmative denial, even when neither permits a material effect.
        material_gate = None
        if operation in ('REPAIR', 'MAKE_OBJECT', 'SING', 'SIGN_HALL_PETITION', 'OFFER_FEED'):
            from um_sorok_organism.material_conjunction import evaluate_material_conjunction
            material_gate = evaluate_material_conjunction(
                world, self.user_id, loc, 'FEED' if operation == 'OFFER_FEED' else operation)
            if material_gate['readset']:
                world.setdefault('material_gate_audit', []).append({
                    'clock': world['clock']+1, 'actor': self.user_id,
                    'participant_kind': 'HUMAN_AUTHORED_NEIGHBOR',
                    'operation': operation, 'location': loc,
                    'evaluation': deepcopy(material_gate),
                    'not_participant_knowledge': True})
        if material_gate is not None and material_gate['decision'] in ('BLOCKED', 'UNRESOLVED'):
            status = 'BLOCKED'
            material_outcome = 'VISITOR_MATERIAL_ATTEMPT_NOT_AVAILABLE'
        elif operation == 'MOVE':
            if destination not in world['sites']:
                status = 'BLOCKED'
            elif not self._destination_permitted(world, destination):
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
        elif operation == 'LOOK':
            source = _bound_source(world)
            sight = source.get('user_conditions', {}).get(loc, {})
            candidate = _public_encounter_projection(world, loc).get(target_object_ref)
            # P6 outward ORIENT is a bodily attempt, NOT P6 INSPECT_OBJECT.
            # Keep the world-owned physical target/location/public status.
            # Do not ask visitor legibility or attention to authorize turning:
            # that is a separate, private, source-qualified MII operation.
            # Unknown, nonpublic and absent objects uniformly block the
            # object-targeted attempt, without emitting the cover sentence.
            if (type(candidate) is not dict or
                candidate.get('location') != loc or
                type(candidate.get('public_glance')) is not str):
                status = 'BLOCKED'
        elif operation in ('SAY', 'SING', 'OFFER_FEED', 'PLEDGE_OFFER','PROPOSE_MEETING') and target_actor_ref is not None:
            # Unaddressed singing is ordinary activity; only an explicitly
            # authored, presently accessible addressee can qualify a joint
            # occasion. The visitor cannot bind the addressee's response.
            sight = _bound_source(world).get('user_conditions', {}).get(loc, {})
            if (target_actor_ref not in self.runtime.ledger.actors()
                    or world['positions'].get(target_actor_ref) != loc
                    or sight.get('light') != 'lit'
                    or sight.get('sightline') != 'unobstructed'):
                status = 'BLOCKED'
            if operation == 'OFFER_FEED':
                from um_sorok_organism.material_provisioning import visitor_held_food_available
                if not visitor_held_food_available(world, self.user_id, loc):
                    status = 'BLOCKED'
        elif operation == 'SIGN_HALL_PETITION':
            # A human's authored contribution is not an actor policy or a
            # second vote for a constituted actor. The actual institution
            # owns opportunity, duplicate exclusion, quorum and policy.
            from um_sorok_organism.institutional_reproduction import (
                contribute_to_hall_petition)
            actual = contribute_to_hall_petition(world, self.user_id, loc)
            status = actual['status']
            material_outcome = actual['outcome']
            policy_ref = actual.get('policy_receipt')
        elif operation == 'MAKE_OBJECT':
            # A human-authored material contribution is not a generated
            # actor's technical power. The existing owner settles actual
            # stock, artifact identity and ownership. Explicit local grant
            # remains necessary even at a controllerless site.
            from um_sorok_organism.material_objects import produce_artifact
            sight = _bound_source(world).get('user_conditions', {}).get(loc, {})
            site = world.get('sites', {}).get(loc, {})
            grants = site.get('material_use_grants', [])
            if (type(grants) is list and self.user_id in grants
                    and sight.get('light') == 'lit'
                    and sight.get('sightline') == 'unobstructed'):
                actual = produce_artifact(world, self.user_id, loc)
                status = actual['status']
                material_outcome = actual['outcome']
                if status == 'PERFORMED':
                    made_object_ref = actual['object_ref']
            else:
                status = 'BLOCKED'
                material_outcome = 'VISITOR_MATERIAL_ATTEMPT_NOT_AVAILABLE'
        elif operation == 'REPAIR':
            # A thin human participant is not a registered synthetic actor.
            # Existing CO artifact settlement accepts a material worker ID.
            # Public entrance is not a grant to consume someone else's stock.
            # Even at a controllerless site require an explicit visitor grant.
            from um_sorok_organism.material_objects import repair_artifact
            source = _bound_source(world)
            sight = source.get('user_conditions', {}).get(loc, {})
            site = world.get('sites', {}).get(loc, {})
            grants = site.get('material_use_grants', [])
            target = world.get('material_objects', {}).get(target_object_ref)
            allowed = (type(grants) is list and self.user_id in grants
                       and type(target) is dict
                       and target.get('kind') == 'WORKED_MATERIAL_ARTIFACT'
                       and target.get('id') == target_object_ref
                       and target.get('location') == loc
                       and target.get('visible') is True
                       and target.get('grade') == GRADE
                       and sight.get('light') == 'lit'
                       and sight.get('sightline') == 'unobstructed')
            if allowed:
                actual = repair_artifact(world, self.user_id, loc, target_object_ref)
                status = actual['status']
                material_outcome = actual['outcome']
            else:
                status = 'BLOCKED'
                material_outcome = 'VISITOR_MATERIAL_ATTEMPT_NOT_AVAILABLE'
        # Existing continuity owner shares the same transaction as the
        # authored act. No discretionary human offer during absent passage.
        world['clock'] += 1
        if world.get('scheduled_obligations') or operation in ('PLEDGE_OFFER','OFFER_FEED'):
            from um_sorok_organism.continuity_clock import (
                settle_human_offer_deadlines, record_human_offer_commitment,
                record_authored_food_offer, withdraw_human_offer_commitment)
            settle_human_offer_deadlines(world)
        if (operation in ('PROPOSE_MEETING','CHECK_IN_MEETING')
                or any(row.get('kind')=='HUMAN_ACTOR_MEETING_WINDOW'
                       for row in world.get('scheduled_obligations',[]))):
            from um_sorok_organism.continuity_clock import (
                settle_meeting_deadlines, record_meeting_proposal, record_meeting_checkin, meeting_record)
            settle_meeting_deadlines(world)
        ref = stable_id('neighbor_user', {'user': self.user_id,
            'request_id': request_id, 'payload_hash': payload_hash})
        commitment_ref=None
        if status=='PERFORMED' and operation=='PLEDGE_OFFER':
            commitment_ref=record_human_offer_commitment(
                world,self.user_id,target_actor_ref,loc,due_clock,ref)
        elif status=='PERFORMED' and operation=='OFFER_FEED':
            commitment_ref=record_authored_food_offer(
                world,self.user_id,target_actor_ref,loc,ref)
        elif status=='PERFORMED' and operation=='WITHDRAW_PLEDGE':
            commitment_ref=withdraw_human_offer_commitment(
                world,self.user_id,target_commitment_ref,ref)
        if status=='PERFORMED' and operation=='PROPOSE_MEETING':
            meeting_ref=record_meeting_proposal(world,self.user_id,target_actor_ref,loc,due_clock,ref)
            meeting=meeting_record(world,meeting_ref)
        elif status=='PERFORMED' and operation=='CHECK_IN_MEETING':
            meeting=record_meeting_checkin(world,self.user_id,target_commitment_ref,loc,ref)
            meeting_ref=meeting['id']
        evidence = []
        if status == 'PERFORMED' and operation in ('MOVE', 'SAY', 'LOOK', 'REPAIR', 'MAKE_OBJECT', 'SIGN_HALL_PETITION', 'SING', 'OFFER_FEED', 'PLEDGE_OFFER','PROPOSE_MEETING','CHECK_IN_MEETING'):
            _bound_source(world)
            for actor_id, actor in self.runtime.ledger.actors().items():
                eligible = sensory_evidence(world, actor,
                    {'spoken_text': cover_text if operation == 'LOOK' else text},
                    operation, origin, loc, ref)
                for sign in eligible:
                    if operation in ('OFFER_FEED','PLEDGE_OFFER','PROPOSE_MEETING','CHECK_IN_MEETING') and actor_id != target_actor_ref:
                        # This scoped implementation only supplies the
                        # addressee's qualified offer; bystander witnessing
                        # remains a separate, unimplemented projection.
                        continue
                    # A transient user sound remains physically transient.
                    # R21's pre-action constitution read records the eligible
                    # cue ref; later *subjective* uptake must be separately
                    # earned by its competent owner. Extending the lifetime
                    # cannot authorize an actor memory or perception.
                    cue = add_cue(world, sign['kind'], sign['tags'],
                        location=loc, modality=sign['modality'],
                        description=sign['description'], source_actor=None,
                        private_to=actor_id)
                    if operation == 'SAY' and target_actor_ref is not None:
                        # The utterance is not the MII reader, and even a truthful
                        # acknowledgement is not evidence that the speaker heard
                        # the earlier sign. No private exposure/ref enters CO.
                        cue['visitor_event_ref'] = ref
                        sight = _bound_source(world)['actor_conditions'][actor_id]
                        visible_speaker = (sight.get('visual') is True
                            and sight.get('light') == 'lit'
                            and sight.get('sightline') == 'unobstructed'
                            and sight.get('facing') == 'entrance')
                        if (visible_speaker and actor['body'].get('language',0)>=.35):
                            cue['visitor_ref'] = self.user_id
                            if actor_id == target_actor_ref:
                                cue['visitor_speech_addressed_to_recipient'] = True
                        cue['lexical_comprehension'] = sign['lexical_comprehension']
                        cue['not_proof_of_speaker_recognition_or_claim_truth'] = True
                    if operation=='MAKE_OBJECT':
                        # Link the actual authored occurrence for audit;
                        # no inferred maker recognition or actor attention.
                        cue['visitor_event_ref'] = ref
                    if operation=='PLEDGE_OFFER':
                        cue.update(visitor_event_ref=ref,visitor_ref=self.user_id,
                                   commitment_ref=commitment_ref,due_clock=due_clock,
                                   no_recipient_consent_or_comprehension_established=True)
                    if operation in ('PROPOSE_MEETING','CHECK_IN_MEETING'):
                        cue.update(visitor_event_ref=ref,visitor_ref=self.user_id,
                                   meeting_ref=meeting_ref,checkin_clock=meeting['checkin_clock'],
                                   meeting_clock=meeting['meeting_clock'],
                                   no_future_presence_or_actor_consent_inferred=True)
                    if operation in ('SING', 'OFFER_FEED'):
                        # Actual human authorship is not a synthetic actor.
                        # Only a simultaneously eligible visual channel can
                        # bind this provisional encounter participant identity.
                        cue['visitor_event_ref'] = ref
                        if sign.get('visual_identity_eligible') is True:
                            cue['visitor_ref'] = self.user_id
                            if actor_id == target_actor_ref:
                                cue['visitor_vocal_addressed_to_recipient' if operation == 'SING'
                                    else 'visitor_food_addressed_to_recipient'] = True
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
        if operation == 'LOOK':
            event.update(target_object_ref=target_object_ref,
                         authored_cover_text=cover_text,
                         visitor_reading='NOT_ESTABLISHED',
                         other_actor_interpretation='NOT_ESTABLISHED',
                         user_look_is_not_private_mii_attend=True)
        if operation == 'MAKE_OBJECT':
            event.update(material_outcome=material_outcome,
                         made_object_ref=made_object_ref,
                         actor_meaning_not_established=True)
        if operation == 'REPAIR':
            event.update(target_object_ref=target_object_ref,
                         material_outcome=material_outcome,
                         actor_meaning_not_established=True)
        if (operation in ('SING', 'OFFER_FEED', 'PLEDGE_OFFER')
                or (operation=='SAY' and target_actor_ref is not None)):
            event['target_actor_ref'] = target_actor_ref
        if operation=='PLEDGE_OFFER':
            event['due_clock']=due_clock
        if operation in ('PROPOSE_MEETING','CHECK_IN_MEETING'):
            event['target_actor_ref']=target_actor_ref
            if operation=='PROPOSE_MEETING':event['due_clock']=due_clock
            else:event['target_commitment_ref']=target_commitment_ref
            if meeting_ref is not None:event['meeting_ref']=meeting_ref
        if operation=='WITHDRAW_PLEDGE':
            event.update(target_commitment_ref=target_commitment_ref,
                         administrative_act_not_presence=True,
                         notification='NOT_PERFORMED_BY_WITHDRAWAL')
        if commitment_ref is not None:
            event['human_offer_commitment_ref']=commitment_ref
        if operation == 'SIGN_HALL_PETITION':
            event.update(material_outcome=material_outcome,
                         institutional_policy_ref=policy_ref,
                         no_inferred_common_motive=True)
        if material_gate is not None and material_gate['readset']:
            # Analyst/world receipt only, not a visitor or actor concept.
            event['objective_material_gate_decision'] = material_gate['decision']
            event['objective_material_gate_source_refs'] = deepcopy(material_gate['readset'])
        world.setdefault('neighbor_user_events', []).append(event)
        world.setdefault('neighbor_user_requests', {})[req_key] = {
            'event_ref': ref, 'payload_hash': payload_hash, 'status': status,
            'ledger_receipt': None,
            **({'meeting_ref':meeting_ref} if meeting_ref is not None else {}),
            **({'made_object_ref':made_object_ref} if made_object_ref is not None else {}),
            **({'human_offer_commitment_ref':commitment_ref}
               if commitment_ref is not None else {})}
        receipt = self.runtime.ledger.commit(self.runtime.world_id, version, world,
            {}, {}, 'NEIGHBOR_USER_CONTRIBUTION', None,
            {'user_event_ref': ref, 'source': 'SOURCEFREE_USER_SUBMITTED',
             'user': self.user_id, 'payload_hash': payload_hash,
             'performed': status == 'PERFORMED',
             'candidate_cue_refs': [e['cue_ref'] for e in evidence],
             **({'meeting_ref':meeting_ref} if meeting_ref is not None else {}),
             **({'target_commitment_ref':target_commitment_ref}
                if operation=='WITHDRAW_PLEDGE' else {}),
             **({'made_object_ref':made_object_ref} if made_object_ref is not None else {}),
             'no_actor_motive_or_consent_issued': True,
             'look_cannot_issue_actor_belief_or_visitor_reading': operation == 'LOOK'})
        # The world record already contains durable request idempotency. Its
        # canonical event ref is the source for later actor reads, not this
        # returned envelope ID; never make a second write to attach it.
        return {'status': status, 'event_ref': ref, 'receipt': receipt['id'],
                'idempotent_replay': False, 'potential_actor_evidence': evidence,
                'actor_uptake': 'NOT_ESTABLISHED',
                **({'meeting_ref':meeting_ref} if meeting_ref is not None else {}),
                **({'made_object_ref':made_object_ref} if made_object_ref is not None else {}),
                **({'human_offer_commitment_ref':commitment_ref}
                   if commitment_ref is not None else {})}

    def own_food_commitments(self):
        """Own authored contract history, not another person's private life.

        Cross-check against the existing immutable contribution ledger.
        Reading does not advance time, acknowledge an offer or create a cue.
        """
        from um_sorok_organism.continuity_clock import HUMAN_OFFER_KIND
        _,world=self._world()
        history=self.runtime.ledger.events()
        committed={e['envelope']['payload'].get('user_event_ref'):e
                   for e in history if e['kind']=='NEIGHBOR_USER_CONTRIBUTION'
                   and e['envelope']['world']==self.runtime.world_id
                   and e['envelope']['payload'].get('user')==self.user_id
                   and e['envelope']['payload'].get('performed') is True}
        result=[]
        for row in world.get('scheduled_obligations',[]):
            if row.get('kind')!=HUMAN_OFFER_KIND or row.get('responsible_actor')!=self.user_id:
                continue
            event=committed.get(row['source_user_event_ref'])
            sources=[e for e in world.get('neighbor_user_events',[])
                     if e.get('event_ref')==row['source_user_event_ref']]
            if (event is None or len(sources)!=1
                    or sources[0].get('operation')!='PLEDGE_OFFER'
                    or sources[0].get('human_offer_commitment_ref')!=row['id']
                    or sources[0].get('target_actor_ref')!=row['recipient']
                    or sources[0].get('due_clock')!=row['due_clock']
                    or sources[0].get('clock')!=row['origin_clock']
                    or sources[0].get('payload_hash')!=event['envelope']['payload'].get('payload_hash')):
                raise EncounterRefusal('UNQUALIFIED_HUMAN_OFFER_COMMITMENT')
            if row['status']=='OFFER_AUTHORED_IN_WINDOW':
                f=committed.get(row['fulfillment_user_event_ref'])
                matching=[e for e in world.get('neighbor_user_events',[])
                          if e.get('event_ref')==row['fulfillment_user_event_ref']]
                if (f is None or len(matching)!=1
                        or matching[0].get('operation')!='OFFER_FEED'
                        or matching[0].get('human_offer_commitment_ref')!=row['id']
                        or matching[0].get('target_actor_ref')!=row['recipient']
                        or matching[0].get('clock')!=row['settled_at_clock']
                        or not row['origin_clock']<row['settled_at_clock']<row['due_clock']
                        or matching[0].get('payload_hash')!=f['envelope']['payload'].get('payload_hash')):
                    raise EncounterRefusal('UNQUALIFIED_HUMAN_OFFER_FULFILLMENT')
            if row['status']=='WITHDRAWN_BY_AUTHORED_ACT':
                f=committed.get(row.get('withdrawal_user_event_ref'))
                matching=[e for e in world.get('neighbor_user_events',[])
                          if e.get('event_ref')==row.get('withdrawal_user_event_ref')]
                if (f is None or len(matching)!=1
                        or matching[0].get('operation')!='WITHDRAW_PLEDGE'
                        or matching[0].get('target_commitment_ref')!=row['id']
                        or matching[0].get('human_offer_commitment_ref')!=row['id']
                        or matching[0].get('clock')!=row['settled_at_clock']
                        or not row['origin_clock']<row['settled_at_clock']<row['due_clock']
                        or matching[0].get('payload_hash')!=f['envelope']['payload'].get('payload_hash')
                        or f['envelope']['payload'].get('target_commitment_ref')!=row['id']
                        or matching[0].get('perceptual_candidates')!=[]):
                    raise EncounterRefusal('UNQUALIFIED_HUMAN_OFFER_WITHDRAWAL')
            result.append({k:deepcopy(row[k]) for k in (
                'id','recipient','location','origin_clock','due_clock','status',
                'source_user_event_ref','settled_at_clock',
                'fulfillment_user_event_ref','withdrawal_user_event_ref') if k in row})
        return result

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
                # Actor identity, private action and outcome stay in the
                # existing owner/ledger audit, not in visitor-facing return.
                # The finite MII surface is the *only* qualified observation.
                'owner_audit_remains_in_existing_ledger':True,
                'visitor_surface':view,
                'new_world_event':True,
                'no_visitor_selected_actor_intention_or_response':True,
                'no_unseen_private_psychology_on_visitor_surface':True,
                'grade':'SOURCEFREE_RESEARCH_PROVISIONAL'}

    def continue_present_life_until(self, occasion_ref: str, target_clock: int,
                                    *, max_beats: int = 24, profile=None):
        """Owner-side bounded continuation of a present, polycentric occasion.

        Absolute modeled clock, not wall time or visitor instruction to act.
        Existing initiative owns WHO, existing semantic runtime owns WHAT,
        and existing MII owns finite exposure after each committed beat.
        Recover interval counts from the ledger, not a new scheduler store.
        Serialized sourcefree driver: a new human contribution or other
        owner transition cuts this occasion; never silently replay a scene.
        """
        from um_sorok_organism.initiative import MAX_BEATS, choose_next_actor
        _text(occasion_ref, 'OCCASION_REF', 120)
        if type(target_clock) is not int or target_clock < 0:
            raise EncounterRefusal('INVALID_PRESENT_TARGET_CLOCK')
        if type(max_beats) is not int or not 1 <= max_beats <= MAX_BEATS:
            raise EncounterRefusal('INVALID_PRESENT_BEAT_BUDGET')
        if profile is not None and (type(profile) is not dict or
                profile.get('scope') != self.new_private_profile()['scope']):
            raise EncounterRefusal('MII_PROFILE_SCOPE_MISMATCH')

        def current_occasion():
            _, world = self._world()
            visitor = world.get('neighbor_users', {}).get(self.user_id)
            if not isinstance(visitor, dict) or visitor.get('present') is not True:
                raise EncounterRefusal('VISITOR_NOT_PRESENT_FOR_LIVE_OCCASION')
            history = self.runtime.ledger.events()
            matches = [(i,e) for i,e in enumerate(history)
                       if e.get('kind') == 'NEIGHBOR_USER_CONTRIBUTION'
                       and e.get('envelope',{}).get('world') == self.runtime.world_id
                       and e.get('envelope',{}).get('payload',{}).get('user') == self.user_id
                       and e.get('envelope',{}).get('payload',{}).get('performed') is True
                       and e.get('envelope',{}).get('payload',{}).get('user_event_ref') == occasion_ref]
            if len(matches) != 1:
                raise EncounterRefusal('NO_QUALIFIED_USER_LIFE_OCCASION')
            index, source = matches[0]
            rows = [e for e in world.get('neighbor_user_events',[])
                    if e.get('event_ref') == occasion_ref
                    and e.get('user') == self.user_id and e.get('status') == 'PERFORMED'
                    and e.get('clock') == source.get('clock')]
            if len(rows) != 1:
                raise EncounterRefusal('NO_QUALIFIED_USER_LIFE_OCCASION')
            suffix = history[index+1:]
            if any(e.get('kind') != 'ACTOR_LIFE_TRANSITION'
                   or e.get('envelope',{}).get('world') != self.runtime.world_id
                   for e in suffix):
                raise EncounterRefusal('PRESENT_OCCASION_INTERRUPTED')
            if target_clock < source['clock'] or target_clock-source['clock'] > MAX_BEATS:
                raise EncounterRefusal('PRESENT_OCCASION_HORIZON_OUT_OF_BOUNDS')
            counts = {}
            for event in suffix:
                aid = event.get('actor_id')
                if type(aid) is not str:
                    raise EncounterRefusal('PRESENT_OCCASION_UNQUALIFIED_ACTOR_EVENT')
                counts[aid] = counts.get(aid,0)+1
            return world, counts, len(suffix)

        world, counts, prior_beats = current_occasion()
        initial = world['clock']
        frames = []
        committed = 0
        while world['clock'] < target_clock and committed < max_beats:
            if prior_beats + committed >= MAX_BEATS:
                break
            decision = choose_next_actor(world, self.runtime.ledger.actors(), counts)
            if decision is None:
                break
            previous = world['clock']
            result = self.independent_actor_beat(decision['actor'])
            if result.get('selection_grade') == 'INJECTED_NOT_NATIVE_ACTOR_CHOICE':
                raise EncounterRefusal('LIVE_OCCASION_FORGED_ACTOR_SELECTION')
            committed += 1
            # An actual present surface must be read now, before it is
            # superseded. A retry does NOT fabricate missed exposures.
            world, counts, total = current_occasion()
            if total != prior_beats + committed or world['clock'] <= previous:
                raise EncounterRefusal('PRESENT_OCCASION_UNEXPECTED_OWNER_ADVANCE')
            if profile is not None:
                frames.append({'modeled_clock':world['clock'],
                               'visitor_surface':self.private_surface(profile)})
        current = world['clock']
        return {'status':('AT_OR_PAST_PRESENT_TARGET' if current >= target_clock
                          else 'HELD_AT_BOUNDED_PRESENT_CONTINUATION'),
                'source_user_event_ref':occasion_ref,
                'target_modeled_clock':target_clock,
                'actual_modeled_clock':current,
                'modeled_clock_advance_this_call':current-initial,
                'beats_committed_this_call':committed,
                'new_world_events':committed>0,
                'new_present_surfaces':frames,
                'no_unseen_history_reconstructed':True,
                'no_visitor_selected_actor_intention_or_response':True,
                'real_calendar_elapsed_not_established':True,
                'grade':'SOURCEFREE_RESEARCH_PROVISIONAL'}

    def _own_visit_transitions(self, world, history=None):
        """Derive visits from the existing committed contribution history.

        Repeated LEAVE while already absent is not a new departure; movement
        within a visit is not a new arrival. Match the world event to its
        existing ledger receipt rather than admitting an uncommitted record.
        """
        receipts = {}
        for row in (self.runtime.ledger.events() if history is None else history):
            env = row.get('envelope', {})
            payload = env.get('payload', {})
            if (row.get('kind') == 'NEIGHBOR_USER_CONTRIBUTION'
                    and env.get('world') == self.runtime.world_id
                    and payload.get('user') == self.user_id
                    and payload.get('performed') is True):
                receipts[payload.get('user_event_ref')] = (row, payload)
        present = False
        arrival = departure = None
        for event in world.get('neighbor_user_events', []):
            if (event.get('user') != self.user_id
                    or event.get('status') != 'PERFORMED'
                    or event.get('operation') not in ('MOVE', 'LEAVE')):
                continue
            ref = event.get('event_ref')
            source = receipts.get(ref)
            authored = {'user': self.user_id, 'operation': event['operation'],
                        'text': None, 'destination': (
                            event.get('destination') if event['operation'] == 'MOVE'
                            else None)}
            if (source is None or source[0].get('clock') != event.get('clock')
                    or source[1].get('payload_hash') != event.get('payload_hash')
                    or digest(authored) != event.get('payload_hash')
                    or ref != stable_id('neighbor_user', {
                        'user': self.user_id, 'request_id': event.get('request_id'),
                        'payload_hash': event.get('payload_hash')})):
                raise EncounterRefusal('VISIT_TRANSITION_WITHOUT_COMMITTED_SOURCE')
            if event['operation'] == 'MOVE' and not present:
                present = True
                arrival = event
            elif event['operation'] == 'LEAVE' and present:
                present = False
                departure = event
        if present != bool(world.get('neighbor_users', {}).get(
                self.user_id, {}).get('present')):
            raise EncounterRefusal('VISIT_HISTORY_PRESENCE_CONFLICT')
        return arrival, departure, present

    def continue_absent_life_until(self, departure_ref: str, target_clock: int,
                                   *, max_segments: int = 24,
                                   period_processes=None):
        """Owner-side bounded absence continuation, NOT a visitor action.

        The target is an absolute modeled-world clock, not real wall time or
        permission to invent a private diary. A retry after committed progress
        resumes only the remaining interval. Existing CO discontinuities,
        ordinary passage and autonomous initiative do all life writing.
        This is a serialized sourcefree research driver; a real multi-user
        calendar/authorization service is not supplied by this interface.
        """
        from um_sorok_organism.continuity_clock import (
            MAX_HORIZON, next_discontinuity)
        _text(departure_ref, 'DEPARTURE_REF', 120)
        if type(target_clock) is not int or target_clock < 0:
            raise EncounterRefusal('INVALID_ABSENCE_TARGET_CLOCK')
        if type(max_segments) is not int or not 1 <= max_segments <= 240:
            raise EncounterRefusal('INVALID_ABSENCE_SEGMENT_BUDGET')
        # Owner-side only: these are already source-qualified routine
        # premises, not visitor choices of what another person does.
        # Existing CO allocation requalifies them at every actual interval.
        if period_processes is not None:
            from um_sorok_organism.historical_social_reproduction import KINDS
            if (type(period_processes) is not list or len(period_processes)>512
                    or any(type(p) is not dict or p.get('kind') not in KINDS
                           for p in period_processes)):
                raise EncounterRefusal('INVALID_ABSENCE_PERIOD_PROCESSES')
        period_kw=({'processes':deepcopy(period_processes)}
                   if period_processes is not None else {})
        _, world = self._world()
        _, departure, present = self._own_visit_transitions(world)
        if (present or departure is None
                or departure['event_ref'] != departure_ref):
            raise EncounterRefusal('NO_CURRENT_QUALIFIED_DEPARTURE')
        if target_clock < departure['clock']:
            raise EncounterRefusal('ABSENCE_TARGET_PRECEDES_DEPARTURE')
        if target_clock - world['clock'] > MAX_HORIZON:
            raise EncounterRefusal('ABSENCE_HORIZON_EXCEEDS_OWNER_BOUND')

        def require_no_visitors(w):
            if any(row.get('present') is True
                   for row in w.get('neighbor_users', {}).values()):
                raise EncounterRefusal('WORLD_HAS_PRESENT_VISITOR')

        require_no_visitors(world)
        initial = world['clock']
        segments = 0
        while world['clock'] < target_clock and segments < max_segments:
            require_no_visitors(world)
            previous = world['clock']
            remaining = target_clock - previous
            actors = self.runtime.ledger.actors()
            discontinuity = next_discontinuity(world, actors, remaining)
            if discontinuity is not None:
                # This owner may settle an actor event at the horizon itself,
                # advancing one additional tick. Report actual clock, never
                # backdate reentry to the requested cut.
                self.runtime.advance_to_discontinuity(horizon=remaining,**period_kw)
            elif remaining > 1:
                # Leave one tick for a real independently chosen activity,
                # instead of narrating all ordinary life from elapsed time.
                self.runtime.advance_to_discontinuity(horizon=remaining - 1,**period_kw)
            elif actors:
                self.runtime.continue_without_user(beats=1)
            else:
                self.runtime.advance_to_discontinuity(horizon=1,**period_kw)
            _, world = self._world()
            segments += 1
            if world['clock'] <= previous:
                break
        current = world['clock']
        return {
            'status': ('AT_OR_PAST_ABSENCE_TARGET' if current >= target_clock
                       else 'HELD_AT_BOUNDED_ABSENCE_CONTINUATION'),
            'departure_event_ref': departure_ref,
            'target_modeled_clock': target_clock,
            'actual_modeled_clock': current,
            'modeled_clock_advance_this_call': current - initial,
            'segments_executed_this_call': segments,
            'new_world_events': current > initial,
            'unseen_life_not_a_visitor_report': True,
            'real_calendar_elapsed_not_established': True,
            'grade': 'SOURCEFREE_RESEARCH_PROVISIONAL',
        }

    def _actual_look_receipt(self, world, history, selected, ref, clock, location):
        """Existing one-world outward LOOK identity, not a claim of reading."""
        rows = [e for e in world.get('neighbor_user_events', [])
                if e.get('event_ref') == ref and e.get('user') == self.user_id
                and e.get('clock') == clock and e.get('destination') == location
                and e.get('operation') == 'LOOK' and e.get('status') == 'PERFORMED'
                and e.get('target_object_ref') == selected]
        if len(rows) != 1:
            return None
        event = rows[0]
        receipts = [e for e in history
                    if e.get('kind') == 'NEIGHBOR_USER_CONTRIBUTION'
                    and e.get('clock') == clock
                    and e.get('envelope', {}).get('world') == self.runtime.world_id
                    and e.get('envelope', {}).get('payload', {}).get('user_event_ref') == ref
                    and e['envelope']['payload'].get('user') == self.user_id
                    and e['envelope']['payload'].get('payload_hash') == event.get('payload_hash')
                    and e['envelope']['payload'].get('performed') is True]
        return receipts[0]['id'] if len(receipts) == 1 else None

    def _presented_recognition(self, world, history, profile, selected, offered,
                               committed_look, close_granted):
        """Bridge the existing P6 earned-recognition contract to CO LOOK
        plus private MII close presentation. A LOOK alone is not inspection.
        This only qualifies a sourcefree familiar marking currently visible,
        not the real human's memory, expertise, or comprehension.
        """
        if selected not in offered:
            return {}, None
        obj=world.get('material_objects',{}).get(selected,{})
        mark=obj.get('public_recognition')
        if (obj.get('grade')!='SOURCEFREE_TEST_ONLY'
                or obj.get('kind') in ('WORKED_MATERIAL_ARTIFACT', 'INCIDENTALLY_EXPOSED_DOCUMENT')
                or type(mark) is not dict
                or set(mark)!= {'identity','marking','evidence'}
                or any(type(v) is not str or not v.strip() or len(v)>200
                       for v in mark.values())
                or type(obj.get('public_close')) is not str
                or mark['evidence'] not in obj['public_close']
                or mark['evidence'] not in offered[selected]):
            return {}, None
        # A changed marking/label cannot inherit an old inspection.
        fingerprint=self.mii.digest({'object':selected, 'recognition':mark})
        def actual_look(ref,clock,location):
            return self._actual_look_receipt(world, history, selected, ref, clock, location)
        receipt=None; exposure_ref=None; origin_clock=None
        if close_granted and committed_look is not None:
            origin_clock=committed_look['clock']
            receipt=actual_look(committed_look['event_ref'],origin_clock,
                                committed_look['destination'])
        # Do not trust recognized/seen cache. MII cold normalization clears
        # it; reconstruct only from an earlier actually offered close and
        # its matching world LOOK. App-trusted sidecar, not authentication.
        if receipt is None:
            for entry in reversed(profile.get('exposures',[])):
                if type(entry) is not dict:continue
                context=entry.get('context',{})
                previous=entry.get('offered',{})
                if (entry.get('scope')!=profile['scope']
                        or entry.get('selected')!=selected
                        or context.get('world')!=self.runtime.world_id
                        or context.get('recognition_source_fingerprint')!=fingerprint
                        or context.get('user_close_granted_by_mii') is not True
                        or type(entry.get('clock')) is not int
                        or entry['clock']>=world['clock']
                        or type(previous.get(selected)) is not str
                        or mark['evidence'] not in previous[selected]
                        or entry.get('entry_hash')!=self.mii.digest(
                            {k:v for k,v in entry.items() if k!='entry_hash'})):
                    continue
                receipt=actual_look(entry.get('request_id'),entry['clock'],context.get('room'))
                if receipt is not None:
                    exposure_ref=entry['exposure_id'];origin_clock=entry['clock'];break
        if receipt is None:return {},None
        row={'object_id':selected,**deepcopy(mark),'event_id':receipt,
             'turn':origin_clock,'recognition_source':'QUALIFIED_PRIVATE_CLOSE_PRESENTATION',
             'human_recognition_not_established':True,
             'present_marking_required':True}
        if exposure_ref is not None:row['prior_exposure_ref']=exposure_ref
        return {selected:row},fingerprint if close_granted else None

    def private_surface(self, profile: dict, *, command: str | None = None,
                        target: str | None = None):
        """Project the existing CO world into the *existing* protected MII reader.

        P6 makes outward ORIENT and close INSPECT distinct operations. A user
        can turn toward a public object without reading it. The world records
        the bodily attempt; MII alone qualifies visitor availability and
        optional close detail; CO alone owns any actor-local interpretation.
        This projection does not install a rival P6 world or MII profile store.
        """
        if self.mii is None:
            raise EncounterRefusal('MII_READER_NOT_INSTALLED')
        if (type(profile) is not dict or
                profile.get('scope') != self.new_private_profile()['scope']):
            raise EncounterRefusal('MII_PROFILE_SCOPE_MISMATCH')
        _, world = self._world()
        visitor = world.get('neighbor_users', {}).get(self.user_id)
        if not visitor or not visitor['present']:
            raise EncounterRefusal('USER_NOT_PRESENT')
        loc = visitor['location']
        source = _bound_source(world)
        user_view = source.get('user_conditions', {}).get(loc, {})
        audible = (user_view.get('hearing') is True and
                   user_view.get('sound_path') == 'audible')
        # Translate the precommitted, sourcefree world conditions into the
        # already protected P6/MII availability interface. This is a
        # READ-ONLY projection, NOT a second source or an adopted sensor law.
        # MII, not NeighborEncounter, decides glance versus close eligibility.
        published = _public_encounter_projection(world, loc)
        mii_house = {
            'presentation_conditions': {
                'grade': 'SOURCEFREE_FIXTURE',
                'observer': self.user_id,
                'light': user_view.get('light', 'unknown'),
                'sightline': user_view.get('sightline', 'unknown'),
                'legibility': user_view.get('legibility', 'unknown'),
                'objects': {},
            },
            'objects': {key: {'room': obj.get('location')}
                        for key, obj in published.items()},
        }
        available = self.mii.candidate_details(
            mii_house, loc, {key: obj['public_glance']
                             for key, obj in published.items()}, self.user_id)
        selected, basis = self.mii.select_detail(
            available, profile, command=command, target=target, offered=available)
        offered = {selected: available[selected]} if selected in available else {}
        # A close reading requires ALL of: actual world-owned LOOK, correct
        # user + target + world clock, source-graded public close text,
        # and MII's *existing* close availability. The actor sees none of
        # these private eligibility/attention facts.
        committed_look = next((
            event for event in reversed(world.get('neighbor_user_events', []))
            if event.get('user') == self.user_id
            and event.get('operation') == 'LOOK'
            and event.get('status') == 'PERFORMED'
            and event.get('target_object_ref') == selected
            and event.get('destination') == loc
            and event.get('clock') == world['clock']
        ), None) if command == 'look' and target == selected else None
        history = self.runtime.ledger.events()
        look_receipt = None
        if committed_look is not None and selected in offered:
            look_receipt = self._actual_look_receipt(
                world, history, selected, committed_look['event_ref'],
                committed_look['clock'], loc)
        if (committed_look is not None and selected in offered
                and published[selected].get('grade') == 'SOURCEFREE_TEST_ONLY'
                and type(published[selected].get('public_close')) is str
                and (published[selected].get('source_kind') != 'INCIDENTALLY_EXPOSED_DOCUMENT'
                     or look_receipt is not None)
                and self.mii.close_available(mii_house, self.user_id, selected)):
            offered[selected] = published[selected]['public_close']
        visible_identity = (self.mii.glance_available(mii_house, self.user_id)
                            and user_view.get('sightline') == 'unobstructed')
        mandatory = [{'kind': 'LOCATION', 'text': loc}]
        for actor_id, actor_loc in sorted(world['positions'].items()):
            if visible_identity and actor_loc == loc:
                mandatory.append({'kind': 'CO_PRESENT_ACTOR',
                                  'actor_ref': actor_id, 'interpretation': 'NONE'})
        # Existing CO world.resolve publishes a modality-typed performed_*
        # sign and public_history row, while runtime.step binds that occurrence
        # to the immutable ACTOR_LIFE_TRANSITION. Read those actual producers,
        # not the process-local generated prose. This is a finite MII exposure
        # of the present occurrence, NOT historical reconstruction or a new
        # sensory world. The sound itself does not encode words or identity.
        last_event = history[-1]
        envelope = last_event.get('envelope', {})
        actual = envelope.get('payload', {}).get('actual', {})
        current_clock = world['clock']
        # A partial joint settlement may contain an actually enacted signal.
        # Only the CO owner's explicit performed-prefix receipt can qualify
        # it; an arbitrary partial attempt, plan or narration cannot.
        directed_signal = (last_event.get('kind') == 'ACTOR_LIFE_TRANSITION'
                and last_event.get('clock') == current_clock
                and envelope.get('world') == self.runtime.world_id
                and type(actual) is dict and actual.get('clock') == current_clock
                and actual.get('actor') == last_event.get('actor_id')
                and envelope.get('payload',{}).get('actor_selection_grade')
                    == 'ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE'
                and actual.get('action') == 'SIGNAL'
                and actual.get('status') in ('PERFORMED','PARTIAL')
                and actual.get('target') in world.get('neighbor_users', {})
                and actual.get('human_directed_signal_prefix_performed') is True
                and world.get('public_history') and world.get('cues'))
        if directed_signal:
            public = world['public_history'][-1]
            cue = world['cues'][-1]
            prefix_ref = actual.get('human_directed_signal_cue_ref')
            if (type(prefix_ref) is str
                    and public.get('human_directed_signal_cue_ref') == prefix_ref
                    and public.get('human_directed_signal_prefix_performed') is True
                    and all(public.get(k) == actual.get(k) for k in
                            ('actor','target','action','status','clock'))
                    and cue.get('id') == prefix_ref
                    and cue.get('kind') == 'performed_signal'
                    and cue.get('human_directed_signal_prefix_performed') is True
                    and cue.get('source_actor') == actual['actor']
                    and cue.get('clock') == current_clock
                    and cue.get('last_access_clock',-1) >= current_clock
                    and cue.get('location') == loc
                    and cue.get('modality') == 'auditory'
                    and cue.get('private_to') is None):
                if audible:
                    addressed = (visible_identity and actual['target'] == self.user_id)
                    mandatory.append({'kind':'CO_PUBLIC_OCCURRENCE',
                        'text': ('A signal is directed toward you.' if addressed
                                 else 'A signal sounds nearby.'),
                        'modality':'auditory',
                        'source_event_ref':last_event['id'],
                        'source_cue_ref':prefix_ref,
                        'source':'EXISTING_CO_PERFORMED_SIGNAL_PREFIX',
                        'speaker_identity':'NOT_ESTABLISHED',
                        'lexical_content':'NOT_CAPTURED_OR_RECONSTRUCTED',
                        'interpretation':'NONE'})
                # A visible material handoff is not inferred from the sound.
                # It requires this visitor's own actual offer, exact material
                # settlement and a separately committed, locally visible sign.
                if (visible_identity and actual['target'] == self.user_id
                        and actual['status'] == 'PERFORMED'
                        and actual.get('outcome') == 'JOINT_ACTIVITY_PERFORMED'):
                    transfer_ref = actual.get('human_food_transfer_cue_ref')
                    feeding_ref = actual.get('material_feeding_ref')
                    offer_ref = actual.get('human_food_offer_event_ref')
                    if (all(type(x) is str and x for x in
                            (transfer_ref, feeding_ref, offer_ref))
                            and public.get('human_food_transfer_cue_ref') == transfer_ref
                            and public.get('material_feeding_ref') == feeding_ref
                            and public.get('human_food_offer_event_ref') == offer_ref):
                        signs = [c for c in world['cues']
                                 if c.get('id') == transfer_ref]
                        settlements = [e for e in world.get('material_feeding_events',[])
                                       if e.get('id') == feeding_ref]
                        offers = [e for e in world.get('neighbor_user_events',[])
                                  if e.get('event_ref') == offer_ref]
                        if len(signs)==len(settlements)==len(offers)==1:
                            sign, settlement, offer = signs[0], settlements[0], offers[0]
                            prev = history[-2] if len(history)>1 else {}
                            prior = prev.get('envelope',{}).get('payload',{})
                            if (sign.get('kind')=='performed_human_food_transfer'
                                    and sign.get('modality')=='visual'
                                    and sign.get('private_to')==self.user_id
                                    and sign.get('source_actor')==actual['actor']
                                    and sign.get('location')==loc
                                    and sign.get('clock')==current_clock
                                    and sign.get('last_access_clock',-1)>=current_clock
                                    and sign.get('material_feeding_ref')==feeding_ref
                                    and sign.get('human_offer_event_ref')==offer_ref
                                    and settlement.get('clock')==current_clock
                                    and settlement.get('giver')==self.user_id
                                    and settlement.get('recipient')==actual['actor']
                                    and settlement.get('site')==loc
                                    and settlement.get('human_authored_offer_ref')==offer_ref
                                    and settlement.get('food_source')=='GIVER_HELD_FOOD'
                                    and settlement.get('food_consumed')==1
                                    and settlement.get('recipient_independently_accepted') is True
                                    and offer.get('user')==self.user_id
                                    and offer.get('target_actor_ref')==actual['actor']
                                    and offer.get('operation')=='OFFER_FEED'
                                    and offer.get('status')=='PERFORMED'
                                    and offer.get('destination')==loc
                                    and offer.get('clock')==current_clock-1
                                    and prev.get('kind')=='NEIGHBOR_USER_CONTRIBUTION'
                                    and prev.get('clock')==current_clock-1
                                    and prev.get('envelope',{}).get('world')==self.runtime.world_id
                                    and prior.get('user_event_ref')==offer_ref
                                    and prior.get('user')==self.user_id
                                    and prior.get('performed') is True
                                    and prior.get('payload_hash')==offer.get('payload_hash')):
                                mandatory.append({'kind':'CO_PUBLIC_OCCURRENCE',
                                    'text':'The offered food is taken.',
                                    'modality':'visual',
                                    'source_event_ref':last_event['id'],
                                    'source_cue_ref':transfer_ref,
                                    'source':'EXISTING_CO_MATERIAL_SETTLEMENT_SIGN',
                                    'interpretation':'NONE'})
        if (not directed_signal and last_event.get('kind') == 'ACTOR_LIFE_TRANSITION'
                and last_event.get('clock') == current_clock
                and envelope.get('world') == self.runtime.world_id
                and type(actual) is dict and actual.get('clock') == current_clock
                and actual.get('actor') == last_event.get('actor_id')
                and actual.get('status') == 'PERFORMED'
                and world.get('public_history') and world.get('cues')):
            historical_public = world['public_history'][-1]
            cue = world['cues'][-1]
            action = actual.get('action')
            # CO currently appends exactly one primary sign as the last cue
            # for this world resolution; refuse mismatches rather than guess.
            # Both the committed public row and the cue must agree with the
            # transition. Never expose the objective audit payload or tags.
            if (type(action) is str and type(historical_public) is dict
                    and historical_public.get('actor') == actual.get('actor')
                    and historical_public.get('clock') == current_clock
                    and historical_public.get('action') == action
                    and historical_public.get('status') == 'PERFORMED'
                    and type(cue) is dict and type(cue.get('id')) is str
                    and cue.get('kind') == 'performed_' + action.lower()
                    and cue.get('source_actor') == actual.get('actor')
                    and cue.get('clock') == current_clock
                    and cue.get('last_access_clock', -1) >= current_clock
                    and cue.get('location') == loc
                    and cue.get('private_to') is None):
                # The existing owner qualifies these four actions as
                # auditory; descriptions of outcomes are NOT spoken text.
                # A nearby sound is not recognition of its source or meaning.
                sounds = {'SPEAK': 'Speech sounds nearby.',
                          'SING': 'Singing sounds nearby.',
                          'SIGNAL': 'A signal sounds nearby.',
                          'ASK': 'Speech sounds nearby.'}
                movements = {'MOVE': 'Someone moves nearby.',
                             'ORIENT': 'Someone turns nearby.'}
                if (audible and cue.get('modality') == 'auditory'
                        and action in sounds):
                    # R47 emits a physical vocal manner, not private affect.
                    # Only this committed, presently audible sign may carry it.
                    text = sounds[action]
                    if action == 'SPEAK':
                        from um_sorok_organism.expectation_afterlife import CADENCES
                        cadence = cue.get('vocal_cadence')
                        if (type(cadence) is str and cadence in CADENCES
                                and cue.get('description') == CADENCES[cadence]
                                and ('vocal_cadence:' + cadence.lower()) in cue.get('tags', [])):
                            text = CADENCES[cadence]
                    mandatory.append({'kind': 'CO_PUBLIC_OCCURRENCE',
                        'text': text, 'modality': 'auditory',
                        'source_event_ref': last_event['id'],
                        'source_cue_ref': cue['id'],
                        'source': 'EXISTING_CO_PUBLIC_WORLD_SIGN',
                        'speaker_identity': 'NOT_ESTABLISHED',
                        'lexical_content': 'NOT_CAPTURED_OR_RECONSTRUCTED',
                        'interpretation': 'NONE'})
                elif (visible_identity and cue.get('modality') == 'visual'
                        and action in movements):
                    mandatory.append({'kind': 'CO_PUBLIC_OCCURRENCE',
                        'text': movements[action], 'modality': 'visual',
                        'source_event_ref': last_event['id'],
                        'source_cue_ref': cue['id'],
                        'source': 'EXISTING_CO_PUBLIC_WORLD_SIGN',
                        'interpretation': 'NONE'})
        # R19: a particular material offer can be refused, independently of
        # its benefit. Do not interpret silence, WAIT, or a generic refusal
        # as a response to this human's offer. Only the actual source-bound
        # outward event qualifies, in the giver's current visual field.
        if (visible_identity and last_event.get('kind')=='ACTOR_LIFE_TRANSITION'
                and last_event.get('clock')==current_clock
                and envelope.get('world')==self.runtime.world_id
                and type(actual) is dict and actual.get('clock')==current_clock
                and actual.get('actor')==last_event.get('actor_id')
                and actual.get('action')=='REFUSE'
                and actual.get('status')=='PERFORMED'
                and actual.get('target')==self.user_id
                and actual.get('outcome')=='PARTICULAR_HUMAN_FOOD_OFFER_REFUSED'
                and envelope.get('payload',{}).get('actor_selection_grade')
                    =='ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE'
                and world.get('public_history') and world.get('cues')):
            public=world['public_history'][-1]
            cue=world['cues'][-1]
            offer_ref=actual.get('human_food_offer_refused_event_ref')
            sign_ref=actual.get('human_food_refusal_cue_ref')
            prev=history[-2] if len(history)>1 else {}
            prior=prev.get('envelope',{}).get('payload',{})
            offers=[e for e in world.get('neighbor_user_events',[])
                    if e.get('event_ref')==offer_ref]
            if (type(offer_ref) is str and type(sign_ref) is str
                    and len(offers)==1
                    and all(public.get(k)==actual.get(k) for k in
                        ('clock','actor','target','action','status','outcome',
                         'human_food_offer_refused_event_ref','human_food_refusal_cue_ref'))
                    and cue.get('id')==sign_ref
                    and cue.get('kind')=='performed_refuse'
                    and cue.get('source_actor')==actual['actor']
                    and cue.get('human_food_offer_refused_event_ref')==offer_ref
                    and cue.get('clock')==current_clock
                    and cue.get('last_access_clock',-1)>=current_clock
                    and cue.get('location')==loc
                    and cue.get('modality')=='visual'
                    and cue.get('private_to') is None
                    and actual.get('material_feeding_ref') is None
                    and not any(x.get('human_authored_offer_ref')==offer_ref
                                for x in world.get('material_feeding_events',[]))
                    and prev.get('kind')=='NEIGHBOR_USER_CONTRIBUTION'
                    and prev.get('clock')==current_clock-1
                    and prev.get('envelope',{}).get('world')==self.runtime.world_id
                    and prior.get('user_event_ref')==offer_ref
                    and prior.get('user')==self.user_id
                    and prior.get('performed') is True):
                offer=offers[0]
                if (offer.get('user')==self.user_id
                        and offer.get('target_actor_ref')==actual['actor']
                        and offer.get('operation')=='OFFER_FEED'
                        and offer.get('status')=='PERFORMED'
                        and offer.get('destination')==loc
                        and offer.get('clock')==current_clock-1
                        and prior.get('payload_hash')==offer.get('payload_hash')):
                    mandatory.append({'kind':'CO_PUBLIC_OCCURRENCE',
                        'text':'The offered food is declined.',
                        'modality':'visual','source_event_ref':last_event['id'],
                        'source_cue_ref':sign_ref,
                        'source':'EXISTING_CO_PARTICULAR_REFUSAL_SIGN',
                        'interpretation':'NONE'})
        # R27's existing branch-local common-occurrence admission produces
        # an actual sourcefree auditory sign, NOT verified real-world news
        # or a scripted event with an assigned actor response. Receive only
        # the committed local sign. Do not render its analyst description as
        # spoken words or expose its proposal's required actor locations.
        if (audible and last_event.get('kind') == 'SOURCEFREE_CONTINGENT_WORLD_NOTICE'
                and last_event.get('clock') == current_clock
                and envelope.get('world') == self.runtime.world_id
                and world.get('cues')):
            source_receipt = envelope.get('payload', {})
            cue = world['cues'][-1]
            if (type(source_receipt) is dict
                    and source_receipt.get('independent_branch_eligibility')
                        == 'ELIGIBLE_SOURCEFREE_NOTICE_ONLY'
                    and source_receipt.get('not_proof_of_current_real_world_event') is True
                    and source_receipt.get('grade') == GRADE
                    and type(cue) is dict and type(cue.get('id')) is str
                    and cue['id'] == source_receipt.get('cue_ref')
                    and type(cue.get('contingent_offer_id')) is str
                    and cue['contingent_offer_id'] == source_receipt.get('offer_id')
                    and type(cue.get('contingent_offer_hash')) is str
                    and cue['contingent_offer_hash'] == source_receipt.get('proposal_hash')
                    and cue.get('external_sign_only_not_verified_news_or_world_damage') is True
                    and cue.get('clock') == current_clock
                    and cue.get('last_access_clock', -1) >= current_clock
                    and cue.get('location') == loc
                    and cue.get('modality') == 'auditory'
                    and cue.get('source_actor') is None
                    and cue.get('private_to') is None):
                mandatory.append({'kind': 'CO_PUBLIC_OCCURRENCE',
                    'text': 'An external sound is audible nearby.',
                    'modality': 'auditory',
                    'source_event_ref': last_event['id'],
                    'source_cue_ref': cue['id'],
                    'source': 'EXISTING_CO_BRANCH_LOCAL_CONTINGENT_SIGN',
                    'lexical_content': 'NOT_CAPTURED_OR_RECONSTRUCTED',
                    'external_event_truth': 'NOT_ESTABLISHED',
                    'interpretation': 'NONE'})
        if self._last_actor_tip is not None:
            receipt, at_clock, tip = self._last_actor_tip
            actor_location = world['positions'].get(self._last_actor_ref)
            # A CO public_tip is generic prose, NOT a modality-typed emitted
            # sound. Audibility alone cannot turn a silent world action into
            # heard speech or grant the visitor an actor's internal report.
            # Preserve R2's visible expression only when it is tied to this
            # exact actual one-world actor transition. A future source-typed
            # auditory expression needs MIII/CO owner receiving.
            last = last_event
            # This scoped interaction has typed enacted signs. Do not let
            # an untyped prose tip substitute for a blocked/unheard signal
            # or disclose the actor's private conditions of acceptance.
            human_signal_attempt = (type(actual) is dict
                and actual.get('action')=='SIGNAL'
                and actual.get('target') in world.get('neighbor_users',{}))
            particular_refusal = (type(actual) is dict
                and actual.get('action')=='REFUSE'
                and actual.get('human_food_offer_refused_event_ref') is not None)
            if (not human_signal_attempt and not particular_refusal
                    and visible_identity and actor_location == loc
                    and at_clock == world['clock']
                    and last['id'] == receipt
                    and last['kind'] == 'ACTOR_LIFE_TRANSITION'
                    and last['actor_id'] == self._last_actor_ref
                    and last['clock'] == world['clock']
                    and last['envelope'].get('world') == self.runtime.world_id
                    and type(tip) is str and tip.strip()):
                mandatory.append({'kind': 'PUBLIC_TIP', 'text': tip[:500],
                                  'source': 'EXISTING_ORGANISM_PUBLIC_EXPRESSION',
                                  'modality_grade': 'SOURCEFREE_VISUAL_ONLY_UNTYPED'})
        close_granted=bool(committed_look and selected in offered
                           and offered[selected]!=available[selected])
        earned,recognition_fingerprint=self._presented_recognition(
            world,history,profile,selected,offered,committed_look,close_granted)
        self.mii.merge_recognition(profile,earned)
        recognition={selected:self.mii.recognized_for(profile,selected)} if earned else {}
        view = self.mii.surface(room=loc, orientation='SOURCEFREE_UNKNOWN',
            exit_name='SOURCEFREE_UNQUALIFIED', available=available,
            candidates=available, offered=offered, selected=selected,
            basis=basis, narration=mandatory, recognition=recognition)
        # On actual reentry expose only the visitor's own elapsed modeled
        # interval, not the intervening actor audit, motives or a retrospective
        # story. Subsequent LOOK can disclose currently accessible changes.
        arrival, departure, present = self._own_visit_transitions(world, history)
        if (present and arrival is not None and departure is not None
                and arrival['clock'] == world['clock']
                and arrival['clock'] > departure['clock']):
            view['return_context'] = {
                'departure_event_ref': departure['event_ref'],
                'arrival_event_ref': arrival['event_ref'],
                'modeled_clock_difference': arrival['clock'] - departure['clock'],
                'real_calendar_elapsed_not_established': True,
                'intervening_life_not_disclosed': True,
            }
        # Explicitly distinguish a received institutional assertion from
        # the world's real policy or a successful application. This metadata
        # is recorded by MII with the actual finite exposure, never actor state.
        if (selected in offered and
                published[selected].get('source_kind') == 'CO_PUBLIC_NOTICE'):
            view['optional']['source_kind'] = 'CO_PUBLIC_NOTICE'
            view['optional']['published_words_available'] = bool(
                committed_look is not None and
                type(published[selected].get('public_close')) is str and
                self.mii.close_available(mii_house, self.user_id, selected))
            view['optional']['institutional_truth'] = 'NOT_ESTABLISHED'
        # Preserve how a particular textual presentation was obtained in
        # the existing private exposure ledger, not as a new world fact,
        # assertion of human knowledge, or an actor's representation of it.
        if selected in offered and close_granted and look_receipt is not None:
            kind = published[selected].get('source_kind')
            if kind in ('CO_PUBLIC_NOTICE', 'INCIDENTALLY_EXPOSED_DOCUMENT'):
                view['optional']['acquisition_provenance'] = {
                    'route': ('PUBLIC_INSTITUTIONAL_DISPLAY' if kind == 'CO_PUBLIC_NOTICE'
                              else 'INCIDENTALLY_EXPOSED_MATERIAL_FACE'),
                    'look_receipt': look_receipt,
                    'target_ref': selected,
                    'presentation_clock': world['clock'],
                    'content_truth': 'NOT_ESTABLISHED',
                    'human_comprehension': 'NOT_ESTABLISHED',
                    'personal_entrusting': 'NOT_ESTABLISHED',
                }
                if kind == 'INCIDENTALLY_EXPOSED_DOCUMENT':
                    view['optional']['acquisition_provenance']['further_access'] = 'NOT_GRANTED'
        prior_offered = (profile['exposures'][-1].get('offered', {})
                         if profile.get('exposures') else {})
        before = len(profile.get('exposures', []))
        self.mii.record_exposure(profile, turn=world['clock'], clock=world['clock'],
            available=available, candidates=available, offered=offered,
            selected=selected, rendered=view, basis=basis,
            request_id=(committed_look.get('event_ref') if committed_look else None),
            context={'room': loc, 'world': self.runtime.world_id,
                     'command': command,
                     'user_close_granted_by_mii': close_granted,
                     **({'recognition_source_fingerprint':recognition_fingerprint}
                        if recognition_fingerprint is not None else {})})
        # Reuse MII's existing private, optional acquired-attention mechanic.
        # It is never a world event or evidence that Nadia watched the gaze.
        if (len(profile.get('exposures', [])) > before
                and committed_look is not None):
            self.mii.update_attention(
                profile, target=selected, prior_offered=prior_offered,
                command='look', turn=world['clock'])
        return view

    def new_private_profile(self):
        if self.mii is None:
            raise EncounterRefusal('MII_READER_NOT_INSTALLED')
        root = self.runtime.ledger.events(1)[0]['id']
        scope = {'root': root, 'branch': self.runtime.world_id, 'user': self.user_id}
        return self.mii.default_profile(scope)
    
    def _mii_scope_session(self):
        """Only bridge protected MII's scope() read ABI; NOT a P6 world writer."""
        if self.mii is None:
            raise EncounterRefusal('MII_READER_NOT_INSTALLED')
        root = self.runtime.ledger.events(1)[0]['id']
        return SimpleNamespace(
            branch_id=self.runtime.world_id,
            meta={'user_actor': self.user_id},
            read_root=lambda: {'root_hash': root},
        )

    def load_private_profile(self, profile_path):
        """Reuse protected MII's cold profile reader, scoped to this CO root.

        The path is an application-trusted sidecar location, NOT a path
        supplied by a visitor utterance or an authenticated real-user ID.
        MII's tamper/mismatch reset remains the only profile recovery owner.
        """
        profile = self.mii.load_profile(
            Path(profile_path), self._mii_scope_session())
        if profile.get('scope') != self.new_private_profile()['scope']:
            raise EncounterRefusal('MII_PROFILE_SCOPE_MISMATCH')
        return profile

    def save_private_profile(self, profile_path, profile):
        """The protected MII writer owns derivative user history; CO does not."""
        if self.mii is None:
            raise EncounterRefusal('MII_READER_NOT_INSTALLED')
        if (type(profile) is not dict or
                profile.get('scope') != self.new_private_profile()['scope']):
            raise EncounterRefusal('MII_PROFILE_SCOPE_MISMATCH')
        self.mii.save_profile(Path(profile_path), profile)

    def private_surface_stored(self, profile_path, *, command: str | None = None,
                               target: str | None = None):
        """One cold-reopenable MII presentation with no world/actor mutation.

        Reuse P6's sidecar and advisory file lock. The app must provide an
        access-controlled storage path; this does NOT authenticate users or
        grant access to the private profile of another real human.
        """
        path = Path(profile_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = path.with_name(path.name + '.lock')
        with lock_path.open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                profile = self.load_private_profile(path)
                view = self.private_surface(profile, command=command, target=target)
                self.save_private_profile(path, profile)
                return view
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)

