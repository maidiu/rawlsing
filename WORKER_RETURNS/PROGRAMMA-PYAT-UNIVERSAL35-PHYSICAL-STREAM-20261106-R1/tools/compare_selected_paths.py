"""Compare current filtered scan with the projected selected-column producer."""
from __future__ import annotations
import hashlib, itertools, json, os, pickle, resource, shutil, subprocess, sys, time
from pathlib import Path

HERE=Path(__file__).resolve(); REPO_ROOT=HERE.parents[4]
if str(REPO_ROOT) not in sys.path: sys.path.insert(0,str(REPO_ROOT))
from rawlsing_next.pre553_original35_physical_stream import bounded_physical_cell_stream
from rawlsing_next.pre553_physical_decoder import decode_sav, decode_dta
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceIdentity, NativeSourcePackage, NativeSourceRule, materialize_native_preimages
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.source_configuration.reader import reader_configuration_from_config


def rss():
    try:
        return int(subprocess.check_output(["ps","-o","rss=","-p",str(os.getpid())],text=True).strip())*1024
    except Exception:
        return None


def select_names(doc, max_items):
    routing={row["question_id"]:row for row in doc.get("routing",())}
    qualified=[]
    for slot in doc.get("response_slots",()):
        name=slot["slot"]["name"]
        if routing.get(name,{}).get("typed_state")!="ELIGIBLE_APPLICABLE": continue
        if any(v.get("response_state")=="SUBSTANTIVE_RESPONSE" and v.get("canonical_value") is not None for v in slot.get("values",())):
            qualified.append(name)
    qualified=qualified[:max_items]
    names=set(qualified)
    coordinate=next((s["slot"]["name"] for s in doc.get("coordinate_slots",()) if s["slot"]["name"] not in names),None)
    if coordinate is None:
        coordinate=next((s["name"] for s in doc.get("physical_slots",()) if s["name"] not in names),None)
    if not qualified or coordinate is None: raise RuntimeError("selection incomplete")
    return tuple(qualified), coordinate


def digest(cells):
    h=hashlib.sha256(); n=0
    for cell in cells:
        h.update(pickle.dumps(cell, protocol=5)); n+=1
    return h.hexdigest(), n


def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("--source-id",required=True); ap.add_argument("--max-items",type=int,default=1); ap.add_argument("--batch-size",type=int,default=10000)
    ap.add_argument("--binding",default=str(REPO_ROOT/".local-logs/pyat-universal35/source-runtime-binding.local.json")); ap.add_argument("--outdir",default=str(REPO_ROOT/".local-logs/pyat-universal35/physical-stream/results")); ap.add_argument("--tmpdir",default=str(REPO_ROOT/".local-logs/pyat-universal35/physical-stream/tmp"))
    args=ap.parse_args(); Path(args.tmpdir).mkdir(parents=True,exist_ok=True); os.environ["TMPDIR"]=args.tmpdir
    binding=json.loads(Path(args.binding).read_text()); root=binding["USER_ORIGINAL35_DATA_ROOT"]
    lib=SourceConfigLibrary(source_root=root); cfg=lib.load_original(args.source_id); doc=cfg.document; rc=reader_configuration_from_config(cfg); res=lib.resolve_source_path(args.source_id)
    path=res["resolved_source_path"]
    start=time.perf_counter(); inc=(decode_sav(path,encoding=rc.encoding,expected_source_sha256=cfg.original_source_sha256) if doc["identity"]["source_format"]=="SAV" else decode_dta(path,encoding=rc.encoding,expected_source_sha256=cfg.original_source_sha256))
    decode_wall=time.perf_counter()-start; decode_rss=rss()
    selected, coordinate=select_names(doc,args.max_items); wanted=set(selected)|{coordinate}
    base_start=time.perf_counter(); base_cells=[]; all_cells=0
    for cell in inc.iter_cells():
        all_cells+=1
        if cell.variable_name in wanted: base_cells.append(cell)
    base_wall=time.perf_counter()-base_start
    projected=tuple(bounded_physical_cell_stream(inc, batch_size=args.batch_size, include_variables=tuple(selected)+(coordinate,)).iter_cells())
    projected_wall=time.perf_counter()-base_start-base_wall
    identical=len(base_cells)==len(projected) and all(a==b for a,b in zip(base_cells,projected))
    base_digest=digest(base_cells); proj_digest=digest(projected)
    package=NativeSourcePackage(
        source=NativeSourceIdentity(source_id=args.source_id,family=str(doc["identity"]["family"]),wave=str(doc["identity"]["wave"]),canonical_filename=str(doc["identity"]["source_artifact_id"]),declared_sha256=inc.source_sha256,source_format=str(doc["identity"]["source_format"]),expected_rows=inc.row_count),
        selected=tuple(NativeSourceRule(implementation_id=args.source_id+":"+name,source_variable_code=name,unit="person") for name in selected),
        coordinate_variable=coordinate, study_product_id=str(doc["identity"]["study_product_id"]), release_id=str(doc["identity"]["release_id"]), instrument_release_id=str(doc["identity"]["instrument_release_id"]), as_of="TEST_ONLY")
    base_stream=ExactPhysicalCellStream(source_sha256=inc.source_sha256,row_count=inc.row_count,cell_iter_factory=lambda: tuple(base_cells),decoder_metadata_digest=inc.physical_metadata_digest)
    projected_stream=bounded_physical_cell_stream(inc,batch_size=args.batch_size,include_variables=tuple(selected)+(coordinate,))
    native={}
    for label,stream in (("current_filtered",base_stream),("projected",projected_stream)):
        t=time.perf_counter(); bundle=materialize_native_preimages(package=package,incidence=stream); native[label]={"wall_s":time.perf_counter()-t,"release_ref":bundle.release.release_ref.as_dict(),"replay_ref":bundle.release.replay_manifest.ref.as_dict(),"semantic_release_hash":bundle.release.semantic_release_hash,"public_object_count":len(bundle.release.public_objects)}
    inc.close()
    native_equal=all(native["current_filtered"][key]==native["projected"][key] for key in ("release_ref","replay_ref","semantic_release_hash","public_object_count"))
    payload={"schema":"PYAT_UNIVERSAL35_SELECTED_READER_COMPARE@1","source_id":args.source_id,"selected_items":list(selected),"coordinate":coordinate,"source_sha256":inc.source_sha256,"row_count":inc.row_count,"source_bytes":Path(path).stat().st_size,"decode_wall_s":decode_wall,"decode_rss":decode_rss,"baseline":{"wall_s":base_wall,"all_cells_created":all_cells,"selected_cells":len(base_cells),"digest":base_digest[0],"selected_digest_count":base_digest[1]},"projected":{"wall_s":projected_wall,"selected_cells":len(projected),"digest":proj_digest[0],"selected_digest_count":proj_digest[1],"maxrss":rss()},"exact_selected_cells":identical,"native_package":native,"native_package_outputs_equal":native_equal}
    Path(args.outdir).mkdir(parents=True,exist_ok=True); out=Path(args.outdir)/f"{args.source_id}_selected_compare.json"; out.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"path":str(out),"source_id":args.source_id,"selected_items":list(selected),"coordinate":coordinate,"baseline_wall_s":base_wall,"projected_wall_s":projected_wall,"baseline_all_cells":all_cells,"selected_cells":len(projected),"exact":identical,"digests":(base_digest[0],proj_digest[0]),"native_equal":native_equal},sort_keys=True))

if __name__=="__main__": main()
