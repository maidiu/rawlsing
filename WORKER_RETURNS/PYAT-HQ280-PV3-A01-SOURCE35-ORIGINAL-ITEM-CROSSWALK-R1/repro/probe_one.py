#!/usr/bin/env python3
"""Probe exact nesting of the FIRST implementation record only (early-exit)."""
import ijson, re, sys
CW='/tmp/rawlsing_hq280_LR_A/02_ORIGINAL_ITEM_IDENTITY_CARRIER_CROSSWALK.json'
def items():
    with open(CW,'rb') as f:
        yield from ijson.items(f,'implementations.item')
n=0
paths=[]
for rec in items():
    n+=1
    def walk(prefix, obj):
        if isinstance(obj,dict):
            for k,v in obj.items():
                walk(f'{prefix}.{k}', v)
        elif isinstance(obj,list):
            paths.append(f'{prefix} [] len={len(obj)}')
            for i,v in enumerate(obj[:2]):
                walk(f'{prefix}[{i}]', v)
        else:
            paths.append(f'{prefix} = {str(obj)[:60]}')
    walk('impl', rec)
    if n>=1: break
print('records streamed:', n)
for p in paths: print(p)
