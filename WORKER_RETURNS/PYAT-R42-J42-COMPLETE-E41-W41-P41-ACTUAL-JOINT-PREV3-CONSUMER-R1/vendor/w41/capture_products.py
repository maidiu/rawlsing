"""Execute maximal enumerated lawful bank and publish scoped receipts."""
import json,hashlib,sys
from pathlib import Path
import objective_world as w
ROOT=Path(__file__).resolve().parent

def write(name,data):
    b=(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n').encode();(ROOT/name).write_bytes(b)
    return hashlib.sha256(b).hexdigest()

def validate(p):
    expected={f'{family}/{mode}/budget{budget}' for family in w.FAMILIES for mode in w.CLOCKS for budget in (0,2,5,10)}
    if set(p['worlds'])!=expected:raise ValueError('EXPECTED_WORLD_OUTPUT_OMISSION')
    if set(p['multifield'])!={f'W{i}' for i in range(1,9)}:raise ValueError('EXPECTED_F6_CASE_OMISSION')
    if len(p['independent_fields']['values_read'])!=2:raise ValueError('EXPECTED_NATIVE_FIELD_OMISSION')
    if p['retained_context']['state']!='RETAINED_CONTEXT_VALUES_READ':raise ValueError('EXPECTED_RETAINED_FF_PRODUCT_MISSING')
    if p['position_context']['state']!='EXACT_J04_RECONSTRUCTION_CONTEXT_READ':raise ValueError('EXPECTED_J04_PRODUCT_MISSING')
    for view in p['worlds'].values():
        if view['native_consumer']['material']['state']!='OPTIONS_AND_SOURCE_SUPPORT_PRODUCED':raise ValueError('EXPECTED_ORIGINAL_CLIENT_PRODUCT_MISSING')
    if p['temporal']['measured_delta'] is not None:raise ValueError('UNISSUED_MEASURED_TEMPORAL_DELTA')

def capture():
    p=w.product();validate(p)
    digest=write('current_historical_asof_world_consumer_receipts.json',p)
    write('field_forge_structural_product_refs.json',dict(
        retained_GT2=p['retained_context'],retained_J04=p['position_context'],
        native_selected_keys=list(w.t35.E.STRUCTURAL_KEYS),
        modeled_rule_families=list(w.FAMILIES),
        limits='No V555 route or strong mechanism truth; no new structural position issuer; GT2 M5 operative currentness held'))
    write('multifield_nonpooling_and_bounds_receipts.json',dict(
        independent_source_fields=p['independent_fields'],native_F6_evidence=p['multifield'],
        matched=[dict(case='W1',state='SUPPORTED_SYNTHESIS',use='SOURCEFREE_EXPERIMENT_ONLY')],
        unmatched=[dict(evidence=f'W{i}',world='E04_ABC_Y_SYNTHETIC_RELEASE',state='NO_MATCHED_SOURCE_ESTIMAND_OR_TRANSPORT_CONTRACT') for i in range(1,9)],
        F6_N9_join='HOLD_EXACT_F6_REAL_USE_AND_WORLD_PURPOSE_ADMISSION_REQUIRED',
        world_consumer='ObjectiveWorld.evidence_view reads actual F6P, changes display class and preserves bounds; separate scope; not an authorized N9 F6 join'))
    write('measured_temporal_eligibility_and_method.json',p['temporal'])
    dependencies={}
    for key,view in p['worlds'].items():
        dependencies[key]=dict(snapshot=view['snapshot_hash'],selected_learned=view['learned_binding'],
            structural_refs={k:v['field_ref'] for k,v in view['structural_values'].items()},
            consumer_hash=view['native_consumer']['receipt_hash'],
            original_client='product.nonparent.consume; NONPARENT_OPTIONS')
    write('world_snapshot_and_dependency_graph.json',dict(schema=w.SCHEMA,
        worlds=dependencies,retained_context_resolution=p['retained_context']['resolution_ref'],
        position_resolution=p['position_context']['resolution_ref'],
        native_fields=p['independent_fields']['dependency_readset'],
        F6_products={k:v['product_ref'] for k,v in p['multifield'].items()},
        source_isolation='No cross-bank respondent, unit, scope or probability merge',
        purposes=p['purposes'],receipt_file_sha256=digest))
    # Capture actual imports with relative paths, exact imported bytes and pin ancestry.
    pins={x['local']:x for x in json.loads((ROOT/'owner_pins.json').read_text())}
    imports=[]
    for name,mod in sorted(sys.modules.items()):
        path=getattr(mod,'__file__',None)
        if not path:continue
        path=Path(path).resolve()
        if path.suffix!='.py' or not path.is_relative_to(ROOT):continue
        local=path.relative_to(ROOT).as_posix();b=path.read_bytes()
        imports.append(dict(module=name,module_file=local,sha256=hashlib.sha256(b).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),owner_pin=pins.get(local)))
    write('evidence/imports.json',imports)
    summary=dict(product_sha256=digest,world_views=len(p['worlds']),F6_cases=len(p['multifield']),
        retained_F5_paths=2,native_separate_fields=2,measured_pairs=0,
        no_drop='PASS_FOR_FROZEN_ENUMERATED_BANK_ONLY',all35_occupancy='HELD_NOT_PROVED')
    write('evidence/product_capture.json',summary)
    return summary

if __name__=='__main__':print(json.dumps(capture(),sort_keys=True))
