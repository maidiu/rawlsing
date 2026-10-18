"""WG0I independent validator, mutation court and cold CLI.

All expectations come from the frozen Phase A oracle and the pinned O35E matrix;
WG0R output is never used to derive a pass.  The probe frontier is an explicit
TEST_ONLY fixture for option/carrier/route/weight hostile cases, not source
authority and not a WG0R claim.
"""
from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
REPO = Path(subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], cwd=R, text=True).strip())
ORACLE = json.loads((R / "phase_a/01_PHASE_A_FROZEN_ORACLE.json").read_text())
LEDGER = [json.loads(line) for line in
          (R / "phase_a/02_ITEM_IDENTITY_LEDGER.jsonl").read_text().splitlines()]
STAGE_MATRIX = R / "stage/o35e_matrix.json"
O35E_COMMIT = "30a2ef61230cea4583945493a1ad489f5ab213c5"
O35E_PATH = ("WORKER_RETURNS/PYAT-R28-O35E-ORIGINAL-35-ELIGIBILITY-NATIVE-R1/"
             "01_35_WAVE_ELIGIBLE_ITEM_OPERATION_MATRIX.json")
BASE = "68873526efe5a39a0849aa401666ac997870f156"
WG0R_BRANCH = "origin/agent/rabochii-pyat-r37-wg0r-current35-frontier-succession-r1"
OPS = list(ORACLE["operation_census"]["classes"])
STATUSES = list(ORACLE["item_census"]["status_counts"].keys())


def load_matrix():
    if not STAGE_MATRIX.is_file():
        STAGE_MATRIX.parent.mkdir(parents=True, exist_ok=True)
        STAGE_MATRIX.write_bytes(subprocess.check_output(
            ["git", "show", O35E_COMMIT + ":" + O35E_PATH], cwd=REPO))
    return json.loads(STAGE_MATRIX.read_text())


def strict_json(value):
    text = json.dumps(value, sort_keys=True, allow_nan=False)
    json.loads(text)
    return text


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def expected_ledger_ids():
    return {(r["wave"], r["question_id"], r["p2_identity"], r["governed_hash"]) for r in LEDGER}


def matrix_items(matrix):
    return [it for w in matrix["waves"] for it in (w.get("items") or [])]


def matrix_ids(matrix):
    return {(w["atlas_id"], it["question_id"], it["p2_exact_identity_sha256"],
             it["governed_row_payload_hash"])
            for w in matrix["waves"] for it in (w.get("items") or [])}


