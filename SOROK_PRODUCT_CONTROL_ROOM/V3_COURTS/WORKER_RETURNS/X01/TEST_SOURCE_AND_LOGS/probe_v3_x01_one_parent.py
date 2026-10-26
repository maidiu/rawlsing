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
from v3.io.parent_baseline_from_behavior import infer_parent_baseline_and_regime
from v3.engine.expectation_baseline import derive_child_expectation_baseline, load_need_axis_rules
from v3.io.identity_to_backbone import child_model_from_parent_baseline_and_regime
cases={
 'one_present_loving_low_material': {'parent_behavior': {'father': {'parental_warmth':85,'parental_authority':45,'parental_material_support':20}}},
 'one_present_cold_high_material': {'parent_behavior': {'father': {'parental_warmth':30,'parental_authority':80,'parental_material_support':80}}},
 'both_present_loving_low_material': {'parent_behavior': {'father': {'parental_warmth':85,'parental_authority':45,'parental_material_support':20}, 'mother': {'parental_warmth':85,'parental_authority':45,'parental_material_support':20}}},
}
out={}
for name,ident in cases.items():
 b,r=infer_parent_baseline_and_regime(ident)
 d=derive_child_expectation_baseline(parent_baseline=b,transmission_regime=r,rules=load_need_axis_rules())
 out[name]={'inferred':b,'regime':r,'derived':d,'child_model':child_model_from_parent_baseline_and_regime(b,r,age=0)}
print(json.dumps(out,indent=2,sort_keys=True))
