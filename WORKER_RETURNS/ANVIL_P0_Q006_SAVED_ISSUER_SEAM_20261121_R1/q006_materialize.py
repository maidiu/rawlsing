#!/usr/bin/env python3
"""Materialize the private Q006 q103 recorded-operation artifact from the
exact owner decision, held R2 decision and existing q006 private inputs.

The output is private mode 0600.  This script never reads original microdata.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    semantic_hash,
)


OWNER_SHA = "e3de52e027cc5418544f3f9bf72f62995ea81ce6ae6148faa000fa3b9f6a96f5"


def _ref(value):
    if isinstance(value, dict):
        value = "|".join((value["kind"], value["object_id"], value["content_hash"]))
    parts = value.split("|") if isinstance(value, str) else []
    if len(parts) != 3:
        raise SystemExit(
            "Q006_EXACT_QUESTION_REF_MISSING: independently held custody "
            "provides only the native question object ID, not the full "
            "kind|object_id|content_hash question ref; supply --question-ref "
            "from custody"
        )
    return ExactRef(parts[0], parts[1], parts[2])


def _authority_ref(value):
    if isinstance(value, dict):
        value = value
    else:
        value = {"authority_id": value, "authority_version": "1.0.0",
                 "authority_content_hash": hashlib.sha256(str(value).encode()).hexdigest()}
    return AuthorityRef(value["authority_id"], value["authority_version"],
                        value["authority_content_hash"])


def _authority(owner_sha, role, operation, scope, roots, codes, kind, families):
    material = {
        "owner_decision_sha256": owner_sha,
        "role": role,
        "operation": operation,
        "scope": scope,
        "roots": roots,
        "codes": list(codes),
    }
    digest = semantic_hash(material)
    universe = _ref(roots["universe"])
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(ExactRef(
            "OWNER_DECISION", "q006-q103-" + owner_sha, owner_sha,
        ),),
        producer_replay_locator_or_reference_root=ExactRef(
            "REPLAY_ROOT", "q006-" + role + "-" + owner_sha, digest,
        ),
        authority_id="Q006-Q103-" + role,
        authority_version="1.0.0",
        authority_content_hash=digest,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=(operation,),
        governed_object_families=tuple(families),
        scope_envelope={
            "source_universe_refs": [universe.as_dict()],
            "source_sha256": roots["source"],
            "release": roots["release"],
            "scope": scope,
            "recorded_raw_codes": list(codes),
        },
        effective_time_or_interval="OWNER_DECISION_CURRENT",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash(material),
        replay_protocol_ref=ExactRef(
            "REPLAY_PROTOCOL", "q006-" + role, digest,
        ),
    )


def validate_operation_authorities(authorities, operation, universe_root):
    """Exercise the same positive-authority checks before any estate read."""
    universe = _ref(universe_root)
    registry = AuthorityRegistry(tuple(authorities))
    for authority in authorities:
        for family in authority.governed_object_families:
            registry.require(
                authority.authority_ref,
                operation=operation,
                object_family=family,
                source_universe_ref=universe.as_dict(),
            )
    return True


def materialize(*, owner_path: Path, r2_path: Path, q006_dir: Path, output: Path, question_ref=None):
    owner_bytes = owner_path.read_bytes()
    if hashlib.sha256(owner_bytes).hexdigest() != OWNER_SHA:
        raise SystemExit("OWNER_DECISION_HASH_MISMATCH")
    owner = json.loads(owner_bytes)
    r2 = json.loads(r2_path.read_bytes())
    src = r2["waves"]["SRC04"]
    if owner["source_binding"] != {k: src[k] for k in (
        "custody_estate_path", "decision_ref", "manifest_sha256",
        "saved_i02", "source_sha256",
    )}:
        raise SystemExit("R2_SOURCE_BINDING_MISMATCH")
    inputs = json.loads((q006_dir / "inputs_private.json").read_text())
    if inputs["decision_sha256"] != OWNER_SHA:
        raise SystemExit("Q006_INPUT_DECISION_HASH_MISMATCH")
    roots = src["saved_i02"]
    if roots != inputs["source_binding"]["saved_i02"]:
        raise SystemExit("Q006_ROOT_BINDING_MISMATCH")
    question = _ref(question_ref or inputs["native_question_ref"])
    codes = tuple(str(code) for code in owner["denominator"]["recorded_raw_codes"])
    if tuple(str(code) for code in inputs["recorded_raw_codes"]) != codes:
        raise SystemExit("Q006_CODE_BINDING_MISMATCH")
    interpretation = tuple(
        (str(code), str(owner["interpretation"][code][0]))
        for code in codes
    )
    scope = owner["scope"]
    operation = "Q103-OP-RECORDED-RESPONSE-ONLY"
    owner_scope = {
        "host": owner["host"],
        "scope": scope,
        "question_id": owner["question_id"],
        "questionnaire_sha256": owner["questionnaire_sha256"],
        "denominator": owner["denominator"],
    }
    source_auth = _authority(
        OWNER_SHA, "SOURCE", operation, owner_scope, roots, codes,
        "SOURCE_SEMANTICS_TOPOLOGY",
        ("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0",
         "RoutingEligibilityFact@1.0.0"),
    )
    routing_auth = _authority(
        OWNER_SHA, "ROUTING", operation, owner_scope, roots, codes,
        "ROUTING_RISK_SET", ("RoutingEligibilityFact@1.0.0",),
    )
    query_auth = _authority(
        OWNER_SHA, "QUERY", operation, owner_scope, roots, codes,
        "PREDICATE_GRAMMAR",
        ("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0",
         "EmpiricalFact@1.0.0"),
    )
    suffix = semantic_hash({"owner": OWNER_SHA, "codes": codes})
    op = {
        "schema": "ANVIL_Q006_Q103_OPERATION@1",
        "owner_decision_sha256": OWNER_SHA,
        "source_id": "SRC04",
        "source_root": roots["source"],
        "release_root": roots["release"],
        "universe_root": roots["universe"],
        "replay_root": roots["replay"],
        "question_ref": question.as_dict(),
        "authorized_operation": operation,
        "allowed_raw_codes": list(codes),
        "interpretation": [list(x) for x in interpretation],
        "authorities": [x.as_dict() for x in (source_auth, routing_auth, query_auth)],
        "query_authority_ref": query_auth.authority_ref.as_dict(),
        "routing_authority_ref": routing_auth.authority_ref.as_dict(),
        "source_authority_ref": source_auth.authority_ref.as_dict(),
        "recorded_risk_ref": {
            "kind": "RISK_SET",
            "object_id": "urn:rawlsing:q006:q103:recorded:" + suffix,
            "content_hash": suffix,
        },
        "routing_rule_ref": {
            "kind": "ROUTING_RULE",
            "object_id": "urn:rawlsing:q006:q103:recorded-only:" + suffix,
            "content_hash": suffix,
        },
        "member_set_replay_ref": {
            "kind": "MEMBER_SET",
            "object_id": "urn:rawlsing:q006:q103:members:" + suffix,
            "content_hash": suffix,
        },
        "measure_basis_ref": {
            "kind": "MEASURE_BASIS",
            "object_id": "urn:rawlsing:q006:q103:RAW:" + suffix,
            "content_hash": semantic_hash({"measure": "RAW", "owner": OWNER_SHA}),
        },
        "response_state_semantics_ref": {
            "kind": "RESPONSE_STATE_SEMANTICS",
            "object_id": "urn:rawlsing:q006:q103:recorded-only:" + suffix,
            "content_hash": semantic_hash({"interpretation": interpretation, "owner": OWNER_SHA}),
        },
        "target_domain_replay_ref": {
            "kind": "TARGET_DOMAIN",
            "object_id": "urn:rawlsing:q006:q103:domain:" + suffix,
            "content_hash": semantic_hash({"question": question.as_dict(), "codes": list(codes)}),
        },
        "predicate_replay_root": {
            "kind": "REPLAY_ROOT",
            "object_id": "urn:rawlsing:q006:q103:predicate:" + suffix,
            "content_hash": semantic_hash({"kind": "predicate", "owner": OWNER_SHA}),
        },
        "query_replay_root": {
            "kind": "REPLAY_ROOT",
            "object_id": "urn:rawlsing:q006:q103:query:" + suffix,
            "content_hash": semantic_hash({"kind": "query", "owner": OWNER_SHA}),
        },
        "transform_ref": {
            "kind": "RECORDED_VALUE_TRANSFORM",
            "object_id": "urn:rawlsing:q006:q103:transform:" + suffix,
            "content_hash": semantic_hash({"transform": "R5_RAW_TO_RECORDED_OWNER_INTERPRETATION", "owner": OWNER_SHA}),
        },
        "approved_nonanswer_states": ["UNRESOLVED"],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(op, stream, indent=2, sort_keys=True)
        stream.write("\n")
    os.chmod(output, 0o600)
    return output, hashlib.sha256(output.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner-decision", type=Path, required=True)
    ap.add_argument("--r2-decision", type=Path, required=True)
    ap.add_argument("--q006-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--question-ref", default=None)
    args = ap.parse_args()
    output, digest = materialize(
        owner_path=args.owner_decision, r2_path=args.r2_decision,
        q006_dir=args.q006_dir, output=args.output,
        question_ref=args.question_ref,
    )
    print(json.dumps({"schema": "ANVIL_Q006_OPERATION_MATERIALIZED@1",
                      "output": str(output), "sha256": digest,
                      "mode": oct(output.stat().st_mode & 0o777)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
