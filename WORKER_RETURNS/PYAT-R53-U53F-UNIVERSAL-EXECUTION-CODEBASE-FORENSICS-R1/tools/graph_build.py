"""04/05 — anchored universal producer→consumer graph and unresolved edges."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

SEALED_NODES = [
    ("source_authority", "SOURCE_AUTHORITY", "data/ddm_build_copy/ddm_v550_question_relation_authority.py",
     "question-relation authority index / CLOSED_35 roster", "Source/semantic authority owners"),
    ("u_epre", "U_EPRE", "rawlsing_next/pre553_source_local_universe_admission.py",
     "source-local universe admission", "Source/operation issuer"),
    ("compiler", "FINITE_COMPILER", "rawlsing_next/pre553_discovery_exact.py",
     "exact-bounded discovery/frontier", "Discovery owner"),
    ("batch", "I03_I05_BATCH", "rawlsing_next/pre553_batch_runner.py",
     "batch execution runner", "Batch owner"),
    ("c11", "C11_ROUTE_B", "rawlsing_next/pre553_source_backed_c11_facade.py",
     "source-backed C11 facade", "C11 owner"),
    ("routeb", "ROUTE_B", "rawlsing_next/pre553_route_b_production.py",
     "Route B production/empirical objects", "Route B owner"),
    ("i03", "I03_QUERY", "rawlsing_next/pre553_empirical_query.py",
     "exact empirical query", "I03 owner"),
    ("i05", "I05_PROVIDER", "rawlsing_next/pre553_empirical_possibility_provider.py",
     "single-binding N10E public provider", "I05/N10E owner"),
    ("c1", "C1_COMPOSITION", "rawlsing_next/pre553_analytical_composition.py",
     "multi-binding/joint/recursive composition", "C1 owner"),
    ("learned_m1", "F2_F4_M1", "rawlsing_next/pre553_learned_empirical_adjudication.py",
     "learned empirical adjudication", "M1 owner"),
    ("learned_m2", "F2_F4_M2", "rawlsing_next/pre553_learned_product_release.py",
     "learned product release", "M2 owner"),
    ("lifecycle", "F2_F4_B5", "rawlsing_next/pre553_learned_product_lifecycle.py",
     "learned product lifecycle", "B5 owner"),
    ("learned_i4", "F2_F4_I4", "rawlsing_next/pre553_learned_world_composition.py",
     "learned world composition", "I4 owner"),
    ("f5_ff", "F5_STRUCTURAL", "rawlsing_next/field_forge_conditional_support.py",
     "Field Forge conditional support", "Field Forge owner"),
    ("f7_v553", "F7_TEMPORAL", "data/ddm_build_copy/ddm_v553_temporal_pressure.py",
     "V553 temporal pressure method", "Temporal method owner"),
]
BRANCH_NODES = [
    ("f6m", "F6_PARTIAL", "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
     "WORKER_RETURNS/PYAT-R23-F6C-NATIVE-F6-COMPARATIVE-CONTINUATION-R1/05_NATIVE_STAGE/rawlsing_next/pre553_heterogeneous_synthesis.py",
     "F6M partial-bound synthesis", "F6 scientific/model owner", "BRANCH_BLOB_R23_F6C"),
    ("f43", "F43_WORLD_PRODUCTS", "100ae7832ddc2c5edb7abdbd7e2cb94b5f9e8733",
     "WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1/f43_product.py",
     "retained F5 + F6 bounds + F7 method products", "F43 author", "BRANCH_COMMIT_100ae783"),
    ("w41", "N9_WORLD", "b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2",
     "WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/objective_world.py",
     "ObjectiveWorld retained/sourcefree world", "W41 author", "BRANCH_COMMIT_b0a68e4f"),
    ("j42", "N9_N10E_N10W_JOIN", "f53cb0d2bce52640268c844c398bbd8007d28edc",
     "WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1/runtime/j42_join.py",
     "E41+W41+P41 joined consumer", "J42 author", "BRANCH_COMMIT_f53cb0d2"),
    ("p41", "P41_SERVICE", "f27d1101048638bba395143a48efb7ef00bfcda4",
     "WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-N10E-N10W-SERVING-R1/runtime/p41_service.py",
     "P41 progressive service", "P41 author", "BRANCH_COMMIT_f27d1101"),
    ("e41", "E41_SLICE_PROVIDER", "6e123bafe749d6997c764ae117fb5e68e0139ed7",
     "WORKER_RETURNS/PYAT-R41-E41-FULL-EMPIRICAL-F1F4-COMPUTED-POSSIBILITY-R1/e41_provider_extension.py",
     "E41 computed N10E slice extension", "E41 author", "BRANCH_COMMIT_6e123baf"),
    ("e04_nonparent", "F8_E04_CONSUMER", "2181b832d3c4376d4b9428e13f4354f273be8f32",
     "WORKER_RETURNS/PYAT-USERDIRECT-20261015-R10-E04-GENERIC-WORLD-POSSIBILITY-SERVICE-R1/product/nonparent.py",
     "original NONPARENT_OPTIONS consumer", "E04 owner", "BLOB_PINNED_R10"),
]

CURATED = [
    ("source_authority", "u_epre", "SOURCE_TO_U_EPRE", "DOCUMENTARY_PROPOSED",
     "data/ddm_build_copy/ddm_v550_question_relation_authority.py:570",
     "CLOSED_35 roster function exists; no source-indexed U/E_pre issuance path found"),
    ("u_epre", "compiler", "U_EPRE_TO_FINITE_COMPILER", "DOCUMENTARY_PROPOSED",
     "rawlsing_next/pre553_source_local_universe_admission.py:1",
     "admission module documents source-local use; no universal planner call site found"),
    ("compiler", "batch", "COMPILER_TO_BATCH", "DOCUMENTARY_PROPOSED",
     "rawlsing_next/pre553_batch_runner.py:1",
     "batch runner is separate; no static call from discovery"),
    ("f5_ff", "f43", "F5_FF_TO_F43", "DOCUMENTARY_PROPOSED",
     "WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1/00_RETURN.md:1",
     "F43 retained GT2 context consumes FF->V554->M4 relation at retained scope only"),
    ("f6m", "f43", "F6_TO_F43", "DOCUMENTARY_PROPOSED",
     "WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1/00_RETURN.md:1",
     "F43 F6M/F6P evidence and bounds; original N9 admission not granted"),
    ("f7_v553", "f43", "F7_TO_F43", "DOCUMENTARY_PROPOSED",
     "WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1/00_RETURN.md:1",
     "F43 F7 strict pre-guard over V553/EE1; observed pairs held"),
    ("f43", "w41", "F43_TO_N9_WORLD", "DOCUMENTARY_PROPOSED",
     "WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1/f43_product.py:1",
     "F43 original_client_view uses W41 ObjectiveWorld; F43 channels not admitted to it"),
    ("w41", "j42", "N9_TO_JOINED", "DOCUMENTARY_PROPOSED",
     "WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1/00_RETURN.md:1",
     "J42 consumes 84 W41 worlds"),
    ("j42", "p41", "JOIN_TO_P41", "EXACT_STATIC_EDGE",
     "WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1/runtime/j42_join.py:1",
     "J42 imports/stages P41 service"),
    ("e41", "j42", "E41_TO_JOIN", "DOCUMENTARY_PROPOSED",
     "WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1/00_RETURN.md:1",
     "J42 consumes E41 computed slices"),
    ("w41", "e04_nonparent", "N9_TO_E04", "DOCUMENTARY_PROPOSED",
     "WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/00_RETURN.md:1",
     "W41 original_client_view invokes unchanged NONPARENT_OPTIONS"),
    ("p41", "e04_nonparent", "P41_TO_E04", "DOCUMENTARY_PROPOSED",
     "WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-N10E-N10W-SERVING-R1/00_RETURN.md:1",
     "P41 original consumer path uses unchanged E04 consumer"),
]

UNRESOLVED = [
    ("source_authority", "u_epre", "SOURCE_INDEXED_OPERATION_ISSUANCE", "DOCUMENTARY_PROPOSED",
     "No generic source-indexed U/E_pre or per-wave operation issuance found"),
    ("u_epre", "compiler", "UNIVERSAL_WORKLOAD_PLANNER", "DYNAMIC_UNRESOLVED",
     "No source-parameterized universal worklist compiler call site found in sealed tree"),
    ("compiler", "batch", "COMPILER_TO_BATCH_EXACT", "DYNAMIC_UNRESOLVED",
     "Discovery and batch are not statically joined in the sealed canonical modules"),
    ("f5_ff", "w41", "F5_STRUCTURAL_TO_N9_ROUTE", "INCOMPATIBLE",
     "Retained GT2 CONTEXT is not structural-route permission; no N9 route join"),
    ("f6m", "w41", "F6_TO_N9_ORIGINAL", "INCOMPATIBLE",
     "No F6 target/transport/model grant; F6 stays separate readonly evidence"),
    ("f7_v553", "w41", "F7_OBSERVED_PAIR_TO_N9", "DYNAMIC_UNRESOLVED",
     "0 observed original comparable pairs; policy epochs are synthetic"),
    ("w41", "e04_nonparent", "N9_TO_E04_EXACT", "DOCUMENTARY_PROPOSED",
     "Actual consumer only in worker-return scope; not sealed canonical"),
    ("p41", "e04_nonparent", "P41_TO_E04_EXACT", "DOCUMENTARY_PROPOSED",
     "P41 consumer is worker-return scope; not sealed canonical"),
    ("e04_nonparent", "n11", "F8_TO_N11_ADOPTION", "INCOMPATIBLE",
     "N11 adoption remains A42/HQ; no accepted joined estate"),
]


def node_blob(node, sealed):
    _, _, ref_or_blob, path, _, _, provenance = node
    if provenance.startswith("BRANCH_COMMIT_"):
        commit = ref_or_blob
        got = C.run(["git", "rev-parse", f"{commit}:{path}"], check=False)
        return got.stdout.strip() if got.returncode == 0 else ""
    if provenance.startswith("BRANCH_BLOB") or provenance.startswith("BLOB_PINNED"):
        return ref_or_blob
    return sealed.get(path, "")


def main():
    sealed_rows = {row["path"]: row for row in C.ls_tree()}
    sealed = {path: row["blob"] for path, row in sealed_rows.items()}
    nodes = []
    module_to_id = {}
    for node in SEALED_NODES:
        node_id, stage, path, role, owner = node
        blob = sealed.get(path, "")
        nodes.append(dict(node_id=node_id, stage=stage, path=path, blob=blob,
                          role=role, owner=owner, status="SEALED_TREE_MODULE",
                          provenance="SEALED_TREE"))
        module_to_id["rawlsing_next." + Path(path).stem] = node_id
        module_to_id[Path(path).stem] = node_id
    for node in BRANCH_NODES:
        node_id, stage, ref, path, role, owner, provenance = node
        blob = node_blob(node, sealed)
        nodes.append(dict(node_id=node_id, stage=stage, path=path, blob=blob,
                          role=role, owner=owner,
                          status="BRANCH_ONLY_RETURN_MODULE" if blob else "DOCUMENTARY_ONLY",
                          provenance=provenance))
        module_to_id[Path(path).stem] = node_id
    module_to_id["product.nonparent"] = "e04_nonparent"
    module_to_id["nonparent"] = "e04_nonparent"

    exports = {}
    edges = []
    for node in nodes:
        blob = node["blob"]
        if not blob:
            continue
        try:
            tree = ast.parse(C.read_blob(blob).decode("utf-8", "replace"))
        except SyntaxError:
            continue
        funcs = {n.name: n.lineno for n in tree.body if isinstance(n, ast.FunctionDef)}
        exports[node["node_id"]] = funcs
        imported = {}
        for item in ast.walk(tree):
            if isinstance(item, ast.ImportFrom) and item.module:
                target = module_to_id.get(item.module)
                if target:
                    edges.append(dict(caller=node["node_id"], callee=target,
                                      kind="IMPORT", callee_symbol=",".join(
                                          a.name for a in item.names),
                                      line=item.lineno, caller_path=node["path"],
                                      caller_blob=blob, status="EXACT_STATIC_EDGE"))
                    for alias in item.names:
                        imported[alias.asname or alias.name] = target
            if isinstance(item, ast.Call) and isinstance(item.func, ast.Name):
                target = imported.get(item.func.id)
                if target:
                    edges.append(dict(caller=node["node_id"], callee=target,
                                      kind="CALL", callee_symbol=item.func.id,
                                      line=getattr(item, "lineno", 0),
                                      caller_path=node["path"], caller_blob=blob,
                                      status="EXACT_STATIC_EDGE"))
    for source, target, kind, status, anchor, note in CURATED:
        edges.append(dict(caller=source, callee=target, kind=kind,
                          callee_symbol="", line=0, caller_path="", caller_blob="",
                          doc_anchor=anchor, status=status, note=note))
    seen = set()
    unique = []
    for edge in edges:
        key = (edge["caller"], edge["callee"], edge["kind"], edge["line"],
               edge.get("callee_symbol", ""), edge.get("doc_anchor", ""))
        if key in seen:
            continue
        seen.add(key)
        unique.append(edge)
    blob_by_id = {n["node_id"]: (n["blob"], n["path"]) for n in nodes}
    for edge in unique:
        if edge.get("doc_anchor") and not edge.get("caller_blob"):
            blob, path = blob_by_id.get(edge["caller"], ("", ""))
            edge["caller_blob"] = blob
            edge["caller_path"] = path
    anchored = [e for e in unique if e.get("caller_blob") and (e.get("line") or e.get("doc_anchor"))]
    nodes_jsonl = "\n".join(json.dumps(dict(record_type="node", **n), sort_keys=True) for n in nodes) + "\n"
    edges_jsonl = "\n".join(json.dumps(dict(record_type="edge", **e), sort_keys=True) for e in unique) + "\n"
    C.write_text(C.OUT / "04_UNIVERSAL_PRODUCER_CONSUMER_GRAPH.jsonl",
                 nodes_jsonl + edges_jsonl)
    C.write_tsv(C.OUT / "05_UNRESOLVED_DYNAMIC_AND_MISSING_EDGES.tsv",
                ("source_stage", "target_stage", "edge_kind", "status", "reason"),
                UNRESOLVED)
    receipt = dict(schema="R53_U53F_GRAPH_RECEIPT@1",
                   nodes=len(nodes), edges=len(unique), anchored_edges=len(anchored),
                   exact_static_edges=sum(1 for e in unique if e["status"] == "EXACT_STATIC_EDGE"),
                   documentary_edges=sum(1 for e in unique if e["status"] == "DOCUMENTARY_PROPOSED"),
                   unresolved=len(UNRESOLVED),
                   node_status_counts=dict(__import__("collections").Counter(n["status"] for n in nodes)),
                   limitation="Only declared nodes are graphed; static import/call edges are from exact AST; "
                              "documentary edges are anchored claims, not executed proof.")
    C.write_json(C.EVID / "graph_receipt.json", receipt)
    print(json.dumps(receipt, indent=1))


if __name__ == "__main__":
    main()
