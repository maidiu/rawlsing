#!/usr/bin/env python3
"""Private SRC16 racpres recorded-only driver.

The owner decision, current-use successor, historical closure and operation
document are supplied by the controller.  This script performs the exact
preflight before any cold estate/index open, then uses the existing recorded
I03 issuance path.  It does not issue authority or infer source semantics.
"""
from __future__ import annotations

import argparse
import dataclasses
from hashlib import sha256
import json
import os
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from typing import Any, Mapping

from rawlsing_next.pre553_anvil_stream_carrier_qualification import HeldStreamPins
from rawlsing_next.pre553_anvil_stream_native_i03 import VerifiedAnvilStreamEstate
from rawlsing_next.pre553_anvil_stream_issuance import issue_and_execute_stream_i03
from rawlsing_next.pre553_anvil_stream_recorded import (
    HeldRecordedOperation,
    RecordedUniverseUse,
    build_recorded_operation,
)
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, canonical_json

from src16_operator import (
    OPERATION,
    Src16Dependency,
    Src16OperatorError,
    validate_preflight,
)


def _ref(value: Any) -> ExactRef:
    if isinstance(value, ExactRef):
        return value
    if isinstance(value, str):
        parts = value.split("|")
        if len(parts) == 3 and all(parts):
            return ExactRef(parts[0], parts[1], parts[2])
    if isinstance(value, dict):
        return ExactRef(value["kind"], value["object_id"], value["content_hash"])
    raise Src16OperatorError("SRC16_EXACT_REF_INVALID")


def _authority_ref(value: Any) -> AuthorityRef:
    if isinstance(value, AuthorityRef):
        return value
    return AuthorityRef(
        value["authority_id"], value["authority_version"],
        value["authority_content_hash"],
    )


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value


def _stored_code_cell(code: str, state: str) -> Any:
    if state == "SUBSTANTIVE_RESPONSE":
        text = str(code)
        body = text[1:] if text.startswith("-") else text
        return int(text) if body.isdigit() else text
    return {"typed_response_state": state}


