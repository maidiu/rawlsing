#!/usr/bin/env python3
from __future__ import annotations
import base64,csv,hashlib,io,json,lzma,pathlib,subprocess,zlib
from collections import Counter,defaultdict

ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT
for p in [ROOT,*ROOT.parents]:
    if (p/".git").exists():
        REPO=p; break

N01_COMMIT="d4a2b141a68e077d1c2189c68d4bf75d11f13b9d"
N01_ROOT="data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1/PSC_FIRST_ACTIVE_WAVE_R1/WORKER_RETURNS/N01-R2"
N01_MANIFEST=N01_ROOT+"/N01_R2_CURRENT_IMPLEMENTATION_IDENTITY_MANIFEST.json"
R3A_COMMIT="9a31f6ddd984a43076cb89043a70ab19195332f5"
R3A_ROOT="WORKER_COMMISSIONS/EE-R3A"
R3A_ORD=R3A_ROOT+"/04_SELECTED_18012_ORDINALS_COMPLEMENT.json"
R3A_CONTRACT=R3A_ROOT+"/02_SELECTED_18012_ID_SELECTOR_CONTRACT.json"
EXPECTED_LEDGER_SHA="0ac4cd90c19c859438ec12ddfa69c37e9b9c85607884e0f4ea93bc6b52493723"
EXPECTED_SELECTED_ID_SHA="582dc702d1c974b5e57931c2462468523cf73ddf997c00f05dc5e5c0e95ba7b0"
EXPECTED = {
"Afrobarometer":(890,"6b9a0d7af74bd36db0ea9d02b67b0ccc788957acf31724260fbeb7952ff63ae3","012c5d0ae24dbce28fa3a48f24fc53a480df12c7860ae486d9f2f16f569a4983"),
"Arab Barometer":(1665,"cf597a52c57a3e8169bec8050dd5bf7d0a8d2f35a7a732700b1d7d5a921c48f8","40870e62d41bf6877894c3673373f4442a1e2b632fefc8a31350244493225fca"),
"Asian Barometer":(797,"264e501aeacb259935084c1e2227969464d5e4d677b7f3c8b7bf3bea0f9760ac","aceda6c729b2e1e50308a86d35a39ee3653c88d73c157c73b9a5ac208bd2a438"),
"EVS":(2215,"e835b3a15c88d5961b474f445903424b45fa42ac412de7f4941f8462ac4c0c01","cd8e17f4d93bd12547a8a032d88745b681bd58b71f4184a335e147d766532667"),
"GSS":(5959,"d59c83cd4185e6fa8f7c97f2b294f2928512c0da2961210fa98af658d02f36e6","dc9897f42d7e1048ee11300466d77100fc3118bf5f980ab330c27cfb53d883af"),
"Latinobarómetro":(766,"7af23264fb71549b003dc6a936a81d21709a674c91b019e14c4f00f70ed8b4b6","81d5cdf04c9f596e66190cb607a6c86e64182227e68292ba2cc668119b4c9c1a"),
"LiTS":(4402,"b06cf35a0e24f446008781e1c87968e00b398fa3a3c246c6f1a2c80de2c4c24f","a620325970b9879563a7bd910e9fdacc7c41596f6c788c93b6ac530e8ba322d2"),
"South Asia":(123,"2887205cb37fd01ba053e8a8e0fba6f4be8105bbdf8bce25118f84441b4b496c","ae3b375eb7b8b8c374f799819390c819b20e6bf9c140ce2345614baa32ce8f03"),
"WVS":(1195,"d4722273b3cf7c81fa3f74a6415de27ddc891396e089b69ceb054bfa54f0e572","d1f9d49afe3cc05ae0d8145a4f118bff2f403c42141addf7913ef84d7ed2505a")
}

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def git_bytes(ref,path):
    return subprocess.check_output(["git","show",f"{ref}:{path}"],cwd=REPO)
def loadj(ref,path): return json.loads(git_bytes(ref,path).decode("utf-8"))

def reconstruct_n01():
    m=loadj(N01_COMMIT,N01_MANIFEST); chunks=[]
    for part in m["carrier"]["parts"]:
        b=git_bytes(N01_COMMIT,N01_ROOT+"/"+part["path"])
        assert len(b)==part["bytes"] and sha(b)==part["sha256"]
        chunks.append(b)
    seed=lzma.decompress(base64.b64decode(b"".join(chunks)),format=lzma.FORMAT_XZ)
    assert sha(seed)==m["carrier"]["seed_csv_sha256"]
    seeds=list(csv.DictReader(io.StringIO(seed.decode("utf-8"),newline="")))
    rows=[]
    for s in seeds:
        hh=hashlib.sha256((s["source_family"]+"\x1f"+s["wave"]+"\x1f"+s["source_variable_code"]).encode()).hexdigest()
        rows.append({"question_implementation_id":"question_impl.phase0."+hh[:20],**s})
    assert len(rows)==18276 and len({x["question_implementation_id"] for x in rows})==18276
    observed=[]
    last=None
    for r in rows:
        if r["source_family"]!=last:
            observed.append(r["source_family"]); last=r["source_family"]
    assert observed==m["family_order"], (observed,m["family_order"])
    assert len(observed)==9
    return rows,m

def main():
    rows,m=reconstruct_n01()
    ordc=loadj(R3A_COMMIT,R3A_ORD)
    excluded=set(ordc["excluded_ordinals_1_based"])
    selected=[i for i in range(1,18277) if i not in excluded]
    assert len(selected)==18012
    ids=[rows[i-1]["question_implementation_id"] for i in selected]
    assert sha(("".join(x+"\n" for x in ids)).encode("ascii"))==EXPECTED_SELECTED_ID_SHA
    contract=loadj(R3A_COMMIT,R3A_CONTRACT)
    assert contract["selection"]["selected_id_stream_sha256"]==EXPECTED_SELECTED_ID_SHA

    byfam=defaultdict(list)
    for i in selected: byfam[rows[i-1]["source_family"]].append(i)
    assert set(byfam)==set(EXPECTED)
    for fam,(count,ordsha,carrier_sha) in EXPECTED.items():
        ords=byfam[fam]
        actual_ordsha=sha(("".join(f"{i}\n" for i in ords)).encode("ascii"))
        actual_carrier=sha(f"{EXPECTED_LEDGER_SHA}:{actual_ordsha}".encode("ascii"))
        assert len(ords)==count
        assert actual_ordsha==ordsha
        assert actual_carrier==carrier_sha

    print(json.dumps({
        "schema":"RAWLSING_EE_R4C_REPLAY@1.0.0",
        "status":"PASS",
        "selected_count":len(selected),
        "unit_count":len(byfam),
        "unit_counts":{k:len(v) for k,v in sorted(byfam.items())},
        "selected_id_stream_sha256":EXPECTED_SELECTED_ID_SHA,
        "partition":"EXACT_N01_SOURCE_FAMILY_BLOCKS_INTERSECT_R3A_SELECTOR"
    },ensure_ascii=False,indent=2,sort_keys=True))

if __name__=="__main__": main()