def validate_matrix(matrix, *, claimed_digest=None):
    """Return a list of typed violations against the frozen oracle."""
    v = []

    def bad(code, detail=""):
        if isinstance(detail, (dict, list)):
            detail = json.dumps(detail, sort_keys=True, separators=(",", ":"))
        v.append({"code": code, "detail": str(detail)[:300]})

    waves = matrix.get("waves") or []
    if len(waves) != 35:
        bad("SOURCE_COUNT_MISMATCH", len(waves))
    if [w.get("atlas_id") for w in waves] != ["SRC%02d" % i for i in range(1, 36)]:
        bad("SOURCE_IDENTITY_MISMATCH")
    items = matrix_items(matrix)
    if len(items) != 18259:
        bad("ITEM_COUNT_MISMATCH", len(items))
    if sum(int(w.get("qra_row_count") or 0) for w in waves) != 18259:
        bad("QRA_ROW_COUNT_MISMATCH")
    for w in waves:
        if len(w.get("items") or []) != int(w.get("qra_row_count") or -1):
            bad("WAVE_ITEM_COUNT_MISMATCH", w.get("atlas_id"))
        if sum((w.get("qra_status_counts") or {}).values()) != len(w.get("items") or []):
            bad("WAVE_STATUS_COUNT_MISMATCH", w.get("atlas_id"))
    ids = matrix_ids(matrix)
    if len(ids) != len(items):
        bad("DUPLICATE_ITEM_IDENTITY", len(items) - len(ids))
    expected = expected_ledger_ids()
    if ids != expected:
        bad("IDENTITY_SET_MISMATCH", {"missing": len(expected - ids),
                                     "extra": len(ids - expected)})
    status = collections.Counter(it.get("qra_authority_status") for it in items)
    want = collections.Counter(ORACLE["item_census"]["status_counts"])
    if status != want:
        bad("STATUS_CENSUS_MISMATCH", {k: [status.get(k), want.get(k)]
                                       for k in set(status) | set(want)
                                       if status.get(k) != want.get(k)})
    topology = collections.Counter((it.get("topology_metadata") or {}).get("p2_response_topology")
                                   for it in items)
    want_top = collections.Counter(r["p2_topology"] for r in LEDGER)
    if topology != want_top:
        bad("TOPOLOGY_CENSUS_MISMATCH", {str(k): [topology.get(k), want_top.get(k)]
                                         for k in set(topology) | set(want_top)
                                         if topology.get(k) != want_top.get(k)})
    for it in items:
        if it.get("original_item_operation_eligibility") != "HOLD_SOURCE_SCIENTIFIC_E_PRE_UNISSUED":
            bad("OPERATION_ELIGIBILITY_UPGRADED", it.get("question_id"))
            break
    # Per-item semantic/topology identity against the frozen ledger.
    ledger_by_key = {(r["wave"], r["question_id"]): r for r in LEDGER}
    for w in waves:
        for it in w.get("items") or []:
            row = ledger_by_key.get((w["atlas_id"], it["question_id"]))
            if row is None:
                bad("LEDGER_ROW_MISSING", it.get("question_id"))
                continue
            if it.get("p2_exact_identity_sha256") != row["p2_identity"]:
                bad("P2_IDENTITY_MISMATCH", it.get("question_id"))
            if it.get("governed_row_payload_hash") != row["governed_hash"]:
                bad("GOVERNED_HASH_MISMATCH", it.get("question_id"))
            if it.get("qsmv2_final_payload_hash") != row["qsmv2_hash"]:
                bad("QSMV2_SEMANTIC_MISMATCH", it.get("question_id"))
            if it.get("relation_use_status") != row["relation_use_status"]:
                bad("RELATION_USE_STATUS_MISMATCH", it.get("question_id"))
            t = it.get("topology_metadata") or {}
            if t.get("p2_response_topology") != row["p2_topology"]:
                bad("ITEM_TOPOLOGY_MISMATCH", it.get("question_id"))
            if t.get("manual_response_topology") != row["manual_topology"]:
                bad("MANUAL_TOPOLOGY_MISMATCH", it.get("question_id"))
            if t.get("p2_response_binding_status") != row["binding_status"]:
                bad("BINDING_STATUS_MISMATCH", it.get("question_id"))
    # Positive-item preservation and source-version currentness.
    gss = [it for it in items if it.get("qra_authority_status") == "FROZEN_ACCEPTED_GSS"]
    if len(gss) != 52:
        bad("POSITIVE_ITEM_MISSING", len(gss))
    src_expected = {s["atlas_id"]: s for s in ORACLE["source_census"]["sources"]}
    for w in waves:
        exp = src_expected.get(w.get("atlas_id"))
        if exp and w.get("sample_risk_design_edition") != exp["sample_risk_design_edition"]:
            bad("SOURCE_VERSION_MISMATCH", w.get("atlas_id"))
            break
        if exp and w.get("source_use_status") != exp["source_use_status"]:
            bad("SOURCE_USE_STATUS_MISMATCH", w.get("atlas_id"))
            break
    # Excluded/active census.
    census = matrix.get("census") or {}
    if census.get("active_rows") != 18259 or census.get("all_rows") != 18518 or \
            census.get("excluded_Asian_W6_rows") != 259:
        bad("ACTIVE_EXCLUDED_CENSUS_MISMATCH", census)
    if claimed_digest is not None:
        core = copy.deepcopy(matrix)
        core.pop("_claimed_digest", None)
        if claimed_digest != sha256(canon(core)):
            bad("FALSE_NO_CHANGE_DIGEST_MISMATCH")
    return v


