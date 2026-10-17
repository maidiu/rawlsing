"""Read-only P1 test-only CLI; consumes fabricated fixture JSON, emits no owner writes."""
import argparse, json
from pathlib import Path
from p1_contract import evaluate, select_test_only

def main():
    ap=argparse.ArgumentParser(description='P1 source-free proposal and alternative court')
    ap.add_argument('--context',default='fixtures/context_base.json')
    ap.add_argument('--packet',default='fixtures/packet_base.json')
    ap.add_argument('--policy',default='fixtures/policy_design_weights.json')
    ap.add_argument('--seed',default='0f'*32)
    ap.add_argument('--coordinate',type=int,default=0)
    a=ap.parse_args()
    ctx=json.loads(Path(a.context).read_text())
    packet=json.loads(Path(a.packet).read_text())
    policy=json.loads(Path(a.policy).read_text())
    result=evaluate(packet,ctx)
    selection=select_test_only(result,policy,seed_hex=a.seed,coordinate=a.coordinate)
    print(json.dumps({'evaluation':result,'selection':selection},indent=2,sort_keys=True))

if __name__=='__main__':main()
