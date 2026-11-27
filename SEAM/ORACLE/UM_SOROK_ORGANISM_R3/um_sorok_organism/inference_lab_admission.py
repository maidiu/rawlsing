"""Local exact owner-admission court for captured developmental workloads.

The existing development.admit function remains the only admission authority.
No world write, new actor state owner, remote witness disclosure, or claim that
acceptance establishes human psychological adequacy. Scratch results are not
committed life. The real continuing owner course supplies all baseline facts.
"""
from collections import Counter
from time import perf_counter_ns

from .types import canonical, copy, digest
from .development import admit, InvalidDevelopment
from .inference_lab import verify_workload, size, MAX_TAPE_BYTES, _local_read, _local_write

SCHEMA="RAWLSING_LOCAL_ADMISSION_WITNESSES_V1"


def _candidates(proposal,issued_trial):
    if type(proposal) is not dict or type(proposal.get("candidates")) is not list:
        raise ValueError("LAB_INVALID_DEVELOPMENT_PROPOSAL")
    candidates=copy(proposal["candidates"])
    if issued_trial is not None:
        # Exact existing runtime assembly: actual trial recording is not
        # optional semantic narration. Duplicate/forged model records refuse.
        candidates.insert(0,{"kind":"RECORD_POSSIBLE_END_TRIAL","trial":copy(issued_trial)})
    return candidates


class AdmissionCapture:
    """Optional fixture-local observation of the actual runtime.admit call."""
    def __init__(self,capture,*,max_bytes=64*1024*1024):
        if type(max_bytes) is not int or not 1<=max_bytes<MAX_TAPE_BYTES:
            raise ValueError("LAB_ADMISSION_WITNESS_CAP")
        self.capture=capture;self.rows=[];self.seqs=set()
        self.max_bytes=max_bytes;self.bytes=0;self.failed=False

    def invoke(self,owner,actor,experience,event_ref,candidates,*,issued_trial=None):
        if self.failed:raise ValueError("LAB_ADMISSION_CAPTURE_INCOMPLETE")
        if not self.capture.rows:raise ValueError("LAB_ADMISSION_WITHOUT_SEMANTIC_CALL")
        r=self.capture.rows[-1];p=r["packet"]
        if (r["task"]!="development" or r["seq"] in self.seqs
                or p.get("actor",{}).get("id")!=actor.get("id")
                or p.get("experience")!=experience
                or p.get("historical_psychodynamic_context",{}).get("objective_event_ref")!=event_ref
                or _candidates(r["proposal"],issued_trial)!=candidates):
            self.failed=True
            raise ValueError("LAB_ADMISSION_SOURCE_MISMATCH")
        rec={"seq":r["seq"],"actor_before":copy(actor),"event_ref":event_ref,
             "experience_digest":digest(experience),"issued_trial":copy(issued_trial),
             "packet_digest":r["packet_digest"]}
        if self.bytes+size(rec)>self.max_bytes:
            self.failed=True
            raise ValueError("LAB_ADMISSION_WITNESS_CAP")
        start=perf_counter_ns()
        try:
            effects=owner(actor,experience,event_ref,candidates,issued_trial=issued_trial)
            rec["owner_elapsed_ns"]=perf_counter_ns()-start
            rec["actor_after_digest"]=digest(actor);rec["effects"]=copy(effects)
            n=size(rec)+1
            if self.bytes+n>self.max_bytes:raise ValueError("LAB_ADMISSION_WITNESS_CAP")
        except Exception:
            self.failed=True
            raise
        self.seqs.add(r["seq"]);self.rows.append(rec);self.bytes+=n
        return effects

    def document(self,workload,state):
        p=verify_workload(workload)
        if self.failed or p["owner_state_sha256"]!=digest(state):
            raise ValueError("LAB_ADMISSION_CAPTURE_INCOMPLETE")
        expected={r["seq"] for r in p["rows"] if r["task"]=="development"}
        if self.seqs!=expected:raise ValueError("LAB_ADMISSION_WITNESS_COVERAGE")
        events={}
        for row in state["events"]:
            env=row["envelope"]
            if env["kind"]=="ACTOR_LIFE_TRANSITION":
                event=env["payload"]["objective_ref"]
                if event in events:raise ValueError("LAB_DUPLICATE_COMMITTED_EVENT")
                events[event]=row
        rows=copy(self.rows)
        for w in rows:
            e=events[w["event_ref"]];env=e["envelope"];aid=w["actor_before"]["id"]
            if (env["payload"]["developmental_effects"][aid]!=w["effects"]
                    or env["actor_digests"][aid]!=w["actor_after_digest"]
                    or digest(env["payload"]["private_actor_experience_receipts"][aid])!=w["experience_digest"]):
                raise ValueError("LAB_ADMISSION_COMMITTED_STATE_MISMATCH")
            w["committed_event_id"]=e["id"]
        payload={"schema":SCHEMA,"workload_sha256":workload["sha256"],
                 "source_head":p["source_head"],"owner_state_sha256":p["owner_state_sha256"],
                 "rows":rows}
        return {"payload":payload,"sha256":digest(payload)}


