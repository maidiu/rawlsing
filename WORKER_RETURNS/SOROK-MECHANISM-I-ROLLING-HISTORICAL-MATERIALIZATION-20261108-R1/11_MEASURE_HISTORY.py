#!/usr/bin/env python3
"""Measure existing committed history readers; never invokes a provider."""
import argparse
import json
import math
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1'))
from run_p4 import open_owner
from rawlsing_next.sorok_history.owner import HistoricalWorld, digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--samples', type=int, choices=range(20, 101), default=24)
    args = parser.parse_args()
    started = time.perf_counter()
    owner = open_owner(args.state / 'actual-p2')
    open_s = time.perf_counter() - started
    rows = []
    try:
        h = HistoricalWorld(owner.base_owner.fanin.session)
        targets = [r['id'] for r in h.visible_surfaces()]
        for name, read in [('depth', lambda: [h.query_depth(t) for t in targets]),
                           ('graph', h.history_graph)]:
            expected = None
            times = []
            for index in range(args.samples + 1):
                started = time.perf_counter()
                result = read()
                elapsed = time.perf_counter() - started
                identity = digest(result)
                if expected is None:
                    expected = identity
                if identity != expected:
                    raise ValueError('reader changed committed truth during benchmark')
                rows.append({'reader': name, 'sample': index,
                    'phase': 'first_after_open' if index == 0 else 'warm',
                    'seconds': elapsed, 'result_hash': identity})
                if index:
                    times.append(elapsed)
            ordered = sorted(times)
            rows.append({'reader': name, 'phase': 'summary', 'n': len(times),
                'p50_seconds': ordered[math.ceil(.5 * len(times)) - 1],
                'p95_seconds': ordered[math.ceil(.95 * len(times)) - 1],
                'max_seconds': max(times), 'target_count': len(targets)})
        rows.append({'phase': 'resources', 'cold_owner_open_seconds': open_s,
            'state_bytes': sum(p.stat().st_size for p in args.state.rglob('*') if p.is_file()),
            'graph_json_bytes': len(json.dumps(h.history_graph()).encode()),
            'process_peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'rss_units': 'Darwin ru_maxrss bytes', 'provider_calls': 0,
            'scope': 'SOURCEFREE_SYNTHETIC engineering cohort, not production population'})
    finally:
        owner.close()
    args.out.write_text(''.join(json.dumps(row, sort_keys=True) + '\n' for row in rows))
    print(json.dumps([r for r in rows if r['phase'] in {'summary', 'resources'}]))


if __name__ == '__main__':
    main()
