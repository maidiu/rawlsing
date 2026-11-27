"""Explicit local laboratory for existing semantic operations, not a psyche.

Private, sourcefree research only. A digest proves integrity against accidental
change, not provenance, authorization, or model adequacy. No network by default.
"""
from collections import Counter
from pathlib import Path
from time import perf_counter_ns
import json
import os
import re

from .types import canonical, copy, digest
from .live_psychological_llm import ExplicitJSONLLMProvider

SCHEMA="RAWLSING_SOURCEFREE_INFERENCE_WORKLOAD_V1"
GRADE="SOURCEFREE_FIXTURE_ONLY_NOT_EMPIRICAL"
TASKS=frozenset(("actor_attempt","development","expression","adult_constructor",
                 "blind_adult_interview","family_pathway_selection"))
MAX_PACKET_BYTES=128000
MAX_PROPOSAL_BYTES=256000
MAX_TAPE_BYTES=128*1024*1024


def size(value):
    return len(canonical(value).encode("utf-8"))


def _integer(v,lo,hi):
    if type(v) is not int or not lo<=v<=hi:
        raise ValueError("LAB_INVALID_INTEGER_LIMIT")
    return v


def _head(value):
    if type(value) is not str or not re.fullmatch("[0-9a-f]{40}",value):
        raise ValueError("LAB_EXACT_SOURCE_HEAD_REQUIRED")
    return value


def _local_write(path,value):
    """Exclusive private file, no overwrite or symlink-follow at destination."""
    raw=canonical(value).encode("utf-8")
    if len(raw)>MAX_TAPE_BYTES:raise ValueError("LAB_FILE_LIMIT")
    fd=os.open(Path(path),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,"wb") as out:
        out.write(raw);out.flush();os.fsync(out.fileno())


def _local_read(path):
    with open(path,"rb") as src:
        raw=src.read(MAX_TAPE_BYTES+1)
    if len(raw)>MAX_TAPE_BYTES:raise ValueError("LAB_FILE_LIMIT")
    result=json.loads(raw.decode("utf-8"))
    if canonical(result).encode("utf-8")!=raw:
        raise ValueError("LAB_NONCANONICAL_FILE")
    return result


class WorkloadCapture:
    """Explicit sourcefree local capture; no production logging or runtime change.

    The caller MUST own the fictional test fixture and verify source rights.
    Neither grade nor a hash is an authentication of source rights.
    """
    def __init__(self,*,source_head,fixture,sourcefree_fixture_attested=False,
                 max_rows=10000,max_bytes=64*1024*1024):
        if sourcefree_fixture_attested is not True:
            raise ValueError("LAB_SOURCEFREE_ATTESTATION_REQUIRED")
        if type(fixture) is not str or not re.fullmatch("[A-Za-z0-9_.-]{1,100}",fixture):
            raise ValueError("LAB_FIXTURE_ID_INVALID")
        self.meta={"schema":SCHEMA,"grade":GRADE,"source_head":_head(source_head),
                   "fixture":fixture}
        self.max_rows=_integer(max_rows,1,100000)
        self.max_bytes=_integer(max_bytes,1,MAX_TAPE_BYTES-65536)
        self.rows=[];self.bytes=0;self.failed=False

    def invoke(self,provider,task,packet):
        if self.failed:raise RuntimeError("LAB_CAPTURE_INCOMPLETE")
        if task not in TASKS or type(packet) is not dict:
            raise ValueError("LAB_INVALID_PACKET")
        frozen=copy(packet);n=size(frozen)
        if (n>MAX_PACKET_BYTES or len(self.rows)>=self.max_rows
                or self.bytes+n>self.max_bytes):
            self.failed=True
            raise ValueError("LAB_CAPTURE_CAP")
        # Snapshot before semantic work: a callback cannot rewrite its input.
        start=perf_counter_ns()
        try:
            answer=provider.propose(task,copy(frozen))
            if type(answer) is not dict or size(answer)>MAX_PROPOSAL_BYTES:
                raise ValueError("LAB_INVALID_PROPOSAL")
            if answer.get("task") not in (None,task):
                raise ValueError("LAB_TASK_MISMATCH")
            row={"seq":len(self.rows),"task":task,"packet":frozen,
                 "packet_digest":digest(frozen),"proposal":copy(answer),
                 "proposal_digest":digest(answer),
                 "elapsed_ns":perf_counter_ns()-start}
            row_bytes=size(row)+1
            if self.bytes+row_bytes>self.max_bytes:
                raise ValueError("LAB_CAPTURE_CAP")
        except Exception:
            self.failed=True
            raise
        self.rows.append(row);self.bytes+=row_bytes
        return copy(answer)

    def document(self):
        if self.failed or not self.rows:raise ValueError("LAB_CAPTURE_INCOMPLETE")
        payload={**self.meta,"rows":copy(self.rows)}
        return {"payload":payload,"sha256":digest(payload)}

    def save(self,path):
        _local_write(path,self.document())


