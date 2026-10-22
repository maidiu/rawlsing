"""Frozen consumer oracle: actual enacted inspection exhausts the shared tool;
omission preserves it. E must therefore refuse/accept material help respectively.
No expected result is selected from the candidate's generated speech.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from joined.session import JoinedSession


def test_material_source_reaches_expression_consumer(tmp_path):
    results = {}
    for perform in ('e2', 'omit'):
        session = JoinedSession.start(tmp_path/perform, perform=perform)
        try:
            assert session.product.source['b_performed'] is True
            assert session.product._world(session.branch_id).actor_state['A']['tools_remaining'] == (0 if perform == 'e2' else 1)
            result = session.do_help()
            results[perform] = result['accepted']
            assert session.verify()['ok'] is True
        finally:
            session.close()
    assert results == {'e2': False, 'omit': True}


def test_fresh_process_reopens_same_material_person(tmp_path):
    import json
    import subprocess
    session = JoinedSession.start(tmp_path/'cold', perform='omit')
    product_root = str(session.product.root)
    source = session.product.source
    session.close()
    code = """import json,sys
from joined.session import JoinedSession
s=JoinedSession.open(sys.argv[1])
try:
 print(json.dumps({'root':str(s.product.root),'source':s.product.source,
                   'accepted':s.do_help()['accepted'],'verify':s.verify()['ok']}))
finally:s.close()
"""
    import os
    env = {**os.environ, 'PYTHONPATH': str(Path(__file__).resolve().parents[1]),
           'PYTHONDONTWRITEBYTECODE': '1'}
    run = subprocess.run([sys.executable, '-B', '-c', code, str(tmp_path/'cold')],
                         env=env, text=True, capture_output=True, timeout=60)
    assert run.returncode == 0, run.stderr
    observed = json.loads(run.stdout)
    assert observed == {'root':product_root,'source':source,'accepted':True,'verify':True}
