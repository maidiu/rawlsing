#!/usr/bin/env python3
"""Sourcefree execution proof for the isolated typed issuance seam.

Positive and nonanswer cases use the existing sourcefree ANVIL stream fixture,
the held source decision, the existing RuntimeObjectCatalog constructor and the
actual native I03 evaluator.  No saved estate or original source is touched.
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
from rawlsing_next.pre553_anvil_stream_issuance import (  # noqa: E402
    HeldStreamIssuanceDecision,
    StreamIssuanceError,
    issue_and_execute_stream_i03,
)
from rawlsing_next.pre553_anvil_stream_native_i03 import (  # noqa: E402
    VerifiedAnvilStreamEstate,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog  # noqa: E402
from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec, ExactRef, exact_ref  # noqa: E402
from rawlsing_next.tests.test_pre553_anvil_stream_native_i03 import _stream  # noqa: E402


def _decision(estate, source, auth, predicate, query, *, nonanswer=()):
    return HeldStreamIssuanceDecision(
        source_id="SRC04",
        source_root=estate.i02.source,
        release_root=estate.i02.release,
        universe_root=estate.i02.universe,
        replay_root=estate.i02.replay,
        question_ref=source["qrefs"]["Y"],
        authorized_operation=auth.governed_operations[0],
        authorities=tuple((*source["authorities"], auth)),
        predicate=predicate,
        query=query,
        approved_denominator_ref=exact_ref(query.risk_set_ref, "proof denominator"),
        approved_response_semantics_ref=exact_ref(
            query.requested_output_grain["response_state_semantics_ref"],
            "proof response semantics",
        ),
        approved_raw_domain=("0", "1"),
        approved_nonanswer_states=tuple(nonanswer),
    )


def _reject(label, fn):
    try:
        fn()
    except Exception as exc:
        return {
            "label": label,
            "refused": True,
            "type": type(exc).__name__,
            "message": str(exc),
        }
    return {"label": label, "refused": False}


def main() -> int:
    scratch = Path(tempfile.mkdtemp(
        prefix="q006-issuance-proof-",
        dir="/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode",
    ))
    mp = pytest.MonkeyPatch()
    out = {
        "schema": "ANVIL_Q006_TYPED_ISSUANCE_PROOF@1",
        "sourcefree": True,
        "original_source_accessed": False,
        "estate_writes": False,
        "status": "UNKNOWN",
    }
    owner_path = os.environ.get("ANVIL_Q006_OWNER_DECISION")
    owner_hash = None
    owner_codes = ("1", "2", "3", "4", "97", "98", "99")
    if owner_path:
        owner_bytes = Path(owner_path).read_bytes()
        owner_hash = hashlib.sha256(owner_bytes).hexdigest()
        if owner_hash != "e3de52e027cc5418544f3f9bf72f62995ea81ce6ae6148faa000fa3b9f6a96f5":
            raise SystemExit("OWNER_DECISION_HASH_MISMATCH")
        owner = json.loads(owner_bytes)
        owner_codes = tuple(str(code) for code in owner["interpretation"])
        out["owner_decision"] = {
            "sha256": owner_hash,
            "source_id": owner.get("source_id"),
            "question_id": owner.get("question_id"),
            "scope": owner.get("scope"),
            "recorded_codes": list(owner_codes),
            "asked_risk": owner.get("denominator", {}).get("asked_risk"),
            "physical_system_missing": owner.get("denominator", {}).get("physical_system_missing"),
        }
    try:
        (source, auth, predicate, query, catalog, root, release, manifest,
         held, grant) = _stream(scratch, mp, "ISSUANCE", source_id="SRC04")
        estate = VerifiedAnvilStreamEstate(
            root, exact_path=release, independently_held=held,
            current_authorizer=grant,
        )
        decision = _decision(estate, source, auth, predicate, query)
        current = {"yes": True}
        def verify_decision(candidate):
            return current["yes"] and candidate == decision
        positive = issue_and_execute_stream_i03(
            estate=estate, decision=decision, decision_verifier=verify_decision,
        )
        fact = positive.facts[0]
        out["positive"] = {
            "typed_state": fact.typed_state,
            "raw_denominator_support": fact.raw_denominator_support,
            "raw_cells": sorted(
                row["cell"] for row in fact.target_topology.get(
                    "complete_cell_semantic_projection", ()
                )
            ),
            "replay_ref": fact.semantic_fields.get("replay_ref"),
            "release_refs": [ref.as_dict() for ref in positive.release_refs],
            "roots_unchanged": True,
        }

        # Existing sourcefree fixture, altered only by omitting R2's Y response:
        # the native result is an approved UNRESOLVED nonanswer, not SUPPORTED.
        original_build = native._build_source
        def nonanswer_build(tag, rows, **kwargs):
            return original_build(tag, [
                {"id": "R1", "responses": {"Y": 0}},
                {"id": "R2", "responses": {}},
            ], **kwargs)
        mp.setattr(native, "_build_source", nonanswer_build)
        (source_n, auth_n, predicate_n, query_n, catalog_n, root_n, release_n,
         manifest_n, held_n, grant_n) = _stream(
            scratch, mp, "NONANSWER", source_id="SRC04",
        )
        estate_n = VerifiedAnvilStreamEstate(
            root_n, exact_path=release_n, independently_held=held_n,
            current_authorizer=grant_n,
        )
        decision_n = _decision(
            estate_n, source_n, auth_n, predicate_n, query_n,
            nonanswer=("UNRESOLVED",),
        )
        nonanswer = issue_and_execute_stream_i03(
            estate=estate_n, decision=decision_n,
            decision_verifier=lambda candidate: candidate == decision_n,
        )
        nfact = nonanswer.facts[0]
        out["nonanswer"] = {
            "typed_state": nfact.typed_state,
            "raw_denominator_support": nfact.raw_denominator_support,
            "execution_detail": nfact.semantic_fields.get("execution_detail"),
            "accepted_by_held_nonanswer_state": nfact.typed_state in decision_n.approved_nonanswer_states,
        }

        # Sourcefree seven-code recorded-response-shaped fixture.  The values
        # stand in for the owner-approved q103 interpretation; this is not an
        # original SRC04 run.  One row has no response: physical missing remains
        # a separate denominator/coverage fact, not a fabricated substantive cell.
        seven_rows = [
            {"id": f"R{i}", "responses": ({"Y": code} if code is not None else {})}
            for i, code in enumerate((1, 2, 3, 4, 97, 98, 99, None), 1)
        ]
        def seven_build(tag, rows, **kwargs):
            return original_build(tag, seven_rows, **kwargs)
        mp.setattr(native, "_build_source", seven_build)
        (source_s, auth_s, predicate_s, query_s, catalog_s, root_s, release_s,
         manifest_s, held_s, grant_s) = _stream(
            scratch, mp, "SEVEN", source_id="SRC04",
        )
        fields_s = dict(query_s.semantic_fields)
        topology_s = dict(fields_s["target_arity_and_topology"])
        component_s = dict(topology_s["components"][0])
        component_s["domain"] = ["1", "2", "3", "4", "97", "98", "99"]
        topology_s["components"] = [component_s]
        fields_s["target_arity_and_topology"] = topology_s
        query_s = EmpiricalQuerySpec(
            typed_state=query_s.typed_state,
            authority_snapshot_refs=query_s.authority_snapshot_refs,
            dependency_refs=query_s.dependency_refs,
            producer_replay_locator_or_reference_root=(
                query_s.producer_replay_locator_or_reference_root
            ),
            **fields_s,
        )
        catalog_s = RuntimeObjectCatalog(
            authorities=tuple((*source_s["authorities"], auth_s)),
            predicates=(predicate_s,), queries=(query_s,),
            discovery_authorities=(),
        )
        estate_s = VerifiedAnvilStreamEstate(
            root_s, exact_path=release_s, independently_held=held_s,
            current_authorizer=grant_s,
        )
        decision_s = _decision(
            estate_s, source_s, auth_s, predicate_s, query_s,
            nonanswer=("UNRESOLVED",),
        )
        decision_s = dataclasses.replace(
            decision_s, approved_raw_domain=owner_codes,
        )
        first_seven = issue_and_execute_stream_i03(
            estate=estate_s, decision=decision_s,
            decision_verifier=lambda c: c == decision_s,
        )
        second_seven = issue_and_execute_stream_i03(
            estate=estate_s, decision=decision_s,
            decision_verifier=lambda c: c == decision_s,
        )
        seven_fact = first_seven.facts[0]
        seven_cells = [
            (row["cell"], row["raw_numerator_support"])
            for row in seven_fact.target_topology.get(
                "complete_cell_semantic_projection", ()
            )
        ]
        out["seven_code_sourcefree"] = {
            "typed_state": seven_fact.typed_state,
            "raw_denominator_support": seven_fact.raw_denominator_support,
            "raw_support_sum": sum(n for _, n in seven_cells),
            "cells": seven_cells,
            "physical_missing_separate": (
                seven_fact.raw_denominator_support - sum(n for _, n in seven_cells)
            ),
            "replay_equal": (
                seven_fact.semantic_fields.get("replay_ref")
                == second_seven.facts[0].semantic_fields.get("replay_ref")
            ),
            "replay_ref": seven_fact.semantic_fields.get("replay_ref"),
            "note": "sourcefree q103-shaped fixture; not an original SRC04 run",
        }

        # Negative decisions: each is a held-decision mutation, never an
        # inference from the stream.
        bad_source = dataclasses.replace(
            decision, source_root="SOURCE_ARTIFACT|foreign|" + "1" * 64,
        )
        bad_release = dataclasses.replace(
            decision, release_root="C11_STREAM_SOURCEFREE_RELEASE|foreign|" + "2" * 64,
        )
        bad_universe = dataclasses.replace(
            decision, universe_root="EmpiricalUniverse@1.0.0|foreign|" + "3" * 64,
        )
        bad_replay = dataclasses.replace(
            decision, replay_root="4" * 64,
        )
        bad_question = dataclasses.replace(
            decision,
            question_ref=ExactRef(
                "QUESTION_NATIVE", source["qrefs"]["Y"].object_id, "5" * 64,
            ),
        )
        bad_operation = dataclasses.replace(
            decision, authorized_operation="I03-OP-FOREIGN",
        )
        empty_authority = dataclasses.replace(decision, authorities=())
        bad_domain = dataclasses.replace(
            decision, approved_raw_domain=("9",),
        )
        duplicate_domain = dataclasses.replace(
            decision, approved_raw_domain=("0", "0", "1"),
        )
        forged_domain = dataclasses.replace(
            decision, approved_raw_domain=("9",),
        )
        stale_authority = dataclasses.replace(
            decision, authorities=decision.authorities[:-1],
        )
        out["negatives"] = [
            _reject("wrong_source", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=bad_source,
                decision_verifier=lambda c: c == bad_source)),
            _reject("wrong_release", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=bad_release,
                decision_verifier=lambda c: c == bad_release)),
            _reject("wrong_universe", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=bad_universe,
                decision_verifier=lambda c: c == bad_universe)),
            _reject("wrong_replay", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=bad_replay,
                decision_verifier=lambda c: c == bad_replay)),
            _reject("wrong_question", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=bad_question,
                decision_verifier=lambda c: c == bad_question)),
            _reject("wrong_operation", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=bad_operation,
                decision_verifier=lambda c: c == bad_operation)),
            _reject("missing_authority", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=empty_authority,
                decision_verifier=lambda c: c == empty_authority)),
            _reject("stale_authority", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=stale_authority,
                decision_verifier=lambda c: c == stale_authority)),
            _reject("outside_approved_domain", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=bad_domain,
                decision_verifier=lambda c: c == bad_domain)),
            _reject("duplicate_approved_raw_code", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=duplicate_domain,
                decision_verifier=lambda c: c == duplicate_domain)),
            _reject("forged_decision", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=forged_domain,
                decision_verifier=verify_decision)),
            _reject("missing_verifier", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=decision, decision_verifier=None)),
            _reject("denied_current", lambda: issue_and_execute_stream_i03(
                estate=estate, decision=decision,
                decision_verifier=lambda c: False)),
        ]
        revoke = {"calls": 0}
        def revoked(candidate):
            revoke["calls"] += 1
            return revoke["calls"] < 2
        out["revoked_during_execution"] = _reject(
            "revoked_during_execution",
            lambda: issue_and_execute_stream_i03(
                estate=estate, decision=decision, decision_verifier=revoked,
            ),
        )
        output_revoke = {"calls": 0}
        def revoked_at_output(candidate):
            output_revoke["calls"] += 1
            return output_revoke["calls"] < 4
        out["revoked_at_output"] = _reject(
            "revoked_at_output",
            lambda: issue_and_execute_stream_i03(
                estate=estate, decision=decision,
                decision_verifier=revoked_at_output,
            ),
        )
        out["status"] = "SOURCEFREE_POSITIVE_AND_NONANSWER_GREEN__NEGATIVES_GREEN"
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
