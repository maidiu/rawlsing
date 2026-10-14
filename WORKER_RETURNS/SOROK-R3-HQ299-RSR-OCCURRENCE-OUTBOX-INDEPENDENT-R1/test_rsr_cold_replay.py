"""Fresh Python subprocess replay, explicitly measuring harness persistence."""
from pathlib import Path
import subprocess,sys,json

SCRIPT=Path(__file__).with_name('rsr_cold_replay.py')

def step(action,path,exit_status):
    p=subprocess.run([sys.executable,str(SCRIPT),action,str(path)],
                     capture_output=True,text=True,timeout=10,check=False)
    assert p.returncode==exit_status, (action,p.returncode,p.stderr,p.stdout)
    return p.stdout.strip()


def test_cold_commit_then_crash_then_recover_then_retry_delivery_and_ack(tmp_path):
    state=tmp_path/'state.json'
    step('prepare_committed',state,79)
    first=json.loads(step('recover_committed',state,0))
    assert first=={'status':'RECOVERED_COMMITTED','events':1,'delivery':'DELIVERED_UNACKED','perceived':False}
    second=json.loads(step('recover_after_delivery',state,0))
    assert second=={'status':'ACK_WITHOUT_PERCEPTION_CLAIM','events':1,'state':'ACKNOWLEDGED'}


def test_cold_crash_after_in_memory_admit_without_harness_persist_loses_event(tmp_path):
    state=tmp_path/'state.json'
    step('prepare_unpersisted',state,79)
    result=json.loads(step('recover_unpersisted',state,0))
    assert result=={'status':'UNPERSISTED_ADMIT_LOST','events':0,'outbox':0}
