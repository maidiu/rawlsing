"""Preregistered, matched sourcefree inference-economy campaign.

The plan is not a psychological classifier or a model router. It samples
existing owner packets, commits exact request hashes before remote work,
and records declared price assumptions separately from provider usage.
No model call is made during planning. No human/production data authorized.
"""
from collections import defaultdict
from pathlib import Path
import re
import os

from .types import copy, digest, canonical
from .inference_lab import (verify_workload, size, _integer, TASKS,
    compare_frozen, LiveBudget, BudgetedLiveProvider, BudgetStop)
from .live_psychological_llm import ExplicitJSONLLMProvider, _semantic_packet_profile

SCHEMA="RAWLSING_PREREGISTERED_INFERENCE_CAMPAIGN_V1"
BUDGET_FIELDS={"max_calls","max_wire_bytes","input_token_ceiling",
    "completion_token_limit","input_nanos_per_token","output_nanos_per_token",
    "max_budget_nanos"}
ARM_FIELDS={"name","endpoint","model","key_env","compiled","completion_limit_field",
    "input_nanos_per_token","output_nanos_per_token"}
REQUIRED_ARM=ARM_FIELDS-{"completion_limit_field","input_nanos_per_token","output_nanos_per_token"}


def normalize_config(config):
    if type(config) is not dict or set(config)!={"arms","budget"}:
        raise ValueError("LAB_CAMPAIGN_CONFIG")
    b=config["budget"]
    if type(b) is not dict or set(b)!=BUDGET_FIELDS:
        raise ValueError("LAB_CAMPAIGN_BUDGET_FIELDS")
    bounds={"max_calls":100000,"max_wire_bytes":10**12,
        "input_token_ceiling":10**7,"completion_token_limit":131072,
        "input_nanos_per_token":10**9,"output_nanos_per_token":10**9,
        "max_budget_nanos":10**15}
    for k,v in b.items():_integer(v,1,bounds[k])
    if type(config["arms"]) is not list or not 1<=len(config["arms"])<=32:
        raise ValueError("LAB_CAMPAIGN_ARMS")
    arms=[];names=set()
    for a in config["arms"]:
        if type(a) is not dict or set(a)-ARM_FIELDS or not REQUIRED_ARM<=set(a):
            raise ValueError("LAB_CAMPAIGN_ARM_FIELDS")
        name=a["name"]
        if type(name) is not str or not re.fullmatch("[A-Za-z0-9_.-]{1,80}",name) or name in names:
            raise ValueError("LAB_CAMPAIGN_ARM_NAME")
        names.add(name)
        if type(a["key_env"]) is not str or not re.fullmatch("[A-Za-z_][A-Za-z0-9_]{0,127}",a["key_env"]):
            raise ValueError("LAB_CAMPAIGN_KEY_ENV")
        if type(a["compiled"]) is not bool:raise ValueError("LAB_CAMPAIGN_COMPILED_FLAG")
        row={**a,"completion_limit_field":a.get("completion_limit_field","max_completion_tokens"),
            "input_nanos_per_token":a.get("input_nanos_per_token",b["input_nanos_per_token"]),
            "output_nanos_per_token":a.get("output_nanos_per_token",b["output_nanos_per_token"])}
        for k in ("input_nanos_per_token","output_nanos_per_token"):
            _integer(row[k],1,b[k])
        # Use the existing adapter to validate endpoint/model/cap. The planning
        # key is a dummy and this adapter cannot send without its transport.
        _planner_provider(row,b,lambda _:None)
        arms.append(row)
    return {"arms":arms,"budget":copy(b)}


def _planner_provider(a,b,transport):
    return ExplicitJSONLLMProvider(endpoint=a["endpoint"],model=a["model"],
        api_key="local-planning-placeholder-not-a-credential",
        allow_private_actor_data=True,transport=transport,
        compact_exact_packet=a["compiled"],compact_structured_packet=a["compiled"],
        completion_token_limit=b["completion_token_limit"],
        completion_limit_field=a["completion_limit_field"],metrics_capacity=1)


def stratum(row):
    if row["task"]!="development":return row["task"]
    shape=_semantic_packet_profile("development",row["packet"])["development_offer_shape"]
    return "development/named_offer_present" if shape["nonempty_family_fields"] else "development/no_named_offer"


