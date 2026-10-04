"""HQ196-R1 — emit the successor instrument, crosswalk and return packet.

Documentary only. Reads historical artifacts; writes the repaired instrument.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

COURT = Path(__file__).resolve().parent
sys.path.insert(0, str(COURT))

import hq196_successor_generator as G  # noqa: E402
import hq196_successor_model as M  # noqa: E402

RET = COURT.parents[4] / "WORKER_RETURNS" / "PYAT-HQ196-R9-WARRANT-ACCOUNTING-SUCCESSOR-R1"
LAW = G.LAW
C4B = G.C4B
C4C = G.C4C

# C4B requirement key -> successor account name
C4B_MAP = {
    "full_file_sha256_passes": "full_file_sha256_passes",
    "path_opens": "path_level_opens",
    "decoder_invocations": "decoder_invocations",
    "metadata_header_reads": "metadata_reads",
    "selected_reads": "selected_column_reads",
    "full_reads": "full_reads",
    "retries": "retries",
}
SPLIT_NOTE = ("SPLIT_BY_SETTLED_O1_C07_LAW: C4B carried one combined 'metadata_header_reads' account. "
              "The settled law names 'metadata reads' and 'header-prefix reads' as separate mandatory accounts, "
              "so the combined term was split rather than restated.")


def w(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")
    print(f"wrote {path.relative_to(COURT.parents[4])}")


def crosswalk(successor: dict) -> dict:
    c4b_by_key = {s["source_key"]: s["source_access_accounting"] for s in C4B["sources"]}
    rows = []
    for s in successor["sources"]:
        k = s["source_key"]
        accts = {a["account_name"]: a for a in s["source_access_accounting"]["accounts"]}
        c4b_block = c4b_by_key[k]
        seen = set()

        for c4b_name, requirement in c4b_block.items():
            succ_name = C4B_MAP[c4b_name]
            a = accts[succ_name]
            seen.add(succ_name)
            if c4b_name == "metadata_header_reads":
                split = accts.get("header_prefix_reads")
                rows.append({
                    "source_key": k,
                    "c4b_account": c4b_name,
                    "c4b_requirement_token": requirement,
                    "c4_candidate_state": "DROPPED__DQ01",
                    "successor_accounts": [succ_name] + (["header_prefix_reads"] if split else []),
                    "successor_budget_types": {
                        succ_name: a["expected_pre_launch_budget"]["budget_type"],
                        **({"header_prefix_reads": split["expected_pre_launch_budget"]["budget_type"]} if split else {}),
                    },
                    "repair_action": "RESTORED_AND_SPLIT",
                    "note": SPLIT_NOTE if split else None,
                })
            else:
                rows.append({
                    "source_key": k,
                    "c4b_account": c4b_name,
                    "c4b_requirement_token": requirement,
                    "c4_candidate_state": "DROPPED__DQ01",
                    "successor_accounts": [succ_name],
                    "successor_budget_types": {succ_name: a["expected_pre_launch_budget"]["budget_type"]},
                    "repair_action": "RESTORED",
                    "note": None,
                })

        for name, a in accts.items():
            if name in seen:
                continue
            rows.append({
                "source_key": k,
                "c4b_account": None,
                "c4b_requirement_token": None,
                "c4_candidate_state": "DROPPED__DQ01",
                "successor_accounts": [name],
                "successor_budget_types": {name: a["expected_pre_launch_budget"]["budget_type"]},
                "repair_action": "ADDED_BY_SETTLED_O1_C07_LAW",
                "note": ("Not named as a separate C4B account. Required by the settled O1-C07 mandatory-separate-"
                         "account list, or by a per-source frozen value."),
            })

    return {
        "schema": "PYAT_HQ196_C4B_TO_SUCCESSOR_ACCOUNTING_CROSSWALK@1.0.0",
        "purpose": "Exact crosswalk for the DQ-01 repair: what C4B required, what the C4 candidate dropped, "
                   "and what the successor binds in its place.",
        "sources": {
            "c4b_unsigned_template": G.P_C4B,
            "c4_warrant_candidate": G.P_C4,
            "o1_c07_accounting_law": G.P_LAW,
            "hq196_adjudication": G.P_ADJ,
        },
        "dq01_evidence": {
            "c4b_block_present_for_all_seven": True,
            "c4_candidate_block_present_for_any": False,
            "verification": "Read directly from the exact git objects; see 01_HISTORICAL_TO_SUCCESSOR_CROSSWALK.json.",
        },
        "row_count": len(rows),
        "rows": rows,
    }


def bound_vs_pending(successor: dict) -> dict:
    bound, pending = [], []
    for s in successor["sources"]:
        for a in s["source_access_accounting"]["accounts"]:
            b = a["expected_pre_launch_budget"]
            row = {
                "source_key": s["source_key"],
                "account": a["account_name"],
                "budget_type": b["budget_type"],
                "budget_value": b["budget_value"],
                "budget_expression": b["budget_expression"],
                "provenance": a["provenance"],
            }
            if b["budget_type"] == "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE":
                row["pending_dependency"] = a.get("pending_dependency")
                row["derivation_note"] = a.get("derivation_note")
                pending.append(row)
            else:
                if a.get("reviewer_confirmation_required"):
                    row["reviewer_confirmation_required"] = True
                if a.get("derivation_note"):
                    row["derivation_note"] = a["derivation_note"]
                bound.append(row)

    by_type: dict[str, int] = {}
    for s in successor["sources"]:
        for a in s["source_access_accounting"]["accounts"]:
            t = a["expected_pre_launch_budget"]["budget_type"]
            by_type[t] = by_type.get(t, 0) + 1

    return {
        "schema": "PYAT_HQ196_BOUND_VALUES_AND_PENDING_VALUES@1.0.0",
        "principle": "Only values already frozen by authority are bound. Everything else is typed as a blocker, "
                     "never invented and never null.",
        "totals": {
            "accounts_total": len(bound) + len(pending),
            "bound": len(bound),
            "pending": len(pending),
            "by_budget_type": by_type,
        },
        "bound_values": bound,
        "pending_values": pending,
        "pending_value_law": {
            "representation": "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE",
            "is_a_null": False,
            "waives_nothing": True,
            "blocks_issuance": True,
            "difference": "A null would silently waive a launch prerequisite. A typed pending value records that "
                          "authority named the account but has not yet supplied a number, and it keeps the "
                          "account visible as a blocker.",
        },
        "explicitly_not_invented": {
            "path_open_budgets": "Not invented for any source. SRC27's authority wording 'multiple' is recorded "
                                 "verbatim and not converted to a number.",
            "decoder_invocation_counts": "Not invented for any source.",
            "byte_ceilings": "Not invented for any source.",
            "src27_selected_reads": "Not invented, per commission.",
        },
        "floors_not_promoted": {
            "src27_accounts_bound_as_floor": ["source_path_existence_access_checks", "full_file_sha256_passes",
                                              "metadata_reads", "full_reads"],
            "authority_wording": "The hardened note says the run 'will require at minimum' each of these.",
            "promotion_to_ceiling": "PROHIBITED. No maximum is supplied for these four accounts.",
        },
    }


def blocker_matrix(successor: dict) -> dict:
    inv = M.check_invariants(successor)
    pend = [r for r in bound_vs_pending(successor)["pending_values"]]
    hist = C4C["issuance_blockers_summary"]
    return {
        "schema": "PYAT_HQ196_ISSUANCE_BLOCKER_MATRIX@1.0.0",
        "statement": "This lane cannot close R9 and cannot issue the warrant. Every blocker below remains OPEN.",
        "carried_from_c4_candidate": [{"blocker": b, "status": "OPEN", "still_open": True} for b in hist],
        "documentary_blockers": [
            {"id": "DQ-01", "status": "REPAIRED_IN_THIS_LANE",
             "statement": "C4 candidate dropped C4B's per-source source_access_accounting block.",
             "resolution": "Restored for all seven fresh-read sources, under the settled two-stage O1-C07 law.",
             "note": "Restoring the fields does NOT close any technical account and authorizes nothing."},
        ],
        "technical_blockers_still_open": [
            {"id": "R9-SEL-03", "token": G.PENDING_SEL, "status": "OPEN",
             "statement": "The frozen selected_reads=1 budgets for SRC02/SRC06/SRC14 have no implementation owner; "
                          "the bound reader exposes no usecols argument.",
             "effect": "Budgets remain bound EXACT at 1 and are NOT relaxed. The missing owner is a blocker, not "
                       "grounds to change the budget.",
             "accounts_affected": ["SRC02/selected_column_reads", "SRC06/selected_column_reads",
                                   "SRC14/selected_column_reads", "SRC27/selected_column_reads"]},
            {"id": "R9-BROKER-ACCEPT", "token": G.PENDING_BROKER, "status": "OPEN",
             "statement": "Path-open, existence-check, decoder-invocation and byte accounts await broker "
                          "implementation acceptance.",
             "effect": "Typed UNBOUND_PENDING_TECHNICAL_ACCEPTANCE. Not null, not invented.",
             "pending_account_count": len(pend)},
        ],
        "counts": {
            "accounts_awaiting_a_bound_value": len(pend),
            "instrument_invariants_passing": len([r for r in inv if r["ok"]]),
            "instrument_invariants_failing": len([r for r in inv if not r["ok"]]),
        },
        "issuance_gate": {
            "may_this_lane_issue": False,
            "may_this_lane_authorize_access": False,
            "may_this_lane_close_R9": False,
            "required_before_issuance": [
                "All seven access locators filled by HQ or the accountable resource owner. No search was performed here.",
                "HQ approval recorded.",
                "Required user/resource-owner approval recorded.",
                "Instrument signed.",
                "R9-SEL-03 closed: a selected-reader implementation exists that performs the frozen operation.",
                "R9-BROKER-ACCEPT closed: path-open, decoder and byte accounts carry accepted numeric budgets.",
                "Independent integration review of the freeze completed.",
            ],
        },
    }


def schema_doc(successor: dict) -> dict:
    return {
        "schema": "PYAT_HQ196_PER_SOURCE_ACCOUNTING_SCHEMA@1.0.0",
        "settled_law": {
            "two_stage": {
                "stage_1_pre_launch_FROZEN": ["expected_pre_launch_budget", "measurement_basis", "stop_condition",
                                              "provenance"],
                "stage_2_during_run_MEASURED_RETAINED_ON_RETURN": ["runtime_observed_exact_count"],
                "never_merged": True,
                "why": "REQUIRED_EXACT_COUNT means the budget must be exact BEFORE launch. It does NOT mean the "
                       "observed number must already have been observed before launch.",
            },
            "non_substitutability": "Literal path opens, reader invocations and decoder invocations are separately "
                                    "named, non-substitutable quantities. A higher-level proxy may not be renamed "
                                    "path_opens.",
        },
        "account_object_shape": {
            "account_name": "string — stable account identifier",
            "layer": "string — the layer at which the quantity is counted",
            "expected_pre_launch_budget": {
                "budget_type": "EXACT | MAX | ZERO | FLOOR | UNBOUND_PENDING_TECHNICAL_ACCEPTANCE",
                "budget_value": "integer, or null ONLY when budget_type is UNBOUND_PENDING_TECHNICAL_ACCEPTANCE",
                "budget_expression": "string, used when the authority states the budget in words",
                "frozen_before_launch": "always true",
                "may_be_null": "always false — the budget object itself is never null or absent",
            },
            "measurement_basis": {
                "what_measured": "required — what quantity is being counted",
                "layer": "required — at which layer",
                "mechanism": "required — by what mechanism, or PENDING: <owner to be established>",
                "point_in_run": "required — at what point in the run",
            },
            "runtime_observed_exact_count": {
                "value": "integer, or null before execution",
                "status": "NOT_EXECUTED | OBSERVED",
                "typed_reason": "required whenever value is null",
                "null_permitted_by_law": "true — return metric only",
                "must_not_be_read_as": "a zero, an empty result, or a PASS",
            },
            "stop_condition_if_exceeded": "required",
            "provenance": "required — list of exact artifact@commit:json.path citations",
            "pending_dependency": "optional — typed token when the value awaits technical acceptance",
        },
        "budget_type_vocabulary": M.BUDGET_TYPES_DOC,
        "typed_null_law": {
            "return_metric": M.RETURN_METRIC_NULL_LAW,
            "pre_launch_budget": M.PRE_LAUNCH_BUDGET_NULL_LAW,
            "machine_readable_rule": successor["typed_null_law"]["machine_readable_rule"],
        },
        "mandatory_separate_accounts": M.MANDATORY_SEPARATE_ACCOUNTS,
        "accounts_present_per_source": {
            s["source_key"]: [a["account_name"] for a in s["source_access_accounting"]["accounts"]]
            for s in successor["sources"]
        },
    }


def invariants_doc(successor: dict) -> dict:
    res = M.check_invariants(successor)
    return {
        "schema": "PYAT_HQ196_INVARIANTS@1.0.0",
        "all_pass": all(r["ok"] for r in res),
        "count": len(res),
        "failed": [r for r in res if not r["ok"]],
        "results": res,
        "how_verified": "hq196_successor_model.check_invariants, executed against the emitted instrument. "
                        "Re-runnable; not a narrative assertion.",
    }


def main() -> None:
    s = G.build_successor()

    w(COURT / "01_UNSIGNED_SUCCESSOR.json", s)
    cw = crosswalk(s)
    w(COURT / "02_C4B_TO_SUCCESSOR_ACCOUNTING_CROSSWALK.json", cw)

    # ---- return packet ----
    w(RET / "01_HISTORICAL_TO_SUCCESSOR_CROSSWALK.json", {
        "schema": "PYAT_HQ196_HISTORICAL_TO_SUCCESSOR_CROSSWALK@1.0.0",
        "purpose": "Full lineage: every historical input to the successor, what it contributed, and what it did not.",
        "historical_inputs": [
            {"role": "documentary_base", "commit": "d43756fb3c80645ac887cca90026ecbdb10dd18c",
             "artifact": "HQ196_R9_THREE_WAY_ADJUDICATION_R1.md",
             "contributed": ["settled two-stage O1-C07 contract meaning", "non-substitutability of path opens / "
                             "reader invocations / decoder invocations", "REQUIRED_EXACT_COUNT interpretation",
                             "R9-SEL-03 selected-read implementation mismatch", "DQ-01 documentary finding",
                             "eight outstanding broker proof items"],
             "did_not_contribute": ["any numeric budget"]},
            {"role": "c4b_unsigned_template", "commit": "c2af4f61d68e9803af83f8e26f633acfe31062fa",
             "artifact": "WORKER_RETURNS/PYAT-C4B-WORKLOAD-ORACLE-FREEZE-R1/07_UNSIGNED_SOURCE_WARRANT_TEMPLATE.json",
             "contributed": ["the seven-source scope", "the per-source source_access_accounting block DQ-01 restored",
                             "SRC26 raw_nominal_case_size 174 and decoded_dictionary_data_width 332",
                             "preconditions", "retry_stop_law", "retention_privacy", "semantic_ceilings"],
             "did_not_contribute": ["numeric account budgets (C4B carried only requirement TOKENS)"]},
            {"role": "c4_warrant_candidate", "commit": "8ff40d37de69db2d8a6053a7c2242f481677f1a4",
             "artifact": "WORKER_RETURNS/PYAT-C4-EXECUTABLE-FREEZE-FANIN-R1/04_SOURCE_EXECUTION_WARRANT_CANDIDATE.json",
             "contributed": ["per-source identity, reader lanes, allowed operations, authority bindings",
                             "resolved execution surface", "zero_authorizations", "issuance blockers",
                             "SRC27 route-pass and accounting_warning"],
             "did_not_contribute": ["source_access_accounting — DROPPED, the DQ-01 defect"]},
            {"role": "o1_c07_accounting_law", "commit": "8ff40d37de69db2d8a6053a7c2242f481677f1a4",
             "artifact": "WORKER_RETURNS/PYAT-C4-EXECUTABLE-FREEZE-FANIN-R1/07_EXECUTION_ACCOUNTING_AND_FAILURE_LAW.json",
             "contributed": ["the ten mandatory separate accounts", "frozen zero budgets",
                             "per-source expected operation classes and frozen values",
                             "SRC26 expected_header_prefix_bytes 176", "SRC27 'at minimum' floors",
                             "measurement_basis_requirement", "typed-null reporting law"],
             "did_not_contribute": ["path-open, decoder or byte budgets — none supplied"]},
        ],
        "frozen_values_bound": [
            "retries = 0 (ZERO) for all seven sources",
            "SRC02/SRC06/SRC14 selected_column_reads = 1 (EXACT), full_reads = 0 (EXACT)",
            "SRC08/SRC12 metadata_reads = 1 (EXACT), selected_column_reads = 0, row_data_reads = 0, selected_columns = 0",
            "SRC26 header_prefix_bytes = 176 (EXACT) at its declared account",
            "SRC27 governed_full_route_passes = 1 (EXACT, max 1), retries = 0",
            "SRC27 existence/hash/metadata/full accounts = FLOOR 1 from the 'at minimum' wording",
            "SRC35 fresh_reads = 0 and excluded from the seven",
        ],
        "values_deliberately_not_bound": {
            "path_open_budgets": "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE on all seven",
            "decoder_invocation_counts": "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE on all seven",
            "byte_ceilings": "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE on all seven",
            "src27_selected_reads": "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE — commission forbids inventing it",
            "src27_path_opens": "UNBOUND — authority says 'multiple' and deliberately supplies no number",
        },
        "accounting_crosswalk": cw,
        "totals": bound_vs_pending(s)["totals"],
    })

    w(RET / "02_PER_SOURCE_ACCOUNTING_SCHEMA.json", schema_doc(s))
    w(RET / "03_BOUND_VALUES_AND_PENDING_VALUES.json", bound_vs_pending(s))
    w(RET / "04_ISSUANCE_BLOCKER_MATRIX.json", blocker_matrix(s))
    w(RET / "05_INVARIANTS.json", invariants_doc(s))
    print("\nall invariants pass:", invariants_doc(s)["all_pass"])


if __name__ == "__main__":
    main()
