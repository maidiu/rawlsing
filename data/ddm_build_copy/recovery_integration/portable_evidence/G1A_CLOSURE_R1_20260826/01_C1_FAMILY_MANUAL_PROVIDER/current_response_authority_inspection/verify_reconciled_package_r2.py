#!/usr/bin/env python3
import csv, hashlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(10_000_000)
ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / 'MANIFEST.json'
MAP = ROOT / 'V550_response_option_map_reconciled_sav_derived_r2.csv'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def truth(v: str) -> bool:
    return str(v or '').strip().lower() in {'1','true','yes'}

m = json.loads(MANIFEST.read_text(encoding='utf-8'))
fail = []

# Hash + byte verification for every packaged file tracked by manifest.
for name, meta in m['files'].items():
    p = ROOT / name
    if not p.exists():
        fail.append(f'missing:{name}')
        continue
    got = sha256(p)
    if got != meta['sha256']:
        fail.append(f'hash:{name}:{got}!={meta["sha256"]}')
    if p.stat().st_size != meta['bytes']:
        fail.append(f'bytes:{name}:{p.stat().st_size}!={meta["bytes"]}')

# Binding registry / raw dictionary integrity.
with (ROOT/'latinobarometro_sav_to_authority_binding_registry.csv').open(encoding='utf-8', newline='') as f:
    bindings = list(csv.DictReader(f))
if len(bindings) != 872:
    fail.append(f'binding_registry_row_count:{len(bindings)}!=872')
raw_to_auth = defaultdict(set)
for r in bindings:
    raw_to_auth[(r['wave'], r['raw_var_code'])].add(r['authority_var_code'])
if any(len(v) > 1 for v in raw_to_auth.values()):
    fail.append('raw_to_multiple_authority_collision')

with (ROOT/'latinobarometro_sav_direct_identifier_alias_authority.csv').open(encoding='utf-8', newline='') as f:
    aliases = list(csv.DictReader(f))
if len(aliases) != 359:
    fail.append(f'direct_alias_count:{len(aliases)}!=359')
if any(r['binding_cardinality'] != 'ONE_TO_ONE' or not truth(r['runtime_alias_eligible']) or not truth(r['requires_identifier_resolution']) for r in aliases):
    fail.append('direct_alias_contract_violation')

with (ROOT/'latinobarometro_sav_family_binding_authority.csv').open(encoding='utf-8', newline='') as f:
    family = list(csv.DictReader(f))
if len(family) != 110:
    fail.append(f'family_binding_count:{len(family)}!=110')
if any(r['binding_cardinality'] != 'ONE_TO_MANY_FAMILY' or truth(r['runtime_alias_eligible']) for r in family):
    fail.append('family_binding_contract_violation')

# Raw names must exist in the shipped SAV dictionaries.
dicts = {}
for wave in ('1995','2011','2024'):
    with (ROOT/f'latinobarometro_{wave}_sav_dictionary.csv').open(encoding='utf-8', newline='') as f:
        dicts[wave] = {r['raw_var_code'] for r in csv.DictReader(f)}
for r in aliases + family:
    if r['raw_var_code'] not in dicts[r['wave']]:
        fail.append(f'raw_not_in_sav_dictionary:{r["wave"]}:{r["raw_var_code"]}')

# Direct alias resolution audit must independently pass all 359 rows.
with (ROOT/'latinobarometro_sav_direct_alias_resolution_audit.csv').open(encoding='utf-8', newline='') as f:
    aa = list(csv.DictReader(f))
if len(aa) != 359 or any(r.get('status') != 'PASS' for r in aa):
    fail.append('direct_alias_resolution_audit_not_359_PASS')

# Runtime-map integrity and composition.
rows = signed = intensity = quarantine = q_signed = q_intensity = q_polarity = alias_replica = 0
serialized_hashes = set()
with MAP.open('rb') as fb:
    fb.readline()
    for line in fb:
        h = hashlib.blake2b(line, digest_size=16).digest()
        if h in serialized_hashes:
            fail.append('runtime_exact_duplicate_serialized_row')
            break
        serialized_hashes.add(h)

with MAP.open(encoding='utf-8', newline='') as f:
    rdr = csv.DictReader(f)
    if len(rdr.fieldnames or []) != 71:
        fail.append(f'runtime_column_count:{len(rdr.fieldnames or [])}!=71')
    for r in rdr:
        rows += 1
        rd = bool(r.get('response_direction','').strip())
        ri = bool(r.get('response_intensity','').strip())
        pol = bool(r.get('polarity','').strip())
        if rd: signed += 1
        if ri: intensity += 1
        q = r.get('directionality_status') == 'quarantined_legacy_unreconciled'
        if q:
            quarantine += 1
            q_signed += int(rd); q_intensity += int(ri); q_polarity += int(pol)
        if 'SAV_RAW_IDENTIFIER_ALIAS:' in r.get('notes',''):
            alias_replica += 1
