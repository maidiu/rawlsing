#!/usr/bin/env python3
"""Streaming structural probe of the LR-A 423MB crosswalk (memory-bounded, ijson)."""
import ijson, json, sys, collections

CW = '/tmp/rawlsing_hq280_LR_A/02_ORIGINAL_ITEM_IDENTITY_CARRIER_CROSSWALK.json'

def main():
    top_keys, impl_fields, carriers_seen = [], collections.Counter(), collections.Counter()
    sample_impl = None
    n = 0
    with open(CW, 'rb') as f:
        for prefix, event, value in ijson.parse(f, use_float=True):
            top_keys.append(prefix) if event == 'map_key' and not prefix.startswith('implementations') else None
            if prefix == 'implementations.item' and event == 'start_map':
                n += 1
                if sample_impl is None:
                    sample_impl = {}
                continue
            if prefix.startswith('implementations.item.') and event in ('string','number','boolean','null'):
                key = prefix.split('.')[-1]
                impl_fields[key] += 1
                if sample_impl is not None and len(sample_impl) < 60:
                    sample_impl[key] = value
    print('top-level map keys seen:', sorted(set(k for k in top_keys if k)))
    print('implementations streamed:', n)
    print('distinct per-impl fields:', len(impl_fields))
    for k, c in impl_fields.most_common(40):
        print('   ', k, c)
    print()
    print('sample implementation (first values):')
    print(json.dumps(sample_impl, indent=1, default=str)[:2500])

main()
