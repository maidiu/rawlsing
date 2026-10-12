#!/usr/bin/env python3
"""HQ280 PV3 A05 - independent expected-work and consumer no-drop oracle.

Standalone: imports NOTHING from the repository and nothing from A04's binder.
The expected universe below is an EXTERNAL FROZEN FIXTURE, authored before and
apart from any submitted manifest. Deterministic; source-free; no raw survey.

Set model
  E  independently expected runnable operations   (the oracle's own frozen set)
  H  held obligations (must stay visible, must NOT be runnable)
  D  explicit denials   (must stay visible, must NOT be runnable)
  NA source-intrinsic non-applicable              (must stay visible)
  J  constructed jobs submitted by a producer
  R  typed results (per job)
  A  released products
  C  required consumers satisfied
"""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass, field
from typing import Mapping

SCHEMA_VERSION = "HQ280_PV3_A05_EXPECTED_WORK@1.0.0"
CANON = dict(sort_keys=True, separators=(",", ":"))


def h(o) -> str:
    return hashlib.sha256(json.dumps(o, **CANON).encode()).hexdigest()


# --------------------------------------------------------------------------- keys
def documentary_item_key(source, wave, item, form, slot) -> str:
    return h({"k": "DOC_ITEM", "source": source, "wave": wave,
              "item": item, "form": form, "slot": slot})


def operation_key(op_class, roles, target) -> str:
    return h({"k": "OP", "class": op_class, "roles": list(roles), "target": target})


def expected_work_key(item_k, op_k, authority, risk, topology, version=SCHEMA_VERSION) -> str:
    return h({"k": "EXPECTED_WORK", "item": item_k, "op": op_k,
              "authority": authority, "risk": risk, "topology": topology, "v": version})


def execution_attempt_key(exp_k, attempt:int) -> str:
    return h({"k": "ATTEMPT", "expected": exp_k, "n": attempt})


def output_identity(exp_k, result_type, value) -> str:
    return h({"k": "OUTPUT", "expected": exp_k, "type": result_type, "value": value})


# ------------------------------------------------------- EXTERNAL FROZEN UNIVERSE
# Four runnable expected operations that mirror B1-R's A+B 8-respondent XOR slice
# plus two extra classes (non-scalar, routing-conditioned). Nothing here is read
# from any submitted manifest.
def frozen_universe():
    E, H, D, NA = [], [], [], []
    common = dict(source="FIXTURE-XOR-4CASE", wave="W1", authority="AUTH-SOURCEFREE-XOR",
                  risk="RISK-8R-COMMON", topology="SCALAR_2X2")
    def add_E(op_class, roles, target, consumer, topology="SCALAR_2X2", item="Q1", form="F1", slot="S1"):
        ik = documentary_item_key(common["source"], common["wave"], item, form, slot)
        ok = operation_key(op_class, roles, target)
        ek = expected_work_key(ik, ok, common["authority"], common["risk"], topology)
        E.append({"expected_work_key": ek, "documentary_item_key": ik, "operation_key": ok,
                  "op_class": op_class, "roles": list(roles), "target": target,
                  "topology": topology, "required_consumer": consumer,
                  "authority": common["authority"], "risk": common["risk"],
                  "item": item, "form": form, "slot": slot, "source": common["source"], "wave": common["wave"]})
    add_E("UNARY_DISTRIBUTION", ["BASE"], "A", "C1_analytical_composition", item="A")
    add_E("UNARY_DISTRIBUTION", ["BASE"], "B", "C1_analytical_composition", item="B")
    add_E("PAIR_RESPONSE_COTRAVEL", ["CONDITIONER", "TARGET"], "J2", "FieldForge_conditional_support",
          topology="SCALAR_2X2", item="B", form="F1", slot="S2")
    add_E("NONSCALAR_TOPOLOGY_PRESERVATION", ["BASE"], "N1", "C1_analytical_composition",
          topology="MULTISELECT_RANKED", item="N1")

    def add_hold(kind, item, reason):
        ik = documentary_item_key(common["source"], common["wave"], item, "F1", "S1")
        ok = operation_key("UNARY_DISTRIBUTION", ["BASE"], item)
        ek = expected_work_key(ik, ok, common["authority"], common["risk"], "SCALAR_2X2")
        row = {"expected_work_key": ek, "documentary_item_key": ik, "operation_key": ok,
               "item": item, "state": kind, "reason": reason, "runnable": False}
        (H if kind == "HELD" else D if kind == "DENIED" else NA).append(row)
    add_hold("HELD", "V1", "UNCERTIFIED_DIRECTIONALITY__SCIENCE_ISSUER_DECISION_REQUIRED")
    add_hold("HELD", "V2", "ROUTING_UNRESOLVED_RESPONSE_AUTHORITY_GAP")
    add_hold("DENIED", "V3", "EXPLICIT_FAIL_CLOSED_SOURCE_GAP")
    add_hold("NA", "V4", "SOURCE_INTRINSIC_NONAPPLICABLE__NO_COADMINISTERED_TARGET")
    return {"schema": SCHEMA_VERSION, "E": E, "H": H, "D": D, "NA": NA,
            "frontier_digest": h([e["expected_work_key"] for e in sorted(E, key=lambda x: x["expected_work_key"])])}


# ------------------------------------------------------------------- no-drop check
TYPED_NULL = "MEASURED_NULL"
FORBIDDEN_NULL_SOURCES = {"AUTHORITY_UNAVAILABLE", "ZERO_DENOMINATOR", "UNEXECUTED", "UNVISITED"}


