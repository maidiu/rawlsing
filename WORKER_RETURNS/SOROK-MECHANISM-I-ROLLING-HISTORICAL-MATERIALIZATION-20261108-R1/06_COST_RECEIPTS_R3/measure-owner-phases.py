#!/usr/bin/env python3
"""Controlled sourcefree owner spans, explicitly separate from live inference."""
import argparse
import functools
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import pytest
from rawlsing_next.tests.test_sorok_history_episodes import source_world, candidate, commit
from rawlsing_next.sorok_history.owner import HistoricalWorld, digest

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--state', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
args.state.mkdir(parents=True)  # never replace an existing owner
patch = pytest.MonkeyPatch()
spans, ended, active = [], {}, []


def instrument(cls, method):
    original = getattr(cls, method)
    @functools.wraps(original)
    def measured(self, *a, **kw):
        started = time.perf_counter()
        depth = len(active)
        active.append(method)
        try:
            result = original(self, *a, **kw)
            if method == 'admit_surface':
                ended[result['id']] = time.perf_counter()
            if method == 'lease' and result:
                spans.append({'operation': 'queue_lead_before_lease', 'depth': depth,
                    'seconds': started - ended[result['job']['target_id']]})
            return result
        finally:
            active.pop()
            spans.append({'operation': method, 'seconds': time.perf_counter() - started,
                          'depth': depth, 'inclusive': True})
    patch.setattr(cls, method, measured)


for method in ['admit_surface', 'configure_experimental_history', 'lease', 'record_candidate',
               'commit_candidate', '_build_history_graph', 'query_depth', 'query_relations']:
    instrument(HistoricalWorld, method)
cpu = time.process_time()
started = time.perf_counter()
fanin = None
try:
    fanin, history, book, tool, entities, parent = source_world(args.state, patch)
    construction = time.perf_counter() - started
    from bp4.world import WorldState
    instrument(WorldState, 'admit_material_history')
    leased = history.lease()
    result = commit(history, leased, candidate(leased, book, tool, entities, parent))
    assert result['status'] == 'INDEX_READY'
    depth = history.query_depth(book['id'])
    graph = history.query_relations(entities[0]['ref']['object_id'])
    receipt = {'schema': 'SOROK_MI_COMPONENT_COST@1',
        'grade': 'CONTROLLED_SOURCEFREE_COMPONENT_TIMING_NOT_LIVE',
        'constructor_seconds': construction, 'cpu_seconds': time.process_time() - cpu,
        'process_peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'spans': spans, 'nested_spans_are_not_additive': True,
        'provider_calls': 0, 'candidate_origin': 'deterministic sourcefree test proposal',
        'source_sha': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'source_blobs': {str(p): subprocess.check_output(['git', 'hash-object', str(p)], text=True).strip()
                         for p in [Path('rawlsing_next/sorok_history/owner.py'),
                                   Path('rawlsing_next/tests/test_sorok_history_episodes.py'),
                                   Path(sys.modules[WorldState.__module__].__file__).resolve().relative_to(ROOT)]},
        'admission_status': result['status'], 'depth_hash': digest(depth),
        'relations_hash': digest(graph), 'target_count': 2}
    args.out.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'spans': spans}))
finally:
    if fanin:
        fanin.close()
    patch.undo()
