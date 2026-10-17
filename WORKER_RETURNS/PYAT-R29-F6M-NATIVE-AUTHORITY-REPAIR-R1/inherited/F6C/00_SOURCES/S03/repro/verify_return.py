"""Verify delivered file identities and deterministic source-free replay."""
from pathlib import Path
import sys
import json
import hashlib

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from rawlsing_next.pre553_heterogeneous_synthesis import synthesize, conditional
from rawlsing_next.pre553_empirical_objects import semantic_hash

RETURN = Path(__file__).resolve().parents[1]


def main():
    manifest=json.loads((RETURN/'ARTIFACT_MANIFEST.json').read_text())
    for record in manifest['files']:
        data=(ROOT/record['path']).read_bytes()
        assert len(data)==record['bytes'],record['path']
        assert hashlib.sha256(data).hexdigest()==record['sha256'],record['path']
    b=json.loads((RETURN/'SYNTHETIC_WORLD_BUNDLE.json').read_text())
    assert synthesize(**b['replay'])==b
    assert semantic_hash({k:v for k,v in b.items() if k!='content_hash'})==b['content_hash']
    forbidden={'actor_state','personality','biography','childhood_history','parent','coparent','person_id'}
    def inspect(value):
        if isinstance(value,dict):
            assert not (set(value)&forbidden)
            for v in value.values(): inspect(v)
        elif isinstance(value,list):
            for v in value: inspect(v)
    inspect(b)
    assert b['test_origin'] is True
    receipts=json.loads((RETURN/'CONTRIBUTION_VALUE_RECEIPTS.json').read_text())
    receipt=conditional(b,{'material_security':'secure'},'employment_position')
    assert receipt==receipts['A_B_equal']['consumer_receipt']
    assert len({receipts[k]['consumer_receipt']['probabilities']['formal'] for k in ['A_only','A_B_equal','A_triple_B']})==3
    print(f"Verified {len(manifest['files'])} file identities, source-free replay and value-reading receipts; no real-source qualification.")


if __name__=='__main__': main()
