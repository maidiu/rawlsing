"""M03 finite selector custody and read-time validation; no response selection.

This validates the existing TEST_ONLY M01 first-event/claim contract. It neither
issues an owner grant nor implements a new memory-to-belief mechanism.
"""

import json
from dataclasses import asdict
from candidate import can008_candidate_rule as rule, owner_transitions as owner
from candidate.candidate_registry_fixture import canon, digest, parse_time

SCHEMA = "M03_CANONICAL_CLAIM_SELECTION@1"


def require(ok, code):
    from cell import Refusal

    if not ok:
        raise Refusal(code)


def source_basis(c):
    from cell import events, RULE_ID, VERSION

    first, _ = events()
    c.verify_grant()
    require(c.e1 == first and c.reg.verify_event(first), "CLAIM_SOURCE_EVENT_BINDING")
    require(
        c.ctx.verify() and c.ctx.actor_id == first.actor_scope,
        "CLAIM_CONTEXT_INTEGRITY",
    )
    expected_rule = rule.build_default_binding()
    require(c.binding == expected_rule, "CLAIM_RULE_BINDING")
    claim = owner.canonical_claim(
        first.actor_scope,
        "FIXTURE_PRIVATE_FEEDBACK_APPRAISAL",
        "RESPECTED",
        first.effective_causal_time,
        first.actor_scope,
        [first.event_id],
    )
    require(
        c.ctx.claims.get(claim["claim_id"]) == claim, "CLAIM_CANONICAL_SOURCE_BINDING"
    )
    receipt = c.first_receipt
    require(isinstance(receipt, dict), "CLAIM_FIRST_RESPONSE_MISSING")
    require(
        receipt.get("receipt_hash")
        == rule._sha(
            rule._canon({k: v for k, v in receipt.items() if k != "receipt_hash"})
        ),
        "CLAIM_FIRST_RESPONSE_INTEGRITY",
    )
    expected_event = {
        k: getattr(first, k)
        for k in (
            "event_id",
            "event_hash",
            "issuer_authority_id",
            "issuer_authority_version",
            "actor_scope",
            "world_ref",
            "world_as_of",
            "effective_causal_time",
        )
    }
    expected_event["role"] = "PRECIPITATING_EVENT_STREAM"
    require(
        receipt.get("precipitating_event") == expected_event,
        "CLAIM_FIRST_RESPONSE_SOURCE",
    )
    require(
        (
            receipt.get("rule_id"),
            receipt.get("rule_version"),
            receipt.get("rule_content_hash"),
        )
        == (
            expected_rule.rule_id,
            expected_rule.rule_version,
            expected_rule.rule_content_hash,
        ),
        "CLAIM_FIRST_RESPONSE_RULE",
    )
    return dict(
        schema=SCHEMA,
        canonical_claim_ref=claim["claim_id"],
        canonical_claim_hash=claim["canonical_content_hash"],
        actor=first.actor_scope,
        world_ref=first.world_ref,
        world_as_of=first.world_as_of,
        source_event=asdict(first),
        owning_rule_id=expected_rule.rule_id,
        owning_rule_version=expected_rule.rule_version,
        owning_rule_hash=expected_rule.rule_content_hash,
        response_rule_id=RULE_ID,
        response_rule_version=VERSION,
        response_source_hash=c.grant,
        first_response_receipt_hash=receipt["receipt_hash"],
    )


