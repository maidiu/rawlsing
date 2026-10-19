"""Verify the discovered sourcefree portable export without reading survey data.

The external packet is never executed. Only its pinned files and unchanged
canonical catalog objects are read. Native I03/Batch/M1 are not invoked.
"""
import argparse
from collections import Counter, defaultdict
import datetime
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))
from rawlsing_next.pre553_empirical_authority import Pre553AuthorityConflict
from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_batch_runner import BatchUnitSpec, BatchManifest, BatchExecutionRunner, BatchIntegrityError
import retained_catalog

MANIFEST_SHA = '46b38c21f2b331575b12f2eadd09348299ab9c6736983f9f281fd48644ff8106'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def audit(packet):
    raw = (packet / '08_PACKET_MANIFEST.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA:
        raise ValueError('portable manifest identity changed')
    manifest = json.loads(raw)
    checked = []
    for spec in manifest['files']:
        if Path(spec['path']).name != spec['path']:
            raise ValueError('packet path is not a plain filename')
        data = (packet / spec['path']).read_bytes()
        if (len(data), hashlib.sha256(data).hexdigest()) != (spec['bytes'], spec['sha256']):
            raise ValueError('portable packet file drift: ' + spec['path'])
        checked.append(spec)
    checksum_files = []
    for line in (packet / 'SHA256SUMS.txt').read_text().splitlines():
        expected, filename = line.split(maxsplit=1)
        filename = filename.strip().lstrip('*')
        if Path(filename).name != filename:
            raise ValueError('checksum path is not a plain filename')
        if hashlib.sha256((packet / filename).read_bytes()).hexdigest() != expected:
            raise ValueError('packet checksum changed: ' + filename)
        checksum_files.append(filename)
    if len(checked) != 7 or len(checksum_files) != 9:
        raise ValueError('portable packet inventory drift')
    rows = [json.loads(line) for line in (packet / '04_PER_OBJECT_AUTHORITY_BINDINGS.jsonl').read_text().splitlines()]
    snapshots = [json.loads(line) for line in (packet / '03_AUTHORITY_SNAPSHOT_CLOSURE.jsonl').read_text().splitlines()]
    if Counter(x['object_family'] for x in rows) != {
        'EmpiricalFact': 60, 'EmpiricalPredicate': 35,
        'EmpiricalQuerySpec': 63, 'DiscoveryResultReceipt': 50,
    } or len(snapshots) != 24:
        raise ValueError('retained family counts drift')
    selected = [x for x in rows if x['object_family'] in ('EmpiricalQuerySpec', 'EmpiricalPredicate')] + snapshots
    for wrapper in selected:
        if hashlib.sha256(canonical(wrapper['preimage'])).hexdigest() != wrapper['preimage_sha256']:
            raise ValueError('complete retained object digest mismatch')
    documents = [x['preimage'] for x in selected]
    if canonical(documents) != gzip.decompress((HERE / 'evidence/retained_native_catalog_preimages.json.gz').read_bytes()):
        raise ValueError('banked canonical preimages differ from verified portable export')
    freeze = json.loads((HERE / 'evidence/RETAINED_NATIVE_CATALOG_FREEZE.json').read_text())
    source = freeze['independent_expected_source']
    original = subprocess.check_output(['git', 'show', source['commit'] + ':' + source['path']], cwd=REPO)
    if hashlib.sha256(original).hexdigest() != source['sha256']:
        raise ValueError('independent original Git oracle drift')
    original_refs = [x for x in json.loads(original)['exact_ref_manifest']
                     if x['kind'].split('@')[0] in ('AuthoritySnapshot', 'EmpiricalQuerySpec', 'EmpiricalPredicate')]
    if sorted(original_refs, key=lambda x: (x['kind'], x['content_hash'])) != freeze['expected_refs']:
        raise ValueError('frozen query oracle differs from independent accepted Git oracle')
    groups = defaultdict(list)
    for wrapper in snapshots:
        d = wrapper['preimage']
        fields = d['semantic_fields']
        key = tuple(fields[n] for n in ('authority_id', 'authority_version', 'authority_content_hash'))
        groups[key].append(d)
    conflicts = []
    for key, variants in groups.items():
        if len(variants) > 1:
            conflicts.append({'authority_id': key[0], 'authority_version': key[1], 'authority_content_hash': key[2],
                              'public_snapshot_hashes': [v['content_hash'] for v in variants],
                              'different_semantic_fields': [k for k in variants[0]['semantic_fields']
                                  if variants[0]['semantic_fields'][k] != variants[1]['semantic_fields'][k]]})
    try:
        retained_catalog.build_retained_catalog()
    except Pre553AuthorityConflict as exc:
        whole_archive = {'status': 'RED_PRESERVED', 'exception': type(exc).__name__, 'detail': str(exc)}
    else:
        raise AssertionError('full archive unexpectedly became a valid authority registry')
    scoped = retained_catalog.build_original_scoped_catalog()
    objects = retained_catalog.materialize_retained_objects()
    release_ref = ExactRef(**json.loads(original)['projection_and_release_refs']['release_refs'][0])
    query_ref = scoped.query_refs[0]
    query = scoped.resolve_query_exact(query_ref)
    manifest = BatchManifest(units=(BatchUnitSpec(job_kind='QUERY', job_ref=query_ref, release_refs=(release_ref,)),))
    try:
        BatchExecutionRunner(manifest=manifest, repository=C11Repository())
    except BatchIntegrityError as exc:
        batch_gate = {'grade': 'EXACT_RELEASE_PREIMAGE_UNAVAILABLE; NO_EXECUTION',
                      'exception': type(exc).__name__, 'detail': str(exc),
                      'query_ref': query_ref.as_dict(), 'release_ref': release_ref.as_dict(),
                      'native_ordered_target_refs': canonicalize(query.target_refs),
                      'native_condition_predicate_ref': canonicalize(query.condition_predicate_ref),
                      'native_risk_set_ref': canonicalize(query.risk_set_ref),
                      'native_measure_basis_ref': canonicalize(query.measure_basis_ref)}
    else:
        raise AssertionError('missing exact release unexpectedly passed native Batch gate')
    deferred = [r for r in rows if r['object_family'] == 'EmpiricalFact']
    if not all('$deferred_retained_member' in r['preimage']['dependency_refs'] for r in deferred):
        raise ValueError('Fact deferred-payload disposition changed')
    return {
        'schema': 'O35B_PORTABLE_RETAINED_PACKET_AUDIT_R1',
        'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'external_locator': 'LOCAL_TRANSFERRED_D2P_PORTABLE_PACKET; HOST_PATH_REDACTED',
        'portable_manifest_sha256': MANIFEST_SHA, 'seven_file_hashes_and_sizes': checked,
        'nine_checksum_entries_verified': sorted(checksum_files),
        'checkpoint_file_currently_available': False,
        'checkpoint_hash_grade': 'UPSTREAM_EXPORT_RECEIPT_ONLY; NOT_REMEASURED_HERE',
        'closure_identity_grade': 'RECORDED_NOT_RECOMPUTED_FROM_FULL_CHECKPOINT',
        'native_individual_objects_materialized': len(objects),
        'native_individual_object_counts': dict(Counter(o.schema_id for o in objects)),
        'independent_Git_query_predicate_snapshot_ref_counts': dict(Counter(r['kind'] for r in original_refs)),
        'original_oracle_exact_ref_count': len(json.loads(original)['exact_ref_manifest']),
        'retained_public_object_inventory_count': 234,
        'whole_24_snapshot_archive_as_one_catalog': whole_archive,
        'distinct_authority_ref_triples_in_archive': len(groups), 'conflicting_snapshot_pairs': conflicts,
        'scoped_catalog': {'snapshots': len(scoped.authorities), 'predicates': len(scoped.predicates),
                           'queries': len(scoped.queries), 'grade': 'EXACT_SOURCEFREE_NATIVE_PACKET_BINDING; NO_EXECUTION_GRANT'},
        'actual_original_query_Batch_gate': batch_gate,
        'deferred_Facts_not_materializable': len(deferred),
        'deferred_payload_bytes_upstream_declared': 3276820474,
        'source_read_calls': 0, 'I03_runs': 0, 'I05_runs': 0, 'Batch_runs': 0, 'M1_original_runs': 0,
        'original_native_execution_edge': 'NOT_PROVED',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    args = parser.parse_args()
    receipt = audit(args.packet.resolve())
    (HERE / 'evidence/retained_packet_audit.json').write_text(json.dumps(receipt, indent=2) + '\n')
    for name in ('retained_catalog_junit.xml', 'retained_full_catalog_RED.xml'):
        file = HERE / 'evidence' / name
        tree = ET.parse(file)
        for element in tree.iter():
            if 'hostname' in element.attrib:
                element.set('hostname', 'LOCAL_HOST')
        serialized = ET.tostring(tree.getroot(), encoding='unicode')
        file.write_text('\n'.join(line.rstrip() for line in serialized.splitlines()) + '\n')
    print(json.dumps({'individual_objects': receipt['native_individual_objects_materialized'],
                      'scoped_catalog': receipt['scoped_catalog'], 'archive_conflict_pairs': len(receipt['conflicting_snapshot_pairs']),
                      'deferred_facts': receipt['deferred_Facts_not_materializable']}))