def baseline():
    matrix = load_matrix()
    v = validate_matrix(matrix)
    status = collections.Counter(it["qra_authority_status"] for it in matrix_items(matrix))
    topology = collections.Counter((it.get("topology_metadata") or {}).get("p2_response_topology")
                                   for it in matrix_items(matrix))
    return {
        "schema": "PYAT_R37_WG0I_BASELINE@1",
        "violations": v,
        "ok": not v,
        "sources": len(matrix["waves"]),
        "items": len(matrix_items(matrix)),
        "all_rows": matrix["census"]["all_rows"],
        "excluded": matrix["census"]["excluded_Asian_W6_rows"],
        "status_counts": dict(status),
        "topology_counts": {str(k): v2 for k, v2 in topology.items()},
        "estimated_operations": len(matrix_items(matrix)) * len(OPS),
        "permitted": 0,
        "oracle_digest": ORACLE["oracle_digest_sha256"],
        "ledger_sha256": ORACLE["item_census"]["identity_ledger"]["sha256"],
    }


# ---------------------------------------------------------------- matrix mutations

def _wave(matrix, atlas_id):
    return next(w for w in matrix["waves"] if w["atlas_id"] == atlas_id)


def mutate_matrix(name):
    m = copy.deepcopy(load_matrix())
    if name == "rf01_missing_item":
        _wave(m, "SRC01")["items"].pop(0)
    elif name == "rf02_substituted_same_cardinality":
        w = _wave(m, "SRC01")
        w["items"][0] = copy.deepcopy(w["items"][1])
    elif name == "rf06_topology_collapse":
        for w in m["waves"]:
            for it in w["items"]:
                if (it.get("topology_metadata") or {}).get("p2_response_topology") in (
                        "ranked_choice", "multiselect", "ranking_or_multiselect"):
                    it["topology_metadata"]["p2_response_topology"] = "scalar"
                    return m
        raise RuntimeError("no ranked/multiselect item")
    elif name == "rf07_d62_shadow":
        for w in m["waves"]:
            for it in w["items"]:
                if it.get("qsmv2_final_payload_hash"):
                    it["qsmv2_final_payload_hash"] = "d62" + "0" * 61
                    return m
        raise RuntimeError("no qsmv2 item")
    elif name == "rf09_source_version_change":
        w = _wave(m, "SRC01")
        dm = dict(w.get("dataset_manifest_identity") or {})
        dm["actual_source_edition_hash"] = "0" * 64
        w["dataset_manifest_identity"] = dm
        w["sample_risk_design_edition"] = "CHANGED_EDITION"
    elif name == "rf10_false_no_change":
        _wave(m, "SRC01")["qra_status_counts"]["GOVERNED_ADMINISTRATIVE_DISPOSITION"] += 1
    elif name == "rf11_post_result_deletion":
        for w in m["waves"]:
            w["items"] = [it for it in w["items"] if it.get("qra_authority_status") != "FROZEN_ACCEPTED_GSS"]
    elif name == "rf12_hidden_unvisited":
        m["census"]["excluded_Asian_W6_rows"] = 0
        m["census"]["all_rows"] = m["census"]["active_rows"]
    else:
        raise ValueError("unknown matrix mutation " + name)
    return m


MATRIX_EXPECT = {
    "rf01_missing_item": "ITEM_COUNT_MISMATCH",
    "rf02_substituted_same_cardinality": "IDENTITY_SET_MISMATCH",
    "rf06_topology_collapse": "TOPOLOGY_CENSUS_MISMATCH",
    "rf07_d62_shadow": "QSMV2_SEMANTIC_MISMATCH",
    "rf09_source_version_change": "SOURCE_VERSION_MISMATCH",
    "rf10_false_no_change": "FALSE_NO_CHANGE_DIGEST_MISMATCH",
    "rf11_post_result_deletion": "ITEM_COUNT_MISMATCH",
    "rf12_hidden_unvisited": "ACTIVE_EXCLUDED_CENSUS_MISMATCH",
}


def run_matrix_mutation(name):
    m = mutate_matrix(name)
    claimed = ORACLE["oracle_digest_sha256"] if name == "rf10_false_no_change" else None
    v = validate_matrix(m, claimed_digest=claimed)
    codes = [x["code"] for x in v]
    return {"name": name, "violations": v, "detected": MATRIX_EXPECT[name] in codes,
            "codes": codes}