def committed_binding(c):
    basis = source_basis(c)
    entries = c.journal.read_effects("FIRST_EVENT_COMPLETE")
    require(len(entries) == 1, "CLAIM_FIRST_COMMIT_REQUIRED")
    entry = entries[0]
    payload = entry["payload"]
    require(
        canon(payload.get("claim_selection_basis")) == canon(basis),
        "CLAIM_FIRST_COMMIT_SELECTION_BINDING",
    )
    require(
        payload["source_rule"] == c.grant
        and payload["state_hash"] == digest(payload["state"]),
        "CLAIM_FIRST_COMMIT_INTEGRITY",
    )
    require(
        entry["effective_causal_time"] == c.e1.effective_causal_time
        and entry["causal_parent_refs"] == [c.e1.event_id],
        "CLAIM_FIRST_COMMIT_TIME_SOURCE",
    )
    require(
        payload["state"]["claims"].get(basis["canonical_claim_ref"])
        == c.ctx.claims[basis["canonical_claim_ref"]],
        "CLAIM_FIRST_COMMIT_CANONICAL_STATE",
    )
    return dict(
        schema=SCHEMA,
        basis=basis,
        first_event_entry_hash=entry["entry_hash"],
        first_owner_state_hash=payload["state_hash"],
    )


def validate_journaled_transition_ancestry(c, consumed_transitions=None):
    """Require journaled ancestry and, when given, coverage of consumed transitions."""
    entries = c.journal.read_effects("ADP017_COMMIT")
    transitions = list(c.ctx.epistemic_transitions)
    journaled = []
    for entry in entries:
        payload = entry.get("payload") or {}
        result = payload.get("result") or {}
        recorded = result.get("transition") or {}
        transition_id = recorded.get("transition_id")
        matches = [
            t for t in transitions if t.get("transition_id") == transition_id
        ]
        require(len(matches) == 1, "CLAIM_TRANSITION_ANCESTRY_MISSING")
        transition = matches[0]
        require(
            transition.get("pre_state_hash") == payload.get("before"),
            "CLAIM_TRANSITION_PRESTATE_ANCESTRY",
        )
        require(
            transition.get("post_state_set_hash")
            == recorded.get("post_state_set_hash"),
            "CLAIM_TRANSITION_POSTSTATE_ANCESTRY",
        )
        journaled.append(transition_id)
    require(
        len(journaled) == len(set(journaled)),
        "CLAIM_TRANSITION_JOURNAL_DUPLICATE",
    )
    if consumed_transitions is not None:
        for transition in consumed_transitions:
            require(
                transition.get("transition_id") in set(journaled),
                "CLAIM_TRANSITION_UNJOURNALED",
            )


def validate_binding(c):
    """Validate preserved commitment, not the untrusted outer selector hint."""
    from cell import Refusal

    try:
        if c._claim_selection_binding_json is None:
            require(
                c.claim_id is None
                and c.first_receipt is None
                and c.ctx.verify()
                and not c.ctx.claims
                and not c.ctx.memories
                and not c.reg._events
                and not c.journal.entries
                and not c.history.entries,
                "CLAIM_SELECTION_BINDING_MISSING",
            )
            return None
        require(
            isinstance(c._claim_selection_binding_json, str),
            "CLAIM_SELECTION_BINDING_TYPE",
        )
        binding = json.loads(c._claim_selection_binding_json)
        expected = committed_binding(c)
        require(canon(binding) == canon(expected), "CLAIM_SELECTION_CHECKPOINT_BINDING")
        validate_journaled_transition_ancestry(c)
        return expected
    except Refusal:
        raise
    except (ValueError, TypeError, KeyError, AttributeError):
        raise Refusal("CLAIM_SELECTION_BINDING_MALFORMED") from None


def bind_committed(c):
    c._claim_selection_binding_json = canon(committed_binding(c))


