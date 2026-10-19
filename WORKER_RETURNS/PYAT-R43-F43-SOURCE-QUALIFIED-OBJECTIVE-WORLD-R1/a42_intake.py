"""Exact A42 receipt-intake validation only; no estate rerun or adoption."""
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
LOCAL = ROOT / 'deps/a42'


def dependencies():
    manifest = json.loads((ROOT / 'a42_dependency_manifest.json').read_text())
    raw = (ROOT / 'a42_intake_dependency.tar.gz').read_bytes()
    if hashlib.sha256(raw).hexdigest() != manifest['archive_sha256']:
        raise ValueError('A42_ARCHIVE_CHANGED')
    pins = {p['local']: p for p in manifest['files']}
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as stream:
        if {m.name for m in stream.getmembers()} != set(pins):
            raise ValueError('A42_MEMBERS_CHANGED')
        for member in stream.getmembers():
            data = stream.extractfile(member).read()
            dest = LOCAL / member.name
            if not member.isfile() or not dest.resolve().is_relative_to(LOCAL.resolve()):
                raise ValueError('UNSAFE_A42_MEMBER')
            if hashlib.sha256(data).hexdigest() != pins[member.name]['sha256']:
                raise ValueError('A42_OWNER_PREIMAGE_CHANGED')
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(data)
            if dest.read_bytes() != data:
                raise ValueError('A42_IMPORT_CHANGED')
    sys.path.insert(0, str(LOCAL))
    from a42 import core
    return core


def make_bank(commit):
    core = dependencies()
    gp = core.GitPreimage(REPO)
    prefix = ROOT.relative_to(REPO).as_posix()
    products = json.loads(gp.blob_at(commit, prefix + '/world_products.json'))
    artifact_paths = ['world_products.json', 'f43_product.py', 'bounded_methods.py',
                      '00_EXPECTED_WORLD_FREEZE.json', '01_METHOD_ORACLE.json',
                      'cell_envelope_bounds.py', 'bootstrap_f43.py',
                      'dependency_manifest.json', 'w41_dependency.tar.gz',
                      'evidence/imports.json', 'output_grades.json',
                      'tests/test_bounded_world.py', 'tests/test_bounded_world.py.proof.json',
                      'evidence/proof_witness.json']
    artifacts = [gp.verify(commit, prefix + '/' + path) for path in artifact_paths]
    defs = [
        ('F43-RETAINED-F5-CONTEXT', 'HISTORICAL_RETAINED_EVIDENCE', ['SRC02'], ['F5'], [],
         'retained_view GT2 FF/V554/M4 CONTEXT and J04 source-domain reconstruction'),
        ('F43-BOUNDED-F6-CANDIDATE', 'SOURCEFREE_LOCAL_POSITIVE', [], [], ['F6'],
         'f6_view F6M/F6P partial conditionals; original_N9_admitted=false'),
        ('F43-TEMPORAL-CANDIDATE', 'SOURCEFREE_LOCAL_POSITIVE', [], [], ['F7'],
         'temporal_view V553/EE1 and strict pre-guard; no observed pair'),
        ('F43-ORIGINAL-E04-TEST', 'SOURCEFREE_INTEGRATED_POSITIVE', [], [], ['F5','F7'],
         'unchanged product.nonparent.consume NONPARENT_OPTIONS under T35 TEST_ONLY rules'),
    ]
    receipts = []
    for rid, grade, waves, gates, functional, claim in defs:
        receipts.append(dict(receipt_id=rid, origin_commit=commit, claim_id=claim, grade=grade,
            coverage=dict(wave_ids=waves, axis_ids=[], f_gate_ids=gates, functional_gates=functional,
                          register_151_ids=[], ledger_101_ids=[], global_relations=[],
                          global_contributions=functional,
                          occupancy_grain_note='Retained or sourcefree exact scope only; zero new original measured cells'),
            currentness=dict(archive_or_current='ARCHIVE', as_of='2026-10-19',
                             note='T35 TEST_CURRENT uses explicit future fixture clocks; never real CURRENT'),
            artifacts=artifacts, unknown_bounds=dict(original_measured_occupancy=0,
                observed_temporal_pairs=0, real_F6_N9_join=False,
                independent_new_method_acceptance=False), downstream_consumer_read_refs=[]))
    return dict(schema=core.R41_SCHEMA, receipts=receipts,
                full_original_product_complete=products['full_original_F5_F7_N9_complete'])


def validate_bank(bank):
    core = dependencies(); gp = core.GitPreimage(REPO)
    scope = core.load_scope(gp)
    accepted = core.ingest_r41_bank(bank, gp, scope)
    controls = {}
    # Actual A42 guards must reject false original occupancy and forged consumer.
    bad = deepcopy(bank); bad['receipts'][0]['grade'] = 'ORIGINAL_MEASURED_OCCUPANCY'
    try:
        core.ingest_r41_bank(bad, gp, scope)
    except core.PreimageError as exc:
        controls['sourcefree_promoted_to_original'] = str(exc)
    else:
        raise AssertionError('A42_ACCEPTED_FALSE_PROMOTION')
    bad = deepcopy(bank); bad['receipts'][0]['downstream_consumer_read_refs'] = ['F43_FAKE_ACTOR_RECEIVER']
    try:
        core.ingest_r41_bank(bad, gp, scope)
    except core.PreimageError as exc:
        controls['forged_consumer'] = str(exc)
    else:
        raise AssertionError('A42_ACCEPTED_FORGED_CONSUMER')
    return dict(schema='F43_A42_NATIVE_INTAKE@1', validated_receipts=len(accepted),
                owner='A42 exact 843175b0587b54db3df1f461ad9f7f1314894372',
                receipt_ids=[r['receipt_id'] for r in accepted], negative_controls=controls,
                original_measured_delta=0, N11_adoption=False, N12_wake=False,
                scope='Exact native intake only; A42 full estate was not rerun or mutated')


if __name__ == '__main__':
    commit = sys.argv[1]
    bank = make_bank(commit)
    result = validate_bank(bank)
    (ROOT / 'A42_RECEIPT_BANK.json').write_text(json.dumps(bank, indent=2) + '\n')
    (ROOT / 'evidence/a42_native_intake.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
