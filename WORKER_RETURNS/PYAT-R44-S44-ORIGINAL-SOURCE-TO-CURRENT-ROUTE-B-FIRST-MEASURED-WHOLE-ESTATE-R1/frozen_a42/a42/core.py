"""A42 v2 whole-estate acceptance core over the frozen A41 and R41 returns."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

RETURN_ROOT = Path(__file__).resolve().parent.parent
FROZEN = RETURN_ROOT / "frozen_a41"
if str(FROZEN.parent) not in sys.path:
    sys.path.insert(0, str(FROZEN.parent))
from frozen_a41.a41.gitpreimage import GitPreimage, PreimageError  # noqa: E402

R42_STARTUP = "cebb6c4197e101a28f07ab7f088221250d225056"
A41_COMMIT = "4a51e5c0efe4522dbc0b379c5e118efc356d0c1c"
E41_COMMIT = "6e123bafe749d6997c764ae117fb5e68e0139ed7"
W41_COMMIT = "b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2"
P41_COMMIT = "f27d1101048638bba395143a48efb7ef00bfcda4"
A41_DIR = "WORKER_RETURNS/PYAT-R41-A41-N11-WHOLE-ESTATE-ACCEPTANCE-ASSEMBLY-R1"

# v2 non-substitutable grades, strongest first. Only the first two may ever fill
# an original measured occupancy cell.
GRADE_RANK = {
    "SCIENTIFIC_SOURCE_AUTHORIZED_ACCEPTED": 0,
    "ORIGINAL_MEASURED_OCCUPANCY": 0,
    "INDEPENDENTLY_ACCEPTED_SOURCEFREE": 1,
    "HISTORICAL_RETAINED_EVIDENCE": 2,
    "HISTORICAL_SCOPE_POSITIVE": 2,
    "SOURCEFREE_INTEGRATED_POSITIVE": 3,
    "SOURCEFREE_LOCAL_POSITIVE": 4,
    "VALID_EMPIRICAL_NULL": 5,
    "EMPIRICAL_NULL_WITH_CAUSE": 5,
    "DOCUMENTARY_IDENTITY_RECONCILIATION": 6,
    "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER": 7,
    "SOURCE_INTRINSIC_NONAPPLICABILITY_PROVED": 8,
}
ORIGINAL_GRADES = ("SCIENTIFIC_SOURCE_AUTHORIZED_ACCEPTED", "ORIGINAL_MEASURED_OCCUPANCY")
GRADE_TO_STATUS = {
    "SCIENTIFIC_SOURCE_AUTHORIZED_ACCEPTED": "ORIGINAL_MEASURED_OCCUPANCY",
    "ORIGINAL_MEASURED_OCCUPANCY": "ORIGINAL_MEASURED_OCCUPANCY",
    "INDEPENDENTLY_ACCEPTED_SOURCEFREE": "INDEPENDENTLY_ACCEPTED_SOURCEFREE__NOT_ORIGINAL_OCCUPANCY",
    "HISTORICAL_RETAINED_EVIDENCE": "HISTORICAL_OR_RETAINED__NOT_CURRENT_OCCUPANCY",
    "HISTORICAL_SCOPE_POSITIVE": "HISTORICAL_OR_RETAINED__NOT_CURRENT_OCCUPANCY",
    "SOURCEFREE_INTEGRATED_POSITIVE": "SOURCEFREE_INTEGRATED_POSITIVE__NOT_ORIGINAL_OCCUPANCY",
    "SOURCEFREE_LOCAL_POSITIVE": "SOURCEFREE_LOCAL_POSITIVE__NOT_ORIGINAL_OCCUPANCY",
    "VALID_EMPIRICAL_NULL": "VALID_EMPIRICAL_NULL_WITH_CAUSE",
    "EMPIRICAL_NULL_WITH_CAUSE": "VALID_EMPIRICAL_NULL_WITH_CAUSE",
    "DOCUMENTARY_IDENTITY_RECONCILIATION": "ACCOUNTED_IDENTITY_ONLY__NOT_OCCUPIED",
    "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER": "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER",
    "SOURCE_INTRINSIC_NONAPPLICABILITY_PROVED": "SOURCE_INTRINSIC_NONAPPLICABILITY_PROVED",
}
MISSING_STATUS = "MISSING_EXPECTED_ORIGINAL_SCIENCE__NOT_INTRINSICALLY_INAPPLICABLE"


def _strongest(grades):
    return sorted(grades, key=lambda g: GRADE_RANK[g])[0]


def load_scope(gp: GitPreimage):
    """Load the frozen A41 scope and independently re-verify every declared doc."""
    raw = gp.blob_at(A41_COMMIT, A41_DIR + "/evidence/expected_scope_frozen.json")
    scope = json.loads(raw)
    rec = gp.verify(A41_COMMIT, A41_DIR + "/evidence/expected_scope_frozen.json")
    for key, doc in scope["declared_documents"].items():
        gp.verify(R42_STARTUP, doc["path"], expect_blob_sha1=doc["blob_sha1"])
    scope["_a41_scope_preimage"] = rec
    scope["_r42_startup"] = R42_STARTUP
    return scope


def load_a41_bank(gp: GitPreimage):
    raw = gp.blob_at(A41_COMMIT, A41_DIR + "/evidence/receipt_bank_frozen.json")
    bank = json.loads(raw)
    rec = gp.verify(A41_COMMIT, A41_DIR + "/evidence/receipt_bank_frozen.json")
    # Independently re-verify every artifact preimage at its origin commit.
    for r in bank["receipts"]:
        for a in r["artifacts"]:
            gp.verify(r["origin_commit"], a["path"], expect_blob_sha1=a["blob_sha1"],
                      expect_sha256=a["sha256"], expect_bytes=a["bytes"])
    return bank, rec


# v1 -> v2 grade mapping. Only E04L/F6P are independently accepted (R39I I2).
A41_GRADE_OVERRIDES = {
    "E04L-SOURCEFREE-READTHROUGH": "INDEPENDENTLY_ACCEPTED_SOURCEFREE",
    "F6P-SOURCEFREE-PARTIAL-BOUND": "INDEPENDENTLY_ACCEPTED_SOURCEFREE",
    "I2-R39I-INDEPENDENT-COURT": "INDEPENDENTLY_ACCEPTED_SOURCEFREE",
    "O35B-P1-M1-NATIVE-BINDING": "SOURCEFREE_LOCAL_POSITIVE",
    "WV1-SOURCEFREE-WORLD-CONSUMPTION": "SOURCEFREE_LOCAL_POSITIVE",
    "EE1-SOURCEFREE-TEMPORAL-NULL": "VALID_EMPIRICAL_NULL",
    "O35B-ORIGINAL35-ACCOUNTING": "DOCUMENTARY_IDENTITY_RECONCILIATION",
    "O35B-C11-REPLAY-BLOCKER": "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER",
    "AS2B-LITS-HISTORICAL-POSITIVE": "HISTORICAL_SCOPE_POSITIVE",
}


def a41_receipts_v2(gp):
    bank, rec = load_a41_bank(gp)
    out = []
    for r in bank["receipts"]:
        out.append({
            "receipt_id": r["receipt_id"],
            "origin_commit": r["origin_commit"],
            "claim_id": r["claim_id"],
            "grade": A41_GRADE_OVERRIDES[r["receipt_id"]],
            "evidence_state": r["evidence_state"],
            "proof_grade": r["proof_grade"],
            "coverage": {
                "wave_ids": r["coverage"]["wave_ids"],
                "axis_ids": r["coverage"]["axis_ids"],
                "f_gate_ids": [],
                "functional_gates": [],
                "register_151_ids": r["coverage"]["register_151_ids"],
                "ledger_101_ids": r["coverage"]["ledger_101_ids"],
                "global_relations": [],
                "global_contributions": r["coverage"]["global_relations"],
                "occupancy_grain_note": r["coverage"]["occupancy_grain_note"],
            },
            "unknown_bounds": r.get("unknown_bounds"),
            "verified_artifacts": len(r["artifacts"]),
            "carried_from": "A41_FROZEN_BANK_" + rec["blob_sha1"][:12],
        })
        rel = r["coverage"].get("global_relations") or []
        fmap = {"cross_family_F6": "F6", "temporal_F7": "F7", "possibility_F8": "F8"}
        out[-1]["coverage"]["functional_gates"] = [fmap[x] for x in rel if x in fmap]
    return out


R41_SCHEMA = "A42_NATIVE_RECEIPT@2.0.0"


def ingest_r41_bank(bank, gp, scope):
    """Verify the A42 R41 receipts: preimages, anti-promotion, consumers, clocks."""
    out = []
    for r in bank["receipts"]:
        for field in ("receipt_id", "origin_commit", "claim_id", "grade", "coverage",
                      "currentness", "artifacts", "unknown_bounds"):
            if field not in r:
                raise PreimageError(f"R41_RECEIPT_MISSING_FIELD:{field}:{r.get('receipt_id')}")
        if r["grade"] not in GRADE_RANK:
            raise PreimageError(f"R41_RECEIPT_UNKNOWN_GRADE:{r['grade']}")
        for a in r["artifacts"]:
            gp.verify(r["origin_commit"], a["path"], expect_blob_sha1=a.get("blob_sha1"),
                      expect_sha256=a.get("sha256"), expect_bytes=a.get("bytes"))
        cov = r["coverage"]
        for key in ("wave_ids", "axis_ids", "f_gate_ids", "functional_gates",
                    "register_151_ids", "ledger_101_ids", "global_relations",
                    "global_contributions", "occupancy_grain_note"):
            if key not in cov:
                raise PreimageError(f"R41_COVERAGE_MISSING:{key}:{r['receipt_id']}")
        # Anti-promotion: no original occupancy while U/E_pre is unissued.
        if r["grade"] in ORIGINAL_GRADES:
            if not cov["wave_ids"]:
                raise PreimageError(f"ORIGINAL_OCCUPANCY_WITH_EMPTY_WAVE_SCOPE:{r['receipt_id']}")
            wmap = scope["wave_expected_u_e_pre"]
            for wid in cov["wave_ids"]:
                if wmap.get(wid) != "ISSUED_AND_RECONCILED":
                    raise PreimageError(
                        f"FALSE_PROMOTION_SOURCEFREE_TO_ORIGINAL_OCCUPANCY:{wid}:{wmap.get(wid)}")
        # Consumer registry + currentness clock.
        declared = set(scope.get("declared_consumers", []))
        for ref in r.get("downstream_consumer_read_refs", []):
            if declared and ref not in declared:
                raise PreimageError(f"R41_UNKNOWN_OR_FORGED_CONSUMER_REF:{ref}")
        cn = r["currentness"]
        if cn.get("archive_or_current") not in ("ARCHIVE", "CURRENT"):
            raise PreimageError(f"R41_BAD_CURRENTNESS:{r['receipt_id']}")
        if cn.get("as_of", "") > scope.get("declared_clock", "9999"):
            raise PreimageError(f"R41_CURRENTNESS_CLOCK_VIOLATION:{r['receipt_id']}")
        out.append(r)
    return out


def load_w41_register(gp):
    raw = gp.blob_at(W41_COMMIT,
                     "WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/original35_world_eligibility_register.json")
    d = json.loads(raw)
    return {row["id"]: row for row in d["rows"]}


def assess_v2(scope, receipts, w41_register, old_manifest):
    cell_recs = defaultdict(list)
    for rec in receipts:
        cov = rec["coverage"]
        for wid in cov["wave_ids"]:
            for aid in list(cov["axis_ids"]) + list(cov["f_gate_ids"]):
                cell_recs[f"{wid}.{aid}"].append(rec)

    cells = []
    tally = defaultdict(int)
    for cell in scope["cells"]:
        covering = cell_recs.get(cell["cell_id"], [])
        if covering:
            primary = _strongest([r["grade"] for r in covering])
            status = GRADE_TO_STATUS[primary]
            evidence = [{"receipt_id": r["receipt_id"], "grade": r["grade"],
                         "origin_commit": r["origin_commit"]} for r in
                        sorted(covering, key=lambda x: x["receipt_id"])]
            missing = None
        else:
            primary = None
            status = MISSING_STATUS
            evidence = []
            missing = {"owner": "COMPETENT_ORIGINAL35_SOURCE_OPERATION_ISSUER_OR_NAMED_PRODUCER",
                       "obligation": cell["required_proof"]}
        tally[status] += 1
        cells.append({"cell_id": cell["cell_id"], "source_id": cell["source_id"],
                      "axis_id": cell["axis_id"], "axis_family": cell["axis_family"],
                      "identity": cell["identity"], "expected_u_e_pre": cell["expected_u_e_pre"],
                      "consumed_grade": primary, "cell_status": status,
                      "actual_evidence": evidence, "missing_obligation": missing})

    waves = []
    for w in scope["waves"]:
        wc = [c for c in cells if c["source_id"] == w["source_id"]]
        grades = {c["consumed_grade"] for c in wc if c["consumed_grade"]}
        if grades & set(ORIGINAL_GRADES):
            state = "ORIGINAL_MEASURED_OCCUPIED"
        elif grades & {"HISTORICAL_RETAINED_EVIDENCE", "HISTORICAL_SCOPE_POSITIVE"}:
            state = "HISTORICAL_OR_RETAINED_ONLY"
        elif "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER" in grades:
            state = "BLOCKED_NARROW_OWNER"
        elif "DOCUMENTARY_IDENTITY_RECONCILIATION" in grades:
            state = "IDENTITY_ACCOUNTED_ONLY"
        else:
            state = "EXPECTED_UNISSUED"
        waves.append({"source_id": w["source_id"], "source_name": w["source_name"],
                      "identity": w["identity"], "expected_u_e_pre": w["expected_u_e_pre"],
                      "wave_occupancy_state": state,
                      "occupied_or_accounted_cells": sum(1 for c in wc if c["consumed_grade"]),
                      "missing_cells": sum(1 for c in wc if c["consumed_grade"] is None)})

    # per-wave F rows + author-declared W41 F5/F6/F7 status
    f_rows = []
    for c in cells:
        if c["axis_family"] != "F_GATE":
            continue
        wr = w41_register.get(c["source_id"], {})
        declared = wr.get(c["axis_id"]) if c["axis_id"] in ("F5", "F6", "F7") else None
        f_rows.append({"gate_id": c["axis_id"], "grain": scope["f1_f8_gate_grain"][c["axis_id"]],
                       "source_id": c["source_id"], "identity": c["identity"],
                       "expected_u_e_pre": c["expected_u_e_pre"],
                       "consumed_grade": c["consumed_grade"], "cell_status": c["cell_status"],
                       "actual_evidence": c["actual_evidence"],
                       "missing_obligation": c["missing_obligation"],
                       "w41_author_declared_status": declared,
                       "local_pass_cannot_close_global": c["axis_id"] in ("F6", "F7", "F8")})

    functional = defaultdict(list)
    global_contrib = defaultdict(list)
    for rec in receipts:
        for g in rec["coverage"].get("functional_gates", []):
            functional[g].append(rec)
        for g in rec["coverage"].get("global_contributions", []):
            global_contrib[g].append(rec)
    for name, rel in scope["global_relations"].items():
        contrib = global_contrib.get(name, [])
        accepted = [r for r in receipts if name in r["coverage"].get("global_relations", [])]
        f_rows.append({
            "gate_id": name.split("_")[-1], "grain": rel["grain"], "source_id": "GLOBAL",
            "global_relation_name": name, "expected_status": rel["expected_status"],
            "consumed_grade": (_strongest([r["grade"] for r in accepted]) if accepted else None),
            "cell_status": ("ACCEPTED" if accepted else
                            "OPEN_GLOBAL_OBLIGATION__SOURCEFREE_CONTRIBUTION_ONLY"
                            if contrib else "OPEN_GLOBAL_OBLIGATION__UNCLOSED"),
            "functional_grade": (_strongest([r["grade"] for r in contrib]) if contrib else None),
            "actual_evidence": [{"receipt_id": r["receipt_id"], "grade": r["grade"]}
                                for r in contrib],
            "missing_obligation": rel["obligation"],
            "local_pass_cannot_close_global": True})

    # 151 / 101 / unmatched
    cov_reg = defaultdict(list)
    cov_led = defaultdict(list)
    for rec in receipts:
        for rid in rec["coverage"]["register_151_ids"]:
            cov_reg[rid].append(rec)
        for lid in rec["coverage"]["ledger_101_ids"]:
            cov_led[lid].append(rec)
    cw = scope["crosswalk_151_101"]
    reg_rows = {r["id"]: r for r in scope["register_151_rows"]}
    unmatched = [{"register_id": rid, "group": reg_rows[rid]["group"],
                  "obligation": reg_rows[rid]["obligation"],
                  "declared_status": reg_rows[rid]["declared_status"],
                  "resolution": "STILL_MISSING__UNRESOLVED",
                  "competent_retirement_ref": None}
                 for rid in cw["unmatched_register_rows"]]
    register_out = [{"register_id": r["id"], "obligation": r["obligation"],
                     "evidence_receipts": [x["receipt_id"] for x in cov_reg.get(r["id"], [])],
                     "completion_state": "EVIDENCE_PRESENT" if cov_reg.get(r["id"]) else "MISSING_EXPECTED"}
                    for r in scope["register_151_rows"]]
    ledger_out = [{"ledger_id": t["id"], "action": t["action"],
                   "evidence_receipts": [x["receipt_id"] for x in cov_led.get(t["id"], [])],
                   "completion_state": "EVIDENCE_PRESENT" if cov_led.get(t["id"]) else "MISSING_EXPECTED"}
                  for t in scope["ledger_101_rows"]]

    functional_out = {}
    for gate in ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"):
        recs = functional.get(gate, [])
        functional_out[gate] = {
            "functional_grade": (_strongest([r["grade"] for r in recs]) if recs else None),
            "evidence_receipts": [r["receipt_id"] for r in recs],
            "note": "functional/method maturity, NOT original per-wave occupancy"}

    blockers = [{"kind": "MISSING_EXPECTED_CELL_EVIDENCE", "cell_id": c["cell_id"],
                 "owner": c["missing_obligation"]["owner"]}
                for c in cells if c["missing_obligation"]]
    for row in f_rows:
        if row.get("source_id") == "GLOBAL":
            blockers.append({"kind": "OPEN_GLOBAL_RELATION",
                             "cell_id": "GLOBAL." + row["global_relation_name"],
                             "owner": "COMPETENT_GLOBAL_RELATION_OWNER"})

    functional_evidence_gates = sorted(g for g, rs in functional.items() if rs)
    verdict = {
        "n11_state": "N11_NOT_READY",
        "functional_evidence_gates": functional_evidence_gates,
        "verdict_scope": "whole declared estate 35/1890/151/101/F1-F8 global (A42 v2)",
        "original_measured_occupied_cells": tally.get("ORIGINAL_MEASURED_OCCUPANCY", 0),
        "independently_accepted_sourcefree_cells": tally.get(
            "INDEPENDENTLY_ACCEPTED_SOURCEFREE__NOT_ORIGINAL_OCCUPANCY", 0),
        "historical_or_retained_cells": tally.get(
            "HISTORICAL_OR_RETAINED__NOT_CURRENT_OCCUPANCY", 0),
        "sourcefree_integrated_cells": tally.get(
            "SOURCEFREE_INTEGRATED_POSITIVE__NOT_ORIGINAL_OCCUPANCY", 0),
        "sourcefree_local_cells": tally.get(
            "SOURCEFREE_LOCAL_POSITIVE__NOT_ORIGINAL_OCCUPANCY", 0),
        "valid_null_cells": tally.get("VALID_EMPIRICAL_NULL_WITH_CAUSE", 0),
        "identity_accounted_only_cells": tally.get("ACCOUNTED_IDENTITY_ONLY__NOT_OCCUPIED", 0),
        "blocked_cells": tally.get("DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER", 0),
        "intrinsic_nonapplicability_cells": tally.get("SOURCE_INTRINSIC_NONAPPLICABILITY_PROVED", 0),
        "missing_expected_cells": tally.get(MISSING_STATUS, 0),
        "original_measured_missing_cells": len(cells) - tally.get("ORIGINAL_MEASURED_OCCUPANCY", 0),
        "total_cells": len(cells),
        "finite_blocker_count": len(blockers),
        "global_relations_closed": 0,
        "global_relations_open": 3,
        "unmatched_register_rows": len(unmatched),
        "unmatched_resolved_by_competent_retirement": 0,
        "unmatched_still_unresolved": len(unmatched),
        "can_self_adopt_n11": False,
        "notes": ["SOURCEFREE_LOCAL_PASS != ORIGINAL_ESTATE_OCCUPANCY",
                  "R41 sourcefree integration does not create original U/E_pre",
                  "per-wave F6/F7/F8 cells cannot discharge the global F6/F7/F8 capabilities"],
    }
    old = old_manifest["verdict"]
    delta = {
        "old_a41_original_measured": old["original_measured_occupied_cells"],
        "new_a42_original_measured": verdict["original_measured_occupied_cells"],
        "old_missing_expected": old["missing_expected_cells"],
        "new_missing_expected": verdict["missing_expected_cells"],
        "missing_delta": verdict["missing_expected_cells"] - old["missing_expected_cells"],
        "old_sourcefree_local": old["sourcefree_covered_cells"],
        "new_sourcefree_local": verdict["sourcefree_local_cells"],
        "new_sourcefree_integrated_cells": verdict["sourcefree_integrated_cells"],
        "new_independently_accepted_sourcefree_cells": verdict["independently_accepted_sourcefree_cells"],
        "new_historical_or_retained_cells": verdict["historical_or_retained_cells"],
        "no_new_original_occupied_cells": (old["original_measured_occupied_cells"]
                                           == verdict["original_measured_occupied_cells"] == 0),
        "old_functional_evidence_gates": [],
        "new_functional_evidence_gates": functional_evidence_gates,
        "new_functional_grades": {g: functional_out[g]["functional_grade"]
                                  for g in functional_out if functional_out[g]["functional_grade"]},
    }
    return {"verdict": verdict, "delta": delta, "cells": cells, "waves": waves,
            "f1_f8_rows": f_rows, "functional_maturity": functional_out,
            "register_151": register_out, "ledger_101": ledger_out,
            "unmatched_register_resolution": unmatched,
            "crosswalk": cw, "blocker_ledger": blockers,
            "grade_tally": dict(sorted(tally.items())),
            "receipts": [{"receipt_id": r["receipt_id"], "grade": r["grade"],
                          "origin_commit": r["origin_commit"], "claim_id": r["claim_id"],
                          "verified_artifacts": r.get("verified_artifacts"),
                          "unknown_bounds": r.get("unknown_bounds"),
                          "currentness": r.get("currentness")} for r in receipts]}


SCHEMA = "PYAT_A42_N11_CANDIDATE@2.0.0"


def artifacts(acc, scope, old_manifest, receipt_meta):
    v = acc["verdict"]
    per_gate = defaultdict(list)
    for row in acc["f1_f8_rows"]:
        per_gate[row["gate_id"]].append(row)
    f1f8 = {
        "schema": SCHEMA, "artifact": "f1_f8_acceptance_matrix.json",
        "grade": "CANDIDATE_NOT_READY", "scope_digest": scope["scope_digest"],
        "declared_gate_grain": scope["f1_f8_gate_grain"],
        "global_relation_rule": ("F6/F7/F8 are separate global relation/service obligations; "
                                 "per-wave cells cannot discharge them."),
        "row_count": len(acc["f1_f8_rows"]),
        "per_wave_row_count": sum(1 for r in acc["f1_f8_rows"] if r.get("source_id") != "GLOBAL"),
        "global_row_count": sum(1 for r in acc["f1_f8_rows"] if r.get("source_id") == "GLOBAL"),
        "functional_maturity": acc["functional_maturity"],
        "rows": acc["f1_f8_rows"],
        "gate_summary": {g: {"rows": len(rows),
                             "original_measured": sum(1 for r in rows if r["consumed_grade"] in ORIGINAL_GRADES),
                             "functional_grade": acc["functional_maturity"].get(g, {}).get("functional_grade"),
                             "missing": sum(1 for r in rows if r["consumed_grade"] is None),
                             "global_unclosed": g in ("F6", "F7", "F8")}
                         for g, rows in sorted(per_gate.items())},
        "n11_state": v["n11_state"],
    }
    manifest = {
        "schema": SCHEMA, "artifact": "estate_acceptance_manifest.json",
        "grade": "CANDIDATE_NOT_READY", "startup": R42_STARTUP,
        "a41_frozen_source": A41_COMMIT, "scope_digest": scope["scope_digest"],
        "declared_documents": scope["declared_documents"],
        "expected_accounting": {"source_count": scope["source_count"],
                                "axis_counts": scope["axis_counts"],
                                "expected_cell_count": scope["expected_cell_count"],
                                "register_151_count": scope["register_151_count"],
                                "ledger_101_count": scope["ledger_101_count"]},
        "verdict": v, "delta": acc["delta"], "grade_tally": acc["grade_tally"],
        "receipts": acc["receipts"], "receipt_meta": receipt_meta,
        "crosswalk_151_101": acc["crosswalk"],
        "unmatched_register_resolution": acc["unmatched_register_resolution"],
        "functional_maturity": acc["functional_maturity"],
        "waves": acc["waves"], "cells": acc["cells"],
        "register_151": acc["register_151"], "ledger_101": acc["ledger_101"],
        "blocker_ledger": acc["blocker_ledger"],
        "global_relations": scope["global_relations"],
        "j42_state": "PENDING_PHYSICAL_RETURN__NOT_COUNTED",
    }
    L = ["# A42 - N11 whole-estate terminal acceptance assembly - CANDIDATE v2", "",
         f"**State: {v['n11_state']}** at the exact whole declared-estate grain.", "",
         "A42 ingests the actual E41/W41/P41 native returns (preimage verified) into the",
         "frozen A41 executable assembler. It does NOT self-adopt N11, wake N12 or issue",
         "source/model/actor permission. Recording R41 science is not completing the",
         "original estate.", "",
         f"- R42 startup: `{R42_STARTUP}`",
         f"- frozen A41 source: `{A41_COMMIT}`",
         f"- frozen scope digest: `{scope['scope_digest']}`",
         f"- expected cells: {scope['expected_cell_count']} (35 x 54)", "",
         "## Occupancy by grade (non-substitutable)", "", "| Grade | Cells |", "|---|---|",
         f"| original measured occupancy | {v['original_measured_occupied_cells']} |",
         f"| independently accepted sourcefree | {v['independently_accepted_sourcefree_cells']} |",
         f"| historical or retained | {v['historical_or_retained_cells']} |",
         f"| sourcefree integrated positive | {v['sourcefree_integrated_cells']} |",
         f"| sourcefree local positive | {v['sourcefree_local_cells']} |",
         f"| valid empirical null | {v['valid_null_cells']} |",
         f"| accounted identity only | {v['identity_accounted_only_cells']} |",
         f"| development blocker, narrow owner | {v['blocked_cells']} |",
         f"| missing expected original science | {v['missing_expected_cells']} |",
         f"| **total** | **{v['total_cells']}** |", "",
         "## R41 fan-in delta vs frozen A41", "",
         f"- original measured: {acc['delta']['old_a41_original_measured']} -> "
         f"{acc['delta']['new_a42_original_measured']} (no new original occupied cells: "
         f"{acc['delta']['no_new_original_occupied_cells']})",
         f"- missing expected: {acc['delta']['old_missing_expected']} -> "
         f"{acc['delta']['new_missing_expected']} (delta {acc['delta']['missing_delta']})",
         f"- new sourcefree integrated cells: {acc['delta']['new_sourcefree_integrated_cells']}",
         f"- new independently accepted sourcefree cells: "
         f"{acc['delta']['new_independently_accepted_sourcefree_cells']}",
         f"- new historical/retained cells: {acc['delta']['new_historical_or_retained_cells']}",
         "", "## Functional F1-F8 maturity (method, NOT original per-wave occupancy)", "",
         "| Gate | Functional grade |", "|---|---|"]
    for g in ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"):
        L.append(f"| {g} | {acc['functional_maturity'][g]['functional_grade'] or 'NONE'} |")
    L += ["", "## Global F1-F8 obligations (UNACCEPTED)", ""]
    for row in acc["f1_f8_rows"]:
        if row.get("source_id") == "GLOBAL":
            L.append(f"- `{row['global_relation_name']}`: {row['cell_status']}")
    L += ["", f"## 81 unmatched register rows", "",
          f"- still unresolved: {v['unmatched_still_unresolved']}",
          f"- resolved by competent retirement: {v['unmatched_resolved_by_competent_retirement']}",
          "- scientific flag: no competent retirement/succession decision was found in the",
          "  declared corpus; these are NOT assumed defects and NOT silently retired.", "",
          "## Terminal decision", "",
          "N11 remains NOT_READY. The exact remaining owners are the original35 U/E_pre/source",
          "issuer, the LiTS C11 custodian preimages, the F6/F7/F8 global owners, and the 81",
          "unmatched register obligations. J42 remains a pending physical return.", ""]
    md = "\n".join(L) + "\n"
    intake = {
        "schema": SCHEMA, "artifact": "n11_r41_return_intake_and_delta.json",
        "old_a41_source": A41_COMMIT,
        "old_a41": {"receipts": 9,
                    "verdict": old_manifest["verdict"],
                    "grade_tally": old_manifest.get("grade_tally")},
        "new_a42": {"receipts": len(acc["receipts"]), "verdict": v,
                    "grade_tally": acc["grade_tally"]},
        "delta": acc["delta"],
        "grade_buckets": {
            "SOURCEFREE_LOCAL": [r["receipt_id"] for r in acc["receipts"]
                                 if r["grade"] == "SOURCEFREE_LOCAL_POSITIVE"],
            "RETAINED_HISTORIC": [r["receipt_id"] for r in acc["receipts"]
                                  if r["grade"] in ("HISTORICAL_RETAINED_EVIDENCE",
                                                    "HISTORICAL_SCOPE_POSITIVE")],
            "INTEGRATED_SOURCEFREE": [r["receipt_id"] for r in acc["receipts"]
                                      if r["grade"] == "SOURCEFREE_INTEGRATED_POSITIVE"],
            "INDEPENDENTLY_ACCEPTED_SOURCEFREE": [r["receipt_id"] for r in acc["receipts"]
                                                  if r["grade"] == "INDEPENDENTLY_ACCEPTED_SOURCEFREE"],
            "SOURCE_AUTHORIZED": [],
            "GLOBAL_ACCEPTED": [],
        },
        "r41_intake": receipt_meta,
        "no_invented_original_occupancy": True,
        "f6p_not_world_acceptance": True,
        "j42_state": "PENDING_PHYSICAL_RETURN__NOT_COUNTED",
    }
    wake = {
        "schema": SCHEMA, "artifact": "original35_source_positive_execution_wake_packet.json",
        "state": "ORIGINAL_SOURCE_POSITIVE_BLOCKED__AUTHORIZATION_AND_CUSTODY_REQUIRED",
        "original35_u_e_pre": "UNISSUED",
        "eligible_operation_count": None,
        "eligible_operation_count_reason": "null with cause: no competent U/E_pre issued",
        "required_permissions": [
            "competent original35 source/operation/U/E_pre issuer grant",
            "competent current source+host+purpose warrant OR complete archived preimages",
        ],
        "c11_prerequisite": {
            "o35b_commit": "c714af26a5a749706c6da06df40ac0ef026c6296",
            "source_release_ref": "LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669",
            "semantic_hash": "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f",
            "missing": "all 15 native C11 SourceReleaseCandidate sections",
        },
        "nearest_source_positive_campaign": (
            "once granted: original I03/Batch -> M1 -> N10E -> F1-F4 for the exact granted "
            "waves, with the already-built A41/A42 acceptance machine as the consumer"),
        "does_not_authorize": ["raw source open", "source/model/actor/FF/N11/N12 rights"],
    }
    j42 = {
        "schema": SCHEMA, "artifact": "j42_addon_endpoint.json",
        "state": "PENDING_PHYSICAL_RETURN",
        "endpoint": "A42_NATIVE_RECEIPT@2.0.0",
        "expected_return_head": None,
        "required_fields": ["receipt_id", "origin_commit", "claim_id", "grade",
                            "coverage", "currentness", "artifacts", "unknown_bounds"],
        "note": "J42 has not published a return head; no J42 product is counted.",
    }
    return f1f8, manifest, md, intake, wake, j42
