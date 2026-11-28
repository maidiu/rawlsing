"""Explicit local laboratory for existing semantic operations, not a psyche.

Private, sourcefree research only. A digest proves integrity against accidental
change, not provenance, authorization, or model adequacy. No network by default.
"""
from collections import Counter, deque
from pathlib import Path
from time import perf_counter_ns
from threading import Lock
import json
import os
import re

from .types import canonical, copy, digest
from .live_psychological_llm import ExplicitJSONLLMProvider

SCHEMA="RAWLSING_SOURCEFREE_INFERENCE_WORKLOAD_V1"
GRADE="SOURCEFREE_FIXTURE_ONLY_NOT_EMPIRICAL"
TASKS=frozenset(("actor_attempt","development","expression","adult_constructor",
                 "blind_adult_interview","family_pathway_selection"))
CHECKPOINT_TASK="developmental_checkpoint"
LIVE_TURN_TASK="live_conditional_turn"
CAPTURE_TASKS=TASKS|{CHECKPOINT_TASK,LIVE_TURN_TASK}


def _packet_limit(task):
    return 1024*1024 if task==CHECKPOINT_TASK else 512*1024 if task==LIVE_TURN_TASK else MAX_PACKET_BYTES


def _call_task(provider,task,packet):
    if task in (CHECKPOINT_TASK,LIVE_TURN_TASK) and callable(getattr(provider,"call",None)):
        return provider.call(packet)
    return provider.propose(task,packet)
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
        if task not in CAPTURE_TASKS or type(packet) is not dict:
            raise ValueError("LAB_INVALID_PACKET")
        frozen=copy(packet);n=size(frozen)
        if (n>_packet_limit(task) or len(self.rows)>=self.max_rows
                or self.bytes+n>self.max_bytes):
            self.failed=True
            raise ValueError("LAB_CAPTURE_CAP")
        # Snapshot before semantic work: a callback cannot rewrite its input.
        start=perf_counter_ns()
        try:
            answer=_call_task(provider,task,copy(frozen))
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

    def document(self,*,owner_state_sha256=None):
        if self.failed or not self.rows:raise ValueError("LAB_CAPTURE_INCOMPLETE")
        if owner_state_sha256 is not None and (type(owner_state_sha256) is not str
                or not re.fullmatch("[0-9a-f]{64}",owner_state_sha256)):
            raise ValueError("LAB_OWNER_STATE_DIGEST_INVALID")
        payload={**self.meta,"rows":copy(self.rows),"owner_state_sha256":owner_state_sha256}
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
    if type(p) is not dict or set(p)!={"schema","grade","source_head","fixture","rows","owner_state_sha256"}:
        raise ValueError("LAB_WORKLOAD_SHAPE")
    if (p["schema"]!=SCHEMA or p["grade"]!=GRADE or digest(p)!=doc["sha256"]
            or size(doc)>MAX_TAPE_BYTES):
        raise ValueError("LAB_WORKLOAD_INTEGRITY")
    _head(p["source_head"])
    state_sha=p["owner_state_sha256"]
    if state_sha is not None and (type(state_sha) is not str or not re.fullmatch("[0-9a-f]{64}",state_sha)):
        raise ValueError("LAB_OWNER_STATE_DIGEST_INVALID")
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
                or row["seq"]!=i or row["task"] not in CAPTURE_TASKS
                or type(row["packet"]) is not dict or type(row["proposal"]) is not dict
                or row["proposal"].get("task") not in (None,row["task"])
                or digest(row["packet"])!=row["packet_digest"]
                or digest(row["proposal"])!=row["proposal_digest"]
                or size(row["packet"])>_packet_limit(row["task"])
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
    if not want or not want<=CAPTURE_TASKS:raise ValueError("LAB_TASK_SELECTION")
    counts=Counter();out=[]
    for row in p["rows"]:
        t=row["task"]
        if t in want and counts[t]<per_task:
            counts[t]+=1;out.append(row)
    if not out:raise ValueError("LAB_EMPTY_SELECTION")
    return out