class CaptureProvider:
    """Preserve the installed provider's grade and original operation."""
    def __init__(self,provider,capture):
        self.provider=provider;self.capture=capture
        self.grade=getattr(provider,"grade","UNSPECIFIED_SEMANTIC_ADAPTER_NO_PROVEN_GRADE")

    def propose(self,task,packet):
        return self.capture.invoke(self.provider,task,packet)


def verify_workload(doc,*,source_head=None):
    if type(doc) is not dict or set(doc)!={"payload","sha256"}:
        raise ValueError("LAB_WORKLOAD_ENVELOPE")
    p=doc["payload"]
    if type(p) is not dict or set(p)!={"schema","grade","source_head","fixture","rows"}:
        raise ValueError("LAB_WORKLOAD_SHAPE")
    if (p["schema"]!=SCHEMA or p["grade"]!=GRADE or digest(p)!=doc["sha256"]
            or size(doc)>MAX_TAPE_BYTES):
        raise ValueError("LAB_WORKLOAD_INTEGRITY")
    _head(p["source_head"])
    if source_head is not None and p["source_head"]!=_head(source_head):
        raise ValueError("LAB_SOURCE_HEAD_MISMATCH")
    if type(p["fixture"]) is not str or not re.fullmatch("[A-Za-z0-9_.-]{1,100}",p["fixture"]):
        raise ValueError("LAB_FIXTURE_ID_INVALID")
    rows=p["rows"]
    if type(rows) is not list or not 1<=len(rows)<=100000:
        raise ValueError("LAB_WORKLOAD_ROWS")
    for i,row in enumerate(rows):
        if (type(row) is not dict or set(row)!={"seq","task","packet","packet_digest",
                    "proposal","proposal_digest","elapsed_ns"} or type(row["seq"]) is not int
                or row["seq"]!=i or row["task"] not in TASKS
                or type(row["packet"]) is not dict or type(row["proposal"]) is not dict
                or row["proposal"].get("task") not in (None,row["task"])
                or digest(row["packet"])!=row["packet_digest"]
                or digest(row["proposal"])!=row["proposal_digest"]
                or size(row["packet"])>MAX_PACKET_BYTES
                or size(row["proposal"])>MAX_PROPOSAL_BYTES):
            raise ValueError("LAB_WORKLOAD_ROW_INTEGRITY")
        _integer(row["elapsed_ns"],0,10**20)
    return copy(p)


def load_workload(path,*,source_head=None):
    doc=_local_read(path)
    verify_workload(doc,source_head=source_head)
    return doc


class ExactTapeProvider:
    """Exact callback replay for actual owner continuation, NOT a history-only LLM.

    No output is reused if the current packet or operation differs. The replay
    has zero authority to adapt an old proposal to a new actor or occurrence.
    """
    def __init__(self,document,*,source_head,original_grade):
        self.rows=verify_workload(document,source_head=source_head)["rows"]
        self.index=0
        # Exact reproduction of the recorded provider's externally supplied
        # grade for hermetic state comparison; never claim a live model ran.
        self.grade=original_grade

    def propose(self,task,packet):
        if self.index>=len(self.rows):raise ValueError("LAB_TAPE_EXHAUSTED")
        row=self.rows[self.index]
        if task!=row["task"] or digest(packet)!=row["packet_digest"]:
            raise ValueError("LAB_TAPE_CONTEXT_MISMATCH")
        self.index+=1
        return copy(row["proposal"])

    def finish(self):
        if self.index!=len(self.rows):raise ValueError("LAB_TAPE_UNUSED_ROWS")


def selected_rows(document,*,per_task=1,tasks=None):
    """Deterministic first-N per task, independent of semantic answers."""
    _integer(per_task,1,10000)
    p=verify_workload(document)
    want=TASKS if tasks is None else frozenset(tasks)
    if not want or not want<=TASKS:raise ValueError("LAB_TASK_SELECTION")
    counts=Counter();out=[]
    for row in p["rows"]:
        t=row["task"]
        if t in want and counts[t]<per_task:
            counts[t]+=1;out.append(row)
    if not out:raise ValueError("LAB_EMPTY_SELECTION")
    return out


