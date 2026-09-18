#!/usr/bin/env python3
"""EE-P2R1 contract-level calibration against the governed CLOSED_35_WAVES envelope.

This is structural calibration only.  It does not open any empirical carrier.
It proves that the new generic carrier->C11->I03/I05 seam contains no proving-
wave/source golden path and records exactly where governed heterogeneity enters
the already-existing PRE553 contracts.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import subprocess
from pathlib import Path

from rawlsing_next.pre553_empirical_objects import semantic_hash


AUTHORITY_COMMIT = "7d4703148057fe1d2fdd7bbf94df306abf8b21de"
AUTHORITY_PATH = (
    "data/ddm_build_copy/bindings/"
    "question_relation_registry_35wave_active_v1.csv"
)
SEAM_PATH = Path("rawlsing_next/pre553_carrier_execution.py")

FORBIDDEN_GENERIC_LITERALS = (
    "WVS",
    "LiTS",
    "Q291",
    "Q301",
    "Afrobarometer",
    "Arab Barometer",
    "Asian Barometer",
    "Latinobar",
    "South Asia",
    ".sav",
    ".dta",
)


def git_bytes(commit: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"exact governed envelope unavailable from {commit}:{path}: "
            + completed.stderr.decode("utf-8", "replace").strip()
        )
    return completed.stdout


def literal_strings(source: str) -> tuple[str, ...]:
    tree = ast.parse(source)
    return tuple(
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-receipt", type=Path)
    args = parser.parse_args()

    authority_raw = git_bytes(AUTHORITY_COMMIT, AUTHORITY_PATH)
    authority_sha256 = hashlib.sha256(authority_raw).hexdigest()
    rows = list(csv.DictReader(io.StringIO(authority_raw.decode("utf-8-sig"))))
    pairs = sorted({
        (str(row.get("source_family") or "").strip(),
         str(row.get("canonical_wave") or "").strip())
        for row in rows
        if str(row.get("source_family") or "").strip()
        and str(row.get("canonical_wave") or "").strip()
    })
    if len(pairs) != 35:
        raise RuntimeError(f"governed CLOSED_35_WAVES count mismatch: {len(pairs)}")
    if ("Asian Barometer", "W6") in pairs:
        raise RuntimeError("illegal Asian Barometer W6 present in governed 35-wave scope")

    seam_source = SEAM_PATH.read_text(encoding="utf-8")
    literals = literal_strings(seam_source)
    golden_path_hits = sorted({
        token
        for token in FORBIDDEN_GENERIC_LITERALS
        if any(token in literal for literal in literals)
    })
    if golden_path_hits:
        raise RuntimeError(
            "generic seam contains proving-source/wave literal(s): "
            + ", ".join(golden_path_hits)
        )

    required_generic_tokens = {
        "exact_only_materialization": "materialize_public_object",
        "exact_authority_registry": "AuthorityRegistry",
        "carrier_neutral_executor": "CarrierNeutralResearchExecutor",
        "i03": "execute_empirical_query",
        "i05": "execute_exact_bounded_discovery",
        "no_fuzzy_contract": "no latest/default/fuzzy",
    }
    lower_source = seam_source.lower()
    missing_contract_tokens = [
        key for key, token in required_generic_tokens.items()
        if token.lower() not in lower_source
    ]
    if missing_contract_tokens:
        raise RuntimeError(
            "generic seam contract surface missing: " + ", ".join(missing_contract_tokens)
        )

    # This is the calibration map: each heterogeneity dimension remains an
    # authority/C11/query input, never a source branch in the generic executor.
    carriage = {
        "source_family_and_wave_currentness":
            "EmpiricalUniverse + exact authority/source-relation refs inside sealed C11; executor performs no family/wave selection",
        "source_universe_identity":
            "EmpiricalQuerySpec.empirical_universe_refs + exact C11 release resolution",
        "variable_qid_identity":
            "exact predicate/query/C11 semantic refs; generic seam carries refs and never source column names",
        "response_and_special_state_semantics":
            "sealed RespondentEvent typed states + exact predicate/query authority",
        "respondent_event_topology":
            "C11 event topology + EmpiricalQuerySpec target_arity_and_topology; validated by existing I03",
        "routing_applicability_risk_set":
            "sealed RoutingEligibilityFact + exact predicate/query risk_set refs",
        "measure_weight_design_estimand":
            "EmpiricalQuerySpec measure basis and existing I03 authority checks; no default weight in seam",
        "predicate_query_grammar":
            "exact canonical RuntimeObjectCatalog + AuthorityRegistry",
        "source_release_and_replay":
            "exact C11 release refs + repository snapshot + I03/I05 replay refs",
        "optional_accelerator_applicability":
            "candidate/source preparation below C11 only; absent from carrier-neutral executor",
        "unsupported_or_missing_authority":
            "exact materialization/resolution fails closed; no hash inversion/latest/default/fuzzy fallback",
    }

    family_counts = {}
    for family, _wave in pairs:
        family_counts[family] = family_counts.get(family, 0) + 1

    material = {
        "schema": "EE_P2R1_FULL_35_WAVE_CONTRACT_CALIBRATION@1.0.0",
        "status": "PASS__GENERIC_EXECUTION_SEAM_CALIBRATED_AGAINST_GOVERNED_CLOSED_35_WAVES",
        "authority_commit": AUTHORITY_COMMIT,
        "authority_path": AUTHORITY_PATH,
        "authority_sha256": authority_sha256,
        "governed_pair_count": len(pairs),
        "governed_pairs": [
            {"source_family": family, "wave": wave} for family, wave in pairs
        ],
        "family_counts": dict(sorted(family_counts.items())),
        "empirical_source_access": False,
        "outcome_access": False,
        "generic_seam_path": str(SEAM_PATH),
        "generic_seam_sha256": hashlib.sha256(
            seam_source.encode("utf-8")
        ).hexdigest(),
        "forbidden_generic_literal_hits": golden_path_hits,
        "heterogeneity_carriage": carriage,
        "law":
            "WAVE_SPECIFIC_AUTHORITY_AND_OUTPUTS != WAVE_SPECIFIC_GENERIC_CODE",
        "calibration_kind":
            "CONTRACT_AUTHORITY_FAILURE_BEHAVIOR_ONLY__NOT_35_CARRIER_EXECUTION",
    }
    receipt = {**material, "receipt_identity": semantic_hash(material)}
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.write_receipt:
        args.write_receipt.parent.mkdir(parents=True, exist_ok=True)
        args.write_receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