def select_cases(document,*,per_stratum=3,tasks=None):
    """Evenly spaced cases within packet-shape strata, never selected by answer.

    Named offers are a transport-shape discriminator, NOT absence/presence
    of developmental need. Midpoint when one case; endpoints when two or more.
    The selection is coverage-oriented, not population-representative.
    """
    _integer(per_stratum,1,10000)
    p=verify_workload(document)
    want=TASKS if tasks is None else frozenset(tasks)
    if not want or not want<=TASKS:raise ValueError("LAB_CAMPAIGN_TASKS")
    groups=defaultdict(list)
    for r in p["rows"]:
        if r["task"] in want:groups[stratum(r)].append(r)
    if not groups:raise ValueError("LAB_CAMPAIGN_NO_CASES")
    selected=[];coverage={}
    for name,rows in sorted(groups.items()):
        n=min(per_stratum,len(rows))
        indices=[len(rows)//2] if n==1 else [i*(len(rows)-1)//(n-1) for i in range(n)]
        cases=[rows[i] for i in indices]
        coverage[name]={"available":len(rows),"selected":len(cases),
                        "first_seq":rows[0]["seq"],"last_seq":rows[-1]["seq"]}
        selected.extend({"seq":r["seq"],"task":r["task"],"stratum":name,
                         "packet_digest":r["packet_digest"]} for r in cases)
    return sorted(selected,key=lambda r:r["seq"]),coverage


def _wire(row,a,b):
    requests=[]
    def receive(req):
        requests.append({"request_sha256":digest(req),"request_bytes":size(req)})
        answer=copy(row["proposal"])
        # The captured callback permits omitted task. The HTTP grammar requires
        # it; fill ONLY the mock planning response, never the captured packet.
        answer.setdefault("task",row["task"])
        return {"choices":[{"message":{"content":canonical(answer)}}]}
    provider=_planner_provider(a,b,receive)
    provider.propose(row["task"],copy(row["packet"]))
    if len(requests)!=1:raise ValueError("LAB_CAMPAIGN_WIRE_COUNT")
    metric=provider.usage_snapshot()["receipts"][-1]
    if requests[0]["request_bytes"]!=metric["request_bytes"]:
        raise ValueError("LAB_CAMPAIGN_WIRE_ACCOUNTING")
    return {**requests[0],"packet_variant":metric["packet_variant"]}


def build_plan(document,config,*,per_stratum=3,tasks=None,sequence_ids=None):
    p=verify_workload(document)
    if any(r["task"] not in TASKS for r in p["rows"]):
        raise ValueError("LAB_CHECKPOINT_REQUIRES_SEPARATE_OWNER_QUALIFIED_TRANSPORT")
    cfg=normalize_config(config);b=cfg["budget"]
    if sequence_ids is None:
        cases,coverage=select_cases(document,per_stratum=per_stratum,tasks=tasks)
        selection={"per_stratum":per_stratum,"tasks":sorted(TASKS if tasks is None else set(tasks)),
            "rule":"EVEN_SEQUENCE_COVERAGE_WITH_DEVELOPMENT_OFFER_SHAPE_NOT_DEMAND"}
    else:
        if (tasks is not None or type(sequence_ids) is not list or not sequence_ids
                or any(type(i) is not int or not 0<=i<len(p["rows"]) for i in sequence_ids)
                or sorted(set(sequence_ids))!=sequence_ids):
            raise ValueError("LAB_CAMPAIGN_EXPLICIT_SEQUENCE")
        cases=[];coverage={}
        for i in sequence_ids:
            r=p["rows"][i];name=stratum(r)
            cases.append({"seq":i,"task":r["task"],"stratum":name,"packet_digest":r["packet_digest"]})
            coverage[name]=coverage.get(name,0)+1
        selection={"rule":"EXPLICIT_REVIEWED_CASE_IDS_NOT_RANDOM_SAMPLE","sequence_ids":sequence_ids}
    arms=cfg["arms"];schedule=[];totals={}
    if len(cases)*len(arms)>100000:raise ValueError("LAB_CAMPAIGN_PLAN_SIZE_CAP")
    for i,case in enumerate(cases):
        row=p["rows"][case["seq"]];shift=i%len(arms)
        for a in arms[shift:]+arms[:shift]:
            wire=_wire(row,a,b)
            schedule.append({"seq":case["seq"],"arm":a["name"],**wire})
            t=totals.setdefault(a["name"],{"calls":0,"request_bytes":0})
            t["calls"]+=1;t["request_bytes"]+=wire["request_bytes"]
    reserve=b["input_token_ceiling"]*b["input_nanos_per_token"]+b["completion_token_limit"]*b["output_nanos_per_token"]
    calls=len(schedule);wire_bytes=sum(x["request_bytes"] for x in schedule)
    needed=reserve*calls
    violations=[]
    if calls>b["max_calls"]:violations.append("CALL_LIMIT")
    if wire_bytes>b["max_wire_bytes"]:violations.append("WIRE_BYTE_LIMIT")
    if needed>b["max_budget_nanos"]:violations.append("DECLARED_RESERVATION_LIMIT")
    payload={"schema":SCHEMA,"source_head":p["source_head"],
        "workload_sha256":document["sha256"],"config_sha256":digest(cfg),
        "selection":selection,
        "cases":cases,"coverage":coverage,"schedule":schedule,"arms":totals,
        "planned_calls":calls,"planned_wire_bytes":wire_bytes,
        "declared_reserve_nanos":needed,"budget":copy(b),
        "models":[{k:v for k,v in a.items() if k!="key_env"} for a in arms],
        "status":"EXCEEDS_DECLARED_LIMITS" if violations else "FITS_DECLARED_LIMITS",
        "violations":violations,"billing_guarantee":False,"network_calls":0}
    return {"payload":payload,"sha256":digest(payload)}


def verify_plan(document,config,plan):
    if type(plan) is not dict or set(plan)!={"payload","sha256"}:
        raise ValueError("LAB_PLAN_ENVELOPE")
    p=plan["payload"]
    if type(p) is not dict or p.get("schema")!=SCHEMA or digest(p)!=plan["sha256"]:
        raise ValueError("LAB_PLAN_INTEGRITY")
    selection=p["selection"]
    if selection.get("rule")=="EXPLICIT_REVIEWED_CASE_IDS_NOT_RANDOM_SAMPLE":
        expected=build_plan(document,config,sequence_ids=selection["sequence_ids"])
    else:
        expected=build_plan(document,config,per_stratum=selection["per_stratum"],tasks=selection["tasks"])
    if plan!=expected:raise ValueError("LAB_PLAN_RECONSTRUCTION_MISMATCH")
    if p["status"]!="FITS_DECLARED_LIMITS":raise ValueError("LAB_PLAN_EXCEEDS_DECLARED_LIMITS")
    return copy(p)


class PlannedLiveProvider(BudgetedLiveProvider):
    """Refuse any changed wire payload before the existing HTTPS boundary."""
    def __init__(self,*,schedule,**kwargs):
        self.expected=copy(schedule);self.cursor=0
        super().__init__(**kwargs)

    def _request(self,payload):
        if self.cursor>=len(self.expected):
            self.budget.fail();raise BudgetStop("LAB_UNPLANNED_REQUEST")
        item=self.expected[self.cursor]
        if item["request_sha256"]!=digest(payload) or item["request_bytes"]!=size(payload):
            self.budget.fail();raise BudgetStop("LAB_REQUEST_PLAN_MISMATCH")
        self.cursor+=1
        return super()._request(payload)


def _observation_sink(path):
    # Separate local write-ahead evidence file: any write failure stops further
    # sends. The budget journal is separately durable even on process failure.
    fd=os.open(Path(path),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    os.close(fd)
    def append(row):
        with open(path,"ab") as f:
            f.write(canonical(row).encode("utf-8")+b"\n");f.flush();os.fsync(f.fileno())
    return append


def execute_plan(document,config,plan,*,journal,observation_log,sourcefree_live_authorized=False):
    if sourcefree_live_authorized is not True:raise ValueError("LAB_LIVE_AUTHORIZATION_REQUIRED")
    p=verify_plan(document,config,plan);cfg=normalize_config(config)
    # Resolve all credentials before any send, and never serialize them.
    keys={a["name"]:os.environ[a["key_env"]] for a in cfg["arms"]}
    if any(not k for k in keys.values()):raise ValueError("LAB_EMPTY_PROVIDER_KEY")
    sink=_observation_sink(observation_log)
    b=LiveBudget(journal=journal,sourcefree_live_authorized=True,**cfg["budget"])
    arms={}
    for a in cfg["arms"]:
        name=a["name"]
        arms[name]=PlannedLiveProvider(schedule=[x for x in p["schedule"] if x["arm"]==name],
            budget=b,endpoint=a["endpoint"],model=a["model"],api_key=keys[name],
            allow_private_actor_data=True,metrics_capacity=1,
            compact_exact_packet=a["compiled"],compact_structured_packet=a["compiled"],
            profile_semantic_demand=True,completion_limit_field=a["completion_limit_field"])
    result=compare_frozen(document,arms,sequence_ids=[x["seq"] for x in p["cases"]],
        rotate_arms=True,on_observation=sink)
    result["plan_sha256"]=plan["sha256"];result["budget"]=b.snapshot()
    result["mode"]="EXPLICIT_PREREGISTERED_SOURCEFREE_LIVE_PROPOSAL_ONLY"
    result["models"]=p["models"]
    # Per-model declared-rate estimates, NOT invoices. No discounts assumed.
    rates={a["name"]:a for a in cfg["arms"]};costs={}
    for o in result["observations"]:
        t=costs.setdefault(o["arm"],{"known_usage_nanos":0,"unknown_usage_calls":0})
        u=(o.get("metric") or {}).get("usage") or {};a=rates[o["arm"]]
        x=u.get("input_tokens");y=u.get("output_tokens")
        if type(x) is int and type(y) is int:
            t["known_usage_nanos"]+=x*a["input_nanos_per_token"]+y*a["output_nanos_per_token"]
        else:t["unknown_usage_calls"]+=1
    result["declared_model_rate_estimates"]=costs
    result["all_planned_wire_checks_consumed"]=all(x.cursor==len(x.expected) for x in arms.values())
    return result
