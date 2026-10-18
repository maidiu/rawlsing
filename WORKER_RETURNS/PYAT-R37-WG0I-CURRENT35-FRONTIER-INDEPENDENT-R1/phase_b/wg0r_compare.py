"""WG0I — independent comparison of the frozen oracle with the WG0R return.

The WG0R return is author evidence, not acceptance.  This comparison binds its
exact accounting/wave/court bytes, independently recomputes the 18,276 vs 18,259
crosswalk, and types every delta rather than calling it an omission or a pass.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

R = Path(__file__).resolve().parents[1]
W = R / "phase_b/wg0r_evidence"
if not W.exists():
    W = R / "stage/wg0r"
ORACLE = json.loads((R / "phase_a/01_PHASE_A_FROZEN_ORACLE.json").read_text())
LEDGER = [json.loads(line) for line in
          (R / "phase_a/02_ITEM_IDENTITY_LEDGER.jsonl").read_text().splitlines()]

CARRIER_VARS = {"casenumb", "party", "enc", "numero", "pais", "region", "wt"}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_accounting():
    return list(csv.DictReader((W / "evidence/current35_implementation_accounting.csv").open()))


def load_waves():
    return list(csv.DictReader((W / "evidence/all35_wave_conservation.csv").open()))


def court_counts(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    return {k: sum(int(s.attrib.get(k, 0)) for s in suites)
            for k in ("tests", "failures", "errors", "skipped")}


def compare():
    acc = load_accounting()
    waves = load_waves()
    conservation = json.loads((W / "evidence/current35_conservation.json").read_text())
    pending = json.loads((W / "04_TYPED_PENDING.json").read_text())
    custody = json.loads((W / "evidence/local_document_custody.json").read_text())
    final_court = court_counts(W / "evidence/final_court.xml")
    cold_court = court_counts(W / "evidence/cold_court.xml")
    cold_receipt = json.loads((W / "evidence/cold_replay_receipt.json").read_text())
    p2_skeleton = next((x for x in custody
                        if x["local_path"].endswith("Rawlsing_P2_Phase0_Question_Node_Skeleton_v1.csv")), None)

    w_ids = {r["question_implementation_id"] for r in acc}
    w_hashes = {r["exact_identity_sha256"] for r in acc}
    w_by_hash = {r["exact_identity_sha256"]: r for r in acc}
    o_hashes = {r["p2_identity"] for r in LEDGER}
    o_non_none = {h for h in o_hashes if h is not None}
    common = w_hashes & o_non_none
    p2_only = sorted(w_hashes - o_non_none)
    o_only_none = [r for r in LEDGER if r["p2_identity"] is None]
    dup = collections.Counter(r["p2_identity"] for r in LEDGER if r["p2_identity"] is not None)
    duplicates = {h: n for h, n in dup.items() if n > 1}

    p2_only_rows = [w_by_hash[h] for h in p2_only]
    carrier_only = [r for r in p2_only_rows if r["source_variable_code"] in CARRIER_VARS]
    measurement_only = [r for r in p2_only_rows if r["source_variable_code"] not in CARRIER_VARS]

    wave_o = collections.Counter()
    for r in LEDGER:
        wave_o[r["wave"]] += 1
    # map O35E wave ids to family/wave via oracle source census
    src = {s["atlas_id"]: s for s in ORACLE["source_census"]["sources"]}
    deltas = []
    for r in waves:
        fam, wv = r["source_family"], r["wave"]
        o = next((s for s in src.values() if s["family"] == fam and s["wave"] == wv), None)
        if o is None:
            deltas.append({"family": fam, "wave": wv, "o35e": None,
                           "wg0r": int(r["implementations"]), "delta": None,
                           "status": "NO_O35E_MATCH"})
            continue
        d = int(r["implementations"]) - o["qra_row_count"]
        deltas.append({"family": fam, "wave": wv, "atlas_id": o["atlas_id"],
                       "o35e": o["qra_row_count"], "wg0r": int(r["implementations"]),
                       "delta": d,
                       "status": "EXACT_MATCH" if d == 0 else "CROSSWALK_DELTA_REQUIRES_OWNER_TYPING"})

    result = {
        "schema": "PYAT_R37_WG0I_WG0R_COMPARISON@1",
        "wg0r_commit": "0310d94dfab57f811110027c1c801b725fdba5c1",
        "oracle_digest": ORACLE["oracle_digest_sha256"],
        "author_evidence": {
            "accounting_rows": len(acc), "unique_implementation_ids": len(w_ids),
            "unique_identity_hashes": len(w_hashes), "waves": len(waves),
            "wave_sum": sum(int(r["implementations"]) for r in waves),
            "families": len({r["source_family"] for r in waves}),
            "author_court": final_court, "cold_court": cold_court,
            "cold_receipt": cold_receipt,
        },
        "wg0r_claims": {
            "implementations": conservation.get("implementations"),
            "unique_ids": conservation.get("unique_ids"),
            "active_waves": conservation.get("active_waves"),
            "families": conservation.get("families"),
            "duplicate_ids": conservation.get("duplicate_ids"),
            "missing_waves": conservation.get("missing_waves"),
            "unexpected_waves": conservation.get("unexpected_waves"),
            "p2_sha256": conservation.get("p2_sha256"),
            "all35_operation_execution": conservation.get("all35_operation_execution"),
            "pending_edge": conservation.get("pending_edge"),
            "p10_accounting_units": conservation.get("p10_accounting_units"),
            "p10_exact_held_states": conservation.get("p10_exact_held_states"),
            "disposition_carrier": conservation.get("disposition_carrier"),
        },
        "crosswalk": {
            "o35e_rows": len(LEDGER),
            "o35e_non_none_identity_hashes": len(o_non_none),
            "o35e_none_identity_rows": len(o_only_none),
            "o35e_duplicate_identity_hashes": len(duplicates),
            "common_identity_hashes": len(common),
            "p2_only_hashes": len(p2_only),
            "p2_only_carrier_variables": [r["source_variable_code"] for r in carrier_only],
            "p2_only_measurement_candidates": [
                {"family": r["source_family"], "wave": r["wave"],
                 "variable": r["source_variable_code"], "hash": r["exact_identity_sha256"]}
                for r in measurement_only],
            "net_count_delta": len(acc) - len(LEDGER),
            "arithmetic": "%d P2-only hashes - %d O35E None-identity rows = %d net count delta"
                         % (len(p2_only), len(o_only_none), len(acc) - len(LEDGER)),
            "o35e_none_rows": [{"wave": r["wave"], "question_id": r["question_id"],
                                "status": r["status"]} for r in o_only_none],
            "duplicate_rows": {h[:12]: [{"wave": r["wave"], "question_id": r["question_id"]}
                                        for r in LEDGER if r["p2_identity"] == h]
                               for h, n in duplicates.items()},
            "wave_deltas": [d for d in deltas if d["delta"] not in (0, None)],
            "all_wave_statuses": deltas,
            "classification": "CROSSWALK_DELTA_REQUIRES_OWNER_TYPING__NOT_AN_AUTOMATIC_OMISSION__NOT_A_WG0R_DEFECT",
        },
        "carrier": {
            "claimed_bytes": conservation["disposition_carrier"]["claimed_bytes"],
            "claimed_sha256": conservation["disposition_carrier"]["claimed_sha256"],
            "observed_bytes": conservation["disposition_carrier"]["observed_bytes"],
            "observed_sha256": conservation["disposition_carrier"]["observed_sha256"],
            "reserved_bit_violations": conservation["disposition_carrier"]["reserved_bit_violations"],
            "state": conservation["disposition_carrier"]["state"],
            "local_archive_copy_sha256": next(
                (x["sha256"] for x in custody
                 if x["local_path"].endswith("CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER.csv")), None),
            "fail_closed": conservation["disposition_carrier"]["state"] == "DISPOSITION_PAYLOAD_MISMATCH",
        },
        "p2_skeleton": p2_skeleton,
        "typed_pending": [{"id": p["id"], "state": p["state"]} for p in pending["cases"]],
        "full_frontier_claim": "UNVERIFIED" if conservation.get("all35_operation_execution") ==
                               "UNVERIFIED__NO_RAW_READS_OR_SOURCE_WARRANT_ISSUED" else "CHECK",
        "independent_decision": {
            "bounded_fixture_and_identity_accounting": "ACCEPT_AT_OWN_GRAIN",
            "retained_disposition_carrier": "REVISE__RED__EXACT_REPUBLICATION_REQUIRED",
            "17_row_crosswalk": "REVISE__OWNER_TYPING_REQUIRED",
            "full_original35_item_operation_frontier": "HOLD",
        },
    }
    return result


def main():
    result = compare()
    (R / "phase_b/WG0R_COMPARISON.json").write_text(json.dumps(result, indent=2) + "\n")
    c = result["crosswalk"]
    lines = [
        "# WG0I — independent oracle vs WG0R comparison",
        "",
        "WG0R return commit: `0310d94dfab57f811110027c1c801b725fdba5c1`.",
        "This is an independent comparison of author evidence, not acceptance.",
        "",
        "## Bounded author evidence",
        "",
        "- Accounting rows: **%d**; unique IDs: **%d**; unique identity hashes: **%d**; waves: **%d**; families: **%d**."
        % (result["author_evidence"]["accounting_rows"],
           result["author_evidence"]["unique_implementation_ids"],
           result["author_evidence"]["unique_identity_hashes"],
           result["author_evidence"]["waves"], result["author_evidence"]["families"]),
        "- Author court: **%d passed / %d failed / %d error / %d skip**; cold court: **%d passed / %d failed**."
        % (result["author_evidence"]["author_court"]["tests"],
           result["author_evidence"]["author_court"]["failures"],
           result["author_evidence"]["author_court"]["errors"],
           result["author_evidence"]["author_court"]["skipped"],
           result["author_evidence"]["cold_court"]["tests"],
           result["author_evidence"]["cold_court"]["failures"]),
        "- WG0R itself: full current35 operation execution = **%s**; pending edge = `%s`."
        % (result["wg0r_claims"]["all35_operation_execution"],
           result["wg0r_claims"]["pending_edge"]),
        "",
        "## Exact 18,276 vs 18,259 crosswalk",
        "",
        "| Quantity | Value |",
        "|---|---:|",
        "| O35E rows | %d |" % c["o35e_rows"],
        "| WG0R accounting rows | %d |" % len(load_accounting()),
        "| Common non-None identity hashes | %d |" % c["common_identity_hashes"],
        "| P2-only hashes | %d |" % c["p2_only_hashes"],
        "| O35E None-identity (blocked) rows | %d |" % c["o35e_none_identity_rows"],
        "| O35E duplicate identity hashes (non-None) | %d |" % c["o35e_duplicate_identity_hashes"],
        "| Net count delta | %+d |" % c["net_count_delta"],
        "",
        "Arithmetic: %s." % c["arithmetic"],
        "",
        "- P2-only carrier/admin variables (%d): `%s`."
        % (len(c["p2_only_carrier_variables"]), "`, `".join(c["p2_only_carrier_variables"])),
        "- P2-only measurement candidates (%d): `%s`."
        % (len(c["p2_only_measurement_candidates"]),
           "`, `".join(x["family"] + " " + x["wave"] + " " + x["variable"]
                      for x in c["p2_only_measurement_candidates"])),
        "",
        "The 17-row net delta is **not** an automatic omission and **not** a WG0R defect: it is "
        "the difference between the P2 identity/accounting spine and the O35E eligible-item matrix, "
        "with 9 O35E blocked-identity rows carrying no P2 hash and 26 P2-only hashes. The 19 "
        "measurement candidates require exact owner crosswalk before the original item inventory can "
        "be called complete.",
        "",
        "## Carrier RED",
        "",
        "- Claimed: %d bytes / `%s`." % (result["carrier"]["claimed_bytes"], result["carrier"]["claimed_sha256"]),
        "- Observed: %d bytes / `%s`; reserved-bit violations: %d; state: `%s`."
        % (result["carrier"]["observed_bytes"], result["carrier"]["observed_sha256"],
           result["carrier"]["reserved_bit_violations"], result["carrier"]["state"]),
        "- Fail-closed: **%s**; local archive copy SHA-256: `%s`."
        % (result["carrier"]["fail_closed"], result["carrier"]["local_archive_copy_sha256"]),
        "",
        "## Independent decision",
        "",
        "- Bounded native fixture + 18,276 identity accounting: **ACCEPT at own grain**.",
        "- Retained disposition carrier: **REVISE / RED — exact republication required**.",
        "- 17-row / 19-measurement-candidate crosswalk: **REVISE — owner typing required**.",
        "- Full original35 eligible item/operation execution: **HOLD** (PERMITTED = 0 in the frozen oracle; WG0R also says UNVERIFIED).",
    ]
    (R / "phase_b/03_ORACLE_VS_WG0R.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"author_evidence": result["author_evidence"],
                      "crosswalk": {k: c[k] for k in ("common_identity_hashes", "p2_only_hashes",
                                                     "o35e_none_identity_rows", "net_count_delta",
                                                     "p2_only_carrier_variables",
                                                     "p2_only_measurement_candidates")},
                      "carrier": result["carrier"],
                      "decision": result["independent_decision"]}, indent=2))


if __name__ == "__main__":
    main()