def compare_frozen(document,arms,*,per_task=1,tasks=None,sequence_ids=None,
                   rotate_arms=False,on_observation=None):
    """Matched frozen proposal workloads, not owner admission or life equivalence.

    No choice of winner, auto escalation, retry, or psychological rating.
    A provider exception remains an observed failure. A budget stop retains
    all completed observations and prevents any subsequent provider call.
    """
    if sequence_ids is None:
        rows=selected_rows(document,per_task=per_task,tasks=tasks)
    else:
        all_rows=verify_workload(document)["rows"]
        if (type(sequence_ids) is not list or not sequence_ids
                or any(type(i) is not int or not 0<=i<len(all_rows) for i in sequence_ids)
                or len(set(sequence_ids))!=len(sequence_ids)):
            raise ValueError("LAB_SEQUENCE_SELECTION")
        rows=[all_rows[i] for i in sequence_ids]
    if type(rotate_arms) is not bool or (on_observation is not None and not callable(on_observation)):
        raise ValueError("LAB_COMPARISON_OPTIONS")
    if type(arms) is not dict or not arms:raise ValueError("LAB_ARMS_REQUIRED")
    for name in arms:
        if type(name) is not str or not re.fullmatch("[A-Za-z0-9_.-]{1,80}",name):
            raise ValueError("LAB_ARM_ID_INVALID")
    observations=[];stopped=False
    order=list(arms)
    for i,row in enumerate(rows):
        if stopped:break
        shift=i%len(order) if rotate_arms else 0
        for name in order[shift:]+order[:shift]:
            provider=arms[name]
            prior=provider.usage_snapshot()["total"] if hasattr(provider,"usage_snapshot") else None
            start=perf_counter_ns()
            try:
                proposal=_call_task(provider,row["task"],copy(row["packet"]))
                if type(proposal) is not dict or size(proposal)>MAX_PROPOSAL_BYTES:
                    raise ValueError("LAB_INVALID_PROPOSAL")
                outcome="PROPOSAL_RETURNED"
            except BudgetStop:
                proposal=None;outcome="BUDGET_STOP";stopped=True
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
            if on_observation is not None:on_observation(copy(observations[-1]))
            if stopped:break
    return {"schema":"RAWLSING_FROZEN_PROPOSAL_COMPARISON_V1",
            "planned_observations":len(rows)*len(arms),
            "status":"STOPPED_BUDGET_OR_UNKNOWN_SPEND" if stopped else "COMPLETED",
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
                 max_budget_nanos,sourcefree_live_authorized=False,profiles=None):
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
        self._profiles={}
        if profiles is not None:
            if type(profiles) is not dict or not profiles or len(profiles)>32:
                raise ValueError("LAB_PROFILE_TABLE")
            for name,p in profiles.items():
                if (type(name) is not str or not re.fullmatch("[A-Za-z0-9_.-]{1,64}",name)
                        or name=="legacy" or type(p) is not dict or set(p)!={"model","endpoint",
                            "input_token_ceiling","completion_token_limit","input_nanos_per_token",
                            "output_nanos_per_token"} or type(p["model"]) is not str or not p["model"]
                        or type(p["endpoint"]) is not str or not p["endpoint"]):
                    raise ValueError("LAB_PROFILE_INVALID")
                a=_integer(p["input_token_ceiling"],1,10**7)
                b=_integer(p["completion_token_limit"],1,131072)
                c=_integer(p["input_nanos_per_token"],1,10**9)
                e=_integer(p["output_nanos_per_token"],1,10**9)
                if a*c+b*e>self.max_budget:raise ValueError("LAB_PROFILE_RESERVATION_TOO_LARGE")
                self._profiles[name]={"model":p["model"],"endpoint":p["endpoint"],
                    "input_ceiling":a,"output_limit":b,"input_rate":c,"output_rate":e,
                    "reserve":a*c+b*e}
        self.pending_profile=None
        self.calls=0;self.wire_bytes=0;self.reserved=0;self.estimated_reported=0
        self.stopped=False;self.pending=False
        # One shared allowance across historical and live providers in this process.
        # Reject overlap rather than racing or borrowing another call's reservation.
        self.dispatch_lock=Lock()
        self.path=Path(journal)
        _local_write(self.path,{"schema":"RAWLSING_LIVE_BUDGET_V1",
             "max_calls":self.max_calls,"max_wire_bytes":self.max_wire_bytes,
             "reserve_per_call_nanos":self.reserve,"max_budget_nanos":self.max_budget,
             "input_token_ceiling":self.input_ceiling,"completion_token_limit":self.output_limit,
             "input_nanos_per_token":self.input_rate,"output_nanos_per_token":self.output_rate,
             "billing_guarantee":False,**({"profiles":{k:{x:y for x,y in v.items() if x!="endpoint"}
                for k,v in self._profiles.items()}} if self._profiles else {})})
        # Journal is append-only in this single-process lab; no resume.
        self.log=Path(str(self.path)+".jsonl")
        fd=os.open(self.log,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        os.close(fd)

    def _append(self,row):
        with open(self.log,"ab") as f:
            f.write(canonical(row).encode("utf-8")+b"\n");f.flush();os.fsync(f.fileno())

    def profile(self,name):
        if name is None:
            # A heterogeneous allowance cannot silently fall back to legacy rates.
            if self._profiles:raise ValueError("LAB_NAMED_PROFILE_REQUIRED")
            return {"input_ceiling":self.input_ceiling,"output_limit":self.output_limit,
                    "input_rate":self.input_rate,"output_rate":self.output_rate,"reserve":self.reserve}
        if name not in self._profiles:raise ValueError("LAB_UNKNOWN_PROFILE")
        return copy(self._profiles[name])

    def begin(self,request,*,profile=None):
        p=self.profile(profile)
        if profile is not None and request.get("model")!=p["model"]:
            raise BudgetStop("LAB_PROFILE_MODEL_MISMATCH")
        if self.stopped or self.pending:raise BudgetStop("LAB_LIVE_STOPPED")
        n=size(request)
        if (self.calls>=self.max_calls or self.wire_bytes+n>self.max_wire_bytes
                or self.reserved+p["reserve"]>self.max_budget):
            self.stopped=True
            raise BudgetStop("LAB_LIVE_BUDGET_EXHAUSTED")
        self.calls+=1;self.wire_bytes+=n;self.reserved+=p["reserve"];self.pending=True
        self.pending_profile=profile
        self._append({"event":"RESERVED_BEFORE_SEND","attempt":self.calls,
                      "wire_bytes":n,"request_sha256":digest(request),"reserved_nanos":p["reserve"],
                      "budget_profile":profile,
                      "cumulative_reserved_nanos":self.reserved})

    def settle(self,usage):
        if not self.pending:raise BudgetStop("LAB_NO_PENDING_RESERVATION")
        p=self.profile(self.pending_profile)
        a=usage.get("input_tokens");b=usage.get("output_tokens")
        if (type(a) is not int or type(b) is not int or a<0 or b<0
                or a>p["input_ceiling"] or b>p["output_limit"]):
            self._append({"event":"USAGE_REJECTED","attempt":self.calls,"budget_profile":self.pending_profile,
                          "input_tokens":a if type(a) is int and a>=0 else None,
                          "output_tokens":b if type(b) is int and b>=0 else None})
            self.fail()
            raise BudgetStop("LAB_USAGE_UNKNOWN_OR_ABOVE_DECLARED_CEILING")
        self.pending=False
        profile=self.pending_profile;self.pending_profile=None
        estimated=a*p["input_rate"]+b*p["output_rate"]
        self.estimated_reported+=estimated
        self._append({"event":"USAGE_REPORTED","attempt":self.calls,"budget_profile":profile,"input_tokens":a,
                      "output_tokens":b,"declared_rate_estimate_nanos":estimated})
        # Retain the whole reservation, including unspent allowance, for
        # conservative authorization. Cached tokens receive no price discount.

    def fail(self):
        self.stopped=True
        if self.pending:
            self.pending=False
            self._append({"event":"UNCERTAIN_SPEND_STOP","attempt":self.calls,
                          "budget_profile":self.pending_profile})
            self.pending_profile=None

    def snapshot(self):
        return {"attempts":self.calls,"wire_bytes":self.wire_bytes,
                "reserved_nanos":self.reserved,
                "reported_usage_rate_estimate_nanos":self.estimated_reported,
                "stopped":self.stopped,"pending":self.pending,"billing_guarantee":False}


class _BudgetedWireMixin:
    """One existing LiveBudget for ordinary, historical and one-response live wire dispatch."""
    def __init__(self,*,budget,budget_profile=None,**kwargs):
        if not isinstance(budget,LiveBudget):raise TypeError("LAB_BUDGET_REQUIRED")
        if kwargs.get("transport") is not None:
            raise ValueError("LAB_LIVE_NO_TRANSPORT_OVERRIDE")
        if "completion_token_limit" in kwargs:
            raise ValueError("LAB_BUDGET_OWNS_COMPLETION_LIMIT")
        self.budget=budget;self.budget_profile=budget_profile
        p=budget.profile(budget_profile)
        if budget_profile is not None and (kwargs.get("model")!=p["model"]
                or kwargs.get("endpoint")!=p["endpoint"]):
            raise ValueError("LAB_PROFILE_PROVIDER_MISMATCH")
        super().__init__(completion_token_limit=p["output_limit"],**kwargs)

    def _dispatch_wire(self,payload,receipt):
        # Provider counters are not evidence of sending if a budget rejects
        # preflight. Bind this invocation to its own durable reservation.
        if not self.budget.dispatch_lock.acquire(blocking=False):
            if receipt is not None:receipt.update(attempts=0,budget_disposition="CONCURRENT_REFUSED")
            raise BudgetStop("LAB_SHARED_BUDGET_CONCURRENT_DISPATCH")
        before=self.budget.calls
        try:
            return super()._dispatch_wire(payload,receipt)
        finally:
            if receipt is not None:
                n=self.budget.calls-before
                receipt["attempts"]=n
                receipt["budget_profile"]=self.budget_profile
                receipt["budget_request_sha256"]=digest(payload) if n else None
                receipt["budget_attempt"]=self.budget.calls if n else None
                receipt["budget_disposition"]=("RESERVATION_UNCERTAIN" if n and self.budget.stopped else
                    "RESERVATION_SETTLED" if n else "PREFLIGHT_REFUSED")
            self.budget.dispatch_lock.release()

    def _request(self,payload):
        if payload.get(self.completion_limit_field)!=self.budget.profile(self.budget_profile)["output_limit"]:
            raise BudgetStop("LAB_OUTPUT_CAP_MISSING")
        self.budget.begin(payload,profile=self.budget_profile)
        try:
            result=super()._request(payload)
            self.budget.settle(self._reported_usage(result))
            return result
        except BaseException as exc:
            self.budget.fail()
            if not isinstance(exc,Exception):raise
            raise BudgetStop("LAB_LIVE_TRANSPORT_OR_USAGE_FAILURE") from None


class BudgetedLiveProvider(_BudgetedWireMixin,ExplicitJSONLLMProvider):
    """Existing isolated-task laboratory provider, unchanged external API."""


def budgeted_combined_provider(mode,*,budget,**kwargs):
    """Use the existing reservation for either actual combined inference ABI.

    Lazy import preserves the laboratory's older-owner overlay compatibility.
    No automatic network dispatch, retry, model choice or disclosure authority.
    Two instances may share one allowance; they remain different causal modes.
    """
    from .live_psychological_llm import (ExplicitDevelopmentalCheckpointProvider,
                                         ExplicitLiveTurnProvider)
    if mode=="HISTORICAL":base=ExplicitDevelopmentalCheckpointProvider
    elif mode=="LIVE":base=ExplicitLiveTurnProvider
    else:raise ValueError("LAB_COMBINED_PROVIDER_MODE")
    class CombinedBudgetedProvider(_BudgetedWireMixin,base):
        pass
    return CombinedBudgetedProvider(budget=budget,**kwargs)



class CombinedCaptureProvider:
    """Capture real combined owner requests with the existing private tape.
    No additional invocation, projection, or owner mutation.
    """
    def __init__(self,provider,capture,mode):
        if mode not in ("HISTORICAL","LIVE"):raise ValueError("LAB_COMBINED_PROVIDER_MODE")
        self.provider=provider;self.capture=capture
        self.task=CHECKPOINT_TASK if mode=="HISTORICAL" else LIVE_TURN_TASK
        self.grade=getattr(provider,"grade","UNSPECIFIED_SEMANTIC_ADAPTER_NO_PROVEN_GRADE")

    def call(self,request):
        return self.capture.invoke(self.provider,self.task,request)



# A whole-request structural demand envelope, not a measure of inner life.
# Known map containers are normalized by value shape, but new field families
# elsewhere remain visible. No text, actor names or latent values are retained.
_DEMAND_MAP_FIELDS=frozenset(("actor_contexts","peer_tips","conditional_family_sources_analyst_only"))
_DEMAND_AXES=("packet_bytes","nodes","max_depth","max_list","max_map","text_bytes","max_text")
_DEMAND_SCHEMA="RAWLSING_COMBINED_DEMAND_ENVELOPE_R61_V1"


def combined_demand(mode,request):
    if mode=="HISTORICAL":
        if type(request) is not dict or set(request)!={"mode","context","previous"} or request["mode"] not in ("BOOTSTRAP","ORDINARY","TERMINAL"):
            raise ValueError("LAB_DEMAND_REQUEST")
        stage=request["mode"];limit=_packet_limit(CHECKPOINT_TASK)
    elif mode=="LIVE":
        if type(request) is not dict or set(request)!={"grade","source","principal","principal_packet","peer_tips"}:
            raise ValueError("LAB_DEMAND_REQUEST")
        stage="LIVE";limit=_packet_limit(LIVE_TURN_TASK)
    else:raise ValueError("LAB_COMBINED_PROVIDER_MODE")
    n=size(request)
    if n>limit:raise ValueError("LAB_DEMAND_SIZE")
    axes=dict.fromkeys(_DEMAND_AXES,0);axes["packet_bytes"]=n
    def visit(value,depth=0,field=None):
        axes["nodes"]+=1;axes["max_depth"]=max(axes["max_depth"],depth)
        if depth>96 or axes["nodes"]>250000:raise ValueError("LAB_DEMAND_COMPLEXITY")
        typ=type(value)
        if typ is dict:
            axes["max_map"]=max(axes["max_map"],len(value))
            if field in _DEMAND_MAP_FIELDS:
                shapes=sorted({visit(v,depth+1) for v in value.values()})
                return digest(["MAP",shapes])
            return digest(["OBJECT",[(k,visit(v,depth+1,k)) for k,v in sorted(value.items())]])
        if typ is list:
            axes["max_list"]=max(axes["max_list"],len(value))
            return digest(["LIST",sorted({visit(v,depth+1) for v in value})])
        if typ is str:
            m=len(value.encode("utf-8"));axes["text_bytes"]+=m
            axes["max_text"]=max(axes["max_text"],m)
        if typ not in (str,int,float,bool,type(None)):raise ValueError("LAB_DEMAND_VALUE")
        return typ.__name__
    return {"shape":digest([_DEMAND_SCHEMA,mode,stage,visit(request)]),"axes":axes,"stage":stage}


def _within(d,bounds):
    return all(bounds[k][0]<=d["axes"][k]<=bounds[k][1] for k in _DEMAND_AXES)


class CombinedDemandEnvelope:
    """Fit on explicitly reviewed paired courses; veto failures, test held-out.

    Reuses verified private workload tapes. Each review refers to a particular
    captured request and separately retained actual owner evidence. The caller
    supplies review judgments: a digest does not authenticate them. This is an
    experimental coverage mechanism, not validation of model adequacy or a
    claim that structural similarity proves psychological interchangeability.
    No labels, proposals, or private packet content in the compiled envelope.
    """
    def __init__(self,*,mode,owner_head,reference_profile,candidate_profile,
                 reference_identity,candidate_identity,courses,sourcefree_review_attested=False):
        if sourcefree_review_attested is not True:raise ValueError("LAB_DEMAND_REVIEW_REQUIRED")
        self.mode=mode;self.owner_head=_head(owner_head)
        self.reference=reference_profile;self.candidate=candidate_profile
        self.reference_identity=reference_identity;self.candidate_identity=candidate_identity
        if (mode not in ("HISTORICAL","LIVE") or type(reference_profile) is not str
                or type(candidate_profile) is not str or reference_profile==candidate_profile
                or any(type(v) is not str or not re.fullmatch("[0-9a-f]{64}",v)
                       for v in (reference_identity,candidate_identity))):
            raise ValueError("LAB_DEMAND_PROFILE_BINDING")
        if type(courses) not in (list,tuple) or not 3<=len(courses)<=1000:
            raise ValueError("LAB_DEMAND_COURSES")
        task=CHECKPOINT_TASK if mode=="HISTORICAL" else LIVE_TURN_TASK
        groups={};course_ids=set();request_ids=set();evidence_ids=set();manifest=[]
        for c in courses:
            if (type(c) is not dict or set(c)!={"workload","partition","reviews"}
                    or c["partition"] not in ("FIT","HOLDOUT")):
                raise ValueError("LAB_DEMAND_COURSE")
            tape=c["workload"];p=verify_workload(tape,source_head=owner_head)
            cid=tape["sha256"]
            # Distinct actual course state and fixture identity, not simply a
            # different elapsed time or name on a duplicated workload.
            course_key=p["owner_state_sha256"]
            if course_key is None or course_key in course_ids:raise ValueError("LAB_DEMAND_COURSE_STATE")
            course_ids.add(course_key)
            want={r["seq"]:r for r in p["rows"] if r["task"]==task}
            if not want or type(c["reviews"]) is not list:raise ValueError("LAB_DEMAND_EMPTY")
            seen=set()
            for review in c["reviews"]:
                required={"seq","request_digest","reference_identity","candidate_identity",
                          "reference_disposition","candidate_disposition","quality_verdict",
                          "reference_cost_nanos","candidate_cost_nanos","review_digest"}
                if type(review) is not dict or set(review)!=required:raise ValueError("LAB_DEMAND_REVIEW")
                i=review["seq"]
                if type(i) is not int or i not in want or i in seen:raise ValueError("LAB_DEMAND_REVIEW_SEQUENCE")
                seen.add(i);row=want[i];rd=row["packet_digest"]
                if (review["request_digest"]!=rd or rd in request_ids
                        or review["reference_identity"]!=reference_identity
                        or review["candidate_identity"]!=candidate_identity
                        or type(review["review_digest"]) is not str
                        or not re.fullmatch("[0-9a-f]{64}",review["review_digest"])
                        or review["review_digest"] in evidence_ids
                        or review["quality_verdict"] not in ("ADEQUATE","INADEQUATE","UNRESOLVED")):
                    raise ValueError("LAB_DEMAND_REVIEW_BINDING")
                request_ids.add(rd);evidence_ids.add(review["review_digest"])
                costs=[]
                for k in ("reference_cost_nanos","candidate_cost_nanos"):
                    v=review[k]
                    if v is not None:_integer(v,0,10**15)
                    costs.append(v)
                ok=(review["quality_verdict"]=="ADEQUATE"
                    and review["reference_disposition"]==review["candidate_disposition"]=="OWNER_OPERATION_RETURNED"
                    and None not in costs and costs[1]<costs[0])
                d=combined_demand(mode,row["packet"])
                g=groups.setdefault(d["shape"],{"FIT":[],"HOLDOUT":[]})
                g[c["partition"]].append((course_key,d,ok))
                manifest.append({"workload":cid,"partition":c["partition"],"review":copy(review)})
            # No dropping adverse or unreviewed operations from a course.
            if seen!=set(want):raise ValueError("LAB_DEMAND_INCOMPLETE_REVIEW")
        self._rules={};self._summary={}
        for shape,g in groups.items():
            fit=g["FIT"];hold=g["HOLDOUT"];reason="QUALIFIED_EXPERIMENTAL_ENVELOPE"
            if any(not x[2] for x in fit+hold):reason="ADVERSE_OR_UNKNOWN_REVIEW"
            elif len({x[0] for x in fit})<2 or not hold:reason="INSUFFICIENT_DISTINCT_COURSES"
            else:
                bounds={k:[min(x[1]["axes"][k] for x in fit),max(x[1]["axes"][k] for x in fit)]
                        for k in _DEMAND_AXES}
                if any(not _within(x[1],bounds) for x in hold):reason="HELDOUT_OUTSIDE_FIT"
                else:self._rules[shape]=bounds
            self._summary[shape]={"disposition":reason,"fit_rows":len(fit),"holdout_rows":len(hold)}
        self.digest=digest({"schema":_DEMAND_SCHEMA,"mode":mode,"owner_head":owner_head,
            "reference_profile":reference_profile,"candidate_profile":candidate_profile,
            "reference_identity":reference_identity,"candidate_identity":candidate_identity,
            "reviews":manifest,"rules":self._rules})
        self._request_ids=frozenset(request_ids)

    def summary(self):
        return {"schema":_DEMAND_SCHEMA,"qualification_digest":self.digest,
                "scope":"SOURCEFREE_REVIEW_ASSERTIONS_NOT_MODEL_ADEQUACY",
                "qualified_shapes":len(self._rules),"shapes":copy(self._summary)}

    def assess(self,request):
        try:d=combined_demand(self.mode,request)
        except (TypeError,ValueError,RecursionError):return "UNSUPPORTED_REQUEST"
        if d["shape"] not in self._rules:return "NO_QUALIFIED_SHAPE"
        if not _within(d,self._rules[d["shape"]]):return "OUTSIDE_DEMAND_BOUNDS"
        return "MATCHED_REVIEWED_ENVELOPE" if digest(request) in self._request_ids else "NOVEL_WITHIN_REVIEWED_ENVELOPE"


class CombinedAllocationProvider:
    """Select an explicitly qualified profile at an actual owner request.

    Exact owner HEAD + whole request + mode are required for transfer.
    A reviewed qualification is an external assertion, not proof of scientific
    adequacy; this sourcefree operator cannot authenticate that assertion.
    Unmatched requests use the reference profile, not a cheap-model guess.
    No retry or automatic fallback after any attempt, even after rejection.
    """
    def __init__(self,mode,*,owner_head,budget,reference_profile,provider_options,
                 qualifications=(),sourcefree_allocation_authorized=False,metrics_capacity=128,
                 demand_envelope=None,sourcefree_envelope_dispatch=False):
        if sourcefree_allocation_authorized is not True:
            raise ValueError("LAB_ALLOCATION_AUTHORIZATION_REQUIRED")
        if mode not in ("HISTORICAL","LIVE"):raise ValueError("LAB_COMBINED_PROVIDER_MODE")
        self.mode=mode;self.owner_head=_head(owner_head);self.reference=reference_profile
        if (type(provider_options) is not dict or reference_profile not in provider_options
                or not 1<=len(provider_options)<=32):
            raise ValueError("LAB_ALLOCATION_PROVIDERS")
        self.providers={};self.identities={}
        for name,options in provider_options.items():
            if type(name) is not str or type(options) is not dict or "metrics_capacity" in options:
                raise ValueError("LAB_ALLOCATION_PROVIDER_OPTIONS")
            self.providers[name]=budgeted_combined_provider(mode,budget=budget,
                budget_profile=name,metrics_capacity=1,**options)
            p=self.providers[name];profile=budget.profile(name)
            self.identities[name]=digest({"mode":mode,"owner_head":self.owner_head,
                "profile":name,"declared":{k:v for k,v in profile.items() if k!="endpoint"},
                "endpoint_digest":digest(profile["endpoint"]),
                "completion_limit_field":p.completion_limit_field,
                "compact_exact_packet":p.compact_exact_packet,
                "compact_structured_packet":p.compact_structured_packet,
                "compact_task_prompt":p.compact_task_prompt,
                "timeout_seconds":p.timeout_seconds})
        self.envelope=demand_envelope;self.envelope_dispatch=sourcefree_envelope_dispatch
        if type(sourcefree_envelope_dispatch) is not bool or (sourcefree_envelope_dispatch and demand_envelope is None):
            raise ValueError("LAB_DEMAND_DISPATCH_OPTIONS")
        if demand_envelope is not None:
            e=demand_envelope
            if (not isinstance(e,CombinedDemandEnvelope) or e.mode!=mode or e.owner_head!=owner_head
                    or e.reference!=reference_profile or e.candidate not in self.providers
                    or e.reference_identity!=self.identities[reference_profile]
                    or e.candidate_identity!=self.identities[e.candidate]):
                raise ValueError("LAB_DEMAND_ROUTER_BINDING")
        self.routes={}
        if type(qualifications) not in (list,tuple) or len(qualifications)>100000:
            raise ValueError("LAB_ALLOCATION_QUALIFICATIONS")
        for row in qualifications:
            if (type(row) is not dict or set(row)!={"owner_head","mode","request_digest",
                        "reference_profile","candidate_profile","qualification_digest",
                        "reference_identity","candidate_identity"}
                    or row["owner_head"]!=self.owner_head or row["mode"]!=mode
                    or row["reference_profile"]!=reference_profile
                    or row["candidate_profile"] not in self.providers
                    or row["candidate_profile"]==reference_profile
                    or row["reference_identity"]!=self.identities[reference_profile]
                    or row["candidate_identity"]!=self.identities[row["candidate_profile"]]
                    or any(type(row[k]) is not str or not re.fullmatch("[0-9a-f]{64}",row[k])
                           for k in ("request_digest","qualification_digest"))
                    or row["request_digest"] in self.routes):
                raise ValueError("LAB_ALLOCATION_QUALIFICATION_INVALID")
            self.routes[row["request_digest"]]=copy(row)
        self._metrics=deque(maxlen=_integer(metrics_capacity,1,100000))
        self._total=0;self._lock=Lock()
        self.grade="SOURCEFREE_EXACT_QUALIFICATION_ROUTER_NOT_MODEL_ADEQUACY"

    def profile_identity(self,name):
        return self.identities[name]

    def usage_snapshot(self):
        return {"total":self._total,"evicted":self._total-len(self._metrics),
                "receipts":copy(list(self._metrics))}

    def call(self,request):
        if not self._lock.acquire(blocking=False):
            raise BudgetStop("LAB_ALLOCATION_CONCURRENT_CALL")
        try:
            d=digest(request);row=self.routes.get(d)
            name=row["candidate_profile"] if row else self.reference
            basis="EXACT_REVIEWED_REQUEST" if row else "REFERENCE_UNMATCHED"
            qualification=row["qualification_digest"] if row else None
            envelope_decision=None
            if not row and self.envelope is not None:
                envelope_decision=self.envelope.assess(request)
                if self.envelope_dispatch and envelope_decision in ("MATCHED_REVIEWED_ENVELOPE","NOVEL_WITHIN_REVIEWED_ENVELOPE"):
                    name=self.envelope.candidate;basis="SOURCEFREE_EXPERIMENTAL_ENVELOPE"
                    qualification=self.envelope.digest
            p=self.providers[name];before=p.usage_snapshot()["total"]
            try:
                return p.call(copy(request))
            finally:
                after=p.usage_snapshot()
                if after["total"]==before+1 and after["receipts"]:
                    receipt=after["receipts"][-1]
                else:
                    receipt={"attempts":None,"outcome":"ALLOCATION_RECEIPT_MISSING"}
                receipt.update(allocation_profile=name,allocation_identity=self.identities[name],
                    allocation_basis=basis,allocation_owner_head=self.owner_head,
                    allocation_qualification_digest=qualification,
                    envelope_decision=envelope_decision,
                    envelope_qualification_digest=self.envelope.digest if self.envelope else None)
                self._metrics.append(receipt);self._total+=1
        finally:self._lock.release()



def reconcile_budget_owner_receipts(budget,*,historical_receipts=(),live_receipts=()):
    """Join the existing durable budget and owner receipts; never infer admission.

    This is a local completed/held operation accounting view, not a billing
    statement, psychological quality grade, or additional ledger. Native
    cycle/turn completion is distinguished from formation admission and from
    model adequacy. Unlinked or uncertain reservations remain in the cost.
    """
    if not isinstance(budget,LiveBudget):raise TypeError("LAB_BUDGET_REQUIRED")
    if not budget.dispatch_lock.acquire(blocking=False):
        raise BudgetStop("LAB_ACCOUNTING_DURING_DISPATCH")
    try:
        raw=budget.log.read_bytes()
        if len(raw)>MAX_TAPE_BYTES:raise ValueError("LAB_ACCOUNTING_LOG_LIMIT")
        rows=[json.loads(line) for line in raw.splitlines()]
        attempts={}
        for row in rows:
            i=row.get("attempt");event=row.get("event")
            if type(i) is not int or i<1:raise ValueError("LAB_ACCOUNTING_ATTEMPT")
            if event=="RESERVED_BEFORE_SEND":
                if i in attempts or i!=len(attempts)+1:raise ValueError("LAB_ACCOUNTING_SEQUENCE")
                p=budget.profile(row.get("budget_profile"))
                if row.get("reserved_nanos")!=p["reserve"]:
                    raise ValueError("LAB_ACCOUNTING_RESERVATION")
                attempts[i]={"attempt":i,"budget_profile":row.get("budget_profile"),
                    "wire_bytes":row["wire_bytes"],"wire_sha256":row["request_sha256"],
                    "reserved_nanos":row["reserved_nanos"],"usage_state":"UNSETTLED",
                    "rate_estimate_nanos":None,"owner_disposition":"UNLINKED"}
            else:
                if i not in attempts or row.get("budget_profile")!=attempts[i]["budget_profile"]:
                    raise ValueError("LAB_ACCOUNTING_PROFILE_LINK")
                a=attempts[i]
                if event=="USAGE_REPORTED" and a["usage_state"]=="UNSETTLED":
                    p=budget.profile(a["budget_profile"])
                    x=_integer(row["input_tokens"],0,p["input_ceiling"])
                    y=_integer(row["output_tokens"],0,p["output_limit"])
                    estimate=x*p["input_rate"]+y*p["output_rate"]
                    if row.get("declared_rate_estimate_nanos")!=estimate:
                        raise ValueError("LAB_ACCOUNTING_RATE")
                    a.update(usage_state="REPORTED",input_tokens=x,output_tokens=y,rate_estimate_nanos=estimate)
                elif event=="USAGE_REJECTED" and a["usage_state"]=="UNSETTLED":
                    a.update(usage_state="REJECTED",input_tokens=row.get("input_tokens"),
                             output_tokens=row.get("output_tokens"))
                elif event=="UNCERTAIN_SPEND_STOP" and a["usage_state"] in ("UNSETTLED","REJECTED"):
                    a["usage_state"]="UNCERTAIN"
                else:raise ValueError("LAB_ACCOUNTING_EVENT_ORDER")
        if (len(attempts)!=budget.calls or sum(a["reserved_nanos"] for a in attempts.values())!=budget.reserved
                or sum(a["wire_bytes"] for a in attempts.values())!=budget.wire_bytes
                or sum(a["rate_estimate_nanos"] or 0 for a in attempts.values())!=budget.estimated_reported):
            raise ValueError("LAB_ACCOUNTING_BUDGET_MISMATCH")
        unlinked_receipts=0;preflight=0
        for mode,receipts in (("HISTORICAL",historical_receipts),("LIVE",live_receipts)):
            for row in receipts:
                m=row.get("transport_receipt") or {}
                if m.get("attempts")==0 and m.get("budget_disposition") in ("PREFLIGHT_REFUSED","CONCURRENT_REFUSED"):
                    preflight+=1;continue
                i=m.get("budget_attempt")
                if i is None:
                    unlinked_receipts+=1;continue
                if type(i) is not int or i not in attempts:
                    raise ValueError("LAB_ACCOUNTING_UNKNOWN_OWNER_ATTEMPT")
                a=attempts[i]
                if (a["owner_disposition"]!="UNLINKED" or m.get("attempts")!=1
                        or m.get("budget_profile")!=a["budget_profile"]
                        or m.get("budget_request_sha256")!=a["wire_sha256"]):
                    raise ValueError("LAB_ACCOUNTING_OWNER_LINK")
                d=row.get("cycle_disposition") if mode=="HISTORICAL" else row.get("outcome")
                status=("OWNER_OPERATION_RETURNED" if d==("CYCLE_RETURNED" if mode=="HISTORICAL"
                         else "ACTUAL_TURN_COMMITTED") else "HELD_OR_OTHER")
                a.update(owner_mode=mode,owner_disposition=status,owner_raw_disposition=d,
                         allocation_basis=m.get("allocation_basis"),envelope_decision=m.get("envelope_decision"))
        groups={}
        for a in attempts.values():
            key=a["budget_profile"] or "legacy"
            g=groups.setdefault(key,{"attempts":0,"owner_operations_returned":0,"held_or_other":0,
                "unlinked":0,"reserved_nanos":0,"known_rate_estimate_nanos":0,"unknown_usage_attempts":0})
            g["attempts"]+=1;g["reserved_nanos"]+=a["reserved_nanos"]
            if a["owner_disposition"]=="OWNER_OPERATION_RETURNED":g["owner_operations_returned"]+=1
            elif a["owner_disposition"]=="UNLINKED":g["unlinked"]+=1
            else:g["held_or_other"]+=1
            if a["rate_estimate_nanos"] is None:g["unknown_usage_attempts"]+=1
            else:g["known_rate_estimate_nanos"]+=a["rate_estimate_nanos"]
        return {"scope":"OWNER_OPERATION_DISPOSITION_NOT_SEMANTIC_ADEQUACY_OR_BILLING",
                "attempts":list(attempts.values()),"profiles":groups,"preflight_refusals":preflight,
                "unlinked_owner_receipts":unlinked_receipts,"billing_guarantee":False}
    finally:budget.dispatch_lock.release()


def save_report(path,report):
    _local_write(path,report)