def effect_provenance(c, effect, transition, cut, selected):
    require(
        parse_time(effect["effective_causal_time"]) <= cut,
        "CLAIM_EFFECT_AFTER_RESPONSE",
    )
    require(
        effect["effective_causal_time"] == c.e1.effective_causal_time,
        "CLAIM_EFFECT_SOURCE_TIME",
    )
    require(
        effect["actor_id"] == c.ctx.actor_id and effect["claim_ref"] == selected,
        "CLAIM_EFFECT_ACTOR_SCOPE",
    )
    require(
        (
            effect["owning_rule_id"],
            effect["owning_rule_version"],
            effect["owning_rule_hash"],
        )
        == (c.binding.rule_id, c.binding.rule_version, c.binding.rule_content_hash),
        "CLAIM_EFFECT_RULE",
    )
    require(
        tuple(effect["causal_parent_refs"]) == (c.e1.event_id,)
        and tuple(effect["actor_facing_basis_refs"])
        == (c.e1.event_id + ":" + c.e1.event_hash,),
        "CLAIM_EFFECT_SOURCE_BASIS",
    )
    require(
        transition["effect"] == effect
        and transition["actor_id"] == c.ctx.actor_id
        and transition["authority_hash"] == owner.PINS["ADP017_JSON"],
        "CLAIM_EFFECT_TRANSITION_BINDING",
    )
    fields = {k: v for k, v in effect.items() if k != "effect_id"}
    require(
        effect["effect_id"]
        == digest(
            [
                "EPISTEMIC_EFFECT",
                fields,
                transition["pre_state_hash"],
                transition["target_record_ref"],
            ]
        ),
        "CLAIM_EFFECT_IDENTITY",
    )
    original_record = {
        k: v
        for k, v in transition.items()
        if k not in ("transition_id", "post_state_set_hash")
    }
    require(
        transition["transition_id"] == digest(original_record),
        "CLAIM_TRANSITION_IDENTITY",
    )
    for parent in effect["causal_parent_refs"]:
        event = c.reg.event(parent)
        require(
            event is not None and parse_time(event["effective_causal_time"]) <= cut,
            "CLAIM_PARENT_AFTER_RESPONSE_OR_MISSING",
        )
    return dict(
        effect_id=effect["effect_id"],
        transition_id=transition["transition_id"],
        effective_causal_time=effect["effective_causal_time"],
    )


