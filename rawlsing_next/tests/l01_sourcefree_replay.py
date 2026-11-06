"""Deterministic L01 cold first-consumer replay and executable-source receipt."""
from pathlib import Path
import hashlib
import json
import sys

from rawlsing_next.tests.test_l01_evidence_world_consumer import build_evidence_world, view
from rawlsing_next.pre553_empirical_objects import semantic_hash


def replay():
    handle, readers, _, _, _ = build_evidence_world()
    first = view(handle)
    second = view(handle, 'T1')
    assert first.state == second.state == 'PROGRESSIVE_WORLD_SELECTED_VIEW'
    assert first.world_routes != second.world_routes
    assert first.n10e_steps == second.n10e_steps
    for step, native, reader in zip(first.n10e_steps, first.n10w['world_conditioned_prefixes'], readers):
        assert step['request_key'] == reader.request.key
        material = native['native_material']
        assert material['state'] == 'OPTIONS_AND_SOURCE_SUPPORT_PRODUCED'
        assert material['source_balance_reads'][0]['denominator'] == 4
        assert material['source_balance_reads'][0]['source_balance_count'] == 4
        assert material['route_probability'] is None
    root = Path(__file__).resolve().parents[2]
    modules = {}
    for module in tuple(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if not filename: continue
        path = Path(filename).resolve()
        if not path.is_relative_to(root) or path.suffix != '.py': continue
        modules[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        'scope': 'SOURCEFREE_TEST_ONLY_AUTHOR_REPLAY',
        'first_consumer': 'rawlsing_next.sourcefree_world.nonparent.consume',
        't0': first.material(), 't1': second.material(),
        'loaded_repository_source_sha256': dict(sorted(modules.items())),
        'output_hash': semantic_hash([first.material(), second.material()]),
        'runtime_historical_git_required': False,
    }


if __name__ == '__main__':
    print(json.dumps(replay(), sort_keys=True, indent=2))
