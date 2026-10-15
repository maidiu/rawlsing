from pathlib import Path
import sys,os
R=Path(__file__).resolve().parents[1]
C=R/'runtime/can3/runtime/author/runtime_root/court_repaired'
S=C/'runtime_root/source';CAN=S/'WORKER_RETURNS/SOROK-R3-HQ300-CAN008-FIRST-POSITIVE-SOURCEFREE-R1'
sys.path[:0]=[str(S),str(CAN),str(CAN/'candidate'),str(CAN/'rsm_court_reproduction')]
os.environ.update(HQ300_STAGE=str(S),HQ298_STAGE=str(S))