# ---------------------------------------------------------------- probe frontier

PROBE_FIELDS = {
    "options": ["1", "2", "3"],
    "carrier": "RESPONDENT",
    "route": "FORWARD",
    "risk_set": "COMMON_ELIGIBLE_RISK_SET",
    "weight": None,
    "denominator": 2,
    "form": "A",
    "split": "NONE",
}


def probe_frontier():
    matrix = load_matrix()
    special = None
    for w in matrix["waves"]:
        for it in w.get("items") or []:
            if (it.get("topology_metadata") or {}).get("p2_response_topology") in (
                    "ranked_choice", "multiselect", "ranking_or_multiselect"):
                special = (w["atlas_id"], it)
                break
        if special:
            break
    rows = []
    for w in matrix["waves"]:
        if special and w["atlas_id"] == special[0]:
            it = special[1]
        else:
            it = (w.get("items") or [None])[0]
        if it is None:
            continue
        rows.append({
            "wave": w["atlas_id"], "question_id": it["question_id"],
            "p2_identity": it["p2_exact_identity_sha256"],
            "status": it["qra_authority_status"],
            "topology": (it.get("topology_metadata") or {}).get("p2_response_topology"),
            "semantic_version": it.get("qsmv2_final_payload_hash") or it["p2_exact_identity_sha256"],
            "frontier_state": "PRODUCER_PENDING",
            "operation_classes": {op: "HOLD" for op in OPS},
            **PROBE_FIELDS,
            "option_ids": ["%s:o%d" % (it["question_id"], i) for i in (1, 2, 3)],
        })
    return {"schema": "PYAT_R37_WG0I_TESTONLY_PROBE_FRONTIER@1", "rows": rows}


def validate_probe(frontier):
    v = []

    def bad(code, detail=""):
        if isinstance(detail, (dict, list)):
            detail = json.dumps(detail, sort_keys=True, separators=(",", ":"))
        v.append({"code": code, "detail": str(detail)[:300]})

    rows = frontier.get("rows") or []
    if len(rows) != 35:
        bad("PROBE_SOURCE_COUNT_MISMATCH", len(rows))
    ledger = {(r["wave"], r["question_id"]): r for r in LEDGER}
    for r in rows:
        key = (r["wave"], r["question_id"])
        if key not in ledger:
            bad("PROBE_IDENTITY_NOT_IN_ORACLE", key)
            continue
        if r.get("p2_identity") != ledger[key]["p2_identity"]:
            bad("PROBE_P2_IDENTITY_MISMATCH", key)
        if r.get("status") != ledger[key]["status"]:
            bad("PROBE_STATUS_MISMATCH", key)
        if r.get("topology") != ledger[key]["p2_topology"]:
            bad("TOPOLOGY_COLLAPSE", key)
        if r.get("semantic_version") != (ledger[key]["qsmv2_hash"] or ledger[key]["p2_identity"]):
            bad("SEMANTIC_VERSION_MISMATCH", key)
        opts = r.get("options") or []
        ids = r.get("option_ids") or []
        if len(opts) != len(set(opts)) or len(ids) != len(set(ids)):
            bad("DUPLICATE_OPTION", key)
        if r.get("carrier") != "RESPONDENT":
            bad("CARRIER_MISMATCH", key)
        if r.get("route") != "FORWARD":
            bad("ROUTE_MISMATCH", key)
        if r.get("risk_set") != "COMMON_ELIGIBLE_RISK_SET":
            bad("RISK_SET_MISMATCH", key)
        if r.get("weight") is not None:
            bad("WEIGHT_OR_DENOMINATOR_MISMATCH", key)
        if r.get("denominator") != 2:
            bad("WEIGHT_OR_DENOMINATOR_MISMATCH", key)
        if r.get("form") != "A" or r.get("split") != "NONE":
            bad("FORM_SPLIT_MISMATCH", key)
        if r.get("frontier_state") != "PRODUCER_PENDING":
            bad("FRONTIER_STATE_MISMATCH", key)
        if set(r.get("operation_classes") or {}) != set(OPS) or \
                any(x != "HOLD" for x in (r.get("operation_classes") or {}).values()):
            bad("OPERATION_NOT_HELD", key)
    return v


