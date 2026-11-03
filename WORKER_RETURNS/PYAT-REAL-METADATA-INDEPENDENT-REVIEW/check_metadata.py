"""Independent checks for SRC04 real metadata projection/crosswalk and form/route scope."""
from __future__ import annotations
import csv, hashlib, json, subprocess
from pathlib import Path

REVIEW = Path(__file__).resolve().parent
SNAP = Path((REVIEW / 'evidence/snapshot.path').read_text().strip())
SIB = Path('/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007')
CONFIG = SNAP / 'rawlsing_next/source_configuration/data/SRC04/source.config.json'
CROSSWALK = SNAP / 'rawlsing_next/source_configuration/data/SRC04/crosswalk.json'
CODEBOOK = Path('/Users/matthewsmith/Desktop/Rawlsing/data/FINAL CODEBOOKS/FINAL FINAL CODEBOOKS/Arab Barometer Wave 1 codebook.csv')
DIRECTION = Path('/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/directionality_authority/arab_barometer_I_directionality_authority.csv')
OPTION = Path('/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/reports/arab_barometer_response_option_authority.csv')

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def csv_rows(p):
 with Path(p).open(newline='', encoding='utf-8', errors='replace') as f:
  r=csv.DictReader(f); return tuple(r)
def git_show(path):
 return subprocess.check_output(['git','-C',str(SIB),'show',f'agent/pyat-campaign-a-src04-original-c11:{path}'], text=True)

