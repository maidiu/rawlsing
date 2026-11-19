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


def propose_compositions(situated, max_steps=3):
    options={o['action']:o for o in situated.candidate_actions}
    currents=situated.currents
    projects=[x for x in currents if x.get('kind')=='ONGOING_ACTIVITY']
    out=[]
    # These are compositional *grammars* of already feasible means, not new
    # psychologically preinstalled desires. Purposes derive from actor projects.
    for p in projects:
        if 'WORK' in options and 'REPAIR' in options:
            candidate=('WORK','REPAIR')
        elif 'MAKE_SPACE' in options and 'SING' in options:
            candidate=('MAKE_SPACE','SING')
        elif 'PRACTICE' in options and 'SING' in options:
            candidate=('PRACTICE','SING')
        elif 'ASK' in options and 'JOIN' in options:
            candidate=('ASK','JOIN')
        else:continue
        if len(candidate)>max_steps:continue
        refs=tuple(sorted({p['ref']} | {r for a in candidate for r in options[a].get('basis',[]) }))
        out.append(ComposedActivity(stable_id('composed',{'actor':situated.actor,
          'purpose':p['object'],'steps':candidate,'basis':refs}),
          situated.actor,p['object'],candidate,refs))
    # Deduplicate across current projects without destroying different ends.
    return out