def mutate_probe(name):
    f = copy.deepcopy(probe_frontier())
    r = f["rows"][0]
    if name == "rf03_duplicate_options":
        r["options"] = ["1", "1", "2"]
        r["option_ids"] = [r["option_ids"][0], r["option_ids"][0], r["option_ids"][1]]
    elif name == "rf04_country_form_split":
        r["form"] = "B"
        r["split"] = "SPLIT_A"
    elif name == "rf05_household_person":
        r["carrier"] = "HOUSEHOLD"
    elif name == "rf06_mr_collapse":
        for row in f["rows"]:
            if row["topology"] in ("ranked_choice", "multiselect", "ranking_or_multiselect"):
                row["topology"] = "scalar"
                return f
        raise RuntimeError("no ranked/multiselect probe row")
    elif name == "rf07_d62_shadow":
        r["semantic_version"] = "d62" + "0" * 61
    elif name == "rf08_wrong_weight":
        r["weight"] = 1.0
    elif name == "rf09_source_version":
        r["semantic_version"] = "0" * 64
        r["status"] = "FROZEN_ACCEPTED_GSS"
    else:
        raise ValueError("unknown probe mutation " + name)
    return f


PROBE_EXPECT = {
    "rf03_duplicate_options": "DUPLICATE_OPTION",
    "rf04_country_form_split": "FORM_SPLIT_MISMATCH",
    "rf05_household_person": "CARRIER_MISMATCH",
    "rf06_mr_collapse": "TOPOLOGY_COLLAPSE",
    "rf07_d62_shadow": "SEMANTIC_VERSION_MISMATCH",
    "rf08_wrong_weight": "WEIGHT_OR_DENOMINATOR_MISMATCH",
    "rf09_source_version": "SEMANTIC_VERSION_MISMATCH",
}


def run_probe_mutation(name):
    v = validate_probe(mutate_probe(name))
    codes = [x["code"] for x in v]
    return {"name": name, "violations": v, "detected": PROBE_EXPECT[name] in codes,
            "codes": codes}


# ---------------------------------------------------------------- WG0R comparison

def wg0r_status():
    head = subprocess.check_output(["git", "rev-parse", WG0R_BRANCH], cwd=REPO,
                                   text=True).strip()
    commits = subprocess.check_output(["git", "log", "--oneline", BASE + ".." + head],
                                      cwd=REPO, text=True).strip()
    files = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", head,
         "WORKER_RETURNS/"], cwd=REPO, text=True).splitlines()
    returns = sorted({p.split("/")[2] for p in files
                      if len(p.split("/")) > 2 and "WG0R" in p.split("/")[2].upper()})
    return {"branch": WG0R_BRANCH, "head": head, "base": BASE,
            "commits_beyond_base": len([x for x in commits.splitlines() if x.strip()]),
            "return_dirs": returns,
            "output_present": len([x for x in commits.splitlines() if x.strip()]) > 0}


def cold_payload():
    payload = {"baseline": baseline(),
               "matrix_mutations": [run_matrix_mutation(n) for n in MATRIX_EXPECT],
               "probe_mutations": [run_probe_mutation(n) for n in PROBE_EXPECT],
               "probe_baseline": {"violations": validate_probe(probe_frontier())}}
    return payload


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["baseline", "matrix-mutation", "probe-mutation",
                                        "cold", "wg0r-status"])
    ap.add_argument("name", nargs="?")
    args = ap.parse_args()
    if args.command == "baseline":
        print(strict_json(baseline()))
    elif args.command == "matrix-mutation":
        print(strict_json(run_matrix_mutation(args.name)))
    elif args.command == "probe-mutation":
        print(strict_json(run_probe_mutation(args.name)))
    elif args.command == "cold":
        print(strict_json(cold_payload()))
    elif args.command == "wg0r-status":
        print(strict_json(wg0r_status()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
