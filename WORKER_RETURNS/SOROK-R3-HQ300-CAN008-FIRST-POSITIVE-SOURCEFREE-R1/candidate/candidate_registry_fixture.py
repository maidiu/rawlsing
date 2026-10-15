"""HQ300 — WORKER CANDIDATE REGISTRY FIXTURE.

###############################################################################
## THIS IS NOT ACCEPTED AUTHORIZATION.                                       ##
##                                                                           ##
## This registry is a WORKER-LOCAL FIXTURE used only to exercise the          ##
## candidate positive chain in isolated sourcefree terrain. It is NOT the     ##
## production positive-transition-authority registry of                       ##
## rawlsing_next/v3_psepf_zero_positive_guard.py. That registry is EMPTY by   ##
## design and MUST REMAIN EMPTY; the imported guard must continue to DENY     ##
## every production positive transition.                                     ##
##                                                                           ##
## Changing the imported guard, or granting real owner positive authority,    ##
## is FORBIDDEN by commission and is NOT done anywhere in this package.       ##
###############################################################################
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

FIXTURE_ID = "WORKER_CANDIDATE_REGISTRY_FIXTURE"
FIXTURE_VERSION = "1.0.0"
FIXTURE_GRAIN = "SOURCEFREE_CANDIDATE_FIXTURE__NOT_ACCEPTED_AUTHORIZATION"
PRODUCTION_REGISTRY_UNTOUCHED = True


@dataclass(frozen=True)
class CandidateRuleRegistration:
    rule_id: str
    rule_version: str
    rule_content_hash: str
    issuer_authority_id: str
    issuer_authority_version: str
    actor_scope: str
    temporal_scope: str
    effect_kinds: Tuple[str, ...]
    target_owner_kind: str
    admission_state: str  # CANDIDATE_ADMITTED_IN_FIXTURE | REJECTED


class CandidateRegistryFixture:
    """Deterministic in-memory candidate registry. No production side effects."""

    def __init__(self) -> None:
        self._rules: Dict[str, CandidateRuleRegistration] = {}
        self._admissions: List[Dict[str, Any]] = []

    def register(self, reg: CandidateRuleRegistration) -> Dict[str, Any]:
        if reg.admission_state != "CANDIDATE_ADMITTED_IN_FIXTURE":
            return {"status": "REFUSED", "code": "REGISTRATION_NOT_ADMITTED"}
        if reg.target_owner_kind not in ("ADP016", "ADP017", "CAN008_CURRENT"):
            return {"status": "REFUSED", "code": "UNKNOWN_TARGET_OWNER_KIND"}
        key = f"{reg.rule_id}@{reg.rule_version}"
        if key in self._rules:
            return {"status": "REFUSED", "code": "DUPLICATE_RULE_REGISTRATION"}
        self._rules[key] = reg
        receipt = {
            "status": "CANDIDATE_REGISTERED_IN_FIXTURE",
            "rule_key": key,
            "fixture_id": FIXTURE_ID,
            "fixture_grain": FIXTURE_GRAIN,
            "production_registry_mutated": False,
        }
        self._admissions.append(receipt)
        return receipt

    def lookup(self, rule_id: str, rule_version: str) -> Optional[CandidateRuleRegistration]:
        return self._rules.get(f"{rule_id}@{rule_version}")

    def admit_event_identity(self, event_id: str, event_hash: str,
                             issuer_authority_id: str) -> Dict[str, Any]:
        """Candidate-side event-identity custody. Duplicate identity refused."""
        for a in self._admissions:
            if a.get("event_id") == event_id and a.get("kind") == "EVENT_IDENTITY":
                return {"status": "REFUSED", "code": "BLOCK_DUPLICATE_EVENT_IDENTITY",
                        "event_id": event_id}
        rec = {"kind": "EVENT_IDENTITY", "event_id": event_id, "event_hash": event_hash,
               "issuer_authority_id": issuer_authority_id,
               "status": "EVENT_IDENTITY_ADMITTED_IN_FIXTURE"}
        self._admissions.append(rec)
        return rec

    def ledger(self) -> List[Dict[str, Any]]:
        return list(self._admissions)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "fixture_id": FIXTURE_ID,
            "fixture_version": FIXTURE_VERSION,
            "fixture_grain": FIXTURE_GRAIN,
            "production_registry_untoched": PRODUCTION_REGISTRY_UNTOUCHED,
            "registered_rules": [f"{r.rule_id}@{r.rule_version}" for r in self._rules.values()],
            "ledger": self._admissions,
        }


# The singleton fixture used by the candidate chain in this package.
CANDIDATE_REGISTRY = CandidateRegistryFixture()
