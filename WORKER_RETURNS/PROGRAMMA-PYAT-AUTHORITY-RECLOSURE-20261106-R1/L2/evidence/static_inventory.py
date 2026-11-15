#!/usr/bin/env python3
"""Read-only deterministic L2 static census. stdout JSON; no file writes."""
import ast
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT=Path("repo_mirror") if Path("repo_mirror/data/ddm_build_copy").is_dir() else Path(".")
CORE=[
 "compile_v551_relation_evidence_atoms.py","ddm_v551_atoms.py","ddm_v551_directionality_expectation.py",
 "ddm_v551_conditional.py","compile_v552_structural_ddm.py","ddm_v552_structural.py",
 "ddm_v552_contract.py","ddm_v552_validation.py","ddm_pipeline_boundary_contract.py",
 "ddm_pipeline_boundary_consumer.py","ddm_v550_schema.py","ddm_v550_manifest.py","ddm_v550_support.py"]
UPSTREAM=[
 "ddm_v550_bridge.py","ddm_v550_response_semantics_authority.py","ddm_v550_question_use.py",
 "ddm_v550_family_overlay.py","ddm_v550_question_relation_authority.py","ddm_v550_response_options.py"]
DOWNSTREAM=["compile_v552j_structural_handoff.py","ddm_v552j_handoff.py","ddm_v552j_validation.py"]
CURRENT=[
 "pre553_empirical_authority.py","pre553_empirical_query.py","pre553_structural_admission.py",
 "pre553_source_relations.py","pre553_runtime_authority.py","pre553_empirical_objects.py",
 "pre553_c11_ingest.py","pre553_source_backed_c11_facade.py"]
ASSETS=[
 "response_scale_encoding_registry_35wave_active_v1.csv",
 "response_scale_encoding_registry_35wave_active_v1.manifest.json",
 "v550_v551_response_semantics_contract_binding_v1.csv",
 "v550_v551_response_semantics_contract_binding_v1.manifest.json"]
DETECT={"read_csv","read_parquet","read_text","read_bytes","open","read_status_document",
 "inspect_artifact","require_canonical_parquet","load_closed_35_waves","to_parquet","to_csv",
 "atomic_write_json","publish_staged_directory","json.load","json.loads","sha256_file"}

def csvg(rows,headers,sep=","):
    buf=io.StringIO()
    w=csv.DictWriter(buf,fieldnames=headers,delimiter=sep,lineterminator="\n",extrasaction="ignore")
    w.writeheader();w.writerows(rows)
    return buf.getvalue()

def fullname(call):
    if isinstance(call,ast.Name):return call.id
    if isinstance(call,ast.Attribute):return fullname(call.value)+"."+call.attr
    return "<dynamic>"

def scan(p,stage):
    raw=p.read_bytes();source=raw.decode("utf-8");t=ast.parse(source)
    parent={}
    for node in ast.walk(t):
        for child in ast.iter_child_nodes(node):parent[child]=node
    cells=[]
    for node in ast.walk(t):
        if not isinstance(node,ast.Call):continue
        name=fullname(node.func);short=name.rsplit(".",1)[-1]
        if short not in DETECT and name not in DETECT:continue
        f=node
        while f in parent and not isinstance(f,(ast.FunctionDef,ast.AsyncFunctionDef)):
            f=parent[f]
        symbol=f.name if isinstance(f,(ast.FunctionDef,ast.AsyncFunctionDef)) else "<module>"
        expression=ast.get_source_segment(source,node) or ""
        cells.append(dict(stage=stage,path=str(p.relative_to(ROOT)),line=node.lineno,
            symbol=symbol,call=name,expression=" ".join(expression.split())[:420]))
    return raw,source,cells

def main():
    inventory=[];io_rows=[]
    groups=[
        ("L2_CORE", "data/ddm_build_copy/",CORE),
        ("UPSTREAM_L1_BOUNDARY", "data/ddm_build_copy/",UPSTREAM),
        ("DOWNSTREAM_L4_HANDOFF","data/ddm_build_copy/",DOWNSTREAM),
        ("CURRENT_L6_NEIGHBOR","rawlsing_next/",CURRENT),
        ("AUTHORITY_REPO_ASSET","data/ddm_build_copy/authority/",ASSETS),
    ]
    for stage,prefix,names in groups:
        for n in names:
            p=ROOT/prefix/n
            if not p.is_file():raise FileNotFoundError(p)
            if p.suffix==".py":
                raw,source,cells=scan(p,stage)
                if stage in ("L2_CORE","DOWNSTREAM_L4_HANDOFF"):
                    io_rows.extend(cells)
                line_count=len(source.splitlines())
            else:
                raw=p.read_bytes();line_count=len(raw.splitlines())
            inventory.append(dict(stage=stage,path=prefix+n,sha256=hashlib.sha256(raw).hexdigest(),
                bytes=len(raw),lines=line_count,static_io_calls=sum(1 for r in io_rows if r["path"]==prefix+n),
                inspected="YES",scope_note="full source text inspected by static census; upstream/current bounded to named modules"))
    inventory.sort(key=lambda r:r["path"])
    io_rows.sort(key=lambda r:(r["path"],int(r["line"]),r["call"]))
    print(json.dumps({
        "inventory":csvg(inventory,["stage","path","sha256","bytes","lines","static_io_calls","inspected","scope_note"],sep="\t"),
        "io":csvg(io_rows,["stage","path","line","symbol","call","expression"]),
        "stats":{"files":len(inventory),"core":len(CORE),"upstream":len(UPSTREAM),"downstream":len(DOWNSTREAM),"current":len(CURRENT),"assets":len(ASSETS),
                 "io_rows":len(io_rows),"core_io":sum(r["stage"]=="L2_CORE" for r in io_rows),
                 "downstream_io":sum(r["stage"]=="DOWNSTREAM_L4_HANDOFF" for r in io_rows)}
    },ensure_ascii=False))

if __name__=="__main__":main()
