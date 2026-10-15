"""Frozen sourcefree inputs, equal-information packets and exact pairing checks."""
import copy,gzip,hashlib,itertools,json,pathlib,re
from collections import Counter,defaultdict
from assay.architecture import build_packet,DerivedCache,canonical
from assay.corpus import MENUS
ROOT=pathlib.Path(__file__).resolve().parents[1];R2=ROOT/'runtime_root/rba/exec/r2'
class IntegrityError(ValueError):pass
def load_cases():return json.loads((R2/'data/corpus.json').read_text())+json.loads((ROOT/'fixtures/heldout_cases.json').read_text())
def load_key():return json.loads((R2/'data/oracle.json').read_text())|json.loads((ROOT/'fixtures/heldout_key.json').read_text())
def load_schedule():return json.loads(gzip.decompress((ROOT/'fixtures/schedule.json.gz').read_bytes()))
def verify_freeze():
 path=ROOT/(ROOT/'CURRENT_FREEZE').read_text().strip();raw=path.read_bytes();f=json.loads(raw)
 for p,h in f['files'].items():
  if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h:raise IntegrityError('R3_FROZEN_SOURCE_CHANGED:'+p)
 for p,h in f['original_frozen_files'].items():
  if hashlib.sha256((R2/p).read_bytes()).hexdigest()!=h:raise IntegrityError('ORIGINAL_R2_CHANGED:'+p)
 return hashlib.sha256(raw).hexdigest()
def packet(case,row,cache=None):
 # Evaluator trial ID stays local. Shared opaque public ID cannot encode arm.
 safe_row=dict(row,id=row['public_response_id'])
 p,receipt=build_packet(case,safe_row,cache)
 if set(p)!={'response_id','instruction','facts','representation','menu','output_schema'}:raise IntegrityError('PAYLOAD_KEYS')
 return p,receipt
def validate_schedule(rows,cases):
 by_case={c['id']:c for c in cases};ids=[r['id'] for r in rows]
 if len(ids)!=len(set(ids)):raise IntegrityError('DUPLICATE_TRIAL')
 if {r['case'] for r in rows}!=set(by_case):raise IntegrityError('CASE_COMPLETENESS')
 blocks=defaultdict(list)
 for r in rows:
  if any(not re.fullmatch('[0-9a-f]{32}',r[k]) for k in ['id','block','public_response_id']):raise IntegrityError('OPAQUE_ID')
  c=by_case[r['case']]
  if (r['family'],r['k'])!=(c['family'],c['k']):raise IntegrityError('CONTEXT_BINDING')
  blocks[r['block']].append(r)
 orders=defaultdict(Counter);rotations=defaultdict(Counter);publics=[]
 for block,g in blocks.items():
  if len(g)!=3 or {r['arm'] for r in g}!=set('ABC'):raise IntegrityError('PAIR_COMPLETENESS')
  if len({r['case'] for r in g})!=1 or len({tuple(r['menu']) for r in g})!=1 or len({r['public_response_id'] for r in g})!=1:raise IntegrityError('PAIR_CONTEXT')
  g=sorted(g,key=lambda r:r['execution_index'])
  if [r['execution_index'] for r in g]!=[0,1,2]:raise IntegrityError('EXECUTION_INDEX')
  c=g[0]['case'];menu=MENUS[by_case[c]['k']]
  if set(g[0]['menu'])!=set(menu) or len(g[0]['menu'])!=len(menu):raise IntegrityError('MENU_CONSERVATION')
  orders[c][''.join(r['arm'] for r in g)]+=1;rotations[c][tuple(g[0]['menu'])]+=1;publics.append(g[0]['public_response_id'])
 if len(publics)!=len(set(publics)):raise IntegrityError('PUBLIC_ID_REUSE_ACROSS_BLOCKS')
 for c in by_case:
  menu=MENUS[by_case[c]['k']];expected={''.join(x):len(menu) for x in itertools.permutations('ABC')}
  if dict(orders[c])!=expected:raise IntegrityError('ARM_ORDER_IMBALANCE')
  want={tuple(menu[i:]+menu[:i]):6 for i in range(len(menu))}
  if dict(rotations[c])!=want:raise IntegrityError('MENU_ROTATION_IMBALANCE')
 return dict(cases=len(cases),blocks=len(blocks),trials=len(rows),orders=dict(sum(orders.values(),Counter())))
