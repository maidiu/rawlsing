"""Physical import closure probe, never invokes temporal compilation/source readers."""
from pathlib import Path
import sys,importlib,json,hashlib,traceback
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'native'),str(R/'temporal/closure')]
results=[]
for name in ['rawlsing_next.pre553_route_b_production','rawlsing_next.pre553_learned_world_composition','rawlsing_next.field_forge_conditional_support','rawlsing_next.m1_admitted_field_forge_relation_v554_ingress','rawlsing_next.prev3_objective_position_materializer','rawlsing_next.prev3_objective_position_v557_v558_publication','data.ddm_build_copy.ddm_v553_temporal_pressure']:
 try:
  m=importlib.import_module(name);p=Path(m.__file__).resolve();b=p.read_bytes();row=dict(module=name,status='IMPORTED_NATIVE',file=str(p),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha256=hashlib.sha256(b).hexdigest())
  if name.endswith('ddm_v553_temporal_pressure'):row['empty_readiness_typed_errors']=m.validate_v553_temporal_pressure_readiness({});row['compiler_executed']=False
 except Exception as exc:row=dict(module=name,status='IMPORT_HOLD',error_type=type(exc).__name__,detail=str(exc),traceback=traceback.format_exc())
 results.append(row)
(R/'05_REAL_PYTEST_COLD_JUNIT/owner_import_probe.json').write_text(json.dumps(dict(results=results,original_sources_read=False,temporal_compilation=False,J04_item_materialization=False),indent=2)+'\n');print([(r['module'],r['status']) for r in results])
