"""SOURCEFREE compact temporal world performance, NOT general person generation.

No actor psychology, empirical probability, production authority or native V3 transition.
One macro-period actor performed-action means an aggregate source-owned historical fact;
it is NOT an intention, a narrator assertion, or a transcript of individual days.
"""
from dataclasses import dataclass
from sorok_interval_participation_producer_r1 import (
    WorldRegime, EpochOutcome, WORLD_OWNER, example_inputs, diagnostic_candidate,
    fingerprint,
)

ACTOR_OWNER = 'TEST_ONLY_MACRO_ACTOR_PERFORMER@1'
COUNTERPART_OWNER = 'TEST_ONLY_MACRO_COUNTERPART_WORLD_PERFORMER@1'
PERIOD_WORLD_RULE = 'TEST_ONLY_PERIOD_WORLD_EFFECT@1'


@dataclass(frozen=True)
class MacroActorAct:
    actor_id: str
    start: int
    end: int
    proposal: str  # AGREE / REFUSE / UNRESOLVED (not actual performance)
    realized_conduct: str  # ACTED / RESISTED_BUT_ACTED / REFUSED / UNKNOWN
    actual_act_ref: str
    source_owner: str = ACTOR_OWNER


@dataclass(frozen=True)
class MacroWorldResponse:
    household_id: str
    start: int
    end: int
    material_status: str  # AVAILABLE / BLOCKED / UNKNOWN
    counterpart_response: str  # ACCOMMODATED / OBSTRUCTED / UNKNOWN
    actual_world_ref: str
    source_owner: str = COUNTERPART_OWNER


def realize_period(regime: WorldRegime, act: MacroActorAct, world: MacroWorldResponse) -> dict:
    """Compute, don't presume, macro-period participation.

    Input `realized_conduct` must be separately sourced by actor performer; this
    finite world model does not create that actor choice or its causal history.
    The model is synthetic and only demonstrates faithful owner-bound conversion.
    """
    def refuse(code): return {'status': 'REFUSED', 'reason': code, 'epoch': None}
    if act.source_owner != ACTOR_OWNER or world.source_owner != COUNTERPART_OWNER:
        return refuse('UPSTREAM_SOURCE_OWNER_MISMATCH')
    if (act.actor_id, world.household_id) != (regime.actor_id, regime.household_id):
        return refuse('UPSTREAM_ACTOR_HOUSEHOLD_MISMATCH')
    if (act.start, act.end) != (world.start, world.end):
        return refuse('UPSTREAM_TIME_MISMATCH')
    if act.start < regime.start or act.end > regime.end or act.start >= act.end:
        return refuse('ACTIVITY_OUTSIDE_REGIME')
    if not act.actual_act_ref or not world.actual_world_ref:
        return refuse('UPSTREAM_PERFORMANCE_OR_WORLD_REF_MISSING')
    if act.proposal not in ('AGREE','REFUSE','UNRESOLVED') or act.realized_conduct not in ('ACTED','RESISTED_BUT_ACTED','REFUSED','UNKNOWN'):
        return refuse('UNKNOWN_ACTOR_ACTION_KIND')
    if world.material_status not in ('AVAILABLE','BLOCKED','UNKNOWN') or world.counterpart_response not in ('ACCOMMODATED','OBSTRUCTED','UNKNOWN'):
        return refuse('UNKNOWN_WORLD_RESPONSE_KIND')
    performed = act.realized_conduct in ('ACTED','RESISTED_BUT_ACTED')
    if performed and world.material_status == 'AVAILABLE' and world.counterpart_response == 'ACCOMMODATED':
        result='CONFIRMED'
    elif act.realized_conduct == 'REFUSED' or world.material_status == 'BLOCKED' or world.counterpart_response == 'OBSTRUCTED':
        result='NOT_PERFORMED'
    else:
        result='UNKNOWN'
    if act.realized_conduct == 'REFUSED' and result=='CONFIRMED':
        return refuse('IMPOSSIBLE_REFUSAL_AND_PERFORMANCE')
    epoch = EpochOutcome(act.actor_id, world.household_id, regime.scope_id, act.start, act.end,
                         act.realized_conduct, result,
                         actor_act_receipt=act.actual_act_ref,
                         world_receipt=world.actual_world_ref,
                         source_owner=WORLD_OWNER,
                         source_valid_to=world.end)
    return {'status': 'DERIVED', 'reason': 'TEST_ONLY_ACTUAL_PERIOD_WORLD_RULE',
            'actor_source': ACTOR_OWNER, 'counterpart_source': COUNTERPART_OWNER,
            'world_rule': PERIOD_WORLD_RULE, 'actor_intent': act.proposal,
            'world_outcome': result, 'epoch': epoch,
            'receipt_hash': fingerprint((regime,act,world,result,PERIOD_WORLD_RULE))}


def produce_life():
    regime, _ = example_inputs()
    acts = [MacroActorAct('NADIA',96,108,'UNRESOLVED','RESISTED_BUT_ACTED','ACTOR_MACRO_96_108'),
            MacroActorAct('NADIA',108,120,'AGREE','ACTED','ACTOR_MACRO_108_120')]
    worlds = [MacroWorldResponse('HH1',96,108,'AVAILABLE','ACCOMMODATED','W1'),
              MacroWorldResponse('HH1',108,120,'AVAILABLE','ACCOMMODATED','W2')]
    out=[realize_period(regime,a,w) for a,w in zip(acts,worlds)]
    if any(x['status']!='DERIVED' for x in out):
        raise RuntimeError('TEST_ONLY_MACRO_WORLD_DERIVATION_FAILED')
    diag=diagnostic_candidate(regime, tuple(x['epoch'] for x in out))
    return {'regime':regime,'periods':out,'formation_diagnostic':diag}
