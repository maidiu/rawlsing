"""Offline accounting for the existing RFA-06C2 balanced primary sample.
No provider calls, semantic scoring, or custody/acceptance promotion.
"""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path

MAPPING_BLOB = 'ec6a8c9cbcc1c527ca1ad93a95e56bdcdf3573cd'
TRANSIENT = 'OPERATIONAL_TRANSIENT_NO_CANDIDATE'
TERMINAL = set('SCHEMA_VALID SCHEMA_INVALID JSON_PARSE_INVALID STRUCTURAL_INVALID MODEL_REFUSAL MODEL_TRUNCATED PROVIDER_SCHEMA_FAILURE PERMANENT_PROVIDER_FAILURE PROVIDER_MODEL_MISMATCH NO_TEXT_CANDIDATE'.split())
FIELDS = ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def clock(value):
    t = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(t.utcoffset() is not None, 'RFA_CLOCK_ZONE')
    return t


def reduce_attempts(entry, records):
    """Records ordered by original filename; missing usage is never zero."""
    run = entry['source_run_id']
    previous_end = None
    first = None
    known = Counter()
    coverage = Counter()
    durations = []
    statuses = []
    request = None
    for i, r in enumerate(records, 1):
        require(r['attempt_id'] == f'{run}-A{i:04d}' and r['run_id'] == run, 'RFA_ATTEMPT_GAP_OR_ID')
        require((r['case_id'], r['condition'], r.get('requested_model', r.get('model')), r.get('replicate', r.get('replicate_ordinal'))) == (entry['case_id'], entry['condition'], entry['model'], entry['replicate']), 'RFA_CELL_DRIFT')
        identity = r['request_identity_sha256']
        require(isinstance(identity, str) and len(identity) == 64 and all(x in '0123456789abcdef' for x in identity), 'RFA_REQUEST_ID')
        require(request is None or request == identity, 'RFA_RETRY_REQUEST_DRIFT')
        request = identity
        require(not statuses or statuses[-1] == TRANSIENT, 'RFA_AFTER_TERMINAL')
        status = r['status']
        require(status in TERMINAL or status == TRANSIENT, 'RFA_STATUS')
        start, end = clock(r['started_at_utc']), clock(r['ended_at_utc'])
        require(end >= start and (previous_end is None or start >= previous_end), 'RFA_CHRONOLOGY')
        first = first or start
        previous_end = end
        seconds = r['latency_seconds']
        require(type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0, 'RFA_LATENCY')
        durations.append(seconds)
        statuses.append(status)
        usage = r.get('usage')
        require(usage is None or isinstance(usage, dict), 'RFA_USAGE_SHAPE')
        for k in FIELDS:
            v = (usage or {}).get(k)
            if v is not None:
                require(type(v) is int and v >= 0, 'RFA_USAGE_VALUE')
                known[k] += v
                coverage[k] += 1
    terminal = bool(statuses and statuses[-1] in TERMINAL)
    return {'run': run, 'model': entry['model'], 'condition': entry['condition'],
            'attempts': len(records), 'statuses': statuses, 'terminal_observed': terminal,
            'known_usage': {k: known[k] for k in FIELDS},
            'usage_observations': {k: coverage[k] for k in FIELDS},
            'complete_observed_usage': bool(records) and all(coverage[k] == len(records) for k in FIELDS),
            'sum_attempt_seconds': sum(durations),
            'observed_span_seconds': (previous_end-first).total_seconds() if first else None,
            'time_to_terminal_seconds': (previous_end-first).total_seconds() if terminal else None,
            'time_to_adequate_result_seconds': None}


def audit(mapping, opus_raw, cross_raw):
    data = Path(mapping).read_bytes()
    blob = hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    require(blob == MAPPING_BLOB, 'RFA_MAPPING_SOURCE_DRIFT')
    entries = json.loads(data)['entries']
    require(len(entries) == len({e['source_run_id'] for e in entries}) == 60, 'RFA_PRIMARY_UNIVERSE')
    rows = []
    for e in entries:
        root = opus_raw if e['source_kind'] == 'EXISTING_OPUS_R2' else cross_raw
        paths = sorted(Path(root).glob(e['source_run_id']+'-A*.json'))
        records = [json.loads(p.read_bytes()) for p in paths]
        require(all(p.name == r['attempt_id']+'.json' for p,r in zip(paths,records)), 'RFA_FILENAME_ID')
        rows.append(reduce_attempts(e, records))
    groups = {}
    for model in sorted({r['model'] for r in rows}):
        rs = [r for r in rows if r['model'] == model]
        groups[model] = {'expected_runs':len(rs), 'observed_runs':sum(r['attempts']>0 for r in rs),
            'terminal_runs':sum(r['terminal_observed'] for r in rs), 'observed_attempts':sum(r['attempts'] for r in rs),
            'known_usage':{k:sum(r['known_usage'][k] for r in rs) for k in FIELDS},
            'usage_observations':{k:sum(r['usage_observations'][k] for r in rs) for k in FIELDS},
            'observed_attempt_seconds':sum(r['sum_attempt_seconds'] for r in rs),
            'terminal_span_observations':sum(r['terminal_observed'] for r in rs),
            'terminal_span_seconds':sum(r['time_to_terminal_seconds'] or 0 for r in rs),
            'complete_observed_usage':all(r['terminal_observed'] and r['complete_observed_usage'] for r in rs)}
    return {'scope':'OBSERVED_PRIMARY_ATTEMPTS_ONLY_NOT_CUSTODY_OR_ADEQUACY',
            'network_calls':0, 'mapping_blob':blob, 'models':groups, 'rows':rows,
            'limitations':['No smoke/secondary runs; no proof of archive completeness or request freeze validation.',
            'Known tokens only; thinking included in output, not added; no invoice or historical rates inferred.',
            'Terminal span includes gaps between attempts; excludes subsequent scoring and repair outside this archive.']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('mapping','opus-raw','cross-raw'):
        p.add_argument('--'+name, required=True)
    a=p.parse_args()
    print(json.dumps(audit(a.mapping,a.opus_raw,a.cross_raw), indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
