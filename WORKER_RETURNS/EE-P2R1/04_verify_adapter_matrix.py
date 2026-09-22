#!/usr/bin/env python3
"""EE-P2R1 accepted-owner adapter matrix and WVS-C portability adjudication."""
from __future__ import annotations

import argparse
import ast
import json
import runpy
import subprocess
from pathlib import Path

from rawlsing_next.pre553_empirical_objects import semantic_hash

OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
A_PATH = "rawlsing_next/pre553_r5_source_backed_adapter.py"
B_PATH = "rawlsing_next/pre553_source_backed_c11_facade.py"
C_PATH = "rawlsing_next/pre553_route_c_accelerators.py"
A_BLOB = "d4915e7e6755ba1850756aebff72f982f73a332b"
C_BLOB = "abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889"
P2X_A_FIRST_BUILD = "02a7ff71ae65b1aa8c52add0b315244a9eaea9df"
P2X_RETURN = "29e434a385719f9835e0bcd252fb24bc37675a99"


def ensure(commit: str) -> None:
    p=subprocess.run(["git","cat-file","-e",commit+"^{commit}"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if p.returncode:
        subprocess.run(["git","fetch","--no-tags","origin",commit],check=True,stdout=subprocess.DEVNULL)


def git_text(commit: str, path: str) -> str:
    ensure(commit)
    return subprocess.run(["git","show",f"{commit}:{path}"],check=True,stdout=subprocess.PIPE,text=True).stdout


def functions(source: str):
    tree=ast.parse(source)
    return {node.name:node for node in ast.walk(tree) if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))}


def arg_names(fn):
    return tuple(a.arg for a in (*fn.args.args,*fn.args.kwonlyargs))


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=Path); args=ap.parse_args()
    a=git_text(OWNER_COMMIT,A_PATH); b=git_text(OWNER_COMMIT,B_PATH); c=git_text(OWNER_COMMIT,C_PATH)
    af,bf,cf=functions(a),functions(b),functions(c)
    if "build_r5_source_backed_c11_repository" not in af:
        raise RuntimeError("accepted Candidate-A repository builder absent")
    if not {"reader","projection"} <= set(arg_names(af["build_r5_source_backed_c11_repository"])):
        raise RuntimeError("Candidate-A accepted builder signature drift")
    if "build_source_backed_c11_repository" not in bf:
        raise RuntimeError("accepted Candidate-B repository builder absent")
    if not {"source","projection"} <= set(arg_names(bf["build_source_backed_c11_repository"])):
        raise RuntimeError("Candidate-B accepted builder signature drift")
    if "build_route_c_repository" not in cf:
        raise RuntimeError("accepted Candidate-C repository builder absent")
    c_repo_args=set(arg_names(cf["build_route_c_repository"]))
    if not {"cacc1","projection"} <= c_repo_args:
        raise RuntimeError("Candidate-C repository builder signature drift")
    i05=cf.get("execute_route_c_exact_bounded_discovery")
    if i05 is None:
        raise RuntimeError("Candidate-C I05 owner entrypoint absent")
    i05_args=set(arg_names(i05))
    if not {"cacc1","cacc2_directory","cacc2_manifest"} <= i05_args:
        raise RuntimeError("Candidate-C I05 accelerator requirements drift")

    lits_c_ns=runpy.run_path("WORKER_RETURNS/EE-P2R1/03_materialize_lits_c_real_bindings.py")
    lits_c=lits_c_ns["materialize"]()
    if lits_c["role_count"] != 19 or lits_c["distinct_runtime_predicate_count"] != 18:
        raise RuntimeError("LiTS-C real role binding closure failed")

    matrix = {
      "LITS_I": {
        "A": {
          "status":"READY__PRESERVED_R5_PLUS_ACCEPTED_PROJECTION_TO_COMMON_RUNNER",
          "owner_entrypoint":"build_r5_source_backed_c11_repository",
          "preserve_first_build_receipt":P2X_A_FIRST_BUILD,
          "rebuild_performed_here":False,
        },
        "B": {
          "status":"READY__CACHELESS_SOURCE_BACKED_C11_TO_COMMON_RUNNER",
          "owner_entrypoint":"build_source_backed_c11_repository",
          "broken_B16_bootstrap_used":False,
        },
        "C": {
          "status":"READY__REAL_CACC1_CACC2_BINDINGS_MATERIALIZED_TO_COMMON_RUNNER",
          "owner_entrypoint":"build_route_c_repository",
          "role_count":19,
          "distinct_runtime_predicates":18,
          "third_accelerator_created":False,
        },
      },
      "WVS7": {
        "A": {
          "status":"PREPARATION_READY__GENERIC_R5_OWNER_PLUS_EXACT_GOVERNED_PROJECTION",
          "dispositive_r5_build_performed_here":False,
        },
        "B": {
          "status":"PREPARATION_READY__SOURCE_BACKED_OWNER_PLUS_EXACT_GOVERNED_PROJECTION",
          "dispositive_source_execution_performed_here":False,
        },
        "C": {
          "status":"WVS7_C__CURRENT_PORTABILITY_FAILURE",
          "reason":"accepted Candidate-C repository path requires CACC1 and accepted I05 path requires CACC1+CACC2; no zero-accelerator repository/I05 entrypoint exists",
          "wvs_accelerator_invented":False,
          "blocks_wvs_A_or_B":False,
        },
      },
    }
    material={
      "schema":"EE_P2R1_ABC_ADAPTER_QUALIFICATION_MATRIX@1.0.0",
      "status":"PASS__LAWFUL_FINAL_P2_CELLS_BINDABLE__WVS_C_PORTABILITY_FAILURE_PRESERVED",
      "owner_commit":OWNER_COMMIT,
      "owner_paths":{"A":A_PATH,"B":B_PATH,"C":C_PATH},
      "owner_blobs":{"A":A_BLOB,"C":C_BLOB},
      "p2x_adopted_return":P2X_RETURN,
      "source_access":False,
      "performance_measurement":False,
      "candidate_redesign":False,
      "matrix":matrix,
    }
    result={**material,"receipt_identity":semantic_hash(material)}
    rendered=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(rendered,encoding="utf-8")
    print(rendered,end="")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
