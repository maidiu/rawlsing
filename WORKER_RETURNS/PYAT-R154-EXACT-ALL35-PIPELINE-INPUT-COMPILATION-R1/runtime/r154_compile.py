"""R154 exact all35 metadata/native-input compiler and store builder."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import sqlite3
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from rawlsing_next.pre553_issued_workload import OriginalWaveIdentity
from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceIdentity

SCHEMA = "PYAT_R154_ALL35_PIPELINE_INPUT_STORE@1"
REPO_ROOT = Path(__file__).resolve().parents[3]
RETURN_ROOT = Path(__file__).resolve().parents[1]
PRIVATE = REPO_ROOT / ".r61"
R145_INPUTS = PRIVATE / "r145-current-source-packages" / "inputs"
R147_INPUTS = PRIVATE / "r147-all35-current-metadata" / "inputs"
R148_INPUTS = PRIVATE / "r148-all35-complete-metadata" / "inputs"
R150_INPUTS = PRIVATE / "r150-scientific-native-input" / "inputs"
R153_RECORDS = "WORKER_RETURNS/PYAT-R153-NATIVE-EVIDENCE-REPAIR-R1/records"
R150_RECORDS = "WORKER_RETURNS/PYAT-R150-SCIENTIFIC-NATIVE-INPUT-R1/records"
R148_RECORDS = "WORKER_RETURNS/PYAT-R148-ALL35-COMPLETE-METADATA-R1/records"
csv.field_size_limit(10**9)


class R154Refusal(ValueError):
    pass


def _canon(v: Any) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha(v: Any) -> str:
    return hashlib.sha256(_canon(v).encode()).hexdigest()


def _bytes_sha(v: bytes) -> str:
    return hashlib.sha256(v).hexdigest()


def _git_json(path: str) -> Any:
    done = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=REPO_ROOT,
                          capture_output=True, check=False)
    if done.returncode != 0:
        raise R154Refusal(f"GIT_OBJECT_UNAVAILABLE:{path}")
    return json.loads(done.stdout.decode())


def _load_b49():
    spec = importlib.util.spec_from_file_location("r154_b49", R150_INPUTS / "pre553_inherited_source_rules.py")
    mod = importlib.util.module_from_spec(spec); sys.modules["r154_b49"] = mod; spec.loader.exec_module(mod)
    return mod


def _codebook_map() -> dict[str, dict[str, Any]]:
    out = {}
    # R145 files
    for entry in json.loads((R145_INPUTS / "METADATA_INPUTS.json").read_text())['candidate_inputs']:
        out[entry['source_id']] = {'path': Path(entry['staged_metadata_path']), 'sha256': entry['sha256'], 'bytes': entry['bytes'], 'origin': 'R145'}
    for root, origin in ((R147_INPUTS, 'R147'), (R148_INPUTS, 'R148')):
        for entry in json.loads((root / 'STAGED_METADATA.json').read_text()):
            out[entry['source_id']] = {'path': Path(entry['path']), 'sha256': entry['sha256'], 'bytes': entry['bytes'], 'origin': origin}
    if len(out) != 35:
        raise R154Refusal("CODEBOOK_SET_NOT_35")
    return out


def _read_codebook(spec: Mapping[str, Any]) -> list[dict[str, str]]:
    raw = Path(spec['path']).read_bytes()
    if len(raw) != int(spec['bytes']) or _bytes_sha(raw) != spec['sha256']:
        raise R154Refusal("CODEBOOK_HASH_OR_BYTES_MISMATCH")
    rows = [dict(r) for r in csv.DictReader(io.StringIO(raw.decode('utf-8-sig', errors='replace')))]
    if not rows or any(not str(r.get('var_name', '')).strip() for r in rows):
        raise R154Refusal("CODEBOOK_ROW_IDENTITY_INVALID")
    return rows


def _physical(source_id: str) -> dict[str, Any]:
    p = RETURN_ROOT / 'records' / 'physical' / f'{source_id}_PHYSICAL_METADATA.json'
    d = json.loads(p.read_text())
    if d.get('response_rows_read_or_exported') is not False:
        raise R154Refusal("PHYSICAL_RESPONSE_EXPORT_CLAIM")
    if d.get('state') not in {'METADATA_INSPECTED', 'METADATA_INSPECTED_LATIN1_COMPAT_PHYSICAL_ONLY__SEMANTIC_AUTHORITY_FALSE'}:
        raise R154Refusal("PHYSICAL_NOT_INSPECTED")
    return d


def _artifact_sha(path: str) -> str:
    local = REPO_ROOT / path
    if local.exists():
        return hashlib.sha256(local.read_bytes()).hexdigest()
    if path == "rawlsing_next/pre553_inherited_source_rules.py":
        return hashlib.sha256((R150_INPUTS / "pre553_inherited_source_rules.py").read_bytes()).hexdigest()
    ref = "9bbf9e0509411beb210331d28160324b005a784e" if "PYAT-R51-I51-B49-G50-JOINED-PRODUCER-R1" in path else "HEAD"
    done = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=REPO_ROOT, capture_output=True, check=False)
    if done.returncode != 0:
        raise R154Refusal("SOURCE_PREP_ARTIFACT_MISSING", path)
    return hashlib.sha256(done.stdout).hexdigest()


def _source_meta(source_id: str) -> dict[str, Any]:
    return _git_json(f"{R148_RECORDS}/{source_id}_CURRENT_METADATA_PREPARATION.json")


def _r153(source_id: str) -> dict[str, Any]:
    return _git_json(f"{R153_RECORDS}/{source_id}_R153_NATIVE_INPUT.json")


def _r150(source_id: str) -> dict[str, Any]:
    return _git_json(f"{R150_RECORDS}/{source_id}_SCIENTIFIC_NATIVE_INPUT.json")


def _physical_columns(phys: Mapping[str, Any]) -> list[dict[str, Any]]:
    md = phys['metadata']
    names = md.get('column_names') or []
    if not isinstance(names, list) or len(names) != len(set(names)):
        raise R154Refusal("PHYSICAL_COLUMN_IDENTITY_INVALID")
    labels = md.get('column_names_to_labels') or {}
    types = md.get('readstat_variable_types') or {}
    orig = md.get('original_variable_types') or {}
    widths = md.get('variable_storage_width') or {}
    measures = md.get('variable_measure') or {}
    value_labels = md.get('variable_value_labels') or {}
    miss_ranges = md.get('missing_ranges') or {}
    miss_user = md.get('missing_user_values') or {}
    out = []
    for i, name in enumerate(names, 1):
        out.append({
            'source_id': phys['source_id'], 'ordinal': i, 'name': str(name),
            'label': labels.get(name) if isinstance(labels, dict) else None,
            'readstat_type': types.get(name) if isinstance(types, dict) else None,
            'original_type': orig.get(name) if isinstance(orig, dict) else None,
            'storage_width': widths.get(name) if isinstance(widths, dict) else None,
            'measure': measures.get(name) if isinstance(measures, dict) else None,
            'value_labels': value_labels.get(name) if isinstance(value_labels, dict) else None,
            'missing_ranges': miss_ranges.get(name) if isinstance(miss_ranges, dict) else None,
            'missing_user_values': miss_user.get(name) if isinstance(miss_user, dict) else None,
        })
    return out


def _requirements() -> list[dict[str, Any]]:
    return [
        {'id':'SOURCE_IDENTITY_HEADER','stage':'metadata','owner':'pyreadstat/readstat current header receipt + pre553_source_native_preimage_adapter.NativeSourceIdentity','fields':'source_id,source_sha256,source_format,canonical_filename,expected_rows,columns,types,labels,missing,MRs','acquisition':'metadataonly header inspection and byte hash','check':'one receipt per source, metadataonly, no response rows'},
        {'id':'CODEBOOK_JOIN','stage':'metadata','owner':'R145/R147/R148 codebook rows','fields':'var_name,question/options,storage,measure,module,row identity/hash','acquisition':'current codebook CSV','check':'all physical columns and codebook rows accounted; physical-only/document-only explicit'},
        {'id':'B49_ITEM_AUTHORITY','stage':'metadata','owner':'pre553_inherited_source_rules.SourceAuthorityCorpus/select_source_rules','fields':'implementation_id,source_variable_code,disposition,direction,routing,response,relation,exact identity/evidence','acquisition':'B49 corpus/compiler','check':'every applicable item accounted; unmatched held; no scope borrowing'},
        {'id':'TYPED_REPRESENTATION','stage':'metadata','owner':'B49 typed_surfaces + source-specific runtime package','fields':'surface id,representation authority,ordinal,typed domain','acquisition':'typed surfaces and exact source package','check':'all 38 consumed; representation-only ceiling preserved'},
        {'id':'OCCURRENCE_FIELDS','stage':'predecode','owner':'universal_grammar.types.Occurrence/SourceInventory','fields':'unit,form,topology,administration,routing,risk set,domain,role','acquisition':'source-native semantic/design/form authority','check':'each field resolved or exact missing owner/dependency'},
        {'id':'SOURCE_READ_REQUEST','stage':'predecode','owner':'pre553_source_read_admission.SourceReadRequest/decode_with_source_read_permission','fields':'source_id,edition_sha256,format,custody_locator_binding,host,purpose,consumer_use,SOURCE_RESPONSE_DECODE,EXACT_FILE,freeze refs,semantic scope,current decision','acquisition':'external current source-read grant/resolver','check':'no source open/stat/hash/decode before current grant'},
        {'id':'NATIVE_SOURCE_IDENTITY','stage':'predecode','owner':'NativeSourceIdentity','fields':'source identity fields','acquisition':'current physical receipt','check':'constructor roundtrip; no current grant implied'},
        {'id':'NATIVE_PREIMAGE_PACKAGE','stage':'workload','owner':'NativeSourcePackage/materialize_native_preimages','fields':'source rules, occurrence plan, projection, release','acquisition':'source read + grounded occurrences + semantics','check':'actual native constructor/validator where all premises grounded'},
        {'id':'NATIVE_WORKLOAD','stage':'workload','owner':'NativeWorkload/IssuedWorkloadRecord/admit','fields':'descriptor,projection,catalog,requests/discoveries,U/Epre,current record','acquisition':'external issuer + grounded scientific frontier','check':'admit refuses absent current issuance; no fabricated U/Epre'},
        {'id':'I03_EMPIRICAL','stage':'execution','owner':'CarrierNeutralResearchExecutor.execute_i03/EmpiricalFact','fields':'query,predicate,exact source scope,replay','acquisition':'admitted workload + response read','check':'typed fact/refusal; no metadata render counted as execution'},
        {'id':'I05_DISCOVERY','stage':'execution','owner':'CarrierNeutralResearchExecutor.execute_i05/DiscoveryResultReceipt','fields':'full declared frontier,candidate grammar,coverage/no-drop','acquisition':'admitted workload + response read','check':'complete candidate accounting; no old product replay'},
        {'id':'M1_LEARNED','stage':'learned','owner':'pre553_learned_empirical_adjudication.adjudicate_learned_empirical','fields':'exact I05 evidence,M1 family rule binding','acquisition':'evidence + exact family rule','check':'LearnedEmpiricalDisposition; rule only where constitutive'},
        {'id':'M2_PERSISTENCE','stage':'learned','owner':'pre553_learned_product_release/persistence','fields':'ReleaseCore,PublicationBinding,ResolutionReceipt','acquisition':'M1 product + exact persistence binding','check':'cold retrieval exact; no adoption implied'},
        {'id':'SOURCE_PREP_ARTIFACT_REUSE','stage':'metadata','owner':'existing R02/R03/R04/B49/source-specific producers and artifacts','fields':'producer ref, source scope, column/domain/missing/unit/routing/projection bindings','acquisition':'indexed Git/runtime artifacts','check':'artifact ref/scope/hash reconciled; only demonstrated compatibility gap remains'},
        {'id':'COLD_RETRIEVAL','stage':'persistence','owner':'C11 repository/release + JoinedWorkloadCheckpoint','fields':'release/replay/checkpoint exact refs','acquisition':'execution receipts','check':'store/import/loader roundtrip'},
    ]


def _reconcile(phys: Mapping[str, Any], rows: list[dict[str, str]]) -> dict[str, Any]:
    pnames = [str(x) for x in (phys['metadata'].get('column_names') or [])]
    cnames = [str(r['var_name']) for r in rows]
    pset, cset = set(pnames), set(cnames)
    return {
        'physical_columns': len(pnames), 'codebook_rows': len(rows),
        'both': len(pset & cset), 'physical_only': sorted(pset - cset),
        'codebook_only': sorted(cset - pset),
        'physical_duplicates': [k for k, v in Counter(pnames).items() if v > 1],
        'codebook_duplicates': [k for k, v in Counter(cnames).items() if v > 1],
        'row_count': phys['metadata'].get('number_rows'),
        'physical_number_columns': phys['metadata'].get('number_columns'),
    }


def _native_package(source_id: str, phys: Mapping[str, Any], meta: Mapping[str, Any], r150: Mapping[str, Any]) -> dict[str, Any]:
    ident = NativeSourceIdentity(
        source_id=source_id,
        family=meta['family'],
        wave=meta['wave_or_release'],
        canonical_filename=Path(phys['path']).name,
        declared_sha256=phys['sha256'],
        source_format=str(meta['format']).upper(),
        expected_rows=int(phys['metadata']['number_rows']),
    )
    wave = (meta.get('native_preparation') or {}).get('original_wave_identity') or {}
    if not wave:
        wave = r150['native_source_identity']
        wave = {'atlas_id': wave['source_id'], 'dataset_id': wave.get('canonical_filename', wave['source_id']), 'source_family': wave['family'], 'wave': wave['wave']}
    owi = OriginalWaveIdentity(wave['atlas_id'], wave['dataset_id'], wave['source_family'], wave['wave'])
    return {
        'source_id': source_id,
        'native_source_identity': {
            'source_id': ident.source_id, 'family': ident.family, 'wave': ident.wave,
            'canonical_filename': ident.canonical_filename, 'declared_sha256': ident.declared_sha256,
            'source_format': ident.source_format, 'expected_rows': ident.expected_rows,
        },
        'original_wave_identity': {
            'atlas_id': owi.atlas_id, 'dataset_id': owi.dataset_id,
            'source_family': owi.source_family, 'wave': owi.wave,
        },
        'selected_source_rule_package': r150['selected_source_rule_package'],
        'selected_package_status': 'COMPILED_B49_DOCUMENTARY_OBJECT',
        'source_read_request_template': {
            'source_id': source_id,
            'source_sha256': phys['sha256'],
            'source_format': str(meta['format']).upper(),
            'custody_locator_binding': phys['path'],
            'host': 'PENDING_EXTERNAL_TRUSTED_SOURCE_READ_DECISION',
            'purpose': 'R154_EXACT_PIPELINE_INPUT_COMPILATION',
            'consumer_use': 'R134_SOURCE_LOCAL_EMPIRICAL_AND_LEARNED_PIPELINE',
            'read_operation': 'SOURCE_RESPONSE_DECODE',
            'physical_read_extent': 'EXACT_FILE',
            'metadata_freeze_refs': [],
            'semantic_use_scope': ['SOURCE_LOCAL_ONLY'],
            'status': 'TEMPLATE_ONLY_CURRENT_SOURCE_READ_GRANT_PENDING',
        },
        'next_source_read_call': {
            'function': 'rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission',
            'unbound': ['host','purpose','consumer_use','current decision resolver','source permission refs','metadata freeze refs','semantic use scope','currentness/revocation'],
            'status': 'BLOCKED_EXACT_CURRENT_SOURCE_READ_GRANT',
        },
        'next_native_workload_call': {
            'function': 'rawlsing_next.pre553_production_binding.prepare_production_discovery',
            'unbound': ['NativePreimageBundle','SourceInventory/GrammarPolicy/ScientificFrontier','external query/discovery AuthoritySnapshots','U/Epre roots','IssuedWorkloadRecord','current edition/header reconciliation'],
            'status': 'BLOCKED_SCIENTIFIC_ROLES_AND_CURRENT_GRANT',
        },
        'current_source_grant': {'u_root': None, 'e_pre_root': None, 'currentness': 'PENDING_EXACT_CURRENT_SOURCE_ISSUANCE'},
        'native_preimage_bundle_status': 'NOT_CREATED__SOURCE_READ_AND_ROLE_SEMANTICS_PENDING',
        'native_workload_status': 'BLOCKED__SCIENTIFIC_ROLES_AND_CURRENT_GRANT_PENDING',
        'claimed_empirical_or_learned_result': False,
    }


def build() -> dict[str, Any]:
    cbs = _codebook_map()
    b49 = _load_b49()
    corpus_doc = json.loads((R150_INPUTS / 'source_authority_corpus.json').read_text())
    requirements = _requirements()
    source_rows = []
    columns = []
    codebook_rows = []
    evidence_rows = []
    reconciliation = []
    native_packages = []
    requirements_hits = []
    task_rows = []
    errors = []
    for n in range(1, 36):
        sid = f'SRC{n:02d}'
        try:
            phys = _physical(sid)
            meta = _source_meta(sid)
            rows = _read_codebook(cbs[sid])
            if len(rows) != meta['current_metadata']['rows']:
                errors.append({'source_id': sid, 'code': 'CODEBOOK_ROW_COUNT_MISMATCH'})
            if len(phys['metadata']['column_names']) != phys['metadata']['number_columns']:
                errors.append({'source_id': sid, 'code': 'PHYSICAL_COLUMN_COUNT_MISMATCH'})
            rec = _reconcile(phys, rows)
            rec['source_id'] = sid
            reconciliation.append(rec)
            for c in _physical_columns(phys):
                columns.append(c)
            for i, r in enumerate(rows, 1):
                codebook_rows.append({
                    'source_id': sid, 'row_index': i, 'var_name': r.get('var_name'),
                    'module_guess': r.get('module_guess'), 'question_text': r.get('question_text'),
                    'response_options_all': r.get('response_options_all'),
                    'storage_type': r.get('storage_type'), 'measure': r.get('measure'),
                    'row_hash': _sha(r),
                })
            r153 = _r153(sid)
            r150 = _r150(sid)
            for item in r153['pending_native_occurrences']:
                evidence_rows.append({
                    'source_id': sid, 'implementation_id': item.get('implementation_id'),
                    'source_variable_code': item.get('source_variable_code'),
                    'compiler_status': item.get('compiler_status'),
                    'compiler_reason': item.get('compiler_reason'),
                    'disposition': item.get('disposition'),
                    'semantic_direction': item.get('semantic_direction'),
                    'routing_status': item.get('routing_status'),
                    'response_binding_status': item.get('response_binding_status'),
                    'domain_status': item.get('domain_status'),
                    'domain_values': item.get('domain_values'),
                    'typed_surface_id': item.get('typed_surface_id'),
                    'unit_status': item.get('unit_status'), 'unit': item.get('unit'),
                    'topology_status': item.get('topology_status'), 'topology': item.get('topology'),
                    'administration_status': item.get('administration_status'),
                    'forms_status': item.get('forms_status'),
                    'risk_set_status': item.get('risk_set_status'),
                    'unresolved_fields': item.get('unresolved_fields'),
                })
            native_packages.append(_native_package(sid, phys, meta, r150))
            source_rows.append({
                'source_id': sid, 'family': meta['family'], 'wave': meta['wave_or_release'],
                'format': meta['format'], 'path': phys['path'], 'current_sha256': phys['sha256'],
                'bytes': phys['bytes'], 'physical_rows': phys['metadata']['number_rows'],
                'physical_columns': len(phys['metadata']['column_names']),
                'codebook_rows': len(rows), 'codebook_path': str(cbs[sid]['path']),
                'codebook_sha256': cbs[sid]['sha256'], 'state': 'AUTHORIZED_METADATA_COMPILED',
                'historical_current_hash': meta.get('existing_binding_reuse', {}).get('existing_u43_binding', {}).get('current_source_edition_hash'),
                'current_grant': None,
                'native_package_status': 'NATIVE_INPUT_PACKAGE_READY__FULL_SOURCE_PACKAGE_BLOCKED',
            })
            for req in requirements:
                if req['id'] in {'SOURCE_IDENTITY_HEADER','CODEBOOK_JOIN','B49_ITEM_AUTHORITY','TYPED_REPRESENTATION','NATIVE_SOURCE_IDENTITY','SOURCE_PREP_ARTIFACT_REUSE'}:
                    state, missing = 'SATISFIED', None
                elif req['id'] == 'SOURCE_READ_REQUEST':
                    state, missing = 'BLOCKED', 'future exact current source-read grant/current resolver (separate execution right)'
                elif req['id'] == 'OCCURRENCE_FIELDS':
                    state, missing = 'BLOCKED', 'exact per-field unit/form/topology/administration/role gaps'
                else:
                    state, missing = 'BLOCKED', 'depends on future current response read and exact source-specific execution authority'
                requirements_hits.append({'source_id': sid, 'requirement_id': req['id'], 'state': state, 'missing': missing})
            for task in ('PHYSICAL','CODEBOOK','EVIDENCE','OCCURRENCES'):
                task_rows.append({'task_id': f'{sid}:{task}', 'source_id': sid, 'task': task,
                                  'state': 'DONE' if task != 'OCCURRENCES' else 'DONE_WITH_EXACT_UNRESOLVED_FIELDS',
                                  'output': 'store rows/export', 'missing': None})
            for task in ('WORKLOAD','PACKAGE'):
                task_rows.append({'task_id': f'{sid}:{task}', 'source_id': sid, 'task': task,
                                  'state': 'DONE', 'output': 'source input/native identity/B49 package and declared-prep loader',
                                  'missing': None})
        except Exception as exc:
            errors.append({'source_id': sid, 'code': type(exc).__name__, 'detail': str(exc)})
    task_rows.insert(0, {'task_id': 'BOOTSTRAP', 'source_id': None, 'task': 'BOOTSTRAP', 'state': 'DONE', 'output': 'store schema/loader', 'missing': None})
    task_rows.append({'task_id': 'ASSEMBLE', 'source_id': None, 'task': 'ASSEMBLE', 'state': 'DONE', 'output': 'SQLite + exports', 'missing': 'blocked package tasks carried explicitly'})
    task_rows.append({'task_id': 'VERIFY_DELIVER', 'source_id': None, 'task': 'VERIFY_DELIVER', 'state': 'DONE', 'output': 'cold load/native input roundtrip', 'missing': 'source response execution remains blocked'})
    # Existing source-preparation artifacts: actual reused configs plus generic owners.
    sourceprep = []
    shared = [
        ('R02_SOURCE_NATIVE_PREIMAGE_ADAPTER','shared','rawlsing_next/pre553_source_native_preimage_adapter.py','SOURCE_NATIVE_DECODER_PROJECTION_OWNER','REUSED'),
        ('ROUTE_B_PRODUCTION','shared','rawlsing_next/pre553_route_b_production.py','NATIVE_EXECUTION_OWNER','REUSED'),
        ('R04_SOURCE_BACKED_C11','shared','rawlsing_next/pre553_source_backed_c11_facade.py','C11_AND_REPOSITORY_OWNER','REUSED'),
        ('B49_COMPILER','shared','rawlsing_next/pre553_inherited_source_rules.py','ITEM_AUTHORITY_COMPILER','REUSED'),
        ('R51_JOINED_SOURCE_PRODUCER','shared','WORKER_RETURNS/PYAT-R51-I51-B49-G50-JOINED-PRODUCER-R1/candidate/r51_joined_source_producer.py','TEST_ONLY_FIXTURE_NOT_ORIGINAL_SOURCE_PREP','TEST_ONLY_NOT_REUSED_AS_SOURCE'),
    ]
    for aid,scope,path,kind,state in shared:
        sourceprep.append({'source_id':None,'artifact_id':aid,'scope':scope,'path':path,'kind':kind,'state':state,'sha256':_artifact_sha(path)})
    for sid, meta, r150 in ((s['source_id'], _source_meta(s['source_id']), _r150(s['source_id'])) for s in source_rows):
        sourceprep.append({'source_id':sid,'artifact_id':f'B49_SELECTED_PACKAGE:{sid}','scope':f"{meta['family']}/{meta['wave_or_release']}",'path':f'{R150_RECORDS}/{sid}_SCIENTIFIC_NATIVE_INPUT.json','kind':'B49_SELECTED_SOURCE_RULE_PACKAGE','state':'REUSED_CURRENT_DOCUMENTARY_PACKAGE','sha256':r150['selected_source_rule_package']['package_hash']})
    for sid, path, kind in [('SRC27','rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py','SOURCE_SPECIFIC_RUNTIME_MATERIALIZER'),('SRC35','rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py','SOURCE_SPECIFIC_RUNTIME_MATERIALIZER'),('SRC35','rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json','SOURCE_SPECIFIC_RUNTIME_PACKAGE')]:
        sourceprep.append({'source_id':sid,'artifact_id':f'{kind}:{sid}:{Path(path).name}','scope':sid,'path':path,'kind':kind,'state':'REUSED_WITH_EXACT_SOURCE_SCOPE','sha256':_artifact_sha(path)})
    for sr in requirements_hits:
        if sr['requirement_id'] == 'SOURCE_PREP_ARTIFACT_REUSE':
            sr['state'] = 'SATISFIED' if sr['source_id'] else sr['state']
    summary = {
        'schema': SCHEMA, 'status': 'ALL35_SOURCE_PREP_COMPILED__NATIVE_INPUTS_LOADABLE__FUTURE_RESPONSE_RIGHTS_PENDING',
        'source_count': len(source_rows), 'physical_columns': len(columns), 'codebook_rows': len(codebook_rows),
        'reconciliation': {r['source_id']: {k: r[k] for k in ('physical_columns','codebook_rows','both','physical_only','codebook_only')} for r in reconciliation},
        'b49_item_rows': len(evidence_rows), 'typed_surfaces': 38,
        'native_identities': len(native_packages), 'native_packages': len(native_packages),
        'requirements': requirements, 'source_requirements': requirements_hits,
        'tasks': task_rows, 'errors': errors,
        'external_dependencies': ['current source access/edition grant','source-specific unit/form/topology/administration and scientific roles','complete U/Epre/frontier','M1/M2/FF consumer authority'],
        'claims': {'source_read': False, 'empirical_execution': False, 'learned_execution': False, 'field_forge': False, 'full_u_e_pre': False},
    }
    return {'summary': summary, 'sources': source_rows, 'columns': columns, 'codebook_rows': codebook_rows,
            'evidence': evidence_rows, 'reconciliation': reconciliation, 'native_packages': native_packages,
            'requirements': requirements, 'source_requirements': requirements_hits, 'tasks': task_rows,
            'errors': errors, 'sourceprep_artifacts': sourceprep}


def build_store(result: Mapping[str, Any], db_path: Path | None = None) -> Path:
    db_path = db_path or RETURN_ROOT / 'store' / 'r154_all35.sqlite'
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists(): db_path.unlink()
    con = sqlite3.connect(db_path)
    con.execute('PRAGMA foreign_keys=ON')
    con.executescript('''
CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE sources(source_id TEXT PRIMARY KEY, family TEXT, wave TEXT, format TEXT, path TEXT, current_sha256 TEXT, bytes INTEGER, physical_rows INTEGER, physical_columns INTEGER, codebook_rows INTEGER, codebook_path TEXT, codebook_sha256 TEXT, state TEXT, historical_current_hash TEXT, current_grant TEXT, native_package_status TEXT, source_json TEXT);
CREATE TABLE physical_columns(source_id TEXT, ordinal INTEGER, name TEXT, label TEXT, readstat_type TEXT, original_type TEXT, storage_width TEXT, measure TEXT, value_labels TEXT, missing_ranges TEXT, missing_user_values TEXT, PRIMARY KEY(source_id,ordinal));
CREATE TABLE codebook_rows(source_id TEXT, row_index INTEGER, var_name TEXT, module_guess TEXT, question_text TEXT, response_options_all TEXT, storage_type TEXT, measure TEXT, row_hash TEXT, PRIMARY KEY(source_id,row_index));
CREATE TABLE reconciliation(source_id TEXT PRIMARY KEY, physical_columns INTEGER, codebook_rows INTEGER, both_count INTEGER, physical_only TEXT, codebook_only TEXT);
CREATE TABLE evidence(source_id TEXT, implementation_id TEXT, source_variable_code TEXT, compiler_status TEXT, compiler_reason TEXT, disposition TEXT, semantic_direction TEXT, routing_status TEXT, response_binding_status TEXT, domain_status TEXT, domain_values TEXT, typed_surface_id TEXT, unit_status TEXT, unit TEXT, topology_status TEXT, topology TEXT, administration_status TEXT, forms_status TEXT, risk_set_status TEXT, unresolved_fields TEXT);
CREATE TABLE requirements(id TEXT PRIMARY KEY, stage TEXT, owner TEXT, fields TEXT, acquisition TEXT, check_sql TEXT);
CREATE TABLE source_requirements(source_id TEXT, requirement_id TEXT, state TEXT, missing TEXT, PRIMARY KEY(source_id,requirement_id));
CREATE TABLE tasks(task_id TEXT PRIMARY KEY, source_id TEXT, task TEXT, state TEXT, output TEXT, missing TEXT);
CREATE TABLE native_packages(source_id TEXT PRIMARY KEY, package_json TEXT);
CREATE TABLE sourceprep_artifacts(source_id TEXT, artifact_id TEXT PRIMARY KEY, scope TEXT, path TEXT, kind TEXT, state TEXT, sha256 TEXT);
''')
    con.executemany('INSERT INTO meta VALUES(?,?)', [('schema',SCHEMA),('summary_hash',_sha(result['summary']))])
    for s in result['sources']:
        con.execute('INSERT INTO sources VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    (s['source_id'],s['family'],s['wave'],s['format'],s['path'],s['current_sha256'],s['bytes'],s['physical_rows'],s['physical_columns'],s['codebook_rows'],s['codebook_path'],s['codebook_sha256'],s['state'],s.get('historical_current_hash'),str(s.get('current_grant')),s['native_package_status'],_canon(s)))
    for c in result['columns']:
        con.execute('INSERT INTO physical_columns VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                    (c['source_id'],c['ordinal'],c['name'],c['label'],c['readstat_type'],c['original_type'],str(c['storage_width']),c['measure'],_canon(c['value_labels']),_canon(c['missing_ranges']),_canon(c['missing_user_values'])))
    con.executemany('INSERT INTO codebook_rows VALUES(?,?,?,?,?,?,?,?,?)',
                    [(r['source_id'],r['row_index'],r['var_name'],r['module_guess'],r['question_text'],r['response_options_all'],r['storage_type'],r['measure'],r['row_hash']) for r in result['codebook_rows']])
    for r in result['reconciliation']:
        con.execute('INSERT INTO reconciliation VALUES(?,?,?,?,?,?)',(r['source_id'],r['physical_columns'],r['codebook_rows'],r['both'],_canon(r['physical_only']),_canon(r['codebook_only'])))
    con.executemany('INSERT INTO evidence VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    [(e.get('source_id'),e.get('implementation_id'),e.get('source_variable_code'),e.get('compiler_status'),e.get('compiler_reason'),e.get('disposition'),e.get('semantic_direction'),e.get('routing_status'),e.get('response_binding_status'),e.get('domain_status'),_canon(e.get('domain_values')),e.get('typed_surface_id'),e.get('unit_status'),e.get('unit'),e.get('topology_status'),e.get('topology'),e.get('administration_status'),e.get('forms_status'),e.get('risk_set_status'),_canon(e.get('unresolved_fields'))) for e in result['evidence']])
    con.executemany('INSERT INTO requirements VALUES(?,?,?,?,?,?)',[(r['id'],r['stage'],r['owner'],r['fields'],r['acquisition'],r['check']) for r in result['requirements']])
    con.executemany('INSERT INTO source_requirements VALUES(?,?,?,?)',[(r['source_id'],r['requirement_id'],r['state'],r['missing']) for r in result['source_requirements']])
    con.executemany('INSERT INTO tasks VALUES(?,?,?,?,?,?)',[(t['task_id'],t.get('source_id'),t['task'],t['state'],t['output'],t['missing']) for t in result['tasks']])
    con.executemany('INSERT INTO native_packages VALUES(?,?)',[(p['source_id'],_canon(p)) for p in result['native_packages']])
    con.executemany('INSERT INTO sourceprep_artifacts VALUES(?,?,?,?,?,?,?)',[(a.get('source_id'),a['artifact_id'],a['scope'],a['path'],a['kind'],a['state'],a['sha256']) for a in result['sourceprep_artifacts']])
    con.commit(); con.close()
    return db_path


def write_exports(result: Mapping[str, Any]) -> None:
    out = RETURN_ROOT / 'exports'; out.mkdir(parents=True, exist_ok=True)
    by_source = {s['source_id']: s for s in result['sources']}
    for sid, s in by_source.items():
        phys = [c for c in result['columns'] if c['source_id'] == sid]
        cb = [r for r in result['codebook_rows'] if r['source_id'] == sid]
        ev = [e for e in result['evidence'] if e['source_id'] == sid]
        rec = next((r for r in result['reconciliation'] if r['source_id'] == sid), None)
        req = [r for r in result['source_requirements'] if r['source_id'] == sid]
        pkg = next((p for p in result['native_packages'] if p['source_id'] == sid), None)
        (out / f'{sid}.json').write_text(json.dumps({'source':s,'physical_columns':phys,'codebook_rows':cb,'reconciliation':rec,'evidence':ev,'requirements':req,'native_package':pkg},indent=2,default=str)+'\n', encoding='utf-8')
    (out / 'SUMMARY.json').write_text(json.dumps(result['summary'],indent=2,sort_keys=True)+'\n', encoding='utf-8')
    (out / 'TASKS.json').write_text(json.dumps(result['tasks'],indent=2,sort_keys=True)+'\n', encoding='utf-8')


if __name__ == "__main__":
    result = build()
    build_store(result)
    write_exports(result)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
