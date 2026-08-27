#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from rawlsing_next.pre553_as4i0_route_b_driver import load_and_validate_as3r2, preflight_receipt, require_runtime_catalog_payload, RuntimeCatalogPreimageMissing

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--as3r2",required=True,type=Path)
    p.add_argument("--receipt",required=True,type=Path)
    p.add_argument("--runtime-catalog",type=Path)
    a=p.parse_args()
    seal=load_and_validate_as3r2(a.as3r2)
    out=preflight_receipt()
    try:
        require_runtime_catalog_payload(a.runtime_catalog or (a.as3r2/"__missing_runtime_catalog__.json"),seal)
        out["runtime_catalog_preimages"]="PRESENT_AND_EXACT"
    except RuntimeCatalogPreimageMissing as exc:
        out["status"]="PASS_PREFLIGHT__EXECUTION_FAILS_CLOSED_ON_MISSING_RUNTIME_PREIMAGES"
        out["blocker"]=str(exc)
    a.receipt.parent.mkdir(parents=True,exist_ok=True)
    a.receipt.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
