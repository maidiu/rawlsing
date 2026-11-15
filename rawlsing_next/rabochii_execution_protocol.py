"""Machine-checkable Rabochii execution-discipline contracts.

This module governs worker orchestration only.  It does not alter Rawlsing
empirical, semantic, authority, PRE-V3, V3, or V2 object semantics.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

EXECUTION_STATE_SCHEMA = "RABOCHII_EXECUTION_STATE@1.0.0"
COURT_SPEC_SCHEMA = "RABOCHII_COURT_SPEC@1.0.0"

PROFILES = frozenset({
    "DISCOVER",
    "SEMANTIC_AUTHORITY",
    "IMPLEMENT",
    "VERIFY_REGRESSION",
    "HOSTILE_AUDIT",
    "REAL_EXECUTION",
    "INTEGRATE",
    "RECOVERY_FORENSIC",
    "CLOSURE_ONLY",
    "TERMINAL",
})

CLAIM_TYPES = frozenset({
    "DETERMINISTIC_EXECUTION",
    "EXACT_IDENTITY",
    "EXISTENCE",
    "BOUNDED_ABSENCE",
    "SEMANTIC_INTERPRETATION",
    "AUTHORITY_COMPETENCE",
    "EMPIRICAL_REPLAY",
    "INDEPENDENT_AUDIT",
    "INTEGRATION_EQUIVALENCE",
})

CLAIM_STATES = frozenset({"UNKNOWN", "READY", "IN_FLIGHT", "PROVEN", "REFUTED", "BLOCKED"})
OWNER_STATES = frozenset({"PENDING", "IN_FLIGHT", "PROVEN", "REFUTED", "CANCELLED", "UNAVAILABLE"})
PROOF_MODES = frozenset({"EXACT", "SEEDED", "DISTRIBUTIONAL", "NONDETERMINISTIC_OBSERVATIONAL"})
TERMINAL_STATES = frozenset({"OPEN", "PENDING_EXTERNAL", "NEEDS_HQ_DECISION", "PASS", "BLOCKED"})
BLOCKER_CLASSES = frozenset({
    "BLOCKED_AUTHORITY",
    "BLOCKED_SEMANTIC_CONTRADICTION",
    "BLOCKED_EXECUTION_CAPABILITY",
    "BLOCKED_MATERIAL_UNAVAILABLE",
    "BLOCKED_RESOURCE",
    "BLOCKED_INTEGRATION",
    "BLOCKED_INSUFFICIENT_EVIDENCE",
})
COMPATIBILITY_STATES = frozenset({"VERIFIED", "INCOMPATIBLE", "UNVERIFIED"})
VOLATILITY = frozenset({"IMMUTABLE", "SNAPSHOT", "EVENTUALLY_CONSISTENT", "LIVE"})
RECOMPUTE_COSTS = frozenset({"LOW", "MEDIUM", "HIGH", "UNKNOWN"})
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_PYTHON_RE = re.compile(r"^3\.\d+$")
_ALLOWED_COURT_ENV = frozenset({"PYTHONHASHSEED", "PYTEST_DISABLE_PLUGIN_AUTOLOAD"})


def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and bool(_SHA_RE.fullmatch(value))


def _claims_by_id(state: Mapping[str, Any], errors: list[str]) -> dict[str, Mapping[str, Any]]:
    raw = state.get("claims")
    if not isinstance(raw, list):
        errors.append("claims must be a list")
        return {}
    result: dict[str, Mapping[str, Any]] = {}
    for index, claim in enumerate(raw):
        if not isinstance(claim, Mapping):
            errors.append(f"claims[{index}] must be an object")
            continue
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id:
            errors.append(f"claims[{index}].id must be a nonempty string")
            continue
        if claim_id in result:
            errors.append(f"duplicate claim id {claim_id}")
            continue
        result[claim_id] = claim
    return result


def validate_execution_state(state: Mapping[str, Any]) -> tuple[str, ...]:
    """Return protocol violations for one worker runtime-state object."""
    errors: list[str] = []

    if state.get("schema_id") != EXECUTION_STATE_SCHEMA:
        errors.append(f"schema_id must be {EXECUTION_STATE_SCHEMA}")

    profile = state.get("profile")
    phase = state.get("phase")
    if profile not in PROFILES:
        errors.append(f"unknown profile {profile!r}")
    if phase not in PROFILES:
        errors.append(f"unknown phase {phase!r}")

    candidate = state.get("semantic_candidate_sha")
    tip = state.get("branch_tip_sha")
    if not _is_sha(candidate):
        errors.append("semantic_candidate_sha must be a lowercase 40-hex SHA")
    if not _is_sha(tip):
        errors.append("branch_tip_sha must be a lowercase 40-hex SHA")

    evidence_sha = state.get("evidence_execution_sha")
    if evidence_sha is not None and not _is_sha(evidence_sha):
        errors.append("evidence_execution_sha must be null or a lowercase 40-hex SHA")

    transition_from = state.get("profile_transition_from")
    if transition_from is not None and transition_from != profile:
        if transition_from not in PROFILES:
            errors.append(f"unknown profile_transition_from {transition_from!r}")
        if not state.get("profile_transition_authority_ref"):
            errors.append("profile transition requires profile_transition_authority_ref")

    revision = state.get("terminal_definition_revision", 1)
    if not isinstance(revision, int) or revision < 1:
        errors.append("terminal_definition_revision must be an integer >= 1")
    elif revision > 1 and not state.get("revision_authority_ref"):
        errors.append("terminal-definition revision requires revision_authority_ref")

    claims = _claims_by_id(state, errors)
    terminal_ids = state.get("frozen_terminal_claim_ids")
    if not isinstance(terminal_ids, list) or not terminal_ids:
        errors.append("frozen_terminal_claim_ids must be a nonempty list")
        terminal_ids = []
    else:
        seen_terminal: set[str] = set()
        for claim_id in terminal_ids:
            if claim_id in seen_terminal:
                errors.append(f"duplicate terminal claim id {claim_id}")
            seen_terminal.add(claim_id)
            if claim_id not in claims:
                errors.append(f"terminal claim {claim_id!r} is not present in claims")

    all_owner_ids: set[str] = set()
    owner_states_by_claim: dict[str, list[tuple[str, str]]] = {}

    for claim_id, claim in claims.items():
        claim_type = claim.get("type")
        claim_state = claim.get("status")
        proof_mode = claim.get("proof_mode")
        required = claim.get("required_proofs")

        if claim_type not in CLAIM_TYPES:
            errors.append(f"{claim_id}: unknown claim type {claim_type!r}")
        if claim_state not in CLAIM_STATES:
            errors.append(f"{claim_id}: unknown claim status {claim_state!r}")
        if proof_mode not in PROOF_MODES:
            errors.append(f"{claim_id}: unknown proof_mode {proof_mode!r}")
        if not isinstance(required, int) or required < 1:
            errors.append(f"{claim_id}: required_proofs must be an integer >= 1")
            required = 1

        owners = claim.get("proof_owners", [])
        if not isinstance(owners, list):
            errors.append(f"{claim_id}: proof_owners must be a list")
            owners = []

        substantive = 0
        proven_compatible = 0
        owner_states_by_claim[claim_id] = []

        for index, owner in enumerate(owners):
            if not isinstance(owner, Mapping):
                errors.append(f"{claim_id}.proof_owners[{index}] must be an object")
                continue
            owner_id = owner.get("id")
            owner_state = owner.get("status")
            if not isinstance(owner_id, str) or not owner_id:
                errors.append(f"{claim_id}.proof_owners[{index}].id must be nonempty")
                continue
            if owner_id in all_owner_ids:
                errors.append(f"duplicate proof-owner id {owner_id}")
            all_owner_ids.add(owner_id)
            if owner_state not in OWNER_STATES:
                errors.append(f"{claim_id}/{owner_id}: unknown owner status {owner_state!r}")
                continue

            owner_states_by_claim[claim_id].append((owner_id, owner_state))
            if owner_state in {"PENDING", "IN_FLIGHT", "PROVEN"}:
                substantive += 1

            subject_sha = owner.get("subject_sha")
            if subject_sha is not None and not _is_sha(subject_sha):
                errors.append(f"{claim_id}/{owner_id}: subject_sha must be a lowercase 40-hex SHA")

            compatibility = owner.get("compatibility", "UNVERIFIED")
            if compatibility not in COMPATIBILITY_STATES:
                errors.append(f"{claim_id}/{owner_id}: unknown compatibility {compatibility!r}")

            volatility = owner.get("volatility", "IMMUTABLE")
            if volatility not in VOLATILITY:
                errors.append(f"{claim_id}/{owner_id}: unknown volatility {volatility!r}")

            if owner_state == "PROVEN":
                if compatibility != "VERIFIED":
                    errors.append(f"{claim_id}/{owner_id}: PROVEN owner requires VERIFIED compatibility")
                else:
                    proven_compatible += 1
                if _is_sha(candidate) and subject_sha and subject_sha != candidate:
                    if owner.get("relevant_tree_equivalent") is not True:
                        errors.append(
                            f"{claim_id}/{owner_id}: evidence on a non-candidate SHA requires "
                            "relevant_tree_equivalent=true"
                        )

        if substantive > required and not bool(claim.get("allow_extra_independent_proofs", False)):
            errors.append(
                f"{claim_id}: {substantive} live/proven proof owners exceed required_proofs={required}; "
                "duplicate execution requires explicit independent-proof authority"
            )

        if claim_state == "PROVEN" and proven_compatible < required:
            errors.append(
                f"{claim_id}: claim is PROVEN but only {proven_compatible} compatible proof owners "
                f"satisfy required_proofs={required}"
            )
        if claim_state == "IN_FLIGHT" and not any(
            owner_state in {"PENDING", "IN_FLIGHT"}
            for _, owner_state in owner_states_by_claim[claim_id]
        ):
            errors.append(f"{claim_id}: IN_FLIGHT claim requires a PENDING or IN_FLIGHT proof owner")

    terminal_claims = [claims[cid] for cid in terminal_ids if cid in claims]
    all_terminal_proven = bool(terminal_claims) and all(
        claim.get("status") == "PROVEN" for claim in terminal_claims
    )

    if all_terminal_proven and phase not in {"CLOSURE_ONLY", "TERMINAL"}:
        errors.append("all terminal claims are PROVEN; phase must be CLOSURE_ONLY or TERMINAL")

    action = state.get("current_action")
    if phase not in {"CLOSURE_ONLY", "TERMINAL"}:
        if not isinstance(action, Mapping):
            errors.append("non-closure phase requires current_action")
        else:
            advances = action.get("advances_claim_id")
            if advances not in claims:
                errors.append("current_action must name an existing advances_claim_id")
            elif claims[advances].get("status") == "PROVEN":
                errors.append("current_action may not reopen an already PROVEN claim")
    elif phase == "CLOSURE_ONLY" and isinstance(action, Mapping):
        advances = action.get("advances_claim_id")
        if advances is not None:
            errors.append("CLOSURE_ONLY action may not advance/reopen a substantive claim")

    terminal = state.get("terminal")
    if not isinstance(terminal, Mapping):
        errors.append("terminal must be an object")
        terminal = {}
    terminal_state = terminal.get("status")
    if terminal_state not in TERMINAL_STATES:
        errors.append(f"unknown terminal status {terminal_state!r}")

    if terminal_state == "PASS":
        if phase != "TERMINAL":
            errors.append("PASS requires phase TERMINAL")
        if not all_terminal_proven:
            errors.append("PASS requires every frozen terminal claim to be PROVEN")

    if terminal_state == "PENDING_EXTERNAL":
        if not any(
            claim.get("status") == "IN_FLIGHT" for claim in terminal_claims
        ):
            errors.append("PENDING_EXTERNAL requires an IN_FLIGHT terminal claim")

    if terminal_state == "BLOCKED":
        blocker_class = terminal.get("blocker_class")
        if blocker_class not in BLOCKER_CLASSES:
            errors.append("BLOCKED requires a recognized blocker_class")
        blocking_ids = terminal.get("blocking_claim_ids")
        if not isinstance(blocking_ids, list) or not blocking_ids:
            errors.append("BLOCKED requires nonempty blocking_claim_ids")
            blocking_ids = []
        fresh = state.get("fresh_state")
        if not isinstance(fresh, Mapping) or fresh.get("checked") is not True:
            errors.append("BLOCKED requires fresh_state.checked=true")
            fresh = {}
        if fresh.get("branch_tip_sha") != tip:
            errors.append("BLOCKED requires fresh_state.branch_tip_sha equal to current branch_tip_sha")
        observed = set(fresh.get("observed_proof_owner_ids", []) or [])
        for claim_id in blocking_ids:
            if claim_id not in claims:
                errors.append(f"blocking claim {claim_id!r} is unknown")
                continue
            for owner_id, owner_state in owner_states_by_claim.get(claim_id, []):
                if owner_id not in observed:
                    errors.append(f"BLOCKED fresh-state gate did not refresh proof owner {owner_id}")
                if owner_state in {"PENDING", "IN_FLIGHT"}:
                    errors.append(
                        f"BLOCKED claim {claim_id} still has active proof owner {owner_id}; "
                        "use PENDING_EXTERNAL or refresh/resolve the owner"
                    )

    checkpoint = state.get("checkpoint_state")
    if profile == "REAL_EXECUTION" or phase == "REAL_EXECUTION":
        if not isinstance(checkpoint, Mapping):
            errors.append("REAL_EXECUTION requires checkpoint_state")
        else:
            if checkpoint.get("mode") != "WRITE_AHEAD":
                errors.append("REAL_EXECUTION checkpoint_state.mode must be WRITE_AHEAD")
            pending = checkpoint.get("volatile_result_pending")
            if not isinstance(pending, bool):
                errors.append("checkpoint_state.volatile_result_pending must be boolean")
                pending = False
            recompute_cost = checkpoint.get("recompute_cost")
            if recompute_cost not in RECOMPUTE_COSTS:
                errors.append(f"unknown checkpoint recompute_cost {recompute_cost!r}")
            durable_ref = checkpoint.get("durable_checkpoint_ref")
            if durable_ref is not None and (not isinstance(durable_ref, str) or not durable_ref):
                errors.append("durable_checkpoint_ref must be null or a nonempty string")
            if pending:
                if durable_ref is not None:
                    errors.append("volatile_result_pending cannot coexist with durable_checkpoint_ref")
                if not isinstance(action, Mapping) or action.get("kind") != "PERSIST_CHECKPOINT":
                    errors.append(
                        "volatile REAL_EXECUTION result is pending; next legal action must be PERSIST_CHECKPOINT"
                    )

    envelope = state.get("mutation_envelope")
    if profile in {"IMPLEMENT", "INTEGRATE"} and not isinstance(envelope, Mapping):
        errors.append(f"{profile} requires mutation_envelope")

    return tuple(errors)


def validate_court_spec(spec: Mapping[str, Any]) -> tuple[str, ...]:
    """Validate the bounded, non-shell court specification consumed by CI."""
    errors: list[str] = []
    if spec.get("schema_id") != COURT_SPEC_SCHEMA:
        errors.append(f"schema_id must be {COURT_SPEC_SCHEMA}")

    candidate = spec.get("semantic_candidate_sha")
    if not _is_sha(candidate):
        errors.append("semantic_candidate_sha must be a lowercase 40-hex SHA")

    version = spec.get("python_version")
    if not isinstance(version, str) or not _PYTHON_RE.fullmatch(version):
        errors.append("python_version must look like 3.N")

    tests = spec.get("tests")
    if not isinstance(tests, list) or not tests:
        errors.append("tests must be a nonempty list")
        tests = []
    for index, value in enumerate(tests):
        if not isinstance(value, str):
            errors.append(f"tests[{index}] must be a string")
            continue
        path = Path(value)
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"tests[{index}] must be a safe relative path")
        if not value.startswith("rawlsing_next/tests/") or not value.endswith(".py"):
            errors.append(f"tests[{index}] must be a rawlsing_next/tests/*.py path")

    env = spec.get("env", {})
    if not isinstance(env, Mapping):
        errors.append("env must be an object")
    else:
        for key, value in env.items():
            if key not in _ALLOWED_COURT_ENV:
                errors.append(f"court env key {key!r} is not allowed")
            if not isinstance(value, str):
                errors.append(f"court env value for {key!r} must be a string")

    mode = spec.get("determinism_mode", "EXACT")
    if mode not in PROOF_MODES:
        errors.append(f"unknown determinism_mode {mode!r}")

    return tuple(errors)


def _load(path: str) -> Mapping[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, Mapping):
        raise ValueError("top-level JSON value must be an object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=("state", "court"))
    parser.add_argument("path")
    args = parser.parse_args(argv)

    value = _load(args.path)
    errors = (
        validate_execution_state(value)
        if args.kind == "state"
        else validate_court_spec(value)
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 2
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
