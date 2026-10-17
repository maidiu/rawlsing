"""Independent execution record for the E06I court.

Runs the exact candidate bridge against the exact staged native owners with a
reviewer-authored read-only profiler (sys.setprofile; no wrapping, no doubles)
and writes 02_EXECUTED_ORIGINAL_OWNER_AND_BOTH_CLIENTS.json.

env: E06_CANDIDATE_ROOT (staged candidate return directory)
"""
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

CAND = os.environ.get('E06_CANDIDATE_ROOT')
if not CAND or not os.path.exists(os.path.join(CAND, 'bridge.py')):
    raise SystemExit('E06_CANDIDATE_ROOT must point at the staged candidate return directory')
CAND = os.path.realpath(CAND)
RT = os.path.realpath(os.path.join(CAND, 'runtime'))
RET = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path[:0] = [os.path.join(CAND, 'repro'), CAND, os.path.join(RT, 'owners'), RT,
                os.path.join(RT, 'rawlsing_next', 'tests'), os.path.join(RT, 'rawlsing_next')]

from support import (bridge, request, rows, grants, hydrate, clone, AuthorityRegistry,
                     TestOnlyRegistry, GSS, NCA, E, NativeBridge)  # noqa: E402
from rawlsing_next import pre553_n9_n10w_progressive_candidate as e03  # noqa: E402

WATCH = {
    'ingest_c11_source_release', 'execute_empirical_query',
    'provide_empirical_possibility_slice', 'compose_positioned_subject_possibility',
    'evaluate_positioned_subject_possibility', 'resolve_v558',
    'materialize_resolved_structural_context', 'validate_resolved_structural_context',
    '_authorize_cached_use', 'require_positive_authority', 'consume', 'evaluate',
    'serve', 'accept', '_require_exact_i03_authority_fitness',
}


class Probe:
    def __init__(self):
        self.counts = Counter()
        self.c11 = None
        self.compositions = []
        self.f8 = []
        self.client_snapshots = []
        self.held = []

    def profile(self, frame, event, arg):
        name = frame.f_code.co_name
        path = frame.f_code.co_filename
        if not path.startswith(RT) or name not in WATCH:
            return
        if event == 'call':
            self.counts[(os.path.relpath(path, CAND), frame.f_code.co_firstlineno, name)] += 1
            if name == 'evaluate_positioned_subject_possibility':
                ev = frame.f_locals.get('evidence', ())
                self.held.extend(ev)
                self.f8.append(dict(ids=[id(x) for x in ev],
                                    refs=[x.evidence_ref.as_dict() for x in ev]))
            if name in ('consume', 'evaluate') and 'snapshot' in frame.f_locals:
                snap = frame.f_locals['snapshot']
                self.held.append(snap)
                self.client_snapshots.append(dict(consumer=name, snapshot_object_id=id(snap),
                                                  snapshot_hash=snap.snapshot_hash))
        elif event == 'return' and arg is not None:
            if name == 'compose_positioned_subject_possibility' and hasattr(arg, 'possibility_slice_evidence_or_null'):
                ev = arg.possibility_slice_evidence_or_null
                if ev is not None:
                    self.held.append(ev)
                    self.compositions.append(dict(id=id(ev), evidence_ref=ev.evidence_ref.as_dict(),
                                                  fact_ref=arg.producer_fact_ref.as_dict(),
                                                  query_ref=frame.f_locals['empirical_query'].ref.as_dict()))
            elif name == 'ingest_c11_source_release' and hasattr(arg, 'accepted'):
                cand = frame.f_locals['candidate']
                self.c11 = [e.semantic_projection() for e in cand.respondent_events]


def collect_imports():
    manifest = {x['local']: x for x in json.loads(open(os.path.join(CAND, 'source_manifest.json')).read())}
    out = []
    for mod in sorted(sys.modules):
        m = sys.modules[mod]
        p = getattr(m, '__file__', None)
        if not p or not os.path.realpath(p).startswith(RT) or not p.endswith('.py'):
            continue
        local = os.path.relpath(os.path.realpath(p), CAND)
        entry = manifest[local]
        b = open(p, 'rb').read()
        assert hashlib.sha256(b).hexdigest() == entry['sha256']
        assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == entry['git_blob']
        out.append(dict(module=mod, file=local, commit=entry['commit'], source_path=entry['path'],
                        git_blob=entry['git_blob'], sha256=entry['sha256'], verified=True))
    return out


def strata_from_c11(events):
    records = defaultdict(dict)
    for e in events:
        m = e['semantic_fields']
        person = m['scoped_respondent_ref']['content_hash']
        q = m['native_question_ref']['object_id'].rsplit('-', 1)[-1]
        records[person][q] = int(m['raw_response_value'])
    c = Counter((''.join(str(r[q]) for q in 'ABC'), r['Y']) for r in records.values())
    return len(records), len(events), {k: [c[(k, 1)], c[(k, 0)]] for k in sorted({k for k, _ in c})}


