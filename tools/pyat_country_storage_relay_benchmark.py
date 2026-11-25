"""Same-host sourcefree storage comparisons, no original survey data.
Historical production modules loaded from immutable git objects; current
carrier builds one identical on-disk artifact opened by all three variants.
Timing is separate from tracemalloc (Python allocation peak, not tree RSS).
"""
import dataclasses
import gc
import hashlib
import importlib
import json
import statistics
import subprocess
import sys
import tempfile
import time
import tracemalloc
import types
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pyreadstat
from rawlsing_next import pre553_country_numeric_carrier as carrier
from rawlsing_next import pre553_physical_decoder as decoder
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec, canonical_json

PARENT = "f5e9c9a03ccddb5bdfab2114c5f5f551002914f6"
B = "9e8572463f731fb1c3c9da1501bec48c80ad6143"
A = "d988a39f7741a839e89ac37bf13f5acfe1c2936a"


def historical(sha, name):
    path = "rawlsing_next/" + name + ".py"
    body = subprocess.check_output(["git","show",sha+":"+path])
    module_name = "rawlsing_next._relay_" + sha[:8] + "_" + name
    mod = types.ModuleType(module_name)
    mod.__package__ = "rawlsing_next"
    mod.__file__ = str(Path.cwd()/path)
    sys.modules[module_name] = mod
    exec(compile(body,sha+":"+path,"exec"),mod.__dict__)
    return mod


def measure(variants, repetitions=3):
    outputs = {}
    elapsed = {name: [] for name in variants}
    names = tuple(variants)
    # Rotate order to avoid attributing a single warmup to one implementation.
    for repeat in range(repetitions):
        order = names[repeat % len(names):] + names[:repeat % len(names)]
        for name in order:
            gc.collect()
            start=time.perf_counter()
            result=variants[name]()
            elapsed[name].append(time.perf_counter()-start)
            if name in outputs:
                assert result==outputs[name], (name,"within-version drift")
            outputs[name]=result
    assert len(set(outputs.values()))==1, outputs
    peaks={}
    for name,fn in variants.items():
        gc.collect()
        tracemalloc.start()
        try:
            assert fn()==outputs[name]
            _,peaks[name]=tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
    return {name:{"median_seconds":statistics.median(elapsed[name]),
                  "samples_seconds":elapsed[name],
                  "python_peak_allocated_bytes":peaks[name]} for name in variants}


def main():
    old_decoder=historical(PARENT,"pre553_physical_decoder")
    b_decoder=historical(B,"pre553_physical_decoder")
    old_carrier=historical(PARENT,"pre553_country_numeric_carrier")
    b_carrier=historical(B,"pre553_country_numeric_carrier")
    codec=R5TypedValueCodec()
    a_carrier=historical(A,"pre553_country_numeric_carrier")
    # A and B-R3 use identical decoder source; keep the inherited comparator
    # and compare A vs R3 for actual authenticated cold reading.
    ds={"parent":old_decoder,"B":b_decoder,"A":decoder}
    cs={"parent":old_carrier,"B":b_carrier,"A":a_carrier,"B_R3":carrier}
    n,p=3072,193
    values=np.arange(n,dtype=np.float64)
    frame=pd.DataFrame({"v"+str(i): (values+i)%7 if i%2==0
                       else (values*1.000001+i/13) for i in range(p-1)})
    frame.insert(23,"country",np.where(np.arange(n)%2==0,1.,2.))
    frame.loc[0,"country"]=float("nan")
    with tempfile.TemporaryDirectory() as d:
        root=Path(d)
        for ext,writer in (("sav",pyreadstat.write_sav),("dta",pyreadstat.write_dta)):
            src=root/("source."+ext)
            writer(frame,str(src))
            sha=hashlib.sha256(src.read_bytes()).hexdigest()
            def selected(mod):
                method=getattr(mod,"decode_"+ext)
                # Fresh content-bound incidence for every timed invocation.
                with method(src,expected_source_sha256=sha) as inc:
                    h=hashlib.sha256()
                    count=0
                    for c in inc.iter_native_column("country"):
                        count+=1
                        h.update(canonical_json(codec.encode((c.row_ordinal,c.variable_ordinal,
                            c.variable_name,c.raw_value,c.missing_state.value,
                            c.source_missing_declaration,c.raw_value_label))).encode("ascii"))
                    assert count==n
                    return h.hexdigest()
            result=measure({name:lambda mod=mod:selected(mod) for name,mod in ds.items()})
            print("RELAY_SELECTED_DECODER",json.dumps({"format":ext,"rows":n,"width":p,
                  "source_bytes":src.stat().st_size,"measurements":result}),flush=True)
        src=root/"source.sav"
        sha=hashlib.sha256(src.read_bytes()).hexdigest()
        path=root/"country.sqlite"
        with decoder.decode_sav(src,expected_source_sha256=sha) as inc:
            receipt=carrier.build_country(inc,country_variable="country",country_value=1.,
                        output=path,require_current=lambda:True,block_rows=16)
        def opening(mod):
            rec=mod.CountryReceipt(**dataclasses.asdict(receipt))
            with mod.CountryReader(path,rec,require_current=lambda:True) as reader:
                # Same exact file, externally pinned receipt and selected query.
                return (tuple(reader.matching_rows({"v0":0.})),len(reader._lane_auth))
        result=measure({name:lambda mod=mod:opening(mod) for name,mod in cs.items()},repetitions=4)
        with carrier.CountryReader(path,receipt,require_current=lambda:True) as read:
            lanes=len(read._lane_auth)
        print("RELAY_COLD_INVENTORY",json.dumps({"country_rows":receipt.country_rows,
              "width":p,"lanes":lanes,"bytes":receipt.bytes,"measurements":result}),flush=True)
    # Inventory hash isolated from SQLite and caller allocations. The input is
    # shared identically before tracing begins; only temporary allocations count.
    v=tuple((j,"é"+str(j)) for j in range(300))
    b=tuple((i,16,hashlib.sha256(str(i).encode()).digest()) for i in range(256))
    l=tuple((i,j,hashlib.sha256(f"{i}:{j}".encode()).digest())
            for i in range(256) for j in range(300))
    result=measure({name:lambda mod=mod:mod._manifest_root(v,b,l)
                    for name,mod in cs.items()},repetitions=4)
    print("RELAY_MANIFEST_HASH",json.dumps({"lanes":len(l),"measurements":result}),flush=True)


if __name__=="__main__":
    main()
