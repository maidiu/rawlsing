"""Import the original committed research candidate without copying or repairing it."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
R1 = ROOT.parent / 'SOROK_CONTINGENT_LIVES_CAUSAL_COURT_R1'
sys.path.insert(0, str(R1))
from court import model as m, intervene, rehash, replace_event


def ancestors(trace, event_id):
    seen=set()
    def visit(key):
        for parent in trace.get(key).parents:
            if parent not in seen:
                seen.add(parent)
                visit(parent)
    visit(event_id)
    return seen
