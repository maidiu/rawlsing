import sys, types, json, subprocess
from pathlib import Path
source=Path(__import__('os').environ['RAWLSING_STAGING_ROOT'])
if str(source) not in sys.path: sys.path.insert(0,str(source))
_RUBY="require 'yaml'; require 'json'; print JSON.generate(YAML.safe_load(STDIN.read, [], [], true))"
def safe_load(value):
    if hasattr(value,'read'): value=value.read()
    p=subprocess.run(['ruby','-e',_RUBY],input=value,capture_output=True,text=True)
    if p.returncode!=0: raise ValueError(p.stderr)
    return json.loads(p.stdout)
m=sys.modules.get('yaml') or types.ModuleType('yaml'); m.safe_load=safe_load; sys.modules['yaml']=m
from v3.io.identity_to_backbone import backbone_state_from_identity
from v3.io.parent_baseline_from_behavior import infer_parent_baseline_and_regime
def snap(state):
    return {
      'expectation_baseline': dict(state.expectation_baseline),
      'child_model': dict(state.child_model),
      'capacity': {k:getattr(state.capacity,k) for k in ('time','money','health','social_support','skill','mobility','risk_tolerance','legitimacy')},
      'autonomy_drive': state.autonomy_drive, 'safety_drive': state.safety_drive,
      'autonomy_condition': state.autonomy_condition, 'safety_condition': state.safety_condition,
      'initial_state_provenance_keys': sorted((state.initial_state_provenance or {}).keys()),
      'initial_state_expectation_provenance': (state.initial_state_provenance or {}).get('fields',{}).get('expectation_baseline'),
      'initial_state_child_model_provenance': (state.initial_state_provenance or {}).get('fields',{}).get('child_model'),
      'magnets': [(m.label,m.magnet_type,m.intensity) for m in state.active_magnets],
      'generation_diagnostics': state.generation_diagnostics,
    }
out={}
s=backbone_state_from_identity({}, year=1990, age=0)
out['missing_parent']=snap(s)
pid={'parent_behavior': {'father': {'parental_warmth':85,'parental_authority':45,'parental_material_support':20},
                       'mother': {'parental_warmth':85,'parental_authority':45,'parental_material_support':20}}}
b,r=infer_parent_baseline_and_regime(pid)
ident={'parent_expectation_baseline': b, 'transmission_regime': r}
s2=backbone_state_from_identity(ident, year=1990, age=0)
out['loving_low_material']=snap(s2)
out['inputs']={'parent_identity':pid,'inferred_parent_baseline':b,'transmission_regime':r}
print(json.dumps(out,indent=2,sort_keys=True,default=str))
