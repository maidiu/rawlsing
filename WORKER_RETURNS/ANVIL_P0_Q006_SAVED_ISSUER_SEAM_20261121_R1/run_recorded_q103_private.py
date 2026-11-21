#!/usr/bin/env python3
"""Private MainMac harness contract for the recorded-only q103 native read.

It loads the held owner decision, requires an exact operation document containing
the authority/ref preimages, constructs the recorded operation, and executes the
existing native I03 path.  No original estate is touched by the author run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from types import MappingProxyType

from rawlsing_next.pre553_anvil_stream_native_i03 import VerifiedAnvilStreamEstate
from rawlsing_next.pre553_anvil_stream_issuance import issue_and_execute_stream_i03
from rawlsing_next.pre553_anvil_stream_recorded import (
    HeldRecordedOperation,
    build_recorded_operation,
)
from rawlsing_next.pre553_anvil_stream_carrier_qualification import HeldStreamPins
from rawlsing_next.pre553_carrier_execution import materialize_public_object
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    exact_ref,
)


def _ref(value):
    return exact_ref(value)


def _authority_ref(value):
    if isinstance(value, AuthorityRef):
        return value
    return AuthorityRef(
        value["authority_id"], value["authority_version"],
        value["authority_content_hash"],
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner-decision", type=Path, required=True)
    ap.add_argument("--operation-json", type=Path, required=True)
    ap.add_argument("--stream-root", type=Path, required=True)
    ap.add_argument("--release-path", type=Path, required=True)
    args = ap.parse_args()
    owner_bytes = args.owner_decision.read_bytes()
    owner_sha = hashlib.sha256(owner_bytes).hexdigest()
    if owner_sha != "e3de52e027cc5418544f3f9bf72f62995ea81ce6ae6148faa000fa3b9f6a96f5":
        raise SystemExit("OWNER_DECISION_HASH_MISMATCH")
    owner = json.loads(owner_bytes)
    binding = owner["source_binding"]
    roots = binding["saved_i02"]
    held = HeldStreamPins(
        source_id=owner["source_id"],
        source_sha256=binding["source_sha256"],
        manifest_sha256=binding["manifest_sha256"],
        exact_release_path=str(args.release_path),
        roots=roots,
    )
    estate = VerifiedAnvilStreamEstate(
        args.stream_root, exact_path=args.release_path,
        independently_held=held,
        # Exact owner/stream current binding, not a true-for-anything callback.
        current_authorizer=lambda pins: (
            pins.manifest_sha256 == binding["manifest_sha256"]
            and pins.source_sha256 == binding["source_sha256"]
        ),
    )
    doc = json.loads(args.operation_json.read_text())
    authorities = tuple(
        materialize_public_object(item) for item in doc["authorities"]
    )
    if any(type(item) is not AuthoritySnapshot for item in authorities):
        raise SystemExit("OPERATION_AUTHORITY_FAMILY_MISMATCH")
    operation = HeldRecordedOperation(
        owner_decision_sha256=owner_sha,
        source_id=doc["source_id"],
        source_root=doc["source_root"],
        release_root=doc["release_root"],
        universe_root=doc["universe_root"],
        replay_root=doc["replay_root"],
        question_ref=_ref(doc["question_ref"]),
        authorized_operation=doc["authorized_operation"],
        allowed_raw_codes=tuple(str(x) for x in doc["allowed_raw_codes"]),
        interpretation=tuple((str(a), str(b)) for a, b in doc["interpretation"]),
        authorities=authorities,
        query_authority_ref=_authority_ref(doc["query_authority_ref"]),
        routing_authority_ref=_authority_ref(doc["routing_authority_ref"]),
        source_authority_ref=_authority_ref(doc["source_authority_ref"]),
        recorded_risk_ref=_ref(doc["recorded_risk_ref"]),
        routing_rule_ref=_ref(doc["routing_rule_ref"]),
        member_set_replay_ref=_ref(doc["member_set_replay_ref"]),
        measure_basis_ref=_ref(doc["measure_basis_ref"]),
        response_state_semantics_ref=_ref(doc["response_state_semantics_ref"]),
        target_domain_replay_ref=_ref(doc["target_domain_replay_ref"]),
        predicate_replay_root=_ref(doc["predicate_replay_root"]),
        query_replay_root=_ref(doc["query_replay_root"]),
        transform_ref=_ref(doc["transform_ref"]),
        approved_nonanswer_states=tuple(doc.get("approved_nonanswer_states", ())),
    )
    decision, plan, missing = build_recorded_operation(
        estate=estate, operation=operation, question_ref=operation.question_ref,
    )
    result = issue_and_execute_stream_i03(
        estate=estate, decision=decision,
        decision_verifier=lambda candidate: candidate == decision,
        recorded_plan=plan,
    )
    out = {
        "schema": "ANVIL_Q006_RECORDED_Q103_PRIVATE_RESULT@1",
        "owner_decision_sha256": owner_sha,
        "query_ref": decision.query.ref.as_dict(),
        "predicate_ref": decision.predicate.ref.as_dict(),
        "missing": missing,
        "facts": [
            {
                "typed_state": fact.typed_state,
                "raw_denominator_support": fact.raw_denominator_support,
                "raw_numerator_support": fact.raw_numerator_support,
                "cells": [
                    [row["cell"], row["raw_numerator_support"], row["cell_state"]]
                    for row in fact.target_topology.get(
                        "complete_cell_semantic_projection", ()
                    )
                ],
                "replay_ref": fact.semantic_fields.get("replay_ref"),
            }
            for fact in result.facts
        ],
        "release_refs": [ref.as_dict() for ref in result.release_refs],
    }
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
