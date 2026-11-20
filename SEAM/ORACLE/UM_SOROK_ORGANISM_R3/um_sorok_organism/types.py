"""Common research read-models; dictionaries on disk are intentionally JSON-addressable.
These data classes are output interfaces, NOT a new SOROK canonical ontology.
"""
from dataclasses import dataclass, field, asdict
from typing import Any
import hashlib, json

GRADE = 'SOURCEFREE_RESEARCH_PROVISIONAL'


def canonical(x: Any) -> str:
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(x: Any) -> str:
    return hashlib.sha256(canonical(x).encode('utf-8')).hexdigest()


def copy(x):
    return json.loads(canonical(x))


def stable_id(prefix: str, value: Any) -> str:
    return prefix + '_' + digest(value)[:16]


@dataclass
class AccessibleEncounter:
    actor: str
    world_clock: int
    location: str
    cues: list[dict]
    affordances: list[str]
    access_receipts: list[str]
    inaccessible_count: int = 0


@dataclass
class Constitution:
    actor: str
    clock: int
    body: dict
    forms: dict
    links: list[dict]
    projects: list[dict]
    activity_links: list[dict]
    memories: list[dict]
    traces: list[dict]
    other_models: dict
    self_model: dict
    relations: list[dict]
    unknowns: list[str]
    history_refs: list[str] = field(default_factory=list)
    source_grade: str = GRADE
    composition_methods: list[dict] = field(default_factory=list)
    relational_motifs: list[dict] = field(default_factory=list)
    # Sourcefree qualified history: neither an unfinished possible end nor
    # a signal path is a motive, self-knowledge, or invented counterfactual.
    possible_ends: list[dict] = field(default_factory=list)
    evidence_paths: list[dict] = field(default_factory=list)
    expectations: list[dict] = field(default_factory=list)


@dataclass
class Situated:
    actor: str
    clock: int
    recruited: list[dict] = field(default_factory=list)
    dormant: list[str] = field(default_factory=list)
    inhibited: list[str] = field(default_factory=list)
    currents: list[dict] = field(default_factory=list)
    accessible_cues: list[dict] = field(default_factory=list)
    candidate_actions: list[dict] = field(default_factory=list)
    disagreements: list[dict] = field(default_factory=list)
    readset: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    antagonisms: list[dict] = field(default_factory=list)
    suspended_actions: list[dict] = field(default_factory=list)
    learned_compositions: list[dict] = field(default_factory=list)


@dataclass
class Attempt:
    actor: str
    action: str
    target: str | None = None
    object_ref: str | None = None
    means: list[str] = field(default_factory=list)
    basis: list[str] = field(default_factory=list)
    intention: str = ''
    # Actor-selected project purpose is separate from the pooled reasons why
    # a physical operation was eligible. None is a lawful first attempt.
    purpose_selection: dict = field(default_factory=dict)
    # Private actor-policy decision identity; world executes only action/target/object.
    practical_selection: dict = field(default_factory=dict)
    scene_hash: str = ''
    grade: str = GRADE

    def document(self):
        return asdict(self)


@dataclass
class Resolution:
    status: str
    performed: list[dict]
    world_delta: dict
    personal_effects: dict
    witnesses: list[str]
    objective_description: str
    grade: str = GRADE


def newborn(actor_id: str, name: str, location: str = 'home') -> dict:
    return {
        'id': actor_id, 'name': name, 'role': 'child', 'age_days': 0,
        'location': location,
        'body': {'nutrition': .78, 'rest': .78, 'comfort': .66, 'pain': 0.0,
                 'arousal': .40, 'motor': .17, 'sensor': .40, 'language': 0.0,
                 'illness': 0.0, 'regulation': .28},
        'forms': {}, 'links': [], 'projects': [], 'activity_links': [], 'composition_methods': [], 'relational_motifs': [], 'activity_history': [],
        'possible_ends': [], 'evidence_paths': [], 'expectations': [],
        'memories': [], 'traces': [],
        'other_models': {}, 'self_model': {}, 'unknowns': ['adult_purpose', 'adult_ideology'],
        'grade': GRADE, 'history_refs': [], 'current_activity': None,
    }


def adult(actor_id: str, name: str, location='home', age_days=30 * 365) -> dict:
    a = newborn(actor_id, name, location)
    a['role'] = 'adult'; a['age_days'] = age_days
    a['body'].update({'motor': .84, 'sensor': .85, 'language': .90, 'regulation': .68,
                      'rest': .75, 'comfort': .76})
    a['unknowns'] = ['complete_life_history', 'objective_private_respondent_psyche']
    return a


def blank_world(world_id='w1'):
    return {'id': world_id, 'clock': 0, 'positions': {},
            'sites': {'home': {'food': 12, 'stock': 8, 'access': 'public'},
                      'workshop': {'food': 1, 'stock': 5, 'access': 'public',
                                   'controller':'workshop_steward', 'food_price':1.0},
                      'hall': {'food': 0, 'stock': 2, 'access': 'controlled'}},
            'relations': {}, 'accounts':{'workshop_steward':12.0},'material_claims':[],
            'institutions': {'workshop_steward':{'controls':'workshop','wage':.25,'claims_output':True},'hall_board': {'controls': 'hall', 'members': [], 'rule': 'hall_permission'}},
            'cues': [], 'historical_periods': [], 'public_history': [],
            'ambient': {'work_shifts': {}, 'material_prices': {'food': 1}, 'weather': 'ordinary'},
            'grade': GRADE}