@dataclass
class Verdict:
    ok: bool
    failures: list = field(default_factory=list)
    notes: list = field(default_factory=list)

    def fail(self, code, detail=""):
        self.failures.append({"code": code, "detail": detail})


def verify(universe, manifest) -> Verdict:
    """manifest = {jobs:[{expected_work_key,...}], results:{}, products:[], consumers:[]}"""
    v = Verdict(ok=True)
    exp = {e["expected_work_key"]: e for e in universe["E"]}
    exp_keys = set(exp)
    jobs = {j["expected_work_key"]: j for j in manifest.get("jobs", [])}
    job_keys = set(jobs)

    # 1. omission (false negative)
    missing = exp_keys - job_keys
    if missing:
        v.fail("EXPECTED_OPERATION_OMITTED", sorted(missing))
    # 2. unauthorized extra (false positive)
    extra = job_keys - exp_keys
    if extra:
        v.fail("UNAUTHORIZED_EXTRA_JOB", sorted(extra))
    # 3. multiplicity
    for k in exp_keys & job_keys:
        if jobs[k].get("count", 1) != 1:
            v.fail("EXPECTED_MULTIPLICITY_MISMATCH", {"key": k, "count": jobs[k].get("count")})
    # 4. results: typed class + no false null from forbidden sources + no UNAVAILABLE-as-success
    results = manifest.get("results", {})
    for k in exp_keys:
        if k not in job_keys:
            continue
        r = results.get(k)
        if r is None:
            v.fail("MISSING_TYPED_RESULT", k)
            continue
        rt = r.get("result_type")
        if rt == TYPED_NULL and r.get("null_source") in FORBIDDEN_NULL_SOURCES:
            v.fail("FALSE_EMPIRICAL_NULL", {"key": k, "null_source": r.get("null_source")})
        if rt in ("UNAVAILABLE", "UNVISITED", "PARTIAL", "ADAPTIVE_PARTIAL") and r.get("reported_success"):
            v.fail("PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS", {"key": k, "type": rt})
        if r.get("source_denominator", 1) == 0 and rt not in ("MEASURED_ZERO_DENOMINATOR", TYPED_NULL):
            v.fail("ZERO_DENOMINATOR_NOT_TYPED", k)
    # 5. products and required consumers
    products = {p["expected_work_key"] for p in manifest.get("products", [])}
    consumers = {(c["expected_work_key"], c["consumer"]) for c in manifest.get("consumers", [])}
    for k, e in exp.items():
        if k in job_keys and k not in products:
            v.fail("PRODUCT_ABSENT", k)
        if k in products and (k, e["required_consumer"]) not in consumers:
            v.fail("REQUIRED_CONSUMER_OMITTED", {"key": k, "required": e["required_consumer"]})
    # 6. holds/denials/NA stay visible and never runnable
    for grp in ("H", "D", "NA"):
        for row in universe[grp]:
            if row["expected_work_key"] in job_keys:
                v.fail("HELD_OR_DENIED_WORK_EXECUTED", {"state": row["state"], "item": row["item"]})
            if row["documentary_item_key"] not in manifest.get("visible_documentary_items", []):
                v.fail("HELD_OR_DENIED_WORK_NOT_VISIBLE", {"state": row["state"], "item": row["item"]})
    # 7. candidate own-_dk used as an approved co-travel joint
    for j in manifest.get("jobs", []):
        cond, tgt = j.get("roles_pair", ("", ""))
        base = lambda s: s[:-3] if s.endswith("_dk") else s
        if cond and tgt and base(cond) == base(tgt):
            v.fail("CANDIDATE_OWN_DK_JOINT", {"conditioner": cond, "target": tgt})
    # 8. expectation must not be derived from output
    if manifest.get("expected_derived_from", "EXTERNAL_FROZEN") != "EXTERNAL_FROZEN":
        v.fail("EXPECTED_SET_OUTPUT_DERIVED", manifest.get("expected_derived_from"))
    # 9. source identity
    for j in manifest.get("jobs", []):
        e = exp.get(j["expected_work_key"])
        if e and (j.get("source"), j.get("wave")) != (e["source"], e["wave"]):
            v.fail("SOURCE_IDENTITY_MISMATCH", {"key": j["expected_work_key"]})
    v.ok = not v.failures
    return v


# ------------------------------------------------------------------ fixture builders
def honest_manifest(universe):
    jobs, results, products, consumers = [], {}, [], []
    for e in universe["E"]:
        k = e["expected_work_key"]
        jobs.append({"expected_work_key": k, "count": 1, "source": e["source"], "wave": e["wave"],
                     "op_class": e["op_class"], "roles_pair": tuple(e["roles"]) if len(e["roles"]) == 2 else ("", "")})
        results[k] = {"result_type": "MEASURED_POSITIVE" if e["op_class"] != "NONSCALAR_TOPOLOGY_PRESERVATION"
                      else "TOPOLOGY_PRESERVED", "null_source": None, "reported_success": True, "source_denominator": 8}
        products.append({"expected_work_key": k})
        consumers.append({"expected_work_key": k, "consumer": e["required_consumer"]})
    vis = [row["documentary_item_key"] for grp in ("H", "D", "NA") for row in universe[grp]]
    return {"expected_derived_from": "EXTERNAL_FROZEN", "jobs": jobs, "results": results,
            "products": products, "consumers": consumers, "visible_documentary_items": vis}


def key_of(universe, op_class):
    return next(e["expected_work_key"] for e in universe["E"] if e["op_class"] == op_class)