def validate_consumption(c, at):
    """Read actual selected claim/effects/permission at the response cut."""
    from cell import Refusal

    try:
        binding = validate_binding(c)
        require(binding is not None, "CLAIM_SELECTION_NOT_COMMITTED")
        cut = parse_time(at)
        require(
            parse_time("1998-01-01T00:00:00Z")
            <= cut
            < parse_time("2001-01-01T00:00:00Z"),
            "CLAIM_RESPONSE_OUTSIDE_RULE_SCOPE",
        )
        selected = c.claim_id
        claim = c.ctx.claims.get(selected)
        require(claim is not None, "CLAIM_SELECTION_UNKNOWN")
        require(owner.verify_claim(claim), "CLAIM_SELECTION_CANONICAL_INTEGRITY")
        require(
            parse_time(claim["temporal_scope"]) <= cut, "CLAIM_SELECTION_AFTER_RESPONSE"
        )
        require(
            selected == binding["basis"]["canonical_claim_ref"],
            "CLAIM_SELECTION_SOURCE_SCOPE",
        )
        grant = c.ctx.emissions.get(selected)
        require(
            grant is not None
            and grant["event_id"] == c.e1.event_id
            and grant["event_hash"] == c.e1.event_hash
            and grant["rule_hash"] == c.binding.rule_content_hash
            and grant["stance_kind"] == "BELIEF",
            "CLAIM_EMISSION_SOURCE_BINDING",
        )
        active = [
            (k, v) for k, v in c.ctx.stances.items() if v["claim_ref"] == selected
        ]
        snapshot = c.ctx.state_sets.get(selected)
        permission = c.ctx.permissions.get(selected)
        transitions = [
            t
            for t in c.ctx.epistemic_transitions
            if t["effect"]["claim_ref"] == selected
        ]
        if (
            transitions
            and snapshot is not None
            and snapshot.get("current_claim_accessibility") == "CLAIM_ACCESSIBLE"
            and active
        ):
            terminal = transitions[-1]
            journal_entries = [
                e
                for e in c.journal.read_effects("ADP017_COMMIT")
                if (
                    ((e.get("payload") or {}).get("result") or {})
                    .get("transition", {})
                    .get("effect", {})
                    .get("claim_ref")
                    == selected
                )
            ]
            journaled_ids = [
                ((e.get("payload") or {}).get("result") or {})
                .get("transition", {})
                .get("transition_id")
                for e in journal_entries
            ]
            if terminal.get("transition_id") not in journaled_ids:
                require(
                    terminal.get("effect", {}).get("stance_operation")
                    != "SUPERSEDE_EXACT_RECORD",
                    "CLAIM_TRANSITION_UNJOURNALED",
                )
                if journal_entries:
                    require(
                        terminal.get("pre_state_hash")
                        == (journal_entries[-1].get("payload") or {}).get("after"),
                        "CLAIM_TRANSITION_PRESTATE_ANCESTRY",
                    )
        proofs = []
        if snapshot is None:
            require(
                not active and not transitions and permission is None,
                "CLAIM_STATE_MATERIAL_MISSING",
            )
            disposition = "BOUND_CANONICAL_CLAIM_NO_APPLIED_STANCE"
        else:
            require(
                snapshot["actor_id"] == c.ctx.actor_id
                and snapshot["claim_id"] == selected,
                "CLAIM_SNAPSHOT_ACTOR_SCOPE",
            )
            require(
                snapshot["current_state_hash"]
                == digest(
                    {k: v for k, v in snapshot.items() if k != "current_state_hash"}
                ),
                "CLAIM_SNAPSHOT_INTEGRITY",
            )
            require(
                tuple(snapshot["accessibility_basis_refs"])
                == (c.e1.event_id + ":" + c.e1.event_hash,),
                "CLAIM_ACCESS_SOURCE_BINDING",
            )
            require(
                transitions
                and snapshot["last_transition_ref"]
                == transitions[-1]["transition_id"],
                "CLAIM_LAST_TRANSITION_TERMINAL",
            )
            require(
                snapshot["current_state_hash"]
                == transitions[-1]["post_state_set_hash"],
                "CLAIM_LAST_TRANSITION_STATE",
            )
            require(
                permission is not None
                and permission["actor_id"] == c.ctx.actor_id
                and permission["claim_id"] == selected
                and permission["epistemic_state_hash"] == snapshot["current_state_hash"]
                and tuple(permission["basis_refs"])
                == (c.e1.event_id + ":" + c.e1.event_hash,),
                "CLAIM_CURRENT_PERMISSION_BINDING",
            )
            expected_permission = owner.first_person_permission(
                "BELIEF" if active else None, snapshot["current_claim_accessibility"]
            )
            require(
                permission["permission"] == expected_permission,
                "CLAIM_CURRENT_PERMISSION_VALUE",
            )
            require(
                len({v["effect_id"] for k, v in active}) == len(active)
                and all(k == v["effect_id"] for k, v in active),
                "CLAIM_DUPLICATE_EFFECT",
            )
            for key, effect in active:
                matches = [
                    t
                    for t in transitions
                    if t["effect"]["effect_id"] == effect["effect_id"]
                ]
                require(len(matches) == 1, "CLAIM_EFFECT_TRANSITION_REQUIRED")
                proofs.append(effect_provenance(c, effect, matches[0], cut, selected))
            last = [
                t
                for t in transitions
                if t["transition_id"] == snapshot["last_transition_ref"]
            ]
            require(
                len(last) == 1
                and last[0]["post_state_set_hash"] == snapshot["current_state_hash"],
                "CLAIM_LAST_TRANSITION_BINDING",
            )
            last_proof = effect_provenance(c, last[0]["effect"], last[0], cut, selected)
            if last_proof not in proofs:
                proofs.append(last_proof)
            disposition = "BOUND_CANONICAL_CLAIM_WITH_NATIVE_STATE"
        return dict(
            schema=SCHEMA,
            verified_binding=binding,
            selected_claim_ref=selected,
            response_as_of=at,
            canonical_claim_time=claim["temporal_scope"],
            actual_effect_provenance=proofs,
            disposition=disposition,
            production_authority="NOT_ISSUED_TEST_ONLY",
        )
    except Refusal:
        raise
    except (ValueError, TypeError, KeyError, AttributeError):
        raise Refusal("CLAIM_CONSUMPTION_PROVENANCE_MALFORMED") from None
