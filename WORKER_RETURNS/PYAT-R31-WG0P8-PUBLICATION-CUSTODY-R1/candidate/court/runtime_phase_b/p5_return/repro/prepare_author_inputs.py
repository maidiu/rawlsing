"""File-location transport only: fresh native baseline for the frozen J numeric script."""
import pathlib,sys,runpy,shutil
R=pathlib.Path(__file__).resolve().parents[1];C=R/'review/runtime_phase_b/candidate'
sys.path[:0]=[str(C/'repro'),str(C/'pinned')]
import common_v1
sys.modules['common']=common_v1;sys.modules['wg0p2_workload']=common_v1.w
runpy.run_path(str(C/'pinned/predecessors/j/repro/probe.py'),run_name='__main__')
dest=C/'pinned/predecessors/j/observations';dest.mkdir(parents=True,exist_ok=True)
shutil.copyfile(C/'observations/baseline.json',dest/'baseline.json')
print('FRESH_NATIVE_BASELINE_TRANSPORTED_TO_FROZEN_NUMERIC_READER_PATH')
