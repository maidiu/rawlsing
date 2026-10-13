#!/usr/bin/env python3
"""PYAT R3 S05 - empirical composition probe on the implementation base.

Establishes, by IMPORT rather than by prose, which of the mission's named
machinery actually exists in the implementation base tree, and therefore
whether the requested composition is constructible at all.
"""
import json, importlib, sys, traceback
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r3s05")
COMPONENTS = [
 ("C11 release",        "rawlsing_next.pre553_c11_repository"),
 ("C11 integrity",      "rawlsing_next.pre553_c11_integrity"),
 ("Route B",            "rawlsing_next.pre553_source_backed_c11_facade"),
 ("empirical query",    "rawlsing_next.pre553_empirical_query"),
 ("discovery exact",    "rawlsing_next.pre553_discovery_exact"),
 ("batch runner",       "rawlsing_next.pre553_batch_runner"),
 ("analytical comp",    "rawlsing_next.pre553_analytical_composition"),
 ("field forge",        "rawlsing_next.field_forge_conditional_support"),
 ("learned product",    "rawlsing_next.pre553_learned_product_release"),
 ("V2 verifier E",      "rawlsing_next.pre553_original_workload_v2_verifier_candidate"),
 ("V2 contract",        "rawlsing_next.pre553_original_workload_contract_v2_candidate"),
 ("governed batch",     "rawlsing_next.pre553_governed_batch_checkpoint_integration_candidate"),
 ("durable checkpoint", "rawlsing_next.pre553_batch_durable_checkpoint_candidate"),
 ("separate principal", "rawlsing_next.pre553_b5_separate_principal_verifier_candidate"),
]
rows=[]
for label, mod in COMPONENTS:
    try:
        importlib.import_module(mod); rows.append({"component":label,"module":mod,"state":"PRESENT_IMPORTABLE"})
    except ModuleNotFoundError as e:
        rows.append({"component":label,"module":mod,"state":"ABSENT","error":str(e)[:60]})
    except Exception as e:
        rows.append({"component":label,"module":mod,"state":"PRESENT_IMPORT_ERROR","error":f"{type(e).__name__}: {str(e)[:60]}"})
present=[r for r in rows if r["state"]=="PRESENT_IMPORTABLE"]
absent=[r for r in rows if r["state"]=="ABSENT"]
mission_critical_absent=[r for r in absent if r["component"] in
   ("V2 verifier E","V2 contract","governed batch","durable checkpoint","batch runner") ]
out={"schema":"PYAT_R3_S05_COMPOSITION_PROBE@1",
 "base":"7f29aec36d24f16da52d84f17c00f08db3a55434",
 "components":rows,"present":len(present),"absent":len(absent),
 "composition_possible_on_base": len(mission_critical_absent)==0,
 "mission_critical_absent":[r["component"] for r in mission_critical_absent],
 "verdict":("COMPOSABLE" if not mission_critical_absent else
   "NOT_COMPOSABLE_ON_BASE__CANDIDATE_MODULES_LIVE_ON_UNMERGED_WORKER_BRANCHES")}
print(json.dumps(out,indent=1))