if rows != 392572: fail.append(f'runtime_rows:{rows}!=392572')
if signed != 28239 or intensity != 28239: fail.append(f'runtime_signed_intensity:{signed}/{intensity}!=28239/28239')
if quarantine != 42506: fail.append(f'quarantine_rows:{quarantine}!=42506')
if q_signed or q_intensity or q_polarity: fail.append(f'quarantine_has_directional_authority:{q_signed}/{q_intensity}/{q_polarity}')
if alias_replica: fail.append(f'raw_alias_replicas_present:{alias_replica}')

# Canonical runtime rows must equal the nine current packets projected to the 71 runtime fields.
with MAP.open(encoding='utf-8', newline='') as f:
    rdr = csv.DictReader(f); fields = rdr.fieldnames or []
    runtime_canon = Counter()
    for r in rdr:
        if r.get('directionality_status') == 'quarantined_legacy_unreconciled':
            continue
        s = '\x1f'.join(r.get(k,'') for k in fields)
        runtime_canon[hashlib.blake2b(s.encode(), digest_size=16).digest()] += 1
packets = [
    'afrobarometer_response_option_authority.csv','arab_barometer_response_option_authority.csv',
    'asian_barometer_response_option_authority.csv','evs_response_option_authority.csv',
    'gss_response_option_authority.csv','latinobarometro_response_option_authority.csv',
    'lits_response_option_authority.csv','south_asia_response_option_authority.csv',
    'wvs_response_option_authority.csv'
]
packet_rows = Counter(); packet_total = 0
for name in packets:
    p = ROOT/'authority_inputs'/name
    with p.open(encoding='utf-8-sig', newline='') as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            s = '\x1f'.join((r.get(k,'') or '') for k in fields)
            packet_rows[hashlib.blake2b(s.encode(), digest_size=16).digest()] += 1
            packet_total += 1
if packet_total != 350066: fail.append(f'packet_total:{packet_total}!=350066')
if runtime_canon != packet_rows: fail.append('runtime_canonical_rows_not_equal_current_packet_union')

# Historical 700 court: shipped table must be 700 PASS and truthful about actual runtime row/sign counts.
with (ROOT/'35wave_response_semantics_runtime_court_validation_r2.csv').open(encoding='utf-8', newline='') as f:
    court = list(csv.DictReader(f))
if len(court) != 700 or any(not r.get('court_status','').startswith('PASS') or r.get('validation_status') != 'PASS' for r in court):
    fail.append('historical_700_runtime_court_not_700_PASS')

# Recompute exact runtime rows/signs for all court keys.
cert_keys = {(r['source_family'],r['canonical_wave'],r['var_code'],r['response_semantics_contract_hash']) for r in court if r['contract_coverage_status']=='CERTIFIED_ACTIVE_RESPONSE_SCALE'}
no_keys = {(r['source_family'],r['canonical_wave'],r['var_code']) for r in court if r['contract_coverage_status']!='CERTIFIED_ACTIVE_RESPONSE_SCALE'}
cert_acc = defaultdict(lambda:[0,0,0,set(),0,0]) # rows,signed,intensity,subcodes,subsigned,subintensity
no_acc = defaultdict(lambda:[0,0,0])
with MAP.open(encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        k4=(r['source_family'],r['canonical_wave'],r['var_code'],r['response_semantics_contract_hash'])
        sub=truth(r.get('is_substantive'))
        if k4 in cert_keys:
            x=cert_acc[k4]; x[0]+=1; x[1]+=int(bool(r['response_direction'].strip())); x[2]+=int(bool(r['response_intensity'].strip()))
            if sub:
                x[3].add(r['value_code_normalized']); x[4]+=int(bool(r['response_direction'].strip())); x[5]+=int(bool(r['response_intensity'].strip()))
        k3=(r['source_family'],r['canonical_wave'],r['var_code'])
        if k3 in no_keys:
            x=no_acc[k3]; x[0]+=1; x[1]+=int(bool(r['response_direction'].strip())); x[2]+=int(bool(r['response_intensity'].strip()))
for r in court:
    if r['contract_coverage_status']=='CERTIFIED_ACTIVE_RESPONSE_SCALE':
        k=(r['source_family'],r['canonical_wave'],r['var_code'],r['response_semantics_contract_hash']); x=cert_acc[k]
        exp=int(r['substantive_category_count'] or 0)
        if x[0]!=int(r['runtime_rows']) or x[1]!=int(r['runtime_signed_rows']) or x[2]!=int(r['runtime_intensity_rows']) or len(x[3])!=exp or x[4]!=exp or x[5]!=exp:
            fail.append(f'certified_court_metric_mismatch:{k}')
            break
    else:
        k=(r['source_family'],r['canonical_wave'],r['var_code']); x=no_acc[k]
        if x[0]!=int(r['runtime_rows']) or x[1]!=0 or x[2]!=0 or int(r['runtime_signed_rows'])!=0 or int(r['runtime_intensity_rows'])!=0:
            fail.append(f'no_scale_court_metric_mismatch:{k}')
            break

if fail:
    print('FAIL_RECONCILED_SAV_DERIVED_R2')
    for x in fail: print(x)
    sys.exit(2)
print('PASS_RECONCILED_SAV_DERIVED_R2')
