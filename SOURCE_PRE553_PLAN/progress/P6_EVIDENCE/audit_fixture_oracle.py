#!/usr/bin/env python3
"""P6 fixture-oracle consistency audit (read-only)."""
from __future__ import annotations
import json, sys, traceback
from pathlib import Path
ROOT = Path('/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r157-final-review')
sys.path.insert(0, str(ROOT))
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.source_configuration.fixture import load_fixture_stream

lib = SourceConfigLibrary()
fail = []
rows = []
for sid in sorted(lib.available_source_ids()):
    o = lib.load_original(sid).document
    f = lib.load_fixture_config(sid).document
    stream = lib.load_fixture_stream(sid)
    cells = tuple(stream.iter_cells())
    osup = set(o['supported_scope']['supported_question_ids'])
    fsup = set(f['supported_scope']['supported_question_ids'])
    fq = {q['question_id'] for q in f['questions']}
    fslots = {(s['ordinal'], s['name']) for s in f['physical_slots']}
    cellslots = {(c.variable_ordinal, c.variable_name) for c in cells}
    response_q = {x['question_id'] for x in f['response_slots']}
    response_slots = {(x['slot']['ordinal'], x['slot']['name']) for x in f['response_slots']}
    coordinate_slots = {(x['slot']['ordinal'], x['slot']['name']) for x in f['coordinate_slots']}
    weight_slots = {(x['slot']['ordinal'], x['slot']['name']) for x in f['weight_slots']}
    rows.append({
        'source_id': sid,
        'original_supported': len(osup),
        'fixture_supported': len(fsup),
        'fixture_questions': len(fq),
        'fixture_response_slots': len(response_slots),
        'fixture_coordinate_slots': len(coordinate_slots),
        'fixture_weight_slots': len(weight_slots),
        'fixture_physical_slots': len(fslots),
        'fixture_cells': len(cells),
        'supported_eq': osup == fsup,
        'supported_subset': fsup <= fq,
        'all_response_questions_supported': response_q <= fsup,
        'all_supported_have_response': fsup <= response_q,
        'all_fixture_slots_in_cells': fslots <= cellslots,
        'all_cells_in_fixture_slots': cellslots <= fslots,
        'response_slots_in_fslots': response_slots <= fslots,
        'coordinate_slots_in_fslots': coordinate_slots <= fslots,
        'weight_slots_in_fslots': weight_slots <= fslots,
    })
    if osup != fsup:
        fail.append(f'{sid}: original supported set differs from fixture supported set ({len(osup)} vs {len(fsup)})')
    for k in ('supported_subset','all_response_questions_supported','all_supported_have_response',
              'all_fixture_slots_in_cells','all_cells_in_fixture_slots','response_slots_in_fslots',
              'coordinate_slots_in_fslots','weight_slots_in_fslots'):
        if not rows[-1][k]:
            fail.append(f'{sid}: {k} false')
print(json.dumps({'failures': fail, 'sources': rows}, indent=1))