def compare_frozen(document,arms,*,per_task=1,tasks=None):
    """Matched frozen proposal workloads, not owner admission or life equivalence.

    No choice of winner, auto escalation, retry, or psychological rating.
    A provider exception remains an observed failure. A live budget stop
    propagates, so no further arm is attempted after an unknown spend.
    """
    rows=selected_rows(document,per_task=per_task,tasks=tasks)
    if type(arms) is not dict or not arms:raise ValueError("LAB_ARMS_REQUIRED")
    observations=[]
    for row in rows:
        for name,provider in arms.items():
            if type(name) is not str or not re.fullmatch("[A-Za-z0-9_.-]{1,80}",name):
                raise ValueError("LAB_ARM_ID_INVALID")
            prior=provider.usage_snapshot()["total"] if hasattr(provider,"usage_snapshot") else None
            start=perf_counter_ns()
            try:
                proposal=provider.propose(row["task"],copy(row["packet"]))
                if type(proposal) is not dict or size(proposal)>MAX_PROPOSAL_BYTES:
                    raise ValueError("LAB_INVALID_PROPOSAL")
                outcome="PROPOSAL_RETURNED"
            except BudgetStop:
                raise
            except Exception:
                proposal=None;outcome="REJECTED_OR_FAILED"
            metric=None
            if prior is not None:
                snap=provider.usage_snapshot()
                if snap["total"]==prior+1 and snap["receipts"]:
                    metric=snap["receipts"][-1]
                else:raise ValueError("LAB_PROVIDER_RECEIPT_MISSING")
            observations.append({"arm":name,"seq":row["seq"],"task":row["task"],
                  "packet_digest":row["packet_digest"],"outcome":outcome,
                  "proposal":copy(proposal),"proposal_digest":digest(proposal),
                  "equals_recorded_proposal":proposal==row["proposal"],
                  "elapsed_ns":perf_counter_ns()-start,"metric":metric})
    return {"schema":"RAWLSING_FROZEN_PROPOSAL_COMPARISON_V1",
            "workload_sha256":document["sha256"],
            "source_head":document["payload"]["source_head"],
            "scope":"PROPOSAL_ONLY_NOT_ADMITTED_DEVELOPMENT",
            "observations":observations,"totals":summarize(observations)}


def summarize(observations):
    """Retain missing usage as missing, never manufacture free calls."""
    groups={}
    for row in observations:
        key=row["arm"]+"/"+row["task"]
        t=groups.setdefault(key,{"calls":0,"proposal_returned":0,"attempts":0,
            "request_bytes":0,"elapsed_ns":0,"input_tokens":0,"output_tokens":0,
            "unknown_usage_calls":0,"unknown_request_bytes_calls":0})
        t["calls"]+=1;t["proposal_returned"]+=row["outcome"]=="PROPOSAL_RETURNED"
        t["elapsed_ns"]+=row["elapsed_ns"]
        m=row.get("metric") or {};t["attempts"]+=m.get("attempts",0)
        if type(m.get("request_bytes")) is int:t["request_bytes"]+=m["request_bytes"]
        else:t["unknown_request_bytes_calls"]+=1
        u=m.get("usage") or {}
        if type(u.get("input_tokens")) is int and type(u.get("output_tokens")) is int:
            t["input_tokens"]+=u["input_tokens"];t["output_tokens"]+=u["output_tokens"]
        else:t["unknown_usage_calls"]+=1
    for t in groups.values():
        if t["unknown_usage_calls"]:
            t["known_input_tokens"]=t.pop("input_tokens")
            t["known_output_tokens"]=t.pop("output_tokens")
            t["input_tokens"]=None;t["output_tokens"]=None
    return groups


class BudgetStop(RuntimeError):
    pass


