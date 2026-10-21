#!/usr/bin/env python3
"""B53H proposed *structural prefilter*, never a native/scientific acceptance.

Usage:
  python 03_manifest_gate_prototype.py --roster trusted_roster.json \
      --expected-roster-sha256 <PIN_FROM_PROTECTED_POLICY> --manifest candidate.json

A passing self-authored JSON is NOT proof of R1/R4/R5/R6 execution; only
independent runtime with canonical fixed expectations can supply that proof.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA = "PYAT_B53H_UNIVERSAL_SOURCEFREE_PROMOTION@1"
GRADES = {"UNIVERSAL_SOURCEFREE_SHAPE_PROVED", "UNIVERSAL_ENGINE_SOURCEFREE_SHAPE_PROVED_SCOPED"}
STATES = {"SOURCE_RIGHT_HOLD", "SEMANTIC_UNKNOWN", "SCIENTIFIC_UNISSUED",
          "READY_FOR_AUTHORIZED_TRANCHE", "SOURCEFREE_SHAPE_TESTED", "ORIGINAL_EXECUTED"}
RECEIPT_CLASSES = {"I03", "I05", "BATCH"}
SHA = re.compile(r"^[0-9a-f]{64}$")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def parse_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate(roster, expected_sha, candidate):
    errors = []

    def require(condition, reason):
        if not condition:
            errors.append(reason)

    require(bool(SHA.fullmatch(expected_sha)), "TRUSTED_ROSTER_SHA_INVALID")
    require(digest(roster) == expected_sha, "TRUSTED_ROSTER_SHA_MISMATCH")
    require(candidate.get("schema") == SCHEMA, "PROMOTION_SCHEMA_MISMATCH")
    require(candidate.get("grade") in GRADES, "UNIVERSAL_GRADE_MISMATCH")
    require(candidate.get("canonical_roster_sha256") == expected_sha, "CANDIDATE_ROSTER_ROOT_MISMATCH")
    require(bool(re.fullmatch(r"[0-9a-f]{40}", candidate.get("base_sha", ""))), "BASE_SHA_MISSING")

    expected = roster.get("waves", [])
    expected_ids = [w.get("source_wave_id") for w in expected]
    require(len(expected_ids) == len(set(expected_ids)) == 35, "CANONICAL_35_UNIQUENESS")
    require(sum(w.get("format") == "SAV" for w in expected) == 31, "CANONICAL_SAV_31")
    require(sum(w.get("format") == "DTA" for w in expected) == 4, "CANONICAL_DTA_4")
    received = candidate.get("waves", [])
    actual_ids = [w.get("source_wave_id") for w in received]
    require(len(actual_ids) == 35 and set(actual_ids) == set(expected_ids)
            and len(set(actual_ids)) == 35, "WAVE_EXPECTED_EMITTED_ANTI_JOIN")
    actual_map = {w.get("source_wave_id"): w for w in received}
    for wave in expected:
        w = actual_map.get(wave.get("source_wave_id"), {})
        require(w.get("status") in STATES, "WAVE_BAD_STATUS:" + str(wave.get("source_wave_id")))
        if w.get("status") in {"SOURCE_RIGHT_HOLD", "SEMANTIC_UNKNOWN", "SCIENTIFIC_UNISSUED"}:
            require(w.get("original_u_root") is None and w.get("original_e_pre_root") is None,
                    "UNISSUED_ORIGINAL_ROOT_MUST_BE_NULL:" + str(wave.get("source_wave_id")))
            require(bool(w.get("hold_reason")), "MISSING_HOLD_REASON:" + str(wave.get("source_wave_id")))

    require(bool(candidate.get("production_entrypoint")) and
            not any(x in candidate.get("production_entrypoint", "") for x in
                    ("r51_joined_source_producer", "g50.fixture", "rawlsing_next.tests")),
            "NO_PUBLIC_INDEPENDENT_PRODUCTION_ENTRYPOINT")
    require(candidate.get("scientific_original_grade") == "NOT_ISSUED",
            "SOURCEFREE_CLAIM_PRETENDS_ORIGINAL_SCIENCE")
    require(candidate.get("e_pre_value_blind") is True, "E_PRE_NOT_FROZEN_BEFORE_VALUES")
    require(candidate.get("cold_restoration") is True, "COLD_RESTORATION_MISSING")

    fixtures = candidate.get("fixtures", [])
    require(len(fixtures) >= 3, "THREE_SOURCE_SHAPE_FIXTURES_REQUIRED")
    family_set, shape_set, formats, code_sets = set(), set(), set(), set()
    ids = set()
    shape_markers = set()
    executed_shapes = set()
    for f in fixtures:
        fid = str(f.get("fixture_id", ""))
        require(fid and fid not in ids, "FIXTURE_ID_DUPLICATE_OR_MISSING:" + fid)
        ids.add(fid)
        family_set.add(f.get("family"))
        formats.add(f.get("format"))
        codes = f.get("native_item_codes", [])
        require(bool(codes) and len(set(codes)) == len(codes), "NATIVE_CODES_INVALID:" + fid)
        code_sets.add(tuple(sorted(codes)))
        markers = frozenset(f.get("shape_markers", []))
        shape_markers.update(markers)
        shape_set.add((f.get("format"), markers, tuple(sorted(codes))))
        require(bool(f.get("independent_fixture_authority_ref")), "UNPINNED_FIXTURE_ORACLE:" + fid)
        exp = f.get("expected_operation_ids", [])
        got = f.get("result_operation_ids", [])
        require(len(exp) == len(set(exp)) and len(got) == len(set(got)) and
                set(exp) == set(got) and bool(exp), "SOURCEFREE_OPERATION_ANTI_JOIN:" + fid)
        native = set(f.get("native_called_owners", []))
        require({"C11", "I03", "BATCH"}.issubset(native), "NATIVE_C11_I03_BATCH_MISSING:" + fid)
        require(bool(f.get("source_value_mutation_assertion_id")), "SOURCE_DEPENDENCY_MISSING:" + fid)
        if "I05" in native:
            executed_shapes.add((f.get("format"), markers, tuple(sorted(codes))))
    require(len(family_set) >= 2, "FAMILY_DIVERSITY_MISSING")
    require(formats.issuperset({"SAV", "DTA"}), "SAV_DTA_HETEROGENEITY_MISSING")
    require(len(shape_set) >= 3 and len(code_sets) >= 3, "IDENTITY_RELABELED_FIXTURE_NOT_HETEROGENEOUS")
    require(bool(shape_markers & {"ROUTED", "SPLIT_FORM"}), "ROUTE_FORM_ADVERSARY_MISSING")
    require("HOUSEHOLD_UNIT" in shape_markers, "HOUSEHOLD_ADVERSARY_MISSING")
    require(bool(shape_markers & {"WEIGHT_DESIGN", "MULTIRESPONSE", "RANKED", "REPEATED"}),
            "DESIGN_TOPOLOGY_ADVERSARY_MISSING")
    require(len(executed_shapes) >= 2, "TWO_DISTINCT_I05_NATIVE_SHAPES_REQUIRED")

    metamorphic = candidate.get("metamorphic_pairs", [])
    require(any(m.get("reserved_names_absent") and m.get("bijective_source_valid_rename")
                and m.get("normalized_operation_parity") and m.get("normalized_consumer_parity")
                for m in metamorphic), "ARBITRARY_NAMES_METAMORPHIC_GATE_MISSING")
    require(bool(candidate.get("named_native_consumer")), "REAL_NAMED_CONSUMER_MISSING")
    require(bool(candidate.get("same_consumer_red_assertion")), "SOURCE_FAULT_NAMED_RED_MISSING")
    require(bool(candidate.get("restore_same_consumer_green_assertion")),
            "SOURCE_FAULT_COLD_RESTORE_MISSING")

    # These fields are deliberately *not* enough to certify native execution.
    # An external independent CI job must run and inspect actual sourcefree
    # programs, methods, red/green traces, and source/issuer custody.
    return {"state": "REVISE_UNIVERSAL_PROMOTION" if errors else
                    "STRUCTURAL_CONTRACT_PASS_NEEDS_TRUSTED_NATIVE_PROOF",
            "errors": sorted(set(errors)), "scope": "STRUCTURAL_MANIFEST_PREFILTER_ONLY",
            "never_implies": ["ORIGINAL35_SCIENTIFIC_COMPLETED", "N11_ACCEPTED",
                              "R53_STOP_RELEASED", "NATIVE_RUNTIME_PROVED"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roster", required=True)
    ap.add_argument("--expected-roster-sha256", required=True)
    ap.add_argument("--manifest", required=True)
    args = ap.parse_args()
    result = validate(parse_json(args.roster), args.expected_roster_sha256,
                      parse_json(args.manifest))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not result["errors"] else 2


if __name__ == "__main__":
    sys.exit(main())
