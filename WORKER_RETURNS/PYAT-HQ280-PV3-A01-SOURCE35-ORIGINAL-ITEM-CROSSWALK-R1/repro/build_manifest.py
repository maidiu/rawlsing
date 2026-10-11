#!/usr/bin/env python3
"""HQ280 PV3 A01 — build 06_MANIFEST.json (hashes + external pointers).

Large/sensitive derived data is hash-pinned and kept OUT of Git. Small reports are hashed.
Manifest records: input hashes, per-file report hashes, external large dataset SHA/size/
availability, control refs, terminal string, and changed-file inventory.
"""
import json, hashlib, os, glob, subprocess

BASE = '/tmp/rawlsing_hq280_PV3A01'
RET = 'worktree/WORKER_RETURNS/PYAT-HQ280-PV3-A01-SOURCE35-ORIGINAL-ITEM-CROSSWALK-R1'

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

def main():
    # inputs
    lra_zip = '/tmp/rawlsing_hq280_LR_A/RAWLSING_HQ280_LR_A_SOURCE_SCIENCE_FORENSIC_RETURN_R1.zip'
    cw = '/tmp/rawlsing_hq280_LR_A/02_ORIGINAL_ITEM_IDENTITY_CARRIER_CROSSWALK.json'
    large = BASE + '/external/crosswalk_per_implementation.jsonl'

    # committed small reports (relative to return dir)
    committed = []
    for rel in sorted(os.listdir(RET)):
        if rel.startswith(('00_', '01_', '02_', '03_', '04_', '05_', '06_')) and rel.endswith(('.json', '.md')):
            committed.append({
                'path': rel,
                'sha256': sha256_file(os.path.join(RET, rel)),
                'bytes': os.path.getsize(os.path.join(RET, rel)),
                'committed_to_git': True,
            })
    repro = []
    for rel in sorted(glob.glob(RET + '/repro/*')):
        repro.append({
            'path': 'repro/' + os.path.basename(rel),
            'sha256': sha256_file(rel),
            'bytes': os.path.getsize(rel),
            'committed_to_git': True,
        })

    manifest = {
        'schema': 'HQ280_PV3_A01_MANIFEST@1.0.0',
        'commission': 'PYAT-HQ280-PV3-A01-SOURCE35-ORIGINAL-ITEM-CROSSWALK-R1',
        'terminal': 'HQ280_PV3_A01_ALL35_ORIGINAL_ITEM_IDENTITY_CONSERVED_OR_EXACT_INSTRUMENT_HOLDS__GITHUB_PUSHED',
        'authority_and_control': {
            'governing_decision': 'HQD-2026-10-10-280',
            'parallel_operating_seal': '908ee4e74849884b1d4c2f532209a0ca57538b67',
            'canonical_baseline': 'a70a069fa948e0f3c041b389edcc732b6b948a4f',
            'canonical_baseline_ref': 'integration/pre-main-reconciliation-r1',
            'semantic_pre_main': '1f47063c3205a45888b3c55e81e7485943ed1390',
            'lr_a_crosswalk_canonical_control_stamp': '6a8c91d99dca1ae2fd3559ba3c11ee26649e3cd9',
            'note': 'LR-A stamp is not the operating-HQ canonical; no reconciliation asserted.',
        },
        'assigned_branch': 'agent/rabochii-pyat-hq280-pv3-a01-source35-original-item-crosswalk-r1',
        'inputs': {
            'lr_a_archive': {
                'path': lra_zip,
                'sha256': sha256_file(lra_zip),
                'expected_sha256': 'e201e7923e1d34520dec7134a51e338b5204d55e39c3caa6a51b65888663600b',
                'bytes': os.path.getsize(lra_zip),
                'verified': sha256_file(lra_zip) == 'e201e7923e1d34520dec7134a51e338b5204d55e39c3caa6a51b65888663600b',
            },
            'crosswalk': {
                'path': cw, 'sha256': sha256_file(cw), 'bytes': os.path.getsize(cw),
                'schema': 'RAWLSING_HQ280_LR_A_CROSSWALK@1.0.0',
                'access': 'streamed (ijson), memory-bounded, never fully loaded',
            },
        },
        'committed_reports': committed,
        'committed_repro': repro,
        'external_large_dataset': {
            'pointer': 'WORKER_RETURNS/PYAT-HQ280-PV3-A01-SOURCE35-ORIGINAL-ITEM-CROSSWALK-R1/../external/crosswalk_per_implementation.jsonl',
            'local_path': large,
            'sha256': sha256_file(large),
            'bytes': os.path.getsize(large),
            'records': sum(1 for _ in open(large)),
            'committed_to_git': False,
            'reason': 'per-implementation identity dataset is large; hash-pinned, external only',
            'sensitivity': 'data-only identity crosswalk; no respondent microdata, no lineage export',
        },
        'acceptance_summary': {
            'original_item_identity': 'CONSERVED',
            'witness_checks_all_pass': True,
            'anti_join_two_sided': True,
            'no_respondent_microdata_executed': True,
            'semantic_adoption_granted': False,
            'model_or_use_grant': False,
            'canonical_mutated': False,
        },
        'method_notes': [
            'streaming/chunked deterministic derivation (ijson) over the 423MB crosswalk',
            'record input hash + schema in every report',
            'large data-only outputs partitioned outside Git; manifest + small per-wave counts/gap samples in Git',
            'unknown counts labeled UNKNOWN, never zero',
        ],
    }
    with open(RET + '/06_MANIFEST.json', 'w') as f:
        json.dump(manifest, f, indent=1)
    print('committed reports:', len(committed), '| repro files:', len(repro))
    print('external large sha256:', manifest['external_large_dataset']['sha256'],
          '| records:', manifest['external_large_dataset']['records'])
    print('lr_a_archive verified:', manifest['inputs']['lr_a_archive']['verified'])

if __name__ == '__main__':
    main()