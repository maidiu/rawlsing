"""Bounded intervention harness over byte-frozen inherited implementation.

Monkeypatches are scoped to one sequential run; this harness is not thread safe.
No psychology, alternative actor engine, or new developmental law is introduced.
"""
from pathlib import Path
import sys
from unittest.mock import patch
from dataclasses import asdict
sys.path.insert(0, str(Path(__file__).parent / 'inherited/causal_experiment'))
import world_intersection as model


def intervene(material, params=model.WorldParameters(), notification_minute=960):
    """Change employer material facts only; optional clock intervention is diagnostic."""
    original_add = model.Journal.add
    def add(journal, event_id, day, minute, *args, **kwargs):
        if event_id == 'father_receives_work_news':
            minute = notification_minute
        return original_add(journal, event_id, day, minute, *args, **kwargs)
    with patch.object(model, 'work_facts', return_value=dict(material)), patch.object(model.Journal, 'add', add):
        return model.simulate('ROUTINE', params)


def behavior(trace):
    return dict(father=dict(trace.get('father_response').facts),
                child_actions=trace.actor_actions, count=trace.child_practice_count,
                later=trace.child_project_after)


def rehash(event, **updates):
    from dataclasses import replace
    event = replace(event, **updates)
    body = asdict(event); body.pop('hash')
    return replace(event, hash=model.digest(body))


def replace_event(trace, event):
    from dataclasses import replace
    return replace(trace, events=tuple(event if e.id == event.id else e for e in trace.events))


def threshold_variant(threshold):
    """Isolated one-literal policy mutation; never modify the frozen source."""
    import types
    name = '_research_threshold_' + str(threshold)
    source = Path(model.__file__).read_text()
    assert source.count('if count>=3:') == 1
    variant = types.ModuleType(name)
    sys.modules[name] = variant
    try:
        exec(compile(source.replace('if count>=3:', f'if count>={int(threshold)}:'), '<threshold-sensitivity>', 'exec'), variant.__dict__)
    finally:
        del sys.modules[name]
    return variant
