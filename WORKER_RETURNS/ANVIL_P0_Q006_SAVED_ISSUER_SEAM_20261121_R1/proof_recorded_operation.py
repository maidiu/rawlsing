#!/usr/bin/env python3
"""Sourcefree seven-code recorded-response operation proof.

Builds the operation query/predicate from exact held operation fields, then
uses the existing native I03 path with a scoped recorded-routing projection.
No original SRC04 data or estate is touched.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

IMPLEMENTER = Path(os.environ.get(
    "ANVIL_IMPLEMENTER",
    "/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/REMONT_Q006_ISSUER",
)).resolve()
sys.path.insert(0, str(IMPLEMENTER))

import pytest  # noqa: E402
import rawlsing_next.tests.test_pre553_empirical_query as native  # noqa: E402
from rawlsing_next.pre553_anvil_stream_issuance import issue_and_execute_stream_i03  # noqa: E402
from rawlsing_next.pre553_anvil_stream_native_i03 import VerifiedAnvilStreamEstate  # noqa: E402
from rawlsing_next.pre553_anvil_stream_recorded import (  # noqa: E402
    HeldRecordedOperation,
    RecordedResponseError,
    build_recorded_operation,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog  # noqa: E402
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash  # noqa: E402
from rawlsing_next.tests.test_pre553_anvil_stream_native_i03 import _stream  # noqa: E402

OWNER = Path(os.environ.get(
    "ANVIL_Q006_OWNER_DECISION",
    "/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/"
    "evidence/P0_TWO_SAVED_WAVES_PRIVATE/q006_q103_owner_decision.json",
))
OWNER_SHA = "e3de52e027cc5418544f3f9bf72f62995ea81ce6ae6148faa000fa3b9f6a96f5"


def main() -> int:
    owner_bytes = OWNER.read_bytes()
    owner_sha = hashlib.sha256(owner_bytes).hexdigest()
    if owner_sha != OWNER_SHA:
        raise SystemExit("OWNER_DECISION_HASH_MISMATCH")
    owner = json.loads(owner_bytes)
    codes = tuple(str(code) for code in owner["interpretation"])
    scratch = Path(tempfile.mkdtemp(
        prefix="q006-recorded-operation-",
        dir="/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode",
    ))
    mp = pytest.MonkeyPatch()
    out = {
        "schema": "ANVIL_Q006_RECORDED_OPERATION_PROOF@1",
        "sourcefree": True,
        "original_source_accessed": False,
        "owner_decision_sha256": owner_sha,
        "owner_codes": list(codes),
        "status": "UNKNOWN",
    }
    try:
        rows = [
            {"id": f"R{i}", "responses": ({"Y": code} if code is not None else {})}
            for i, code in enumerate((1, 2, 3, 4, 97, 98, 99, None), 1)
        ]
        original_build = native._build_source
        def seven_build(tag, rows_arg, **kwargs):
            return original_build(tag, rows, **kwargs)
        mp.setattr(native, "_build_source", seven_build)
        (source, auth, predicate_unused, query_unused, catalog_unused, root, release,
         manifest, held, grant) = _stream(scratch, mp, "RECORDED", source_id="SRC04")
        estate = VerifiedAnvilStreamEstate(
            root, exact_path=release, independently_held=held,
            current_authorizer=grant,
        )
        question_ref = source["qrefs"]["Y"]
        risk_ref = ExactRef(
            "RISK_SET",
            "recorded-response-" + owner_sha + "-" + question_ref.content_hash,
            semantic_hash({"owner_decision_sha256": owner_sha, "codes": list(codes)}),
        )
        routing_rule_ref = ExactRef(
            "ROUTING_RULE",
            "recorded-only-" + owner_sha,
            semantic_hash({"owner_decision_sha256": owner_sha, "rule": "RECORDED_ONLY"}),
        )
        member_set_ref = ExactRef(
            "MEMBER_SET",
            "recorded-members-" + owner_sha,
            semantic_hash({"owner_decision_sha256": owner_sha, "set": "RECORDED"}),
        )
        operation = HeldRecordedOperation(
            owner_decision_sha256=owner_sha,
            source_id="SRC04",
            source_root=estate.i02.source,
            release_root=estate.i02.release,
            universe_root=estate.i02.universe,
            replay_root=estate.i02.replay,
            question_ref=question_ref,
            authorized_operation=auth.governed_operations[0],
            allowed_raw_codes=codes,
            interpretation=tuple(
                (str(code), str(owner["interpretation"][code][0]))
                for code in codes
            ),
            authorities=tuple((*source["authorities"], auth)),
            query_authority_ref=auth.authority_ref,
            routing_authority_ref=source["routing_auth"].authority_ref,
            source_authority_ref=source["source_auth"].authority_ref,
            recorded_risk_ref=risk_ref,
            routing_rule_ref=routing_rule_ref,
            member_set_replay_ref=member_set_ref,
            measure_basis_ref=ExactRef(
                "MEASURE_BASIS", "RAW", semantic_hash({"measure": "RAW"}),
            ),
            response_state_semantics_ref=ExactRef(
                "RESPONSE_STATE_SEMANTICS", "RECORDED_ONLY",
                semantic_hash({"semantics": "RECORDED_ONLY", "codes": list(codes)}),
            ),
            target_domain_replay_ref=ExactRef(
                "TARGET_DOMAIN", "recorded-" + question_ref.content_hash,
                semantic_hash({"question": question_ref.as_dict(), "codes": list(codes)}),
            ),
            predicate_replay_root=ExactRef(
                "REPLAY_ROOT", "recorded-predicate-" + owner_sha,
                semantic_hash({"kind": "predicate", "owner": owner_sha}),
            ),
            query_replay_root=ExactRef(
                "REPLAY_ROOT", "recorded-query-" + owner_sha,
                semantic_hash({"kind": "query", "owner": owner_sha}),
            ),
        )
        decision, recorded_routing, missing = build_recorded_operation(
            estate=estate, operation=operation, question_ref=question_ref,
        )
        out["built"] = {
            "allowed_codes": list(operation.allowed_raw_codes),
            "recorded_routing_facts": len(recorded_routing),
            "physical_missing_respondents": missing,
            "query_ref": decision.query.ref.as_dict(),
            "predicate_ref": decision.predicate.ref.as_dict(),
        }
        first = issue_and_execute_stream_i03(
            estate=estate, decision=decision,
            decision_verifier=lambda candidate: candidate == decision,
            recorded_routing=recorded_routing,
        )
        second = issue_and_execute_stream_i03(
            estate=estate, decision=decision,
            decision_verifier=lambda candidate: candidate == decision,
            recorded_routing=recorded_routing,
        )
        fact = first.facts[0]
        cells = [
            (row["cell"], row["raw_numerator_support"], row["cell_state"])
            for row in fact.target_topology.get("complete_cell_semantic_projection", ())
        ]
        out["native"] = {
            "typed_state": fact.typed_state,
            "raw_denominator_support": fact.raw_denominator_support,
            "raw_numerator_support": fact.raw_numerator_support,
            "cells": cells,
            "recorded_codes_present": [c for c, _, _ in cells],
            "physical_missing_excluded": missing,
            "replay_equal": (
                fact.semantic_fields.get("replay_ref")
                == second.facts[0].semantic_fields.get("replay_ref")
            ),
            "replay_ref": fact.semantic_fields.get("replay_ref"),
            "release_refs": [ref.as_dict() for ref in first.release_refs],
        }

        # Negative operation/authority paths.
        bad_release = dataclasses.replace(
            operation,
            release_root="C11_STREAM_SOURCEFREE_RELEASE|foreign|" + "2" * 64,
        )
        missing_authority = dataclasses.replace(operation, authorities=())
        bad_source = dataclasses.replace(
            operation, source_root="SOURCE_ARTIFACT|foreign|" + "1" * 64,
        )
        duplicate_codes = dataclasses.replace(
            operation, allowed_raw_codes=("1", "1", "2", "3", "4", "97", "98", "99"),
        )
        unknown_codes = dataclasses.replace(
            operation, allowed_raw_codes=("1", "2", "3", "4", "97", "98"),
        )
        def reject(label, fn):
            try:
                fn()
            except Exception as exc:
                return {"label": label, "refused": True,
                        "type": type(exc).__name__, "message": str(exc)}
            return {"label": label, "refused": False}
        neg = [
            reject("wrong_release", lambda: build_recorded_operation(
                estate=estate, operation=bad_release, question_ref=question_ref)),
            reject("wrong_source", lambda: build_recorded_operation(
                estate=estate, operation=bad_source, question_ref=question_ref)),
            reject("missing_authority", lambda: build_recorded_operation(
                estate=estate, operation=missing_authority, question_ref=question_ref)),
            reject("duplicate_code", lambda: build_recorded_operation(
                estate=estate, operation=duplicate_codes, question_ref=question_ref)),
            reject("unknown_code", lambda: build_recorded_operation(
                estate=estate, operation=unknown_codes, question_ref=question_ref)),
            reject("denied_verifier", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=decision,
                decision_verifier=lambda candidate: False,
                recorded_routing=recorded_routing)),
        ]
        out["negatives"] = neg
        out["status"] = (
            "RECORDED_ONLY_NATIVE_SEVEN_CODE_GREEN__DENOMINATOR_7"
            if fact.raw_denominator_support == 7
            and len(cells) == 7
            and all(x["refused"] for x in neg)
            else "RECORDED_ONLY_NATIVE_INVARIANT_FAULT"
        )
    except Exception as exc:
        out["status"] = "ERROR"
        out["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        mp.undo()
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
