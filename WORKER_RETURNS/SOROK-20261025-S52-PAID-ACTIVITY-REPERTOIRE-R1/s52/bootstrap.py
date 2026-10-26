"""Install S52 over the accepted S51/S49 and actual G18 sources."""
from __future__ import annotations
import sys
from pathlib import Path
RETURN=Path(__file__).resolve().parents[1]
REPO=RETURN.parents[1]
S51=REPO/"WORKER_RETURNS"/"SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1"
S49=REPO/"WORKER_RETURNS"/"SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1"
G18=Path("/Users/matthewsmith/Desktop/Rawlsing/rawlsing-r31j/WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1/candidate/vendor/bp2/vendor/g18")
CUTS={"s51":"2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65","s49":"6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43"}
_INSTALLED=False
def install():
 global _INSTALLED
 if _INSTALLED:return
 for p in (str(RETURN),str(S51),str(S49),str(G18)):
  if p in sys.path:sys.path.remove(p)
  sys.path.insert(0,p)
 from s51.bootstrap import install as s51_install
 s51_install()
 import s51  # noqa
 import lab_sgi1.history  # noqa
 _INSTALLED=True
def roots():
 install()
 return {"s52_return":str(RETURN),"s51_return":str(S51),"s49_return":str(S49),"g18_source":str(G18),"cuts":dict(CUTS)}
__all__=["CUTS","G18","RETURN","S49","S51","install","roots"]
