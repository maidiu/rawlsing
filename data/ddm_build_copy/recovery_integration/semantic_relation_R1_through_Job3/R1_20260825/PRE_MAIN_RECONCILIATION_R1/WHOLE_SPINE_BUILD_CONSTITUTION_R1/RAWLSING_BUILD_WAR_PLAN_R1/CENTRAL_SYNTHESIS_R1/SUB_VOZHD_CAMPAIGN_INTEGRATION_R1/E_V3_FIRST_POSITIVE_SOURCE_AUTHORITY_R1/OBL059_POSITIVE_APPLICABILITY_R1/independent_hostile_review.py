"""Exactly one fresh hostile review of frozen OBL059 R1 candidate.

Reviewer role is intentionally separate from implementation role. This script
attacks the frozen executable only; it has no repair or adoption authority.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from positive_applicability_authority import (
    NEGATIVE_DECISION,
    POSITIVE_DECISION,
    evaluate_direct_positive_applicability,
)
from governed_bounded_court import fixture

REVIEWER_ROLE = "RABOCHII_INDEPENDENT_HOSTILE_REVIEWER_OBL059_R1"
FROZEN_COMMIT = "8f209b52f81a5c1bf5ed158782f25f56153ac68e"
EXPECTED_AUTHORITY_SHA256 = "20a0bce78f290da4e47146e7a06c478d1f483133cc0a47eb8b1060bbf19a27b2"
EXPECTED_COURT_SHA256 = "2851a5407dbdc9cab71f776cd5327b6262d576da776fba4d3f6032a2306b028b"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def attack(name, mutate, expected="negative"):
    packet = fixture()
    mutate(packet)
    try:
        result = evaluate_direct_positive_applicability(packet)
    except Exception as exc:
        return {
            "name": name,
            "pass": False,
            "failure": "UNCAUGHT_EXCEPTION_INSTEAD_OF_FAIL_CLOSED",
            "exception_type": type(exc).__name__,
            "exception": str(exc),
        }

    if expected == "negative":
        ok = result.get("decision") == NEGATIVE_DECISION
    elif expected == "positive":
        ok = result.get("decision") == POSITIVE_DECISION
    else:
        raise AssertionError(expected)
    return {
        "name": name,
        "pass": ok,
        "decision": result.get("decision"),
        "reason": result.get("reason"),
        "project_current_state_created": result.get("project_current_state_created"),
    }


def main():
    here = Path(__file__).resolve().parent
    authority_hash = sha256(here / "positive_applicability_authority.py")
    court_hash = sha256(here / "governed_bounded_court.py")
    freeze_ok = authority_hash == EXPECTED_AUTHORITY_SHA256 and court_hash == EXPECTED_COURT_SHA256

    attacks = []
    attacks.append(attack("baseline_exact_noncurrent_synthetic", lambda p: None, expected="positive"))
    attacks.append(attack("missing_actor", lambda p: p.pop("actor_id")))
    attacks.append(attack("wrong_world", lambda p: p["opportunity"].__setitem__("world_id", "urn:wrong:world")))
    attacks.append(attack("wrong_time", lambda p: p["opportunity"].__setitem__("time_id", "urn:wrong:time")))
    attacks.append(attack("wrong_opportunity", lambda p: p["opportunity"].__setitem__("opportunity_id", "urn:wrong:opportunity")))
    attacks.append(attack("adp010_self_authority", lambda p: p.__setitem__(
        "claimed_positive_applicability_source",
        "V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0",
    )))
    attacks.append(attack("v554_alias", lambda p: p.__setitem__("claimed_positive_applicability_source", "V554")))
    attacks.append(attack("can001_alias", lambda p: p.__setitem__("claimed_positive_applicability_source", "CAN-001")))
    attacks.append(attack("can003_alias", lambda p: p.__setitem__("claimed_positive_applicability_source", "CAN-003")))
    attacks.append(attack("routing_alias", lambda p: p.__setitem__("claimed_positive_applicability_source", "ROUTING")))
    attacks.append(attack("stale_actor", lambda p: p["evidence"]["actor_activation"].__setitem__("stale", True)))
    attacks.append(attack("wrong_phase_actor", lambda p: p["evidence"]["developmental_phase"].__setitem__("actor_id", "urn:wrong:actor")))
    attacks.append(attack("wrong_phase_world", lambda p: p["evidence"]["developmental_phase"].__setitem__("world_id", "urn:wrong:world")))
    attacks.append(attack("wrong_phase_time", lambda p: p["evidence"]["developmental_phase"].__setitem__("time_id", "urn:wrong:time")))
    attacks.append(attack("classification_owned_by_candidate", lambda p: p["evidence"]["subject_classification"].__setitem__(
        "semantic_owner", "OBL059_FIRST_POSITIVE_OEE_DIRECT_POSITIVE_APPLICABILITY_SOURCE_AUTHORITY@R1"
    )))
    attacks.append(attack("project_current_scope", lambda p: p.__setitem__("execution_scope", "PROJECT_CURRENT")))

    # Required malformed-input attack families. A fail-closed candidate must return
    # a negative receipt rather than raise while trying to hash its rejection.
    attacks.append(attack("malformed_actor_bytes", lambda p: p.__setitem__("actor_id", b"bad-actor")))
    attacks.append(attack("malformed_world_set", lambda p: p.__setitem__("world_id", {"not", "json"})))
    attacks.append(attack("malformed_opportunity_id_object", lambda p: p.__setitem__("adp010_opportunity_id", object())))

    failures = [a for a in attacks if not a["pass"]]
    terminal = (
        "PASS__OBL059_FROZEN_CANDIDATE_RESISTED_SINGLE_FRESH_HOSTILE_REVIEW"
        if freeze_ok and not failures
        else "FAIL__OBL059_FROZEN_CANDIDATE_HOSTILE_REVIEW"
    )
    result = {
        "reviewer_role": REVIEWER_ROLE,
        "fresh_independent_review_ordinal": 1,
        "repair_authority": False,
        "frozen_commit": FROZEN_COMMIT,
        "frozen_authority_sha256": authority_hash,
        "frozen_court_sha256": court_hash,
        "freeze_identity_verified": freeze_ok,
        "attack_count": len(attacks),
        "failures": failures,
        "terminal": terminal,
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if terminal.startswith("PASS__") else 1


if __name__ == "__main__":
    raise SystemExit(main())
