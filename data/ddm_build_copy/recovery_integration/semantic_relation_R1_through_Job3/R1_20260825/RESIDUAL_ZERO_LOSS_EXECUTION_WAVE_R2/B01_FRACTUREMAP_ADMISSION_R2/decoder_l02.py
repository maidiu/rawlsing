import struct, pandas as pd
from pathlib import Path

def read_sav_selected(path: Path, want=None):
    f=path.open("rb"); h=f.read(176)
    if h[:4] != b"$FL2": raise RuntimeError("Expected $FL2 SAV")
    layout,case_size,compression,weight_index,ncases=struct.unpack("<5i",h[64:84]); bias=struct.unpack("<d",h[84:92])[0]
    if layout != 2 or compression != 1: raise RuntimeError((layout,compression))
    vars=[]; ext={}; vlraw=[]
    while True:
        raw=f.read(4)
        if len(raw)!=4: raise EOFError("dictionary")
        rt=struct.unpack("<i",raw)[0]
        if rt==2:
            r=f.read(28); typ,haslab,nmiss,pr,wr=struct.unpack("<5i",r[:20]); short=r[20:28].decode("latin1").rstrip(" \x00")
            label=""
            if haslab:
                L=struct.unpack("<i",f.read(4))[0]; label=f.read(L).decode("utf-8","replace"); f.read((-L)%4)
            miss=[f.read(8) for _ in range(abs(nmiss))]
            vars.append({"dict_index":len(vars)+1,"short":short,"type":typ,"label":label,"nmiss":nmiss,"missing_raw":miss})
        elif rt==3:
            cnt=struct.unpack("<i",f.read(4))[0]; ents=[]
            for _ in range(cnt):
                value=f.read(8); L=f.read(1)[0]; label=f.read(L).decode("utf-8","replace"); f.read((-(1+L))%8); ents.append((value,label))
            if struct.unpack("<i",f.read(4))[0] != 4: raise RuntimeError("value-label variable record")
            nv=struct.unpack("<i",f.read(4))[0]; idx=list(struct.unpack("<"+"i"*nv,f.read(4*nv))); vlraw.append((idx,ents))
        elif rt==6:
            n=struct.unpack("<i",f.read(4))[0]; f.read(n*80)
        elif rt==7:
            subtype,size,count=struct.unpack("<3i",f.read(12)); ext[subtype]=f.read(size*count)
        elif rt==999:
            f.read(4); data_pos=f.tell(); break
        else: raise RuntimeError(f"unknown record {rt}")
    longmap={}
    if 13 in ext:
        for pair in ext[13].decode("utf-8","replace").split("\t"):
            if "=" in pair:
                k,v=pair.split("=",1); longmap[k]=v
    for v in vars: v["name"]=longmap.get(v["short"],v["short"])
    labels={}
    for idxs,ents in vlraw:
        typ=vars[idxs[0]-1]["type"]; mp={}
        for raw,label in ents:
            value=struct.unpack("<d",raw)[0] if typ==0 else raw[:typ].decode("utf-8","replace").rstrip()
            mp[value]=label
        for idx in idxs: labels[vars[idx-1]["name"]]=mp
    if want is None: want=[v["name"] for v in vars]
    slot_name={i:v["name"] for i,v in enumerate(vars) if v["name"] in want}
    miss={}
    for i,v in enumerate(vars):
        if v["type"]==0 and v["missing_raw"]:
            miss[i]=set(struct.unpack("<"+"d"*len(v["missing_raw"]),b"".join(v["missing_raw"])))
        else: miss[i]=set()
    rows=[]; cur={}; slot=0; case=0
    while case<ncases:
        codes=f.read(8)
        if len(codes)<8: break
        raws=[f.read(8) for _ in range(sum(c==253 for c in codes))]; ri=0; eof=False
        for code in codes:
            if code==0: continue
            if code==252: eof=True; break
            v=vars[slot]
            if code==253:
                raw=raws[ri]; ri+=1; value=struct.unpack("<d",raw)[0] if v["type"]==0 else raw
            elif v["type"]==0:
                value=float("nan") if code in (254,255) else float(code)-bias
            else:
                value=b"        " if code==254 else None
            if slot in slot_name:
                if v["type"]==0 and value in miss[slot]: value=float("nan")
                cur[slot_name[slot]]=value
            slot += 1
            if slot==case_size:
                rows.append(cur); cur={}; slot=0; case+=1
                if case>=ncases: break
        if eof: break
    pos=f.tell(); size=path.stat().st_size
    if len(rows)!=ncases or slot!=0 or pos!=size:
        raise RuntimeError({"decoded":len(rows),"expected":ncases,"slot":slot,"position":pos,"size":size})
    df=pd.DataFrame(rows,columns=want)
    meta={"layout":layout,"case_size":case_size,"compression":compression,"weight_index":weight_index,"ncases":ncases,"bias":bias,"data_pos":data_pos, "file_end":pos, "file_size":size, "variable_count":len(vars), "variables":{v["name"]:{"dict_index":v["dict_index"],"short":v["short"],"type":v["type"],"label":v["label"],"value_labels":labels.get(v["name"],{})} for v in vars if v["name"] in want}}
    return df,meta