def verify_admissions(workload,document):
    p=verify_workload(workload)
    if type(document) is not dict or set(document)!={"payload","sha256"}:
        raise ValueError("LAB_ADMISSION_ENVELOPE")
    a=document["payload"]
    if (type(a) is not dict or set(a)!={"schema","workload_sha256","source_head",
                                      "owner_state_sha256","rows"}
            or a["schema"]!=SCHEMA or a["workload_sha256"]!=workload["sha256"]
            or a["source_head"]!=p["source_head"] or a["owner_state_sha256"]!=p["owner_state_sha256"]
            or digest(a)!=document["sha256"] or size(document)>MAX_TAPE_BYTES):
        raise ValueError("LAB_ADMISSION_INTEGRITY")
    expected={r["seq"] for r in p["rows"] if r["task"]=="development"}
    if type(a["rows"]) is not list:raise ValueError("LAB_ADMISSION_ROWS")
    found={}
    for w in a["rows"]:
        if (type(w) is not dict or set(w)!={"seq","actor_before","event_ref","experience_digest",
                 "issued_trial","packet_digest","owner_elapsed_ns","actor_after_digest","effects",
                 "committed_event_id"} or type(w["seq"]) is not int
                or w["seq"] not in expected or w["seq"] in found):
            raise ValueError("LAB_ADMISSION_WITNESS_COVERAGE")
        r=p["rows"][w["seq"]];packet=r["packet"]
        if (w["packet_digest"]!=r["packet_digest"]
                or w["actor_before"]["id"]!=packet["actor"]["id"]
                or w["event_ref"]!=packet["historical_psychodynamic_context"]["objective_event_ref"]
                or w["experience_digest"]!=digest(packet["experience"])):
            raise ValueError("LAB_ADMISSION_SOURCE_MISMATCH")
        # Reexecute the actual baseline through the original owner, no final
        # actor state used as input. A hash alone is not the reconstruction.
        actor=copy(w["actor_before"])
        effects=admit(actor,copy(packet["experience"]),w["event_ref"],
                      _candidates(r["proposal"],w["issued_trial"]),
                      issued_trial=copy(w["issued_trial"]))
        if effects!=w["effects"] or digest(actor)!=w["actor_after_digest"]:
            raise ValueError("LAB_ADMISSION_BASELINE_MISMATCH")
        found[w["seq"]]=copy(w)
    if set(found)!=expected:raise ValueError("LAB_ADMISSION_WITNESS_COVERAGE")
    return found


def evaluate_admissions(workload,document,comparison):
    """Evaluate returned development proposals only; do not rank or mutate life."""
    rows=verify_admissions(workload,document)
    if (comparison.get("workload_sha256")!=workload["sha256"]
            or comparison.get("source_head")!=workload["payload"]["source_head"]):
        raise ValueError("LAB_COMPARISON_SOURCE_MISMATCH")
    results=[];totals={}
    for item in comparison["observations"]:
        if item["task"]!="development":continue
        w=rows.get(item["seq"])
        if w is None or item["packet_digest"]!=w["packet_digest"]:
            raise ValueError("LAB_COMPARISON_PACKET_MISMATCH")
        if digest(item["proposal"])!=item["proposal_digest"]:
            raise ValueError("LAB_COMPARISON_PROPOSAL_MISMATCH")
        r=workload["payload"]["rows"][w["seq"]]
        actor=copy(w["actor_before"]);initial=digest(actor)
        start=perf_counter_ns();effects=None;err=None
        if item["outcome"]!="PROPOSAL_RETURNED":
            outcome="NO_PROPOSAL_TO_ADMIT"
        else:
            try:
                effects=admit(actor,copy(r["packet"]["experience"]),w["event_ref"],
                              _candidates(item["proposal"],w["issued_trial"]),
                              issued_trial=copy(w["issued_trial"]))
                outcome="OWNER_ACCEPTED_SCRATCH"
            except InvalidDevelopment:
                outcome="OWNER_REFUSED_SCRATCH"
            except Exception:
                outcome="OWNER_EVALUATION_ERROR"
        post=digest(actor)
        row={"seq":w["seq"],"arm":item["arm"],"outcome":outcome,
             "packet_digest":w["packet_digest"],"elapsed_ns":perf_counter_ns()-start,
             "effects":effects,"actor_after_digest":post,
             "actor_changed":initial!=post,
             "matches_recorded_admission":outcome=="OWNER_ACCEPTED_SCRATCH"
                  and post==w["actor_after_digest"] and effects==w["effects"],
             "refusal_mutated_scratch":outcome=="OWNER_REFUSED_SCRATCH" and post!=initial}
        results.append(row);totals.setdefault(item["arm"],Counter())[outcome]+=1
    return {"schema":"RAWLSING_SCRATCH_ADMISSION_COMPARISON_V1",
            "scope":"LOCAL_OWNER_ADMISSION_NOT_LIFE_CONTINUATION_OR_SCIENCE",
            "workload_sha256":workload["sha256"],"witness_sha256":document["sha256"],
            "observations":results,"totals":{k:dict(v) for k,v in totals.items()}}
