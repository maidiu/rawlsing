"""Reproducible cold product, control receipts and exact import custody."""
import bootstrap
from pathlib import Path
import hashlib
import importlib
import json
import subprocess
import sys
from world_join import SelectedWorld, product, t35
from fixture import ref
from product.nonparent import consume
from rawlsing_next.pre553_empirical_objects import semantic_hash
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
EVIDENCE=ROOT/'evidence'
def write(name,value):
    (EVIDENCE/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
def controls():
    w=SelectedWorld();w.stage_release('alternate')
    source_hashes={k:p.native_provider.world['rows_hash'] for k,p in w.release_bank.items()}
    a=w.epoch(t35.E2);rules=deepcopy(w.service.catalog.records)
    w.select_release('alternate');b=w.epoch(t35.E2)
    assert source_hashes=={k:p.native_provider.world['rows_hash'] for k,p in w.release_bank.items()}
    assert rules==w.service.catalog.records and a['snapshot']['fields']==b['snapshot']['fields']
    p=w.prepared;snapshot=w.snapshot(t35.E2);stored=p.composition.m2_artifacts.release
    p.repository._releases.pop(stored.ref.key)
    try:
        consume(w.service,snapshot)
    except ValueError as exc:
        removed=dict(state='REFUSED',reason=str(exc))
    else:
        raise AssertionError('REMOVED_RELEASE_STILL_CONSUMED')
    p.repository.register_release(stored)
    restored=consume(w.service,snapshot)
    assert restored==b['nonparent']
    checkpoint=p.lifecycle.export_checkpoint();selected=p.composition.b5_selection_receipt
    p.lifecycle.withdraw_product(selected.selected_release_ref,withdrawal_reason_ref=ref('Reason','revoke'),withdrawal_scope_ref=p.contract.selection_scope_ref,event_authority_ref=ref('LifecycleAuthority','withdraw'),event_rule_ref=ref('LifecycleRule','withdraw'),selection_attestation_ref=ref('SelectionAttestation','withdraw'),current_transitions={selected.selection_key_ref.key:None})
    try:
        consume(w.service,w.snapshot(t35.E1))
    except ValueError as exc:
        withdrawn=dict(state='REFUSED_FRESH_HISTORICAL',reason=str(exc))
    else:
        raise AssertionError('WITHDRAWN_HISTORICAL_EVIDENCE_FRESHLY_USED')
    archive=w.service.historical_receipt(restored['receipt_hash'])
    assert archive['fresh_use_authorized'] is False
    base=SelectedWorld(rules='base').epoch(t35.E2)
    return dict(release_only=dict(before=a,after=b,structural_objects_unchanged=True,
                all_upstream_source_hashes_before_and_after=source_hashes,
                mechanism='Actual I4 REGISTER/PUBLISH/SELECT_CURRENT in shared M2/B5 stores; no row or rule edits'),
                rule_only=dict(base=base,revised=a,empirical_unchanged=base['nonparent']['material']['empirical']==a['nonparent']['material']['empirical']),
                removal=removed,restored_nonparent=restored,withdrawal=withdrawn,
                archival=archive,archival_b5_selection=p.lifecycle.resolve_current_as_of(selected.selection_key_ref,as_of_checkpoint=checkpoint).selected_release_ref.as_dict())
def imports():
    records=[]
    for name,module in sorted(sys.modules.items()):
        file=getattr(module,'__file__',None)
        if not file:continue
        path=Path(file).resolve()
        if not path.is_relative_to(REPO) or path.suffix!='.py':continue
        data=path.read_bytes();relative=path.relative_to(REPO).as_posix()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        record=dict(module=name,module_file=relative,blob_sha1=blob,sha256=hashlib.sha256(data).hexdigest())
        if relative.startswith('rawlsing_next/'):
            expected=subprocess.check_output(['git','rev-parse',bootstrap.SEALED+':'+relative],text=True).strip()
            assert blob==expected,(name,'UNPINNED_NATIVE_IMPORT')
            record.update(commit=bootstrap.SEALED,expected_blob_sha1=expected,preimage='MATCH')
        records.append(record)
    return records
from copy import deepcopy
if __name__=='__main__':
    EVIDENCE.mkdir(exist_ok=True)
    cold=[]
    for label in ('a','b'):
        data=subprocess.check_output([sys.executable,'-B',str(ROOT/'world_join.py')],cwd=REPO)
        (EVIDENCE/('cold_'+label+'.json')).write_bytes(data)
        cold.append(dict(label=label,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
    assert cold[0]['sha256']==cold[1]['sha256']
    write('cold_replay.json',dict(state='BYTE_IDENTICAL_FRESH_PROCESSES',runs=cold))
    write('controls.json',controls())
    write('imports.json',imports())
    manifest=json.loads((ROOT/'source_manifest.json').read_text())
    for pin in manifest:
        actual=(ROOT/pin['local']).read_bytes()
        expected=subprocess.check_output(['git','show',pin['commit']+':'+pin['path']])
        assert actual==expected,pin['local']
    write('owner_preimages.json',dict(state='ALL_EXACT_VENDOR_PREIMAGES_MATCH',pins=manifest))
