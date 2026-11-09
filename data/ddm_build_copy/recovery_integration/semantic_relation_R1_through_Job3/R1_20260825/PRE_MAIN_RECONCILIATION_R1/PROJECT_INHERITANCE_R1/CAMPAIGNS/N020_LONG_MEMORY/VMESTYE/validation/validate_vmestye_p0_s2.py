#!/usr/bin/env python3
"""Stage-aware VMESTYE P0 structural validator.

This validator is separate from the protected pre-dispatch bootstrap script. It
checks the corrected P0 assembly at its actual returned heads and never treats
source identity as functional, scientific, native, actor or protected acceptance.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

CENSUS_HEADER = [
    "census_id", "estate_id", "source_commit_sha", "source_path", "source_blob_sha",
    "source_row_locator", "source_exact_id", "source_composite_id", "record_grain",
    "branch_name_or_commit_only", "live_head_sha_if_verified",
    "current_branch_or_protected_status", "source_grade", "source_read_depth",
    "negative_status", "candidate_current_owner", "related_RM_ids",
    "related_LMX_LMQ_F_AR_ids", "related_programma_ids",
    "related_sorok_recipient_ids", "duplicate_alias_of", "join_state",
    "missing_link_type", "next_owner", "evidence_id",
]
AJ_HEADER = [
    "check_id", "estate_id", "source_ref", "source_grain", "expected_count",
    "observed_input_count", "observed_output_count", "duplicate_count",
    "source_minus_output_ids", "output_minus_source_ids", "aliases_distinguished",
    "unjoined_ids", "ambiguous_join_ids", "unread_ids", "branch_only_ids",
    "negative_ids", "count_verdict", "semantic_verdict", "owner", "falsifier",
    "evidence_id",
]
COVERAGE_HEADER = [
    "receipt_id", "estate_id", "source_sha", "source_blob_sha", "key_extraction_rule",
    "source_id_digest", "sorted_output_id_digest", "input_count", "output_count",
    "missing_count", "extra_count", "duplicate_count", "overlap_or_subset_relation",
    "reader_and_method", "review_status", "proof_ceiling", "negative_cases",
]
RM_HEADER = [
    "frozen_check_id", "zl01_reported_check_id", "source_rm_id",
    "authoritative_census_estate_id", "authoritative_census_source_exact_id",
    "migration_rule", "current_receiving_state",
]
G4_CONTRACT_HEADER = [
    "edge_id", "source_commit_sha", "source_path", "source_blob_sha",
    "source_row_1based", "original_requiredness", "original_predicate",
    "original_G2_kind", "original_G2_edge_condition",
]
G4_RECEIPT_HEADER = [
    "source_commit_sha", "source_blob_sha", "source_path", "source_row_ordinal",
    "census_estate_id", "census_source_exact_id", "original_requiredness",
    "original_predicate", "original_g2_kind", "original_g2_edge_condition",
    "original_g2_evidence_pointer", "retained_negative", "exact_row_verdict",
    "semantic_verdict",
]
P1_HEADERS = {
    "OPERATION_TRACES.tsv": [
        "prong_id", "trace_id", "finding_id", "census_id", "estate_id",
        "source_commit_sha", "source_path", "source_composite_id", "source_grain",
        "input_source_ref", "input_semantics", "selected_rule_ref",
        "transformation_human_language", "output_object", "producer_edge_id",
        "first_consumer_id", "first_consumer_evidence_id", "negative_or_refusal",
        "execution_status", "proof_grade", "missing_next_edge",
    ],
    "AUTHORITY_USE.tsv": [
        "prong_id", "authority_use_id", "finding_id", "trace_id", "authority_id",
        "authority_rule_source_ref", "applicability_predicate", "rule_available",
        "rule_selected_for_scope", "rule_applied_to_output", "refusal_enforced",
        "resulting_output_ref", "first_consumer_evidence_id", "authority_status",
        "proof_grade", "falsifier",
    ],
    "EVIDENCE.tsv": [
        "prong_id", "evidence_id", "finding_id", "census_id", "estate_id",
        "source_commit_sha", "source_blob_sha", "source_path", "source_row_locator",
        "source_composite_id", "source_grain", "claim_kind", "claim_supported",
        "evidence_kind", "observed_cut", "proof_grade", "original_native_status",
        "negative_or_refusal", "independent_review_ref",
    ],
    "COVERAGE.tsv": [
        "prong_id", "coverage_id", "census_id", "estate_id", "source_commit_sha",
        "source_path", "source_composite_id", "source_grain", "finding_id",
        "trace_presence", "authority_presence", "evidence_presence",
        "first_consumer_presence", "coverage_status", "missing_joins", "next_owner",
    ],
    "UNJOINS.tsv": [
        "prong_id", "unjoin_id", "census_id", "estate_id", "source_commit_sha",
        "source_path", "source_composite_id", "source_grain", "finding_id",
        "join_target_type", "attempted_target_id", "failure_code",
        "candidate_aliases", "evidence_id", "negative_preserved",
        "unresolved_question", "next_owner", "falsifier", "status",
    ],
}
STAGES = (
    "PREPARED",
    "DISPATCHED_BY_USER",
    "ACTIVE_VERIFIED",
    "RETURNED_AT_SHA",
    "INDEPENDENT_REVIEWED",
    "ACCEPTED_TO_VMESTYE",
)
STAGE_HEADER = [
    "subject_id", "author_actor", "branch", "candidate_head_sha", "stage",
    "review_actor", "reviewer_head_sha", "reviewed_candidate_head_sha",
    "review_verdict", "independent", "protected_adoption_sha",
    "runner_authorization", "runner_id", "host", "model", "effort", "s3_authorized",
]
ASSEMBLY_HEADER = [
    "relative_path", "base_protected_commit", "source_commit_sha",
    "source_blob_sha", "action", "sha256", "overlap_status",
]


def digest_keys(keys: Iterable[Iterable[Any]]) -> str:
    material = "\n".join(sorted(json.dumps(list(k), separators=(",", ":")) for k in keys)) + "\n"
    return "sha256:" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def key_tuple(value: str) -> tuple[Any, ...]:
    parsed = json.loads(value)
    if not isinstance(parsed, list):
        raise ValueError("composite key must be a JSON array")
    return tuple(parsed)


def parse_int(value: Any, name: str) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} is not an integer: {value!r}") from exc


def json_list(value: str, name: str) -> list[Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{name} is not JSON: {value!r}") from exc
    if not isinstance(parsed, list):
        raise ValueError(f"{name} is not a JSON list")
    return parsed


class SourceRepo:
    def __init__(self, root: Path):
        self.root = root
        self._cache: dict[tuple[str, str], bytes] = {}
        self._blob_cache: dict[str, bytes] = {}

    def show(self, commit: str, path: str) -> bytes:
        key = (commit, path)
        if key not in self._cache:
            proc = subprocess.run(
                ["git", "-C", str(self.root), "show", f"{commit}:{path}"],
                capture_output=True,
                check=False,
            )
            if proc.returncode != 0:
                raise FileNotFoundError(f"source unavailable: {commit}:{path}: {proc.stderr.decode()[:240]}")
            self._cache[key] = proc.stdout
        return self._cache[key]

    def blob(self, sha: str) -> bytes:
        if sha not in self._blob_cache:
            proc = subprocess.run(
                ["git", "-C", str(self.root), "cat-file", "blob", sha],
                capture_output=True,
                check=False,
            )
            if proc.returncode != 0:
                raise FileNotFoundError(f"source blob unavailable: {sha}")
            self._blob_cache[sha] = proc.stdout
        return self._blob_cache[sha]


class Validator:
    def __init__(self, root: Path, git_root: Path, source_root: Path | None = None):
        self.root = root
        self.git = SourceRepo(git_root)
        self.source_root = source_root
        self.failures: list[tuple[str, str]] = []
        self.checks: list[dict[str, str]] = []

    def check(self, check_id: str, ok: bool, detail: str) -> bool:
        status = "PASS" if ok else "FAIL"
        self.checks.append({"check_id": check_id, "status": status, "detail": detail})
        if not ok:
            self.failures.append((check_id, detail))
        return ok

    def hold(self, check_id: str, detail: str) -> None:
        self.checks.append({"check_id": check_id, "status": "HOLD", "detail": detail})
        self.failures.append((check_id, detail))

    def read_table(self, rel: str, header: list[str], check_id: str) -> list[dict[str, str]]:
        path = self.root / rel
        if not path.is_file():
            self.hold(check_id, f"missing {rel}")
            return []
        try:
            with path.open(encoding="utf-8", newline="") as handle:
                raw = list(csv.reader(handle, delimiter="\t", strict=True))
        except (OSError, csv.Error) as exc:
            self.hold(check_id, f"cannot parse {rel}: {exc}")
            return []
        if not raw:
            self.hold(check_id, f"empty {rel}")
            return []
        if raw[0] != header:
            self.check(check_id, False, f"{rel}: header mismatch")
            return []
        rows = []
        for number, row in enumerate(raw[1:], 2):
            if len(row) != len(header):
                self.check(check_id, False, f"{rel}:{number}: width {len(row)} != {len(header)}")
                continue
            rows.append(dict(zip(header, row)))
        self.check(check_id, True, f"{rel}: {len(rows)} rows, {len(header)} columns")
        return rows

    def source_keys(self, estate: str, commit: str, path: str) -> set[tuple[Any, ...]]:
        text = self.git.show(commit, path).decode("utf-8")
        base = Path(path).name
        if estate in ("LMX44", "LMQ30"):
            rows = list(csv.DictReader(text.splitlines()))
            field = "obligation_id" if estate == "LMX44" else "queue_id"
            return {(row[field],) for row in rows}
        if estate in ("C6_F29", "C6_AR58", "C6_AUX7"):
            rows = list(csv.DictReader(text.splitlines(), delimiter="\t"))
            wanted = {"C6_F29": {"FUNCTION"}, "C6_AR58": {"RELEASE"}, "C6_AUX7": {"DENOMINATOR", "CROSSREF"}}[estate]
            return {(row["ROW_TYPE"], row["ID"]) for row in rows if row["ROW_TYPE"] in wanted}
        if estate == "C777_CASE55":
            return {(row["case_id"],) for row in map(json.loads, text.splitlines()) if row}
        if estate == "PROG_COMPONENT62":
            return {(row["id"],) for row in map(json.loads, text.splitlines()) if row}
        if estate == "PROG_SEAM82":
            return {(row["edge_id"],) for row in map(json.loads, text.splitlines()) if row}
        if estate == "PROG_OWNER345":
            return {(row["origin_key"],) for row in map(json.loads, text.splitlines()) if row}
        if estate == "PROG_GAP49":
            return {(gap,) for gap in set(re.findall(r"GAP-\d{3}", text))}
        if estate == "SECTIONS11":
            match = re.match(r"(\d{2})_", base)
            return {(f"S{match.group(1)}",)} if match else set()
        if estate == "R157_SOURCES35":
            return {(row["source_id"],) for row in json.loads(text)["sources"]}
        if estate == "RECENT_CAMPAIGN30":
            return {(row["record_id"],) for row in csv.DictReader(text.splitlines(), delimiter="\t")}
        if estate in ("PYAT_SR01_2416", "PYAT_SR01_UNRESOLVED373"):
            rows = [row for row in map(json.loads, text.splitlines()) if row]
            if estate.endswith("UNRESOLVED373"):
                rows = [row for row in rows if row.get("spine_relation") == "UNRESOLVED"]
            return {
                (row["row_kind"], row["source_registry"], row["source_record_id"],
                 row["source_row_1_based"], row["target_modern_requirement_or_section"])
                for row in rows
            }
        if estate in ("SOROK_SR01_1314", "SOROK_SR01_UNRESOLVED51"):
            rows = [row for row in map(json.loads, text.splitlines()) if row]
            if estate.endswith("UNRESOLVED51"):
                rows = [row for row in rows if row.get("spine_relation") == "UNRESOLVED"]
            return {
                (row["source_registry"], row["source_record_id"],
                 row["target_modern_requirement_or_stage"])
                for row in rows
            }
        if estate == "SOROK_ASSETS304":
            return {(row["id"],) for row in json.loads(text)["assets"]}
        if estate == "SOROK_FUNCTION144":
            return {(row["id"],) for row in json.loads(text)["records"]}
        if estate == "SOROK_W1_INPUT100":
            return {(row["source_row_id"],) for row in map(json.loads, text.splitlines()) if row}
        if estate == "SOROK_VERSIONED_SEAM38":
            return {(row["seam_id"],) for row in map(json.loads, text.splitlines()) if row and row.get("record_type") == "VERSIONED_SEAM"}
        if estate == "SOROK_PHASE_GATES83":
            return {(row["gate_id"],) for row in map(json.loads, text.splitlines()) if row and row.get("record_type") == "GATE"}
        if estate == "SOROK_SOURCE_INDEX_ONLY48":
            return {(value,) for value in json.loads(text)["source_depth"]["still_index_only_ids"]}
        if estate.startswith("D0"):
            rows = list(csv.reader(text.splitlines()))
            return {(base, row[0], number) for number, row in enumerate(rows[1:], 2) if row}
        if estate == "VMESTYE_COMMISSION21":
            return {(row["commission_id"],) for row in csv.DictReader(text.splitlines(), delimiter="\t")}
        if estate == "VMESTYE_FLIGHTS18":
            return {(row["worker_id"],) for row in csv.DictReader(text.splitlines(), delimiter="\t")}
        if estate == "VMESTYE_GATES9":
            return {(row["gate_id"],) for row in csv.DictReader(text.splitlines(), delimiter="\t")}
        raise KeyError(f"no source key builder for {estate}")

    def validate_census(self) -> tuple[list[dict[str, str]], dict[str, list[dict[str, str]]]]:
        rows = self.read_table("CONTROL/P0_RETURN_AND_BRANCH_CENSUS.tsv", CENSUS_HEADER, "A_CENSUS_HEADER")
        ids = [row["census_id"] for row in rows]
        self.check("A_CENSUS_ID", len(ids) == len(set(ids)), "census_id must be unique")
        full_ids = [
            (row["estate_id"], row["source_commit_sha"], row["source_path"],
             row["source_blob_sha"], row["source_exact_id"], row["source_composite_id"])
            for row in rows
        ]
        self.check("A_CENSUS_COMPOSITE_UNIQUE", len(full_ids) == len(set(full_ids)),
                   "full source composite identity must be unique")
        self.check("A_CENSUS_NEGATIVE", all(row["negative_status"].strip() for row in rows),
                   "every census row must retain a typed negative/status")
        groups: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            groups[row["estate_id"]].append(row)
        source_ok = True
        for estate, estate_rows in sorted(groups.items()):
            expected: set[tuple[Any, ...]] = set()
            try:
                for commit, path in sorted({(row["source_commit_sha"], row["source_path"]) for row in estate_rows}):
                    expected |= self.source_keys(estate, commit, path)
            except Exception as exc:
                source_ok = False
                self.check(f"A_SOURCE_KEYS:{estate}", False, f"source key extraction failed: {exc}")
                continue
            observed = {key_tuple(row["source_composite_id"]) for row in estate_rows}
            missing = sorted(expected - observed)
            extra = sorted(observed - expected)
            ok = expected == observed
            if not ok:
                source_ok = False
                self.check(
                    f"A_SOURCE_KEYS:{estate}", False,
                    f"source/output key mismatch missing={missing[:8]} extra={extra[:8]} "
                    f"expected={len(expected)} observed={len(observed)}",
                )
        expected_total = sum(len(self.source_keys(estate, commit, path)) for estate, estate_rows in groups.items() for commit, path in {(row["source_commit_sha"], row["source_path"]) for row in estate_rows})
        self.check("A_CENSUS_COUNT", len(rows) == expected_total, f"observed {len(rows)} census rows; source-derived expected {expected_total}")
        if source_ok:
            self.check("A_SOURCE_KEY_SETS", True, "all 32 census estates exactly equal their source key sets")
        return rows, groups

    def external_source_count(self, check_id: str, source_ref: str) -> int | None:
        if not source_ref or "://" in source_ref:
            return None
        if source_ref.startswith("AJ-"):
            return None
        if "::" in source_ref:
            commit, path = source_ref.split("::", 1)
            path = path.split("#", 1)[0]
            if not path or path.endswith("/D02") or path.endswith("/D03") or path.endswith("/D04") or path.endswith("/D05") or path.endswith("/D06") or path.endswith("/D07") or path.endswith("/SECTIONS/"):
                return None
            try:
                text = self.git.show(commit, path).decode("utf-8")
            except Exception:
                return None
            return self.count_source_text(check_id, path, text)
        if re.fullmatch(r"[0-9a-f]{40}", source_ref):
            try:
                data = self.git.blob(source_ref)
            except Exception:
                return None
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                return None
            return self.count_source_text(check_id, "", text)
        return None

    def count_source_text(self, check_id: str, path: str, text: str) -> int | None:
        if check_id.startswith("SOROK_SRC_14_"):
            kind = check_id.rsplit(":", 1)[-1]
            rows = [json.loads(line) for line in text.splitlines() if line.strip()]
            if kind == "MANIFEST":
                return sum(row.get("record_type") == "MANIFEST" for row in rows)
            return sum(row.get("record_type") == kind for row in rows)
        if check_id == "SOROK_SRC_07_GITHUB_ACCESSIBLE_ASSET_LOCATOR_R1.json":
            return len(json.loads(text)["assets"])
        if check_id == "SOROK_SRC_09_INHERITED_144_FUNCTIONS_TO_WORKING_SPINE_R1.json":
            return len(json.loads(text)["records"])
        if check_id == "SOROK_SRC_12_W1_W2_INPUT_DISPOSITIONS_R1.jsonl":
            return len([line for line in text.splitlines() if line.strip()])
        if check_id == "SOROK_SRC_08_INITIAL_EVIDENCE_GRADED_DEPENDENCY_AND_SEAM_REGISTER_R1.json:ORIGINAL_E":
            return len(json.loads(text).get("original_E", []))
        if check_id == "SOROK_SRC_08_INITIAL_EVIDENCE_GRADED_DEPENDENCY_AND_SEAM_REGISTER_R1.json:ORIGINAL_D":
            return len(json.loads(text).get("original_D", []))
        if check_id == "SOROK_SRC_15_W7_VERSIONED_SEAMS_AND_GATE_JOIN_CANDIDATES_R1.jsonl":
            return len([line for line in text.splitlines() if line.strip()])
        if check_id == "SOROK_SRC_10_RECONCILIATION_QUEUE_SOURCE_GAPS_AND_CLOSEOUT_CHECK_R1.md:W8R_DIRECT_NOW":
            return len(set(re.findall(r"WORKNOW-\d+", text)))
        if check_id == "SOROK_SRC_TARGET_OVERRIDE":
            data = json.loads(text)
            return len(data.get("conservation", {}).get("target_specific_overrides", []))
        if check_id.startswith("PYAT_SRC_"):
            if path.endswith(".md"):
                return len(set(re.findall(r"GAP-\d{3}", text)))
            return len([line for line in text.splitlines() if line.strip()])
        return None

    def validate_anti_joins(self, groups: dict[str, list[dict[str, str]]]) -> None:
        rows = self.read_table("CONTROL/P0_NO_DROP_ANTI_JOINS.tsv", AJ_HEADER, "A_ANTI_JOIN_TABLE")
        self.check("A_ANTI_JOIN_COUNT", len(rows) == 110, f"observed {len(rows)} anti-join checks; expected 110")
        self.check("A_ANTI_JOIN_IDS", len({r["check_id"] for r in rows}) == len(rows), "check_id must be unique")
        ok = True
        for row in rows:
            check_id = row["check_id"]
            try:
                expected = parse_int(row["expected_count"], "expected_count")
                observed_input = parse_int(row["observed_input_count"], "observed_input_count")
                observed_output = parse_int(row["observed_output_count"], "observed_output_count")
                duplicate = parse_int(row["duplicate_count"], "duplicate_count")
                residual = json_list(row["source_minus_output_ids"], "source_minus_output_ids")
                extra = json_list(row["output_minus_source_ids"], "output_minus_source_ids")
            except ValueError as exc:
                ok = False
                self.check(f"A_ANTI_JOIN_ROW:{check_id}", False, str(exc))
                continue
            local = expected == observed_input == observed_output and duplicate == 0 and not residual and not extra
            if not local:
                ok = False
                self.check(f"A_ANTI_JOIN_ROW:{check_id}", False, "count/residual mismatch")
            if check_id.startswith("AJ-RM"):
                continue
            if check_id.startswith("AJ-D02_") or check_id.startswith("AJ-D03_") or check_id.startswith("AJ-D04_") or check_id.startswith("AJ-D05_") or check_id.startswith("AJ-D06_") or check_id.startswith("AJ-D07_"):
                continue
            estate = row["estate_id"]
            if estate in groups:
                census_count = len(groups[estate])
                if census_count != expected:
                    ok = False
                    self.check(f"A_ANTI_JOIN_CENSUS:{check_id}", False, f"expected {expected}, census {census_count}")
                continue
            source_count = self.external_source_count(check_id, row["source_ref"])
            if source_count is not None and source_count != expected:
                ok = False
                self.check(f"A_ANTI_JOIN_SOURCE:{check_id}", False, f"expected {expected}, source {source_count}")
        if ok:
            self.check("A_ANTI_JOIN_ROWS", True, "all 110 anti-join rows are internally exact and source-count checked")

    def validate_coverage(self, groups: dict[str, list[dict[str, str]]]) -> None:
        rows = self.read_table("CONTROL/P0_COVERAGE_RECEIPTS.tsv", COVERAGE_HEADER, "A_COVERAGE_TABLE")
        self.check("A_COVERAGE_COUNT", len(rows) == 111, f"observed {len(rows)} receipts; expected 111")
        self.check("A_COVERAGE_IDS", len({r["receipt_id"] for r in rows}) == len(rows), "receipt_id must be unique")
        ok = True
        for row in rows:
            rid = row["receipt_id"]
            try:
                input_count = parse_int(row["input_count"], "input_count")
                output_count = parse_int(row["output_count"], "output_count")
                missing = parse_int(row["missing_count"], "missing_count")
                extra = parse_int(row["extra_count"], "extra_count")
                duplicate = parse_int(row["duplicate_count"], "duplicate_count")
            except ValueError as exc:
                ok = False
                self.check(f"A_COVERAGE_ROW:{rid}", False, str(exc))
                continue
            if not (input_count == output_count and missing == extra == duplicate == 0):
                ok = False
                self.check(f"A_COVERAGE_ROW:{rid}", False, "counts do not preserve exact no-drop")
                continue
            if not row["source_id_digest"].startswith("sha256:") or not row["sorted_output_id_digest"].startswith("sha256:"):
                ok = False
                self.check(f"A_COVERAGE_ROW:{rid}", False, "digest grammar invalid")
                continue
            estate = row["estate_id"]
            if rid == "REC-PROG_SEAM82_PREDICATE_TUPLES":
                continue
            if estate in groups:
                selected = groups[estate]
                match = re.search(r"source_path=([^;]+)", row["key_extraction_rule"])
                if match:
                    selected = [item for item in selected if item["source_path"] == match.group(1)]
                material = "\n".join(sorted(item["source_composite_id"] for item in selected)) + "\n"
                computed = "sha256:" + hashlib.sha256(material.encode("utf-8")).hexdigest()
                if computed != row["sorted_output_id_digest"] or computed != row["source_id_digest"]:
                    ok = False
                    self.check(f"A_COVERAGE_DIGEST:{rid}", False, f"computed {computed}")
            elif row["source_id_digest"] != row["sorted_output_id_digest"]:
                ok = False
                self.check(f"A_COVERAGE_DIGEST:{rid}", False, "source/output digest mismatch")
        if ok:
            self.check("A_COVERAGE_ROWS", True, "all 111 receipts preserve exact counts and available digests")

    def validate_sr01(self, groups: dict[str, list[dict[str, str]]]) -> None:
        for estate, expected in (("PYAT_SR01_2416", 2416), ("SOROK_SR01_1314", 1314)):
            rows = groups.get(estate, [])
            self.check(f"A_SR01_COUNT:{estate}", len(rows) == expected, f"observed {len(rows)}; expected {expected}")
            keys = {key_tuple(row["source_composite_id"]) for row in rows}
            self.check(f"A_SR01_KEYS:{estate}", len(keys) == expected, f"unique composite keys {len(keys)}")

    def validate_rm(self, census_rows: list[dict[str, str]], anti_rows: list[dict[str, str]]) -> None:
        bijection = self.read_table("CONTROL/P0_RM_CHECK_ID_BIJECTION_V1.tsv", RM_HEADER, "B_RM_TABLE")
        requirements = self.read_table(
            "CONTROL/P0_ANTI_JOIN_REQUIREMENTS.tsv",
            ["join_id", "source_estate_id", "source_sha", "source_locator", "source_key_rule",
             "expected_members_at_cut", "ZL00_source_readback", "protected_bootstrap_members",
             "ZL01_output_file", "ZL01_row_identity_contract", "mandatory_anti_join",
             "overlap_subset_policy", "negative_and_disposition_preservation", "scope_ceiling",
             "owner", "current_status"],
            "B_RM_REQUIREMENTS",
        )
        self.check("B_RM_BIJECTION_COUNT", len(bijection) == 30, f"observed {len(bijection)} RM mappings; expected 30")
        self.check("B_RM_REQUIREMENTS_COUNT", len(requirements) == 56, f"observed {len(requirements)} requirements; expected 56")
        frozen = [row["frozen_check_id"] for row in bijection]
        reported = [row["zl01_reported_check_id"] for row in bijection]
        self.check("B_RM_BIJECTION_IDS", len(set(frozen)) == 30 and len(set(reported)) == 30,
                   "frozen and reported RM IDs must be unique")
        self.check("B_RM_FROZEN_IDS", set(frozen) == {f"AJ-RM{i:02d}" for i in range(1, 31)},
                   "frozen AJ-RM01..AJ-RM30 identity set exact")
        requirement_ids = {row["join_id"] for row in requirements}
        self.check("B_RM_REQUIREMENTS_IDS", set(frozen) <= requirement_ids,
                   "all frozen RM checks must exist in the 56 requirements")
        anti = {row["check_id"]: row for row in anti_rows}
        census_rm = {row["source_exact_id"]: row for row in census_rows if row["estate_id"] == "RECENT_CAMPAIGN30"}
        ok = True
        for row in bijection:
            fid = row["frozen_check_id"]
            rm = row["source_rm_id"]
            if row["authoritative_census_estate_id"] != "RECENT_CAMPAIGN30" or row["authoritative_census_source_exact_id"] != rm:
                ok = False
                self.check(f"B_RM_SELECTOR:{fid}", False, "authoritative census selector is not RECENT_CAMPAIGN30 + exact RM")
                continue
            census = census_rm.get(rm)
            if not census or not census["negative_status"].strip():
                ok = False
                self.check(f"B_RM_NEGATIVE:{fid}", False, "RM census negative is missing")
                continue
            check = anti.get(fid)
            if not check:
                ok = False
                self.check(f"B_RM_ANTI_JOIN:{fid}", False, "frozen RM check missing from 110 anti-joins")
                continue
            expected_negative = f"estate_id=RECENT_CAMPAIGN30;source_exact_id={rm};negative_status"
            if expected_negative not in check["negative_ids"]:
                ok = False
                self.check(f"B_RM_ANTI_JOIN:{fid}", False, "RM negative selector does not use the exact census namespace")
            if parse_int(check["expected_count"], "expected_count") != 1:
                ok = False
                self.check(f"B_RM_ANTI_JOIN:{fid}", False, "RM anti-join expected count is not 1")
        if ok:
            self.check("B_RM_MAPPINGS", True, "30/30 RM mappings, selectors and retained negatives are exact")

    def validate_d02_d07(self, census_rows: list[dict[str, str]], anti_rows: list[dict[str, str]]) -> None:
        per_file = [row for row in anti_rows if "__" in row["check_id"] and row["check_id"].startswith(("AJ-D02_", "AJ-D03_", "AJ-D04_", "AJ-D05_", "AJ-D06_", "AJ-D07_"))]
        self.check("C_D02_D07_SELECTOR_COUNT", len(per_file) == 23, f"observed {len(per_file)} per-file selectors; expected 23")
        ok = True
        total = 0
        source_total = 0
        for row in per_file:
            source_ref = row["source_ref"]
            if "::" not in source_ref or "#blob=" not in source_ref:
                ok = False
                self.check(f"C_D02_D07_SELECTOR:{row['check_id']}", False, "source_ref lacks exact path/blob")
                continue
            commit, rest = source_ref.split("::", 1)
            path, blob = rest.split("#blob=", 1)
            expected = parse_int(row["expected_count"], "expected_count")
            matching = [
                census for census in census_rows
                if census["source_path"] == path and census["source_commit_sha"] == commit
                and census["source_blob_sha"] == blob
            ]
            if len(matching) != expected:
                ok = False
                self.check(
                    f"C_D02_D07_SELECTOR:{row['check_id']}", False,
                    f"selector resolved {len(matching)} rows; expected {expected}",
                )
                continue
            try:
                source_count = len(self.source_keys(row["estate_id"], commit, path))
            except Exception as exc:
                ok = False
                self.check(f"C_D02_D07_SOURCE:{row['check_id']}", False, f"source unavailable: {exc}")
                continue
            source_total += source_count
            try:
                source_text = self.git.show(commit, path).decode("utf-8")
                source_rows = list(csv.reader(source_text.splitlines()))
                source_width = len(source_rows[0]) if source_rows else 0
                bad_widths = [number for number, item in enumerate(source_rows[1:], 2) if len(item) != source_width]
            except Exception as exc:
                bad_widths = []
                self.hold(f"C_D02_D07_QUOTING:{row['check_id']}", f"cannot inspect CSV quoting: {exc}")
            if bad_widths:
                self.hold(
                    f"C_D02_D07_QUOTING:{row['check_id']}",
                    f"source CSV rows {bad_widths} have width != header {source_width}; "
                    "identities retained, field-level interpretation requires source-owner qualification",
                )
            if source_count != expected:
                ok = False
                self.check(
                    f"C_D02_D07_SOURCE:{row['check_id']}", False,
                    f"source file has {source_count} keyed records; claim is {expected}",
                )
            if any(not census["negative_status"].strip() for census in matching):
                ok = False
                self.check(f"C_D02_D07_NEGATIVE:{row['check_id']}", False, "source row lost negative status")
            if f"estate_id={row['estate_id']}" not in row["unjoined_ids"] or f"source_path={path}" not in row["unjoined_ids"]:
                ok = False
                self.check(f"C_D02_D07_FILTER:{row['check_id']}", False, "unjoined selector lacks grouped estate/path")
            total += len(matching)
        self.check("C_D02_D07_ROWS", source_total == total, f"source rows={source_total}, census rows={total}; expected source-derived equality")
        if ok and total == 364:
            self.check("C_D02_D07_SELECTORS", True, "23 file selectors resolve exactly 364 grouped census rows")

    def g4_source(self) -> dict[str, dict[str, Any]]:
        path = "PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/CURRENT_SEAM_STATES.jsonl"
        commit = "7a5429ffbc48efd25e28c912da80c822e66bc182"
        text = self.git.show(commit, path).decode("utf-8")
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
        return {row["edge_id"]: row for row in rows}

    def validate_g4(self) -> None:
        contract = self.read_table("CONTROL/P0_PROG_SEAM82_PREDICATE_CONTRACT_V1.tsv", G4_CONTRACT_HEADER, "D_G4_CONTRACT")
        receipt = self.read_table("CONTROL/P0_SEAM_PREDICATE_RECEIPTS.tsv", G4_RECEIPT_HEADER, "D_G4_RECEIPTS")
        source = self.g4_source()
        self.check("D_G4_ROW_COUNTS", len(contract) == 82 and len(receipt) == 82 and len(source) == 82,
                   f"contract={len(contract)} receipt={len(receipt)} source={len(source)}")
        self.check("D_G4_EDGE_IDS", len({row["edge_id"] for row in contract}) == 82 and
                   {row["edge_id"] for row in contract} == set(source),
                   "82 edge IDs must equal source edge IDs")
        ok = True
        if_count = 0
        for row in contract:
            edge = row["edge_id"]
            src = source.get(edge)
            if not src:
                ok = False
                self.check(f"D_G4_EDGE:{edge}", False, "edge missing from source")
                continue
            if row["original_requiredness"] == "IF":
                if_count += 1
            g2 = src.get("original_G2", {})
            expected = {
                "original_requiredness": src.get("original_requiredness"),
                "original_predicate": src.get("original_predicate"),
                "original_G2_kind": g2.get("kind"),
                "original_G2_edge_condition": g2.get("edge_condition"),
            }
            for field, value in expected.items():
                if str(row[field]) != str(value):
                    ok = False
                    self.check(f"D_G4_FIELD:{edge}:{field}", False, f"contract={row[field]!r} source={value!r}")
        self.check("D_G4_IF_COUNT", if_count == 26, f"observed {if_count} IF predicates; expected 26")
        receipt_by_edge = {row["census_source_exact_id"]: row for row in receipt}
        contract_by_edge = {row["edge_id"]: row for row in contract}
        for edge, row in receipt_by_edge.items():
            other = contract_by_edge.get(edge)
            if not other:
                ok = False
                self.check(f"D_G4_RECEIPT:{edge}", False, "receipt has no matching contract edge")
                continue
            pairs = (
                ("source_commit_sha", "source_commit_sha"),
                ("source_blob_sha", "source_blob_sha"),
                ("source_path", "source_path"),
                ("source_row_ordinal", "source_row_1based"),
                ("original_requiredness", "original_requiredness"),
                ("original_predicate", "original_predicate"),
                ("original_g2_kind", "original_G2_kind"),
                ("original_g2_edge_condition", "original_G2_edge_condition"),
            )
            for receipt_field, contract_field in pairs:
                if row[receipt_field] != other[contract_field]:
                    ok = False
                    self.check(f"D_G4_RECEIPT:{edge}:{receipt_field}", False, "receipt differs from contract")
        if ok:
            self.check("D_G4_FIELDS", True, "82/82 G4 source predicates, requiredness and evidence fields exact; 26 IF preserved")

    def validate_p1_schema(self) -> None:
        path = self.root / "CONTROL/P0_SCHEMA_AND_LEASES.md"
        if not path.is_file():
            self.hold("F_P1_SCHEMA", "missing P0_SCHEMA_AND_LEASES.md")
            return
        text = path.read_text(encoding="utf-8")
        ok = True
        for name, header in P1_HEADERS.items():
            needle = "\t".join(header)
            if needle not in text:
                ok = False
                self.check(f"F_P1_HEADER:{name}", False, f"frozen header missing or changed ({len(header)} columns)")
        self.check("F_P1_VERSION", "VMESTYE_P1_PRONG_TABLES_V1" in text, "version marker present")
        leases = re.findall(r"^\| ZL-(\d{2}) \| `([^`]+)`", text, flags=re.MULTILINE)
        leases = [(f"ZL-{number}", path_value) for number, path_value in leases if 2 <= int(number) <= 14]
        self.check("F_P1_LEASES", len(leases) == 13 and len({p for _, p in leases}) == 13,
                   f"observed {len(leases)} ZL-02..ZL-14 prong leases")
        self.check("F_P1_FKS", all(token in text for token in ("foreign key", "finding_id", "census_id", "UNJOINS.tsv")),
                   "foreign-key and explicit-unjoin law present")
        if ok:
            self.check("F_P1_SCHEMA", True, "five frozen headers, enums, FK law and 13 distinct leases present")

    def validate_stage(self) -> None:
        rows = self.read_table("CONTROL/P0_S2_STAGE_MANIFEST.tsv", STAGE_HEADER, "E_STAGE_TABLE")
        self.check("E_STAGE_COUNT", len(rows) == 2 and {row["subject_id"] for row in rows} == {"ZL00", "ZL01"},
                   f"observed stage subjects {[row['subject_id'] for row in rows]}")
        ok = True
        for row in rows:
            subject = row["subject_id"]
            stage = row["stage"]
            if stage not in STAGES:
                ok = False
                self.check(f"E_STAGE_VALUE:{subject}", False, f"unknown stage {stage}")
                continue
            if not re.fullmatch(r"[0-9a-f]{40}", row["candidate_head_sha"]):
                ok = False
                self.check(f"E_STAGE_HEAD:{subject}", False, "candidate head is not an exact SHA")
            if stage in {"INDEPENDENT_REVIEWED", "ACCEPTED_TO_VMESTYE"}:
                if row["independent"] != "YES" or not row["review_actor"] or row["reviewed_candidate_head_sha"] != row["candidate_head_sha"]:
                    ok = False
                    self.check(f"E_STAGE_REVIEW:{subject}", False, "review is not independent or not at the exact candidate head")
            if stage == "ACCEPTED_TO_VMESTYE":
                if row["review_verdict"] != "ACCEPT" or not row["protected_adoption_sha"]:
                    ok = False
                    self.check(f"E_STAGE_ACCEPTANCE:{subject}", False, "acceptance has no ACCEPT verdict/protected adoption")
            elif row["protected_adoption_sha"]:
                ok = False
                self.check(f"E_STAGE_ACCEPTANCE:{subject}", False, "unaccepted candidate claims protected adoption")
            if row["author_actor"] == row["review_actor"]:
                ok = False
                self.check(f"E_STAGE_INDEPENDENCE:{subject}", False, "author and reviewer are identical")
            if "LOCAL_S2_STRUCTURAL" not in row["runner_authorization"] or row["s3_authorized"] != "NO":
                ok = False
                self.check(f"E_STAGE_AUTHORITY:{subject}", False, "runner authorization/ceiling is not local S2 structural only")
        if ok:
            self.check("E_STAGE_PROGRESSION", True, "stage machine and exact-head review/acceptance guards hold")

    def validate_assembly(self) -> None:
        rows = self.read_table("CONTROL/P0_S2_ASSEMBLY_MANIFEST.tsv", ASSEMBLY_HEADER, "E_ASSEMBLY_TABLE")
        self.check("E_ASSEMBLY_COUNT", len(rows) == 17, f"observed {len(rows)} candidate files; expected 17")
        self.check("E_ASSEMBLY_PATHS", len({row["relative_path"] for row in rows}) == len(rows), "candidate path overlap")
        ok = True
        for row in rows:
            path = self.root / row["relative_path"]
            if not path.is_file():
                ok = False
                self.check(f"E_ASSEMBLY_FILE:{row['relative_path']}", False, "missing assembly file")
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != row["sha256"]:
                ok = False
                self.check(f"E_ASSEMBLY_HASH:{row['relative_path']}", False, "assembly hash drift")
            if not re.fullmatch(r"[0-9a-f]{40}", row["source_commit_sha"]) or not re.fullmatch(r"[0-9a-f]{40}", row["source_blob_sha"]):
                ok = False
                self.check(f"E_ASSEMBLY_ORIGIN:{row['relative_path']}", False, "candidate origin is not exact")
        if ok:
            self.check("E_ASSEMBLY", True, "17 candidate files are hash-exact and origin-pinned without overlap")

    def run(self) -> tuple[list[dict[str, str]], list[tuple[str, str]]]:
        census_rows, groups = self.validate_census()
        anti_rows = []
        anti_path = self.root / "CONTROL/P0_NO_DROP_ANTI_JOINS.tsv"
        if anti_path.is_file():
            anti_rows = list(csv.DictReader(anti_path.open(encoding="utf-8"), delimiter="\t"))
        self.validate_anti_joins(groups)
        self.validate_coverage(groups)
        self.validate_sr01(groups)
        self.validate_rm(census_rows, anti_rows)
        self.validate_d02_d07(census_rows, anti_rows)
        self.validate_g4()
        self.validate_p1_schema()
        self.validate_stage()
        self.validate_assembly()
        return self.checks, self.failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--git-repo", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    validator = Validator(args.root, args.git_repo)
    checks, failures = validator.run()
    for row in checks:
        print(f"{row['status']}\t{row['check_id']}\t{row['detail']}")
    if args.receipt:
        with args.receipt.open("w", encoding="utf-8", newline="") as handle:
            handle.write("check_id\tstatus\tdetail\n")
            for row in checks:
                handle.write(f"{row['check_id']}\t{row['status']}\t{row['detail']}\n")
    if args.json:
        args.json.write_text(json.dumps({"checks": checks, "failures": failures}, indent=2) + "\n", encoding="utf-8")
    if failures:
        print("P0_S2_VALIDATOR_FAIL", file=sys.stderr)
        for check_id, detail in failures:
            print(f"ERROR {check_id} {detail}", file=sys.stderr)
        return 1
    print("P0_S2_VALIDATOR_PASS__SOURCE_IDENTITY_AND_STRUCTURE_ONLY__NO_SCIENTIFIC_OR_NATIVE_AUTHORITY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
