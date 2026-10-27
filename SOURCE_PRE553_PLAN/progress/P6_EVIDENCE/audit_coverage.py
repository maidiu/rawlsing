#!/usr/bin/env python3
"""P6 independent coverage audit over the R157 candidate (read-only)."""
from __future__ import annotations
import gzip, hashlib, json, os, sys
from pathlib import Path

ROOT = Path('/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r157-final-review')
EVID = ROOT / 'rawlsing_next/source_configuration/evidence'
DATA = ROOT / 'rawlsing_next/source_configuration/data'
SIDS = [f'SRC{i:02d}' for i in range(1, 36)]

def load_json(p):
    return json.loads(Path(p).read_text())

def aug(path, sid):
    # exact-case component join
    rel = Path(path)
    cur = ROOT
    for part in rel.parts:
        matches = [e for e in cur.iterdir() if e.name == part]
        if not matches:
            raise FileNotFoundError(f'{sid}: missing exact-case {part} under {cur}')
        cur = matches[0]
    return cur

def iter_gz(p):
    with gzip.open(p, 'rt', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

roster = load_json(EVID / 'SOURCE_ROSTER.json')
roster_by = {s['source_id']: s for s in roster['sources']}
phys_ev = {}
for r in iter_gz(EVID / 'PHYSICAL_SLOTS.jsonl.gz'):
    phys_ev.setdefault(r['source_id'], []).append(r)
item_ev = {}
for r in iter_gz(EVID / 'ITEM_EVIDENCE.jsonl.gz'):
    item_ev.setdefault(r['source_id'], []).append(r)
unmatched = load_json(EVID / 'UNMATCHED_RELATIONS.json')
unmatched_ids = {r['implementation_id']: r for r in unmatched['records']}

fail = []
all_items = {}
all_slots = {}
summary = []
source_rows = []
for sid in SIDS:
    # discover original config exact-case
    cand = None
    for name in (f'{sid}.config.json', f'{sid}.source.config.json',
                 f'src{sid[3:]}.config.json', f'src{sid[3:]}.source.config.json',
                 'source.config.json'):
        p = DATA / sid / name
        if not p.is_file():
            continue
        if _exact := [e for e in p.parent.iterdir() if e.name == name]:
            cand = _exact[0]; break
    if cand is None:
        fail.append(f'{sid}: no original config'); continue
    doc = load_json(cand)
    if doc['identity']['source_id'] != sid or doc['config_purpose'] != 'SOURCE_PREPARATION':
        fail.append(f'{sid}: original config identity/purpose'); continue
    if doc['binding']['identity_class'] != 'ORIGINAL_SOURCE':
        fail.append(f'{sid}: original config binding class')
    if doc['binding']['source_sha256'] != doc['identity']['expected_source_sha256']:
        fail.append(f'{sid}: original binding SHA')
    if doc['binding']['row_count'] != doc['identity']['source_row_count']:
        fail.append(f'{sid}: original binding rows')
    # physical slot match
    slots = [(int(x['ordinal']), x['name']) for x in doc['physical_slots']]
    evslots = [(int(x['ordinal']), x['name']) for x in phys_ev.get(sid, [])]
    if len(slots) != len(set(slots)):
        fail.append(f'{sid}: duplicate physical slot keys')
    if slots != evslots:
        fail.append(f'{sid}: physical slots differ from evidence: {len(slots)} vs {len(evslots)}')
    if len(slots) != int(roster_by[sid]['physical_columns']):
        fail.append(f'{sid}: physical slot denominator')
    if len(slots) != int(doc['identity']['source_column_count']):
        fail.append(f'{sid}: identity physical count')
    all_slots[sid] = slots
    # items
    ids = [x['implementation_id'] for x in doc['items']]
    if len(ids) != len(set(ids)):
        fail.append(f'{sid}: duplicate item IDs')
    if len(ids) != int(roster_by[sid]['original_items']):
        fail.append(f'{sid}: item denominator {len(ids)} != {roster_by[sid]["original_items"]}')
    if len(ids) != int(doc['identity']['original_item_count']):
        fail.append(f'{sid}: identity item count')
    ev_by_id = {x['implementation_id']: x for x in item_ev.get(sid, [])}
    if set(ids) != set(ev_by_id):
        fail.append(f'{sid}: item ID set differs from evidence ({len(ids)} vs {len(ev_by_id)})')
    for it in doc['items']:
        iid = it['implementation_id']
        all_items.setdefault(iid, []).append(sid)
        ev = ev_by_id.get(iid)
        if ev is None:
            continue
        if it['exact_identity_sha256'] != ev['exact_identity_sha256']:
            fail.append(f'{sid}/{iid}: exact identity hash differs')
    # source item count in evidence
    summary.append((sid, len(slots), len(ids)))
    # supported scope
    sup = doc['supported_scope']
    source_rows.append({
        'source_id': sid,
        'declared_supported': sup['declared_supported'],
        'expectation': sup['native_validation_expectation'],
        'supported_question_ids': len(set(sup['supported_question_ids'])),
        'questions': len(doc['questions']),
        'response_slots': len(doc['response_slots']),
        'weight_slots': len(doc['weight_slots']),
        'routing_rules': len(doc['routing']),
        'coordinate_slots': len(doc['coordinate_slots']),
        'residuals': len(doc['residuals']),
        'held_dispositions': sum(1 for s in doc['physical_slots'] if str(s['disposition']).startswith('HELD')),
        'config_path': str(cand.relative_to(ROOT)),
    })

# global totals
tot_slots = sum(x[1] for x in summary)
tot_items = sum(x[2] for x in summary)
if tot_slots != 18413: fail.append(f'total physical slots {tot_slots} != 18413')
if tot_items != 18276: fail.append(f'total items {tot_items} != 18276')
if len(all_items) != 18276: fail.append(f'unique implementation IDs {len(all_items)} != 18276')
if any(len(v) != 1 for v in all_items.values()):
    fail.append('an implementation ID occurs in more than one source config')
if len(unmatched_ids) != 26: fail.append('unmatched list count != 26')
# unmatched present and explicitly held
for iid, rec in unmatched_ids.items():
    if iid not in all_items:
        fail.append(f'unmatched {iid} absent from configs')
missing_link = []
for sid in SIDS:
    doc = load_json(aug(next(x['config_path'] for x in source_rows if x['source_id']==sid), sid))
    for it in doc['items']:
        if it['implementation_id'] in unmatched_ids:
            if it.get('relation') is not None:
                fail.append(f'{sid}/{it["implementation_id"]}: unmatched carries relation')
            if 'UNMATCHED' not in (it['mapping_status'] + ' ' + it['disposition'] + ' ' + it['authority_status']):
                missing_link.append((sid, it['implementation_id']))
if missing_link:
    fail.append(f'unmatched IDs not marked explicit: {missing_link[:5]}')

# relation accounting: exact rows
exact = 0
rel_by_status = {}
for sid in SIDS:
    dop = next(x for x in source_rows if x['source_id']==sid)
    doc = load_json(aug(dop['config_path'], sid))
    for it in doc['items']:
        rel = it.get('relation')
        if rel is not None:
            status = rel.get('status')
            rel_by_status[status] = rel_by_status.get(status, 0) + 1
            if status in ('EXACT', 'EXACT_MATCH', 'MATCHED_EXACT'):
                exact += 1

print(json.dumps({
    'failures': fail,
    'totals': {'physical_slots': tot_slots, 'items': tot_items, 'unique_items': len(all_items),
               'unmatched_ids': len(unmatched_ids), 'exact_relation_items': exact,
               'relation_status_counts': rel_by_status},
    'sources': source_rows,
}, indent=1))
