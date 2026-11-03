"""Sourcefree real-source metadata-binding trace into existing C11 and R03 owners.

Input contract is generic: the caller supplies the source configuration,
crosswalk, nonrespondent fixture and local metadata paths. No wave or source ID
is compiled into this module, and no R03 policy is manufactured.

The original source bytes are never opened. The C11 projection is built
from validated metadata; the only native release built here is the declared
nonrespondent fixture through the existing C11 factory.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def csv_shape(path: Path) -> tuple[list[str], int, str]:
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        count = sum(1 for _ in reader)
    return header, count, sha(path)


def find_release_ref(value: Any) -> Mapping[str, Any] | None:
    if isinstance(value, Mapping):
        ref = value.get("release_ref")
        if isinstance(ref, Mapping) and ref.get("kind") == "C11LogicalRelease":
            return ref
        if (value.get("kind") == "C11LogicalRelease"
                and isinstance(value.get("object_id"), str)
                and isinstance(value.get("content_hash"), str)):
            return value
        for child in value.values():
            found = find_release_ref(child)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_release_ref(child)
            if found is not None:
                return found
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", required=True,
                        help="root containing the frozen source_configuration package")
    parser.add_argument("--source-config", required=True)
    parser.add_argument("--crosswalk", required=True)
    parser.add_argument("--fixture-config", required=True)
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--codebook", required=True)
    parser.add_argument("--directionality", required=True)
    parser.add_argument("--option-authority", required=True)
    parser.add_argument("--validation-results", required=True)
    parser.add_argument("--metadata-origin", default="")
    parser.add_argument("--form-route-owner", default="source form/administration evidence owner named by the source exception ledger")
    parser.add_argument("--r03-policy-owner", default="R03 GrammarPolicy/direction owner")
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    sys.path.insert(0, str(Path(args.package_root).resolve()))

    from rawlsing_next.source_configuration.schema import canonical_config_hash, load_source_config
    from rawlsing_next.source_configuration.factory import (
        build_governed_c11_projection,
        build_validated_c11_release_from_config,
    )
    from rawlsing_next.source_configuration.fixture import load_fixture_stream
    from rawlsing_next.universal_grammar.types import OccurrenceKey

    config_path = Path(args.source_config)
    crosswalk_path = Path(args.crosswalk)
    fixture_config_path = Path(args.fixture_config)
    fixture_path = Path(args.fixture)
    config = load_source_config(config_path)
    fixture_config = load_source_config(fixture_config_path)
    fixture_stream = load_fixture_stream(fixture_path)
    crosswalk = read_json(crosswalk_path)
    validation_path = Path(args.validation_results)
    validation = read_json(validation_path)
    codebook_header, codebook_rows, codebook_hash = csv_shape(Path(args.codebook))
    direction_header, direction_rows, direction_hash = csv_shape(Path(args.directionality))
    option_header, option_rows, option_hash = csv_shape(Path(args.option_authority))

    # Actual existing C11 caller: metadata projection, no source read.
    projection = build_governed_c11_projection(config)
    # The only native release is the explicitly nonrespondent fixture.
    fixture_projection = build_governed_c11_projection(
        fixture_config,
        source_sha256=fixture_stream.source_sha256,
        row_count=fixture_stream.row_count,
    )
    fixture_release = build_validated_c11_release_from_config(
        fixture_config, stream=fixture_stream)
    expected_release = find_release_ref(validation)

    # Trace the exact configured response items into the R03 normal key type.
    # The candidate keys are formed only to test the input contract; they are
    # not accepted while form/repeat and routing exactness are unresolved.
    response_slots = config.document["response_slots"]
    r03_candidates = []
    for slot in response_slots:
        question_id = slot["question_id"]
        candidate = OccurrenceKey(item_id=question_id)
        r03_candidates.append(candidate.material())
    r03_candidate_count = len(r03_candidates)
    r03_unique_count = len({json.dumps(key, sort_keys=True) for key in r03_candidates})

    supported_scope = config.document["supported_scope"]
    form_slice = supported_scope.get("supported_form_slice")
    form_exact = not ("NO_FORM_VARIABLE_EVIDENCE" in str(form_slice)
                      or "UNKNOWN" in str(form_slice))
    repeat_exact = False  # no repeat identity is declared in the config contract
    routing = config.document["routing"]
    routing_unknown = sum(
        1 for row in routing if row.get("typed_state") != "ROUTING_KNOWN")
    risk_set_unresolved = sum(
        1 for row in routing
        if str((row.get("risk_set_ref") or {}).get("object_id", "")).endswith("unresolved"))
    route_exact = routing_unknown == 0 and risk_set_unresolved == 0
    policy_exact = False
    direction_statuses = Counter()
    with Path(args.directionality).open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            direction_statuses[str(row.get("directional_certification_status", ""))] += 1

    first_missing = {
        "artifact": f"exact {config.source_id} source form/repetition identity for configured response operands",
        "fields": ["supported_scope.supported_form_slice", "OccurrenceKey.form_id", "OccurrenceKey.repeat_id"],
        "current_value": form_slice,
        "owner": args.form_route_owner,
        "why": "The source configuration records a single-file SAV shape but explicitly lacks form, ballot or administration variable evidence; R03 form/repeat identity is not established.",
        "next_missing": {
            "artifact": "exact routing/eligibility and denominator handoff",
            "fields": ["routing[].typed_state", "routing[].risk_set_ref", "risk_set_refs"],
            "counts": {"routing_entries": len(routing),
                       "routing_unknown": routing_unknown,
                       "risk_set_unresolved": risk_set_unresolved},
            "owner": args.form_route_owner,
        },
        "downstream_missing": {
            "artifact": "exact R03 GrammarPolicy/authorized direction grant",
            "owner": args.r03_policy_owner + "; no policy is supplied by the source configuration",
        },
    }
    result = {
        "schema": "PYAT_REAL_METADATA_BINDING_RECEIPT@1.0.0",
        "mode": "TEST_ONLY_SOURCEFREE_METADATA_BINDING",
        "metadata_origin": args.metadata_origin,
        "source": {
            "source_id": config.source_id,
            "config_id": config.config_id,
            "family": config.document["identity"]["family"],
            "wave": config.document["identity"]["wave"],
            "edition_sha256": config.active_source_sha256,
            "row_count": config.active_row_count,
            "column_count": config.document["identity"]["source_column_count"],
            "source_bytes": config.document["identity"]["source_bytes"],
            "source_config_sha256": sha(config_path),
            "config_canonical_sha256": canonical_config_hash(config),
            "crosswalk_sha256": sha(crosswalk_path),
            "fixture_config_sha256": sha(fixture_config_path),
            "fixture_sha256": sha(fixture_path),
            "fixture_nonrespondent": True,
            "validation_results_sha256": sha(validation_path),
            "validation_status": validation.get("status"),
            "codebook": {"sha256": codebook_hash, "rows": codebook_rows,
                         "columns": len(codebook_header)},
            "directionality": {"sha256": direction_hash, "rows": direction_rows,
                               "columns": len(direction_header),
                               "certification_status_counts": dict(sorted(direction_statuses.items()))},
            "option_authority": {"sha256": option_hash, "rows": option_rows,
                                 "columns": len(option_header)},
        },
        "mapping": {
            "crosswalk_entries": len(crosswalk.get("entries", ())),
            "crosswalk_method": crosswalk.get("method"),
            "config_physical_slots": len(config.document["physical_slots"]),
            "config_items": len(config.document["items"]),
            "config_questions": len(config.document["questions"]),
            "response_slots": len(response_slots),
            "coordinate_slots": len(config.document["coordinate_slots"]),
            "routing_entries": len(routing),
            "item_mapping": "EXACT_CONFIG_ITEM_AND_CROSSWALK_NAME",
            "option_mapping": "CONFIGURED_RESPONSE_SLOTS_AND_OPTION_AUTHORITY",
        },
        "c11": {
            "caller": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "projection_ref": projection.projection_identity_ref.as_dict(),
            "projection_source_sha256": projection.expected_source_sha256,
            "respondents": len(projection.respondents),
            "questions": len(projection.questions),
            "response_slots": len(projection.response_slots),
            "coordinate_slots": len(projection.coordinate_slots),
            "routing_facts": len(projection.routing),
            "original_source_read_performed": False,
            "fixture_release": {
                "caller": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
                "fixture_config_id": fixture_config.config_id,
                "fixture_source_sha256": fixture_stream.source_sha256,
                "fixture_rows": fixture_stream.row_count,
                "release_ref": fixture_release.release_ref.as_dict(),
                "public_objects": len(fixture_release.public_objects),
                "expected_validation_release_matches": (
                    expected_release is not None
                    and expected_release.get("content_hash") == fixture_release.release_ref.content_hash
                ),
            },
        },
        "r03": {
            "entrypoint": "rawlsing_next.universal_grammar.types.OccurrenceKey",
            "candidate_count": r03_candidate_count,
            "unique_candidate_count": r03_unique_count,
            "item_identity_available": True,
            "form_exact": form_exact,
            "repeat_exact": repeat_exact,
            "route_exact": route_exact,
            "policy_exact": policy_exact,
            "inventory_constructed": False,
            "execution_performed": False,
            "form_slice": form_slice,
            "routing_unknown_count": routing_unknown,
            "risk_set_unresolved_count": risk_set_unresolved,
            "candidate_scope": "item-only candidate keys; not accepted as exact occurrences",
        },
        "first_missing": first_missing,
        "limits": {
            "original_source_read": False,
            "restricted_material_published": False,
            "original_workload_issued": False,
            "production_edit": False,
            "merge": False,
            "ci": False,
            "policy_fabricated": False,
            "r03_execution": False,
        },
        "owner_limits": {
            "source_form_route_risk": args.form_route_owner,
            "r03_policy_direction": args.r03_policy_owner + "; no policy is supplied here",
            "c11_original_read": "separate source-read permission owner; not exercised",
        },
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "source": result["source"]["source_id"],
        "edition_sha256": result["source"]["edition_sha256"],
        "c11_projection_ref": result["c11"]["projection_ref"],
        "fixture_release_ref": result["c11"]["fixture_release"]["release_ref"],
        "c11_counts": {key: result["c11"][key] for key in (
            "respondents", "questions", "response_slots", "coordinate_slots", "routing_facts")},
        "r03_candidates": r03_candidate_count,
        "form_exact": form_exact,
        "route_exact": route_exact,
        "policy_exact": policy_exact,
        "first_missing": first_missing,
        "execution_performed": False,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
