"""Compare science after explicitly validating path-derived inherited hashes."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

import bootstrap_f43 as boot
import objective_world as w

CASES = ('W1', 'W2', 'W3', 'W4', 'W6', 'W7', 'W8')
MODULE = 'owners/f6p/native/rawlsing_next/pre553_heterogeneous_synthesis.py'


def projection(value, root):
    out = deepcopy(value)
    omitted = []
    for case in CASES:
        evidence = out['F6'][case]['native_evidence']['evidence']
        original_hash = evidence.pop('native_output_hash')
        portable_hash = evidence.pop('portable_projection_hash')
        if evidence['source_product']['module_file'] != MODULE:
            raise ValueError('UNEXPECTED_NATIVE_SOURCE_PATH')
        if w.semantic_hash(dict(evidence, native_output_hash=original_hash)) != portable_hash:
            raise ValueError('PORTABLE_NATIVE_RECEIPT_HASH_INVALID:' + case)
        original = deepcopy(evidence)
        original['source_product']['module_file'] = str(root.resolve() / 'deps/w41' / MODULE)
        if w.semantic_hash(original) != original_hash:
            raise ValueError('PATH_DERIVED_NATIVE_RECEIPT_HASH_INVALID:' + case)
        omitted.extend(f'/F6/{case}/native_evidence/evidence/{key}'
                       for key in ('native_output_hash', 'portable_projection_hash'))
    return out, omitted


def check(cold_root):
    warm_root = boot.ROOT
    warm_raw = (warm_root / 'world_products.json').read_bytes()
    cold_raw = (cold_root / 'world_products.json').read_bytes()
    a, omitted = projection(json.loads(warm_raw), warm_root)
    b, omitted_cold = projection(json.loads(cold_raw), cold_root)
    if omitted != omitted_cold or a != b:
        raise ValueError('COLD_SCIENTIFIC_REPLAY_MISMATCH')
    canonical = json.dumps(a, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    return dict(schema='F43_EXACT_COLD_SCIENTIFIC_REPLAY@1', scientific_projection_equal=True,
                warm_sha256=hashlib.sha256(warm_raw).hexdigest(),
                cold_sha256=hashlib.sha256(cold_raw).hexdigest(),
                scientific_projection_sha256=hashlib.sha256(canonical).hexdigest(),
                validated_then_excluded_paths=omitted,
                native_hashes_validated_against_actual_module_paths=True,
                limitation='Raw product bytes differ in 14 inherited path-derived hashes; no observation, clock, population, mass, uncertainty, permission, release or source identity is excluded')


if __name__ == '__main__':
    result = check(Path(sys.argv[1]))
    (boot.ROOT / 'evidence/cold_replay.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