def support_of(receipt):
    out = []
    for s in receipt['empirical_steps']:
        cells = {c['cell']: c['raw_numerator_support'] for c in s['cells']}
        out.append([cells.get('1'), s['denominator']])
    return out


probe = Probe()
sys.setprofile(probe.profile)
try:
    products = {}
    b = bridge()
    p = b.prepare(request())
    products['CURRENT'] = b.read(p)
    products['HISTORICAL'] = bridge().execute(request('HISTORICAL_AS_OF'))
    products['Y_CHANGED'] = bridge(empirical_changed=True).execute(request())
    products['ZERO_SUPPORT'] = bridge(support_loss=True).execute(request())
    products['REVERSE'] = b.execute(request(target='A', conditions=(('Y', 1),)), scalar_only=True)
    products['PRE_NCA_PUBLICATION'] = bridge().execute(request('TYPED_PARTIAL_PRE_NCA_PUBLICATION'))

    life = bridge()
    lp = life.prepare(request())
    before = life.read(lp)
    w = life.provider.world
    projection = deepcopy(life.provider.cache[('Y', (('A', 1),))]) if life.provider.cache else None
    archive = life.archive(before)
    w['registry'] = AuthorityRegistry(w['source']['authorities'])
    withdrawn = life.read(lp)
    w['registry'] = AuthorityRegistry(hydrate(x.as_dict()) for x in reversed(grants(w)))
    restored = life.read(lp)
    products['QUERY_GRANT_LIFECYCLE'] = dict(
        before=before, withdrawn=withdrawn, restored=restored, archive=archive,
        same_acceptance=before['acceptance'] == restored['acceptance'],
        restored_receipt_equal=restored['selected_world_receipt'] == before['selected_world_receipt'],
        projection_available=projection is not None)

    selective = {}
    for role in (GSS, NCA):
        n = bridge()
        np_ = n.prepare(request())
        a = n.read(np_)
        rr = rows()
        next(x for x in rr if x['role'] == role)['status'] = 'REVOKED_TEST_ONLY'
        n.adapter.registry = TestOnlyRegistry(rr)
        z = n.read(np_)
        selective[role] = dict(before=a, after=z)
    products['SELECTIVE_NATIVE_REVOCATION'] = selective

    zero_rows = rows()
    row = next(x for x in zero_rows if x['role'] == NCA)
    row['values']['active_subscriptions'] = 0
    row['values']['prepaid'] = 0
    row['values']['postpaid'] = 0
    products['OBSERVED_NATIVE_ZERO'] = NativeBridge(zero_rows, enabled=True).execute(request())
finally:
    sys.setprofile(None)

import e04t_empirical  # noqa: E402
import product.empirical  # noqa: E402
import e05_n9_selected_world_adapter  # noqa: E402

respondents, events, strata = strata_from_c11(probe.c11 or [])
imports = collect_imports()
same_object = bool(probe.compositions) and all(
    any(c['id'] in f['ids'] and c['evidence_ref'] in f['refs'] for f in probe.f8)
    for c in probe.compositions)

record = dict(
    schema='E06I_EXECUTED_ORIGINAL_OWNER_AND_BOTH_CLIENTS@1',
    grade='INDEPENDENT_REVIEWER_EXECUTION',
    executed_at_utc=datetime.now(timezone.utc).isoformat(),
    pid=os.getpid(),
    candidate_sha='f9c52113de38caececc450f0e54c980f64ed3981',
    candidate_root_alias='<E06_CANDIDATE_ROOT>',
    products=products,
    source_reconstruction=dict(actual_respondents=respondents, actual_C11_events=events, strata=strata),
    native_imports=imports,
    callee_frames=[dict(file=f, line=l, function=n, count=c) for (f, l, n), c in sorted(probe.counts.items())],
    f8_evidence=dict(compositions=len(probe.compositions), consumed_inputs=len(probe.f8),
                     same_concrete_C1_object_into_F8=same_object,
                     evidence_refs=[c['evidence_ref'] for c in probe.compositions[:3]]),
    client_snapshots=probe.client_snapshots,
    module_identity=dict(
        e04t=e04t_empirical.__file__.replace(CAND, '<E06_CANDIDATE_ROOT>'),
        original_empirical=product.empirical.__file__.replace(CAND, '<E06_CANDIDATE_ROOT>'),
        e05r=e05_n9_selected_world_adapter.__file__.replace(CAND, '<E06_CANDIDATE_ROOT>'),
        e04t_is_not_original=e04t_empirical.GenericProgressiveProvider is not product.empirical.GenericProgressiveProvider),
    positive_support=support_of(products['CURRENT']['selected_world_receipt']),
)
Path(os.path.join(RET, '02_EXECUTED_ORIGINAL_OWNER_AND_BOTH_CLIENTS.json')).write_text(
    json.dumps(record, separators=(',', ':'), sort_keys=True) + '\n')
print('E06I observed', len(imports), 'native imports;', respondents, 'respondents;', events, 'C11 events;',
      len(probe.compositions), 'compositions; same_object', same_object)
print('positive support', record['positive_support'])
