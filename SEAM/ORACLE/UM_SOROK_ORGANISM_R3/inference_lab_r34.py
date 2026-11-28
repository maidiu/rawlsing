"""R20: intake the existing executed R34 owner course, without rescripting life.

Only the F (unprojected) course is captured. P/Lbad remain owner experiments,
not approved live projections. The original CourseWire still executes its
hermetic policy/transport and retains its own assertions and receipts.
"""
from contextlib import nullcontext
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

from um_sorok_organism import runtime as runtime_module
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider
from um_sorok_organism.types import copy, digest
from um_sorok_organism.inference_lab import WorkloadCapture, ExactTapeProvider, verify_workload
from um_sorok_organism.inference_lab_admission import AdmissionCapture

FIXTURE="R34_ACQUIRED_LIFE_F"


def _owner():
    directory=Path(__file__).resolve().parents[2]/"NEIGHBORMULCH"
    if str(directory) not in sys.path:sys.path.insert(0,str(directory))
    import constitutive_life_campaign as owner
    if Path(owner.__file__).resolve()!=directory/"constitutive_life_campaign.py":
        raise ValueError("LAB_R34_OWNER_IMPORT_MISMATCH")
    return owner


def _course(wrap,*,observer=None):
    owner=_owner();original=owner.CourseWire.propose;admit=runtime_module.admit
    def call(wire,task,packet):
        if wire.arm!="F":raise ValueError("LAB_R34_FULL_COURSE_ONLY")
        # Preserve the actual owner wire/callback; the lab sees original input,
        # before transport compilation. No replacement policy is introduced.
        provider=CallbackLLMProvider(lambda t,p:original(wire,t,p))
        return wrap(provider,task,packet)
    def observe(*args,**kwargs):return observer.invoke(admit,*args,**kwargs)
    context=patch.object(runtime_module,"admit",side_effect=observe) if observer else nullcontext()
    with tempfile.TemporaryDirectory(prefix="lab_r34_") as tmp:
        db=Path(tmp)/"life.sqlite"
        with context,patch.object(owner.CourseWire,"propose",call):
            course=owner.run_course(db,"F")
        rt=ConstitutiveRuntime(db)
        try:
            final={"world":rt.ledger.world("w1")[1],"actors":rt.ledger.actors(),
                   "events":rt.ledger.events(),"verification":rt.verify()}
            if not final["verification"]["valid"] or digest(final)!=course["state_digest"]:
                raise ValueError("LAB_R34_COLD_STATE_MISMATCH")
            return {**final,"course":course}
        finally:rt.close()


def capture_r34(head,*,with_admissions=False):
    cap=WorkloadCapture(source_head=head,fixture=FIXTURE,sourcefree_fixture_attested=True)
    observer=AdmissionCapture(cap) if with_admissions else None
    state=_course(cap.invoke,observer=observer)
    doc=cap.document(owner_state_sha256=digest(state))
    if observer:return doc,state,observer.document(doc,state)
    return doc,state


def replay_r34(doc,head):
    p=verify_workload(doc,source_head=head)
    if p["fixture"]!=FIXTURE:raise ValueError("LAB_R34_FIXTURE_MISMATCH")
    tape=ExactTapeProvider(doc,source_head=head,original_grade="SOURCEFREE_R34_OWNER_WIRE")
    def wrap(provider,task,packet):
        recorded=tape.propose(task,packet)
        # Required original owner fixture observations, not callback-free replay.
        actual=provider.propose(task,copy(packet))
        if actual!=recorded:raise ValueError("LAB_R34_OWNER_DECISION_MISMATCH")
        return recorded
    state=_course(wrap);tape.finish()
    if digest(state)!=p["owner_state_sha256"]:
        raise ValueError("LAB_R34_REPLAY_MISMATCH")
    return state
