#!/usr/bin/env python3
"""P6 independent fixture-native replay for all 35 sources."""
from __future__ import annotations
import json, time, traceback
from pathlib import Path
import sys

ROOT = Path('/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r157-final-review')
sys.path.insert(0, str(ROOT))
from rawlsing_next.source_configuration.library import SourceConfigLibrary

lib = SourceConfigLibrary()
rows = {sid: lib.records[sid] for sid in lib.available_source_ids()}
out = {'index_hash': None, 'sources': [], 'failures': []}
for sid in sorted(rows):
    t0 = time.time()
    rec = {'source_id': sid}
    try:
        original = lib.load_original(sid)
        fixture = lib.load_fixture_config(sid)
        stream = lib.load_fixture_stream(sid)
        sup = fixture.document['supported_scope']
        orig_sup = original.document['supported_scope']
        rec.update({
            'fixture_declared_supported': sup['declared_supported'],
            'fixture_expectation': sup['native_validation_expectation'],
            'fixture_supported_questions': len(set(sup['supported_question_ids'])),
            'original_declared_supported': orig_sup['declared_supported'],
            'original_expectation': orig_sup['native_validation_expectation'],
            'fixture_items': len(fixture.document['items']),
            'fixture_physical_slots': len(fixture.document['physical_slots']),
            'original_items': len(original.document['items']),
            'original_physical_slots': len(original.document['physical_slots']),
            'fixture_source_sha256': stream.source_sha256,
            'fixture_row_count': stream.row_count,
            'fixture_identity_class': fixture.identity_class,
            'fixture_purpose': fixture.config_purpose,
        })
        release = lib.build_fixture_release(sid)
        rec['release_ref'] = release.release_ref.as_dict()
        rec['semantic_release_hash'] = release.semantic_release_hash
        rec['public_object_count'] = len(release.public_objects)
        rec['release_matches_index'] = release.release_ref.content_hash == (rows[sid].get('release_ref') or {}).get('content_hash')
        if not rec['release_matches_index']:
            out['failures'].append(f'{sid}: release hash differs from index')
        if sup['declared_supported'] is not True:
            out['failures'].append(f'{sid}: fixture declared_supported is not true')
        if sup['native_validation_expectation'] != 'POSITIVE_RELEASE':
            out['failures'].append(f'{sid}: fixture expectation is {sup["native_validation_expectation"]}')
        if len(fixture.document['items']) != len(original.document['items']):
            out['failures'].append(f'{sid}: fixture/original item count differs')
        if len(fixture.document['physical_slots']) != len(original.document['physical_slots']):
            out['failures'].append(f'{sid}: fixture/original slot count differs')
    except BaseException as exc:
        rec['error'] = f'{type(exc).__name__}: {exc}'
        rec['traceback'] = traceback.format_exc()
        out['failures'].append(f'{sid}: {type(exc).__name__}: {exc}')
    rec['seconds'] = round(time.time() - t0, 3)
    out['sources'].append(rec)
    print(json.dumps(rec, sort_keys=True), flush=True)

print(json.dumps({'summary': {'sources': len(out['sources']), 'failures': out['failures']}}, indent=1), flush=True)
Path('/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r157-final-review/.r61/r157-p6/native_replay.json').write_text(json.dumps(out, indent=1))
