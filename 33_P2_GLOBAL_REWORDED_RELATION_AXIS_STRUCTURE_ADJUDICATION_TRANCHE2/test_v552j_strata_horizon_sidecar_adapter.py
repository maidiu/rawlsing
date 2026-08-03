#!/usr/bin/env python3
import pandas as pd
from v552j_strata_horizon_sidecar_adapter import enrich

p=pd.DataFrame([{"question_implementation_id":"q1","packet_id":"p1"},{"question_implementation_id":"q2","packet_id":"p2"}])
s=pd.DataFrame([{"question_implementation_id":"q1","stratum_id":"s1","horizon_type":"bounded"}])
o=enrich(p,s)
assert len(o)==2 and o.loc[0,"stratum_id"]=="s1" and pd.isna(o.loc[1,"stratum_id"])
try:
    enrich(p,pd.concat([s,s],ignore_index=True))
except ValueError as e:
    assert "duplicate" in str(e)
else:
    raise AssertionError("duplicate sidecar keys did not fail")
p2=p.copy();p2["stratum_id"]=["conflict",""]
try:
    enrich(p2,s)
except ValueError as e:
    assert "conflicting" in str(e)
else:
    raise AssertionError("conflict did not fail")
print("PASS: synthetic sidecar tests")
