"""Reconcile published U43 metadata with F43's immutable prospective scope.

This reads no survey input and performs no source/semantic/operation issuance.
Historical source hashes and country aliases narrow issuer questions only.
"""
import hashlib
import io
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parent


def read_inputs():
    manifest = json.loads((ROOT / 'u43_metadata_read_cut_manifest.json').read_text())
    raw = (ROOT / 'u43_metadata_read_cut.tar.gz').read_bytes()
    if hashlib.sha256(raw).hexdigest() != manifest['archive_sha256']:
        raise ValueError('U43_METADATA_ARCHIVE_CHANGED')
    pins = {r['local']: r for r in manifest['files']}
    values = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as stream:
        if {m.name for m in stream.getmembers()} != set(pins):
            raise ValueError('U43_METADATA_MEMBERS_CHANGED')
        for member in stream.getmembers():
            if not member.isfile():
                raise ValueError('U43_NONFILE_METADATA')
            data = stream.extractfile(member).read()
            pin = pins[member.name]
            blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            if hashlib.sha256(data).hexdigest() != pin['sha256'] or blob != pin['blob_sha1']:
                raise ValueError('U43_METADATA_PREIMAGE_CHANGED')
            values[member.name] = json.loads(data)
    return manifest, values


def reconcile():
    manifest, inputs = read_inputs()
    frozen_raw = (ROOT / '00_EXPECTED_WORLD_FREEZE.json').read_bytes()
    frozen = json.loads(frozen_raw)
    packets = inputs['original35_issuer_decision_packets.json']
    permitted = inputs['currently_permitted_native_manifests.json']
    handoff = inputs['B43_A42_HANDOFF.json']
    summary = inputs['evidence/original35_frontier_summary.json']
    expected_ids = [w['id'] for w in frozen['waves']]
    if [p['atlas_id'] for p in packets] != expected_ids or [p['atlas_id'] for p in permitted['waves']] != expected_ids:
        raise ValueError('U43_F43_WAVE_OMISSION_OR_IDENTITY_DISAGREEMENT')
    suffixes = ('SOURCE_HOST_PURPOSE', 'COMPLETE_NATIVE_U', 'RESPONSE_ROUTING_CARRIER',
                'SCIENTIFIC_E_PRE', 'CONSUMER_PURPOSE')
    authority = {p['atlas_id']: p for p in permitted['waves']}
    rows = []
    countries = {}
    for wave, packet in zip(frozen['waves'], packets):
        sid = wave['id']; source = packet['source']; current = authority[sid]
        decisions = [d['demand_id'] for d in packet['demands']]
        if decisions != [sid + ':' + suffix for suffix in suffixes] or set(current['owner_decisions']) != set(decisions):
            raise ValueError('U43_EXACT_OWNER_DECISION_CLOSURE_CHANGED:' + sid)
        if (packet['competent_issuer_identity'] is not None or
                any(d['authenticated_owner_ref'] is not None for d in packet['demands']) or
                source['current_source_access_permission'] is not None or
                source['current_source_edition_hash'] is not None or
                current['native_manifest'] is not None or current['state'] != 'NOT_YET_ISSUED'):
            raise ValueError('NEW_POTENTIAL_AUTHORITY_REQUIRES_SEPARATE_REVIEW:' + sid)
        countries[sid] = sorted({r['canonical_iso2'] for r in source['historical_country_rows']
                                 if r.get('canonical_iso2')})
        rows.append(dict(source_id=sid, source_name=wave['name'],
            F43_decision_id=f'F43-{sid}-SOURCE-FIELD-TIME', U43_decision_ids=decisions,
            U43_research_inventory_root=packet['research_inventory_root'],
            historical_source_hashes=source['historical_country_registry_source_hashes'],
            historical_country_aliases=countries[sid],
            current_native_manifest=None, current_source_permission=None,
            current_source_edition_hash=None, complete_administered_U=None,
            independently_issued_E_pre=None, original_measured_occupancy=False,
            downstream_F5_F6_F7_decisions_still_required=True,
            interpretation='Metadata narrows issuer requests; historical country or source hash is not current population/design/time compatibility'))
    if (permitted['original_measured_wave_count'] != 0 or permitted['U_E_pre_count'] is not None
            or handoff['permitted_original_manifests'] or handoff['source_or_actor_rights_issued']
            or summary['original_permitted_manifests'] != 0):
        raise ValueError('U43_STATUS_REQUIRES_NEW_SOURCE_QUALIFICATION')
    pairs = []
    for candidate in frozen['pairs']:
        left, right = candidate['left'], candidate['right']
        overlap = sorted(set(countries[left]) & set(countries[right]))
        pairs.append(dict(left=left, right=right, family_relation=candidate['family_relation'],
            documented_historical_country_overlap=overlap,
            country_metadata_state='HISTORICAL_ALIAS_CANDIDATE_ONLY' if countries[left] and countries[right]
                else 'HISTORICAL_COUNTRY_METADATA_INCOMPLETE',
            F6_target_estimand_compatibility=None, F7_observed_comparable_pair=None,
            source_or_transport_permission=False,
            interpretation='No overlap is not intrinsic nonapplicability; overlap does not authorize population joins or observed change'))
    if len(rows) != 35 or len(pairs) != 595 or sum(len(r['U43_decision_ids']) for r in rows) != 175:
        raise ValueError('RECONCILIATION_SCOPE_LOSS')
    return dict(schema='F43_U43_PROSPECTIVE_AUTHORITY_RECONCILIATION@1',
        U43_read_cut=manifest['files'][0]['commit'], input_preimages=manifest['files'],
        F43_scope_sha256=hashlib.sha256(frozen_raw).hexdigest(),
        source_waves=rows, prospective_pairs=pairs,
        summary=dict(waves=35, F43_cells=105, prospective_pairs=595,
            exact_U43_owner_decisions=175,
            historical_source_hash_waves=sum(bool(r['historical_source_hashes']) for r in rows),
            historical_country_metadata_waves=sum(bool(countries[r['source_id']]) for r in rows),
            same_family_candidates_with_documented_country_overlap=sum(
                p['family_relation']=='SAME_FAMILY_CANDIDATE_ONLY' and bool(p['documented_historical_country_overlap']) for p in pairs),
            permitted_original_manifests=0, original_measured_occupancy=0,
            original_U_count=None, eligible_E_pre_count=None),
        authority_status='NO_QUALIFYING_NEW_GRANT; all35 current manifests NOT_YET_ISSUED',
        scientific_status='RECONCILED_PROSPECTIVE_METADATA_NOT_MEASURED_F5_F6_F7',
        preserves_existing_science=True, changes_existing_A42_receipt_grade=False,
        further_execution='External source/host/purpose, operation, FF, F6 transport/model, observed-time and receiving-use decisions required')


if __name__ == '__main__':
    out = reconcile()
    (ROOT / 'U43_F43_RECONCILIATION.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out['summary']))