cfg=json.loads(CONFIG.read_text()); cw=json.loads(CROSSWALK.read_text())
items=cfg['items']; slots=cfg['physical_slots']; entries=cw['entries']
by_ord={int(x['physical_ordinal']):x for x in entries}
config_names={int(x['ordinal']):x['name'] for x in slots}
entry_names={int(x['physical_ordinal']):x['physical_name'] for x in entries}
config_item_names=[x['source_variable_code'] for x in items]
cross_item_names=[x['physical_name'] for x in entries]
codebook=csv_rows(CODEBOOK); direction=csv_rows(DIRECTION); option=csv_rows(OPTION)
release=json.loads(git_show('campaign_a_src04/evidence/RELEASE_RECEIPT.json'))
selection=json.loads(git_show('campaign_a_src04/evidence/SLICE_SELECTION.json'))
source_config=json.loads(git_show('rawlsing_next/source_configuration/data/SRC04/source.config.json'))
source_scope=source_config['supported_scope']; routing=source_config['routing']
routing_unknown=sum(1 for x in routing if x.get('typed_state') != 'ROUTING_KNOWN')
risk_unresolved=sum(1 for x in routing if str((x.get('risk_set_ref') or {}).get('object_id','')).endswith('unresolved'))
result={
 'schema':'PYAT_REAL_METADATA_INDEPENDENT_CHECKS@1.0.0',
 'candidate_commit':'c8e0215f6f222eb7b09ef0a8d198b23f0780dac2',
 'review_start_head':'3aa57b99a2cbef3ab9f55acc92b73670757a3028',
 'crosswalk':{
   'config_file_sha256':sha(CONFIG),'config_canonical':cfg.get('config_id'),
   'crosswalk_sha256':sha(CROSSWALK),'method':cw.get('method'),
   'entries':len(entries),'config_items':len(items),'config_physical_slots':len(slots),
   'ordinals_exact':set(by_ord)==set(config_names),
   'names_exact':entry_names==config_names,
   'items_exact':set(config_item_names)==set(cross_item_names),
   'items_order_exact':config_item_names==cross_item_names,
   'codebook_names_exact':all(e['physical_name'] in e['codebook_var_names'] for e in entries),
   'unique_physical_names':len(set(entry_names))==len(entry_names),
   'codebook_rows':len(codebook),'directionality_rows':len(direction),
   'directionality_status_counts':{s:sum(1 for r in direction if r.get('directional_certification_status')==s) for s in sorted({r.get('directional_certification_status') for r in direction})},
   'option_rows':len(option),
   'codebook_sha256':sha(CODEBOOK),'directionality_sha256':sha(DIRECTION),'option_sha256':sha(OPTION),
 },
 'prior_accepted_src04':{
   'release_ref':release['release']['release_ref'],
   'source_sha256':release['source_sha256'],
   'source_rows':release['source_rows'],
   'source_columns':release['source_columns'],
   'selected_response_slots':release['selected_response_slots'],
   'selected_coordinate_slots':release['selected_coordinate_slots'],
   'routing_state':release['authority']['routing_state'],
   'supported_unit_slice':source_scope['supported_unit_slice'],
   'supported_form_slice':source_scope['supported_form_slice'],
   'config_routing_entries':len(routing),
   'config_routing_unknown':routing_unknown,
   'config_risk_set_unresolved':risk_unresolved,
   'form_repeat_resolution':'single SAV/source-interview-row; no form or repeat variable; R03 form_id=None, repeat_id=None for the accepted bounded slice',
   'routing_risk_resolution':'not resolved; accepted release keeps ROUTING_UNKNOWN and unresolved risk-set refs',
   'slice_selection_path':'campaign_a_src04/evidence/SLICE_SELECTION.json',
   'slice_selected_response_slots':len(selection.get('selected_response_slots',[])),
 },
 'replayed_receipt':{
   'path':'WORKER_RETURNS/PYAT-REAL-METADATA-INDEPENDENT-REVIEW/evidence/REPLAYED_RECEIPT.json',
   'sha256':sha(REVIEW/'evidence/REPLAYED_RECEIPT.json'),
   'source':json.loads((REVIEW/'evidence/REPLAYED_RECEIPT.json').read_text())['source'],
   'c11':json.loads((REVIEW/'evidence/REPLAYED_RECEIPT.json').read_text())['c11'],
   'r03':json.loads((REVIEW/'evidence/REPLAYED_RECEIPT.json').read_text())['r03'],
 },
 'findings':{
   'real_metadata_projection_distinct_from_fixture_release':True,
   'crosswalk_exact_181':set(by_ord)==set(config_names) and entry_names==config_names and set(config_item_names)==set(cross_item_names) and len(entries)==181,
   'form_repeat_prior_bounded_resolution':'single SAV / no form or repeat variable; form_id=None, repeat_id=None is the exact bounded-slice shape',
   'form_repeat_estate_wide_absence':False,
   'routing_risk_exact':False,
   'first_genuinely_unresolved_input':'exact routing/eligibility and denominator/risk-set handoff for the bounded SRC04 slice (178 routing entries ROUTING_UNKNOWN; 178 unresolved risk-set refs)',
   'downstream_missing_input':'R03 GrammarPolicy/authorized direction grant',
   'metadata_return_first_missing_classification':'REVISE: the return should not call form/repeat the first missing artifact for the prior bounded single-SAV slice; routing/risk-set is the first genuinely unresolved source input.',
 },
 'tests':{
   'replay_receipt_sha256':sha(REVIEW/'evidence/REPLAYED_RECEIPT.json'),
   'candidate_receipt_sha256':sha(SNAP/'WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/01_REDACTED_RECEIPT.json'),
   'receipts_equal':json.loads((REVIEW/'evidence/REPLAYED_RECEIPT.json').read_text())==json.loads((SNAP/'WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/01_REDACTED_RECEIPT.json').read_text()),
 },
 'scope':{'sourcefree':True,'metadata_only':True,'fixture_only':True,'original_data':False,'production_edit':False,'merge':False,'ci':False},
}
out=REVIEW/'evidence/CHECKS.json'; out.write_text(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
print(json.dumps({k:result['findings'][k] for k in result['findings']},indent=2))
print('crosswalk exact',result['findings']['crosswalk_exact_181'],'receipt equal',result['tests']['receipts_equal'])