class LiveBudget:
    """Single-process, single-use spend authorization with durable reservations.

    Currency in integer nanodollars; declared conservative ceiling/rate, not
    billing truth. Provider tokenization, hidden fees, price or cap violations
    can invalidate monetary assumptions. Never claim a guaranteed bill cap.
    No retry; failed/unknown transport consumes its reservation and stops.
    """
    def __init__(self,*,journal,max_calls,max_wire_bytes,input_token_ceiling,
                 completion_token_limit,input_nanos_per_token,output_nanos_per_token,
                 max_budget_nanos,sourcefree_live_authorized=False):
        if sourcefree_live_authorized is not True:
            raise ValueError("LAB_LIVE_AUTHORIZATION_REQUIRED")
        self.max_calls=_integer(max_calls,1,100000)
        self.max_wire_bytes=_integer(max_wire_bytes,1,10**12)
        self.input_ceiling=_integer(input_token_ceiling,1,10**7)
        self.output_limit=_integer(completion_token_limit,1,131072)
        self.input_rate=_integer(input_nanos_per_token,1,10**9)
        self.output_rate=_integer(output_nanos_per_token,1,10**9)
        self.max_budget=_integer(max_budget_nanos,1,10**15)
        self.reserve=self.input_ceiling*self.input_rate+self.output_limit*self.output_rate
        if self.reserve>self.max_budget:raise ValueError("LAB_BUDGET_BELOW_ONE_RESERVATION")
        self.calls=0;self.wire_bytes=0;self.reserved=0;self.estimated_reported=0
        self.stopped=False;self.pending=False
        self.path=Path(journal)
        _local_write(self.path,{"schema":"RAWLSING_LIVE_BUDGET_V1",
             "max_calls":self.max_calls,"max_wire_bytes":self.max_wire_bytes,
             "reserve_per_call_nanos":self.reserve,"max_budget_nanos":self.max_budget,
             "input_token_ceiling":self.input_ceiling,"completion_token_limit":self.output_limit,
             "input_nanos_per_token":self.input_rate,"output_nanos_per_token":self.output_rate,
             "billing_guarantee":False})
        # Journal is append-only in this single-process lab; no resume.
        self.log=Path(str(self.path)+".jsonl")
        fd=os.open(self.log,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        os.close(fd)

    def _append(self,row):
        with open(self.log,"ab") as f:
            f.write(canonical(row).encode("utf-8")+b"\n");f.flush();os.fsync(f.fileno())

    def begin(self,request):
        if self.stopped or self.pending:raise BudgetStop("LAB_LIVE_STOPPED")
        n=size(request)
        if (self.calls>=self.max_calls or self.wire_bytes+n>self.max_wire_bytes
                or self.reserved+self.reserve>self.max_budget):
            self.stopped=True
            raise BudgetStop("LAB_LIVE_BUDGET_EXHAUSTED")
        self.calls+=1;self.wire_bytes+=n;self.reserved+=self.reserve;self.pending=True
        self._append({"event":"RESERVED_BEFORE_SEND","attempt":self.calls,
                      "wire_bytes":n,"reserved_nanos":self.reserve,
                      "cumulative_reserved_nanos":self.reserved})

    def settle(self,usage):
        if not self.pending:raise BudgetStop("LAB_NO_PENDING_RESERVATION")
        a=usage.get("input_tokens");b=usage.get("output_tokens")
        if (type(a) is not int or type(b) is not int or a<0 or b<0
                or a>self.input_ceiling or b>self.output_limit):
            self.fail()
            raise BudgetStop("LAB_USAGE_UNKNOWN_OR_ABOVE_DECLARED_CEILING")
        self.pending=False
        estimated=a*self.input_rate+b*self.output_rate
        self.estimated_reported+=estimated
        self._append({"event":"USAGE_REPORTED","attempt":self.calls,"input_tokens":a,
                      "output_tokens":b,"declared_rate_estimate_nanos":estimated})
        # Retain the whole reservation, including unspent allowance, for
        # conservative authorization. Cached tokens receive no price discount.

    def fail(self):
        self.stopped=True
        if self.pending:
            self.pending=False
            self._append({"event":"UNCERTAIN_SPEND_STOP","attempt":self.calls})

    def snapshot(self):
        return {"attempts":self.calls,"wire_bytes":self.wire_bytes,
                "reserved_nanos":self.reserved,
                "reported_usage_rate_estimate_nanos":self.estimated_reported,
                "stopped":self.stopped,"pending":self.pending,"billing_guarantee":False}


class BudgetedLiveProvider(ExplicitJSONLLMProvider):
    """Reuse existing HTTPS implementation; cap before every actual request."""
    def __init__(self,*,budget,**kwargs):
        if not isinstance(budget,LiveBudget):raise TypeError("LAB_BUDGET_REQUIRED")
        if kwargs.get("transport") is not None:
            raise ValueError("LAB_LIVE_NO_TRANSPORT_OVERRIDE")
        if "completion_token_limit" in kwargs:
            raise ValueError("LAB_BUDGET_OWNS_COMPLETION_LIMIT")
        self.budget=budget
        super().__init__(completion_token_limit=budget.output_limit,**kwargs)

    def _request(self,payload):
        if payload.get(self.completion_limit_field)!=self.budget.output_limit:
            raise BudgetStop("LAB_OUTPUT_CAP_MISSING")
        self.budget.begin(payload)
        try:
            result=super()._request(payload)
            self.budget.settle(self._reported_usage(result))
            return result
        except Exception:
            self.budget.fail()
            raise BudgetStop("LAB_LIVE_TRANSPORT_OR_USAGE_FAILURE") from None


def save_report(path,report):
    _local_write(path,report)
