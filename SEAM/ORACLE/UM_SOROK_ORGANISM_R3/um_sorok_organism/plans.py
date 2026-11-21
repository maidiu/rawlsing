"""Novel *compositions* of existing, historically qualified means.

Never creates a new physical opcode nor assumes the intended result.
The plan remains an actor-specific hypothesis; each step executes through the
normal actor/world/developmental loop and is independently resolved.
"""
from dataclasses import asdict, dataclass
from .types import GRADE, stable_id

@dataclass(frozen=True)
class ComposedActivity:
    id: str
    actor: str
    object: str
    steps: tuple[str,...]
    basis: tuple[str,...]
    grade: str=GRADE


def qualified_learned_compositions(constitution, encounter, active_forms, projects, options):
    """Apply actor-acquired methods only when their antecedents exist now.

    A semantic proposal cannot turn absence of bodily means, present forms or
    material permissions into success. It only makes a *possible* new project
    composition eligible for independent future world transaction.
    """
    available={o['action'] for o in options}
    forms=set(active_forms)
    out=[]
    for rule in constitution.composition_methods:
        if rule.get('status')!='ACTIVE':continue
        if rule.get('locations') and encounter.location not in rule['locations']:continue
        if not set(rule['source_forms']).issubset(forms):continue
        operations=rule['operations']
        if not set(operations).issubset(available):continue
        # Object proposed during acquisition, rather than an automatic
        # transparent motive inferred from two technical operations.
        out.append({'id':rule['id'],'operations':operations,
          'object':rule.get('hypothesized_end','UNKNOWN_END'),
          'source_forms':rule['source_forms'],'origin':rule['origin'],
          'grade':rule['grade'],'acquired_not_born':True})
    return out


def propose_compositions(situated, max_steps=3):
    options={o['action']:o for o in situated.candidate_actions}
    currents=situated.currents
    projects=[x for x in currents if x.get('kind')=='ONGOING_ACTIVITY']
    out=[]
    for method in situated.learned_compositions:
        steps=tuple(method['operations'])
        if len(steps)>max_steps:continue
        out.append(ComposedActivity(stable_id('composed',{'actor':situated.actor,
          'method':method['id'],'steps':steps}),situated.actor,method['object'],
          steps,tuple(method['source_forms']+[method['id']])))
    # These older algorithmic patterns are inherited provisional grammar,
    # explicitly *not* evidence of a separately acquired method.
    # These are compositional *grammars* of already feasible means, not new
    # psychologically preinstalled desires. Purposes derive from actor projects.
    for p in projects:
        # A globally feasible operation does not become this project's means.
        # Both component operations must be actor/project-attributed in the
        # situated candidate set, not merely available through another purpose.
        owned=set(p.get('means',[]))
        project_basis='project:'+p['ref']
        patterns=(('WORK','REPAIR'),('MAKE_SPACE','SING'),
                  ('PRACTICE','SING'),('ASK','JOIN'))
        candidate=next((pair for pair in patterns
            if len(pair)<=max_steps and all(a in owned and a in options
                and project_basis in options[a].get('basis',[]) for a in pair)),None)
        if candidate is None:continue
        # Preserve form evidence; NEVER merge another project's motive/basis
        # into the object whose course this plan purports to continue.
        form_refs={r for a in candidate for r in options[a].get('basis',[])
                   if r!='organism' and not str(r).startswith('project:')}
        refs=tuple(sorted({project_basis}|form_refs))
        out.append(ComposedActivity(stable_id('composed',{'actor':situated.actor,
          'purpose':p['object'],'steps':candidate,'basis':refs}),
          situated.actor,p['object'],candidate,refs))
    # Deduplicate across current projects without destroying different ends.
    return out