def _write_private(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
    os.chmod(path, 0o600)


def _positive_current(
    *, owner_path: Path, operation_path: Path, use_path: Path,
    closure_path: Path, expected_sha: str, expected_op_sha: str,
    expected_use_sha: str, expected_closure_sha: str,
) -> bool:
    return (
        sha256(owner_path.read_bytes()).hexdigest() == expected_sha
        and sha256(operation_path.read_bytes()).hexdigest() == expected_op_sha
        and sha256(use_path.read_bytes()).hexdigest() == expected_use_sha
        and sha256(closure_path.read_bytes()).hexdigest() == expected_closure_sha
    )


def prepare_and_run(
    *, owner_path: Path, operation_path: Path, r2_path: Path,
    stream_root: Path, release_path: Path,
    universe_use_path: Path, universe_closure_path: Path,
) -> dict[str, Any]:
    owner_bytes = owner_path.read_bytes()
    operation_bytes = operation_path.read_bytes()
    use_bytes = universe_use_path.read_bytes()
    closure_bytes = universe_closure_path.read_bytes()
    r2 = json.loads(r2_path.read_bytes())
    owner = json.loads(owner_bytes)
    source_id = owner.get("source_id")
    if source_id != "SRC16":
        raise Src16OperatorError("SRC16_OWNER_SOURCE_MISMATCH")
    binding = owner.get("source_binding")
    if not isinstance(binding, dict):
        raise Src16OperatorError("SRC16_OWNER_BINDING_MISSING")
    roots = binding.get("saved_i02")
    if not isinstance(roots, dict):
        raise Src16OperatorError("SRC16_OWNER_ROOTS_MISSING")
    operation_doc = json.loads(operation_bytes)
    for key in ("source_root", "release_root", "universe_root", "replay_root"):
        if operation_doc.get(key) != roots.get(key.replace("_root", "")):
            raise Src16OperatorError("SRC16_OPERATION_ROOT_MISMATCH", key)
    if operation_doc.get("source_id") != source_id:
        raise Src16OperatorError("SRC16_OPERATION_SOURCE_MISMATCH")
    if operation_doc.get("authorized_operation") != OPERATION:
        raise Src16OperatorError("SRC16_OPERATION_NAME_MISMATCH")

    # Exact current positive authorization, raw-domain shape and structured
    # owner scope are checked here, before the cold index/estate is opened.
    prepared = validate_preflight(
        owner_bytes=owner_bytes, r2=r2, operation_bytes=operation_bytes,
        use_bytes=use_bytes, closure_bytes=closure_bytes,
    )
    expected_hashes = (
        sha256(owner_bytes).hexdigest(),
        sha256(operation_bytes).hexdigest(),
        sha256(use_bytes).hexdigest(),
        sha256(closure_bytes).hexdigest(),
    )
    if not _positive_current(
        owner_path=owner_path, operation_path=operation_path,
        use_path=universe_use_path, closure_path=universe_closure_path,
        expected_sha=expected_hashes[0], expected_op_sha=expected_hashes[1],
        expected_use_sha=expected_hashes[2], expected_closure_sha=expected_hashes[3],
    ):
        raise Src16OperatorError("SRC16_POSITIVE_CURRENT_REVOKED_BEFORE_READ")

    held = HeldStreamPins(
        source_id=source_id,
        source_sha256=binding["source_sha256"],
        manifest_sha256=binding["manifest_sha256"],
        exact_release_path=str(release_path),
        roots=roots,
    )
    estate = VerifiedAnvilStreamEstate(
        stream_root, exact_path=release_path, independently_held=held,
        current_authorizer=lambda pins: _positive_current(
            owner_path=owner_path, operation_path=operation_path,
            use_path=universe_use_path, closure_path=universe_closure_path,
            expected_sha=expected_hashes[0], expected_op_sha=expected_hashes[1],
            expected_use_sha=expected_hashes[2], expected_closure_sha=expected_hashes[3],
        ),
    )
    operation = HeldRecordedOperation(
        owner_decision_sha256=prepared.owner_sha256,
        source_id=operation_doc["source_id"],
        source_root=operation_doc["source_root"],
        release_root=operation_doc["release_root"],
        universe_root=operation_doc["universe_root"],
        replay_root=operation_doc["replay_root"],
        question_ref=_ref(operation_doc["question_ref"]),
        authorized_operation=operation_doc["authorized_operation"],
        allowed_raw_codes=tuple(str(x) for x in operation_doc["allowed_raw_codes"]),
        interpretation=prepared.interpretation,
        authorities=prepared.authorities,
        query_authority_ref=_authority_ref(operation_doc["query_authority_ref"]),
        routing_authority_ref=_authority_ref(operation_doc["routing_authority_ref"]),
        source_authority_ref=_authority_ref(operation_doc["source_authority_ref"]),
        recorded_risk_ref=_ref(operation_doc["recorded_risk_ref"]),
        routing_rule_ref=_ref(operation_doc["routing_rule_ref"]),
        member_set_replay_ref=_ref(operation_doc["member_set_replay_ref"]),
        measure_basis_ref=_ref(operation_doc["measure_basis_ref"]),
        response_state_semantics_ref=_ref(
            operation_doc["response_state_semantics_ref"]
        ),
        target_domain_replay_ref=_ref(operation_doc["target_domain_replay_ref"]),
        predicate_replay_root=_ref(operation_doc["predicate_replay_root"]),
        query_replay_root=_ref(operation_doc["query_replay_root"]),
        transform_ref=_ref(operation_doc["transform_ref"]),
        approved_nonanswer_states=tuple(
            str(x) for x in operation_doc.get("approved_nonanswer_states", ())
        ),
        state_bearing_raw_codes=bool(
            operation_doc.get("state_bearing_raw_codes", False)
        ),
    )
    decision, plan, missing = build_recorded_operation(
        estate=estate, operation=operation, question_ref=operation.question_ref,
    )

    historical = next(
        (a for a in estate.iter_family("AuthoritySnapshot")
         if a.ref == prepared.historical_ref), None,
    )
    if historical is None:
        raise Src16OperatorError("SRC16_HISTORICAL_SNAPSHOT_MISSING")
    if historical.decision_state != "DEFER":
        raise Src16OperatorError("SRC16_HISTORICAL_SNAPSHOT_NOT_DEFER")
    use_doc = json.loads(use_bytes)
    if "positive_snapshot_ref" in use_doc:
        if _ref(use_doc["positive_snapshot_ref"]) != prepared.positive.ref:
            raise Src16OperatorError("SRC16_USE_POSITIVE_SNAPSHOT_MISMATCH")
    use = RecordedUniverseUse(
        historical_snapshot=historical,
        positive_snapshot=prepared.positive,
        owner_decision_sha256=prepared.owner_sha256,
        operation_document_sha256=expected_hashes[1],
        source_id=operation.source_id,
        source_root=operation.source_root,
        release_root=operation.release_root,
        universe_root=operation.universe_root,
        replay_root=operation.replay_root,
        question_ref=operation.question_ref,
        query_ref=decision.query.ref,
        predicate_ref=decision.predicate.ref,
        operation=operation.authorized_operation,
        risk_ref=operation.recorded_risk_ref,
        interpretation=operation.interpretation,
        scope=prepared.expected_scope,
        current_verifier=lambda: _positive_current(
            owner_path=owner_path, operation_path=operation_path,
            use_path=universe_use_path, closure_path=universe_closure_path,
            expected_sha=expected_hashes[0], expected_op_sha=expected_hashes[1],
            expected_use_sha=expected_hashes[2], expected_closure_sha=expected_hashes[3],
        ),
        historical_scope_grade=prepared.historical_scope_grade,
    )
    plan = dataclasses.replace(plan, universe_use=use)
    universe_objects = tuple(estate.iter_family("EmpiricalUniverse"))
    if len(universe_objects) != 1 or universe_objects[0].ref.key != estate.i02.universe:
        raise Src16OperatorError("SRC16_EXACT_UNIVERSE_OBJECT_MISSING")
    use.authorize(universe_objects[0], decision.query, decision.predicate)

    def verify_decision(candidate):
        return (
            _positive_current(
                owner_path=owner_path, operation_path=operation_path,
                use_path=universe_use_path, closure_path=universe_closure_path,
                expected_sha=expected_hashes[0], expected_op_sha=expected_hashes[1],
                expected_use_sha=expected_hashes[2], expected_closure_sha=expected_hashes[3],
            )
            and candidate.source_id == decision.source_id
            and candidate.source_root == decision.source_root
            and candidate.release_root == decision.release_root
            and candidate.universe_root == decision.universe_root
            and candidate.replay_root == decision.replay_root
            and candidate.question_ref == decision.question_ref
            and candidate.authorized_operation == decision.authorized_operation
            and candidate.authorities == decision.authorities
            and candidate.predicate == decision.predicate
            and candidate.query == decision.query
            and candidate.approved_denominator_ref == decision.approved_denominator_ref
            and candidate.approved_response_semantics_ref == decision.approved_response_semantics_ref
            and candidate.approved_raw_domain == decision.approved_raw_domain
            and candidate.approved_nonanswer_states == decision.approved_nonanswer_states
        )

    result = issue_and_execute_stream_i03(
        estate=estate, decision=decision,
        decision_verifier=verify_decision, recorded_plan=plan,
    )
    cell_counts = {
        canonical_json(row["cell"]): row["raw_numerator_support"]
        for row in result.facts[0].target_topology.get(
            "complete_cell_semantic_projection", ()
        )
    } if result.facts else {}
    return {
        "schema": "ANVIL_Q006_SRC16_RECORDED_PRIVATE_RESULT@1",
        "source_id": source_id,
        "owner_decision_sha256": prepared.owner_sha256,
        "question_ref": decision.question_ref.as_dict(),
        "historical_snapshot_ref": prepared.historical_ref.as_dict(),
        "positive_snapshot_ref": prepared.positive.ref.as_dict(),
        "missing": missing,
        "scope_kind": operation_doc.get("scope_kind"),
        "state_bearing_raw_codes": operation.state_bearing_raw_codes,
        "asked_eligibility": operation_doc.get("asked_eligibility"),
        "substantive_vote_denominator": operation_doc.get(
            "substantive_vote_denominator"
        ),
        "stored_code_bins": [
            {
                "raw_code": code,
                "state": state,
                "cell": _stored_code_cell(code, state),
                "raw_numerator_support": cell_counts.get(
                    canonical_json(_stored_code_cell(code, state)), 0
                ),
            }
            for code, state in prepared.interpretation
        ],
        "facts": [
            {
                "typed_state": fact.typed_state,
                "p02_failure_state": fact.semantic_fields.get("p02_failure_state"),
                "execution_detail": fact.semantic_fields.get("execution_detail"),
                "raw_denominator_support": fact.raw_denominator_support,
                "raw_numerator_support": fact.raw_numerator_support,
                "cells": [
                    [
                        _plain(row["cell"]),
                        row["raw_numerator_support"],
                        row["cell_state"],
                    ]
                    for row in fact.target_topology.get(
                        "complete_cell_semantic_projection", ()
                    )
                ],
                "replay_ref": _plain(fact.semantic_fields.get("replay_ref")),
            }
            for fact in result.facts
        ],
        "positive_counts_accepted": bool(
            result.facts
            and result.facts[0].typed_state == "SUPPORTED"
            and result.facts[0].raw_denominator_support > 0
            and len(result.facts[0].target_topology.get(
                "complete_cell_semantic_projection", ()
            )) > 0
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner-decision", type=Path, required=True)
    ap.add_argument("--operation-json", type=Path, required=True)
    ap.add_argument("--r2-decision", type=Path, required=True)
    ap.add_argument("--stream-root", type=Path, required=True)
    ap.add_argument("--release-path", type=Path, required=True)
    ap.add_argument("--universe-use-decision", type=Path, required=True)
    ap.add_argument("--universe-closure", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    try:
        result = prepare_and_run(
            owner_path=args.owner_decision,
            operation_path=args.operation_json,
            r2_path=args.r2_decision,
            stream_root=args.stream_root,
            release_path=args.release_path,
            universe_use_path=args.universe_use_decision,
            universe_closure_path=args.universe_closure,
        )
    except Src16Dependency as exc:
        result = {
            "schema": "ANVIL_Q006_SRC16_RECORDED_EXACT_HOLD@1",
            "status": "EXACT_HOLD",
            "dependency": exc.code,
            "detail": exc.detail,
        }
        _write_private(args.output, result)
        return 2
    except Src16OperatorError as exc:
        result = {
            "schema": "ANVIL_Q006_SRC16_RECORDED_OPERATOR_REFUSAL@1",
            "status": "REFUSED",
            "code": exc.code,
            "detail": exc.detail,
        }
        _write_private(args.output, result)
        return 1
    _write_private(args.output, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
