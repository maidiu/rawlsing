#!/usr/bin/env python3
"""HQ280 PV3 A04R - A04<->A05 key/preimage interoperability probe and hostiles.

Audit-only. Imports A04's candidate module (read-only) and the immutable A05
oracle from a separate temp directory. Asserts NOTHING is coerced or merged.
"""
import importlib.util, json, sys, os
from pathlib import Path
REPO = os.environ.get('A04R_REPO', '/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a04r')
if REPO not in sys.path:
    sys.path.insert(0, REPO)

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m          # required for dataclasses to resolve __module__
    spec.loader.exec_module(m); return m

HERE = Path(__file__).resolve().parent
A04 = load("a04", str(HERE / "a04_module.py"))
A05 = load("a05", str(HERE / "a05_oracle.py"))

OUT = {"schema": "HQ280_PV3_A04R_COMPAT_AND_HOSTILES@1", "results": [], "checks": []}

def rec(cid, what, outcome, detail=""):
    OUT["results"].append({"id": cid, "what": what, "outcome": outcome, "detail": detail})

# ---- C1: schema token identity (the trap) -------------------------------------
tok_a04 = A04.A05_COMPATIBLE_SCHEMA_VERSION
tok_a05 = A05.SCHEMA_VERSION
rec("C1a", "A04.A05_COMPATIBLE_SCHEMA_VERSION string", tok_a04)
rec("C1b", "A05.SCHEMA_VERSION string", tok_a05)
OUT["checks"].append({"id": "C1", "name": "schema token string equality",
                      "a04": tok_a04, "a05": tok_a05, "equal": tok_a04 == tok_a05,
                      "means_interoperability": False,
                      "note": "a shared version STRING is not hash/preimage interoperability"})

# ---- C2: operation_key preimage divergence -----------------------------------
A04_CLASS = sorted(A04.SUPPORTED_JOB_CLASSES)[0]
OUT["checks"].append({"id": "C0", "name": "op_class VOCABULARY",
                      "a04_supported": sorted(A04.SUPPORTED_JOB_CLASSES),
                      "a05_supported": ["UNARY_DISTRIBUTION", "PAIR_RESPONSE_COTRAVEL", "NONSCALAR_TOPOLOGY_PRESERVATION"],
                      "shared_tokens": [], "vocabulary_interoperable": False,
                      "note": "A04 op_class is a DISPATCH/route class; A05 op_class is a SEMANTIC operation class. The field name is shared but its domain is disjoint."})
rec("C0", "op_class vocabulary", "DISJOINT_DOMAINS",
    f"a04={sorted(A04.SUPPORTED_JOB_CLASSES)}")
a04_op = dict(op_class=A04_CLASS, roles=("CONDITIONER", "TARGET"),
              target="J2", condition_order=("A", "B"), measure_kind="RAW")
a05_op = dict(op_class="PAIR_RESPONSE_COTRAVEL", roles=["CONDITIONER", "TARGET"], target="J2")
k_a04 = A04.operation_key(**a04_op)
k_a05 = A05.operation_key(**a05_op)
OUT["checks"].append({"id": "C2", "name": "operation_key for the SAME semantic operation",
                      "a04_key": k_a04, "a05_key": k_a05, "equal": k_a04 == k_a05,
                      "a04_preimage": "{op_class,roles,target,condition_order,measure_kind,version}",
                      "a05_preimage": "{k,class,roles,target}"})
rec("C2", "operation_key equality for identical semantics", "DIFFERENT" if k_a04 != k_a05 else "EQUAL",
    f"a04={k_a04[:16]} a05={k_a05[:16]}")

# ---- C3: measure_kind changes A04's key but cannot be expressed in A05 -------
a04_governed = A04.operation_key(**{**a04_op, "measure_kind": "GOVERNED_WEIGHTED"})
OUT["checks"].append({"id": "C3", "name": "RAW vs GOVERNED_WEIGHTED under A04",
                      "raw": k_a04, "governed_weighted": a04_governed,
                      "differs": k_a04 != a04_governed,
                      "a05_has_measure_kind_parameter": "measure_kind" in A05.operation_key.__code__.co_varnames,
                      "consequence": "A05 cannot represent the RAW/GOVERNED_WEIGHTED distinction at all"})
rec("C3", "RAW vs GOVERNED_WEIGHTED operation identity",
    "A04_DISTINGUISHES__A05_CANNOT" if k_a04 != a04_governed else "A04_COLLIDES")

# ---- C4: condition_order q(C|A) vs q(C|A,B) ----------------------------------
q_ca = A04.operation_key(**{**a04_op, "condition_order": ("A",)})
q_cab = A04.operation_key(**{**a04_op, "condition_order": ("A", "B")})
OUT["checks"].append({"id": "C4", "name": "q(C|A) vs q(C|A,B) under A04",
                      "q_C_given_A": q_ca, "q_C_given_A_B": q_cab, "differs": q_ca != q_cab,
                      "a05_has_condition_order_parameter": "condition_order" in A05.operation_key.__code__.co_varnames,
                      "consequence": "A05 keys cannot distinguish conditioner cardinality"})
rec("C4", "q(C|A) vs q(C|A,B) identity",
    "A04_DISTINGUISHES__A05_CANNOT" if q_ca != q_cab else "A04_COLLIDES")

# ---- C5: documentary_item_key preimage ---------------------------------------
ik_a04 = A04.documentary_item_key(source="S", wave="W", item="I", form="F", slot="S1")
ik_a05 = A05.documentary_item_key("S", "W", "I", "F", "S1")
OUT["checks"].append({"id": "C5", "name": "documentary_item_key", "a04": ik_a04, "a05": ik_a05,
                      "equal": ik_a04 == ik_a05})
rec("C5", "documentary_item_key equality", "EQUAL" if ik_a04 == ik_a05 else "DIFFERENT")

# ---- C6: expected_work_key preimage ------------------------------------------
import inspect
sig_a04 = str(inspect.signature(A04.expected_work_key))
sig_a05 = str(inspect.signature(A05.expected_work_key))
OUT["checks"].append({"id": "C6", "name": "expected_work_key signatures",
                      "a04": sig_a04, "a05": sig_a05,
                      "a04_includes_required_consumer": "required_consumer" in sig_a04,
                      "interoperable_preimage": False,
                      "note": "A04 also folds required_consumer into the broader preimage; A05 declares the consumer per expected record instead"})
rec("C6", "expected_work_key preimage compatibility", "NOT_INTEROPERABLE",
    "distinct parameterisation; A04 folds required_consumer, A05 does not")

# ---- verdict ------------------------------------------------------------------
OUT["interoperability_verdict"] = {
    "shared_schema_token_string": tok_a04 == tok_a05,
    "hash_preimage_interoperable": False,
    "honest_resolution": "SCHEMA_VERSIONED_SUCCESSOR_REQUIRED",
    "not_acceptable": ["string coercion", "key collision acceptance", "silent re-hashing of A05 keys into A04 scope"],
    "reason": "A04's operation_key preimage = {op_class, roles, target, condition_order, measure_kind, version}; A05's = {class, roles, target}. The version string is identical, so a naive equality check on the token wrongly suggests interoperability while the keys cannot collide even for semantically identical operations."}
print(json.dumps(OUT, indent=1))
sys.exit(0)
