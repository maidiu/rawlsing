#!/usr/bin/env python3
"""Optional legacy R5/R6 coverage transfer.  NOT S1 IDENTITY TRUTH.

No K1-K3 recensus, no synthetic invention, no source authentication, no
architecture selection.  An existing R5/R6 SPINE was an expected R5 output, not
a historical accepted input; this transfer therefore cannot satisfy FRAME S1.
Use r7_inventory.py with exact pinned source bytes for the 118 identity inventory.
"""
import argparse,copy,hashlib,json,pathlib,sys
from anvil import REQUIRED
from r7_integrated import check_history

def transfer(source_bytes):
    source=json.loads(source_bytes)
    if source.get('schema') not in ('ANVIL_SPINE_R5','ANVIL_SPINE_R6'):
        raise ValueError('R5/R6 SPINE only')
    obj={'schema':'ANVIL_R7_INHERITED_CONSERVATION',
         'source_authentication':'NOT_AUTHENTICATED_BY_LOCAL_CHECK',
         'source_spine_sha256':hashlib.sha256(source_bytes).hexdigest(),
         'transfer_method':'VERBATIM_R5_R6_SEMANTIC_COVERAGE_NO_RECLASSIFICATION',
         'sufficient_for_s1':False,
         's1_identity_truth':'r7_inventory.py EXACT_BYTES_PINNED_118_INVENTORY_ONLY',
         'coverage':copy.deepcopy(source.get('coverage',{}))}
    issues=[];check_history(obj,issues)
    if issues:raise ValueError('Legacy source insufficient or internally inconsistent: '+repr(issues[:12]))
    return obj

def main():
    p=argparse.ArgumentParser();p.add_argument('source_spine');p.add_argument('output');a=p.parse_args()
    path=pathlib.Path(a.output)
    if path.exists():raise SystemExit('Refusing to overwrite historical conservation transfer')
    try:obj=transfer(pathlib.Path(a.source_spine).read_bytes())
    except (OSError,ValueError) as exc:raise SystemExit(str(exc))
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
    print(json.dumps({'status':'TRANSFERRED_ONLY_NOT_SOURCE_AUTHENTICATED_NOT_S1_IDENTITY_TRUTH','historical_records':sum(map(len,REQUIRED.values())),
                      'path':str(path),'source_sha256':obj['source_spine_sha256']},indent=2))
if __name__=='__main__':sys.exit(main())
