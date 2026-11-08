#!/usr/bin/env python3
"""Read-only verification of the C14 combined fan-in content snapshot.

Reads immutable Git objects and C14 text/TSV/JSONL only. Does not execute
source/tests or read respondent/SAV/DTA/DB data. Writes only the C15 lease.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HQ = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq")
PROGRAMMA = "WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1"
OUT = ROOT / PROGRAMMA / "C15_HQ_FANIN_C14_REREVIEW/logs/verify_c14.json"

CONTENT = "f42b73abf2532f9a4ea589e7f80841e15585d8e1"
PROVENANCE = "ea7e878a82e2343591724433fcd6b13910602c84"
C8 = "55fca441d1c674c256473c264cabda48f2df0e52"
BASE = "46104b8ddf44db4d5a32e603ca9332cebbbb1f94"
CANON = f"{PROGRAMMA}/03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl"
ALIAS = f"{PROGRAMMA}/03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl"


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", str(HQ), *args], capture_output=True, check=True).stdout


def show(rev: str, path: str) -> bytes:
    return git("show", f"{rev}:{path}")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_tsv(data: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(data.decode()), delimiter="\t"))


def main() -> int:
    checks: dict[str, bool] = {}
    findings: list[dict[str, object]] = []

    def check(name: str, ok: bool) -> None:
        checks[name] = bool(ok)
        if not ok:
            findings.append({"check": name, "ok": False})

    # Commit identity and separation.
    check("content_commit_exists", git("cat-file", "-t", CONTENT).decode().strip() == "commit")
    check("provenance_commit_exists", git("cat-file", "-t", PROVENANCE).decode().strip() == "commit")
    check("c8_commit_exists", git("cat-file", "-t", C8).decode().strip() == "commit")
    check("c14_parent_is_23a3454b", git("rev-parse", f"{CONTENT}^").decode().strip() == "23a3454b8dc3a6f2824899f6d6ee3bb3a6316521")
    check("provenance_parent_is_content", git("rev-parse", f"{PROVENANCE}^").decode().strip() == CONTENT)
    check("c8_is_ancestor_of_base", subprocess.run(["git", "-C", str(HQ), "merge-base", "--is-ancestor", C8, BASE]).returncode == 0)

    # Canonical/alias 55-case content.
    canon = show(CONTENT, CANON)
    alias = show(CONTENT, ALIAS)
    check("canonical_alias_byte_equal", canon == alias)
    check("canonical_sha_f21823", sha(canon) == "f21823f83e6aed6a64695150bf4ed43df2e7fd88b3310ab26752476acc61a778")
    rows = [json.loads(line) for line in canon.decode().splitlines()]
    check("55_rows", len(rows) == 55)
    check("55_unique_ids", len({r.get("case_id") for r in rows}) == 55)
    fam = Counter(r.get("case_family") for r in rows)
    check("families_1_2_10_2_7_29_4", fam == Counter({"C1": 1, "C2": 2, "C3": 10, "C4": 2, "C5": 7, "C6": 29, "C9": 4}))
    tax = Counter(r.get("frozen_taxonomy_verdict") for r in rows)
    check("taxonomy_25_30", tax == Counter({"FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED": 25, "NOT_RUN": 30}))
    schema_bad = []
    for r in rows:
        miss = [k for k in "ABCDEFGHIJ" if k not in r or str(r[k]).strip() == ""]
        if miss or not str(r.get("forward_walk", "")).strip() or not str(r.get("reverse_walk", "")).strip() or not str(r.get("exact_hold", "")).strip() or not str(r.get("frozen_taxonomy_verdict", "")).strip():
            schema_bad.append((r.get("case_id"), miss))
    check("A_J_schema_all_55", not schema_bad)

    # C8 51-case historical snapshot preservation.
    c8_canon = show(C8, CANON)
    c8_rows = [json.loads(line) for line in c8_canon.decode().splitlines()]
    by8 = {r["case_id"]: r for r in c8_rows}
    by14 = {r["case_id"]: r for r in rows}
    check("c8_51_rows", len(c8_rows) == 51)
    check("c8_03_sha_cc427562", sha(c8_canon) == "cc4275628286f31ba3695d92910f52d639a3f2d54ca7d43852bbd9d12b614251")
    check("c8_ids_all_preserved", set(by8).issubset(by14))
    check("c8_taxonomy_preserved", all(by8[c]["frozen_taxonomy_verdict"] == by14[c]["frozen_taxonomy_verdict"] for c in by8))
    aj_changed = [c for c in by8 if any(by8[c].get(k) != by14[c].get(k) for k in "ABCDEFGHIJ")]
    check("c8_A_J_preserved", not aj_changed)
    check("q3_supplemental_only_F03_F08", {c for c in by14 if "q3_supplemental" in by14[c]} == {"C6-F03_QREL", "C6-F08_Q_USE"})
    for cid in ("C6-F03_QREL", "C6-F08_Q_USE"):
        q = by14[cid].get("q3_supplemental", {})
        check(f"q3_{cid}_no_promotion", q.get("no_promotion") is True and q.get("current_grade_preserved") == "NOT_RUN__UNPROVED_CURRENT_SELECTION")
        check(f"q3_{cid}_original_not_run", q.get("original_historical_run") in ("NOT_OBSERVED", "NOT_RUN"))
        check(f"q3_{cid}_current_unproved", q.get("current_selection") == "UNPROVED_CURRENT_SELECTION")

    # Derived-table counts and ID equality.
    t02 = read_tsv(show(CONTENT, f"{PROGRAMMA}/02_CURRENT_IMPLEMENTATIONS_PRE_FORGE_VS_WHOLE_PREV3.tsv"))
    t05 = read_tsv(show(CONTENT, f"{PROGRAMMA}/05_SEVERED_OR_INCOMPLETE_MINIMAL_OWNER_REPAIRS.tsv"))
    t01 = read_tsv(show(CONTENT, f"{PROGRAMMA}/01_LEGACY_SELECTED_AUTHORITY_USE_AND_INCOMPLETE_CALLEE_COVERAGE.tsv"))
    t08 = read_tsv(show(CONTENT, f"{PROGRAMMA}/08_COVERAGE_DENOMINATORS_COLD_HANDOFF.tsv"))
    cases02 = [r for r in t02 if r.get("ROW_TYPE") == "CASE"]
    check("02_153_rows", len(t02) == 153)
    check("02_55_cases", len(cases02) == 55 and len({r["CASE_ID"] for r in cases02}) == 55)
    check("02_case_ids_equal_03", {r["CASE_ID"] for r in cases02} == set(by14))
    check("02_register_counts", Counter(r["ROW_TYPE"] for r in t02) == Counter({"CASE": 55, "748_CURRENT_OWNER": 30, "FF_REGISTER": 26, "FF_DEPENDENCY": 16, "POST_FF_REGISTER": 15, "POST_FF_SEAM": 11}))
    check("05_55_rows_ids_equal_03", len(t05) == 55 and {r.get("CASE_ID") for r in t05} == set(by14))
    check("01_94_rows", len(t01) == 94)
    check("08_60_rows", len(t08) == 60)
    agenda = read_tsv(show(CONTENT, f"{PROGRAMMA}/07_SECONDARY_AGENDA_NON_DROP_AND_WORKER_COLLISION.md")) if False else None
    # 07 is Markdown; count A01-A17 rows by text.
    agenda_text = show(CONTENT, f"{PROGRAMMA}/07_SECONDARY_AGENDA_NON_DROP_AND_WORKER_COLLISION.md").decode()
    check("17_agenda_gates", all(f"**A{i:02d}**" in agenda_text for i in range(1, 18)))

    # C9 review lineage: reviewed author d540, correction 02a13a5e, review 05a750ad.
    c9 = [r for r in rows if r["case_family"] == "C9"]
    check("4_c9_cases", len(c9) == 4)
    check("c9_source_cut_02a13a5e", all(r.get("source_cut") == "02a13a5e01880835434b30d9a3587147f9dab0de" for r in c9))
    check("c9_review_cut_05a750ad", all(r.get("review_cut") == "05a750ad6bcab8124c1f5d86b8867181fa4ee92c" for r in c9))
    c9_review = show(CONTENT, f"{PROGRAMMA}/C9_P1_EXISTING_SUCCESSOR_INDEPENDENT_REVIEW/REVIEW.json").decode()
    check("c9_review_target_is_d540", '"author_return": "d540cfcc44359f8f78aceccf8afb247c4a7ad80d"' in c9_review)
    check("c9_review_cut_reviews_source_cut", all(r.get("source_cut") == "d540cfcc44359f8f78aceccf8afb247c4a7ad80d" for r in c9))
    check("c9_acceptance_label_qualified", all("AFTER" in str(r.get("hq_disposition", "")) or "CORRECTION" in str(r.get("hq_disposition", "")) for r in c9))

    # C6-F08 exact hold and 04 wording.
    f08 = by14["C6-F08_Q_USE"]
    check("c6_f08_exact_hold_no_quc_reader", "NO_QUC_READER" not in str(f08.get("exact_hold", "")))
    text04 = show(CONTENT, f"{PROGRAMMA}/04_PROVED_EQUIVALENCES_AND_NO_BUILD_DECISIONS.md").decode()
    check("04_no_unqualified_no_quc_reader", "F08 no QUC reader" not in text04)

    # C14 record lineage / terminal criteria wording.
    text00 = show(CONTENT, f"{PROGRAMMA}/00_EXECUTIVE_REAL_OPERATIONS_AND_VERDICT.md").decode()
    text09 = show(CONTENT, f"{PROGRAMMA}/09_INDEPENDENT_REVIEW_REQUEST_AND_EXACT_HEAD.md").decode()
    check("00_c9_non_test_wording_qualified", "real sourcefree non-test API path" not in text00)
    audit = json.loads(show(CONTENT, f"{PROGRAMMA}/C14_POST_C9_C13_FANIN/GOAL_AUDIT.json"))
    crit = {c["criterion_id"]: c["status"] for c in audit["terminal_criteria"]}
    check("00_c8_stale_line_absent", "C8 independent rereview of the C7 correction has **not** been performed" not in text00)
    check("00_base_46104b8d", "46104b8ddf44db4d5a32e603ca9332cebbbb1f94" in text00)
    check("09_base_46104b8d", "46104b8ddf44db4d5a32e603ca9332cebbbb1f94" in text09)
    check("09_no_all_prior_reviewer_gate", "different session from every C1" not in text09)
    check("T6_not_blanket_hold", "NOT RE-ADJUDICATED HERE" not in crit.get("T6", ""))
    check("T3_limit_not_positive", "SATISFIED_AT_ZERO_FULL_EQUIVALENCE_CLAIMS" not in crit.get("T3", ""))
    check("T4_limit_not_positive", "SATISFIED_AT_ZERO_PROVED_SEVERANCES" not in crit.get("T4", ""))

    # Evidence pins.
    c9_cases_sha = sha(show(CONTENT, f"{PROGRAMMA}/C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER/01_CASES.jsonl"))
    c9_ledger_sha = sha(show(CONTENT, f"{PROGRAMMA}/C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER/P1_CANDIDATE_BOUNDARY/04_BOUNDARY_LEDGER.jsonl"))
    c9_review_sha = sha(show(CONTENT, f"{PROGRAMMA}/C9_P1_EXISTING_SUCCESSOR_INDEPENDENT_REVIEW/REVIEW.json"))
    c10_trace_sha = sha(show(CONTENT, f"{PROGRAMMA}/C10_Q3_F03_FIRST_CONSUMER_EFFECT/TRACE.jsonl"))
    c11_trace_sha = sha(show(CONTENT, f"{PROGRAMMA}/C11_Q3_F08_FIRST_CONSUMER_EFFECT/TRACE.jsonl"))
    c12_map_sha = sha(show(CONTENT, f"{PROGRAMMA}/C12_F08_FUNCTIONAL_RESPONSIBILITY/RESPONSIBILITY_MAP.jsonl"))
    c13_map_sha = sha(show(CONTENT, f"{PROGRAMMA}/C13_F03_FUNCTIONAL_RESPONSIBILITY/RESPONSIBILITY_MAP.jsonl"))
    check("c9_cases_sha_e05ed087", c9_cases_sha == "e05ed0876aaba76c9085784b654c4c10b2d3d72771ed2449d5d9247438e41400")
    check("c9_ledger_sha_09964387", c9_ledger_sha == "09964387b58fa94be6783fc6a789a9f5445253eeb28f198d9d865dc57c8b5e49")
    check("c9_review_sha_d56b499e", c9_review_sha == "d56b499e672c7d8094fc955e8035deb90167fc979a8e8c484cef10f1f4ff3b35")
    check("c10_trace_sha_53c2b4ed", c10_trace_sha == "53c2b4ed0ae775682f4ae7b7cd477868d6dc9dadd4d70bf802ce45670cb97184")
    check("c11_trace_sha_6a23bf6a", c11_trace_sha == "6a23bf6a1e99c5fbbe9e0ddeca6ae8c5c52d823e793701ee46e4e85aeed0d22b")
    check("c12_map_sha_5067649b", c12_map_sha == "5067649bbd16a2c95426ae88e112c56da2667029071b53cfc0a48bb8991675a1")
    check("c13_map_sha_66e7ee95", c13_map_sha == "66e7ee95f2d6d02a27d08b238319d0a9ba460129cf8b65bae7cfb34ef4db9ed2")

    # Provenance/content metadata at the pair, not self-hash.
    text09_prov = show(PROVENANCE, f"{PROGRAMMA}/09_INDEPENDENT_REVIEW_REQUEST_AND_EXACT_HEAD.md").decode()
    check("provenance_names_content", CONTENT in text09_prov)
    check("provenance_self_placeholder", "SEE_BRANCH_HEAD__VERIFY_GIT_REV_PARSE_HEAD" in text09_prov)

    report = {
        "schema": "PYAT777_C15_C14_REVIEW_VERIFICATION_V1",
        "reviewer_worktree": str(ROOT),
        "reviewer_branch": git("branch", "--show-current").decode().strip(),
        "reviewer_head": git("rev-parse", "HEAD").decode().strip(),
        "content_snapshot": CONTENT,
        "provenance_commit": PROVENANCE,
        "c8_accepted_content": C8,
        "c8_03_sha256": sha(c8_canon),
        "c14_03_sha256": sha(canon),
        "counts": {
            "cases": len(rows),
            "families": dict(fam),
            "taxonomy": dict(tax),
            "c8_cases": len(c8_rows),
            "02_rows": len(t02),
            "02_case_rows": len(cases02),
            "05_rows": len(t05),
            "01_rows": len(t01),
            "08_rows": len(t08),
        },
        "evidence_pins": {
            "c9_cases": c9_cases_sha,
            "c9_ledger": c9_ledger_sha,
            "c9_review": c9_review_sha,
            "c10_trace": c10_trace_sha,
            "c11_trace": c11_trace_sha,
            "c12_map": c12_map_sha,
            "c13_map": c13_map_sha,
        },
        "terminal_criteria": crit,
        "checks": checks,
        "failed_checks": findings,
        "failed_check_count": len(findings),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    print("C14_CONTENT_SNAPSHOT_VERIFICATION")
    print(f"content={CONTENT}")
    print(f"provenance={PROVENANCE}")
    print(f"c8={C8} c8_03_sha={sha(c8_canon)} c14_03_sha={sha(canon)}")
    print(f"cases={len(rows)} unique={len({r['case_id'] for r in rows})} families={dict(fam)}")
    print(f"taxonomy={dict(tax)}")
    print(f"c8_rows={len(c8_rows)} 02_rows={len(t02)} 02_cases={len(cases02)} 05_rows={len(t05)} 01_rows={len(t01)} 08_rows={len(t08)}")
    print(f"terminal={crit}")
    print(f"failed_check_count={len(findings)}")
    for f in findings:
        print("FAILED_CHECK", json.dumps(f, sort_keys=True))
    print("PASS" if not findings else "REVISE_REQUIRED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
