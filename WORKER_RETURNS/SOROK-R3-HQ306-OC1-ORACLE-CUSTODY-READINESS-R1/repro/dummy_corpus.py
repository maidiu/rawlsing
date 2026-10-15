"""Dummy-corpus construction: fictional test-only scenarios and answer sets.

All content is entirely fictional. No real heldout answer keys or unblinded
hidden scenario content is published in the repository. Ephemeral fixture
credentials are used for TEST_ONLY signatures with a transparent verification root.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from custody_protocol import (
    CustodyCapsule,
    EscrowState,
    MockSigner,
    MockSignature,
    Person,
    Role,
    RoleAssignment,
    ScenarioCase,
    assert_no_leakage,
    detect_leakage,
    require_second_signature,
    roles_conflict,
    verify_blind_pairing,
    verify_purpose,
    EditAfterFreezeError,
    IdentityMismatchError,
    ConflictError,
    SignatureError,
    LeakageError,
    BlindIDPairingError,
    DuplicateFamilyError,
)

# ---- fictional dummy scenarios (never real heldout content) ----

DUMMY_SCENARIOS: List[Dict[str, Any]] = [
    {
        "case_id": f"CASE-{i:03d}",
        "family_id": f"FAM-{i // 3:02d}",
        "blind_id": f"BLIND-{uuid.uuid4().hex[:12]}",
        "k_label": f"K{(i % 6) + 1}",
        "facts": {
            "context": f"synthetic-lab-context-{i}",
            "description": f"Fictional test-only scenario {i}",
        },
        "lawful_answers": ["OPTION_A", "OPTION_B", "OTHER_UNSCORABLE"],
        "other_unscorable": True,
    }
    for i in range(12)
]

_TEMPLATE_SIGS = frozenset(
    hashlib.sha256(json.dumps(s["facts"], sort_keys=True).encode()).hexdigest()
    for s in DUMMY_SCENARIOS
)


def build_dummy_corpus() -> List[ScenarioCase]:
    cases = []
    for s in DUMMY_SCENARIOS:
        cases.append(ScenarioCase(
            case_id=s["case_id"],
            family_id=s["family_id"],
            blind_id=s["blind_id"],
            k_label=s["k_label"],
            facts_digest=semantic_digest(s["facts"]),
            lawful_answers=tuple(s["lawful_answers"]),
            other_unscorable=s["other_unscorable"],
            hidden_origin_digest=semantic_digest({"hidden": s["case_id"]}),
            public_projection_digest=semantic_digest({"public": s["case_id"]}),
        ))
    return cases


def semantic_digest(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()


def build_capsule(
    purpose: str,
    scenario_frame: str,
    cases: List[ScenarioCase],
    version: int = 1,
) -> CustodyCapsule:
    verify_purpose(purpose)
    content = {
        "cases": [
            {
                "case_id": c.case_id, "family_id": c.family_id,
                "blind_id": c.blind_id, "k_label": c.k_label,
                "facts_digest": c.facts_digest,
                "lawful_answers": list(c.lawful_answers),
                "other_unscorable": c.other_unscorable,
            }
            for c in cases
        ],
    }
    content_digest = semantic_digest(content)
    lawful_set = {c.case_id: list(c.lawful_answers) for c in cases}
    return CustodyCapsule(
        capsule_id=f"CAPSULE-{uuid.uuid4().hex[:12]}",
        schema_version="CUSTODY_CAPSULE@1",
        purpose=purpose,
        scenario_frame=scenario_frame,
        family_graph_digest=semantic_digest({
            "families": sorted({c.family_id for c in cases})
        }),
        content_digest=content_digest,
        contribution_digest=semantic_digest({"contributors": ["dummy_author"]}),
        public_projection_digest=semantic_digest({"public": "visible"}),
        hidden_projection_digest=semantic_digest({"hidden": "sealed"}),
        lawful_set_digest=semantic_digest(lawful_set),
        coder_rubric_digest=semantic_digest({"rubric": "deterministic_typed"}),
        split_assignment_digest=semantic_digest({"split": "dev_holdout"}),
        generation_history_digest=semantic_digest({"history": ["v1"]}),
        rejected_alternatives_digest=semantic_digest({"rejected": []}),
        freeze_timestamp=0.0,
        version=version,
    )


def build_model_visible_packet(case: ScenarioCase) -> Dict[str, Any]:
    """Build a model-visible packet WITHOUT leaking any hidden tokens."""
    packet = {
        "public_projection": {"context": f"synthetic-lab-context-{case.case_id}"},
        "menu": ["OPTION_A", "OPTION_B", "OTHER_UNSCORABLE"],
        "request_id": f"REQ-{uuid.uuid4().hex[:12]}",
    }
    assert_no_leakage(packet)
    return packet


def build_coder_input(case: ScenarioCase, response: str) -> Dict[str, Any]:
    """Build coder input WITHOUT arm, provider, expected answer or result labels."""
    return {
        "response": response,
        "schema_rubric": "deterministic_typed_v1",
        "menu": list(case.lawful_answers),
        # explicitly NO arm, provider, expected answer, or desired result
    }
