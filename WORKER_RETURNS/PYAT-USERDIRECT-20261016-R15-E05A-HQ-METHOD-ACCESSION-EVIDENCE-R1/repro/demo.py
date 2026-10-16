"""JSON request -> real accepted machinery -> receipt, consumer values, rendering."""
from bootstrap import ROOT,RT
import argparse,json,pathlib
from handoff import fixture_handoff,render_markdown
p=argparse.ArgumentParser();p.add_argument('--request',required=True);p.add_argument('--output');p.add_argument('--scalar-only',action='store_true');args=p.parse_args()
rows=json.loads((RT/'WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json').read_text())['fields']
packet=fixture_handoff(rows).execute(json.loads(pathlib.Path(args.request).read_text()),consumer_mode='SCALAR_ONLY' if args.scalar_only else 'BOTH_ORIGINAL_CLIENTS')
if args.output:
 dest=pathlib.Path(args.output).resolve()
 if not dest.is_relative_to(ROOT):raise ValueError('COMMISSIONED_RETURN_OUTPUT_ONLY')
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(packet,indent=2)+'\n');dest.with_suffix('.md').write_text(render_markdown(packet))
else:print(json.dumps(packet,indent=2))
